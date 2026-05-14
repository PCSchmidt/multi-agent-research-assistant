"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, health, keys, research
from app.config import settings
from app.middleware.cost_tracking import CostTrackingMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Runs startup and shutdown logic:
    - Startup: Validate environment variables, check DB connection
    - Shutdown: Cleanup resources
    """
    # Startup
    print(f"[STARTUP] Environment: {settings.environment}")
    print(f"[STARTUP] Debug mode: {settings.debug}")
    print(f"[STARTUP] Supabase URL: {settings.supabase_url}")
    print(f"[STARTUP] LangSmith project: {settings.langchain_project}")
    print(f"[STARTUP] Cost controls: max {settings.max_papers_per_query} papers, max {settings.max_llm_calls_per_query} LLM calls")

    # Validate critical env vars
    required_vars = [
        "supabase_url",
        "supabase_key",
        "openai_api_key",  # Still needed for embeddings
        "langchain_api_key",
    ]
    missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Validate at least one LLM provider is configured
    if not any([settings.anthropic_api_key, settings.openrouter_api_key]):
        raise ValueError("At least one LLM provider required: ANTHROPIC_API_KEY or OPENROUTER_API_KEY")

    print("[STARTUP] All required environment variables present")

    # Check database connection
    from app.db.client import check_db_connection
    db_healthy = await check_db_connection()
    if not db_healthy:
        print("[WARNING] Database connection check failed - service degraded")
    else:
        print("[STARTUP] Database connection healthy")

    yield

    # Shutdown
    print("[SHUTDOWN] Closing application")


# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Research Assistant API",
    description="Academic research assistant with LangGraph orchestration",
    version="0.7.0",
    docs_url="/docs" if settings.debug else None,  # Disable docs in production
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cost tracking middleware
app.add_middleware(CostTrackingMiddleware)

# Rate limiting middleware (v0.12)
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(health.router)

# Research endpoints (v0.8+)
app.include_router(research.router)

# Analytics endpoints (v0.12+)
app.include_router(analytics.router)

# API key management endpoints (v0.15+)
app.include_router(keys.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Multi-Agent Research Assistant API",
        "version": "0.7.0",
        "docs": "/docs" if settings.debug else "disabled",
        "health": "/health",
    }
