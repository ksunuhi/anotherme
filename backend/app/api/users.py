"""
Users API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.post import Post
from app.models.friendship import Friendship
from app.models.message import Message
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    """
    # Update only provided fields
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
        # Also update display_name if not separately set
        if not current_user.display_name or current_user.display_name == current_user.full_name:
            current_user.display_name = user_update.full_name

    if user_update.bio is not None:
        current_user.bio = user_update.bio

    if user_update.city is not None:
        current_user.city = user_update.city

    if user_update.region is not None:
        current_user.region = user_update.region

    if user_update.country is not None:
        current_user.country = user_update.country

    if user_update.profile_picture_url is not None:
        current_user.profile_picture_url = user_update.profile_picture_url

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/me/stats")
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's statistics
    """
    # Count birthday twins
    birthday_twins_count = db.query(func.count(User.id)).filter(
        and_(
            User.birth_date == current_user.birth_date,
            User.id != current_user.id,
            User.is_discoverable == True
        )
    ).scalar()

    # Count friends (people I follow)
    friends_count = db.query(func.count(Friendship.id)).filter(
        Friendship.user_id == current_user.id
    ).scalar()

    # Count my posts
    posts_count = db.query(func.count(Post.id)).filter(
        Post.author_id == current_user.id
    ).scalar()

    # Count unread messages
    unread_messages_count = db.query(func.count(Message.id)).filter(
        and_(
            Message.recipient_id == current_user.id,
            Message.is_read == False
        )
    ).scalar()

    return {
        "birthdayTwins": birthday_twins_count,
        "friends": friends_count,
        "posts": posts_count,
        "messages": unread_messages_count
    }


@router.get("/birthday-twins", response_model=List[UserResponse])
async def get_birthday_twins(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get users with the same birthday as current user
    """
    twins = db.query(User).filter(
        and_(
            User.birth_date == current_user.birth_date,
            User.id != current_user.id,
            User.is_discoverable == True
        )
    ).limit(limit).offset(offset).all()

    return twins


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get another user's profile by ID
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_discoverable and user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user's profile is not discoverable"
        )

    return user


@router.get("/search/by-birthday")
async def search_by_birthday(
    year: int = Query(..., ge=1900, le=2024),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search users by specific birthday
    """
    from datetime import date

    try:
        search_date = date(year, month, day)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date"
        )

    users = db.query(User).filter(
        and_(
            User.birth_date == search_date,
            User.id != current_user.id,
            User.is_discoverable == True
        )
    ).limit(limit).offset(offset).all()

    return users
