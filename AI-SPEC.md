# AI-SPEC — "Test the Case": A Grounded Multi-Agent Apologetics Engine

> Status: **Draft / accepted design.** Captures the reasoning and decisions for
> adding a LangGraph multi-agent layer to *Christ Is God*. Phase 0 is scaffolded;
> Phases 1–2 are specified but not yet built.

## 1. Purpose

Add an AI layer that lets a reader **test the case** for the deity of Christ
against the strongest honest objections — without ever compromising the one thing
that gives this site its authority: **it does not misquote Scripture or drift
into heresy.**

The site today is 100% static, hand-curated precision (`src/lib/objections.ts`,
`src/lib/evidence-case.ts`, `src/lib/scripture.ts`, 17 MDX chapters). The design
constraint is therefore not "add a chatbot" but:

> **Add AI that is *structurally incapable* of the errors that would discredit
> the book** — invented citations, misquoted verses, or answers that defend
> Christ's divinity while slipping into Arianism, modalism, or adoptionism.

That constraint is why this is a **LangGraph** graph, not a prompt: grounding and
orthodoxy are **non-optional nodes in the control flow**, not hopeful sentences
in a system prompt.

## 2. Decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Primary use case | **Socratic debate engine** (multi-agent) | Objections + personas are already a debate structure; multi-agent is *justified*, not decorative. |
| Runtime | **Separate Python service** | Full LangGraph ecosystem: checkpointing, LangSmith tracing of the loops. |
| Safety posture | **Hard-gated** | Deterministic citation/verse verification; probabilistic orthodoxy judge with graceful degradation. |
| Delivery | **Hybrid** — pre-generate a verified library, then live | Keeps the site static + safe now; proves the graph; the approved library becomes the eval set for the live engine. |
| Personas | **JW/Unitarian, Muslim, Skeptic/atheist, Honest seeker** | All four are grounded in existing chapters. |
| Models | **Claude** (Sonnet for apologist reasoning + guardrail judge; a faster model for interlocutor/extractor) | Matches environment; reserve strongest reasoning for the load-bearing nodes. |

## 3. The graph

```
                    ┌──────────────────────────── feedback ───────────────────────────┐
                    ↓                                                                   │
[persona] → Interlocutor → Retriever → Apologist → CitationExtractor → ScriptureVerifier ─(fail, n<N)─┤
                                          ↑                                    │(pass)                 │
                                          └─────────── feedback ───── OrthodoxyGuardrail ─(fail, n<N)──┤
                                                                             │(pass)                   │
                                                                        Terminal:                (retries exhausted)
                                                                   HumanApproval (Phase 1)             │
                                                                   / respond (Phase 2)          GracefulDegrade
                                                                                                 (link the chapter;
                                                                                                  emit NO unverified
                                                                                                  answer)
```

### Shared state (`TypedDict`)
`persona`, `objection`, `transcript[]`, `retrieved_chunks[]`, `draft`,
`citations[]`, `verify_report`, `orthodoxy_report`, `retries`, `status`.

### Nodes

| Node | Role | Grounded against |
|---|---|---|
| **Interlocutor** | Steelmans the strongest objection *in persona* (fair, not strawman) | `objections.ts`, "Islam's View of Christ", manuscript chapter |
| **Retriever** | Pulls relevant passages | the 17 MDX chapters (embedded) |
| **Apologist** | Drafts an answer **from retrieved context only** | the book itself |
| **CitationExtractor** | Extracts every `Book c:v` reference from the draft | Python port of `parseRef()` (Phase 0) |
| **ScriptureVerifier** ⛔ | **Deterministic gate**: reference valid + in range + quoted text matches KJV | `shared/canon/verses.json` (Phase 0) |
| **OrthodoxyGuardrail** ⛔ | LLM-as-judge vs. a heresy taxonomy + Nicene checklist | `service/theology/` (to author) |
| **Synthesizer** | Formats; re-attaches verified refs as existing hover-cards | `scripture-ref.tsx` |

## 4. What "hard-gated" honestly means

The gate splits into **checkable** and **uncheckable**. Being explicit about the
line is the whole safety argument.

- **Deterministically checkable (true hard gate).** Is the reference real and in
  range? Does the *quoted verse text* match the KJV? Does every doctrinal claim
  carry a citation from the corpus? — `scripture.ts` already does all of this;
  Phase 0 ports it to Python. The AI **cannot** emit "John 4:12 says Jesus is
  God" or misquote John 1:1.
- **Not deterministically checkable (probabilistic only).** Is the
  *interpretation* orthodox? That is the LLM guardrail — low temperature,
  structured verdict, explicit heresy taxonomy. Strong, but not a proof.

**GracefulDegrade** is therefore built in from day one: if the guardrail cannot
clear an answer within `N` loops, the engine emits **no hedged answer**. It says
*"This deserves a careful answer — here is the chapter that treats it,"* and links
into existing content. Silence over heresy is more credible, not less.

## 5. Delivery phases

