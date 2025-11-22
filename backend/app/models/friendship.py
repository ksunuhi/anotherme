"""
Friendship model (one-way)
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Friendship(Base):
    __tablename__ = "friendships"
    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    friend_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Friendship {self.user_id} -> {self.friend_id}>"
