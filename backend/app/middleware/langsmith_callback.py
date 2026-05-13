"""LangSmith callback handler for capturing trace URLs and token usage."""

from typing import Any
from uuid import UUID

from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult


class LangSmithTraceCallback(AsyncCallbackHandler):
    """
    Callback handler to capture LangSmith trace information and token usage.

    Captures:
    - run_id for constructing trace URLs
    - Token usage (input/output tokens)
    - LLM calls count
    """

    def __init__(self):
        """Initialize callback handler."""
        super().__init__()
        self.run_id: UUID | None = None
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.llm_calls = 0
        self.trace_url: str | None = None

    async def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Capture the root run_id when the chain starts."""
        if parent_run_id is None:  # This is the root run
            self.run_id = run_id
            # Construct LangSmith trace URL
            # Public URL format: https://smith.langchain.com/public/{run_id}/r
            self.trace_url = f"https://smith.langchain.com/public/{run_id}/r"
            print(f"[LANGSMITH] Root run_id captured: {run_id}")
            print(f"[LANGSMITH] Trace URL: {self.trace_url}")

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        """Capture token usage from LLM responses."""
        self.llm_calls += 1

        # Extract token usage from response
        if response.llm_output and "usage" in response.llm_output:
            usage = response.llm_output["usage"]
            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)

            self.input_tokens += input_tokens
            self.output_tokens += output_tokens
            self.total_tokens += input_tokens + output_tokens

            print(f"[LANGSMITH] LLM call #{self.llm_calls}: {input_tokens} in, {output_tokens} out")

    def get_trace_info(self) -> dict[str, Any]:
        """
        Get captured trace information.

        Returns:
            Dictionary with trace URL and token usage
        """
        return {
            "run_id": str(self.run_id) if self.run_id else None,
            "trace_url": self.trace_url,
            "total_tokens": self.total_tokens,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "llm_calls": self.llm_calls,
        }

    def calculate_cost_usd(self) -> float:
        """
        Calculate cost in USD based on token usage.

        Uses Claude Sonnet 4 pricing:
        - Input: $3.00 per 1M tokens
        - Output: $15.00 per 1M tokens

        Returns:
            Cost in USD
        """
        input_cost = (self.input_tokens / 1_000_000) * 3.00
        output_cost = (self.output_tokens / 1_000_000) * 15.00
        return input_cost + output_cost
