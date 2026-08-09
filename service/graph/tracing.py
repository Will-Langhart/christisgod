"""LangSmith tracing setup for the debate graph (AI-SPEC.md §2).

LangChain/LangGraph auto-trace to LangSmith when the right env vars are set. This
module makes that ergonomic:

- `configure()` turns tracing ON automatically when a LANGSMITH_API_KEY is present
  (unless you explicitly set LANGSMITH_TRACING=false), sets a default project, and
  mirrors the modern LANGSMITH_* vars to the legacy LANGCHAIN_* names for older
  langchain builds. It never prints or returns the key.
- `run_config(persona, objection)` returns the LangChain run config so each graph
  invocation shows up named and tagged by persona — the difference between a
  searchable trace and a wall of anonymous runs.

Secrets live only in service/.env (gitignored); nothing here logs their values.
"""

from __future__ import annotations

import os

from . import config  # importing config loads service/.env (via python-dotenv)


def _truthy(v: str | None) -> bool:
    return (v or "").strip().lower() in ("1", "true", "yes", "on")


def tracing_enabled() -> bool:
    return _truthy(os.getenv("LANGSMITH_TRACING")) or _truthy(os.getenv("LANGCHAIN_TRACING_V2"))


def configure() -> bool:
    """Enable + normalize LangSmith env. Returns whether tracing ends up on."""
    key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
    if not key:
        return tracing_enabled()  # respect an explicit flag; otherwise off

    # Key present → default tracing ON unless the user explicitly turned it off.
    if os.getenv("LANGSMITH_TRACING") is None and os.getenv("LANGCHAIN_TRACING_V2") is None:
        os.environ["LANGSMITH_TRACING"] = "true"

    project = (
        os.getenv("LANGSMITH_PROJECT")
        or os.getenv("LANGCHAIN_PROJECT")
        or config.LANGSMITH_PROJECT
    )
    os.environ.setdefault("LANGSMITH_PROJECT", project)

    # Legacy aliases so both new and old langchain versions pick this up.
    os.environ.setdefault("LANGCHAIN_API_KEY", key)
    os.environ.setdefault("LANGCHAIN_TRACING_V2", os.environ.get("LANGSMITH_TRACING", "true"))
    os.environ.setdefault("LANGCHAIN_PROJECT", os.environ["LANGSMITH_PROJECT"])
    return tracing_enabled()


def run_config(persona: str, objection: str, kind: str = "debate",
               mode: str | None = None) -> dict:
    """LangChain run config to pass as `graph.invoke(state, config=...)`.

    `kind` names the run in LangSmith ("debate" for the single-shot graph, "chat"
    for the conversational one); `mode` (direct/debate) is added as a searchable
    tag so a LangSmith view can filter chat traffic by mode."""
    tags = [kind, f"persona:{persona}"]
    metadata = {"persona": persona, "objection": objection}
    if mode:
        tags.append(f"mode:{mode}")
        metadata["mode"] = mode
    return {"run_name": f"{kind}:{persona}", "tags": tags, "metadata": metadata}


def status() -> dict:
    """Non-secret snapshot of the tracing config (booleans + names only)."""
    return {
        "tracing_enabled": tracing_enabled(),
        "has_api_key": bool(os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")),
        "project": os.getenv("LANGSMITH_PROJECT") or os.getenv("LANGCHAIN_PROJECT"),
    }


if __name__ == "__main__":
    configure()
    st = status()
    print("LangSmith tracing:")
    print(f"  enabled : {st['tracing_enabled']}")
    print(f"  api key : {'present' if st['has_api_key'] else 'MISSING (set LANGSMITH_API_KEY in .env)'}")
    print(f"  project : {st['project']}")

    if st["has_api_key"]:
        try:
            from langsmith import Client

            projects = list(Client().list_projects(limit=1))
            print(f"  connect : ok ({'project exists' if projects else 'authenticated'})")
        except ImportError:
            print("  connect : langsmith not installed (pip install -r requirements.txt)")
        except Exception as e:  # noqa: BLE001
            print(f"  connect : FAILED — {type(e).__name__}: {e}")
