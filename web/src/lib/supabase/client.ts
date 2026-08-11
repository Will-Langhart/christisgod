"use client";

// Browser-side Supabase client (client components). Reads the session from
// cookies written by the server client + proxy, so auth state is shared across
// the SSR boundary. Returns null when Supabase is unconfigured so callers can
// stay dormant rather than crash.

import { createBrowserClient } from "@supabase/ssr";
import { SUPABASE_ANON_KEY, SUPABASE_URL, isSupabaseConfigured } from "./config";

export function createClient() {
  if (!isSupabaseConfigured) return null;
  return createBrowserClient(SUPABASE_URL!, SUPABASE_ANON_KEY!);
}
