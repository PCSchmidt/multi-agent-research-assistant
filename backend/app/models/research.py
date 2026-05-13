"""Pydantic models for research domain."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Author(BaseModel):
    """Paper author."""

    name: str
    affiliations: list[str] | None = None


class Paper(BaseModel):
    """Academic paper metadata."""

    id: UUID | None = None
    paper_id: str = Field(..., description="S2 corpus ID, arXiv ID, or local ID")
    source: Literal["s2", "arxiv", "local"]

    title: str
    authors: list[Author]
    abstract: str | None = None
    year: int | None = None
    venue: str | None = None
    citation_count: int = 0
    url: str | None = None

    relevance_score: float | None = Field(None, ge=0.0, le=1.0)
    citation_number: int | None = Field(None, gt=0)


class Citation(BaseModel):
    """Citation reference in answer."""

    number: int = Field(..., gt=0)
    paper_id: str
    relevance_score: float | None = Field(None, ge=0.0, le=1.0)


class EvalScores(BaseModel):
    """Evaluation metrics."""

    # RAGAS metrics (for local corpus)
    faithfulness: float | None = Field(None, ge=0.0, le=1.0)
    answer_relevancy: float | None = Field(None, ge=0.0, le=1.0)
    context_precision: float | None = Field(None, ge=0.0, le=1.0)
    ragas_status: Literal["pending", "completed", "failed", "skipped"] | None = None

    # Manual metrics (for live search)
    citation_accuracy: float | None = Field(None, ge=0.0, le=1.0)
    has_recent_papers: bool | None = None
    coverage_gaps: list[str] | None = None
    source_diversity: Literal["balanced", "skewed", "n/a"] | None = None


class AgentStatus(BaseModel):
    """Agent execution status for timeline."""

    id: UUID | None = None
    session_id: UUID | None = None
    agent: Literal["search_s2", "search_arxiv", "search_local", "synthesize", "evaluate"]
    status: Literal["pending", "active", "completed", "failed"]

    metadata: dict | None = Field(default_factory=dict)
    error_message: str | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime | None = None


class ResearchSession(BaseModel):
    """Research session with query and results."""

    id: UUID | None = None
    user_id: UUID
    query: str
    answer: str | None = None
    status: Literal["pending", "processing", "completed", "failed"] = "pending"

    # Cost tracking
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    llm_calls_count: int = 0

    # Metadata
    langsmith_trace_url: str | None = None
    error_message: str | None = None

    created_at: datetime | None = None
    completed_at: datetime | None = None


class ResearchResponse(BaseModel):
    """Response returned to frontend."""

    session_id: UUID
    query: str
    answer: str
    citations: list[Citation]
    papers: list[Paper]
    agent_statuses: list[AgentStatus] | None = None
    eval_scores: EvalScores | None = None

    # Metadata
    langsmith_trace_url: str | None = None
    cost_usd: float = 0.0
    total_tokens: int = 0
    processing_time_seconds: float | None = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "unhealthy"]
    environment: str
    database_connected: bool
    timestamp: datetime = Field(default_factory=datetime.now)
