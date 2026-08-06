import type { ReactNode } from "react";
import { ScriptureRef } from "@/components/scripture-ref";
import { parseRef } from "@/lib/scripture";

// Plain-text counterpart to the MDX rehype plugin (rehype-scripture.mjs): finds
// scripture references inside a string and wraps them in the same ScriptureRef
// hover-card used across the book. Used for the dialogue answers, which are plain
// strings rather than MDX. Book-form list kept in sync with the rehype plugin.
const BOOK_FORMS = [
  "Deuteronomy", "Ecclesiastes", "Thessalonians", "Lamentations",
  "Philippians", "Corinthians", "Colossians", "Revelation", "Zechariah",
  "Zephaniah", "Ephesians", "Galatians", "Habakkuk", "Proverbs", "Jeremiah",
  "Nehemiah", "Hebrews", "Genesis", "Exodus", "Numbers", "Joshua", "Judges",
  "Malachi", "Matthew", "Timothy", "Obadiah", "Chronicles", "Leviticus",
  "Isaiah", "Daniel", "Hosea", "Romans", "Samuel", "Psalms", "Psalm",
  "Haggai", "Micah", "Nahum", "Esther", "Philemon", "Titus", "James",
  "Peter", "Jonah", "Joel", "Amos", "Ruth", "Mark", "Luke", "John", "Acts",
  "Jude", "Kings", "Job", "Song",
  "Matt", "Phil", "Col", "Rom", "Cor", "Gal", "Eph", "Heb", "Deut", "Exod",
  "Lev", "Num", "Josh", "Judg", "Prov", "Eccl", "Isa", "Jer", "Ezek", "Dan",
  "Hos", "Mic", "Zech", "Mal", "Ps", "Psa", "Tim", "Pet", "Thess", "Jas",
  "Rev", "Gen", "Chron",
].sort((a, b) => b.length - a.length);

const REF_SOURCE =
  `(?:[1-3]\\s)?(?:${BOOK_FORMS.join("|")})\\.?\\s+\\d+:\\d+(?:[\\u2013-]\\d+)?(?:,\\s?\\d+(?:[\\u2013-]\\d+)?)*`;

export function linkifyScripture(text: string): ReactNode[] {
  const re = new RegExp(REF_SOURCE, "g");
  const out: ReactNode[] = [];
  let last = 0;
  let key = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    const matched = m[0];
    if (!parseRef(matched)) continue; // reject patristic look-alikes / bad chapters
    if (m.index > last) out.push(text.slice(last, m.index));
    out.push(
      <ScriptureRef key={key++} dataRef={matched}>
        {matched}
      </ScriptureRef>,
    );
    last = m.index + matched.length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}
