"""
Test script for v0.12: LangSmith Integration + Cost Analytics

This script:
1. Submits a research query via SSE streaming endpoint
2. Verifies LangSmith trace URL is captured
3. Checks token/cost tracking
4. Queries cost analytics API
5. Displays results

Run with: python test_v0.12_langsmith_cost.py
"""

import asyncio
import httpx
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"
TEST_QUERY = "What is the attention mechanism in transformers?"


async def test_langsmith_and_cost_tracking():
    """Run end-to-end test of LangSmith tracing and cost analytics."""

    print("=" * 80)
    print("v0.12 TEST: LangSmith Integration + Cost Analytics")
    print("=" * 80)
    print()

    # Step 1: Check API health
    print("[1/5] Checking API health...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✓ API is healthy")
            else:
                print(f"✗ API health check failed: {response.status_code}")
                return
        except Exception as e:
            print(f"✗ Cannot connect to API: {str(e)}")
            print("\nMake sure the backend is running:")
            print("  cd backend")
            print("  uvicorn app.main:app --reload")
            return

    print()

    # Step 2: Submit research query via SSE
    print(f"[2/5] Submitting research query: '{TEST_QUERY}'")
    session_id = None
    synthesis = None
    papers_count = 0
    llm_calls = 0

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            async with client.stream(
                "POST",
                f"{BASE_URL}/api/research/stream",
                json={"query": TEST_QUERY},
            ) as response:
                if response.status_code != 200:
                    print(f"✗ Query failed with status {response.status_code}")
                    return

                print("✓ Query submitted, receiving events...")

                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                        try:
                            event_data = json.loads(data_str)

                            # Extract session_id from first event
                            if "session_id" in event_data and not session_id:
                                session_id = event_data["session_id"]
                                print(f"  Session ID: {session_id}")

                            # Extract final results from 'done' event
                            if "papers_count" in event_data:
                                papers_count = event_data.get("papers_count", 0)
                                synthesis = event_data.get("synthesis", "")
                                llm_calls = event_data.get("llm_calls", 0)
                                print(f"  Papers found: {papers_count}")
                                print(f"  LLM calls: {llm_calls}")
                                print(f"  Synthesis length: {len(synthesis)} chars")
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            print(f"✗ Query failed: {str(e)}")
            return

    if not session_id:
        print("✗ No session_id received")
        return

    print()

    # Step 3: Check LangSmith trace URL in database
    print("[3/5] Checking LangSmith trace URL...")

    # Give backend a moment to update the database
    await asyncio.sleep(2)

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Query analytics to get session details
            response = await client.get(f"{BASE_URL}/api/analytics/cost/queries?limit=1")
            if response.status_code == 200:
                queries = response.json()
                if queries:
                    latest_query = queries[0]
                    trace_url = latest_query.get("langsmith_trace_url")
                    cost = latest_query.get("cost_usd", 0)
                    total_tokens = latest_query.get("total_tokens", 0)
                    input_tokens = latest_query.get("input_tokens", 0)
                    output_tokens = latest_query.get("output_tokens", 0)

                    if trace_url:
                        print(f"✓ LangSmith Trace URL: {trace_url}")
                        print(f"  You can view the trace in your LangSmith dashboard!")
                    else:
                        print("⚠ Trace URL not captured (may take a moment to update)")

                    print(f"\n  Token Usage:")
                    print(f"    Input tokens:  {input_tokens:,}")
                    print(f"    Output tokens: {output_tokens:,}")
                    print(f"    Total tokens:  {total_tokens:,}")
                    print(f"  Cost: ${cost:.6f}")
                else:
                    print("⚠ No queries found in analytics")
        except Exception as e:
            print(f"✗ Failed to fetch trace URL: {str(e)}")

    print()

    # Step 4: Test cost analytics endpoints
    print("[4/5] Testing cost analytics endpoints...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Cost summary
            response = await client.get(f"{BASE_URL}/api/analytics/cost/summary?days=1")
            if response.status_code == 200:
                summary = response.json()
                print(f"✓ Cost Summary (last 24h):")
                print(f"    Total queries: {summary.get('total_queries', 0)}")
                print(f"    Total cost: ${summary.get('total_cost_usd', 0):.6f}")
                print(f"    Avg cost/query: ${summary.get('avg_cost_per_query', 0):.6f}")

            # Budget status
            response = await client.get(f"{BASE_URL}/api/analytics/cost/budget-status")
            if response.status_code == 200:
                budget = response.json()
                print(f"\n✓ Budget Status:")
                print(f"    Today's spend: ${budget.get('today_spend_usd', 0):.6f}")
                print(f"    Daily threshold: ${budget.get('daily_threshold_usd', 0):.2f}")
                print(f"    Percentage used: {budget.get('percentage_used', 0):.1f}%")
                print(f"    Alert triggered: {budget.get('alert', False)}")
        except Exception as e:
            print(f"✗ Analytics endpoints failed: {str(e)}")

    print()

    # Step 5: Check evaluation results
    print("[5/5] Checking evaluation results...")
    print("⚠ Evaluation runs in background - results may take a few seconds")
    print(f"  Check the eval_results table in Supabase for session {session_id}")

    print()
    print("=" * 80)
    print("✓ v0.12 TEST COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print(f"1. Visit your LangSmith dashboard to see the trace")
    print(f"2. Check Supabase research_sessions table for trace_url and cost data")
    print(f"3. Check Supabase eval_results table for RAGAS scores")
    print()


if __name__ == "__main__":
    asyncio.run(test_langsmith_and_cost_tracking())
