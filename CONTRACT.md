# CONTRACT.md
# Project Identity and Build Contract

## Project Name
multi-agent-research-assistant

## Owner
Chris Schmidt (p.christopher.schmidt@gmail.com)

## Build Type
**Production** - Portfolio-grade build targeting v1.0 Production Live with full deployment, CI/CD, and public GitHub visibility.

## Purpose
Multi-agent AI research assistant demonstrating:
- LangGraph agent orchestration (Planner → Retriever → Critic → Synthesizer pipeline)
- RAGAS evaluation culture as first-class deliverable
- Production observability (LangSmith tracing)
- Full-stack ML engineering (streaming UI, pgvector, FastAPI)

Fills identified portfolio gap: visible multi-agent work with evals and observability.

## Target Users
1. **Primary**: Technical reviewers (hiring managers, senior engineers) evaluating portfolio
2. **Secondary**: Self (actual research tool use case)

## Complexity Tier
**Medium-High** - Multi-agent DAG, vector retrieval, streaming SSE, auth, RAGAS evals, Docker Compose orchestration

## Tech Stack (Non-Negotiable)

### Frontend
- Expo SDK 52+ with Expo Router (React Native for iOS, Android, Web)
- TypeScript (strict mode)
- NativeWind (Tailwind CSS for React Native)
- Server-Sent Events (SSE) for streaming responses
- EAS Build for native app compilation

### Backend
- FastAPI (Python 3.11+)
- LangGraph (agent orchestration DAG)
- Pydantic (state schema validation)

### AI/ML
- LLM: claude-sonnet-4-20250514 (Anthropic API)
- Embeddings: text-embedding-3-small (OpenAI)
- Evals: RAGAS (faithfulness, answer relevancy, context precision)
- Tracing: LangSmith

### Data
- Database: Supabase (PostgreSQL)
- Vector store: pgvector extension on Supabase
- Auth: Supabase Auth (email/OAuth)
- RLS: Row-level security on all tables

### Infrastructure
- Local dev: Docker Compose (backend), Expo Go (frontend)
- CI/CD: GitHub Actions
- Deployment: EAS Build (iOS/Android native apps) + Vercel (web) + Railway/Render (backend)

## Database Schema (MVP)

```sql
-- Managed by Supabase Auth
users

-- User API keys (encrypted, optional BYOK)
user_api_keys
  - id (uuid, pk)
  - user_id (uuid, fk)
  - provider (text)  -- 'anthropic', 'openai', 'openrouter', etc.
  - encrypted_key (text)  -- pgcrypto encrypted
  - is_active (boolean)
  - created_at (timestamp)
  - updated_at (timestamp)

-- Research sessions
research_sessions
  - id (uuid, pk)
  - user_id (uuid, fk)
  - query (text)
  - answer (text)
  - provider_used (text)  -- Track which provider served this query
  - papers_retrieved (int)  -- Count of papers used
  - llm_calls (int)  -- Cost tracking
  - tokens_used (int)  -- Cost tracking
  - cost_usd (float)  -- Estimated cost
  - created_at (timestamp)

-- Papers (from live search or local corpus)
papers
  - id (uuid, pk)
  - session_id (uuid, fk)
  - paper_id (text)  -- S2 corpus ID or arXiv ID
  - title (text)
  - authors (jsonb)  -- array of author names
  - abstract (text)
  - year (int)
  - venue (text)
  - citation_count (int)
  - url (text)
  - source (text)  -- 's2', 'arxiv', 'local'
  - created_at (timestamp)

-- Local canonical corpus (pgvector)
canonical_papers
  - id (uuid, pk)
  - paper_id (text)  -- S2 corpus ID or arXiv ID
  - title (text)
  - abstract (text)
  - metadata (jsonb)  -- authors, year, venue, etc.
  - embedding (vector(1536))  -- pgvector for semantic search
  - created_at (timestamp)

-- Eval logs
eval_logs
  - id (uuid, pk)
  - session_id (uuid, fk)
  - eval_type (text)  -- 'ragas_local' or 'manual_live'
  - faithfulness (float)  -- RAGAS (local corpus only)
  - answer_relevancy (float)  -- RAGAS (local corpus only)
  - context_precision (float)  -- RAGAS (local corpus only)
  - citation_accuracy (float)  -- Manual rubric (live search)
  - recency_score (float)  -- Manual rubric (live search)
  - coverage_score (float)  -- Manual rubric (live search)
  - created_at (timestamp)
```

## Agent Architecture

**LangGraph ReAct agent** (single node with tools, not multi-node pipeline):

| Component | Responsibility | Model/Tool |
|-----------|----------------|------------|
| **ReAct Agent** | Reasoning loop: decide which tools to call, when to synthesize | Claude Sonnet 4 |
| **Tools Available** | | |
| `search_semantic_scholar` | Search recent papers (2022-2024) from Semantic Scholar API | S2 API (free tier) |
| `search_arxiv` | Search preprints from arXiv API | arXiv API (free) |
| `get_paper_details` | Fetch abstract, citations, venue, authors for a paper | S2/arXiv APIs |
| `search_local_corpus` | Semantic search over canonical works (pgvector) | OpenAI embeddings + cosine similarity |
| `synthesize_findings` | Generate cited answer from collected papers | Claude Sonnet 4 (streaming) |
| **Evaluator** | Post-response: RAGAS (local corpus) + manual rubric (live search) | RAGAS library + custom metrics (async) |

**Hybrid retrieval strategy:** Combine live academic search (recent papers) with local pgvector (canonical foundational works).

## Evaluation Strategy

