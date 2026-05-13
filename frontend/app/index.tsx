import { Redirect } from 'expo-router';

// Root index - redirect to auth or dashboard based on auth state
// For now, default to auth flow
export default function Index() {
  // TODO: Check auth state here (will add Supabase auth check in v0.12)
  const isAuthenticated = true; // v0.10: Bypass auth for testing

  if (isAuthenticated) {
    return <Redirect href="/(tabs)" />;
  }

  return <Redirect href="/(auth)/login" />;
}