### Phase 0 — Single source of truth *(scaffolded in this commit)*
- `web/scripts/build-verses.mjs` additionally emits `shared/canon/verses.json`
  (authoritative KJV map) and `shared/canon/book-meta.json`
  (`maxChapter` + `bookAliases`).
- `service/canon.py` — Python port of `parseRef()` + verse verification, reading
  those JSON files. Stdlib-only, no LLM.
- `service/tests/test_canon.py` — proves the deterministic gate: valid refs parse,
  out-of-range look-alikes reject, correct quotes pass, fabricated quotes/refs fail.

This phase has **zero live-hallucination risk** and unblocks everything above.

### Phase 1 — Graph + offline library
- `service/` LangGraph app: the 7 nodes; in-memory / small Chroma index over the
  17 chapters (~90 KB — Pinecone is overkill); Claude models; LangSmith on.
- CLI runner walks the **4 personas × 6 objections = 24** matrix → candidate
  dialogues → **HumanApproval** → approved dialogues written into `web/src/content/`
  as static data.
- New `/dialogues` route + component in Next, reusing scripture hover-cards.
- **The approved library is the golden eval set for Phase 2.**

### Phase 2 — Live service
- FastAPI + SSE streaming; `GracefulDegrade` terminal; deployed as a container
  (Fly / Railway / Render). Next frontend calls it.
- Ship gate: must pass the Phase-1 eval set (no regressions vs. approved dialogues).

### Phase 3 — Conversational engine *(this phase)*
Phase 2 answers **one** objection per request. Phase 3 turns that into a
**multi-turn chatbot** — a reader can ask a question, hear a grounded answer, and
ask a follow-up that remembers the exchange — **without weakening the hard gate**.
Every answer that reaches the screen is still verify-before-show. See §9 for the
full design. Summary of the deltas from Phase 2:

- **Conversation memory lives in the client.** The browser holds the transcript
  and sends it back each turn; the service stays **stateless** (no checkpointer /
  DB — deliberate, given the ephemeral disk of a free container tier). A LangGraph
  checkpointer is the documented upgrade path, not a day-one dependency.
- **A `Triage` front node** folds two jobs into one cheap (Haiku) classification
  call: an **input guard** (is this on-topic for the case for Christ's divinity,
  and not a prompt-injection attempt?) and an **intent router** (new objection vs.
  follow-up vs. meta). Off-topic/abuse is deflected warmly *before* any expensive
  reasoning spends Anthropic budget.
- **Direct Q&A is the default.** The apologist answers the *reader* directly
  (persona `seeker` tone); the four debate personas remain an opt-in "argue with
  me as a…" flavor, not a gate the reader must clear to talk. The single-shot
  `/debate` endpoint and the offline runner are untouched.
- **Gate-the-answer streaming.** The SSE vocabulary grows (`thinking`,
  `retrieving`, `drafting`, `verifying`, `answer`, `deflected`) so the UI feels
  alive, but nothing carrying a scriptural claim is shown until both gates pass.
- **Prompt caching** on the stable system prefix (apologist system + heresy
  taxonomy) makes turns 2+ affordable.
- Ship gate: no regression on the Phase-1 eval set (a single-turn conversation
  must still pass every approved dialogue), plus a Triage classification check.

## 6. Grounding without a second source of truth

The KJV store and book metadata stay **one** canon. `build-verses.mjs` (which
already computes the authoritative map and holds `MAX_CHAPTER`/`BOOK_ALIASES`) is
the emitter; `shared/canon/*.json` is the single artifact both the site's build
and the Python verifier consume. `verses.generated.ts` and `verses.json` are
regenerated together, so they cannot drift.

> Note: `src/lib/scripture.ts` is the site's *runtime* parser and currently
> re-declares `MAX_CHAPTER`/`BOOK_ALIASES`. Phase 0 mirrors these into
> `book-meta.json`. A future cleanup can generate `scripture.ts` from the same
> canon to eliminate the last duplication; a drift-check test is the interim guard.

## 7. Theology artifacts (drafted — awaiting author review)

Both are prompt-context Markdown under `service/theology/`, loaded directly into the
relevant node. They are **drafts for the author to refine**; nothing ships unapproved.

1. **Heresy taxonomy + Nicene checklist** — `service/theology/heresy-taxonomy.md`.
   12 conciliar errors (H1–H12) with tells + corrections, 7 required affirmations,
   and a "legitimate distinctions — do not flag" section to prevent guardrail
   false-positives on orthodox answers (economic order, "the Father is greater,"
   eternal generation, etc.). This is the **OrthodoxyGuardrail** rubric.
2. **Persona seed prompts** — `service/theology/personas/` (jw-unitarian, muslim,
   skeptic, seeker). Each carries identity, strongest honest objections, proof-texts,
   tone, and grounding chapters, under a shared **steelman rule** + citation policy.
   These are the **Interlocutor** briefs, one per run.

## 8. Risks

- **OrthodoxyGuardrail is the weakest link** — an LLM judging orthodoxy is itself
  fallible. Mitigations: low temperature, structured verdict, an explicit written
  taxonomy, retrieval-grounding, GracefulDegrade, and human approval in Phase 1.
