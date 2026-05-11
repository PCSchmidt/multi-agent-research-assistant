"""Local corpus search using pgvector embeddings."""

from openai import AsyncOpenAI
from app.models.research import Paper, Author
from app.db.client import get_supabase_admin_client  # Use admin client for v0.8-v0.9 testing (bypasses RLS)
from app.config import settings

# Initialize OpenAI client for embeddings
openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


async def search_local_corpus(
    query: str,
    match_threshold: float = 0.7,
    limit: int = 5,
) -> list[Paper]:
    """
    Search local canonical papers corpus using vector similarity.

    Args:
        query: Search query to embed and match against
        match_threshold: Minimum similarity score (0.0-1.0, default 0.7)
        limit: Max number of results (capped at 5 by cost controls)

    Returns:
        List of Paper objects ranked by relevance

    Note:
        Uses OpenAI text-embedding-3-small (1536 dimensions).
        Searches against pre-seeded canonical papers in Supabase.
    """
    # Enforce cost control limit
    limit = min(limit, settings.max_papers_per_query)

    # Generate embedding for query
    embedding = await _embed_text(query)

    # Search using pgvector function
    supabase = get_supabase_admin_client()

    result = supabase.rpc(
        "search_canonical_papers",
        {
            "query_embedding": embedding,
            "match_threshold": match_threshold,
            "match_count": limit,
        },
    ).execute()

    # Parse results
    papers = []
    for row in result.data:
        # Parse authors from JSONB
        authors = [
            Author(
                name=author.get("name", "Unknown"),
                affiliations=author.get("affiliations"),
            )
            for author in row.get("authors", [])
        ]

        paper = Paper(
            paper_id=row["paper_id"],
            source="local",
            title=row["title"],
            authors=authors,
            abstract=row.get("abstract"),
            year=row.get("year"),
            venue=row.get("venue"),
            citation_count=row.get("citation_count", 0),
            url=row.get("url"),
            relevance_score=float(row["similarity"]),
        )
        papers.append(paper)

    return papers


async def _embed_text(text: str) -> list[float]:
    """
    Generate embedding for text using OpenAI.

    Args:
        text: Text to embed

    Returns:
        Embedding vector (1536 dimensions)
    """
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        encoding_format="float",
    )

    return response.data[0].embedding


async def add_canonical_paper(
    paper_id: str,
    source: str,
    title: str,
    authors: list[Author],
    abstract: str,
    year: int,
    venue: str | None = None,
    citation_count: int = 0,
    url: str | None = None,
    tags: list[str] | None = None,
    notes: str | None = None,
) -> str:
    """
    Add a paper to the canonical corpus (admin operation).

    Args:
        paper_id: Paper identifier (S2 ID, arXiv ID, DOI, etc.)
        source: Source ('s2', 'arxiv', 'manual')
        title: Paper title
        authors: List of authors
        abstract: Paper abstract (required for embedding)
        year: Publication year
        venue: Venue/conference/journal
        citation_count: Citation count
        url: Paper URL
        tags: Optional tags (e.g., ['foundational', 'survey'])
        notes: Curator notes

    Returns:
        UUID of inserted canonical paper

    Note:
        Requires admin/service role permissions.
        Automatically generates embedding from title + abstract.
    """
    from app.db.client import get_supabase_admin_client

    # Generate embedding
    embedding_text = f"{title}\n\n{abstract}"
    embedding = await _embed_text(embedding_text)

    # Insert into canonical_papers table
    supabase = get_supabase_admin_client()

    result = (
        supabase.table("canonical_papers")
        .insert(
            {
                "paper_id": paper_id,
                "source": source,
                "title": title,
                "authors": [author.model_dump() for author in authors],
                "abstract": abstract,
                "year": year,
                "venue": venue,
                "citation_count": citation_count,
                "url": url,
                "embedding": embedding,
                "tags": tags or [],
                "notes": notes,
            }
        )
        .execute()
    )

    return result.data[0]["id"]
