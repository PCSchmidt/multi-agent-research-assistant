# CHANGELOG.md
# Project change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v0.13] - 2026-05-13 - Docker Compose Polish

### Added

- **Docker Compose Configuration**
  - Polished docker-compose.yml with comprehensive comments and usage instructions
  - Backend service with FastAPI + hot-reload enabled
  - Frontend service with Expo web server
  - Named volume for frontend node_modules (performance improvement on Windows/Mac)
  - Health checks for backend service
  - Restart policies (unless-stopped) for both services
  - Network isolation (research-net bridge network)
  
- **Environment Configuration**
  - Root .env.example as pointer to backend/.env.example
  - Clear documentation of required API keys
  - Environment variable for EXPO_PUBLIC_API_URL in docker-compose.yml
  
- **Documentation**
  - Docker Compose Quick Start section in README.md
  - "Option 1: Docker Compose (Recommended)" vs "Option 2: Manual Setup" paths
  - DOCKER.md reference guide created
  - Usage instructions: up, down, logs, restart commands
  - Troubleshooting section for common Docker issues
  - Mobile development notes (Docker web-only, use npm start for iOS/Android)
  
- **Verification Script**
  - docker-verify.sh script for automated testing
  - Checks: Docker running, .env exists, services healthy, endpoints accessible
  - Output shows running containers and service URLs

### Changed

- Updated README.md to mark Docker Compose as implemented (moved from "In Progress")
- Improved docker-compose.yml command for frontend: uses `npx expo start --web`
- Added port 19000 for Expo Dev Tools (optional)

### Status

- Gate closed: 2026-05-13
- Actual hours: ~2h
- Status: 100% complete
- Next gate: v0.14 - CI/CD Pipeline

---

## [v0.0] - 2026-05-09 - SCOPE CONFIRMED

### Added
- PROJECT FOUNDATION
  - CONTRACT.md: Project identity, stack, build type, success criteria
  - VERSION_ROADMAP.md: Full 17-gate roadmap v0.0 → v1.0 (86-147h estimated)
  - SPEC.md: Current gate specification
  - DECISIONS.md: 7 architectural decisions documented
  - CHANGELOG.md: This file
  - Memory files: MEMORY_SEMANTIC.md, MEMORY_EPISODIC.md, MEMORY_CORRECTIONS.md
  
- ARCHITECTURE DECISIONS
  - LangGraph for multi-agent orchestration (Planner → Retriever → Critic → Synthesizer → Evaluator)
  - pgvector on Supabase (single DB, simpler ops)
  - Claude Sonnet 4 for all agent nodes (consistency)
  - Async Evaluator node (low latency)
  - Multi-provider BYOK with LiteLLM (Anthropic, OpenAI, OpenRouter)
  - Email auth only for v1.0 (defer OAuth)
  - Seeded RAGAS test set (reproducibility)

- SCOPE LOCKED
  - Build type: Production → v1.0 Production Live
  - Stack: Next.js 14 + FastAPI + LangGraph + Supabase + pgvector + LiteLLM
  - LLM: Claude Sonnet 4 (claude-sonnet-4-20250514)
  - Embeddings: OpenAI text-embedding-3-small
  - Evals: RAGAS (faithfulness ≥0.75, answer relevancy ≥0.70, context precision ≥0.65)
  - Tracing: LangSmith
  - BYOK: Multi-provider support with owner keys as default

### Status
- Gate closed: 2026-05-09
- Actual hours: ~3.5h
- Next gate: v0.1 - MOCKUPS APPROVED

---

## [v0.3] - 2026-05-11 - Chat UI Components (Retroactive)

### Added

- **Chat Components (React Native)**
  - StreamingMessage component with citation parsing
  - CitationRenderer component (touchable, numbered superscripts)
  - PaperDetailsPanel modal (bottom sheet for paper details)
  - MessageList component with FlatList
  - Main chat screen in app/(tabs)/index.tsx
  
