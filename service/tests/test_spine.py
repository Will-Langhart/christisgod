"""Exercises the DETERMINISTIC spine — citation_extractor → scripture_verifier →
synthesizer — with NO llm and NO langgraph. Proves the hard gate rejects a
fabricated citation inside a realistic draft and passes a clean one.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from graph.nodes.citation_extractor import citation_extractor  # noqa: E402
from graph.nodes.scripture_verifier import scripture_verifier  # noqa: E402
from graph.nodes.synthesizer import synthesizer  # noqa: E402


def _run_gate(draft: str) -> dict:
    state = {"draft": draft}
    state.update(citation_extractor(state))
    state.update(scripture_verifier(state))
    return state


def test_extractor_finds_references():
    state = {"draft": "As John 1:1 and Colossians 1:16 show, the Son is Creator."}
    out = citation_extractor(state)
    raws = {c["raw"] for c in out["citations"]}
    assert "John 1:1" in raws
    assert "Colossians 1:16" in raws


def test_clean_draft_passes_gate():
    draft = 'Thomas confessed, "My Lord and my God" (John 20:28), addressing Jesus as God.'
    state = _run_gate(draft)
    assert state["verify_ok"], state.get("verify_feedback")


def test_nonexistent_verse_is_rejected():
    # John 4 has no verse 99 — the full-KJV store rejects fabricated verse numbers.
    draft = "Scripture plainly says Jesus is God (John 4:99)."
    state = _run_gate(draft)
    assert not state["verify_ok"]
    assert state["retries"] == 1


def test_verse_outside_the_book_now_verifies():
    # Gethsemane (Matthew 26:39) — not quoted in the book, but a real KJV verse.
    draft = 'Jesus prayed, "let this cup pass from me" (Matthew 26:39).'
    state = _run_gate(draft)
    assert state["verify_ok"], state.get("verify_feedback")


def test_out_of_range_reference_is_rejected():
    draft = "See Ephesians 18:2 for the divine claim."
    state = _run_gate(draft)
    assert not state["verify_ok"]


def test_misquote_warns_but_passes_gate():
    # The reference (John 1:1) is real, so the gate passes; the bogus quote is
    # surfaced as a non-blocking warning for human review.
    draft = 'John 1:1 reads, "the Word was a god," proving subordination.'
    state = _run_gate(draft)
    assert state["verify_ok"]
    assert state.get("citation_warnings")


def test_synthesizer_collects_verified_refs():
    draft = "The Word was God (John 1:1)."
    state = _run_gate(draft)
    assert state["verify_ok"]
    out = synthesizer(state)
    assert out["final"] == draft


def test_synthesizer_strips_leaked_source_tags():
    draft = "As [source: 11-xii-the-manuscript] and [13-xiv-objections] show, John 1:1."
    out = synthesizer({"draft": draft, "citations": []})
    assert "source:" not in out["final"]
    assert "11-xii" not in out["final"] and "13-xiv" not in out["final"]


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
