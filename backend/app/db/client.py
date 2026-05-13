"""Supabase client initialization and connection management."""

from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Get Supabase client instance (singleton).

    Uses anon key for user-level operations.
    For admin operations, use get_supabase_admin_client().

    Returns:
        Supabase client instance
    """
    return create_client(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key,
    )


@lru_cache(maxsize=1)
def get_supabase_admin_client() -> Client:
    """
    Get Supabase admin client with service role key.

    Use sparingly - bypasses Row Level Security (RLS).
    Only for migrations, admin operations, or background jobs.

    Returns:
        Supabase admin client instance
    """
    return create_client(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_service_role_key,
    )


async def check_db_connection() -> bool:
    """
    Check if database connection is healthy.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = get_supabase_client()
        # Simple query to verify connection
        result = client.table("research_sessions").select("id").limit(1).execute()
        return True
    except Exception as e:
        print(f"Database connection check failed: {e}")
        return False
