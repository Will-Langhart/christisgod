import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";
import { SUPABASE_ANON_KEY, SUPABASE_URL, isSupabaseConfigured } from "./config";

// Refresh the Supabase session on each matched request and mirror the refreshed
// auth cookies onto both the request (for downstream server components) and the
// response (so the browser stores them). This is the documented @supabase/ssr
// pattern, ported to Next 16's `proxy` convention (formerly `middleware`).
//
// Dormant when Supabase is unconfigured: returns an untouched NextResponse so
// the site behaves exactly as before accounts existed.
export async function updateSession(request: NextRequest): Promise<NextResponse> {
  let response = NextResponse.next({ request });

  if (!isSupabaseConfigured) return response;

  const supabase = createServerClient(SUPABASE_URL!, SUPABASE_ANON_KEY!, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet) {
        for (const { name, value } of cookiesToSet) {
          request.cookies.set(name, value);
        }
        response = NextResponse.next({ request });
        for (const { name, value, options } of cookiesToSet) {
          response.cookies.set(name, value, options);
        }
      },
    },
  });

  // IMPORTANT: getClaims()/getUser() must be called to trigger a token refresh.
  // Do not run logic between client creation and this call.
  await supabase.auth.getClaims();

  return response;
}
