"""
Contact form schemas
"""
from pydantic import BaseModel, EmailStr, Field


class ContactFormRequest(BaseModel):
    """Contact form submission"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)


class ContactFormResponse(BaseModel):
    """Contact form response"""
    success: bool
    message: str
