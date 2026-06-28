import { visit, SKIP } from "unist-util-visit";

// Plain ESM so @next/mdx can resolve it by absolute path string (required for
// Turbopack's serializable MDX options + Node's require.resolve).

// Surface forms of book names + abbreviations as they appear in the prose.
// Longest first so the alternation matches greedily (Philippians before Phil).
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
  // abbreviations
  "Matt", "Phil", "Col", "Rom", "Cor", "Gal", "Eph", "Heb", "Deut", "Exod",
  "Lev", "Num", "Josh", "Judg", "Prov", "Eccl", "Isa", "Jer", "Ezek", "Dan",
  "Hos", "Mic", "Zech", "Mal", "Ps", "Psa", "Tim", "Pet", "Thess", "Jas",
  "Rev", "Gen", "Chron",
].sort((a, b) => b.length - a.length);

const REF_SOURCE =
  `(?:[1-3]\\s)?(?:${BOOK_FORMS.join("|")})\\.?\\s+\\d+:\\d+(?:[\\u2013-]\\d+)?(?:,\\s?\\d+(?:[\\u2013-]\\d+)?)*`;

const SKIP_TAGS = new Set(["h1", "h2", "h3", "h4", "h5", "h6", "a", "code", "pre"]);

// Highest chapter per (normalized) book — rejects patristic citations that
// share a book name, e.g. Ignatius "to the Ephesians 18:2" (Eph. has 6).
// Keyed by lowercased, dot/space-stripped book token (matches surface + abbr).
const MAX_CHAPTER = {
  genesis: 50, gen: 50, exodus: 40, exod: 40, leviticus: 27, lev: 27,
  numbers: 36, num: 36, deuteronomy: 34, deut: 34, joshua: 24, josh: 24,
  judges: 21, judg: 21, ruth: 4, samuel: 31, kings: 22, psalms: 150,
  psalm: 150, ps: 150, psa: 150, proverbs: 31, prov: 31, ecclesiastes: 12,
  eccl: 12, isaiah: 66, isa: 66, jeremiah: 52, jer: 52, lamentations: 5,
  ezekiel: 48, ezek: 48, daniel: 12, dan: 12, hosea: 14, hos: 14, joel: 3,
  amos: 9, micah: 7, mic: 7, zechariah: 14, zech: 14, malachi: 4, mal: 4,
  matthew: 28, matt: 28, mark: 16, luke: 24, john: 21, acts: 28, romans: 16,
  rom: 16, corinthians: 16, cor: 16, galatians: 6, gal: 6, ephesians: 6,
  eph: 6, philippians: 4, phil: 4, colossians: 4, col: 4, thessalonians: 5,
  thess: 5, timothy: 6, tim: 6, titus: 3, hebrews: 13, heb: 13, james: 5,
  jas: 5, peter: 5, pet: 5, jude: 1, revelation: 22, rev: 22, job: 42,
};

// True when the matched reference is a plausible biblical citation (its chapter
// does not exceed the book's real length).
function isValidRef(matched) {
  const m = matched.match(/^(?:[1-3]\s)?([A-Za-z]+)\.?\s+(\d+):/);
  if (!m) return true;
  const max = MAX_CHAPTER[m[1].toLowerCase()];
  if (max === undefined) return true;
  return parseInt(m[2], 10) <= max;
}

export function rehypeScripture() {
  return (tree) => {
    const re = new RegExp(REF_SOURCE, "g");
    visit(tree, "text", (node, index, parent) => {
      if (
        index === undefined ||
        !parent ||
        parent.type !== "element" ||
        SKIP_TAGS.has(parent.tagName)
      ) {
        return;
      }

      const value = node.value;
      re.lastIndex = 0;
      if (!re.test(value)) return;
      re.lastIndex = 0;

      const out = [];
      let last = 0;
      let m;
      while ((m = re.exec(value)) !== null) {
        const start = m.index;
        const matched = m[0];
        if (!isValidRef(matched)) continue; // skip patristic look-alikes
        if (start > last) out.push({ type: "text", value: value.slice(last, start) });
        out.push({
          type: "element",
          tagName: "a",
          properties: { className: ["scripture-ref"], dataRef: matched },
          children: [{ type: "text", value: matched }],
        });
        last = start + matched.length;
      }
      if (last < value.length) out.push({ type: "text", value: value.slice(last) });

      parent.children.splice(index, 1, ...out);
      return [SKIP, index + out.length];
    });
  };
}

export default rehypeScripture;
