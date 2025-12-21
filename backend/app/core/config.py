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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour (combined with 30-min inactivity timeout)

    # CORS - comma-separated string that gets split into list
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://localhost:8080,http://127.0.0.1:8000,http://127.0.0.1:8080"

    # Email Configuration
    ADMIN_EMAIL: str = "admin@example.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "AnotherMe"
    SMTP_FROM_EMAIL: str = "noreply@anotherme.com"

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:8080"

    # Rate Limiting (format: "count/time_window")
    # Examples: "5/minute", "10/5minutes", "3/hour", "100/day"
    RATE_LIMIT_LOGIN: str = "5/15minutes"
    RATE_LIMIT_REGISTER: str = "3/hour"
    RATE_LIMIT_FORGOT_PASSWORD: str = "3/hour"
    RATE_LIMIT_CREATE_POST: str = "10/5minutes"
    RATE_LIMIT_CREATE_COMMENT: str = "20/5minutes"
    RATE_LIMIT_SEND_MESSAGE: str = "30/5minutes"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_allowed_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
