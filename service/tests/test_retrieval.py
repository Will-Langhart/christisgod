"""Retrieval tests that need NO embedding stack — they exercise chunking and the
keyword fallback path (search() degrades to it when chromadb isn't installed).
The Chroma path is covered by a live run once requirements are installed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from graph import retrieval  # noqa: E402


def test_chunks_are_extracted_from_all_chapters():
    rows = retrieval.chunks()
    assert len(rows) > 40  # 17 chapters, several prose paragraphs each
    chapters = {stem for _cid, _t, stem in rows}
    assert len(chapters) >= 15
    # No MDX scaffolding leaked in as a chunk.
    assert all(not t.lstrip().startswith(("import", "<", "#")) for _c, t, _s in rows)


def test_keyword_search_is_relevant():
    hits = retrieval._keyword_search("firstborn of creation, was the Son created?", 5)
    assert hits
    joined = " ".join(hits).lower()
    assert "firstborn" in joined or "creation" in joined


def test_search_degrades_without_chromadb():
    # On a host without chromadb, search() must still return results (fallback),
    # not raise. (When chromadb IS installed this exercises the Chroma path.)
    hits = retrieval.search("worship given to Christ", 4)
    assert isinstance(hits, list) and hits


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except Exception:  # noqa: BLE001
            failed += 1
            print(f"  ✗ {t.__name__}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
