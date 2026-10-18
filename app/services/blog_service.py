"""Blog CRUD and administrative management service with multi-language support."""

from sqlalchemy.orm import Session
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate


class BlogService:
    @staticmethod
    def get_all_blogs(db: Session, lang: str | None = None) -> list[Blog]:
        """Fetch blogs sorted by newest first, optionally filtered by language with fallback to English/all."""
        if lang:
            lang_code = lang.lower().split("-")[0]
            blogs = db.query(Blog).filter(Blog.language == lang_code).order_by(Blog.id.desc()).all()
            if blogs:
                return blogs

        return db.query(Blog).order_by(Blog.id.desc()).all()

    @staticmethod
    def get_blog_by_id(db: Session, blog_id: int) -> Blog | None:
        """Fetch a single blog by ID."""
        return db.query(Blog).filter(Blog.id == blog_id).first()

    @staticmethod
    def create_blog(db: Session, data: BlogCreate, language: str = "en") -> Blog:
        """Create a new blog post with specified language."""
        lang_code = language.lower().split("-")[0] if language else "en"
        blog = Blog(
            title=data.title.strip(),
            content=data.content.strip(),
            language=lang_code,
        )
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def update_blog(db: Session, blog_id: int, data: BlogUpdate, language: str | None = None) -> Blog | None:
        """Update an existing blog post."""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return None

        if data.title is not None:
            blog.title = data.title.strip()
        if data.content is not None:
            blog.content = data.content.strip()
        if language is not None:
            blog.language = language.lower().split("-")[0]

        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def delete_blog(db: Session, blog_id: int) -> bool:
        """Delete a blog post by ID."""
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return False

        db.delete(blog)
        db.commit()
        return True


blog_service = BlogService()
