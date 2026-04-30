"""
conftest.py — Playwright e2e fixtures for the AI Village Workshop demos.

Exposes:
  - `http_server` (session): serves the workshop directory on a free port
    so demos can be loaded via http://, not file:// (matters for SSE,
    fetch CORS, and getting the same behavior as a real attendee).
  - `demo_url(name)` (function): returns the absolute URL for a demo file
    name (e.g. `demo_url('tmp-forge-live.html')`).
  - `page` (function, override): the standard pytest-playwright page
    fixture with console-error and pageerror listeners attached. Any
    console error during a test causes the test to fail at teardown —
    silent JS exceptions don't escape unnoticed.

Why a custom http.server: pytest-playwright's `page` lets you `page.goto()`
a `file://` URL but several demo behaviors (Ctrl+P toggle, fetch to the
relay, console behavior) only behave correctly under http://, and we want
the e2e tests to mirror what an attendee actually runs.
"""

import http.server
import os
import socket
import socketserver
import threading

import pytest

WORKSHOP = os.path.dirname(os.path.abspath(__file__))


def _free_port():
    """Bind to 0, read the assigned port, release. The narrow window between
    release and the test server's bind is acceptable for local-only tests."""
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope='session')
def http_server():
    port = _free_port()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=WORKSHOP, **kw)
        def log_message(self, *a, **kw):
            pass

    class ReuseTCPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    httpd = ReuseTCPServer(('127.0.0.1', port), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f'http://127.0.0.1:{port}'
    httpd.shutdown()
    httpd.server_close()


@pytest.fixture
def demo_url(http_server):
    def _url(name):
        return f'{http_server}/demos/{name}'
    return _url


@pytest.fixture
def safe_page(page):
    """Wraps pytest-playwright's `page` fixture with console-error and
    pageerror listeners. Tests don't see the listener directly — it raises
    at fixture teardown if any error fires during the test. Use this
    fixture in tests instead of the bare `page` so silent JS exceptions
    don't escape unnoticed."""
    errors = []

    def on_console(msg):
        if msg.type == 'error':
            errors.append(f'[console.error] {msg.text}')

    def on_pageerror(exc):
        errors.append(f'[pageerror] {exc}')

    page.on('console', on_console)
    page.on('pageerror', on_pageerror)
    yield page
    if errors:
        pytest.fail('Console errors during test:\n  ' + '\n  '.join(errors[:10]))
