"""
Group and GroupMembership models
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    group_type = Column(String, nullable=False, index=True)  # birthday, custom
    birth_year = Column(Integer, index=True)
    birth_month = Column(Integer, index=True)
    birth_day = Column(Integer, index=True)
    member_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Group {self.name}>"


class GroupMembership(Base):
    __tablename__ = "group_memberships"
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='unique_membership'),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    group_id = Column(String, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, index=True)

    def __repr__(self):
        return f"<GroupMembership {self.user_id} in {self.group_id}>"
