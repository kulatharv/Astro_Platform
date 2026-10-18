from .dependencies import get_current_user, get_db, require_admin, require_authenticated_user
from .routes import (
    admin_router,
    auth_router,
    blogs_router,
    feedback_router,
    horoscope_router,
    kundali_router,
    pages_router,
    panchang_router,
    prediction_router,
)

__all__ = [
    "get_db",
    "get_current_user",
    "require_authenticated_user",
    "require_admin",
    "admin_router",
    "auth_router",
    "blogs_router",
    "feedback_router",
    "horoscope_router",
    "kundali_router",
    "pages_router",
    "panchang_router",
    "prediction_router",
]
