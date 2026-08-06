# service/ — the apologetics engine (LangGraph)

The Python home of the multi-agent "Test the Case" engine. See the full design in
[`../AI-SPEC.md`](../AI-SPEC.md).

## Status

- **Phase 0 — Single source of truth: ✅ scaffolded (this is what's here now).**
  - `canon.py` — the deterministic hard gate. A stdlib-only port of the reference
    parser in `web/src/lib/scripture.ts`, reading the generated canon in
    `../shared/canon/`. Provides `parse_ref`, `lookup_verse`, `verify_citation`.
  - `tests/test_canon.py` — proves the gate (valid refs parse, out-of-range
    look-alikes reject, correct quotes pass, misquotes and fabricated refs fail).
- **Phase 1 — graph + offline library: 🚧 skeleton in place.**
  - `graph/` — the compiled debate `StateGraph` (`build.py`), shared `state.py`,
    `config.py`, and the seven `nodes/`. Deterministic nodes (citation_extractor,
    scripture_verifier, synthesizer, terminal) are **complete**; the LLM nodes
    (interlocutor, apologist, orthodoxy_guardrail) have **first-draft prompts**
    to refine; `retriever` uses a **Chroma** embedding index (`graph/retrieval.py`,
    local model — no embeddings key) and degrades to a keyword scorer if chromadb
    isn't installed.
  - `runner/run_matrix.py` — the offline persona × objection runner (24 dialogues),
    with `--dry-run` (needs no deps).
  - `tests/test_spine.py` — the deterministic spine (extract → verify → synth),
    **6/6 passing**, no LLM / no langgraph.
- **Phase 2 — live FastAPI/SSE service: not started.** (Flip `config.TERMINAL_MODE`
  to `respond`; wrap `graph.build_graph()` in a streaming endpoint.)

### Running Phase 1

```bash
python3 -m runner.run_matrix --dry-run          # enumerate the matrix (no deps)

python3 -m venv .venv && . .venv/bin/activate   # real run needs Python 3.10+
pip install -r requirements.txt

cp .env.example .env                             # then paste your key into .env
python3 -m graph.retrieval --build               # build the Chroma index (once)
python3 -m runner.run_matrix --persona muslim    # run + human-approve into library/
```

`.env` holds `ANTHROPIC_API_KEY` (and optional LangSmith keys); it is gitignored —
never commit it. Rebuild the index (`python3 -m graph.retrieval --build --force`)
after editing chapter content. Before a real run, review the theology drafts and
the LLM node prompts.

## The canon (single source of truth)

`../shared/canon/` is generated — never hand-edit it:

```bash
cd ../web && node scripts/build-verses.mjs
```

That one command regenerates, in the same pass:
- `web/src/lib/verses.generated.ts` (the site's hover-card verse store), and
- `shared/canon/verses.json` + `shared/canon/book-meta.json` (this service's gate).

Because both come from the same `out` map, the site and the verifier cannot drift.

## Run the Phase 0 gate tests

No dependencies required:

```bash
python3 tests/test_canon.py
```

(or `python3 -m pytest` once pytest is installed.)

## Next (Phase 1)

The graph nodes from AI-SPEC.md §3 — Interlocutor, Retriever, Apologist,
CitationExtractor, **ScriptureVerifier (uses `canon.verify_citation`)**,
OrthodoxyGuardrail, Synthesizer — plus the CLI runner over the
4 personas × 6 objections matrix. Requires: `langgraph`, `langchain`,
`langchain-anthropic`, `chromadb`, `langsmith` (Python 3.10+).

The two theology artifacts are drafted in `theology/` and **await your review**
(AI-SPEC.md §7):
- `theology/heresy-taxonomy.md` — the OrthodoxyGuardrail rubric.
- `theology/personas/` — the four Interlocutor seed briefs.
