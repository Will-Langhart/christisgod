"""Configuration for the debate graph — models, limits, and paths.

Everything is overridable by environment variable so the same graph runs in the
Phase 1 offline runner and the Phase 2 live service without code changes.
"""

from __future__ import annotations

import os
from pathlib import Path

# --- paths -----------------------------------------------------------------
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent
THEOLOGY_DIR = SERVICE_DIR / "theology"
TAXONOMY_PATH = THEOLOGY_DIR / "heresy-taxonomy.md"
PERSONAS_DIR = THEOLOGY_DIR / "personas"
CONTENT_DIR = REPO_ROOT / "web" / "src" / "content"  # the 17 MDX chapters
OBJECTIONS_PATH = REPO_ROOT / "shared" / "objections.json"

# --- models (Claude) -------------------------------------------------------
# Strongest reasoning on the load-bearing nodes; a faster model for the
# interlocutor. The extractor and verifier use NO llm — they are deterministic.
APOLOGIST_MODEL = os.getenv("APOLOGIST_MODEL", "claude-sonnet-5")
GUARDRAIL_MODEL = os.getenv("GUARDRAIL_MODEL", "claude-sonnet-5")
INTERLOCUTOR_MODEL = os.getenv("INTERLOCUTOR_MODEL", "claude-haiku-4-5")

# Low temperature everywhere — this is not a place for creativity.
APOLOGIST_TEMPERATURE = float(os.getenv("APOLOGIST_TEMPERATURE", "0.2"))
GUARDRAIL_TEMPERATURE = float(os.getenv("GUARDRAIL_TEMPERATURE", "0.0"))
INTERLOCUTOR_TEMPERATURE = float(os.getenv("INTERLOCUTOR_TEMPERATURE", "0.4"))

# --- control ---------------------------------------------------------------
# Max apologist re-drafts before GracefulDegrade fires (AI-SPEC.md §4).
MAX_RETRIES = int(os.getenv("DEBATE_MAX_RETRIES", "3"))
RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", "6"))

# Phase 1 offline runner terminates at HumanApproval; Phase 2 live service
# terminates at `respond`. Toggled here.
TERMINAL_MODE = os.getenv("DEBATE_TERMINAL", "human_approval")  # or "respond"
