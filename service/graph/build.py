"""Assemble the debate StateGraph (AI-SPEC.md §3).

Flow:
    interlocutor → retriever → apologist → citation_extractor → scripture_verifier
      ├─ verify fail  & retries<MAX → apologist   (re-draft with feedback)
      ├─ verify fail  & retries≥MAX → graceful_degrade
      └─ verify pass                → orthodoxy_guardrail
                                        ├─ orthodoxy fail & retries<MAX → apologist
                                        ├─ orthodoxy fail & retries≥MAX → graceful_degrade
                                        └─ orthodoxy pass               → synthesizer → <terminal>

<terminal> is human_approval (Phase 1 offline) or respond (Phase 2 live),
selected by config.TERMINAL_MODE.

This module imports langgraph; install requirements.txt before importing it. The
individual deterministic nodes import and test without langgraph.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from . import config
from .nodes import (
    apologist,
    citation_extractor,
    graceful_degrade,
    human_approval,
    interlocutor,
    orthodoxy_guardrail,
    respond,
    retriever,
    scripture_verifier,
    synthesizer,
)
from .state import DebateState


def _after_verify(state: DebateState) -> str:
    if state.get("verify_ok"):
        return "orthodoxy_guardrail"
    return "apologist" if state.get("retries", 0) < config.MAX_RETRIES else "graceful_degrade"


def _after_guardrail(state: DebateState) -> str:
    if state.get("orthodoxy_ok"):
        return "synthesizer"
    return "apologist" if state.get("retries", 0) < config.MAX_RETRIES else "graceful_degrade"


def build_graph(checkpointer=None):
    """Return a compiled debate graph. Pass a LangGraph checkpointer to persist
    state (recommended for the live service; optional for the offline runner)."""
    from . import tracing

    if tracing.configure():
        print(f"· LangSmith tracing on → project '{tracing.status()['project']}'")

    g = StateGraph(DebateState)

    g.add_node("interlocutor", interlocutor)
    g.add_node("retriever", retriever)
    g.add_node("apologist", apologist)
    g.add_node("citation_extractor", citation_extractor)
    g.add_node("scripture_verifier", scripture_verifier)
    g.add_node("orthodoxy_guardrail", orthodoxy_guardrail)
    g.add_node("synthesizer", synthesizer)
    g.add_node("graceful_degrade", graceful_degrade)

    terminal = human_approval if config.TERMINAL_MODE == "human_approval" else respond
    g.add_node("terminal", terminal)

    g.add_edge(START, "interlocutor")
    g.add_edge("interlocutor", "retriever")
    g.add_edge("retriever", "apologist")
    g.add_edge("apologist", "citation_extractor")
    g.add_edge("citation_extractor", "scripture_verifier")

    g.add_conditional_edges("scripture_verifier", _after_verify,
                            ["orthodoxy_guardrail", "apologist", "graceful_degrade"])
    g.add_conditional_edges("orthodoxy_guardrail", _after_guardrail,
                            ["synthesizer", "apologist", "graceful_degrade"])

    g.add_edge("synthesizer", "terminal")
    g.add_edge("terminal", END)
    g.add_edge("graceful_degrade", END)

    return g.compile(checkpointer=checkpointer)
