"""Blog Business Engine."""

from sqlalchemy.orm import Session
from shared.errors import NotFoundError
from .repository import BlogRepository
from .schemas import BlogPostCreate, BlogPostResponse


class BlogEngine:
    def __init__(self, db: Session):
        self.repo = BlogRepository(db)

    def get_post(self, slug: str) -> BlogPostResponse:
        post = self.repo.get_by_slug(slug)
        if not post:
            raise NotFoundError(f"Blog post with slug '{slug}' not found.")
        return BlogPostResponse.model_validate(post)

    def list_posts(self, lang: str = "en", limit: int = 20) -> list[BlogPostResponse]:
        posts = self.repo.list_posts(lang=lang, limit=limit)
        return [BlogPostResponse.model_validate(p) for p in posts]

    def create_post(self, data: BlogPostCreate) -> BlogPostResponse:
        post = self.repo.create_post(data)
        return BlogPostResponse.model_validate(post)
