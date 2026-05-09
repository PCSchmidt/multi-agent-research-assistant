# SPEC.md
# Current Gate Specification

## Current Version: v0.1
**Gate:** MOCKUPS APPROVED  
**Status:** Pending GO approval  
**Estimate:** 6-10h

---

## Previous Gate: v0.0 - SCOPE CONFIRMED
**Status:** ✅ CLOSED  
**Completed:** 2026-05-09  
**Actual hours:** 3.5h (estimated 4-6h, -13% variance)

## Goal
Produce visual design system and wireframes for all screens (chat panel, agent timeline, source panel, auth screens).

## Deliverables
- [ ] DESIGN_SYSTEM.md - Colors, typography, spacing, component patterns
- [ ] FRONTEND_SPEC.md - Component hierarchy, props, state management patterns
- [ ] Wireframes - Chat panel with streaming message display
- [ ] Wireframes - Agent timeline with status indicators
- [ ] Wireframes - Source panel (citation detail view)
- [ ] Wireframes - Auth screens (login, signup, password reset)
- [ ] Empty state designs
- [ ] Citation renderer mockup (numbered superscripts)
- [ ] User review and approval

## Approval Criteria
User types: `MOCKUPS APPROVED`

## Active Tasks
Waiting for user to type `GO` to begin mockups work.

## Next Gate
**v0.2 - Frontend Shell**  
Will build: Next.js scaffolding, auth UI, layout, protected routes

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
