"""
Password Reset Token Model
"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from datetime import datetime, timedelta
from app.core.database import Base
import secrets


class PasswordResetToken(Base):
    """Password reset tokens for forgot password functionality"""

    __tablename__ = "password_reset_tokens"

    id = Column(String, primary_key=True, index=True, default=lambda: secrets.token_urlsafe(32))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def create_token(cls, user_id: str, expires_in_hours: int = 1):
        """
        Create a new password reset token

        Args:
            user_id: User ID to create token for
            expires_in_hours: Token expiration time in hours (default: 1)

        Returns:
            PasswordResetToken instance
        """
        token = secrets.token_urlsafe(48)
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)

        return cls(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )

    def is_valid(self) -> bool:
        """Check if token is still valid (not expired and not used)"""
        return not self.used and datetime.utcnow() < self.expires_at

    def mark_as_used(self):
        """Mark token as used"""
        self.used = True
