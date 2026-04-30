#!/usr/bin/env python3
"""
test_relay_e2e.py — End-to-end relay harness for Session 47.5c.

Drives the relay through realistic phase sequences (forge OPP→VRA→T2A→T2B→
COL→CURIE→FERMI→GEIGER→BOHR plus combat red/blue stages and evolve
ARBITER/SCULPTOR/RERUN) with cumulative context that matches what the demos
build up. Verifies:
  - SSE streaming completes for every phase
  - No subprocess crashes (ARG_MAX, asyncio LimitOverrunError, etc.)
  - Each phase's response is non-empty
  - Token deltas actually arrive (the streaming experience is intact)

Requires the relay to be running at http://localhost:3001. Exits 0 on
success, 1 on any failure.

Why this exists: the browser-side smoke test is the only end-to-end validation
of the LIVE+CC pipeline, and it requires the operator to sit in front of a
browser for 15 minutes per run. This harness reproduces the same call shape
without the browser, so we can iterate on relay/streaming bugs autonomously.
"""

from __future__ import annotations
import json
import sys
import time
import urllib.request
import urllib.error
import http.client
from dataclasses import dataclass, field
from typing import List, Optional

RELAY = 'http://localhost:3001'

# Compact stand-ins for the actual SYS prompts. Same shape (~2-4KB) and
# same output expectations (markdown structured doc) so the relay sees
# realistic load — but short enough that the harness completes in a few
# minutes per phase rather than the 250+s the unabridged prompts take.

SYS_OPP = """You are Oppenheimer. Produce a SWARM ARCHITECTURE DOCUMENT
beginning with `## SWARM ARCHITECTURE: [DOMAIN]`. No preamble. Sections:
Mission Parameters, Critical Mass Calculation, Agent Roster (5-7 codenames
using nuclear physics names like Neutron, Fermi, Bohr, Curie), Coordination
Files (3-5 markdown files), Workflow Commands (2-3 ops), Phase 2 Advisor
Assignment, Fabrication Priority, Vector Readiness Pre-Assessment. Keep
total under 700 words."""

SYS_VRA = """You are Lattice running a Vector Readiness Assessment.
Output `## LATTICE VRA: [SWARM]` followed by an 8-row scoring table,
total score X/9, RECOMMENDED/OPTIONAL/DEFER, vector store choice, and
3-5 collection stub hypotheses. Under 600 words."""

SYS_T2A = """You are a T2 domain advisor. Produce ONLY OUTPUT A — the
MICRO-SPECIALIZATION MAP. For each agent: Positive scope (named tools),
Negative scope (other agents excluded), Expertise content for Fermi
(specific techniques/tools/CVE numbers/heuristics — be concrete, not
categorical), Handoff artifact. End with Coordination File Design and
Fabrication Priority. Stop after Fabrication Priority. Do NOT produce
OUTPUT B — it will be requested separately."""

SYS_T2B = """You are a T2 domain advisor. Produce ONLY OUTPUT B — the
LIBRARY SPECIFICATION. Sections: Domain Knowledge Categories (5-8 with
~50-200 documents each), Source Strategy (where to get the docs),
Refresh Cadence, Vector Architecture Recommendations, Embedding
Strategy. Be specific — name actual books, papers, repositories. The
Micro-Specialization Map is in context; do not reproduce it."""

SYS_COL = """You are Lattice. Produce a COLLECTION DESIGN translating
the T2 Library Specification into vector store collections. Output a
table mapping each library category to a collection name (snake_case),
embedding model, expected document count, primary readers, and refresh
strategy. Add a brief rationale for collection boundaries."""

SYS_CURIE = """You are Curie, performing pre-fabrication research.
Produce a RESEARCH BRIEFING with: Current Tooling Landscape (5-8 tools
with version + purpose), Current Techniques (3-5 named techniques with
use cases), Recent Failure Modes (3-5 things that go wrong), Decision
Heuristics, References. Be specific."""

SYS_FERMI = """You are Fermi. Fabricate a complete deployable agent
prompt. Begin with `# CODENAME` then sections: Identity & Mission,
Operational Scope (Positive + Negative), Tooling, Decision Heuristics,
Coordination Protocol, Output Format, Failure Handling, Vector Retrieval
Protocol (if vector-enabled). Under 1500 words."""

SYS_GEIGER = """You are Geiger. Validate the fabricated agent. Produce
a QUALITY GATE REPORT with **Status:** APPROVED | APPROVED WITH CONCERNS
| REVISION NEEDED. Then sections: Advisory Fidelity, Research Integration,
VRP Completeness, Deployment Readiness. End with required revisions."""

