"""Configuration module for loading environment variables and settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    LOGGING_LEVEL: str = "INFO"
    """Logging level for the application."""

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


settings = Settings()  # type: ignore[call-arg]
"""Instance of the `Settings` class that loads the configuration from environment variables.

This is a singleton pattern implementation - a single instance of Settings is created
and reused throughout the application, ensuring consistent configuration across all modules."""
