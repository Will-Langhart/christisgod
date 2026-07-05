import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { chapters, chapterBySlug } from "@/lib/chapters";
import { chapterExcerpt } from "@/lib/excerpt";
import { pathBySlug } from "@/lib/reading-paths";
import { bookMeta } from "@/lib/book-meta";
import { chapterGraph } from "@/lib/structured-data";
import { contentMTime } from "@/lib/content-mtime";
import { ChapterNav } from "@/components/chapter-nav";
import { OnThisPage } from "@/components/on-this-page";
import { ShareButton } from "@/components/share-button";

export function generateStaticParams() {
  return chapters.map((c) => ({ slug: c.slug }));
}

export const dynamicParams = false;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const chapter = chapterBySlug(slug);
  if (!chapter) return {};
  const title = chapter.numeral
    ? `${chapter.numeral}. ${chapter.title}`
    : chapter.title;
  const description = chapterExcerpt(slug, chapter.subtitle);
  const url = `/read/${slug}`;
  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      title,
      description,
      type: "article",
      url,
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
    },
  };
}

export default async function ChapterPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ path?: string }>;
}) {
  const { slug } = await params;
  const { path: pathSlug } = await searchParams;

  const chapter = chapterBySlug(slug);
  if (!chapter) notFound();

  const activePath = pathSlug ? pathBySlug(pathSlug) : null;

  const { default: Content } = await chapter.load();
  const description = chapterExcerpt(slug, chapter.subtitle);

  const jsonLd = chapterGraph({
    title: chapter.title,
    slug,
    description,
    modified: contentMTime(slug),
  });

  return (
    <div className="flex gap-10">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article className="min-w-0 flex-1 py-10 lg:py-14">
        <header className="mb-10">
          {activePath && (
            <p className="mb-3 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.2em] text-ink-faint">
              Reading:{" "}
              <span className="text-gold">{activePath.label}</span>
            </p>
          )}
          <div className="chapter-crest" aria-hidden>
            <span className="chapter-crest__mark">✠</span>
          </div>
          {chapter.numeral && (
            <p className="font-[family-name:var(--font-ui)] text-sm font-semibold uppercase tracking-[0.25em] text-gold">
              Chapter {chapter.numeral}
            </p>
          )}
          <h1 className="mt-2 font-[family-name:var(--font-display)] text-4xl font-semibold leading-tight text-ink sm:text-5xl">
            {chapter.title}
          </h1>
          {chapter.subtitle && (
            <p className="mt-3 font-[family-name:var(--font-serif)] text-xl italic text-ink-faint">
              {chapter.subtitle}
            </p>
          )}
          <div className="mt-6 flex items-center gap-4">
            <div className="h-px w-24 bg-gradient-to-r from-gold to-transparent" />
            <ShareButton title={`${chapter.title} · ${bookMeta.title}`} />
          </div>
        </header>

        <div className="prose chapter-body">
          <Content />
        </div>

        <div className="chapter-endmark" aria-hidden>
          ❧
        </div>

        <ChapterNav slug={chapter.slug} pathSlug={pathSlug} />
      </article>

      {/* On-this-page rail (wide screens) */}
      <aside className="hidden w-56 shrink-0 xl:block">
        <div className="sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto py-14">
          <OnThisPage />
        </div>
      </aside>
    </div>
  );
}
