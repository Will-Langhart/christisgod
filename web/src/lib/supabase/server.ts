import "server-only";

// Server-side Supabase client (server components, route handlers). Uses Next 16's
// async `cookies()` and the getAll/setAll cookie contract required by
// @supabase/ssr. Returns null when Supabase is unconfigured.
//
// Note: setAll throws inside a Server Component render (cookies are read-only
// there); that's expected and harmless — the session is refreshed in proxy.ts,
// so we swallow it. In Route Handlers / Server Actions, setAll works normally.

import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";
import { SUPABASE_ANON_KEY, SUPABASE_URL, isSupabaseConfigured } from "./config";

export async function createClient() {
  if (!isSupabaseConfigured) return null;

  const cookieStore = await cookies();

  return createServerClient(SUPABASE_URL!, SUPABASE_ANON_KEY!, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          for (const { name, value, options } of cookiesToSet) {
            cookieStore.set(name, value, options);
          }
        } catch {
          // Called from a Server Component — safe to ignore; proxy.ts refreshes.
        }
      },
    },
  });
}
