"""Agent tools for academic research."""

from .semantic_scholar import search_semantic_scholar, get_paper_details_s2
from .arxiv_search import search_arxiv
from .local_corpus import search_local_corpus

__all__ = [
    "search_semantic_scholar",
    "get_paper_details_s2",
    "search_arxiv",
    "search_local_corpus",
]
