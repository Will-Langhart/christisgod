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
- **Phase 2 — live FastAPI/SSE service: 🚧 skeleton in place.**
  - `api/app.py` — FastAPI app; `GET /health` and `POST /debate` (SSE stream of
    the debate for one objection). Same graph as Phase 1, terminal `respond`
    instead of `human_approval` (set via `DEBATE_TERMINAL=respond`, done in-app).
  - `api/sse.py` — framework-free SSE formatting + validation (`tests/test_api_sse.py`,
    4/4, no FastAPI/LLM deps).
  - Streams transcript turns as `interlocutor` / `draft` / `progress` events, then a
    `done` event with the final answer, verified citations (with KJV text), and any
    non-blocking quote warnings.

### Running Phase 2 (live service)

```bash
# from service/, venv active, ANTHROPIC_API_KEY set
uvicorn api.app:app --port 8600 --reload

curl -N -X POST localhost:8600/debate -H 'content-type: application/json' \
  -d '{"persona":"skeptic","objection":"Was Jesus made God at Nicaea?"}'
```

Restrict browser origins with `CORS_ORIGINS` (comma-separated; defaults to
christisgod.app + localhost). The Next frontend consumes `/debate` via `EventSource`
/ fetch-stream for a new `/dialogues` route.

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
never commit it. Either the **repo-root `.env`** or **`service/.env`** works
(both are loaded; service-local wins). Rebuild the index
(`python3 -m graph.retrieval --build --force`) after editing chapter content.
Before a real run, review the theology drafts and the LLM node prompts.

### LangSmith tracing

Tracing auto-enables when `LANGSMITH_API_KEY` is set (traces go to project
`christisgod-debate`; override with `LANGSMITH_PROJECT`). Each run is named and
tagged by persona. Confirm it's wired:

```bash
python3 -m graph.tracing        # prints enabled / key present / project + connect check
```

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
