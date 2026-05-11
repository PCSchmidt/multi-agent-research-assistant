"""Semantic Scholar API tool for searching academic papers."""

import httpx
from typing import Literal
from app.models.research import Paper, Author
from app.config import settings

S2_API_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,authors,abstract,year,venue,citationCount,externalIds,url"


async def search_semantic_scholar(
    query: str,
    year_range: str | None = None,
    limit: int = 5,
) -> list[Paper]:
    """
    Search Semantic Scholar for academic papers.

    Args:
        query: Search query (e.g., "attention mechanisms in transformers")
        year_range: Optional year filter (e.g., "2022-2024" or "2020-")
        limit: Max number of results (capped at 5 by cost controls)

    Returns:
        List of Paper objects with metadata

    Raises:
        httpx.HTTPError: If API request fails
    """
    # Enforce cost control limit
    limit = min(limit, settings.max_papers_per_query)

    # Build API request
    params = {
        "query": query,
        "fields": S2_FIELDS,
        "limit": limit,
    }
    if year_range:
        params["year"] = year_range

    headers = {}
    if settings.s2_api_key:
        headers["x-api-key"] = settings.s2_api_key

    # Make request
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{S2_API_BASE}/paper/search",
            params=params,
            headers=headers,
        )
        response.raise_for_status()

    # Parse response
    data = response.json()
    papers = []

    for item in data.get("data", []):
        # Extract authors
        authors = [
            Author(name=author.get("name", "Unknown"))
            for author in item.get("authors", [])
        ]

        # Get S2 URL or fallback to external URL
        paper_url = item.get("url")
        if not paper_url and item.get("externalIds"):
            # Try to construct DOI URL
            doi = item.get("externalIds", {}).get("DOI")
            if doi:
                paper_url = f"https://doi.org/{doi}"

        paper = Paper(
            paper_id=item["paperId"],
            source="s2",
            title=item.get("title", "Untitled"),
            authors=authors,
            abstract=item.get("abstract"),
            year=item.get("year"),
            venue=item.get("venue"),
            citation_count=item.get("citationCount", 0),
            url=paper_url,
        )
        papers.append(paper)

    return papers


async def get_paper_details_s2(paper_id: str) -> Paper | None:
    """
    Get detailed metadata for a specific paper by Semantic Scholar ID.

    Args:
        paper_id: Semantic Scholar corpus ID

    Returns:
        Paper object with full metadata, or None if not found
    """
    headers = {}
    if settings.s2_api_key:
        headers["x-api-key"] = settings.s2_api_key

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{S2_API_BASE}/paper/{paper_id}",
                params={"fields": S2_FIELDS},
                headers=headers,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    item = response.json()

    # Extract authors
    authors = [
        Author(name=author.get("name", "Unknown"))
        for author in item.get("authors", [])
    ]

    # Get URL
    paper_url = item.get("url")
    if not paper_url and item.get("externalIds"):
        doi = item.get("externalIds", {}).get("DOI")
        if doi:
            paper_url = f"https://doi.org/{doi}"

    return Paper(
        paper_id=item["paperId"],
        source="s2",
        title=item.get("title", "Untitled"),
        authors=authors,
        abstract=item.get("abstract"),
        year=item.get("year"),
        venue=item.get("venue"),
        citation_count=item.get("citationCount", 0),
        url=paper_url,
    )
