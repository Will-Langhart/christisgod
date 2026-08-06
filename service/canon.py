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


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    reason: str
    display: str | None = None  # canonical ref, when parseable


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

    if quoted_text is not None:
        if _normalize_text(quoted_text) not in _normalize_text(canon):
            return VerifyResult(
                ok=False,
                reason=f"quoted text does not match KJV for {parsed.display!r}",
                display=parsed.display,
            )

    return VerifyResult(ok=True, reason="verified", display=parsed.display)


def verify_citations(items: list[dict]) -> list[VerifyResult]:
    """Batch verify with POOLED quote-matching. Each item is ``{"raw", "quoted"}``.

    A reference still fails hard if it's unparseable, out of range, or names a
    verse that doesn't exist. But a quote passes if it matches its own reference
    *or any other verse cited in the same answer* — so interleaved quotes and
    references ("...text A..." and "...text B..." (Ref A, Ref B)) don't trigger a
    false misquote rejection. A genuine misquote (text matching no cited verse)
    still fails.
    """
    parsed_all = [parse_ref(it["raw"]) for it in items]
    texts = [lookup_verse(p.display) if p else None for p in parsed_all]
    pool = [_normalize_text(t) for t in texts if t]

    results: list[VerifyResult] = []
    for it, parsed, text in zip(items, parsed_all, texts):
        if parsed is None:
            results.append(VerifyResult(False, f"unparseable or out-of-range reference: {it['raw']!r}"))
            continue
        if text is None:
            results.append(VerifyResult(
                False, f"{parsed.display!r} is not a real KJV verse (check the verse number)",
                display=parsed.display))
            continue
        quoted = it.get("quoted")
        if quoted:
            nq = _normalize_text(quoted)
            if nq not in _normalize_text(text) and not any(nq in t for t in pool):
                results.append(VerifyResult(
                    False, f"quoted text matches no cited verse (near {parsed.display!r})",
                    display=parsed.display))
                continue
        results.append(VerifyResult(True, "verified", display=parsed.display))
    return results
