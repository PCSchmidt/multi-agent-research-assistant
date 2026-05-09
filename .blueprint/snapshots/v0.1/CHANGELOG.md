# CHANGELOG.md
# Project change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[v0.1]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.1
[v0.0]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.0
