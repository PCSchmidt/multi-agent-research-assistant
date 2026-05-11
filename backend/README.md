# Backend - Multi-Agent Research Assistant

FastAPI backend with LangGraph orchestration for academic research.

## Tech Stack

- **FastAPI** - Web framework
- **LangGraph** - Agent orchestration
- **Claude Sonnet 4** - LLM for reasoning and synthesis
- **OpenAI** - Embeddings (text-embedding-3-small)
- **Supabase** - PostgreSQL + pgvector
- **LangSmith** - Tracing and observability
- **RAGAS** - Evaluation framework

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings and environment variables
│   ├── api/
│   │   └── routes/
│   │       └── health.py    # Health check endpoint
│   ├── db/
│   │   ├── client.py        # Supabase client
│   │   └── migrations/
│   │       └── 001_initial_schema.sql
│   ├── middleware/
│   │   └── cost_tracking.py # LLM cost tracking
│   └── models/
│       └── research.py      # Pydantic models
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
├── Dockerfile
├── .env.example
└── pytest.ini
```

## Setup

### 1. Copy environment file

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys:
- `SUPABASE_URL` and `SUPABASE_KEY` from Supabase project settings
- `ANTHROPIC_API_KEY` from Anthropic console
- `OPENAI_API_KEY` from OpenAI console
- `LANGCHAIN_API_KEY` from LangSmith

### 2. Install dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Run database migrations

Apply the schema migration to your Supabase database:

1. Go to Supabase Dashboard → SQL Editor
2. Copy contents of `app/db/migrations/001_initial_schema.sql`
3. Run the migration

### 4. Start development server

```bash
uvicorn app.main:app --reload --port 8000
```

API will be available at:
- **Root**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_health.py -v

# Run only unit tests
pytest -m unit

# Run RAGAS eval tests (slow)
pytest -m ragas
```

Coverage report will be in `htmlcov/index.html`.

## Docker

### Build image

```bash
docker build -t research-assistant-backend .
```

### Run container

```bash
docker run -p 8000:8000 --env-file .env research-assistant-backend
```

### Docker Compose (from project root)

```bash
docker-compose up
```

## Environment Variables

See `.env.example` for full list. Required variables:

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase anon key |
| `ANTHROPIC_API_KEY` | Claude API key |
| `OPENAI_API_KEY` | OpenAI API key (for embeddings) |
| `LANGCHAIN_API_KEY` | LangSmith API key |

## Cost Controls

The backend implements cost safeguards:

- **Max 5 papers per query** (hard limit)
- **Max 10 LLM calls per query** (circuit breaker)
- **Rate limiting**: 10 queries/hour per user (default keys)
- **Budget alerts**: Email when daily spend > $10

Configure in `.env`:
```bash
MAX_PAPERS_PER_QUERY=5
MAX_LLM_CALLS_PER_QUERY=10
DAILY_SPEND_ALERT_USD=10.0
RATE_LIMIT_QUERIES_PER_HOUR=10
```

## API Endpoints

### Health Check
```bash
GET /health
```

Returns:
```json
{
  "status": "healthy",
  "environment": "development",
  "database_connected": true,
  "timestamp": "2026-05-10T12:00:00Z"
}
```

## Development

### Code Quality

```bash
# Lint with ruff
ruff check app/

# Type check with mypy
mypy app/

# Format code
ruff format app/
```

### Hot Reload

The development server watches for file changes:
```bash
uvicorn app.main:app --reload
```

### Debugging

Set breakpoints and run:
```bash
python -m debugpy --listen 5678 -m uvicorn app.main:app --reload
```

Attach your IDE debugger to port 5678.

## Next Steps (Upcoming Gates)

- **v0.8**: ReAct Agent + Academic API Tools
- **v0.9**: Hybrid Retrieval + Paper Ingestion
- **v0.10**: Synthesis + Streaming
- **v0.11**: Evaluation (RAGAS + Manual)
- **v0.12**: LangSmith Integration + Cost Analytics

---

**Version**: 0.7.0  
**Status**: Backend Foundation ✅