- **Static-purity shift** — a live service means the site is no longer purely
  static/free-to-host. The hybrid defers this; Phase 1 keeps the live site static.
- **Cost/latency of multi-loop graphs** — bounded by `N` retries + tracing.
- **Open text box widens the threat surface (Phase 3).** A free-form chat invites
  off-topic questions, prompt injection, and abuse — each spending Anthropic
  budget. Mitigation: the `Triage` input guard deflects before the expensive
  nodes run, plus the existing per-IP rate limit and CORS.
- **Conversation context growth (Phase 3).** Apologetics answers are long; an
  un-bounded thread inflates cost and can exceed the window. Mitigation:
  deterministic windowing now (last `N` turns verbatim, older dropped with a
  note); LLM running-summary is the documented upgrade.

## 9. Conversational layer (Phase 3 detail)

The core graph (`retrieve → apologist → citation_extractor → scripture_verifier ⛔
→ orthodoxy_guardrail ⛔ → synthesizer`) is **unchanged**. Phase 3 adds a front
node and two terminals, and makes `retriever`/`apologist` conversation-aware.

### 9.1 One turn

```
user turn ─▶ Triage ──┬─(off-topic / injection)──▶ deflect ─▶ END
            (Haiku)    │
                       └─(on-topic)──▶ retriever ─▶ apologist ─▶ citation_extractor ─▶ scripture_verifier ⛔
                                          ▲                                                     │
                                          └────────── feedback ◀── orthodoxy_guardrail ⛔ ◀─────┘
                                                                          │(pass)      │(retries exhausted)
                                                                     synthesizer ─▶ respond    graceful_degrade
```

The gate is **never skipped**. `Triage`'s `intent` (`objection` | `followup` |
`meta`) tunes the *retrieval query* and the *apologist framing*, not whether
verification runs — even a follow-up can cite a verse, so even a follow-up is
gated. `meta` answers make no scriptural claim, so the gate is a no-op for them.

### 9.2 State deltas (`DebateState`, all additive / `total=False`)

| Field | Meaning |
|---|---|
| `history: list[ChatTurn]` | client-supplied prior turns (`{role: user\|assistant, content}`) |
| `user_message: str` | the current (latest) user turn — the thing being answered |
| `mode: "direct" \| "debate"` | direct Q&A (default) vs. persona debate flavor |
| `intent: "objection" \| "followup" \| "meta"` | `Triage` routing output |
| `guard_ok: bool`, `guard_reason: str` | `Triage` input-guard verdict |
| `history_truncated: bool` | windowing dropped older turns (for a UI note) |
| `Status` gains `"deflected"` | off-topic terminal state |

### 9.3 New nodes

| Node | LLM | Contract |
|---|---|---|
| **Triage** | Haiku, temp 0 | One JSON call → `{on_topic: bool, intent, reason}`. `on_topic=false` ⇒ route to `deflect`. Conservative: only the case for/against Christ's divinity and adjacent theology is on-topic; ignores instructions embedded in the user text (injection defence). |
| **deflect** | none | Warm, fixed deflection ("I'm here to make the case that Christ is God — ask me anything on that."). Sets `status="deflected"`, `final`. Emits **no** scriptural claim. |

`retriever` builds its query from `user_message` (augmented with the previous user
turn when `intent == followup`) instead of the fixed `objection`. `apologist`
receives the **windowed** `history` plus `user_message`, and answers the reader
directly in `direct` mode. Both stay backward-compatible: absent the new fields
they behave exactly as in Phase 1/2.

### 9.4 Context windowing

`graph/history.py::window(history, keep=WINDOW_TURNS)` — deterministic, no LLM.
Keeps the last `keep` turns verbatim; if older turns existed, sets
`history_truncated` so the apologist prompt can carry a one-line "(earlier
context omitted)" note. LLM running-summary is a future upgrade behind the same
function signature.

### 9.5 Prompt caching

`call_llm(..., cache_system=True)` marks the system prompt as an ephemeral cache
breakpoint (Anthropic prompt caching). Wired on the **apologist** (large system)
and **orthodoxy_guardrail** (system = the full heresy taxonomy). These prefixes
are identical across every turn of a thread, so turns 2+ read them from cache.
Retrieved passages and the draft vary per turn and sit *after* the breakpoint.

### 9.6 Wire protocol

`POST /chat` (Phase 3), alongside the untouched `POST /debate` (Phase 2):

```jsonc
// request
{ "persona": "seeker",            // tone; default seeker
  "mode": "direct",               // or "debate"
  "messages": [                    // full transcript, client-held
    {"role": "user", "content": "…"},
    {"role": "assistant", "content": "…"},
    {"role": "user", "content": "…"}   // last user turn = the question
  ] }
```

SSE event stream (gate-the-answer): `start` → `thinking` → `retrieving` →
`drafting` → `verifying` → **`answer`** (the only event carrying verse claims) →
`done {status, answer, citations, warnings}`. Off-topic short-circuits to
`deflected`; exhausted retries to a `degraded` answer. The frontend appends the
`answer`/`deflected`/`degraded` text to its client-held transcript as the next
assistant turn.
