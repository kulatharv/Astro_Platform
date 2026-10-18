"""Typed domain and infrastructure exceptions for Astro-Platform."""

class AstroError(Exception):
    """Base exception for all astrological platform errors."""
    def __init__(self, message: str, code: str = "ASTRO_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code

class ChartComputationError(AstroError):
    def __init__(self, message: str = "Error calculating birth chart."):
        super().__init__(message, code="CHART_COMPUTATION_ERROR")

class PredictionError(AstroError):
    def __init__(self, message: str = "Error evaluating domain prediction."):
        super().__init__(message, code="PREDICTION_ERROR")

class NarrativeError(AstroError):
    def __init__(self, message: str = "Error synthesizing AI narrative."):
        super().__init__(message, code="NARRATIVE_ERROR")

class AuthError(AstroError):
    def __init__(self, message: str = "Authentication failed."):
        super().__init__(message, code="AUTH_ERROR")

class NotFoundError(AstroError):
    def __init__(self, message: str = "Requested resource not found."):
        super().__init__(message, code="NOT_FOUND_ERROR")

class ValidationError(AstroError):
    def __init__(self, message: str = "Input validation failed."):
        super().__init__(message, code="VALIDATION_ERROR")
