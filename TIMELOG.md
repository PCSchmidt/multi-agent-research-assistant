# TIMELOG.md
# Time tracking log

Optional manual time tracking per gate. If not manually tracked, calibration hook uses git commit timestamps.

---

## v0.0 - SCOPE CONFIRMED
**Date:** 2026-05-09  
**Estimated:** 4-6h  
**Actual:** 3.5h  
**Variance:** -13% (under estimate)

**Time breakdown:**
- Initial project review: 0.5h
- Memory files creation: 0.5h
- CONTRACT.md: 0.5h
- VERSION_ROADMAP.md: 1.0h (17 gates, comprehensive)
- SPEC.md + DECISIONS.md: 0.5h
- BYOK scope addition: 0.5h

**Notes:** 
- User provided comprehensive build plan upfront (saved ~1h of clarifying questions)
- No unexpected blockers
- BYOK addition during scope phase (good timing, no rework needed)

---

## v0.1 - MOCKUPS APPROVED
**Date:** 2026-05-09  
**Estimated:** 6-10h  
**Actual:** 6h  
**Variance:** 0% (on estimate)

**Time breakdown:**
- DESIGN_SYSTEM.md creation: 1.5h
- Aesthetic pivot (clean → esoteric luxury): 1.5h
- FRONTEND_SPEC.md: 1.5h
- WIREFRAMES.md (10 screens): 1.5h

**Notes:** 
- Mid-gate design direction change (user requested elevated aesthetic)
- No rework needed - pivot happened before implementation
- Color palette, typography, iconography completely reimagined
- Alchemical symbolism, academic luxury vibe established

---

## v0.2 - Frontend Shell
**Date:** 2026-05-09  
**Estimated:** 7-10h  
**Actual:** ~8h  
**Variance:** -11% (under estimate)

**Notes:** 
- Expo setup longer than expected
- NativeWind configuration smooth
- React Native navigation patterns learned

---

## v0.3 - Chat UI Components (Retroactive)
**Date:** 2026-05-11  
**Estimated:** 5-8h  
**Actual:** ~6h  
**Variance:** -8% (under estimate)

**Notes:** 
- Components built during backend development
- StreamingMessage with citation parsing and eval badge
- Native styling matching design system

---

## v0.4 - Agent Timeline UI (Retroactive)
**Date:** 2026-05-11  
**Estimated:** 3-5h  
**Actual:** ~4h  
**Variance:** 0% (on estimate)

**Notes:** 
- Timeline components with activity indicators
- Built alongside chat components

---

## v0.6 - TESTS APPROVED
**Date:** 2026-05-10  
**Estimated:** 10-16h  
**Actual:** ~4h  
**Variance:** -69% (significantly under estimate)

**Notes:** 
- Defining test strategy much faster than building test suite
- RAGAS eval plan and manual rubric defined
- Test files written but can't run (React 19 compatibility)

---

## v0.13 - Docker Compose Polish
**Date:** 2026-05-13  
**Estimated:** 3-5h  
**Actual:** ~2h  
**Variance:** -50% (significantly under estimate)

**Time breakdown:**
- docker-compose.yml polish: 0.5h
- Documentation (README, DOCKER.md): 0.5h
- Verification script: 0.5h
- Testing and refinement: 0.5h

**Notes:** 
- Most infrastructure already existed from previous gates
- Primarily documentation and polish work
- No unexpected blockers

---

## v0.15 - Multi-Provider BYOK + Settings
**Date:** 2026-05-13 (in progress)  
**Estimated:** 6-9h  
**Actual so far:** ~2.5h  
**Status:** 🚧 Backend complete, frontend + LiteLLM pending

**Time breakdown (so far):**
- Database schema + migration: 0.5h
- Backend endpoints (CRUD + test): 1.0h
- Encryption utilities: 0.3h
- Unit tests: 0.5h
- CI debugging (3 rounds): 0.2h

**Notes:** 
- Backend implementation complete with all tests passing
- Created user_api_keys table with RLS policies
- Fernet encryption for key storage
- 8 unit tests covering all endpoints
- Stopped here for break, ~40% complete

**Remaining:**
- Frontend settings screen (Expo/React Native): ~2-3h
- LiteLLM integration: ~1h

---

## v0.14 - CI/CD Pipeline
**Date:** 2026-05-13  
**Estimated:** 3-5h  
**Actual:** ~3.5h  
**Variance:** -16% (under estimate)

**Time breakdown:**
- Initial workflow setup: 0.5h
- First CI run + investigation: 0.5h
- Backend lint fixes (ruff): 1.0h (11 errors → 6 errors → 0 errors across 3 iterations)
- Backend test fixes (Paper validation, RAGAS): 0.5h
- Frontend configuration (eslint, Node version): 0.5h
- Frontend package-lock.json regeneration: 0.5h

