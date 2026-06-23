"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { chapters } from "@/lib/chapters";
import { clsx } from "clsx";

export function ChapterList({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();

  return (
    <nav aria-label="Table of contents" className="font-[family-name:var(--font-ui)]">
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-ink-faint">
        Contents
      </p>
      <ol className="space-y-0.5">
        {chapters.map((c) => {
          const href = `/read/${c.slug}`;
          const active = pathname === href;
          return (
            <li key={c.slug}>
              <Link
                href={href}
                onClick={onNavigate}
                className={clsx(
                  "group flex gap-2.5 rounded-md px-2.5 py-1.5 text-[0.9rem] leading-snug transition",
                  active
                    ? "bg-parchment-deep text-ink"
                    : "text-ink-soft hover:bg-parchment-deep/60 hover:text-ink",
                )}
              >
                <span
                  className={clsx(
                    "mt-px w-7 shrink-0 text-right text-xs tabular-nums",
                    active ? "text-gold" : "text-ink-faint group-hover:text-gold",
                  )}
                >
                  {c.numeral ?? "✦"}
                </span>
                <span className={clsx(active && "font-semibold")}>{c.title}</span>
              </Link>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
