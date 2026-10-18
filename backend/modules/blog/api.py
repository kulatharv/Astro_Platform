"""Blog Router and Public Service Interface."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.db import get_db
from shared.errors import NotFoundError
from .schemas import BlogPostCreate, BlogPostResponse
from .engine import BlogEngine

router = APIRouter(prefix="/api/blogs", tags=["blogs"])


class BlogService:
    def get_post(self, slug: str, db: Session) -> BlogPostResponse:
        engine = BlogEngine(db)
        return engine.get_post(slug)

    def list_posts(self, lang: str, db: Session, limit: int = 20) -> list[BlogPostResponse]:
        engine = BlogEngine(db)
        return engine.list_posts(lang=lang, limit=limit)

    def create_post(self, req: BlogPostCreate, db: Session) -> BlogPostResponse:
        engine = BlogEngine(db)
        return engine.create_post(req)

    def create_blog(self, db: Session, data: BlogPostCreate, language: str = "en"):
        if not getattr(data, "slug", None):
            import re
            data.slug = re.sub(r"[^\w]+", "-", data.title.lower()).strip("-")
        data.language = language
        engine = BlogEngine(db)
        return engine.create_post(data)

    def get_blog_by_id(self, db: Session, blog_id: int):
        from .models import BlogPost
        return db.query(BlogPost).filter(BlogPost.id == blog_id).first()

    def delete_blog(self, db: Session, blog_id: int):
        from .models import BlogPost
        post = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
        if post:
            db.delete(post)
            db.commit()
            return True
        return False

    def get_all_blogs(self, db: Session, lang: str = "en"):
        engine = BlogEngine(db)
        return [self.get_blog_by_id(db, p.id) for p in engine.list_posts(lang=lang)]



blog_service = BlogService()


@router.get("", response_model=list[BlogPostResponse])
def list_blogs(lang: str = "en", limit: int = 20, db: Session = Depends(get_db)):
    return blog_service.list_posts(lang=lang, db=db, limit=limit)


@router.get("/{slug}", response_model=BlogPostResponse)
def get_blog(slug: str, db: Session = Depends(get_db)):
    try:
        return blog_service.get_post(slug=slug, db=db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_blog(req: BlogPostCreate, db: Session = Depends(get_db)):
    return blog_service.create_post(req, db=db)
