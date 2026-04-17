from functools import lru_cache

from app.repositories.database_repository import DatabaseRepository
from app.services.gemini_service import GeminiService
from app.services.agent_service import AgentService

@lru_cache
def get_db_repository() -> DatabaseRepository:
    return DatabaseRepository()

@lru_cache
def get_gemini_service() -> GeminiService:
    return GeminiService()

def get_agent_service() -> AgentService:
    return AgentService(
        db_repo=get_db_repository(),
        llm=get_gemini_service(),
    )