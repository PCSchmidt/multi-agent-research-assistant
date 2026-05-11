"""Cost tracking middleware for LLM usage."""

import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings


# Claude Sonnet 4 pricing (as of 2026-05-10)
CLAUDE_SONNET_4_INPUT_PRICE_PER_MTOK = 3.0  # $3 per 1M tokens
CLAUDE_SONNET_4_OUTPUT_PRICE_PER_MTOK = 15.0  # $15 per 1M tokens

# OpenAI text-embedding-3-small pricing
OPENAI_EMBEDDING_PRICE_PER_MTOK = 0.02  # $0.02 per 1M tokens


class CostTrackingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track LLM costs per request.

    Captures token usage from response headers and calculates cost.
    Logs to console in development, stores in database in production.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and track costs."""
        start_time = time.time()

        # Add request ID for tracing
        request_id = request.headers.get("x-request-id", "unknown")
        request.state.request_id = request_id
        request.state.llm_calls_count = 0
        request.state.total_input_tokens = 0
        request.state.total_output_tokens = 0

        # Process request
        response = await call_next(request)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Extract token usage from request state (set by agent during execution)
        input_tokens = getattr(request.state, "total_input_tokens", 0)
        output_tokens = getattr(request.state, "total_output_tokens", 0)
        llm_calls = getattr(request.state, "llm_calls_count", 0)

        # Calculate cost
        cost_usd = calculate_claude_cost(input_tokens, output_tokens)

        # Add cost headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Processing-Time"] = f"{processing_time:.3f}"
        response.headers["X-LLM-Calls"] = str(llm_calls)
        response.headers["X-Input-Tokens"] = str(input_tokens)
        response.headers["X-Output-Tokens"] = str(output_tokens)
        response.headers["X-Total-Tokens"] = str(input_tokens + output_tokens)
        response.headers["X-Cost-USD"] = f"{cost_usd:.6f}"

        # Log in development
        if settings.is_development and (input_tokens > 0 or output_tokens > 0):
            print(
                f"[COST] {request.method} {request.url.path} | "
                f"calls={llm_calls} | tokens={input_tokens + output_tokens} | "
                f"cost=${cost_usd:.4f} | time={processing_time:.2f}s"
            )

        return response


def calculate_claude_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost for Claude Sonnet 4 usage.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Cost in USD
    """
    input_cost = (input_tokens / 1_000_000) * CLAUDE_SONNET_4_INPUT_PRICE_PER_MTOK
    output_cost = (output_tokens / 1_000_000) * CLAUDE_SONNET_4_OUTPUT_PRICE_PER_MTOK
    return input_cost + output_cost


def calculate_embedding_cost(tokens: int) -> float:
    """
    Calculate cost for OpenAI embeddings.

    Args:
        tokens: Number of tokens embedded

    Returns:
        Cost in USD
    """
    return (tokens / 1_000_000) * OPENAI_EMBEDDING_PRICE_PER_MTOK


def check_daily_spend_alert(daily_spend_usd: float) -> bool:
    """
    Check if daily spend exceeds alert threshold.

    Args:
        daily_spend_usd: Total spend for the day in USD

    Returns:
        True if alert threshold exceeded
    """
    return daily_spend_usd >= settings.daily_spend_alert_usd
