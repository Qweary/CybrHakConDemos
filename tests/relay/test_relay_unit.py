"""Direct unit tests against swarm_relay modules.

Two slices:
  - Pure-function tests (build_args, per_call_timeout, CORS_HEADERS) —
    no event loop, no network, instant.
  - In-process app tests (aiohttp.test_utils.TestClient) — spin up
    make_app() against a real loop and hit endpoints. No claude binary
    needed because we never POST to /v1/chat here; the test_snapshots
    /health check + the live harness cover the subprocess path.

Imports rely on pyproject.toml `pythonpath = ["src"]` so `pytest tests/`
finds swarm_relay without `pip install -e .`.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from unittest.mock import MagicMock

from aiohttp.test_utils import TestClient, TestServer
from yarl import URL

from swarm_relay.claude_subprocess import build_args
from swarm_relay.server import make_app, per_call_timeout
from swarm_relay.settings import (
    CORS_HEADERS,
    MAX_PERCALL_TIMEOUT_SEC,
    MIN_PERCALL_TIMEOUT_SEC,
    TIMEOUT_SEC,
)


# ── build_args (pure function, no subprocess) ────────────────────────


def test_build_args_streaming_includes_stream_json():
    args = build_args('/usr/bin/claude', 'be brief', 'haiku', streaming=True)
    assert args[0] == '/usr/bin/claude'
    assert '-p' in args
    assert '--model' in args and 'haiku' in args
    assert '--output-format' in args
    fmt_idx = args.index('--output-format')
    assert args[fmt_idx + 1] == 'stream-json'
    assert '--include-partial-messages' in args
    assert '--verbose' in args  # required by CLI when stream-json + --print


def test_build_args_json_omits_streaming_flags():
    args = build_args('/c', '', 'haiku', streaming=False)
    fmt_idx = args.index('--output-format')
    assert args[fmt_idx + 1] == 'json'
    assert 'stream-json' not in args
    assert '--include-partial-messages' not in args


def test_build_args_omits_system_when_empty_string():
    args = build_args('/c', '', 'haiku', streaming=True)
    assert '--system-prompt' not in args


def test_build_args_includes_system_when_provided():
    args = build_args('/c', 'be brief and structured', 'haiku', streaming=True)
    assert '--system-prompt' in args
    sys_idx = args.index('--system-prompt')
    assert args[sys_idx + 1] == 'be brief and structured'


def test_build_args_includes_subprocess_safety_flags():
    """The flags that turn `claude -p` from a full agent into a thin
    completion endpoint. Cuts ~30k cached tokens to ~3k per call."""
    args = build_args('/c', 'sys', 'haiku', streaming=False)
    assert '--tools' in args
    tools_idx = args.index('--tools')
    assert args[tools_idx + 1] == ''  # empty string strips the toolset
    assert '--disable-slash-commands' in args
    assert '--setting-sources' in args
    assert '--no-session-persistence' in args
    assert '--permission-mode' in args


# ── per_call_timeout (request → effective timeout) ───────────────────


def _mock_request(timeout_param: str | int | None = None):
    """Minimal request stub — per_call_timeout only reads
    request.rel_url.query.get('timeout')."""
    req = MagicMock()
    if timeout_param is None:
        req.rel_url = URL('/v1/chat')
    else:
        req.rel_url = URL(f'/v1/chat?timeout={timeout_param}')
    return req


def test_per_call_timeout_default_when_unset():
    assert per_call_timeout(_mock_request()) == TIMEOUT_SEC


def test_per_call_timeout_returns_in_range_value_unchanged():
    assert per_call_timeout(_mock_request(120)) == 120


def test_per_call_timeout_clamps_below_min():
    assert per_call_timeout(_mock_request(0)) == MIN_PERCALL_TIMEOUT_SEC
    assert per_call_timeout(_mock_request(-100)) == MIN_PERCALL_TIMEOUT_SEC


def test_per_call_timeout_clamps_above_max():
    assert per_call_timeout(_mock_request(99999)) == MAX_PERCALL_TIMEOUT_SEC


def test_per_call_timeout_invalid_falls_through_to_default():
    """Garbage in shouldn't blow up — falls through to TIMEOUT_SEC."""
    assert per_call_timeout(_mock_request('not-a-number')) == TIMEOUT_SEC
    assert per_call_timeout(_mock_request('')) == TIMEOUT_SEC  # empty query string


