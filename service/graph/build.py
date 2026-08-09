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
    deflect,
    graceful_degrade,
    human_approval,
    interlocutor,
    meta_reply,
    orthodoxy_guardrail,
    respond,
    retriever,
    scripture_verifier,
    synthesizer,
    triage,
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


def _after_triage(state: DebateState) -> str:
    if not state.get("guard_ok", True):
        return "deflect"
    # Meta questions ("who are you?", "be shorter") carry no scriptural claim —
    # skip retrieval and both gates for a fast, light reply (AI-SPEC.md §9.1).
    if state.get("intent") == "meta":
        return "meta_reply"
    return "retriever"


def build_chat_graph(checkpointer=None):
    """Return the compiled conversational graph (AI-SPEC.md §9).

    Same core as the debate graph — retriever → apologist → the two hard gates →
    synthesizer → respond — but fronted by `Triage` (on-topic guard + intent
    router) and with `deflect` as the off-topic terminal. There is no
    interlocutor: in direct Q&A mode the reader is the interlocutor. The gate is
    never skipped, so every answer that reaches the reader is verify-before-show.
    """
    from . import tracing

    if tracing.configure():
        print(f"· LangSmith tracing on → project '{tracing.status()['project']}'")

    g = StateGraph(DebateState)

    g.add_node("triage", triage)
    g.add_node("retriever", retriever)
    g.add_node("apologist", apologist)
    g.add_node("citation_extractor", citation_extractor)
    g.add_node("scripture_verifier", scripture_verifier)
    g.add_node("orthodoxy_guardrail", orthodoxy_guardrail)
    g.add_node("synthesizer", synthesizer)
    g.add_node("graceful_degrade", graceful_degrade)
    g.add_node("deflect", deflect)
    g.add_node("meta_reply", meta_reply)
    g.add_node("respond", respond)

    g.add_edge(START, "triage")
    g.add_conditional_edges("triage", _after_triage,
                            ["retriever", "meta_reply", "deflect"])
    g.add_edge("retriever", "apologist")
    g.add_edge("apologist", "citation_extractor")
    g.add_edge("citation_extractor", "scripture_verifier")

    g.add_conditional_edges("scripture_verifier", _after_verify,
                            ["orthodoxy_guardrail", "apologist", "graceful_degrade"])
    g.add_conditional_edges("orthodoxy_guardrail", _after_guardrail,
                            ["synthesizer", "apologist", "graceful_degrade"])

    g.add_edge("synthesizer", "respond")
    g.add_edge("respond", END)
    g.add_edge("graceful_degrade", END)
    g.add_edge("deflect", END)
    g.add_edge("meta_reply", END)

    return g.compile(checkpointer=checkpointer)