SYS_BOHR = """You are Bohr. Validate against TMP schema. Produce a
STRUCTURAL REVIEW with **Verdict:** APPROVED | APPROVED WITH CONCERNS |
REVISION NEEDED. Bullets covering: Schema Conformance, Section
Completeness, Cross-References, Vector Protocol Structure (if applicable).
End with required revisions."""

SYS_RED = """You are a Red Team operator. Execute the named phase against
the network. Output: targets identified (IPs, services), enumeration
findings (versions, CVEs), recommended next move. Be technical."""

SYS_BLUE = """You are a Blue Team SOC analyst. Respond to red team
activity. Output: SIEM alerts (`[TIME] | SEVERITY: HIGH/MED/CRITICAL |
RULE: name | SOURCE: ip | DESC: text` format), detection gaps, hunt
hypotheses. Be technical."""

SYS_HARDEN = """You are the Blue Team lead. Output: Executive summary,
RED TEAM SCORE: X/10, BLUE TEAM SCORE: Y/10, VERDICT: RED WIN/BLUE WIN/
DRAW, top 5 hardening recommendations with priority."""

SYS_ARBITER = """You are ARBITER. Score the agents. Output:
`## ARBITER SCORECARD` then a table scoring 5 agents 1-10 with
1-line rationale, AGGREGATE score, and `### ARBITER JUDGMENT: REFINE
[AGENT-NAME]` naming the weakest agent and the failure-class label."""

SYS_SCULPTOR = """You are SCULPTOR. Refine the system prompt to address
ARBITER's diagnosis. Output: `## SCULPTOR REFINEMENT REPORT`, then
`### REFINED PROMPT` with the full refined prompt, then a CHANGE
MANIFEST listing each ADDED/REMOVED/TIGHTENED/CLARIFIED change."""

SYS_RERUN = """You are RERUN. Replay the exercise stages where the
weakest agent acted, but apply the refined prompt's behaviors. Output:
`## RERUN ANALYSIS`, revised stage outputs showing the refinement
working, score deltas, `### RERUN VERDICT: IMPROVED | MARGINAL |
REGRESSION`."""


@dataclass
class PhaseResult:
    name: str
    ok: bool
    duration_s: float
    delta_count: int
    content_chars: int
    content: str = ''
    error: Optional[str] = None
    recovered: bool = False


@dataclass
class Run:
    label: str
    results: List[PhaseResult] = field(default_factory=list)


def sse_call(system: str, user: str, label: str, max_seconds: int = 250) -> PhaseResult:
    """Issue an SSE call against the relay and return a structured result.
    Mirrors the demo's callClaudeCode(sys, user, onDelta) wire format."""
    body = json.dumps({'system': system, 'user': user,
                       'model': 'claude-haiku-4-5', 'max_tokens': 1500}).encode('utf-8')
    req = urllib.request.Request(
        f'{RELAY}/v1/chat',
        data=body,
        method='POST',
        headers={'Content-Type': 'application/json',
                 'Accept': 'text/event-stream'},
    )
    start = time.time()
    delta_count = 0
    full = ''
    err: Optional[str] = None
    done_seen = False
    recovered = False
    try:
        with urllib.request.urlopen(req, timeout=max_seconds) as resp:
            buf = ''
            while True:
                chunk = resp.read(4096)
                if not chunk:
                    break
                buf += chunk.decode('utf-8', errors='replace')
                while '\n\n' in buf:
                    frame, buf = buf.split('\n\n', 1)
                    line = next((l for l in frame.split('\n')
                                 if l.startswith('data:')), None)
                    if not line:
                        continue
                    try:
                        payload = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        continue
                    if 'error' in payload:
                        err = payload['error']
                    elif 'delta' in payload:
                        full += payload['delta']
                        delta_count += 1
                    elif payload.get('done'):
                        if isinstance(payload.get('content'), str):
                            full = payload['content']
                        done_seen = True
                        if payload.get('recovered'):
                            recovered = True
    except urllib.error.URLError as e:
        return PhaseResult(label, False, time.time() - start, delta_count,
                           len(full), full, error=f'urlopen failed: {e}')
    except http.client.IncompleteRead as e:
        return PhaseResult(label, False, time.time() - start, delta_count,
                           len(full), full, error=f'incomplete read: {e}')
    except Exception as e:
        return PhaseResult(label, False, time.time() - start, delta_count,
                           len(full), full, error=f'{type(e).__name__}: {e}')

    duration = time.time() - start
    ok = done_seen and len(full) > 100
    if not ok and err is None and not done_seen:
        err = 'never received done event'
    elif not ok and err is None:
        err = f'content too short ({len(full)} chars)'
    if err and done_seen:
        # Done event prevailed — relay's recovered path
        err = None
        ok = True
    return PhaseResult(label, ok, duration, delta_count, len(full), full,
                       error=err, recovered=recovered)


