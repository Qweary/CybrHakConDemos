"""
test_workshop_e2e.py — Playwright e2e tests for the AI Village Workshop demos.

Covers what test_workshop.py cannot: actual browser behavior. Smoke checks
that each demo loads cleanly, toggles work (Ctrl+P / Ctrl+D / Space step
gate), and phase tooltips are wired. Does NOT make live API calls — those
are a separate concern (S50 territory).

Run with:
  .venv-e2e/bin/pytest test_workshop_e2e.py -v
"""

from __future__ import annotations

import re

import pytest

DEMOS = [
    ('forge',  'forge.html'),
    ('combat', 'combat.html'),
    ('evolve', 'evolve.html'),
]


def _goto(page, url):
    """Navigate and wait for DOMContentLoaded — the demos register listeners
    in inline scripts that run synchronously, so DOM-ready is enough."""
    page.goto(url, wait_until='domcontentloaded')


# ── Smoke ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize('label,name', DEMOS)
def test_demo_loads(safe_page, demo_url, label, name):
    """Page returns 200 and loads without console errors (the safe_page
    fixture asserts no console errors at teardown)."""
    response = safe_page.goto(demo_url(name), wait_until='domcontentloaded')
    assert response is not None and response.status == 200, \
        f'{label}: HTTP {response.status if response else "(no response)"}'


@pytest.mark.parametrize('label,name', DEMOS)
def test_pmode_default(safe_page, demo_url, label, name):
    """Body must carry `pmode` class on load — Session 41-44 polish locks
    this in as the default presentation mode."""
    _goto(safe_page, demo_url(name))
    body_class = safe_page.evaluate('() => document.body.className')
    assert 'pmode' in body_class, f'{label}: body class is "{body_class}", expected pmode'


@pytest.mark.parametrize('label,name', DEMOS)
def test_title_present(safe_page, demo_url, label, name):
    """Document title is non-empty. The demos don't all share a title
    string — checking presence rather than exact match keeps the test
    resilient to title polish."""
    _goto(safe_page, demo_url(name))
    title = safe_page.title()
    assert title and title.strip(), f'{label}: empty document title'


# ── Toggles ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize('label,name', DEMOS)
def test_pmode_ctrl_p_toggle(safe_page, demo_url, label, name):
    """Ctrl+P toggles the `pmode` class on body. The demos all install
    this handler in their main script."""
    _goto(safe_page, demo_url(name))
    # Default ON
    assert 'pmode' in safe_page.evaluate('() => document.body.className')
    safe_page.keyboard.press('Control+p')
    assert 'pmode' not in safe_page.evaluate('() => document.body.className'), \
        f'{label}: Ctrl+P did not remove pmode'
    safe_page.keyboard.press('Control+p')
    assert 'pmode' in safe_page.evaluate('() => document.body.className'), \
        f'{label}: Ctrl+P did not restore pmode'


# Per-demo demo-mode assertion: each demo signals demo mode differently.
DEMO_MODE_PROBE = {
    'forge':  '() => document.getElementById("ibtn")?.textContent || ""',
    'combat': '() => document.getElementById("combat-demo-btn")?.classList.contains("active")',
    'evolve': '() => document.getElementById("demo-btn")?.classList.contains("active")',
}
DEMO_MODE_ON_VALUE = {
    'forge':  '▶ RUN DEMO',  # the ibtn label flips when DEMO MODE is on
    'combat': True,
    'evolve': True,
}
DEMO_MODE_OFF_VALUE = {
    'forge':  '⚛ INITIATE FISSION',
    'combat': False,
    'evolve': False,
}


