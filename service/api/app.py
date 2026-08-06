"""Phase 2 live service — FastAPI + Server-Sent Events over the debate graph.

The SAME graph as the Phase 1 offline runner (AI-SPEC.md §5), but the terminal is
`respond` (emit the answer) instead of `human_approval`, and if the retry budget
is exhausted it degrades gracefully rather than shipping an unverified answer.

Run (from service/, in the venv, with ANTHROPIC_API_KEY set):
    uvicorn api.app:app --port 8600 --reload

Endpoints:
    GET  /health          -> liveness + available personas
    POST /debate          -> text/event-stream of the debate for one objection
"""

from __future__ import annotations

import os

# Live service emits the answer rather than awaiting human approval. Must be set
# before graph.config is first imported (it reads this at import time).
os.environ.setdefault("DEBATE_TERMINAL", "respond")

import sys  # noqa: E402
import time  # noqa: E402
from collections import defaultdict, deque  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Header, Request  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import JSONResponse, StreamingResponse  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from canon import lookup_verse  # noqa: E402
from api.sse import PERSONAS, ROLE_EVENT, format_event, validate_persona  # noqa: E402

app = FastAPI(title="Christ Is God — Test the Case", version="0.1.0")

# Restrict origins in production via CORS_ORIGINS (comma-separated).
_origins = os.getenv(
    "CORS_ORIGINS",
    "https://christisgod.app,http://localhost:3000,http://localhost:3100",
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins if o.strip()],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- lightweight abuse protection --------------------------------------------
# Each /debate call spends Anthropic budget, so guard the endpoint. If
# DEBATE_API_TOKEN is set, a matching `Authorization: Bearer <token>` is required
# (protects against non-browser abuse; a browser token is not truly secret — put
# real per-user auth in front before heavy promotion). Plus a per-IP rate limit.
_API_TOKEN = os.getenv("DEBATE_API_TOKEN")
_RATE_PER_MIN = int(os.getenv("DEBATE_RATE_PER_MIN", "10"))
_hits: dict[str, deque] = defaultdict(deque)


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    return fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "?")


def _rate_ok(ip: str) -> bool:
    now = time.time()
    dq = _hits[ip]
    while dq and now - dq[0] > 60:
        dq.popleft()
    if len(dq) >= _RATE_PER_MIN:
        return False
    dq.append(now)
    return True


_graph = None


def graph():
    """Build the compiled graph once, lazily (keeps startup/import cheap)."""
    global _graph
    if _graph is None:
        from graph import build_graph

        _graph = build_graph()
    return _graph


class DebateRequest(BaseModel):
    persona: str
    objection: str
    objection_href: str | None = "/"
    objection_label: str | None = "the relevant chapter"


@app.get("/health")
def health():
    return {"ok": True, "personas": list(PERSONAS)}


def _stream(req: DebateRequest):
    state = {
        "persona": req.persona,
        "objection": req.objection,
        "objection_href": req.objection_href or "/",
        "objection_label": req.objection_label or "the relevant chapter",
        "retries": 0,
        "status": "running",
    }
    from graph.tracing import run_config

    yield format_event("start", {"persona": req.persona, "objection": req.objection})

    seen = 0
    last: dict = state
    try:
        for snapshot in graph().stream(state, config=run_config(req.persona, req.objection),
                                       stream_mode="values"):
            last = snapshot
            turns = snapshot.get("transcript", [])
            while seen < len(turns):
                turn = turns[seen]
                seen += 1
                yield format_event(ROLE_EVENT.get(turn["role"], "turn"),
                                   {"content": turn["content"]})
    except Exception as e:  # noqa: BLE001 — surface as an SSE error, don't 500 mid-stream
        yield format_event("error", {"message": f"{type(e).__name__}: {e}"})
        return

    verified = [
        {"display": c["display"], "text": lookup_verse(c["display"])}
        for c in last.get("citations", [])
        if c.get("ok") and c.get("display")
    ]
    yield format_event("done", {
        "status": last.get("status"),
        "answer": last.get("final", ""),
        "citations": verified,
        "warnings": last.get("citation_warnings", []),
    })


@app.post("/debate")
def debate(req: DebateRequest, request: Request, authorization: str | None = Header(default=None)):
    if _API_TOKEN and authorization != f"Bearer {_API_TOKEN}":
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    if not _rate_ok(_client_ip(request)):
        return JSONResponse({"error": "rate limit exceeded, try again shortly"}, status_code=429)
    err = validate_persona(req.persona)
    if err:
        return JSONResponse({"error": err}, status_code=400)
    if not req.objection.strip():
        return JSONResponse({"error": "objection must not be empty"}, status_code=400)
    return StreamingResponse(_stream(req), media_type="text/event-stream")
