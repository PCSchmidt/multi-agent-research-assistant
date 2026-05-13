"""Unit tests for manual evaluation rubric."""

import pytest

from app.evaluation.manual_rubric import (
    _compute_source_diversity,
    compute_manual_metrics,
    extract_coverage_gaps_prompt,
)
from app.models.research import Author, Paper


@pytest.fixture
def sample_papers_diverse():
    """Sample papers from diverse sources."""
    return [
        Paper(
            paper_id="s2_paper_1",
            title="Paper from Semantic Scholar",
            authors=[Author(name="Author A")],
            abstract="Test abstract",
            year=2023,
            source="semantic_scholar",
            citation_count=100,
        ),
        Paper(
            paper_id="arxiv_paper_1",
            title="Paper from arXiv",
            authors=[Author(name="Author B")],
            abstract="Test abstract",
            year=2024,
            source="arxiv",
            citation_count=50,
        ),
        Paper(
            paper_id="local_paper_1",
            title="Paper from local corpus",
            authors=[Author(name="Author C")],
            abstract="Test abstract",
            year=2020,
            source="local",
            citation_count=500,
        ),
    ]


@pytest.fixture
def sample_papers_skewed():
    """Sample papers from single source."""
    return [
        Paper(
            paper_id=f"s2_{i}",
            title=f"Paper {i}",
            authors=[Author(name=f"Author {i}")],
            abstract="Test abstract",
            year=2023,
            source="semantic_scholar",
        )
        for i in range(5)
    ]


@pytest.mark.asyncio
async def test_compute_manual_metrics_with_citations(sample_papers_diverse):
    """Test manual metrics computation with proper citations."""
    answer = """
    Recent work on transformers [1] has shown significant improvements.
    The attention mechanism [2] enables better long-range dependencies.
    Building on foundational work [3], we can achieve state-of-the-art results.
    """

    metrics = await compute_manual_metrics(answer, sample_papers_diverse)

    assert "citation_accuracy" in metrics
    assert "has_recent_papers" in metrics
    assert "source_diversity" in metrics
    assert "coverage_gaps" in metrics

    # Should have citations [1], [2], [3]
    assert metrics["citation_accuracy"] == 1.0  # 3 citations / 3 papers

    # Should have recent papers (2023, 2024)
    assert metrics["has_recent_papers"] is True

    # Should be balanced (3 different sources)
    assert metrics["source_diversity"] == "balanced"

    # Coverage gaps should be None (placeholder for manual annotation)
    assert metrics["coverage_gaps"] is None


@pytest.mark.asyncio
async def test_compute_manual_metrics_no_citations(sample_papers_diverse):
    """Test manual metrics with answer containing no citations."""
    answer = "This is an answer without any citations."

    metrics = await compute_manual_metrics(answer, sample_papers_diverse)

    # No citations found
    assert metrics["citation_accuracy"] == 0.0


@pytest.mark.asyncio
async def test_compute_manual_metrics_old_papers_only():
    """Test recency detection with only old papers."""
    old_papers = [
        Paper(
            paper_id="old_1",
            title="Old Paper",
            authors=[Author(name="Author")],
            abstract="Abstract",
            year=2015,
            source="test",
        ),
        Paper(
            paper_id="old_2",
            title="Another Old Paper",
            authors=[Author(name="Author")],
            abstract="Abstract",
            year=2018,
            source="test",
        ),
    ]

    answer = "Test answer [1] [2]"
    metrics = await compute_manual_metrics(answer, old_papers)

    # No recent papers (threshold is 2022+)
    assert metrics["has_recent_papers"] is False


def test_compute_source_diversity_balanced(sample_papers_diverse):
    """Test source diversity with balanced sources."""
    diversity = _compute_source_diversity(sample_papers_diverse)
    assert diversity == "balanced"


def test_compute_source_diversity_skewed(sample_papers_skewed):
    """Test source diversity with skewed sources."""
    diversity = _compute_source_diversity(sample_papers_skewed)
    assert diversity == "skewed"


def test_compute_source_diversity_not_enough_papers():
    """Test source diversity with insufficient papers."""
    single_paper = [
        Paper(
            paper_id="test_1",
            title="Test",
            authors=[Author(name="Author")],
            abstract="Abstract",
            year=2020,
            source="test",
        )
    ]

    diversity = _compute_source_diversity(single_paper)
    assert diversity == "n/a"


def test_compute_source_diversity_mostly_one_source():
    """Test source diversity when one source dominates."""
    papers = [
        # 7 from S2
        *[
            Paper(
                paper_id=f"s2_{i}",
                title=f"Paper {i}",
                authors=[Author(name="Author")],
                abstract="Abstract",
                year=2020,
                source="semantic_scholar",
            )
            for i in range(7)
        ],
        # 2 from arXiv
        *[
            Paper(
                paper_id=f"arxiv_{i}",
                title=f"Paper {i}",
                authors=[Author(name="Author")],
                abstract="Abstract",
                year=2020,
                source="arxiv",
            )
            for i in range(2)
        ],
    ]

    # 7/9 = 77% from one source -> skewed
    diversity = _compute_source_diversity(papers)
    assert diversity == "skewed"


def test_extract_coverage_gaps_prompt(sample_papers_diverse):
    """Test coverage gaps prompt generation."""
    query = "What are transformers in NLP?"

    prompt = extract_coverage_gaps_prompt(query, sample_papers_diverse)

    # Verify prompt contains key elements
    assert "MANUAL EVALUATION" in prompt
    assert query in prompt
    assert "Paper from Semantic Scholar" in prompt
    assert "Paper from arXiv" in prompt
    assert "Paper from local corpus" in prompt
    assert "Missing Seminal Works" in prompt


@pytest.mark.asyncio
async def test_compute_manual_metrics_empty_papers():
    """Test manual metrics with empty papers list."""
    answer = "Test answer"
    metrics = await compute_manual_metrics(answer, [])

    assert metrics["citation_accuracy"] is None
    assert metrics["has_recent_papers"] is False
    assert metrics["source_diversity"] == "n/a"
