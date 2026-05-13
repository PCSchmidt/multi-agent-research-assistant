"""Cost analytics endpoints."""

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.config import settings
from app.db.client import get_supabase_admin_client

router = APIRouter(tags=["analytics"], prefix="/api/analytics")


class CostSummary(BaseModel):
    """Cost summary for a time period."""

    total_cost_usd: float = Field(..., description="Total cost in USD")
    total_tokens: int = Field(..., description="Total tokens used")
    total_queries: int = Field(..., description="Total queries executed")
    avg_cost_per_query: float = Field(..., description="Average cost per query")
    avg_tokens_per_query: float = Field(..., description="Average tokens per query")
    period_start: str = Field(..., description="Start of period (ISO datetime)")
    period_end: str = Field(..., description="End of period (ISO datetime)")


class QueryCost(BaseModel):
    """Individual query cost details."""

    session_id: str
    query: str
    cost_usd: float
    total_tokens: int
    input_tokens: int
    output_tokens: int
    llm_calls: int
    created_at: str
    langsmith_trace_url: str | None = None


class DailyCostSummary(BaseModel):
    """Daily cost aggregation."""

    date: str
    total_cost_usd: float
    total_tokens: int
    query_count: int
    avg_cost_per_query: float


@router.get("/cost/summary", response_model=CostSummary)
async def get_cost_summary(
    user_id: str | None = Query(None, description="Filter by user ID"),
    days: int = Query(7, ge=1, le=90, description="Number of days to include"),
):
    """
    Get cost summary for a time period.

    Args:
        user_id: Optional user filter
        days: Number of days to include (default: 7, max: 90)

    Returns:
        Cost summary with totals and averages
    """
    try:
        supabase = get_supabase_admin_client()

        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        # Build query
        query = supabase.table("research_sessions").select(
            "cost_usd,total_tokens,created_at"
        ).gte("created_at", start_time.isoformat()).lte(
            "created_at", end_time.isoformat()
        )

        if user_id:
            query = query.eq("user_id", user_id)

        # Execute query
        result = query.execute()

        sessions = result.data

        # Calculate aggregates
        total_cost = sum(s.get("cost_usd", 0) or 0 for s in sessions)
        total_tokens_sum = sum(s.get("total_tokens", 0) or 0 for s in sessions)
        total_queries = len(sessions)

        avg_cost = total_cost / total_queries if total_queries > 0 else 0
        avg_tokens = total_tokens_sum / total_queries if total_queries > 0 else 0

        return CostSummary(
            total_cost_usd=round(total_cost, 6),
            total_tokens=total_tokens_sum,
            total_queries=total_queries,
            avg_cost_per_query=round(avg_cost, 6),
            avg_tokens_per_query=round(avg_tokens, 2),
            period_start=start_time.isoformat(),
            period_end=end_time.isoformat(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cost summary: {str(e)}") from e


@router.get("/cost/queries", response_model=list[QueryCost])
async def get_query_costs(
    user_id: str | None = Query(None, description="Filter by user ID"),
    limit: int = Query(50, ge=1, le=500, description="Number of queries to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """
    Get individual query costs with details.

    Args:
        user_id: Optional user filter
        limit: Number of results (default: 50, max: 500)
        offset: Pagination offset

    Returns:
        List of query costs ordered by most recent
    """
    try:
        supabase = get_supabase_admin_client()

        # Build query
        query = supabase.table("research_sessions").select(
            "id,query,cost_usd,total_tokens,input_tokens,output_tokens,llm_calls_count,created_at,langsmith_trace_url"
        ).order("created_at", desc=True).range(offset, offset + limit - 1)

        if user_id:
            query = query.eq("user_id", user_id)

        # Execute query
        result = query.execute()

        # Map to response model
        queries = []
        for session in result.data:
            queries.append(
                QueryCost(
                    session_id=session["id"],
                    query=session.get("query", ""),
                    cost_usd=session.get("cost_usd", 0) or 0,
                    total_tokens=session.get("total_tokens", 0) or 0,
                    input_tokens=session.get("input_tokens", 0) or 0,
                    output_tokens=session.get("output_tokens", 0) or 0,
                    llm_calls=session.get("llm_calls_count", 0) or 0,
                    created_at=session.get("created_at", ""),
                    langsmith_trace_url=session.get("langsmith_trace_url"),
                )
            )

        return queries

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch query costs: {str(e)}") from e


@router.get("/cost/daily", response_model=list[DailyCostSummary])
async def get_daily_costs(
    user_id: str | None = Query(None, description="Filter by user ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days to include"),
):
    """
    Get daily cost aggregations.

    Args:
        user_id: Optional user filter
        days: Number of days to include (default: 30)

    Returns:
        List of daily cost summaries ordered by date descending
    """
    try:
        supabase = get_supabase_admin_client()

        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        # Build query
        query = supabase.table("research_sessions").select(
            "cost_usd,total_tokens,created_at"
        ).gte("created_at", start_time.isoformat()).lte(
            "created_at", end_time.isoformat()
        )

        if user_id:
            query = query.eq("user_id", user_id)

        result = query.execute()

        # Aggregate by day
        daily_aggregates = {}
        for session in result.data:
            date_str = session.get("created_at", "")[:10]  # Extract YYYY-MM-DD
            if date_str not in daily_aggregates:
                daily_aggregates[date_str] = {
                    "total_cost": 0,
                    "total_tokens": 0,
                    "query_count": 0,
                }

            daily_aggregates[date_str]["total_cost"] += session.get("cost_usd", 0) or 0
            daily_aggregates[date_str]["total_tokens"] += session.get("total_tokens", 0) or 0
            daily_aggregates[date_str]["query_count"] += 1

        # Convert to response model
        daily_summaries = []
        for date_str, agg in sorted(daily_aggregates.items(), reverse=True):
            avg_cost = agg["total_cost"] / agg["query_count"] if agg["query_count"] > 0 else 0
            daily_summaries.append(
                DailyCostSummary(
                    date=date_str,
                    total_cost_usd=round(agg["total_cost"], 6),
                    total_tokens=agg["total_tokens"],
                    query_count=agg["query_count"],
                    avg_cost_per_query=round(avg_cost, 6),
                )
            )

        return daily_summaries

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch daily costs: {str(e)}") from e


@router.get("/cost/budget-status")
async def get_budget_status(
    user_id: str | None = Query(None, description="Filter by user ID"),
):
    """
    Check current spend against daily budget threshold.

    Returns budget status and alert if threshold exceeded.
    """
    try:
        supabase = get_supabase_admin_client()

        # Get today's spending
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        query = supabase.table("research_sessions").select(
            "cost_usd"
        ).gte("created_at", today_start.isoformat()).lt(
            "created_at", today_end.isoformat()
        )

        if user_id:
            query = query.eq("user_id", user_id)

        result = query.execute()

        # Calculate today's total
        today_spend = sum(s.get("cost_usd", 0) or 0 for s in result.data)

        # Check against threshold
        threshold = settings.daily_spend_alert_usd
        alert = today_spend >= threshold

        return {
            "today_spend_usd": round(today_spend, 6),
            "daily_threshold_usd": threshold,
            "alert": alert,
            "percentage_used": round((today_spend / threshold * 100), 2) if threshold > 0 else 0,
            "remaining_budget_usd": max(0, threshold - today_spend),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check budget status: {str(e)}") from e
