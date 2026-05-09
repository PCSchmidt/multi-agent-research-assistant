# VERSION_ROADMAP.md
# Full gate roadmap: v0.0 → v1.0 Production Live

**Calibration multiplier applied:** 2.0x (default - fewer than 3 prior estimation entries)

**Total estimated hours:** 50-87h (raw estimates × 2.0x multiplier)

## Roadmap Structure

This is a Production build. The roadmap follows Syntaris's five-phase model:
1. **SCOPE CONFIRMED** - Foundation files, architecture locked
2. **MOCKUPS APPROVED** - Visual design, component specs
3. **FRONTEND APPROVED** - Static UI implementation
4. **TESTS APPROVED** - Test strategy, RAGAS eval plan
5. **GO** (multiple gates) - Backend, deployment, production launch

---

## Phase 1: Foundation

### v0.0 - SCOPE CONFIRMED
**Goal:** Lock project scope, stack, agent architecture  
**Deliverables:** CONTRACT.md, SPEC.md, VERSION_ROADMAP.md, DECISIONS.md, memory files  
**Estimate:** 4-6h (2-3h × 2.0x)  
**Status:** In progress  
**Approval token:** `SCOPE CONFIRMED`

---

## Phase 2: Design

### v0.1 - MOCKUPS APPROVED
**Goal:** Visual design system and wireframes for all screens  
**Deliverables:**
- DESIGN_SYSTEM.md (colors, typography, spacing, component patterns)
- FRONTEND_SPEC.md (component hierarchy, props, state patterns)
- Wireframes (chat panel, agent timeline, source panel, auth screens)
- Empty state designs
- Citation renderer mockup

**Estimate:** 6-10h (3-5h × 2.0x)  
**Status:** Pending  
**Approval token:** `MOCKUPS APPROVED`

---

## Phase 3: Frontend Implementation

### v0.2 - Frontend Shell
**Goal:** Next.js app scaffolding, routing, auth UI (no backend wire-up)  
**Deliverables:**
- Next.js 14 App Router project initialized
- Supabase Auth UI components (login, signup, password reset)
- Layout with navigation
- Protected route middleware
- Tailwind configured per design system

**Estimate:** 5-8h  
**Status:** Pending  
**Blocked by:** MOCKUPS APPROVED

### v0.3 - Chat UI Components
**Goal:** Static chat panel, streaming placeholder, citation renderer  
**Deliverables:**
- ChatPanel component with input and message list
- StreamingMessage component (simulated streaming with mock data)
- CitationRenderer component (numbered superscripts)
- SourcePanel component (shows chunk when citation clicked)
- Empty states for all components

**Estimate:** 4-7h  
**Status:** Pending  
**Blocked by:** v0.2

### v0.4 - Agent Timeline UI
**Goal:** Agent status visualization  
**Deliverables:**
- AgentTimeline component
- Status indicators for each node (Planner, Retriever, Critic, Synthesizer, Evaluator)
- Active/completed/pending states with visual transitions
- EvalBadge component (shows RAGAS scores)

**Estimate:** 3-5h  
**Status:** Pending  
**Blocked by:** v0.3

### v0.5 - FRONTEND APPROVED
**Goal:** All UI components working with mock data, component tests passing  
**Deliverables:**
- Playwright smoke tests (auth flow, chat interaction, citation clicks)
- Vitest component tests for ChatPanel, CitationRenderer, AgentTimeline
- Visual regression screenshots
- No console errors
- Responsive design verified (desktop, tablet, mobile)

**Estimate:** 4-6h  
**Status:** Pending  
**Approval token:** `FRONTEND APPROVED`  
**Blocked by:** v0.4

---

## Phase 4: Test Strategy

### v0.6 - TESTS APPROVED
**Goal:** Test plan locked, RAGAS eval strategy defined  
**Deliverables:**
- TESTS.md with coverage targets:
  - Backend: pytest, ≥80% coverage on agent nodes
  - Frontend: vitest, ≥70% coverage on components
  - E2E: Playwright, critical paths (auth, query → answer, citation click)
- RAGAS eval plan:
  - Seeded test set (10 query-answer pairs)
  - Faithfulness ≥ 0.75
  - Answer relevancy ≥ 0.70
  - Context precision ≥ 0.65
- LangSmith trace verification plan

**Estimate:** 10-16h (5-8h × 2.0x)  
**Status:** Pending  
**Approval token:** `TESTS APPROVED`  
**Blocked by:** FRONTEND APPROVED

