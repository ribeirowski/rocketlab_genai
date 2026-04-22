import logging

from app.services.guardrail_service import GuardrailService
from app.exceptions import UnsafeSQLException, GuardrailException, SQLGenerationException, DatabaseQueryException
from app.repositories.database_repository import DatabaseRepository
from app.repositories.history_repository import HistoryRepository
from app.repositories.question_repository import QuestionRepository
from app.services.gemini_service import GeminiService
from app.schemas.agent import QueryResponse

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self, db_repo: DatabaseRepository, llm: GeminiService):
        self.db_repo = db_repo
        self.llm = llm
        self.guardrail = GuardrailService(llm)
        self.history = HistoryRepository()
        self.questions = QuestionRepository()

    def run(self, question: str) -> QueryResponse:
        logger.info("Question received: %s", question)
        
        self.guardrail.validate(question)

        schema = self.db_repo.get_schema()
        # Append an explicit list of available tables to the schema so the LLM uses the correct names
        try:
            tables = self.db_repo.get_tables()
            tables_line = "\n\nTabelas disponíveis: " + ", ".join(tables)
        except Exception:
            tables_line = ""
        schema_with_tables = schema + tables_line + "\nNÃO use tabelas que não existam no banco."

        sql = self.llm.generate_sql(question, schema_with_tables)
        # Prevent generated SQL from targeting internal/audit tables
        hidden_tables = {"questions", "query_history", "feedback"}
        sql_lower = sql.lower()
        for t in hidden_tables:
            if f" {t} " in f" {sql_lower} " or f".{t}" in sql_lower:
                raise GuardrailException(
                    "Generated SQL references internal tables which should not be queried directly."
                )
        
        self.guardrail.validate_sql(sql)

        if not self.db_repo.is_safe_sql(sql):
            raise UnsafeSQLException(sql)
        
        question_id = self.questions.get_or_create(question)

        try:
            data = self.db_repo.execute_read_query(sql)
            analysis = self.llm.generate_analysis(question, sql, data)

            self.history.save(
                question_id=question_id,
                generated_sql=sql,
                analysis=analysis,
                row_count=len(data),
                success=True,
            )

            logger.info("Response generated: %d records", len(data))

            return QueryResponse(
                question_id=question_id,
                question=question,
                sql=sql,
                data=data,
                analysis=analysis,
                row_count=len(data),
            )
        except DatabaseQueryException as e:
            # If execution failed because a table does not exist, attempt a single automatic retry
            msg = str(e)
            if "no such table" in msg.lower():
                # build hint with available tables and retry SQL generation once
                try:
                    available = self.db_repo.get_tables()
                except Exception:
                    available = []

                schema_hint = schema + "\n\n-- AVISO: Tabelas disponíveis: " + ", ".join(available)
                schema_hint += "\n-- NÃO gere SQL usando tabelas que não existam."

                try:
                    new_sql = self.llm.generate_sql(question, schema_hint)
                except Exception as gen_err:
                    # Generation failed on retry; raise a SQLGenerationException with details
                    raise SQLGenerationException(
                        f"SQL generation retry failed after missing-table error. Original DB error: {msg}. Generation error: {gen_err}"
                    ) from gen_err

                # if new_sql equals old sql, abort
                if new_sql.strip().lower() == sql.strip().lower():
                    raise SQLGenerationException(
                        f"Generated SQL references non-existent table and automatic retry produced same SQL. Details: {msg}"
                    ) from e

                # Try executing the new SQL once
                try:
                    data = self.db_repo.execute_read_query(new_sql)
                    analysis = self.llm.generate_analysis(question, new_sql, data)
                    self.history.save(
                        question_id=question_id,
                        generated_sql=new_sql,
                        analysis=analysis,
                        row_count=len(data),
                        success=True,
                    )
                    return QueryResponse(
                        question_id=question_id,
                        question=question,
                        sql=new_sql,
                        data=data,
                        analysis=analysis,
                        row_count=len(data),
                    )
                except DatabaseQueryException as exec_err:
                    # still failing: raise a clear SQLGenerationException with available tables
                    raise SQLGenerationException(
                        f"Generated SQL references tables that do not exist. DB error: {exec_err}. Tabelas disponíveis: {available}"
                    ) from exec_err
            # Otherwise re-raise the original database error
            raise
        except Exception as e:
            self.history.save(
                question_id=question_id,
                generated_sql=sql,
                row_count=0,
                success=False,
                error=str(e),
            )
            raise