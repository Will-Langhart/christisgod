// Next 16 Proxy (formerly Middleware). Refreshes the Supabase auth session
// cookie on navigation so server components see a fresh user. No-op until
// Supabase is configured (see src/lib/supabase/config.ts).

import type { NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/proxy";

export async function proxy(request: NextRequest) {
  return updateSession(request);
}

export const config = {
  // Run on everything except static assets and image files, so auth cookies
  // refresh on real navigations without touching CSS/JS/images.
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico|ttf|woff2?)$).*)",
  ],
};
