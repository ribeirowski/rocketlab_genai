from fastapi import APIRouter, Depends

from app.config import get_settings
from app.schemas.common import HealthResponse
from app.repositories.database_repository import DatabaseRepository
from app.dependencies import get_db_repository

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def health_check(db: DatabaseRepository = Depends(get_db_repository)):
    return HealthResponse(
        status="ok",
        message=f"{get_settings().APP_NAME} is running.",
        version=get_settings().APP_VERSION,
        db_connected=db.health_check(),
        db_tables=db.get_tables(),
        model=get_settings().GEMINI_MODEL,
    )