"""
CLI script to ingest canonical papers into local corpus.

Usage:
    python scripts/ingest_papers.py --file papers.json
    python scripts/ingest_papers.py --paper-id arxiv:1706.03762
    python scripts/ingest_papers.py --seed-defaults
"""

import asyncio
import json
import argparse
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.tools.local_corpus import add_canonical_paper
from app.tools.semantic_scholar import get_paper_details_s2
from app.models.research import Author


async def ingest_from_file(file_path: str):
    """
    Ingest papers from JSON file.

    Expected format:
    [
        {
            "paper_id": "arxiv:1706.03762",
            "source": "arxiv",
            "title": "Attention Is All You Need",
            "authors": [{"name": "Ashish Vaswani"}, ...],
            "abstract": "...",
            "year": 2017,
            "venue": "NeurIPS",
            "citation_count": 50000,
            "url": "https://arxiv.org/abs/1706.03762",
            "tags": ["foundational", "transformers"]
        },
        ...
    ]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    print(f"Ingesting {len(papers)} papers from {file_path}...")

    for i, paper_data in enumerate(papers, 1):
        try:
            # Parse authors
            authors = [Author(**author) for author in paper_data.get("authors", [])]

            # Add to canonical corpus
            paper_uuid = await add_canonical_paper(
                paper_id=paper_data["paper_id"],
                source=paper_data["source"],
                title=paper_data["title"],
                authors=authors,
                abstract=paper_data["abstract"],
                year=paper_data["year"],
                venue=paper_data.get("venue"),
                citation_count=paper_data.get("citation_count", 0),
                url=paper_data.get("url"),
                tags=paper_data.get("tags", []),
                notes=paper_data.get("notes"),
            )

            print(f"  [{i}/{len(papers)}] OK {paper_data['title'][:60]}... (ID: {paper_uuid})")

        except Exception as e:
            print(f"  [{i}/{len(papers)}] FAILED: {paper_data.get('title', 'Unknown')[:60]}...")
            print(f"           Error: {e}")

    print(f"\nDONE: Ingestion complete: {len(papers)} papers processed")


async def ingest_by_s2_id(paper_id: str):
    """Fetch paper from Semantic Scholar by ID and ingest."""
    print(f"Fetching paper {paper_id} from Semantic Scholar...")

    paper = await get_paper_details_s2(paper_id)

    if not paper:
        print(f"ERROR: Paper not found: {paper_id}")
        return

    # Add to canonical corpus
    paper_uuid = await add_canonical_paper(
        paper_id=paper.paper_id,
        source=paper.source,
        title=paper.title,
        authors=paper.authors,
        abstract=paper.abstract or "",
        year=paper.year or 2024,
        venue=paper.venue,
        citation_count=paper.citation_count,
        url=paper.url,
        tags=["imported"],
    )

    print(f"OK: Ingested: {paper.title}")
    print(f"  UUID: {paper_uuid}")


async def seed_default_papers():
    """Seed database with foundational ML/AI papers."""
    print("Seeding canonical papers (foundational ML/AI works)...\n")

    # Foundational papers (will be created as JSON file)
    default_papers = [
        {
            "paper_id": "arxiv:1706.03762",
            "source": "arxiv",
            "title": "Attention Is All You Need",
            "authors": [
                {"name": "Ashish Vaswani"},
                {"name": "Noam Shazeer"},
                {"name": "Niki Parmar"},
                {"name": "Jakob Uszkoreit"},
                {"name": "Llion Jones"},
                {"name": "Aidan N. Gomez"},
                {"name": "Lukasz Kaiser"},
                {"name": "Illia Polosukhin"},
            ],
            "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
            "year": 2017,
            "venue": "NeurIPS",
            "citation_count": 100000,
            "url": "https://arxiv.org/abs/1706.03762",
            "tags": ["foundational", "transformers", "attention", "seminal"]
        },
        {
            "paper_id": "arxiv:1810.04805",
            "source": "arxiv",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "authors": [
                {"name": "Jacob Devlin"},
                {"name": "Ming-Wei Chang"},
                {"name": "Kenton Lee"},
                {"name": "Kristina Toutanova"},
            ],
            "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
            "year": 2018,
            "venue": "NAACL",
            "citation_count": 80000,
            "url": "https://arxiv.org/abs/1810.04805",
            "tags": ["foundational", "transformers", "nlp", "pre-training"]
        },
        {
            "paper_id": "arxiv:2004.04906",
            "source": "arxiv",
            "title": "Longformer: The Long-Document Transformer",
            "authors": [
                {"name": "Iz Beltagy"},
                {"name": "Matthew E. Peters"},
                {"name": "Arman Cohan"},
            ],
            "abstract": "Transformer-based models are unable to process long sequences due to their self-attention operation, which scales quadratically with the sequence length. To address this limitation, we introduce the Longformer with an attention mechanism that scales linearly with sequence length, making it easy to process documents of thousands of tokens or longer.",
            "year": 2020,
            "venue": "arXiv",
            "citation_count": 5000,
            "url": "https://arxiv.org/abs/2004.04906",
            "tags": ["transformers", "attention", "efficiency", "long-context"]
        },
        {
            "paper_id": "arxiv:2001.04451",
            "source": "arxiv",
            "title": "Reformer: The Efficient Transformer",
            "authors": [
                {"name": "Nikita Kitaev"},
                {"name": "Lukasz Kaiser"},
                {"name": "Anselm Levskaya"},
            ],
            "abstract": "Large Transformer models routinely achieve state-of-the-art results on a number of tasks but training these models can be prohibitively costly, especially on long sequences. We introduce two techniques to improve the efficiency of Transformers. For the first time we show that locality-sensitive hashing can be used to reduce the self-attention complexity from O(L^2) to O(L log L).",
            "year": 2020,
            "venue": "ICLR",
            "citation_count": 3000,
            "url": "https://arxiv.org/abs/2001.04451",
            "tags": ["transformers", "attention", "efficiency", "sparse"]
        },
        {
            "paper_id": "arxiv:2005.14165",
            "source": "arxiv",
            "title": "Language Models are Few-Shot Learners",
            "authors": [
                {"name": "Tom B. Brown"},
                {"name": "Benjamin Mann"},
                {"name": "Nick Ryder"},
            ],
            "abstract": "We show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even becoming competitive with prior state-of-the-art fine-tuning approaches. We train GPT-3, an autoregressive language model with 175 billion parameters.",
            "year": 2020,
            "venue": "NeurIPS",
            "citation_count": 40000,
            "url": "https://arxiv.org/abs/2005.14165",
            "tags": ["foundational", "language-models", "few-shot", "gpt"]
        },
    ]

    # Write to temp file and ingest
    temp_file = Path("temp_seed_papers.json")
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(default_papers, f, indent=2)

    await ingest_from_file(str(temp_file))

    # Clean up temp file
    temp_file.unlink()


async def main():
    parser = argparse.ArgumentParser(
        description="Ingest canonical papers into local corpus"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to JSON file containing papers"
    )
    parser.add_argument(
        "--paper-id",
        type=str,
        help="Semantic Scholar paper ID to fetch and ingest"
    )
    parser.add_argument(
        "--seed-defaults",
        action="store_true",
        help="Seed database with default foundational papers"
    )

    args = parser.parse_args()

    if args.file:
        await ingest_from_file(args.file)
    elif args.paper_id:
        await ingest_by_s2_id(args.paper_id)
    elif args.seed_defaults:
        await seed_default_papers()
    else:
        parser.print_help()
        print("\nError: Must specify --file, --paper-id, or --seed-defaults")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
