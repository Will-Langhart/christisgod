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

import math
import re

from .config import (
    CHROMA_COLLECTION,
    CHROMA_DIR,
    CONTENT_DIR,
    RETRIEVER_FETCH_K,
    RETRIEVER_MMR_LAMBDA,
    RETRIEVER_TOP_K,
)

# --- chunking (shared by both paths) --------------------------------------

# Non-prose lines we never want as a chunk. Headings ("#") are handled
# separately below — tracked as section context, not skipped blindly.
_SKIP_PREFIXES = ("import", "export", "<", "{")
_ROMAN_RE = re.compile(r"^[ivxlcdm]+$")


def _chapter_title(stem: str) -> str:
    """Human title from a filename stem, e.g. ``03-iv-jesus-is-god`` → "Jesus Is
    God". Drops the leading order number and roman-numeral tokens."""
    parts = stem.split("-")
    while parts and (parts[0].isdigit() or _ROMAN_RE.match(parts[0])):
        parts.pop(0)
    return " ".join(w.capitalize() for w in parts) or stem


def chunks() -> list[tuple[str, str, str]]:
    """Return (chunk_id, text, chapter_stem) for every prose paragraph.

    Each chunk's text is prefixed with a plain-language context line — the
    chapter title and the nearest ``##`` section heading — so both the embedding
    and the keyword scorer see where the paragraph sits in the argument, and so
    the Apologist reading the passage knows its section. The prefix deliberately
    avoids a leading ``#`` so the paragraph still reads as prose.
    """
    out: list[tuple[str, str, str]] = []
    for path in sorted(CONTENT_DIR.glob("*.mdx")):
        stem = path.stem
        title = _chapter_title(stem)
        section: str | None = None
        for i, para in enumerate(path.read_text("utf-8").split("\n\n")):
            para = para.strip()
            if not para:
                continue
            if para.startswith("#"):  # a heading — remember it, don't emit it
                section = para.lstrip("#").strip()
                continue
            if para.startswith(_SKIP_PREFIXES) or len(para) <= 120:
                continue
            ctx = f"{title} — {section}" if section else title
            out.append((f"{stem}#{i}", f"Chapter: {ctx}\n{para}", stem))
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


# --- MMR rerank (deterministic, no extra model call) -----------------------

def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def _mmr(distances: list[float], vectors: list[list[float]], k: int,
         lambda_: float = RETRIEVER_MMR_LAMBDA) -> list[int]:
    """Maximal Marginal Relevance selection over an over-retrieved candidate set.

    Balances relevance (from Chroma's distances — smaller is closer, so we invert
    and min-max normalise to [0,1]) against redundancy (max cosine similarity to
    an already-picked passage). Returns the chosen indices, in pick order. Pure
    Python, deterministic, no embedding-model call. Degrades to plain top-k if the
    candidate vectors are unusable.
    """
    n = len(vectors)
    k = min(k, n)
    if k <= 0:
        return []
    lo, hi = min(distances), max(distances)
    span = (hi - lo) or 1.0
    relevance = [(hi - d) / span for d in distances]  # 1.0 = nearest, 0.0 = farthest

    selected: list[int] = []
    candidates = list(range(n))
    while candidates and len(selected) < k:
        best_i, best_score = candidates[0], None
        for i in candidates:
            redundancy = max(
                ((_cosine(vectors[i], vectors[j]) + 1.0) / 2.0 for j in selected),
                default=0.0,
            )
            score = lambda_ * relevance[i] - (1.0 - lambda_) * redundancy
            if best_score is None or score > best_score:
                best_score, best_i = score, i
        selected.append(best_i)
        candidates.remove(best_i)
    return selected


def search(query: str, k: int = RETRIEVER_TOP_K, fetch_k: int | None = None) -> list[str]:
    """Top-k chapter passages for a query, as ``"[source: chapter] text"`` strings.

    Over-retrieves ``fetch_k`` candidates by embedding similarity, then reranks to
    ``k`` with MMR so the passages are relevant *and* non-redundant. Uses Chroma if
    available; otherwise the keyword fallback. Never raises on a missing embedding
    stack — it degrades, and if MMR cannot run it falls back to plain top-k order.
    """
    try:
        col = _get_collection()
    except ImportError:
        return _keyword_search(query, k)

    fetch_k = fetch_k or max(RETRIEVER_FETCH_K, k)
    res = col.query(
        query_texts=[query],
        n_results=fetch_k,
        include=["documents", "metadatas", "embeddings", "distances"],
    )
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    embs = res.get("embeddings", [[]])[0]

    order = list(range(len(docs)))
    if embs is not None and len(embs) == len(docs) and dists:
        vectors = [list(v) for v in embs]
        order = _mmr(list(dists), vectors, k)
    else:  # embeddings unavailable — keep Chroma's own top-k ordering
        order = order[:k]

    return [
        f"[source: {(metas[i] or {}).get('chapter', '?')}]\n{docs[i]}"
        for i in order
    ]


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
