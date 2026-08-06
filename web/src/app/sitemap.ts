import type { MetadataRoute } from "next";
import { chapters } from "@/lib/chapters";
import { contentMTimes } from "@/lib/content-mtime";
import { readingPaths } from "@/lib/reading-paths";
import { site } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  const mtimes = contentMTimes();
  const newest = [...mtimes.values()].reduce(
    (acc, d) => (d > acc ? d : acc),
    new Date(0),
  );
  const lastModified = newest.getTime() > 0 ? newest : new Date();

  const home = {
    url: site.url,
    lastModified,
    changeFrequency: "monthly" as const,
    priority: 1,
  };

  const chapterUrls = chapters.map((c) => ({
    url: `${site.url}/read/${c.slug}`,
    lastModified: mtimes.get(c.slug) ?? lastModified,
    changeFrequency: "monthly" as const,
    priority: 0.8,
  }));

  const pathUrls = readingPaths.map((p) => ({
    url: `${site.url}/path/${p.slug}`,
    lastModified,
    changeFrequency: "monthly" as const,
    priority: 0.6,
  }));

  const featuredUrls = ["case", "dialogues", "history", "parallels"].map((slug) => ({
    url: `${site.url}/${slug}`,
    lastModified,
    changeFrequency: "monthly" as const,
    priority: 0.9,
  }));

  return [home, ...featuredUrls, ...chapterUrls, ...pathUrls];
}
