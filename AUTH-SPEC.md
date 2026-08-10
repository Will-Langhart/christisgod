# AUTH-SPEC — Accounts: Google & Microsoft sign-in via Supabase

> Status: **Phase 4A built (foundation).** Captures the reasoning and decisions
> for adding user accounts to *Christ Is God*. Continues the numbering of
> `AI-SPEC.md` as **Phase 4 (Accounts)** — it must not weaken anything that spec
> locked. Phase 4A (sign-in) is implemented against the Supabase project
> `christisgod` (`qpqlllccyudypgdvtwcx`); see `AUTH-SETUP.md` for the console
> steps that turn it on. Phases 4B–4D remain specified but unbuilt.
>
> **Deviation from §2:** the author elected to ship **all three sign-in methods
> now — Google, Microsoft (Azure), and email/password** — rather than deferring
> Microsoft. The deferral rationale still holds as background, but the buttons are
> wired for all three; enabling Microsoft is a Supabase dashboard toggle.

## 1. Purpose

The site today is **anonymous**. Anyone reads the 17 MDX chapters; anyone talks to
the conversational engine (`web/src/components/live-debate.tsx` → the stateless
`/chat` service). Every AI session is amnesiac, every note is `localStorage`-bound
to one browser, and the only thing standing between the `ANTHROPIC_API_KEY` and
abuse is a per-**IP** rate limit that resets on every scale-to-zero cold start.

Add accounts so a *person* — not a browser — is remembered:

- **Remember AI chats** — conversations with the engine persist across sessions and devices.
- **Bookmarks & notes** — highlights/annotations on passages, synced everywhere (today: `reading-progress` + `localStorage`).
- **Rate-limit / protect the AI** — usage tied to a real identity, so cost and abuse are governable.
- **Gated / member content** — an entitlement tier for member-only *features* (see §4 for the mission caveat).

The design constraint mirrors `AI-SPEC.md`'s: this is **not** "bolt on a login
button." It is:

> **Add identity without compromising the two things that give this site its
> character — the reading experience stays fast, static, and open to everyone; and
> the AI hard gate (verify-before-show) is untouched.**

Auth is a *seam beside* the existing architecture, never a rewrite of it.

## 2. Decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Auth provider | **Supabase Auth** (managed Postgres + GoTrue) | One managed service gives OAuth, a Postgres DB, and **Row-Level Security** — the last is what makes storing sensitive religious Q&A defensible. |
| Identity providers | **Google now; Microsoft (Azure/Entra) deferred** | Google covers the consumer audience. Microsoft's value is institutional (churches/seminaries on M365) — no such audience exists yet, and adding `azure` later is a provider toggle with **zero** data-model or service change. See §7. |
| Web integration | **`@supabase/ssr`, cookie sessions** | Next 16 App Router: browser client + server client + middleware refresh. Sessions are JWTs in cookies, SSR-safe. |
| Persistence of personal data | **Browser ↔ Supabase direct, guarded by RLS** | Keeps the Python service **stateless** (its stated design value). The service never becomes a database. |
| AI history writes | **Browser writes turns after the stream completes** | Consonant with "client holds memory" (AI-SPEC §9). Service stays stateless; no service-role key in the hot path. Service-side writes are the documented upgrade, not day one. |
| Service ↔ identity | **Service *verifies* the Supabase JWT; it does not issue or store** | Read-only trust of the token lets `/chat` know *who* is asking — enough for per-user rate limits — without the service owning auth. |
| Reading content | **Stays static + open to all** | The book is evangelistic; it is never gated (§4). Only convenience/AI features sit behind a tier. |
| Rate-limit posture | **Identity-keyed, tiered** | Evolve `_client_ip` keying into `sub`-or-IP; authenticated users get a higher, durable budget; anonymous users keep the current per-IP cap. |

## 3. Architecture — the three-actor topology

Auth has to flow cleanly between three systems, two of which already exist:

