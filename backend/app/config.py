"""Application configuration using Pydantic settings."""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # FastAPI
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Supabase
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_key: str = Field(..., description="Supabase anon key")
    supabase_service_role_key: str = Field(
        ..., description="Supabase service role key (for admin operations)"
    )

    # Anthropic (Claude) - Optional when using OpenRouter
    anthropic_api_key: str | None = Field(
    default=None, description="Anthropic API key (optional, falls back to OpenRouter)"
)

    # OpenAI (Embeddings)
    openai_api_key: str = Field(..., description="OpenAI API key")

    # Semantic Scholar (optional)
    semantic_scholar_api_key: str | None = Field(
        default=None, description="Semantic Scholar API key (optional)"
    )

    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_endpoint: str = "https://api.smith.langchain.com"
    langchain_api_key: str = Field(..., description="LangSmith API key")
    langchain_project: str = "multi-agent-research-assistant"

    # Model Configuration
    default_model: str = Field(
        default="anthropic/claude-3.5-haiku",
        description="Default LLM model (OpenRouter format: provider/model-name)",
    )
    openrouter_api_key: str | None = Field(
        default=None, description="OpenRouter API key (optional, for multi-provider access)"
    )


    # Cost Controls
    max_papers_per_query: int = Field(
        default=5, ge=1, le=20, description="Max papers to retrieve per query"
    )
    max_llm_calls_per_query: int = Field(
        default=10, ge=1, le=50, description="Max LLM calls per query (circuit breaker)"
    )
    daily_spend_alert_usd: float = Field(
        default=10.0, ge=0, description="Daily spend threshold for alerts (USD)"
    )
    rate_limit_queries_per_hour: int = Field(
        default=10, ge=1, description="Rate limit: queries per hour per user"
    )

    # CORS
    cors_origins: str = Field(
        default="http://localhost:8081,http://localhost:3000,http://localhost:19006",
        description="Comma-separated CORS origins",
    )

    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> list[str]:
        """Parse comma-separated CORS origins into list."""
        return [origin.strip() for origin in v.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"


# Global settings instance
settings = Settings()