- **Streaming & Interaction**
  - Animated streaming indicator (three pulsing dots)
  - Citation tap handling (opens paper details panel)
  - Keyboard-aware scrolling (KeyboardAvoidingView)
  - Safe area handling for mobile devices
  
- **Eval Badge Integration**
  - Quality scores display in StreamingMessage
  - Shows faithfulness, relevancy, citation accuracy
  - Green badge styling (success-500 color)
  - Conditional rendering when eval scores available
  
- **Styling**
  - Native StyleSheet matching DESIGN_SYSTEM.md colors
  - Touch interaction patterns (TouchableOpacity)
  - Message bubbles with user/assistant differentiation
  - Responsive max-width (85% of screen)

### Status

- Gate closed: 2026-05-11 (retroactive - components built during backend development)
- Actual hours: ~6h
- Status: 100% complete
- Next gate: v0.4 - Agent Timeline UI

---

## [v0.4] - 2026-05-11 - Agent Timeline UI (Retroactive)

### Added

- **Timeline Components**
  - AgentTimeline component (header, scrollable, footer)
  - AgentNode component (individual agent status display)
  - Activity indicator (animated dot + "In Progress" label)
  - Empty state hint text
  
- **Status Visualization**
  - Pending, active, completed status badges
  - Color-coded by agent type (design system colors)
  - Timestamp display when available
  - Metadata display (papers found, tokens, etc.)
  
- **Layout**
  - Scrollable timeline (max-height: 400px)
  - Border styling matching design system
  - Header with "Research Workflow" title
  - Footer hint when no activity
  
### Status

- Gate closed: 2026-05-11 (retroactive - components built during backend development)
- Actual hours: ~4h
- Status: 100% complete
- Next gate: v0.5 - FRONTEND APPROVED (pending test tooling)

---

## [v0.1] - 2026-05-09 - MOCKUPS APPROVED

