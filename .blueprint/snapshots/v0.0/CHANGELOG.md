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

[v0.0]: https://github.com/PCSchmidt/multi-agent-research-assistant/releases/tag/blueprint-gate-v0.0
