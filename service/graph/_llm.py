"""Thin Claude wrapper shared by the LLM nodes.

Kept in one place so model wiring, retries, and (later) LangSmith tracing are
configured once. Imports langchain-anthropic lazily so the deterministic nodes
and tests do not require the LLM stack to be installed.
"""

from __future__ import annotations


def _extract_text(content) -> str:
    """Flatten a LangChain message's content to plain text.

    Claude 5 can return a list of typed blocks (e.g. a `thinking` block plus a
    `text` block). Keep only the text; never str() the whole list (that leaks the
    thinking signature into the answer)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts).strip()
    return str(content)


def call_llm(model: str, system: str, user: str, temperature: float | None = None,
             max_tokens: int = 4096, cache_system: bool = False) -> str:
    """Single-shot completion. Returns the assistant text.

    `temperature` is omitted unless explicitly set — the Claude 5 models reject a
    `temperature` parameter, so passing one 400s. Set a per-node temperature via
    env only for a model that still supports it.

    `max_tokens` defaults high enough that thinking tokens plus the answer/JSON
    verdict are not truncated (a truncated guardrail JSON was being parsed as a
    spurious FAIL).

    `cache_system` marks the system prompt as an ephemeral prompt-cache breakpoint
    (AI-SPEC.md §9.5). Set it on nodes whose system prompt is large and identical
    across every turn of a conversation (apologist, orthodoxy guardrail) so turns
    2+ read that prefix from cache instead of re-billing it.

    Raises a clear error if the LLM stack isn't installed yet (Phase 1 setup),
    so a missing dependency is obvious rather than a cryptic ImportError deep in
    a node.
    """
    try:
        from langchain_anthropic import ChatAnthropic
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "LLM stack not installed. `pip install -r requirements.txt` and set "
            "ANTHROPIC_API_KEY to run the graph. (Deterministic nodes/tests do "
            "not need this.)"
        ) from e

    kwargs: dict = {"model": model, "max_tokens": max_tokens}
    if temperature is not None:
        kwargs["temperature"] = temperature
    llm = ChatAnthropic(**kwargs)

    # Prompt caching: send the system prompt as a content block carrying
    # cache_control. Anthropic caches the prefix up to that breakpoint; a short
    # prompt below the model's minimum cacheable length is simply not cached (no
    # error), so this is always safe to request.
    if cache_system:
        system_msg = SystemMessage(content=[{
            "type": "text", "text": system,
            "cache_control": {"type": "ephemeral"},
        }])
    else:
        system_msg = SystemMessage(content=system)

    resp = llm.invoke([system_msg, HumanMessage(content=user)])
    return _extract_text(resp.content)