### Added
- DESIGN SYSTEM (Esoteric Research Aesthetic)
  - DESIGN_SYSTEM.md: Complete visual language for academic luxury interface
  - Color palette: Antique gold (#D4A574), parchment (#F5F3F0), scholarly neutrals
  - Agent colors: Alchemical symbolism (amethyst, sienna, vermillion, verdigris, gold)
  - Typography: Crimson Pro serif (authority), Inter sans (readability), IBM Plex Mono (precision)
  - Spacing: 8px base unit (generous breathing room), 1440px max width
  - Components: Paper textures, gold accents, refined materials, slow ceremonial animations
  - Icons: Alchemical glyphs (☉ sulfur, ⚖ balance, ⚭ borromean rings)
  
- FRONTEND ARCHITECTURE
  - FRONTEND_SPEC.md: Component hierarchy, TypeScript interfaces, data flow
  - Page structure: Next.js App Router (auth, dashboard, settings)
  - Component tree: ChatPage → ChatPanel + AgentTimeline + SourcePanel
  - SSE streaming: agent_status, content_chunk, citation, eval_scores events
  - State management: React hooks, no global state library
  - Testing strategy: Vitest (unit), React Testing Library (component), Playwright (E2E)
  
- WIREFRAMES
  - WIREFRAMES.md: 10 complete ASCII wireframes
  - Chat page (desktop 3-column, mobile single-column)
  - Source panel (slide-over with citation detail)
  - Auth screens (login, signup with controlled access notice)
  - Settings/BYOK (provider selector, key management)
  - Agent timeline detail view (expanded metrics)
  - RAGAS badge states (evaluating, passing, warning, failing)
  - Error states (connection lost, retry flow)

### Design Philosophy
- **Aesthetic:** Rare manuscript archive meets quantum research lab
- **Vibe:** Exclusive, esoteric, authoritative - not consumer tech
- **Inspiration:** CERN interfaces, ancient language decoders, alchemical laboratories

### Status
- Gate closed: 2026-05-09
- Actual hours: 6h
- Next gate: v0.2 - Frontend Shell

---

## [v0.9] - 2026-05-11 - Hybrid Retrieval + Paper Ingestion

### Added
- **Multi-Source Paper Retrieval**
  - Semantic Scholar API integration with retry logic
  - arXiv API integration for preprints
  - Local pgvector corpus search (canonical papers)
  - Hybrid merge: combines results by relevance, citations, recency
  
- **Paper Ingestion Pipeline**
  - OpenAI text-embedding-3-small integration (1536-dim vectors)
  - CLI script for bulk paper ingestion
  - 5 canonical papers seeded (attention mechanisms, transformers, BERT, GPT, ResNet)

- **LangGraph Agent Execution**
  - ReAct pattern implementation
  - Tool execution (search_s2_tool, search_arxiv_tool, search_local_tool)
  - State management (ResearchState with papers, messages, llm_calls_count)

### Status
- Gate closed: 2026-05-11
- Actual hours: ~4h
- Status: 85% complete (E2E verification pending network stability)
- Next gate: v0.10 - SSE Streaming Integration

---

## [v0.10] - 2026-05-12 - SSE Streaming Integration

### Added
- **Server-Sent Events Streaming**
  - `/api/research/stream` endpoint
  - Real-time status updates, paper discoveries, synthesis chunks
  - Event types: status, paper, synthesis, done, error
  
- **Frontend Streaming Integration**
  - `streamResearchQuery()` client function
  - Chat UI wired to backend SSE endpoint
  - Loading states and error handling
  - 60-second timeout protection
  
- **Auth Bypass for Testing**
  - Temporary bypass in frontend for development
  - To be replaced with proper auth in v0.12

### Status
- Gate closed: 2026-05-12
- Actual hours: ~2h
- Status: 100% complete
- Next gate: v0.11 - Fault-Tolerant Tool Execution

---

## [v0.11] - 2026-05-12 - Fault-Tolerant Tool Execution

### Added

- **Retry Logic**
  - Exponential backoff with tenacity decorator
  - Handles 429 rate limit errors
  - 3 retry attempts with 2-10s backoff

- **Graceful Degradation**
  - Try/catch wrappers around all tool calls
  - Tools return error messages instead of raising exceptions
  - Agent continues with available sources when one fails
  - Generates synthesis even when all tools fail

- **State Management Fix**
  - Switched from astream() to ainvoke() for complete final state
  - Fixed synthesis extraction to identify AIMessage correctly
  - Proper message type filtering (AIMessage vs SystemMessage)

### Changed

- **Tool Wrappers**
  - `search_s2_tool`: Returns formatted error on API failure
  - `search_arxiv_tool`: Returns formatted error on network failure
  - `search_local_tool`: Returns formatted error on database failure

### Fixed

- LangGraph state accumulation issue (astream partial updates)
- Synthesis extraction incorrectly returning system prompt
- Agent not executing via HTTP endpoint (deployment blocker resolved)

### Verified

- Agent makes 4 LLM calls end-to-end
- Generates proper synthesis when external APIs fail
- Returns complete state with llm_calls_count
- Fault tolerance working: all APIs failed (internet outage) → agent still provided comprehensive answer

### Status

- Gate closed: 2026-05-12
- Actual hours: ~4.5h
- Status: 100% complete
- Next gate: v0.11b - Evaluation Framework

---

## [v0.11b] - 2026-05-12 - Evaluation Framework (RAGAS + Manual Rubric)

### Added

- **RAGAS Evaluation Module**
  - Faithfulness metric (groundedness in retrieved contexts)
  - Answer relevancy metric (relevance to question)
  - Context precision metric (quality of retrieved contexts)
  - Threshold checking: faithfulness ≥0.75, answer_relevancy ≥0.70, context_precision ≥0.65
  - Async evaluation to avoid blocking main response

- **Manual Evaluation Rubric**
  - Citation accuracy heuristic (checks if citations [1], [2] present in answer)
  - Recency check (detects papers from 2022-2024)
  - Source diversity metric (balanced vs skewed across S2/arXiv/local)
  - Coverage gaps placeholder (for manual annotation)

- **Seeded Test Set**
  - 10 canonical queries for NLP/ML domains
  - Topics: transformers, attention, BERT, GPT-3, efficient attention
  - Difficulty levels: easy (3), medium (4), hard (3)
  - All answerable using seeded canonical papers

- **Evaluation Integration**
  - Background evaluation task spawned after synthesis completes
  - Results logged to Supabase eval_results table
  - Evaluation doesn't block user response (fire-and-forget)

### Files Created

- `backend/app/evaluation/ragas_evaluator.py` - RAGAS integration
- `backend/app/evaluation/manual_rubric.py` - Manual metrics computation
- `backend/app/evaluation/test_set.py` - 10 seeded test queries
- `backend/app/evaluation/eval_task.py` - Async background evaluation task
- `backend/tests/unit/test_ragas_evaluator.py` - RAGAS tests
- `backend/tests/unit/test_manual_rubric.py` - Manual rubric tests

### Files Modified

- `backend/app/api/routes/research.py` - Added evaluation trigger after synthesis

### Verified

- All evaluation modules import successfully
- Test set contains 10 queries as expected
- RAGAS evaluator can process valid inputs
- Manual rubric computes metrics correctly

### Status

- Gate closed: 2026-05-12
- Actual hours: ~3h
- Status: 100% complete
- Next gate: v0.12 - LangSmith Integration + Cost Analytics

---

## [v0.12] - 2026-05-12 - LangSmith Integration + Cost Analytics

### Added

- **LangSmith Tracing**
  - Callback handler to capture run_id and token usage
  - Metadata tags: user_id, session_id, query, tools_available
  - Tags: research_query, multi_agent
  - Trace URLs logged to research_sessions table
  - Public trace URL format: `https://smith.langchain.com/public/{run_id}/r`

- **Token Usage Tracking**
  - Input tokens, output tokens, total tokens per query
  - Captured via LangSmith callback on_llm_end events
  - Logged to research_sessions table

- **Cost Calculation**
  - Claude Sonnet 4 pricing: $3.00 per 1M input tokens, $15.00 per 1M output tokens
  - Automatic cost calculation after each query
  - Cost stored in research_sessions.cost_usd

- **Cost Analytics API**
  - `GET /api/analytics/cost/summary?days=7` - Aggregate summary (total cost, tokens, queries, averages)
  - `GET /api/analytics/cost/queries?limit=50` - Individual query costs with trace links
  - `GET /api/analytics/cost/daily?days=30` - Daily cost aggregations
  - `GET /api/analytics/cost/budget-status` - Budget threshold check

- **Rate Limiting**
  - Middleware enforces 10 queries/hour per user (configurable)
  - Database-backed tracking (stateless, works across instances)
  - Returns 429 status code when limit exceeded
  - In-memory fallback if database unavailable

- **Budget Alerts**
  - Triggers when daily spend exceeds threshold ($10 default)
  - Logs alert to console
  - Email notification placeholder (ready for integration)
  - Budget status endpoint shows percentage used and remaining budget

### Files Created

- `backend/app/middleware/langsmith_callback.py` - LangSmith callback handler
- `backend/app/api/routes/analytics.py` - Cost analytics endpoints
- `backend/app/middleware/rate_limiting.py` - Rate limiting middleware
- `backend/app/utils/budget_alerts.py` - Budget monitoring system

### Files Modified

- `backend/app/api/routes/research.py` - Added LangSmith callback, trace logging, cost tracking
- `backend/app/main.py` - Registered analytics router and rate limiting middleware

### Verified

- All v0.12 modules import successfully
- LangSmith environment variables configured correctly
- Token tracking via callback handler
- Cost calculation formula implemented
- Analytics endpoints structured and ready

### Status

- Gate closed: 2026-05-12
- Actual hours: ~2.5h
- Status: 100% complete
- Next gate: v0.13 - Docker Compose Polish

---

[v0.12]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.12
[v0.11b]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.11b
[v0.11]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.11
[v0.10]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.10
[v0.9]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.9
[v0.4]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.4
[v0.3]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.3
[v0.1]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.1
[v0.0]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.0
