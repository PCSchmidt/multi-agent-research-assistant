# BYOK (Bring Your Own Key) Implementation Research

## Executive Summary

**Scope:** Allow users to optionally provide their own API keys (Anthropic, OpenAI, OpenRouter) with fallback to owner's default keys.

**Timeline Recommendation:** 
- **Option A:** Implement in v0.15 as originally planned (after CI/CD, before production)
- **Option B:** Implement now in v0.10.5 (before frontend integration, cleaner architecture)
- **Option C:** MVP now (basic encryption + storage), full features in v0.15

**Estimated Effort:** 6-9 hours (per VERSION_ROADMAP.md v0.15)

---

## Architecture Overview

### Key Hierarchy
```
Query → Check user_api_keys table for user_id
  ├─ User key exists? → Use user's key
  └─ No user key? → Fallback to owner's default key (from .env)
```

### Data Flow
```
1. User enters API key in Settings UI
2. Frontend → POST /api/keys (encrypted over HTTPS)
3. Backend encrypts key with pgcrypto
4. Store in user_api_keys table with RLS
5. On research query:
   - Fetch user's keys from DB
   - Decrypt using pgcrypto
   - Initialize LLM clients with user/default keys
   - Execute query
```

---

## Implementation Breakdown

### 1. Database Layer (1-2h)

**New Table: `user_api_keys`**
```sql
CREATE TABLE user_api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    provider TEXT NOT NULL CHECK (provider IN ('anthropic', 'openai', 'openrouter')),
    encrypted_key TEXT NOT NULL,  -- pgcrypto encrypted
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Only one active key per provider per user
    UNIQUE(user_id, provider, is_active)
);

-- Indexes
CREATE INDEX idx_user_api_keys_user_id ON user_api_keys(user_id);
CREATE INDEX idx_user_api_keys_provider ON user_api_keys(provider);

-- RLS Policies (users can only see their own keys)
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own API keys"
    ON user_api_keys FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own API keys"
    ON user_api_keys FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own API keys"
    ON user_api_keys FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own API keys"
    ON user_api_keys FOR DELETE
    USING (auth.uid() = user_id);
```

**Encryption Functions (using pgcrypto):**
```sql
-- Already enabled in 001_initial_schema.sql:
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt function (use owner's encryption key from env)
SELECT pgp_sym_encrypt('sk-ant-api03-...', 'ENCRYPTION_SECRET_KEY');

-- Decrypt function
SELECT pgp_sym_decrypt(encrypted_key, 'ENCRYPTION_SECRET_KEY') FROM user_api_keys;
```

**Migration:** `backend/app/db/migrations/002_user_api_keys.sql`

---

### 2. Backend API Endpoints (2-3h)

**File:** `backend/app/api/routes/keys.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.db.client import get_supabase_client
from app.config import settings

router = APIRouter(tags=["keys"], prefix="/api/keys")

class APIKeyRequest(BaseModel):
    provider: Literal["anthropic", "openai", "openrouter"]
    api_key: str = Field(..., min_length=10)

class APIKeyResponse(BaseModel):
    id: str
    provider: str
    is_active: bool
    created_at: str

# POST /api/keys - Save new key
@router.post("/", response_model=APIKeyResponse)
async def save_api_key(request: APIKeyRequest, user_id: str = Depends(get_current_user)):
    supabase = get_supabase_client()
    
    # Encrypt key using pgcrypto
    result = supabase.rpc(
        'encrypt_api_key',
        {'plaintext_key': request.api_key, 'secret': settings.encryption_key}
    ).execute()
    
    encrypted_key = result.data
    
    # Insert into database
    data = {
        "user_id": user_id,
        "provider": request.provider,
        "encrypted_key": encrypted_key,
        "is_active": True,
    }
    
    # Upsert (deactivate old keys, insert new)
    # ... implementation
    
    return APIKeyResponse(...)

# GET /api/keys - List user's keys (masked)
@router.get("/")
async def list_api_keys(user_id: str = Depends(get_current_user)):
    supabase = get_supabase_client()
    result = supabase.table("user_api_keys")\
        .select("id, provider, is_active, created_at")\
        .eq("user_id", user_id)\
        .execute()
    
    return result.data

# DELETE /api/keys/{key_id}
@router.delete("/{key_id}")
async def delete_api_key(key_id: str, user_id: str = Depends(get_current_user)):
    supabase = get_supabase_client()
    # Verify ownership + delete
    # ... implementation
```

