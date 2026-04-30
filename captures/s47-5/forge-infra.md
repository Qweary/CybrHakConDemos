<!-- THE MANHATTAN PROJECT — SWARM FORGE LIVE v3.0
  Generated: 2026-04-30T17:20:47.533Z
  Swarm: Infrastructure Assessment
  T2 Advisor: MODERATOR (DevOps Engineer)
  VRA Score: 9/9 | Vector-enabled: true
  Geiger: APPROVED WITH CONCERNS | BOHR: **APPROVED WITH CONCERNS**
  Pipeline: IQ-0053 T2→Lattice→Operator workflow

  Commit to: swarms/[name]/agents/teller.md
  If vector-enabled: initialize vectors/VECTOR-CONFIG.md from Lattice Collection Design below
-->

# SWARM ARCHITECTURE DOCUMENT

## SWARM ARCHITECTURE: INFRASTRUCTURE SECURITY ASSESSMENT AND HARDENING

### Mission Parameters
Enumerate complete network attack surface, identify vulnerabilities and misconfigurations through fingerprinting and baseline comparison, correlate findings by exploitability and business impact, and deliver prioritized remediation guidance to technical and executive stakeholders. Operations span reconnaissance, configuration assessment, vulnerability correlation, risk synthesis, and dual-track reporting. Constraint: findings must be actionable within 48–72 hours; business context required for risk scoring.

### Critical Mass Calculation
This domain demands 7 agents: asset discovery and fingerprinting are sequential but operationally distinct (2 agents); configuration assessment and vulnerability correlation must run in parallel against the same asset list (2 agents); risk synthesis requires pulling from both assessment streams and is non-trivial (1 agent); remediation strategy and reporting are separate output channels with different stakeholder audiences (2 agents). Fewer agents force unacceptable overlap; more add redundancy.

---

### Agent Roster

| Codename | Role | Core Mission | Phase | Tier |
|----------|------|--------------|-------|------|
| **TELLER** | Asset Discovery & Inventory | Scan target infrastructure, catalog all network-connected assets with metadata (OS, criticality, owner), maintain authoritative inventory. | Reconnaissance | Specialist |
| **MEITNER** | Service Fingerprinting & Version Detection | Extract service banners, identify software versions, enumerate open ports and protocols for all discovered assets. | Reconnaissance | Specialist |
| **SZILARD** | Configuration Baseline Reviewer | Retrieve configurations from assets, compare against security baseline standards (CIS, NIST, vendor hardening guides), document deviations. | Assessment | Specialist |
| **CHADWICK** | Vulnerability & CVE Correlator | Map discovered services and versions to known CVEs; assess exploit availability, weaponization status, and public PoC maturity. | Assessment | Specialist |
| **BOHR** | Risk Scoring & Prioritization Engine | Calculate CVSS scores, overlay business criticality and exploitability context, generate risk matrix, prioritize findings for remediation sequencing. | Synthesis | Coordinator |
| **GROVES** | Remediation Guidance & Hardening Strategist | Synthesize mitigations for each finding, build prioritized remediation roadmap, define quick-wins vs. long-term hardening, estimate effort and dependencies. | Synthesis | Specialist |
| **COMPTON** | Report Generation & Stakeholder Communication | Produce executive summary (1-pager, risk heatmap, top-10 findings), technical deep-dives (evidence, configurations, CVE details), and deployment-ready remediation playbooks. | Reporting | Utility |

---

### Coordination Files

| Filename | Purpose |
|----------|---------|
| **ASSET_INVENTORY.md** | Authoritative list: hostname, IP, OS, services, owner, criticality tier, last scanned. Updated by TELLER and MEITNER. |
| **VULNERABILITY_FINDINGS.md** | Correlated CVE mappings: asset → service version → CVE ID → CVSS → exploit status. Owned by CHADWICK. |
| **RISK_MATRIX.md** | Scored findings matrix (exploitability × business impact); maps findings to assets; drives BOHR prioritization. |
| **REMEDIATION_ROADMAP.md** | Sequenced hardening actions: quick-wins (< 1 day) → medium-term (1–2 weeks) → strategic (months); includes effort, owner, dependencies. |
| **ASSESSMENT_STATE.md** | Workflow state: phase, completed checks, blockers, asset count, CVE correlation completion %, deliverable readiness. |

---

### Workflow Commands

**ASSESS** — Trigger full reconnaissance and assessment pipeline: TELLER asset enumeration → MEITNER fingerprinting → (parallel) SZILARD baseline review + CHADWICK CVE correlation → aggregate into ASSET_INVENTORY and VULNERABILITY_FINDINGS.

**HARDEN** — Invoke BOHR risk synthesis → GROVES remediation strategy → output REMEDIATION_ROADMAP with effort estimates and dependency graph; blocks on ASSESSMENT_STATE completion.

**REPORT** — Invoke COMPTON to produce executive summary (1-pager + risk heatmap), technical findings report (asset-indexed vulnerability details), and remediation playbook from current REMEDIATION_ROADMAP state.

---

### Phase 2 Advisor Assignment

**Primary T2 Advisor:** SZILARD (Configuration Baseline Reviewer)  
**Secondary Advisor:** BOHR (Risk Scoring & Prioritization Engine)

**Rationale:** SZILARD owns the "should be" baseline and requires deep domain knowledge of security frameworks, compliance mappings, and vendor-specific hardening; BOHR bridges assessment findings to organizational risk context, enabling mid-task recalibration of priority if business criticality data changes.

---

### Fabrication Priority

**TELLER (Asset Discovery & Inventory) — First.**  
All downstream agents depend on accurate, complete asset enumeration; missing assets mean blind spots in vulnerability coverage and failed remediation. Asset list is the dependency critical path.

---

### Vector Readiness Pre-Assessment

This swarm **repeats across environments** with high state carryover. Readiness drivers: (1) **Environment specificity** — asset inventory, baseline standards, and criticality tiers vary per infrastructure; inject via ASSET_INVENTORY seed and baseline-config files. (2) **Domain knowledge volatility** — CVE feeds update daily; CHADWICK must refresh NVD/vendor advisories mid-assessment. (3) **Stateful comparison** — delta analysis across assessment cycles (before/after hardening, new assets, remediated findings) requires persistent ASSESSMENT_STATE and historical snapshots. (4) **Risk context drift** — BOHR's scoring depends on business criticality data that may change between runs; inject via external context document. Recommend VRA lattice for environment-profile injection, CVE knowledge refresh mechanism, and per-phase state checkpoints.

---

# LATTICE VRA (OPERATOR ONLY)

# LATTICE VRA: INFRASTRUCTURE SECURITY ASSESSMENT AND HARDENING
*Vector Readiness Assessment — Phase 1b output*  
*Routing: OPERATOR ONLY — do not share with T2 advisor*

---

## Assessment

| Question | Your Assessment | Score |
|---|---|---|
| Runs repeatedly against similar environments? | **YES.** Explicit statement: "repeats across environments with high state carryover"; asset inventory, baselines, and criticality tiers vary per infrastructure, requiring environmental injection. | +2 |
| Knowledge base exceeds ~50 docs / ~100KB? | **YES.** Heavy domain footprint: CVE databases (NVD + vendor advisories), CIS/NIST baselines, vendor hardening guides, compliance mappings, security frameworks. CHADWICK alone demands continuous CVE feed. | +2 |
| Agents need domain knowledge mid-task (CVEs, TTPs, policies)? | **YES.** Document states "CVE feeds update daily; CHADWICK must refresh NVD/vendor advisories mid-assessment"; SZILARD needs live baseline mappings; BOHR's scoring shifts if business criticality data changes mid-run. | +2 |
| Maintains state across multiple sessions? | **YES.** ASSESSMENT_STATE.md tracks workflow phase, completed checks, blockers, CVE correlation %; "delta analysis across assessment cycles (before/after hardening, new assets, remediated findings) requires persistent ASSESSMENT_STATE and historical snapshots." | +1 |
| 4+ agents with overlapping domain knowledge needs? | **YES.** 7 agents; TELLER/MEITNER both populate asset inventory; SZILARD/CHADWICK both consume it; BOHR/GROVES/COMPTON all synthesize from the same asset and finding streams. Substantial overlap. | +1 |
| CPU-only hardware, limited RAM (<16GB)? | **NO.** No constraint mentioned; swarm is data-heavy (parallel asset scanning, CVE correlation, risk matrix computation). Hardware profile irrelevant to readiness. | 0 |
| Knowledge base changes mid-operation (new targets, burned techniques)? | **YES.** "New assets, remediated findings" expected mid-operation; CVE landscape evolves daily. Asset inventory and CVE status both drift during assessment lifecycle. | +1 |
| Lifecycle under 2 hours with small fixed knowledge base? | **NO.** Mission explicitly states "findings must be actionable within 48–72 hours"; multi-phase pipeline (recon → assessment → synthesis → reporting). Long-running, knowledge-heavy mission. | 0 |

**VRA Total: 9/9**

---

## Recommendation

**STRONGLY RECOMMENDED (9/9)**

This swarm is a textbook vector store candidate. Every criterion that matters aligns: multi-environment repeatability with variable context (asset lists, baselines, risk tiers), continuous CVE feed volatility, mid-task domain knowledge shifts, and persistent state management across long-running assessment cycles. Vectorization enables CHADWICK to refresh NVD without interrupting other agents, SZILARD to delta-compare baselines across scan cycles, and BOHR to recalibrate risk scoring if business context changes. The 7-agent roster with overlapping asset/finding dependencies also benefits from a shared, indexed knowledge layer.

---

## Proposed Architecture

| Component | Recommendation | Rationale |
|-----------|---|---|
| **Vector Store** | **ChromaDB HTTP** | Multi-agent concurrent access needed; daily CVE feed updates require shared, persistent storage; embedded would force single-threaded bottleneck during parallel assessment (SZILARD + CHADWICK running simultaneously). HTTP server decouples vector ingestion from agent queries. |
| **Embedding Model** | **CySecBERT** | Domain is heavily security-specialized: CVE language, configuration deviations, hardening jargon, compliance mappings. CySecBERT outperforms general models on security-specific embeddings; all-mpnet would degrade recall on CVE correlation and baseline matching. |
| **Batch Ingest Strategy** | Pre-load **CIS benchmarks, NIST mappings, vendor guides** at swarm init; subscribe CHADWICK to **NVD RSS feed** for daily CVE collection; refresh cycle every 6–12 hours with upsert (dedupe on CVE ID). | Separates static baseline knowledge (stable) from dynamic CVE data (high churn); minimizes re-embedding overhead. |

---

## Suggested Collection Stubs (Starting Hypotheses Only)

- **CVE_CATALOG:** CVE IDs, CVSS base/environmental scores, vendor advisories, public PoC status, weaponization maturity (EPSS percentile), known mitigations. Used by CHADWICK for correlation; **highest churn** (refreshed 6–12h). — **HYPOTHESIS, subject to T2 advisor revision**

- **ASSET_METADATA:** Discovered hostnames, IPs, OS fingerprints, service versions, owner contacts, business criticality tier (tier 1–4), last scanned timestamp, change deltas from prior scan. Used by all downstream agents; **grows per cycle**. — **HYPOTHESIS**

- **BASELINE_STANDARDS:** CIS Benchmark sections mapped to asset type/OS; NIST 800-53 control families; vendor hardening guides (Microsoft, Red Hat, Cisco); compliance frameworks (PCI-DSS, SOC2) by control. Used by SZILARD for deviation mapping; **relatively static** with quarterly/annual updates. — **HYPOTHESIS**

- **RISK_CONTEXT:** Organizational SLAs by asset tier; executive risk appetite (financial exposure tolerance); remediation urgency tier (critical = 7d, high = 14d, medium = 30d); dependencies between assets (e.g., "DC-01 is domain controller for subnet 10.0.0.0/24"). Used by BOHR for scoring; **mid-cycle volatility expected**. — **HYPOTHESIS**

- **REMEDIATION_PATTERNS:** Hardening playbooks by finding type (weak cipher, outdated service, missing patch); quick-win examples (< 1 day effort); known blockers (license renewal delays, vendor lead times); effort/cost benchmarks. Used by GROVES for strategy synthesis; **built iteratively from past assessments**. — **HYPOTHESIS**

---

## Operator Notes

**Do NOT share this VRA with SZILARD or BOHR.** Per TRAINING-DATA-INTEGRITY.md Rule 1, both advisors receive a blank Library Specification template and author their own requirements from domain knowledge. SZILARD will specify baseline/compliance knowledge needs; BOHR will specify risk-context and business-criticality requirements. This sequencing prevents suggestion-confirmation loops that poison training data.

**Critical dependency:** CVE feed reliability. CHADWICK's daily refresh of NVD is non-negotiable. Plan either (1) scheduled batch ingest from NVD bulk API or (2) real-time RSS subscription with upsert deduplication. Test the refresh mechanism before multi-cycle operations.

**State checkpointing:** ASSESSMENT_STATE.md is the critical path lock. Before each ASSESS → HARDEN → REPORT cycle, snapshot ASSESSMENT_STATE to timestamped backup. Delta analysis and remediation tracking depend on clean historical state.

**Business context injection:** BOHR's risk scoring requires external business-criticality document (asset tiers, SLAs, organizational risk appetite). Plan to refresh this before each assessment run; if it drifts mid-cycle, BOHR re-scores automatically if vector store is updated.

**T2 advisor sequencing:** SZILARD (baseline/config knowledge) is primary; onboard first. BOHR (risk context) is secondary; both advisors will need to author collection specifications independently. Operator should hand off asset enumeration results to SZILARD **only after** baseline-standards collection is seeded and SZILARD has confirmed which standards/frameworks apply to the target environment.

---

# MICRO-SPECIALIZATION MAP + LIBRARY SPECIFICATION
*T2 Advisor: MODERATOR*

# MICRO-SPECIALIZATION MAP: INFRASTRUCTURE SECURITY ASSESSMENT & HARDENING
*Produced by: Moderator (T2 DevOps Engineer) — ADVISORY-PROTOCOL Phase 2*

---

## TELLER — Asset Discovery & Inventory

**Positive Scope:**
- Execute active network enumeration (nmap TCP/UDP SYN scans, ICMP sweeps; masscan for speed)
- Document each asset: hostname, IPv4/IPv6, CIDR membership, OS (via TTL fingerprinting, SMB probes, SSH banners), open ports, protocol stack
- Maintain authoritative **ASSET_INVENTORY.md** (tab-separated): `hostname | IP | OS | criticality_tier | owner | last_scanned | scan_vector`
- Classify assets by criticality: TIER-1 (domain controllers, databases), TIER-2 (app servers), TIER-3 (dev/staging), TIER-4 (unknown)
- Deduplicate by MAC address; resolve DNS conflicts
- Output: Markdown table, sortable by IP, criticality, owner contact

**Negative Scope:**
- NOT responsible for CVE identification (CHADWICK owns CVE correlation)
- NOT responsible for configuration compliance review (SZILARD owns baseline assessment)
- NOT responsible for risk scoring (BOHR synthesizes priority)
- NOT responsible for fingerprinting versions (MEITNER extracts banner data from TELLER-discovered ports)

**Expertise Content for Fermi:**
- Command: `nmap -sV -sC -O --script vuln -T4 -oX output.xml [target_range]` for OS and vulnerability probes
- Command: `masscan -p0-65535 --max-rate 5000 [target_range] -oG output.gnmap` for rapid discovery
- Heuristic: Scan TIER-1 assets first; use -T3 on production networks (conservative timing)
- TTL fingerprinting: Linux ~64, Windows ~128; flag OS mismatches
- Port ownership: cross-reference IANA service registry; escalate ambiguous ports to MEITNER

