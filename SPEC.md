# SPEC.md
# Current Gate Specification

## Current Version: v0.2
**Gate:** Frontend Shell (Expo - React Native + Web)  
**Status:** Pending GO approval  
**Estimate:** 7-10h (updated for Expo multi-platform setup)

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
Build Expo (React Native) scaffolding with Supabase auth, navigation, and protected routes targeting iOS, Android, and Web (no backend wire-up yet).

## Deliverables
- [ ] Expo SDK 52+ project initialized with TypeScript
- [ ] Expo Router configured (file-based routing for iOS, Android, Web)
- [ ] NativeWind installed and configured with design system tokens
- [ ] Supabase React Native SDK integrated
- [ ] Auth screens (LoginScreen, SignupScreen, PasswordResetScreen) using React Native components
- [ ] Navigation structure (tab navigator or stack navigator)
- [ ] Protected route middleware (Expo Router auth guards)
- [ ] DashboardLayout with navigation bar
- [ ] Empty ChatScreen with layout structure (React Native layout)
- [ ] Settings screen skeleton (for BYOK later)
- [ ] Responsive behavior tested (mobile portrait/landscape, tablet, web)
- [ ] Verified running on iOS Simulator, Android Emulator, and web browser
- [ ] Basic routing verified (auth screens, dashboard, settings)

## Approval Criteria
- All screens accessible on iOS, Android, and Web
- Auth flow works (signup → login → protected dashboard) on all platforms
- Design system colors/fonts applied via NativeWind
- No console errors or warnings across platforms
- Touch interactions work correctly on mobile

## Active Tasks
Waiting for user to type `GO` to begin Expo frontend implementation.

## Next Gate
**v0.3 - Chat UI Components**  
Will build: ChatPanel, MessageList, StreamingText, CitationRenderer with mock data (React Native components)

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
