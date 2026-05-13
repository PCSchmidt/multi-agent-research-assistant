/**
 * API client for backend communication
 * Handles SSE streaming for research queries
 */

// API base URL - update for your environment
// @ts-ignore - Expo provides process.env at build time
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

// Partial paper data received during SSE streaming
// Full paper type is in types/research.ts
export interface StreamedPaper {
  title: string;
  authors: string[];
  year?: number;
  source: string;
}

export interface StreamEvent {
  type: 'status' | 'paper' | 'synthesis' | 'done' | 'error';
  data: any;
}

export interface StreamCallbacks {
  onStatus?: (message: string) => void;
  onPaper?: (paper: StreamedPaper) => void;
  onSynthesis?: (content: string) => void;
  onDone?: (result: { session_id: string; papers_count: number; synthesis: string }) => void;
  onError?: (error: string) => void;
}

/**
 * Stream a research query via SSE
 *
 * @param query - Research question
 * @param callbacks - Event callbacks for different stream events
 * @returns Promise that resolves when stream completes
 */
export async function streamResearchQuery(
  query: string,
  callbacks: StreamCallbacks
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/research/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('ReadableStream not supported');
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      // Decode chunk and add to buffer
      buffer += decoder.decode(value, { stream: true });

      // Process complete events (separated by \n\n)
      const events = buffer.split('\n\n');
      buffer = events.pop() || ''; // Keep incomplete event in buffer

      for (const eventText of events) {
        if (!eventText.trim()) continue;

        // Parse SSE event
        const lines = eventText.split('\n');
        let eventType = '';
        let eventData = '';

        for (const line of lines) {
          if (line.startsWith('event:')) {
            eventType = line.substring(6).trim();
          } else if (line.startsWith('data:')) {
            eventData = line.substring(5).trim();
          }
        }

        if (!eventType || !eventData) continue;

        // Parse JSON data
        try {
          const data = JSON.parse(eventData);

          // Route to appropriate callback
          switch (eventType) {
            case 'status':
              callbacks.onStatus?.(data.message);
              break;
            case 'paper':
              callbacks.onPaper?.(data);
              break;
            case 'synthesis':
              callbacks.onSynthesis?.(data.content);
              break;
            case 'done':
              callbacks.onDone?.(data);
              break;
            case 'error':
              callbacks.onError?.(data.message);
              break;
          }
        } catch (e) {
          console.error('Failed to parse SSE event data:', e);
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

/**
 * Submit a research query (non-streaming)
 * @deprecated Use streamResearchQuery for better UX
 */
export async function submitResearchQuery(query: string): Promise<{
  session_id: string;
  status: string;
  message: string;
}> {
  const response = await fetch(`${API_BASE_URL}/api/research/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}