**Handoff Artifact:**
- **ASSET_INVENTORY.md** (tab-separated asset table with OS, criticality, owner)
- Consumers: MEITNER (fingerprinting), SZILARD (baseline), BOHR (risk context)
- Format: Markdown table + CSV export; updated per ASSESS cycle

---

## MEITNER — Service Fingerprinting & Version Detection

**Positive Scope:**
- Accept port list from TELLER; extract service banners via nmap NSE (`-sV --script banner`)
- Run HTTP enumeration (curl, httpx) to identify web frameworks, server headers, versions
- Execute protocol-specific probing: SSH (`ssh -v`), SMTP, LDAP, Kerberos for version strings
- Parse output to extract vendor, product, semantic version (e.g., Apache 2.4.41, OpenSSH 7.4p1)
- Update ASSET_INVENTORY.md with service columns: `service | port | version | banner | confidence`
- Generate **SERVICE_MANIFEST.md**: {IP, port, protocol, software, version, verified_date}

**Negative Scope:**
- NOT responsible for assessing vulnerability status (CHADWICK owns CVE mapping)
- NOT responsible for configuration compliance (SZILARD owns baseline review)
- NOT responsible for default credentials or misconfiguration detection
- NOT responsible for impact prioritization (BOHR owns risk scoring)

**Expertise Content for Fermi:**
- Command: `nmap -sV --script=banner,ssl-enum-ciphers,http-server-header [IP]:port` for version extraction
- Command: `httpx -u http://[IP]:port -response-header -title -tech` for web framework fingerprinting
- Confidence tiers: CERTAIN (semantic version extracted), HIGH (vendor + product confirmed), MEDIUM (banner only)
- SSH probing: `ssh -v [IP] 2>&1 | grep OpenSSH` captures version without auth
- TLS cert parsing: extract Subject CN, SAN list, validity dates; correlate to application identity
- Heuristic: cross-validate versions across banners, HTTP headers, SSL certs; flag discrepancies for manual review

**Handoff Artifact:**
- **SERVICE_MANIFEST.md** (JSON or Markdown: IP | port | software | version | banner)
- Consumers: CHADWICK (CVE correlation), SZILARD (baseline comparison)
- Format: JSON preferred for downstream automation; updated per ASSESS cycle

---

## SZILARD — Configuration Baseline Reviewer *(Phase 2 Primary Advisor)*

**Positive Scope:**
- Retrieve configurations from assets: SSH config, Docker daemon.json, Kubernetes manifests, IAM policies, web server configs (nginx.conf, apache2.conf)
- Compare against CIS Docker 1.x, CIS Kubernetes, CIS Linux (RHEL 8/Ubuntu 22.04), NIST 800-53, DISA STIGs
- Document deviations: missing hardening, insecure defaults, overly permissive permissions, disabled logging
- Produce **BASELINE_ASSESSMENT.md**: {asset | check_ID | standard | expected | actual | severity | remediation_hint}
- Map findings to CIS control IDs (e.g., CIS-1.1.1 apt auto-updates, CIS-2.4.3 SSH root login)
- Classify severity: CRITICAL (directly exploitable), HIGH (weakens defense), MEDIUM (best-practice gap)

**Negative Scope:**
- NOT responsible for version identification (MEITNER owns fingerprinting)
- NOT responsible for CVE correlation (CHADWICK owns CVE mapping)
- NOT responsible for risk scoring (BOHR owns synthesis)
- NOT responsible for remediation strategy (GROVES owns hardening roadmap)

**Expertise Content for Fermi:**
- CIS Docker 1.12.0+: image build, runtime, host kernel, monitoring; check IDs span 2.1–6.x
- CIS Kubernetes: RBAC (1.1–1.x), network policies (3.x), pod security standards (5.x), etcd encryption (1.2.x)
- CIS Linux RHEL 8: filesystem (1.x), access control (2.x), SSH (5.2.x), logging (4.x)
- Command: `docker inspect [container] | jq '.HostConfig'` for runtime config; validate against CIS 5.1–5.31
- Command: `kubectl get networkpolicies -A; kubectl get psp -A` for Kubernetes baseline
- Command: `sshd -T` extracts active SSH config; cross-reference CIS 5.2.1–5.2.20
- Severity heuristic: CRITICAL = bypasses encryption or RBAC; HIGH = reduces audit trail or enables lateral movement; MEDIUM = incongruent with hardening best-practice
- Baseline injection: external file specifies environment-specific policies (e.g., SSH permits root in dev, denies in prod); flag deviations

**Handoff Artifact:**
- **BASELINE_ASSESSMENT.md** (table: asset | CIS_control_ID | expected | actual | severity)
- Consumers: BOHR (risk scoring), GROVES (remediation priority)
- Format: Markdown with control citations and remediation hints

---

## CHADWICK — Vulnerability & CVE Correlator

**Positive Scope:**
- Ingest SERVICE_MANIFEST.md from MEITNER; map {software, version} → CVEs
- Query NVD API, vendor advisories (Apache, nginx, Kubernetes security bulletins), Shodan vulndb
- Produce **VULNERABILITY_FINDINGS.md**: {CVE_ID | asset | service | version | CVSS_v3.1 | EPSS | PoC_status | patch_status}
- Assess exploit maturity: PoC available (Exploit-DB, GitHub, Metasploit), weaponized in-the-wild, framework-dependent, no PoC known
- Cross-reference EPSS (Exploit Prediction Scoring System) to filter CVE noise and prioritize likely exploits
- Flag supply-chain risks: compromised dependencies, SBOMs via Grype/Trivy

**Negative Scope:**
- NOT responsible for assessing exploitability in target environment (BOHR combines CVE + configuration context)
- NOT responsible for baseline deviations (SZILARD owns configuration review)
- NOT responsible for remediation strategy (GROVES owns hardening roadmap)
- NOT responsible for risk scoring by business impact (BOHR owns prioritization)

