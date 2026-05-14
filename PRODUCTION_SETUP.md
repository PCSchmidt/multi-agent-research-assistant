# Production Deployment Guide

## Step 1: Supabase Production Setup

### 1.1 Run Migrations

Go to your Supabase production dashboard → SQL Editor and run these migrations in order:

**Migration 1: Initial Schema**
- File: `backend/app/db/migrations/001_initial_schema.sql`
- Creates: research_sessions, papers, canonical_papers, eval_results, agent_statuses tables
- Enables: pgvector extension

**Migration 2: User API Keys (BYOK)**
- File: `supabase/migrations/20260513_user_api_keys.sql`
- Creates: user_api_keys table with encryption
- Enables: pgcrypto extension

### 1.2 Get Connection Details

From Supabase Dashboard → Settings → API:
- Copy **Project URL**: `https://hdzhvpomcnnwfiirzykl.supabase.co`
- Copy **anon/public key**: This is your `SUPABASE_KEY`
- Copy **service_role key**: This is your `SUPABASE_SERVICE_ROLE_KEY`

⚠️ **Keep service_role key secret** - it bypasses RLS policies

---

## Step 2: Railway Backend Deployment

### 2.1 Configure Environment Variables

In Railway dashboard → Settings → Variables, add all variables from `RAILWAY_ENV_VARS.md`:

**Critical ones:**
- `ENVIRONMENT=production`
- `DEBUG=false`
- `SUPABASE_URL` (from Step 1.2)
- `SUPABASE_KEY` (from Step 1.2)
- `SUPABASE_SERVICE_ROLE_KEY` (from Step 1.2)
- `ANTHROPIC_API_KEY` (your default key)
- `OPENAI_API_KEY` (your default key)
- `LANGCHAIN_API_KEY` (your LangSmith key)

### 2.2 Configure Build Settings

Railway should auto-detect Python. If not, set:
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.3 Get Backend URL

After deployment, Railway will give you a domain like:
`https://multi-agent-research-assistant-production.up.railway.app`

**Save this URL** - you'll need it for Vercel and mobile apps.

---

## Step 3: Vercel Frontend Deployment

### 3.1 Configure Project

In Vercel dashboard for `multi-agent-research-assistant`:
- **Framework Preset**: Automatically detected (Next.js/Expo)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` or `expo export:web`
- **Output Directory**: `.next` or `dist`

### 3.2 Environment Variables

Add in Vercel → Settings → Environment Variables:

```
EXPO_PUBLIC_API_URL=<your-railway-backend-url>
```

Example:
```
EXPO_PUBLIC_API_URL=https://multi-agent-research-assistant-production.up.railway.app
```

### 3.3 Deploy

Push to `main` branch → Vercel auto-deploys

Your web app will be at: `https://multi-agent-research-assistant-nine.vercel.app`

### 3.4 Update Railway CORS

Go back to Railway → Variables and update:
```
CORS_ORIGINS=https://multi-agent-research-assistant-nine.vercel.app
```

Redeploy Railway backend for CORS changes to take effect.

---

## Step 4: Verify Deployment

### 4.1 Backend Health Check

Visit: `https://<your-railway-domain>/health`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-14T..."
}
```

### 4.2 Frontend Verification

1. Visit your Vercel URL
2. Try to login (auth should work via Supabase)
3. Submit a research query
4. Verify streaming works

### 4.3 Check Logs

- **Railway**: Dashboard → Logs (check for errors)
- **Vercel**: Dashboard → Deployments → View Function Logs
- **Supabase**: Dashboard → Logs → Postgres Logs

---

## Step 5: Mobile Apps (Optional - Requires Apple/Google Accounts)

Since you don't have Apple Developer or Google Play Console accounts yet, skip this for now.

When ready, see `EAS_BUILD_GUIDE.md` for mobile deployment.

---

## Troubleshooting

### Backend won't start
- Check Railway logs for Python errors
- Verify all environment variables are set
- Check Supabase connection (try querying from backend logs)

### Frontend can't connect to backend
- Verify `EXPO_PUBLIC_API_URL` is correct in Vercel
- Check Railway logs for CORS errors
- Ensure `CORS_ORIGINS` includes Vercel domain

### Database errors
- Verify migrations ran successfully in Supabase SQL Editor
- Check RLS policies aren't blocking queries
- Verify service_role_key is correct

---

## Security Checklist

- [ ] `DEBUG=false` in Railway
- [ ] Service role key is secret (not in git)
- [ ] API keys are owner's defaults only
- [ ] CORS limited to Vercel domain only
- [ ] Rate limiting enabled (10 queries/hour)
- [ ] Daily spend alerts configured ($10/day)

---

## Next Steps After Deployment

1. Test end-to-end flow (signup → query → results)
2. Monitor costs in LangSmith dashboard
3. Set up error monitoring (Sentry, etc.)
4. Create CHANGELOG.md and HANDOFF.md
5. Make GitHub repo public
6. Share portfolio links

---

**Production URLs (Update after deployment):**

- Backend API: `https://___.up.railway.app`
- Web App: `https://multi-agent-research-assistant-nine.vercel.app`
- Supabase: `https://hdzhvpomcnnwfiirzykl.supabase.co`
