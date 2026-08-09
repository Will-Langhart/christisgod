# Deploying the live apologetics service

The `Dockerfile` (repo root) builds the FastAPI/SSE service in `service/api/app.py`.
It is container-verified locally (health, auth, validation). Pushing to a cloud
host requires **your** host login and secrets — the steps below are yours to run.

## What the container needs

| Env var | Required | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | **yes** | the graph 400s/errs without it |
| `DEBATE_API_TOKEN` | see note | if set, **both** `/chat` and `/debate` require `Authorization: Bearer <token>`. For a **public browser** chat, leave it **unset** (a browser token isn't secret) and rely on the CORS allow-list + rate limit. |
| `DEBATE_RATE_PER_MIN` | no (default 10) | per-IP requests/minute, shared across `/chat` + `/debate`. Each conversational turn is one request; raise it if real users hit the limit. |
| `CORS_ORIGINS` | no | comma-separated; defaults to christisgod.app + localhost |
| `LANGSMITH_API_KEY` / `LANGSMITH_PROJECT` | no | tracing (project defaults to `christisgod-debate`) |
| `DEBATE_TERMINAL` | baked to `respond` | already set in the image |

> ⚠️ Each `/debate` call spends Anthropic budget. `DEBATE_API_TOKEN` + the rate
> limit are MVP protection; a browser token is not truly secret. Add real per-user
> auth (or a server-side proxy) before promoting this widely.

## Local (build + smoke test)

```bash
docker build -t christisgod-service .
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=sk-... christisgod-service
curl localhost:8080/health

# Phase 3 conversational endpoint (what the site's chat box calls):
curl -N -X POST localhost:8080/chat \
  -H 'content-type: application/json' \
  -d '{"persona":"seeker","mode":"direct","messages":[{"role":"user","content":"Does John 1:1 call Jesus God?"}]}'

# Phase 2 single-shot endpoint (still available):
curl -N -X POST localhost:8080/debate \
  -H 'content-type: application/json' \
  -d '{"persona":"skeptic","objection":"Was Jesus made God at Nicaea?"}'
```

The image is Docker-verified for Phase 3: `/health`, `/chat` (full SSE stream to
an `approved` answer), and the CORS allow-list all pass in the container.

## Fly.io (uses fly.toml)

```bash
brew install flyctl && fly auth login          # your credentials
fly launch --copy-config --no-deploy           # or edit `app` name in fly.toml first
fly secrets set ANTHROPIC_API_KEY=sk-... DEBATE_API_TOKEN=$(openssl rand -hex 16) \
  LANGSMITH_API_KEY=lsv2_... LANGSMITH_PROJECT=christisgod
fly deploy
fly open        # note the https URL
```

## Render (free Docker web service — no card) — recommended

Uses `render.yaml` (repo root). The repo must be on GitHub.

1. Push this branch to GitHub.
2. Render dashboard → **New → Blueprint** → pick this repo/branch. It reads
   `render.yaml` and provisions a free Docker web service.
3. In the service's **Environment**, set the secret values (`sync: false`):
   `ANTHROPIC_API_KEY`, `DEBATE_API_TOKEN` (any random string), and optionally
   `LANGSMITH_API_KEY`. The non-secret vars come from the blueprint.
4. Render builds the `Dockerfile` and deploys. First build downloads the embedding
   model; later builds are cached. `healthCheckPath: /health`.

Notes:
- **Free plan = 512 MB RAM.** onnxruntime + chromadb + the graph may be tight; if
  it OOMs on boot, bump to the Starter instance (or trim memory).
- Free services **spin down after ~15 min idle** and cold-start on the next hit
  (adds a few seconds). Fine for sporadic traffic.

## Railway (Dockerfile auto-detected)

Point a service at this repo (root `Dockerfile`), set the env vars from the table
above. Railway needs a card/verified account.

## Wiring the site's live mode

The live chat box on `/dialogues` (`web/src/components/live-debate.tsx`) is built
and **dormant until configured** — it POSTs to the service's `/chat` directly from
the browser (no Vercel proxy, so long streams aren't cut by function timeouts). It
offers both **Ask a question** (direct Q&A) and **Debate me** (the persona spars
with the reader) modes.

To activate:
1. On the **Vercel (web) project**, set `NEXT_PUBLIC_DEBATE_API=https://<render-url>`
   (build-time public var). Optionally `NEXT_PUBLIC_DEBATE_TOKEN` if the service
   has `DEBATE_API_TOKEN` set — but a browser token is not secret, so for public
   browser use prefer leaving the service token unset and relying on its CORS
   allow-list + rate limit.
2. Redeploy the site (`cd web && vercel deploy --prod --yes`). The box appears.

The service's `CORS_ORIGINS` must include `https://christisgod.app` (it does by
default). The static 24-dialogue library works with or without the live service.
