"""
Application configuration settings using pydantic-settings.

Loads environment variables from .env file and provides type-safe configuration.
"""

import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file into os.environ so third-party libraries (like OpenAI SDK) can access them
from pathlib import Path
from dotenv import load_dotenv

# Get the directory containing this config file, then go up to backend/
_backend_dir = Path(__file__).parent.parent
_env_file = _backend_dir / ".env"
load_dotenv(_env_file)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All sensitive configuration should be stored in .env file and never committed.
    See backend/.env.example for required variables.
    """

    # Database configuration
    DATABASE_URL: str = Field(
        ...,
        description="Neon PostgreSQL connection string with async driver (postgresql+asyncpg://...)"
    )

    # Authentication configuration
    BETTER_AUTH_SECRET: str = Field(
        ...,
        description="JWT secret key for Better Auth (minimum 32 characters, must match frontend)"
    )

    # CORS configuration
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    # Application configuration
    DEBUG: bool = Field(
        default=False,
        description="Debug mode - enables detailed error messages and auto-reload"
    )

    # OpenAI API Key (required for AI Chatbot - Phase III)
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key for AI chatbot functionality"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS_ORIGINS string into a list of allowed origins.

        Returns:
            List of origin URLs (e.g., ["http://localhost:3000", "https://app.example.com"])
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


# Global settings instance
settings = Settings()
