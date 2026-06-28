import Link from "next/link";
import { ArrowLeft, ArrowRight, List } from "lucide-react";
import { chapters, chapterBySlug } from "@/lib/chapters";
import { pathBySlug, pathChapters } from "@/lib/reading-paths";

export function ChapterNav({
  slug,
  pathSlug,
}: {
  slug: string;
  pathSlug?: string;
}) {
  const activePath = pathSlug ? pathBySlug(pathSlug) : null;
  const list = activePath ? pathChapters(activePath) : chapters;

  const idx = list.findIndex((c) => c.slug === slug);
  const prev = idx > 0 ? list[idx - 1] : null;
  const next = idx < list.length - 1 ? list[idx + 1] : null;

  const href = (c: { slug: string }) =>
    pathSlug ? `/read/${c.slug}?path=${pathSlug}` : `/read/${c.slug}`;

  return (
    <div className="mt-16 border-t border-rule pt-8">
      {activePath && (
        <div className="mb-6">
          <Link
            href={`/path/${pathSlug}`}
            className="group inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-sm uppercase tracking-wide text-ink-faint transition hover:text-gold"
          >
            <List className="h-3.5 w-3.5" />
            <span>
              Path:{" "}
              <span className="text-gold group-hover:underline">
                {activePath.label}
              </span>
            </span>
          </Link>
        </div>
      )}

      <nav className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {prev ? (
          <Link
            href={href(prev)}
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
            href={href(next)}
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
    </div>
  );
}