@pytest.mark.parametrize('label,name', DEMOS)
def test_ctrl_d_toggles_demo_mode(safe_page, demo_url, label, name):
    """Ctrl+D toggles DEMO MODE. Each demo signals the on/off state
    differently — the probe table above maps each to a concrete query."""
    _goto(safe_page, demo_url(name))
    # default OFF
    initial = safe_page.evaluate(DEMO_MODE_PROBE[label])
    if label == 'forge':
        # forge keeps demo OFF by default, ibtn shows ⚛ INITIATE FISSION
        assert DEMO_MODE_OFF_VALUE[label] in (initial or ''), \
            f'forge: ibtn label "{initial}" — expected "{DEMO_MODE_OFF_VALUE[label]}" before toggle'
    else:
        assert initial is False, f'{label}: demo mode should be OFF on load'
    # toggle ON
    safe_page.keyboard.press('Control+d')
    after_on = safe_page.evaluate(DEMO_MODE_PROBE[label])
    if label == 'forge':
        assert DEMO_MODE_ON_VALUE[label] in (after_on or ''), \
            f'forge: ibtn label "{after_on}" after Ctrl+D — expected to contain "{DEMO_MODE_ON_VALUE[label]}"'
    else:
        assert after_on is True, f'{label}: demo mode did not turn ON after Ctrl+D'
    # toggle OFF again
    safe_page.keyboard.press('Control+d')
    after_off = safe_page.evaluate(DEMO_MODE_PROBE[label])
    if label == 'forge':
        assert DEMO_MODE_OFF_VALUE[label] in (after_off or ''), \
            f'forge: ibtn label "{after_off}" after second Ctrl+D — expected "{DEMO_MODE_OFF_VALUE[label]}"'
    else:
        assert after_off is False, f'{label}: demo mode did not turn OFF after second Ctrl+D'


@pytest.mark.parametrize('label,name', DEMOS)
def test_space_advances_step_gate(safe_page, demo_url, label, name):
    """Inject a step-gate-style button, press Space, assert the button's
    click handler fired. The demos all listen for Space → click `.step-btn`
    in the DOM. We verify the listener wiring without running a full demo."""
    _goto(safe_page, demo_url(name))
    # Inject a step-btn that flags when clicked
    safe_page.evaluate('''() => {
        const b = document.createElement('button');
        b.className = 'step-btn';
        b.style.position = 'fixed';
        b.style.top = '0';
        b.id = '__test_step';
        b.onclick = () => { window.__step_clicked = true; };
        document.body.appendChild(b);
        window.__step_clicked = false;
    }''')
    safe_page.keyboard.press('Space')
    clicked = safe_page.evaluate('() => window.__step_clicked')
    assert clicked is True, f'{label}: Space did not fire a step-btn click'


# ── Phase tooltips ───────────────────────────────────────────────────────

PHASE_SELECTORS = {
    'forge':  '.ph[title]',           # 9 phases
    'combat': '.phase[title]',        # 14 phases (7 red + 7 blue)
    'evolve': '.eph[title]',          # 6 phases
}
EXPECTED_MIN = {'forge': 8, 'combat': 14, 'evolve': 6}


@pytest.mark.parametrize('label,name', DEMOS)
def test_phase_tooltips_present(safe_page, demo_url, label, name):
    """Each phase cell has a non-empty `title` attribute (S41-S44 polish
    audit lock-in). Loops over the live DOM rather than the source file so
    we catch render-time breakage too."""
    _goto(safe_page, demo_url(name))
    titles = safe_page.evaluate(f'''() => Array.from(
        document.querySelectorAll('{PHASE_SELECTORS[label]}'))
        .map(el => el.getAttribute('title') || '')''')
    assert len(titles) >= EXPECTED_MIN[label], \
        f'{label}: only {len(titles)} phase cells with title (expected ≥ {EXPECTED_MIN[label]})'
    empty = [i for i, t in enumerate(titles) if not t.strip()]
    assert not empty, f'{label}: phase cells {empty} have empty title'


# ── Tok-count + provider button presence (lightweight smoke for S47.5c/d) ─

@pytest.mark.parametrize('label,name', DEMOS)
def test_tok_count_element_present(safe_page, demo_url, label, name):
    """Token-count ticker (S47.5c) is present in the DOM (initially hidden;
    becomes visible during a LIVE+CC stream)."""
    _goto(safe_page, demo_url(name))
    has = safe_page.evaluate('() => !!document.getElementById("tok-count")')
    assert has, f'{label}: #tok-count element missing'


# Per-demo CLAUDE CODE provider button id
CC_BTN_ID = {'forge': 'prv-cc', 'combat': 'cprv-cc', 'evolve': 'eprv-cc'}


@pytest.mark.parametrize('label,name', DEMOS)
def test_claude_code_button_clickable(safe_page, demo_url, label, name):
    """Clicking the CLAUDE CODE provider button doesn't throw and selects
    the button (verified via .sel class on the button)."""
    _goto(safe_page, demo_url(name))
    btn_id = CC_BTN_ID[label]
    btn = safe_page.locator(f'#{btn_id}')
    assert btn.count() == 1, f'{label}: #{btn_id} not found'
    btn.click()
    classes = safe_page.evaluate(f'() => document.getElementById("{btn_id}").className')
    assert 'sel' in classes, f'{label}: #{btn_id} not selected after click (class: "{classes}")'
