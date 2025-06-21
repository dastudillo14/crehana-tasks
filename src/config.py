from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """
    # Application settings
    APP_NAME: str = "Task Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    PORT: int = 8000

    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/task_management.db"

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Create a single instance of the settings to be used throughout the application
settings = AppSettings() 