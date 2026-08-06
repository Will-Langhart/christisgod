# Deploying the live apologetics service

The `Dockerfile` (repo root) builds the FastAPI/SSE service in `service/api/app.py`.
It is container-verified locally (health, auth, validation). Pushing to a cloud
host requires **your** host login and secrets — the steps below are yours to run.

## What the container needs

| Env var | Required | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | **yes** | the graph 400s/errs without it |
| `DEBATE_API_TOKEN` | strongly recommended | if set, `/debate` requires `Authorization: Bearer <token>`. Guards against non-browser abuse. |
| `DEBATE_RATE_PER_MIN` | no (default 10) | per-IP requests/minute |
| `CORS_ORIGINS` | no | comma-separated; defaults to christisgod.app + localhost |
| `LANGSMITH_API_KEY` / `LANGSMITH_PROJECT` | no | tracing (project defaults to `christisgod-debate`) |
| `DEBATE_TERMINAL` | baked to `respond` | already set in the image |

> ⚠️ Each `/debate` call spends Anthropic budget. `DEBATE_API_TOKEN` + the rate
> limit are MVP protection; a browser token is not truly secret. Add real per-user
> auth (or a server-side proxy) before promoting this widely.

## Local (build + smoke test)

```bash
docker build -t christisgod-service .
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=sk-... -e DEBATE_API_TOKEN=dev christisgod-service
curl localhost:8080/health
curl -N -X POST localhost:8080/debate -H 'authorization: Bearer dev' \
  -H 'content-type: application/json' \
  -d '{"persona":"skeptic","objection":"Was Jesus made God at Nicaea?"}'
```

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

## Wiring the site's live mode (later)

Once deployed, set `NEXT_PUBLIC_DEBATE_API=https://<your-service-url>` on the web
project and add the live-mode box to `/dialogues` (not yet built). The static
24-dialogue library works with or without the live service.
