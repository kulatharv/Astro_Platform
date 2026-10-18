"""User activity telemetry and testing feedback API routes."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.feedback import ActivityCreate, FeedbackCreate
from app.services.feedback_service import feedback_service

router = APIRouter(prefix="/api", tags=["Feedback & Activity"])


@router.post("/user-activity")
async def record_user_activity(request: Request, db: Session = Depends(get_db)):
    """Record user interaction and navigation telemetry."""
    user_id = request.session.get("user_id")
    if not user_id:
        return {"ok": False, "error": "Authentication required"}

    payload = await request.json()
    module = str(payload.get("module", "activity"))[:40]
    action = str(payload.get("action", "view"))[:40]
    person_name = str(payload.get("person_name", "") or "")
    birth_date = str(payload.get("birth_date", "") or "")
    birth_time = str(payload.get("birth_time", "") or "")
    birth_city = str(payload.get("birth_city", "") or "")
    details = f"{module}: {person_name} | {birth_date} {birth_time} | {birth_city}"

    feedback_service.log_activity(
        db,
        action=f"{module}_{action}",
        user_id=user_id,
        details=details,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return {"ok": True}


@router.post("/testing-feedback")
async def submit_testing_feedback(request: Request, db: Session = Depends(get_db)):
    """Submit testing feedback from users."""
    user_id = request.session.get("user_id")
    if not user_id:
        return {"ok": False, "error": "Authentication required"}

    payload = await request.json()
    data = FeedbackCreate(
        module=str(payload.get("module", "general")),
        person_name=str(payload.get("person_name", "") or ""),
        birth_date=str(payload.get("birth_date", "") or ""),
        birth_time=str(payload.get("birth_time", "") or ""),
        birth_city=str(payload.get("birth_city", "") or ""),
        accuracy=str(payload.get("accuracy", "") or ""),
        experience=str(payload.get("experience", "") or ""),
        usefulness=str(payload.get("usefulness", "") or ""),
        comments=str(payload.get("comments", "") or ""),
    )
    item = feedback_service.submit_feedback(db, data, user_id=user_id)

    feedback_service.log_activity(
        db,
        action=f"{item.module}_feedback",
        user_id=user_id,
        details=f"Feedback submitted for {item.person_name or item.birth_city}",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return {"ok": True}
