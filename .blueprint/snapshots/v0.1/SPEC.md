# SPEC.md
# Current Gate Specification

## Current Version: v0.2
**Gate:** Frontend Shell  
**Status:** Pending GO approval  
**Estimate:** 5-8h

---

## Previous Gate: v0.1 - MOCKUPS APPROVED
**Status:** ✅ CLOSED  
**Completed:** 2026-05-09  
**Actual hours:** 6h (estimated 6-10h, 0% variance)

## Previous Gate: v0.0 - SCOPE CONFIRMED
**Status:** ✅ CLOSED  
**Completed:** 2026-05-09  
**Actual hours:** 3.5h (estimated 4-6h, -13% variance)

## Goal
Build Next.js scaffolding with Supabase auth, layout, and protected routes (no backend wire-up yet).

## Deliverables
- [ ] Next.js 14 project initialized (App Router, TypeScript, Tailwind)
- [ ] Supabase client SDK configured
- [ ] Auth components (LoginPage, SignupPage, PasswordResetPage)
- [ ] DashboardLayout with NavBar, protected route middleware
- [ ] Design system tokens in Tailwind config (colors, fonts, spacing)
- [ ] Empty ChatPage with layout structure (3-column grid)
- [ ] Settings page skeleton (for BYOK later)
- [ ] Responsive breakpoints configured
- [ ] Basic routing verified (/login, /signup, /dashboard, /settings)

## Approval Criteria
- All routes accessible
- Auth flow works (signup → login → protected dashboard)
- Design system colors/fonts applied
- No console errors

## Active Tasks
Waiting for user to type `GO` to begin frontend implementation.

## Next Gate
**v0.3 - Chat UI Components**  
Will build: ChatPanel, MessageList, StreamingText, CitationRenderer with mock data

---

## Project Summary (for quick reference)

### What We're Building
Multi-agent AI research assistant with LangGraph orchestration:
- User submits research question
- LangGraph DAG decomposes → retrieves → critiques → synthesizes
- Streamed cited answer with agent status timeline
- RAGAS evals + LangSmith tracing visible

### Why This Matters
Portfolio project filling identified gaps:
- No visible multi-agent work
- LLM usage limited to black-box API calls
- No evals culture demonstrated

### Tech Stack (Locked)
- Frontend: Next.js 14 + TypeScript + Tailwind
- Backend: FastAPI + LangGraph
- LLM: Claude Sonnet 4
- Embeddings: OpenAI text-embedding-3-small
- Database: Supabase (PostgreSQL + pgvector)
- Evals: RAGAS
- Tracing: LangSmith

### Target Outcome (v1.0)
Live deployed URL, working auth, end-to-end query flow, RAGAS scores visible, LangSmith traces accessible, all tests passing, public GitHub repo.

---

**Last updated:** 2026-05-09
