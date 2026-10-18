"""User Feedback collection and Activity audit logging service."""

from sqlalchemy.orm import Session
from app.models.activity import UserActivity
from app.models.feedback import Feedback
from app.schemas.feedback import ActivityCreate, FeedbackCreate


class FeedbackService:
    @staticmethod
    def log_activity(
        db: Session,
        action: str,
        user_id: int | None = None,
        details: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> UserActivity:
        """Create an audit log activity entry."""
        activity = UserActivity(
            user_id=user_id,
            action=action[:80],
            details=details,
            ip_address=ip_address[:64] if ip_address else None,
            user_agent=user_agent,
        )
        db.add(activity)
        db.commit()
        return activity

    @staticmethod
    def submit_feedback(db: Session, data: FeedbackCreate, user_id: int | None = None) -> Feedback:
        """Record user feedback and satisfaction metrics."""
        item = Feedback(
            user_id=user_id,
            module=data.module[:40],
            person_name=data.person_name[:120] if data.person_name else None,
            birth_date=data.birth_date[:20] if data.birth_date else None,
            birth_time=data.birth_time[:20] if data.birth_time else None,
            birth_city=data.birth_city[:120] if data.birth_city else None,
            accuracy=data.accuracy[:40] if data.accuracy else None,
            experience=data.experience[:40] if data.experience else None,
            usefulness=data.usefulness[:40] if data.usefulness else None,
            comments=data.comments,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


feedback_service = FeedbackService()
