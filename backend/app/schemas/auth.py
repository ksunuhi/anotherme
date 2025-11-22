"""
Authentication schemas (request/response models)
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class UserRegister(BaseModel):
    """Registration request schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)
    birth_date: date
    gender: str = Field(..., pattern="^(Male|Female|Other|Prefer not to say)$")
    city: str = Field(..., min_length=1, max_length=100)
    region: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    profile_picture_url: Optional[str] = None


class UserLogin(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload schema"""
    user_id: Optional[str] = None
