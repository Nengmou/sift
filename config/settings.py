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
    secret_key: str
    app_url: str = "http://localhost:8000"

    # Database
    database_url: str

    # LLM
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "google/gemini-flash-1.5"

    # Email
    resend_api_key: str
    email_from: str = "Sift <hello@usesift.app>"

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


@lru_cache
def get_settings() -> Settings:
    return Settings()
