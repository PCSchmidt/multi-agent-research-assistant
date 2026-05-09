import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';

// TODO: Move to environment variables using expo-constants and app.config.js
const supabaseUrl = 'https://hdzhvpomcnnwfiirzykl.supabase.co';
const supabaseAnonKey = 'sb_publishable_SNlozH3Su-_BOiW5Mil1Mw_aIFwBHSJ';

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});
