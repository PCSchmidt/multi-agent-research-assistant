# DECISIONS.md
# Architectural Decision Log

## Format
Each entry: decision made, why it was made, what alternatives were considered, consequences.

---

## Decision 1: LangGraph over raw function calls
**Date:** 2026-05-09  
**Context:** Need to orchestrate multi-agent pipeline (Planner → Retriever → Critic → Synthesizer)

**Decision:** Use LangGraph's `StateGraph` for agent orchestration instead of raw Python function calls or custom DAG executor.

**Why:**
- Makes agent DAG inspectable and debuggable (can add breakpoints, replay nodes)
- Native LangSmith integration for zero-config tracing
- State schema validation via Pydantic
- Portfolio signal: demonstrates professional ML tooling, not ad-hoc scripts
- Addresses "black-box API calls" gap - graph definition is explicit and readable

**Alternatives considered:**
- Raw function pipeline: Simpler but loses inspectability and tracing
- Custom DAG with Celery/Airflow: Overkill for in-memory agent flow
- LlamaIndex agents: Less control over DAG structure than LangGraph

**Consequences:**
- +30min learning curve for LangGraph API
- Enables easy node-level testing and debugging
- LangSmith traces automatically include graph structure

---

## Decision 2: pgvector on Supabase over standalone vector DB
**Date:** 2026-05-09  
**Context:** Need vector store for semantic search over document chunks

**Decision:** Use pgvector extension on Supabase PostgreSQL instead of standalone vector DB (Pinecone, Weaviate, Chroma).

**Why:**
- Reduces operational surface area (one DB instead of two)
- Supabase already required for auth and relational data
- pgvector cosine similarity is sufficient for portfolio-scale corpus (hundreds to low thousands of chunks)
- Simplifies Docker Compose setup (no additional service)
- Cost: Free tier covers use case (Pinecone free tier has tighter limits)

**Alternatives considered:**
- Pinecone: Better at massive scale (millions of vectors) but overkill here
- Chroma: Good for local dev but requires deployment strategy
- Weaviate: Feature-rich but adds deployment complexity

**Consequences:**
- Supabase free tier limit: 500MB database (acceptable for corpus size)
- Query performance may degrade beyond ~10k chunks (not a concern for v1.0)
- Easier rollback/snapshot strategy (single DB dump)

---

## Decision 3: Claude Sonnet 4 for all agent nodes
**Date:** 2026-05-09  
**Context:** Each agent node needs an LLM (Planner, Critic, Synthesizer)

**Decision:** Use `claude-sonnet-4-20250514` for all nodes instead of mixing models (e.g., Haiku for Critic, Opus for Synthesizer).

**Why:**
- Simplifies token budgeting and cost forecasting
- Sonnet 4 is fast enough that latency difference vs. Haiku is negligible for this use case
- Quality consistency across all nodes
- Avoids model-switching bugs (different APIs, different prompt formats)
- Per user feedback: portfolio focus is architecture/evals, not cost optimization

**Alternatives considered:**
- Haiku for Critic (cheaper, faster): Saves ~$0.002 per query but risks lower quality filtering
- Opus for Synthesizer (higher quality): Minimal quality gain for 3x cost increase
- GPT-4o for comparison: Mixing providers complicates debugging

**Consequences:**
- Cost per query: ~$0.015-0.025 (acceptable for portfolio demo)
- Can swap models per-node later if needed (LangGraph makes this trivial)
- Consistent prompt engineering across all nodes

---

## Decision 4: Async Evaluator node (not in hot path)
**Date:** 2026-05-09  
**Context:** RAGAS evals take 2-5 seconds to run, would block response streaming

**Decision:** Run Evaluator node asynchronously after response is delivered to user, not as a blocking step in the LangGraph DAG.

**Why:**
- User latency: Query → answer should be <10s; adding 2-5s eval time breaks this
- Eval scores are diagnostic, not required for the answer itself
- Async pattern common in production systems (e.g., analytics, logging)

