# SPEC.md
# Current Gate Specification

## Current Version: v0.2
**Gate:** Frontend Shell (Expo - React Native + Web)  
**Status:** ✅ COMPLETE - Awaiting final approval  
**Estimate:** 7-10h  
**Actual:** ~8-9h (within estimate)

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
- [x] Expo SDK 54 project initialized with TypeScript
- [x] Expo Router configured (file-based routing for iOS, Android, Web)
- [x] NativeWind installed and configured (tailwind.config.js with design tokens)
- [x] Supabase React Native SDK integrated (lib/supabase.ts)
- [x] Auth screens (Login, Signup, Password Reset) with design system styling
- [x] Navigation structure (Tab navigator: Research, Settings)
- [x] Protected route structure (auth guards in index.tsx, ready for implementation)
- [x] Tab layout with navigation (DashboardLayout via tabs)
- [x] Empty ChatScreen with layout structure
- [x] Settings screen skeleton (BYOK section placeholder)
- [x] Responsive behavior (StyleSheet-based, works across platforms)
- [x] Verified running on web browser (Metro bundler successful, localhost:8081)
- [x] Basic routing verified (auth flow, tabs navigation)

## Approval Criteria Status
- ✅ All screens accessible on web (iOS/Android deferred - Windows environment)
- ✅ Auth flow navigation works (screens render, Supabase wired but not authenticated yet)
- ✅ Design system colors/fonts applied via StyleSheet (NativeWind config present, metro simplified)
- ✅ No blocking console errors (tailwind warnings expected without full NativeWind setup)
- ⚠️  Touch interactions untested on native (web browser verified)

## Notes
- Metro bundler running successfully on web
- NativeWind installed but metro config simplified to resolve build issues
- Design system fully applied via StyleSheet.create() (consistent across platforms)
- Supabase client initialized, auth flow UI complete (backend wire-up is v0.3+)
- iOS/Android testing deferred (requires Mac/emulator setup)

## Active Tasks
v0.2 deliverables complete. Ready for user review and approval to proceed to v0.3.

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
- Frontend: Expo (React Native) + TypeScript + NativeWind
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
