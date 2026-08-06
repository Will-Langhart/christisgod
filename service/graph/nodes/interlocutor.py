"""Interlocutor — voices the strongest *honest* form of the objection, in the
loaded persona (AI-SPEC.md §3). Uses the faster model.

The persona brief (service/theology/personas/<persona>.md) IS the system prompt's
backbone. The wrapper text below is a DRAFT — refine it alongside the briefs.
"""

from __future__ import annotations

from functools import lru_cache

from .._llm import call_llm
from ..config import INTERLOCUTOR_MODEL, INTERLOCUTOR_TEMPERATURE, PERSONAS_DIR
from ..state import DebateState


@lru_cache(maxsize=8)
def load_persona(persona: str) -> str:
    return (PERSONAS_DIR / f"{persona}.md").read_text("utf-8")


# DRAFT — author's review. Wraps the persona brief with the steelman rule.
_SYSTEM = """You are role-playing an interlocutor in a good-faith theological \
dialogue, so that a Christian apologetic can be tested against the strongest \
honest form of an objection.

Follow this persona brief exactly. Voice the objection as the tradition's *best* \
advocates would — never a strawman, never mockery. Concede genuine difficulties. \
Stay in character; do not secretly argue the Christian side. Do not misquote the \
Bible. You may cite your tradition's own sources (Qur'an, NWT, a named scholar) \
as clearly attributed claims.

--- PERSONA BRIEF ---
{brief}
--- END BRIEF ---

Raise ONE focused objection, in your own voice, in 3–6 sentences."""


def interlocutor(state: DebateState) -> dict:
    brief = load_persona(state["persona"])
    user = f"The topic to press: {state['objection']}"
    content = call_llm(
        INTERLOCUTOR_MODEL,
        _SYSTEM.format(brief=brief),
        user,
        temperature=INTERLOCUTOR_TEMPERATURE,
    )
    return {"transcript": [{"role": "interlocutor", "content": content}]}
