"use client";

import { useState } from "react";
import { Loader2, Mail, Lock } from "lucide-react";
import { createClient } from "@/lib/supabase/client";

type Mode = "signin" | "signup";
type OAuthProvider = "google" | "azure";

// Sign-in surface: Google + Microsoft OAuth, plus email/password (sign in or
// create an account). A single client component so it can drive the Supabase
// browser client directly. Dormant if Supabase is unconfigured (the page guards
// that, but we double-check here).
export function AuthForm({ next = "/" }: { next?: string }) {
  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState<"" | OAuthProvider | "email">("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const redirectTo =
    typeof window !== "undefined"
      ? `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`
      : undefined;

  async function withOAuth(provider: OAuthProvider) {
    const supabase = createClient();
    if (!supabase || busy) return;
    setBusy(provider);
    setError("");
    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: { redirectTo },
    });
    if (error) {
      setError(error.message);
      setBusy("");
    }
    // On success the browser is redirected to the provider; no further UI here.
  }

  async function withEmail(e: React.FormEvent) {
    e.preventDefault();
    const supabase = createClient();
    if (!supabase || busy) return;
    setBusy("email");
    setError("");
    setNotice("");

    if (mode === "signup") {
      const { error } = await supabase.auth.signUp({
        email,
        password,
        options: { emailRedirectTo: redirectTo },
      });
      if (error) setError(error.message);
      else setNotice("Check your email to confirm your account, then sign in.");
      setBusy("");
      return;
    }

    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError(error.message);
      setBusy("");
      return;
    }
    // Signed in — go where the user intended.
    window.location.assign(next);
  }

  return (
    <div className="w-full max-w-sm">
      {/* OAuth */}
      <div className="flex flex-col gap-3">
        <ProviderButton
          label="Continue with Google"
          onClick={() => withOAuth("google")}
          loading={busy === "google"}
          disabled={!!busy}
          icon={<GoogleIcon />}
        />
        <ProviderButton
          label="Continue with Microsoft"
          onClick={() => withOAuth("azure")}
          loading={busy === "azure"}
          disabled={!!busy}
          icon={<MicrosoftIcon />}
        />
      </div>

      <div className="my-6 flex items-center gap-3 text-ink-faint">
        <span className="h-px flex-1 bg-rule" />
        <span className="font-[family-name:var(--font-ui)] text-xs uppercase tracking-wider">
          or
        </span>
        <span className="h-px flex-1 bg-rule" />
      </div>

      {/* Email / password */}
      <form onSubmit={withEmail} className="flex flex-col gap-3">
        <label className="flex items-center gap-2 rounded-md border border-rule bg-surface px-3 py-2 focus-within:border-lapis">
          <Mail className="h-4 w-4 text-ink-faint" aria-hidden />
          <input
            type="email"
            required
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-transparent font-[family-name:var(--font-ui)] text-sm text-ink outline-none placeholder:text-ink-faint"
          />
        </label>
        <label className="flex items-center gap-2 rounded-md border border-rule bg-surface px-3 py-2 focus-within:border-lapis">
          <Lock className="h-4 w-4 text-ink-faint" aria-hidden />
          <input
            type="password"
            required
            minLength={8}
            autoComplete={mode === "signup" ? "new-password" : "current-password"}
            placeholder={mode === "signup" ? "Create a password (8+ chars)" : "Your password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-transparent font-[family-name:var(--font-ui)] text-sm text-ink outline-none placeholder:text-ink-faint"
          />
        </label>

        <button
          type="submit"
          disabled={!!busy}
          className="mt-1 inline-flex items-center justify-center gap-2 rounded-md bg-lapis px-4 py-2.5 font-[family-name:var(--font-ui)] text-sm font-medium text-parchment transition hover:bg-lapis-bright disabled:opacity-60"
        >
          {busy === "email" && <Loader2 className="h-4 w-4 animate-spin" aria-hidden />}
          {mode === "signup" ? "Create account" : "Sign in"}
        </button>
      </form>

      {error && (
        <p className="mt-4 font-[family-name:var(--font-ui)] text-sm text-vermillion">{error}</p>
      )}
      {notice && (
        <p className="mt-4 font-[family-name:var(--font-ui)] text-sm text-ink-soft">{notice}</p>
      )}

      <p className="mt-6 text-center font-[family-name:var(--font-ui)] text-sm text-ink-soft">
        {mode === "signin" ? "New here?" : "Already have an account?"}{" "}
        <button
          type="button"
          onClick={() => {
            setMode(mode === "signin" ? "signup" : "signin");
            setError("");
            setNotice("");
          }}
          className="font-medium text-lapis underline-offset-2 hover:underline"
        >
          {mode === "signin" ? "Create an account" : "Sign in"}
        </button>
      </p>
    </div>
  );
}

function ProviderButton({
  label,
  onClick,
  loading,
  disabled,
  icon,
}: {
  label: string;
  onClick: () => void;
  loading: boolean;
  disabled: boolean;
  icon: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="inline-flex items-center justify-center gap-3 rounded-md border border-rule-strong bg-surface px-4 py-2.5 font-[family-name:var(--font-ui)] text-sm font-medium text-ink transition hover:border-gold hover:bg-parchment disabled:opacity-60"
    >
      {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : icon}
      {label}
    </button>
  );
}

function GoogleIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" aria-hidden>
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1A11 11 0 0 0 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z"
      />
    </svg>
  );
}

function MicrosoftIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" aria-hidden>
      <path fill="#F25022" d="M2 2h9.5v9.5H2z" />
      <path fill="#7FBA00" d="M12.5 2H22v9.5h-9.5z" />
      <path fill="#00A4EF" d="M2 12.5h9.5V22H2z" />
      <path fill="#FFB900" d="M12.5 12.5H22V22h-9.5z" />
    </svg>
  );
}
