"""
Message schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_serializer
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

    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime, _info):
        """Ensure datetime is serialized as UTC with Z suffix"""
        if dt.tzinfo is None:
            # Treat naive datetime as UTC
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Convert aware datetime to UTC
        return dt.astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

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

    @field_serializer('last_message_time')
    def serialize_datetime(self, dt: datetime, _info):
        """Ensure datetime is serialized as UTC with Z suffix"""
        if dt.tzinfo is None:
            # Treat naive datetime as UTC
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Convert aware datetime to UTC
        return dt.astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
