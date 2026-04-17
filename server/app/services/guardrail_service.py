import re
import logging

from app.services.gemini_service import GeminiService
from app.exceptions import GuardrailException

logger = logging.getLogger(__name__)

DOMAIN_KEYWORDS = re.compile(
    r"\b(produtos?|vendas?|pedidos?|consumidores?|clientes?|vendedores?|"
    r"entregas?|avalia[çc][õo]es|avalia[çc][aã]o|"
    r"receita|categoria|estado|frete|prazo|estoque|ticket|status|rating|"
    r"lucro|quantidade|ranking|top|mais vendidos?|atraso|satisfa[çc][aã]o)\b",
    re.IGNORECASE,
)

INJECTION_PATTERNS = re.compile(
    r"(ignore\s+(all\s+)?previous|forget\s+instructions|você\s+é\s+agora|"
    r"DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO|UPDATE\s+\w+\s+SET|"
    r"ALTER\s+TABLE|TRUNCATE|--\s*bypass|;.*(DROP|DELETE|INSERT|UPDATE))",
    re.IGNORECASE,
)

FORBIDDEN_SQL_KEYWORDS = re.compile(
    r"\b(DROP|DELETE|INSERT|UPDATE|ALTER|TRUNCATE|GRANT|REVOKE|ATTACH|DETACH)\b",
    re.IGNORECASE,
)

MAX_QUESTION_LENGTH = 500

class GuardrailService:
    def __init__(self, llm_service: GeminiService):
        self.llm = llm_service

    def validate(self, question: str) -> None:
        self._check_length(question)
        self._check_injection(question)
        self._check_relevance_llm(question)

    def validate_sql(self, sql: str) -> None:
        if FORBIDDEN_SQL_KEYWORDS.search(sql):
            logger.warning("SQL blocked by guardrails: %s", sql)
            raise GuardrailException("SQL generated contains operations not allowed.")

    def _check_length(self, question: str) -> None:
        if not question or not question.strip():
            raise GuardrailException("Question cannot be empty.")
        if len(question) > MAX_QUESTION_LENGTH:
            raise GuardrailException(
                f"Question too long. Limit: {MAX_QUESTION_LENGTH} characters."
            )

    def _check_injection(self, question: str) -> None:
        if INJECTION_PATTERNS.search(question):
            logger.warning("Injection attempt detected: %s", question)
            raise GuardrailException(
                "Invalid question. Please ask a question about e-commerce data."
            )

    def _check_relevance_llm(self, question: str) -> None:
        if DOMAIN_KEYWORDS.search(question):
            return

        system = (
            "Você é um validador de perguntas para um sistema de análise de e-commerce. "
            "Responda APENAS com 'SIM' se a pergunta for sobre vendas, produtos, pedidos, "
            "consumidores, vendedores, entregas, avaliações ou dados do e-commerce. "
            "Responda APENAS com 'NÃO' para qualquer outro assunto."
        )
        prompt = f"A pergunta abaixo é sobre dados de e-commerce?\nPergunta: {question}\nResposta:"

        try:
            result = self.llm._call(system, prompt)
            if "NÃO" in result.upper() or "NAO" in result.upper():
                logger.info("Question outside the domain blocked: %s", question)
                raise GuardrailException(
                    "Only able to answer questions about e-commerce data "
                    "(sales, products, orders, consumers, etc.)."
                )
        except GuardrailException:
            raise
        except Exception as e:
            logger.warning("Guardrail LLM failed, allowing question: %s", e)