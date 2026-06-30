import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, ArrowLeft, BookOpen } from "lucide-react";
import { readingPaths, pathBySlug, pathChapters } from "@/lib/reading-paths";
import { bookMeta } from "@/lib/book-meta";
import { site } from "@/lib/site";

export function generateStaticParams() {
  return readingPaths.map((p) => ({ slug: p.slug }));
}

export const dynamicParams = false;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const path = pathBySlug(slug);
  if (!path) return {};
  const url = `/path/${slug}`;
  return {
    title: `${path.label} · ${bookMeta.title}`,
    description: path.description,
    alternates: { canonical: url },
    openGraph: { title: path.label, description: path.description, type: "website", url },
    twitter: { card: "summary_large_image", title: path.label, description: path.description },
  };
}

export default async function PathPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const path = pathBySlug(slug);
  if (!path) notFound();

  const chapters = pathChapters(path);
  const first = chapters[0];

  return (
    <div className="flex min-h-full flex-col">
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-20">
        {/* Back link */}
        <Link
          href="/"
          className="group mb-12 inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-sm uppercase tracking-wide text-ink-faint transition hover:text-gold"
        >
          <ArrowLeft className="h-3.5 w-3.5 transition group-hover:-translate-x-0.5" />
          All paths
        </Link>

        {/* Header */}
        <header className="mb-14">
          <p className="font-[family-name:var(--font-ui)] text-sm font-semibold uppercase tracking-[0.25em] text-gold">
            Reading Path · {chapters.length} chapters
          </p>
          <h1 className="mt-3 font-[family-name:var(--font-display)] text-4xl font-semibold leading-tight text-ink sm:text-5xl">
            {path.label}
          </h1>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-xl italic text-ink-faint">
            {path.description}
          </p>
          <div className="mt-8 h-px w-24 bg-gold" />
        </header>

        {/* Chapter list */}
        <ol className="mb-14 space-y-2">
          {chapters.map((c, i) => (
            <li key={c.slug}>
              <Link
                href={`/read/${c.slug}?path=${slug}`}
                className="group flex items-baseline gap-4 rounded-lg px-4 py-3 transition hover:bg-parchment-deep/60"
              >
                <span className="w-6 shrink-0 text-right font-[family-name:var(--font-ui)] text-sm tabular-nums text-gold">
                  {i + 1}
                </span>
                <span className="min-w-0">
                  <span className="font-[family-name:var(--font-display)] text-xl text-ink group-hover:text-gold">
                    {c.title}
                  </span>
                  {c.subtitle && (
                    <span className="block font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
                      {c.subtitle}
                    </span>
                  )}
                </span>
                <ArrowRight className="ml-auto mt-1 h-4 w-4 shrink-0 self-center text-rule-strong opacity-0 transition group-hover:opacity-100 group-hover:text-gold" />
              </Link>
            </li>
          ))}
        </ol>

        {/* CTA */}
        {first && (
          <Link
            href={`/read/${first.slug}?path=${slug}`}
            className="inline-flex items-center gap-2 rounded-lg border border-gold bg-gold/10 px-6 py-3 font-[family-name:var(--font-ui)] text-sm font-semibold uppercase tracking-wide text-gold transition hover:bg-gold/20"
          >
            <BookOpen className="h-4 w-4" />
            Start reading
          </Link>
        )}
      </main>

      <footer className="border-t border-rule px-6 py-10 text-center font-[family-name:var(--font-ui)] text-sm text-ink-faint">
        <p>
          {bookMeta.title} — {bookMeta.subtitle} · {bookMeta.year}
        </p>
      </footer>
    </div>
  );
}
