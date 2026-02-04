"""
Health check endpoint.

This module provides a simple health check endpoint to verify that the API
is running and responsive. It returns the current status and timestamp.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """
    Health check response schema.

    Attributes:
        status: Current health status of the API (always "healthy" when responding)
        timestamp: ISO 8601 formatted UTC timestamp of the health check
    """

    status: str
    timestamp: datetime


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns the API health status and current UTC timestamp.
    This endpoint can be used by load balancers, monitoring systems,
    or clients to verify that the API is operational.

    Returns:
        HealthResponse: Health status and timestamp

    Example Response:
        {
            "status": "healthy",
            "timestamp": "2026-01-13T10:30:45.123456Z"
        }
    """
    return HealthResponse(status="healthy", timestamp=datetime.now(timezone.utc))
