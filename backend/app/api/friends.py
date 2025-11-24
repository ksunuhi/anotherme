"""
Friends API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.friendship import Friendship
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_my_friends(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of friends (people I follow)
    """
    # Get friend IDs
    friend_ids = db.query(Friendship.friend_id).filter(
        Friendship.user_id == current_user.id
    ).limit(limit).offset(offset).all()

    if not friend_ids:
        return []

    friend_ids = [f[0] for f in friend_ids]

    # Get friend users
    friends = db.query(User).filter(User.id.in_(friend_ids)).all()

    return friends


@router.post("/{friend_id}", status_code=status.HTTP_201_CREATED)
async def add_friend(
    friend_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a friend (two-way automatic friendship)
    When A adds B:
    - B is added to A's friend list
    - A is automatically added to B's friend list
    """
    # Check if trying to add self
    if friend_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot add yourself as a friend"
        )

    # Check if user exists
    friend = db.query(User).filter(User.id == friend_id).first()
    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if friendship already exists (either direction)
    existing = db.query(Friendship).filter(
        or_(
            and_(
                Friendship.user_id == current_user.id,
                Friendship.friend_id == friend_id
            ),
            and_(
                Friendship.user_id == friend_id,
                Friendship.friend_id == current_user.id
            )
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already friends"
        )

    # Create two-way friendship
    # A -> B
    friendship1 = Friendship(
        user_id=current_user.id,
        friend_id=friend_id
    )
    # B -> A
    friendship2 = Friendship(
        user_id=friend_id,
        friend_id=current_user.id
    )

    db.add(friendship1)
    db.add(friendship2)
    db.commit()

    return {
        "message": "Friend added successfully",
        "friend": UserResponse.model_validate(friend)
    }


@router.delete("/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(
    friend_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a friend (remove two-way friendship)
    When A removes B:
    - B is removed from A's friend list
    - A is automatically removed from B's friend list
    """
    # Find both directions of friendship
    friendships = db.query(Friendship).filter(
        or_(
            and_(
                Friendship.user_id == current_user.id,
                Friendship.friend_id == friend_id
            ),
            and_(
                Friendship.user_id == friend_id,
                Friendship.friend_id == current_user.id
            )
        )
    ).all()

    if not friendships:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friendship not found"
        )

    # Delete both directions
    for friendship in friendships:
        db.delete(friendship)

    db.commit()

    return None


@router.get("/mutual/{user_id}")
async def get_mutual_friends(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mutual friends between current user and another user
    """
    # Get my friend IDs
    my_friend_ids = db.query(Friendship.friend_id).filter(
        Friendship.user_id == current_user.id
    ).all()
    my_friend_ids = {f[0] for f in my_friend_ids}

    # Get their friend IDs
    their_friend_ids = db.query(Friendship.friend_id).filter(
        Friendship.user_id == user_id
    ).all()
    their_friend_ids = {f[0] for f in their_friend_ids}

    # Find intersection
    mutual_ids = my_friend_ids.intersection(their_friend_ids)

    if not mutual_ids:
        return {"count": 0, "friends": []}

    # Get mutual friend users
    mutual_friends = db.query(User).filter(User.id.in_(mutual_ids)).all()

    return {
        "count": len(mutual_friends),
        "friends": [UserResponse.model_validate(f) for f in mutual_friends]
    }


@router.get("/check/{user_id}")
async def check_friendship(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check friendship status between current user and another user
    With two-way friendships, if A is friends with B, then B is friends with A
    """
    # Check if friendship exists (either direction means mutual friendship)
    are_friends = db.query(Friendship).filter(
        or_(
            and_(
                Friendship.user_id == current_user.id,
                Friendship.friend_id == user_id
            ),
            and_(
                Friendship.user_id == user_id,
                Friendship.friend_id == current_user.id
            )
        )
    ).first() is not None

    return {
        "are_friends": are_friends
    }
