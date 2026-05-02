#!/usr/bin/env python3
"""
test_workshop.py — AI Village Workshop validation suite
Exit 0: all tests pass.  Exit 1: one or more failures.
"""

import ast
import os
import re
import sys
from html.parser import HTMLParser

WORKSHOP    = os.path.dirname(os.path.abspath(__file__))

WEB         = os.path.join(WORKSHOP, 'web')

FORGE       = os.path.join(WEB, 'forge.html')
COMBAT      = os.path.join(WEB, 'combat.html')
EVOLVE      = os.path.join(WEB, 'evolve.html')

RELAY       = os.path.join(WORKSHOP, 'relay.py')
TMP_RELAY_SRC = os.path.join(WORKSHOP, 'src', 'tmp_relay')
README      = os.path.join(WORKSHOP, 'README.md')
LAB1        = os.path.join(WORKSHOP, 'labs', 'LAB-1-FORGE.md')
LAB2        = os.path.join(WORKSHOP, 'labs', 'LAB-2-COMBAT.md')
GUIDE       = os.path.join(WORKSHOP, 'docs', 'attendee', 'workshop-guide.md')
OLLAMA_SETUP = os.path.join(WORKSHOP, 'docs', 'attendee', 'providers', 'ollama.md')
CC_SETUP    = os.path.join(WORKSHOP, 'docs', 'attendee', 'providers', 'claude-code.md')

results = []


def check(name, ok, detail=''):
    results.append((name, ok, detail))
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}] {name}')
    if not ok and detail:
        print(f'         → {detail}')


