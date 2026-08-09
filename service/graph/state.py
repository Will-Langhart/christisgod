"""The shared state that flows through the debate graph (AI-SPEC.md §3)."""

from __future__ import annotations

import operator
from typing import Annotated, Literal, TypedDict

Persona = Literal["jw-unitarian", "muslim", "skeptic", "seeker"]
Status = Literal["running", "approved", "degraded", "rejected", "deflected"]
Mode = Literal["direct", "debate"]
Intent = Literal["objection", "followup", "meta"]


class Turn(TypedDict):
    role: str  # "interlocutor" | "apologist" | "system"
    content: str


class ChatTurn(TypedDict):
    role: str  # "user" | "assistant"
    content: str


class CitationCheck(TypedDict):
    raw: str
    ok: bool
    reason: str
    display: str | None
    quoted: str | None
    warning: str | None


class DebateState(TypedDict, total=False):
    # inputs
    persona: Persona
    objection: str  # the objection question, verbatim
    objection_href: str  # chapter link — used by GracefulDegrade
    objection_label: str  # human label for the chapter link

    # conversational inputs (Phase 3 — AI-SPEC.md §9). Absent in Phase 1/2.
    mode: Mode  # "direct" Q&A (default) or persona "debate"
    history: list[ChatTurn]  # prior turns, client-supplied (windowed before use)
    user_message: str  # the current user turn — the thing being answered
    history_truncated: bool  # windowing dropped older turns (UI note)

    # triage (Phase 3)
    intent: Intent  # objection | followup | meta
    guard_ok: bool  # input guard: on-topic + not an injection attempt
    guard_reason: str  # why the guard deflected (when guard_ok is False)

    # transcript accumulates (reducer appends across nodes)
    transcript: Annotated[list[Turn], operator.add]

    # working values (overwritten each loop)
    retrieved: list[str]  # retrieved chapter passages
    draft: str  # apologist's latest answer
    citations: list[CitationCheck]
    verify_ok: bool
    verify_feedback: str  # why verification failed, fed back to apologist
    citation_warnings: list[str]  # non-blocking quote-accuracy flags for human review
    orthodoxy_ok: bool
    orthodoxy_report: str  # guardrail rationale / flagged heresies
    orthodoxy_feedback: str  # fed back to apologist on failure

    # control
    retries: int
    status: Status
    final: str  # approved answer, or the graceful-degrade message
