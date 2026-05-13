# Docker Compose Setup Guide

Complete guide for running the Multi-Agent Research Assistant using Docker Compose.

---

## Overview

Docker Compose orchestrates the complete local development environment:
- **Backend**: FastAPI + LangGraph agent (port 8000)
- **Frontend**: Expo web server (port 8081)
- **Database**: Supabase Cloud (configured via .env)

**Benefits:**
- Single-command startup (`docker-compose up`)
- Hot-reload enabled for both backend and frontend
- Isolated environment (no Python venv or npm global installs needed)
- Consistent across team members

---

## Quick Start

See [README.md](README.md) for Docker Compose quick start instructions.

For detailed setup, troubleshooting, and mobile development, refer to the sections in README.md.

---

## Verification

Run the verification script to test that all services start correctly:

```bash
bash docker-verify.sh
```

This script checks:
- Docker is running
- backend/.env exists
- Services start without errors
- Backend health endpoint responds
- Frontend is accessible

---

**Last Updated**: 2026-05-13  
**Version**: v0.13 - Docker Compose Polish
