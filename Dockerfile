# Container for the "Test the Case" apologetics engine (service/api/app.py).
# Build context is the REPO ROOT — the service reads sibling dirs at runtime:
#   /app/service            the graph + API
#   /app/shared/canon       the full-KJV verification store (kjv.json.gz, book-meta)
#   /app/web/src/content     the 17 MDX chapters (retrieval corpus)
#
# Build:  docker build -t christisgod-service .
# Run:    docker run -p 8080:8080 -e ANTHROPIC_API_KEY=... christisgod-service
FROM python:3.11-slim

# libgomp1 is needed by onnxruntime (Chroma's local embedding model).
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies first for layer caching.
COPY service/requirements.txt service/requirements.txt
RUN pip install --no-cache-dir -r service/requirements.txt

# The pieces the running service reads.
COPY service/ service/
COPY shared/ shared/
COPY web/src/content/ web/src/content/

# Pre-build the Chroma index at image-build time so the embedding model is baked
# in and the first request isn't a cold download. Needs network during build.
# --force makes the rebuild unconditional, so a stale index can never be baked in
# (e.g. if service/.chroma were ever removed from .dockerignore).
RUN cd service && python -m graph.retrieval --build --force

ENV PORT=8080 \
    DEBATE_TERMINAL=respond \
    PYTHONUNBUFFERED=1
EXPOSE 8080

WORKDIR /app/service
# Shell form so ${PORT} is expanded (hosts inject their own PORT).
CMD uvicorn api.app:app --host 0.0.0.0 --port ${PORT}
