// Type definitions for academic research data structures

export interface Paper {
  id: string;
  paperId: string; // S2 corpus ID or arXiv ID
  title: string;
  authors: Author[];
  abstract: string;
  year: number;
  venue: string;
  citationCount: number;
  url: string;
  source: 's2' | 'arxiv' | 'local';
}

export interface Author {
  name: string;
  authorId?: string;
}

export interface Citation {
  number: number; // [1], [2], etc.
  paperId: string; // References Paper.id
  relevanceScore?: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  papers?: Paper[]; // Papers referenced in this message
  evalScores?: EvalScores;
  agentStatuses?: AgentStatus[]; // Agent workflow timeline
  timestamp: Date;
  isStreaming?: boolean;
}

export interface EvalScores {
  faithfulness?: number; // 0-1 (RAGAS - local corpus)
  answerRelevancy?: number; // 0-1 (RAGAS - local corpus)
  contextPrecision?: number; // 0-1 (RAGAS - local corpus)
  citationAccuracy?: number; // 0-1 (Manual rubric - live search)
  recencyScore?: number; // 0-1 (Manual rubric - live search)
  coverageScore?: number; // 0-1 (Manual rubric - live search)
  status: 'evaluating' | 'completed' | 'failed';
}

export interface AgentStatus {
  agent: 'search_s2' | 'search_arxiv' | 'search_local' | 'synthesize' | 'evaluate';
  status: 'pending' | 'active' | 'completed' | 'failed';
  timestamp?: Date;
  metadata?: Record<string, any>;
}
