import re
import time
import logging

from google import genai
from google.genai import types

from app.config import get_settings
from app.exceptions import SQLGenerationException, RateLimitException

logger = logging.getLogger(__name__)

PLURAL_KEYWORDS = r"\b(produtos|vendedores|categorias|itens|clientes|pedidos|estados|regiões|cidades)\b"

class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL
        
    def _call(self, system_instruction: str, prompt: str) -> str:
        # Simple retry/backoff for transient errors (including 429)
        max_retries = 3
        backoff = 1.0
        last_exc = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        max_output_tokens=get_settings().GEMINI_MAX_TOKENS,
                        temperature=0.0,
                    ),
                )

                # Defensive checks: ensure response and response.text exist
                if response is None:
                    raise RuntimeError("Empty response from Gemini client")
                text = getattr(response, 'text', None)
                if text is None:
                    # Try to log the response object for debugging
                    logger.error("Gemini response has no text attribute: %s", repr(response))
                    raise RuntimeError("Gemini returned no text in response")

                return text.strip()
            except Exception as e:
                last_exc = e
                # Detect rate limit in error message
                if "429" in str(e) or isinstance(e, RateLimitException):
                    logger.warning("Gemini rate limit detected (attempt %d/%d): %s", attempt, max_retries, e)
                    # If it's the last attempt, raise RateLimitException
                    if attempt == max_retries:
                        raise RateLimitException("Rate limit exceeded.") from e
                else:
                    logger.warning("Gemini call failed (attempt %d/%d): %s", attempt, max_retries, e)

                # simple exponential backoff
                time.sleep(backoff)
                backoff *= 2

        # If we exhausted retries, raise the last exception wrapped
        raise RuntimeError(f"Gemini client failed after {max_retries} attempts: {last_exc}") from last_exc
    
    def _build_sql_prompt(self, question: str, schema: str) -> str:
        plural_hint = ""
        if re.search(PLURAL_KEYWORDS, question.lower()):
            plural_hint = (
                "\nIMPORTANTE: A pergunta usa substantivo no plural. "
                "Retorne os TOP 3 por grupo usando ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)."
            )
        return f"Schema:\n{schema}\n\nPergunta: {question}{plural_hint}\nSQL:"

    def generate_sql(self, question: str, schema: str) -> str:
        system = (
            "Você é um analista de dados expert em SQLite3. "
            "Dado um schema, escreva APENAS o SQL para responder à pergunta. "
            "Retorne somente o código SQL, sem markdown, sem explicações. "
            "Use aliases descritivos em português nas colunas. "
            "Use SOMENTE as tabelas listadas no bloco 'Schema' fornecido. NÃO invente nomes de tabelas. "
            "SEMPRE use GROUP BY e agregações quando a pergunta envolver listas. "
            "NUNCA retorne todas as linhas de uma tabela sem filtro ou agregação. "
            "NUNCA use INSERT, UPDATE, DELETE, DROP, ALTER ou TRUNCATE. "
            "Para ranking dentro de grupos, use ROW_NUMBER() com PARTITION BY. "
            "Quando a pergunta especificar quantidade explícita (ex: top 5, os 10 maiores), use exatamente esse número. "
            "Quando a pergunta não especificar quantidade e pedir agregação por grupo, retorne TODOS os grupos ordenados. "
            "Quando a pergunta usar substantivo no singular por grupo, retorne top 1 por grupo. "
            "Quando a pergunta usar substantivo no plural por grupo SEM quantidade definida, retorne top 3 por grupo."
        )
        prompt = self._build_sql_prompt(question, schema)
        try:
            raw = self._call(system, prompt)
            sql = re.sub(r"```(?:sql)?|```", "", raw).strip()
            logger.debug("Generated SQL: %s", sql)
            return sql
        except RateLimitException:
            raise 
        except Exception as e:
            raise SQLGenerationException(f"Gemini failed to generate SQL: {e}") from e
        
    def generate_analysis(self, question: str, sql: str, data: list[dict]) -> str:
        system = (
            "Você é um analista de dados de e-commerce. "
            "Analise os resultados em português, de forma clara e objetiva. "
            "Destaque os principais insights em no máximo 3 parágrafos."
        )
        prompt = (
            f"Pergunta: {question}\n"
            f"SQL executado: {sql}\n"
            f"Total de registros: {len(data)}\n"
            f"Amostra dos dados: {data[:20]}\n\n"
            "Análise:"
        )
        try:
            return self._call(system, prompt)
        except RateLimitException:
            raise
        except Exception as e:
            logger.error("Failed to generate analysis: %s", e)
            return "Analysis unavailable at the moment."