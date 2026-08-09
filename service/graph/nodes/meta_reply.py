"""meta_reply — the light path for meta questions (AI-SPEC.md §9.1).

When Triage tags a turn `meta` ("who are you?", "what can I ask?", "be shorter"),
there is no scriptural claim to make, so we skip retrieval and both gates and
answer directly with the fast model. Like `deflect`, this node is trusted to emit
no verse claim — its system prompt forbids citing Scripture, which keeps the
hard-gate invariant ("nothing with a verse in it ships unverified") intact.
"""

from __future__ import annotations

from .._llm import call_llm
from ..config import TRIAGE_MODEL
from ..history import render, window
from ..state import DebateState

# DRAFT — author's review.
_SYSTEM = """You are the assistant for the book *Christ Is God: The Divinity of \
Christ*. Your one job is to help readers test the case that Jesus Christ is God, \
grounded in Scripture.

The reader has asked a META question — about you, your purpose, or how to use this \
chat — not a theological question. Answer it briefly (1–3 sentences), warmly, and \
plainly. Invite them to ask a real question about the deity of Christ.

Do NOT cite, quote, or reference any Bible verse in this reply — there is nothing \
to prove here, only to orient the reader."""


def meta_reply(state: DebateState) -> dict:
    parts = []
    recent, truncated = window(state.get("history"))
    convo = render(recent, truncated)
    if convo:
        parts.append(f"CONVERSATION SO FAR:\n{convo}\n")
    parts.append(f"READER'S MESSAGE:\n{state.get('user_message', '')}")

    content = call_llm(TRIAGE_MODEL, _SYSTEM, "\n".join(parts))
    return {
        "status": "approved",
        "final": content,
        "transcript": [{"role": "assistant", "content": content}],
    }
