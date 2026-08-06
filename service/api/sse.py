"""Framework-free helpers for the live API (AI-SPEC.md §5, Phase 2).

Kept separate from app.py so the SSE formatting and validation are testable
without importing FastAPI or the LLM stack.
"""

from __future__ import annotations

import json

PERSONAS = ("jw-unitarian", "muslim", "skeptic", "seeker")

# Map a transcript turn's role to the SSE event name the frontend listens for.
ROLE_EVENT = {
    "interlocutor": "interlocutor",  # the objection, voiced in persona
    "apologist": "draft",            # an apologist draft (may repeat on retry)
    "system": "progress",            # verifier / guardrail / synth notes
}


def format_event(name: str, data: dict) -> str:
    """One Server-Sent Event frame."""
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def validate_persona(persona: str) -> str | None:
    """Return an error message if the persona is unknown, else None."""
    if persona not in PERSONAS:
        return f"unknown persona {persona!r}; choose one of {', '.join(PERSONAS)}"
    return None
