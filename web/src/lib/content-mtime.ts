// Last-modified times for chapter MDX sources, used for sitemap <lastmod> and
// Article dateModified. Content filenames are prefixed with an order number
// (e.g. "00-i-introduction.mdx"), so we match a chapter slug on the suffix.
//
// Note: this reads filesystem mtime. Locally that reflects real edit times; in
// a fresh CI/Vercel checkout it reflects build time, which is still a valid
// (if conservative) freshness signal.
import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { chapters } from "@/lib/chapters";

const CONTENT_DIR = join(process.cwd(), "src", "content");

function mdxFiles(): string[] {
  try {
    return readdirSync(CONTENT_DIR).filter((f) => f.endsWith(".mdx"));
  } catch {
    return [];
  }
}

function mtimeOf(file: string): Date | undefined {
  try {
    return statSync(join(CONTENT_DIR, file)).mtime;
  } catch {
    return undefined;
  }
}

/** mtime of a single chapter's MDX source, or undefined if not found. */
export function contentMTime(slug: string): Date | undefined {
  const file = mdxFiles().find((f) => f.endsWith(`-${slug}.mdx`));
  return file ? mtimeOf(file) : undefined;
}

/** mtime for every chapter slug that has a matching MDX source. */
export function contentMTimes(): Map<string, Date> {
  const files = mdxFiles();
  const map = new Map<string, Date>();
  for (const c of chapters) {
    const file = files.find((f) => f.endsWith(`-${c.slug}.mdx`));
    const mtime = file ? mtimeOf(file) : undefined;
    if (mtime) map.set(c.slug, mtime);
  }
  return map;
}
