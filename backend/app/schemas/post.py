"""
Post schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    """Schema for creating a post"""
    content: str = Field(..., min_length=1, max_length=2000)
    visibility: str = Field(default="public")  # public, birthday_twins, friends
    title: Optional[str] = Field(None, max_length=200)


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    content: str = Field(..., min_length=1, max_length=2000)
    title: Optional[str] = Field(None, max_length=200)


class PostAuthor(BaseModel):
    """Nested author info for post response"""
    id: str
    full_name: str
    display_name: Optional[str]
    profile_picture_url: Optional[str]

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    """Schema for post response"""
    id: str
    author_id: str
    author: Optional[PostAuthor] = None
    title: Optional[str]
    content: str
    visibility: str
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    is_liked: bool = False  # Whether current user has liked this post

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime, _info):
        """Ensure datetime is serialized as UTC with Z suffix"""
        if dt.tzinfo is None:
            # Treat naive datetime as UTC
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Convert aware datetime to UTC
        return dt.astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    """Schema for creating a comment"""
    content: str = Field(..., min_length=1, max_length=500)
    parent_comment_id: Optional[str] = None


class CommentResponse(BaseModel):
    """Schema for comment response"""
    id: str
    post_id: str
    author_id: str
    author: Optional[PostAuthor] = None
    parent_comment_id: Optional[str]
    content: str
    like_count: int
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime, _info):
        """Ensure datetime is serialized as UTC with Z suffix"""
        if dt.tzinfo is None:
            # Treat naive datetime as UTC
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Convert aware datetime to UTC
        return dt.astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    class Config:
        from_attributes = True
