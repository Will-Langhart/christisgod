"""Deterministic Scripture canon — the hard gate for the apologetics engine.

A Python port of the reference parser in ``web/src/lib/scripture.ts``, reading the
generated canon in ``shared/canon/`` (produced by ``web/scripts/build-verses.mjs``).
This module is the ScriptureVerifier node's core: it can tell, with certainty,
whether a reference is real and in range, and whether a *quoted* verse matches the
KJV. It uses no LLM and has no third-party dependencies. See AI-SPEC.md §4.
"""

from __future__ import annotations

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


def lookup_verse(display: str) -> str | None:
    """Authoritative KJV text for a canonical ``"Book c:v"`` key, or ``None``."""
    return _verses().get(display)


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
            reason=f"no KJV text on record for {parsed.display!r}; cite from the corpus",
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
