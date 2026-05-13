"""API key management endpoints."""

from typing import Annotated

from anthropic import Anthropic
from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAI

from app.db.client import get_supabase_client
from app.models.api_keys import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyTestResponse,
    Provider,
)
from app.utils.encryption import decrypt_api_key, encrypt_api_key

router = APIRouter(prefix="/api/keys", tags=["API Keys"])


# TODO: Replace with actual auth dependency from Supabase
async def get_current_user():
    """
    Get current authenticated user.

    For now, returns a mock user. Will be replaced with Supabase auth.

    Returns:
        Dict with user ID
    """
    # Mock user for development
    # In production, this will verify Supabase JWT and return actual user
    return {"sub": "00000000-0000-0000-0000-000000000000"}


@router.post("", response_model=APIKeyResponse, status_code=status.HTTP_200_OK)
async def save_api_key(
    key_data: APIKeyCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Save or update an API key for a provider.

    The key is encrypted before storage using Fernet encryption.

    Args:
        key_data: Provider and API key
        current_user: Authenticated user from dependency

    Returns:
        Created/updated key metadata (without the actual key)

    Raises:
        HTTPException: If database operation fails
    """
    supabase = get_supabase_client()
    user_id = current_user["sub"]

    try:
        # Encrypt the API key
        encrypted_key = encrypt_api_key(key_data.api_key)

        # Upsert key (insert or update if exists)
        response = (
            supabase.table("user_api_keys")
            .upsert(
                {
                    "user_id": user_id,
                    "provider": key_data.provider,
                    "encrypted_key": encrypted_key,
                },
                on_conflict="user_id,provider",
            )
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save API key",
            )

        return response.data[0]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save API key: {str(e)}",
        ) from e


@router.get("", response_model=list[APIKeyResponse])
async def list_api_keys(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    List all API keys for the current user.

    Returns only metadata (provider, timestamps), never the actual keys.

    Args:
        current_user: Authenticated user from dependency

    Returns:
        List of API key metadata

    Raises:
        HTTPException: If database operation fails
    """
    supabase = get_supabase_client()
    user_id = current_user["sub"]

    try:
        response = (
            supabase.table("user_api_keys")
            .select("id, user_id, provider, created_at, updated_at")
            .eq("user_id", user_id)
            .execute()
        )

        return response.data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list API keys: {str(e)}",
        ) from e


@router.delete("/{provider}")
async def delete_api_key(
    provider: Provider,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Delete an API key for a provider.

    Args:
        provider: Provider name (anthropic, openai, openrouter)
        current_user: Authenticated user from dependency

    Returns:
        Success message

    Raises:
        HTTPException: If database operation fails
    """
    supabase = get_supabase_client()
    user_id = current_user["sub"]

    try:
        supabase.table("user_api_keys").delete().eq("user_id", user_id).eq(
            "provider", provider
        ).execute()

        return {"message": "API key deleted successfully", "provider": provider}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete API key: {str(e)}",
        ) from e


@router.post("/{provider}/test", response_model=APIKeyTestResponse)
async def test_api_key(
    provider: Provider,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Test an API key by making a simple API call.

    Args:
        provider: Provider name (anthropic, openai, openrouter)
        current_user: Authenticated user from dependency

    Returns:
        Test result with success status

    Raises:
        HTTPException: If key not found or database operation fails
    """
    supabase = get_supabase_client()
    user_id = current_user["sub"]

    try:
        # Fetch the encrypted key
        response = (
            supabase.table("user_api_keys")
            .select("encrypted_key")
            .eq("user_id", user_id)
            .eq("provider", provider)
            .single()
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No API key found for provider: {provider}",
            )

        # Decrypt the key
        api_key = decrypt_api_key(response.data["encrypted_key"])

        # Test the key with a simple API call
        success = False
        error = None

        try:
            if provider == "anthropic":
                client = Anthropic(api_key=api_key)
                client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=10,
                    messages=[{"role": "user", "content": "test"}],
                )
                success = True

            elif provider == "openai":
                client = OpenAI(api_key=api_key)
                client.models.list()
                success = True

            elif provider == "openrouter":
                # OpenRouter uses OpenAI-compatible API
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://openrouter.ai/api/v1",
                )
                client.models.list()
                success = True

        except Exception as test_error:
            error = str(test_error)

        return APIKeyTestResponse(
            success=success,
            provider=provider,
            error=error,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test API key: {str(e)}",
        ) from e