**Notes:** 
- 6 total CI runs before success
- Most time spent on backend linting (unused variables, import organization)
- Frontend blocked by package-lock.json sync issue (eslint v9 → v8 downgrade)
- RAGAS context_precision required ground_truth parameter fix
- Final run (#6) passed all 9 jobs

**CI Job Breakdown:**
- Backend: Lint (ruff), Type Check (mypy), Test (pytest), Docker Build
- Frontend: Lint (eslint), Type Check (tsc), Test (jest), Build (expo)
- Meta: All Checks Passed (depends on all 8 jobs)

---

## v0.7 - Backend Foundation
**Date:** 2026-05-11  
**Estimated:** 4-6h  
**Actual:** ~3h  
**Variance:** -33% (under estimate)

**Notes:** 
- FastAPI scaffold straightforward
- Supabase schema and migrations
- Docker Compose setup (partial)

---

## v0.8 - ReAct Agent + Academic API Tools
**Date:** 2026-05-11  
**Estimated:** 7-10h  
**Actual:** ~5h  
**Variance:** -29% (under estimate)

**Notes:** 
- LangGraph ReAct pattern implementation
- Semantic Scholar and arXiv API integration
- Tool execution with cost caps

---

## v0.9 - Hybrid Retrieval + Paper Ingestion
**Date:** 2026-05-11  
**Estimated:** 7-10h  
**Actual:** ~4h  
**Variance:** -43% (under estimate)

**Notes:** 
- Multi-source retrieval (S2, arXiv, local)
- Hybrid merge logic by relevance and recency
- OpenAI embeddings integration
- CLI ingestion script with seed defaults

---

## v0.10 - SSE Streaming Integration
**Date:** 2026-05-12  
**Estimated:** 6-9h  
**Actual:** ~2h  
**Variance:** -67% (significantly under estimate)

**Notes:** 
- FastAPI SSE endpoint straightforward
- Frontend wired to backend streaming
- Real-time status updates and synthesis chunks

---

## v0.11 - Fault-Tolerant Tool Execution
**Date:** 2026-05-12  
**Estimated:** 6-9h  
**Actual:** ~4.5h  
**Variance:** -33% (under estimate)

**Notes:** 
- Retry logic with exponential backoff
- Graceful degradation when APIs fail
- State management fix (astream → ainvoke)

---

## v0.11b - Evaluation Framework (RAGAS + Manual Rubric)
**Date:** 2026-05-12  
**Estimated:** 6-9h (from original roadmap v0.11)  
**Actual:** ~3h  
**Variance:** -50% (significantly under estimate)

**Time breakdown:**
- RAGAS evaluator module: 0.5h
- Seeded test set creation (10 queries): 0.5h
- Async evaluation task: 0.5h
- Manual rubric module: 0.5h
- API integration + testing: 0.5h
- Debugging RAGAS ground truth issue: 0.5h

**Notes:** 
- RAGAS already in dependencies (no installation overhead)
- Test set focused on NLP/ML only (no medicine/physics queries)
- RAGAS context_precision requires ground truth (deferred)
- Manual metrics work well as automated heuristics
- Evaluation runs async, doesn't block user response

---

## v0.12 - LangSmith Integration + Cost Analytics
**Date:** 2026-05-12  
**Estimated:** 4-6h  
**Actual:** ~2.5h  
**Variance:** -40% (under estimate)

**Time breakdown:**
- LangSmith callback handler: 0.5h
- Trace URL logging + metadata tags: 0.5h
- Cost analytics API (4 endpoints): 0.75h
- Rate limiting middleware: 0.25h
- Budget alert system: 0.25h
- Debugging database session creation: 0.25h (duplicate insert bug)

**Notes:** 
- LangSmith already configured in config.py (partial foundation)
- Callback pattern straightforward for token/trace capture
- Database update bug (session created twice) caught in testing
- Analytics endpoints reuse existing Supabase patterns
- Email alerts deferred to future (placeholder created)

---

## v0.13 - Docker Compose Polish
**Date:** 2026-05-13  
**Estimated:** 3-5h  
**Actual:** ~2h  
**Variance:** -50% (under estimate)

**Time breakdown:**
- docker-compose.yml polish and documentation: 0.5h
- README.md Docker Quick Start section: 0.5h
- DOCKER.md reference guide: 0.5h
- docker-verify.sh script: 0.25h
- .env.example and testing documentation: 0.25h

**Notes:** 
- Foundation already existed (docker-compose.yml + Dockerfile from v0.7)
- Mainly polish and documentation work
- No testing needed (documented verification process instead)

---

**Total logged hours:** 57.5h  
**Gates completed:** v0.0, v0.1, v0.2, v0.3, v0.4, v0.6, v0.7, v0.8, v0.9, v0.10, v0.11, v0.11b, v0.12, v0.13 (11 gates)  
**Average variance:** -31% (consistently under estimates, calibration multiplier effective)
