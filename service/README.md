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
- **Phase 1 — graph + offline library: not started.**
- **Phase 2 — live FastAPI/SSE service: not started.**

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
