"""
Posts API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.api.auth import get_current_user
from app.core.security_utils import sanitize_post_content, sanitize_comment_content
from app.models.user import User
from app.models.post import Post, PostLike, Comment
from app.models.friendship import Friendship
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostAuthor, CommentCreate, CommentResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_post_author(user: User) -> PostAuthor:
    """Convert User to PostAuthor"""
    return PostAuthor(
        id=user.id,
        full_name=user.full_name,
        display_name=user.display_name,
        profile_picture_url=user.profile_picture_url
    )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/5minutes")  # Max 10 posts per 5 minutes
async def create_post(
    request: Request,
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new post
    """
    # Sanitize user input to prevent XSS attacks
    sanitized_content = sanitize_post_content(post_data.content)

    # Create post
    new_post = Post(
        author_id=current_user.id,
        title=post_data.title,
        content=sanitized_content,
        visibility=post_data.visibility
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Prepare response
    response = PostResponse.model_validate(new_post)
    response.author = get_post_author(current_user)
    response.is_liked = False

    return response


@router.get("/feed", response_model=List[PostResponse])
async def get_feed(
    filter_type: str = Query("friends", regex="^(friends|twins|my)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get posts feed based on filter
    - friends: Posts from friends
    - twins: Posts from birthday twins
    - my: Only my posts
    """
    query = db.query(Post).order_by(Post.created_at.desc())

    if filter_type == "my":
        # Only my posts
        query = query.filter(Post.author_id == current_user.id)

    elif filter_type == "friends":
        # Get friend IDs
        friend_ids = db.query(Friendship.friend_id).filter(
            Friendship.user_id == current_user.id
        ).all()
        friend_ids = [f[0] for f in friend_ids]

        if not friend_ids:
            return []

        # Posts from friends
        query = query.filter(Post.author_id.in_(friend_ids))

    elif filter_type == "twins":
        # Get users with same birthday
        twin_ids = db.query(User.id).filter(
            and_(
                User.birth_date == current_user.birth_date,
                User.id != current_user.id,
                User.is_discoverable == True
            )
        ).all()
        twin_ids = [t[0] for t in twin_ids]

        if not twin_ids:
            return []

        # Posts from birthday twins
        query = query.filter(Post.author_id.in_(twin_ids))

    # Apply pagination
    posts = query.limit(limit).offset(offset).all()

    # Get liked post IDs for current user
    liked_post_ids = set(
        db.query(PostLike.post_id).filter(
            PostLike.user_id == current_user.id
        ).all()
    )
    liked_post_ids = {pid[0] for pid in liked_post_ids}

    # Get all author IDs
    author_ids = list(set([p.author_id for p in posts]))
    authors = db.query(User).filter(User.id.in_(author_ids)).all()
    authors_dict = {a.id: get_post_author(a) for a in authors}

    # Prepare response
    result = []
    for post in posts:
        post_response = PostResponse.model_validate(post)
        post_response.author = authors_dict.get(post.author_id)
        post_response.is_liked = post.id in liked_post_ids
        result.append(post_response)

    return result


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single post by ID
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Get author
    author = db.query(User).filter(User.id == post.author_id).first()

    # Check if liked
    is_liked = db.query(PostLike).filter(
        and_(
            PostLike.user_id == current_user.id,
            PostLike.post_id == post_id
        )
    ).first() is not None

    # Prepare response
    response = PostResponse.model_validate(post)
    response.author = get_post_author(author) if author else None
    response.is_liked = is_liked

    return response


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a post (only by author)
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if user is the author
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own posts"
        )

    # Update post (sanitize content to prevent XSS)
    post.content = sanitize_post_content(post_data.content)
    if post_data.title is not None:
        post.title = post_data.title
    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)

    # Check if liked
    is_liked = db.query(PostLike).filter(
        and_(
            PostLike.user_id == current_user.id,
            PostLike.post_id == post_id
        )
    ).first() is not None

    # Prepare response
    response = PostResponse.model_validate(post)
    response.author = get_post_author(current_user)
    response.is_liked = is_liked

    return response


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a post (only by author)
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if user is the author
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own posts"
        )

    db.delete(post)
    db.commit()

    return None


@router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
async def like_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Like a post (or unlike if already liked)
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if already liked
    existing_like = db.query(PostLike).filter(
        and_(
            PostLike.user_id == current_user.id,
            PostLike.post_id == post_id
        )
    ).first()

    if existing_like:
        # Unlike (trigger will auto-decrement like_count)
        db.delete(existing_like)
        db.commit()
        db.refresh(post)  # Refresh to get updated like_count from trigger
        return {"liked": False, "like_count": post.like_count}
    else:
        # Like (trigger will auto-increment like_count)
        new_like = PostLike(
            user_id=current_user.id,
            post_id=post_id
        )
        db.add(new_like)
        db.commit()
        db.refresh(post)  # Refresh to get updated like_count from trigger
        return {"liked": True, "like_count": post.like_count}


# ===== COMMENT ENDPOINTS =====

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all comments for a post
    """
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Get comments (only top-level, no replies for now)
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at.asc()).all()

    # Get all unique author IDs
    author_ids = list(set([c.author_id for c in comments]))
    authors = db.query(User).filter(User.id.in_(author_ids)).all()
    authors_dict = {a.id: get_post_author(a) for a in authors}

    # Prepare response
    result = []
    for comment in comments:
        comment_response = CommentResponse.model_validate(comment)
        comment_response.author = authors_dict.get(comment.author_id)
        result.append(comment_response)

    return result


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/5minutes")  # Max 20 comments per 5 minutes
async def create_comment(
    request: Request,
    post_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a comment on a post
    """
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Sanitize comment content to prevent XSS attacks
    sanitized_content = sanitize_comment_content(comment_data.content)

    # Create comment
    new_comment = Comment(
        post_id=post_id,
        author_id=current_user.id,
        content=sanitized_content,
        parent_comment_id=comment_data.parent_comment_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    db.refresh(post)  # Refresh to get updated comment_count from trigger

    # Prepare response
    response = CommentResponse.model_validate(new_comment)
    response.author = get_post_author(current_user)

    return response


@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    post_id: str,
    comment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a comment (only by author)
    """
    comment = db.query(Comment).filter(
        and_(
            Comment.id == comment_id,
            Comment.post_id == post_id
        )
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Check if user is the author
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )

    db.delete(comment)
    db.commit()

    return None
