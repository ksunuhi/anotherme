"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "AnotherMe"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./database/anotherme.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    # CORS - comma-separated string that gets split into list
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://localhost:8080,http://127.0.0.1:8000,http://127.0.0.1:8080"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_allowed_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
