import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas.feedback import FeedbackRequest, FeedbackItem, FeedbackListResponse
from app.repositories.feedback_repository import FeedbackRepository

router = APIRouter(prefix="/feedback", tags=["Feedback"])
repo = FeedbackRepository()
logger = logging.getLogger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_feedback(body: FeedbackRequest) -> None:
    repo.save(
        question_id=body.question_id,
        rating=body.rating,
        comment=body.comment,
    )

@router.get("/", response_model=FeedbackListResponse)
def list_feedback(page: int = 1, limit: int = 20) -> FeedbackListResponse:
    items = repo.list(page=page, limit=limit)
    return FeedbackListResponse(
        items=items,
        total=repo.count(),
        page=page,
        limit=limit,
    )
