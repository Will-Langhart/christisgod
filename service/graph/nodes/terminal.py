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


def graceful_degrade(state: DebateState) -> dict:
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
