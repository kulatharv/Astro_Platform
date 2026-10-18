"""Blog Post ORM Model."""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from shared.db import Base
from shared.timezone import now_ist


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    slug = Column(String(250), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    language = Column(String(10), default="en", index=True)
    tags = Column(JSON, nullable=True)
    author = Column(String(100), default="Astro AI")
    created_at = Column(DateTime(timezone=True), default=now_ist)


Blog = BlogPost

