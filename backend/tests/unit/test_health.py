"""Tests for health check endpoint."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Test /health endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "environment" in data
    assert "database_connected" in data
    assert "timestamp" in data

    # Status should be healthy or unhealthy
    assert data["status"] in ["healthy", "unhealthy"]


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "0.7.0"
