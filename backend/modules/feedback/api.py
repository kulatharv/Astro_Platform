"""Feedback Router and Public Service Interface."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.db import get_db
from .schemas import FeedbackCreate, FeedbackResponse
from .engine import FeedbackEngine

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


class FeedbackService:
    def submit(self, req: FeedbackCreate, db: Session, user_id: int = None) -> FeedbackResponse:
        engine = FeedbackEngine(db)
        return engine.submit_feedback(req, user_id=user_id)

    def list_all(self, db: Session, limit: int = 50) -> list[FeedbackResponse]:
        engine = FeedbackEngine(db)
        return engine.get_recent_feedback(limit=limit)


feedback_service = FeedbackService()


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(req: FeedbackCreate, db: Session = Depends(get_db)):
    return feedback_service.submit(req, db=db)


@router.get("", response_model=list[FeedbackResponse])
def get_feedback_list(limit: int = 50, db: Session = Depends(get_db)):
    return feedback_service.list_all(db=db, limit=limit)
