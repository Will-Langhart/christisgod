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


def test_full_kjv_verse_outside_the_book_resolves():
    # Matthew 26:39 (Gethsemane) isn't quoted in the book, but the full-KJV store
    # must still verify it — the apologist may cite any real verse.
    r = verify_citation("Matthew 26:39", "let this cup pass from me")
    assert r.ok, r.reason


def test_verse_range_resolves():
    assert "firstborn" in (lookup_verse("Colossians 1:15-17") or "")


def test_quote_ignores_punctuation_and_case():
    r = verify_citation("John 1:1", "In the beginning was the WORD,")
    assert r.ok, r.reason


def test_misquote_warns_but_does_not_block():
    # A non-verbatim quote near a REAL reference is a warning, not a hard failure.
    r = verify_citation("John 1:1", "the Word was a god")
    assert r.ok  # reference is real → not blocked
    assert r.warning is not None  # but flagged for review


def test_real_quote_with_slightly_wrong_verse_number_passes():
    # "all things consist" is Colossians 1:17; attaching it to 1:16 is an
    # attribution slip, not a fabrication — it must not hard-block.
    r = verify_citation("Colossians 1:16", "by him all things consist")
    assert r.ok, r.reason


def test_nonexistent_verse_number_fails():
    # John 4 exists but has no verse 99 — the full-KJV store catches bad numbers.
    r = verify_citation("John 4:99")
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
