from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Core
    environment: str = "development"
    secret_key: str = "dev-secret-key-change-me-in-production-32ch"
    app_url: str = "http://localhost:8000"

    # Database — defaults to SQLite for local dev; set DATABASE_URL for Postgres
    database_url: str = "sqlite:///./sift.db"

    # LLM — optional; scoring falls back to heuristics when absent
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "google/gemini-flash-1.5"

    # Email — optional; dry-run mode when absent
    resend_api_key: str = ""
    email_from: str = "Sift <hello@usesift.app>"
    dry_run_email: bool = True

    # Magic link TTL in minutes
    magic_link_ttl_minutes: int = 15

    # Session TTL in days
    session_ttl_days: int = 30

    @field_validator("secret_key")
    @classmethod
    def secret_key_min_length(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def has_openrouter(self) -> bool:
        return bool(self.openrouter_api_key.strip())

    @property
    def has_resend(self) -> bool:
        return bool(self.resend_api_key.strip()) and not self.dry_run_email


@lru_cache
def get_settings() -> Settings:
    return Settings()
