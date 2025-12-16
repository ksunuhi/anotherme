"""
Messages API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.api.auth import get_current_user
from app.core.security_utils import sanitize_message_content
from app.models.user import User
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse, MessageSender, ConversationResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_message_sender(user: User) -> MessageSender:
    """Convert User to MessageSender"""
    return MessageSender(
        id=user.id,
        full_name=user.full_name,
        display_name=user.display_name,
        profile_picture_url=user.profile_picture_url
    )


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/5minutes")  # Max 30 messages per 5 minutes
async def send_message(
    request: Request,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to another user
    """
    # Check if recipient exists
    recipient = db.query(User).filter(User.id == message_data.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )

    # Cannot message yourself
    if message_data.recipient_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot send a message to yourself"
        )

    # Sanitize message content to prevent XSS attacks
    sanitized_content = sanitize_message_content(message_data.content)

    # Create message
    new_message = Message(
        sender_id=current_user.id,
        recipient_id=message_data.recipient_id,
        content=sanitized_content,
        is_read=False
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Prepare response
    response = MessageResponse.model_validate(new_message)
    response.sender = get_message_sender(current_user)

    return response


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of all conversations (users you've messaged with)
    Returns most recent message for each conversation
    """
    # Get all unique users that current user has communicated with
    # (either sent to or received from)

    # Subquery for latest message with each user
    from sqlalchemy import literal_column

    conversations = []

    # Get all users current user has messaged with
    users_query = db.query(User.id).filter(
        or_(
            User.id.in_(
                db.query(Message.recipient_id).filter(Message.sender_id == current_user.id)
            ),
            User.id.in_(
                db.query(Message.sender_id).filter(Message.recipient_id == current_user.id)
            )
        )
    ).distinct().all()

    user_ids = [u[0] for u in users_query]

    for user_id in user_ids:
        # Get last message with this user
        last_message = db.query(Message).filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
                and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
            )
        ).order_by(desc(Message.created_at)).first()

        if not last_message:
            continue

        # Count unread messages from this user
        unread_count = db.query(func.count(Message.id)).filter(
            and_(
                Message.sender_id == user_id,
                Message.recipient_id == current_user.id,
                Message.is_read == False
            )
        ).scalar()

        # Get user info
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            continue

        conversations.append(ConversationResponse(
            user_id=user.id,
            user_name=user.full_name,
            user_display_name=user.display_name,
            last_message=last_message.content,
            last_message_time=last_message.created_at,
            unread_count=unread_count
        ))

    # Sort by most recent message
    conversations.sort(key=lambda c: c.last_message_time, reverse=True)

    return conversations


@router.get("/conversation/{user_id}", response_model=List[MessageResponse])
async def get_conversation(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all messages between current user and another user
    """
    # Check if user exists
    other_user = db.query(User).filter(User.id == user_id).first()
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get messages between these two users
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).offset(offset).limit(limit).all()

    # Mark messages as read (messages sent TO current user FROM other user)
    unread_messages = db.query(Message).filter(
        and_(
            Message.sender_id == user_id,
            Message.recipient_id == current_user.id,
            Message.is_read == False
        )
    ).all()

    for msg in unread_messages:
        msg.is_read = True

    if unread_messages:
        db.commit()

    # Get sender info
    current_user_info = get_message_sender(current_user)
    other_user_info = get_message_sender(other_user)

    # Prepare response
    result = []
    for message in messages:
        msg_response = MessageResponse.model_validate(message)
        msg_response.sender = current_user_info if message.sender_id == current_user.id else other_user_info
        result.append(msg_response)

    return result


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread messages
    """
    count = db.query(func.count(Message.id)).filter(
        and_(
            Message.recipient_id == current_user.id,
            Message.is_read == False
        )
    ).scalar()

    return {"unread_count": count}


@router.put("/{message_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_as_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a message as read
    """
    message = db.query(Message).filter(
        and_(
            Message.id == message_id,
            Message.recipient_id == current_user.id
        )
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    message.is_read = True
    db.commit()

    return None
