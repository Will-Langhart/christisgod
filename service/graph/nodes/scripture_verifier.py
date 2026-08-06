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
        }
        for cite, result in zip(citations, results)
    ]

    failures = [c for c in checks if not c["ok"]]
    ok = not failures

    update: dict = {"citations": checks, "verify_ok": ok}
    if not ok:
        update["retries"] = state.get("retries", 0) + 1
        update["verify_feedback"] = "Citation problems to fix:\n" + "\n".join(
            f"  - {c['raw']}: {c['reason']}" for c in failures
        )
        update["transcript"] = [
            {"role": "system", "content": f"[verifier] rejected: {len(failures)} bad citation(s)"}
        ]
    return update
