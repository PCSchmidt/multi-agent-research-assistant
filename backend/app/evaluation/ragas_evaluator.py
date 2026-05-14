"""RAGAS-based evaluation for research quality.

This module evaluates research responses using RAGAS metrics:
- Faithfulness: How well the answer is grounded in the retrieved contexts
- Answer Relevancy: How relevant the answer is to the question
- Context Precision: How precise/relevant the retrieved contexts are

RAGAS evaluation is primarily for local corpus queries where we have
full control over the retrieval pipeline.
"""

import asyncio

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, context_precision, faithfulness

from app.models.research import Paper


class RAGASEvaluator:
    """Evaluates research responses using RAGAS metrics."""

    def __init__(self):
        """Initialize RAGAS evaluator with metrics."""
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
        ]

    async def evaluate_response(
        self,
        question: str,
        answer: str,
        contexts: list[str],
        ground_truth: str | None = None,
    ) -> dict[str, float]:
        """
        Evaluate a research response using RAGAS metrics.

        Args:
            question: The user's research query
            answer: The synthesized answer from the agent
            contexts: List of context strings (paper abstracts) used for synthesis
            ground_truth: Optional ground truth answer for comparison

        Returns:
            Dictionary with metric scores:
            {
                "faithfulness": float (0-1),
                "answer_relevancy": float (0-1),
                "context_precision": float (0-1),
            }

        Raises:
            ValueError: If inputs are invalid (empty answer, no contexts, etc.)
            Exception: If RAGAS evaluation fails
        """
        # Validate inputs
        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty")
        if not contexts or len(contexts) == 0:
            raise ValueError("At least one context is required for evaluation")
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        # Prepare data for RAGAS
        # RAGAS expects a dataset with specific column names
        data = {
            "question": [question],
            "answer": [answer],
            "contexts": [contexts],  # List of lists
        }

        # Add ground truth if provided (required for context_precision)
        if ground_truth:
            data["reference"] = [ground_truth]

        dataset = Dataset.from_dict(data)

        # Select metrics based on available data
        # context_precision requires 'reference' (ground truth)
        metrics_to_use = [faithfulness, answer_relevancy]
        if ground_truth:
            metrics_to_use.append(context_precision)

        try:
            # Run evaluation in executor to avoid blocking
            # RAGAS uses OpenAI by default for evaluation, which can be slow
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: evaluate(dataset, metrics=metrics_to_use)
            )

            # Extract scores
            # RAGAS returns lists (one value per sample), so we extract the first element
            scores = {
                "faithfulness": float(result["faithfulness"][0]) if isinstance(result["faithfulness"], list) else float(result["faithfulness"]),
                "answer_relevancy": float(result["answer_relevancy"][0]) if isinstance(result["answer_relevancy"], list) else float(result["answer_relevancy"]),
            }

            # Add context_precision only if it was evaluated
            if ground_truth and "context_precision" in result:
                cp_value = result["context_precision"]
                scores["context_precision"] = float(cp_value[0]) if isinstance(cp_value, list) else float(cp_value)

            return scores

        except Exception as e:
            raise Exception(f"RAGAS evaluation failed: {str(e)}") from e

    async def evaluate_from_papers(
        self,
        question: str,
        answer: str,
        papers: list[Paper],
    ) -> dict[str, float]:
        """
        Evaluate response using paper abstracts as contexts.

        This is a convenience method that extracts contexts from Paper objects.

        Args:
            question: The user's research query
            answer: The synthesized answer
            papers: List of Paper objects used for synthesis

        Returns:
            Dictionary with metric scores
        """
        # Extract contexts from papers (use abstracts)
        contexts = []
        for paper in papers:
            if paper.abstract:
                # Truncate long abstracts to avoid context length issues
                abstract = paper.abstract[:1000]
                contexts.append(abstract)

        if not contexts:
            raise ValueError("No paper abstracts available for evaluation")

        return await self.evaluate_response(
            question=question,
            answer=answer,
            contexts=contexts,
        )

    def check_thresholds(
        self,
        scores: dict[str, float],
        thresholds: dict[str, float] | None = None,
    ) -> tuple[bool, dict[str, bool]]:
        """
        Check if scores meet quality thresholds.

        Args:
            scores: Dictionary of metric scores
            thresholds: Optional custom thresholds. Defaults to:
                - faithfulness >= 0.75
                - answer_relevancy >= 0.70
                - context_precision >= 0.65

        Returns:
            Tuple of (all_passed, per_metric_results)
        """
        if thresholds is None:
            thresholds = {
                "faithfulness": 0.75,
                "answer_relevancy": 0.70,
                "context_precision": 0.65,
            }

        results = {}
        for metric, threshold in thresholds.items():
            if metric in scores:
                results[metric] = scores[metric] >= threshold

        all_passed = all(results.values())
        return all_passed, results


# Global evaluator instance
evaluator = RAGASEvaluator()