# ── CORS_HEADERS shape ───────────────────────────────────────────────


def test_cors_headers_has_three_required_fields():
    assert set(CORS_HEADERS) == {
        'Access-Control-Allow-Origin',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Headers',
    }


def test_cors_headers_origin_is_permissive():
    """Per FRG-10 user direction: relay stays a relay (* origin)."""
    assert CORS_HEADERS['Access-Control-Allow-Origin'] == '*'


def test_cors_headers_methods_include_post_and_options():
    methods = CORS_HEADERS['Access-Control-Allow-Methods']
    assert 'POST' in methods
    assert 'OPTIONS' in methods
    assert 'GET' in methods


# ── In-process app (aiohttp test client; no claude needed) ───────────


@asynccontextmanager
async def _client():
    """Spin up make_app() bound to a TestServer, hand back a TestClient.
    No subprocess, no real port — runs entirely in the asyncio loop.
    Static layer still mounts because WEB_DIR exists in this repo;
    that's fine, /forge.html etc. would serve. We only test routes
    that don't need a real claude binary."""
    app = make_app()
    async with TestClient(TestServer(app)) as c:
        yield c


def _async_test(coro):
    """Drive an async test through asyncio.run. Lets us avoid adding
    pytest-asyncio just for a handful of integration tests."""
    return asyncio.run(coro)


def test_health_returns_status_ok():
    async def go():
        async with _client() as c:
            r = await c.get('/health')
            assert r.status == 200
            body = await r.json()
            assert body['status'] == 'ok'
            assert 'claude_binary_present' in body
            assert 'claude_binary_path' in body
    _async_test(go())


def test_health_carries_cors_headers():
    """cors_middleware must apply to every response, including JSON."""
    async def go():
        async with _client() as c:
            r = await c.get('/health')
            assert r.headers.get('Access-Control-Allow-Origin') == '*'
            assert 'POST' in r.headers.get('Access-Control-Allow-Methods', '')
    _async_test(go())


def test_get_v1_chat_returns_405_with_allow_header():
    """BUG-04: GET /v1/chat must 405, not be swallowed by static catch-all."""
    async def go():
        async with _client() as c:
            r = await c.get('/v1/chat')
            assert r.status == 405
            assert r.headers.get('Allow') == 'POST, OPTIONS'
    _async_test(go())


def test_options_preflight_returns_204_with_cors():
    async def go():
        async with _client() as c:
            r = await c.options('/v1/chat')
            assert r.status == 204
            assert r.headers.get('Access-Control-Allow-Origin') == '*'
    _async_test(go())


def test_dotfile_filter_blocks_root_dotfile():
    """BUG-04: a .env or .git dropped into web/ must not leak."""
    async def go():
        async with _client() as c:
            r = await c.get('/.env')
            assert r.status == 404
    _async_test(go())


def test_dotfile_filter_blocks_nested_dotfile():
    """A dotfile anywhere in the path must 404 (not just the basename)."""
    async def go():
        async with _client() as c:
            r = await c.get('/forge/.gitignore')
            assert r.status == 404
            r = await c.get('/.git/config')
            assert r.status == 404
    _async_test(go())


def test_dotfile_filter_lets_normal_paths_through():
    """The filter must NOT 404 paths that merely contain a dot in
    the filename (e.g., /forge.html)."""
    async def go():
        async with _client() as c:
            r = await c.get('/forge.html')
            assert r.status == 200  # served by the static layer
    _async_test(go())


def test_index_route_serves_launcher():
    """GET / serves web/index.html (Phase 4c launcher)."""
    async def go():
        async with _client() as c:
            r = await c.get('/')
            assert r.status == 200
            body = await r.text()
            assert 'DEMO LAUNCHER' in body  # cyberpunk title in the launcher
    _async_test(go())
