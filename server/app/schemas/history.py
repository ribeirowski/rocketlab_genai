from datetime import datetime
from pydantic import BaseModel

class HistoryItem(BaseModel):
    id: int
    question: str
    generated_sql: str
    analysis: str | None
    row_count: int
    success: bool
    error: str | None
    created_at: datetime

class HistoryListResponse(BaseModel):
    items: list[HistoryItem]
    total: int
    page: int
    limit: int