#!/usr/bin/env python3
"""
test_workshop.py — AI Village Workshop validation suite
Exit 0: all tests pass.  Exit 1: one or more failures.
"""

import ast
import hashlib
import os
import sys
from html.parser import HTMLParser

WORKSHOP    = os.path.dirname(os.path.abspath(__file__))
ROOT        = os.path.dirname(WORKSHOP)

DEMOS_SRC   = os.path.join(ROOT, 'demos')
DEMOS_WS    = os.path.join(WORKSHOP, 'demos')

FORGE_SRC   = os.path.join(DEMOS_SRC, 'tmp-forge-live.html')
COMBAT_SRC  = os.path.join(DEMOS_SRC, 'tmp-combat-live.html')
EVOLVE_SRC  = os.path.join(DEMOS_SRC, 'tmp-evolve-live.html')
FORGE_WS    = os.path.join(DEMOS_WS, 'tmp-forge-live.html')
COMBAT_WS   = os.path.join(DEMOS_WS, 'tmp-combat-live.html')
EVOLVE_WS   = os.path.join(DEMOS_WS, 'tmp-evolve-live.html')

RELAY       = os.path.join(WORKSHOP, 'relay.py')
README      = os.path.join(WORKSHOP, 'README.md')
LAB1        = os.path.join(WORKSHOP, 'labs', 'LAB-1-FORGE.md')
LAB2        = os.path.join(WORKSHOP, 'labs', 'LAB-2-COMBAT.md')
GUIDE       = os.path.join(WORKSHOP, 'WORKSHOP-GUIDE.md')
OLLAMA_SETUP = os.path.join(WORKSHOP, 'OLLAMA-SETUP.md')

results = []


def check(name, ok, detail=''):
    results.append((name, ok, detail))
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}] {name}')
    if not ok and detail:
        print(f'         → {detail}')


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read_text(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


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
    ('forge (workshop)', FORGE_WS),
    ('combat (workshop)', COMBAT_WS),
    ('evolve (workshop)', EVOLVE_WS),
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
    forge_html  = read_text(FORGE_WS)
    combat_html = read_text(COMBAT_WS)
    evolve_html = read_text(EVOLVE_WS)
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

# ── 9. demos/ ↔ workshop/demos/ hash parity ──────────────────────────────────
print('\n── File hash parity (demos/ == ai-village-workshop/demos/) ──────────')
for name, src, ws in [
    ('forge',  FORGE_SRC,  FORGE_WS),
    ('combat', COMBAT_SRC, COMBAT_WS),
    ('evolve', EVOLVE_SRC, EVOLVE_WS),
]:
    try:
        ok = sha256(src) == sha256(ws)
        check(f'{name}: hashes match', ok,
              detail='Files differ — workshop copy is out of sync' if not ok else '')
    except FileNotFoundError as e:
        check(f'{name}: hashes match', False, str(e))

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
