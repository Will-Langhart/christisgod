"""OrthodoxyGuardrail — LLM-as-judge against the heresy taxonomy (AI-SPEC.md §4).

This is the system's weakest link by design: an LLM judging orthodoxy is itself
fallible. Mitigations here: temperature 0, an explicit written rubric, a
structured verdict, and — critically — the taxonomy's §3 "do not flag legitimate
distinctions" section, which prevents the common false-positive of flagging
orthodox talk of the economic order / 'the Father is greater' / eternal generation.

DRAFT judge prompt — refine with the author.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache

from .._llm import call_llm
from ..config import GUARDRAIL_MODEL, GUARDRAIL_TEMPERATURE, TAXONOMY_PATH
from ..state import DebateState


@lru_cache(maxsize=1)
def load_taxonomy() -> str:
    return TAXONOMY_PATH.read_text("utf-8")


# DRAFT — author's review.
_SYSTEM = """You are an orthodoxy reviewer. Judge whether the ANSWER stays within \
historic Nicene/Chalcedonian Christian orthodoxy, using ONLY the rubric below.

Judge conservatively but fairly: FAIL only if the answer *asserts or clearly \
implies* one of the errors (H1–H12), or *denies* a required affirmation. Do NOT \
fail an answer for discussing an error in order to refute it, and do NOT fail the \
legitimate distinctions in §3 of the rubric (economic order, 'the Father is \
greater', Jesus praying, eternal generation, 'firstborn' as supremacy).

--- RUBRIC ---
{rubric}
--- END RUBRIC ---

Respond with ONLY a JSON object:
{{"verdict": "PASS" | "FAIL", "flagged": ["H#", ...], "missing_affirmations": \
[int, ...], "rationale": "one paragraph; quote the offending phrase if FAIL"}}"""


def _parse_verdict(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        # Fail closed: an unparseable judge verdict is treated as not-approved.
        return {"verdict": "FAIL", "flagged": [], "missing_affirmations": [],
                "rationale": f"unparseable guardrail output: {text[:200]}"}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"verdict": "FAIL", "flagged": [], "missing_affirmations": [],
                "rationale": "guardrail returned invalid JSON"}


def orthodoxy_guardrail(state: DebateState) -> dict:
    user = f"ANSWER TO JUDGE:\n{state.get('draft', '')}"
    raw = call_llm(
        GUARDRAIL_MODEL,
        _SYSTEM.format(rubric=load_taxonomy()),
        user,
        temperature=GUARDRAIL_TEMPERATURE,
    )
    verdict = _parse_verdict(raw)
    ok = verdict.get("verdict") == "PASS"
    report = json.dumps(verdict, ensure_ascii=False)

    update: dict = {"orthodoxy_ok": ok, "orthodoxy_report": report}
    if not ok:
        update["retries"] = state.get("retries", 0) + 1
        update["orthodoxy_feedback"] = verdict.get("rationale", "orthodoxy check failed")
        update["transcript"] = [
            {"role": "system", "content": f"[guardrail] FAIL: {verdict.get('rationale', '')}"}
        ]
    return update
