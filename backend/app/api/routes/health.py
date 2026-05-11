"""Health check endpoint."""

from fastapi import APIRouter
from app.models.research import HealthResponse
from app.db.client import check_db_connection
from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns application status, environment, and database connectivity.
    Used by Docker health checks and monitoring systems.
    """
    db_connected = await check_db_connection()

    return HealthResponse(
        status="healthy" if db_connected else "unhealthy",
        environment=settings.environment,
        database_connected=db_connected,
    )
