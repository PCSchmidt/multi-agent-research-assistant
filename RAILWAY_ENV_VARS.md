# Railway Production Environment Variables

Copy these into Railway's Environment Variables section:

## Required Variables

### FastAPI Configuration
```
ENVIRONMENT=production
DEBUG=false
API_HOST=0.0.0.0
PORT=8000
```

### Supabase (Production Project)
Get these from your Supabase production dashboard:
- Project Settings → API → Project URL
- Project Settings → API → Project API keys

```
SUPABASE_URL=https://hdzhvpomcnnwfiirzykl.supabase.co
SUPABASE_KEY=<your-production-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-production-service-role-key>
```

### LLM Provider Keys (Owner's Default Keys)
These are YOUR API keys that serve as defaults when users don't provide their own:

```
ANTHROPIC_API_KEY=<your-anthropic-api-key>
OPENAI_API_KEY=<your-openai-api-key>
```

### LangSmith Tracing
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<your-langsmith-api-key>
LANGCHAIN_PROJECT=multi-agent-research-assistant-production
```

### Cost Controls
```
MAX_PAPERS_PER_QUERY=5
MAX_LLM_CALLS_PER_QUERY=10
DAILY_SPEND_ALERT_USD=10.0
RATE_LIMIT_QUERIES_PER_HOUR=10
```

### CORS Origins
**IMPORTANT**: Update this after Vercel deployment to include your Vercel domain

```
CORS_ORIGINS=https://multi-agent-research-assistant-nine.vercel.app
```

## Optional Variables

### Semantic Scholar API
```
S2_API_KEY=<optional-s2-api-key>
```

## Railway-Specific

Railway will automatically set `PORT` - your app should use `$PORT` from environment.
The backend is already configured to use `API_PORT` which defaults to 8000.

## Next Steps

1. Add all these variables in Railway dashboard: Settings → Variables
2. Update `CORS_ORIGINS` after Vercel deployment
3. Run migrations on production Supabase
4. Deploy and test

## Migration Command (Run Once)

After Railway deploys, you need to run migrations on your production Supabase.
You can do this from your local machine pointing to production Supabase:

```bash
# Set production Supabase credentials temporarily
export SUPABASE_URL=https://hdzhvpomcnnwfiirzykl.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>

# Run migrations (if using Supabase CLI)
# Or manually run SQL files in Supabase SQL Editor
```
