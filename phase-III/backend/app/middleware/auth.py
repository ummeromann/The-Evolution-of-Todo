"""
JWT authentication middleware for FastAPI.

Provides JWT token validation and user extraction for protected routes.
Integrates with Better Auth JWT tokens issued by the frontend.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from uuid import UUID
from app.config import settings

# HTTP Bearer token security scheme
security = HTTPBearer()


def decode_jwt(token: str) -> dict:
    """
    Decode and validate JWT token.

    Validates the token signature, expiration, and structure according to
    the Better Auth JWT contract defined in auth-flow.md.

    Args:
        token: JWT token string

    Returns:
        Decoded payload dict containing:
            - sub (str): User ID (UUID)
            - email (str): User email
            - iat (int): Issued at timestamp
            - exp (int): Expiration timestamp
            - iss (str): Issuer

    Raises:
        HTTPException 401: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    FastAPI dependency to get current authenticated user ID.

    Extracts and validates JWT token from Authorization: Bearer header,
    then returns the authenticated user's ID for use in protected routes.

    Usage:
        @router.get("/api/tasks")
        async def list_tasks(
            user_id: UUID = Depends(get_current_user),
            db: AsyncSession = Depends(get_db)
        ):
            # user_id is guaranteed to be authenticated
            tasks = await get_user_tasks(db, user_id)
            return tasks

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        User ID (UUID) from validated JWT token's 'sub' claim

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or missing user ID
    """
    token = credentials.credentials
    payload = decode_jwt(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UUID(user_id)
