"""Async evaluation task for research sessions.

This module provides background evaluation of research responses:
1. RAGAS evaluation for local corpus queries
2. Manual rubric metrics for live search queries
3. Logging results to Supabase eval_results table
"""

import asyncio
from uuid import UUID
from datetime import datetime

from app.evaluation.ragas_evaluator import evaluator as ragas_evaluator
from app.evaluation.manual_rubric import compute_manual_metrics
from app.models.research import Paper
from app.db.client import get_supabase_admin_client
from app.config import settings


async def evaluate_research_session(
    session_id: str | UUID,
    query: str,
    answer: str,
    papers: list[Paper],
    run_ragas: bool = True,
    run_manual: bool = True,
) -> dict:
    """
    Evaluate a research session asynchronously.

    This function runs evaluation metrics and logs results to the database.
    It's designed to run in the background without blocking the main response.

    Args:
        session_id: Research session UUID
        query: The user's research query
        answer: The synthesized answer from the agent
        papers: List of papers retrieved and used in synthesis
        run_ragas: Whether to run RAGAS evaluation (for local corpus queries)
        run_manual: Whether to compute manual rubric metrics

    Returns:
        Dictionary with evaluation results
    """
    session_id_str = str(session_id)

    # Initialize result dict
    eval_result = {
        "session_id": session_id_str,
        "ragas_status": "skipped" if not run_ragas else "pending",
        "faithfulness": None,
        "answer_relevancy": None,
        "context_precision": None,
        "citation_accuracy": None,
        "has_recent_papers": None,
        "source_diversity": None,
        "coverage_gaps": None,
        "evaluator": "ragas",
        "notes": None,
    }

    # Run RAGAS evaluation if requested
    if run_ragas and papers:
        try:
            print(f"[EVAL] Running RAGAS evaluation for session {session_id_str}")
            ragas_scores = await ragas_evaluator.evaluate_from_papers(
                question=query,
                answer=answer,
                papers=papers,
            )

            eval_result["faithfulness"] = ragas_scores.get("faithfulness")
            eval_result["answer_relevancy"] = ragas_scores.get("answer_relevancy")
            eval_result["context_precision"] = ragas_scores.get("context_precision")
            eval_result["ragas_status"] = "completed"

            # Check thresholds
            passed, per_metric = ragas_evaluator.check_thresholds(ragas_scores)
            print(f"[EVAL] RAGAS scores: {ragas_scores}")
            print(f"[EVAL] Thresholds passed: {passed} - {per_metric}")

        except Exception as e:
            print(f"[EVAL] RAGAS evaluation failed: {str(e)}")
            eval_result["ragas_status"] = "failed"
            eval_result["notes"] = f"RAGAS error: {str(e)}"

    # Run manual rubric metrics if requested
    if run_manual and papers:
        try:
            print(f"[EVAL] Computing manual rubric metrics for session {session_id_str}")
            manual_metrics = await compute_manual_metrics(
                answer=answer,
                papers=papers,
            )

            eval_result["citation_accuracy"] = manual_metrics.get("citation_accuracy")
            eval_result["has_recent_papers"] = manual_metrics.get("has_recent_papers")
            eval_result["source_diversity"] = manual_metrics.get("source_diversity")
            eval_result["coverage_gaps"] = manual_metrics.get("coverage_gaps")

            print(f"[EVAL] Manual metrics: {manual_metrics}")

        except Exception as e:
            print(f"[EVAL] Manual rubric computation failed: {str(e)}")
            if eval_result["notes"]:
                eval_result["notes"] += f"; Manual rubric error: {str(e)}"
            else:
                eval_result["notes"] = f"Manual rubric error: {str(e)}"

    # Log to database
    try:
        supabase = get_supabase_admin_client()

        # Insert eval results
        insert_data = {
            "session_id": session_id_str,
            "faithfulness": eval_result["faithfulness"],
            "answer_relevancy": eval_result["answer_relevancy"],
            "context_precision": eval_result["context_precision"],
            "ragas_status": eval_result["ragas_status"],
            "citation_accuracy": eval_result["citation_accuracy"],
            "has_recent_papers": eval_result["has_recent_papers"],
            "source_diversity": eval_result["source_diversity"],
            "coverage_gaps": eval_result["coverage_gaps"],
            "evaluator": eval_result["evaluator"],
            "notes": eval_result["notes"],
        }

        result = supabase.table("eval_results").insert(insert_data).execute()
        print(f"[EVAL] Results logged to database for session {session_id_str}")

    except Exception as e:
        print(f"[EVAL] Failed to log eval results to database: {str(e)}")
        # Don't raise - evaluation logging failure shouldn't break the request

    return eval_result


def spawn_evaluation_task(
    session_id: str | UUID,
    query: str,
    answer: str,
    papers: list[Paper],
    run_ragas: bool = True,
    run_manual: bool = True,
) -> asyncio.Task:
    """
    Spawn evaluation as a background task.

    This creates a fire-and-forget task that won't block the main response.
    The task will complete in the background and log results to the database.

    Args:
        session_id: Research session UUID
        query: The user's research query
        answer: The synthesized answer
        papers: List of papers used in synthesis
        run_ragas: Whether to run RAGAS evaluation
        run_manual: Whether to compute manual metrics

    Returns:
        asyncio.Task that's running in the background
    """
    task = asyncio.create_task(
        evaluate_research_session(
            session_id=session_id,
            query=query,
            answer=answer,
            papers=papers,
            run_ragas=run_ragas,
            run_manual=run_manual,
        )
    )

    # Add done callback to catch any exceptions
    def log_task_exception(task: asyncio.Task):
        try:
            task.result()
        except Exception as e:
            print(f"[EVAL] Background evaluation task failed: {str(e)}")

    task.add_done_callback(log_task_exception)

    return task
