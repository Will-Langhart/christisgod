"""Phase 1 offline runner — walk the persona × objection matrix, run the debate
graph, and let a human approve each result before it enters the verified library
(AI-SPEC.md §5). The approved library doubles as the Phase 2 eval set.

Usage:
    python3 -m runner.run_matrix                     # all personas × all objections
    python3 -m runner.run_matrix --persona muslim    # one persona
    python3 -m runner.run_matrix --dry-run           # enumerate, don't call the graph

Requires the LLM stack (requirements.txt) + ANTHROPIC_API_KEY for a real run.
--dry-run needs neither.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from graph.config import OBJECTIONS_PATH, PERSONAS_DIR

OUT_DIR = Path(__file__).resolve().parent.parent / "library"  # approved dialogues land here
PERSONAS = ["jw-unitarian", "muslim", "skeptic", "seeker"]


def load_objections() -> list[dict]:
    return json.loads(OBJECTIONS_PATH.read_text("utf-8"))


def iter_matrix(personas: list[str], objections: list[dict]):
    for persona in personas:
        for obj in objections:
            yield persona, obj


def run_one(graph, persona: str, obj: dict) -> dict:
    from graph.tracing import run_config

    state = {
        "persona": persona,
        "objection": obj["question"],
        "objection_href": obj.get("href", "/"),
        "objection_label": obj.get("linkLabel", "the relevant chapter"),
        "retries": 0,
        "status": "running",
    }
    # run_config names + tags the LangSmith trace by persona/objection.
    return graph.invoke(state, config=run_config(persona, obj["question"]))


def approve(result: dict) -> bool:
    if result.get("status") == "degraded":
        print("  ⚠ degraded (no answer emitted):", result.get("final", ""))
        # Diagnostics: which gate rejected, and why (so tuning isn't blind).
        print(f"    retries={result.get('retries')} "
              f"verify_ok={result.get('verify_ok')} "
              f"orthodoxy_ok={result.get('orthodoxy_ok')}")
        if result.get("verify_feedback"):
            print("    last verify feedback:", result["verify_feedback"])
        if result.get("orthodoxy_report"):
            print("    last guardrail verdict:", result["orthodoxy_report"])
        return False
    print("\n--- ANSWER ---\n" + result.get("final", "") + "\n")
    return input("  approve into library? [y/N] ").strip().lower() == "y"


def save(persona: str, obj: dict, result: dict) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    slug = obj["href"].strip("/").replace("/", "-") or "root"
    path = OUT_DIR / f"{persona}__{slug}.json"
    path.write_text(json.dumps(
        {"persona": persona, "objection": obj["question"],
         "answer": result.get("final", ""),
         "citations": [c for c in result.get("citations", []) if c.get("ok")],
         "transcript": result.get("transcript", [])},
        indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"  ✓ saved {path.name}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", choices=PERSONAS, action="append")
    ap.add_argument("--objection", help="substring filter on the objection question")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    personas = args.persona or PERSONAS
    objections = load_objections()
    if args.objection:
        needle = args.objection.lower()
        objections = [o for o in objections if needle in o["question"].lower()]
        if not objections:
            print(f"no objection matches {args.objection!r}")
            return

    if args.dry_run:
        for persona, obj in iter_matrix(personas, objections):
            print(f"  {persona:14s} × {obj['question']}")
        total = len(personas) * len(objections)
        print(f"\n{total} dialogues would run "
              f"({len(personas)} personas × {len(objections)} objections). "
              f"Persona briefs: {PERSONAS_DIR}")
        return

    from graph import build_graph  # lazy: needs langgraph

    graph = build_graph()
    approved = 0
    for persona, obj in iter_matrix(personas, objections):
        print(f"\n=== {persona} × {obj['question']} ===")
        result = run_one(graph, persona, obj)
        if approve(result):
            save(persona, obj, result)
            approved += 1
    print(f"\n{approved} dialogue(s) approved into {OUT_DIR}")


if __name__ == "__main__":
    main()
