"""Unit tests for RAGAS evaluator.

These tests verify:
1. RAGAS evaluator can process valid inputs
2. Evaluation scores are in valid ranges (0-1)
3. Threshold checking works correctly
4. Error handling for invalid inputs
"""

import pytest

from app.evaluation.ragas_evaluator import RAGASEvaluator
from app.models.research import Author, Paper


@pytest.fixture
def evaluator():
    """Create RAGAS evaluator instance."""
    return RAGASEvaluator()


@pytest.fixture
def sample_papers():
    """Sample papers for testing."""
    return [
        Paper(
            paper_id="test_paper_1",
            title="Attention Is All You Need",
            authors=[Author(name="Vaswani et al.")],
            abstract="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
            year=2017,
            source="test",
            citation_count=50000,
        ),
        Paper(
            paper_id="test_paper_2",
            title="BERT: Pre-training of Deep Bidirectional Transformers",
            authors=[Author(name="Devlin et al.")],
            abstract="We introduce BERT, a new language representation model that uses bidirectional transformers. BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context.",
            year=2018,
            source="test",
            citation_count=40000,
        ),
    ]


@pytest.mark.asyncio
async def test_evaluate_response_valid_inputs(evaluator):
    """Test evaluation with valid inputs."""
    question = "What is the attention mechanism in transformers?"
    answer = "The attention mechanism in transformers allows the model to dynamically focus on different parts of the input sequence. It computes attention weights by comparing query, key, and value representations."
    contexts = [
        "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
        "Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks.",
    ]

    scores = await evaluator.evaluate_response(
        question=question,
        answer=answer,
        contexts=contexts,
    )

    # Verify all scores are present
    assert "faithfulness" in scores
    assert "answer_relevancy" in scores
    assert "context_precision" in scores

    # Verify scores are in valid range [0, 1]
    for metric, score in scores.items():
        assert 0 <= score <= 1, f"{metric} score {score} out of range [0, 1]"


@pytest.mark.asyncio
async def test_evaluate_from_papers(evaluator, sample_papers):
    """Test evaluation using Paper objects."""
    question = "What are transformers in NLP?"
    answer = "Transformers are neural network architectures based on attention mechanisms [1]. They were introduced in the paper 'Attention Is All You Need' and have since become the foundation for models like BERT [2]."

    scores = await evaluator.evaluate_from_papers(
        question=question,
        answer=answer,
        papers=sample_papers,
    )

    # Verify all scores are present and in valid range
    assert "faithfulness" in scores
    assert "answer_relevancy" in scores
    assert "context_precision" in scores

    for metric, score in scores.items():
        assert 0 <= score <= 1


@pytest.mark.asyncio
async def test_evaluate_empty_answer_raises_error(evaluator):
    """Test that empty answer raises ValueError."""
    with pytest.raises(ValueError, match="Answer cannot be empty"):
        await evaluator.evaluate_response(
            question="What is attention?",
            answer="",
            contexts=["Some context"],
        )


@pytest.mark.asyncio
async def test_evaluate_no_contexts_raises_error(evaluator):
    """Test that empty contexts list raises ValueError."""
    with pytest.raises(ValueError, match="At least one context is required"):
        await evaluator.evaluate_response(
            question="What is attention?",
            answer="Attention is a mechanism.",
            contexts=[],
        )


@pytest.mark.asyncio
async def test_evaluate_empty_question_raises_error(evaluator):
    """Test that empty question raises ValueError."""
    with pytest.raises(ValueError, match="Question cannot be empty"):
        await evaluator.evaluate_response(
            question="",
            answer="Some answer",
            contexts=["Some context"],
        )


def test_check_thresholds_default(evaluator):
    """Test threshold checking with default thresholds."""
    scores = {
        "faithfulness": 0.80,
        "answer_relevancy": 0.75,
        "context_precision": 0.70,
    }

    all_passed, per_metric = evaluator.check_thresholds(scores)

    assert all_passed is True
    assert per_metric["faithfulness"] is True
    assert per_metric["answer_relevancy"] is True
    assert per_metric["context_precision"] is True


def test_check_thresholds_some_fail(evaluator):
    """Test threshold checking when some metrics fail."""
    scores = {
        "faithfulness": 0.80,  # Pass (>= 0.75)
        "answer_relevancy": 0.65,  # Fail (< 0.70)
        "context_precision": 0.60,  # Fail (< 0.65)
    }

    all_passed, per_metric = evaluator.check_thresholds(scores)

    assert all_passed is False
    assert per_metric["faithfulness"] is True
    assert per_metric["answer_relevancy"] is False
    assert per_metric["context_precision"] is False


def test_check_thresholds_custom(evaluator):
    """Test threshold checking with custom thresholds."""
    scores = {
        "faithfulness": 0.85,
        "answer_relevancy": 0.80,
        "context_precision": 0.75,
    }

    custom_thresholds = {
        "faithfulness": 0.90,  # Higher threshold
        "answer_relevancy": 0.75,
        "context_precision": 0.70,
    }

    all_passed, per_metric = evaluator.check_thresholds(scores, custom_thresholds)

    assert all_passed is False  # faithfulness fails high threshold
    assert per_metric["faithfulness"] is False
    assert per_metric["answer_relevancy"] is True
    assert per_metric["context_precision"] is True


@pytest.mark.asyncio
async def test_evaluate_from_papers_no_abstracts_raises_error(evaluator):
    """Test that papers without abstracts raise ValueError."""
    papers_without_abstracts = [
        Paper(
            paper_id="test_1",
            title="Test Paper",
            authors=[Author(name="Test Author")],
            abstract=None,  # No abstract
            year=2020,
            source="test",
        )
    ]

    with pytest.raises(ValueError, match="No paper abstracts available"):
        await evaluator.evaluate_from_papers(
            question="Test question",
            answer="Test answer",
            papers=papers_without_abstracts,
        )


def test_check_thresholds_edge_case_exact_match(evaluator):
    """Test threshold checking with exact threshold match."""
    scores = {
        "faithfulness": 0.75,  # Exact match with threshold
        "answer_relevancy": 0.70,  # Exact match
        "context_precision": 0.65,  # Exact match
    }

    all_passed, per_metric = evaluator.check_thresholds(scores)

    # Exact match should pass (>= comparison)
    assert all_passed is True
    assert all(per_metric.values())
