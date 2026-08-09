"""The seven debate-graph nodes (AI-SPEC.md §3).

Deterministic (no llm): citation_extractor, scripture_verifier, synthesizer,
terminal.* — these import and run without the LLM stack.
LLM-backed: interlocutor, apologist, orthodoxy_guardrail, retriever(placeholder).
"""

from .apologist import apologist
from .citation_extractor import citation_extractor
from .interlocutor import interlocutor
from .orthodoxy_guardrail import orthodoxy_guardrail
from .retriever import retriever
from .scripture_verifier import scripture_verifier
from .synthesizer import synthesizer
from .terminal import deflect, graceful_degrade, human_approval, respond
from .triage import triage

__all__ = [
    "interlocutor",
    "retriever",
    "apologist",
    "citation_extractor",
    "scripture_verifier",
    "orthodoxy_guardrail",
    "synthesizer",
    "human_approval",
    "respond",
    "graceful_degrade",
    "triage",
    "deflect",
]
