"""
Message schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    """Schema for sending a message"""
    recipient_id: str
    content: str = Field(..., min_length=1, max_length=2000)


class MessageSender(BaseModel):
    """Nested sender info for message response"""
    id: str
    full_name: str
    display_name: Optional[str]
    profile_picture_url: Optional[str]

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: str
    sender_id: str
    recipient_id: str
    content: str
    is_read: bool
    created_at: datetime
    sender: Optional[MessageSender] = None

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Schema for conversation (chat) response"""
    user_id: str
    user_name: str
    user_display_name: Optional[str]
    last_message: str
    last_message_time: datetime
    unread_count: int
