"""
Statistics API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.user import User

router = APIRouter()


@router.get("/birthday-stats")
async def get_birthday_statistics(
    db: Session = Depends(get_db)
):
    """
    Get platform statistics (PUBLIC - no auth required)

    Returns:
    - Total members count
    - Unique birthdates count
    - Top 5 most popular birthdates with counts
    - Recent signups (last 7 days)
    """

    # Total members (discoverable only)
    total_members = db.query(func.count(User.id)).filter(
        User.is_discoverable == True
    ).scalar() or 0

    # Unique birthdates count
    unique_birthdates = db.query(func.count(func.distinct(User.birth_date))).filter(
        User.is_discoverable == True
    ).scalar() or 0

    # Recent signups (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_signups = db.query(func.count(User.id)).filter(
        User.created_at >= seven_days_ago,
        User.is_discoverable == True
    ).scalar() or 0

    # Top 5 most popular birthdates
    top_birthdates = db.query(
        User.birth_date,
        func.count(User.id).label('count')
    ).filter(
        User.is_discoverable == True,
        User.birth_date.isnot(None)
    ).group_by(
        User.birth_date
    ).order_by(
        desc('count')
    ).limit(5).all()

    # Format top birthdates
    top_birthdates_formatted = [
        {
            "date": bd.birth_date.isoformat() if bd.birth_date else None,
            "count": bd.count
        }
        for bd in top_birthdates
    ]

    return {
        "totalMembers": total_members,
        "uniqueBirthdates": unique_birthdates,
        "recentSignups": recent_signups,
        "topBirthdates": top_birthdates_formatted
    }