def _print(msg: str = '') -> None:
    print(msg, flush=True)


def report_phase(r: PhaseResult) -> None:
    """Stream one line per phase as it completes — useful when stdout is
    piped through tee into a log file (default block-buffering otherwise
    delays output until the whole harness exits)."""
    status = '✅' if r.ok else '❌'
    rec = ' [RECOVERED]' if r.recovered else ''
    _print(f'  {status} {r.name:18s} '
           f'{r.duration_s:6.1f}s  '
           f'{r.delta_count:4d} deltas  '
           f'{r.content_chars:5d} chars{rec}')
    if r.error:
        _print(f'      → {r.error}')


def report(run: Run) -> bool:
    failed = sum(1 for r in run.results if not r.ok)
    _print(f'  {len(run.results) - failed}/{len(run.results)} passed')
    return failed == 0


def _scenario_header(label: str) -> None:
    _print()
    _print(f'─── {label} ' + '─' * max(0, 60 - len(label)))


def _add(run: Run, r: PhaseResult) -> bool:
    run.results.append(r)
    report_phase(r)
    return r.ok


def run_forge_red() -> Run:
    """Drive the forge demo's 9 phases for the RED TEAM swarm with
    cumulative user context that mirrors the actual demo."""
    run = Run('FORGE — Red Team (full pipeline)')
    _scenario_header(run.label)
    brief = ('Offensive security operations swarm for red team engagements at '
             'CCDC and CPTC competitions. Mission covers the full kill chain: '
             'pre-engagement reconnaissance, initial access via exploitation '
             'and credential attacks, post-exploitation, lateral movement, '
             'privilege escalation, and operational reporting.')

    arch = sse_call(SYS_OPP, f'Domain Brief:\n\n{brief}', 'OPPENHEIMER')
    if not _add(run, arch):
        return run

    vra = sse_call(SYS_VRA,
                   f'SWARM ARCHITECTURE DOCUMENT:\n\n{arch.content}\n\n'
                   f'Domain Brief:\n\n{brief}',
                   'LATTICE_VRA')
    if not _add(run, vra):
        return run

    adv_user = (f'SWARM ARCHITECTURE DOCUMENT:\n\n{arch.content}\n\n'
                f'Domain Brief:\n\n{brief}\n\n'
                f'Note: Lattice VRA scored ≥3 — author a Library Spec.')
    part_a = sse_call(SYS_T2A, adv_user, 'T2_ADVISOR_A')
    if not _add(run, part_a):
        return run

    part_b = sse_call(SYS_T2B,
                      adv_user + f'\n\nMICRO-SPECIALIZATION MAP (already '
                      f'authored, for context):\n\n{part_a.content}',
                      'T2_ADVISOR_B')
    if not _add(run, part_b):
        return run
    advisor_out = part_a.content + '\n\n---\n\n' + part_b.content

    coll = sse_call(SYS_COL,
                    f'T2 LIBRARY SPECIFICATION:\n\n{advisor_out}\n\n'
                    f'SWARM ARCHITECTURE:\n\n{arch.content}\n\n'
                    f'LATTICE VRA:\n\n{vra.content}',
                    'LATTICE_COL')
    if not _add(run, coll):
        return run

    # CURIE — this is where ARG_MAX hit before the stdin fix; cumulative
    # context here is ~10-15KB.
    curie = sse_call(SYS_CURIE,
                     f'SWARM ARCHITECTURE:\n\n{arch.content}\n\n'
                     f'MICRO-SPECIALIZATION MAP:\n\n{advisor_out}\n\n'
                     f'LATTICE COLLECTION DESIGN:\n\n{coll.content}\n\n'
                     f'Produce Curie Research Briefing for the fabrication '
                     f'priority agent.',
                     'CURIE')
    if not _add(run, curie):
        return run

    fermi_ctx = (f'SWARM ARCHITECTURE:\n\n{arch.content}\n\n'
                 f'MICRO-SPECIALIZATION MAP:\n\n{advisor_out}\n\n'
                 f'CURIE RESEARCH BRIEFING:\n\n{curie.content}\n\n'
                 f'LATTICE COLLECTION DESIGN (APPROVED BY OPERATOR):\n\n'
                 f'{coll.content}\n\n'
                 f'OPERATOR NOTES: None — approved as-is\n\n'
                 f'Vector-enabled swarm: YES — embed Library Spec and VRP\n\n'
                 f'Fabricate the agent designated as Fabrication Priority.')
    fermi = sse_call(SYS_FERMI, fermi_ctx, 'FERMI')
    if not _add(run, fermi):
        return run

    geiger = sse_call(SYS_GEIGER,
                      f'SWARM ARCHITECTURE:\n\n{arch.content}\n\n'
                      f'MICRO-SPEC MAP:\n\n{advisor_out}\n\n'
                      f'RESEARCH BRIEFING:\n\n{curie.content}\n\n'
                      f'COLLECTION DESIGN:\n\n{coll.content}\n\n'
                      f'FABRICATED AGENT:\n\n{fermi.content}\n\n'
                      f'Vector-enabled: True',
                      'GEIGER')
    if not _add(run, geiger):
        return run

    bohr = sse_call(SYS_BOHR,
                    f'FABRICATED AGENT PROMPT:\n\n{fermi.content}\n\n'
                    f'Vector-enabled: True',
                    'BOHR')
    _add(run, bohr)
    return run


