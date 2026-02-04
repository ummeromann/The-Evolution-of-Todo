"""
FastAPI dependencies for the application.

This module provides reusable dependencies for FastAPI route handlers,
including database session management and authentication.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db as get_database_session
from app.middleware.auth import get_current_user

# Re-export dependencies for cleaner imports in route handlers
# Usage:
#   db: AsyncSession = Depends(get_db)
#   user_id: UUID = Depends(get_current_user)
__all__ = ["get_db", "get_current_user"]


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency.

    Yields an async database session and ensures proper cleanup.
    The session automatically commits on success and rolls back on exceptions.

    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()

    Yields:
        AsyncSession: Database session for executing queries
    """
    async for session in get_database_session():
        yield session
