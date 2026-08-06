"""Retriever — returns the chapter passages most relevant to the objection.

PLACEHOLDER: a dependency-free keyword/overlap retriever over the 17 MDX
chapters, so the graph spine runs before the embedding stack is wired. Replace
`_score` with a Chroma similarity search over embedded chunks for Phase 1 proper
(see AI-SPEC.md §5). The node's return contract stays the same.
"""

from __future__ import annotations

import re

from ..config import CONTENT_DIR, RETRIEVER_TOP_K
from ..state import DebateState

_WORD_RE = re.compile(r"[a-z]{4,}")
_STOP = {"that", "this", "with", "from", "have", "does", "said", "they", "what",
         "when", "would", "which", "there", "their", "about", "jesus", "christ",
         "god"}  # drop terms too common in *this* corpus to discriminate


def _terms(text: str) -> set[str]:
    return {w for w in _WORD_RE.findall(text.lower()) if w not in _STOP}


def _paragraphs() -> list[tuple[str, str]]:
    out = []
    for path in sorted(CONTENT_DIR.glob("*.mdx")):
        for para in path.read_text("utf-8").split("\n\n"):
            para = para.strip()
            if len(para) > 120 and not para.startswith(("import", "<", "#")):
                out.append((path.stem, para))
    return out


def retriever(state: DebateState) -> dict:
    query = _terms(state.get("objection", ""))
    scored = []
    for stem, para in _paragraphs():
        overlap = len(query & _terms(para))
        if overlap:
            scored.append((overlap, stem, para))
    scored.sort(key=lambda t: t[0], reverse=True)
    top = [f"[{stem}] {para}" for _, stem, para in scored[:RETRIEVER_TOP_K]]
    return {"retrieved": top}
