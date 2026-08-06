// Builds the FULL King James Version verification store for the apologetics
// verifier (service/canon.py): shared/canon/kjv.json.gz — every verse, keyed
// "Book c:v" — plus an authoritative shared/canon/book-meta.json covering all
// 66 books (accurate maxChapter from the data + name aliases).
//
// This is the VERIFICATION corpus (checks any citation the apologist makes),
// distinct from the site's small curated verses.json (hover-cards) and from the
// RETRIEVAL corpus (the 17 chapters that ground the argument). See AI-SPEC.md §4.
//
// Run:  node scripts/build-kjv.mjs
// Source: aruljohn/Bible-kjv (public-domain KJV, per-book JSON).
import { writeFile, mkdir } from "node:fs/promises";
import { gzipSync } from "node:zlib";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CANON = join(ROOT, "..", "shared", "canon");

// [canonical display name, aruljohn file stem]. Canonical names match the style
// used elsewhere (e.g. singular "Psalm", "Song of Solomon").
const BOOKS = [
  ["Genesis", "Genesis"], ["Exodus", "Exodus"], ["Leviticus", "Leviticus"],
  ["Numbers", "Numbers"], ["Deuteronomy", "Deuteronomy"], ["Joshua", "Joshua"],
  ["Judges", "Judges"], ["Ruth", "Ruth"], ["1 Samuel", "1Samuel"],
  ["2 Samuel", "2Samuel"], ["1 Kings", "1Kings"], ["2 Kings", "2Kings"],
  ["1 Chronicles", "1Chronicles"], ["2 Chronicles", "2Chronicles"],
  ["Ezra", "Ezra"], ["Nehemiah", "Nehemiah"], ["Esther", "Esther"],
  ["Job", "Job"], ["Psalm", "Psalms"], ["Proverbs", "Proverbs"],
  ["Ecclesiastes", "Ecclesiastes"], ["Song of Solomon", "SongofSolomon"],
  ["Isaiah", "Isaiah"], ["Jeremiah", "Jeremiah"], ["Lamentations", "Lamentations"],
  ["Ezekiel", "Ezekiel"], ["Daniel", "Daniel"], ["Hosea", "Hosea"],
  ["Joel", "Joel"], ["Amos", "Amos"], ["Obadiah", "Obadiah"], ["Jonah", "Jonah"],
  ["Micah", "Micah"], ["Nahum", "Nahum"], ["Habakkuk", "Habakkuk"],
  ["Zephaniah", "Zephaniah"], ["Haggai", "Haggai"], ["Zechariah", "Zechariah"],
  ["Malachi", "Malachi"], ["Matthew", "Matthew"], ["Mark", "Mark"],
  ["Luke", "Luke"], ["John", "John"], ["Acts", "Acts"], ["Romans", "Romans"],
  ["1 Corinthians", "1Corinthians"], ["2 Corinthians", "2Corinthians"],
  ["Galatians", "Galatians"], ["Ephesians", "Ephesians"],
  ["Philippians", "Philippians"], ["Colossians", "Colossians"],
  ["1 Thessalonians", "1Thessalonians"], ["2 Thessalonians", "2Thessalonians"],
  ["1 Timothy", "1Timothy"], ["2 Timothy", "2Timothy"], ["Titus", "Titus"],
  ["Philemon", "Philemon"], ["Hebrews", "Hebrews"], ["James", "James"],
  ["1 Peter", "1Peter"], ["2 Peter", "2Peter"], ["1 John", "1John"],
  ["2 John", "2John"], ["3 John", "3John"], ["Jude", "Jude"],
  ["Revelation", "Revelation"],
];

// Common abbreviations the prose / model may emit (normalized: lowercased, no
// dots/spaces). Full names are auto-added below.
const ABBREV = {
  gen: "Genesis", ex: "Exodus", exod: "Exodus", lev: "Leviticus", num: "Numbers",
  deut: "Deuteronomy", josh: "Joshua", judg: "Judges", "1sam": "1 Samuel",
  "2sam": "2 Samuel", "1kgs": "1 Kings", "2kgs": "2 Kings", "1chr": "1 Chronicles",
  "2chr": "2 Chronicles", neh: "Nehemiah", ps: "Psalm", psa: "Psalm",
  psalms: "Psalm", prov: "Proverbs", eccl: "Ecclesiastes", song: "Song of Solomon",
  sos: "Song of Solomon", isa: "Isaiah", jer: "Jeremiah", lam: "Lamentations",
  ezek: "Ezekiel", dan: "Daniel", hos: "Hosea", obad: "Obadiah", mic: "Micah",
  nah: "Nahum", hab: "Habakkuk", zeph: "Zephaniah", hag: "Haggai",
  zech: "Zechariah", mal: "Malachi", matt: "Matthew", rom: "Romans",
  "1cor": "1 Corinthians", "2cor": "2 Corinthians", gal: "Galatians",
  eph: "Ephesians", phil: "Philippians", philem: "Philemon", col: "Colossians",
  "1thess": "1 Thessalonians", "2thess": "2 Thessalonians", "1tim": "1 Timothy",
  "2tim": "2 Timothy", heb: "Hebrews", jas: "James", "1pet": "1 Peter",
  "2pet": "2 Peter", "1jn": "1 John", "2jn": "2 John", "3jn": "3 John",
  rev: "Revelation",
};

async function main() {
  const kjv = {};
  const maxChapter = {};
  const bookAliases = { ...ABBREV };

  for (const [name, stem] of BOOKS) {
    const url = `https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/${stem}.json`;
    const res = await fetch(url);
    if (!res.ok) {
      console.warn(`! failed ${name} (${stem}): ${res.status}`);
      continue;
    }
    const data = await res.json();
    maxChapter[name] = data.chapters.length;
    bookAliases[name.toLowerCase().replace(/\s+/g, "")] = name; // full-name alias
    for (const ch of data.chapters) {
      for (const v of ch.verses) kjv[`${name} ${ch.chapter}:${v.verse}`] = v.text;
    }
    process.stdout.write(`· ${name} (${data.chapters.length} ch)\n`);
  }

  await mkdir(CANON, { recursive: true });
  await writeFile(join(CANON, "kjv.json.gz"), gzipSync(Buffer.from(JSON.stringify(kjv))));
  await writeFile(
    join(CANON, "book-meta.json"),
    JSON.stringify({ maxChapter, bookAliases }, null, 2) + "\n",
    "utf8",
  );
  console.log(
    `\n✓ ${Object.keys(kjv).length} verses, ${Object.keys(maxChapter).length} books ` +
    `→ ${CANON}/kjv.json.gz + book-meta.json`,
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
