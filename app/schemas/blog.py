from datetime import datetime
from pydantic import BaseModel, Field


class BlogCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class BlogUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
