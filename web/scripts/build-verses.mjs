// Harvests every scripture reference from the MDX content, fetches accurate
// public-domain KJV text, and generates src/lib/verses.generated.ts.
//
// Run:  node scripts/build-verses.mjs
//
// Source: aruljohn/Bible-kjv (public domain KJV, per-book JSON).
import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const CONTENT_DIR = join(ROOT, "src", "content");
const OUT = join(ROOT, "src", "lib", "verses.generated.ts");

// Canonical book name (as used by scripture.ts) → aruljohn filename stem.
const BOOK_ALIASES = {
  gen: "Genesis", genesis: "Genesis",
  ex: "Exodus", exod: "Exodus", exodus: "Exodus",
  lev: "Leviticus", leviticus: "Leviticus",
  num: "Numbers", numbers: "Numbers",
  deut: "Deuteronomy", deuteronomy: "Deuteronomy",
  josh: "Joshua", joshua: "Joshua",
  judg: "Judges", judges: "Judges",
  ruth: "Ruth",
  "1sam": "1 Samuel", "2sam": "2 Samuel",
  "1kings": "1 Kings", "2kings": "2 Kings",
  ps: "Psalm", psa: "Psalm", psalm: "Psalm", psalms: "Psalm",
  prov: "Proverbs", proverbs: "Proverbs",
  eccl: "Ecclesiastes", ecclesiastes: "Ecclesiastes",
  isa: "Isaiah", isaiah: "Isaiah",
  jer: "Jeremiah", jeremiah: "Jeremiah",
  lam: "Lamentations", lamentations: "Lamentations",
  ezek: "Ezekiel", ezekiel: "Ezekiel",
  dan: "Daniel", daniel: "Daniel",
  hos: "Hosea", hosea: "Hosea",
  joel: "Joel", amos: "Amos",
  mic: "Micah", micah: "Micah",
  zech: "Zechariah", zechariah: "Zechariah",
  mal: "Malachi", malachi: "Malachi",
  matt: "Matthew", matthew: "Matthew",
  mark: "Mark", luke: "Luke", john: "John", acts: "Acts",
  rom: "Romans", romans: "Romans",
  "1cor": "1 Corinthians", "2cor": "2 Corinthians",
  "1corinthians": "1 Corinthians", "2corinthians": "2 Corinthians",
  gal: "Galatians", galatians: "Galatians",
  eph: "Ephesians", ephesians: "Ephesians",
  phil: "Philippians", philippians: "Philippians",
  col: "Colossians", colossians: "Colossians",
  "1thess": "1 Thessalonians", "2thess": "2 Thessalonians",
  "1thessalonians": "1 Thessalonians", "2thessalonians": "2 Thessalonians",
  "1tim": "1 Timothy", "2tim": "2 Timothy",
  "1timothy": "1 Timothy", "2timothy": "2 Timothy",
  titus: "Titus",
  heb: "Hebrews", hebrews: "Hebrews",
  jas: "James", james: "James",
  "1pet": "1 Peter", "2pet": "2 Peter",
  "1peter": "1 Peter", "2peter": "2 Peter",
  "1samuel": "1 Samuel", "2samuel": "2 Samuel",
  "1john": "1 John", "2john": "2 John", "3john": "3 John",
  jude: "Jude",
  rev: "Revelation", revelation: "Revelation",
  job: "Job",
};

// Canonical book → aruljohn filename stem.
const FILE_STEM = (book) =>
  book === "Psalm" ? "Psalms" : book.replace(/\s+/g, "");

// Max chapter per book — used to reject patristic look-alikes (e.g. Ignatius
// "to the Ephesians 18:2" is not biblical Ephesians, which has only 6 chapters).
const MAX_CHAPTER = {
  Genesis: 50, Exodus: 40, Leviticus: 27, Numbers: 36, Deuteronomy: 34,
  Joshua: 24, Judges: 21, Ruth: 4, "1 Samuel": 31, "2 Samuel": 24,
  "1 Kings": 22, "2 Kings": 25, Psalm: 150, Proverbs: 31, Ecclesiastes: 12,
  Isaiah: 66, Jeremiah: 52, Lamentations: 5, Ezekiel: 48, Daniel: 12,
  Hosea: 14, Joel: 3, Amos: 9, Micah: 7, Zechariah: 14, Malachi: 4,
  Matthew: 28, Mark: 16, Luke: 24, John: 21, Acts: 28, Romans: 16,
  "1 Corinthians": 16, "2 Corinthians": 13, Galatians: 6, Ephesians: 6,
  Philippians: 4, Colossians: 4, "1 Thessalonians": 5, "2 Thessalonians": 3,
  "1 Timothy": 6, "2 Timothy": 4, Titus: 3, Hebrews: 13, James: 5,
  "1 Peter": 5, "2 Peter": 3, "1 John": 5, "2 John": 1, "3 John": 1,
  Jude: 1, Revelation: 22, Job: 42,
};

const BOOK_FORMS = [
  "Deuteronomy", "Ecclesiastes", "Thessalonians", "Lamentations",
  "Philippians", "Corinthians", "Colossians", "Revelation", "Zechariah",
  "Ephesians", "Galatians", "Proverbs", "Jeremiah", "Hebrews", "Genesis",
  "Exodus", "Numbers", "Joshua", "Judges", "Malachi", "Matthew", "Timothy",
  "Leviticus", "Isaiah", "Daniel", "Hosea", "Romans", "Samuel", "Psalms",
  "Psalm", "Micah", "Titus", "James", "Peter", "Joel", "Amos", "Ruth",
  "Mark", "Luke", "John", "Acts", "Jude", "Kings", "Job",
  "Matt", "Phil", "Col", "Rom", "Cor", "Gal", "Eph", "Heb", "Deut", "Exod",
  "Lev", "Num", "Josh", "Judg", "Prov", "Eccl", "Isa", "Jer", "Ezek", "Dan",
  "Hos", "Mic", "Zech", "Mal", "Ps", "Psa", "Tim", "Pet", "Thess", "Jas",
  "Rev", "Gen",
].sort((a, b) => b.length - a.length);