**Alternatives considered:**
- Blocking eval: Simple but kills UX with 15s+ response times
- No eval in runtime: Only run on test set (loses real-time feedback signal)
- Client-side eval trigger: Adds complexity, doesn't match usage pattern

**Consequences:**
- Eval badge in UI shows "Evaluating..." state briefly after answer streams
- Need task queue or background worker (can use FastAPI BackgroundTasks for MVP)
- Eval failures don't block user flow (logged but not surfaced as errors)

---

## Decision 5: Email auth only for v1.0 (no OAuth)
**Date:** 2026-05-09  
**Context:** Supabase Auth supports email, Google, GitHub, etc.

**Decision:** Launch v1.0 with email/password auth only. OAuth providers (Google, GitHub) deferred to post-v1.0.

**Why:**
- Reduces surface area for deployment gate (no OAuth app registration, callback URLs, etc.)
- Email auth sufficient to demonstrate auth flow for portfolio
- Can add OAuth providers in 1-2h after v1.0 if needed
- Per build plan: target users are technical reviewers, not general public (email signup acceptable)

**Alternatives considered:**
- Google OAuth only: Fewer steps for user but requires Google Cloud project setup
- Both email + OAuth: Ideal UX but adds deployment config complexity

**Consequences:**
- Slightly higher friction for demo users (signup form vs. "Sign in with Google")
- Can add OAuth post-launch with zero schema changes (Supabase handles it)

---

## Decision 6: Seeded test set for RAGAS, not production queries
**Date:** 2026-05-09  
**Context:** RAGAS evals need ground truth (query, expected answer, source chunks)

**Decision:** Create a seeded test set of 10 hand-crafted query-answer pairs for reproducible RAGAS evaluation. Do not run RAGAS on arbitrary production queries.

**Why:**
- Reproducibility: TESTS APPROVED gate requires consistent eval scores
- Ground truth: RAGAS metrics (faithfulness, answer relevancy) need reference answers
- Portfolio signal: Shows evals discipline, not just "we ran a metric once"
- Production queries lack ground truth (defeats the purpose of RAGAS)

**Alternatives considered:**
- Eval all production queries: No ground truth → metrics are meaningless
- Generate synthetic test set with LLM: Risky (model evaluating itself)
- Use existing Q&A dataset (SQuAD, NaturalQuestions): Domain mismatch

**Consequences:**
- Upfront cost: 2-3h to create test set at TESTS APPROVED gate
- Test set becomes a static asset (versioned in repo)
- RAGAS badge in UI shows scores from async evals (still useful signal, not test set scores)

---

## Decision 7: Multi-Provider BYOK with LiteLLM
**Date:** 2026-05-09  
**Context:** Need to support user-provided API keys to avoid owner financing token usage, while maintaining controlled demo access for portfolio reviewers

**Decision:** Implement optional BYOK with multi-provider support (Anthropic, OpenAI, OpenRouter) using LiteLLM for provider abstraction. Owner's keys serve as default; user keys override when present.

