import { chapterBySlug, type Chapter } from "@/lib/chapters";

export type ReadingPath = {
  slug: string;
  label: string;
  description: string;
  chapters: string[];
};

export const readingPaths: ReadingPath[] = [
  {
    slug: "compact-case",
    label: "The Short Case",
    description:
      "The essential argument in five chapters — start here if you're short on time.",
    chapters: [
      "i-introduction",
      "iii-romans-95",
      "iv-jesus-is-god",
      "xv-a-compact-apologetic-case",
      "xvi-conclusion",
    ],
  },
  {
    slug: "skeptic",
    label: "I'm a skeptic",
    description:
      "Philosophical and textual evidence for a reader who wants the strongest case.",
    chapters: [
      "ii-the-monotheistic-context",
      "iv-jesus-is-god",
      "x-the-holy-trinity",
      "xiv-anticipating-objections",
      "xvi-conclusion",
    ],
  },
  {
    slug: "different-faith",
    label: "Talking with a friend of a different faith",
    description:
      "Chapters that address the manuscript evidence and how Christ is viewed in other traditions.",
    chapters: [
      "ii-the-monotheistic-context",
      "iv-jesus-is-god",
      "xii-the-manuscript-and-textual-witness",
      "xiii-islams-view-of-christ",
      "xvi-conclusion",
    ],
  },
  {
    slug: "new-believer",
    label: "I'm a new Christian",
    description:
      "Build a firm foundation for understanding who Jesus is and why it matters.",
    chapters: [
      "i-introduction",
      "iv-jesus-is-god",
      "viii-worship-given-to-christ",
      "x-the-holy-trinity",
      "xvi-conclusion",
    ],
  },
];

export const pathBySlug = (slug: string): ReadingPath | undefined =>
  readingPaths.find((p) => p.slug === slug);

export const pathChapters = (path: ReadingPath): Chapter[] =>
  path.chapters.map((s) => chapterBySlug(s)).filter((c): c is Chapter => c != null);