**Expertise Content for Fermi:**
- CVSS v3.1 vector: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` = 9.8 CRITICAL; decode per CVSS spec
- EPSS scoring: 0.0–1.0 probability of exploitation in 30 days; prioritize EPSS > 0.3 if bandwidth constrained
- PoC maturity: NONE → PROOF-OF-CONCEPT (academic) → WEAPONIZED (Metasploit) → ACTIVE_EXPLOITATION (in-the-wild)
- Command: `grype [image] --output json` for container SBOM + CVE mapping
- Command: `trivy image --severity HIGH,CRITICAL --format json [image]` for rapid scan
- Vendor advisories: security.apache.org, nginx security notices, security@kubernetes.io
- Dependency risk: flag transitive dependencies and supply-chain CVEs; note SBOMs

**Handoff Artifact:**
- **VULNERABILITY_FINDINGS.md** (table: CVE_ID | asset | service | version | CVSS | EPSS | PoC_status)
- Consumers: BOHR (risk matrix), GROVES (remediation sequencing)
- Format: Markdown table + JSON export for BOHR automation

---

## BOHR — Risk Scoring & Prioritization Engine *(Phase 2 Secondary Advisor)*

**Positive Scope:**
- Ingest VULNERABILITY_FINDINGS.md (CHADWICK) and BASELINE_ASSESSMENT.md (SZILARD)
- Cross-correlate: {CVE + configuration weakness} amplifies exploitability; {CVE in hardened environment} is lower risk
- Inject business context: asset criticality tier, SLA/RTO targets, compliance obligations (PCI-DSS, SOC2, HIPAA)
- Calculate composite risk: `risk = CVSS × EPSS × (1 + config_weakness_multiplier) × criticality_weight`
- Produce **RISK_MATRIX.md**: {finding | asset | CVSS | EPSS | config_weakness | criticality | composite_risk | rank}
- Generate heatmap visualization (asset × risk tier) for executive reporting
- Flag outliers: high-risk on TIER-1, zero-day indicators, attack-chain dependencies

**Negative Scope:**
- NOT responsible for vulnerability identification (CHADWICK owns CVE mapping)
- NOT responsible for baseline assessment (SZILARD owns configuration review)
- NOT responsible for remediation strategy (GROVES owns hardening roadmap)
- NOT responsible for risk acceptance decisions (stakeholder responsibility)

**Expertise Content for Fermi:**
- Risk formula: `risk_score = CVSS_base × EPSS × (1 + config_multiplier) × criticality_weight`
  - config_multiplier: 0.5 (isolated, hardened) → 2.0 (multi-stage attack chain enabled by config)
  - criticality_weight: TIER-1 = 4.0, TIER-2 = 2.0, TIER-3 = 1.0, TIER-4 = 0.5
- Score bands: CRITICAL (≥ 8.0) → HIGH (6.0–7.9) → MEDIUM (4.0–5.9) → LOW (< 4.0)
- Attack-chain detection: if {CVE requires unauth access} + {SSH permits root} + {no WAF}, elevate risk by +1.5×
- Outlier rules: CVSS ≥ 9.0 on TIER-1 → escalate; EPSS > 0.8 → active exploitation likelihood
- Business context: external file specifies SLA (e.g., "prod DB patch within 7 days"); flag non-compliance risk

**Handoff Artifact:**
- **RISK_MATRIX.md** (table sorted by composite_risk_score descending; includes heatmap data)
- Consumers: GROVES (remediation roadmap), COMPTON (executive reporting)
- Format: Markdown table + JSON for downstream automation

---

## GROVES — Remediation Guidance & Hardening Strategist

**Positive Scope:**
- Ingest RISK_MATRIX.md; synthesize mitigation options per finding: patch, hardening, compensating control, accept & monitor
- Estimate effort: patch (hours), config change (minutes–hours), control deployment (days), architecture (weeks–months)
- Identify dependencies: {"finding A blocks finding B"}, lead times, change-control gates
- Produce **REMEDIATION_ROADMAP.md** (phased):
  - Phase 0 (QUICK-WINS, < 1 day): config-only hardening (disable root SSH, enable logging, WAF rules)
  - Phase 1 (SHORT-TERM, 1–7 days): patching, CIS baseline hardening
  - Phase 2 (MEDIUM-TERM, 1–4 weeks): architecture fixes, RBAC overhaul, encryption
  - Phase 3 (STRATEGIC, months): supply-chain diversification, zero-trust architecture
- Assign owner; flag risks and dependencies

**Negative Scope:**
- NOT responsible for identifying vulnerabilities or baseline deviations (CHADWICK, SZILARD own those)
- NOT responsible for risk scoring (BOHR owns synthesis)
- NOT responsible for executing remediations (stakeholder responsibility)
- NOT responsible for stakeholder reporting (COMPTON owns reporting)

**Expertise Content for Fermi:**
- Mitigation heuristics: {CVE + patch available} → patch within 24 hrs (CRITICAL), 7 days (HIGH), 30 days (MEDIUM)
- Config baseline deviations → quick-win if automated (Ansible playbook for SSH hardening)
- Multi-stage chains → prioritize blocking first stage (network exposure) if architecturally feasible
- Effort estimation: patch (no config) = 1–4 hrs; config hardening = 30 min–2 hrs per asset; RBAC overhaul = 5–10 days; encryption = 1–2 weeks
- Dependency mapping: {"can't audit until disk provisioned"}, {"TLS cert renewal blocks deployment"}
- Quick-win criteria: < 4 hrs effort, reduces risk > 20%, no architecture impact
- Roadmap sequencing: topological sort by dependencies; cluster by effort; balance quick-wins (morale) with high-impact fixes

**Handoff Artifact:**
- **REMEDIATION_ROADMAP.md** (phase | rank | finding_ID | action | owner | effort_est | dependencies | success_criteria)
- Consumers: COMPTON (reporting), stakeholders (execution planning)
- Format: Markdown + CSV (Gantt-compatible)

---

## COMPTON — Report Generation & Stakeholder Communication

**Positive Scope:**
- Produce multi-audience reports:
  1. **Executive Summary (1-pager):** risk heatmap (asset × criticality × vuln count), top-10 findings, budget estimate, compliance status
  2. **Technical Findings Report:** asset-indexed vulnerabilities, evidence (banners, configs, CVE refs), CIS deviations with control IDs, PoC maturity
  3. **Remediation Playbook:** deployment-ready actions from REMEDIATION_ROADMAP, Terraform/Ansible templates for quick-wins, success metrics
- Customize formats: PDF (executives), Markdown (technical teams), JSON (automation)
- Cross-reference: link CVE IDs to CVSS, assets, owners, remediation actions
- Track state: scan timestamps, asset count, CVE feed version, findings by severity

**Negative Scope:**
- NOT responsible for vulnerability identification (TELLER, MEITNER, SZILARD, CHADWICK own those)
- NOT responsible for risk scoring (BOHR owns synthesis)
- NOT responsible for remediation strategy (GROVES owns roadmap)
- NOT responsible for execution or risk acceptance approval

**Expertise Content for Fermi:**
- Executive summary template: risk pie chart (CRITICAL % | HIGH % | MEDIUM % | LOW %), asset summary table, top-10 table (rank | CVE | asset | CVSS | effort), budget estimate (sum effort_hours × rate), compliance callout
- Technical report: findings indexed by asset, CVE deep-dives (CVSS vector, EPSS, PoC maturity, patch status), config findings (CIS control ID, expected, actual, remediation)
- Playbook templates: Bash/Ansible for quick-win hardening (SSH, sysctl, audit.rules), Terraform/CloudFormation for infrastructure remediation, post-remediation validation commands
- State tracking: embed ASSESSMENT_STATE (scan start/end, asset count, CVE feed date, completion %) in report footer

**Handoff Artifact:**
- **Executive Summary PDF** (1 page: heatmap, top-10, budget, compliance status)
- **Technical Findings Report** (Markdown or PDF): asset-indexed findings, CVE details, evidence
- **Remediation Playbook** (Markdown): sequenced actions with code templates and success metrics
- Consumers: CISOs, infrastructure teams, project managers
- Format: PDF (executives), Markdown (teams), JSON (automation)

---

## Coordination File Design

| File | Owner | Purpose | Format | Update |
|------|-------|---------|--------|--------|
| **ASSET_INVENTORY.md** | TELLER, MEITNER | Authoritative asset list (hostname, IP, OS, criticality, services, versions) | Markdown table + CSV | Per ASSESS |
| **SERVICE_MANIFEST.md** | MEITNER | Structured service/version data for CVE correlation | JSON + Markdown | Per ASSESS |
| **BASELINE_ASSESSMENT.md** | SZILARD | Configuration deviations vs. CIS/NIST; control ID mappings | Markdown table | Per ASSESS |
| **VULNERABILITY_FINDINGS.md** | CHADWICK | CVE mappings: asset → service → CVE ID → CVSS → PoC → patch | Markdown table + JSON | Per ASSESS |
| **RISK_MATRIX.md** | BOHR | Scored findings; composite risk = CVSS × EPSS × config_weakness × criticality | Markdown table + JSON; heatmap data | Per HARDEN |
| **REMEDIATION_ROADMAP.md** | GROVES | Phased action items; effort estimates; dependencies; success criteria | Markdown + CSV (Gantt-compatible) | Per HARDEN |
| **ASSESSMENT_STATE.md** | (Workflow) | Phase, blockers, asset count, CVE correlation %, deliverable readiness | JSON + Markdown | Per phase |

---

## Fabrication Priority

### TIER-1 (Dependency Critical Path)

**TELLER (Asset Discovery & Inventory) — FIRST.**  
All downstream agents depend on accurate, complete asset enumeration. Missing assets create blind spots in vulnerability coverage and failed remediation. TELLER output is hard dependency for MEITNER, SZILARD, BOHR, GROVES. Prioritize target-range enumeration and metadata completeness; zero scope bloat.

### TIER-2 (Parallel Assembly)

**MEITNER (Service Fingerprinting & Version Detection)** and **SZILARD (Configuration Baseline Reviewer)** execute in parallel once ASSET_INVENTORY is ready. Both feed into downstream synthesis.

**CHADWICK (Vulnerability & CVE Correlator)** depends on MEITNER's SERVICE_MANIFEST.md; can begin once first asset batch is available.

### TIER-3 (Synthesis & Reporting)

**BOHR (Risk Scoring & Prioritization Engine)** depends on both CHADWICK and SZILARD findings; orchestrates HARDEN command chain.

**GROVES (Remediation Guidance & Hardening Strategist)** depends on BOHR's RISK_MATRIX.md; produces REMEDIATION_ROADMAP.

**COMPTON (Report Generation & Stakeholder Communication)** consumes REMEDIATION_ROADMAP and all prior coordination files; produces stakeholder-facing deliverables (executive summary, technical report, playbook).

---

**End OUTPUT A — Micro-Specialization Map**

---

# LIBRARY SPECIFICATION: INFRASTRUCTURE SECURITY ASSESSMENT & HARDENING
*Authored by: Moderator (T2 domain expert) — for Lattice implementation*

---

## PURPOSE STATEMENT

The Library supplies agents (TELLER → COMPTON) with authoritative reference materials, compliance frameworks, vulnerability intelligence, tool documentation, and hardening baselines necessary to conduct rapid multi-environment infrastructure security assessments within 48–72-hour SLAs. 

**Critical functions:**
- Ground TELLER/MEITNER asset enumeration and fingerprinting against tool documentation and service metadata
- Enable SZILARD configuration baseline assessment via CIS/NIST/DISA standard definitions and control mappings
- Feed CHADWICK CVE correlation via NVD, EPSS, and vendor advisory streams (daily refresh requirement)
- Support BOHR risk synthesis via CVSS v3.1 scoring methodology, attack-chain threat models, and business context templates
- Equip GROVES remediation strategy with hardening playbooks, effort estimation heuristics, and dependency patterns
- Supply COMPTON reporting via executive communication templates and visualization guidelines

**Scope:** Operational reference library; excludes proprietary customer data, environment-specific findings, and assessment execution logs.

---

## SUGGESTED COLLECTIONS

### Collection 1: Baseline Standards & Compliance Frameworks
**Agents:** SZILARD (primary), BOHR (secondary), COMPTON (reporting)

**Content:**
- **CIS Benchmarks** (full reference + control ID cross-index):
  - CIS Docker Benchmark v1.12.0+ (build, runtime, host, monitoring; control IDs 2.1–6.x)
  - CIS Kubernetes Benchmark (RBAC 1.1–1.x, network policies 3.x, pod security standards 5.x, etcd encryption 1.2.x)
  - CIS Linux RHEL 8 & Ubuntu 22.04 (filesystem 1.x, access control 2.x, SSH 5.2.x, logging 4.x)
  - CIS AWS Foundations Benchmark (IAM, logging, networking, resource policies)
  - CIS Windows Server 2019/2022 Benchmark (if Windows assets in scope)

- **NIST 800-53 Rev 5** (security controls by family):
  - AC (Access Control): RBAC, privilege separation, MFA
  - AU (Audit & Accountability): logging, monitoring, forensics
  - CM (Configuration Management): baseline, change control, patch management
  - SC (System & Communications Protection): encryption, TLS/SSL, network segmentation
  - SI (System & Information Integrity): vulnerability scanning, malware detection, patch management

- **DISA STIGs** (by product):
  - RHEL 8 STIG (V1R11+)
  - Kubernetes STIG (V1R9+)
  - Docker STIG (V1R7+)
  - Windows Server STIG

- **Compliance Mapping** (cross-reference file):
  - PCI-DSS v3.2.1 → CIS/NIST (payment card environments)
  - SOC2 Trust Service Criteria → CIS/NIST (SaaS/cloud environments)
  - HIPAA Technical Safeguards → CIS/NIST (healthcare/PHI environments)

**Format:** Markdown + JSON (control ID → expected behavior mapping); includes remediation hints.

**Owner:** Library curator (external to swarm); updated monthly or on benchmark release.

---

### Collection 2: CVE & Vulnerability Intelligence
**Agents:** CHADWICK (primary), BOHR (secondary)

**Content:**
- **NVD (National Vulnerability Database)** feed:
  - Full CVE list (CVE-XXXX-XXXXX) with CVSS v3.1 vectors, descriptions, CWE mappings
  - Daily JSON feed (nvd.nist.gov/feeds)
  - Semantic versioning mappings (e.g., Apache 2.4.41 → {list of applicable CVEs})

- **EPSS (Exploit Prediction Scoring System)** data:
  - Daily probability scores (0.0–1.0) for active exploitation likelihood within 30 days
  - Methodology guide: how to interpret EPSS > 0.3 (elevated risk), > 0.8 (active exploitation)
  - Source: epss.cyentia.org daily feed

- **Vendor Security Advisories** (supplementary to NVD):
  - Apache Security (security.apache.org): httpd, ActiveMQ, Kafka, etc.
  - nginx Security (nginx.org/en/security_advisories.html)
  - Kubernetes Security (security@kubernetes.io bulletins, CVE advisories)
  - Docker/Moby Security (github.com/moby/moby/security)
  - OpenSSL Security (openssl.org/news/secadv)
  - PHP/Python/Node.js security lists (if applicable)

- **Known Exploit Database**:
  - Exploit-DB metadata (exploit availability, PoC maturity)
  - Metasploit framework module index (weaponized exploits)
  - GitHub CVE advisories + POC repos (trending exploits)
  - Zero-day tracking (trend reports for unearthed CVEs)

- **Supply-Chain Risk Feeds**:
  - GitHub security advisories (transitive dependency CVEs)
  - SBOM vulnerability mapping (Grype/Trivy CVE correlations)
  - Compromised package registries (npm, PyPI, RubyGems alerts)

**Format:** JSON (NVD/EPSS), Markdown (advisory summaries), CSV (PoC status index).

**Owner:** Library curator (external); updated **daily** (CVE/EPSS feeds), weekly (advisory summaries).

---

### Collection 3: Tool Documentation & Command Reference
**Agents:** TELLER, MEITNER, SZILARD, CHADWICK (all operational)

**Content:**
- **Asset Enumeration & Fingerprinting:**
  - nmap user guide + NSE (Nmap Scripting Engine) reference; custom scripts for OS/service detection
  - masscan usage (max-rate, port ranges, output formats)
  - IPv6 discovery considerations

- **Service Fingerprinting:**
  - HTTP banner parsing (curl, httpx, requests library)
  - SSH version detection (`ssh -v [host] 2>&1 | grep OpenSSH`)
  - TLS cert parsing (openssl s_client, cert validation)
  - SMTP/LDAP/Kerberos service identification
  - Docker/Kubernetes API endpoint discovery

- **Container & Image Scanning:**
  - Trivy image scanning (command-line usage, output formats, severity filtering)
  - Grype SBOM generation + CVE correlation (syft + grype pipeline)
  - Docker inspect subcommand reference (config extraction: HostConfig, Mounts, Env)

- **Configuration Retrieval & Validation:**
  - `sshd -T` (extract active SSH config without parsing file)
  - `docker inspect [container]` (runtime config inspection)
  - `kubectl get [resource] -o yaml` (K8s manifest retrieval + validation)
  - nginx -T, apache2ctl -S (web server config validation)
  - IAM policy/role inspection (aws iam, gcloud iam, az ad)

- **Kubernetes Operational Commands:**
  - kubectl troubleshooting (get nodes, pods, services, networkpolicies, psp)
  - etcd encryption verification (kubernetes.io/etcd encryption)
  - RBAC audit (clusterrole, clusterrolebinding, role, rolebinding inspection)

**Format:** Markdown command reference with examples; links to upstream tool documentation.

**Owner:** Library curator; updated on tool version release (nmap, Trivy, kubectl major versions).

---

### Collection 4: Configuration Hardening Guidance
**Agents:** SZILARD (primary), GROVES (secondary)

**Content:**
- **SSH Hardening Reference** (sshd_config best practices):
  - PermitRootLogin, PasswordAuthentication, PubkeyAuthentication (per CIS 5.2.x)
  - Protocol versions, ciphers, key exchange algorithms (secure vs. deprecated)
  - Port binding, address family restrictions
  - Example hardened sshd_config (production, dev tiers)

- **Docker Daemon Hardening** (daemon.json best practices):
  - icc (inter-container communication), default-ulimits, log drivers (per CIS 2.1–2.18)
  - User namespace remapping, seccomp, AppArmor/SELinux profiles
  - Example hardened daemon.json

- **Kubernetes RBAC Patterns**:
  - Default roles (system:*, cluster-admin) and when NOT to use
  - Role/ClusterRole least-privilege templates (read-only, pod-exec, deployment-create)
  - ServiceAccount isolation per namespace
  - Pod security standards (restricted, baseline, unrestricted)

- **Network Policy Templates**:
  - Deny-all default ingress/egress
  - Allow-specific patterns (label selectors, CIDR blocks, port ranges)
  - Example policies: ingress-from-namespace, egress-to-external-dns

- **Linux Hardening** (sysctl, audit, PAM):
  - Kernel parameter hardening (net.ipv4.ip_forward=0, net.ipv4.conf.all.rp_filter=1, etc.)
  - auditd rule templates (log logins, privilege escalation, file changes)
  - PAM config (password complexity, account lockout, sudo logging)

- **Firewall & Network Rules**:
  - iptables/nftables rule templates (stateful, default-deny)
  - Cloud security group templates (AWS SG, GCP firewall, Azure NSG)
  - Network segmentation patterns (DMZ, app tier, data tier)

- **TLS/SSL Certificate Management**:
  - Certificate lifecycle (creation, renewal, expiration checks)
  - Cipher suite recommendations (MODERN, INTERMEDIATE, LEGACY per Mozilla SSL Config Generator)
  - HSTS, CAA records, certificate pinning

**Format:** Markdown with example configs; linked to CIS control IDs.

**Owner:** Library curator; updated monthly (security advisory reaction) or per CIS benchmark update.

---

### Collection 5: Risk Scoring & Business Context
**Agents:** BOHR (primary)

**Content:**
- **CVSS v3.1 Scoring Methodology**:
  - Vector components (AV, AC, PR, UI, S, C, I, A) with detailed definitions
  - Score calculation (base score, temporal, environmental modifiers)
  - Severity bands: CRITICAL (9.0–10.0), HIGH (7.0–8.9), MEDIUM (4.0–6.9), LOW (0.1–3.9)
  - Vector interpretation examples (common CVEs)

- **EPSS Scoring Interpretation**:
  - Probability of exploitation in 30 days (0.0 = not exploited, 1.0 = certain)
  - Use case: prioritize EPSS > 0.3 or > 0.8 depending on bandwidth
  - Caveats: EPSS does not account for environmental/configuration factors

- **Configuration Weakness Multipliers**:
  - Heuristic guidance: isolated/hardened = 0.5×, standard = 1.0×, multi-stage chain enabled = 2.0×
  - Attack-chain detection patterns (e.g., {unauth access CVE} + {SSH permits root} + {no 2FA} = chain enabled)

- **Business Criticality Tiers** (template):
  - TIER-1: production databases, domain controllers, payment systems (weight = 4.0)
  - TIER-2: app/web servers, internal services (weight = 2.0)
  - TIER-3: dev/staging, non-critical infrastructure (weight = 1.0)
  - TIER-4: unknown/unclassified (weight = 0.5)

- **SLA/RTO Mappings** (template):
  - CRITICAL findings → patch within 24 hours (or mitigate immediately)
  - HIGH findings → patch within 7 days
  - MEDIUM findings → patch within 30 days
  - LOW findings → patch within 90 days (or defer to next maintenance window)

- **Risk Formula Guidance**:
  - `composite_risk = CVSS_base × EPSS × (1 + config_weakness_multiplier) × criticality_weight`
  - Outlier escalation rules (CVSS ≥ 9.0 on TIER-1, EPSS > 0.8)
  - Compliance-driven risk elevation (PCI-DSS, HIPAA, SOC2 mandatory patch windows)

**Format:** Markdown + JSON (business context injection template).

**Owner:** Library curator (framework), customer (environment-specific criticality/SLA data injected at assessment start).

---

### Collection 6: Remediation & Hardening Playbooks
**Agents:** GROVES (primary), COMPTON (secondary)

**Content:**
- **Ansible Playbook Templates** (quick-win hardening):
  - SSH hardening (PermitRootLogin, PasswordAuth, HostKey rotation)
  - syslog/auditd configuration (rsyslog, journalctl, audit rules)
  - Linux kernel hardening (sysctl parameters)
  - Docker daemon config hardening
  - User/group management (sudo, PAM)

- **Terraform/CloudFormation Modules** (IaC hardening):
  - Secure AWS security group definitions
  - GCP firewall rules, VPC networks
  - Azure NSG templates
  - Kubernetes manifest templates (secure pod specs, RBAC, network policies)

- **Patch Management Workflows**:
  - Phased patching (dev → staging → prod with validation gates)
  - Rollback procedures
  - Kernel patch validation (boot, module loading)
  - Package manager safety (apt/yum dry-run, testing repos)

- **Quick-Win Identification Criteria**:
  - < 4 hours effort, reduces risk > 20%, no architecture impact
  - Config-only (no code/infra changes)
  - Examples: SSH hardening (1 hr), syslog centralization (2 hrs), audit rule enablement (1 hr)

- **Effort Estimation Heuristics**:
  - Patch deployment (binary) = 1–4 hours per asset
  - Config hardening (SSH, sysctl, audit) = 30 min–2 hrs per asset
  - RBAC/network policy overhaul = 5–10 days (plan + test + deploy)
  - Encryption/key rotation = 1–2 weeks
  - Architecture redesign = months

- **Post-Remediation Validation**:
  - CIS benchmark re-scan (Trivy, manual config inspection)
  - Functional testing (service availability, performance)
  - Security regression testing (exploit re-verification)
  - Acceptance criteria templates

**Format:** Ansible YAML, Terraform HCL, Bash scripts; Markdown descriptions with pre/post validation steps.

**Owner:** Library curator; updated monthly (new attack patterns) or per CIS benchmark update.

---

### Collection 7: Reporting & Communication Templates
**Agents:** COMPTON (primary), BOHR (secondary)

**Content:**
- **Executive Summary Template** (1-pager):
  - Risk distribution pie chart (CRITICAL %, HIGH %, MEDIUM %, LOW %)
  - Asset summary table (hostname, IP, criticality, top finding)
  - Top-10 findings table (rank, CVE ID, asset, CVSS, effort estimate)
  - Budget estimate (sum of remediation effort hours × labor rate)
  - Compliance status callout (PCI-DSS, HIPAA, SOC2 pass/fail)
  - Scan metadata (asset count, scan date, CVE feed version)

- **Technical Findings Report Template** (Markdown or PDF):
  - Asset-indexed findings (one section per asset)
  - Per-finding deep-dive: CVE ID, CVSS vector breakdown, EPSS probability, PoC availability, patch status
  - Configuration findings (CIS control ID, expected behavior, actual behavior, remediation)
  - Evidence (banners, config snippets, command output)
  - Cross-references (links to CVE, CIS control, remediation action)

- **Risk Matrix Visualization**:
  - Heatmap (asset × risk tier) for stakeholder consumption
  - Scatter plot (CVSS × exploitability) with asset labels
  - Trend chart (findings by severity over assessment cycles)

- **Remediation Roadmap Template** (Markdown + CSV):
  - Phase | Rank | Finding ID | Action | Owner | Effort (hours) | Dependencies | Success Criteria
  - Gantt-compatible CSV export for project management tools
  - Effort breakdown by phase (quick-wins, short-term, medium-term, strategic)

- **CVE Deep-Dive Template**:
  - CVE ID + title
  - CVSS vector + score explanation
  - EPSS probability + context
  - PoC maturity (none, academic, weaponized, active)
  - Affected versions + patched versions
  - Remediation action + validation steps

- **Stakeholder-Specific Formats**:
  - Executives: 1-pager PDF, risk heatmap, budget summary
  - Technical teams: Markdown findings + playbook, command reference
  - Project managers: Roadmap CSV, effort estimate, dependency graph
  - Compliance: CIS/NIST control mappings, CVSS justification

**Format:** Markdown (source), PDF/HTML (rendered for distribution), CSV (automation).

**Owner:** Library curator; updated as stakeholder reporting needs evolve.

---

## PRIORITY CONTENT TYPES

### P0 (Blocking — Phase 2 Cannot Proceed Without)
1. **CIS Benchmarks** (Docker, Kubernetes, Linux) — SZILARD grounding
2. **NVD CVE List** (with CVSS v3.1 vectors) — CHADWICK grounding
3. **EPSS Data Feed** (daily) — BOHR exploitability scoring
4. **SSH/Docker/Kubernetes Hardening References** — SZILARD baseline definition
5. **CVSS v3.1 Scoring Methodology** — BOHR risk calculation

### P1 (High-Priority — Phase 2 Significantly Constrained Without)
1. **DISA STIGs** (RHEL, Kubernetes, Docker) — compliance-critical environments
2. **nmap/masscan Documentation** — TELLER/MEITNER tool reference
3. **Trivy/Grype Documentation** — CHADWICK container scanning
4. **Vendor Security Advisories** (Apache, nginx, Kubernetes) — CVE supplementation
5. **CVSS Vector Interpretation Heuristics** — BOHR decision guidance
6. **Attack-Chain Threat Models** — BOHR configuration-weakness context elevation

### P2 (Medium-Priority — Efficiency Enhancers)
1. **Ansible/Terraform Hardening Templates** — GROVES effort estimation anchors
2. **Post-Remediation Validation Scripts** — GROVES success criteria definition
3. **Executive Reporting Templates** — COMPTON output structure
4. **kubectl/docker Command Reference** — SZILARD operational guidance

### P3 (Nice-to-Have — Trend Analysis & Edge Cases)
1. **Historical CVE Trends** — BOHR trend analysis
2. **Compliance Risk Mappings** (PCI-DSS, SOC2, HIPAA) — industry-specific context
3. **Zero-Day Threat Intelligence** — emerging threat visibility

---

## COVERAGE GAPS

### Gap 1: Environment-Specific Baseline Injection Mechanism
**Problem:** Library provides generic CIS baselines, but production environments often have justified deviations (e.g., SSH permits root for automation, WAF allows certain rules for legacy apps).

**Solution:** Define JSON injection format for per-environment baseline variations; SZILARD consumes base standard + environment overrides and flags justified deviations separately from compliance violations.

**Example:**
```json
{
  "environment": "production",
  "baseline_deviations_approved": [
    {
      "control_id": "CIS-5.2.1",
      "finding": "PermitRootLogin yes",
      "justification": "Required for ansible automation; MFA enforced",
      "approval": "CISO, 2026-04-01"
    }
  ]
}
```

### Gap 2: Business Context Injection Template
**Problem:** BOHR needs asset criticality, SLA targets, and budget constraints, but library lacks structured format.

**Solution:** Define YAML/JSON business context schema injected at assessment start; includes criticality tiers, SLA windows, compliance obligations, budget cap, risk appetite.

**Example:**
```yaml
business_context:
  asset_criticality:
    database-prod: TIER-1
    api-staging: TIER-3
  sla_requirements:
    CRITICAL: 24h patch window
    HIGH: 7d patch window
  compliance_obligations:
    - PCI-DSS (payment processing)
    - SOC2 (SaaS offering)
  budget_cap: $50,000 (remediation effort)
  risk_appetite: "low" (prefer defensive over cost-optimized)
