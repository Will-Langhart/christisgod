import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { chapters } from "@/lib/chapters";

export function ChapterNav({ slug }: { slug: string }) {
  const idx = chapters.findIndex((c) => c.slug === slug);
  const prev = idx > 0 ? chapters[idx - 1] : null;
  const next = idx < chapters.length - 1 ? chapters[idx + 1] : null;

  return (
    <nav className="mt-16 grid grid-cols-1 gap-3 border-t border-rule pt-8 sm:grid-cols-2">
      {prev ? (
        <Link
          href={`/read/${prev.slug}`}
          className="group flex flex-col gap-1 rounded-lg border border-rule p-4 transition hover:border-gold"
        >
          <span className="flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs uppercase tracking-wide text-ink-faint">
            <ArrowLeft className="h-3.5 w-3.5" /> Previous
          </span>
          <span className="font-[family-name:var(--font-display)] text-lg text-ink group-hover:text-gold">
            {prev.numeral ? `${prev.numeral}. ` : ""}
            {prev.title}
          </span>
        </Link>
      ) : (
        <span />
      )}
      {next ? (
        <Link
          href={`/read/${next.slug}`}
          className="group flex flex-col gap-1 rounded-lg border border-rule p-4 text-right transition hover:border-gold sm:items-end"
        >
          <span className="flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs uppercase tracking-wide text-ink-faint">
            Next <ArrowRight className="h-3.5 w-3.5" />
          </span>
          <span className="font-[family-name:var(--font-display)] text-lg text-ink group-hover:text-gold">
            {next.numeral ? `${next.numeral}. ` : ""}
            {next.title}
          </span>
        </Link>
      ) : (
        <span />
      )}
    </nav>
  );
}
