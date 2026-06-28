import { chapters, chapterBySlug } from "@/lib/chapters";
import { OG_SIZE, OG_CONTENT_TYPE, renderOgImage } from "@/lib/og";

export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export function generateStaticParams() {
  return chapters.map((c) => ({ slug: c.slug }));
}

export const dynamicParams = false;

export const alt = "Christ Is God — The Divinity of Christ";

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const chapter = chapterBySlug(slug);
  return renderOgImage({
    eyebrow: chapter?.numeral ? `Chapter ${chapter.numeral}` : undefined,
    title: chapter?.title ?? "Christ Is God",
    subtitle: chapter?.subtitle ?? undefined,
  });
}