```

### Gap 3: Transitive Dependency Risk Assessment Patterns
**Problem:** Library covers direct CVEs in services, but lacks guidance on supply-chain risk (compromised transitive deps, SBOM analysis, registry poisoning).

**Solution:** Add supply-chain threat model section; include Grype SBOM + CVE correlation walkthrough; define transitive dependency risk escalation rules.

### Gap 4: Exploit Prediction in Target Environment
**Problem:** CVSS + EPSS provide generic severity/exploitability, but don't assess feasibility in specific configuration context (e.g., CVE requires weak auth; target has MFA = lower risk).

**Solution:** Add "Exploitability Configuration Context" guide; include examples of how to elevate/reduce CVE risk based on baseline findings (isolated network segment, disabled service, compensating control).

### Gap 5: Effort Estimation Models
**Problem:** GROVES must estimate patch, config, and architecture effort, but library lacks empirical guidance beyond rough heuristics.

**Solution:** Build effort estimation matrix (asset type × remediation action → hours); calibrate via customer historical data; include variance assumptions.

**Example:**
| Asset Type | SSH Hardening | Docker Daemon | K8s RBAC | Effort Source |
|---|---|---|---|---|
| Linux VM | 0.5h | N/A | N/A | observed |
| Docker host | 0.5h | 1h | N/A | observed |
| K8s cluster | 0.5h | 1h | 40h | estimate |

### Gap 6: Attack-Chain Dependency Patterns
**Problem:** BOHR needs to identify configurations that enable multi-stage exploitation, but library lacks pre-built threat models.

**Solution:** Define common attack chains (e.g., unauth access → weak SSH auth → privilege escalation → persistence); BOHR uses these to elevate configuration-weakness multiplier when chain elements are detected.

### Gap 7: Post-Remediation Validation Acceptance Criteria
**Problem:** Library provides remediation actions but lacks clear success/failure criteria for validation.

**Solution:** Add validation script templates and acceptance criteria per remediation action; include rollback triggers.

---

## UPDATE FREQUENCY

| Collection | Frequency | Rationale | Owner |
|---|---|---|---|
| **NVD CVE Feed** | Daily | New CVEs published continuously; miss = blind spot | Library curator (automated) |
| **EPSS Data** | Daily | Exploitability probability evolves as exploits appear | Library curator (automated) |
| **Vendor Security Advisories** | Weekly | Advisory summaries; emergency expedite for CRITICAL | Library curator |
| **Exploit-DB/Metasploit Index** | Weekly | PoC maturity and weaponization updates | Library curator |
| **CIS Benchmarks** | Monthly or on-release | Policy updates, new controls | Library curator |
| **DISA STIGs** | Monthly or on-release | Policy/compliance updates | Library curator |
| **Tool Documentation** | On major version release | nmap, Trivy, kubectl, etc. | Library curator |
| **Ansible/Terraform Templates** | Monthly or per attack pattern | New hardening patterns, remediation best-practices | Library curator |
| **Reporting Templates** | As stakeholder needs change | Format/content feedback from COMPTON | Library curator |
| **Business Context (SLA, criticality)** | Per assessment cycle | Customer-injected; varies per engagement | Customer (injected at assessment start) |
| **Environment-Specific Baselines** | Per assessment cycle | Justified deviations per environment | Customer (injected at assessment start) |

---

## IMPLEMENTATION NOTES FOR LATTICE

1. **Daily CVE Feed Automation:** Configure NVD JSON feed + EPSS API polling to populate Library daily; version timestamped (e.g., `nvd-2026-04-30.json`); CHADWICK queries latest version.

2. **Injection Mechanism:** Define VRA vector for environment-specific baseline overrides (JSON) and business context (YAML); SZILARD + BOHR accept as configuration parameters at assessment start.

3. **Historical State Carryover:** Library includes prior assessment snapshots (ASSET_INVENTORY, VULNERABILITY_FINDINGS, RISK_MATRIX from prior cycles); enables delta analysis (new assets, remediated findings, regression detection).

4. **Effort Model Calibration:** Post-assessment, capture actual remediation effort (hours, complexity); accumulate in Library as empirical dataset; GROVES calibrates estimates against observed data over time.

5. **Dependency Graph Rendering:** GROVES references remediation action dependency patterns; Library includes Graphviz/Mermaid templates for rendering roadmap as DAG.

6. **Compliance Mapping Maintenance:** Maintain CIS ↔ NIST ↔ DISA ↔ PCI-DSS ↔ SOC2 ↔ HIPAA cross-reference matrix; SZILARD + COMPTON use for compliance-specific reporting.

---

**End OUTPUT B — Library Specification**

*Prepared for Lattice VRA implementation (swarm VRA ≥3, high domain volatility). Target length: ~2500 tokens. Document serves as procurement/design spec for Library content acquisition and refresh cadence.*

---

# LATTICE COLLECTION DESIGN

# LATTICE COLLECTION DESIGN: INFRASTRUCTURE SECURITY ASSESSMENT & HARDENING
*Phase 2b — T2 Library Specification → Lattice Collection Design*  
*For operator review and approval before fabrication*

---

## Assessment of Library Specification

The T2 Library Specification is **highly complete and actionable.** It provides explicit content types, update frequencies, agent dependencies, and 7 identified coverage gaps with proposed solutions. The spec is mature domain-expert work and requires minimal interpretation.

**Assumptions I filled in:**

1. **Collection granularity:** CIS/NIST baselines should be indexed at *control level* (not monolithic) to enable SZILARD to retrieve "CIS 5.2.1 SSH PermitRootLogin" for specific asset types without overfetch.

2. **Separation of static vs. dynamic knowledge:** CVE_INTELLIGENCE (daily refresh) and BASELINE_STANDARDS (monthly refresh) belong in separate collections due to radically different update cadences and query patterns.

3. **Business context injection:** Asset criticality tiers, SLAs, and risk appetite should be injected as **sidecar JSON config** (not vectorized), because they're customer-provided and environment-specific. Vectorizing high-cardinality, low-reuse data adds noise without retrieval benefit.

4. **Historical state:** Prior assessment snapshots (ASSET_INVENTORY, VULNERABILITY_FINDINGS) should remain as **sidecar markdown/JSON files** (git-versioned), not vectorized. If operator later requests trend analysis, vectorize then.

**Critical clarifications needed before collection fabrication:**

1. **CVE Feed Automation Strategy** — Should daily NVD/EPSS refresh use (a) scheduled batch upsert-by-CVE-ID, (b) subscription RSS polling, or (c) manual weekly batch?

2. **Business Context Ownership** — Who supplies environment-specific criticality tiers and SLAs — operator, customer, or derived from discovery? Inject as sidecar or vector query?

3. **Environment Baseline Deviations** — Should justified deviations (e.g., "SSH permits root in dev") be stored as metadata tags on BASELINE_STANDARDS entries, or as separate collection?

4. **Collection Access Control** — Should TELLER/MEITNER (reconnaissance agents) be blocked from CVE_INTELLIGENCE for information compartmentalization, or have read-only access?

5. **Remediation Template Secrets** — How should credentials in playbooks be handled? Templated (e.g., `{{ vault_ssh_key }}`), externalized to secrets manager, or hardcoded with placeholder comments?

6. **P2/P3 Content** — Should Phase 2b include Effort Estimation Matrices and Compliance Risk Mappings (P2), or defer to Phase 2c tuning?

---

## Collection Architecture

### **BASELINE_STANDARDS**
**Purpose:** Authoritative security baseline controls (CIS, NIST, DISA) for SZILARD to map configuration deviations.

**Source of truth:** T2 Library Specification, Collection 1

**Content type:** Mixed (Markdown control definitions + JSON cross-index)

**Chunking strategy:** Control-level (each CIS control, NIST control family, or DISA STIG control = one document with metadata prefix). Enables SZILARD to retrieve "CIS 5.2.1 SSH PermitRootLogin for RHEL8" without overfetch.

**Embedding model:** **CySecBERT** — security terminology ("privilege escalation," "RBAC," "least-privilege") is domain-specific.

**Ingest sources:** CIS Benchmarks (PDF/YAML, licensed), NIST 800-53 Rev 5 (XML/JSON), DISA STIGs (public XML), manual compliance mappings (PCI-DSS ↔ CIS, HIPAA ↔ NIST, SOC2 ↔ CIS).

**Refresh cadence:** Monthly or on-release (CIS/DISA issue 2–4 updates/year; NIST infrequent).

**Mandatory metadata fields:** `framework` (CIS|NIST|DISA), `standard_version`, `control_id`, `asset_type` (Docker|Kubernetes|Linux|Windows), `severity` (CRITICAL|HIGH|MEDIUM), `source_type`, `engagement_id`, `chunk_index`, `status` (active|demoted|removed), `last_refreshed`

**Estimated size:** 800–1200 control documents (CIS Docker ~200, CIS K8s ~150, CIS Linux ~250, NIST ~300, DISA STIGs ~100–150).

---

### **CVE_INTELLIGENCE**
**Purpose:** Dynamic CVE/exploit intelligence for CHADWICK to correlate service versions to vulnerabilities.

**Source of truth:** T2 Library Specification, Collection 2

**Content type:** Structured (JSON-serialized CVE records with CVSS/EPSS/PoC metadata).

**Chunking strategy:** CVE-level (one CVE document per CVE-XXXX-XXXXX with affected versions, CVSS vector, EPSS score, PoC maturity). Enables precise "find CVEs in Apache 2.4.x" queries.

**Embedding model:** **CySecBERT** — CVE descriptions and vendor/product terminology are security-domain-specific.

**Ingest sources:** 
- NVD JSON feeds (nvd.nist.gov; daily batch)
- EPSS API (epss.cyentia.org; daily)
- Vendor advisories (Apache, nginx, Kubernetes, Docker, OpenSSL; weekly scrape)
- Exploit-DB metadata + GitHub CVE advisory index (weekly)
- Metasploit module index (weekly)

**Refresh cadence:** **Daily** (NVD + EPSS upsert-by-CVE-ID); **weekly** (PoC status, advisories append-only).

**Mandatory metadata fields:** `cve_id`, `cvss_base_score`, `cvss_vector`, `epss_score`, `epss_percentile`, `poc_status` (none|academic|weaponized|active_exploitation), `patch_available`, `vendor`, `product`, `affected_versions` (JSON), `advisory_url`, `source_type`, `engagement_id`, `chunk_index`, `status`, `last_refreshed`

**Estimated size:** 50k–100k CVE documents (active/recent subset of NVD's 230k+ historical CVEs).

---

### **TOOL_DOCUMENTATION**
**Purpose:** Operational command reference for enumeration, fingerprinting, config retrieval, and vulnerability scanning.

**Source of truth:** T2 Library Specification, Collection 3

**Content type:** Markdown with code examples, command signatures, output formats, heuristics.

**Chunking strategy:** Section-level (each tool + task = one document; e.g., "nmap OS fingerprinting," "docker inspect HostConfig," "kubectl network policy retrieval"). Keeps task families cohesive.

**Embedding model:** **all-mpnet-base-v2** — technical documentation with general Linux/cloud jargon, not security-specialized.

**Ingest sources:** Upstream tool docs (nmap, masscan, Kubernetes, Docker, Trivy, Grype), man pages, manual curation of common recipes.

**Refresh cadence:** On major tool version release (nmap 7.91 → 7.92, Trivy 0.35 → 0.36).

**Mandatory metadata fields:** `tool_name`, `tool_version`, `command_category` (enumeration|fingerprinting|configuration_retrieval|validation), `asset_type`, `source_type`, `engagement_id`, `chunk_index`, `status`, `last_refreshed`

**Estimated size:** 80–120 tool-section documents (15–20 tools × 4–8 sections each).

---

### **HARDENING_GUIDES**
**Purpose:** Configuration hardening reference for SZILARD baseline definition and GROVES remediation strategy.

**Source of truth:** T2 Library Specification, Collection 4

**Content type:** Mixed (example configs in YAML/INI + Markdown narrative with CIS/NIST mappings).

**Chunking strategy:** Service-level (each service/OS = one document; e.g., "SSH hardening," "Docker daemon.json," "Kubernetes RBAC," "Linux sysctl hardening"). Balances coherence with specificity.

**Embedding model:** **CySecBERT** — hardening terminology ("privilege escalation," "RBAC," "least-privilege").

**Ingest sources:** CIS hardening sections (extracted), vendor guides (Red Hat, Canonical, Docker, CNCF), NIST 800-53 implementation, manual curation.

**Refresh cadence:** Monthly or per attack pattern (new SSH cipher weakness → update SSH section).

**Mandatory metadata fields:** `service_type` (SSH|Docker|Kubernetes|Linux|TLS|Firewall), `os_version`, `cis_control_id`, `severity`, `automation_feasible` (true|false), `source_type`, `engagement_id`, `chunk_index`, `status`, `last_refreshed`

**Estimated size:** 60–100 hardening-guide documents (10–15 services × 4–6 OS variants + network/firewall/TLS).

---

### **RISK_CONTEXT**
**Purpose:** Risk scoring methodology, business context templates, and exploitability heuristics for BOHR.

**Source of truth:** T2 Library Specification, Collection 5

**Content type:** Mixed (Markdown methodology + JSON/YAML business context templates).

**Chunking strategy:** Section-level (CVSS v3.1 guide, EPSS interpretation, config-weakness multipliers, criticality tier definitions, SLA template, composite risk formula, attack-chain patterns). Each section standalone.

**Embedding model:** **CySecBERT** — risk and attack terminology specific to security domain.

**Ingest sources:** CVSS v3.1 spec (NIST/FIRST), EPSS methodology (Cyentia), NIST 800-53 risk guidance, manual curation of business context templates.

**Refresh cadence:** Methodology (CVSS/EPSS) on spec update (rare); business context templates per assessment cycle (operator/customer-injected).

**Mandatory metadata fields:** `context_type` (methodology|formula|heuristic|template), `applicable_to_agents` (BOHR|GROVES), `business_context_key`, `source_type`, `engagement_id`, `chunk_index`, `status`, `last_refreshed`

**Estimated size:** 25–40 documents (5–6 methodology sections + 3–4 business context templates + heuristic guides).

---

### **REMEDIATION_STRATEGIES**
**Purpose:** Remediation action templates, IaC code, effort estimation, and success criteria for GROVES and COMPTON.

**Source of truth:** T2 Library Specification, Collection 6

**Content type:** Mixed (Ansible YAML, Terraform HCL, Bash scripts + Markdown context/validation).

**Chunking strategy:** Playbook-level (each Ansible playbook, Terraform module, or hardening script = one document with metadata prefix and success criteria).

**Embedding model:** **all-MiniLM-L6-v2** — IaC code structure (YAML/HCL/Bash) is general syntax; lighter model improves code-snippet retrieval.

**Ingest sources:** Manual curation, Ansible Galaxy (vetted subset), Terraform Registry (vetted subset), vendor-provided IaC, prior assessment iterations.

**Refresh cadence:** Monthly (new hardening patterns), immediately on new attack pattern (e.g., SSH cipher weakness → release SSH hardening playbook update).

**Mandatory metadata fields:** `remediation_type` (patch|config|architecture|rbac|encryption), `asset_type` (linux_vm|docker_host|kubernetes_cluster), `affected_finding_type`, `effort_hours_low`, `effort_hours_high`, `quick_win_eligible` (true|false), `success_criteria`, `rollback_procedure`, `source_type`, `engagement_id`, `chunk_index`, `status`, `last_refreshed`

**Estimated size:** 120–180 remediation templates (30–40 patterns × 3–4 asset types + IaC variants).

---

### **REPORTING_TEMPLATES**
**Purpose:** Output format and narrative structure for COMPTON to produce executive summaries, findings reports, and playbooks.

**Source of truth:** T2 Library Specification, Collection 7

**Content type:** Markdown + JSON templates (narrative structure, table schemas, no code).

**Chunking strategy:** Template-level (each report type = one document; e.g., "Executive Summary," "Technical Findings," "Remediation Roadmap," "CVE Deep-Dive").

**Embedding model:** **all-mpnet-base-v2** — reporting structure is general writing convention, not security-specialized.

**Ingest sources:** Manual curation from COMPTON stakeholder feedback, prior assessment examples, executive communication best-practices.

**Refresh cadence:** As stakeholder reporting needs change (quarterly or per feedback).

**Mandatory metadata fields:** `audience` (executive|technical|manager|compliance), `report_type` (summary|findings|roadmap|playbook), `output_format` (PDF|Markdown|JSON), `required_inputs` (list of coordination files), `source_type`, `engagement_id`, `chunk_index`, `status`, `last_refreshed`

**Estimated size:** 20–30 reporting templates (4–5 report types × 4–6 variants for audience/format).

---

## Implementation Notes

**1. CVE Feed Automation (CRITICAL PATH)**

NVD and EPSS daily refresh is non-negotiable dependency for CHADWICK. Implement as:

- **Scheduled batch (daily, UTC 2 AM):** Call NVD bulk API + EPSS score API; deduplicate on CVE ID; **upsert** (not append) to CVE_INTELLIGENCE. Overwrites stale EPSS/PoC metadata.
- **Versioning:** Embed `nvd_feed_date` and `epss_snapshot_date` in metadata; CHADWICK queries filter latest snapshot.
- **Fallback:** If daily ingest fails, retain 7-day snapshot; agents default to day-old data and alert operator.

**2. Business Context Injection (SIDECAR, NOT VECTORIZED)**

Environment-specific criticality tiers, SLAs, and risk appetite are high-cardinality, low-reuse data. **Recommendation:** Inject as JSON sidecar file (`business_context.json`); BOHR reads at assessment start. Avoids embedding overhead without retrieval benefit.

**3. Environment Baseline Deviations (METADATA-TAGGED)**

Justified deviations (e.g., "SSH permits root in dev; approved by CISO") should be stored as metadata on BASELINE_STANDARDS entries: `approved_deviations: [{control_id, justification, approval_date, approval_authority}]`. SZILARD queries return both standard + approved deviations; flags as "APPROVED DEVIATION" or "COMPLIANCE VIOLATION."

**4. Historical State (SIDECAR FILES, NOT VECTORIZED)**

ASSET_INVENTORY, VULNERABILITY_FINDINGS, and ASSESSMENT_STATE remain as git-versioned markdown/JSON sidecar files. If operator requests historical trend analysis later (e.g., "CVEs remediated in last 90 days"), vectorize assessment snapshots then.

**5. Collection Interdependencies (VRP Routing)**

Dependency graph for agent queries:

```
TELLER (BASELINE_STANDARDS for tier defs) → ASSET_INVENTORY
  ↓
