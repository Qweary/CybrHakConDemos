# Phase 0 — Hardcoded Path & Assumption Audit

Read-only enumeration of every hardcoded path, magic constant, layout
assumption, and cross-file coupling in the workshop today. Each finding
is tagged with the phase that should fix it. No code changes in this
phase — output is just this document.

Generated against the `refactor/restructure` branch root commit.

---

## 1. `ai-village-workshop/` parent-directory assumption

The repo *was* a subdirectory under that name; the layout was flattened
but references survived. Tests, docs, and instructions all still point
at a directory that no longer exists.

### 1a. Test code (Phase 2 fix)

| File | Line | Reference |
|---|---|---|
| `test_workshop.py` | 14–15 | `WORKSHOP = …; ROOT = os.path.dirname(WORKSHOP)` — `ROOT` is now `…/Qweary/`, not the workshop parent |
| `test_workshop.py` | 17–25 | `DEMOS_SRC = ROOT/demos`, `DEMOS_WS = WORKSHOP/demos` — both used to differ; now collapsed to the same path or one is missing |
| `test_workshop.py` | 638 | Section header literally says `demos/ == ai-village-workshop/demos/` |
| `test_workshop.py` | 638–649 | Hash-parity check causes the only 3 failing tests on this branch |
| `test_workshop_e2e.py` | 10 | Docstring `cd ai-village-workshop` |

### 1b. Documentation (Phase 2 fix)

| File | Line | Reference |
|---|---|---|
| `README.md` | 62 | Tree literal `ai-village-workshop/` |
| `TESTING.md` | 13, 19, 35, 47, 54, 72, 75, 92 | Multiple `ai-village-workshop/...` paths |
| `ATTENDEE-SETUP.md` | 52, 83 | "from the `ai-village-workshop/` directory" |
| `CLAUDE-CODE-SETUP.md` | 38 | "from the `ai-village-workshop/` directory" |
| `OLLAMA-SETUP.md` | 101 | `inside ai-village-workshop/` |
| `WORKSHOP-GUIDE.md` | 57, 72, 115 | Three `cd ai-village-workshop && ...` examples |

### 1c. Shell (Phase 2 fix)

`run_tests.sh` itself uses `WORKSHOP="$(cd "$(dirname "$0")" && pwd)"`
which is correct (script-dir-relative), so no change there. The
*comments and error messages* assume `.venv-e2e/` lives next to the
script — true today but worth documenting once we move tests under
`tests/`.

---

## 2. `python -m http.server` exposure pattern

Multiple docs tell attendees to run `python3 -m http.server 8080`. By
default that binds `0.0.0.0` and serves the *entire workshop tree* —
which is exactly the surprise-network-exposure risk you flagged.

| File | Line | Reference |
|---|---|---|
| `ATTENDEE-SETUP.md` | 84–85, 88, 114 | "`python3 -m http.server 8080`" + `localhost:8080/demos/...` |
| `OLLAMA-SETUP.md` | 101 | Same recommendation in CORS troubleshooting |
| `WORKSHOP-GUIDE.md` | 72, 75, 103, 115 | Repeated four times |
| `CLAUDE-CODE-SETUP.md` | 75 | "(file:// or localhost:8080)" — neutral mention |
| `README.md` | (implicit) | "How to run" implies opening files directly |

**Resolution (per locked decision):** all of these go away in Phase 4.
The relay becomes the single host on `127.0.0.1:3001`. Replace every
`localhost:8080/demos/X.html` with `http://localhost:3001/X.html`.

The `conftest.py` `http_server` fixture (lines 21, 36, 46, 56, 59) was
the test-side equivalent of that pattern. It's correctly bound to
`127.0.0.1` (random port, not 0.0.0.0:8080) so it's safe — but in
Phase 7 we should kill it and have e2e tests start the real relay
instead, so they exercise the same code path attendees use.

---

## 3. Hardcoded `localhost:3001` (relay endpoint)

The relay's address is duplicated across both code and docs. Any future
port change requires editing 8+ places.

### 3a. Code