```
  Browser (web/, Next 16)  ──cookie session (JWT)──▶  Supabase
   │   live-debate.tsx                                 (Auth · Postgres · RLS)
   │   read/[slug], reading-progress                        ▲
   │                                                        │ RLS: auth.uid() = user_id
   │──JWT as `Authorization: Bearer`──▶  Python service (service/api/app.py)
   │                                     stateless RAG · holds ANTHROPIC_API_KEY
   │                                     verifies JWT → per-user rate limit
   ▼
  reads/writes conversations, messages, annotations, profiles  (direct, RLS-guarded)
```

Three paths, three distinct trust models:

1. **Browser ↔ Supabase (auth + personal data).** Standard `@supabase/ssr` cookie
   session. CRUD on `annotations`, `conversations`, `messages` goes **direct** from
   the browser; **RLS is the guardrail**, so no bespoke API is needed for it.
2. **Browser ↔ Python `/chat` (the AI).** Unchanged wire protocol (`live-debate.tsx`
   already POSTs the full transcript). The **only** addition: forward the Supabase
   JWT as `Authorization: Bearer <jwt>`. The service verifies it (§5) to identify
   the caller and pick the right rate-limit budget. If absent → anonymous path,
   exactly today's behavior.
3. **Service ↔ Supabase.** By default **none** — the service stays stateless and
   the browser persists history. A future robust-write mode (service writes
   assistant turns with the service-role key) is the documented upgrade, gated
   behind an env flag so the default stays creds-light.

The keystone is path 2's *verify* step. Without it, per-user limits and history
are advisory. It is the one genuinely new piece of engineering; everything else is
configuration and RLS-guarded CRUD.

## 4. Data model (Supabase / Postgres) + what "gated" honestly means

Supabase manages `auth.users`. We add a `public` schema that references it. **Every
table below carries an RLS policy of the form `auth.uid() = user_id`** — a user can
only ever read/write their own rows, enforced *at the database*, not in app code. A
bug in application code cannot leak data past a correct RLS policy. That property is
non-negotiable here because we are storing **people's religious questions and
doubts under their identity** — arguably sensitive data.