### RAGAS Eval Targets (for local pgvector corpus only)
- Faithfulness: ≥ 0.75
- Answer relevancy: ≥ 0.70
- Context precision: ≥ 0.65
- Seeded test set: 10 queries over canonical corpus

### Manual Eval Rubric (for live academic search)
- **Citation accuracy:** Do cited papers actually support the claims? (manual check on 10 test queries)
- **Recency:** Includes recent papers (2022-2024) when relevant? (automated: check year distribution)
- **Coverage:** Misses obvious seminal works? (manual check: expected papers present?)
- **Source diversity:** Multiple perspectives vs. echo chamber? (automated: venue/author diversity)
- Test set: 10 academic queries across ML, medicine, physics

## In Scope for v1.0
- **Live academic search:**
  - Semantic Scholar API integration (metadata + abstracts)
  - arXiv API integration (preprints)
  - Hybrid retrieval (live recent papers + local canonical corpus)
  - Abstract-based synthesis (NOT full PDF reading)
- **Multi-provider BYOK (Bring Your Own Key):**
  - Default: Owner's API keys (controlled access)
  - Optional: Users can provide their own keys via Settings
  - Supported providers: Anthropic, OpenAI, OpenRouter (extensible)
  - Encrypted key storage (pgcrypto)
  - Key hierarchy: User keys override default keys
- **Cost controls:**
  - Max 5 papers per query (hard limit)
  - Max 10 LLM calls per query (circuit breaker)
  - Rate limiting: 10 queries/hour/user on default keys
  - Budget alerts (email if daily spend > $10)
  - Cost tracking per query (tokens, LLM calls, estimated USD)

## Out of Scope for v1.0 (Deferred to v2.0)
- Full PDF reading / parsing (figures, equations, methodology sections)
- Citation graph traversal (follow references, forward citations)
- Multi-hop iterative refinement (agent re-querying based on gaps)
- Web search beyond academic databases (general Google/Bing search)
- Document upload UI (local corpus seeded via CLI script only)
- Multi-user collaboration features
- Model fine-tuning
- Public signup (controlled access only - owner approves users)

## Banned Items
- Mocking the database in integration tests (learned from prior incident per user feedback)
- Storing session tokens in non-compliant format
- Skipping git hooks (--no-verify)
- Committing secrets (.env files, API keys)

## Environment Variables Required
```bash
# LLM & Embeddings
ANTHROPIC_API_KEY        # Claude Sonnet 4 for ReAct agent
OPENAI_API_KEY           # text-embedding-3-small for local corpus embeddings

# Academic Search APIs
SEMANTIC_SCHOLAR_API_KEY # S2 API key (free tier: 100 req/5min, get from semanticscholar.org/product/api)
# arXiv API requires no auth

# Observability
LANGCHAIN_API_KEY        # LangSmith tracing
LANGCHAIN_TRACING_V2     # Enable tracing (set to "true")
LANGCHAIN_PROJECT        # Project name: "multi-agent-research-assistant"

# Database
SUPABASE_URL             # Supabase project URL
SUPABASE_ANON_KEY        # Public/anon key
SUPABASE_SERVICE_ROLE_KEY # Admin key (backend only)

# Cost Controls (optional, defaults set)
MAX_PAPERS_PER_QUERY     # Default: 5
MAX_LLM_CALLS_PER_QUERY  # Default: 10
RATE_LIMIT_QPH           # Queries per hour, default: 10
BUDGET_ALERT_THRESHOLD   # Daily spend alert (USD), default: 10
```

## Success Criteria (v1.0 Production Live)
1. **Live deployed on three platforms:**
   - iOS app in TestFlight (or App Store)
   - Android app in Play Console (internal testing or production)
   - Web app URL accessible to portfolio reviewers
2. **Working auth flow** (email signup/login with controlled access) on all platforms
3. **End-to-end academic research working:**
   - Query submitted → agent searches Semantic Scholar + arXiv + local corpus
   - Hybrid retrieval (live + local papers)
   - Synthesized answer with proper citations ([1], [2], etc.)
   - Citations link to paper source (S2, arXiv, or local)
   - Streamed response (SSE)
4. **Evaluation system:**
   - RAGAS scores visible in UI (for local corpus queries)
   - Manual eval rubric completed for 10 test queries (citation accuracy, recency, coverage)
   - Eval metrics logged to Supabase
5. **Observability:**
   - LangSmith traces accessible for all agent runs
   - Cost dashboard shows tokens used, LLM calls, cost per query, daily spend
6. **Multi-provider BYOK working:**
   - Settings page (encrypted storage, provider switching)
   - Default keys work for portfolio reviewers
   - User keys override when provided
7. **Cost controls enforced:**
   - Max 5 papers/query verified
   - Max 10 LLM calls/query circuit breaker working
   - Rate limiting (10 queries/hour) on default keys
   - Budget alert email sent when threshold hit
8. **All tests passing in CI:**
   - Unit tests (backend: pytest, frontend: Vitest)
   - Integration tests (real S2/arXiv API calls, Supabase)
   - Native E2E tests (Detox for iOS/Android, Playwright for web)
9. **Documentation:**
   - README with setup-from-clone instructions (all platforms)
   - API key acquisition guide (S2, Anthropic, OpenAI)
   - Example queries with expected results
10. **GitHub repo public** with clean commit history

---

**Contract established:** 2026-05-09  
**Revised for Academic Research Assistant:** 2026-05-10  
**Last updated:** 2026-05-12  
**Status:** v0.12 complete (LangSmith + Cost Analytics), next: v0.13 Docker Compose Polish
