import type { MetadataRoute } from "next";
import { site } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // Everything is public and indexable. Disallow the dynamically
      // generated OG image routes — they are only meant to be fetched by
      // social/crawler unfurlers via <meta>, not indexed as standalone pages.
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/*/opengraph-image", "/opengraph-image"],
      },
    ],
    sitemap: `${site.url}/sitemap.xml`,
    host: site.url,
  };
}
