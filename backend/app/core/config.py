from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and `.env`.

    This keeps local, test, and production configuration out of business code.
    Secrets such as API keys should be added here later, then supplied through
    `.env` or deployment environment variables.
    """

    app_name: str = "SupportOps Agent"
    app_env: str = "development"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # Cache settings so every import gets the same parsed configuration object.
    return Settings()


settings = get_settings()
