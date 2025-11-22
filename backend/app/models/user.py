"""
User model
"""
from sqlalchemy import Column, String, Date, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    display_name = Column(String)
    birth_date = Column(Date, nullable=False, index=True)
    gender = Column(String, nullable=False)  # Male, Female, Other, Prefer not to say
    city = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False)
    profile_picture_url = Column(String)
    bio = Column(Text)
    is_discoverable = Column(Boolean, default=True, index=True)
    email_verified = Column(Boolean, default=False)
    oauth_provider = Column(String)  # google, facebook, or None
    oauth_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<User {self.email}>"
