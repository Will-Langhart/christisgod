"""Retriever node — returns the chapter passages most relevant to the objection.

Thin wrapper over graph.retrieval.search, which uses a Chroma embedding index
(local model, no embeddings key) and degrades to a keyword scorer if chromadb
isn't installed. Rebuild the index after content edits:
`python3 -m graph.retrieval --build`.
"""

from __future__ import annotations

from .. import retrieval
from ..config import RETRIEVER_TOP_K
from ..state import DebateState


def retriever(state: DebateState) -> dict:
    passages = retrieval.search(state.get("objection", ""), RETRIEVER_TOP_K)
    return {"retrieved": passages}