| File | Line | Reference |
|---|---|---|
| `relay.py` | 41 | `PORT = 3001` (the canonical declaration) |
| `relay.py` | 11, 33 | Doc comments quoting `localhost:3001` |
| `demos/tmp-forge-live.html` | 1950, 1988 | `fetch('http://localhost:3001/v1/chat'...)` x2 |
| `demos/tmp-combat-live.html` | 2247, 2282 | Same x2 |
| `demos/tmp-evolve-live.html` | 1553, 1588 | Same x2 |
| `test_relay_e2e.py` | 33 | `RELAY = 'http://localhost:3001'` |

### 3b. Docs

| File | Lines |
|---|---|
| `CLAUDE-CODE-SETUP.md` | 48, 49, 60, 78, 106–111, 114, 136 — 8 references |
| `WORKSHOP-GUIDE.md` | 29, 57 |
| `ATTENDEE-SETUP.md` | 55 |

**Resolution:** keep `PORT = 3001` as the default but let it become
configurable via `--port` / env var in Phase 5. The 6 demo `fetch()`
URLs become same-origin (`/v1/chat`, no host) once Phase 4 puts demos
behind the relay — that single change deletes 6 hardcoded URLs and
makes the port irrelevant to the demos.

---

## 4. Hardcoded `localhost:11434` (Ollama)

Six call sites + four doc references. Less critical than 3001 because
Ollama itself owns the port — but each demo independently builds the
URL string. A shared `providers.js` (Phase 6) collapses this to one
constant.

| File | Lines |
|---|---|
| `demos/tmp-forge-live.html` | 2079 |
| `demos/tmp-combat-live.html` | 2363 |
| `demos/tmp-evolve-live.html` | 1599 |
| `OLLAMA-SETUP.md` | 40, 43, 60, 85 |
| `ATTENDEE-SETUP.md` | 25 |
| `WORKSHOP-GUIDE.md` | 31 |

---

## 5. Hardcoded model strings & token budgets

Model identity and budget are split across relay env-var defaults +
inline demo body. There is no single source of truth.

### 5a. Relay (`relay.py`)

| Line | Constant |
|---|---|
| 46 | `TIMEOUT_SEC = int(os.environ.get('TMP_RELAY_TIMEOUT_SEC', '600'))` |
| 53 | `SUBPROC_LIMIT = int(os.environ.get('TMP_RELAY_SUBPROC_LIMIT', str(4 * 1024 * 1024)))` |
| 58 | `DEFAULT_MODEL = os.environ.get('TMP_RELAY_MODEL', 'claude-haiku-4-5')` |
| 152 | Body fallback `'claude-haiku-4-5'` (duplicates 58) |
| 287 | `STALL_WARN_SEC = 30` (function-local, not configurable) |
| 134 | `?timeout=` clamp `[60, 1800]` — magic numbers inline |

### 5b. Demos

| File | Refs |
|---|---|
| `demos/tmp-forge-live.html` | line 1925 (`max_tokens:1800`), 1936, 1953, 1990, 2055 (`TMP_DEFAULT_TIMEOUT=600`), 2095 |
| `demos/tmp-combat-live.html` | 2250 (`max_tokens:900`), 2284, 2365, 2387 |
| `demos/tmp-evolve-live.html` | 1556 (`max_tokens:1400`), 1590, 1601, 1618, 1627 |

`max_tokens` differs per demo (forge:1800, evolve:1400, combat:900) —
intentional, but undocumented and inline.

### 5c. Drift risk

`relay.py:152` falls back to `'claude-haiku-4-5'` if `DEFAULT_MODEL` is
unset, but `DEFAULT_MODEL` defaults to `'claude-haiku-4-5'`, so the
fallback is dead code today. If someone sets `TMP_RELAY_MODEL=""` they
get the body-supplied model — surprising behavior.

**Resolution:** Phase 5 settings module consolidates these into one
place; Phase 6 `providers.js` consolidates the demo side.

---

## 6. localStorage key sprawl

There are at least **7 distinct localStorage keys** scattered across
demos, with non-obvious overlap and sub-cases. Documented inconsistently.

