"""arXiv API tool for searching preprints."""

import httpx
import xml.etree.ElementTree as ET
from app.models.research import Paper, Author
from app.config import settings

ARXIV_API_BASE = "http://export.arxiv.org/api/query"


async def search_arxiv(
    query: str,
    category: str | None = None,
    limit: int = 5,
) -> list[Paper]:
    """
    Search arXiv for preprints and papers.

    Args:
        query: Search query (supports arXiv query syntax)
        category: Optional arXiv category filter (e.g., "cs.AI", "cs.LG")
        limit: Max number of results (capped at 5 by cost controls)

    Returns:
        List of Paper objects with metadata

    Raises:
        httpx.HTTPError: If API request fails

    Note:
        arXiv API is free and doesn't require authentication.
        Query syntax: https://info.arxiv.org/help/api/user-manual.html#query_details
    """
    # Enforce cost control limit
    limit = min(limit, settings.max_papers_per_query)

    # Build search query
    search_query = f"all:{query}"
    if category:
        search_query = f"cat:{category} AND {search_query}"

    # Make request
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(ARXIV_API_BASE, params=params)
        response.raise_for_status()

    # Parse XML response
    papers = _parse_arxiv_response(response.text)
    return papers[:limit]


def _parse_arxiv_response(xml_text: str) -> list[Paper]:
    """
    Parse arXiv API XML response into Paper objects.

    Args:
        xml_text: XML response from arXiv API

    Returns:
        List of Paper objects
    """
    papers = []
    root = ET.fromstring(xml_text)

    # arXiv uses Atom namespace
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    for entry in root.findall("atom:entry", ns):
        # Extract arXiv ID from URL
        arxiv_url = entry.find("atom:id", ns)
        if arxiv_url is not None:
            arxiv_id = arxiv_url.text.split("/")[-1]  # e.g., "2103.00020v1" or "2103.00020"
            # Strip version suffix if present
            if "v" in arxiv_id:
                arxiv_id = arxiv_id.split("v")[0]
        else:
            continue  # Skip entries without ID

        # Title
        title_elem = entry.find("atom:title", ns)
        title = title_elem.text.strip() if title_elem is not None else "Untitled"

        # Authors
        authors = []
        for author_elem in entry.findall("atom:author", ns):
            name_elem = author_elem.find("atom:name", ns)
            if name_elem is not None:
                authors.append(Author(name=name_elem.text.strip()))

        # Abstract
        summary_elem = entry.find("atom:summary", ns)
        abstract = summary_elem.text.strip() if summary_elem is not None else None

        # Published year
        published_elem = entry.find("atom:published", ns)
        year = None
        if published_elem is not None:
            try:
                year = int(published_elem.text[:4])  # Extract year from ISO timestamp
            except (ValueError, IndexError):
                pass

        # Category (primary)
        category_elem = entry.find("atom:category", ns)
        venue = None
        if category_elem is not None:
            category = category_elem.get("term", "")
            venue = f"arXiv:{category}" if category else "arXiv"
        else:
            venue = "arXiv"

        # URL
        paper_url = f"https://arxiv.org/abs/{arxiv_id}"

        paper = Paper(
            paper_id=arxiv_id,
            source="arxiv",
            title=title,
            authors=authors,
            abstract=abstract,
            year=year,
            venue=venue,
            citation_count=0,  # arXiv doesn't provide citation counts
            url=paper_url,
        )
        papers.append(paper)

    return papers
