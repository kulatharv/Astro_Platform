"""Feedback database repository."""

from sqlalchemy.orm import Session
from .models import Feedback, ActivityLog
from .schemas import FeedbackCreate


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, data: FeedbackCreate, user_id: int = None) -> Feedback:
        fb = Feedback(
            user_id=user_id,
            module=data.module,
            rating=data.rating,
            comment=data.comment
        )
        self.db.add(fb)
        self.db.commit()
        self.db.refresh(fb)
        return fb

    def list_feedback(self, limit: int = 50, offset: int = 0) -> list[Feedback]:
        return self.db.query(Feedback).order_by(Feedback.created_at.desc()).offset(offset).limit(limit).all()

    def log_activity(self, action: str, details: str = None, user_id: int = None, ip_address: str = None) -> ActivityLog:
        log = ActivityLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