const REF_RE = new RegExp(
  `(?:[1-3]\\s)?(?:${BOOK_FORMS.join("|")})\\.?\\s+\\d+:\\d+(?:[\\u2013-]\\d+)?(?:,\\s?\\d+(?:[\\u2013-]\\d+)?)*`,
  "g",
);

function normKey(book) {
  return book.toLowerCase().replace(/\./g, "").replace(/\s+/g, "");
}

// Parse a raw ref → { book, chapter, verses:[from,to] } for the PRIMARY span.
function parsePrimary(raw) {
  const m = raw.match(/^\s*((?:[1-3]\s*)?[A-Za-z]+\.?)\s+(\d+):(\d+)(?:[–-](\d+))?/);
  if (!m) return null;
  const book = BOOK_ALIASES[normKey(m[1])];
  if (!book) return null;
  const chapter = parseInt(m[2], 10);
  if (chapter > (MAX_CHAPTER[book] ?? 999)) return null; // reject look-alikes
  const from = parseInt(m[3], 10);
  const to = m[4] ? parseInt(m[4], 10) : from;
  return { book, chapter, from, to };
}

async function main() {
  // 1. Harvest refs from all MDX.
  const files = (await readdir(CONTENT_DIR)).filter((f) => f.endsWith(".mdx"));
  const refs = new Set();
  for (const f of files) {
    const text = await readFile(join(CONTENT_DIR, f), "utf8");
    for (const m of text.matchAll(REF_RE)) refs.add(m[0]);
  }

  // 2. Reduce to needed primary spans, grouped by book.
  const needed = new Map(); // book -> Set("chapter:from-to")
  const spans = [];
  for (const raw of refs) {
    const p = parsePrimary(raw);
    if (!p) continue;
    const key = `${p.chapter}:${p.from}-${p.to}`;
    if (!needed.has(p.book)) needed.set(p.book, new Set());
    if (!needed.get(p.book).has(key)) {
      needed.get(p.book).add(key);
      spans.push(p);
    }
  }

  // 3. Fetch each needed book once.
  const cache = new Map();
  for (const book of needed.keys()) {
    const stem = FILE_STEM(book);
    const url = `https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/${stem}.json`;
    const res = await fetch(url);
    if (!res.ok) {
      console.warn(`! failed ${book} (${stem}): ${res.status}`);
      continue;
    }
    const data = await res.json();
    const byCh = new Map();
    for (const ch of data.chapters) {
      const vmap = new Map();
      for (const v of ch.verses) vmap.set(v.verse, v.text);
      byCh.set(ch.chapter, vmap);
    }
    cache.set(book, byCh);
    process.stdout.write(`· ${book}\n`);
  }

  // 4. Build the verse map.
  const out = {};
  for (const p of spans) {
    const byCh = cache.get(p.book);
    const vmap = byCh?.get(String(p.chapter));
    if (!vmap) continue;
    const parts = [];
    for (let v = p.from; v <= p.to; v++) {
      const t = vmap.get(String(v));
      if (t) parts.push(t);
    }
    if (parts.length === 0) continue;
    const text = parts.join(" ");
    const display =
      p.from === p.to
        ? `${p.book} ${p.chapter}:${p.from}`
        : `${p.book} ${p.chapter}:${p.from}-${p.to}`;
    out[display] = text;
    // also store the single primary verse for fallback lookups
    out[`${p.book} ${p.chapter}:${p.from}`] = vmap.get(String(p.from)) ?? text;
  }

  const keys = Object.keys(out).sort();
  const body =
    `// AUTO-GENERATED by scripts/build-verses.mjs. Do not edit by hand.\n` +
    `// Public-domain King James Version text (source: aruljohn/Bible-kjv).\n` +
    `export const GENERATED_VERSES: Record<string, string> = {\n` +
    keys
      .map((k) => `  ${JSON.stringify(k)}: ${JSON.stringify(out[k])},`)
      .join("\n") +
    `\n};\n`;
  await writeFile(OUT, body, "utf8");
  console.log(`\n✓ wrote ${keys.length} verse entries → ${OUT}`);

  // 5. Emit the shared canon consumed by the LangGraph verifier service
  //    (service/canon.py). This keeps ONE source of truth: verses.generated.ts
  //    and verses.json are written from the same `out` map in the same pass, so
  //    they cannot drift. See AI-SPEC.md §6.
  const SHARED = join(ROOT, "..", "shared", "canon");
  await mkdir(SHARED, { recursive: true });

  const verseJson = {};
  for (const k of keys) verseJson[k] = out[k];
  await writeFile(
    join(SHARED, "verses.json"),
    JSON.stringify(verseJson, null, 2) + "\n",
    "utf8",
  );
  // NB: book-meta.json + the full kjv.json.gz verification store are owned by
  // build-kjv.mjs (all 66 books). verses.json here is just the site's curated
  // hover-card set / verifier fallback.
  console.log(`✓ wrote shared verses.json → ${SHARED}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
