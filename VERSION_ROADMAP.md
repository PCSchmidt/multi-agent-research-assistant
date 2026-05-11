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
**Goal:** Expo app scaffolding with React Native, routing, auth UI (no backend wire-up)  
**Deliverables:**
- Expo SDK 52+ project initialized (iOS, Android, Web targets)
- Expo Router configured (file-based routing)
- Supabase React Native SDK integrated
- Auth screens (login, signup, password reset) with React Native components
- Layout with navigation (tab/stack navigators)
- Protected route middleware (Expo Router auth guards)
- NativeWind configured per design system tokens
- Verified on: iOS Simulator/Android Emulator/Web browser

**Estimate:** 7-10h (Expo setup, native navigation patterns, cross-platform auth flow)  
**Status:** Pending  
**Blocked by:** MOCKUPS APPROVED

### v0.3 - Chat UI Components
**Goal:** Static chat panel, streaming placeholder, citation renderer (React Native components)  
**Deliverables:**
- ChatPanel component with TextInput and FlatList (React Native)
- StreamingMessage component (simulated streaming with mock data)
- CitationRenderer component (numbered superscripts, touchable)
- SourcePanel component (bottom sheet or modal, shows chunk when citation tapped)
- Empty states for all components
- NativeWind styling matching design system
- Touch interaction patterns (tap, swipe, scroll)

**Estimate:** 5-8h (React Native components, touch interactions, cross-platform layout)  
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
**Goal:** All UI components working with mock data, tests passing on all platforms  
**Deliverables:**
- Detox E2E tests (auth flow, chat interaction, citation taps) on iOS/Android
- Playwright tests for web build
- Jest/React Native Testing Library component tests
- Visual regression screenshots (iOS, Android, web)
- No console errors/warnings across platforms
- Responsive design verified (mobile portrait/landscape, tablet, web desktop)

**Estimate:** 5-8h (Detox setup, multi-platform test verification)  
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
- Supabase schema migration (users, research_sessions, papers, eval_logs)
- pgvector extension enabled (for local canonical corpus)
- Supabase client initialized (Python SDK)
- Environment variable validation on startup
- Docker Compose with FastAPI + Supabase (local dev)
- Cost tracking middleware (log LLM calls, token usage per request)

**Estimate:** 4-6h  
**Status:** Pending  
**Blocked by:** TESTS APPROVED

### v0.8 - ReAct Agent + Academic API Tools
**Goal:** LangGraph ReAct agent with academic search tools working  
**Deliverables:**
- ResearchState Pydantic model (query, papers, synthesis, citations, eval_scores)
- LangGraph agent with tool-calling capability (ReAct pattern)
- **Tools implemented:**
  - `search_semantic_scholar(query, year_range, limit)` - S2 API integration
  - `search_arxiv(query, category, limit)` - arXiv API integration
  - `get_paper_details(paper_id)` - fetch abstract, citations, venue, authors
  - `search_local_corpus(query)` - pgvector search over canonical papers
  - `synthesize_findings()` - trigger synthesis when ready
- API key management (S2 API key, arXiv no auth needed)
- Tool execution verified (can fetch real paper metadata)
- **Cost caps in middleware:** max 5 papers/query, max 10 LLM calls/query, circuit breaker

**Estimate:** 7-10h  
**Status:** Pending  
**Blocked by:** v0.7

### v0.9 - Hybrid Retrieval + Paper Ingestion
**Goal:** Combine live academic search with local canonical corpus  
**Deliverables:**

- ✅ **Live search:** Agent can search S2/arXiv for recent papers (2022-2024)
- ✅ **Local corpus:** pgvector search over pre-seeded canonical works
- ✅ **Hybrid merge logic:** Combine results by relevance, recency, citation count
- ✅ **CLI ingestion script:** Feed canonical papers (PDF → extract abstract/metadata → embed → pgvector)
- 🔄 **Seed local corpus:** 5/20-50 canonical papers seeded (can add more incrementally)
- ✅ **OpenAI embeddings integration:** text-embedding-3-small working
- ⚠️ **End-to-end retrieval:** Implemented but E2E test blocked by network connectivity

**Estimate:** 7-10h  
**Actual:** ~4h  
**Status:** 85% Complete (E2E verification pending)  
**Completed:** Core functionality done 2026-05-11  

**What Was Built:**

- Module-level paper storage mechanism for hybrid merge
- Tools store Paper objects during execution while returning text to LLM
- extract_papers_node: retrieves → deduplicates → sorts (relevance > citations > year)
- Fixed local corpus search (admin client bypasses RLS)
- Fixed arXiv API (HTTP → HTTPS + follow_redirects)
- CLI ingestion script with 3 modes (file/S2 ID/seed defaults)
- 5 foundational papers seeded with embeddings

**Testing:**

- 19 unit tests passing (6 hybrid merge, 6 local corpus, 7 prior)
- Integration test verifies full hybrid flow
- E2E test created but blocked by network (can run when available)

**Remaining:**

- E2E verification with real agent + network
- Optional: Seed 15-45 more canonical papers

### v0.10 - Synthesis + Streaming
**Goal:** Agent synthesizes findings and streams cited answer  
**Deliverables:**
- Synthesis logic: papers (abstracts + metadata) → cited answer with proper attribution
- Citation format: [1], [2] with source mapping (title, authors, year, venue, link)
- FastAPI streaming endpoint (/api/research/stream) using SSE
- Frontend wired to SSE endpoint (real streaming, not mock)
- Agent decision-making: decides when to search more vs. synthesize
- Error handling: rate limits, API failures, no results found

**Estimate:** 6-9h  
**Status:** Pending  
**Blocked by:** v0.9