def read_text(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def read_relay_sources():
    """Concatenate relay.py + every Python file under src/tmp_relay/.
    Lets substring invariant checks survive the Phase 5c module split
    without needing to know which module a constant or string ended up
    in. (Phase 7 will reshape these tests; this is the bridge until then.)"""
    chunks = []
    if os.path.exists(RELAY):
        chunks.append(read_text(RELAY))
    if os.path.isdir(TMP_RELAY_SRC):
        for name in sorted(os.listdir(TMP_RELAY_SRC)):
            if name.endswith('.py'):
                chunks.append(read_text(os.path.join(TMP_RELAY_SRC, name)))
    return '\n'.join(chunks)


# ── 1. relay.py syntax ────────────────────────────────────────────────────────
print('\n── relay.py ──────────────────────────────────────────────────────────')
try:
    src = read_text(RELAY)
    ast.parse(src)
    check('relay.py syntax (ast.parse)', True)
except SyntaxError as e:
    check('relay.py syntax (ast.parse)', False, str(e))
except FileNotFoundError:
    check('relay.py syntax (ast.parse)', False, 'relay.py not found')

# ── 2. HTML parse ─────────────────────────────────────────────────────────────
print('\n── HTML parse ────────────────────────────────────────────────────────')


class StrictParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_error(self, message):
        self.errors.append(message)


for label, path in [
    ('forge', FORGE),
    ('combat', COMBAT),
    ('evolve', EVOLVE),
]:
    try:
        html = read_text(path)
        p = StrictParser()
        p.feed(html)
        check(f'{label} parses without fatal error', len(p.errors) == 0,
              detail='; '.join(p.errors[:3]) if p.errors else '')
    except FileNotFoundError:
        check(f'{label} parses without fatal error', False, f'{path} not found')

# ── 3. Ollama button IDs ──────────────────────────────────────────────────────
print('\n── Ollama button IDs ─────────────────────────────────────────────────')
try:
    forge_html  = read_text(FORGE)
    combat_html = read_text(COMBAT)
    evolve_html = read_text(EVOLVE)
    check('forge:  id="prv-ollama"  present', 'prv-ollama'  in forge_html)
    check('combat: id="cprv-ollama" present', 'cprv-ollama' in combat_html)
    check('evolve: id="eprv-ollama" present', 'eprv-ollama' in evolve_html)
except FileNotFoundError as e:
    check('Ollama button IDs', False, str(e))
    forge_html = combat_html = evolve_html = ''

# ── 4. Ollama API call present ────────────────────────────────────────────────
print('\n── Ollama API call ───────────────────────────────────────────────────')
for label, html in [
    ('forge',  forge_html),
    ('combat', combat_html),
    ('evolve', evolve_html),
]:
    has_call = ('callOllama' in html) or ('11434' in html)
    check(f'{label}: callOllama or 11434 endpoint present', has_call)

# ── 4b. CLAUDE CODE provider rebuild (Session 47.5a) ─────────────────────────
# Lock in the LOCAL → CLAUDE CODE rename across all three demos. Catches a
# regression that would put the demos back into the broken "local relay needs
# Anthropic API key" state.
print('\n── CLAUDE CODE provider (S47.5a) ────────────────────────────────────')
# One-line localStorage migration shim that maps pre-S47.5a saved values
# (tmp_provider='local') to the new 'cc' value, so returning users don't land
# on a broken UI. This is the only reference to 'local' that should remain.
MIGRATION_SHIM_RE = re.compile(
    r"if\s*\(\s*\w*Provider\s*===\s*'local'\s*\)\s*\{[^}]*Provider\s*=\s*'cc'[^}]*\}"
)
# After stripping the migration shim, ANY remaining 'local' provider check is
# a stale reference: `forgeProvider==='local'`, `setForgeProvider('local')`,
# `if(p==='local'){...}`, etc.
PROVIDER_LOCAL_RE = re.compile(
    r"""(?:Provider\s*[!=]==\s*'local'
         |setForgeProvider\('local'\)
         |setCombatProvider\('local'\)
         |setEvolveProvider\('local'\)
         |p\s*===?\s*'local'
         |p\s*[!=]==\s*'local'
        )""",
    re.VERBOSE,
)
for label, html, btn_id in [
    ('forge',  forge_html,  'prv-cc'),
    ('combat', combat_html, 'cprv-cc'),
    ('evolve', evolve_html, 'eprv-cc'),
]:
    check(f'{label}: button id="{btn_id}" present', btn_id in html,
          detail=f'CLAUDE CODE button missing — S47.5a rename incomplete')
    check(f'{label}: callClaudeCode function present', 'callClaudeCode' in html,
          detail='callClaudeCode function missing — S47.5a rename incomplete')
    check(f'{label}: no leftover prv-local id', 'prv-local' not in html,
          detail='Old LOCAL button id remains — S47.5a rename incomplete')
    check(f'{label}: no leftover callLocal function', 'callLocal' not in html,
          detail='Old callLocal function remains — S47.5a rename incomplete')
    # Strip the migration shim before searching for stale provider checks —
    # the shim is allowed (and required); any other 'local' provider check is
    # a regression.
    has_shim = MIGRATION_SHIM_RE.search(html) is not None
    stripped = MIGRATION_SHIM_RE.sub('', html)
    stale = PROVIDER_LOCAL_RE.search(stripped)
    check(f'{label}: no leftover provider==\'local\' check',
          stale is None,
          detail=f'Old provider check remains: {stale.group(0) if stale else ""}')
    check(f'{label}: localStorage migration shim from "local" → "cc" present',
          has_shim,
          detail='Migration line missing; returning users with saved tmp_provider="local" will land on a broken UI')

# ── 5. No ../demos/ in workshop README ───────────────────────────────────────
print('\n── README integrity ──────────────────────────────────────────────────')
try:
    readme = read_text(README)
    check('README: no ../demos/ broken reference', '../demos/' not in readme,
          detail='Found "../demos/" — this link breaks when the workshop folder is extracted')
except FileNotFoundError:
    check('README: no ../demos/ broken reference', False, 'README.md not found')

# ── 6. OPENROUTER not in LAB-1 / LAB-2 headers ───────────────────────────────
print('\n── Lab header cleanliness ────────────────────────────────────────────')
for label, path in [('LAB-1', LAB1), ('LAB-2', LAB2)]:
    try:
        lines = read_text(path).splitlines()
        bad = [l.strip() for l in lines if l.startswith('#') and 'OPENROUTER' in l.upper()]
        check(f'{label}: no "OPENROUTER" in section headers', len(bad) == 0,
              detail=f'Found in headers: {bad}' if bad else '')
    except FileNotFoundError:
        check(f'{label}: no "OPENROUTER" in section headers', False, f'{path} not found')

# ── 7. WORKSHOP-GUIDE opener / closer ─────────────────────────────────────────
print('\n── WORKSHOP-GUIDE.md ─────────────────────────────────────────────────')
try:
    guide = read_text(GUIDE)
    check('WORKSHOP-GUIDE: starts with "SYSTEM CONTEXT"', guide.lstrip().startswith('SYSTEM CONTEXT'))
    check('WORKSHOP-GUIDE: ends with "[attendee types here]"', '[attendee types here]' in guide)
except FileNotFoundError:
    check('WORKSHOP-GUIDE: starts with "SYSTEM CONTEXT"', False, 'WORKSHOP-GUIDE.md not found')
    check('WORKSHOP-GUIDE: ends with "[attendee types here]"', False, 'WORKSHOP-GUIDE.md not found')

# ── 8. OLLAMA-SETUP.md ────────────────────────────────────────────────────────
print('\n── OLLAMA-SETUP.md ───────────────────────────────────────────────────')
try:
    setup = read_text(OLLAMA_SETUP)
    check('OLLAMA-SETUP.md exists', True)
    check('OLLAMA-SETUP.md: contains "ollama serve"', 'ollama serve' in setup)
    check('OLLAMA-SETUP.md: contains "ollama pull"',  'ollama pull'  in setup)
except FileNotFoundError:
    check('OLLAMA-SETUP.md exists', False, f'{OLLAMA_SETUP} not found')
    check('OLLAMA-SETUP.md: contains "ollama serve"', False, 'file missing')
    check('OLLAMA-SETUP.md: contains "ollama pull"',  False, 'file missing')

# ── 8b. CLAUDE-CODE-SETUP.md (Session 47.5a) ─────────────────────────────────
print('\n── CLAUDE-CODE-SETUP.md ──────────────────────────────────────────────')
try:
    cc_setup = read_text(CC_SETUP)
    check('CLAUDE-CODE-SETUP.md exists', True)
    check('CLAUDE-CODE-SETUP.md: contains "claude --version"',
          'claude --version' in cc_setup)
    check('CLAUDE-CODE-SETUP.md: contains "[ CLAUDE CODE ]"',
          '[ CLAUDE CODE ]' in cc_setup)
    check('CLAUDE-CODE-SETUP.md: no stale ANTHROPIC_API_KEY export',
          'export ANTHROPIC_API_KEY' not in cc_setup,
          detail='Old API-key-paste setup step still present — should be replaced with Claude Code install verification')
except FileNotFoundError:
    check('CLAUDE-CODE-SETUP.md exists', False, f'{CC_SETUP} not found')
check('No stale RELAY-SETUP.md left at workshop root',
      not os.path.exists(os.path.join(WORKSHOP, 'RELAY-SETUP.md')),
      detail='RELAY-SETUP.md should have been renamed to CLAUDE-CODE-SETUP.md')

# ── 8c. CLAUDE CODE SSE streaming (Session 47.5c) ────────────────────────────
# Locks in the streaming polish — relay must expose the SSE branch, every demo
# must offer `callClaudeCode(sys, user, onDelta)` and a `tok-count` indicator
# in the status bar. Catches a regression that would put the demos back into
# the broken "5 minutes of unmoving UI" state on slower hardware.
print('\n── CLAUDE CODE SSE streaming (S47.5c) ───────────────────────────────')
try:
    relay_src = read_relay_sources()
    check('relay.py: text/event-stream SSE branch present',
          'text/event-stream' in relay_src,
          detail='SSE header gate missing — long-output phases will hit the 300s timeout silently')
    check('relay.py: stream-json output format wired',
          '--output-format' in relay_src and 'stream-json' in relay_src
          and '--include-partial-messages' in relay_src,
          detail='claude CLI streaming flags missing from relay subprocess args')
except FileNotFoundError:
    check('relay.py: text/event-stream SSE branch present', False, 'relay.py not found')

CALLCC_ONDELTA_RE = re.compile(
    r'(?:async\s+)?function\s+callClaudeCode\s*\(\s*sys\s*,\s*user\s*,\s*onDelta\b'
)
for label, html in [('forge', forge_html), ('combat', combat_html), ('evolve', evolve_html)]:
    check(f'{label}: callClaudeCode accepts onDelta callback',
          CALLCC_ONDELTA_RE.search(html) is not None,
          detail='callClaudeCode signature should accept onDelta — gates the SSE path')
    check(f'{label}: tok-count ticker element present',
          'id="tok-count"' in html,
          detail='Header status bar should show tokens: N — visible heartbeat that the model is producing output')

# ── 8d. S47.5d — output budgeting + graceful recovery ────────────────────────
# Locks in the per-phase brevity hints + the recovery banner (continue/retry/
# skip/demo/dismiss). Without these, a single timed-out phase reverts the
# demo to "5 minutes of unmoving UI" or kills the whole forge run.
print('\n── S47.5d output budgeting + recovery (S47.5d) ──────────────────────')
for label, html in [('forge', forge_html), ('combat', combat_html), ('evolve', evolve_html)]:
    # Per-phase output budgets — caps Haiku's runaway output on long phases.
    check(f'{label}: budget(user, tokens) helper defined',
          'function budget(' in html,
          detail='Per-phase brevity helper missing — long phases will run unbounded')
    check(f'{label}: at least one budget() call site present',
          'budget(' in html and html.count('budget(') >= 2,
          detail='budget() helper must be wired into demo phase calls')
    # Recovery banner — phase-level continue / retry / skip / demo / dismiss.
    check(f'{label}: callWithRecovery wrapper present',
          'callWithRecovery' in html,
          detail='Per-phase recovery wrapper missing — single phase failures kill the whole run')
    check(f'{label}: phase-recovery banner CSS present',
          '.phase-recovery{' in html.replace(' ', ''),
          detail='Recovery banner needs CSS — buttons would render unstyled')
    # All 5 button labels must be present in the source so attendees see the
    # full menu on failure.
    for btn in ['Continue waiting', 'Retry phase', 'Skip phase', 'Switch to DEMO', 'Abort run']:
        check(f'{label}: recovery banner has "{btn}" button',
              btn in html,
              detail=f'Recovery banner missing "{btn}" — operator menu incomplete')
    # SSE warning hook — relay's stalled-stream signal surfaces in the demo.
    check(f'{label}: payload.warning handled in SSE parser',
          'payload.warning' in html,
          detail='SSE parser must handle the relay\'s stall warning event so attendees see "stalled — no token in N s" instead of silence')
    # ?timeout= query param threading
    check(f'{label}: ?timeout= URL override threaded through callClaudeCode',
          '?timeout=' in html,
          detail='callClaudeCode must thread opts.timeoutSec to the relay URL — Continue waiting is otherwise a no-op')

# Relay-side S47.5d checks
try:
    relay_src = read_relay_sources()
    check('relay.py: ?timeout= query param honored',
          'rel_url.query.get(\'timeout\')' in relay_src or 'rel_url.query.get("timeout")' in relay_src,
          detail='Relay must honor ?timeout=N to give Continue waiting a working budget bump')
    check('relay.py: stall watchdog (sends warning event)',
          'stall_watcher' in relay_src or 'stall_warned' in relay_src,
          detail='Relay must emit a warning event when no text_delta arrives for >30s — without it attendees see silent panes during long thinking pauses')
    check('relay.py: SUBPROC_LIMIT bumped (4MB)',
          '4 * 1024 * 1024' in relay_src or '4*1024*1024' in relay_src,
          detail='Subprocess line buffer must be 4MB — 64KB default crashes on stream-json snapshot lines')
    check('relay.py: user prompt over stdin (not -p arg)',
          'communicate(input=user' in relay_src and 'proc.stdin.write' in relay_src,
          detail='User prompt must flow over stdin — accumulated context exceeds ARG_MAX as command-line arg by Phase 3+')
except FileNotFoundError:
    check('relay.py: ?timeout= query param honored', False, 'relay.py not found')

# ── 8e. S48 — Playwright e2e infrastructure ──────────────────────────────────
# The e2e suite isn't run from test_workshop.py (different runner, browser
# dependency). But we lock in that the infrastructure files exist so a
# casual cleanup doesn't accidentally delete them.
print('\n── S48 e2e infrastructure (S48) ──────────────────────────────────────')
E2E_FILES = [
    ('conftest.py',           'Pytest fixtures: http_server, demo_url, safe_page'),
    ('test_workshop_e2e.py',  'Playwright smoke + toggle + tooltip tests'),
    ('run_tests.sh',          'Unified runner for static + e2e suites'),
    ('docs/dev/testing.md',   'How-to-run docs for both suites + harness'),
]
for fname, what in E2E_FILES:
    path = os.path.join(WORKSHOP, fname)
    check(f'{fname} present ({what})',
          os.path.exists(path),
          detail=f'{path} missing — S48 infrastructure incomplete')

# ── 9. S41-S44 polish markers ─────────────────────────────────────────────────
# Verify the IDs, classes, and handlers added during the Demo Polish Series
# (Sessions 41–44) are present in all three demo files. These checks fail loudly
# if a future edit accidentally removes a polish deliverable.
print('\n── S41-S44 polish markers ────────────────────────────────────────────')

POLISH_COMMON = [
    ('body class="pmode" default ON',  '<body class="pmode">'),
    ('#error-recovery-banner present', 'id="error-recovery-banner"'),
    ('Ctrl+P pmode toggle handler',    "ctrlKey"),
    ('Space bar step-gate handler',    "'Space'"),
    ('responsive @media 768px block',  '@media (max-width:768px)'),
    ('responsive @media 1024px block', '@media (max-width:1024px)'),
    ('pre-flight no-API-key confirm',  'No API key configured'),
]
for label, html in [('forge', forge_html), ('combat', combat_html), ('evolve', evolve_html)]:
    for name, marker in POLISH_COMMON:
        check(f'{label}: {name}', marker in html,
              detail=f'marker missing: {marker!r}')

# Forge-specific
check('forge: #demo-hdr-badge in header',
      'id="demo-hdr-badge"' in forge_html)
check('forge: .ibtn position:sticky',
      'position:sticky' in forge_html and '.ibtn' in forge_html)
check('forge: ▶ RUN DEMO label toggle',
      '▶ RUN DEMO' in forge_html and '⚛ INITIATE FISSION' in forge_html)

# Combat-specific
check('combat: [ CHECK IMPORT ] button',
      '[ CHECK IMPORT ]' in combat_html)
check('combat: .btm-config row class',
      'class="btm-row btm-config"' in combat_html)
check('combat: .btm-actions row class',
      'class="btm-row btm-actions"' in combat_html)
check('combat: storage event listener for tmp_evolve_export',
      "addEventListener('storage'" in combat_html and 'tmp_evolve_export' in combat_html)
check('combat: checkEvolveExport is named (not IIFE)',
      'function checkEvolveExport()' in combat_html)
check('combat: pulse-border keyframes (banner pulse)',
      '@keyframes pulse-border' in combat_html)
check('combat: evolved-agent name normalization',
      'normEvolved' in combat_html)

# Evolve-specific
check('evolve: .btm-config row class',
      'class="btm-row btm-config"' in evolve_html)
check('evolve: .btm-actions row class',
      'class="btm-row btm-actions"' in evolve_html)
check('evolve: combat-link green affordance after export',
      "var(--grn)" in evolve_html and ".combat-link" in evolve_html)
check('evolve: exportToCombat null guard',
      '!refinedPrompt||!weakestAgentName' in evolve_html
      or '!refinedPrompt || !weakestAgentName' in evolve_html)

# Phase bar tooltips — minimum cell counts per file
import re
forge_ph_titles  = len(re.findall(r'<div class="ph"[^>]*\btitle=', forge_html))
combat_ph_titles = len(re.findall(r'<div class="phase"[^>]*\btitle=', combat_html))
evolve_ph_titles = len(re.findall(r'<div class="eph"[^>]*\btitle=', evolve_html))
check('forge: phase tooltips ≥ 8',  forge_ph_titles >= 8,
      detail=f'found {forge_ph_titles}')
check('combat: phase tooltips ≥ 14', combat_ph_titles >= 14,
      detail=f'found {combat_ph_titles}')
check('evolve: phase tooltips ≥ 6',  evolve_ph_titles >= 6,
      detail=f'found {evolve_ph_titles}')

# Contrast uplift — --gr variable bumped per Spectrum audit
check('forge: --gr bumped to #8080aa',  '--gr:#8080aa'  in forge_html.replace(' ', ''))
check('combat: --gr bumped to #7878a0', '--gr:#7878a0' in combat_html.replace(' ', ''))
check('evolve: --gr bumped to #7878a0', '--gr:#7878a0' in evolve_html.replace(' ', ''))

# ── 9b. Session 46 audit lockdown ─────────────────────────────────────────────
# Static checks for the P0 findings closed in Session 46 (T2 specialist audit:
# Lens / Spectrum / Prism). Prevents regression on stage-breaker fixes.
print('\n── S46 audit lockdown ────────────────────────────────────────────────')

# P0-1 — workshop docs reference live button labels, not the old dead ones
try:
    lab1_txt  = read_text(LAB1)
    lab2_txt  = read_text(LAB2)
    guide_txt = read_text(GUIDE)
except FileNotFoundError as e:
    lab1_txt = lab2_txt = guide_txt = ''
    check('S46 P0-1: workshop docs readable', False, str(e))
else:
    check('S46 P0-1: LAB-1 has no "LAUNCH FORGE"',
          'LAUNCH FORGE' not in lab1_txt,
          detail='Lab still tells attendees to click a button that does not exist')
    check('S46 P0-1: LAB-1 references INITIATE FISSION',
          'INITIATE FISSION' in lab1_txt)
    check('S46 P0-1: LAB-2 has no "LAUNCH EXERCISE"',
          'LAUNCH EXERCISE' not in lab2_txt,
          detail='Lab still tells attendees to click a button that does not exist')
    check('S46 P0-1: LAB-2 references SETUP NETWORK',
          'SETUP NETWORK' in lab2_txt)
    check('S46 P0-1: LAB-2 references ENGAGE',
          'ENGAGE' in lab2_txt)
    check('S46 P0-1: LAB-2 has no "EXPORT TO EVOLVE DEMO"',
          'EXPORT TO EVOLVE DEMO' not in lab2_txt,
          detail='Lab references a button that is actually a link labeled OPEN IN EVOLVE DEMO')
    check('S46 P0-1: WORKSHOP-GUIDE has no "tmp_combat_export"',
          'tmp_combat_export' not in guide_txt,
          detail='Guide references the wrong localStorage key (real key is tmp_evolve_source)')
    check('S46 P0-1: WORKSHOP-GUIDE references tmp_evolve_source',
          'tmp_evolve_source' in guide_txt)
    check('S46 P0-1: WORKSHOP-GUIDE has no "LAUNCH FORGE"',
          'LAUNCH FORGE' not in guide_txt)

# P0-2 — evolve AGENT_PROMPTS rename complete (no more vestigial _RED suffix)
check('S46 P0-2: evolve has no AGENT_PROMPTS_RED (rename complete)',
      'AGENT_PROMPTS_RED' not in evolve_html,
      detail='Vestigial _RED suffix would mislead future readers into thinking these are red-team prompts')
check('S46 P0-2: evolve still has AGENT_PROMPTS',
      'AGENT_PROMPTS' in evolve_html)

# S47 — evolve BLUE preset is now enabled with distinct blue-team-internal content
# (S46 disabled it pending content; S47 authored de-arbiter-blue / de-sculptor-blue / de-rerun-blue).
check('S47 P0-3: evolve BLUE preset button enabled',
      'id="preset-blue-btn"' in evolve_html
      and re.search(r'id="preset-blue-btn"[^>]*\bdisabled\b', evolve_html) is None,
      detail='BLUE preset must be enabled — S47 authored distinct blue-team-internal content; S46 disabled state should be lifted')
check('S47: evolve has de-arbiter-blue script block',
      'id="de-arbiter-blue"' in evolve_html,
      detail='BLUE preset selects this scorecard via de-arbiter-${evolvePreset}; missing block falls back to RED scorecard')
check('S47: evolve has de-sculptor-blue script block',
      'id="de-sculptor-blue"' in evolve_html,
      detail='BLUE preset SCULPTOR phase requires de-sculptor-blue; missing falls back to RED')
check('S47: evolve has de-rerun-blue script block',
      'id="de-rerun-blue"' in evolve_html,
      detail='BLUE preset RERUN phase requires de-rerun-blue; missing falls back to RED')
check('S47: evolve BLUE preset weakest agent differs from RED preset',
      'TELEMETRY-ANALYST' in evolve_html.split('id="de-arbiter-blue"')[1].split('</script>')[0]
      if 'id="de-arbiter-blue"' in evolve_html else False,
      detail='BLUE preset should refine TELEMETRY-ANALYST (Linux host coverage); RED preset refines DETECTION-ENGINEER (FTP detection) — different refinement targets')

# S47 — evolve PHANTOM-specific arbiter/sculptor/rerun for CHAIN mode imports
check('S47: evolve has de-arbiter-phantom script block',
      'id="de-arbiter-phantom"' in evolve_html,
      detail='CHAIN mode imports from PHANTOM FEED route to de-arbiter-phantom via scriptKeyFor()')
check('S47: evolve has de-sculptor-phantom script block',
      'id="de-sculptor-phantom"' in evolve_html)
check('S47: evolve has de-rerun-phantom script block',
      'id="de-rerun-phantom"' in evolve_html)
check('S47: evolve scriptKeyFor() helper routes PHANTOM imports',
      'function scriptKeyFor' in evolve_html
      and 'PHANTOM' in evolve_html
      and 'de-${role}-phantom' in evolve_html,
      detail='scriptKeyFor() helper must route CHAIN+PHANTOM exercises to the phantom triplet; otherwise CHAIN mode silently plays IRONCLAD content for a PHANTOM import')

# S47 — combat cx-harden-evolved alternate verdict for evolved-agent runs
check('S47: combat has cx-harden-evolved alternate hardening report',
      'id="cx-harden-evolved"' in combat_html,
      detail='Without cx-harden-evolved, the cx-harden hardcoded "RED WIN 8/7" plays regardless of evolved-agent presence')
check('S47: combat cx-harden-evolved produces BLUE WIN verdict',
      'id="cx-harden-evolved"' in combat_html
      and 'VERDICT: BLUE WIN' in combat_html.split('id="cx-harden-evolved"')[1].split('</script>')[0],
      detail='cx-harden-evolved must reflect successful blue-side improvement (BLUE WIN), distinguishing evolved from un-evolved runs')
check('S47: combat CDEMO map exposes HARDEN_EVOLVED key',
      'HARDEN_EVOLVED' in combat_html,
      detail='engage() routes to HARDEN_EVOLVED when evolvedAgent is set')
check('S47: combat engage() routes harden by evolvedAgent state',
      "evolvedAgent?'HARDEN_EVOLVED':'HARDEN'" in combat_html.replace(' ', '')
      or "evolvedAgent ? 'HARDEN_EVOLVED' : 'HARDEN'" in combat_html,
      detail='engage() must select HARDEN_EVOLVED when an evolved agent has been imported')

# S47 — Forge content authenticity: per-domain Oppenheimer headings, varied Geiger checklists
check('S47: forge red Oppenheimer uses SWARM ARCHITECTURE: heading',
      '## SWARM ARCHITECTURE: RED TEAM OPERATIONS' in forge_html,
      detail='S46 flagged identical "## Swarm Architecture Document — DOMAIN" headings across all swarms; S47 differentiates per SYS.OPPENHEIMER spec')
check('S47: forge blue Oppenheimer uses SWARM ARCHITECTURE: heading',
      '## SWARM ARCHITECTURE: BLUE TEAM DEFENSE OPERATIONS' in forge_html)
check('S47: forge infra Oppenheimer uses SWARM ARCHITECTURE: heading',
      '## SWARM ARCHITECTURE: INFRASTRUCTURE ASSESSMENT' in forge_html)
check('S47: forge Oppenheimer blocks all carry Mission Parameters section',
      forge_html.count('### Mission Parameters') >= 3,
      detail='Per SYS.OPPENHEIMER spec; replaces uniform "### Domain Workflow Analysis" template')
check('S47: forge Geiger checklists differentiate per domain (audit-section names vary)',
      '### Authorization-First Audit' in forge_html
      and '### Detection Coverage Audit' in forge_html
      and '### Pipeline Integrity Review' in forge_html,
      detail='S46 flagged near-template-identical Geiger reports; S47 leads each report with a domain-load-bearing audit section name')

# P0-4 — combat .sa SIEM-source column has pmode override
check('S46 P0-4: combat body.pmode .sa rule present',
      'body.pmode.sa{' in combat_html.replace(' ', ''))

# P0-5 — tier-note class replaces inline 8px font-size on provider notices.
# Each provider-notice element must (a) carry class="tier-note" and (b) have no
# inline font-size — inline styles win over class selectors and bypass pmode.
TIER_NOTE_IDS = {
    'forge':  ['orfree-notice', 'ollama-notice'],
    'combat': ['cfree-note',    'collama-note'],
    'evolve': ['efree-note',    'eollama-note'],
}
for label, html in [('forge', forge_html), ('combat', combat_html), ('evolve', evolve_html)]:
    check(f'S46 P0-5: {label} has .tier-note CSS class with pmode override',
          '.tier-note{' in html.replace(' ', '')
          and 'body.pmode.tier-note{' in html.replace(' ', ''))
    for nid in TIER_NOTE_IDS[label]:
        m = re.search(r'id="' + re.escape(nid) + r'"[^>]*', html)
        elem = m.group(0) if m else ''
        check(f'S46 P0-5: {label} #{nid} carries class="tier-note"',
              'class="tier-note"' in elem,
              detail=f'Element source: {elem[:120]}')
        check(f'S46 P0-5: {label} #{nid} has no inline font-size',
              'font-size' not in elem,
              detail=f'Inline font-size on #{nid} bypasses pmode override: {elem[:120]}')

# P0-6 — evolve .agent-name has pmode size override
check('S46 P0-6: evolve body.pmode .agent-name rule present',
      'body.pmode.agent-name{' in evolve_html.replace(' ', ''))

# P0-7 — evolve .diff-hdr has pmode size override
check('S46 P0-7: evolve body.pmode .diff-hdr rule present',
      'body.pmode.diff-hdr{' in evolve_html.replace(' ', ''))

# P0-8 — combat / evolve pmode .ts color is NOT forge amber #b07800
ts_pmode_re = re.compile(r'body\.pmode\s+\.ts\s*\{[^}]*color\s*:\s*([#0-9a-fA-F]+)')
for label, html in [('combat', combat_html), ('evolve', evolve_html)]:
    m = ts_pmode_re.search(html)
    color = m.group(1).lower() if m else ''
    check(f'S46 P0-8: {label} body.pmode .ts color is not forge amber',
          color != '#b07800',
          detail=f'Found color={color}; this leaks forge palette into {label}')

# P0-9 — forge :root defines all CSS vars referenced (regression check that
# would have caught the var(--red) / var(--amb) bug shipped in S42).
forge_root_match = re.search(r':root\s*\{([^}]+)\}', forge_html)
forge_root_vars = set()
if forge_root_match:
    for vname in re.findall(r'--([a-zA-Z0-9_-]+)\s*:', forge_root_match.group(1)):
        forge_root_vars.add(vname)
forge_used_vars = set(re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', forge_html))
# Filter out vars defined in dependent scopes (none expected in forge); any
# used var that is not in :root is a regression.
forge_undef = sorted(forge_used_vars - forge_root_vars)
check('S46 P0-9: every var(--X) referenced in forge is defined in :root',
      len(forge_undef) == 0,
      detail=f'Undefined CSS vars used: {forge_undef}')

# P0-11 — combat tmp_evolve_source export uses activeStages (scenario-aware)
check('S46 P0-11: combat tmp_evolve_source export uses activeStages',
      'activeStages.map((st,idx)=>{' in combat_html.replace(' ', ''),
      detail='Hardcoded stages.map would mislabel PHANTOM FEED as IRONCLAD on export')

# ── 9.5. DEMO MODE content placeholder regression (Session 47) ───────────────
# Scans every <script type="text/plain" id="..."> block in the three demos for
# placeholder tokens that indicate authoring left a stub in place. Runs only on
# the workshop copies (sync-parity check below catches any drift in demos/).
print('\n── DEMO content placeholder regression (S47) ────────────────────────')

# Tokens forbidden inside DEMO MODE script blocks. Each entry is (regex, label).
# Patterns are case-insensitive. Anchored to substrings that should never appear
# in authentic agent output — TODO/FIXME/lorem/example.com/etc. are stubs by
# convention; "[Live mode:" was the literal placeholder string the LIVE preset
# path emitted before S47.
PLACEHOLDER_PATTERNS = [
    (r'\bTODO\b',                      'TODO marker'),
    (r'\bFIXME\b',                     'FIXME marker'),
    (r'\blorem\s+ipsum\b',             'lorem ipsum filler'),
    (r'example\.com',                  'example.com placeholder domain'),
    (r'X{6,}',                         'XXXXX redaction placeholder'),
    (r'<replace[\s_-]*this>',          '<replace this> token'),
    (r'\[Live\s+mode:',                '[Live mode: ...] literal placeholder'),
    (r'content\s+would\s+be\s+generated', '"content would be generated" stub'),
    (r'\{\{[a-zA-Z_]+\}\}',            '{{template_token}} stub'),
    (r'\bplaceholder\b\s+(?:text|content|here)', 'placeholder text/content/here'),
]

# Match every <script type="text/plain" id="..."> ... </script> block.
SCRIPT_BLOCK_RE = re.compile(
    r'<script\s+type="text/plain"\s+id="([^"]+)"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)

for label, path in [
    ('forge',  FORGE),
    ('combat', COMBAT),
    ('evolve', EVOLVE),
]:
    try:
        html = read_text(path)
        violations = []
        for match in SCRIPT_BLOCK_RE.finditer(html):
            block_id = match.group(1)
            block_body = match.group(2)
            for pattern, pat_label in PLACEHOLDER_PATTERNS:
                hits = list(re.finditer(pattern, block_body, re.IGNORECASE))
                if hits:
                    sample = hits[0].group(0)
                    violations.append(f'#{block_id}: {pat_label} ("{sample}")')
        check(f'{label}: DEMO script blocks free of placeholder tokens',
              len(violations) == 0,
              detail='; '.join(violations[:5]) if violations else '')
    except FileNotFoundError:
        check(f'{label}: DEMO script blocks free of placeholder tokens', False,
              f'{path} not found')

# Spot-check that the LIVE-mode preset code path no longer emits the literal
# "[Live mode: ... content would be generated here]" string in the JS source.
# This catches re-introduction outside the script-block scan.
EVOLVE_LIVE_PLACEHOLDER = '[Live mode: ${st.rLabel} content would be generated here]'
try:
    evolve_src = read_text(EVOLVE)
    check('evolve: LIVE preset path no longer emits literal placeholder',
          EVOLVE_LIVE_PLACEHOLDER not in evolve_src,
          detail='Literal "[Live mode: ${st.rLabel} content would be generated here]" still present in JS')
except FileNotFoundError:
    check('evolve: LIVE preset path no longer emits literal placeholder', False, 'evolve workshop copy not found')

# Section 10 (hash parity between demos/ and ai-village-workshop/demos/) was
# removed in the Phase 2 path-normalization pass. The two copies were
# collapsed into one when the workshop was promoted to repo root, so the
# parity check had nothing to compare. Phase 3 introduces snapshot tests
# that lock content properly; those replace what this test was meant to do.

# ── Summary ───────────────────────────────────────────────────────────────────
print()
print('─' * 60)
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
total  = len(results)

if failed == 0:
    print(f'  ALL {total} TESTS PASSED')
    sys.exit(0)
else:
    print(f'  {passed}/{total} passed  |  {failed} FAILED')
    print()
    print('  Failed tests:')
    for name, ok, detail in results:
        if not ok:
            print(f'    ✗ {name}')
            if detail:
                print(f'      {detail}')
    sys.exit(1)
