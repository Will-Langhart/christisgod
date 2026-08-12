"""Configuration for the debate graph — models, limits, and paths.

Everything is overridable by environment variable so the same graph runs in the
Phase 1 offline runner and the Phase 2 live service without code changes.
"""

from __future__ import annotations

import os
from pathlib import Path

# Load .env so ANTHROPIC_API_KEY and any overrides are available without exporting
# them by hand. Checks repo-root .env first, then service/.env (service-local wins).
# Both are gitignored. Uses python-dotenv when installed, else a stdlib fallback so
# this works before `pip install` too. Never logs values.
_service_dir = Path(__file__).resolve().parent.parent


def _load_env_file_stdlib(path: Path, override: bool = False) -> None:
    if not path.exists():
        return
    for raw in path.read_text("utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = val


try:
    from dotenv import load_dotenv

    load_dotenv(_service_dir.parent / ".env")  # repo-root .env
    load_dotenv(_service_dir / ".env", override=True)  # service/.env overrides
except ImportError:
    _load_env_file_stdlib(_service_dir.parent / ".env")
    _load_env_file_stdlib(_service_dir / ".env", override=True)

# --- paths -----------------------------------------------------------------
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent
THEOLOGY_DIR = SERVICE_DIR / "theology"
TAXONOMY_PATH = THEOLOGY_DIR / "heresy-taxonomy.md"
PERSONAS_DIR = THEOLOGY_DIR / "personas"
CONTENT_DIR = REPO_ROOT / "web" / "src" / "content"  # the 17 MDX chapters
OBJECTIONS_PATH = REPO_ROOT / "shared" / "objections.json"

# --- retrieval (Chroma) ----------------------------------------------------
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", str(SERVICE_DIR / ".chroma")))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "christisgod-chapters")

# --- models (Claude) -------------------------------------------------------
# Strongest reasoning on the load-bearing nodes; a faster model for the
# interlocutor. The extractor and verifier use NO llm — they are deterministic.
APOLOGIST_MODEL = os.getenv("APOLOGIST_MODEL", "claude-sonnet-5")
GUARDRAIL_MODEL = os.getenv("GUARDRAIL_MODEL", "claude-sonnet-5")
INTERLOCUTOR_MODEL = os.getenv("INTERLOCUTOR_MODEL", "claude-haiku-4-5")
# Triage (Phase 3 §9.3) — cheap classification; the fast model is enough.
TRIAGE_MODEL = os.getenv("TRIAGE_MODEL", "claude-haiku-4-5")

# Temperature is omitted by default — Claude 5 models reject the parameter. Set a
# value via env only for a model that still supports it (then it's passed through).
def _opt_temp(name: str) -> float | None:
    v = os.getenv(name)
    return float(v) if v not in (None, "") else None


APOLOGIST_TEMPERATURE = _opt_temp("APOLOGIST_TEMPERATURE")
GUARDRAIL_TEMPERATURE = _opt_temp("GUARDRAIL_TEMPERATURE")
INTERLOCUTOR_TEMPERATURE = _opt_temp("INTERLOCUTOR_TEMPERATURE")

# --- control ---------------------------------------------------------------
# Max apologist re-drafts before GracefulDegrade fires (AI-SPEC.md §4).
MAX_RETRIES = int(os.getenv("DEBATE_MAX_RETRIES", "3"))
RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", "6"))
# Over-retrieval + MMR rerank (retrieval-quality upgrade). Fetch this many
# candidates by embedding similarity, then MMR narrows to RETRIEVER_TOP_K,
# trading pure relevance for non-redundancy at lambda (1.0 = relevance only).
RETRIEVER_FETCH_K = int(os.getenv("RETRIEVER_FETCH_K", "20"))
RETRIEVER_MMR_LAMBDA = float(os.getenv("RETRIEVER_MMR_LAMBDA", "0.6"))
# HyDE query expansion (retriever node): draft a short hypothetical *orthodox
# answer* with the cheap model and retrieve on it, so adversarially-phrased
# objections land near the book's affirmative prose. Degrades to the raw query
# on any failure. Disable with RETRIEVER_HYDE=0.
RETRIEVER_HYDE = os.getenv("RETRIEVER_HYDE", "1") != "0"

# Conversational layer (Phase 3 §9.4). How many recent turns the apologist sees
# verbatim; older turns are dropped with a note (deterministic windowing).
WINDOW_TURNS = int(os.getenv("DEBATE_WINDOW_TURNS", "6"))

# Phase 1 offline runner terminates at HumanApproval; Phase 2 live service
# terminates at `respond`. Toggled here.
TERMINAL_MODE = os.getenv("DEBATE_TERMINAL", "human_approval")  # or "respond"

# --- tracing ---------------------------------------------------------------
# Default LangSmith project name; tracing auto-enables when LANGSMITH_API_KEY is
# set (see graph/tracing.py).
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "christisgod-debate")
