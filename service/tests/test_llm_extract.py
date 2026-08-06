"""Tests _extract_text — flattening Claude 5 structured content (thinking + text
blocks) to plain text. No LLM/network; pure function."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from graph._llm import _extract_text  # noqa: E402


def test_plain_string_passthrough():
    assert _extract_text("hello") == "hello"


def test_list_keeps_text_drops_thinking():
    content = [
        {"type": "thinking", "thinking": "", "signature": "EuENC-base64-blob"},
        {"type": "text", "text": "The real answer."},
    ]
    assert _extract_text(content) == "The real answer."


def test_list_concatenates_multiple_text_blocks():
    content = [{"type": "text", "text": "A "}, {"type": "text", "text": "B"}]
    assert _extract_text(content) == "A B"


def test_no_thinking_signature_leaks():
    content = [{"type": "thinking", "signature": "SECRET"}, {"type": "text", "text": "ok"}]
    out = _extract_text(content)
    assert "SECRET" not in out and out == "ok"


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
