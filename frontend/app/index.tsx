import { Redirect } from 'expo-router';

// Root index - redirect to auth or dashboard based on auth state
// For now, default to auth flow
export default function Index() {
  // TODO: Check auth state here (will add Supabase auth check)
  const isAuthenticated = false;

  if (isAuthenticated) {
    return <Redirect href="/(tabs)" />;
  }

  return <Redirect href="/(auth)/login" />;
}
