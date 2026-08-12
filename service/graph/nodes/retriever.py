"""Retriever node — returns the chapter passages most relevant to the objection.

Thin wrapper over graph.retrieval.search, which uses a Chroma embedding index
(local model, no embeddings key) and degrades to a keyword scorer if chromadb
isn't installed. Rebuild the index after content edits:
`python3 -m graph.retrieval --build`.
"""

from __future__ import annotations

from .. import config, retrieval
from ..config import RETRIEVER_TOP_K
from ..history import last_user_turn
from ..state import DebateState

# HyDE: a hypothetical *orthodox answer* embeds nearer the book's affirmative
# prose than the objection's adversarial phrasing does. One cheap-model call;
# the result is prepended to (not substituted for) the real query so lexical
# anchors survive for the keyword fallback path.
_HYDE_SYSTEM = (
    "You help a Scripture-retrieval step. Given an objection to the deity of "
    "Christ, write a 1-2 sentence sketch of how an orthodox, Bible-grounded "
    "answer would run — the claims and the kinds of verses it would cite. Do not "
    "address the reader, moralize, or hedge; just the answer's substance so it can "
    "be embedded. No preamble."
)


def _hyde_sketch(query: str) -> str | None:
    """Best-effort hypothetical-answer sketch. Returns None on any failure (LLM
    stack absent, no API key, error) so retrieval always degrades to the raw
    query rather than breaking the graph or the deterministic tests."""
    try:
        from .._llm import call_llm

        sketch = call_llm(config.TRIAGE_MODEL, _HYDE_SYSTEM, query, max_tokens=256)
        return sketch.strip() or None
    except Exception:  # noqa: BLE001 — HyDE is an optimization, never load-bearing
        return None


def retriever(state: DebateState) -> dict:
    # Conversational path (Phase 3): retrieve for the live user turn; on a
    # follow-up, enrich the query with the previous user turn so a terse
    # "and the next verse?" still lands on the right chapter. Falls back to the
    # fixed objection for the Phase 1/2 single-shot path.
    query = state.get("user_message") or state.get("objection", "")
    if state.get("intent") == "followup":
        prev = last_user_turn(state.get("history"))
        if prev:
            query = f"{prev}\n{query}"

    search_query = query
    if config.RETRIEVER_HYDE:
        sketch = _hyde_sketch(query)
        if sketch:
            search_query = f"{sketch}\n{query}"

    passages = retrieval.search(search_query, RETRIEVER_TOP_K)
    return {"retrieved": passages}
