"use client";

import { useEffect, useState } from "react";
import { clsx } from "clsx";

type Item = { id: string; text: string; level: number };

export function OnThisPage() {
  const [items, setItems] = useState<Item[]>([]);
  const [active, setActive] = useState<string>("");

  useEffect(() => {
    const headings = Array.from(
      document.querySelectorAll<HTMLElement>(".chapter-body h2[id], .chapter-body h3[id]"),
    );
    setItems(
      headings.map((h) => ({
        id: h.id,
        text: h.textContent?.replace(/#$/, "").trim() ?? "",
        level: h.tagName === "H2" ? 2 : 3,
      })),
    );

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) setActive(visible[0].target.id);
      },
      { rootMargin: "-90px 0px -65% 0px", threshold: 0 },
    );
    headings.forEach((h) => observer.observe(h));
    return () => observer.disconnect();
  }, []);

  if (items.length === 0) return null;

  return (
    <nav
      aria-label="On this page"
      className="font-[family-name:var(--font-ui)] text-sm"
    >
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-ink-faint">
        On this page
      </p>
      <ul className="space-y-1 border-l border-rule">
        {items.map((it) => (
          <li key={it.id}>
            <a
              href={`#${it.id}`}
              className={clsx(
                "-ml-px block border-l-2 py-1 leading-snug transition",
                it.level === 3 ? "pl-6" : "pl-4",
                active === it.id
                  ? "border-gold font-medium text-ink"
                  : "border-transparent text-ink-faint hover:text-ink",
              )}
            >
              {it.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
