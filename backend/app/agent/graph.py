"""LangGraph research agent with ReAct pattern."""

from datetime import datetime
from uuid import uuid4
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from app.agent.state import ResearchState
from app.config import settings
from app.models.research import Paper, AgentStatus
from app.tools.semantic_scholar import search_semantic_scholar
from app.tools.arxiv_search import search_arxiv
from app.tools.local_corpus import search_local_corpus


# Define tools with LangChain @tool decorator
@tool
async def search_s2_tool(query: str, year_range: str | None = None) -> str:
    """
    Search Semantic Scholar for academic papers.

    Args:
        query: Search query for papers
        year_range: Optional year filter (e.g., "2022-2024")

    Returns:
        JSON string with paper results
    """
    papers = await search_semantic_scholar(query, year_range=year_range, limit=5)
    return _format_papers_for_llm(papers)


@tool
async def search_arxiv_tool(query: str, category: str | None = None) -> str:
    """
    Search arXiv for preprints and papers.

    Args:
        query: Search query
        category: Optional arXiv category (e.g., "cs.AI", "cs.LG")

    Returns:
        JSON string with paper results
    """
    papers = await search_arxiv(query, category=category, limit=5)
    return _format_papers_for_llm(papers)


@tool
async def search_local_tool(query: str) -> str:
    """
    Search local canonical papers corpus using semantic search.

    Args:
        query: Search query

    Returns:
        JSON string with paper results
    """
    papers = await search_local_corpus(query, limit=5)
    return _format_papers_for_llm(papers)


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
3. Call tools to retrieve papers
4. Once you have enough papers (3-5), STOP searching and prepare to synthesize

Guidelines:
- For "recent" queries, use year_range="2022-2024" with Semantic Scholar
- For foundational concepts, search local corpus first
- Don't over-search - 3-5 good papers is enough
- Focus on highly-cited, recent, or canonical works

When you're done searching, say "I have retrieved sufficient papers" and list what you found.
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
        # Check circuit breaker
        if state["llm_calls_count"] >= settings.max_llm_calls_per_query:
            return {
                **state,
                "should_continue": False,
                "error_message": f"Circuit breaker: max {settings.max_llm_calls_per_query} LLM calls reached",
            }

        # Invoke LLM
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)

        # Increment LLM call count
        llm_calls_count = state["llm_calls_count"] + 1

        # Check if agent wants to stop (no tool calls)
        should_continue = bool(response.tool_calls)

        return {
            **state,
            "messages": state["messages"] + [response],
            "llm_calls_count": llm_calls_count,
            "should_continue": should_continue,
        }

    # Define tool execution node
    tool_node = ToolNode(tools)

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
    workflow.add_edge("tools", "agent")

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