| Key | Used by | Purpose |
|---|---|---|
| `tmp_provider` | all 3 demos | Selected provider |
| `tmp_or_key` | forge, combat, evolve (under OpenRouter / OR Free) | OpenRouter API key |
| `tmp_or_model` | all 3 demos | OpenRouter model selection |
| `tmp_evolve_key` | **evolve only** (under Anthropic provider) | Evolve's own Anthropic key |
| `tmp_combat_key` | **combat only** (similar pattern, line 1332) | Combat's own Anthropic key |
| `tmp_ollama_model` | all 3 demos | Ollama model name |
| `tmp_evolve_source` | combat → evolve handoff | Exported exercise transcript |
| `tmp_evolve_export` | evolve → combat handoff | Refined agent state |

**Inconsistencies:**
- Each demo independently decides whether to use the shared `tmp_or_key`
  or its own `tmp_evolve_key` / `tmp_combat_key`. Evolve's logic at
  line 1540–1541 explicitly removes one when the other is in use —
  fragile.
- Documentation at `ATTENDEE-SETUP.md:136-138` claims all three demos
  share `tmp_or_key` but evolve also uses `tmp_evolve_key` for its
  Anthropic-direct path.
- Migration line at `tmp-forge-live.html:1312` (mirrored in combat:800
  and evolve:1244) silently rewrites `tmp_provider='local'` →
  `tmp_provider='cc'` for returning users — load-bearing in Session
  47.5a, but invisible.

**Resolution:** Phase 6 `providers.js` is the natural place to define
these as a single object. Worth a one-line per-key comment.

---

## 7. Demo filenames are referenced in 13+ places

Filename rename in Phase 4 (`tmp-{forge,combat,evolve}-live.html` →
`{forge,combat,evolve}.html`) touches:

### 7a. Cross-demo links *inside* HTML (must update)

| File | Line | Currently |
|---|---|---|
| `demos/tmp-evolve-live.html` | 557 | `<a href="tmp-combat-live.html">` |
| `demos/tmp-combat-live.html` | 2598 | `<a href="tmp-evolve-live.html">` (inline string in JS) |

### 7b. Test references (must update)

| File | Lines |
|---|---|
| `test_workshop.py` | 20–25 (6 lines) |
| `test_workshop_e2e.py` | 21–23 (3 lines) |
| `conftest.py` | 9 (docstring example only) |

### 7c. Documentation references (must update)

| File | Count |
|---|---|
| `README.md` | 5 (lines 17–19, 31, 70–72) |
| `WORKSHOP-GUIDE.md` | 3 (lines 9, 11, 13) |
| `ATTENDEE-SETUP.md` | 3 (lines 79, 85, 105) |
| `OLLAMA-SETUP.md` | 1 (line 101) |
| `labs/LAB-3-EVOLVE.md` | 2 (lines 31, 71) |

Total: ~17 string replacements. Mechanical.

---

## 8. Hardcoded external URLs

Demos send `HTTP-Referer` / `X-Title` headers identifying themselves to
OpenRouter as `https://github.com/The-Manhattan-Project`.

| File | Lines |
|---|---|
| `demos/tmp-forge-live.html` | 1933, 2092 |
| `demos/tmp-combat-live.html` | 2375 |
| `demos/tmp-evolve-live.html` | 1613 |

This URL is not the actual upstream repo (which is
`Qweary/The-Manhattan-Project` per `README.md:54`). Worth a one-line fix
when we touch `providers.js` in Phase 6 — but flag for the upstream
developer; may be intentional shorthand.

The OpenRouter and Anthropic API endpoints themselves (`api.anthropic.com`,
`openrouter.ai/api/v1/chat/completions`) are duplicated 6× — Phase 6
consolidates them in `providers.js`.

---

## 9. `relay.py` magic constants & assumptions worth code-review attention (Phase 5a)

These are all *correct* today, but they encode assumptions that should
be reviewed before the module split:

| Line | Concern |
|---|---|
| 46 | 600s timeout default — based on the FERMI phase observation; what about non-FERMI/non-claude models? |
| 53 | 4 MB stream-json line buffer — defended in comment, but worth confirming against current Claude Code CLI behavior |
| 100–119 | `--tools ""`, `--disable-slash-commands`, `--setting-sources ""` — comments claim 30k → 3k token reduction; worth verifying this is still accurate after recent CLI updates |
| 119 | `--system-prompt` override — what does Claude Code do today if this is empty? |
| 134 | Per-call timeout clamp `[60, 1800]` magic numbers — should be settings constants |
| 287 | `STALL_WARN_SEC = 30` defined inside function (immutable each call) — minor |
| 285, 293 | `asyncio.get_event_loop()` is deprecated in 3.12+ — should be `asyncio.get_running_loop()` |
| 332–349 | `is_error` recovery: prefers streamed content over late error frame. Comment explains why; worth documenting as a tested invariant |
| 305–362 | `pump()` is 60+ lines, nested; ripe for the structural split |
| 384–401 | `finally` block double-cancels stderr_task and stall_task — the cancellation/await dance has a subtle race if either has already completed |
| 406–412 | Post-stream exit-code check is gated by both `not completed` and `not timed_out` — fine but easy to misread |
| 426 | Bind `127.0.0.1` is hardcoded in `main()` — Phase 5/8 should make this configurable for `--bind` flag (with the warning banner you specced) |

---

## 10. Cross-platform pain points (visible today, addressed in Phase 8)

These don't appear as "broken" in current tests but will bite Windows
attendees:

| Concern | Location |
|---|---|
| `python3` vs `python` | All docs say `python3`; Windows usually has `python` |
| `pip install aiohttp` | No pinned version; PEP 668 (externally-managed) breaks this on macOS Homebrew + Debian/Ubuntu |
| `chmod +x run_tests.sh` | Not documented; new clones may not have execute bit |
| `claude` CLI on Windows | Lives at `claude.cmd` (npm shim) vs `claude` (Unix) — `shutil.which('claude')` handles this on Python 3.12+, worth confirming |
| `lsof -i :3001` (CC SETUP:108) | Linux/macOS only; Windows uses `netstat -ano` |
| asyncio subprocess on Windows | `ProactorEventLoop` is the default in 3.8+, but `--no-session-persistence` interaction with Windows pipes deserves a code-review note |

---

## 11. `.gitignore` gaps

`docs/.tmp/` (the working-notes location proposed in the plan) is not
yet in `.gitignore`. Same for any dev-only artifacts under `docs/dev/`
that we don't want to commit. Phase 1 / 2 will need to add:

```
docs/.tmp/
docs/dev/.tmp/
```

Current `.gitignore` already covers `__pycache__/`, `*.pyc`,
`.pytest_cache/`, `.venv-e2e/`, `.venv/`, `.vscode/`, `.idea/`, `.DS_Store`.
Missing: `.claude/` is gitignored locally only by absence — we should
decide whether to commit `.claude/settings.json` (yes, per plan) and
`.claude/settings.local.json` (no — user-specific).

---

## Summary

| Category | Count | Phase that fixes |
|---|---|---|
| `ai-village-workshop` references | 18 | 2 |
| `python -m http.server` exposure docs | 9 | 4 |
| `localhost:3001` references | 21 | 4 (eliminates 6 in HTML), 5 (settings) |
| `localhost:11434` references | 9 | 6 (consolidate in `providers.js`) |
| Model + token-budget magic constants | ~20 | 5 (relay), 6 (demos) |
| localStorage keys | 8 distinct | 6 (single object in `providers.js`) |
| Demo filename references | ~17 | 4 (rename) |
| External URL duplication | 8 | 6 |
| Relay code review items | ~12 | 5a (review), 5b (fix in place) |
| Cross-platform gotchas | 6 | 8 (init scripts + docs) |

No bugs found that block Phase 1. Three items deserve flagging for
**Phase 5a code review** before any refactor:

1. `asyncio.get_event_loop()` deprecation (lines 285, 293)
2. `tmp_provider='local'` migration shim (silently load-bearing)
3. `is_error` recovery semantics (correct today; worth documenting as
   tested invariant before someone "simplifies" it)

Ready for Phase 1: layout proposal review and the file-move plan.