| Table | Columns (sketch) | Serves | RLS |
|---|---|---|---|
| `profiles` | `id` → `auth.users.id`, `display_name`, `avatar_url`, `role ('free'\|'member'\|'admin')`, `created_at` | gated tier; auto-created on signup via trigger | owner read/write; `role` writable only by service-role |
| `conversations` | `id`, `user_id`, `title`, `created_at` | Remember AI chats | `auth.uid() = user_id` |
| `messages` | `id`, `conversation_id`, `role`, `content`, `citations jsonb`, `created_at` | the transcript itself (`citations` = the engine's verified refs) | via `conversation_id` → owner |
| `annotations` | `id`, `user_id`, `chapter_slug`, `anchor`, `note`, `color`, `created_at` | Bookmarks & notes; `chapter_slug` matches `src/content/*.mdx` | `auth.uid() = user_id` |
| `ai_usage` | `user_id`, `window_start`, `request_count`, `token_count` | durable per-user rate limit (§5) | owner read; service-role write |

**What "gated content" honestly means here — a mission caveat.** The instinct is
"members-only chapters." Reject that. The book is the site's evangelistic core; the
chapters are statically generated and should **stay open to everyone**, logged in or
not. Gating belongs on **convenience and cost surfaces**, not the gospel text:

- higher AI rate budget / longer history retention for members,
- unlimited saved notes vs. a free-tier cap,
- opt-in "debate mode" practice tooling, saved/shareable dialogues,
- author/admin curation (flagging a bad AI answer, moderating).

So `profiles.role` gates *features and quotas*, never the argument for Christ's
divinity. This keeps the paywall (if any) off the message.

## 5. The service bridge — JWT verification + identity-keyed rate limiting

This is the load-bearing change to `service/api/app.py`, and it is deliberately
small and backward-compatible.

**Verify.** On `/chat` (and `/debate`), if an `Authorization: Bearer <jwt>` is
present, verify it against Supabase's JWKS (or the shared JWT secret) → extract
`sub` (the user id). Invalid token ⇒ treat as anonymous (don't 401 a public chat
box; degrade to the anonymous tier). This slots in beside the existing
`DEBATE_API_TOKEN` check, which stays for non-browser callers.

**Rate-limit, tiered.** Today `_rate_ok()` keys `_hits` by `_client_ip(request)`.
Evolve the key:

- **Authenticated** (valid `sub`): key by `sub`, higher limit (`DEBATE_RATE_PER_MIN_AUTH`, default e.g. 30).
- **Anonymous** (no/invalid token): key by IP, **current** limit (`DEBATE_RATE_PER_MIN`, default 10) — unchanged behavior.

**Durability caveat (honest limit).** The in-memory `_hits` deque **resets on every
scale-to-zero cold start** and is per-instance — so today's limit is porous by
design. For authenticated users the real ceiling is the **`ai_usage` table**: the
service reads/increments it (service-role) as the durable, cross-instance budget.
In-memory stays as a cheap first-line burst guard; Postgres is the source of truth
for "how much has this person spent this window." Anonymous users keep only the
porous in-memory guard — acceptable, because the expensive privilege (a real
budget) is the carrot for signing in.

**Untouched.** The graph, the SSE vocabulary (`start`→…→`answer`→`done`), the hard
gate (`scripture_verifier ⛔`, `orthodoxy_guardrail ⛔`), `GracefulDegrade`, CORS —
none of it changes. Auth is a header the service reads, not a rewrite of the flow.

## 6. Delivery phases

Ordered so each phase ships value and de-risks the next. Bookmarks (B) deliberately
precedes AI history (C) even though remembering chats is the bigger prize — it
proves the whole auth + RLS + UI loop on something simple, with **zero** changes to
the Python service.

### Phase 4A — Foundation *(auth only; nothing else changes)*
- Supabase project; `@supabase/ssr` + `@supabase/supabase-js` in `web/`.
- Browser client, server client, middleware (session refresh), `/auth/callback` route handler.
- **Google** OAuth app → Supabase Google provider; callback `https://<project>.supabase.co/auth/v1/callback`.
- `profiles` table + `on_auth_user_created` trigger (default `role='free'`).
- Sign-in / sign-out UI (a control in `site-header.tsx`).
- **Ship gate:** a user can sign in with Google and see their name; anonymous
  reading + anonymous `/chat` are **byte-for-byte unchanged**.

### Phase 4B — Bookmarks & notes *(browser ↔ Supabase only)*
- `annotations` table + RLS.
- Wire into `read/[slug]` + `reading-progress`: highlight/annotate a passage,
  keyed by `chapter_slug` + `anchor`; hydrate on load for signed-in users.
- Free-tier note cap; graceful "sign in to save" prompt for anonymous readers.
- **Ship gate:** notes persist across devices for a signed-in user; RLS verified
  (user B cannot read user A's rows); the Python service is untouched.

### Phase 4C — AI history + per-user rate limit *(the service change)*
- `conversations` + `messages` tables + RLS; `ai_usage` table.
- `live-debate.tsx`: on a signed-in session, forward the JWT to `/chat`, and after
  the `done` event **persist** the user turn + assistant answer (with `citations`)
  to Supabase. A conversation list / resume UI.
- `service/api/app.py`: JWT verify + tiered/`ai_usage`-backed rate limit (§5).
- **Ship gate:** a signed-in reader resumes a prior conversation; authenticated
  and anonymous rate tiers both enforce; the hard gate and SSE contract regress on
  nothing (re-run the existing `service/tests/test_api_sse.py`, `test_conversation.py`).

### Phase 4D — Gated tier *(business logic, minimal code)*
- `profiles.role`-gated **features/quotas** per §4 (never chapter text).
- Admin surface for `role` changes (service-role only) and AI-answer flagging.
- **Ship gate:** a `member` sees member features; a `free` user is cleanly
  upsold; role can only be elevated server-side.

## 7. Microsoft — deferred, and why that's cheap

Start Google-only. Add Microsoft when — and only when — there is an **institutional**
audience (a church, seminary, or Christian school on Microsoft 365) that asks for
it. Reasoning:

- Google covers essentially all consumer readers; Microsoft *personal* accounts are
  a small slice who usually also have Google.
- Microsoft's real value is org sign-in ("use your seminary account"), which wants
  **single-tenant** Entra scope — a *different* config from consumer login, so
  guessing now would likely be wrong.
- Deferring costs nothing: Supabase treats `azure` as another provider toggle;
  `signInWithOAuth({ provider: 'azure' })` is the only new call, and **no** table,
  RLS policy, or service code changes. The `common` vs single-tenant scope decision
  is made at that point against a concrete audience.

## 8. What this preserves (the invariants)

Explicit, because the value of the site depends on them:

- **The reading experience stays static + open.** Anonymous readers get the same
  fast, cacheable book. The personal layer (notes, history) is client-side /
  dynamic and additive; it never blocks the gospel content.
- **The AI hard gate is untouched.** `scripture_verifier ⛔` and
  `orthodoxy_guardrail ⛔` run identically for anonymous and authenticated users.
  Identity changes *who is remembered and how much they may spend* — never *what is
  allowed to reach the screen*.
- **The Python service stays stateless** in the default design. It reads a JWT; it
  does not become a database.

## 9. Risks

- **Sensitive-data footprint.** Storing conversations means storing religious
  questions/doubts under an identity. Mitigations: RLS over app logic; a real
  "delete my account and all data" path from day one; retention limits on
  `messages`; minimal profile data.
- **Caching vs. auth.** Personalized/dynamic pages can't be cached like the static
  book. Mitigation: keep pages static and layer personal data client-side so an
  anonymous reader's fast path is preserved (this is also an invariant, §8).
- **RLS is the whole game.** A wrong policy silently leaks the most sensitive data
  on the site. Mitigation: policy tests as a ship gate for 4B/4C (user B cannot see
  user A); default-deny; never rely on the browser to scope reads.
- **Rate-limit porousness.** In-memory `_hits` resets on cold start and is
  per-instance. Mitigation: `ai_usage` in Postgres as the durable ceiling for
  authenticated users (§5); accept the porous in-memory guard for anonymous.
- **Operational surface step-up.** The site goes from "static + one stateless
  container" to "+ a stateful auth/DB service." Real added ops (backups, RLS
  review, auth-provider config). Worth it for history + notes; **overkill if the
  only goal were rate-limiting** — that alone could be done with anonymous device
  tokens. The four-goal scope is what justifies the DB.
- **Third-party dependency.** Supabase (and Google/Azure) become uptime + policy
  dependencies for the personal layer. The static book and the AI gate keep working
  if Supabase is down; only sign-in and persistence degrade.

## 10. Open questions (to resolve before 4A)

1. **Free-tier limits** — note cap, history retention window, anonymous vs.
   authenticated AI budget numbers (§5 uses placeholders).
2. **Is there a member tier at launch?** If not, build 4A–4C and leave `role` at
   `free` for everyone; ship 4D later. (`profiles.role` costs nothing to carry.)
3. **Anonymous → signed-in migration** — when a reader with `localStorage` notes /
   an in-progress chat signs in, do we import that local state into their account?
   (Nice-to-have; can be deferred.)
4. **Data deletion SLA** — what does "delete my data" guarantee and how fast?
5. **Where does the sign-in control live** — header only, or also a soft prompt at
   the chat box / note affordances?
