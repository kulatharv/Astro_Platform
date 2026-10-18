"""Blog database repository."""

from typing import Optional
from sqlalchemy.orm import Session
from .models import BlogPost
from .schemas import BlogPostCreate


class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        return self.db.query(BlogPost).filter(BlogPost.slug == slug).first()

    def list_posts(self, lang: str = "en", limit: int = 20, offset: int = 0) -> list[BlogPost]:
        return (
            self.db.query(BlogPost)
            .filter(BlogPost.language == lang)
            .order_by(BlogPost.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create_post(self, data: BlogPostCreate) -> BlogPost:
        post = BlogPost(
            title=data.title,
            slug=data.slug,
            content=data.content,
            summary=data.summary,
            language=data.language,
            tags=data.tags,
            author=data.author,
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