**Why:**
- **Cost control:** Owner doesn't finance arbitrary user queries
- **Flexibility:** Users can choose their preferred provider (Anthropic vs OpenAI vs OpenRouter)
- **Demo-friendly:** Portfolio reviewers can use app immediately (owner's keys), upgrade to BYOK if needed
- **LiteLLM:** Unified interface across 100+ providers, minimal code changes per provider
- **Security:** pgcrypto encryption at rest, RLS policies per user

**Alternatives considered:**
- BYOK required (no default keys): Blocks portfolio reviewers from instant demo
- Owner keys only, no BYOK: Owner finances all usage (unsustainable)
- Single provider BYOK: Less flexible, locks users into one provider
- Direct provider SDKs instead of LiteLLM: Requires N integration patterns instead of one

**Consequences:**
- +6-9h implementation (Settings UI, encryption, LiteLLM integration)
- Controlled access required (email allowlist or approval flow) to protect default keys
- Must migrate from direct Anthropic/OpenAI SDK calls to LiteLLM wrapper
- Key hierarchy logic in backend (check user keys → fallback to default)
- `research_sessions` table tracks `provider_used` for analytics

**Implementation notes:**
- Supabase `user_api_keys` table with pgcrypto encryption
- Settings page: provider dropdown + key input + test connection
- Backend: `/api/keys` CRUD with RLS enforcement
- LiteLLM config: dynamic provider selection based on user key presence
- Fallback chain: user Anthropic key → default Anthropic key → user OpenAI key → default OpenAI key

---

## Decision 8: Expo (React Native + Web) over Next.js

**Date:** 2026-05-09  
**Context:** Frontend stack selection at v0.2 gate (before any code written). User requirement: app must work on mobile phones and eventually ship to Apple App Store and Google Play Store.

**Decision:** Use Expo Router (React Native for Web + iOS + Android) instead of Next.js. One codebase compiles to three platforms.

**Why:**

- **Portfolio differentiation:** "Shipped to iOS, Android, and web from one codebase" signals broader platform expertise
- **Mobile-first requirement:** App must work on phones (not just responsive web), with eventual native app store presence
- **Timing is perfect:** v0.2 is the first frontend gate - no code exists yet, so pivot cost is minimal
- **Expo maturity:** Expo Router now matches Next.js App Router feature parity (file-based routing, layouts, server actions via API routes)
- **NativeWind:** Tailwind CSS for React Native maintains design system compatibility
- **Supabase support:** Supabase React Native SDK is production-ready

**Alternatives considered:**

- **Next.js + PWA:** Works on mobile browsers, installable, but no true native APIs (limited camera, biometrics, push notifications). No app store presence.
- **Next.js web + separate React Native app:** Two codebases (2x maintenance, divergence risk). Estimate: +30-50h duplicate work.
- **Flutter:** Different language (Dart), steeper learning curve, less relevant to portfolio (JavaScript/TypeScript focus).

**Consequences:**

- **Estimate adjustments:**
  - v0.2 (Frontend Shell): 5-8h → 7-10h (+Expo setup, navigation, Supabase RN SDK)
  - v0.3 (Chat UI): 4-7h → 5-8h (React Native components, NativeWind patterns)
  - v0.5 (Frontend Approved): 4-6h → 5-8h (Detox for native E2E testing)
  - v1.0 (Production Live): 8-16h → 12-20h (+EAS Build, TestFlight, Play Console, app store metadata)
  - **Total increase:** +10-15h across all frontend gates
- **Tech stack changes:**
  - Frontend framework: Next.js 14 → Expo SDK 52+ with Expo Router
  - Styling: Tailwind CSS → NativeWind (Tailwind for React Native)
  - Navigation: Next.js App Router → Expo Router (file-based routing, same pattern)
  - Auth: Supabase JS → Supabase React Native SDK
  - Testing: Playwright → Detox (native E2E), Vitest still for component tests
  - Deployment: Vercel → EAS Build (Expo Application Services) for native builds, Vercel for web build
- **Development environment:**
  - Requires iOS Simulator (Xcode on Mac) or Android Emulator for testing
  - Web testing still works in browser (React Native for Web)
  - EAS Build handles cloud builds (no local Xcode/Android Studio required for production)
- **Portfolio signal upgraded:** Demonstrates cross-platform mobile expertise, not just web development

**Migration path (for reference):**

- Design system already uses Tailwind → NativeWind maps 1:1 for most utilities
- Component patterns (cards, buttons, inputs) translate cleanly to React Native primitives
- FastAPI backend unchanged (still uses REST/SSE endpoints)
- LangGraph agent architecture unchanged

---

## Decision 9: Academic Research Assistant scope (Abstract-based, not full PDF reading)

**Date:** 2026-05-10  
**Context:** User requested pivot from "local vector retrieval Q&A" to "PhD/postdoc-level academic research" capability. Original scope: simple Planner → Retriever → Critic → Synthesizer pipeline over pre-seeded local corpus. New requirement: must search live academic databases, fetch papers, do multi-hop reasoning.

**Critical-thinker pressure-test invoked:** Flagged serious cost scaling issues ($500-$2000/month at moderate usage), complexity creep (citation graphs, full PDF parsing), wrong eval framework (RAGAS doesn't fit live research), and 200-300h estimate risk.

**Decision:** Build "Academic Research Assistant" (not "PhD-level researcher") with these constraints:
- **Search live academic databases:** Semantic Scholar API + arXiv API (metadata + abstracts)
- **Hybrid retrieval:** Live search (recent papers 2022-2024) + local pgvector (canonical foundational works)
- **Abstract-only reading:** Read abstracts + metadata, NOT full PDF parsing (defer to v2.0)
- **ReAct-style agent:** Single LangGraph node with tools, not multi-node pipeline
- **Hard cost caps:** Max 5 papers/query, max 10 LLM calls/query, rate limits on default keys
- **Manual eval rubric:** Citation accuracy, recency, coverage (instead of pure RAGAS)
- **Estimate target:** 130-180h (with 2.0x calibration)

**Why:**
- **Cost control:** Abstract reading costs $0.10-0.30/query vs. $0.50-$2.00 for full PDF reading (10x reduction)
- **No paywall problem:** All APIs provide abstracts free; 50-70% of papers are paywalled for full text
- **Faster implementation:** Avoid PDF parsing rabbit hole (formatting, figures, equations, scanned images)
- **Portfolio signal maintained:** Still demonstrates API integration, hybrid retrieval, multi-source synthesis, academic domain expertise
- **Realistic scope:** "Academic research assistant" is achievable for v1.0; "PhD-level researcher" is a multi-year product

**Alternatives considered:**
1. **Full PhD-level research (original request):** Full PDF reading, citation graph traversal, multi-hop iterative refinement
   - Rejected: 200-300h estimate, uncontrolled costs, paywall failures, complexity creep
2. **Keep original local-only scope:** Simple pgvector retrieval over pre-seeded corpus
   - Rejected: Doesn't meet user's need for live academic research capability
3. **Abstract + introduction/conclusion sections:** Middle ground between abstract-only and full PDF
   - Deferred to v2.0: Adds paywall complexity, still requires PDF parsing

**Consequences:**
- ✅ Cost per query controlled: $0.10-0.30 (sustainable on default keys with rate limits)
- ✅ No paywall failures: All abstracts are freely available
- ✅ Faster backend implementation: Skip PDF parsing complexity
- ✅ Estimate remains reasonable: 130-180h vs. original 94-159h (minor increase)
- ⚠️ Reduced depth: Can't analyze methodology/results sections in detail (only abstract-level synthesis)
- ⚠️ Manual eval required: RAGAS only works for local pgvector corpus, not live search
- 🔄 Deferred to v2.0: Full PDF reading (open-access only), citation graph traversal, multi-hop refinement

**Implementation notes:**
- **Tools for ReAct agent:**
  - `search_semantic_scholar(query, year_range, limit)` - recent papers
  - `search_arxiv(query, category, limit)` - preprints
  - `get_paper_details(paper_id)` - fetch abstract, citations, venue
  - `search_local_corpus(query)` - pgvector for canonical works
  - `synthesize_findings()` - generate cited answer
- **Cost caps enforced in FastAPI middleware:**
  - 5 papers max per query (hard limit)
  - 10 LLM calls max per query (circuit breaker)
  - 10 queries/hour/user on default keys (rate limit)
  - Budget alert if daily spend > $10
- **Eval strategy:**
  - RAGAS (faithfulness, answer relevancy, context precision) on local pgvector corpus
  - Manual rubric for live search: citation accuracy, recency, coverage, source diversity
  - Test set: 10 academic queries across domains (ML, medicine, physics)

**Roadmap impact:**
- v0.7-v0.12 gates redesigned for academic research architecture
- TESTS APPROVED (v0.6) criteria updated for manual eval rubric
- Possibly frontend adjustments for paper list UI, abstract display (minor)

---

**Last updated:** 2026-05-10
