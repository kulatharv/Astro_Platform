import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[3]


def _csv_env(name: str, default: str = "") -> list[str]:
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AstroLogicAI")
    environment: str = os.getenv("ENVIRONMENT", os.getenv("ENV", "development"))
    debug: bool = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}

    # Database Settings (No fallback secret/url)
    database_url: str = os.getenv("DATABASE_URL", "")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    database_pool_recycle_seconds: int = int(os.getenv("DATABASE_POOL_RECYCLE_SECONDS", "1800"))

    # Security & Tokens (No hardcoded fallbacks!)
    secret_key: str = os.getenv("SECRET_KEY", "")
    session_secret_key: str = os.getenv("SESSION_SECRET_KEY", "")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

    # External APIs / AI
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    api_ninjas_key: str | None = os.getenv("API_NINJAS_KEY")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "phi3")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_origins or self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


def validate_settings(settings: Settings) -> None:
    """Fail-fast startup validation for required security environment variables."""
    required_vars = [
        ("SECRET_KEY", settings.secret_key),
        ("SESSION_SECRET_KEY", settings.session_secret_key),
        ("JWT_SECRET_KEY", settings.jwt_secret_key),
        ("DATABASE_URL", settings.database_url),
    ]
    for var_name, var_value in required_vars:
        if not var_value or not str(var_value).strip():
            raise RuntimeError(f"Missing required environment variable: {var_name}")


@lru_cache
def get_settings() -> Settings:
    st = Settings()
    validate_settings(st)
    return st


settings = get_settings()
