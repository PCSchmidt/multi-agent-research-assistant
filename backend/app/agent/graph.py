"""LangGraph research agent with ReAct pattern."""

from datetime import datetime
from uuid import uuid4
import json
from contextvars import ContextVar
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from app.agent.state import ResearchState
from app.config import settings
from app.models.research import Paper, AgentStatus, Author
from app.tools.semantic_scholar import search_semantic_scholar
from app.tools.arxiv_search import search_arxiv
from app.tools.local_corpus import search_local_corpus


# Module-level storage for papers during tool execution
# This allows tools to store Paper objects while returning formatted text to LLM
# Using a simple list since LangGraph tools run sequentially (not concurrently)
_paper_storage: list[Paper] = []


# Define tools with LangChain @tool decorator
@tool
async def search_s2_tool(query: str, year_range: str | None = None) -> str:
    """
    Search Semantic Scholar for academic papers.

    Gracefully handles failures - returns error message instead of crashing.

    Args:
        query: Search query for papers
        year_range: Optional year filter (e.g., "2022-2024")

    Returns:
        JSON string with paper results or error message
    """
    try:
        papers = await search_semantic_scholar(query, year_range=year_range, limit=5)

        # Store papers for hybrid merge
        _paper_storage.extend(papers)

        return _format_papers_for_llm(papers)
    except Exception as e:
        error_msg = f"Semantic Scholar search failed: {str(e)}"
        print(f"[TOOL ERROR] {error_msg}")  # Log for debugging
        return f"⚠️ {error_msg}\n\nContinuing with other sources..."


@tool
async def search_arxiv_tool(query: str, category: str | None = None) -> str:
    """
    Search arXiv for preprints and papers.

    Gracefully handles failures - returns error message instead of crashing.

    Args:
        query: Search query
        category: Optional arXiv category (e.g., "cs.AI", "cs.LG")

    Returns:
        JSON string with paper results or error message
    """
    try:
        papers = await search_arxiv(query, category=category, limit=5)

        # Store papers for hybrid merge
        _paper_storage.extend(papers)

        return _format_papers_for_llm(papers)
    except Exception as e:
        error_msg = f"arXiv search failed: {str(e)}"
        print(f"[TOOL ERROR] {error_msg}")  # Log for debugging
        return f"⚠️ {error_msg}\n\nContinuing with other sources..."


@tool
async def search_local_tool(query: str) -> str:
    """
    Search local canonical papers corpus using semantic search.

    Gracefully handles failures - returns error message instead of crashing.

    Args:
        query: Search query

    Returns:
        JSON string with paper results or error message
    """
    try:
        papers = await search_local_corpus(query, limit=5)

        # Store papers for hybrid merge
        _paper_storage.extend(papers)

        return _format_papers_for_llm(papers)
    except Exception as e:
        error_msg = f"Local corpus search failed: {str(e)}"
        print(f"[TOOL ERROR] {error_msg}")  # Log for debugging
        return f"⚠️ {error_msg}\n\nContinuing with other sources..."


def _format_papers_for_llm(papers: list[Paper]) -> str:
    """Format papers as concise text for LLM context."""
    if not papers:
        return "No papers found."

    result = []
    for i, paper in enumerate(papers, 1):
        authors_str = ", ".join([a.name for a in paper.authors[:3]])
        if len(paper.authors) > 3:
            authors_str += " et al."

        paper_str = f"""
{i}. {paper.title}
   Authors: {authors_str}
   Year: {paper.year or 'Unknown'}
   Venue: {paper.venue or 'Unknown'}
   Citations: {paper.citation_count}
   Abstract: {paper.abstract[:300] if paper.abstract else 'No abstract'}...
   Source: {paper.source.upper()}
   ID: {paper.paper_id}
"""
        result.append(paper_str.strip())

    return "\n\n".join(result)


# System prompt for research agent
RESEARCH_AGENT_PROMPT = """You are an academic research assistant helping users find and synthesize research papers.

Your workflow:
1. Understand the user's research question
2. Search for relevant papers using available tools:
   - search_s2_tool: Semantic Scholar (good for citations, recent papers)
   - search_arxiv_tool: arXiv preprints (good for latest work)
   - search_local_tool: Canonical papers corpus (foundational works)
3. Call tools to retrieve papers (aim for 3-5 relevant papers)
4. Once you have enough papers, STOP searching and synthesize your findings

Search Guidelines:
- For "recent" queries, use year_range="2022-2024" with Semantic Scholar
- For foundational concepts, search local corpus first
- Don't over-search - 3-5 good papers is enough
- Focus on highly-cited, recent, or canonical works

Synthesis Guidelines:
After retrieving papers, provide a clear, well-structured answer that:
1. Directly addresses the user's question
2. Synthesizes findings from the papers you found
3. Uses inline citations in [1], [2] format to reference papers
4. Provides context and explains key concepts
5. Highlights recent advancements or consensus findings

Citation Format:
- Use numbered citations [1], [2], [3] inline where claims are made
- Each number corresponds to a paper from your search results
- Multiple citations for one claim: [1, 2]
- Place citations immediately after the relevant statement

Example synthesis:
"Recent work has shown that efficient attention mechanisms can reduce computational complexity from O(n²) to O(n) [1, 2]. The Mamba architecture achieves this through selective state spaces [1], while FlashAttention uses block-sparse patterns [3]. These approaches maintain performance while enabling longer context windows [1, 2, 3]."

Begin synthesizing once you have 3-5 relevant papers. Do not search indefinitely.
"""


