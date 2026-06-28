// Scripture reference parsing + a KJV verse store (public domain).
// The rehype plugin tags references in the prose; the popover component uses
// these helpers to render verse text and a BibleGateway link.
//
// Verse text is auto-generated from the prose by scripts/build-verses.mjs
// (see GENERATED_VERSES); VERSE_TEXT below holds any manual overrides.
import { GENERATED_VERSES } from "./verses.generated";

// Highest chapter number per book — rejects patristic look-alikes such as
// Ignatius "to the Ephesians 18:2" (biblical Ephesians has only 6 chapters).
const MAX_CHAPTER: Record<string, number> = {
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

// Canonical book names + common abbreviations used in the manuscript.
const BOOK_ALIASES: Record<string, string> = {
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
  ezek: "Ezekiel", ezekiel: "Ezekiel",
  dan: "Daniel", daniel: "Daniel",
  hos: "Hosea", hosea: "Hosea",
  joel: "Joel", amos: "Amos",
  mic: "Micah", micah: "Micah",
  zech: "Zechariah", zechariah: "Zechariah",
  mal: "Malachi", malachi: "Malachi",
  matt: "Matthew", matthew: "Matthew",
  mark: "Mark",
  luke: "Luke",
  john: "John",
  acts: "Acts",
  rom: "Romans", romans: "Romans",
  "1cor": "1 Corinthians", "2cor": "2 Corinthians",
  gal: "Galatians", galatians: "Galatians",
  eph: "Ephesians", ephesians: "Ephesians",
  phil: "Philippians", philippians: "Philippians",
  col: "Colossians", colossians: "Colossians",
  "1thess": "1 Thessalonians", "2thess": "2 Thessalonians",
  "1tim": "1 Timothy", "2tim": "2 Timothy",
  titus: "Titus",
  heb: "Hebrews", hebrews: "Hebrews",
  jas: "James", james: "James",
  "1pet": "1 Peter", "2pet": "2 Peter",
  "1john": "1 John", "2john": "2 John", "3john": "3 John",
  jude: "Jude",
  rev: "Revelation", revelation: "Revelation",
};

export type ParsedRef = {
  raw: string;
  book: string;
  rest: string; // chapter:verse portion
  display: string;
  bibleGatewayUrl: string;
};

function normBookKey(book: string): string {
  return book
    .toLowerCase()
    .replace(/\./g, "")
    .replace(/\s+/g, "");
}

export function parseRef(raw: string): ParsedRef | null {
  // e.g. "1 Corinthians 8:6", "Phil. 1:2", "John 1:1, 14"
  const m = raw.match(/^\s*((?:[1-3]\s*)?[A-Za-z]+\.?)\s+(\d.*)$/);
  if (!m) return null;
  const bookKey = normBookKey(m[1]);
  const book = BOOK_ALIASES[bookKey];
  if (!book) return null;
  const rest = m[2].trim();
  // Reject references whose chapter exceeds the book's real length (patristic
  // citations that share a book name, e.g. Ignatius "to the Ephesians 18").
  const chapter = parseInt(rest, 10);
  if (Number.isFinite(chapter) && chapter > (MAX_CHAPTER[book] ?? 999)) {
    return null;
  }
  const display = `${book} ${rest}`;
  const bibleGatewayUrl =
    "https://www.biblegateway.com/passage/?version=KJV&search=" +
    encodeURIComponent(display);
  return { raw, book, rest, display, bibleGatewayUrl };
}

// Curated KJV text for the highest-value references in the work.
// Keyed by normalized "Book c:v" (single verse / contiguous span).
export const VERSE_TEXT: Record<string, string> = {
  "John 1:1":
    "In the beginning was the Word, and the Word was with God, and the Word was God.",
  "John 1:14":
    "And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth.",
  "John 1:18":
    "No man hath seen God at any time; the only begotten Son, which is in the bosom of the Father, he hath declared him.",
  "John 8:58":
    "Jesus said unto them, Verily, verily, I say unto you, Before Abraham was, I am.",
  "John 10:30": "I and my Father are one.",
  "John 20:28": "And Thomas answered and said unto him, My Lord and my God.",
  "Romans 9:5":
    "Whose are the fathers, and of whom as concerning the flesh Christ came, who is over all, God blessed for ever. Amen.",
  "Colossians 1:15":
    "Who is the image of the invisible God, the firstborn of every creature.",
  "Colossians 1:16":
    "For by him were all things created, that are in heaven, and that are in earth, visible and invisible... all things were created by him, and for him.",
  "Colossians 2:9":
    "For in him dwelleth all the fulness of the Godhead bodily.",
  "Titus 2:13":
    "Looking for that blessed hope, and the glorious appearing of the great God and our Saviour Jesus Christ.",
  "Hebrews 1:8":
    "But unto the Son he saith, Thy throne, O God, is for ever and ever: a sceptre of righteousness is the sceptre of thy kingdom.",
  "Philippians 2:6":
    "Who, being in the form of God, thought it not robbery to be equal with God.",
  "Philippians 2:10":
    "That at the name of Jesus every knee should bow, of things in heaven, and things in earth, and things under the earth.",
  "1 Corinthians 8:6":
    "But to us there is but one God, the Father, of whom are all things, and we in him; and one Lord Jesus Christ, by whom are all things, and we by him.",
  "Isaiah 9:6":
    "For unto us a child is born, unto us a son is given... and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace.",
  "Isaiah 40:3":
    "The voice of him that crieth in the wilderness, Prepare ye the way of the LORD, make straight in the desert a highway for our God.",
  "Acts 20:28":
    "...feed the church of God, which he hath purchased with his own blood.",
  "1 Timothy 3:16":
    "And without controversy great is the mystery of godliness: God was manifest in the flesh...",
  "1 John 5:20":
    "...we are in him that is true, even in his Son Jesus Christ. This is the true God, and eternal life.",
  "Micah 5:2":
    "...out of thee shall he come forth... whose goings forth have been from of old, from everlasting.",
  "Mark 1:1": "The beginning of the gospel of Jesus Christ, the Son of God.",
  "2 Peter 1:1":
    "...through the righteousness of God and our Saviour Jesus Christ.",
  "Revelation 5:13":
    "...Blessing, and honour, and glory, and power, be unto him that sitteth upon the throne, and unto the Lamb for ever and ever.",
  "Deuteronomy 6:4":
    "Hear, O Israel: The LORD our God is one LORD.",
  "Matthew 28:9": "...And they came and held him by the feet, and worshipped him.",
};

// Generated KJV text is authoritative (full, accurate); VERSE_TEXT supplies
// manual overrides only where a hand-trimmed rendering is preferred.
const ALL_VERSES: Record<string, string> = { ...VERSE_TEXT, ...GENERATED_VERSES };

export function lookupVerse(display: string): string | undefined {
  return ALL_VERSES[display];
}
