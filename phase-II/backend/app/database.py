"""
Database configuration and session management for Neon PostgreSQL.

This module sets up the async SQLAlchemy engine and provides session dependencies
for FastAPI route handlers. All database operations use async/await patterns for
optimal performance with Neon's serverless PostgreSQL.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import settings

# Create async engine with connection pooling and health checks
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Maximum number of connections in the pool
    max_overflow=10,  # Maximum overflow connections beyond pool_size
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy loading errors after commit
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an async database session.

    This function yields an AsyncSession that automatically commits on success
    and rolls back on exceptions. Use it as a dependency in route handlers.

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()

    Yields:
        AsyncSession: Database session for executing queries

    Note:
        The session is automatically closed after the request completes.
        All changes are committed if no exceptions occur, otherwise rolled back.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.

    Creates all tables defined in SQLModel models. This should be called
    on application startup in development, or managed via migrations in production.

    Note:
        In production, prefer using Alembic migrations instead of this function.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections gracefully.

    Disposes of the engine and closes all connections in the pool.
    This should be called on application shutdown.
    """
    await engine.dispose()
