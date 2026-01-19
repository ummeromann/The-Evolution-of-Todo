"""
Authentication API endpoints.

This module provides REST API endpoints for user signup and signin.
Uses JWT tokens for authentication compatible with Better Auth.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt

from app.api.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.config import settings
from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(user_id: str, email: str) -> str:
    """
    Create a JWT access token.

    Token structure follows Better Auth JWT contract:
    - sub: User ID (UUID as string)
    - email: User email
    - iat: Issued at timestamp
    - exp: Expiration timestamp (7 days)
    - iss: Issuer identifier
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=7)).timestamp()),
        "iss": "todo-api",
    }
    return jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Register a new user account.

    Creates a new user with the provided email and password.
    Password is securely hashed using bcrypt before storage.
    Returns a JWT access token for immediate authentication.

    Args:
        user_data: User registration data (email, password)
        db: Database session

    Returns:
        TokenResponse: JWT access token and user info

    Raises:
        HTTPException 400: If email is already registered
        HTTPException 422: If validation fails

    Example Request:
        POST /auth/signup
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }

    Example Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer",
            "user": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "created_at": "2026-01-15T10:30:45.123456Z"
            }
        }
    """
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with hashed password
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Generate JWT token
    access_token = create_access_token(str(user.id), user.email)

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/signin", response_model=TokenResponse)
async def signin(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user and return a JWT token.

    Validates user credentials against stored password hash.
    Returns a JWT access token on successful authentication.

    Args:
        credentials: User login data (email, password)
        db: Database session

    Returns:
        TokenResponse: JWT access token and user info

    Raises:
        HTTPException 401: If credentials are invalid

    Example Request:
        POST /auth/signin
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }

    Example Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer",
            "user": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "created_at": "2026-01-15T10:30:45.123456Z"
            }
        }
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password matches
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    access_token = create_access_token(str(user.id), user.email)

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )
