"""Tests for Semantic Scholar tool."""

from unittest.mock import AsyncMock, patch

import pytest

from app.tools.semantic_scholar import get_paper_details_s2, search_semantic_scholar


@pytest.mark.asyncio
async def test_search_semantic_scholar_success():
    """Test successful paper search."""
    mock_response = {
        "data": [
            {
                "paperId": "204e3073870fae3d05bcbc2f6a8e263d9b72e776",
                "title": "Attention Is All You Need",
                "authors": [
                    {"name": "Ashish Vaswani"},
                    {"name": "Noam Shazeer"},
                ],
                "abstract": "The dominant sequence transduction models...",
                "year": 2017,
                "venue": "NeurIPS",
                "citationCount": 50000,
                "url": "https://www.semanticscholar.org/paper/...",
                "externalIds": {"DOI": "10.5555/3295222.3295349"},
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: mock_response,
        )
        mock_get.return_value.raise_for_status = lambda: None

        papers = await search_semantic_scholar("transformers")

        assert len(papers) == 1
        assert papers[0].title == "Attention Is All You Need"
        assert papers[0].source == "s2"
        assert papers[0].year == 2017
        assert len(papers[0].authors) == 2


@pytest.mark.asyncio
async def test_search_semantic_scholar_with_year_filter():
    """Test search with year range filter."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"data": []},
        )
        mock_get.return_value.raise_for_status = lambda: None

        _ = await search_semantic_scholar("attention", year_range="2022-2024")

        # Verify year parameter was passed
        call_args = mock_get.call_args
        assert "year" in call_args.kwargs["params"]
        assert call_args.kwargs["params"]["year"] == "2022-2024"


@pytest.mark.asyncio
async def test_search_semantic_scholar_empty_results():
    """Test handling of no results."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"data": []},
        )
        mock_get.return_value.raise_for_status = lambda: None

        papers = await search_semantic_scholar("nonexistent query xyz")

        assert papers == []


@pytest.mark.asyncio
async def test_get_paper_details_success():
    """Test fetching paper details by ID."""
    mock_paper = {
        "paperId": "test-id",
        "title": "Test Paper",
        "authors": [{"name": "Test Author"}],
        "abstract": "Test abstract",
        "year": 2024,
        "venue": "Test Venue",
        "citationCount": 10,
        "url": "https://example.com",
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: mock_paper,
        )
        mock_get.return_value.raise_for_status = lambda: None

        paper = await get_paper_details_s2("test-id")

        assert paper is not None
        assert paper.title == "Test Paper"
        assert paper.paper_id == "test-id"


@pytest.mark.asyncio
async def test_get_paper_details_not_found():
    """Test handling of paper not found."""
    with patch("httpx.AsyncClient.get") as mock_get:
        from httpx import HTTPStatusError, Request, Response

        mock_response = Response(
            status_code=404,
            request=Request("GET", "https://api.semanticscholar.org/graph/v1/paper/invalid"),
        )
        mock_get.return_value.raise_for_status.side_effect = HTTPStatusError(
            "404", request=mock_response.request, response=mock_response
        )
        mock_get.return_value = mock_response

        paper = await get_paper_details_s2("invalid-id")

        assert paper is None