### v0.11 - Evaluation (RAGAS + Manual Rubric)
**Goal:** Eval pipeline for both local corpus (RAGAS) and live research (manual rubric)  
**Deliverables:**
- **RAGAS evaluation (local pgvector corpus only):**
  - Evaluator async task: answer + chunks → faithfulness, answer_relevancy, context_precision
  - Seeded test set (10 queries) for local corpus, thresholds: ≥ 0.75, ≥ 0.70, ≥ 0.65
  - Logged to Supabase eval_logs table
- **Manual eval rubric (live academic search):**
  - Citation accuracy: Do cited papers support claims? (manual check)
  - Recency: Includes recent papers when relevant? (automated metric)
  - Coverage: Misses obvious seminal works? (manual check)
  - Source diversity: Multiple perspectives vs. echo chamber? (automated metric)
  - Test set: 10 academic queries across domains (ML, medicine, physics)
- EvalBadge in UI shows RAGAS scores (local) + manual quality rating (live)
- Pytest tests for RAGAS reproducibility

**Estimate:** 6-9h  
**Status:** Pending  
**Blocked by:** v0.10

### v0.12 - LangSmith Integration + Cost Analytics
**Goal:** Agent traces visible in LangSmith, cost tracking dashboard  
**Deliverables:**
- LangSmith tracing enabled (LANGCHAIN_TRACING_V2=true)
- All agent tool calls tagged with metadata (user_id, session_id, query, tools_used)
- Traces appearing in LangSmith project "multi-agent-research-assistant"
- Trace links logged to Supabase research_sessions table
- **Cost analytics dashboard:** tokens used, LLM calls, cost per query, daily spend
- Budget alerts (email if daily spend > $10)
- Rate limiting verified (10 queries/hour on default keys)
- LangSmith dashboard screenshot in README

**Estimate:** 4-6h  
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
**Goal:** App deployed on iOS, Android, and web - accessible to portfolio reviewers  
**Deliverables:**
- **iOS:** App submitted to TestFlight (or App Store), invite link in README
- **Android:** App in Play Console internal testing (or production), link in README
- **Web:** Deployed to Vercel (or similar), live URL in README
- **Backend:** Deployed (Railway, Render, or similar)
- Supabase production project configured
- Production .env vars set (owner's default keys)
- Controlled access configured (email allowlist or approval flow)
- EAS Build configuration (eas.json)
- App store metadata (screenshots, descriptions, icons) for iOS/Android
- CHANGELOG.md final entry
- HANDOFF.md (portfolio case study document)
- Git tag: `v1.0-production-live`
- Public GitHub repo

**Estimate:** 12-20h (EAS Build setup, TestFlight/Play Console, app store metadata, multi-platform deployment coordination)  
**Status:** Pending  
**Approval token:** `GO`  
**Blocked by:** v0.15

---

## Gate Summary

| Version | Gate Name | Estimate | Status | Blocked By |
|---------|-----------|----------|--------|------------|
| v0.0 | SCOPE CONFIRMED | 4-6h | ✅ DONE (3.5h actual) | - |
| v0.1 | MOCKUPS APPROVED | 6-10h | ✅ DONE (6h actual) | v0.0 approval |
| v0.2 | Frontend Shell | 7-10h | ✅ DONE (~8h actual) | v0.1 approval |
| v0.3 | Chat UI Components | 5-8h | Pending | v0.2 approval |
| v0.4 | Agent Timeline UI | 3-5h | Pending | v0.3 |
| v0.5 | FRONTEND APPROVED | 5-8h | Pending | v0.4 |
| v0.6 | TESTS APPROVED | 10-16h | Pending | v0.5 approval |
| v0.7 | Backend Foundation | 4-6h | Pending | v0.6 approval |
| v0.8 | ReAct Agent + Academic APIs | 7-10h | Pending | v0.7 |
| v0.9 | Hybrid Retrieval + Ingestion | 7-10h | Pending | v0.8 |
| v0.10 | Synthesis + Streaming | 6-9h | Pending | v0.9 |
| v0.11 | Evaluation (RAGAS + Manual) | 6-9h | Pending | v0.10 |
| v0.12 | LangSmith + Cost Analytics | 4-6h | Pending | v0.11 |
| v0.13 | Docker Compose Polish | 3-5h | Pending | v0.12 |
| v0.14 | CI/CD Pipeline | 3-5h | Pending | v0.13 |
| v0.15 | Multi-Provider BYOK + Settings | 6-9h | Pending | v0.14 |
| v1.0 | Production Live (GO) | 12-20h | Pending | v0.15 |

**Total gates:** 17  
**Total estimated hours (raw):** 65-95h  
**With 2.0x calibration multiplier:** 130-190h  
**Architecture:** Academic Research Assistant (live API search + local canonical corpus, abstract-based synthesis)

---

## Variance Drivers (High Uncertainty Gates)

- **v0.6 TESTS APPROVED** (range: 10-16h) - First time defining manual eval rubric for academic research; test set creation across domains (ML, medicine, physics) can vary
- **v0.8 ReAct Agent + Academic APIs** (range: 7-10h) - Semantic Scholar/arXiv API integration, rate limit handling, cost cap middleware tuning
- **v0.9 Hybrid Retrieval** (range: 7-10h) - Merge logic for live + local results, relevance ranking, canonical corpus curation
- **v1.0 Production Live** (range: 12-20h) - EAS Build (iOS/Android), TestFlight/Play Console setup, multi-platform deployment coordination

All other gates have tighter ranges (±2-3h) reflecting clearer scope.

---

**Roadmap established:** 2026-05-09  
**Next checkpoint:** SCOPE CONFIRMED approval required to proceed to v0.1
