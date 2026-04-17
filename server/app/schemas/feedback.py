from datetime import datetime
from pydantic import BaseModel, Field

class FeedbackRequest(BaseModel):
    question_id: int
    rating: int = Field(..., description="1 for 👍, -1 for 👎")
    comment: str | None = None

class FeedbackItem(BaseModel):
    id: int
    question: str
    rating: int
    comment: str | None
    created_at: datetime

class FeedbackListResponse(BaseModel):
    items: list[FeedbackItem]
    total: int
    page: int
    limit: int
