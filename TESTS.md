# TESTS.md
# Test Strategy & Evaluation Plan

**Project:** Multi-Agent Academic Research Assistant  
**Created:** 2026-05-10  
**Gate:** v0.6 - TESTS APPROVED  

---

## Overview

This document defines the testing strategy, evaluation plans, and quality gates for the Academic Research Assistant. Tests are split into three categories:

1. **Backend Tests** - pytest for API, agent logic, retrieval, synthesis
2. **Frontend Tests** - Jest/RTL for React Native components
3. **E2E Tests** - Playwright for critical web flows

Evaluation is split into two modes:

1. **RAGAS** - Automated metrics for local corpus queries (deterministic retrieval)
2. **Manual Rubric** - Human evaluation for live academic search (non-deterministic)

---

## Backend Testing Strategy

### Framework
- **pytest** (Python 3.11+)
- **pytest-asyncio** for async endpoints
- **pytest-cov** for coverage reporting
- **httpx** for FastAPI test client
- **pytest-mock** for mocking external APIs

### Coverage Target
**≥80% coverage** on core logic:
- Agent tool implementations
- Retrieval merge logic
- Synthesis + citation generation
- Streaming response formatting
- Cost tracking

### Test Organization
```
backend/tests/
├── unit/
│   ├── test_s2_tool.py          # Semantic Scholar API tool
│   ├── test_arxiv_tool.py       # arXiv API tool
│   ├── test_local_tool.py       # Local corpus retrieval
│   ├── test_synthesis.py        # Citation generation logic
│   └── test_cost_tracker.py     # Token counting, cost calc
├── integration/
│   ├── test_react_agent.py      # ReAct agent with mocked tools
│   ├── test_hybrid_retrieval.py # Live + local merge logic
│   └── test_streaming.py        # SSE response formatting
└── e2e/
    └── test_query_flow.py       # Full query → response flow
```

### Key Test Cases

**Semantic Scholar Tool (`test_s2_tool.py`):**
- Returns top 5 papers for valid query
- Handles API rate limit (429) gracefully
- Handles API timeout (5s max)
- Parses paper metadata correctly (title, authors, year, abstract, citationCount)
- Filters by year range (2022-2024 for "recent" queries)
- Returns empty list when no results found

**arXiv Tool (`test_arxiv_tool.py`):**
- Returns top 5 preprints for valid query
- Handles XML parsing correctly
- Maps arXiv categories to venue labels
- Extracts arXiv ID and constructs PDF URL
- Handles malformed XML responses

**Local Corpus Tool (`test_local_tool.py`):**
- Embeds query using OpenAI API
- Performs pgvector cosine similarity search
- Returns papers above relevance threshold (≥0.7)
- Max 5 papers per query
- Handles empty corpus gracefully

**Synthesis (`test_synthesis.py`):**
- Generates cited answer from paper abstracts
- Citation format: `[1]`, `[2]` superscripts
- Citations reference correct papers by index
- Answer stays grounded in abstracts (no hallucination)
- Includes paper metadata in response
- Handles case where no papers retrieved

**Hybrid Retrieval (`test_hybrid_retrieval.py`):**
- Merges live + local results without duplicates (by DOI/arXiv ID)
- Sorts by relevance score descending
- Caps at 5 total papers
- Prefers local canonical when duplicate found
- Logs source distribution (X from S2, Y from local, etc.)

**Cost Tracker (`test_cost_tracker.py`):**
- Counts tokens from Claude API response headers
- Calculates cost correctly ($3/MTok input, $15/MTok output for Sonnet 4)
- Tracks per-query cost in `research_sessions` table
- Raises alert when daily spend exceeds $10
- Enforces 10 LLM call limit per query

