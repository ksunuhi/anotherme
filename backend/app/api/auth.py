"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    validate_password_strength
)
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.models.email_verification import EmailVerificationToken
from app.schemas.auth import (
    UserRegister, UserLogin, Token, TokenData,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse,
    VerifyEmailRequest, VerifyEmailResponse,
    ResendVerificationRequest, ResendVerificationResponse
)
from app.schemas.user import UserResponse, UserMe
from app.core.email import send_password_reset_email, send_verification_email

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


@router.get("/check-email")
async def check_email_availability(email: str, db: Session = Depends(get_db)):
    """
    Check if an email is available for registration
    Returns: {"available": true/false}
    """
    existing_user = db.query(User).filter(User.email == email).first()
    return {"available": existing_user is None, "email": email}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour")  # Max 3 registrations per hour per IP
async def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user

    Steps:
    1. Validate password strength
    2. Check if email already exists
    3. Hash password
    4. Create user in database
    5. Return user data (without password)
    """
    # Validate password strength
    is_valid, errors = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = get_password_hash(user_data.password)

    # Create user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        display_name=user_data.full_name,  # Default to full name
        birth_date=user_data.birth_date,
        gender=user_data.gender,
        city=user_data.city,
        region=user_data.region,
        country=user_data.country,
        bio=user_data.bio,
        profile_picture_url=user_data.profile_picture_url,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create verification token and send email
    verification_token = EmailVerificationToken.create_token(new_user.id)
    db.add(verification_token)
    db.commit()
    db.refresh(verification_token)

    # Send verification email
    send_verification_email(
        to_email=new_user.email,
        user_name=new_user.display_name or new_user.full_name,
        verification_token=verification_token.token
    )

    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("5/15minutes")  # Max 5 login attempts per 15 minutes
async def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return access token

    Steps:
    1. Find user by email
    2. Verify password
    3. Create JWT token
    4. Update last_login timestamp
    5. Return token
    """
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()

    # Verify user exists and password is correct
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in. Check your inbox for the verification link."
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/form", response_model=Token)
@limiter.limit("5/15minutes")  # Max 5 login attempts per 15 minutes
async def login_form(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login using OAuth2 password flow (for Swagger UI)
    Username field should contain the email
    """
    # Find user (username field contains email)
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in. Check your inbox for the verification link."
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserMe)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client should delete token)
    """
    return {"message": "Successfully logged out"}


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
@limiter.limit("3/hour")  # Max 3 password reset requests per hour
async def forgot_password(http_request: Request, request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request password reset email

    Steps:
    1. Find user by email
    2. Create password reset token
    3. Send reset email with token link
    4. Return success message (even if user not found for security)

    Args:
        request: Contains user email
        db: Database session

    Returns:
        Success message
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()

    # Always return success to prevent email enumeration
    # But only send email if user exists
    if user:
        # Create reset token
        reset_token = PasswordResetToken.create_token(user.id)
        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)

        # Send reset email
        send_password_reset_email(
            to_email=user.email,
            user_name=user.display_name or user.full_name,
            reset_token=reset_token.token
        )

    return ForgotPasswordResponse(
        success=True,
        message="If an account exists with this email, a password reset link has been sent."
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password using token

    Steps:
    1. Find token in database
    2. Validate token (not expired, not used)
    3. Validate new password strength
    4. Update user password
    5. Mark token as used
    6. Return success

    Args:
        request: Contains reset token and new password
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If token is invalid/expired or password is weak
    """
    # Find token
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token
    ).first()

    # Validate token exists
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Validate token is still valid (not expired, not used)
    if not reset_token.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This reset link has expired or already been used"
        )

    # Validate new password strength
    is_valid, errors = validate_password_strength(request.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )

    # Get user
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update password
    user.password_hash = get_password_hash(request.new_password)

    # Mark token as used
    reset_token.mark_as_used()

    db.commit()

    return ResetPasswordResponse(
        success=True,
        message="Your password has been successfully reset. You can now log in with your new password."
    )


@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    """
    Verify user email using token

    Steps:
    1. Find token in database
    2. Validate token (not expired, not used)
    3. Mark user email as verified
    4. Mark token as used
    5. Return success

    Args:
        request: Contains verification token
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If token is invalid or expired
    """
    # Find token
    verification_token = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == request.token
    ).first()

    # Validate token exists
    if not verification_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )

    # Validate token is still valid (not expired, not used)
    if not verification_token.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This verification link has expired or already been used"
        )

    # Get user
    user = db.query(User).filter(User.id == verification_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Mark email as verified
    user.email_verified = True

    # Mark token as used
    verification_token.mark_as_used()

    db.commit()

    return VerifyEmailResponse(
        success=True,
        message="Your email has been successfully verified! You can now access all features."
    )


@router.post("/resend-verification", response_model=ResendVerificationResponse)
async def resend_verification(request: ResendVerificationRequest, db: Session = Depends(get_db)):
    """
    Resend email verification link

    Steps:
    1. Find user by email
    2. Check if email is already verified
    3. Create new verification token
    4. Send verification email
    5. Return success message (even if user not found for security)

    Args:
        request: Contains user email
        db: Database session

    Returns:
        Success message
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()

    # Always return success to prevent email enumeration
    # But only send email if user exists and is not verified
    if user:
        if user.email_verified:
            return ResendVerificationResponse(
                success=True,
                message="If an unverified account exists with this email, a verification link has been sent."
            )

        # Create new verification token
        verification_token = EmailVerificationToken.create_token(user.id)
        db.add(verification_token)
        db.commit()
        db.refresh(verification_token)

        # Send verification email
        send_verification_email(
            to_email=user.email,
            user_name=user.display_name or user.full_name,
            verification_token=verification_token.token
        )

    return ResendVerificationResponse(
        success=True,
        message="If an unverified account exists with this email, a verification link has been sent."
    )
