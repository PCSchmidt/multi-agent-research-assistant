-- User API Keys migration
-- Created: 2026-05-13
-- Description: BYOK (Bring Your Own Key) - User API key storage with encryption

-- Enable pgcrypto extension for encryption (if not already enabled)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =====================================================
-- USER API KEYS (BYOK)
-- =====================================================
CREATE TABLE user_api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    provider TEXT NOT NULL CHECK (provider IN ('anthropic', 'openai', 'openrouter')),
    encrypted_key TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Ensure one key per provider per user
    UNIQUE (user_id, provider)
);

-- Index for fast user lookups
CREATE INDEX idx_user_api_keys_user_id ON user_api_keys(user_id);
CREATE INDEX idx_user_api_keys_provider ON user_api_keys(provider);

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Enable RLS
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own keys
CREATE POLICY "Users can view own API keys"
    ON user_api_keys
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: Users can insert their own keys
CREATE POLICY "Users can insert own API keys"
    ON user_api_keys
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own keys
CREATE POLICY "Users can update own API keys"
    ON user_api_keys
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can delete their own keys
CREATE POLICY "Users can delete own API keys"
    ON user_api_keys
    FOR DELETE
    USING (auth.uid() = user_id);

-- =====================================================
-- TRIGGER: Auto-update updated_at
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_api_keys_updated_at
    BEFORE UPDATE ON user_api_keys
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