**Key Retrieval Logic:**
```python
# backend/app/services/key_manager.py

async def get_api_key(user_id: str, provider: str) -> str:
    """
    Get API key for user and provider.
    Falls back to default key if user hasn't configured one.
    """
    supabase = get_supabase_admin_client()  # Admin to decrypt
    
    # Try to fetch user's key
    result = supabase.table("user_api_keys")\
        .select("encrypted_key")\
        .eq("user_id", user_id)\
        .eq("provider", provider)\
        .eq("is_active", True)\
        .single()\
        .execute()
    
    if result.data:
        # Decrypt user's key
        decrypted = supabase.rpc(
            'decrypt_api_key',
            {'encrypted_key': result.data['encrypted_key'], 'secret': settings.encryption_key}
        ).execute()
        return decrypted.data
    
    # Fallback to default key
    default_keys = {
        'anthropic': settings.anthropic_api_key,
        'openai': settings.openai_api_key,
        # ... etc
    }
    return default_keys.get(provider)
```

**Integration into Agent:**
```python
# backend/app/agent/graph.py

async def create_research_agent(user_id: str) -> StateGraph:
    # Get user's API keys (or defaults)
    anthropic_key = await get_api_key(user_id, 'anthropic')
    openai_key = await get_api_key(user_id, 'openai')
    
    # Initialize LLMs with user/default keys
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=anthropic_key,  # User's key or default
        temperature=0.1,
    )
    # ... rest of agent setup
```

---

### 3. Frontend UI (2h)

**File:** `frontend/app/(tabs)/settings.tsx`

Current state: Placeholder UI exists (lines 29-49)

**Updates needed:**
```typescript
import { useState } from 'react';
import { TextInput, Button, ActivityIndicator } from 'react-native';
import { saveAPIKey, testAPIKey, deleteAPIKey } from '@/lib/api';

// State for each provider
const [anthropicKey, setAnthropicKey] = useState('');
const [openaiKey, setOpenaiKey] = useState('');
const [showKeys, setShowKeys] = useState({ anthropic: false, openai: false });
const [saving, setSaving] = useState(false);

// Save handler
const handleSaveKey = async (provider: string, key: string) => {
  setSaving(true);
  try {
    await saveAPIKey(provider, key);
    Alert.alert('Success', 'API key saved successfully');
  } catch (error) {
    Alert.alert('Error', error.message);
  } finally {
    setSaving(false);
  }
};

// Test connection handler
const handleTestKey = async (provider: string, key: string) => {
  try {
    const valid = await testAPIKey(provider, key);
    Alert.alert(valid ? 'Valid' : 'Invalid', ...);
  } catch (error) {
    Alert.alert('Error', 'Connection test failed');
  }
};

// UI Components:
// - TextInput with secureTextEntry (show/hide toggle)
// - Save button per provider
// - Test connection button
// - Delete/revoke button
// - Masked display for saved keys (sk-ant-***...)
```

**API Client Updates:**
```typescript
// frontend/lib/api.ts

export async function saveAPIKey(provider: string, apiKey: string) {
  const response = await fetch(`${API_BASE_URL}/api/keys`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authToken}`,  // Add auth
    },
    body: JSON.stringify({ provider, api_key: apiKey }),
  });
  
  if (!response.ok) throw new Error('Failed to save API key');
  return response.json();
}

export async function testAPIKey(provider: string, apiKey: string): Promise<boolean> {
  // Simple test: try to make minimal API call
  // e.g., for Anthropic, call /v1/messages with max_tokens=1
}
```

---

### 4. Security Considerations

**Encryption:**
- ✅ Keys encrypted at rest using pgcrypto (`pgp_sym_encrypt`)
- ✅ Keys encrypted in transit (HTTPS only)
- ✅ Encryption secret stored in backend .env (never exposed to frontend)
- ✅ RLS ensures users only access their own keys

**Key Validation:**
- Validate key format before saving (e.g., `sk-ant-api03-...`)
- Test key validity with minimal API call
- Sanitize input (prevent injection)

**Rate Limiting:**
- Limit key save operations (prevent abuse)
- User keys subject to provider rate limits (not owner's limits)

**Audit Trail:**
- Log key creation/deletion events
- Track which keys were used for which queries (metadata)

---

### 5. Testing Strategy (1h)

**Backend Tests:**
```python
# backend/tests/unit/test_key_manager.py