---

## Phase 5: Backend Implementation

### v0.7 - Backend Foundation
**Goal:** FastAPI scaffold, Supabase schema, health check  
**Deliverables:**
- FastAPI app with /health endpoint
- Supabase schema migration (users, research_sessions, sources, eval_logs)
- pgvector extension enabled
- Supabase client initialized (Python SDK)
- Environment variable validation on startup
- Docker Compose with FastAPI + Supabase (local dev)

**Estimate:** 4-6h  
**Status:** Pending  
**Blocked by:** TESTS APPROVED

### v0.8 - LangGraph Agent DAG
**Goal:** Agent state graph wired, nodes stubbed  
**Deliverables:**
- ResearchState Pydantic model (query, sub_questions, chunks, answer, citations, eval_scores)
- LangGraph StateGraph with five nodes (plan, retrieve, critique, synthesize, eval)
- Each node accepts state, returns updated state
- Nodes stubbed with TODO comments (no LLM calls yet)
- Graph compilation verified (no cycles, proper edges)

**Estimate:** 5-8h  
**Status:** Pending  
**Blocked by:** v0.7

### v0.9 - Planner + Synthesizer Nodes
**Goal:** LLM-powered planning and synthesis working  
**Deliverables:**
- Planner node: query → sub_questions (Claude Sonnet with structured output)
- Synthesizer node: filtered_chunks → cited answer (Claude Sonnet with streaming)
- FastAPI streaming endpoint (/api/research/stream) using SSE
- Frontend wired to SSE endpoint (real streaming, not mock)
- Citation format: [1], [2], etc. with source mapping

**Estimate:** 6-10h  
**Status:** Pending  
**Blocked by:** v0.8

### v0.10 - Vector Retrieval + Critic
**Goal:** Semantic search and chunk filtering working  
**Deliverables:**
- Document ingestion CLI script (text files → embeddings → pgvector)
- Retriever node: sub_questions → pgvector cosine similarity search → top-k chunks
- Critic node: chunks → relevance scoring → filtered_chunks
- Seed vector store with 50-100 sample chunks (research papers, docs, etc.)
- End-to-end flow working: query → plan → retrieve → critique → synthesize → streamed answer

**Estimate:** 7-12h  
**Status:** Pending  
**Blocked by:** v0.9  
**Note:** Requires real OpenAI API key (replace OpenRouter key before this gate)

### v0.11 - RAGAS Evaluation
**Goal:** Eval pipeline running, scores logged  
**Deliverables:**
- Evaluator node (async): answer + chunks → RAGAS metrics
- RAGAS metrics: faithfulness, answer_relevancy, context_precision
- Metrics logged to Supabase eval_logs table
- EvalBadge in UI shows real scores from DB
- Seeded test set evaluated, all thresholds met (≥ 0.75, ≥ 0.70, ≥ 0.65)
- Pytest tests for RAGAS pipeline reproducibility

**Estimate:** 5-8h  
**Status:** Pending  
**Blocked by:** v0.10

### v0.12 - LangSmith Integration
**Goal:** Agent traces visible in LangSmith dashboard  
**Deliverables:**
- LangSmith tracing enabled (LANGCHAIN_TRACING_V2=true)
- All LangGraph nodes tagged with metadata (node name, user_id, session_id)
- Traces appearing in LangSmith project "multi-agent-research-assistant"
- Trace links logged to Supabase research_sessions table
- LangSmith dashboard screenshot in README

**Estimate:** 3-5h  
**Status:** Pending  
**Blocked by:** v0.11

---

## Phase 6: Deployment & Launch

### v0.13 - Docker Compose Polish
**Goal:** Single-command local dev startup  
**Deliverables:**
- docker-compose.yml with frontend, backend, Supabase (local)
- .env.example file with all required variables
- README section: "Local Development Setup"
- Verified: `docker-compose up` → working app on localhost

**Estimate:** 3-5h  
**Status:** Pending  
**Blocked by:** v0.12

### v0.14 - CI/CD Pipeline
**Goal:** GitHub Actions running tests on every push  
**Deliverables:**
- .github/workflows/ci.yml
- Jobs: lint (ruff, eslint), type-check (mypy, tsc), test (pytest, vitest), build
- Branch protection on main (require CI passing)
- Status badge in README

