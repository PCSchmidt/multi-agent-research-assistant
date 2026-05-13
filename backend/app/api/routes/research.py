"""Research query endpoints."""

import json
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from app.agent.graph import RESEARCH_AGENT_PROMPT, create_research_agent, run_research_query
from app.agent.state import ResearchState
from app.db.client import get_supabase_admin_client
from app.evaluation.eval_task import spawn_evaluation_task
from app.middleware.langsmith_callback import LangSmithTraceCallback
from app.models.research import Paper, ResearchResponse

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


def _format_sse_event(event: str, data: dict) -> str:
    """Format data as Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@router.post("/stream")
async def stream_research_query(request_body: QueryRequest):
    """
    Stream research query execution via Server-Sent Events.

    Events emitted:
    - status: Agent status updates (searching, synthesizing, etc.)
    - paper: Paper found
    - synthesis: Synthesis chunk (partial answer)
    - done: Query complete with final results
    - error: Error occurred
    """
    session_id = str(uuid4())
    user_id = request_body.user_id or "00000000-0000-0000-0000-000000000000"

    async def event_generator():
        print(f"[EVENT_GEN] Starting event generator for query: {request_body.query}")
        try:
            # Create session in database
            supabase = get_supabase_admin_client()
            session_data = {
                "id": session_id,
                "user_id": user_id,
                "query": request_body.query,
                "status": "processing",
            }
            supabase.table("research_sessions").insert(session_data).execute()
            print(f"[DB] Session created: {session_id}")

            # Send initial status
            print("[EVENT_GEN] Yielding initial status event")
            yield _format_sse_event(
                "status",
                {"message": "Starting research query...", "session_id": session_id},
            )

            # Create agent
            print("[EVENT_GEN] Creating research agent...")
            agent = create_research_agent()
            print(f"[EVENT_GEN] Agent created: {type(agent)}")

            # Initialize state
            print("[EVENT_GEN] Initializing agent state...")
            initial_state: ResearchState = {
                "messages": [
                    SystemMessage(content=RESEARCH_AGENT_PROMPT),
                    HumanMessage(content=request_body.query),
                ],
                "query": request_body.query,
                "papers": [],
                "citations": [],
                "synthesis": None,
                "eval_scores": None,
                "agent_statuses": [],
                "llm_calls_count": 0,
                "should_continue": True,
                "error_message": None,
            }
            print(f"[EVENT_GEN] State initialized with {len(initial_state['messages'])} messages")

            # Stream agent execution with LangSmith metadata
            print("[STREAM] Starting agent.ainvoke()...")

            # Create callback handler to capture trace info and token usage
            trace_callback = LangSmithTraceCallback()

            # Configure LangSmith metadata for tracing
            config = {
                "metadata": {
                    "user_id": user_id,
                    "session_id": session_id,
                    "query": request_body.query,
                    "tools_available": ["search_s2", "search_arxiv", "search_local"],
                },
                "tags": ["research_query", "multi_agent"],
                "callbacks": [trace_callback],
            }

            # Use ainvoke to get full final state (astream chunks are partial updates)
            final_state = await agent.ainvoke(initial_state, config=config)
            print(f"[STREAM] Agent finished. Papers: {len(final_state.get('papers', []))}, LLM calls: {final_state.get('llm_calls_count', 0)}")

            # Get trace info from callback
            trace_info = trace_callback.get_trace_info()
            cost_usd = trace_callback.calculate_cost_usd()

            print(f"[LANGSMITH] Trace URL: {trace_info['trace_url']}")
            print(f"[COST] Tokens: {trace_info['total_tokens']} ({trace_info['input_tokens']} in, {trace_info['output_tokens']} out)")
            print(f"[COST] Estimated cost: ${cost_usd:.6f}")

            # Update session with trace URL and cost data
            supabase.table("research_sessions").update({
                "status": "completed",
                "langsmith_trace_url": trace_info["trace_url"],
                "total_tokens": trace_info["total_tokens"],
                "input_tokens": trace_info["input_tokens"],
                "output_tokens": trace_info["output_tokens"],
                "cost_usd": cost_usd,
                "llm_calls_count": trace_info["llm_calls"],
                "completed_at": datetime.now().isoformat(),
            }).eq("id", session_id).execute()
            print("[DB] Session updated with trace URL and cost data")

            # For now, just yield the final result
            # TODO v0.12: Switch back to astream() and implement proper state accumulation for real-time updates

            # Extract papers and synthesis from final state
            papers = final_state.get("papers", []) if final_state else []
            synthesis = final_state.get("synthesis") if final_state else None

            # If no explicit synthesis, extract from last AI message
            if not synthesis and final_state and "messages" in final_state:
                messages = final_state["messages"]
                print(f"[EXTRACT] Total messages: {len(messages)}")
                for i, msg in enumerate(reversed(messages)):
                    msg_type = type(msg).__name__
                    content_preview = msg.content[:100] if hasattr(msg, "content") else "no content"
                    print(f"[EXTRACT] Message {len(messages)-i-1} ({msg_type}): {content_preview}...")
                    if hasattr(msg, "content") and isinstance(msg.content, str):
                        # Look for last AI message (not system, not tool)
                        if msg_type == "AIMessage" and len(msg.content) > 100:
                            synthesis = msg.content
                            print(f"[EXTRACT] Using AIMessage as synthesis (length: {len(msg.content)})")
                            break

            # Spawn background evaluation task
            # This runs asynchronously and logs results to eval_results table
            if synthesis and papers:
                print(f"[EVAL] Spawning evaluation task for session {session_id}")
                spawn_evaluation_task(
                    session_id=session_id,
                    query=request_body.query,
                    answer=synthesis,
                    papers=papers,
                    run_ragas=True,  # Run RAGAS for all queries
                    run_manual=True,  # Compute automated manual metrics
                )

            # Send completion event
            yield _format_sse_event(
                "done",
                {
                    "session_id": session_id,
                    "papers_count": len(papers),
                    "synthesis": synthesis or "No synthesis generated",
                    "llm_calls": final_state.get("llm_calls_count", 0) if final_state else 0,
                },
            )

        except Exception as e:
            yield _format_sse_event("error", {"message": str(e)})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )
