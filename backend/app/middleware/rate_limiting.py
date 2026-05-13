"""Rate limiting middleware for research queries."""

from datetime import datetime, timedelta
from typing import Dict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config import settings
from app.db.client import get_supabase_admin_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for research queries.

    Limits users to N queries per hour based on settings.rate_limit_queries_per_hour.
    Uses Supabase to track query counts (stateless, works across multiple instances).
    """

    async def dispatch(self, request: Request, call_next):
        """Check rate limits before processing request."""
        # Only apply rate limiting to research endpoints
        if not request.url.path.startswith("/api/research"):
            return await call_next(request)

        # Skip for health checks and GET requests
        if request.method != "POST":
            return await call_next(request)

        # Extract user_id (placeholder for now - will use auth in v0.15)
        user_id = "00000000-0000-0000-0000-000000000000"  # Default test user

        # TODO v0.15: Extract from JWT token when auth is implemented
        # if "Authorization" in request.headers:
        #     user_id = extract_user_from_jwt(request.headers["Authorization"])

        try:
            # Check rate limit
            is_allowed = await self.check_rate_limit(user_id)

            if not is_allowed:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Maximum {settings.rate_limit_queries_per_hour} queries per hour allowed",
                        "retry_after_seconds": 3600,  # Retry after 1 hour
                    }
                )

            # Process request
            response = await call_next(request)
            return response

        except HTTPException:
            raise
        except Exception as e:
            print(f"[RATE_LIMIT] Error checking rate limit: {str(e)}")
            # On error, allow request (fail open)
            return await call_next(request)

    async def check_rate_limit(self, user_id: str) -> bool:
        """
        Check if user is within rate limit.

        Args:
            user_id: User ID to check

        Returns:
            True if allowed, False if rate limit exceeded
        """
        try:
            supabase = get_supabase_admin_client()

            # Calculate time window (last hour)
            one_hour_ago = datetime.now() - timedelta(hours=1)

            # Count queries in last hour
            result = supabase.table("research_sessions").select(
                "id",
                count="exact"
            ).eq("user_id", user_id).gte(
                "created_at", one_hour_ago.isoformat()
            ).execute()

            query_count = result.count or 0

            print(f"[RATE_LIMIT] User {user_id}: {query_count}/{settings.rate_limit_queries_per_hour} queries in last hour")

            # Check against limit
            return query_count < settings.rate_limit_queries_per_hour

        except Exception as e:
            print(f"[RATE_LIMIT] Error: {str(e)}")
            # Fail open - allow request if rate limit check fails
            return True


# In-memory rate limit tracker (fallback if database is unavailable)
# Maps user_id -> list of query timestamps
_in_memory_tracker: Dict[str, list[datetime]] = {}


def check_rate_limit_in_memory(user_id: str, limit: int = 10) -> bool:
    """
    In-memory rate limit check (fallback).

    Args:
        user_id: User ID
        limit: Maximum queries per hour

    Returns:
        True if allowed, False if exceeded
    """
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)

    # Get user's query timestamps
    if user_id not in _in_memory_tracker:
        _in_memory_tracker[user_id] = []

    # Remove old timestamps
    _in_memory_tracker[user_id] = [
        ts for ts in _in_memory_tracker[user_id]
        if ts > one_hour_ago
    ]

    # Check count
    if len(_in_memory_tracker[user_id]) >= limit:
        return False

    # Add current timestamp
    _in_memory_tracker[user_id].append(now)
    return True
