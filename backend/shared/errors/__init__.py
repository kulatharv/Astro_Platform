"""Shared error types package."""
from .types import (
    AstroError, ChartComputationError, PredictionError,
    NarrativeError, AuthError, NotFoundError, ValidationError
)

__all__ = [
    "AstroError", "ChartComputationError", "PredictionError",
    "NarrativeError", "AuthError", "NotFoundError", "ValidationError"
]
