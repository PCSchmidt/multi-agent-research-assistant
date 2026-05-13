"""Pydantic models for API key management."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# Supported providers
Provider = Literal["anthropic", "openai", "openrouter"]


class APIKeyCreate(BaseModel):
    """Request model for creating/updating an API key."""

    provider: Provider = Field(..., description="API provider name")
    api_key: str = Field(..., min_length=1, description="API key value")


class APIKeyResponse(BaseModel):
    """Response model for API key (without the actual key)."""

    id: str
    user_id: str
    provider: Provider
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class APIKeyTestRequest(BaseModel):
    """Request model for testing an API key."""

    pass  # No body needed, provider comes from path


class APIKeyTestResponse(BaseModel):
    """Response model for API key test."""

    success: bool
    provider: Provider
    error: str | None = None
