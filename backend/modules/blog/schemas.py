"""Blog validation schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BlogPostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=250)
    slug: Optional[str] = Field(None, max_length=250)
    content: str

    summary: Optional[str] = None
    language: str = "en"
    tags: Optional[List[str]] = []
    author: Optional[str] = "Astro AI"


class BlogPostResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    language: str
    tags: Optional[List[str]] = []
    author: Optional[str] = "Astro AI"
    created_at: datetime

    class Config:
        from_attributes = True


BlogCreate = BlogPostCreate

