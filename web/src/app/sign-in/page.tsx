import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { redirect } from "next/navigation";
import { AuthForm } from "@/components/auth/auth-form";
import { createClient } from "@/lib/supabase/server";
import { isSupabaseConfigured } from "@/lib/supabase/config";

export const metadata: Metadata = {
  title: "Sign in",
  description: "Sign in to save your notes, bookmarks, and conversations.",
  robots: { index: false },
};

export default async function SignInPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; error?: string }>;
}) {
  const { next: nextParam, error } = await searchParams;
  const next = nextParam && nextParam.startsWith("/") ? nextParam : "/";

  // Already signed in? Send them on.
  if (isSupabaseConfigured) {
    const supabase = await createClient();
    const { data } = (await supabase?.auth.getUser()) ?? { data: { user: null } };
    if (data?.user) redirect(next);
  }

  return (
    <main className="relative z-10 mx-auto flex min-h-dvh w-full max-w-md flex-col justify-center px-6 py-16">
      <Link href="/" className="mb-8 flex items-center gap-2.5 self-center text-ink">
        <Image
          src="/christisgod-logo.png"
          alt="Christ Is God"
          width={30}
          height={30}
          unoptimized
          className="h-[30px] w-auto"
        />
        <span className="font-[family-name:var(--font-display)] text-xl font-semibold tracking-tight">
          Christ Is God
        </span>
      </Link>

      <h1 className="mb-2 text-center font-[family-name:var(--font-display)] text-2xl font-semibold text-ink">
        Sign in
      </h1>
      <p className="mb-8 text-center font-[family-name:var(--font-ui)] text-sm text-ink-soft">
        Save your notes, bookmarks, and conversations across devices. Reading the
        book never requires an account.
      </p>

      {isSupabaseConfigured ? (
        <div className="flex justify-center">
          <AuthForm next={next} />
        </div>
      ) : (
        <p className="rounded-md border border-rule bg-surface px-4 py-3 text-center font-[family-name:var(--font-ui)] text-sm text-ink-soft">
          Accounts aren’t enabled yet. Check back soon.
        </p>
      )}

      {error === "auth" && (
        <p className="mt-4 text-center font-[family-name:var(--font-ui)] text-sm text-vermillion">
          Something went wrong finishing sign-in. Please try again.
        </p>
      )}

      <Link
        href="/"
        className="mt-10 self-center font-[family-name:var(--font-ui)] text-sm text-ink-faint hover:text-lapis"
      >
        ← Back to the book
      </Link>
    </main>
  );
}
