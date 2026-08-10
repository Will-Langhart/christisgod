"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LogOut, User as UserIcon } from "lucide-react";
import type { User } from "@supabase/supabase-js";
import { createClient } from "@/lib/supabase/client";

// Header account control. Reads auth state from the browser Supabase client and
// keeps it live via onAuthStateChange. Renders nothing when Supabase is
// unconfigured, so the header is unchanged until accounts are enabled.
export function AccountMenu() {
  // Create the browser client once. Null when Supabase is unconfigured.
  const [supabase] = useState(() => createClient());
  const [ready, setReady] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    if (!supabase) return;
    let active = true;
    supabase.auth.getUser().then(({ data }) => {
      if (!active) return;
      setUser(data.user);
      setReady(true);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_e, session) => {
      setUser(session?.user ?? null);
    });
    return () => {
      active = false;
      sub.subscription.unsubscribe();
    };
  }, [supabase]);

  // Unconfigured, or still resolving: render nothing (no layout flash).
  if (!supabase || !ready) return null;

  if (!user) {
    const next = pathname && pathname.startsWith("/") ? pathname : "/";
    return (
      <Link
        href={`/sign-in?next=${encodeURIComponent(next)}`}
        className="font-[family-name:var(--font-ui)] text-sm font-medium text-ink-soft transition hover:text-lapis"
      >
        Sign in
      </Link>
    );
  }

  const label = displayName(user);

  return (
    <div className="flex items-center gap-3">
      <span
        className="flex max-w-[10rem] items-center gap-1.5 truncate font-[family-name:var(--font-ui)] text-sm text-ink-soft"
        title={user.email ?? label}
      >
        <UserIcon className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />
        <span className="truncate">{label}</span>
      </span>
      <form action="/auth/signout" method="post">
        <button
          type="submit"
          aria-label="Sign out"
          className="inline-flex h-8 w-8 items-center justify-center rounded-md text-ink-faint transition hover:text-vermillion"
        >
          <LogOut className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}

function displayName(user: User): string {
  const meta = user.user_metadata ?? {};
  return (
    (meta.full_name as string) ||
    (meta.name as string) ||
    (user.email ? user.email.split("@")[0] : "Account")
  );
}