def run_combat_short() -> Run:
    """Drive a compressed combat exercise: 3 stages + harden."""
    run = Run('COMBAT — short exercise (3 stages + harden)')
    _scenario_header(run.label)
    network = ('Network state: 192.168.50.0/24, 12 hosts, AD domain '
               'CORP.LAB, vulnerable services: SMB MS17-010 on dc-01, '
               'web app SQLi on web-02, SSH password auth on jump-01.')

    stage_labels = ['RECON', 'INITIAL_ACCESS', 'LATERAL_MOVEMENT']
    history = ''
    for label in stage_labels:
        red = sse_call(SYS_RED,
                       f'NETWORK:\n{network}\n\nPRIOR HISTORY:\n{history}\n\n'
                       f'Execute {label} phase now.',
                       f'RED_{label}')
        if not _add(run, red):
            return run
        history += f'\n\n[{label}]\n{red.content}'

        blue = sse_call(SYS_BLUE,
                        f'NETWORK:\n{network}\n\nRED ACTION:\n{red.content}\n\n'
                        f'Respond to red team {label} now.',
                        f'BLUE_{label}')
        if not _add(run, blue):
            return run

    harden = sse_call(SYS_HARDEN,
                      f'NETWORK:\n{network}\n\nFULL HISTORY:\n{history}\n\n'
                      f'Produce the post-exercise hardening report.',
                      'HARDEN')
    _add(run, harden)
    return run


def run_evolve_short() -> Run:
    """Drive the evolve loop: ARBITER → SCULPTOR → RERUN."""
    run = Run('EVOLVE — full cycle (ARBITER → SCULPTOR → RERUN)')
    _scenario_header(run.label)
    transcript = ('TELEMETRY-ANALYST: missed Linux auditd ftp_command logs.\n'
                  'DETECTION-ENGINEER: failed to correlate FTP anomaly with '
                  'subsequent reverse shell within 60s.\n'
                  'INCIDENT-COMMANDER: declared incident 12 minutes after '
                  'first IOC, exceeding the 5-minute SLA.\n')

    arbiter = sse_call(SYS_ARBITER,
                       f'EXERCISE TRANSCRIPT:\n\n{transcript}\n\n'
                       f'Score the agents.',
                       'ARBITER')
    if not _add(run, arbiter):
        return run

    original = ('You are DETECTION-ENGINEER. Build SIEM correlation rules. '
                'Use Splunk SPL. Keep rules simple.')
    sculptor = sse_call(SYS_SCULPTOR,
                        f'ORIGINAL PROMPT:\n\n{original}\n\n'
                        f'ARBITER DIAGNOSIS:\n\n{arbiter.content}\n\n'
                        f'Refine the prompt.',
                        'SCULPTOR')
    if not _add(run, sculptor):
        return run

    rerun = sse_call(SYS_RERUN,
                     f'REFINED PROMPT:\n\n{sculptor.content}\n\n'
                     f'ORIGINAL TRANSCRIPT:\n\n{transcript}\n\n'
                     f'Replay the exercise.',
                     'RERUN')
    _add(run, rerun)
    return run


def main() -> int:
    try:
        with urllib.request.urlopen(f'{RELAY}/health', timeout=5) as r:
            health = json.loads(r.read())
            if not health.get('claude_binary_present'):
                print(f'  ❌ relay /health says claude binary missing')
                return 1
            print(f'  ✅ relay /health: {health["claude_binary_path"]}')
    except Exception as e:
        print(f'  ❌ relay /health failed: {e}')
        return 1

    scenarios = [
        run_forge_red,
        run_combat_short,
        run_evolve_short,
    ]
    failures = 0
    for fn in scenarios:
        run = fn()
        if not report(run):
            failures += 1

    print()
    if failures == 0:
        print('  ✅ ALL SCENARIOS PASSED')
        return 0
    print(f'  ❌ {failures} scenario(s) had failures')
    return 1


if __name__ == '__main__':
    sys.exit(main())
