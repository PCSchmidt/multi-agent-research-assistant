/**
 * API client for user API key management (BYOK).
 */

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

export type Provider = 'anthropic' | 'openai' | 'openrouter';

export interface APIKeyResponse {
  id: string;
  user_id: string;
  provider: Provider;
  created_at: string;
  updated_at: string;
}

export interface APIKeyTestResponse {
  success: boolean;
  provider: Provider;
  error?: string;
}

/**
 * Save or update an API key for a provider.
 */
export async function saveAPIKey(provider: Provider, apiKey: string): Promise<APIKeyResponse> {
  const response = await fetch(`${API_BASE_URL}/api/keys`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      provider,
      api_key: apiKey,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to save API key');
  }

  return response.json();
}

/**
 * List all API keys for the current user (returns metadata only, not actual keys).
 */
export async function listAPIKeys(): Promise<APIKeyResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/keys`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to list API keys');
  }

  return response.json();
}

/**
 * Delete an API key for a provider.
 */
export async function deleteAPIKey(provider: Provider): Promise<{ message: string; provider: Provider }> {
  const response = await fetch(`${API_BASE_URL}/api/keys/${provider}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete API key');
  }

  return response.json();
}

/**
 * Test an API key connection.
 */
export async function testAPIKey(provider: Provider): Promise<APIKeyTestResponse> {
  const response = await fetch(`${API_BASE_URL}/api/keys/${provider}/test`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to test API key');
  }

  return response.json();
}
