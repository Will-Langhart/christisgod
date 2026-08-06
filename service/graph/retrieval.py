"""Retrieval over the 17 MDX chapters for the Apologist's grounding.

Primary path: a persistent Chroma collection embedded with Chroma's default
local model (ONNX MiniLM) — no embeddings API key, fine for a ~90 KB corpus.
Fallback path: a dependency-free keyword scorer, used automatically if chromadb
isn't installed, so the graph still runs (and the deterministic tests never pull
the embedding stack). chromadb is imported lazily for exactly that reason.

Rebuild the index after editing chapter content:
    python3 -m graph.retrieval --build          # build if empty
    python3 -m graph.retrieval --build --force   # wipe and rebuild
"""

from __future__ import annotations

import re

from .config import CHROMA_COLLECTION, CHROMA_DIR, CONTENT_DIR, RETRIEVER_TOP_K

# --- chunking (shared by both paths) --------------------------------------

_SKIP_PREFIXES = ("import", "export", "<", "#", "{")


def chunks() -> list[tuple[str, str, str]]:
    """Return (chunk_id, text, chapter_stem) for every prose paragraph."""
    out: list[tuple[str, str, str]] = []
    for path in sorted(CONTENT_DIR.glob("*.mdx")):
        stem = path.stem
        for i, para in enumerate(path.read_text("utf-8").split("\n\n")):
            para = para.strip()
            if len(para) > 120 and not para.startswith(_SKIP_PREFIXES):
                out.append((f"{stem}#{i}", para, stem))
    return out


# --- keyword fallback ------------------------------------------------------

_WORD_RE = re.compile(r"[a-z]{4,}")
# Terms too common in *this* corpus to discriminate between chapters.
_STOP = {"that", "this", "with", "from", "have", "does", "said", "they", "what",
         "when", "would", "which", "there", "their", "about", "jesus", "christ",
         "god", "lord", "father", "which", "these", "those", "shall"}


def _terms(text: str) -> set[str]:
    return {w for w in _WORD_RE.findall(text.lower()) if w not in _STOP}


def _keyword_search(query: str, k: int) -> list[str]:
    q = _terms(query)
    scored = []
    for _cid, text, stem in chunks():
        overlap = len(q & _terms(text))
        if overlap:
            scored.append((overlap, stem, text))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [f"[source: {stem}]\n{text}" for _s, stem, text in scored[:k]]


# --- Chroma path -----------------------------------------------------------

_collection = None  # cached handle within a process


def _get_collection(force: bool = False):
    """Lazily import chromadb, (re)build the collection if needed, return it."""
    global _collection
    if _collection is not None and not force:
        return _collection

    import chromadb  # lazy — keeps the fallback and tests dependency-free

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if force:
        try:
            client.delete_collection(CHROMA_COLLECTION)
        except Exception:  # noqa: BLE001 — fine if it didn't exist
            pass
    col = client.get_or_create_collection(CHROMA_COLLECTION)

    if col.count() == 0:
        rows = chunks()
        col.add(
            ids=[cid for cid, _t, _s in rows],
            documents=[t for _c, t, _s in rows],
            metadatas=[{"chapter": s} for _c, _t, s in rows],
        )
    _collection = col
    return col


def search(query: str, k: int = RETRIEVER_TOP_K) -> list[str]:
    """Top-k chapter passages for a query, as ``"[chapter] text"`` strings.

    Uses Chroma if available; otherwise the keyword fallback. Never raises on a
    missing embedding stack — it degrades.
    """
    try:
        col = _get_collection()
    except ImportError:
        return _keyword_search(query, k)

    res = col.query(query_texts=[query], n_results=k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return [f"[source: {(m or {}).get('chapter', '?')}]\n{d}" for d, m in zip(docs, metas)]


def build_index(force: bool = False) -> int:
    """Build/rebuild the Chroma index; return the chunk count. Requires chromadb."""
    col = _get_collection(force=force)
    return col.count()


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if args.build:
        n = build_index(force=args.force)
        print(f"✓ indexed {n} chunks → {CHROMA_DIR} ({CHROMA_COLLECTION})")
    else:
        for line in search("Was Jesus created? firstborn of creation"):
            print("·", line[:100])
