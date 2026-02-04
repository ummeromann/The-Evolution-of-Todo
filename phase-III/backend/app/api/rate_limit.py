"""
Simple in-memory rate limiter for chat endpoints.

This provides basic rate limiting per user to prevent abuse.
For production, consider using Redis-based rate limiting for distributed systems.
"""

from fastapi import HTTPException, status, Request
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import threading


class RateLimiter:
    """
    Token bucket rate limiter.

    Limits requests per user within a time window.
    """

    def __init__(
        self,
        requests_per_minute: int = 20,
        cleanup_interval: int = 300  # Cleanup old entries every 5 minutes
    ):
        self.requests_per_minute = requests_per_minute
        self.window_size = timedelta(minutes=1)
        self.cleanup_interval = cleanup_interval

        # Dict of user_id -> list of request timestamps
        self._requests: Dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()
        self._last_cleanup = datetime.utcnow()

    def _cleanup_old_entries(self):
        """Remove expired request records."""
        now = datetime.utcnow()
        cutoff = now - self.window_size

        with self._lock:
            for user_id in list(self._requests.keys()):
                self._requests[user_id] = [
                    ts for ts in self._requests[user_id]
                    if ts > cutoff
                ]
                # Remove empty entries
                if not self._requests[user_id]:
                    del self._requests[user_id]

            self._last_cleanup = now

    def check_rate_limit(self, user_id: str) -> Tuple[bool, int]:
        """
        Check if user is within rate limit.

        Args:
            user_id: The user identifier

        Returns:
            Tuple of (allowed, remaining_requests)
        """
        now = datetime.utcnow()
        cutoff = now - self.window_size

        # Periodic cleanup
        if (now - self._last_cleanup).total_seconds() > self.cleanup_interval:
            self._cleanup_old_entries()

        with self._lock:
            # Filter to only recent requests
            recent_requests = [
                ts for ts in self._requests[user_id]
                if ts > cutoff
            ]
            self._requests[user_id] = recent_requests

            if len(recent_requests) >= self.requests_per_minute:
                return False, 0

            # Record this request
            self._requests[user_id].append(now)
            remaining = self.requests_per_minute - len(self._requests[user_id])

            return True, remaining


# Global rate limiter instance for chat
chat_rate_limiter = RateLimiter(requests_per_minute=20)


async def check_chat_rate_limit(request: Request) -> None:
    """
    FastAPI dependency for rate limiting chat requests.

    Usage:
        @router.post("/chat", dependencies=[Depends(check_chat_rate_limit)])
        async def send_chat_message(...):

    Raises:
        HTTPException 429 if rate limit exceeded
    """
    # Get user ID from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if user_id is None:
        # If no user ID yet (auth hasn't run), use IP as fallback
        client_ip = request.client.host if request.client else "unknown"
        user_id = f"ip:{client_ip}"
    else:
        user_id = str(user_id)

    allowed, remaining = chat_rate_limiter.check_rate_limit(user_id)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a moment before sending more messages.",
            headers={"Retry-After": "60"}
        )
