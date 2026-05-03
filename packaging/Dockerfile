# packaging/Dockerfile — workshop relay in a single container.
#
# Build:
#   docker build -t tmp-workshop -f packaging/Dockerfile .
#
# Run (from the workshop root or anywhere — image is self-contained):
#   docker run --rm -p 3001:3001 tmp-workshop
#   # → open http://localhost:3001/ in your host browser
#
# Providers in-container:
#   ✓ DEMO MODE        works (no network)
#   ✓ ANTHROPIC        works (browser → api.anthropic.com directly)
#   ✓ OPENROUTER       works (browser → openrouter.ai directly)
#   ✓ OR FREE          works
#   ✓ OLLAMA           works IF Ollama is reachable from inside the
#                      container — pass `--add-host host.docker.internal:host-gateway`
#                      and use http://host.docker.internal:11434 in the demo
#   ✗ CLAUDE CODE      needs the `claude` CLI + the operator's auth tokens.
#                      Two options:
#                       (a) mount your config:
#                           docker run -v ~/.config/claude:/root/.config/claude ...
#                       (b) skip and use one of the other providers.
#                      Detailed instructions: docs/attendee/providers/claude-code.md
#
# Image size: ~80 MB (python:3.12-slim + aiohttp). The claude CLI is
# deliberately NOT installed — its install pulls Node + npm + ~250 MB,
# and the auth flow is per-user OAuth that doesn't survive baking into
# an image anyway.

FROM python:3.12-slim AS runtime

# Install minimal runtime tools — curl for the in-container /health
# probe and tini for proper signal handling so Ctrl+C reaches Python
# instead of being swallowed by PID 1.
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workshop

# Copy package metadata first so dependency install caches when only
# source files change.
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install in editable mode so the in-tree src/tmp_relay/ is the
# canonical Python package; aiohttp comes from pyproject.toml deps.
RUN pip install --no-cache-dir .

# Now copy the rest — these change frequently and don't need their own
# dep-install layer.
COPY relay.py ./
COPY web/ ./web/
COPY labs/ ./labs/
COPY docs/ ./docs/

# Bind 0.0.0.0 inside the container so docker's port forwarding can
# reach the relay. The relay's host exposure is still controlled by
# the operator's `-p` flag (e.g., `-p 127.0.0.1:3001:3001` keeps it
# loopback-only on the host). Outside docker, the same env var is
# what bin/start.{sh,ps1}'s --bind toggle uses.
ENV TMP_RELAY_BIND=0.0.0.0
ENV TMP_RELAY_PORT=3001

EXPOSE 3001

# Healthcheck so docker reports the relay's liveness, not just the
# container's. /health is the cheap endpoint we already snapshot.
HEALTHCHECK --interval=15s --timeout=3s --start-period=3s --retries=3 \
    CMD curl -fsS http://127.0.0.1:3001/health || exit 1

# tini → PID 1 → handles signals; relay.py is invoked directly so
# Python's KeyboardInterrupt path runs cleanly on docker stop.
ENTRYPOINT ["tini", "--"]
CMD ["python3", "relay.py"]
