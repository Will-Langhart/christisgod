"""The multi-agent debate graph for the apologetics engine (AI-SPEC.md §3).

`build_graph` is imported lazily from `.build` to avoid requiring langgraph for
code that only touches state/config/deterministic nodes.
"""

__all__ = ["build_graph"]


def build_graph(*args, **kwargs):
    from .build import build_graph as _bg

    return _bg(*args, **kwargs)
