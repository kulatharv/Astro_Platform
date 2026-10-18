"""Auth Bounded Context Module."""
from .api import auth_router as router, AuthService

__all__ = ["router", "AuthService"]
