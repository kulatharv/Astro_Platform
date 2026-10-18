"""Gateway dependencies for user authentication and session database access."""

from collections.abc import Generator
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from shared.config.settings import settings
from shared.db.session import get_db
from modules.auth.models import User


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Retrieve currently authenticated user from session."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def require_authenticated_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Require user session authentication or raise 401."""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


def require_admin(request: Request) -> bool:
    """Verify administrator privileges in session."""
    if request.session.get("admin") != "true":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin privileges required",
        )
    return True
