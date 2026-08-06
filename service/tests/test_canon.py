"""Proves the deterministic gate in canon.py. Run: python3 -m pytest (or the
plain-stdlib runner at the bottom, so no deps are required for Phase 0)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from canon import parse_ref, lookup_verse, verify_citation  # noqa: E402


def test_parses_valid_reference():
    p = parse_ref("John 20:28")
    assert p is not None
    assert p.book == "John"
    assert p.display == "John 20:28"


def test_parses_numbered_book_and_abbreviation():
    assert parse_ref("1 Corinthians 8:6").book == "1 Corinthians"
    assert parse_ref("Phil. 2:6").book == "Philippians"


def test_rejects_out_of_range_lookalike():
    # Biblical Ephesians has 6 chapters; Ignatius "to the Ephesians 18:2" is not it.
    assert parse_ref("Ephesians 18:2") is None


def test_rejects_unknown_book():
    assert parse_ref("Nephi 3:7") is None


def test_lookup_returns_kjv_text():
    assert "the Word was God" in (lookup_verse("John 1:1") or "")


def test_correct_quote_passes():
    r = verify_citation("John 1:1", "the Word was God")
    assert r.ok, r.reason


def test_quote_ignores_punctuation_and_case():
    r = verify_citation("John 1:1", "In the beginning was the WORD,")
    assert r.ok, r.reason


def test_misquote_fails():
    r = verify_citation("John 1:1", "the Word was a god")
    assert not r.ok


def test_fabricated_reference_fails():
    r = verify_citation("John 4:12", "Jesus is God")  # John 4:12 is not in corpus
    assert not r.ok


def test_out_of_range_reference_fails():
    r = verify_citation("Ephesians 18:2", "anything")
    assert not r.ok


if __name__ == "__main__":
    # Zero-dependency runner so Phase 0 verifies without pytest installed.
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
