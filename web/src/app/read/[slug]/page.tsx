import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { chapters, chapterBySlug } from "@/lib/chapters";
import { ChapterNav } from "@/components/chapter-nav";
import { OnThisPage } from "@/components/on-this-page";

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
  return {
    title,
    description: chapter.subtitle ?? undefined,
  };
}

export default async function ChapterPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const chapter = chapterBySlug(slug);
  if (!chapter) notFound();

  const { default: Content } = await chapter.load();

  return (
    <div className="flex gap-10">
      <article className="min-w-0 flex-1 py-10 lg:py-14">
        <header className="mb-10">
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
          <div className="mt-6 h-px w-24 bg-gold" />
        </header>

        <div className="prose chapter-body">
          <Content />
        </div>

        <ChapterNav slug={chapter.slug} />
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
