"""
Post and Comment models
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200))
    content = Column(Text, nullable=False)  # Max 2000 chars enforced at API level
    visibility = Column(String, nullable=False, index=True)  # public, birthday_twins, friends, group
    group_id = Column(String, ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Post {self.id} by {self.author_id}>"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_comment_id = Column(String, ForeignKey("comments.id", ondelete="CASCADE"), index=True)
    content = Column(Text, nullable=False)  # Max 500 chars enforced at API level
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Comment {self.id} on Post {self.post_id}>"


class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(String, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PostLike {self.user_id} -> {self.post_id}>"


class CommentLike(Base):
    __tablename__ = "comment_likes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    comment_id = Column(String, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<CommentLike {self.user_id} -> {self.comment_id}>"