def create_research_agent() -> StateGraph:
    """
    Create LangGraph research agent with ReAct pattern.

    The agent can use search tools to find papers and tracks
    its progress via agent statuses.

    Returns:
        Compiled StateGraph ready for invocation
    """
    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=settings.anthropic_api_key,
        temperature=0.1,
    )

    # Bind tools to LLM
    tools = [search_s2_tool, search_arxiv_tool, search_local_tool]
    llm_with_tools = llm.bind_tools(tools)

    # Define agent node
    async def agent_node(state: ResearchState) -> ResearchState:
        """
        Agent reasoning node - decides which tool to call next.
        """
        print(f"[AGENT_NODE] Entry: llm_calls={state['llm_calls_count']}, messages={len(state['messages'])}")

        # Check circuit breaker
        if state["llm_calls_count"] >= settings.max_llm_calls_per_query:
            print(f"[AGENT_NODE] Circuit breaker triggered")
            return {
                **state,
                "should_continue": False,
                "error_message": f"Circuit breaker: max {settings.max_llm_calls_per_query} LLM calls reached",
            }

        # Invoke LLM
        messages = state["messages"]
        print(f"[AGENT_NODE] Invoking LLM...")
        response = await llm_with_tools.ainvoke(messages)

        # Increment LLM call count
        llm_calls_count = state["llm_calls_count"] + 1

        # Check if agent wants to stop (no tool calls)
        should_continue = bool(response.tool_calls)
        print(f"[AGENT_NODE] LLM response: tool_calls={len(response.tool_calls) if response.tool_calls else 0}, should_continue={should_continue}")
        if response.tool_calls:
            print(f"[AGENT_NODE] Tool calls: {[tc.get('name') for tc in response.tool_calls]}")

        return {
            **state,
            "messages": state["messages"] + [response],
            "llm_calls_count": llm_calls_count,
            "should_continue": should_continue,
        }

    # Define tool execution node
    tool_node = ToolNode(tools)

    # Define paper extraction node (runs after tools to collect papers)
    async def extract_papers_node(state: ResearchState) -> ResearchState:
        """
        Extract papers from tool results and merge them.

        Implements hybrid retrieval: combines S2, arXiv, and local corpus results.
        """
        # Get papers from storage (populated during tool execution)
        new_papers = _paper_storage.copy()

        # Combine with existing papers from state
        all_papers = state.get("papers", []) + new_papers

        # Clear storage for next iteration
        _paper_storage.clear()

        # Deduplicate papers by paper_id (prefer first occurrence)
        seen_ids = set()
        unique_papers = []
        for paper in all_papers:
            if paper.paper_id not in seen_ids:
                seen_ids.add(paper.paper_id)
                unique_papers.append(paper)

        # Sort by: relevance score (desc), then citation count (desc), then year (desc)
        # This prioritizes: local corpus matches > highly cited > recent
        unique_papers.sort(
            key=lambda p: (
                p.relevance_score or 0,  # Local corpus papers have this
                p.citation_count or 0,   # All papers have this
                p.year or 0,             # Prefer recent papers
            ),
            reverse=True,
        )

        # Limit to max papers
        unique_papers = unique_papers[:settings.max_papers_per_query]

        return {
            **state,
            "papers": unique_papers,
        }

    # Define router
    def should_continue_routing(state: ResearchState) -> str:
        """Route to tools or end based on agent decision."""
        if not state.get("should_continue", True):
            return "end"
        if state.get("error_message"):
            return "end"
        return "continue"

    # Build graph
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("extract_papers", extract_papers_node)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges(
        "agent",
        should_continue_routing,
        {
            "continue": "tools",
            "end": END,
        },
    )
    workflow.add_edge("tools", "extract_papers")
    workflow.add_edge("extract_papers", "agent")

    # Compile
    return workflow.compile()


async def run_research_query(
    query: str,
    session_id: str | None = None,
) -> ResearchState:
    """
    Run research query through agent.

    Args:
        query: User's research question
        session_id: Optional session ID for tracking

    Returns:
        Final agent state with papers and synthesis
    """
    # Clear paper storage from any previous runs
    _paper_storage.clear()

    # Create agent
    agent = create_research_agent()

    # Initialize state
    initial_state: ResearchState = {
        "messages": [
            SystemMessage(content=RESEARCH_AGENT_PROMPT),
            HumanMessage(content=query),
        ],
        "query": query,
        "papers": [],
        "citations": [],
        "synthesis": None,
        "eval_scores": None,
        "agent_statuses": [],
        "llm_calls_count": 0,
        "should_continue": True,
        "error_message": None,
    }

    # Run agent
    final_state = await agent.ainvoke(initial_state)

    return final_state
