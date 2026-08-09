"""Deterministic tests for the Phase 3 conversational layer (AI-SPEC.md §9).

No LLM, no network. Covers history windowing, Triage's post-parse routing logic,
the deflect terminal, and the chat-graph wiring (`_after_triage`).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from graph.build import _after_triage  # noqa: E402
from graph.history import last_user_turn, render, window  # noqa: E402
from graph.nodes.terminal import deflect  # noqa: E402
from graph.nodes.triage import _parse  # noqa: E402


def _convo(n: int):
    return [{"role": "user" if i % 2 == 0 else "assistant", "content": f"t{i}"} for i in range(n)]


# --- windowing -------------------------------------------------------------

def test_window_keeps_all_when_under_limit():
    hist = _convo(4)
    kept, truncated = window(hist, keep=6)
    assert kept == hist and truncated is False


def test_window_trims_and_flags_when_over_limit():
    hist = _convo(10)
    kept, truncated = window(hist, keep=6)
    assert len(kept) == 6 and truncated is True
    assert kept[0]["content"] == "t4"  # kept the *last* six


def test_window_handles_none():
    kept, truncated = window(None)
    assert kept == [] and truncated is False


def test_render_labels_roles_and_notes_truncation():
    out = render([{"role": "user", "content": "why did he pray?"},
                  {"role": "assistant", "content": "the incarnation"}], truncated=True)
    assert "(earlier context omitted)" in out
    assert "Reader: why did he pray?" in out
    assert "Apologist: the incarnation" in out


def test_render_empty_is_blank():
    assert render([]) == ""


def test_last_user_turn_finds_most_recent_user():
    hist = [{"role": "user", "content": "first"},
            {"role": "assistant", "content": "reply"},
            {"role": "user", "content": "second"},
            {"role": "assistant", "content": "reply2"}]
    assert last_user_turn(hist) == "second"


# --- triage parsing --------------------------------------------------------

def test_parse_extracts_embedded_json():
    v = _parse('Sure: {"on_topic": true, "intent": "objection", "reason": "x"} done')
    assert v["on_topic"] is True and v["intent"] == "objection"


def test_parse_returns_empty_on_garbage():
    assert _parse("no json here") == {}


# --- routing ---------------------------------------------------------------

def test_after_triage_routes_offtopic_to_deflect():
    assert _after_triage({"guard_ok": False}) == "deflect"


def test_after_triage_routes_ontopic_to_retriever():
    assert _after_triage({"guard_ok": True}) == "retriever"


def test_after_triage_defaults_to_retriever():
    # Missing guard_ok (e.g. the Phase 1/2 path) must not deflect.
    assert _after_triage({}) == "retriever"


# --- deflect terminal ------------------------------------------------------

def test_deflect_emits_no_scripture_claim():
    out = deflect({})
    assert out["status"] == "deflected"
    assert out["final"]
    # A deflection must never carry a verse reference (nothing to verify).
    import re
    assert not re.search(r"\b[A-Z][a-z]+ \d+:\d+\b", out["final"])


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
