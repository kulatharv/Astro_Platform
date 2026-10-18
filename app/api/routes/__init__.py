from .admin import router as admin_router
from .auth import router as auth_router
from .blogs import router as blogs_router
from .feedback import router as feedback_router
from .horoscope import router as horoscope_router
from .kundali import router as kundali_router
from .pages import router as pages_router
from .panchang import router as panchang_router
from .prediction import router as prediction_router

__all__ = [
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
