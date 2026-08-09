"""Interlocutor — voices the strongest *honest* form of the objection, in the
loaded persona (AI-SPEC.md §3). Uses the faster model.

The persona brief (service/theology/personas/<persona>.md) IS the system prompt's
backbone. The wrapper text below is a DRAFT — refine it alongside the briefs.
"""

from __future__ import annotations

from functools import lru_cache

from .._llm import call_llm
from ..config import INTERLOCUTOR_MODEL, INTERLOCUTOR_TEMPERATURE, PERSONAS_DIR
from ..history import render, window
from ..state import DebateState


@lru_cache(maxsize=8)
def load_persona(persona: str) -> str:
    return (PERSONAS_DIR / f"{persona}.md").read_text("utf-8")


_STEELMAN = """Follow this persona brief exactly. Voice the objection as the \
tradition's *best* advocates would — never a strawman, never mockery. Concede \
genuine difficulties. Stay in character; do not secretly argue the Christian side. \
Do not misquote the Bible. You may cite your tradition's own sources (Qur'an, NWT, \
a named scholar) as clearly attributed claims.

--- PERSONA BRIEF ---
{brief}
--- END BRIEF ---"""

# Phase 1/2 offline path: raise ONE cold objection to seed the debate.
_SYSTEM = """You are role-playing an interlocutor in a good-faith theological \
dialogue, so that a Christian apologetic can be tested against the strongest \
honest form of an objection.

{steelman}

Raise ONE focused objection, in your own voice, in 3–6 sentences."""

# Phase 3 debate mode: a live sparring partner. The READER is defending the deity
# of Christ; you press them, in persona, using the conversation so far.
_SYSTEM_CONVERSATIONAL = """You are role-playing a live interlocutor sparring with \
a reader who is defending the claim that Jesus Christ is God. Your job is to press \
them — as the tradition's most thoughtful advocate — so they can test that case.

{steelman}

Respond to the reader's latest point directly and stay in character. Acknowledge a \
fair point when they make one, then press the strongest remaining difficulty. Keep \
it to 3–6 sentences — this is a conversation, not a lecture. Never break character \
to concede that Jesus is God."""


def interlocutor(state: DebateState) -> dict:
    brief = load_persona(state["persona"])
    steelman = _STEELMAN.format(brief=brief)

    if state.get("user_message"):
        # Conversational debate: respond to the reader, in persona. Set `draft`
        # so the deterministic scripture gate runs over the interlocutor's text
        # (even the skeptic may not fabricate a verse reference).
        parts = []
        recent, truncated = window(state.get("history"))
        convo = render(recent, truncated)
        if convo:
            parts.append(f"CONVERSATION SO FAR:\n{convo}\n")
        parts.append(f"THE READER JUST SAID:\n{state['user_message']}")
        if state.get("verify_feedback"):
            parts.append(f"\nYour previous reply cited Scripture that failed \
verification:\n{state['verify_feedback']}\nQuote only real references, accurately, \
and try again.")
        content = call_llm(
            INTERLOCUTOR_MODEL, _SYSTEM_CONVERSATIONAL.format(steelman=steelman),
            "\n".join(parts), temperature=INTERLOCUTOR_TEMPERATURE,
        )
        return {"draft": content,
                "transcript": [{"role": "interlocutor", "content": content}]}

    # Phase 1/2 single-shot: one cold objection (apologist overwrites `draft`).
    content = call_llm(
        INTERLOCUTOR_MODEL, _SYSTEM.format(steelman=steelman),
        f"The topic to press: {state['objection']}",
        temperature=INTERLOCUTOR_TEMPERATURE,
    )
    return {"transcript": [{"role": "interlocutor", "content": content}]}
