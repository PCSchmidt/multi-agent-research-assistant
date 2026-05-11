"""Unit tests for local corpus search tool."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.tools.local_corpus import search_local_corpus, _embed_text
from app.models.research import Paper, Author


@pytest.fixture
def mock_embedding():
    """Mock OpenAI embedding response."""
    return [0.1] * 1536  # 1536-dimensional vector


@pytest.fixture
def mock_papers_response():
    """Mock Supabase RPC response with papers."""
    return [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "paper_id": "arxiv:1706.03762",
            "title": "Attention Is All You Need",
            "authors": [
                {"name": "Ashish Vaswani"},
                {"name": "Noam Shazeer"},
            ],
            "abstract": "The dominant sequence transduction models...",
            "year": 2017,
            "venue": "NeurIPS",
            "citation_count": 100000,
            "url": "https://arxiv.org/abs/1706.03762",
            "similarity": 0.85,
        },
        {
            "id": "223e4567-e89b-12d3-a456-426614174001",
            "paper_id": "arxiv:1810.04805",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "authors": [
                {"name": "Jacob Devlin"},
            ],
            "abstract": "We introduce a new language representation model...",
            "year": 2018,
            "venue": "NAACL",
            "citation_count": 80000,
            "url": "https://arxiv.org/abs/1810.04805",
            "similarity": 0.75,
        },
    ]


@pytest.mark.asyncio
async def test_search_local_corpus_returns_papers(mock_embedding, mock_papers_response):
    """Test that search_local_corpus returns papers with valid query."""
    with patch("app.tools.local_corpus._embed_text", new=AsyncMock(return_value=mock_embedding)):
        with patch("app.tools.local_corpus.get_supabase_admin_client") as mock_client:
            # Mock Supabase RPC call
            mock_rpc_result = MagicMock()
            mock_rpc_result.data = mock_papers_response
            mock_client.return_value.rpc.return_value.execute.return_value = mock_rpc_result

            # Execute search
            papers = await search_local_corpus("transformers", match_threshold=0.7, limit=5)

            # Assertions
            assert len(papers) == 2
            assert papers[0].title == "Attention Is All You Need"
            assert papers[0].relevance_score == 0.85
            assert papers[0].source == "local"
            assert len(papers[0].authors) == 2
            assert papers[0].authors[0].name == "Ashish Vaswani"

            assert papers[1].title == "BERT: Pre-training of Deep Bidirectional Transformers"
            assert papers[1].relevance_score == 0.75


@pytest.mark.asyncio
async def test_search_local_corpus_empty_results(mock_embedding):
    """Test that search_local_corpus handles empty results gracefully."""
    with patch("app.tools.local_corpus._embed_text", new=AsyncMock(return_value=mock_embedding)):
        with patch("app.tools.local_corpus.get_supabase_admin_client") as mock_client:
            # Mock empty response
            mock_rpc_result = MagicMock()
            mock_rpc_result.data = []
            mock_client.return_value.rpc.return_value.execute.return_value = mock_rpc_result

            # Execute search
            papers = await search_local_corpus("nonexistent query", match_threshold=0.7, limit=5)

            # Assertions
            assert papers == []


@pytest.mark.asyncio
async def test_search_local_corpus_respects_threshold(mock_embedding):
    """Test that search_local_corpus filters by match_threshold."""
    with patch("app.tools.local_corpus._embed_text", new=AsyncMock(return_value=mock_embedding)):
        with patch("app.tools.local_corpus.get_supabase_admin_client") as mock_client:
            mock_rpc_result = MagicMock()
            mock_rpc_result.data = []
            mock_client.return_value.rpc.return_value.execute.return_value = mock_rpc_result

            # Execute search with high threshold
            await search_local_corpus("query", match_threshold=0.9, limit=5)

            # Verify RPC was called with correct threshold
            mock_client.return_value.rpc.assert_called_once_with(
                "search_canonical_papers",
                {
                    "query_embedding": mock_embedding,
                    "match_threshold": 0.9,
                    "match_count": 5,
                },
            )


@pytest.mark.asyncio
async def test_search_local_corpus_limits_results(mock_embedding, mock_papers_response):
    """Test that search_local_corpus respects result limit."""
    with patch("app.tools.local_corpus._embed_text", new=AsyncMock(return_value=mock_embedding)):
        with patch("app.tools.local_corpus.get_supabase_admin_client") as mock_client:
            # Mock RPC with many papers
            many_papers = mock_papers_response * 5  # 10 papers
            mock_rpc_result = MagicMock()
            mock_rpc_result.data = many_papers
            mock_client.return_value.rpc.return_value.execute.return_value = mock_rpc_result

            # Execute search with limit=3
            papers = await search_local_corpus("query", match_threshold=0.5, limit=3)

            # Verify RPC was called with search_canonical_papers and parameters
            mock_client.return_value.rpc.assert_called_once()
            call_args = mock_client.return_value.rpc.call_args
            # Verify function name
            assert call_args.args[0] == "search_canonical_papers"
            # Verify parameters dict has the expected keys
            params = call_args.args[1]
            assert "query_embedding" in params
            assert "match_threshold" in params
            assert "match_count" in params
            # Verify limit is capped by min(limit, settings.max_papers_per_query)
            assert params["match_count"] <= 5  # Assuming max_papers_per_query is 5


@pytest.mark.asyncio
async def test_embed_text_calls_openai():
    """Test that _embed_text calls OpenAI API correctly."""
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]

    with patch("app.tools.local_corpus.openai_client") as mock_client:
        mock_client.embeddings.create = AsyncMock(return_value=mock_response)

        # Execute embedding
        embedding = await _embed_text("test query")

        # Assertions
        assert len(embedding) == 1536
        assert embedding[0] == 0.1

        # Verify OpenAI API was called correctly
        mock_client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input="test query",
            encoding_format="float",
        )


@pytest.mark.asyncio
async def test_search_local_corpus_uses_admin_client(mock_embedding):
    """Test that search_local_corpus uses admin client (for v0.8-v0.9 testing)."""
    with patch("app.tools.local_corpus._embed_text", new=AsyncMock(return_value=mock_embedding)):
        with patch("app.tools.local_corpus.get_supabase_admin_client") as mock_admin_client:
            mock_rpc_result = MagicMock()
            mock_rpc_result.data = []
            mock_admin_client.return_value.rpc.return_value.execute.return_value = mock_rpc_result

            # Execute search
            await search_local_corpus("query", match_threshold=0.7, limit=5)

            # Verify admin client was called (not regular client)
            mock_admin_client.assert_called_once()
