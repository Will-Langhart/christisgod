"""Apologist — drafts the answer, grounded ONLY in retrieved chapter passages,
and revises when the verifier or guardrail sends feedback (AI-SPEC.md §3).

DRAFT system prompt — refine with the author. The hard rules (cite only real KJV
references, quote accurately, stay within Nicene orthodoxy) are what the
downstream gates enforce; stating them here reduces how often the gates must fire.
"""

from __future__ import annotations

from .._llm import call_llm
from ..config import APOLOGIST_MODEL, APOLOGIST_TEMPERATURE
from ..state import DebateState

# DRAFT — author's review.
_SYSTEM = """You are the Apologist for the book *Christ Is God: The Divinity of \
Christ*. You answer objections to the deity of Jesus Christ.

HARD RULES (enforced downstream — obey them to avoid rejection):
1. Ground every claim in the SUPPLIED PASSAGES below. Do not introduce material \
that is not supported by them.
2. Cite Scripture only by real references, and when you quote a verse, quote the \
King James Version accurately. A fabricated or misquoted reference fails.
3. Stay strictly within historic Nicene/Chalcedonian orthodoxy: one God in three \
distinct, co-equal, co-eternal persons; the Son true God and true man; his \
prayers, sending, and 'the Father is greater' reflect the incarnation and the \
personal order — never a lesser divine nature or a created Son.
4. Be fair to the objector. Answer the strongest form; concede real difficulties.

Answer in 4–8 sentences, warm but precise."""

_PASTORAL_NOTE = (
    "\n\nThis objector is an honest seeker, not an adversary. Lead with reassurance "
    "and a clear picture before technical distinctions; define terms plainly."
)


def apologist(state: DebateState) -> dict:
    system = _SYSTEM + (_PASTORAL_NOTE if state.get("persona") == "seeker" else "")

    passages = "\n\n".join(state.get("retrieved", [])) or "(no passages retrieved)"
    last_objection = next(
        (t["content"] for t in reversed(state.get("transcript", []))
         if t["role"] == "interlocutor"),
        state["objection"],
    )

    parts = [f"OBJECTION:\n{last_objection}", f"\nSUPPLIED PASSAGES:\n{passages}"]
    if state.get("verify_feedback"):
        parts.append(f"\nYour previous draft was REJECTED by the citation gate:\n"
                     f"{state['verify_feedback']}\nFix these and re-answer.")
    if state.get("orthodoxy_feedback"):
        parts.append(f"\nYour previous draft was REJECTED by the orthodoxy gate:\n"
                     f"{state['orthodoxy_feedback']}\nCorrect this and re-answer.")

    content = call_llm(
        APOLOGIST_MODEL, system, "\n".join(parts), temperature=APOLOGIST_TEMPERATURE
    )
    return {"draft": content, "transcript": [{"role": "apologist", "content": content}]}
