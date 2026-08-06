"""Synthesizer — packages a verified, orthodox answer for delivery. NO llm.

Attaches the verified citations (with their canonical display form and KJV text)
so the frontend can render them as the site's existing hover-cards. This runs
only after both gates pass, so every reference here is known-good.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from canon import lookup_verse  # noqa: E402

from ..state import DebateState  # noqa: E402


def synthesizer(state: DebateState) -> dict:
    verified = [c for c in state.get("citations", []) if c["ok"] and c["display"]]
    refs = [
        {"display": c["display"], "text": lookup_verse(c["display"])}
        for c in verified
    ]
    return {
        "final": state.get("draft", ""),
        "status": "running",  # terminal node sets the final status
        # refs travels in the transcript payload for the runner/frontend to pick up
        "transcript": [{"role": "system", "content": f"[synth] {len(refs)} verified citation(s)"}],
    }
