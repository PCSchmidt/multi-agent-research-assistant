# Development Setup Guide

Complete guide for setting up and running the Multi-Agent Research Assistant locally.

---

## Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **Git**
- **Expo Go app** (for mobile testing)
- **PostgreSQL** (via Supabase)

---

## Initial Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd multi-agent-research-assistant
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `backend/.env` with your API keys:**

```bash
# Supabase
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# LLM Providers
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

# LangSmith (optional but recommended)
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=research-assistant
LANGCHAIN_TRACING_V2=true

# Optional: Semantic Scholar API key (reduces rate limiting)
SEMANTIC_SCHOLAR_API_KEY=your_s2_key

# Environment
ENVIRONMENT=development
DEBUG=true
```

**Run database migrations:**

```bash
# Using psql (or Supabase SQL Editor)
psql -h <supabase-host> -U postgres -d postgres -f app/db/migrations/001_initial_schema.sql
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (optional)
# EXPO_PUBLIC_API_URL=http://localhost:8000
```

---

## Running the Application

### Backend (API Server)

```bash
cd backend
venv\Scripts\activate  # Windows
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Verify backend is running:**
- Open http://localhost:8000
- Should see: `{"message": "Multi-Agent Research Assistant API", ...}`
- API docs: http://localhost:8000/docs

### Frontend (Web)

```bash
cd frontend
npm start
```

**Verify frontend is running:**
- Open http://localhost:8081 in browser
- Should see Research Assistant chat interface

---

## Mobile Testing (Expo Go)

### Windows Firewall Configuration

**Port 8081 must be accessible from your local network for mobile devices.**

#### Option 1: PowerShell (Recommended)

Run PowerShell **as Administrator**:

```powershell
New-NetFirewallRule -DisplayName "Expo Dev Server" -Direction Inbound -LocalPort 8081 -Protocol TCP -Action Allow
```

#### Option 2: Windows Firewall GUI

1. Open **Windows Defender Firewall** → **Advanced Settings**
2. Click **Inbound Rules** → **New Rule**
3. Select **Port** → Next
4. **TCP**, Specific local ports: `8081` → Next
5. **Allow the connection** → Next
6. Check all profiles (Domain, Private, Public) → Next
7. Name: "Expo Dev Server" → Finish

#### Option 3: Temporarily Disable Firewall (Testing Only)

```powershell
# Disable (run as Administrator)
netsh advfirewall set allprofiles state off

# Re-enable when done
netsh advfirewall set allprofiles state on
```

### Connecting from Mobile Device

1. **Ensure phone and PC are on the same WiFi network**
2. **Find your PC's IP address:**

```bash
ipconfig | grep "IPv4"
# Look for: 192.168.x.x
```

3. **Open Expo Go app on your phone**
4. **Scan the QR code** from the terminal, or
5. **Manually enter:** `exp://192.168.1.12:8081` (replace with your IP)

### Troubleshooting Mobile Connection

**Timeout when scanning QR code?**

- ✅ Check PC and phone are on same WiFi
- ✅ Verify firewall rule exists: `netsh advfirewall firewall show rule name="Expo Dev Server"`
- ✅ Check Expo server is running: `netstat -an | findstr "8081"`
- ✅ Try web browser on phone first: `http://192.168.1.12:8081`

**Still not working?**

- Restart Expo dev server: `npm start`
- Clear Metro cache: `npm start -- --clear`
- Try different WiFi network (avoid corporate/guest networks with isolation)

---

## Testing the Integration

### 1. Web Browser Test

1. Open http://localhost:8081
2. Type a research query (min 10 characters): `"quantum computing error correction"`
3. Click **Submit Query**
4. You should see:
   - Loading spinner on button
   - User message appears in chat
   - Backend processes query
   - Assistant response appears (or error if rate limited)

### 2. Backend Direct Test

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test streaming endpoint
curl -N -X POST http://localhost:8000/api/research/stream \
  -H "Content-Type: application/json" \
  -d '{"query":"quantum computing error correction methods"}'
```

**Expected SSE output:**
```
event: status
data: {"message": "Starting research query...", "session_id": "..."}

event: paper
data: {"title": "...", "authors": [...], ...}

event: synthesis
data: {"content": "..."}

