"""Feedback Business Engine."""

from sqlalchemy.orm import Session
from .repository import FeedbackRepository
from .schemas import FeedbackCreate, FeedbackResponse


class FeedbackEngine:
    def __init__(self, db: Session):
        self.repo = FeedbackRepository(db)

    def submit_feedback(self, data: FeedbackCreate, user_id: int = None) -> FeedbackResponse:
        fb = self.repo.create_feedback(data, user_id=user_id)
        return FeedbackResponse.model_validate(fb)

    def get_recent_feedback(self, limit: int = 50) -> list[FeedbackResponse]:
        items = self.repo.list_feedback(limit=limit)
        return [FeedbackResponse.model_validate(i) for i in items]
