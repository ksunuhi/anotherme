"""
Database models package
Import all models here for easy access
"""
from app.models.user import User
from app.models.post import Post, Comment, PostLike, CommentLike
from app.models.message import Message
from app.models.friendship import Friendship

__all__ = [
    "User",
    "Post",
    "Comment",
    "PostLike",
    "CommentLike",
    "Message",
    "Friendship",
]
