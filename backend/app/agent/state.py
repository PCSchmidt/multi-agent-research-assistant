"""Agent state definition for LangGraph."""

from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from app.models.research import Paper, Citation, EvalScores, AgentStatus


class ResearchState(TypedDict):
    """
    State for research agent graph.

    Uses LangGraph's type-annotated state for message history
    and custom fields for research artifacts.
    """

    # Chat messages (with reducer to append)
    messages: Annotated[list[BaseMessage], add_messages]

    # Research artifacts
    query: str
    papers: list[Paper]
    citations: list[Citation]
    synthesis: str | None
    eval_scores: EvalScores | None
    agent_statuses: list[AgentStatus]

    # Control flow
    llm_calls_count: int
    should_continue: bool
    error_message: str | None
