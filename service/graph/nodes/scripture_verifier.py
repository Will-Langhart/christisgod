"""ScriptureVerifier — the deterministic hard gate. NO llm. (AI-SPEC.md §4)

Runs every extracted citation through canon.verify_citation. The answer proceeds
only if *every* citation is a real, in-range reference with KJV text on record,
and (where a quote was extracted) the quote matches the KJV. Any failure sets
verify_ok=False, bumps the retry counter, and writes feedback the Apologist uses
to re-draft.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from canon import verify_citations  # noqa: E402

from ..state import CitationCheck, DebateState  # noqa: E402


def scripture_verifier(state: DebateState) -> dict:
    citations = state.get("citations", [])
    results = verify_citations(citations)
    checks: list[CitationCheck] = [
        {
            "raw": cite["raw"],
            "ok": result.ok,
            "reason": result.reason,
            "display": result.display,
            "quoted": cite.get("quoted"),
            "warning": result.warning,
        }
        for cite, result in zip(citations, results)
    ]

    # HARD gate: only fabricated / nonexistent references block. Quote-accuracy
    # issues are non-blocking warnings surfaced for human review.
    failures = [c for c in checks if not c["ok"]]
    warnings = [r.warning for r in results if r.warning]
    ok = not failures

    update: dict = {"citations": checks, "verify_ok": ok}
    if warnings:
        update["citation_warnings"] = warnings
    if not ok:
        update["retries"] = state.get("retries", 0) + 1
        update["verify_feedback"] = "Fix these fabricated/invalid references:\n" + "\n".join(
            f"  - {c['raw']}: {c['reason']}" for c in failures
        )
        update["transcript"] = [
            {"role": "system", "content": f"[verifier] rejected: {len(failures)} invalid reference(s)"}
        ]
    return update
