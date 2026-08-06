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


def _degrade_diagnostics(result: dict) -> str:
    """Print + return a one-line reason for a degraded run (which gate, why)."""
    print("  ⚠ degraded (no answer emitted):", result.get("final", ""))
    line = (f"retries={result.get('retries')} verify_ok={result.get('verify_ok')} "
            f"orthodoxy_ok={result.get('orthodoxy_ok')}")
    print("    " + line)
    if result.get("verify_feedback"):
        print("    last verify feedback:", result["verify_feedback"])
    if result.get("orthodoxy_report"):
        print("    last guardrail verdict:", result["orthodoxy_report"])
    gate = ("citation" if result.get("verify_ok") is False
            else "orthodoxy" if result.get("orthodoxy_ok") is False else "unknown")
    return f"{gate} gate | {line}"


def _summary(rows: list[dict]) -> None:
    if not rows:
        return
    marks = {"saved": "✓", "degraded": "⚠", "skipped": "·"}
    print("\n=== summary ===")
    for r in rows:
        print(f"  {marks.get(r['outcome'], '?')} {r['persona']:14s} "
              f"{r['obj'][:46]:46s} {r['outcome']}")
        if r.get("reason"):
            print(f"      {r['reason']}")
    saved = sum(1 for r in rows if r["outcome"] == "saved")
    deg = sum(1 for r in rows if r["outcome"] == "degraded")
    skip = sum(1 for r in rows if r["outcome"] == "skipped")
    print(f"\n{saved} saved · {deg} degraded · {skip} skipped · {len(rows)} total → {OUT_DIR}")


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
    ap.add_argument("--auto", action="store_true",
                    help="save every non-degraded dialogue without prompting; "
                         "review the saved JSON files afterward")
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
    rows: list[dict] = []
    for persona, obj in iter_matrix(personas, objections):
        print(f"\n=== {persona} × {obj['question']} ===")
        result = run_one(graph, persona, obj)

        if result.get("status") == "degraded":
            reason = _degrade_diagnostics(result)
            outcome = "degraded"
        else:
            print("\n--- ANSWER ---\n" + result.get("final", "") + "\n")
            keep = args.auto or input("  approve into library? [y/N] ").strip().lower() == "y"
            if keep:
                save(persona, obj, result)
                outcome = "saved"
            else:
                outcome = "skipped"
            reason = ""
        rows.append({"persona": persona, "obj": obj["question"],
                     "outcome": outcome, "reason": reason})

    _summary(rows)


if __name__ == "__main__":
    main()
