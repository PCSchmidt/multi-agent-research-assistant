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
- Next.js 14+ (App Router)
- TypeScript (strict mode)
- Tailwind CSS
- Server-Sent Events (SSE) for streaming responses

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
- Local dev: Docker Compose
- CI/CD: GitHub Actions
- Deployment: TBD at deployment gate (likely Vercel frontend + Railway/Render backend)

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
  - created_at (timestamp)

-- Document chunks with embeddings
sources
  - id (uuid, pk)
  - session_id (uuid, fk)
  - content (text)
  - metadata (jsonb)
  - embedding (vector(1536))  -- pgvector

-- Eval logs
eval_logs
  - id (uuid, pk)
  - session_id (uuid, fk)
  - faithfulness (float)
  - answer_relevancy (float)
  - context_precision (float)
  - created_at (timestamp)
```

## Agent Architecture

LangGraph StateGraph with five nodes:

| Node | Responsibility | Model/Tool |
|------|----------------|------------|
| Planner | Decompose query into sub-questions, set retrieval strategy | Claude Sonnet (structured output) |
| Retriever | Semantic search via pgvector, re-rank chunks | OpenAI embeddings + cosine similarity |
| Critic | Score chunks for relevance, filter noise | Claude Sonnet (classification) |
| Synthesizer | Generate cited answer, stream to client | Claude Sonnet (streaming) |
| Evaluator | Run RAGAS post-response, log to LangSmith/Supabase | RAGAS library (async) |

## RAGAS Eval Targets (TESTS APPROVED gate thresholds)
- Faithfulness: ≥ 0.75
- Answer relevancy: ≥ 0.70
- Context precision: ≥ 0.65
- All evals must be reproducible (seeded test set)

## In Scope for v1.0
- **Multi-provider BYOK (Bring Your Own Key):**
  - Default: Owner's API keys (controlled access)
  - Optional: Users can provide their own keys via Settings
  - Supported providers: Anthropic, OpenAI, OpenRouter (extensible)
  - Encrypted key storage (pgcrypto)
  - Key hierarchy: User keys override default keys

## Out of Scope for v1.0
- Web search / live internet retrieval
- Multi-user collaboration features
- Document upload UI (seed via CLI script only)
- Model fine-tuning
- Mobile app
- Public signup (controlled access only - owner approves users)

## Banned Items
- Mocking the database in integration tests (learned from prior incident per user feedback)
- Storing session tokens in non-compliant format
- Skipping git hooks (--no-verify)
- Committing secrets (.env files, API keys)

## Environment Variables Required
```bash
ANTHROPIC_API_KEY        # Claude API for agents
OPENAI_API_KEY           # Embeddings
LANGCHAIN_API_KEY        # LangSmith tracing
LANGCHAIN_TRACING_V2     # Enable tracing
LANGCHAIN_PROJECT        # Project name in LangSmith
SUPABASE_URL             # Supabase project URL
SUPABASE_ANON_KEY        # Public/anon key
SUPABASE_SERVICE_ROLE_KEY # Admin key (backend only)
```

## Success Criteria (v1.0 Production Live)
1. Live deployed URL accessible to portfolio reviewers
2. Working auth flow (email signup/login with controlled access)
3. End-to-end query → streamed cited answer working
4. RAGAS eval scores visible in UI
5. LangSmith traces accessible for all agent runs
6. **Multi-provider BYOK working** (Settings page, encrypted storage, provider switching)
7. All tests passing in CI
8. README with setup-from-clone instructions
9. GitHub repo public with clean commit history

---

**Contract established:** 2026-05-09  
**Status:** Awaiting SCOPE CONFIRMED approval
