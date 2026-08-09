"""The multi-agent debate graph for the apologetics engine (AI-SPEC.md §3).

`build_graph` is imported lazily from `.build` to avoid requiring langgraph for
code that only touches state/config/deterministic nodes.
"""

__all__ = ["build_graph", "build_chat_graph"]


def build_graph(*args, **kwargs):
    from .build import build_graph as _bg

    return _bg(*args, **kwargs)


def build_chat_graph(*args, **kwargs):
    from .build import build_chat_graph as _bcg

    return _bcg(*args, **kwargs)
