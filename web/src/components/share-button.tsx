"use client";

import { useState } from "react";
import { Check, Share2 } from "lucide-react";

export function ShareButton({ title }: { title: string }) {
  const [copied, setCopied] = useState(false);

  async function handleShare() {
    const url = typeof window !== "undefined" ? window.location.href : "";
    // Prefer the native share sheet on supporting devices (mobile, Safari).
    if (typeof navigator !== "undefined" && navigator.share) {
      try {
        await navigator.share({ title, url });
        return;
      } catch {
        // User dismissed the sheet — fall through to clipboard copy.
      }
    }
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard blocked — nothing graceful left to do.
    }
  }

  return (
    <button
      type="button"
      onClick={handleShare}
      aria-label="Share this chapter"
      className="inline-flex items-center gap-1.5 rounded-full border border-rule px-3 py-1 font-[family-name:var(--font-ui)] text-xs uppercase tracking-widest text-ink-faint transition hover:border-gold hover:text-gold"
    >
      {copied ? (
        <>
          <Check className="h-3.5 w-3.5" />
          Link copied
        </>
      ) : (
        <>
          <Share2 className="h-3.5 w-3.5" />
          Share
        </>
      )}
    </button>
  );
}
