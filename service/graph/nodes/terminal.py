"""Terminal nodes. NO llm.

- human_approval  : Phase 1 offline runner — a person accepts/rejects the answer
                    before it becomes part of the static verified library.
- respond         : Phase 2 live service — emit the answer as-is (both gates
                    already passed).
- graceful_degrade: the safety exit. When retries are exhausted the engine emits
                    NO unverified answer — it points the reader to the chapter
                    that treats the objection (AI-SPEC.md §4).
"""

from __future__ import annotations

from ..state import DebateState


def human_approval(state: DebateState) -> dict:
    # The runner drives the actual prompt (it owns stdin); this node just marks
    # the answer as awaiting approval. Kept a node so the graph topology matches
    # the live path exactly, differing only in terminal.
    return {"status": "approved"}


def respond(state: DebateState) -> dict:
    return {"status": "approved"}


def deflect(state: DebateState) -> dict:
    """Phase 3 off-topic terminal (AI-SPEC.md §9.3). Fires when Triage judges the
    message off-topic or an injection attempt. Warm, fixed, and — critically —
    carries NO scriptural claim, so it needs no verification."""
    message = (
        "I'm here to make the case that Jesus Christ is God — his divinity, the "
        "Trinity, the incarnation, and the objections raised against them. Ask me "
        "anything along those lines and I'll answer it grounded in Scripture."
    )
    return {
        "status": "deflected",
        "final": message,
        "transcript": [{"role": "system", "content": "[deflect] off-topic; no answer generated"}],
    }


def graceful_degrade(state: DebateState) -> dict:
    if state.get("mode") == "debate":
        # In debate mode the interlocutor (not the apologist) exhausted retries —
        # almost always because it kept citing a verse it couldn't get right.
        # Stay in the exchange rather than pointing at a chapter.
        message = (
            "Let me set that particular proof-text aside rather than lean on a "
            "reference I can't state cleanly. Make your case and I'll press it."
        )
    else:
        label = state.get("objection_label") or "the relevant chapter"
        href = state.get("objection_href", "/")
        message = (
            "This objection deserves a careful answer that we won't shortcut. "
            f"The book treats it directly — see {label} ({href})."
        )
    return {
        "status": "degraded",
        "final": message,
        "transcript": [{"role": "system", "content": "[degrade] retries exhausted; no unverified answer emitted"}],
    }
