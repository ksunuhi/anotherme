"""
User schemas (request/response models)
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str
    display_name: Optional[str] = None
    birth_date: date
    gender: str
    city: str
    region: str
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update schema - all fields optional"""
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    profile_picture_url: Optional[str] = None
    is_discoverable: Optional[bool] = None


class UserResponse(UserBase):
    """User response schema (public info)"""
    id: str
    is_discoverable: bool
    email_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserMe(UserResponse):
    """Current user response (includes private info)"""
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None

    class Config:
        from_attributes = True


class UserSearch(BaseModel):
    """User search filters"""
    birth_date: Optional[date] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