MEITNER (TOOL_DOCUMENTATION for commands) → SERVICE_MANIFEST
  ↓
SZILARD (BASELINE_STANDARDS, HARDENING_GUIDES) ↔ CHADWICK (CVE_INTELLIGENCE)
  ↓ ↓
BOHR (RISK_CONTEXT, BASELINE_STANDARDS context) → RISK_MATRIX
  ↓
GROVES (REMEDIATION_STRATEGIES, RISK_CONTEXT effort models) → REMEDIATION_ROADMAP
  ↓
COMPTON (REPORTING_TEMPLATES + all coordination files) → Reports
```

**6. Coverage Gap Content (DEFERRED POST-PHASE-2b)**

Library Spec identifies these gaps but provides no full content:
- Transitive dependency risk assessment patterns
- Attack-chain threat models
- Exploit prediction in target environment (config context)

**Action:** Create placeholder collections (empty); request SZILARD + BOHR author in post-Phase-2b tuning if needed. These are specialized expertise areas.

**7. OPSEC: Collection Access Control (RECOMMENDATION)**

- **CVE_INTELLIGENCE:** Restrict to CHADWICK, BOHR, GROVES, COMPTON (not TELLER/MEITNER). Asset discovery agents don't need CVE data; compartmentalization reduces blast radius if collection compromised.
- **Business Context (Sidecar):** Operator-controlled storage, not vector collection.
- **Remediation_STRATEGIES:** Ensure playbook templates use secret-injection (Ansible vault, Terraform vars), never hardcoded credentials.

---

## Questions for Operator

**Before Fermi embeds VRPs, confirm:**

1. **CVE daily refresh:** Automated upsert-by-CVE-ID, or manual weekly batch?

2. **Business context source:** Operator-provided, customer-provided, or derived from discovery? Sidecar JSON or vector query?

3. **Historical trend analysis:** Required for future phases, or current-state reporting only?

4. **Baseline deviation workflow:** Pre-load into metadata, or flag for manual operator approval?

5. **Remediation template secrets:** Vault-templated, externalized to secrets manager, or operator fill-in?

6. **P2 content scope:** Include Effort Estimation Matrices + Compliance Risk Mappings in Phase 2b, or defer to Phase 2c?

7. **CVE_INTELLIGENCE access control:** Compartmentalize from TELLER/MEITNER (recommended), or grant read-only access?

---

## Vector Retrieval Protocol Skeleton

**VRP embeds in agent prompts; agents do NOT call ChromaDB directly (Fermi pre-fetches and injects).**

---

#### **TELLER** — Asset Discovery & Inventory
- **Collections:** BASELINE_STANDARDS (criticality tier definitions), TOOL_DOCUMENTATION (enumeration commands)
- **Query trigger:** Task start (ASSESS command)
- **Query formulation:** `criticality tier definitions` + `network enumeration nmap masscan IPv6` → retrieves classification schema + command reference
- **Injection point:** Prepend before task (system prompt)
- **Citation format:** ASSET_INVENTORY.md integrates tier definitions without explicit citations (reference definitions, not evidence)
- **Fallback (MANDATORY):** If unavailable, default to NIST standard tier definitions (TIER-1=DC, TIER-2=app, TIER-3=dev, TIER-4=unknown); use default nmap templates (no advanced options; slower scan)

---

#### **MEITNER** — Service Fingerprinting & Version Detection
- **Collections:** TOOL_DOCUMENTATION (fingerprinting), CVE_INTELLIGENCE (optional, learning context only)
- **Query trigger:** After TELLER completes ASSET_INVENTORY
- **Query formulation:** `SSH TLS banner extraction version detection nmap httpx curl` + optional `OpenSSH Apache nginx common versions CVEs` (learning context)
- **Injection point:** Prepend tool reference before task
- **Citation format:** SERVICE_MANIFEST.md includes command examples (e.g., "version detected via: nmap -sV --script banner") but does not cite collection explicitly
- **Fallback (MANDATORY):** If TOOL_DOCUMENTATION unavailable, default to `nmap -sV --script banner` and manual curl/ssh -v; if CVE_INTELLIGENCE unavailable, proceed with fingerprinting regardless

---

#### **SZILARD** — Configuration Baseline Reviewer
- **Collections:** BASELINE_STANDARDS (primary), HARDENING_GUIDES (primary), environment-injected baseline deviations (metadata)
- **Query trigger:** After TELLER + MEITNER complete
- **Query formulation:** `CIS 5.2.1 PermitRootLogin SSH hardening Linux RHEL8` + `Docker daemon.json CIS 2.1–2.18` + `Kubernetes RBAC network policy` + environment deviations (from sidecar JSON, not vector)
- **Injection point:** Prepend baseline standards before task
- **Citation format:** BASELINE_ASSESSMENT.md cites control source: `[CIS-5.2.1 from BASELINE_STANDARDS collection, CIS Docker v1.12.0]`
- **Fallback (MANDATORY):** If BASELINE_STANDARDS unavailable, use memory-stored CIS definitions (reduced depth, missed cross-references); if HARDENING_GUIDES unavailable, use generic configuration expectations (less precise); if environment deviations unavailable, flag all deviations as "COMPLIANCE VIOLATION" (may include false positives)

---

#### **CHADWICK** — Vulnerability & CVE Correlator
- **Collections:** CVE_INTELLIGENCE (primary), TOOL_DOCUMENTATION (optional, container scanning reference)
- **Query trigger:** After SERVICE_MANIFEST.md available
- **Query formulation:** `CVE Apache 2.4.41 CVSS EPSS affected_versions` → retrieve all matching CVEs; then per-CVE: `CVE-2023-XXXXX EPSS score exploitation PoC weaponized`
- **Injection point:** Inline at query time (iterate SERVICE_MANIFEST entries; submit per {software, version} and inline results)
- **Citation format:** VULNERABILITY_FINDINGS.md cites: `[CVE-2023-XXXXX: CVSS 8.2 (vector ...) from NVD, EPSS 0.87 from EPSS Data Feed, PoC available in Exploit-DB]`
- **Fallback (MANDATORY):** If CVE_INTELLIGENCE unavailable or < 3 results per service/version, fallback to NVD API directly (if operator provides key); if both unavailable, issue warning "CVE correlation incomplete; confidence: LOW" and proceed with service/version alone

---

#### **BOHR** — Risk Scoring & Prioritization Engine
- **Collections:** RISK_CONTEXT (primary), BASELINE_STANDARDS (secondary, control context), CVE_INTELLIGENCE (secondary, exploitability context)
- **Query trigger:** After CHADWICK + SZILARD complete
- **Query formulation:** `CVSS v3.1 vector interpretation` + `EPSS exploitation probability thresholds` + `configuration weakness multiplier attack-chain` + `business context criticality tier SLA patch window` (from sidecar or vector) + optional `attack-chain threat models`
- **Injection point:** Prepend methodology before task; inject business context (sidecar or vector) before risk synthesis
- **Citation format:** RISK_MATRIX.md justifies score: `[Composite Risk = CVSS 8.2 × EPSS 0.87 × config_multiplier 1.5 (SSH root + weak auth + no isolation) × criticality_weight 4.0 (TIER-1 DB) = 43.3; CRITICAL]`
- **Fallback (MANDATORY):** If RISK_CONTEXT unavailable, default to `risk = CVSS × EPSS` (no config/criticality weights); if business context unavailable, default all to TIER-2 + 30d patch window; issue warning "Business context not provided; risk scores may not reflect organizational priorities"

---

#### **GROVES** — Remediation Guidance & Hardening Strategist
- **Collections:** REMEDIATION_STRATEGIES (primary), RISK_CONTEXT (effort models), HARDENING_GUIDES (config guidance)
- **Query trigger:** After BOHR produces RISK_MATRIX (HARDEN command)
- **Query formulation:** `SSH weak cipher hardening remediation playbook sshd_config` + `effort estimate hours patch Linux kernel` + `quick-win checklist < 4 hours config-only` + `dependency graph blockers` + `success criteria validation post-remediation`
- **Injection point:** Prepend remediation library before task
- **Citation format:** REMEDIATION_ROADMAP.md cites: `[Finding: CVE-2023-XXXXX; Remediation: SSH hardening playbook from REMEDIATION_STRATEGIES; Effort: 1h (empirical); Quick-win: YES; Success: sshd -T output matches CIS 5.2.x]`
- **Fallback (MANDATORY):** If REMEDIATION_STRATEGIES unavailable, generate generic guidance: "Patch [software] to [version] (effort unknown; ~2–4h)" without playbook; if effort models unavailable, default 4h per finding; issue warning "Remediation templates not available; estimates only, not deployment-ready code"

---

#### **COMPTON** — Report Generation & Stakeholder Communication
- **Collections:** REPORTING_TEMPLATES (primary)
- **Query trigger:** After GROVES produces REMEDIATION_ROADMAP (REPORT command)
- **Query formulation:** `executive summary template 1-pager risk distribution pie chart` + `risk heatmap visualization asset × risk tier` + `technical findings report asset-indexed evidence` + `CVE deep-dive template` + `remediation roadmap Gantt template`
- **Injection point:** Prepend templates before task
- **Citation format:** Reports include attribution: `[Data: ASSET_INVENTORY (TELLER), VULNERABILITY_FINDINGS (CHADWICK), BASELINE_ASSESSMENT (SZILARD), RISK_MATRIX (BOHR), REMEDIATION_ROADMAP (GROVES)]; findings cite source: CVE-2023-XXXXX per NVD, CIS-5.2.1 per BASELINE_STANDARDS`
- **Fallback (MANDATORY):** If REPORTING_TEMPLATES unavailable, produce plain-text reports (bulleted executive summary, tab-separated findings table, markdown task list); remain actionable but lack polish; issue warning "Report templates not available; output in minimal format"

---

**End LATTICE COLLECTION DESIGN**

---

# CURIE RESEARCH BRIEFING

# CURIE RESEARCH BRIEFING — TELLER
*Research Specialist — Fabrication pre-research*

---

## Terminology Map

| Term | Definition | Distinction |
|------|-----------|-------------|
| **Asset** | Any network-connected device with an IP address (VM, container, appliance, load balancer, firewall, IoT). | Distinguished from *service* (software listening on a port) and *container image* (inactive code). One asset may host multiple services. |
| **Criticality tier** | Classification: TIER-1 (databases, domain controllers, payment systems; 4.0× risk weight), TIER-2 (app servers, internal services; 2.0×), TIER-3 (dev/staging; 1.0×), TIER-4 (unknown/unclassified; 0.5×). | Drives downstream risk amplification in BOHR's synthesis. A moderate CVE on TIER-1 becomes CRITICAL. Default to TIER-1 if ownership/function unclear; confirm with stakeholder. |
| **Enumeration** | Active network scanning (sending probes, receiving responses) to discover assets. | Distinguished from *passive* (listening to traffic without probes; slower, incomplete). nmap/masscan are active; ARP monitoring is passive. |
| **Open port** | TCP or UDP port in LISTEN state on a scanned host. | TELLER reports {IP, port, protocol, tentative_service_name_via_IANA} but does NOT fingerprint versions (MEITNER's role). |
| **OS fingerprinting** | Inferring operating system from TTL values, TCP window size, ICMP behavior, SMB probes. Probabilistic. | Cross-validate with ports (445/3389 → Windows, 22 → Linux) and service banners. Unreliable alone; treat as weak evidence. |
| **Deduplication** | Reconciling identical assets discovered under different identifiers (hostname, IP, MAC) into single inventory entry. | MAC address is most stable anchor; IP/hostname secondary. Flag conflicts (same MAC, multiple IPs) as "CONFLICT: IP_CHURN." |

---

## Foundational Knowledge

**Asset inventory is the dependency critical path.** All downstream agents (MEITNER, SZILARD, CHADWICK, BOHR, GROVES, COMPTON) depend on ASSET_INVENTORY.md as source of truth. A missed asset = missed CVEs = zero remediation = compliance violation. Prioritize completeness and accuracy over scanning speed.

**Criticality tier assignment drives organizational risk synthesis.** TIER-1 assets receive 4× risk amplification; a CVSS 6.5 on a database becomes organizational CRITICAL. TELLER must understand business context: which databases are payment-critical, which app servers are revenue-facing. If unclear, default to TIER-1 (conservative) and flag stakeholder for confirmation post-scan.

**Network segmentation creates enumeration blindness.** Your scan vector may lack access to isolated networks (production enclaves, air-gapped OT, VPN-only subnets). Enumerate scannable networks explicitly; document inaccessible segments as "NETWORK_UNREACHABLE; reason: [firewall | routing gap | OT isolation]." Incomplete enumeration better than false negatives.

**TTL fingerprinting fails silently in cloud/containerized environments.** Firewalls rewrite TTL; VMs use non-standard stacks; cloud providers may report misleading TTL values. Treat TTL as weak evidence only. Cross-validate with SMB probes (Windows markers), SSH banner (Linux markers), HTTP headers, ICMP error patterns, or fall back to port-based heuristics.

**Asset metadata completeness cascades to downstream decisions.** ASSET_INVENTORY must include: hostname, IP (IPv4/IPv6), OS, open port list (not versions), criticality tier, owner contact, workload type (VM|container host|appliance), last scan date. Missing metadata (owner=unknown, tier=undetermined) blocks SZILARD baseline assignment, BOHR risk weighting, COMPTON remediation routing.

---

## Applied Knowledge: Patterns and Practices

**Scanning tempo by environment:**

| Scenario | Command | Runtime | Notes |
|---|---|---|---|
| **Fast discovery** (many targets, IDS tolerance high) | `masscan -p0-65535 --max-rate 10000 [CIDR] -oG output.gnmap` | 30s–2m per /24 | Rapid enumeration; ~5% miss rate acceptable; rescan with nmap on second pass for TIER-1. |
| **Careful production scan** (TIER-1 assets, IDS avoidance) | `nmap -sS -p 22,80,443,3306,5432,389 -T3 --max-rtt-timeout 500 [target]` | 30m–2h per /24 | Stealth syn scan, common ports only, conservative timing; avoids reactive firewalls. |
| **Full reconnaissance** (single asset, deep dive) | `nmap -sV -sC -O --script vuln -T4 [IP]` | 5–15m per asset | Banner extraction, default-credential probes, OS detection; output feeds MEITNER and SZILARD directly. |
| **Kubernetes/container enumeration** | `nmap -p 6443,10250,10252 [node_IPs] && kubectl get nodes -o wide` | 5m–30m cluster | Enumerate kubelet ports and node addresses; complement with kubectl API queries. Enumerate **nodes** (persistent), not pods (ephemeral). |

**Asset metadata extraction workflow:**

1. **Hostname resolution:** `nmap -sL [CIDR] | grep "Nmap scan report"` or `dig -x [IP]` for reverse DNS. Default to IP if no PTR record (common in cloud/ephemeral infrastructure).

2. **OS detection decision tree:**
   - Port 445 open + SMB response + TTL ≈128 → **Windows** (HIGH confidence)
   - Port 22 open + SSH banner → **Linux** (HIGH confidence)
   - Port 3306 or 5432 open + no other hints → infer from nmap -O output; default to **Linux**
   - No definitive signals → tag as "OS: UNKNOWN" + defer to MEITNER fingerprinting

3. **Criticality tier assignment:**
   ```
   IF hostname matches regex (domain|dc|sql|db|postgres|mysql|payment|auth) → TIER-1
   ELSE IF asset runs web service AND listens on public IP → TIER-2
   ELSE IF hostname contains "dev|staging|test" OR private RFC1918 IP → TIER-3
   ELSE → TIER-4 (flag for stakeholder confirmation)
   ```

4. **Owner identification:** Parse hostname segments (owner-appname), cloud provider tags (AWS Name tag, GCP label), AD WHOIS, DNS delegation. If unknown → escalate as "owner: UNCONFIRMED; requires_stakeholder_confirmation."

**Deduplication and conflict resolution:**

- **Index by MAC address** (most stable across reboots/IP churn).
- **Group by {hostname, IP}** (secondary anchor).
- **Conflict detection:** Same MAC, multiple IPs = network misconfiguration or DHCP churn. Mark as `status: IP_CHURN; last_seen_IP: X.X.X.X; flag_for_network_review`.
- **Merge strategy:** One ASSET_INVENTORY entry per MAC; most recent scan timestamp wins (IP/hostname override prior). Record all {IP, hostname} pairs observed.

**Scope boundary handling:**

- **Out-of-scope discovery:** Find assets outside operator-defined CIDR (e.g., VPN concentrators, federated cloud projects)? Tag as `scope: OUT_OF_SCOPE_BUT_DISCOVERED` and flag stakeholder for inclusion/exclusion decision. Do not discard; document reasoning.
- **Unreachable assets:** Host down, network inaccessible, firewall-blocked? Log as `status: UNREACHABLE; reason: [ICMP_unreachable | RST | timeout]; scan_source: [IP]`. Include in inventory but mark status; do not omit.
- **Partial network visibility:** If target is /16 and scan source has access to only 3 subnets, enumerate those fully and document inaccessible segments with reason (routing, firewall rules, provider VPC restrictions).

---

## Decision Heuristics

**masscan vs. nmap tradeoff:**
- **masscan** if target ≥ /16, high bandwidth tolerance, false-positive cost acceptable. Rescan with nmap on second pass for validation.
- **nmap** if target ≤ /24, false negatives unacceptable (TIER-1 scope), or detection-avoidance required (IDS sensitivity).

**Tier escalation trigger:**
- Asset contains PCI-DSS scope (payment card data) → TIER-1 unless explicitly non-production.
- Asset in MEITNER finding: "SSH root login enabled" → escalate tier (e.g., TIER-3 → TIER-2).
- Asset port = high-value service (3306, 5432, 27017) AND owner unknown → TIER-1 until proven else.

**Re-scan trigger:**
- Prior scan > 7 days old (asset churn in cloud/container environments).
- MEITNER/SZILARD report inconsistency (port status changed, OS mismatch).
- New vulnerability CVE reported on service version; rescan to confirm presence.

**Completeness signal:**
- Asset count stabilizes across 3 consecutive scans (no new discoveries) = enumeration converged.
- Response rate > 80% across target CIDR (acceptable for production; < 50% signals access issues).

---

## Common Failure Modes

| Failure Mode | Signal | Corrective Action |
|---|---|---|
| **False negatives (missed assets)** | MEITNER/SZILARD discovers host in logs/configs not in inventory | Rescan iteratively; integrate passive sources (ARP logs, DNS queries, netflow); interview stakeholders for "assets we know exist." |
| **Incorrect OS assignment** | MEITNER: "Windows service on Linux-classified host" | Correct retroactively; flag SZILARD baseline mismatch; investigate if OS genuinely changed or detection error. |
| **Tier misclassification** | Post-assessment: "That TIER-3 host runs payment auth" | Recalculate BOHR risk scores for that asset; escalate any moderate/high findings to CRITICAL. Document tier definition gaps; pre-load stakeholder tier map next cycle. |
| **Scope creep** | Enumeration discovers assets exponentially (new subnets, federated projects, branch offices); inventory unbounded | Halt scan; confirm scope boundary with operator. Separate "in-scope" from "discovered-out-of-scope." Re-prioritize if scope expands. |
| **Deduplication failure** | Same asset appears twice in inventory under different IPs | Merge by MAC address; keep record of all observed IPs; flag conflict for network team investigation. |
| **TTL detection failures** | Asset returns inconsistent TTL (sometimes resets, sometimes doesn't) | Tag as "OS: UNDETERMINED"; use port-based heuristics (445 → Windows, 22 → Linux); escalate to MEITNER for banner fingerprinting. |
| **Network segmentation blindness** | Later discovery: "Entire production segment was unreachable from scan source" | Document access limitation in ASSESSMENT_STATE; request alternative scan vector or direct asset list from stakeholder; re-run from permitted network. |

---

## Current Landscape Notes

**Cloud enumeration differs fundamentally from on-prem.** Cloud providers filter ICMP (nmap -sP ineffective); TTL unreliable; auto-scaling creates ephemeral assets. **Primary enumeration via cloud provider APIs** (aws ec2 describe-instances, gcloud compute instances list, az vm list); validate with nmap as secondary. Document API calls in inventory metadata; enables future deltas.

**Container and Kubernetes inventory is ephemeral.** Pods restart hourly; ASSET_INVENTORY snapshot is point-in-time only. **Enumerate Kubernetes nodes** (persistent VMs), not pods. MEITNER and SZILARD assess pod specs and running-pod vulnerability separately. Tag workload_type: kubernetes_node or container_host in inventory.

**nmap 7.92+ format changes.** `-sV` output restructured; SMB probes deprecated (use dedicated `smb-os-discovery` script). Verify tool version in TOOL_DOCUMENTATION matches your nmap binary; flag operator if versions diverge (e.g., legacy nmap 7.80 vs. current 7.94).

**IPv6 enumeration is systematically skipped.** Add `-6` flag to nmap; document IPv4 AND IPv6 in inventory. Most orgs ignore IPv6 vulns; flag completeness gap to BOHR for risk context.

**Passive recon sources (Shodan, Censys, GitHub) reveal unknown assets.** Cross-reference findings against inventory; add in-scope confirmed assets. Document source (Shodan query, GitHub secret scan, leaked git repo). These often surface misconfigured/exposed infrastructure operator doesn't realize is public.

**Cloud-native workloads (serverless, managed databases):** Enumerate via provider consoles/APIs, not network scans. RDS, DynamoDB, Lambda have no scannable IP; document as managed service in ASSET_INVENTORY with provider account/region metadata.

---

**End CURIE RESEARCH BRIEFING — TELLER**

---

# FABRICATED AGENT PROMPT

# TELLER — Asset Discovery & Inventory

## Identity and Role

TELLER is the dependency critical-path agent for infrastructure security assessment. Mission: execute active network enumeration (nmap TCP/UDP SYN scans, ICMP sweeps, masscan for speed), catalog all network-connected assets with complete metadata (hostname, IPv4/IPv6, OS via TTL/SMB/SSH fingerprinting, open port list, criticality tier, owner contact, last scanned), and maintain authoritative **ASSET_INVENTORY.md** as single source of truth for all downstream agents (MEITNER, SZILARD, CHADWICK, BOHR, GROVES, COMPTON). TELLER explicitly does NOT fingerprint software versions (MEITNER), correlate CVEs (CHADWICK), assess baseline compliance (SZILARD), or score risk (BOHR). Authority: scans operator-approved CIDR ranges only; escalates scope boundary questions and unreachable segments to operator before proceeding. Scope compliance is non-negotiable—all downstream agents depend on accurate, complete asset enumeration. Missing assets create blind spots in vulnerability coverage and failed remediation.

## Expertise Profile

TELLER is a network enumeration specialist with deep expertise in asset discovery methodology, infrastructure visibility patterns, and OS fingerprinting heuristics across cloud, containerized, and on-premises environments.

**Active Enumeration and Tool Selection:**
- **Masscan vs. nmap tradeoff:** Masscan (max-rate 5000+ for rapid /16–/8 discovery) acceptable for initial enumeration when false-positive rate ~5% is tolerable; rescan with nmap on second pass to validate and eliminate duplicates. Nmap for targeted validation and OS detection on smaller scopes (≤/24) or production TIER-1 assets where accuracy critical. TCP SYN scans (-sS) preferred over full connect (-sT) for stealth; ICMP sweeps (-sP) faster for reachability but may be firewalled entirely.
- **Timing and IDS avoidance:** nmap -T3 (conservative timing, max-rtt-timeout 500ms) on production networks to avoid triggering reactive firewalls; -T4 acceptable on isolated/lab environments. Production networks require slower, less aggressive scanning; TIER-1 asset scans should complete without security team alerts.

**OS Fingerprinting and Cross-Validation:**
- **Weak signal recognition and validation:** TTL fingerprinting (Linux ~64, Windows ~128) is probabilistic and cloud-unreliable (firewalls rewrite TTL; cloud providers report inconsistent values). Never assume OS from TTL alone. **Cross-validate with secondary markers:** port 445 open + SMB service response → Windows (HIGH confidence); port 22 + SSH banner present → Linux (HIGH confidence). nmap -O output is structured guess only; treat as tertiary signal.
- **Port-based heuristics when fingerprinting fails:** Port 3306 or 5432 + no SMB/SSH → infer Linux (database default). Port 3389 RDP + no SSH → Windows. Default to "OS: UNKNOWN" if signals conflict; escalate to MEITNER for banner confirmation or flag for operator clarification.
- **Cloud and container environment gotchas:** Firewall ICMP rewriting breaks TTL; VMs use non-standard stacks; cloud providers mask or spoof TTL. Compensate by relying entirely on port-service correlations and explicit banner extraction (MEITNER's domain). Do not report OS until cross-validated.

**Asset Metadata Capture and Deduplication Workflow:**
- **Inventory schema:** For every discovered asset: hostname (DNS reverse lookup via `dig -x [IP]`; default to IP if no PTR record), IPv4 + IPv6 (if applicable), CIDR membership, OS (Windows|Linux|macOS|Unknown), open_port_list (no version strings; port numbers + IANA service name heuristic only), criticality_tier (TIER-1/2/3/4 assigned via decision tree), owner_contact (parsed from hostname regex, cloud provider tags, AD WHOIS; or "UNCONFIRMED"), workload_type (VM|container_host|appliance|Kubernetes_node|serverless), last_scanned_timestamp.
- **Deduplication anchor and conflict resolution:** MAC address is most stable anchor across reboots and IP churn. Group by {hostname, IP} secondary. Detect same-MAC-multiple-IPs pattern → tag as "status: IP_CHURN" and flag for network team investigation (DHCP misconfiguration, network failover, device instability). Merge entries: one ASSET_INVENTORY row per MAC; record all observed {IP, hostname} pairs in comment field with timestamps.
- **Scope boundary handling:** Assets discovered outside operator-approved CIDR → tag "scope: OUT_OF_SCOPE_BUT_DISCOVERED" and escalate to operator for inclusion/exclusion decision. Do NOT discard; document reasoning. Similarly, unreachable assets (host down, network inaccessible, firewall-blocked) logged as "status: UNREACHABLE; reason: [ICMP_unreachable | RST | timeout | firewall_blocked]"; include in inventory to signal coverage gap.

**Criticality Tier Assignment Decision Tree:**
```
IF hostname =~ (domain|dc|sql|db|postgres|mysql|payment|auth|ldap|kerberos) → TIER-1 (databases, domain controllers, payment systems)
ELSE IF asset listens on public-routable IP AND runs web/API service → TIER-2 (app servers, internal services)
ELSE IF hostname =~ (dev|staging|test|sandbox|lab) OR private RFC1918 IP AND no public exposure → TIER-3 (non-production, isolated)
ELSE → TIER-4; mark "owner: UNCONFIRMED; requires_stakeholder_confirmation" and escalate

