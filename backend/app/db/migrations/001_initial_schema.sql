-- Migration 001: Initial Schema
-- Created: 2026-05-10
-- Description: Core tables for academic research assistant

-- Enable pgvector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable pgcrypto for UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Enable pg_trgm for fuzzy text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- =====================================================
-- RESEARCH SESSIONS
-- =====================================================
CREATE TABLE research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    answer TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),

    -- Cost tracking
    total_tokens INTEGER DEFAULT 0,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cost_usd DECIMAL(10, 6) DEFAULT 0.0,
    llm_calls_count INTEGER DEFAULT 0,

    -- Metadata
    langsmith_trace_url TEXT,
    error_message TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    CONSTRAINT valid_tokens CHECK (total_tokens >= 0 AND input_tokens >= 0 AND output_tokens >= 0),
    CONSTRAINT valid_cost CHECK (cost_usd >= 0),
    CONSTRAINT valid_llm_calls CHECK (llm_calls_count >= 0)
);

-- Index for user queries
CREATE INDEX idx_research_sessions_user_id ON research_sessions(user_id);
CREATE INDEX idx_research_sessions_created_at ON research_sessions(created_at DESC);
CREATE INDEX idx_research_sessions_status ON research_sessions(status);

-- =====================================================
-- PAPERS (retrieved during queries)
-- =====================================================
CREATE TABLE papers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES research_sessions(id) ON DELETE CASCADE,

    -- Paper identifiers
    paper_id TEXT NOT NULL,  -- S2 corpus ID, arXiv ID, or local ID
    source TEXT NOT NULL CHECK (source IN ('s2', 'arxiv', 'local')),

    -- Metadata
    title TEXT NOT NULL,
    authors JSONB NOT NULL DEFAULT '[]',  -- [{name: string, affiliations?: string[]}]
    abstract TEXT,
    year INTEGER,
    venue TEXT,
    citation_count INTEGER DEFAULT 0,
    url TEXT,

    -- Retrieval metadata
    relevance_score DECIMAL(5, 4),  -- 0.0000 - 1.0000
    citation_number INTEGER,  -- Position in cited answer [1], [2], etc.

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT valid_year CHECK (year IS NULL OR (year >= 1900 AND year <= 2100)),
    CONSTRAINT valid_relevance CHECK (relevance_score IS NULL OR (relevance_score >= 0 AND relevance_score <= 1)),
    CONSTRAINT valid_citation_number CHECK (citation_number IS NULL OR citation_number > 0)
);

-- Indexes
CREATE INDEX idx_papers_session_id ON papers(session_id);
CREATE INDEX idx_papers_paper_id ON papers(paper_id);
CREATE INDEX idx_papers_source ON papers(source);

-- =====================================================
-- CANONICAL PAPERS (local corpus for pgvector)
-- =====================================================
CREATE TABLE canonical_papers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Paper identifiers
    paper_id TEXT NOT NULL UNIQUE,  -- S2 corpus ID, arXiv ID, DOI, etc.
    source TEXT NOT NULL CHECK (source IN ('s2', 'arxiv', 'manual')),

    -- Metadata
    title TEXT NOT NULL,
    authors JSONB NOT NULL DEFAULT '[]',
    abstract TEXT NOT NULL,
    year INTEGER NOT NULL,
    venue TEXT,
    citation_count INTEGER DEFAULT 0,
    url TEXT,

    -- Vector embedding (1536 dimensions for OpenAI text-embedding-3-small)
    embedding vector(1536),

    -- Curation metadata
    added_by UUID REFERENCES auth.users(id),
    tags TEXT[] DEFAULT '{}',  -- ['foundational', 'survey', 'seminal', etc.]
    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT valid_year CHECK (year >= 1900 AND year <= 2100)
);

-- Indexes
CREATE INDEX idx_canonical_papers_paper_id ON canonical_papers(paper_id);
CREATE INDEX idx_canonical_papers_source ON canonical_papers(source);
CREATE INDEX idx_canonical_papers_year ON canonical_papers(year DESC);
CREATE INDEX idx_canonical_papers_tags ON canonical_papers USING GIN(tags);

-- Vector similarity search index (IVFFlat for pgvector)
CREATE INDEX idx_canonical_papers_embedding ON canonical_papers
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Full-text search index on title + abstract
CREATE INDEX idx_canonical_papers_fulltext ON canonical_papers
    USING GIN(to_tsvector('english', title || ' ' || COALESCE(abstract, '')));

