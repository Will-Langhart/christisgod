"""Tests the framework-free API helpers (api/sse.py) — no FastAPI, no LLM stack."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.sse import PERSONAS, format_event, validate_persona  # noqa: E402


def test_format_event_is_valid_sse_frame():
    frame = format_event("done", {"status": "approved", "answer": "hi"})
    assert frame.startswith("event: done\ndata: ")
    assert frame.endswith("\n\n")
    payload = frame.split("data: ", 1)[1].strip()
    assert json.loads(payload) == {"status": "approved", "answer": "hi"}


def test_format_event_preserves_unicode():
    frame = format_event("turn", {"content": "“My Lord and my God”"})
    assert "“My Lord and my God”" in frame  # ensure_ascii=False


def test_validate_persona_accepts_known():
    for p in PERSONAS:
        assert validate_persona(p) is None


def test_validate_persona_rejects_unknown():
    msg = validate_persona("atheist")
    assert msg and "unknown persona" in msg


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
