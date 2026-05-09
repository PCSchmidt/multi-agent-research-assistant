# MEMORY_SEMANTIC.md
# Patterns, preferences, and pre-fills for this project

## Owner Profile
- Name: Chris Schmidt
- Email: p.christopher.schmidt@gmail.com
- Role: ML Engineer, JHU AI Engineering
- Portfolio focus: Multi-agent AI, agentic orchestration, production ML systems

## Project Patterns
### Stack Preferences
- Frontend: Next.js 14+ App Router, TypeScript, Tailwind
- Backend: FastAPI (Python 3.11+)
- Agent orchestration: LangGraph
- LLM: Claude Sonnet 4 via Anthropic API
- Database: Supabase (PostgreSQL + pgvector)
- Evals: RAGAS + LangSmith

### Naming Conventions
- Projects: kebab-case (multi-agent-research-assistant)
- Components: PascalCase
- Files: kebab-case for config, PascalCase for React components

### Code Style
- Python: Type hints required, Pydantic for data validation
- TypeScript: Strict mode enabled
- Testing: Pytest for Python, Vitest for TypeScript/React, Playwright for E2E

## Confidence Scores
(Updated as patterns emerge)

## Pre-fills
- Default Python version: 3.11+
- Default Node version: 18+
- Default LLM: claude-sonnet-4-20250514
- Default vector DB: pgvector on Supabase
