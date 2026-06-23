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
