"""Conversation-history windowing (AI-SPEC.md §9.4). Deterministic — NO llm.

Keeps the last `keep` turns verbatim and reports whether older turns were
dropped, so the apologist prompt can carry a one-line "(earlier context omitted)"
note. An LLM running-summary is the documented upgrade behind this same
signature — swap the body, keep the return shape.
"""

from __future__ import annotations

from .config import WINDOW_TURNS
from .state import ChatTurn


def window(history: list[ChatTurn] | None, keep: int = WINDOW_TURNS) -> tuple[list[ChatTurn], bool]:
    """Return (recent_turns, truncated).

    `recent_turns` is at most the last `keep` turns; `truncated` is True when
    earlier turns were dropped.
    """
    hist = list(history or [])
    if len(hist) <= keep:
        return hist, False
    return hist[-keep:], True


def render(history: list[ChatTurn] | None, truncated: bool = False) -> str:
    """Format windowed turns for a prompt. Empty string when there is no history."""
    turns = list(history or [])
    if not turns:
        return ""
    lines = ["(earlier context omitted)"] if truncated else []
    for t in turns:
        who = "Reader" if t.get("role") == "user" else "Apologist"
        lines.append(f"{who}: {t.get('content', '').strip()}")
    return "\n".join(lines)


def last_user_turn(history: list[ChatTurn] | None) -> str:
    """The most recent user turn before the current one — used to enrich a
    follow-up's retrieval query. Empty string if none."""
    for t in reversed(list(history or [])):
        if t.get("role") == "user":
            return t.get("content", "").strip()
    return ""