async def test_user_key_overrides_default():
    # Setup: user has custom Anthropic key
    # Assert: get_api_key returns user's key, not default

async def test_fallback_to_default_key():
    # Setup: user has NO custom key
    # Assert: get_api_key returns default from settings

async def test_encryption_roundtrip():
    # Encrypt key → save → retrieve → decrypt
    # Assert: decrypted key == original key

async def test_rls_isolation():
    # User A saves key, User B tries to read
    # Assert: User B cannot see User A's key
```

**Frontend Tests:**
```typescript
// frontend/__tests__/settings.test.tsx

test('save API key shows success message', async () => {
  // Simulate key save
  // Assert: success alert shown
});

test('test connection with invalid key shows error', async () => {
  // Mock API to return 401
  // Assert: error alert shown
});
```

**E2E Test:**
1. User saves Anthropic key via Settings UI
2. Submit research query
3. Verify: Query uses user's key (check LangSmith trace metadata)
4. Delete key
5. Submit another query
6. Verify: Query uses default key

---

## Implementation Options

### Option A: Full Implementation Now (6-9h)
**Pro:** Cleaner architecture, no rework later  
**Con:** Delays v0.10 completion, adds scope

**Steps:**
1. Create `user_api_keys` table + migration
2. Build `/api/keys` endpoints
3. Update agent to use `get_api_key()`
4. Build Settings UI
5. Test encryption + fallback logic

### Option B: MVP Now, Full Features in v0.15 (3-4h now, 3-4h later)
**Pro:** Basic functionality now, polish later  
**Con:** Some rework, two implementation phases

**MVP Scope (now):**
- Database table + encryption
- Simple save/retrieve endpoints (no test connection, no deletion)
- Hardcoded fallback in agent
- Basic Settings UI (text input only)

**v0.15 Scope (later):**
- Test connection feature
- Delete/revoke keys
- Key masking in UI
- Audit logs

### Option C: Defer to v0.15 (0h now, 6-9h later)
**Pro:** Stay focused on v0.10 streaming  
**Con:** All work deferred

**Rationale:** BYOK is nice-to-have for portfolio demo. Most reviewers will use default keys. Can implement after core features work.

---

## Recommendation

**Go with Option C (Defer to v0.15) unless:**
- You want to demo BYOK specifically in portfolio
- You plan to use this tool yourself with your own keys soon
- You have concerns about cost with default keys

**Why defer:**
1. v0.10 streaming is 70% done - finish it first
2. BYOK adds no new UX capability (users can research either way)
3. Cleaner to add BYOK after auth is implemented (v0.12+)
4. Contract already plans it for v0.15

**If you proceed now, use Option B (MVP):**
- Minimal disruption to v0.10
- Basic functionality in place
- Polish in v0.15 as planned

---

## Environment Variables Needed (if implementing)

```bash
# Add to backend/.env
ENCRYPTION_SECRET_KEY=<generate-strong-random-key>  # For pgcrypto encryption

# Generate with:
# openssl rand -base64 32
```

---

## Files to Create/Modify

### New Files:
- `backend/app/db/migrations/002_user_api_keys.sql`
- `backend/app/api/routes/keys.py`
- `backend/app/services/key_manager.py`
- `backend/tests/unit/test_key_manager.py`

### Modified Files:
- `backend/app/agent/graph.py` - Accept user_id, call `get_api_key()`
- `backend/app/api/routes/research.py` - Pass user_id to agent
- `frontend/app/(tabs)/settings.tsx` - Build key management UI
- `frontend/lib/api.ts` - Add key CRUD functions
- `backend/app/config.py` - Add `encryption_secret_key`

---

## Decision Points for User

1. **When?** Option A (now), B (MVP now), or C (defer to v0.15)?
2. **Scope?** Full features or MVP?
3. **Priority?** Does BYOK unlock something critical for you?

**My recommendation:** Finish v0.10 streaming first (30% left), then decide on BYOK.