event: done
data: {"session_id": "...", "papers_count": 5, "synthesis": "..."}
```

### 3. Check Browser Console

Open DevTools (F12) → Console tab:
- ✅ Should see: `"Agent status: Starting research query..."`
- ✅ No CORS errors
- ❌ If 404 errors: backend not running or wrong URL
- ❌ If network errors: check CORS/firewall

---

## Common Issues & Solutions

### Backend Issues

**Import errors / module not found:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

**Database connection failed:**
- Check `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Verify Supabase project is active
- Run migrations if tables don't exist

**Rate limit errors (429) from Semantic Scholar:**
- Add `SEMANTIC_SCHOLAR_API_KEY` to `.env` (get free key from S2)
- Or implement retry logic with exponential backoff
- Or add per-tool error handling (see SPEC.md v0.11 plans)

**Network errors (Errno 11001 getaddrinfo failed):**
- Check internet connection
- Verify no proxy/VPN blocking API access
- Try different network

### Frontend Issues

**Blank screen or loading forever:**
- Check backend is running on port 8000
- Check `EXPO_PUBLIC_API_URL` in `.env` (default: `http://localhost:8000`)
- Open browser console for errors

**Alert.alert() not showing on web:**
- Fixed in v0.10: errors now show as assistant messages instead of alerts
- Alert API is mobile-only, doesn't work on React Native Web

**TypeScript errors in test files:**
- Jest configuration issue, not code issue
- Tests run fine with `npm test`
- Can ignore in VSCode or add `@types/jest`

### Mobile Issues

**Connection timeout on phone:**
- See "Mobile Testing" section above
- Most common: Windows Firewall blocking port 8081

**QR code scanner not working:**
- Manually enter URL: `exp://YOUR_PC_IP:8081`
- Or use web browser on phone: `http://YOUR_PC_IP:8081`

---

## Development Workflow

### Starting a Development Session

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

### Making Changes

**Backend changes:**
- Edit Python files in `backend/app/`
- Uvicorn auto-reloads on file changes
- Check terminal for errors

**Frontend changes:**
- Edit TypeScript files in `frontend/`
- Metro bundler auto-reloads
- Refresh browser or shake phone to reload

**Database schema changes:**
- Create new migration file: `backend/app/db/migrations/00X_description.sql`
- Run migration manually via psql or Supabase SQL Editor
- Update models in `backend/app/models/`

### Testing

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test

# E2E test (manual)
# 1. Start backend + frontend
# 2. Submit query in browser
# 3. Check SSE events in Network tab
# 4. Verify synthesis appears in chat
```

---

## Production Deployment (v0.14+)

Production deployment is planned for v0.14. Current setup is development-only.

**Required for production:**
- Environment variables secured (not in .env files)
- HTTPS for backend (TLS/SSL)
- Auth enabled (v0.12)
- Rate limiting (v0.13)
- Error tracking (Sentry)
- Analytics
- CI/CD pipeline

---

## Useful Commands

### Backend

```bash
# Check Python version
python --version

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install new package
pip install <package>
pip freeze > requirements.txt

# Run tests
pytest -v
pytest tests/unit/test_health.py -v

# Check code style
black app/
ruff check app/
```

### Frontend

```bash
# Check Node version
node --version

# Install new package
npm install <package>

# Clear Metro cache
npm start -- --clear

# TypeScript check
npx tsc --noEmit

# Format code
npx prettier --write .
```

### Network Debugging

```bash
# Check if port is in use
netstat -an | findstr "8000"  # Backend
netstat -an | findstr "8081"  # Frontend

# Find your IP address
ipconfig | grep "IPv4"

# Test backend endpoint
curl http://localhost:8000/health

# Kill process on port (Windows)
taskkill /F /PID <pid>
```

---

## Getting Help

- **SPEC.md** - Product requirements and roadmap
- **VERSION_ROADMAP.md** - Detailed version plan
- **backend/README.md** - Backend architecture
- **frontend/README.md** - Frontend architecture

**Issues during setup?**
1. Check this guide's "Common Issues" section
2. Verify all prerequisites are installed
3. Check terminal/console for error messages
4. Review logs in backend terminal
5. Open DevTools in browser (F12) for frontend errors

---

## Next Steps

After setup is complete:

1. **Verify basic functionality** - Submit a test query
2. **Review SPEC.md** - Understand the product vision
3. **Check VERSION_ROADMAP.md** - See what's planned next
4. **Run tests** - Ensure everything works
5. **Start developing!**

Current status: **v0.12 complete** (LangSmith Integration + Cost Analytics)

Next up: **v0.13** - Docker Compose polish for single-command local dev startup
