import type { MetadataRoute } from "next";
import { bookMeta } from "@/lib/book-meta";
import { site } from "@/lib/site";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: `${bookMeta.title} — ${bookMeta.subtitle}`,
    short_name: bookMeta.title,
    description: bookMeta.tagline,
    start_url: "/",
    display: "standalone",
    background_color: "#f7f1e6",
    theme_color: "#9a7b3f",
    categories: ["books", "education", "reference"],
    lang: "en",
    icons: [
      {
        src: site.logo,
        sizes: "any",
        type: "image/png",
        purpose: "any",
      },
    ],
  };
}
