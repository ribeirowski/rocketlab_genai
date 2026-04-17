import logging

from app.services.guardrail_service import GuardrailService
from app.exceptions import UnsafeSQLException
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
        sql = self.llm.generate_sql(question, schema)
        
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
        except Exception as e:
            self.history.save(
                question_id=question_id,
                generated_sql=sql,
                row_count=0,
                success=False,
                error=str(e),
            )
            raise