# Packaging — runtime wrappers

Choose whichever fits your environment. All four spin up the same relay
+ static demo host on `http://localhost:3001/`.

| Wrapper | Where | When to use |
|---|---|---|
| **Bash launcher** | `bin/start.sh` | macOS / Linux from a fresh clone. Auto-detects `uv` or sets up a venv. |
| **PowerShell launcher** | `bin/start.ps1` | Windows from a fresh clone. Same UX as bash. |
| **Docker** | `packaging/Dockerfile` | Reproducible everywhere. ~150 MB image. CLAUDE CODE provider needs `~/.config/claude/` mounted. |
| **Nix flake** | `packaging/flake.nix` | NixOS or Nix-on-anything. `nix run path:packaging#relay`. Solves the Phase 0 Playwright pain. |
| **VS Code devcontainer** | `.devcontainer/devcontainer.json` | "Reopen in Container" inside VS Code. python:3.12-bookworm with port 3001 forwarded. |

## Quick reference

```bash
# Bash / PowerShell launcher
bin/start.sh                          # macOS / Linux
bin\start.ps1                         # Windows PowerShell
bin/start.sh --port 4000              # alternate port
bin/start.sh --bind 0.0.0.0           # exposes on LAN (5s confirmation)
bin/start.sh --skip-checks            # skip doctor

# Docker
docker build -t tmp-workshop -f packaging/Dockerfile .
docker run --rm -p 3001:3001 tmp-workshop

# Nix flake
nix run path:packaging#relay
cd packaging && nix develop           # dev shell with chromium + pytest

# VS Code devcontainer
# Open the workshop in VS Code → Command Palette → "Reopen in Container"
```

## Env vars (honored by all wrappers)

| Var | Default | Notes |
|---|---|---|
| `TMP_RELAY_BIND` | `127.0.0.1` | Set to `0.0.0.0` to listen on all interfaces. Dockerfile sets this; bin/start.sh sets it from `--bind`. |
| `TMP_RELAY_PORT` | `3001` | Match your `-p` host:container forwarding when in Docker. |
| `TMP_RELAY_TIMEOUT_SEC` | `600` | Per-call subprocess wall-clock. |
| `TMP_RELAY_SUBPROC_LIMIT` | `4194304` (4 MB) | Per-line stream-json buffer. |
| `TMP_RELAY_MODEL` | `claude-haiku-4-5` | Override the default model. Empty = honor the body's `model` field. |

## Windows-specific notes

See `packaging/windows-setup.md` for PowerShell execution policy,
`claude.cmd` resolution, and the Python 3.12+ requirement (caused by
asyncio's subprocess routing for `.cmd` files).

## What about CI?

Out of scope for this kit. The user explicitly chose local-only
operation; no GitHub Actions workflow is shipped.
