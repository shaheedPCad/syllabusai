"""
Clarity LMS - Configuration Management
Uses pydantic-settings for environment variable validation.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Security
    SECRET_KEY: str

    # OpenAI
    OPENAI_API_KEY: str

    # Application
    APP_NAME: str = "Clarity LMS"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
