"use client";

import * as HoverCard from "@radix-ui/react-hover-card";
import { BookOpen, ExternalLink } from "lucide-react";
import { parseRef, lookupVerse } from "@/lib/scripture";

/**
 * Renders an inline scripture reference. On hover/focus it reveals a card with
 * the KJV text (when bundled) and a link to read the full passage.
 *
 * Used as the `a.scripture-ref` mapping from MDX — the rehype plugin tags refs
 * with `class="scripture-ref"` and `data-ref="<reference>"`.
 */
export function ScriptureRef({
  dataRef,
  children,
}: {
  dataRef?: string;
  children?: React.ReactNode;
}) {
  const parsed = dataRef ? parseRef(dataRef) : null;

  if (!parsed) {
    return <span className="scripture-ref">{children}</span>;
  }

  // Try the exact reference, then fall back to the primary verse.
  const primary = `${parsed.book} ${parsed.rest.split(/[,;]/)[0].trim()}`;
  const text = lookupVerse(parsed.display) ?? lookupVerse(primary);

  return (
    <HoverCard.Root openDelay={120} closeDelay={80}>
      <HoverCard.Trigger asChild>
        <a
          href={parsed.bibleGatewayUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="scripture-ref"
        >
          {children}
        </a>
      </HoverCard.Trigger>
      <HoverCard.Portal>
        <HoverCard.Content
          side="top"
          align="center"
          sideOffset={6}
          collisionPadding={12}
          className="z-50 w-[min(22rem,calc(100vw-1.5rem))] rounded-lg border border-rule-strong bg-surface p-4 shadow-xl shadow-black/10 outline-none"
        >
          <div className="mb-1.5 flex items-center gap-1.5 font-[family-name:var(--font-display)] text-base font-semibold text-gold">
            <BookOpen className="h-4 w-4" />
            {parsed.display}
          </div>
          {text ? (
            <p className="font-[family-name:var(--font-serif)] text-[0.98rem] leading-relaxed text-ink-soft">
              &ldquo;{text}&rdquo;
              <span className="ml-1 text-xs uppercase tracking-wide text-ink-faint">
                (KJV)
              </span>
            </p>
          ) : (
            <p className="text-sm text-ink-faint">
              Read the full passage in context.
            </p>
          )}
          <a
            href={parsed.bibleGatewayUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-2.5 inline-flex items-center gap-1 font-[family-name:var(--font-ui)] text-xs font-medium text-gold hover:underline"
          >
            Open on BibleGateway <ExternalLink className="h-3 w-3" />
          </a>
          <HoverCard.Arrow className="fill-[var(--rule-strong)]" />
        </HoverCard.Content>
      </HoverCard.Portal>
    </HoverCard.Root>
  );
}
