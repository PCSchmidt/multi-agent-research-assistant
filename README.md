# Multi-Agent Research Assistant

> Academic research assistant powered by LangGraph, Claude Sonnet 4, and hybrid retrieval

[![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-blue)](https://smith.langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)](https://fastapi.tiangolo.com)
[![Expo](https://img.shields.io/badge/Expo-React%20Native-black)](https://expo.dev)

## Overview

An AI-powered research assistant that combines live academic search (Semantic Scholar, arXiv) with a local canonical corpus to provide cited, synthesized answers to research questions. Built with LangGraph multi-agent orchestration, evaluated with RAGAS metrics, and traced with LangSmith.

**Current Status:** v0.12 - LangSmith Integration + Cost Analytics Complete ✅

## Features

### ✅ Implemented (v0.0 → v0.12)

- **Multi-Agent ReAct Pattern** - LangGraph orchestration with tool-calling agent
- **Hybrid Retrieval** - Combines Semantic Scholar, arXiv, and local pgvector corpus
- **Cited Synthesis** - Claude Sonnet 4 generates answers with `[1], [2]` inline citations
- **SSE Streaming** - Real-time response streaming to frontend
- **Fault Tolerance** - Graceful degradation when external APIs fail
- **RAGAS Evaluation** - Automated quality metrics (faithfulness, answer relevancy, context precision)
- **Manual Rubric** - Citation accuracy, recency, source diversity metrics
- **LangSmith Tracing** - Full observability with trace URLs logged to database
- **Cost Tracking** - Token usage and cost calculated per query ($3/1M input, $15/1M output)
- **Rate Limiting** - 10 queries/hour per user (configurable)
- **Budget Alerts** - Triggers at $10/day threshold

### 🚧 In Progress

- Docker Compose setup (v0.13)
- CI/CD pipeline (v0.14)
- Multi-provider BYOK (v0.15)

## Tech Stack

### Backend
- **Framework:** FastAPI + Uvicorn
- **Agent:** LangGraph (ReAct pattern)
- **LLM:** Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- **Embeddings:** OpenAI `text-embedding-3-small` (1536-dim)
- **Database:** Supabase (PostgreSQL + pgvector)
- **Evals:** RAGAS
- **Tracing:** LangSmith

### Frontend
- **Framework:** Expo (React Native + Web)
- **Language:** TypeScript
- **Styling:** NativeWind (Tailwind for React Native)
- **State:** React hooks (no global state library)

### Academic APIs
- **Semantic Scholar API** - Citation data, recent papers
- **arXiv API** - Preprints and latest research
- **Local Corpus** - pgvector similarity search over canonical papers

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account
- API keys:
  - Anthropic (Claude)
  - OpenAI (embeddings)
  - LangSmith

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run migrations (Supabase)
# Apply backend/app/db/migrations/001_initial_schema.sql to your Supabase project

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── agent/              # LangGraph agent (ReAct pattern)
│   │   ├── api/routes/         # FastAPI endpoints
│   │   ├── db/                 # Supabase client & migrations
│   │   ├── evaluation/         # RAGAS & manual rubric
│   │   ├── middleware/         # Rate limiting, LangSmith callback
│   │   ├── models/             # Pydantic models
│   │   ├── tools/              # Search tools (S2, arXiv, local)
│   │   └── utils/              # Budget alerts
│   ├── tests/                  # Pytest unit tests
│   └── requirements.txt
├── frontend/
│   ├── app/                    # Expo Router pages
│   ├── components/chat/        # Chat UI components
│   ├── data/                   # Mock data
│   ├── lib/                    # API client
│   └── types/                  # TypeScript types
├── SPEC.md                     # Current gate specification
├── VERSION_ROADMAP.md          # Full roadmap (v0.0 → v1.0)
└── CHANGELOG.md                # Detailed change log
```

## API Endpoints

### Research
- `POST /api/research/stream` - Submit query, receive SSE stream
- `GET /api/research/session/{id}` - Get session results

### Analytics
- `GET /api/analytics/cost/summary?days=7` - Cost summary
- `GET /api/analytics/cost/queries?limit=50` - Individual query costs
- `GET /api/analytics/cost/daily?days=30` - Daily cost aggregations
- `GET /api/analytics/cost/budget-status` - Budget threshold check

### Health
- `GET /health` - Health check

## Cost Controls

- **Max papers per query:** 5 (configurable)
- **Max LLM calls per query:** 10 (circuit breaker)
- **Rate limit:** 10 queries/hour per user
- **Daily spend alert:** $10 threshold

## Evaluation Metrics

### RAGAS (Automated)
- **Faithfulness:** ≥0.75 (answer grounded in context)
- **Answer Relevancy:** ≥0.70 (answer addresses question)
- **Context Precision:** ≥0.65 (retrieved context is relevant)

### Manual Rubric (Automated Heuristics)
- **Citation Accuracy:** % of papers cited in answer
- **Recency:** Includes papers from 2022-2024
- **Source Diversity:** Balanced vs skewed across S2/arXiv/local
- **Coverage Gaps:** Manual annotation (placeholder)

## LangSmith Integration

All queries are traced to LangSmith with:
- User ID, session ID, query metadata
- Tool calls (search_s2, search_arxiv, search_local)
- LLM calls with token counts
- Public trace URL: `https://smith.langchain.com/public/{run_id}/r`

Trace URLs are logged to `research_sessions.langsmith_trace_url`.

## Development

### Running Tests

```bash
cd backend
pytest tests/unit/                    # Unit tests
python test_v0.12_langsmith_cost.py   # E2E test
```

### Seeding Local Corpus

```bash
cd backend
python -m app.scripts.ingest_papers --seed-defaults
```

Seeds 5 foundational papers:
- Attention Is All You Need (Transformer, 2017)
- BERT (Pre-training, 2018)
- GPT-3 (Few-shot learning, 2020)
- Longformer (Long sequences, 2020)
- Reformer (Efficient attention, 2020)

## Roadmap

- [x] v0.0-v0.2: Foundation + Frontend Shell
- [x] v0.3-v0.5: Frontend Approved
- [x] v0.6: Test Strategy
- [x] v0.7: Backend Foundation
- [x] v0.8: ReAct Agent + Academic APIs
- [x] v0.9: Hybrid Retrieval + Paper Ingestion
- [x] v0.10: Synthesis + SSE Streaming
- [x] v0.11: Fault-Tolerant Tool Execution
- [x] v0.11b: Evaluation Framework (RAGAS + Manual Rubric)
- [x] v0.12: LangSmith Integration + Cost Analytics
- [ ] v0.13: Docker Compose Polish
- [ ] v0.14: CI/CD Pipeline
- [ ] v0.15: Multi-Provider BYOK
- [ ] v1.0: Production Live

See [VERSION_ROADMAP.md](VERSION_ROADMAP.md) for detailed breakdown.

## License

Private project

## Built With

- [LangGraph](https://langchain-ai.github.io/langgraph/) - Multi-agent orchestration
- [Claude](https://anthropic.com/claude) - LLM (Sonnet 4)
- [LangSmith](https://smith.langchain.com) - Tracing & observability
- [RAGAS](https://docs.ragas.io) - RAG evaluation framework
- [FastAPI](https://fastapi.tiangolo.com) - Backend framework
- [Expo](https://expo.dev) - React Native framework
- [Supabase](https://supabase.com) - PostgreSQL + pgvector
