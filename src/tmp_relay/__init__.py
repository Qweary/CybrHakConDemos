"""tmp_relay — local relay that bridges browser demos to the claude CLI.

The package is split across:
  settings           — env-var defaults and tunables
  claude_subprocess  — args + path resolution + chunked stdin write
  sse                — SSE handler (long, async, stall-watched)
  server             — aiohttp app, routes, middlewares, JSON handler
  cli                — entry point used by both `tmp-relay` and relay.py

Bind is 127.0.0.1 by default — see settings.PORT and the bind logic in
cli.main(). All other tunables are env-var overridable; see settings.
"""

__version__ = '0.1.0'
