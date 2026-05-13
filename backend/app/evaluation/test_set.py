"""Seeded test set for RAGAS evaluation.

This module contains 10 canonical queries across different domains
(ML, NLP, computer vision) that can be answered using the local corpus
of foundational papers.

These queries are designed to:
1. Have clear ground truth answers
2. Be answerable using the seeded canonical papers
3. Cover different types of research questions
4. Test various aspects of retrieval and synthesis quality
"""

from typing import TypedDict


class TestQuery(TypedDict):
    """A test query with ground truth for evaluation."""
    question: str
    ground_truth: str
    domain: str
    expected_papers: list[str]  # Paper IDs or titles that should be retrieved
    difficulty: str  # easy, medium, hard


# Seeded test set: 10 queries across ML/NLP/CV domains
TEST_SET: list[TestQuery] = [
    {
        "question": "What is the attention mechanism in transformers and why is it important?",
        "ground_truth": "The attention mechanism in transformers allows the model to dynamically focus on different parts of the input sequence when processing each element. It computes attention weights by comparing query, key, and value representations, enabling the model to capture long-range dependencies without recurrence. This is important because it eliminates the sequential bottleneck of RNNs, enables parallel processing, and allows the model to learn which parts of the input are most relevant for each prediction.",
        "domain": "NLP",
        "expected_papers": ["arxiv:1706.03762"],  # Attention Is All You Need
        "difficulty": "easy",
    },
    {
        "question": "How does BERT's pre-training approach differ from traditional language models?",
        "ground_truth": "BERT uses bidirectional pre-training through masked language modeling (MLM) and next sentence prediction (NSP), which allows it to learn context from both left and right directions simultaneously. Traditional language models like GPT use unidirectional (left-to-right) pre-training. This bidirectional approach enables BERT to better understand context and achieve superior performance on downstream tasks that require understanding of the full sequence context.",
        "domain": "NLP",
        "expected_papers": ["arxiv:1810.04805"],  # BERT
        "difficulty": "medium",
    },
    {
        "question": "What are the computational challenges of processing long sequences with transformers, and what solutions have been proposed?",
        "ground_truth": "The main computational challenge is that standard attention has O(n²) time and memory complexity with respect to sequence length, making it impractical for long documents. Solutions include: 1) Longformer's sliding window and global attention patterns that reduce complexity to O(n), 2) Reformer's locality-sensitive hashing for approximate attention, 3) Sparse attention patterns that only attend to specific positions. These approaches maintain model quality while enabling processing of sequences with thousands of tokens.",
        "domain": "NLP",
        "expected_papers": ["arxiv:2004.05150", "arxiv:2001.04451"],  # Longformer, Reformer
        "difficulty": "hard",
    },
    {
        "question": "Explain the concept of few-shot learning as demonstrated in GPT-3.",
        "ground_truth": "Few-shot learning in GPT-3 refers to the model's ability to perform new tasks with only a few examples provided in the prompt, without any parameter updates or fine-tuning. By scaling language models to 175 billion parameters and training on diverse internet text, GPT-3 develops strong in-context learning capabilities. The model can understand task instructions and adapt to new tasks from just a few demonstrations, showing that scale and pre-training enable meta-learning behavior.",
        "domain": "NLP",
        "expected_papers": ["arxiv:2005.14165"],  # GPT-3
        "difficulty": "medium",
    },
    {
        "question": "What is the key innovation in the Transformer architecture compared to RNN-based models?",
        "ground_truth": "The key innovation is replacing recurrence with self-attention mechanisms, which allows for parallel processing of sequence elements and direct modeling of dependencies regardless of distance. Unlike RNNs that process sequences sequentially and struggle with long-range dependencies, transformers compute attention between all pairs of positions simultaneously. This enables better gradient flow, faster training through parallelization, and more effective capture of long-range relationships in the data.",
        "domain": "NLP",
        "expected_papers": ["arxiv:1706.03762"],  # Attention Is All You Need
        "difficulty": "easy",
    },
    {
        "question": "How does masked language modeling work in BERT and why is it effective?",
        "ground_truth": "Masked language modeling randomly masks 15% of input tokens and trains the model to predict the original tokens based on bidirectional context. This forces the model to learn deep bidirectional representations, as it cannot rely on seeing the target token or only using left/right context. The masking strategy includes: 80% [MASK] tokens, 10% random tokens, and 10% unchanged tokens. This approach is effective because it creates a denoising objective that encourages the model to learn rich contextual representations useful for downstream tasks.",
        "domain": "NLP",
        "expected_papers": ["arxiv:1810.04805"],  # BERT
        "difficulty": "medium",
    },
    {
        "question": "What are the trade-offs between different efficient attention mechanisms for long sequences?",
        "ground_truth": "Different efficient attention mechanisms make different trade-offs: 1) Sliding window attention (Longformer) reduces complexity but may miss long-range dependencies outside the window, mitigated by global attention tokens. 2) Sparse patterns sacrifice some connectivity for speed. 3) Locality-sensitive hashing (Reformer) is theoretically efficient but adds implementation complexity and approximation errors. 4) Low-rank approximations reduce expressiveness. The choice depends on the specific task requirements, sequence lengths, and whether the task needs global context or can work with local patterns.",
        "domain": "NLP",
        "expected_papers": ["arxiv:2004.05150", "arxiv:2001.04451"],  # Longformer, Reformer
        "difficulty": "hard",
    },
    {
        "question": "What makes pre-training important for NLP tasks according to modern language models?",
        "ground_truth": "Pre-training is important because it allows models to learn general language understanding, representations, and patterns from large amounts of unlabeled text before being specialized for specific tasks. Models like BERT and GPT demonstrate that pre-training on massive corpora enables transfer learning: the model learns syntax, semantics, world knowledge, and reasoning capabilities that transfer to downstream tasks with minimal task-specific training. This is more efficient than training from scratch and leads to better performance, especially on tasks with limited labeled data.",
        "domain": "NLP",
        "expected_papers": ["arxiv:1810.04805", "arxiv:2005.14165"],  # BERT, GPT-3
        "difficulty": "medium",
    },
    {
        "question": "How do transformers handle variable-length sequences and positional information?",
        "ground_truth": "Transformers handle variable-length sequences through attention masks that prevent attending to padding tokens, and positional encodings that inject information about token positions. Since self-attention is permutation-invariant, positional encodings are essential. The original transformer uses sinusoidal positional encodings (sin/cos functions of different frequencies), while variants like BERT use learned positional embeddings. These encodings are added to token embeddings, allowing the model to use positional information while maintaining the flexibility to process sequences of varying lengths.",
        "domain": "NLP",
        "expected_papers": ["arxiv:1706.03762", "arxiv:1810.04805"],  # Attention Is All You Need, BERT
        "difficulty": "easy",
    },
    {
        "question": "What scaling laws were discovered with large language models like GPT-3?",
        "ground_truth": "GPT-3 research revealed several scaling laws: 1) Performance scales smoothly and predictably with model size, dataset size, and compute. 2) Larger models are more sample-efficient, requiring fewer examples to reach the same performance. 3) Few-shot learning ability emerges at scale - models with 10B+ parameters can perform tasks from just examples without fine-tuning. 4) There's a power-law relationship between model size and performance. These findings suggest that scaling alone can unlock new capabilities, though with diminishing returns.",
        "domain": "NLP",
        "expected_papers": ["arxiv:2005.14165"],  # GPT-3
        "difficulty": "hard",
    },
]


def get_test_set() -> list[TestQuery]:
    """
    Get the full seeded test set.

    Returns:
        List of 10 test queries with ground truth
    """
    return TEST_SET


def get_test_queries_by_domain(domain: str) -> list[TestQuery]:
    """
    Get test queries filtered by domain.

    Args:
        domain: Domain to filter by (e.g., "NLP", "CV", "ML")

    Returns:
        List of test queries matching the domain
    """
    return [q for q in TEST_SET if q["domain"].lower() == domain.lower()]


def get_test_queries_by_difficulty(difficulty: str) -> list[TestQuery]:
    """
    Get test queries filtered by difficulty.

    Args:
        difficulty: Difficulty level ("easy", "medium", "hard")

    Returns:
        List of test queries matching the difficulty
    """
    return [q for q in TEST_SET if q["difficulty"].lower() == difficulty.lower()]