**Estimate:** 3-5h  
**Status:** Pending  
**Blocked by:** v0.13

### v0.15 - Multi-Provider BYOK + Settings
**Goal:** Users can optionally provide their own API keys; owner's keys as default  
**Deliverables:**
- Settings page UI (Next.js):
  - Provider selection (Anthropic, OpenAI, OpenRouter)
  - API key input per provider with show/hide toggle
  - Save/update/delete key actions
  - Test key connection button
- Backend key management (FastAPI):
  - `/api/keys` CRUD endpoints
  - Key encryption using pgcrypto (Supabase)
  - Key hierarchy: user keys override default (owner's) keys
- LiteLLM integration:
  - Replace direct Anthropic/OpenAI SDK calls with LiteLLM
  - Dynamic provider selection based on user keys
  - Fallback to default keys if user keys not present
- Supabase schema:
  - `user_api_keys` table with RLS policies
  - pgcrypto encryption for `encrypted_key` column
- Controlled access:
  - Email allowlist or manual approval flow
  - Only owner-approved users can sign up
- Tests:
  - Key encryption/decryption
  - Provider fallback logic
  - Settings page component tests

**Estimate:** 6-9h  
**Status:** Pending  
**Blocked by:** v0.14

### v1.0 - Production Live (GO)
**Goal:** App deployed and accessible to portfolio reviewers  
**Deliverables:**
- Frontend deployed (Vercel or similar)
- Backend deployed (Railway, Render, or similar)
- Supabase production project configured
- Production .env vars set (owner's default keys)
- Controlled access configured (email allowlist or approval flow)
- Live URL in README
- CHANGELOG.md final entry
- HANDOFF.md (portfolio case study document)
- Git tag: `v1.0-production-live`
- Public GitHub repo

**Estimate:** 8-16h (4-8h × 2.0x)  
**Status:** Pending  
**Approval token:** `GO`  
**Blocked by:** v0.15

---

## Gate Summary

| Version | Gate Name | Estimate | Status | Blocked By |
|---------|-----------|----------|--------|------------|
| v0.0 | SCOPE CONFIRMED | 4-6h | ✅ DONE (3.5h actual) | - |
| v0.1 | MOCKUPS APPROVED | 6-10h | Pending | v0.0 approval |
| v0.2 | Frontend Shell | 5-8h | Pending | v0.1 approval |
| v0.3 | Chat UI Components | 4-7h | Pending | v0.2 |
| v0.4 | Agent Timeline UI | 3-5h | Pending | v0.3 |
| v0.5 | FRONTEND APPROVED | 4-6h | Pending | v0.4 |
| v0.6 | TESTS APPROVED | 10-16h | Pending | v0.5 approval |
| v0.7 | Backend Foundation | 4-6h | Pending | v0.6 approval |
| v0.8 | LangGraph Agent DAG | 5-8h | Pending | v0.7 |
| v0.9 | Planner + Synthesizer | 6-10h | Pending | v0.8 |
| v0.10 | Vector Retrieval + Critic | 7-12h | Pending | v0.9 |
| v0.11 | RAGAS Evaluation | 5-8h | Pending | v0.10 |
| v0.12 | LangSmith Integration | 3-5h | Pending | v0.11 |
| v0.13 | Docker Compose Polish | 3-5h | Pending | v0.12 |
| v0.14 | CI/CD Pipeline | 3-5h | Pending | v0.13 |
| v0.15 | Multi-Provider BYOK + Settings | 6-9h | Pending | v0.14 |
| v1.0 | Production Live (GO) | 8-16h | Pending | v0.15 |

**Total gates:** 17  
**Total estimated hours:** 86-147h (with 2.0x calibration multiplier applied to raw estimates)

---

## Variance Drivers (High Uncertainty Gates)

- **v0.6 TESTS APPROVED** (range: 10-16h) - First time defining RAGAS eval strategy; test set creation and threshold tuning can vary significantly
- **v0.10 Vector Retrieval + Critic** (range: 7-12h) - pgvector setup and tuning, chunk re-ranking logic, potential retrieval quality iterations
- **v1.0 Production Live** (range: 8-16h) - Deployment platform unknowns, environment config debugging, DNS/SSL setup

All other gates have tighter ranges (±2-3h) reflecting clearer scope.

---

**Roadmap established:** 2026-05-09  
**Next checkpoint:** SCOPE CONFIRMED approval required to proceed to v0.1
