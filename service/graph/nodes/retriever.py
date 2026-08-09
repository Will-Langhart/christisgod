"""Retriever node — returns the chapter passages most relevant to the objection.

Thin wrapper over graph.retrieval.search, which uses a Chroma embedding index
(local model, no embeddings key) and degrades to a keyword scorer if chromadb
isn't installed. Rebuild the index after content edits:
`python3 -m graph.retrieval --build`.
"""

from __future__ import annotations

from .. import retrieval
from ..config import RETRIEVER_TOP_K
from ..history import last_user_turn
from ..state import DebateState


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
    passages = retrieval.search(query, RETRIEVER_TOP_K)
    return {"retrieved": passages}
