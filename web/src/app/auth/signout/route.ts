import { NextResponse, type NextRequest } from "next/server";
import { createClient } from "@/lib/supabase/server";

// Sign out (clears the session cookies) then return to the referring page, or
// home. POST-only so a stray link/prefetch can't log a user out.
export async function POST(request: NextRequest) {
  const supabase = await createClient();
  if (supabase) await supabase.auth.signOut();

  const referer = request.headers.get("referer");
  const dest = referer && referer.startsWith(new URL(request.url).origin) ? referer : "/";
  return NextResponse.redirect(dest, { status: 303 });
}