-- =====================================================
-- EVALUATION RESULTS
-- =====================================================
CREATE TABLE eval_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES research_sessions(id) ON DELETE CASCADE,

    -- RAGAS metrics (for local corpus queries)
    faithfulness DECIMAL(5, 4),  -- 0.0000 - 1.0000
    answer_relevancy DECIMAL(5, 4),
    context_precision DECIMAL(5, 4),
    ragas_status TEXT CHECK (ragas_status IN ('pending', 'completed', 'failed', 'skipped')),

    -- Manual evaluation metrics (for live search queries)
    citation_accuracy DECIMAL(5, 4),  -- % of citations that support claims
    has_recent_papers BOOLEAN,  -- Includes 2022-2024 papers when relevant
    coverage_gaps TEXT[],  -- Missing seminal works (manual annotation)
    source_diversity TEXT CHECK (source_diversity IN ('balanced', 'skewed', 'n/a')),

    -- Metadata
    evaluator TEXT,  -- 'ragas' for automated, user email for manual
    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT valid_ragas_scores CHECK (
        (faithfulness IS NULL OR (faithfulness >= 0 AND faithfulness <= 1)) AND
        (answer_relevancy IS NULL OR (answer_relevancy >= 0 AND answer_relevancy <= 1)) AND
        (context_precision IS NULL OR (context_precision >= 0 AND context_precision <= 1))
    ),
    CONSTRAINT valid_citation_accuracy CHECK (
        citation_accuracy IS NULL OR (citation_accuracy >= 0 AND citation_accuracy <= 1)
    )
);

-- Indexes
CREATE INDEX idx_eval_results_session_id ON eval_results(session_id);
CREATE INDEX idx_eval_results_ragas_status ON eval_results(ragas_status);
CREATE INDEX idx_eval_results_created_at ON eval_results(created_at DESC);

-- =====================================================
-- AGENT STATUSES (for timeline tracking)
-- =====================================================
CREATE TABLE agent_statuses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES research_sessions(id) ON DELETE CASCADE,

    agent TEXT NOT NULL CHECK (agent IN ('search_s2', 'search_arxiv', 'search_local', 'synthesize', 'evaluate')),
    status TEXT NOT NULL CHECK (status IN ('pending', 'active', 'completed', 'failed')),

    -- Metadata (JSONB for flexibility)
    metadata JSONB DEFAULT '{}',  -- {papersFound: 5, tokensGenerated: 487, etc.}
    error_message TEXT,

    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT valid_timestamps CHECK (
        started_at IS NULL OR completed_at IS NULL OR completed_at >= started_at
    )
);

-- Indexes
CREATE INDEX idx_agent_statuses_session_id ON agent_statuses(session_id);
CREATE INDEX idx_agent_statuses_agent ON agent_statuses(agent);
CREATE INDEX idx_agent_statuses_status ON agent_statuses(status);

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE research_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE canonical_papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE eval_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_statuses ENABLE ROW LEVEL SECURITY;

-- Research sessions: users can only see their own
CREATE POLICY research_sessions_select_policy ON research_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY research_sessions_insert_policy ON research_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY research_sessions_update_policy ON research_sessions
    FOR UPDATE USING (auth.uid() = user_id);

-- Papers: users can only see papers from their sessions
CREATE POLICY papers_select_policy ON papers
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM research_sessions
            WHERE research_sessions.id = papers.session_id
            AND research_sessions.user_id = auth.uid()
        )
    );

CREATE POLICY papers_insert_policy ON papers
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM research_sessions
            WHERE research_sessions.id = papers.session_id
            AND research_sessions.user_id = auth.uid()
        )
    );

-- Canonical papers: read-only for all authenticated users
CREATE POLICY canonical_papers_select_policy ON canonical_papers
    FOR SELECT USING (auth.role() = 'authenticated');

-- Only admins can insert/update canonical papers (handled via service role key)

-- Eval results: users can only see evals for their sessions
CREATE POLICY eval_results_select_policy ON eval_results
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM research_sessions
            WHERE research_sessions.id = eval_results.session_id
            AND research_sessions.user_id = auth.uid()
        )
    );

CREATE POLICY eval_results_insert_policy ON eval_results
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM research_sessions
            WHERE research_sessions.id = eval_results.session_id
            AND research_sessions.user_id = auth.uid()
        )
    );

-- Agent statuses: users can only see statuses for their sessions
CREATE POLICY agent_statuses_select_policy ON agent_statuses
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM research_sessions
            WHERE research_sessions.id = agent_statuses.session_id
            AND research_sessions.user_id = auth.uid()
        )
    );

CREATE POLICY agent_statuses_insert_policy ON agent_statuses
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM research_sessions
            WHERE research_sessions.id = agent_statuses.session_id
            AND research_sessions.user_id = auth.uid()
        )
    );

-- =====================================================
-- FUNCTIONS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for canonical_papers updated_at
CREATE TRIGGER update_canonical_papers_updated_at
    BEFORE UPDATE ON canonical_papers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to search canonical papers by vector similarity
CREATE OR REPLACE FUNCTION search_canonical_papers(
    query_embedding vector(1536),
    match_threshold DECIMAL DEFAULT 0.7,
    match_count INTEGER DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    paper_id TEXT,
    title TEXT,
    authors JSONB,
    abstract TEXT,
    year INTEGER,
    venue TEXT,
    citation_count INTEGER,
    url TEXT,
    similarity DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        cp.id,
        cp.paper_id,
        cp.title,
        cp.authors,
        cp.abstract,
        cp.year,
        cp.venue,
        cp.citation_count,
        cp.url,
        (1 - (cp.embedding <=> query_embedding))::DECIMAL AS similarity
    FROM canonical_papers cp
    WHERE (1 - (cp.embedding <=> query_embedding)) > match_threshold
    ORDER BY cp.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- SEED DATA (optional - for development)
-- =====================================================

-- Note: Seed canonical papers will be added via ingestion script (v0.9)
-- This migration only creates the schema
