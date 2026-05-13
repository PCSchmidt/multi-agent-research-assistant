"""Unit tests for API key management endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing."""
    with patch("app.api.routes.keys.get_supabase_client") as mock:
        mock_client = MagicMock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_auth_user():
    """Mock authenticated user."""
    return {"sub": "test-user-id-123"}


@pytest.mark.asyncio
async def test_save_api_key(mock_supabase_client, mock_auth_user):
    """Test saving a new API key."""
    # Mock Supabase upsert response
    mock_response = MagicMock()
    mock_response.data = [{
        "id": "key-id-123",
        "user_id": "test-user-id-123",
        "provider": "anthropic",
        "created_at": "2026-05-13T00:00:00Z",
        "updated_at": "2026-05-13T00:00:00Z",
    }]
    mock_supabase_client.table.return_value.upsert.return_value.execute.return_value = mock_response

    # Mock encryption function
    with patch("app.api.routes.keys.encrypt_api_key") as mock_encrypt:
        mock_encrypt.return_value = "encrypted_key_data"

        # Mock auth
        with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
            response = client.post(
                "/api/keys",
                json={
                    "provider": "anthropic",
                    "api_key": "sk-ant-test-key-123"
                }
            )

    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "anthropic"
    assert "encrypted_key" not in data  # Should not return the actual key


@pytest.mark.asyncio
async def test_list_api_keys(mock_supabase_client, mock_auth_user):
    """Test listing user's API keys."""
    # Mock Supabase select response
    mock_response = MagicMock()
    mock_response.data = [
        {
            "id": "key-id-1",
            "user_id": "test-user-id-123",
            "provider": "anthropic",
            "created_at": "2026-05-13T00:00:00Z",
        },
        {
            "id": "key-id-2",
            "user_id": "test-user-id-123",
            "provider": "openai",
            "created_at": "2026-05-13T00:00:00Z",
        },
    ]
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mock auth
    with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
        response = client.get("/api/keys")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["provider"] == "anthropic"
    assert data[1]["provider"] == "openai"
    assert "encrypted_key" not in data[0]  # Should never return actual keys


@pytest.mark.asyncio
async def test_delete_api_key(mock_supabase_client, mock_auth_user):
    """Test deleting an API key."""
    # Mock Supabase delete response
    mock_response = MagicMock()
    mock_response.data = None
    mock_supabase_client.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

    # Mock auth
    with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
        response = client.delete("/api/keys/anthropic")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "API key deleted successfully"
    assert data["provider"] == "anthropic"


@pytest.mark.asyncio
async def test_test_api_key_anthropic(mock_supabase_client, mock_auth_user):
    """Test testing an Anthropic API key."""
    # Mock Supabase select to return the encrypted key
    mock_response = MagicMock()
    mock_response.data = [{
        "encrypted_key": "encrypted_anthropic_key",
    }]
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.eq.return_value.single.return_value.execute.return_value = mock_response

    # Mock decryption
    with patch("app.api.routes.keys.decrypt_api_key") as mock_decrypt:
        mock_decrypt.return_value = "sk-ant-test-key-123"

        # Mock Anthropic client
        with patch("app.api.routes.keys.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.return_value = MagicMock(content=[MagicMock(text="test")])

            # Mock auth
            with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
                response = client.post("/api/keys/anthropic/test")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["provider"] == "anthropic"


@pytest.mark.asyncio
async def test_test_api_key_invalid(mock_supabase_client, mock_auth_user):
    """Test testing an invalid API key."""
    # Mock Supabase select to return the encrypted key
    mock_response = MagicMock()
    mock_response.data = [{
        "encrypted_key": "encrypted_invalid_key",
    }]
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.eq.return_value.single.return_value.execute.return_value = mock_response

    # Mock decryption
    with patch("app.api.routes.keys.decrypt_api_key") as mock_decrypt:
        mock_decrypt.return_value = "invalid_key"

        # Mock Anthropic client to raise error
        with patch("app.api.routes.keys.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.side_effect = Exception("Invalid API key")

            # Mock auth
            with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
                response = client.post("/api/keys/anthropic/test")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["provider"] == "anthropic"
    assert "Invalid API key" in data["error"]


@pytest.mark.asyncio
async def test_save_api_key_invalid_provider():
    """Test saving an API key with invalid provider."""
    with patch("app.api.routes.keys.get_current_user", return_value={"sub": "test-user-id"}):
        response = client.post(
            "/api/keys",
            json={
                "provider": "invalid_provider",
                "api_key": "test_key"
            }
        )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_api_keys_empty(mock_supabase_client, mock_auth_user):
    """Test listing API keys when user has none."""
    # Mock Supabase select response with empty list
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mock auth
    with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
        response = client.get("/api/keys")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_delete_nonexistent_key(mock_supabase_client, mock_auth_user):
    """Test deleting a key that doesn't exist."""
    # Mock Supabase delete response
    mock_response = MagicMock()
    mock_response.data = None
    mock_supabase_client.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

    # Mock auth
    with patch("app.api.routes.keys.get_current_user", return_value=mock_auth_user):
        response = client.delete("/api/keys/anthropic")

    # Should still return 200 (idempotent delete)
    assert response.status_code == 200