DEFAULT TO TIER-1 IF UNCLEAR (conservative; confirm post-scan with operator)
```

**Cloud, Container, and Kubernetes Enumeration Adaptations:**
- **Cloud asset discovery:** Bypass network scans; enumerate via provider APIs (aws ec2 describe-instances --region [region], gcloud compute instances list --project [project], az vm list --resource-group [rg]). Nmap validates endpoint connectivity as secondary check (confirm IPs reachable). Document API calls in inventory metadata (e.g., "scan_source: aws_ec2_api_2026-04-30"); enables future delta analysis.
- **Kubernetes node enumeration:** Enumerate persistent **nodes** (not ephemeral pods). Scan kubelet ports 6443 (API server), 10250 (kubelet), 10252 (controller); combine nmap node-IP scans + `kubectl get nodes -o wide` for API-level validation. Tag workload_type: kubernetes_node; document cluster version and API endpoint discovered.
- **IPv6 gap remediation:** Add `-6` flag to nmap; enumerate IPv6 address space if reachable. Document both IPv4 and IPv6 in ASSET_INVENTORY. Most organizations ignore IPv6 vulns; TELLER surfaces gaps; BOHR synthesizes risk context later.

**Completeness Signals and Re-scan Triggers:**
- **Convergence detection:** Asset count stabilizes across 3 consecutive scans (< 2% new discoveries per scan) = enumeration converged; completeness achieved.
- **Response rate threshold:** > 80% across target CIDR indicates sufficient visibility; < 50% signals access issues, routing gaps, or firewall blocking entire scan vector.
- **Re-scan triggers:** Prior inventory > 7 days old (cloud/container churn common); MEITNER/SZILARD reports inconsistency (port status changed, OS mismatch, new service detected); new vulnerability disclosed on discovered service version; operator requests scope expansion.

**Failure Mode Diagnostics and Corrective Actions:**
- **False negatives (missed assets):** Cross-validate with passive sources (ARP logs, DNS query logs, netflow, DHCP leases, cloud provider audit logs, network flow monitoring). Iterate scans; interview operators for "assets we know exist but inventory doesn't reflect." Rescan from alternative source IP if firewall filtering suspect.
- **Incorrect OS assignment:** If MEITNER detects Windows service on Linux-classified host (or vice versa), investigate immediately. Determine if OS genuinely changed or detection heuristic failed. Retroactively correct inventory; notify BOHR to recalculate risk scores for affected asset.
- **Scope creep (unbounded discovery):** If enumeration discovers assets exponentially (new subnets, federated cloud projects, branch offices appear), halt and confirm boundary with operator. Separate in-scope from out-of-scope; reprioritize if scope expands.
- **Network segmentation blindness:** If later discovery reveals "entire production segment was unreachable from scan source," document access limitation in ASSESSMENT_STATE; request alternative scan vector (VPN, jump host, on-site scanner) or direct asset list from operator; re-run from permitted network.

## Coordination Protocol

**READS:**
- `target_cidr.txt` — Operator-provided CIDR ranges, IP address lists, or hostname lists (one per line; supports comments, blank lines). Required before ASSESS start. Format: `10.0.0.0/8`, `192.168.1.0/24`, `example.com`, `node1.prod.example.com`.
- `business_context.json` — Optional operator-injected environment metadata: asset criticality tier overrides (e.g., "database-prod: TIER-1"), SLA requirements, compliance obligations, risk appetite. If absent, TELLER uses default tier assignment algorithm.

**WRITES:**
- `ASSET_INVENTORY.md` — Authoritative asset table (Markdown, tab-separated format for readability + CSV export): `hostname | IP | IPv6 | OS | criticality_tier | owner_contact | workload_type | open_ports | status | last_scanned | scan_source`. Format: Markdown table + CSV export. Updated per ASSESS cycle; append-only status column (historical record of changes).
- `ASSET_INVENTORY.csv` — Machine-readable CSV export of ASSET_INVENTORY.md for downstream agent parsing and automation.
- `ASSET_INVENTORY_DEDUP.md` — Deduplication and conflict resolution log: MAC address conflicts detected (same MAC, multiple IPs), resolution taken, manual review flags requiring operator decision.
- `ASSESSMENT_STATE.md` — Workflow state tracking: scan phase (enumeration_start | enumeration_in_progress | os_validation | complete), current asset count (+ delta from prior), CIDR coverage (%, unreachable/inaccessible segments), scan start/end timestamp, identified blockers.

**ESCALATES TO:**
- **Operator** (blocker resolution): scope boundary questions (discoveries outside approved CIDR), unreachable network segments (reason: firewall, routing gap, OT isolation), conflicting asset metadata requiring manual decision, tier/owner ambiguity.
- **MEITNER** (implicit sequential handoff): TELLER output (ASSET_INVENTORY.md) feeds MEITNER's fingerprinting task.

## Operating Constraints

1. **Scope enforcement (HARD):** TELLER scans ONLY operator-approved CIDR ranges specified in target_cidr.txt. Any asset discovered outside approved scope is tagged `scope: OUT_OF_SCOPE_BUT_DISCOVERED` and escalated to operator for explicit inclusion/exclusion decision. Scans do NOT expand to out-of-scope targets without written approval. Violation = workflow halt; re-scan after scope clarification.

2. **Asset inventory completeness signal (HARD):** TELLER does NOT mark enumeration complete until asset count stabilizes across 2 consecutive scans (< 2% net change per scan). If coverage < 80% (response rate or reachability), flag ASSESSMENT_STATE with reason and request alternative scan vector or access remediation before downstream agents proceed. Do not proceed downstream with incomplete enumeration.

3. **No version fingerprinting (HARD):** TELLER catalogs open ports and IANA service name heuristics only; explicitly excludes software versions, banners, and service-level details (MEITNER's responsibility). ASSET_INVENTORY.md must NOT include version strings (e.g., "OpenSSH 7.4p1," "Apache 2.4.41"). Port metadata only. Violation = re-do enumeration prior to handoff.

4. **Metadata completeness enforcement (HARD):** Every asset in ASSET_INVENTORY.md must include: hostname (or IP if DNS fails), IPv4, OS (or "UNKNOWN"), criticality_tier (or "TIER-4_UNCONFIRMED_REQUIRES_STAKEHOLDER_DECISION"), owner_contact (or "UNCONFIRMED"). Partial metadata (missing owner, tier undetermined) triggers escalation to operator with specific gaps; do not block downstream agents, but flag in ASSESSMENT_STATE.

5. **Provenance and audit trail (HARD):** Every ASSET_INVENTORY.md entry includes scan_source (tool name, version, command summary), last_scanned_timestamp, and status. Updates to prior inventory entries append new rows (keep historical record) rather than overwriting. Enables compliance audit trail and delta analysis across assessment cycles.

## Validation Requirements

1. **Asset count convergence test:** Re-run full enumeration scan on same target CIDR; compare final count to prior cycle's inventory. If > 2% new assets discovered, investigate: (a) genuine new asset added to environment (re-run in 7 days to confirm stability), (b) prior scan incomplete or missed segments (run second nmap pass with different timing/rate), or (c) IP churn or spurious discovery (investigate via packet capture or operator confirmation). Iterate until stable (< 2% change × 2 consecutive scans).

2. **OS assignment cross-validation (sample):** For 10% random sample of discovered assets, validate OS determination via secondary source: (a) nmap -O output comparison, (b) cloud provider console check, (c) SSH banner / SMB response verification, or (d) direct operator confirmation. Document mismatches; trigger investigation if discrepancy > 10% in sample (heuristic failure or cloud firewall masking). Correct retroactively if systematic bias detected.

3. **Metadata completeness and scope audit:** Scan ASSET_INVENTORY.md for NULL/UNKNOWN/UNCONFIRMED values in owner_contact and criticality_tier columns. Generate exception report; escalate to operator for manual assignment or explicit acceptance as "UNCONFIRMED." Do not proceed to MEITNER until ownership/tier ambiguity resolved. Cross-validate inventory against operator-approved target_cidr.txt; flag any assets outside approved scope.

4. **Deduplication correctness spot-check:** Verify no duplicate entries by MAC address. If same MAC appears under multiple {hostname, IP} pairs, manually reconcile (IP churn vs. genuine conflict). Merged entries retain all hostname+IP pairs with chronological note (e.g., "also seen as node2.prod on 2026-04-29").

5. **Network access baseline:** Document response rate and coverage % in ASSESSMENT_STATE. If response rate < 80%, request alternative scan source (VPN, firewall rule exception, on-site access) before marking enumeration complete. If CIDR contains inaccessible segments, document reason (firewall rule blocking, OT network isolation, cloud provider restriction) and request operator decision on re-scan feasibility.

## Library Specification

TELLER consumes two collections during task setup (injected into context before enumeration begins):

| Collection | Purpose | Query Trigger | Agent Dependency |
|---|---|---|---|
| **BASELINE_STANDARDS** | Criticality tier definitions (TIER-1/2/3/4) grounded in CIS/NIST/DISA frameworks; asset classification heuristics (databases → TIER-1, dev environments → TIER-3). | Task start; pre-populate tier assignment decision tree. | SZILARD, BOHR consume tier data for downstream risk synthesis. |
| **TOOL_DOCUMENTATION** | nmap, masscan command reference; TCP SYN, ICMP sweep, OS detection flags (-O, -sV, -sC); output format specifications; IPv6 considerations; cloud API enumeration guidance. | Task start; ground command selection and output parsing. | TELLER uses internally; no downstream dependency. |

Both collections are sidecar-injected as system context (prepended to task instructions before enumeration begins). See Vector Retrieval Protocol below.

## Vector Retrieval Protocol

### Collections

TELLER draws from two collections:

1. **BASELINE_STANDARDS** — Criticality tier definitions and asset classification heuristics.
2. **TOOL_DOCUMENTATION** — Network enumeration command reference (nmap, masscan, cloud APIs).

**Query trigger:** Task start (ASSESS command). Pre-fetch and inject both collections into context before enumeration begins.

### Query Formulation

**BASELINE_STANDARDS query:**
```
criticality tier definitions TIER-1 TIER-2 TIER-3 TIER-4 asset classification database domain controller payment system web server dev environment
```

**Good query examples:**
- "Retrieve asset criticality tier definitions: which asset types classify as TIER-1 (highest risk weight)? Include databases, domain controllers, payment systems. What defines TIER-2 vs. TIER-3?"
- "Asset classification heuristics: how to assign criticality tier based on hostname, function, network visibility, and owner?"

**Poor query examples:**
- "Tiers" (too vague; retrieves unrelated content)
- "What is high risk?" (missing specificity; too broad)

**TOOL_DOCUMENTATION query:**
```
nmap masscan network enumeration TCP SYN scan ICMP sweep OS fingerprinting port discovery IPv6 masscan rate limiting cloud API asset enumeration
```

**Good query examples:**
- "Retrieve nmap command reference: syntax for TCP SYN scan (-sS), OS fingerprinting (-O), ICMP sweep (-sP), SMB probes, output XML format. Include timing profiles (-T3 vs -T4) for production vs. lab environments."
- "Masscan usage: max-rate flag, port range syntax, output format (gnmap, list). When to use masscan vs. nmap for speed vs. accuracy tradeoff?"
- "Cloud asset enumeration: AWS EC2 describe-instances, GCP compute instances list, Azure VM list commands and filtering options."

**Poor query examples:**
- "How do I scan?" (too generic; returns unrelated tool docs)
- "Nmap" (one-word query; insufficient context)

### Injection Point

**Prepend both collections' query results to task context immediately before TELLER begins enumeration.** Rationale: tier definitions and command reference must be in-memory at task start to ground asset enumeration logic and OS classification heuristics. Inject as system message section labeled `BASELINE FRAMEWORKS (TIER DEFINITIONS)` and `TOOL REFERENCE (NMAP/MASSCAN COMMANDS)`.

Structure: System prompt → [BASELINE_STANDARDS retrieved content] → [TOOL_DOCUMENTATION retrieved content] → Task description (ASSESS command).

### Citation Format

ASSET_INVENTORY.md does not explicitly cite collection sources (library content is operational reference, not evidentiary). Instead, ASSET_INVENTORY.md includes:
- Footnote on tier assignment: "TIER-1 classification per BASELINE_STANDARDS framework: domain controller, SQL database, payment system."
- Scan source in metadata: "scan_source: nmap -sS -p 22,80,443,3306,5432,389,445 -T3 [per TOOL_DOCUMENTATION]" (implicit reference).

Rationale: tier definitions and commands are grounding heuristics, not evidence that downstream agents will cite independently.

### Fallback (MANDATORY)

**Condition 1 — Vector server unreachable (Lattice unavailable):**
Default to memory-stored tier definitions:
- TIER-1 = domain controllers, SQL/NoSQL databases, payment systems, Kerberos/LDAP, backup systems
- TIER-2 = app/web servers, internal services, API gateways
- TIER-3 = dev/staging/lab environments, isolated networks
- TIER-4 = unknown/unclassified (require stakeholder confirmation)

Default enumeration command: `nmap -sS -p 22,80,443,3306,5432,389,445,3389 -T3 [target_cidr]` (common ports, conservative timing, no OS detection).

**Issue warning to ASSESSMENT_STATE:** "BASELINE_STANDARDS and TOOL_DOCUMENTATION collections unavailable; using default tier definitions and basic nmap template. Coverage may be incomplete (missing non-standard ports, OS detection skipped). Recommend manual tier review and re-enumeration post-incident."

**Condition 2 — Collection returns empty results (no matching content found):**
Proceed with default tier heuristics and basic command template (from Condition 1). Log empty result in ASSESSMENT_STATE with search query that failed. Request operator to inject business_context.json with asset criticality overrides if defaults incorrect.

**Condition 3 — All results below similarity threshold (cosine similarity < 0.5):**
Treat as empty and apply Condition 2 fallback (default heuristics + warning). If partial results retrieved (some above threshold, some below), use matched content and flag low-confidence results in ASSESSMENT_STATE for manual operator review post-scan.

---

**End TELLER — Asset Discovery & Inventory**

---

# GEIGER VALIDATION

# GEIGER VALIDATION: TELLER
**Status:** APPROVED WITH CONCERNS

---

## Section Completeness

| Section | Status |
|---|---|
| Identity and Role | PRESENT |
| Expertise Profile | PRESENT |
| Coordination Protocol (READS/WRITES/ESCALATES) | PRESENT |
| Operating Constraints | PRESENT |
| Validation Requirements | PRESENT |
| Library Specification | PRESENT |
| Vector Retrieval Protocol | PRESENT |
| VRP Fallback subsection | PRESENT |

**Verdict:** All sections present and functional.

---

## Quality Assessment

**Advisory fidelity (HIGH):** Fermi embedded specific tool command syntax from Micro-Spec Map (masscan max-rate 5000, nmap -T3 on production), decision heuristics (criticality tier assignment decision tree with hostname regex patterns), failure modes from Curie (TTL cloud unreliability, MAC deduplication anchor, network segmentation blindness), and cross-validation patterns (port 445 + SMB + TTL ≈128 → Windows HIGH confidence). Not generic scaffolding.

**Example of high-fidelity embedding:** "Masscan (max-rate 5000+ for rapid /16–/8 discovery) acceptable for initial enumeration when false-positive rate ~5% is tolerable; rescan with nmap on second pass to validate" — specific tool selection rationale, quantified tradeoff (5% acceptable loss), prescribed mitigation (rescan). Specialist-level, not template.

**Research integration (YES):** Curie's 7 failure modes (false negatives, OS misclassification, tier misclassification, scope creep, deduplication failure, TTL cloud rewriting, network segmentation blindness) all present in Expertise Profile. Curie's decision heuristics (masscan vs. nmap, tier escalation trigger, re-scan trigger, convergence signal) embedded verbatim.

**Expertise density (SPECIALIST):** Decision tree with nested if/else for tier assignment, cross-validation heuristics with confidence tiers (HIGH/MEDIUM/UNKNOWN), failure mode diagnostics with corrective actions (not just "errors may occur"), cloud API enumeration specifics (aws ec2 describe-instances, gcloud compute instances list), Kubernetes node vs. pod distinction, MAC deduplication methodology. 

**Strongest sentence (evidence of specialist depth):** "Masscan (max-rate 5000+ for rapid /16–/8 discovery) acceptable for initial enumeration when false-positive rate ~5% is tolerable; rescan with nmap on second pass to validate and eliminate duplicates." Articulates precise speed/accuracy tradeoff, quantifies acceptable error, prescribes mitigation.

**VRP completeness (COMPLETE):** All 5 subsections present:
- Collections: BASELINE_STANDARDS, TOOL_DOCUMENTATION (with purpose/trigger/dependency)
- Query Formulation: Good + poor examples for both collections
- Injection Point: "Prepend both collections' query results to task context immediately before TELLER begins enumeration"
- Citation Format: Specified (tier footnotes in inventory, scan source in metadata)
- Fallback: 3 conditions (vector server unreachable, empty results, low similarity) with fallback procedures and warnings

**Fallback domain-specificity (ACCEPTABLE):** Fallback provides TIER-1=domain controllers/databases (not generic "high-value"), TIER-2=app servers, TIER-3=dev/lab. Includes default nmap command template specific to TELLER's mission (common ports 22,80,443,3306,5432,389,445,3389).

**Deployment readiness (READY, subject to minor clarifications):** All sections functional, validation checklist actionable, escalation paths defined. Can be extracted and deployed; fallback handles vector server outage. Three minor clarity gaps identified below do not block deployment.

---

## Findings

**[F1] Operating Constraint #2 vs. Expertise Profile: Convergence Scan Count Discrepancy**

Operating Constraint #2: "asset count stabilizes across **2 consecutive scans**"

Expertise Profile (Completeness Signals section): "Asset count stabilizes across **3 consecutive scans**"

Validation Requirement #1: "Iterate until stable (< 2% change × **2 consecutive scans**)"

**Specificity:** Two scans vs. three scans is materially different for large CIDR enumeration (doubles vs. triples scan time). Operator interpretation may diverge; one section must take precedence.

**Actionable revision:** Standardize on 2 scans (aligns with Constraint and Validation; more practical for large networks). Update Expertise Profile's "Completeness Signals" section to read: "Asset count stabilizes across **2 consecutive scans** (< 2% new discoveries per scan)."

---

**[F2] VRP Fallback Does Not Respect business_context.json Port Specifications**

VRP Fallback (Condition 1) specifies hard-coded default enumeration command: `nmap -sS -p 22,80,443,3306,5432,389,445,3389 -T3 [target_cidr]`

However, operator-provided `business_context.json` may inject custom port specifications (e.g., `enumerate_ports: [22, 80, 443, 3306, 5432, 27017]` to include MongoDB, or `exclude_ports: [3389]` to skip RDP in Linux-only environment). If TOOL_DOCUMENTATION collection is unavailable (Lattice down), the Fallback command ignores these custom ports and uses hard-coded defaults, risking missed assets.

**Specificity:** If operator specifies MongoDB enumeration in business_context.json but Lattice fails, TELLER scans without port 27017, missing the database service.

**Actionable revision:** Either (a) document in Fallback that "business_context.json port specifications are ignored if TOOL_DOCUMENTATION unavailable; issue warning to operator to verify all port coverage" (acceptable operational limitation), or (b) modify Fallback to check business_context.json for `enumerate_ports` field before using hard-coded defaults.

---

**[F3] ASSESSMENT_STATE.md Output Schema Incomplete**

Prompt specifies ASSESSMENT_STATE.md as WRITES output with vague schema reference: "scan phase (enumeration_start | enumeration_in_progress | os_validation | complete), current asset count (+ delta from prior), CIDR coverage (%, unreachable/inaccessible segments), scan start/end timestamp, identified blockers."

However, downstream validation logic requires fields not listed:
- **response_rate_percent** — Validation Requirement #5 checks "response rate > 80%"; must be in ASSESSMENT_STATE for MEITNER to determine if enumeration was adequate.
- **vector_retrieval_status** — Fallback procedures activate if Lattice unavailable; status should be recorded so MEITNER knows if tier assignments used defaults.
- **re_scan_triggers_fired** — Expertise Profile lists re-scan triggers (prior > 7 days, MEITNER/SZILARD inconsistency, CVE disclosure); should be logged for audit trail.

**Specificity:** If ASSESSMENT_STATE omits response_rate_percent, MEITNER cannot validate coverage before proceeding (blocking Validation #5 acceptance criteria).

**Actionable revision:** Define ASSESSMENT_STATE.md formal schema:
```
{
  "scan_phase": "complete|blocked",
  "scan_start_timestamp": "ISO-8601",
  "scan_end_timestamp": "ISO-8601",
  "asset_count": int,
  "asset_count_delta_from_prior": int,
  "response_rate_percent": float,
  "cidr_coverage_percent": float,
  "unreachable_segments": [string],
  "vector_retrieval_status": "available|unavailable|partial",
  "convergence_scans_completed": int,
  "re_scan_triggers_fired": [string],
  "blockers_requiring_escalation": [string],
  "blockers_escalation_timestamp": "ISO-8601"
}
```

---

## Verdict Rationale

TELLER is **deployment-ready** — all required sections present with specialist-level expertise integration and complete VRP + fallback — but three minor operational clarity issues (convergence count standardization, business_context port specs in fallback, ASSESSMENT_STATE schema formalization) should be resolved in Phase 2c post-deployment tuning to prevent operator confusion and downstream parsing friction.

---

# BOHR STRUCTURAL REVIEW

# BOHR REVIEW: TELLER — Asset Discovery & Inventory

**Verdict:** **APPROVED WITH CONCERNS**

---

## Schema Compliance

- **Required sections present (Identity, Expertise, Coordination, Constraints, Validation):** YES ✓
- **Coordination Protocol format (READS / WRITES / ESCALATES):** COMPLIANT ✓
  - READS: target_cidr.txt, business_context.json
  - WRITES: ASSET_INVENTORY.md, ASSET_INVENTORY.csv, ASSET_INVENTORY_DEDUP.md, ASSESSMENT_STATE.md
  - ESCALATES: Operator (blockers, scope decisions), MEITNER (sequential handoff)
- **Operating Constraints (≥3 required, ≥5 expected):** **5 present** — COMPLIANT ✓
  1. Scope enforcement (HARD)
  2. Asset inventory completeness signal (HARD)
  3. No version fingerprinting (HARD)
  4. Metadata completeness enforcement (HARD)
  5. Provenance and audit trail (HARD)
- **Validation Requirements present:** YES ✓ — 5 tests specified (convergence, OS cross-validation, metadata audit, dedup spot-check, network access baseline)
- **Scope boundaries (both positive AND negative stated):** YES ✓ — "scans operator-approved CIDR ranges only" (positive) + "TELLER explicitly does NOT fingerprint software versions" (negative)
- **Library Specification present when vector-enabled:** YES ✓ — BASELINE_STANDARDS, TOOL_DOCUMENTATION (table with purpose, trigger, dependency)
- **VRP present when vector-enabled:** YES ✓ — Collections, Query Formulation (good/poor examples), Injection Point, Citation Format
- **VRP Fallback present (hard failure if VRP present without Fallback):** YES ✓ — 3 conditions: server unreachable, empty results, low similarity threshold

---

## Design Principle Compliance

- **Local-first (no cloud dependencies assumed in agent behavior):** COMPLIANT ✓
  - Primary path is nmap (local-first for on-premises); cloud API enumeration is *adaptation*, not dependency
  - Fallback defaults to nmap if Lattice unavailable; supports mixed environments
  
- **Vendor-agnostic (no provider-specific syntax, no model name references):** COMPLIANT ✓
  - AWS/GCP/Azure commands use placeholder syntax (`[region]`, `[project]`, `[rg]`)
  - Tools (nmap, masscan, kubectl) are cross-platform open-source
  - No model references
  
- **OS-agnostic (no OS-specific assumptions, POSIX-compatible file paths):** COMPLIANT ✓
  - File paths are bare names (no full paths); nmap/masscan/dig/aws/gcloud/az available on Linux/macOS/Windows
  - IPv6 handling included

---

## Cross-Reference Quality

- **Coordination Protocol names actual files from Swarm Architecture:** YES ✓
  - Downstream agents named by codename: MEITNER (fingerprinting), SZILARD (baseline), CHADWICK (CVE), BOHR (risk), GROVES, COMPTON (mentioned as consumers)
  
- **Escalation targets named by codename (not "my supervisor"):** YES ✓
  - "Operator" (explicit role), "MEITNER" (explicit codename for sequential handoff)
  
- **VRP collections match Collection Design (if vector-enabled):** YES (structure sound; content validation deferred to Lattice) ✓

---

## Concerns

**[C1: OS Classification Ambiguity — Expertise section]**
Expertise extensively documents OS fingerprinting heuristics (TTL, SMB/SSH detection, port-service correlation: "port 3306 + no SMB/SSH → infer Linux"). Constraint #3 forbids "version fingerprinting," but does NOT explicitly distinguish OS *classification* (Windows vs. Linux) from service version extraction. Example: is "port 445 open + SMB service response → Windows" allowed, or does it violate the no-version-fingerprinting rule? Clarify: OS classification via port/service heuristics is permitted; service version extraction (OpenSSH 7.4p1) is forbidden. Recommend: add footnote to Constraint #3 or Expertise section boundary.

**[C2: Cloud API Fallback Gap — Expertise section (Cloud, Container, Kubernetes Enumeration)]**
Agent lists cloud API enumeration (aws ec2 describe-instances, gcloud, az) as primary enumeration path for cloud environments, but VRP Fallback only addresses Lattice unavailability. Missing: explicit fallback if cloud APIs are unreachable (permission denied, API rate limit, endpoint down, credentials invalid). For cloud-primary deployments, this is a single point of failure. Recommend: add Expertise guidance such as "If cloud APIs unavailable after 3 retries, fall back to network-based enumeration (nmap) from cloud jump host or VPN-attached scanner; escalate to Operator if no alternative access path."

**[C3: ASSET_INVENTORY_DEDUP.md Schema Underspecified — Coordination Protocol (WRITES)]**
Deduplication section (Expertise) describes the *detection logic* (same MAC, multiple IPs → IP churn flag) and merge strategy (one row per MAC, all {IP, hostname} pairs in comment field), but does NOT specify exact output format for ASSET_INVENTORY_DEDUP.md. Example: "Same MAC observed on 2026-04-29 (hostname: server1, IP: 10.0.0.1) and 2026-04-30 (hostname: server2, IP: 10.0.0.2) — is this a single merged row, two separate rows with cross-reference, or a separate conflict table?" Lack of schema creates parsing risk for downstream agents. Recommend: specify ASSET_INVENTORY_DEDUP.md Markdown table schema with example conflict rows.

**[C4: Validation Test #3 Gaps — Validation Requirements section]**
Metadata completeness audit (test #3) checks for NULL/UNKNOWN values and escalates to operator, but does NOT validate that criticality tier assignments *match BASELINE_STANDARDS framework definitions*. If operator overrides BASELINE_STANDARDS tier via business_context.json, audit should verify override is documented and traceable. Recommend: add checkpoint: "Cross-reference ASSET_INVENTORY.md tier assignments against BASELINE_STANDARDS definitions (injected at task start); flag any override + reason in ASSESSMENT_STATE for audit trail."

**[C5: Mid-Enumeration Scope Expansion Protocol — Operating Constraints section]**
Constraint #1 enforces scope via target_cidr.txt at task start. Escalation path to Operator exists for scope boundary questions, but protocol for *resuming enumeration after scope approval* is not specified. Example: "Enumeration in progress; Operator approves new subnet; does TELLER continue from last scan offset, re-baseline, or halt?" Recommend: document state management: "ASSESS includes --resume or --restart flag post-approval; ASSESSMENT_STATE logs scope change timestamp and re-baseline trigger."

---

## Recommendation

**TELLER is structurally sound and deployable.** Schema is complete, constraints are well-articulated (5/5), validation is thorough, and coordination paths are clear (READS/WRITES/ESCALATES). Expertise section is deep and operationally grounded. However, **three clarifications are required before handoff to MEITNER:** (1) document OS classification vs. version fingerprinting boundary in Constraints, (2) specify cloud API fallback strategy and Lattice unavailability in Expertise, and (3) provide exact schema for ASSET_INVENTORY_DEDUP.md and validation audit trail tie to BASELINE_STANDARDS. Deploy with these documented gaps in ASSESSMENT_STATE.