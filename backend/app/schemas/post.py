"""
Post schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    """Schema for creating a post"""
    content: str = Field(..., min_length=1, max_length=2000)
    visibility: str = Field(default="public")  # public, birthday_twins, friends, group
    title: Optional[str] = Field(None, max_length=200)
    group_id: Optional[str] = None


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
    group_id: Optional[str]
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    is_liked: bool = False  # Whether current user has liked this post

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

    class Config:
        from_attributes = True
