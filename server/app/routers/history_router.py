import logging

from fastapi import APIRouter, Depends, Query

from app.repositories.history_repository import HistoryRepository
from app.schemas.history import HistoryItem, HistoryListResponse

router = APIRouter(prefix="/history", tags=["History"])
logger = logging.getLogger(__name__)

def get_history_repository() -> HistoryRepository:
    return HistoryRepository()

@router.get("", response_model=HistoryListResponse, )
def list_history(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    repo: HistoryRepository = Depends(get_history_repository),
) -> HistoryListResponse:
    items = repo.list(page=page, limit=limit)
    total = repo.count()
    return HistoryListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
    )