import { notFound } from "next/navigation";
import { readingPaths, pathBySlug } from "@/lib/reading-paths";
import { renderOgImage, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export function generateStaticParams() {
  return readingPaths.map((p) => ({ slug: p.slug }));
}

export const dynamicParams = false;

export const alt = "Christ Is God — Reading Path";

export default async function OgImage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const path = pathBySlug(slug);
  if (!path) notFound();

  return renderOgImage({
    eyebrow: "Reading Path",
    title: path.label,
    subtitle: path.description,
  });
}
