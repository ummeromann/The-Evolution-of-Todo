"""
API routes package.

This module exports all API routers for inclusion in the main FastAPI application.
Each router handles a specific domain of the API (health, tasks, auth, etc.).
"""

from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.auth import router as auth_router

__all__ = ["health_router", "tasks_router", "auth_router"]
