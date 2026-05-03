#!/usr/bin/env python3
"""TMP Local Relay — workshop-root entry point.

Thin shim that bootstraps the in-tree src/tmp_relay/ package and runs
its CLI. The actual implementation (HTTP routing, SSE handler, claude
subprocess plumbing, settings) lives under src/tmp_relay/.

Why this file still exists when there's also a `tmp-relay` console
script (via pyproject.toml): attendees clone the repo and run
`python3 relay.py` without first having to `pip install .`. Both
entry points end at the same code.

Usage:
  python3 relay.py            (no install — uses the in-tree package)
  pip install . && tmp-relay  (installed; same behavior)

Test: curl http://localhost:3001/health
"""

import os
import sys

# Bootstrap: make the in-tree src/tmp_relay/ package importable without
# requiring `pip install -e .`. Power users who pip-install get the
# `tmp-relay` console script instead — both end up at the same code.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, 'src'))

from tmp_relay.cli import main

if __name__ == '__main__':
    main()
