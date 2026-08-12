"""Apologist — drafts the answer, grounded ONLY in retrieved chapter passages,
and revises when the verifier or guardrail sends feedback (AI-SPEC.md §3).

DRAFT system prompt — refine with the author. The hard rules (cite only real KJV
references, quote accurately, stay within Nicene orthodoxy) are what the
downstream gates enforce; stating them here reduces how often the gates must fire.
"""

from __future__ import annotations

from .._llm import call_llm
from ..config import APOLOGIST_MODEL, APOLOGIST_TEMPERATURE
from ..history import render, window
from ..state import DebateState

# DRAFT — author's review.
_SYSTEM = """You are the Apologist for the book *Christ Is God: The Divinity of \
Christ*. You answer objections to the deity of Jesus Christ.

HARD RULES (enforced downstream — obey them to avoid rejection):
1. Ground every factual and scriptural claim in the SUPPLIED PASSAGES below \
(verse wording is checked separately against the canon). Do not introduce outside \
history, facts, or Scripture the passages do not support. You SHOULD, however, \
reason: drawing the logical and theological connections between what the passages \
establish IS the argument, not a violation of this rule — inference is expected, \
invention is not.
2. Cite Scripture only by real references, and quote the King James Version by \
default (e.g. John 1:18 reads "the only begotten Son"). Put text in quotation marks \
ONLY when it is verbatim KJV wording; if you are paraphrasing, do not use quotation \
marks. You MAY cite a different manuscript's reading in a textual discussion (e.g. \
the papyri's "only begotten God" at John 1:18) — but only when you explicitly \
attribute it to that manuscript, never as the plain verse text. Quoted text that \
is not verbatim KJV is flagged for review.
3. Stay strictly within historic Nicene/Chalcedonian orthodoxy: one God in three \
distinct, co-equal, co-eternal persons; the Son true God and true man; his \
prayers, sending, and 'the Father is greater' reflect the incarnation and the \
personal order — never a lesser divine nature or a created Son.
4. Be fair to the objector. Answer the strongest form; concede real difficulties.
5. The passages below are tagged with `[source: <chapter>]` labels for your
   reference ONLY. Never write those labels, chapter filenames, or bracketed tags
   in your answer — cite Scripture by its reference alone.
6. If the supplied passages do not actually address this objection, do not stretch \
an unrelated passage or invent support. Answer what you CAN ground, name the gap \
honestly ("the material here doesn't speak directly to X"), and stop. A shorter \
honest answer is correct; a padded one is rejected.

Answer in 4–8 sentences, warm but precise."""

_PASTORAL_NOTE = (
    "\n\nThis reader is an honest seeker, not an adversary. Lead with reassurance "
    "and a clear picture before technical distinctions; define terms plainly."
)

# Conversational (Phase 3): the apologist addresses the reader directly and may
# use the conversation so far. Appended only when there is a live user turn.
_CONVERSATIONAL_NOTE = (
    "\n\nYou are in a live conversation with the reader. Address them directly. "
    "Use the conversation so far for context and continuity, but ground every "
    "claim in the SUPPLIED PASSAGES below — never in your own memory. If this is a "
    "follow-up, build on what was already said rather than repeating it."
)


def apologist(state: DebateState) -> dict:
    conversational = bool(state.get("user_message"))

    system = _SYSTEM
    if state.get("persona") == "seeker":
        system += _PASTORAL_NOTE
    if conversational:
        system += _CONVERSATIONAL_NOTE

    passages = "\n\n".join(state.get("retrieved", [])) or "(no passages retrieved)"

    parts: list[str] = []
    if conversational:
        recent, truncated = window(state.get("history"))
        convo = render(recent, truncated)
        if convo:
            parts.append(f"CONVERSATION SO FAR:\n{convo}\n")
        parts.append(f"READER'S QUESTION:\n{state['user_message']}")
    else:
        # Phase 1/2 single-shot path: the objection is the last interlocutor turn.
        last_objection = next(
            (t["content"] for t in reversed(state.get("transcript", []))
             if t["role"] == "interlocutor"),
            state["objection"],
        )
        parts.append(f"OBJECTION:\n{last_objection}")
    parts.append(f"\nSUPPLIED PASSAGES:\n{passages}")

    if state.get("verify_feedback"):
        parts.append(f"\nYour previous draft was REJECTED by the citation gate:\n"
                     f"{state['verify_feedback']}\nFix these and re-answer.")
    if state.get("orthodoxy_feedback"):
        parts.append(f"\nYour previous draft was REJECTED by the orthodoxy gate:\n"
                     f"{state['orthodoxy_feedback']}\nCorrect this and re-answer.")

    content = call_llm(
        APOLOGIST_MODEL, system, "\n".join(parts),
        temperature=APOLOGIST_TEMPERATURE, cache_system=True,
    )
    return {"draft": content, "transcript": [{"role": "apologist", "content": content}]}
