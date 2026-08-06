"""CitationExtractor — pulls every scripture reference (and any adjacent quoted
text) out of the Apologist's draft. Deterministic, NO llm.

The reference regex mirrors the harvester in web/scripts/build-verses.mjs. Quote
pairing is a heuristic: the nearest quotation run on *either* side of a reference,
within a small window, is treated as that reference's quoted text (the book cites
both "...text..." (Book c:v) and Book c:v, "...text..."). canon.verify_citation
then decides truth — this node only proposes candidates. Erring toward pairing (and
thus toward a re-draft on mismatch) is the safe direction for a hard gate.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from graph.config import REPO_ROOT  # noqa: E402

from ..state import DebateState  # noqa: E402

# Build the book-name alternation from the shared canon so it never drifts.
_meta = json.loads((REPO_ROOT / "shared" / "canon" / "book-meta.json").read_text("utf-8"))
_BOOK_NAMES = sorted(set(_meta["bookAliases"].values()), key=len, reverse=True)
_BOOK_ALT = "|".join(re.escape(b) for b in _BOOK_NAMES)

# "Book c:v" or "Book c:v-w", optionally with more comma spans.
_REF_RE = re.compile(
    rf"(?:{_BOOK_ALT})\s+\d+:\d+(?:[–-]\d+)?(?:,\s?\d+(?:[–-]\d+)?)*"
)
# A quoted run: straight or curly quotes.
_QUOTE_RE = re.compile(r"[\"“]([^\"“”]{4,})[\"”]")
_MAX_GAP = 120  # chars between a reference and a quote for them to be paired


def _nearest_quote(text: str, ref_start: int, ref_end: int) -> str | None:
    """Nearest quoted run on either side of the reference, within _MAX_GAP."""
    best: tuple[int, str] | None = None
    for m in _QUOTE_RE.finditer(text):
        if m.end() <= ref_start:
            gap = ref_start - m.end()
        elif m.start() >= ref_end:
            gap = m.start() - ref_end
        else:
            gap = 0  # overlaps the ref (shouldn't happen) — treat as closest
        if gap <= _MAX_GAP and (best is None or gap < best[0]):
            best = (gap, m.group(1).strip())
    return best[1] if best else None


def citation_extractor(state: DebateState) -> dict:
    draft = state.get("draft", "")
    seen: set[str] = set()
    citations = []
    for m in _REF_RE.finditer(draft):
        raw = m.group(0)
        if raw in seen:
            continue
        seen.add(raw)
        citations.append({"raw": raw, "quoted": _nearest_quote(draft, m.start(), m.end())})
    return {"citations": citations}
