"""Public Blog API routes."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.blog_service import blog_service

router = APIRouter(prefix="/api", tags=["Blogs"])


@router.get("/blogs")
def get_blogs(request: Request, lang: str | None = None, db: Session = Depends(get_db)):
    """Fetch published blog posts filtered by requested language with fallback."""
    selected_lang = lang or getattr(request.state, "lang", "en")
    return blog_service.get_all_blogs(db, lang=selected_lang)


@router.get("/blogs/{blog_id}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """Fetch a single blog post by ID."""
    blog = blog_service.get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
