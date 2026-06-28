import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const CONTENT_DIR = join(process.cwd(), "src", "content");

// Cache resolved filenames so we only read the directory once per build.
let fileIndex: Map<string, string> | null = null;

function resolveFile(slug: string): string | null {
  if (!fileIndex) {
    fileIndex = new Map();
    for (const name of readdirSync(CONTENT_DIR)) {
      if (!name.endsWith(".mdx")) continue;
      // Files are named `NN-<slug>.mdx`; strip the numeric prefix.
      const stripped = name.replace(/^\d+-/, "").replace(/\.mdx$/, "");
      fileIndex.set(stripped, name);
    }
  }
  const file = fileIndex.get(slug);
  return file ? join(CONTENT_DIR, file) : null;
}

/**
 * Returns a clean, social-friendly excerpt (~chars) drawn from the chapter's
 * first substantive paragraph. Strips MDX/markdown syntax so previews read as
 * plain prose. Falls back to the provided subtitle when no prose is found.
 */
export function chapterExcerpt(
  slug: string,
  fallback?: string | null,
  maxLen = 200,
): string {
  const path = resolveFile(slug);
  if (!path) return fallback ?? "";

  const raw = readFileSync(path, "utf8");
  const firstParagraph = raw
    .split(/\n{2,}/)
    .map((block) => block.trim())
    .find((block) => {
      if (!block) return false;
      // Skip frontmatter, imports, headings, tables, blockquotes, JSX tags.
      if (block.startsWith("---")) return false;
      if (block.startsWith("import ") || block.startsWith("export ")) return false;
      if (/^[#>|]/.test(block)) return false;
      if (block.startsWith("<")) return false;
      return true;
    });

  if (!firstParagraph) return fallback ?? "";

  const clean = firstParagraph
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1") // links → text
    .replace(/[*_`]/g, "") // emphasis/code marks
    .replace(/\s+/g, " ")
    .trim();

  if (clean.length <= maxLen) return clean;
  const truncated = clean.slice(0, maxLen);
  const lastSpace = truncated.lastIndexOf(" ");
  return `${truncated.slice(0, lastSpace > 0 ? lastSpace : maxLen).trimEnd()}…`;
}
