"""The shared state that flows through the debate graph (AI-SPEC.md §3)."""

from __future__ import annotations

import operator
from typing import Annotated, Literal, TypedDict

Persona = Literal["jw-unitarian", "muslim", "skeptic", "seeker"]
Status = Literal["running", "approved", "degraded", "rejected"]


class Turn(TypedDict):
    role: str  # "interlocutor" | "apologist" | "system"
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
