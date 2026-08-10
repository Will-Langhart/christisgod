import { NextResponse, type NextRequest } from "next/server";
import { createClient } from "@/lib/supabase/server";

// OAuth + email-confirmation callback. Supabase redirects here with a `code`
// (PKCE) after Google/Microsoft sign-in or an emailed confirmation link. We
// exchange it for a session (cookies set via the server client) and redirect on.
//
// `next` lets a caller return the user to where they started; we validate it is
// a same-origin path to avoid an open-redirect.
export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const nextParam = searchParams.get("next") ?? "/";
  const next = nextParam.startsWith("/") ? nextParam : "/";

  if (code) {
    const supabase = await createClient();
    if (supabase) {
      const { error } = await supabase.auth.exchangeCodeForSession(code);
      if (!error) {
        // In production behind a proxy, honor the forwarded host so the redirect
        // lands on the public origin rather than the internal one.
        const forwardedHost = request.headers.get("x-forwarded-host");
        const isLocal = process.env.NODE_ENV === "development";
        if (isLocal) return NextResponse.redirect(`${origin}${next}`);
        if (forwardedHost) return NextResponse.redirect(`https://${forwardedHost}${next}`);
        return NextResponse.redirect(`${origin}${next}`);
      }
    }
  }

  return NextResponse.redirect(`${origin}/sign-in?error=auth`);
}
