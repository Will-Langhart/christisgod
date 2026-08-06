"""Deterministic Scripture canon — the hard gate for the apologetics engine.

A Python port of the reference parser in ``web/src/lib/scripture.ts``, reading the
generated canon in ``shared/canon/`` (produced by ``web/scripts/build-verses.mjs``).
This module is the ScriptureVerifier node's core: it can tell, with certainty,
whether a reference is real and in range, and whether a *quoted* verse matches the
KJV. It uses no LLM and has no third-party dependencies. See AI-SPEC.md §4.
"""

from __future__ import annotations

import gzip
import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

# shared/canon lives two levels up from this file (repo-root/shared/canon).
CANON_DIR = Path(__file__).resolve().parent.parent / "shared" / "canon"


@lru_cache(maxsize=1)
def _book_meta() -> dict:
    return json.loads((CANON_DIR / "book-meta.json").read_text("utf-8"))


@lru_cache(maxsize=1)
def _verses() -> dict[str, str]:
    """The verification store, keyed "Book c:v". Prefers the full-KJV
    kjv.json.gz (all 31,102 verses); falls back to the small curated verses.json
    if the full store hasn't been built (`node scripts/build-kjv.mjs`)."""
    full = CANON_DIR / "kjv.json.gz"
    if full.exists():
        with gzip.open(full, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads((CANON_DIR / "verses.json").read_text("utf-8"))


@dataclass(frozen=True)
class ParsedRef:
    raw: str
    book: str
    rest: str  # the "chapter:verse" portion
    display: str  # canonical "Book c:v" form
    bible_gateway_url: str


def _norm_book_key(book: str) -> str:
    return book.lower().replace(".", "").replace(" ", "")


# Mirrors parseRef() in web/src/lib/scripture.ts. Keep the two in step; the
# book-meta.json they both draw from is the guard against drift (AI-SPEC.md §6).
_REF_RE = re.compile(r"^\s*((?:[1-3]\s*)?[A-Za-z]+\.?)\s+(\d.*)$")


def parse_ref(raw: str) -> ParsedRef | None:
    """Parse e.g. ``"1 Corinthians 8:6"`` → ParsedRef, or ``None`` if invalid.

    Rejects references whose chapter exceeds the book's real length, which is how
    patristic look-alikes (Ignatius "to the Ephesians 18:2") are filtered out.
    """
    meta = _book_meta()
    aliases: dict[str, str] = meta["bookAliases"]
    max_chapter: dict[str, int] = meta["maxChapter"]

    m = _REF_RE.match(raw)
    if not m:
        return None
    book = aliases.get(_norm_book_key(m.group(1)))
    if not book:
        return None
    rest = m.group(2).strip()

    chapter_match = re.match(r"\d+", rest)
    if chapter_match:
        chapter = int(chapter_match.group(0))
        if chapter > max_chapter.get(book, 999):
            return None

    display = f"{book} {rest}"
    bible_gateway_url = (
        "https://www.biblegateway.com/passage/?version=KJV&search="
        + quote(display)
    )
    return ParsedRef(raw=raw, book=book, rest=rest, display=display,
                     bible_gateway_url=bible_gateway_url)


_RANGE_RE = re.compile(r"^(.*?)\s+(\d+):(\d+)[–-](\d+)$")


def lookup_verse(display: str) -> str | None:
    """Authoritative KJV text for a canonical ``"Book c:v"`` key, or ``None``.

    Handles verse ranges ("Colossians 1:16-17") by assembling the span from the
    full-KJV single-verse store."""
    store = _verses()
    if display in store:
        return store[display]
    m = _RANGE_RE.match(display)
    if m:
        book, ch, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        parts = [store.get(f"{book} {ch}:{v}") for v in range(a, b + 1)]
        parts = [p for p in parts if p]
        if parts:
            return " ".join(parts)
    return None


def _normalize_text(s: str) -> str:
    """Fold for quote comparison: NFKD, lowercase, strip punctuation, collapse WS."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)  # drop punctuation, curly quotes, ellipses
    return re.sub(r"\s+", " ", s).strip()


@lru_cache(maxsize=1)
def _kjv_blob() -> str:
    """All KJV verse text, normalized, newline-joined. A quoted string is accepted
    as genuine Scripture iff it is a verbatim substring here. Newlines between
    verses prevent accidental cross-verse matches."""
    return "\n".join(_normalize_text(t) for t in _verses().values())


def _quote_is_scripture(quoted: str | None) -> bool:
    """True if the quote is verbatim KJV somewhere. This is the anti-fabrication
    guarantee: the model cannot invent Scripture text. It deliberately does NOT
    require the quote to match the *specific* reference it was attached to — a
    real verse cited with a slightly-off verse number (e.g. Col 1:17 text labelled
    1:16) is an attribution slip, not a hallucination, and shouldn't hard-block."""
    if not quoted:
        return True
    nq = _normalize_text(quoted)
    return bool(nq) and nq in _kjv_blob()


@dataclass(frozen=True)
class VerifyResult:
    ok: bool  # HARD gate: the reference is a real, in-range, existing KJV verse
    reason: str
    display: str | None = None  # canonical ref, when parseable
    warning: str | None = None  # non-blocking: quote near this ref isn't verbatim KJV


def verify_citation(raw: str, quoted_text: str | None = None) -> VerifyResult:
    """The hard gate. A citation passes only if:

    1. the reference parses and is in range, AND
    2. we have KJV text for it (so the model cannot cite a verse we can't check), AND
    3. if ``quoted_text`` is supplied, its normalized form is a contiguous
       substring of the normalized KJV verse — i.e. no misquotation.

    Returns a structured pass/fail with a human-readable reason for the graph's
    conditional edge and for trace/debug output.
    """
    parsed = parse_ref(raw)
    if parsed is None:
        return VerifyResult(ok=False, reason=f"unparseable or out-of-range reference: {raw!r}")

    canon = lookup_verse(parsed.display)
    if canon is None:
        return VerifyResult(
            ok=False,
            reason=f"{parsed.display!r} is not a real KJV verse (check the verse number)",
            display=parsed.display,
        )

    warning = (None if _quote_is_scripture(quoted_text)
               else f"quote near {parsed.display} is not verbatim KJV")
    return VerifyResult(ok=True, reason="verified", display=parsed.display, warning=warning)


def verify_citations(items: list[dict]) -> list[VerifyResult]:
    """Batch verify with POOLED quote-matching. Each item is ``{"raw", "quoted"}``.

    Only the REFERENCE is hard-gated: it fails if unparseable, out of range, or a
    verse that doesn't exist (the real anti-hallucination guarantee — the model
    cannot cite a fake verse). Quote accuracy is a NON-BLOCKING warning: models
    legitimately put paraphrases, titles, and critical discussion of textual
    variants (e.g. the Comma Johanneum) in quotation marks near a real reference,
    and hard-failing those degrades sound answers. Warnings are surfaced for human
    review instead.
    """
    results: list[VerifyResult] = []
    for it in items:
        parsed = parse_ref(it["raw"])
        if parsed is None:
            results.append(VerifyResult(False, f"unparseable or out-of-range reference: {it['raw']!r}"))
            continue
        if lookup_verse(parsed.display) is None:
            results.append(VerifyResult(
                False, f"{parsed.display!r} is not a real KJV verse (check the verse number)",
                display=parsed.display))
            continue
        warning = (None if _quote_is_scripture(it.get("quoted"))
                   else f"quote near {parsed.display} is not verbatim KJV")
        results.append(VerifyResult(True, "verified", display=parsed.display, warning=warning))
    return results
