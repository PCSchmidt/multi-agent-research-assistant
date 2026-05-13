"""Manual evaluation rubric for live academic search.

This module computes automated heuristics and provides placeholders for
manual evaluation metrics:

1. Citation accuracy: Checks if answer contains citations [1], [2], etc.
2. Recency: Checks if recent papers (2022-2024) are included when relevant
3. Source diversity: Measures distribution across different sources (S2, arXiv, local)
4. Coverage gaps: Placeholder for manual annotation of missing seminal works
"""

import re
from typing import Literal

from app.models.research import Paper


async def compute_manual_metrics(
    answer: str,
    papers: list[Paper],
) -> dict:
    """
    Compute manual rubric metrics for a research answer.

    Args:
        answer: The synthesized answer text
        papers: List of papers used in synthesis

    Returns:
        Dictionary with metrics:
        {
            "citation_accuracy": float | None,  # 0-1, % of citations present
            "has_recent_papers": bool,  # True if includes 2022-2024 papers
            "source_diversity": str,  # "balanced", "skewed", "n/a"
            "coverage_gaps": list[str] | None,  # Placeholder for manual annotation
        }
    """
    # Extract citation numbers from answer [1], [2], [3], etc.
    citation_pattern = r"\[(\d+)\]"
    citations_in_answer = set(re.findall(citation_pattern, answer))
    num_citations = len(citations_in_answer)

    # Citation accuracy: ratio of citations present to papers retrieved
    # This is a rough heuristic - true accuracy requires manual verification
    citation_accuracy = None
    if papers:
        max_citation_num = max((int(c) for c in citations_in_answer), default=0)
        # Ideally each paper should be cited at least once
        citation_accuracy = min(num_citations / len(papers), 1.0)

    # Recency check: do we have papers from 2022-2024?
    current_year = 2026  # Update this as needed
    recent_threshold = current_year - 4  # Last 4 years
    has_recent_papers = any(
        paper.year and paper.year >= recent_threshold
        for paper in papers
    )

    # Source diversity: check distribution across sources
    source_diversity = _compute_source_diversity(papers)

    # Coverage gaps: placeholder for manual annotation
    # In practice, a human reviewer would fill this in after reviewing the answer
    coverage_gaps = None

    return {
        "citation_accuracy": citation_accuracy,
        "has_recent_papers": has_recent_papers,
        "source_diversity": source_diversity,
        "coverage_gaps": coverage_gaps,
    }


def _compute_source_diversity(
    papers: list[Paper],
) -> Literal["balanced", "skewed", "n/a"]:
    """
    Compute source diversity metric.

    A balanced response uses multiple sources (Semantic Scholar, arXiv, local).
    A skewed response relies heavily on one source.

    Args:
        papers: List of papers

    Returns:
        "balanced" if sources are diverse, "skewed" if dominated by one source,
        "n/a" if not enough papers to judge
    """
    if not papers or len(papers) < 2:
        return "n/a"

    # Count papers by source
    source_counts = {}
    for paper in papers:
        source = paper.source.lower()
        source_counts[source] = source_counts.get(source, 0) + 1

    # If we have papers from 2+ different sources, consider it balanced
    num_sources = len(source_counts)
    if num_sources >= 2:
        # Check if one source dominates (>70% of papers)
        max_count = max(source_counts.values())
        total_papers = len(papers)

        if max_count / total_papers > 0.7:
            return "skewed"
        else:
            return "balanced"
    else:
        # Only one source used
        return "skewed"


def extract_coverage_gaps_prompt(
    query: str,
    papers: list[Paper],
) -> str:
    """
    Generate a prompt for manual coverage gap annotation.

    This is a helper for human reviewers to identify missing seminal works.

    Args:
        query: The research query
        papers: Papers that were retrieved

    Returns:
        Prompt text for manual review
    """
    paper_list = "\n".join([
        f"- {paper.title} ({paper.year})"
        for paper in papers
    ])

    prompt = f"""
MANUAL EVALUATION: Coverage Gaps

Query: {query}

Retrieved Papers:
{paper_list}

Instructions for Reviewer:
1. Based on your expertise, identify any seminal or highly-relevant papers
   that are missing from the retrieved set.
2. Consider whether the retrieved papers adequately cover the query topic.
3. List any missing works that would significantly improve the answer quality.

Missing Seminal Works (list paper titles or leave blank if coverage is adequate):
_______________________________________________________________________________
_______________________________________________________________________________
_______________________________________________________________________________
"""
    return prompt.strip()
