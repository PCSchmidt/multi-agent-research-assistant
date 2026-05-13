"""Agent tools for academic research."""

from .arxiv_search import search_arxiv
from .local_corpus import search_local_corpus
from .semantic_scholar import get_paper_details_s2, search_semantic_scholar

__all__ = [
    "search_semantic_scholar",
    "get_paper_details_s2",
    "search_arxiv",
    "search_local_corpus",
]