**ReAct Agent (`test_react_agent.py`):**
- Mocked tools (don't hit real APIs in CI)
- Agent selects correct tool based on query intent
- Agent stops after retrieving papers (no infinite loops)
- Agent handles tool errors gracefully (retries once, then fails)
- Agent respects max iteration limit (10)

**Streaming (`test_streaming.py`):**
- SSE format: `data: {json}\n\n`
- Streams agent status updates
- Streams synthesis chunks
- Streams final paper metadata
- Sends `[DONE]` when complete
- Handles client disconnect mid-stream

### Mocking Strategy
**Mock External APIs in CI:**
- Semantic Scholar API → fixture JSON responses
- arXiv API → fixture XML responses
- OpenAI Embeddings API → dummy vectors (768-dim)
- Claude API → fixture synthesis responses

**Use Real APIs in Local Dev:**
- Set `PYTEST_ENV=local` to skip mocks
- Useful for debugging API integration issues
- Rate limit to avoid burning keys

### CI Integration
- Run on every PR to `main`
- Block merge if:
  - Any test fails
  - Coverage drops below 80%
  - New code has <60% coverage
- Store coverage reports in GitHub Actions artifacts

---

## Frontend Testing Strategy

### Framework
- **Jest** (29.x, waiting for React 19 compatibility)
- **React Native Testing Library** (@testing-library/react-native)
- **@testing-library/jest-native** (custom matchers)
- **react-test-renderer** (snapshot tests)

### Coverage Target
**≥70% coverage** when ecosystem compatible:
- Chat components (CitationRenderer, PaperDetailsPanel, StreamingMessage, MessageList)
- Timeline components (AgentNode, AgentTimeline)
- Integration: full ChatScreen flow

### Current Status
**React 19 Blocking Issue:**
- Jest 30 incompatible with React Native preset
- Downgraded to Jest 29 but still hitting compatibility issues
- Test files written and ready (see `frontend/components/**/__tests__/`)
- TypeScript compilation validates component structure in the meantime
- Tests will run when `jest-expo` updates for React 19

### Test Organization
```
frontend/
├── components/
│   ├── chat/__tests__/
│   │   ├── CitationRenderer.test.tsx
│   │   ├── PaperDetailsPanel.test.tsx
│   │   ├── StreamingMessage.test.tsx
│   │   └── MessageList.test.tsx
│   └── timeline/__tests__/
│       ├── AgentNode.test.tsx
│       └── AgentTimeline.test.tsx
└── app/__tests__/
    └── ChatScreen.test.tsx
```

### Key Test Cases

**CitationRenderer:**
- Renders citation number [1], [2], etc.
- Calls onPress with correct citation when tapped
- Applies gold color (#B8935F) and underline

**PaperDetailsPanel:**
- Renders paper metadata (title, authors, year, venue, abstract)
- Shows citation count
- "View Full Paper" button opens URL via Linking
- Modal closes when backdrop tapped

**StreamingMessage:**
- Renders user message with "You" label
- Renders assistant message with "Research Assistant" label
- Parses citations and injects CitationRenderer inline
- Shows eval scores badge when available
- Shows streaming indicator (animated dots) when isStreaming=true

**MessageList:**
- Renders list of messages via FlatList
- Auto-scrolls to bottom when new message arrives
- Shows empty state with example queries when messages=[]
- Passes onCitationPress handler to StreamingMessage

**AgentNode:**
- Renders agent symbol, label, description
- Shows status badge (PENDING, ACTIVE, COMPLETED, FAILED)
- Shows timestamp when available
- Shows metadata (papers found, tokens generated, etc.)
- Applies correct color per agent (sienna, amethyst, bronze, etc.)
- Dimmed opacity for pending, full saturation for completed

**AgentTimeline:**
- Renders "Research Workflow" header
- Shows activity indicator when agents running
- Renders AgentNode for each status
- Scrollable when >5 agents
- Shows footer hint when no activity

**ChatScreen (Integration):**
- Two-column layout on web (messages + timeline)
- Single column on mobile (timeline hidden)
- PaperDetailsPanel opens when citation tapped
- Modal closes when backdrop tapped
- TextInput submits query on Enter (web) or keyboard submit (mobile)
- KeyboardAvoidingView prevents input obscuring on iOS

### Testing Guidelines
- Use `render()` from @testing-library/react-native
- Use `fireEvent.press()` for touch interactions
- Use `getByText()`, `getByTestId()` for queries
- Avoid `UNSAFE_root` when possible (use semantic queries)
- Mock navigation (`jest.mock('expo-router')`)
- Mock Supabase client

### CI Integration
- Run on every PR to `main` (when React 19 compatible)
- Block merge if coverage drops below 70%
- Snapshot tests for visual regression

---

## E2E Testing Strategy

### Framework
- **Playwright** (for web version only)
- Run against `expo start --web` on localhost:8081
- CI: run in headless Chromium

### Coverage
**Critical Paths:**
1. Submit query → see streaming response → tap citation → view paper details → close modal
2. Submit query → see agent timeline update → agents complete → see eval scores
3. Submit second query → verify conversation history preserved
4. Mobile responsive: verify timeline hidden on narrow viewport

### Test Organization
```
e2e/
├── tests/
│   ├── query-flow.spec.ts       # Happy path
│   ├── citation-interaction.spec.ts
│   ├── agent-timeline.spec.ts
│   └── responsive.spec.ts
└── playwright.config.ts
```

### Key Test Cases

**Query Flow (`query-flow.spec.ts`):**
```typescript
test('submit query and receive cited answer', async ({ page }) => {
  await page.goto('http://localhost:8081');
  await page.fill('input[placeholder*="research question"]', 'What is a transformer?');
  await page.press('input', 'Enter');
  
  // Wait for streaming to complete
  await page.waitForSelector('text=/Research Assistant/', { timeout: 30000 });
  await page.waitForSelector('text=/transformer/i');
  
  // Verify citation present
  const citation = page.locator('text=/\\[1\\]/');
  await expect(citation).toBeVisible();
});
```

**Citation Interaction (`citation-interaction.spec.ts`):**
```typescript
test('tap citation opens paper details panel', async ({ page }) => {
  // ... submit query and wait for response
  
  await page.click('text=/\\[1\\]/');
  
  // Verify modal opened
  await expect(page.locator('text=/Paper Details/i')).toBeVisible();
  await expect(page.locator('text=/Abstract/i')).toBeVisible();
  
  // Close modal
  await page.click('text=/Close/i');
  await expect(page.locator('text=/Paper Details/i')).not.toBeVisible();
});
```

**Agent Timeline (`agent-timeline.spec.ts`):**
```typescript
test('agent timeline updates during query', async ({ page }) => {
  await page.goto('http://localhost:8081');
  
  // Verify timeline visible on web
  await expect(page.locator('text=/Research Workflow/i')).toBeVisible();
  
  await page.fill('input', 'What is attention mechanism?');
  await page.press('input', 'Enter');
  
  // Verify agents transition from pending → active → completed
  await expect(page.locator('text=/Semantic Scholar/i')).toBeVisible();
  await expect(page.locator('text=/COMPLETED/i').first()).toBeVisible({ timeout: 30000 });
});
```

**Responsive (`responsive.spec.ts`):**
```typescript
test('timeline hidden on mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
  await page.goto('http://localhost:8081');
  
  // Timeline should not render
  await expect(page.locator('text=/Research Workflow/i')).not.toBeVisible();
});
```

### CI Integration
- Run on every PR to `main` (after backend deployed to staging)
- Run against staging environment, not localhost
- Store Playwright trace on failure
- Block merge if critical path fails

---

## RAGAS Evaluation Plan

### Scope
**Local Corpus Queries Only** (deterministic retrieval from pgvector)

Why not live search?
- Live APIs return different results over time (new papers published)
- RAGAS requires ground truth answer + context
- Manual rubric better suited for non-deterministic search

### Metrics & Thresholds

| Metric | Description | Threshold | Failure Action |
|--------|-------------|-----------|----------------|
| **Faithfulness** | Answer grounded in retrieved papers (no hallucination) | ≥0.75 | Block PR merge |
| **Answer Relevancy** | Answer actually addresses the query | ≥0.70 | Block PR merge |
| **Context Precision** | Retrieved papers are relevant to query | ≥0.65 | Block PR merge |

### Test Set
**10 Seeded Query-Answer Pairs:**

1. **Query:** "What is the attention mechanism in transformers?"  
   **Ground Truth Answer:** "Attention is a mechanism that allows models to weigh the importance of different parts of the input when producing output [1]. Self-attention computes attention scores between all positions in a sequence [2]."  
   **Expected Papers:** Attention Is All You Need (Vaswani 2017), BERT (Devlin 2018)

2. **Query:** "How does Longformer handle long sequences?"  
   **Ground Truth:** "Longformer uses a combination of local windowed attention and global attention on selected tokens to reduce complexity from O(n²) to O(n) [1]."  
   **Expected Papers:** Longformer (Beltagy 2020)

3. **Query:** "What are sparse attention mechanisms?"  
   **Ground Truth:** "Sparse attention reduces the quadratic complexity of self-attention by only computing attention over a subset of positions [1][2]."  
   **Expected Papers:** Reformer (Kitaev 2020), Efficient Attention (Shen 2021)

4. **Query:** "What is retrieval-augmented generation?"  
   **Ground Truth:** "RAG combines retrieval from an external corpus with generation, allowing models to access up-to-date knowledge without retraining [1]."  
   **Expected Papers:** RAG (Lewis 2020)

5. **Query:** "How do vision transformers work?"  
   **Ground Truth:** "ViT splits images into patches, linearly embeds them, and processes them with a standard Transformer encoder [1]."  
   **Expected Papers:** ViT (Dosovitskiy 2020)

6. **Query:** "What is chain-of-thought prompting?"  
   **Ground Truth:** "CoT prompting improves reasoning by encouraging the model to generate intermediate reasoning steps before the final answer [1]."  
   **Expected Papers:** Chain-of-Thought (Wei 2022)

7. **Query:** "What are mixture-of-experts models?"  
   **Ground Truth:** "MoE models use multiple expert networks and a gating mechanism to route inputs, allowing scaling without proportional compute increase [1]."  
   **Expected Papers:** Switch Transformers (Fedus 2021)

8. **Query:** "What is RLHF?"  
   **Ground Truth:** "Reinforcement Learning from Human Feedback trains a reward model from human preferences, then uses it to fine-tune a language model via RL [1]."  
   **Expected Papers:** InstructGPT (Ouyang 2022)

9. **Query:** "How does GPT-4 differ from GPT-3?"  
   **Ground Truth:** "GPT-4 is a multimodal model accepting both text and image inputs, with improved reasoning and reduced hallucination compared to GPT-3 [1]."  
   **Expected Papers:** GPT-4 Technical Report (OpenAI 2023)

10. **Query:** "What is constitutional AI?"  
    **Ground Truth:** "Constitutional AI uses principles written in natural language to guide model behavior, reducing reliance on human feedback for every behavior [1]."  
    **Expected Papers:** Constitutional AI (Bai 2022)

### Test Data Storage
Store in `backend/tests/fixtures/ragas_test_set.json`:
```json
[
  {
    "query": "What is the attention mechanism in transformers?",
    "ground_truth_answer": "...",
    "expected_paper_ids": ["arxiv:1706.03762", "arxiv:1810.04805"],
    "ground_truth_context": ["Abstract of Attention Is All You Need...", "Abstract of BERT..."]
  },
  ...
]
```

### Execution
**Run on every backend PR:**
```bash
cd backend
pytest tests/eval/test_ragas.py --ragas
```

**Test Logic:**
1. For each test case:
   - Submit query to agent (using local corpus tool only, no live search)
   - Retrieve answer, citations, and retrieved papers
2. Compute RAGAS metrics:
   ```python
   from ragas import evaluate
   from ragas.metrics import faithfulness, answer_relevancy, context_precision
   
   results = evaluate(
       dataset=test_set,
       metrics=[faithfulness, answer_relevancy, context_precision]
   )
   ```
3. Assert thresholds:
   ```python
   assert results['faithfulness'] >= 0.75
   assert results['answer_relevancy'] >= 0.70
   assert results['context_precision'] >= 0.65
   ```

**On Failure:**
- Log which test case failed and which metric
- Log retrieved papers vs expected papers
- Store LangSmith trace URL for debugging
- Block PR merge

**Logging:**
- Store eval run in `eval_runs` table (Supabase)
- Store per-query scores in `eval_results` table
- Trend over time: are scores improving or degrading?

---

## Manual Evaluation Rubric

### Scope
**Live Academic Search Queries** (Semantic Scholar + arXiv)

Why manual?
- Results are non-deterministic (new papers published daily)
- No ground truth answer for novel research questions
- Human judgment needed for citation accuracy, recency, coverage

### Evaluation Criteria

#### 1. Citation Accuracy
**Question:** Do the cited papers actually support the claims made?

**Scoring:**
- For each citation `[N]`:
  - **Pass:** Claim is directly supported by the cited paper's abstract
  - **Fail:** Claim is not supported, or citation is wrong paper
  - **Partial:** Claim is tangentially related but not directly supported

**Example:**
- Claim: "Transformers use self-attention to process sequences in parallel [1]"
- Citation [1]: "Attention Is All You Need" (Vaswani 2017)
- **Result:** PASS (abstract explicitly describes self-attention and parallelization)

#### 2. Recency
**Question:** Does the answer include recent papers (2022-2024) when relevant?

**Scoring:**
- **Yes:** At least one paper from 2022-2024 cited (when query asks for "recent" or "latest")
- **No:** All papers pre-2022, despite query asking for recent work
- **N/A:** Query does not ask for recent work (e.g., "What is the original transformer paper?")

**Example:**
- Query: "What are recent advances in sparse attention?"
- Answer cites papers from 2023-2024: **YES**
- Answer cites only papers from 2019-2020: **NO**

#### 3. Coverage
**Question:** Does the answer miss obvious seminal works?

**Scoring:**
- List any major papers that should have been included but weren't
- **No Gaps:** All expected seminal works cited
- **Minor Gap:** 1-2 expected papers missing but answer still comprehensive
- **Major Gap:** Key foundational work missing, answer feels incomplete

**Example:**
- Query: "What is a transformer?"
- Answer cites "BERT" but not "Attention Is All You Need": **Major Gap**

#### 4. Source Diversity
**Question:** Does the answer present multiple perspectives, or just echo one source?

**Scoring:**
- **Balanced:** Cites 3+ different research groups/institutions
- **Skewed:** All papers from same author/group, or single perspective
- **N/A:** Query is narrow enough that single perspective is appropriate

**Example:**
- Query: "What are criticisms of transformers?"
- Answer cites papers from Google, Meta, EleutherAI discussing different limitations: **Balanced**
- Answer cites only Google papers: **Skewed**

### Sampling Strategy
**20% Random Sample:**
- Tag 20% of production queries with `needs_eval=true` (random selection)
- Store query, answer, citations, and retrieved papers in `eval_queue` table
- Manually evaluate weekly batch (Fridays)

**How to Select:**
```sql
SELECT * FROM research_sessions
WHERE needs_eval = true AND eval_status = 'pending'
ORDER BY created_at DESC
LIMIT 10;
```

### Evaluation Process
1. Read the query
2. Read the assistant's answer
3. For each citation:
   - Click through to paper (via source URL)
   - Read abstract
   - Verify claim is supported → mark Pass/Fail/Partial
4. Check recency: any 2022-2024 papers if query asks for recent?
5. Check coverage: any obvious missing papers?
6. Check diversity: multiple perspectives?
7. Record results in `eval_results` table:
   ```sql
   INSERT INTO eval_results (session_id, citation_accuracy, recency, coverage, source_diversity, evaluator, notes)
   VALUES ('...', 0.85, 'Yes', 'No Gaps', 'Balanced', 'chris', 'Good answer, covered key papers');
   ```

### Trending
- Weekly report: % citation accuracy across all evaluated queries
- Track over time: is quality improving?
- Flag degradation: if citation accuracy drops below 80%, investigate

---

## LangSmith Trace Verification

### Goal
Every production query must have a LangSmith trace for debugging and cost transparency.

### What to Verify in Traces

#### 1. Token Counts Match
- LangSmith trace shows total input/output tokens
- Compare to Claude API response headers (`x-anthropic-input-tokens`, `x-anthropic-output-tokens`)
- Assert: LangSmith tokens == API headers tokens
- Why: Catch discrepancies in cost calculation

#### 2. Agent Tool Calls Logged
- Verify each tool invocation appears in trace:
  - `search_semantic_scholar` with query parameter
  - `search_arxiv` with query parameter
  - `search_local_corpus` with query parameter
  - Tool outputs (papers retrieved)
- Why: Debugging failed queries requires seeing what tools were called

#### 3. No Silent Errors
- Check trace for any tool calls that returned errors
- Verify errors were surfaced to user (not swallowed)
- Why: Silent failures degrade UX without visibility

#### 4. Streaming Chunks Captured
- Verify synthesis stream appears in trace
- Check that chunks are in order
- Why: Debugging incomplete/garbled responses

### Automated Checks
**Run daily cron job:**
```python
# backend/scripts/verify_traces.py
from langsmith import Client

client = Client()

# Get yesterday's traces
traces = client.list_runs(
    project_name="multi-agent-research",
    start_time=yesterday,
    end_time=today
)

for trace in traces:
    # Check 1: Token counts match
    assert trace.total_tokens == trace.metadata['api_tokens']
    
    # Check 2: Tool calls logged
    tool_calls = [run for run in trace.child_runs if run.run_type == 'tool']
    assert len(tool_calls) > 0
    
    # Check 3: No silent errors
    for run in trace.child_runs:
        if run.error:
            assert run.error in trace.outputs['error_message']
    
    # Check 4: Streaming captured
    if trace.metadata['streaming']:
        assert len(trace.outputs['chunks']) > 0
```

**On Failure:**
- Send alert to Slack/email
- Log trace URL for manual investigation

### Trace URL in Response
Include LangSmith trace URL in response metadata:
```json
{
  "answer": "...",
  "citations": [...],
  "papers": [...],
  "metadata": {
    "trace_url": "https://smith.langchain.com/public/trace/...",
    "cost": 0.042,
    "total_tokens": 1543
  }
}
```

Display in frontend (dev mode only):
- Add "View Trace" link in eval scores badge
- Link opens LangSmith trace in new tab

---

## Quality Gates

### v0.6 - TESTS APPROVED
**Deliverable:** This document (TESTS.md)  
**Approval Criteria:**
- Test strategy covers backend, frontend, E2E
- RAGAS eval plan defined with seeded test set
- Manual rubric defined with 4 criteria
- LangSmith trace verification plan documented

**Approval Token:** `TESTS APPROVED`

### v0.11 - EVALUATION GATES
**Backend tests passing:**
- ≥80% coverage on core logic
- All unit tests pass
- All integration tests pass

**RAGAS thresholds met:**
- Faithfulness ≥0.75
- Answer Relevancy ≥0.70
- Context Precision ≥0.65

**Manual eval baseline:**
- 10 queries manually evaluated
- Citation accuracy ≥80%
- Coverage: no major gaps
- Source diversity: balanced on multi-perspective queries

**LangSmith traces:**
- All production queries have trace URLs
- Daily verification script passing

### v1.0 - PRODUCTION READY
**All tests passing:**
- Backend: pytest suite green
- Frontend: Jest suite green (when React 19 compatible)
- E2E: Playwright critical paths green

**Eval metrics stable:**
- RAGAS scores above thresholds for 2 weeks
- Manual eval showing ≥80% citation accuracy
- No trace verification failures

**Cost monitoring:**
- Daily spend <$10 on default keys
- Per-query cost avg <$0.10

---

## Test Execution Commands

**Backend:**
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run RAGAS eval only
pytest tests/eval/test_ragas.py --ragas

# Run specific test file
pytest tests/unit/test_s2_tool.py -v
```

**Frontend:**
```bash
cd frontend

# Run all tests (when React 19 compatible)
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

**E2E:**
```bash
cd e2e

# Run all Playwright tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific test
npx playwright test tests/query-flow.spec.ts
```

**LangSmith Verification:**
```bash
cd backend

# Run daily trace verification
python scripts/verify_traces.py --date=2026-05-09
```

---

**Last Updated:** 2026-05-12  
**Status:** TESTS APPROVED ✅ (v0.6 approved 2026-05-10)

## Implementation Status

- **v0.6 TESTS APPROVED:** Test strategy documented ✅
- **v0.11b Evaluation Framework:** Implementation complete ✅
  - RAGAS evaluator module created
  - Manual rubric module created
  - 10-query test set defined
  - Background evaluation task integrated
  - Results logged to `eval_results` table
- **Backend tests:** Unit tests passing (pytest)
- **Frontend tests:** Awaiting React 19 compatibility (test files ready)
- **E2E tests:** Manual testing complete, automated E2E pending
