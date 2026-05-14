# Multi-Agent Research Assistant

> Academic research assistant powered by LangGraph, Claude Sonnet 4, and hybrid retrieval

[![CI](https://github.com/PCSchmidt/multi-agent-research-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/PCSchmidt/multi-agent-research-assistant/actions/workflows/ci.yml)
[![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-blue)](https://smith.langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)](https://fastapi.tiangolo.com)
[![Expo](https://img.shields.io/badge/Expo-React%20Native-black)](https://expo.dev)

## Overview

An AI-powered research assistant that combines live academic search (Semantic Scholar, arXiv) with a local canonical corpus to provide cited, synthesized answers to research questions. Built with LangGraph multi-agent orchestration, evaluated with RAGAS metrics, and traced with LangSmith.

**Current Status:** v1.0 - Production Live ✅

## 🚀 Live Deployment

- **Frontend (Web):** <https://multi-agent-research-assistant-nine.vercel.app>
- **Backend API:** <https://multi-agent-backend-production-a229.up.railway.app>
- **API Docs:** <https://multi-agent-backend-production-a229.up.railway.app/docs>
- **Database:** Supabase (managed PostgreSQL + pgvector)

> **Note:** Mobile apps (iOS/Android) require Apple Developer and Google Play Console accounts for deployment.

## Features

### ✅ Implemented (v0.0 → v1.0)

- **Multi-Agent ReAct Pattern** - LangGraph orchestration with tool-calling agent
- **Hybrid Retrieval** - Combines Semantic Scholar, arXiv, and local pgvector corpus
- **Cited Synthesis** - LLM generates answers with `[1], [2]` inline citations
- **SSE Streaming** - Real-time response streaming to frontend
- **Fault Tolerance** - Graceful degradation when external APIs fail
- **RAGAS Evaluation** - Automated quality metrics (faithfulness, answer relevancy, context precision)
- **Manual Rubric** - Citation accuracy, recency, source diversity metrics
- **LangSmith Tracing** - Full observability with trace URLs logged to database
- **Cost Tracking** - Token usage and cost calculated per query
- **Rate Limiting** - 10 queries/hour per user (configurable)
- **Budget Alerts** - Triggers at $10/day threshold
- **Docker Compose** - Single-command local development environment
- **CI/CD Pipeline** - GitHub Actions with automated testing
- **Multi-Provider BYOK** - Bring Your Own API Keys (Anthropic, OpenAI, OpenRouter)
- **Production Deployment** - Railway (backend), Vercel (frontend), Supabase (database)

## Tech Stack

### Backend
- **Framework:** FastAPI + Uvicorn
- **Agent:** LangGraph (ReAct pattern)
- **LLM:** Multi-provider (Anthropic Claude, OpenAI, OpenRouter) - configurable via BYOK
- **Embeddings:** OpenAI `text-embedding-3-small` (1536-dim)
- **Database:** Supabase (PostgreSQL + pgvector)
- **Evals:** RAGAS
- **Tracing:** LangSmith
- **Deployment:** Railway

### Frontend
- **Framework:** Expo (React Native + Web)
- **Language:** TypeScript
- **Styling:** NativeWind (Tailwind for React Native)
- **State:** React hooks (no global state library)
- **Deployment:** Vercel (web), EAS Build ready (mobile)

### Academic APIs
- **Semantic Scholar API** - Citation data, recent papers
- **arXiv API** - Preprints and latest research
- **Local Corpus** - pgvector similarity search over canonical papers

## Quick Start

### Prerequisites

- **Docker** (Recommended): Docker Desktop installed and running
- **OR Manual Setup**: Python 3.11+, Node.js 18+
- **Supabase account**: Create a project at [supabase.com](https://supabase.com)
- **API keys**:
  - **LLM Provider** (choose one or more):
    - Anthropic (Claude) - [console.anthropic.com](https://console.anthropic.com)
    - OpenRouter (multi-provider, free models available) - [openrouter.ai](https://openrouter.ai)
    - OpenAI (GPT models) - [platform.openai.com](https://platform.openai.com)
  - **Embeddings** (required): OpenAI - [platform.openai.com](https://platform.openai.com)
  - **Tracing** (required): LangSmith - [smith.langchain.com](https://smith.langchain.com)

### Option 1: Docker Compose (Recommended)

**Single-command startup for complete local environment:**

```bash
# 1. Clone repository
git clone https://github.com/PCSchmidt/multi-agent-research-assistant.git
cd multi-agent-research-assistant

# 2. Configure environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys (see Prerequisites above)

# 3. Apply database migrations to your Supabase project
# Go to your Supabase dashboard → SQL Editor
# Run: backend/app/db/migrations/001_initial_schema.sql

# 4. Start all services
docker-compose up

# Services will be available at:
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs  
# - Frontend Web: http://localhost:8081
```

**Useful Docker commands:**
```bash
docker-compose up -d        # Start in background
docker-compose logs -f      # Follow logs
docker-compose down         # Stop all services
docker-compose restart      # Restart after .env changes
```

**Note:** For iOS/Android development, run `npm start` in `frontend/` directory instead of using Docker (Expo Dev Tools needed for mobile).

### Option 2: Manual Setup (Without Docker)

##### Backend Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run migrations (Supabase)
# Apply backend/app/db/migrations/001_initial_schema.sql to your Supabase project

# Start server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm start

# For web only:
# npm run web
```

See [SETUP.md](SETUP.md) for detailed manual setup instructions and troubleshooting.

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
- [x] v0.13: Docker Compose Polish
- [x] v0.14: CI/CD Pipeline
- [x] v0.15: Multi-Provider BYOK
- [x] v1.0: Production Live

See [VERSION_ROADMAP.md](VERSION_ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md) for detailed version history.

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
