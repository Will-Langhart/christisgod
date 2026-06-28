import { bookMeta } from "@/lib/book-meta";
import { OG_SIZE, OG_CONTENT_TYPE, renderOgImage } from "@/lib/og";

export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;
export const alt = `${bookMeta.title} — ${bookMeta.subtitle}`;

export default function Image() {
  return renderOgImage({
    title: bookMeta.title,
    subtitle: bookMeta.tagline,
  });
}
