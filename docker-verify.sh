#!/bin/bash
# Docker Compose Verification Script
# Tests that all services start correctly and are healthy

set -e

echo "=========================================="
echo "Docker Compose Verification"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "[ERROR] Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "[OK] Docker is running"

# Check if .env file exists
if [ ! -f backend/.env ]; then
    echo "[ERROR] backend/.env not found. Copy from backend/.env.example and configure."
    exit 1
fi
echo "[OK] backend/.env exists"

# Start services
echo ""
echo "Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to be healthy (max 60s)..."
sleep 10

# Check backend health
echo ""
echo "Testing backend health endpoint..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "[OK] Backend is healthy (http://localhost:8000)"
else
    echo "[ERROR] Backend health check failed"
    docker-compose logs backend
    exit 1
fi

# Check if frontend is accessible
echo ""
echo "Testing frontend..."
if curl -f http://localhost:8081 > /dev/null 2>&1; then
    echo "[OK] Frontend is accessible (http://localhost:8081)"
else
    echo "[WARN] Frontend may still be starting (this can take 30-60s for first build)"
fi

# Show running containers
echo ""
echo "Running containers:"
docker-compose ps

echo ""
echo "=========================================="
echo "[OK] Verification complete!"
echo "=========================================="
echo ""
echo "Services:"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Frontend Web: http://localhost:8081"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
