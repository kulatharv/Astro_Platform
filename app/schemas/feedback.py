from datetime import datetime
from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    module: str = Field(..., max_length=40)
    person_name: str | None = None
    birth_date: str | None = None
    birth_time: str | None = None
    birth_city: str | None = None
    accuracy: str | None = None
    experience: str | None = None
    usefulness: str | None = None
    comments: str | None = None


class ActivityCreate(BaseModel):
    module: str = "activity"
    action: str = "view"
    person_name: str | None = ""
    birth_date: str | None = ""
    birth_time: str | None = ""
    birth_city: str | None = ""
    details: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    user_id: int | None = None
    module: str
    person_name: str | None = None
    birth_date: str | None = None
    birth_time: str | None = None
    birth_city: str | None = None
    accuracy: str | None = None
    experience: str | None = None
    usefulness: str | None = None
    comments: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
