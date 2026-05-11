"""Research query endpoints."""

from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.agent.graph import run_research_query
from app.models.research import ResearchResponse, Paper, Citation
from app.db.client import get_supabase_admin_client

router = APIRouter(tags=["research"], prefix="/api/research")


class QueryRequest(BaseModel):
    """Research query request."""

    query: str = Field(..., min_length=10, max_length=500)
    user_id: str | None = None


class QueryResponse(BaseModel):
    """Research query response (initial)."""

    session_id: str
    status: str
    message: str


@router.post("/query", response_model=QueryResponse)
async def submit_research_query(request_body: QueryRequest, request: Request):
    """
    Submit a research query.

    The agent will:
    1. Search academic databases (Semantic Scholar, arXiv, local corpus)
    2. Retrieve relevant papers
    3. Return papers for synthesis

    Note: v0.8 returns papers only. Synthesis will be added in v0.10.
    """
    # Generate session ID
    session_id = str(uuid4())

    # For now, use a placeholder user ID (auth will be added later)
    user_id = request_body.user_id or "00000000-0000-0000-0000-000000000000"

    try:
        # Create session in database (using admin client to bypass RLS for testing)
        supabase = get_supabase_admin_client()

        session_data = {
            "id": session_id,
            "user_id": user_id,
            "query": request_body.query,
            "status": "processing",
        }

        supabase.table("research_sessions").insert(session_data).execute()

        # Run agent (v0.8: just retrieval, no synthesis yet)
        final_state = await run_research_query(
            query=request_body.query,
            session_id=session_id,
        )

        # Extract papers from tool results
        # (In v0.8, we'll parse from messages; v0.9 will track papers in state)
        papers = _extract_papers_from_state(final_state)

        # Update session with results
        update_data = {
            "status": "completed" if not final_state.get("error_message") else "failed",
            "completed_at": datetime.now().isoformat(),
            "llm_calls_count": final_state.get("llm_calls_count", 0),
            "error_message": final_state.get("error_message"),
        }

        supabase.table("research_sessions").update(update_data).eq(
            "id", session_id
        ).execute()

        # Store papers
        if papers:
            paper_records = [
                {
                    "session_id": session_id,
                    "paper_id": paper.paper_id,
                    "source": paper.source,
                    "title": paper.title,
                    "authors": [a.model_dump() for a in paper.authors],
                    "abstract": paper.abstract,
                    "year": paper.year,
                    "venue": paper.venue,
                    "citation_count": paper.citation_count,
                    "url": paper.url,
                    "relevance_score": paper.relevance_score,
                }
                for paper in papers
            ]
            supabase.table("papers").insert(paper_records).execute()

        # Track token usage in request state (for middleware)
        request.state.llm_calls_count = final_state.get("llm_calls_count", 0)
        # TODO: Extract actual token counts from LangSmith trace in v0.12

        return QueryResponse(
            session_id=session_id,
            status="completed",
            message=f"Retrieved {len(papers)} papers",
        )

    except Exception as e:
        # Update session as failed
        try:
            supabase.table("research_sessions").update(
                {
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": datetime.now().isoformat(),
                }
            ).eq("id", session_id).execute()
        except:
            pass  # Best effort

        raise HTTPException(status_code=500, detail=f"Research query failed: {str(e)}")


@router.get("/session/{session_id}", response_model=ResearchResponse)
async def get_research_session(session_id: str):
    """
    Get research session results.

    Returns papers, synthesis (when available), and metadata.
    """
    supabase = get_supabase_admin_client()

    # Fetch session
    session_result = (
        supabase.table("research_sessions")
        .select("*")
        .eq("id", session_id)
        .single()
        .execute()
    )

    if not session_result.data:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_result.data

    # Fetch papers
    papers_result = (
        supabase.table("papers").select("*").eq("session_id", session_id).execute()
    )

    papers = [
        Paper(
            paper_id=p["paper_id"],
            source=p["source"],
            title=p["title"],
            authors=[
                type("Author", (), a) for a in p.get("authors", [])
            ],  # Quick hack for now
            abstract=p.get("abstract"),
            year=p.get("year"),
            venue=p.get("venue"),
            citation_count=p.get("citation_count", 0),
            url=p.get("url"),
            relevance_score=p.get("relevance_score"),
        )
        for p in papers_result.data
    ]

    return ResearchResponse(
        session_id=session_id,
        query=session["query"],
        answer=session.get("answer") or "Synthesis pending (v0.10)",
        citations=[],  # Will be populated in v0.10
        papers=papers,
        langsmith_trace_url=session.get("langsmith_trace_url"),
        cost_usd=float(session.get("cost_usd", 0)),
        total_tokens=session.get("total_tokens", 0),
    )


def _extract_papers_from_state(state: dict) -> list[Paper]:
    """
    Extract papers from agent state (temporary implementation for v0.8).

    In v0.9, papers will be properly tracked in state.
    For now, we'll return empty list - papers are in DB via tool calls.
    """
    # TODO: Parse tool results from messages
    # For v0.8, we're verifying tool execution works
    # v0.9 will properly track papers in state
    return []
