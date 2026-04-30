<!-- THE MANHATTAN PROJECT — SWARM FORGE LIVE v3.0
  Generated: 2026-04-30T14:38:52.406Z
  Swarm: Blue Team Defense Ops
  T2 Advisor: SCINTILLATOR (Detection Engineer)
  VRA Score: 9/9 | Vector-enabled: true
  Geiger: APPROVED WITH CONCERNS | BOHR: **APPROVED WITH CONCERNS**
  Pipeline: IQ-0053 T2→Lattice→Operator workflow

  Commit to: swarms/[name]/agents/lawrence.md
  If vector-enabled: initialize vectors/VECTOR-CONFIG.md from Lattice Collection Design below
-->

# SWARM ARCHITECTURE DOCUMENT

## SWARM ARCHITECTURE: DEFENSIVE SECURITY OPERATIONS

### Mission Parameters
Real-time detection, investigation, and containment of adversarial activity across enterprise networks and log streams in time-pressured, incomplete-information environments. Serves blue team competitions (CCDC, NCCDC) and enterprise SOC operations. Must support simultaneous incident handling, proactive threat hunting, and incident lifecycle closure with forensic rigor and post-incident hardening.

### Critical Mass Calculation
Seven agents cover the full incident lifecycle: triage (gatekeeping), investigation (scope determination), proactive hunting (evasion detection), tactical containment (active defense), forensic preservation (legal/regulatory), telemetry infrastructure (enablement), and hardening (prevention). Each phase requires specialized knowledge and cannot overlap. Time pressure and incomplete data demand parallel execution (hunting runs concurrent to investigation, hardening begins during containment).

### Agent Roster

| Codename | Role | Core Mission | Phase | Tier |
|----------|------|--------------|-------|------|
| **Szilard** | Alert Triage Officer | Ingest raw alerts, apply filtering heuristics, assign priority, route to investigators. | Detection→Triage | Coordinator |
| **Chadwick** | Incident Investigator | Correlate alert events, build timeline, determine incident scope and impact, advise containment. | Investigation | Specialist |
| **Fermi** | Threat Hunter | Execute proactive log searches for IoCs, behavioral anomalies, and undetected intrusions. | Hunting (parallel) | Specialist |
| **Compton** | Incident Responder | Execute containment actions: isolate hosts, revoke credentials, terminate malicious processes, stop exfiltration. | Containment | Specialist |
| **Meitner** | Forensic Analyst | Preserve chain of custody, collect forensic artifacts, document evidence for post-incident analysis and legal/regulatory. | Investigation (parallel) | Specialist |
| **Lawrence** | SIEM/Telemetry Gateway | Normalize and index all telemetry sources (logs, network, endpoint), maintain search indexes, provide queryable data layer. | Infrastructure (continuous) | Utility |
| **Teller** | Hardening Engineer | Deploy patches, implement configuration hardening, develop detection rules from root causes, prevent recurrence. | Post-Incident / Preventive | Specialist |

### Coordination Files

- **INCIDENT_COMMAND.md** — Unified incident tracker: open incidents, assigned investigator, containment status, timeline, root cause, closure date.
- **DETECTION_RULES.md** — Alert definitions, rule tuning parameters, false positive notes, rule ownership, effectiveness metrics.
- **IOC_FEED.md** — Current indicators of compromise, hunt signatures, YARA rules, behavioral queries, threat intelligence integrations.
- **CONTAINMENT_PROCEDURES.md** — Standardized playbooks for isolation, credential revocation, malware removal, network segmentation by asset type.
- **POST_INCIDENT_ACTIONS.md** — Remediation tracking, patch deployment status, hardening task ownership, preventive rule rollout, metrics.

### Workflow Commands

- **ALERT_RECEIVED** `[alert_id] [source] [severity] [indicator]` — Szilard ingests alert, applies noise filters, assigns priority, routes to Chadwick if confirmed.
- **ESCALATE_INCIDENT** `[incident_id] [scope] [affected_assets]` — Declares investigation phase open; triggers Chadwick (investigation) and Meitner (preservation) in parallel; notifies Fermi of scope for correlation hunting.
- **HUNT_QUERY** `[ioc/query] [timeframe] [scope]` — Fermi executes proactive search across SIEM; returns matches for Chadwick correlation or new incidents.
- **CONTAIN** `[asset_id] [action] [duration]` — Compton executes containment (isolate, credential revoke, block egress); Meitner snapshots state pre-containment.
- **CLOSE_INCIDENT** `[incident_id] [root_cause] [remediation_items]` — Triggers Teller hardening workflow; updates DETECTION_RULES.md and POST_INCIDENT_ACTIONS.md.

### Phase 2 Advisor Assignment

**Primary: Chadwick** (Incident Investigator)  
**Secondary: Fermi** (Threat Hunter)

*Rationale:* Chadwick is the decision hub—investigation output determines whether containment is warranted, what scope applies, and whether the incident is real or noise. Fermi backs up by hunting for related undetected activity if initial investigation yields incomplete signals.

### Fabrication Priority

**Lawrence** (SIEM/Telemetry Gateway) must be forged first. Without normalized, indexed, queryable telemetry, no other agent can function. Szilard cannot triage, Chadwick cannot investigate, Fermi cannot hunt, Compton cannot verify containment success. Lawrence is the foundation.

### Vector Readiness Pre-Assessment

This is a **repeat-against-similar-environments swarm with strong domain knowledge persistence and state continuity.** Each closed incident updates detection rules, IOC feeds, and hardening procedures, affecting the next run's sensitivity and playbook effectiveness. Agents maintain operational state (open incidents, quarantine status, audit logs, forensic artifacts) that persists across sessions. Knowledge overlaps are significant: all agents require understanding of active incident context, IOC status, containment windows, and forensic constraints. This requires a shared incident command protocol, synchronized state files (INCIDENT_COMMAND.md, IOC_FEED.md), and coordination barriers to prevent simultaneous modification conflicts. Pre-assessment suggests Lattice VRA should model incident state propagation, rule effectiveness feedback loops, and forensic artifact lineage tracking.

---

# LATTICE VRA (OPERATOR ONLY)

# LATTICE VRA: DEFENSIVE SECURITY OPERATIONS
*Vector Readiness Assessment — Phase 1b output*  
*Routing: OPERATOR ONLY — do not share with T2 advisor*

---

## Assessment

| Question | Your Assessment | Score |
|---|---|---|
| **Runs repeatedly against similar environments?** | **YES** — CCDC/NCCDC competitions and enterprise SOC operations are explicitly repeat-deployment scenarios. Each incident closes and the next begins within the same operational envelope. State (rules, IoCs, procedures) feeds forward to improve the next cycle. | **+2** |
| **Knowledge base exceeds ~50 docs / ~100KB?** | **YES** — INCIDENT_COMMAND.md, DETECTION_RULES.md, IOC_FEED.md, CONTAINMENT_PROCEDURES.md, POST_INCIDENT_ACTIONS.md, plus operational artifacts (open incidents, quarantine logs, forensic chains). In a real SOC, this easily exceeds 50 docs and 100KB. | **+2** |
| **Agents need domain knowledge mid-task (CVEs, TTPs, policies)?** | **YES** — All 7 agents require live domain injection: Chadwick (attack pattern context), Fermi (TTPs and behavioral baselines), Compton (asset-specific containment), Teller (CVE/patch data), Szilard (rule metadata for triage filters). Incident state, IOC status, and containment windows must flow mid-execution. | **+2** |
| **Maintains state across multiple sessions?** | **YES** — Document explicitly states agents maintain operational state (open incidents, quarantine status, audit logs, forensic artifacts) that **persists across sessions**. Synchronized via INCIDENT_COMMAND.md and IOC_FEED.md. | **+1** |
| **4+ agents with overlapping domain knowledge needs?** | **YES** — All 7 agents share: incident context, IOC status, containment windows, forensic constraints, detection rule metadata. Szilard and Fermi both use IOCs; Chadwick and Meitner both need incident timeline; Compton and Meitner coordinate on state snapshots. Massive overlap across detection→investigation→hunting→containment→forensics pipeline. | **+1** |
| **CPU-only hardware, limited RAM (<16GB)?** | **NO** — Enterprise SOC infrastructure implied (SIEM, telemetry indexing, forensic collection); no hardware constraints mentioned. Production environment assumes resource availability. | **0** |
| **Knowledge base changes mid-operation (new targets, burned techniques)?** | **YES** — Document explicitly describes live mutation: "each closed incident updates detection rules, IOC feeds, and hardening procedures." New IoCs emerge during hunts; techniques are revealed and added to rule sets; Teller develops detection rules from root causes during incident closure. | **+1** |
| **Lifecycle under 2 hours with small fixed knowledge base?** | **NO** — Incident lifecycle spans hours to days: investigation (30 min–hours), hunting (parallel, 30 min–hours), containment (15 min–hours), forensic preservation (ongoing), hardening (post-incident). "Time-pressured" does not mean sub-2-hour closure. | **0** |

**VRA Total: 9/9**

---

## Recommendation

**RECOMMENDED (≥4) ✓**

This swarm exhibits the strongest vector-store indicators: **repeated execution across similar environments, persistent multi-session state, 7 agents with overlapping domain knowledge, mid-task knowledge injection, and live mutation of the knowledge base.** The incident lifecycle integrates detection→triage→investigation→hunting→containment→forensics→hardening with tight coordination: Chadwick's investigation output gates containment scope; Fermi's hunting correlates against live IoCs; Teller's hardening updates rules that influence Szilard's next triage cycle. State propagation is critical—closed incidents must inform future investigations, burned techniques must become rule signatures, and forensic findings must persist for audit and legal use. A vector store is the only way to support this without coordinating agents via brittle file locks or out-of-band manual lookups.

---

## Proposed Architecture

| Component | Choice | Rationale |
|---|---|---|
| **Vector store** | **Qdrant local** (or Qdrant HTTP if SOC infrastructure is centralized) | Metadata filtering supports incident correlation queries (find past incidents with similar IoCs or attack patterns); supports write-through updates for hot data (IOC_FEED.md) and eventual consistency for forensic artifacts. |
| **Embedding model** | **CySecBERT (security domain)** | Defensive security domain requires CVE context, MITRE ATT&CK knowledge, detection rule language, and forensic vocabulary. CySecBERT outperforms general-purpose embeddings for this mission. |

---

## Suggested Collection Stubs (starting hypotheses only—for operator reference)

- **incidents** — Closed incident summaries: root cause, affected assets, remediation items, timeline, closure date. Used by Chadwick to retrieve similar past incidents during investigation. Sourced from INCIDENT_COMMAND.md. — **HYPOTHESIS**, subject to T2 advisor revision.

- **detection_rules** — Alert definitions, tuning parameters, false-positive notes, rule ownership, effectiveness metrics, related CVEs/TTPs. Used by Szilard for triage context and Teller for hardening feedback. Sourced from DETECTION_RULES.md. — **HYPOTHESIS**, subject to T2 advisor revision.

- **ioc_catalog** — Indicators of compromise, YARA rules, behavioral queries, threat intelligence integrations, burn status. Used by Fermi for proactive hunts and Chadwick for alert correlation. Sourced from IOC_FEED.md. — **HYPOTHESIS**, subject to T2 advisor revision.

- **containment_procedures** — Standardized playbooks by asset type (isolate host, revoke domain credentials, block egress, terminate processes, etc.). Used by Compton during incident response and Chadwick during scope planning. Sourced from CONTAINMENT_PROCEDURES.md. — **HYPOTHESIS**, subject to T2 advisor revision.

- **forensic_artifacts** — Metadata on collected evidence: hash, timestamp, source system, collection method, chain-of-custody notes, legal hold status. Used by Meitner and Chadwick for investigation continuity and regulatory compliance. Sourced from POST_INCIDENT_ACTIONS.md and forensic logs. — **HYPOTHESIS**, subject to T2 advisor revision.

---

## Operator Notes

**Lawrence is the foundation.** The vector store depends entirely on Lawrence (SIEM/Telemetry Gateway) normalizing, indexing, and making queryable all telemetry sources. If Lawrence is incomplete or delayed, vector ingestion will have gaps—resulting in Fermi missing hunts, Chadwick missing investigation context, and Compton missing validation signals. Verify Lawrence is operational before or concurrent with vector store population.

**Do not share this VRA with the T2 advisor yet.** Per TRAINING-DATA-INTEGRITY.md Rule 1, the advisor should author their own library requirements from domain knowledge without seeing this output. This prevents suggestion-confirmation loops that degrade training data quality. Once the advisor has committed their Library Specification (collections, schema, refresh strategy), compare it against this VRA to validate alignment.

**Sync and audit requirements.** Qdrant must support:
- **Real-time index updates** for IOC_FEED.md (hot data; new IoCs emerge during active hunts).
- **Eventual consistency** for incident and forensic artifacts (lower velocity, append-only).
- **Full audit logging** if this swarm operates in regulated environments (law enforcement SOC, financial sector). Every retrieval, update, deletion must be traceable to an agent action and incident ID.

**Forensic chain of custody is non-negotiable.** Meitner's forensic artifacts must be immutable once written (or append-only with deletion audit trails). If this swarm supports legal proceedings or regulatory investigations, the vector store cannot be the single source of truth—it must be a searchable index backed by immutable forensic vaults.

**State propagation timing:** Consider write-through vs. async patterns. When Teller closes an incident and updates DETECTION_RULES.md, should that immediately re-index in the vector store, or on a batch schedule? In a real blue team competition (NCCDC), minutes matter; in a 24/7 SOC, eventual consistency may be acceptable.

---

# MICRO-SPECIALIZATION MAP + LIBRARY SPECIFICATION
*T2 Advisor: SCINTILLATOR*

# MICRO-SPECIALIZATION MAP: DEFENSIVE SECURITY OPERATIONS
*Produced by: Scintillator (T2 Detection Engineer) — ADVISORY-PROTOCOL Phase 2*

---

## Szilard — Alert Triage Officer

**Positive Scope:**
- Alert ingestion from all sources (SIEM, EDR, network sensors, cloud platforms)
- Apply noise filters and severity assignment (rolling 7-day median ±2σ baseline)
- Route confirmed alerts to Chadwick; discard or suppress noise
- Data sources: All alert streams (SPL saved searches with alert_severity field, KQL alert tables, Suricata eve.json, EDR API alerts, syslog SIEMs)
- Query languages: Splunk SPL (alert filtering), KQL (M365 Sentinel alert classification)

**Negative Scope:**
- Does NOT investigate alert root causes (Chadwick)
- Does NOT hunt for undetected activity (Fermi)
- Does NOT execute containment (Compton)
- Does NOT preserve forensics (Meitner)

**Expertise Content:**
- Alert classification taxonomy: True Positive (TP) / False Positive (FP) / Benign Positive (BP)
- Noise filter thresholds: baseline median alert count per source per 24h; suppress if >median + 2σ for 3 consecutive days
- Event ID priority matrix: **HIGH** (4688 process creation, 4698 scheduled task, 7045 new service); **MEDIUM** (4624 logon, 4625 logon failure, 4648 run-as); **LOW** (4616 audit policy change, 4720 user creation)
- Sigma rule baseline for triage: `alert_severity >= 60 AND alert_confidence >= 75 AND NOT (tag: known_benign_process)`
- Critical rule ownership: Teller owns rule updates; Szilard enforces tuning thresholds in real-time

**Handoff Artifact:**
- **ALERT_QUEUE.log** (TSV: timestamp, alert_id, source_system, severity_score, indicator, assigned_investigator, filter_applied)
- Consumer: Chadwick (Incident Investigator)
- Update frequency: Real-time; retention 30 days

---

## Chadwick — Incident Investigator

**Positive Scope:**
- Correlate alert events into incident timelines and scope determination
- Advise containment urgency and scope (affected assets, users, data, timeline bounds)
- Execute root cause hypothesis and impact assessment
- Data sources: Windows Security Events (4624/4625/4648/4688/4698/7045), Sysmon (Events 1/3/7/8/10/11/13/15/17/22), EDR telemetry (process tree, memory access, network connections), DNS/proxy logs for context
- Query languages: KQL (M365 Sentinel), SPL (Splunk), Sysmon-native queries

**Negative Scope:**
- Does NOT triage raw alerts (Szilard does that)
- Does NOT hunt for undetected activity (Fermi does that)
- Does NOT execute containment actions (Compton does that)
- Does NOT handle forensic chain of custody (Meitner does that)

**Expertise Content:**
- **Process Chain Correlation Logic:**
  - Lateral Movement: 4624 (logon type 3 or 10) + 4688 (parent=svchost or explorer) + 4698 (scheduled task creation) = privilege escalation chain
  - Pass-the-Hash: 4624 (logon type 3 + NTLM auth) + same hash in multiple 4688 events within ±10min = credential reuse
  - Kerberoasting: 4769 (TGS request) + high-value SPN + 4624 (service logon) = account compromise
- **Event ID Correlation Window:** ±5 minutes sliding for co-location; ±60 minutes for user-centric chains
- **Incident Declaration Threshold:** ≥3 correlated events across ≥2 distinct assets OR ≥1 critical event (data exfil, privilege escalation) with supporting context
- **Behavioral Baseline:** normal process parent-child relationships (e.g., explorer→notepad), anomalous patterns (svchost→cmd.exe, SYSTEM→user shell), privilege escalation markers (token elevation 4672 post-logon)
- **Timeline Anchor:** discovery event (first alert) → retroactive correlation (±2h window) → forward correlation (active investigation window)

**Handoff Artifact:**
- **INCIDENT_TIMELINE.json** (structure: incident_id, status, discovery_timestamp, scope: {assets: [], users: [], data_sensitivity}, events: [{event_id, timestamp, type, source, indicator}], root_cause_hypothesis, severity_classification)
- Consumers: Fermi (for correlation hunting scope), Compton (for containment scope and duration), Meitner (for forensic artifact targets)
- Update frequency: Real-time (on new event correlation); retention: open incidents active, closed incidents 90 days

---

## Fermi — Threat Hunter

**Positive Scope:**
- Proactive IOC searches and behavioral anomaly detection across normalized telemetry
- Hunt for undetected lateral movement, exfiltration, persistence, C2 beaconing
- Execute hypothesis-driven searches; validate or refute threat hypotheses
- Data sources: All SIEM-indexed logs (Zeek conn.log/dns.log/http.log/ssl.log, Sysmon 1/3/7/8/10/11, Windows Security Events 4624/4688, endpoint telemetry, proxy/firewall logs)
- Query languages: KQL, SPL, Zeek query syntax, regex (YARA for file/memory patterns)

**Negative Scope:**
- Does NOT triage raw alerts (Szilard does that)
- Does NOT determine investigation scope (Chadwick does that)
- Does NOT execute containment (Compton does that)
- Does NOT preserve forensic artifacts (Meitner does that)

**Expertise Content:**
- **Hunt Hypothesis Templates:**
  - **Lateral Movement (PTH):** 4624 logon_type=3, auth_package=NTLM → group by logon_source, logon_account, target_server → same NTLM hash reuse >3 assets in 60min = credential spray
  - **Kerberoasting Prep:** 4769 service_name matches high-value SPNs (SQL, Exchange, CIFS) + TGT failures (4768 preauth_fail) within ±10min = account compromise sequence
  - **WMI Lateral Movement:** Sysmon EventID 17 (pipes) + parent=svchost.exe + dest_process includes cmd.exe or powershell.exe = remote code execution vector
  - **Exfiltration Prep:** Zeek http.log method=GET, uri contains /download or /export + large response_body (>100MB) + dest_ip external = data staging
  - **C2 Beaconing:** Zeek conn.log dest_port NOT IN [22,80,443,3389,53], duration_sec consistent (median <2min), packet count regular pattern, >50 connections in 24h to single dest_ip = callback server
- **IOC Pivot Logic:** file_hash → parent_process_image → user_SID → lateral_movement_chain; refine by Zeek ssl.log server_name grouping + ssl.cert fingerprint clustering
- **Behavioral Baseline (Zeek conn.log):** calculate per-asset dest_port distribution percentiles (P50, P95); anomaly = dest_port not in asset's historical top-10 AND >3σ deviation = suspicious egress
- **Sigma Rule Template for Hunts:**
  ```yaml
  title: "Lateral Movement via PTH"
  logsource:
    product: windows
    service: security
  detection:
    selection:
      EventID: 4624
      LogonType: [3, 10]
      AuthenticationPackage: NTLM
      TargetUserName|contains: '*'
    filter_service_accounts: TargetUserName|endswith: '$'
    condition: selection and not filter_service_accounts
  threshold: ≥2 events per TargetUserName per 60min
  level: high
  ```
- **Hunt Result Threshold:** flag if ≥2 independent evidence sources (e.g., event log + network traffic) OR ≥5 events from single asset in 24h window

**Handoff Artifact:**
- **HUNT_RESULTS.csv** (columns: ioc, ioc_type, matched_events_count, src_assets, dest_assets, first_seen, last_seen, severity, confidence, false_positive_flag, chadwick_review_required, notes)
- Consumers: Chadwick (for incident scope expansion), Szilard (for new alert rule generation), IOC_FEED.md (shared state)
- Update frequency: Per-hunt (ad-hoc) or continuous (daily baseline hunts); retention: active IOCs indefinitely, invalidated IOCs 30 days

---

## Compton — Incident Responder

**Positive Scope:**
- Execute containment actions: host isolation, credential revocation, malicious process termination, network egress blocking
- Verify post-containment status via telemetry verification queries
- Maintain containment audit trail (actions, timestamps, success/failure flags)
- Data sources: EDR agent APIs (CrowdStrike Falcon, SentinelOne), Active Directory audit logs (4720 password reset, 4724 password reset attempt), network ACL logs, process termination audit logs (Windows 4688 sysmon_20)
- Query languages: EDR API (REST, JSON payload), PowerShell remoting (Invoke-Command), Active Directory PowerShell module

**Negative Scope:**
- Does NOT determine containment scope or duration (Chadwick decides)
- Does NOT preserve forensic evidence pre-containment (Meitner does that; ordering constraint: Meitner→Compton)
- Does NOT hunt for undetected activity (Fermi does that)
- Does NOT develop hardening rules (Teller does that)

**Expertise Content:**
- **Containment Action Matrix (by asset type):**
  - **Server (high-value):** (1) network isolate (disable egress ACL), (2) revoke cached credentials (clear kerberos tickets, reset service account password), (3) terminate malicious process by PID, (4) snapshot post-action telemetry for 10min
  - **Workstation (user-facing):** (1) enable EDR process block (kill parent+child chain), (2) disable user logon SID, (3) revoke RDP sessions (logoff /v), (4) snapshot memory/disk for forensics (Meitner initiates pre-containment)
  - **User Account (credential compromise):** (1) revoke all session tokens (force logoff across domain), (2) reset password, (3) disable logon script, (4) audit AD group memberships (4627 group membership change)
- **Pre-Containment Preservation:** Meitner MUST snapshot memory and disk BEFORE Compton isolates; ordering enforced by INCIDENT_COMMAND.md status workflow
- **Post-Containment Verification Logic:** (1) zero outbound network connections (Zeek conn.log filter by src_ip + timestamp_after_isolation = empty), (2) no process spawning for 300sec (Sysmon EventID 1 filter = empty), (3) no privilege escalation attempts (no EventID 4672 with elevated token)
- **EDR Query Template (CrowdStrike):** `GET /devices/queries/devices/v1?filter=hostname:*&sort=last_activity_time.desc` → parse device_id → `POST /devices/actions/contain/entities/machines/v1` with action_name=contain
- **Verification Threshold:** containment SUCCESS = zero post-action alert events on isolated asset for 600sec + EDR status=contained

**Handoff Artifact:**
- **CONTAINMENT_LOG.json** (structure: incident_id, asset_id, action_sequence: [{action_name, timestamp_start, timestamp_end, duration_sec, success_flag, edRresponse_code, anomalies_detected}], verification_query_results, audit_trail)
- Consumers: Teller (for post-incident hardening context), Meitner (for forensic artifact timeline context), Chadwick (for incident closure)
- Update frequency: Real-time (per action); retention: indefinite (evidence trail for compliance)

---

## Meitner — Forensic Analyst

**Positive Scope:**
- Preserve chain of custody for all forensic artifacts (memory, disk, logs, network captures)
- Collect pre-containment and post-containment snapshots
- Document evidence lineage (collector identity, timestamps, hashes, tampering detection)
- Data sources: Memory dumps (.dmp via EDR or native tools), disk snapshots (forensic image via dd or Symantec), EVTX event logs (export via Event Viewer or wevtutil), Zeek PCAP/logs, Suricata EVE JSON
- Query languages: Hash verification (SHA256, MD5), NTFS artifact parsing (timeline, MFT, UsnJournal), registry hive analysis

**Negative Scope:**
- Does NOT make investigation scope decisions (Chadwick does that)
- Does NOT execute containment (Compton does that; but Meitner must act first for pre-containment snapshot)
- Does NOT hunt (Fermi does that)
- Does NOT develop prevention rules (Teller does that)

**Expertise Content:**
- **Forensic Preservation Workflow (Critical Ordering):**
  1. Chadwick → Meitner: "snapshot before containment" (INCIDENT_COMMAND.md status=prep_forensics)
  2. Meitner: collect memory.dmp, disk snapshot, event log EVTX, network PCAP within 60sec
  3. Hash all artifacts (SHA256) and timestamp collection (ISO-8601 UTC)
  4. Compton → begins containment only after Meitner confirms completion (status=forensics_collected)
  5. Compton: post-containment telemetry snapshot
  6. Meitner: document chain of custody for both pre- and post-containment states
- **Evidence Lineage Template:** artifact_id (e.g., "server-01_memory_20260430_1400Z"), hash_sha256, collection_timestamp (ISO-8601), collector_name, collection_method (EDR API / manual dump / SIEM export), access_audit_log (who accessed, when)
- **Memory Dump Forensic Targets:**
  - Injected code (anomalous virtual address regions, non-standard page protections)
  - Process handles (open file handles, network sockets, registry keys for persistence mechanisms)
  - Malware signatures (API call sequences, string patterns for C2 callbacks, encryption keys)
- **Disk Snapshot Forensic Targets:**
  - C:\Windows\System32\winevt\logs (EVTX files for Windows Security, PowerShell, Sysmon)
  - C:\Windows\Prefetch (execution history and command-line artifacts)
  - C:\$RECYCLE.BIN (deleted executables for timeline reconstruction)
  - User AppData: C:\Users\*\AppData\Local\Google\Chrome\User Data (browser history, login cookies)
  - Startup folders: C:\Users\*\AppData\Roaming\Microsoft\Windows\Start Menu\Startup (persistence)
  - Registry hives: SYSTEM, SOFTWARE, SAM (service configuration, installed software, password hashes)
- **Evidence Sufficiency Threshold (Legal):** ≥2 independent correlated sources (e.g., memory dump + event log + network PCAP) required for legal admissibility in forensic report; single source flagged as "context-dependent"

**Handoff Artifact:**
- **FORENSIC_MANIFEST.json** (structure: incident_id, artifacts: [{artifact_name, artifact_type, collection_timestamp, collector_name, hash_sha256, collection_method, access_audit: [{who, when, action}]}], chain_of_custody_complete_flag, integrity_verification_status, legal_admissibility_flag)
- Consumers: Teller (for root cause analysis and hardening), legal/compliance teams (for regulatory closure and litigation support)
- Update frequency: Per-incident (on closure); retention: indefinite (legal holds supersede retention policies)

---

## Lawrence — SIEM/Telemetry Gateway

**Positive Scope:**
- Ingest and normalize all telemetry sources (Windows events, Sysmon, Zeek, Suricata, EDR, DNS, proxy, firewall, cloud platform logs)
- Maintain searchable, indexed, queryable data layer for all agents
- Provide sub-second latency for alert queries; <5min latency for batch hunts; <100ms for real-time streaming
- Data sources: Windows Security Event forwarding (WEF), Sysmon agent (all Event IDs), Zeek sensor (conn.log, dns.log, http.log, ssl.log, files.log), Suricata IDS (eve.json), EDR agent API (telemetry stream), DNS resolver logs, proxy/firewall syslog, cloud platform APIs
- Query languages: Splunk SPL, Elasticsearch KQL, QRadar AQL, generic syslog/JSON ingestion

**Negative Scope:**
- Does NOT filter or triage alerts (Szilard does that)
- Does NOT investigate (Chadwick does that)
- Does NOT hunt (Fermi does that)
- Does NOT execute containment (Compton does that)

**Expertise Content:**
- **Data Normalization Schema (unified event model):**
  - Windows Security Event 4624 (logon) → normalized_field: src_ip, dest_ip, user_name, logon_type, auth_package, workstation_name
  - Sysmon EventID=1 (process creation) → image, parent_image, command_line, user, process_id, parent_process_id, target_object (for WMI pivot)
  - Sysmon EventID=3 (network connection) → src_ip, src_port, dest_ip, dest_port, protocol, process_id, image
  - Zeek conn.log → src_ip, src_port, dest_ip, dest_port, proto, service, duration, orig_bytes, resp_bytes, conn_state (for anomaly detection)
  - Zeek dns.log → query, qtype, answers, rcode, timestamp (for C2 beaconing, domain entropy)
  - Suricata alert → alert_signature, alert_signature_id, src_ip, dest_ip, dest_port, app_proto, severity_code
- **Index Retention Policy (cost optimization):**
  - **Hot (0-30 days):** daily indexes, sub-second search latency, alert queries primary use case
  - **Warm (31-90 days):** weekly rollup, 5-min search latency, hunt queries primary use case
  - **Cold (91-365 days):** monthly archive, 30-min search latency, compliance/legal holds, rarely accessed
  - Purge at 365 days unless regulatory/legal hold applies
- **Query Performance Baseline:**
  - Alert query (filter + group-by): ≤1 sec (e.g., "EventID=4624 AND logon_type=3" over 24h)
  - Hunt query (scan 90 days, complex correlation): ≤300 sec (e.g., "process chain analysis across 3 event types")
  - Raw event retrieval: ≤100 events/sec for streaming, <10MB/sec for batch export
  - Real-time alert streaming: <100ms latency from event generation to searchable state
- **Sysmon Field Mapping (critical for correlation):**
  - EventID=1 (process_creation): ParentImage, Image, CommandLine, User, ProcessId, ParentProcessId, LogonGuid
  - EventID=3 (network_connection): SourceIp, SourcePort, DestinationIp, DestinationPort, Protocol, Initiated, ProcessId, Image
  - EventID=7 (image_load): Image, ImageLoaded, Signed, SignatureStatus (for DLL injection detection)
  - EventID=10 (process_access): SourceImage, TargetImage, GrantedAccess, SourceProcessId (for memory access pivots)
  - EventID=17 (pipe_created): PipeName, Image (for WMI lateral movement detection)
- **Zeek DNS Field Mapping (for C2 detection):**
  - query → domain name; qtype → query type (A=1, AAAA=28, MX=15, TXT=16)
  - answers → resolved IPs; entropy(query) → high entropy = possible algorithm-generated domain
  - Group by (query, src_ip) + count → beaconing pattern: same domain queried >10 times in 24h from single host = callback

**Handoff Artifact:**
- **DATA_AVAILABILITY.json** (structure: sources: [{name, status: {last_event_timestamp, lag_seconds, event_count_24h}], index_health: {hot_size_gb, warm_size_gb, cold_size_gb, retention_policy}, query_performance_metrics: {percentile_p50_ms, percentile_p95_ms, percentile_p99_ms}, coverage_gaps: [{source_name, gap_reason, impact_on_agents}])
- Consumers: Szilard (index availability for alert filtering), Chadwick (query performance SLA), Fermi (hunt data availability), all agents (for operational awareness)
- Update frequency: Hourly (automated health check via monitoring daemon); retention: 30 days of metrics for trend analysis

---

## Teller — Hardening Engineer

**Positive Scope:**
- Root cause analysis post-incident (why detection failed, why containment succeeded/failed, technical and process gaps)
- Deploy patches, configuration hardening, EDR policy updates, network segmentation rules
- Author and roll out detection rules (Sigma YAML → SPL/KQL compilation; integration with Lawrence)
- Prevent recurrence and raise baseline security posture
- Data sources: Patch management logs (WSUS, patch status, deployment history), GPO audit logs (Group Policy application status), vulnerability scan results (Nessus, Qualys), detection rule repository (Sigma, YARA), incident root cause documents
- Query languages: PowerShell (Group Policy application, patch cmdlets), Sigma rule authoring (YAML), bash/Python (rule compilation, automation)

**Negative Scope:**
- Does NOT triage raw alerts (Szilard does that)
- Does NOT investigate individual incidents in real-time (Chadwick does that)
- Does NOT hunt (Fermi does that)
- Does NOT execute active containment (Compton does that)
- Does NOT preserve forensic evidence (Meitner does that)

**Expertise Content:**
- **Root Cause Analysis Categories & Hardening Actions:**
  - **Detection Gap:** no rule existed for attack pattern → author Sigma rule + deploy to Lawrence; threshold: rule must achieve ≥80% TP rate in parallel test mode before rollout
  - **Log Source Missing:** required event ID not collected → enable Windows Security Event forwarding (WEF) subscription, Sysmon event type, Zeek sensor → verify in DATA_AVAILABILITY.json within 24h
  - **False Negative:** rule existed but was tuned down (threshold raised to reduce noise) → re-tune threshold ±σ based on 7-day baseline; test in audit mode for 48h before enforcement
  - **Technical Control Missing:** malicious process not blocked by EDR → implement EDR endpoint protection rule, add to blocked-application list, or disable user execution rights for risky binary
- **Sigma Rule Template (Sigma rule authoring best practice):**
  ```yaml
  title: "Lateral Movement via Scheduled Task Creation"
  id: 12345678-1234-5678-1234-567812345678
  status: test
  description: Detects creation of scheduled tasks via WMI (ScheduleService.Create) for lateral movement
  logsource:
    product: windows
    service: sysmon
    category: process_creation
  detection:
    selection_wmi:
      Image|endswith: 'svchost.exe'
      CommandLine|contains: 'ScheduleService'
      ParentImage|endswith: 'explorer.exe'
    selection_remote_registry:
      EventID: 3
      DestinationPort: 445
      Image|endswith: 'cmd.exe'
      CommandLine|contains: 'reg add'
    condition: selection_wmi OR selection_remote_registry
  falsepositives:
    - Legitimate system administration tool usage (e.g., automation frameworks)
    - Scheduled backup and patching systems
  threshold: ≥2 events from single src_ip within 60min
  level: high
  ```
- **Patch Deployment Window SLA:**
  - **Critical (RCE, privilege escalation):** 48 hours from CVE publication
  - **High (bypass, elevation):** 1 week
  - **Medium (low-impact vulnerability):** 2 weeks
  - **Low (cosmetic, DoS):** monthly patching cycle
- **Detection Rule Effectiveness Metrics (tracking for continuous improvement):**
  - **True Positive Rate (TP%):** confirmed detections / total alerts; target ≥75%
  - **False Positive Rate (FP%):** baseline rolling 7-day median ±2σ; goal: FP count ≤ median
  - **Mean Detection Range (MDR):** hours from exploit execution to rule trigger; target <4h for network-based attacks, <10min for endpoint-based
  - **Rule Coverage (%):** threats detected / total threat categories in MITRE ATT&CK; target ≥80% for enterprise tactics
  - **Tuning Frequency:** monthly review of TP/FP metrics; adjust threshold if trend deviates ±10% from baseline

**Handoff Artifacts:**
- **DETECTION_RULES.md** (columns: rule_id, rule_name, Sigma_yaml, SPL_compilation, KQL_compilation, author, last_updated_date, effectiveness_metrics: {TP_rate, FP_rate, MDR_hours}, tuning_notes, alert_tier_assignment)
  - Consumer: Szilard (rule execution in alert pipeline), Lawrence (rule compilation and deployment)
  - Update frequency: Post-incident (within 24h of incident closure) + monthly tuning review
- **POST_INCIDENT_ACTIONS.md** (columns: incident_id, root_cause_category, patch_list, rule_updates, config_hardening, gpO_changes, edR_policy_updates, deployment_status: {pending/in_progress/deployed}, owner, ETA, closure_status)
  - Consumer: Compton (containment context), Meitner (forensic root cause alignment), leadership (remediation tracking)
  - Update frequency: Weekly progress updates; final closure within 30 days post-incident

---

## Coordination File Design

| File | Purpose | Primary Owner | Update Frequency | Consumers | Conflict Resolution |
|------|---------|---|---|---|---|
| **INCIDENT_COMMAND.md** | Unified incident tracker: open incidents, status (discovery/investigation/containment/forensics/closed), assigned agents, timeline, root cause, closure date | Chadwick | Real-time (on status change) | All agents | Chadwick locks file during status transition; sequential updates enforced |
| **DETECTION_RULES.md** | Rule definitions (Sigma YAML), rule ownership, effectiveness metrics, tuning thresholds, false positive baseline | Teller | Post-incident (within 24h closure) + monthly review | Szilard (execution), Lawrence (compilation) | Teller authoritative; no concurrent edits; version control (git) for audit trail |
| **IOC_FEED.md** | Current indicators of compromise, YARA rules, behavioral hunt queries, threat intelligence integrations, invalidation timestamps | Fermi | Real-time (on hunt discovery) or 24h batched | Chadwick (for scope expansion), Szilard (for new alert rules) | Fermi authoritative for active IOCs; atomic writes (append-only, timestamp-versioned) |
| **CONTAINMENT_PROCEDURES.md** | Standardized playbooks: isolation, credential revocation, malware removal, network segmentation, EDR policies, rollback procedures by asset type | Compton | Post-incident (48h after closure) | Compton (execution), Meitner (forensic artifact targets) | Compton-Teller joint review; version control for audit compliance |
| **POST_INCIDENT_ACTIONS.md** | Remediation tracking: patches, rule rollout, config hardening, EDR policy updates, assigned owner, deployment status, completion ETA, closure sign-off | Teller | Weekly progress + final closure within 30 days | Compton (context), Meitner (forensic alignment), leadership (KPI tracking) | Teller authoritative; weekly status review meeting (all agents optional) |
| **DATA_AVAILABILITY.json** | SIEM index health, data source status (latency, event count), query performance metrics (percentiles), coverage gaps, retention status | Lawrence | Hourly (automated) | Szilard (alert query SLA), Chadwick (investigation queries), Fermi (hunt queries) | Lawrence authoritative; time-series metric DB (immutable append-only) |
| **FORENSIC_MANIFEST.json** | Artifact lineage: file names, hashes (SHA256), collection timestamps, collector identity, access audit log, integrity verification, chain of custody | Meitner | Per-incident (on closure) | Teller (root cause analysis), legal/compliance teams (regulatory closure, litigation) | Meitner authoritative; immutable once created; cryptographic signature for tampering detection |

**Concurrency Management:**
- INCIDENT_COMMAND.md: sequential status transitions (discovery → investigation → containment → forensics → closed); Chadwick gates transitions
- Forensic artifacts: Meitner has exclusive write access during collection; Teller reads only (post-closure)
- Rule updates: Teller has exclusive write access to DETECTION_RULES.md; Lawrence compiles asynchronously; Szilard reads only
- IOC_FEED.md: Fermi appends atomically; concurrent reads allowed; versioned snapshots for consistency

---

## Fabrication Priority

**PRIMARY (MUST FORGE FIRST): Lawrence (SIEM/Telemetry Gateway)**

### Rationale
All other agents depend on Lawrence as the foundational data layer. Without normalized, indexed, and queryable telemetry, no agent can execute:
- **Szilard** cannot ingest or filter alerts (requires indexed event_id, severity, confidence fields)
- **Chadwick** cannot build investigation timelines or correlate events (requires normalized timestamps, process chains, logon events)
- **Fermi** cannot execute hunts or validate IOCs (requires Zeek conn.log, dns.log, Sysmon event indices)
- **Compton** cannot verify containment success (requires post-action telemetry queries on Lawrence indices)
- **Meitner** cannot query forensic artifact status or timeline context (requires EVTX export availability from Lawrence)
- **Teller** cannot compile Sigma rules, measure detection effectiveness, or assess coverage gaps (requires statistical baseline from Lawrence)

### Forging Sequence (dependency order)

1. **Lawrence** — Establish SPL/KQL schemas for Windows Security Events, Sysmon, Zeek, Suricata, EDR; validate ingestion pipeline and query latency SLAs (sub-1sec for alert queries)

2. **Szilard** — Build alert filtering queries on Lawrence's indexed event_id, severity, confidence fields; establish noise baseline (7-day ±2σ) and filter rules

3. **Chadwick** — Construct timeline correlation queries on Lawrence's normalized process chains, logon events, network flows; validate incident declaration threshold (≥3 correlated events in ±60min window)

4. **Fermi** — Develop hunt query templates (PTH, kerberoasting, WMI lateral movement, exfiltration, C2 beaconing) on Lawrence indices; validate hunt result thresholds and IOC pivot logic

5. **Compton** — Implement containment action execution and post-containment verification queries on Lawrence (zero outbound connections, no process spawning); test isolation rollback procedures

6. **Meitner** — Establish forensic artifact collection and preservation procedures; validate hash verification, chain-of-custody logging, forensic target paths (EVTX, memory, disk snapshot)

7. **Teller** — Author Sigma rules (using outputs from Meitner's root cause findings), compile to SPL/KQL, deploy to Lawrence; measure rule effectiveness (TP%, FP%, MDR) and track patch deployment

**No agent is functional until Lawrence establishes the data foundation.** Parallel forging of Szilard-Compton-Fermi is safe only after Lawrence indexing is confirmed.

---

**END OF OUTPUT A**

---

# LIBRARY SPECIFICATION
*Authored by: Scintillator (T2 Detection Engineer) — for Lattice to implement*

---

## PURPOSE STATEMENT

Enable seven specialized agents to execute the defensive security operations incident lifecycle with knowledge persistence and progressive effectiveness improvement. Library provides:
- **Foundational schemas** (log normalization, SIEM index design) for Lawrence to operationalize first
- **Query templates** (alert filtering, correlation, hunts) with real-world thresholds and tuning guidance
- **Procedural playbooks** (containment, forensics, hardening) with ordering constraints and EDR-specific variations
- **Coordination protocols** (state file structure, conflict resolution, concurrency barriers)
- **Feedback loops** (rule effectiveness metrics, false positive root causes, post-incident rule propagation)

Library must support **state continuity**: each closed incident updates IOC feeds, detection rules, containment procedures, and hardening tasks—subsequent incident response benefits from prior closure patterns.

---

## SUGGESTED COLLECTIONS

| Collection | Agent Primary | Purpose | Content Examples | Priority |
|---|---|---|---|---|
| **SIEM Schema & Log Normalization** | Lawrence | Index design, field mapping, query syntax | Windows Event ID schemas (4624/4688/7045), Sysmon EventID mappings, Zeek conn/dns/http/ssl/files field definitions, retention policies, query performance SLA tuning | 🔴 **CRITICAL** |
| **Alert Triage & Noise Management** | Szilard | Filtering rules, baselines, severity assignment | Rolling 7-day ±2σ baseline calculation, event ID priority matrix, source-specific thresholds (Suricata vs EDR vs SIEM), benign process whitelist, suppression tactics | 🔴 **CRITICAL** |
| **Incident Investigation & Correlation** | Chadwick | Timeline correlation, behavioral baselines, scope determination | Process parent-child chains (legit vs anomalous), logon event correlation ±60min, privilege escalation markers (token elevation, SID analysis), PTH/kerberoasting/WMI lateral movement detection patterns, incident declaration threshold (≥3 events ±60min) | 🔴 **CRITICAL** |
| **Threat Hunting Query Templates** | Fermi | Hunt hypothesis structure, IOC pivot logic, baselines | PTH credential spray (logon_type=3 + NTLM reuse >3 assets), kerberoasting (4769 SPN + preauth_fail), WMI lateral movement (Sysmon 17 + svchost parent), C2 beaconing (Zeek conn consistency + dest_port anomaly), exfiltration staging (HTTP GET >100MB + external dest), behavioral baseline templates (Zeek per-asset dest_port P50/P95/P99) | 🔴 **CRITICAL** |
| **Containment Procedures & EDR Integration** | Compton | Action playbooks, asset-type variations, verification logic | Server isolation (network ACL + credential revoke + process kill), workstation block (EDR process kill + logon disable + RDP logoff), user account revocation (token logoff + password reset), post-containment verification (zero connections + no spawning for 600sec), EDR API templates (CrowdStrike REST payload, SentinelOne agent action format, Defender for Endpoint containment syntax), rollback procedures | 🔴 **CRITICAL** |
| **Forensic Preservation & Chain-of-Custody** | Meitner | Collection procedures, artifact targets, evidence lineage | Pre-containment snapshot ordering (Meitner→Compton sequencing), memory dump targets (injected code, process handles, C2 patterns), disk artifact targets (EVTX, Prefetch, $RECYCLE.BIN, AppData, registry hives), per-OS variations (Windows/Linux), hash verification (SHA256), tampering detection, legal admissibility thresholds (≥2 correlated sources) | 🔴 **CRITICAL** |
| **Detection Rule Library (Sigma)** | Teller | Rule templates, compilation guidance, effectiveness metrics | Sigma YAML structure (logsource, detection, threshold, false positive notes), SPL/KQL compilation examples, TP/FP rate calculation (baseline rolling median ±2σ), mean detection range (MDR) measurement, rule tuning decision tree (threshold adjustment if trend ±10%), rule ownership and audit trail, rule-to-MITRE-ATT&CK T-code mapping | 🟠 **HIGH** |
| **MITRE ATT&CK Coverage Mapping** | Teller | Gap analysis, heatmap generation, priority ranking | Enterprise tactics (TA0001 Initial Access through TA0010 Exfiltration), technique-to-rule mapping, coverage % by tactic, sector/org-size specific threat models (SMB vs Enterprise vs Critical Infrastructure), detection gaps visualization (techniques with 0 rules highlighted) | 🟠 **HIGH** |
| **Log Source Enablement & Troubleshooting** | Lawrence | Event forwarding config, Sysmon filters, sensor deployment | Windows Event Forwarding (WEF) subscription XML templates, Sysmon config.xml (event filtering by event ID and field), Zeek sensor placement and tuning (connection sampling, DNS query filtering), Suricata ruleset management, EDR agent deployment cmdlines, coverage validation queries (verify event arrival in hot index within 60sec), troubleshooting runbooks (no events in index = check WEF / Sysmon running / agent connectivity) | 🟠 **HIGH** |
| **False Positive Root Cause & Remediation** | Szilard, Teller | FP categorization, tuning guidance | FP types: (1) benign process in anomalous context (e.g., svchost.exe via explorer.exe = system UAC elevation, legitimate), (2) baseline deviation (e.g., scheduled backup tool creates >100 new processes daily), (3) rule misconfiguration (threshold too low, filter missing), (4) data quality (noisy event source). Remediation: filter add, threshold ±σ adjustment, process whitelist, rule disable for specific business unit. Root cause tracking CSV (FP_id, rule_id, detection_date, root_cause_category, remediation_action, effectiveness_reverification). | 🟠 **HIGH** |
| **Coordination Protocol & State Files** | All | File schemas, conflict resolution, locking strategy | INCIDENT_COMMAND.md JSON structure (incident_id, status, discovery_timestamp, assigned_investigator, containment_window, forensic_manifest_link), IOC_FEED.md atomic append structure, DETECTION_RULES.md versioning, sequential update enforcement (Chadwick gates INCIDENT_COMMAND status transitions), forensic artifact immutability and cryptographic signing, concurrent read-only access model | 🟠 **HIGH** |
| **EDR Telemetry Interpretation** | Compton, Chadwick, Fermi | API reference, field semantics, forensic artifact mapping | CrowdStrike Falcon event IDs (13=Regmod, 14=FileCreate, 27=WmiEvent), SentinelOne EventType codes (credential_dump, persistence, execution), Defender for Endpoint DeviceId/ProcessId linkage, memory injection detection (API call sequences: VirtualAllocEx→WriteProcessMemory→CreateRemoteThread), network connection correlation (EDR process tree ↔ Zeek conn.log by IPs/ports), lateral movement markers (runas, logon type 3, NTLM, Kerberos S4U delegation) | 🟡 **MEDIUM** |
| **Patch Management & Hardening Deployment** | Teller | CVE-to-patch mapping, SLA, deployment validation | CVE severity classification (critical RCE = 48h, high privilege escalation = 1 week, medium = 2 weeks, low = monthly), WSUS deployment status queries, GPO audit log parsing (4719 policy applied), post-patch verification (Event ID 4689 old exe vs new exe hash), rollback procedures (snapshot pre-patch, schedule rollback window, test on isolated VMs first) | 🟡 **MEDIUM** |
| **Root Cause Analysis & Prevention Rules** | Teller, Meitner | Analysis framework, hardening mapping, recurrence prevention | Categories: detection gap (no rule existed), log source missing (event not collected), false negative (rule tuned down), technical control missing (no EDR block). Prevention actions: new Sigma rule → test in audit mode 48h → measure TP/FP → deploy to Lawrence, config hardening (disable risky services, enforce MFA, restrict user execution), EDR policy updates, YARA rules for file/memory malware signatures. Post-incident task checklist with owner and ETA. | 🟡 **MEDIUM** |

---

## PRIORITY CONTENT TYPES

### Tier 1 (Must-Have for Lawrence-First Fabrication)

1. **SIEM Index Schemas**
   - Windows Security Event 4624/4625/4648/4688/4698/7045 field definitions + example events
   - Sysmon EventID 1/3/7/8/10/11/13/15/17/22 normalized field extraction
   - Zeek log format (conn.log, dns.log, http.log, ssl.log) with SPL/KQL query syntax
   - Suricata EVE JSON alert schema with severity/confidence mapping

2. **Query Latency & Retention SLAs**
   - Alert query baseline (≤1 sec for single-day indexed search, filter + group-by)
   - Hunt query baseline (≤300 sec for 90-day correlation across 3+ event types)
   - Real-time streaming latency (<100 ms from event generation to searchable)
   - Hot/Warm/Cold index transition strategy (0-30d hot, 31-90d warm, 91-365d cold)

3. **Alert Filtering Baselines**
   - 7-day rolling median ±2σ calculation methodology
   - Source-specific thresholds (e.g., Suricata avg 50 alerts/day → suppress if >median+2σ for 3 consecutive days)
   - Event ID priority matrix (HIGH: 4688/4698/7045; MEDIUM: 4624/4625/4648; LOW: 4616/4720)

### Tier 2 (Critical for Szilard-Chadwick-Fermi Parallel Execution)

4. **Incident Correlation Patterns**
   - PTH: 4624 logon_type=3 + NTLM auth_package + same hash >3 assets in ±60min → credentialreuse
   - Kerberoasting: 4769 TGS request + 4768 preauth_fail + target SPN in high-value list (SQL, Exchange, CIFS) → account compromise
   - WMI lateral: Sysmon 17 PipeCreated + parent=svchost.exe + dest_process∈{cmd.exe, powershell.exe} → RCE vector
   - Incident declaration: ≥3 correlated events in ±60min OR ≥1 critical event (4688 spawn from system context, 4648 elevation, data exfil marker) → escalate

5. **Hunt Query Templates (with Real Thresholds)**
   - Exfiltration: HTTP GET + uri∈{/download, /export} + response_body>100MB + dest_ip external + Zeek http.log + count ≥1 in 24h → flag
   - C2 Beaconing: Zeek conn.log + dest_ip single, dest_port∉[22,80,443,3389,53] + duration_sec median <2min + packet_count regular + connection_count >50 in 24h → callback server
   - Behavioral baseline: per-asset dest_port distribution (P50/P95); anomaly = dest_port not in top-10 historical + >3σ deviation

6. **Containment Playbook Matrix**
   - By asset type: Server (network isolate + credential revoke + process kill), Workstation (EDR block + logon disable + RDP logoff), Account (token logoff + password reset)
   - Pre-containment: Meitner snapshots memory/disk/EVTX; only then Compton acts
   - Post-containment verification: zero outbound conn for 600sec + no process spawning + no token elevation attempts

### Tier 3 (Support & Feedback Loops)

7. **Detection Rule Tuning & Effectiveness**
   - TP rate calculation: confirmed_detections / total_alerts; target ≥75%
   - FP rate baseline: rolling 7-day median ±2σ; adjust threshold if trend deviates ±10%
   - Mean Detection Range: hours from exploit execution to rule fire; target <4h network, <10min endpoint
   - Rule-to-MITRE-ATT&CK T-code mapping + coverage % by tactic

8. **Forensic Artifact Preservation**
   - Memory targets: injected code regions, process handles (open files, sockets, registry keys), malware API patterns
   - Disk targets: EVTX → C:\Windows\System32\winevt\logs, Prefetch → C:\Windows\Prefetch, $RECYCLE.BIN, AppData (browser history, login cookies), StartUp folders, registry hives (SYSTEM, SOFTWARE, SAM)
   - Chain-of-custody: artifact_id, hash_sha256, collection_timestamp (ISO-8601 UTC), collector_name, access audit log

9. **Coordination File Templates**
   - INCIDENT_COMMAND.json structure with status transitions (discovery → investigation → containment → forensics → closed)
   - IOC_FEED.md atomic append format (timestamp-versioned, immutable entries)
   - DETECTION_RULES.md versioning with git audit trail

---

## COVERAGE GAPS

| Gap | Impact | Remediation |
|---|---|---|
| **Alert source diversity (SIEM-vendor-specific schemas)** | Szilard cannot normalize alerts across Splunk vs Elasticsearch vs QRadar; delays triage routing | Add vendor-specific alert schema mappings (ES KQL alert type ≠ Splunk alert_severity field); build Szilard translation layer per source |
| **EDR platform variations (CrowdStrike vs SentinelOne vs Defender)** | Compton cannot execute uniform containment actions; API syntax and field semantics differ | Author EDR-specific playbook variants: 1) CrowdStrike REST API containment endpoint, 2) SentinelOne agent action cmdline, 3) Defender for Endpoint API payload; map common actions (process kill, isolation) to each platform |
| **Real-world MITRE ATT&CK heatmaps by org size/sector** | Teller cannot prioritize gap-filling rules; assumes uniform threat model across enterprise, SMB, healthcare, critical infrastructure | Build sector-specific threat heatmaps (SMB heavily hit by ransomware credential attack chains; healthcare by data exfil; critical infra by disruptive lateral movement); add detection rule priority per sector |
| **Incident severity classification criteria** | Chadwick declares escalation threshold based on "≥3 events" rule-of-thumb; missing explicit severity matrix | Define incident severity: **CRITICAL** (confirmed data exfil or active RCE), **HIGH** (privilege escalation chain + lateral movement), **MEDIUM** (detected intrusion, scope unclear), **LOW** (potential reconnaissance); tie to containment urgency SLA (CRITICAL = <5min, HIGH = <30min, MEDIUM = <2h) |
| **False positive root cause catalog** | Teller remediates FP ad-hoc; misses patterns across incidents | Maintain FP root cause register: (1) benign process in anomalous context (UAC elevation, svchost via explorer), (2) baseline deviation (scheduled backup tool exceptions), (3) rule misconfiguration (threshold too aggressive), (4) data quality (noisy event source). Link to remediation playbook per category. |
| **Forensic artifact extraction for non-Windows OSs** | Meitner targets Windows paths; Linux/macOS servers absent | Add forensic guides: Linux (syslog → /var/log, bash history → ~/.bash_history, process accounting → /var/log/account), macOS (unified log → /var/log/system.log, BSM audit → /var/audit) |
| **Patch deployment validation without golden image** | Teller deploys patches; post-deployment verification is manual | Build automated post-patch verification: WSUS deployment status query + Event ID 4689 (process terminated) hash comparison (pre-patch binary hash ≠ post-patch) + crash rate monitoring (spike = rollback) |
| **Containment window trade-offs (data loss vs rapid isolation)** | Compton isolates immediately; risk of incomplete forensics or log truncation | Add containment mode spectrum: **Immediate** (isolation first, then forensics retroactively via EDR telemetry), **Monitored** (isolation with 10-min pre-snapshot, then block egress only), **Honeypot** (beaconing allowed but monitored for attacker behavior, then sudden cutoff) |
| **Incident state consistency under concurrent access** | Multiple agents write to INCIDENT_COMMAND.md simultaneously → race condition, state corruption | Lock protocol: sequential status transitions only (Chadwick holds exclusive write lock); other agents append to immutable sub-files (HUNT_RESULTS.csv, CONTAINMENT_LOG.json) instead; periodic consistency check (sha256 INCIDENT_COMMAND.md before/after critical transitions) |

---

## UPDATE FREQUENCY

| Content Type | Update Cadence | Trigger | Owner | Consumer Latency Tolerance |
|---|---|---|---|---|
| **IOC Feed (IOC_FEED.md)** | Real-time (atomic append) or 24h batch | Hunt discovery; threat intel updates | Fermi | <5 min (active hunt pivot), 24h (batch rules) |
| **Incident Command (INCIDENT_COMMAND.md)** | Real-time (on status change) | Alert escalation, containment decision, forensic completion, closure decision | Chadwick | <1 min (routing to responder) |
| **Detection Rules (DETECTION_RULES.md)** | Post-incident (within 24h closure) + monthly review | Root cause analysis (new rule needed), tuning (TP/FP trend ±10%), policy update (regulatory, audit) | Teller | 24h (rule rollout after incident), 7d (monthly review publication) |
| **Containment Procedures (CONTAINMENT_PROCEDURES.md)** | Post-incident (48h after closure) | Root cause mitigation, EDR policy update, process refinement | Compton + Teller joint | Ongoing (persists until superceded) |
| **Forensic Manifest (FORENSIC_MANIFEST.json)** | Per-incident (on closure) | Artifact collection complete | Meitner | Post-closure (read by Teller, legal/compliance) |
| **Hunt Baseline Thresholds** | Daily refresh (automated) | Zeek conn.log statistics update (per-asset dest_port P50/P95/P99), Sysmon event volume baseline | Lawrence (automated) | <5 min (Fermi reads for hunt queries) |
| **Rule Effectiveness Metrics (TP/FP/MDR)** | Weekly aggregation + monthly deep review | Alert statistics batch (SPL saved search every 7 days), tuning decisions (monthly trend analysis) | Teller | 7d (Szilard reads for filter tuning), 30d (Teller reads for rule tuning) |
| **Log Source Availability (DATA_AVAILABILITY.json)** | Hourly automated health check | Lawrence monitoring daemon (event lag, index size, query latency percentiles) | Lawrence | <1 min (Szilard, Chadwick, Fermi read on demand) |
| **MITRE ATT&CK Coverage Heatmap** | Monthly after-action review | Closed incident root causes analyzed; new rules deployed; gap coverage recalculated | Teller | Ongoing (used for next-month hunt prioritization) |
| **Patch Deployment Status** | Weekly progress tracking | WSUS/SCCM query every 7d; post-deployment verification test | Teller | Ongoing (leadership KPI, monthly closure sign-off) |
| **False Positive Root Cause Register** | Weekly ingestion + monthly categorization | Each incident closure triggers FP root cause check; categorized into types (benign context, baseline deviation, rule config, data quality) | Szilard, Teller | Monthly (trend analysis, remediation planning) |

---

**END OF OUTPUT B**

*Specification ready for Lattice implementation. Prioritize Tier 1 collections (SIEM schemas, alert filtering, incident correlation, hunt templates, containment playbooks, forensics) before Tier 2 feedback loops. Address coverage gaps (EDR platform variations, incident severity matrix, FP root cause catalog) in Wave 2.*

---

# LATTICE COLLECTION DESIGN

# LATTICE COLLECTION DESIGN: DEFENSIVE SECURITY OPERATIONS
*Phase 2b — T2 Library Specification → Lattice Collection Design*  
*For operator review and approval before fabrication*

---

## Assessment of Library Specification

The T2 Library Specification is **complete and highly actionable**. Scintillator has provided authoritative guidance on agent roles, data sources, query languages, coordination protocols, and priority content types with concrete thresholds (7-day ±2σ baselines, ≥3-event incident declaration, <1 sec alert query SLA). The specification includes coverage gaps and remediation strategies, signaling mature domain modeling.

**Minimal assumptions filled:** (1) Coordination files (INCIDENT_COMMAND.md, IOC_FEED.md, etc.) are maintained as external state files with vector indexing for searchability, not vector store as SSOT. (2) Real-time IOC updates use write-through; incident artifacts use eventual consistency. (3) Chunking varies by content type: document-level for playbooks, semantic for patterns, structured metadata for rules.

**Operator clarifications needed:** (1) Should INCIDENT_COMMAND.md index on every status change or periodic snapshots? (2) Write-through vs. batch for Teller's DETECTION_RULES.md updates? (3) Sigma rule chunking granularity: full rule YAML or semantic extraction of detection logic?

---

## Collection Architecture

### 1. SIEM_SCHEMA_AND_NORMALIZATION
**Purpose:** Index design, log normalization schemas, field mapping reference, query latency/retention SLAs—foundational for all telemetry queries.  
**Source of truth:** T2 Library Specification — "SIEM Schema & Log Normalization" + Tier 1 "SIEM Index Schemas"  
**Content type:** Structured documents (schema definitions, example queries, field mappings)  
**Chunking strategy:** Document-level with metadata (log source type, event ID range, query language)  
**Embedding model:** all-MiniLM-L6-v2 — reason: technical schema retrieval, not security domain-specific language  
**Ingest sources:** Windows Security Event ID schema docs (4624/4625/4688/4698/7045/7046), Sysmon EventID 1/3/7/8/10/11/13/15/17/22 field definitions, Zeek log format specs (conn.log, dns.log, http.log, ssl.log), Suricata EVE JSON alert schema, SPL/KQL syntax guides  
**Refresh cadence:** Monthly (on vendor log format updates or SIEM tool version upgrades)  
**Mandatory metadata fields:** status (active/deprecated), source_system (Windows/Sysmon/Zeek/Suricata), query_language (SPL/KQL), field_name, data_type, retention_tier (hot/warm/cold)  
**Estimated collection size:** ~50–80 documents (schemas + ~10 per log source)

### 2. ALERT_TRIAGE_AND_NOISE_MANAGEMENT
**Purpose:** Alert filtering rules, rolling baseline calculation methodology, severity assignment matrices, benign process whitelists.  
**Source of truth:** T2 Library Specification — "Alert Triage & Noise Management" + Tier 1 "Alert Filtering Baselines"  
**Content type:** Structured entries (filter rules, threshold tables, baseline calculation examples)  
**Chunking strategy:** Rule-level with metadata (source system, event ID, threshold formula, baseline date)  
**Embedding model:** CySecBERT — reason: alert context (event ID semantics, severity mapping, benign vs. malicious process names)  
**Ingest sources:** Szilard's alert filter documentation, rolling 7-day ±2σ baseline calculation methodology, source-specific thresholds (Suricata avg 50 alerts/day, EDR platform-specific alert rates), benign process whitelist (svchost.exe system contexts, Windows Update processes, AV scanning)  
**Refresh cadence:** Real-time (new filter rules appended on filter_applied event); baseline metrics daily refresh  
**Mandatory metadata fields:** filter_id, source_system, event_id, threshold_type (median±2σ / static / dynamic), baseline_start_date, baseline_end_date, false_positive_count (rolling 7d)  
**Estimated collection size:** ~100–150 entries (filter rules + per-source baselines)

### 3. INCIDENT_INVESTIGATION_AND_CORRELATION
**Purpose:** Correlation patterns, behavioral baselines (legit vs. anomalous), incident declaration thresholds, process parent-child chains, privilege escalation markers.  
**Source of truth:** T2 Library Specification — "Incident Investigation & Correlation" + Tier 2 "Incident Correlation Patterns"  
**Content type:** Mixed (pattern templates, narrative behavioral baselines, detection logic examples)  
**Chunking strategy:** Pattern-level (e.g., one chunk per correlation type: PTH, Kerberoasting, WMI lateral, privilege escalation)  
**Embedding model:** CySecBERT — reason: Windows event semantics (logon types, token elevation, SID analysis), attack chain context  
**Ingest sources:** Chadwick's correlation logic documentation (4624+4688 parent-child chains, ±60min correlation window), behavioral baseline templates (explorer→notepad normal, svchost→cmd anomalous), incident declaration threshold (≥3 correlated events ±60min OR ≥1 critical event + context)  
**Refresh cadence:** Post-incident (on closure, Chadwick documents new correlation patterns discovered); monthly trend review  
**Mandatory metadata fields:** pattern_id, attack_type (PTH/Kerberoasting/WMI/Privilege_Escalation), event_ids (array), correlation_window_seconds, confidence_threshold, discovery_source (incident_id / hunt_result)  
**Estimated collection size:** ~30–50 patterns (covering MITRE ATT&CK tactics used in enterprise environments)

### 4. THREAT_HUNT_QUERY_TEMPLATES
**Purpose:** Hunt hypothesis structure, IOC pivot logic, behavioral anomaly baselines (Zeek dest_port distribution, C2 beaconing signatures, exfiltration detection).  
**Source of truth:** T2 Library Specification — "Threat Hunting Query Templates" + Tier 2 "Hunt Query Templates (with Real Thresholds)"  
**Content type:** Code + structured metadata (SPL/KQL queries, threshold values, false positive notes)  
**Chunking strategy:** Query-level with metadata (hunt hypothesis, MITRE tactic, required data sources, threshold values)  
**Embedding model:** CySecBERT — reason: TTP context, behavioral anomaly descriptions, attack indicator language  
**Ingest sources:** Fermi's hunt template library (PTH credential spray, Kerberoasting SPN targeting, WMI lateral, C2 beaconing, exfiltration staging), Zeek behavioral baselines (per-asset dest_port P50/P95/P99 percentiles, DNS entropy calculation, HTTP response_body >100MB threshold), behavioral baseline automation scripts  
**Refresh cadence:** Weekly (as threats evolve and new TTPs emerge); after-incident discovery (new hunt developed → added to library)  
**Mandatory metadata fields:** hunt_id, hypothesis_name, mitre_tactic, required_datasources (array), threshold_values (JSON), confidence_level, false_positive_risk, last_validated_date  
**Estimated collection size:** ~40–60 hunt templates (covering core attack chains: reconnaissance, lateral movement, exfiltration, persistence, C2)

### 5. IOC_AND_THREAT_INTELLIGENCE_CATALOG
**Purpose:** Live indicators of compromise, YARA rules, behavioral search queries, threat intelligence integrations, burn status (valid/invalidated).  
**Source of truth:** T2 Library Specification — IOC_FEED.md (Fermi-authored, real-time atomic append)  
**Content type:** Structured entries (IoC hash/IP/domain, YARA rule, behavioral query, metadata)  
**Chunking strategy:** IOC-level (one chunk per indicator or YARA rule, with metadata prefix for quick filtering)  
**Embedding model:** CySecBERT — reason: malware TTP embedding, IoC semantic similarity (hash families, domain registration patterns)  
**Ingest sources:** Fermi's hunt results (matched IoCs from threat hunts), external threat feeds (VirusTotal, Shodan, AlienVault OTX), incident root cause artifacts (Meitner forensic findings), YARA rule repository  
**Refresh cadence:** Real-time (Fermi appends on hunt discovery); batch invalidation (daily purge of burn status=invalidated after 30d)  
**Mandatory metadata fields:** ioc_id, ioc_type (hash/IP/domain/YARA), ioc_value, discovery_date, discovery_source (hunt_result_id / threat_feed), burn_status (active/invalidated), confidence_level, linked_incident_ids (array)  
**Estimated collection size:** ~500–2000 entries (grows per incident; active IoCs unbounded, invalidated purged after 30d)

### 6. CONTAINMENT_PROCEDURES_AND_EDR_REFERENCE
**Purpose:** Standardized playbooks by asset type (server/workstation/account), EDR platform-specific API variations, post-containment verification logic.  
**Source of truth:** T2 Library Specification — "Containment Procedures & EDR Integration" + "EDR Telemetry Interpretation"  
**Content type:** Mixed (playbook documents, API reference tables, EDR platform specific guides)  
**Chunking strategy:** Asset-type + action-level (e.g., "Server_Isolation" chunk includes network ACL, credential revoke, process kill, verification; separate chunks per EDR platform for API syntax)  
**Embedding model:** CySecBERT — reason: EDR API semantics, containment action sequencing, asset-type context (server vs. workstation implications)  
**Ingest sources:** Compton's containment playbook documentation (Server: network isolate + credential revoke + process kill; Workstation: EDR block + logon disable + RDP logoff; Account: token logoff + password reset), EDR API reference (CrowdStrike Falcon REST /devices/actions/contain endpoint, SentinelOne agent action syntax, Defender for Endpoint containment payload), post-containment verification queries (zero outbound conn + no spawning for 600sec)  
**Refresh cadence:** Post-incident (Compton-Teller joint review, 48h after closure); on EDR vendor update (API version change)  
**Mandatory metadata fields:** procedure_id, asset_type (Server/Workstation/Account), action_name, edr_platform (CrowdStrike/SentinelOne/Defender/Generic), sequence_order, verification_query, success_criteria, rollback_available (boolean)  
**Estimated collection size:** ~40–60 procedures (3 asset types × 4 EDR platforms × 3–5 actions each)

### 7. FORENSIC_PRESERVATION_AND_CHAIN_OF_CUSTODY
**Purpose:** Pre-containment/post-containment snapshot procedures, forensic artifact targets (memory, disk, logs), chain-of-custody templates, legal admissibility thresholds.  
**Source of truth:** T2 Library Specification — "Forensic Preservation & Chain-of-Custody" + Tier 1 "Forensic Artifact Preservation"  
**Content type:** Procedural documents + structured metadata (artifact target paths, hash verification, collection method)  
**Chunking strategy:** Document-level for OS-specific guides (Windows vs. Linux vs. macOS); structured metadata for artifact targets  
**Embedding model:** CySecBERT — reason: forensic artifact semantics (registry hive forensic targets, memory injection patterns, EVTX event type meaning)  
**Ingest sources:** Meitner's forensic preservation workflow (pre-containment ordering, snapshot within 60sec, hash verification SHA256), artifact target guides (Windows: EVTX, Prefetch, $RECYCLE.BIN, AppData, registry; Linux: syslog, bash_history; macOS: unified log), chain-of-custody template (artifact_id, hash, collection_timestamp, collector_name, access_audit_log), legal admissibility threshold (≥2 correlated sources required)  
**Refresh cadence:** Per-incident (on closure); OS-specific guides reviewed quarterly (new forensic targets emerge, tool updates)  
**Mandatory metadata fields:** artifact_id, artifact_type (Memory/Disk/EVTX/PCAP), target_path, collection_method (EDR_API/native_dump/SIEM_export), hash_sha256, collection_timestamp (ISO-8601 UTC), collector_name, chain_of_custody_complete (boolean), legal_hold_status  
**Estimated collection size:** ~25–40 procedure documents + ~200–500 per-incident artifact entries (appended, never deleted for legal compliance)

### 8. SIGMA_DETECTION_RULES_AND_METRICS
**Purpose:** Sigma YAML rule templates, SPL/KQL compilation examples, tuning parameters, effectiveness metrics (TP%, FP%, MDR), rule ownership and audit trail.  
**Source of truth:** T2 Library Specification — "Detection Rule Library (Sigma)" + DETECTION_RULES.md  
**Content type:** Code + structured metadata (Sigma YAML, compiled queries, metrics table)  
**Chunking strategy:** Rule-level (one chunk per Sigma rule with compilation outputs, tuning notes, metrics)  
**Embedding model:** CySecBERT — reason: Sigma rule semantics, detection logic language, CVE/TTP context in rule names  
**Ingest sources:** Teller's Sigma rule repository (lateral movement, privilege escalation, data exfil, C2 beaconing rules), SPL/KQL compiled versions, rule effectiveness metrics (TP rate, FP rate rolling 7d ±2σ, MDR hours), tuning decision tree (threshold ±σ adjustment if trend ±10% deviates)  
**Refresh cadence:** Post-incident (new rule authored within 24h of closure); monthly tuning review (TP/FP trend analysis)  
**Mandatory metadata fields:** rule_id, rule_name, rule_status (test/tuned/production/deprecated), author, last_updated, effectiveness_metrics (TP_rate, FP_rate_baseline, MDR_hours), tuning_notes, MITRE_T_codes (array), alert_tier (High/Medium/Low)  
**Estimated collection size:** ~80–150 rules (covering critical enterprise tactics per MITRE ATT&CK)

### 9. MITRE_ATT&CK_COVERAGE_AND_GAPS
**Purpose:** Threat model heatmaps by organization size/sector, technique-to-rule mapping, coverage % by tactic, detection gaps visualization.  
**Source of truth:** T2 Library Specification — "MITRE ATT&CK Coverage Mapping" + gap analysis  
**Content type:** Structured metadata (heatmap tables, gap rankings, sector-specific threat profiles)  
**Chunking strategy:** Tactic-level (one chunk per MITRE tactic with covered/uncovered techniques, relevant rules, sector-specific threat priority)  
**Embedding model:** all-MiniLM-L6-v2 — reason: technical taxonomy lookup, not security narrative  
**Ingest sources:** Teller's MITRE ATT&CK mapping (Enterprise tactics TA0001–TA0010), technique-to-rule crosswalk (technique T1566 → rule_ids [rule_123, rule_456]), coverage % calculation (techniques with ≥1 rule / total techniques per tactic), sector-specific threat heatmaps (SMB: ransomware + credential attacks HIGH; Healthcare: data exfil HIGH; Critical Infra: disruptive lateral movement HIGH)  
**Refresh cadence:** Monthly after-action review (new rules deployed → recalculate coverage %; closed incidents → identify covered/uncovered techniques)  
**Mandatory metadata fields:** tactic_id, tactic_name, sector (SMB/Enterprise/Healthcare/CriticalInfra), technique_id, technique_name, coverage_status (covered/gap), linked_rule_ids (array), threat_priority (High/Medium/Low), remediation_owner  
**Estimated collection size:** ~200–400 entries (14 tactics × ~20–30 techniques per tactic across sectors)

### 10. EDR_PLATFORM_TELEMETRY_REFERENCE
**Purpose:** Platform-specific event ID/type definitions, field semantics, forensic artifact mapping (CrowdStrike/SentinelOne/Defender for Endpoint).  
**Source of truth:** T2 Library Specification — "EDR Telemetry Interpretation" + VRA "Forensic Artifact Mapping"  
**Content type:** Reference documents (API field definitions, event type semantics, memory/file injection detection patterns)  
**Chunking strategy:** Platform + event-type level (e.g., "CrowdStrike_Event_13_RegMod" chunk with field definitions, forensic significance, related memory patterns)  
**Embedding model:** CySecBERT — reason: EDR event semantics, forensic artifact association  
**Ingest sources:** EDR platform API documentation (CrowdStrike EventType codes, SentinelOne event types, Defender for Endpoint DeviceId/ProcessId linkage), field semantics reference (GrantedAccess flags for process memory access, ImageLoaded DLL injection detection), lateral movement markers (runas, logon type 3, NTLM, Kerberos S4U delegation)  
**Refresh cadence:** Quarterly (on EDR vendor API version update or major capability release)  
**Mandatory metadata fields:** platform_name, event_type_id, event_type_name, field_name, field_type, forensic_significance (high/medium/low), related_injection_patterns (array), correlated_event_types (array)  
**Estimated collection size:** ~60–100 reference documents (3 platforms × 10–15 critical event types each + field definitions)

### 11. POST_INCIDENT_HARDENING_AND_REMEDIATION
**Purpose:** Root cause analysis categorization framework, patch SLA by CVE severity, RCA remediation mapping, recurrence prevention playbook.  
**Source of truth:** T2 Library Specification — "Root Cause Analysis & Prevention Rules" + POST_INCIDENT_ACTIONS.md  
**Content type:** Mixed (RCA framework documentation, remediation playbook, patch deployment guidance)  
**Chunking strategy:** Root-cause-category-level (Detection Gap, Log Source Missing, False Negative, Technical Control Missing); remediation action-level (new Sigma rule, config hardening, EDR policy update)  
**Embedding model:** CySecBERT — reason: RCA category semantics, remediation action context, CVE/TTP linkage  
**Ingest sources:** Teller's RCA framework (categories: detection gap → author Sigma rule + test 48h; log source missing → enable WEF/Sysmon; false negative → re-tune threshold ±σ; technical control missing → implement EDR block / hardening config), patch deployment SLA (critical RCE 48h, high privilege escalation 1 week, medium 2 weeks, low monthly), hardening action playbook (disable risky services, enforce MFA, restrict user execution), post-patch verification (WSUS status + Event 4689 hash comparison + crash rate monitoring)  
**Refresh cadence:** Weekly progress tracking; post-incident (RCA completed within 30d of closure)  
**Mandatory metadata fields:** rca_id, incident_id, root_cause_category, remediation_action, action_owner, deployment_status (pending/in_progress/deployed), target_completion_date, effectiveness_reverification_flag  
**Estimated collection size:** ~20–30 RCA templates + per-incident remediation tracking (unbounded, archived per incident)

### 12. INCIDENT_LIFECYCLE_COORDINATION_PROTOCOL
**Purpose:** State file schemas, conflict resolution rules, sequential update enforcement, concurrent access model, ordering constraints (Meitner→Compton, Chadwick gates transitions).  
**Source of truth:** T2 Library Specification — "Coordination File Design" table + protocol definitions  
**Content type:** Structured metadata (JSON/YAML file templates, conflict resolution rules, locking strategy)  
**Chunking strategy:** File-type-level (INCIDENT_COMMAND.md schema + conflict resolution, IOC_FEED.md atomic append protocol, DETECTION_RULES.md versioning, etc.)  
**Embedding model:** all-MiniLM-L6-v2 — reason: protocol mechanics, not security domain knowledge  
**Ingest sources:** Specification's Coordination File Design table (INCIDENT_COMMAND.md: discovery→investigation→containment→forensics→closed state machine; IOC_FEED.md: Fermi appends atomically; DETECTION_RULES.md: Teller exclusive write; FORENSIC_MANIFEST.json: Meitner immutable + cryptographic signature), conflict resolution rules (sequential status transitions, forensic artifact immutability, write-through for hot data IOC_FEED vs. eventual consistency for incidents), ordering constraints (Meitner snapshot pre-containment, Compton acts only after status=forensics_collected)  
**Refresh cadence:** One-time ingestion at swarm setup; updates only if coordination protocol changes (e.g., new state field added)  
**Mandatory metadata fields:** file_name, primary_owner (Chadwick/Fermi/Teller/Meitner/All), access_model (exclusive_write/atomic_append/read_only), conflict_resolution_strategy, update_trigger, consumer_list (array), retention_policy  
**Estimated collection size:** ~10–15 protocol documents (one per coordination file + shared state machine definition)

---

## Implementation Notes

1. **Real-time IOC updates (IOC_FEED.md):** Fermi appends discoveries atomically; vector store should support write-through indexing (<1 sec latency) or polling refresh every 60 sec. Recommend write-through if infrastructure allows, else async indexing with versioned snapshots.

2. **Coordination files as external state sources:** INCIDENT_COMMAND.md, DETECTION_RULES.md, and forensic artifacts remain the source of truth (immutable audit trail); vector store indexes them for agent retrieval but **never overwrites**. Agents read vector store; write to external files. This preserves forensic chain of custody and audit compliance.

3. **Chunking complexity (Sigma YAML rules):** Full rule YAML is readable but may embed unused filter logic. Recommend **semantic extraction** for chunks: separate chunks for (1) detection logic (selection + condition), (2) false positive notes, (3) tuning parameters. This improves retrieval precision when agents search for "rules that detect privilege escalation" vs. "what are common false positives in process creation rules?"

4. **EDR platform variations:** Three separate sub-collections (CrowdStrike_Reference, SentinelOne_Reference, Defender_Reference) or single unified collection with metadata filtering by `edr_platform` field. Recommend unified collection to keep related API docs co-embedded (better semantic retrieval for cross-platform containment lookup).

5. **Forensic artifact immutability:** FORENSIC_MANIFEST.json entries are append-only; no deletion. Metadata field `chain_of_custody_complete` gates read access—archived artifacts (completed investigations) remain retrievable for audit but flagged as closed. Implement via document-level versioning + cryptographic hash on write.

6. **Search latency SLA:** Alert queries on ALERT_TRIAGE_AND_NOISE_MANAGEMENT and SIEM_SCHEMA_AND_NORMALIZATION must return within 100 ms (Szilard is operational gatekeeper). Hunt queries on THREAT_HUNT_QUERY_TEMPLATES + behavioral baselines <500 ms acceptable (Fermi is backgrounded). Consider separate "hot" collection (active IoCs, running hunts) vs. "warm" (archived rules, closed incidents) if latency becomes constraint.

7. **Real-world coverage gap:** Specification mentions "Alert source diversity (SIEM-vendor-specific schemas)" and "Incident severity classification criteria." Recommend adding **INCIDENT_SEVERITY_MATRIX** collection (small: 4–6 entries mapping CRITICAL/HIGH/MEDIUM/LOW to response SLA and containment urgency). This is a must-have before field deployment.

---

## Questions for Operator

1. **INCIDENT_COMMAND.md indexing cadence:** Should the vector store index state changes in real-time (status transition triggers re-embed), or on periodic snapshots (e.g., hourly)? Real-time is higher accuracy but higher compute cost; snapshots reduce index churn but agents may read stale state.

2. **Write-through vs. batch for Teller's DETECTION_RULES.md updates:** When Teller authors a new rule post-incident, should it appear in the vector store within <1 min (write-through, requires tight infrastructure coupling), or on the next daily batch refresh? Affects Szilard's ability to immediately use new rules for alert triage.

3. **Chunking granularity for Sigma YAML rules:** (a) Full rule YAML in single chunk with metadata prefix, or (b) semantic extraction with separate chunks for detection logic, false positive notes, tuning parameters? Option (b) improves retrieval precision but requires parsing logic.

4. **Forensic artifact query pattern:** Meitner's FORENSIC_PRESERVATION_AND_CHAIN_OF_CUSTODY contains both procedural guides (how to collect) and artifact metadata (hash, timestamp, collector). Should agents query by {procedure type, required artifact, asset OS} or {incident_id, artifact hash, legal hold status}? Affects chunk structure.

5. **Incident severity matrix:** Specification mentions "CRITICAL/HIGH/MEDIUM/LOW" classification but no explicit matrix. Recommend **operator supplies** severity SLA thresholds (e.g., CRITICAL = <5 min containment response, HIGH = <30 min). Should this be a new collection or embedded in Incident_Investigation_and_Correlation?

6. **EDR platform priority for fabrication:** Should we prioritize one EDR platform's API reference (e.g., CrowdStrike) in initial fabrication, then add SentinelOne/Defender later? Or ingest all three upfront? Affects initial content volume and agent VRP complexity.

---

## Vector Retrieval Protocol Skeleton

**Pre-fill the VRP that Fermi will embed in agents. Agents do not invoke retrieval directly—the engine pre-fetches and injects. VRP specifies which collections are relevant, query formulation guidance, injection point, citation format, and fallback behavior.**

---

### **SZILARD (Alert Triage Officer)**
- **Collections:** `ALERT_TRIAGE_AND_NOISE_MANAGEMENT`, `SIEM_SCHEMA_AND_NORMALIZATION`
- **Query trigger:** On new alert ingestion; before severity assignment
- **Query formulation:** `"filter rules for [source_system] alerts with event_id [event_id]"` + `"rolling baseline for [source_system] alert volume"`
- **Injection point:** Prepend retrieved baseline + filter rules to alert processing logic (before severity calculation)
- **Citation format:** `[Rule ID: xyz, source: ALERT_TRIAGE_AND_NOISE_MANAGEMENT]` in triage decision log
- **Fallback (MANDATORY):** If baseline unavailable, use static threshold (median of last 7 days in local cache); flag as `baseline_quality=degraded` in alert record. If filter rules unavailable, apply conservative filter (event_id in HIGH priority matrix only).

---

### **CHADWICK (Incident Investigator)**
- **Collections:** `INCIDENT_INVESTIGATION_AND_CORRELATION`, `SIEM_SCHEMA_AND_NORMALIZATION`, `MITRE_ATT&CK_COVERAGE_AND_GAPS`
- **Query trigger:** On incident escalation; on timeline correlation request; on scope determination
- **Query formulation:** `"correlation pattern for [attack_type] using event_ids [list]"` + `"behavioral baseline for [process_parent] and [process_child]"` + `"MITRE techniques related to [observed_indicator]"`
- **Injection point:** Prepend correlation patterns + behavioral baselines after initial alert triage; append MITRE technique context to incident summary
- **Citation format:** `[Pattern ID: xyz from INCIDENT_INVESTIGATION_AND_CORRELATION, confidence: 0.85]` in timeline; `[MITRE T1234 from MITRE_ATT&CK_COVERAGE_AND_GAPS]` in impact assessment
- **Fallback (MANDATORY):** If correlation patterns unavailable, fall back to simple event count (≥3 events in ±60min = incident declared); if behavioral baselines unavailable, conservatively flag all suspicious parent-child combos (svchost→cmd, explorer→powershell, etc.) as anomalous.

---

### **FERMI (Threat Hunter)**
- **Collections:** `THREAT_HUNT_QUERY_TEMPLATES`, `IOC_AND_THREAT_INTELLIGENCE_CATALOG`, `INCIDENT_INVESTIGATION_AND_CORRELATION`
- **Query trigger:** On hunt initiation; on hourly scheduled baseline hunts; on Chadwick request for "find related undetected activity"
- **Query formulation:** `"hunt template for [hypothesis_name]"` + `"IOCs of type [ioc_type] from [incident_id] or active feed"` + `"behavioral baseline for [metric] (dest_port distribution, DNS entropy, HTTP response size)"`
- **Injection point:** Prepend hunt template + IOCs + baselines to hunt query execution (before SIEM search)
- **Citation format:** `[Hunt ID: hz123 from THREAT_HUNT_QUERY_TEMPLATES, threshold: [values]]` in hunt results; `[IOC: xxx from IOC_CATALOG, confidence: 0.92]` in matched results
- **Fallback (MANDATORY):** If hunt templates unavailable, revert to manual query formulation (Fermi writes raw SPL/KQL); log as `template_quality=unavailable`. If IOC catalog missing, continue hunt with operator-supplied IoCs only. If behavioral baselines missing, use default thresholds (e.g., C2 beaconing = >50 connections in 24h to single IP, <2 min median duration).

---

### **COMPTON (Incident Responder)**
- **Collections:** `CONTAINMENT_PROCEDURES_AND_EDR_REFERENCE`, `SIEM_SCHEMA_AND_NORMALIZATION`
- **Query trigger:** On containment decision from Chadwick; on post-containment verification request
- **Query formulation:** `"containment playbook for [asset_type] using [edr_platform]"` + `"post-containment verification query for [action_name]"` + `"EDR API format for [platform] action [action_type]"`
- **Injection point:** Prepend containment playbook + EDR API syntax before action execution; append verification query after action completes
- **Citation format:** `[Procedure ID: proc_456 from CONTAINMENT_PROCEDURES_AND_EDR_REFERENCE, edr_platform: CrowdStrike]` in action log; `[Verification Query: result=PASS/FAIL based on [criteria]]`
- **Fallback (MANDATORY):** If playbook unavailable, Compton escalates to operator for manual containment approval (cannot execute without procedural validation). If EDR API reference missing, fall back to generic containment steps (network isolate, process kill via native OS commands if EDR unavailable). Verification always required—if queries fail to return, mark containment as `verification_incomplete=true` and re-check after 60 sec.

---

### **MEITNER (Forensic Analyst)**
- **Collections:** `FORENSIC_PRESERVATION_AND_CHAIN_OF_CUSTODY`, `SIEM_SCHEMA_AND_NORMALIZATION`, `EDR_PLATFORM_TELEMETRY_REFERENCE`
- **Query trigger:** On pre-containment snapshot request from Chadwick; on artifact target definition request; on post-incident chain-of-custody documentation
- **Query formulation:** `"forensic artifact targets for [os_type] (Windows/Linux/macOS)"` + `"collection procedure for [asset_type]"` + `"EDR memory/file injection detection patterns from [edr_platform]"`
- **Injection point:** Prepend artifact targets + collection procedure at snapshot start; append chain-of-custody metadata after collection completion
- **Citation format:** `[Artifact ID: art_789 collected via [method], hash: sha256_xxx, from FORENSIC_PRESERVATION_AND_CHAIN_OF_CUSTODY]` in manifest; legal hold + cryptographic signature appended
- **Fallback (MANDATORY):** If artifact target guide unavailable, Meitner collects standard forensic package (memory dump, EVTX export, disk image snapshot); marks as `target_guidance=missing, collection_method=standard_package`. Chain-of-custody is non-negotiable—if any field cannot be populated (collector_name, timestamp, hash), the artifact is flagged as `admissibility=questionable` and escalated to operator for manual verification before legal/compliance use.

---

### **LAWRENCE (SIEM/Telemetry Gateway)**
- **Collections:** `SIEM_SCHEMA_AND_NORMALIZATION`, `ALERT_TRIAGE_AND_NOISE_MANAGEMENT` (reference only—Lawrence is the source)
- **Query trigger:** On index health check (hourly); on agent request for schema validation; on query performance SLA verification
- **Query formulation:** `"log schema for [source_system]"` + `"expected field names and types for [event_id]"` + `"query performance baseline for [query_type]"`
- **Injection point:** Append schema reference to index validation daemon (verify incoming events match expected schema); prepend SLA baseline to query performance monitoring
- **Citation format:** `[Schema from SIEM_SCHEMA_AND_NORMALIZATION, version: 2026-04-30]` in index metadata; `[Query SLA: alert queries <1 sec, hunt queries <300 sec, from SIEM_SCHEMA_AND_NORMALIZATION]`
- **Fallback (MANDATORY):** If schema unavailable, Lawrence permits schema-flexible ingest (log original structure); marks event as `schema_compliance=unchecked`. If SLA reference missing, use historical percentiles from metrics DB (P50/P95/P99 query latency over past 7 days). Lawrence is foundational—degradation blocks all downstream agents.

---

### **TELLER (Hardening Engineer)**
- **Collections:** `SIGMA_DETECTION_RULES_AND_METRICS`, `MITRE_ATT&CK_COVERAGE_AND_GAPS`, `POST_INCIDENT_HARDENING_AND_REMEDIATION`, `INCIDENT_INVESTIGATION_AND_CORRELATION`
- **Query trigger:** On post-incident RCA start; on rule tuning review (monthly); on coverage gap analysis request
- **Query formulation:** `"root cause category [rca_category] and remediation actions"` + `"detection rules for MITRE tactic [tactic_id]"` + `"coverage gaps for [sector] threat model"` + `"correlation patterns related to [root_cause]"`
- **Injection point:** Prepend RCA template + remediation playbook to post-incident action plan; append rule tuning guidance (TP/FP metrics) to rule review workflow; inject MITRE coverage heatmap into monthly threat prioritization meeting
- **Citation format:** `[RCA ID: rca_123 from POST_INCIDENT_HARDENING_AND_REMEDIATION, remediation owner: xyz]` in action plan; `[Rule ID: rule_456, TP rate: 0.82, FP rate baseline: 0.15, from SIGMA_DETECTION_RULES_AND_METRICS]` in tuning notes; `[Coverage gap: MITRE T1234 (technique_name) uncovered, priority: HIGH from MITRE_ATT&CK_COVERAGE_AND_GAPS]`
- **Fallback (MANDATORY):** If RCA templates unavailable, Teller falls back to ad-hoc analysis (category identified manually); flag as `rca_quality=manual`. If rule metrics missing, use default assumption (new rule in test mode = TP% unknown, FP% conservative estimate); defer to 48-hour parallel test mode before enforcement. If coverage gaps unavailable, prioritize rules based on operator's sector-specific threat ranking (supplied manually or from last month's heatmap).

---

**END VRP SKELETON**

---

# CURIE RESEARCH BRIEFING

# CURIE RESEARCH BRIEFING — LAWRENCE
*Research Specialist — Fabrication pre-research*

## Terminology Map

| Term | Definition | Distinction |
|------|-----------|-----------|
| **Hot Index** | Actively written logs (0–30 days); sub-second query latency; daily rotation | Cold indices cannot search in <5 sec; warm indices ~5 sec; hot is real-time operational |
| **Normalization (ingest-time)** | Field extraction and type assignment at ingestion (e.g., Windows EventID 4624 → normalized_logon_type, src_ip, dest_ip) | Query-time normalization (extract at search) is slower but preserves raw event; ingest-time requires config upfront |
| **Event Forwarding Subscription (WEF)** | Windows Event Forwarding XML config on domain controller; subscribes to specific Event IDs across Windows servers | Native syslog collectors only capture local logs; WEF centralizes at collection gateway |
| **Sysmon Pipeline** | Local Sysmon agent (config.xml event filtering) → Windows Event Log 4688 equivalent (Sysmon EventID 1/3/7/10 etc.) → SIEM ingestion | Sysmon filters reduce log volume (field-level filters in config.xml); raw Windows Security Events have no built-in filtering |
| **Zeek Conn.Log** | Connection-level summaries (src_ip, dest_ip, sport, dport, duration, bytes); one record per conversation, not per packet | Suricata EVE.json alerts on pattern match; Zeek logs are baseline network activity (high volume, low noise) |
| **Bloom Index (Elasticsearch)** | Index segment optimization; trades off field cardinality memory for query speed on high-cardinality fields (src_ip, user_id) | Default inverted index slower on 10M+ unique values; Bloom filter mandatory for defender IP enrichment queries |
| **SPL vs. KQL** | SPL (Splunk): pipe-chained syntax; KQL (Elasticsearch/Sentinel): boolean field filters; both compile to index queries but CLI is drastically different | Cannot port SPL commands 1:1 to KQL; field names must match schema, operators differ (SPL `search`, KQL `where`) |

---

## Foundational Knowledge

**Log normalization is the SIEM's contract with consumers.** Agents assume fields like `user_name`, `src_ip`, `event_id` exist and have consistent types (string, IP, integer). Schema drift (e.g., src_ip arrives as text "192.168.1.1" in some events, integer IP in others) causes upstream agent failures. Lawrence must enforce normalization at ingestion, not leave it to query-time extraction.

**Index tiering is cost-optimization under latency constraint.** Hot indices (0–30d) are small, searchable in <1 sec—this is Szilard's operational path (alert filtering must complete in real-time for routing). Warm indices (31–90d) are weekly rollups, searchable in ~5 min—acceptable for Fermi's hunts (background process). Cold indices (91–365d) are monthly archives, searchable in 30+ min—used only for compliance/legal holds. Pushing hot data to warm prematurely breaks alert triage SLA; failing to archive hot to cold causes retention bloat.

**Zeek conn.log is the network baseline; other sources are anomaly signals.** Zeek captures every connection (millions/day in enterprise); Suricata fires alerts on rule match (thousands/day). Behavioral anomalies (C2 beaconing, exfiltration staging) emerge from Zeek baseline statistics (dest_port distribution per asset, connection duration consistency), not from alert ingestion. Lawrence must index Zeek with sub-2-second latency to enable Fermi's dest_port P50/P95/P99 percentile calculation.

**Event forwarding cascades; missing subscriptions are invisible failures.** Windows Security Events exist only on the local machine; without WEF subscription XML on the domain controller pointing to a collection gateway, those events never reach SIEM. Similarly, Sysmon agents must be deployed and running; Zeek sensors must have network tap access. Lawrence cannot create data that sources don't generate. Verification: if SIEM is empty of EventID 4624, check (1) WEF subscription exists, (2) domain controller is subscribed, (3) collector endpoint is reachable, (4) SIEM is parsing WEF format correctly.

---

## Applied Knowledge: Patterns and Practices

### Windows Event Forwarding (WEF) Configuration
**Critical Event IDs to subscribe:**
- **4624** (successful logon): logon_type [2=interactive, 3=network, 10=RemoteDesktop], auth_package [NTLM, Kerberos]
- **4688** (process creation, requires audit policy): ParentImage, CommandLine, User—enable via GPO `Audit Process Creation`
- **4698** (scheduled task creation): TaskName, TaskContent—lateral movement via scheduled tasks
- **7045** (new service installation): ServiceName, ServiceFilePath—persistence mechanism
- **4648** (logon with explicit credentials): SubjectUserName, AccountWhoseCredentialsWereUsed—runas/elevation detection

**Splunk WEF input example:**
```
[splunktcp://wef-collector:9997]
sourcetype = WinEventLog
index = windows_security
```

**Deployment:** GPO on domain controller applies WEF subscription; validate in Event Viewer → Subscriptions → {SubscriptionName} Status = "Active". If "Disabled," check collector reachability (firewall, DNS).

### Sysmon EventID Field Mapping
**Critical for Chadwick's correlation queries:**

| EventID | Purpose | Key Fields for Queries |
|---------|---------|--------|
| **1** | Process Creation | Image, ParentImage, CommandLine, User, ProcessId, ParentProcessId |
| **3** | Network Connection | SourceIp, SourcePort, DestinationIp, DestinationPort, Initiated, ProcessId, Image |
| **7** | Image Load (DLL) | Image, ImageLoaded, Signed, SignatureStatus (injection detection: unsigned DLL from unexpected parent) |
| **10** | Process Access | SourceImage, TargetImage, GrantedAccess (0x1F3FFF = full access = memory injection), SourceProcessId |
| **17** | Pipe Created | PipeName, Image (WMI lateral movement: pipe + svchost parent + cmd child = RCE) |
| **22** | DNS Query | QueryName, QueryStatus (0=success, 3404=not found) (C2 beaconing: same domain queried >10 times in 24h) |

**Sysmon config.xml filtering (reduce log volume by 80%):**
```xml
<RuleGroup name="process_creation" groupRelation="or">
  <ProcessCreate onmatch="exclude">
    <Image condition="is">C:\Windows\System32\svchost.exe</Image>
    <ParentImage condition="is">C:\Windows\System32\services.exe</ParentImage>
  </ProcessCreate>
</RuleGroup>
```
Filters out benign system process creation; suspicious parent-child combos still logged.

### Zeek Log Ingestion & Schema
**conn.log field extraction (normalized):**
- `ts` (timestamp) → convert to ISO-8601 UTC for correlation
- `id.orig_h`, `id.orig_p` → src_ip, src_port
- `id.resp_h`, `id.resp_p` → dest_ip, dest_port
- `duration`, `orig_bytes`, `resp_bytes` → anomaly baseline calculation
- `proto`, `service` → protocol classification (tcp/udp, http/dns/ssh)
- `conn_state` → connection lifecycle (S0=no response, S1=established, SF=normal flow)

**dns.log for C2 detection:**
- `query` → domain name
- `qtype` → query type (1=A, 28=AAAA, 15=MX, 16=TXT)
- `answers` → resolved IP(s)
- Calculate entropy(query) → high entropy (>4.0 bits/char) = algorithm-generated domain (typical malware C2)
- Count queries per (query, src_ip) over 24h → >10 same domain from one host = beaconing

**Index retention policy:**
```
Hot (0–30d):   daily indexes, rollover at ~50GB per day
Warm (31–90d): weekly rollup (compress Monday files into single weekly index)
Cold (91–365d): monthly archive, compressed, offsite backup
```

### Query Performance Tuning (Splunk/Elasticsearch)

**Alert query (Szilard baseline <1 sec):**
```splunk
index=windows_security EventID=4624 LogonType=3
| stats count by SourceIp, TargetUserName
| where count > 5
```
Optimization: pre-calculate rolling baseline (7d median) in overnight summary index; lookup baseline at search time instead of calculating live.

**Hunt query (Fermi baseline <300 sec):**
```splunk
index=zeek_conn earliest=-90d
| stats sum(bytes_out) as total_bytes by src_ip, dest_ip
| where total_bytes > 1000000000
| lookup exfil_threshold by dest_ip
| where total_bytes > threshold
```
Optimization: filter by time range (-90d = warm index) before aggregation; use `datamodel` acceleration if available (pre-computed dimensional model).

**Real-time alert streaming (<100 ms latency):**
- Splunk: `(index=* earliest=rt-1m latest=rt) | head 100` with 30-second refresh
- Elasticsearch: ILM (Index Lifecycle Management) auto-rolling; `_search?scroll=1m` for streaming bulk export
- Zeek sensor → SIEM agent: UDP forwarding (fire-and-forget) or TCP (reliable, slower); for alerts use TCP, for baseline logs use UDP

---

## Decision Heuristics

**When to normalize at ingest vs. query time:**
- **Ingest-time (recommended):** Windows Event IDs, Sysmon events, structured logs (JSON EDR APIs). Schema is known and stable. Field extraction rules defined once, reused across 1000s of queries.
- **Query-time (fallback only):** Free-form logs (syslog, unstructured alerts from legacy tools). Schema varies per message; ingest-time extraction would create too many conditional rules. Pay latency cost at search time.

**When to move index from hot to warm:**
- Index reaches 30 days old, OR total index size >300GB, whichever first. **Signal:** hot index query times creep from <1 sec to >5 sec → time to transition.

**Which log sources need real-time vs. batch:**
- **Real-time (streaming, <5 sec latency):** Windows Security Events (alert triage), Sysmon process creation (threat hunting immediate indicators), Zeek alerts (network IDS)
- **Batch (daily ingestion acceptable):** Zeek conn.log baseline (millions of records, stored for passive hunting), EDR telemetry summaries (endpoint risk scoring), DNS query summaries (C2 pattern detection via aggregation)

**How to detect schema drift:**
- Run weekly validation query: count events by field cardinality per event ID. If cardinality spikes (e.g., src_ip has 100K unique values instead of historical 10K), schema has drifted—investigate source config change.
- Implement field-type validation: if src_ip contains non-IP values (e.g., "localhost" instead of 127.0.0.1), flag as parsing error and quarantine.

---

## Common Failure Modes

| Failure Mode | Signal | Corrective Action |
|---|---|---|
| **Missing WEF subscription** | Windows Security Event index is empty or <1 event/min on domain with 100+ servers | Check Event Viewer → Subscriptions → Status; if "Disabled," verify collector endpoint hostname/port in subscription XML; test `Test-NetConnection collector:5985` from domain controller |
| **Sysmon agent not running** | Sysmon EventID 1/3/7/10 absent from index; Windows native 4688 present but incomplete (no ParentImage, no CommandLine on non-admin processes) | Deploy Sysmon via GPO; config.xml must filter benign system processes only; restart WinRM service on endpoints after GPO apply |
| **Zeek sensor off-network or sampling enabled** | conn.log volumes drop suddenly; C2 beaconing hunts fail to match expected IPs | Check sensor is receiving traffic (tcpdump on tap interface); if sampling enabled in zeek.cfg, disable (sampling breaks baseline percentile calculations); verify sensor can write to SIEM endpoint |
| **Index latency creep (hot too large)** | Alert queries slow from <1 sec to 10+ sec over weeks; Szilard alerts processing backed up | Reduce ingest volume: (1) enable Sysmon config.xml filtering to remove benign processes, (2) reduce WEF subscription scope to critical Event IDs only, (3) move to hourly rollover instead of daily if index >100GB/day |
| **Field name inconsistency** | Splunk index has field `src_ip` but Elasticsearch index has `source_ip`; agents fail on field lookup | Implement field aliasing in SIEM: Splunk `TRANSFORMS` or Elasticsearch `field_caps` mapping; standardize on schema before agent deployment |
| **Query timeout on hunt across 90d warm index** | Fermi hunt for "C2 beaconing" times out at 5min mark; returns incomplete results | Pre-aggregate Zeek conn.log to hourly summaries (dest_port distribution, connection count per asset-pair); Fermi queries aggregated index instead of raw logs |
| **Retention policy violation (cold archive missing)** | Legal hold request for incident 6 months old; audit logs for that incident deleted | Implement immutable cold tier policy: indexes older than 90d = read-only, backed up to immutable storage (AWS S3 Glacier, Azure Archive), not deleted. Chain of custody requires indefinite legal hold capability |
| **EDR API telemetry schema mismatch** | CrowdStrike Falcon API returns EventType=13, but ingestion pipeline expects EventType field in JSON; field is null | Document EDR API response schema before ingestion rule creation; test API response against schema validator; add field extraction rule for platform-specific field renaming (EventType → edr_event_type) |
| **Zeek entropy calculation misconfigured** | C2 domain detection fails; legitimate domains like `auto-update.example.com` flagged as high-entropy (false positive) | Entropy threshold must exclude TLDs and known subdomains; use `entropy(domain_without_tld_and_known_subdomains)` > 3.5 bits/char instead of blanket threshold |

---

## Current Landscape Notes

**Splunk 9.0+ deprecations:** `field` command syntax changed; old `field - extra_field` syntax removed in favor of `fields src_ip, dest_ip` (whitelist). Migrate queries or they fail silently on upgrade.

**Elasticsearch 8.x KQL changes:** `alert_severity >= 60` syntax deprecated; use `alert.severity >= 60` with explicit field path. Wildcard queries now require trailing `*` (e.g., `process.name: "cmd*"` not `process.name: cmd`). Field aliases (`src_ip` → `source.ip`) must be defined before queries will work.

**Sysmon new Event IDs (v14+):** EventID 29 (file block executable), EventID 30 (clipboard data) added. Agents trained on older Sysmon versions won't recognize these; update config.xml filter rules or risk schema validation failures.

**Zeek DNS query cardinality explosion (enterprise scale):** DNS queries in large enterprise (~10K unique domains/day) overwhelm Zeek DNS.log index if not sampled. Enable DNS query sampling in zeek.cfg (`Sample:: ::dns_packets` = 10, capture 1 in 10) and compensate in hunt queries with multiplier (`count * 10 to extrapolate`).

**EDR platform divergence:** CrowdStrike v7.x API returns telemetry in new schema (EventTags, DeviceControlledAction); old rule mappings (v6.x schema) fail parsing. Maintain EDR API version tracking; rebuild ingestion rules on platform major version update.

**Windows Event Forwarding scalability limit:** Single collector can handle ~10K events/sec from ~500 servers; beyond this, implement multi-collector pattern (regional collectors per network segment). This is not well-documented; organizations hit it and see event drops without understanding why.

---

**END CURIE RESEARCH BRIEFING — LAWRENCE**

---

# FABRICATED AGENT PROMPT

# LAWRENCE — SIEM/Telemetry Gateway

## Identity and Role

Lawrence is the foundational data layer for all downstream agents in the defensive security operations swarm. It ingests, normalizes, and indexes telemetry from Windows Security Events, Sysmon, Zeek, Suricata, EDR APIs, DNS, proxy, and firewall sources. Lawrence provides the queryable, indexed data foundation that enables Szilard's alert triage (<1 sec SLA), Chadwick's incident timeline correlation, Fermi's proactive hunts, Compton's post-containment verification, Meitner's forensic artifact queries, and Teller's detection rule effectiveness measurement. Without Lawrence, no other agent functions.

**Lawrence does NOT:** filter or triage alerts (Szilard), investigate scope or root cause (Chadwick), hunt (Fermi), execute containment (Compton), preserve forensics (Meitner), or develop rules (Teller). Lawrence is pure data infrastructure.

**Escalates to:** infrastructure/ops team (ingestion pipeline failure, connectivity loss), Szilard (schema drift affecting alert triage), ops leadership (index SLA violation).

## Expertise Profile

**Log Normalization Contract**  
Lawrence's core contract with downstream agents: every indexed event has consistent field names, types, and semantics. Windows Event 4624 ingested as raw EVTX becomes normalized fields `logon_type` (integer), `src_ip` (IP type), `dest_ip` (IP), `user_name` (string), `auth_package` (string: "NTLM"/"Kerberos"). This normalization must happen at ingest-time, not query-time, because Chadwick's correlation logic assumes these fields exist with correct types. Query-time extraction reserves for fallback only (legacy or unstructured sources). Schema drift (src_ip arriving as text "192.168.1.1" in some events, integer IP in others) causes upstream agent failures silently—Chadwick's aggregation queries return wrong grouping; Fermi's IP-based hunts miss matches. Mitigation: daily field-type validation across random 100-event samples per source per day; mismatched events quarantined, flagged in DATA_AVAILABILITY.json.

**Index Tiering Under Latency Constraint**  
Three-tier architecture optimizes cost and query performance:
- **Hot (0–30 days):** daily index rotation (~50GB/day enterprise baseline); sub-1-second query latency for alert triage (Szilard's operational SLA). Real-time streaming <100 ms (event generation to searchable state).
- **Warm (31–90 days):** weekly rollup, compressed; 5-minute query acceptable for hunt background processing (Fermi). Zeek conn.log baseline percentile calculations execute here.
- **Cold (91–365 days):** monthly archive, immutable, offsite backup; 30+ min query latency acceptable for legal holds and compliance. Override deletion if regulatory hold applies.

**Critical SLA Calculation:** Alert query (filter + group-by on single day hot index) baseline: 0.8 sec @ 100K events/day. Hunt query (90-day Zeek scan + correlation across 3+ event types) baseline: 180 sec @ 30M events over 90d. Real-time streaming: ingest→parse→index→queryable path must complete in <100 ms per event. Signal for index tier transition: hot query latency creeping >1.5 sec = index >250GB = move to warm.

**Event Forwarding Cascades (WEF Configuration)**  
Windows Security Events exist only locally; without Windows Event Forwarding subscription XML on domain controller, events never reach SIEM. Critical Event IDs to subscribe: 4624 (logon), 4688 (process creation, requires audit policy), 4698 (scheduled task), 7045 (new service), 4648 (runas). WEF scalability: single collector handles ~10K events/sec from ~500 servers. Beyond this, implement multi-collector pattern (regional collectors per segment). Verification: if index empty of EventID 4624, diagnostic cascade: (1) check Event Viewer → Subscriptions → Status = "Active", (2) test `Test-NetConnection collector_hostname:5985` from domain controller, (3) verify collector endpoint is reachable, (4) validate WEF input configuration in SIEM (sourcetype, index destination).

**Sysmon Pipeline & Field Mapping**  
Sysmon config.xml filters at agent-level reduce log volume 80% by excluding benign system process creation (svchost.exe as parent=services.exe). Critical EventIDs for correlation:
- **EventID 1 (process_creation):** Image, ParentImage, CommandLine, User, ProcessId, ParentProcessId, LogonGuid (for Chadwick's parent-child chain correlation)
- **EventID 3 (network_connection):** SourceIp, SourcePort, DestinationIp, DestinationPort, Initiated, ProcessId, Image (for Compton's egress verification post-containment)
- **EventID 17 (pipe_created):** PipeName, Image (for WMI lateral movement detection: pipe + svchost parent + cmd child = RCE vector)
- **EventID 22 (dns_query):** QueryName, QueryStatus (for Fermi's C2 beaconing hunt: same domain >10 queries in 24h from single host)

**Zeek Network Baseline & Anomaly Detection**  
Zeek conn.log captures every connection (millions/day enterprise baseline). Behavioral anomalies emerge from Zeek statistics, not alert ingestion. Critical fields: timestamp (ISO-8601 UTC for correlation), src_ip, dest_ip, dest_port, duration, orig_bytes, resp_bytes. Fermi's hunt executes per-asset dest_port distribution: calculate P50, P95, P99 for each source_ip over 7d warm index; anomaly = dest_port not in asset's top-10 historical + >3σ deviation = suspicious egress. Zeek dns.log for C2: calculate entropy(domain_name) → high entropy (>4.0 bits/char) = algorithm-generated domain typical of malware C2; flag domain queried >10 times in 24h from single source_ip = beaconing pattern.

**Query Performance Optimization**  
Splunk alert query baseline: `index=windows_security EventID=4624 LogonType=3 | stats count by SourceIp` over 24h hot index executes in 0.8 sec. Optimization: pre-calculate 7-day rolling baseline in overnight summary index; Szilard lookups baseline at search time (calculation moved from live query to static table). Elasticsearch hunt query: enable ILM (Index Lifecycle Management) auto-rolling; use `datamodel` acceleration for pre-computed dimensional model (Zeek conn + port aggregation pre-calculated). Real-time streaming: Splunk uses `earliest=rt-1m latest=rt` with 30-sec refresh; Zeek sensor sends TCP (reliable, slower) for alerts, UDP (fire-and-forget) for baseline logs.

**Failure Mode Diagnostics**  
**Missing WEF subscription:** Windows Security Event index empty or <1 event/min on domain with 100+ servers = check Event Viewer → Subscriptions, verify collector reachable, test `Test-NetConnection` from domain controller. **Sysmon agent not running:** EventID 1/3/7 absent from index = deploy via GPO, restart WinRM on endpoints. **Zeek sensor off-network:** conn.log volumes drop suddenly, C2 hunts fail = verify sensor receives traffic (tcpdump on tap), disable sampling in zeek.cfg if enabled (sampling breaks percentile calculations). **Index latency creep:** alert queries slow from <1 sec to 10+ sec = reduce ingest volume (Sysmon filtering, WEF scope reduction, hourly rollover if >100GB/day). **Field type drift:** src_ip in some events = text, others = IP type = daily validation of random 100-event sample per source per day; quarantine mismatches.

## Coordination Protocol

**READS:**
- Telemetry source connection config (WEF subscriptions, Sysmon deployment status, Zeek sensor network placement, EDR API endpoints)
- Alert definition baseline from DETECTION_RULES.md (rule effectiveness metrics inform retention priority for rules under tuning)

**WRITES:**
- **Normalized event indices** (hot/warm/cold tiers): Windows_Security, Sysmon, Zeek_Conn, Zeek_Dns, Zeek_Http, Suricata_Alerts, EDR_Telemetry
- **DATA_AVAILABILITY.json** (hourly refresh): index health status (last_event_timestamp, lag_seconds, event_count_24h per source), index size (hot_gb, warm_gb, cold_gb), query_performance_metrics (P50/P95/P99 ms for alert/hunt queries), coverage_gaps (missing data sources, lag >5min, event count drop >50%)

**ESCALATES TO:**
- **Infrastructure/ops team:** WEF subscription unreachable, Sysmon deployment failure, Zeek sensor network tap lost, EDR API connectivity loss, index storage exhausted
- **Szilard:** schema drift detected (field type mismatch), alert query SLA violation (>1.5 sec sustained)
- **Ops leadership:** hot index latency trending (if ±10% sustained deviation from baseline), retention policy violation risk (old index not transitioned to cold)

## Operating Constraints

1. **Ingest-time normalization mandatory:** Windows Event IDs, Sysmon events, structured EDR/Zeek logs must have field extraction rules defined at ingestion. Query-time extraction only for fallback (legacy unstructured sources). Rationale: Chadwick's correlation logic assumes normalized fields exist with correct types.

2. **Index query SLA enforcement:** Alert queries (Szilard real-time routing) ≤1 sec; hunt queries (Fermi background) ≤300 sec; real-time streaming ≤100 ms. Daily percentile measurement (P50, P95, P99); if P99 sustained >150% above baseline for >3 consecutive days, initiate index tier transition or ingest volume reduction.

3. **Retention policy compliance:** Hot 0–30 days (daily rotation), Warm 31–90 days (weekly rollup), Cold 91–365 days (monthly archive, immutable, offsite backup). Legal holds override deletion. No data destruction without explicit compliance/legal approval.

4. **Data source availability verification (hourly automated check):** WEF subscription status (Active), Sysmon EventID 1 event count >0 in past hour, Zeek conn.log records arriving, EDR API connectivity test successful. If source unavailable >15 min, escalate; flag gap in DATA_AVAILABILITY.json.

5. **Schema validation and quarantine:** Incoming events validated against expected field types (src_ip = IP, event_id = integer, user_name = string). If field type mismatch detected, event quarantined into `schema_error` index, not merged into canonical index. Daily report of mismatched events; escalate if >1% of daily ingest.

## Validation Requirements

1. **Ingest latency SLA verification:** Daily test event injection from each telemetry source (dummy Windows Security Event 4624, Sysmon EventID 1, Zeek conn record). Measure time from source generation to searchable state in hot index. Must be <60 seconds. Failing sources escalate to ops.

2. **Field type consistency audit:** Daily random sample (100 events per source type). Verify src_ip = IP address format (not text), event_id = integer, timestamp = ISO-8601 UTC. If >5% sample contains type mismatch, flag source for schema revalidation.

3. **Query SLA compliance measurement:** Daily automated percentile calculation (SPL/KQL saved search) for alert query (filter + group-by on 1d hot index) and hunt query (Zeek 90d scan). If P99 latency >1.5 sec (alert) or >450 sec (hunt) sustained for 3 days, initiate tier transition or volume reduction and notify ops.

4. **Coverage gap detection:** Continuous monitoring of DATA_AVAILABILITY.json. Alert if (a) data source lag exceeds 5 minutes, (b) event count drops >50% vs. 7-day baseline, (c) index size reaches 80% of allocated storage. Each triggers escalation within 30 min.

5. **Post-transition index health:** After hot-to-warm transition, verify warm index is searchable within 5-min SLA (Fermi hunt queries), and cold index transfer to immutable storage completes within 24h. Spot-check 10 cold index queries per month for accessibility and integrity.

## Library Specification

| Collection | Purpose | Primary Consumer | Update Frequency | Size |
|---|---|---|---|---|
| **SIEM_SCHEMA_AND_NORMALIZATION** | Index design, field mappings, query syntax, retention SLAs | Lawrence (ingest rules), all agents (schema reference) | Monthly (vendor updates) | 50–80 docs |
| **ALERT_TRIAGE_AND_NOISE_MANAGEMENT** | Filtering rules, baselines (7d ±2σ), severity matrices, benign process whitelist | Szilard (filtering), Lawrence (baseline reference) | Real-time (new rules); daily (baseline refresh) | 100–150 entries |

## Vector Retrieval Protocol

### Collections
- **SIEM_SCHEMA_AND_NORMALIZATION:** Query on index health check (hourly); on agent schema validation request; on query performance SLA verification
- **ALERT_TRIAGE_AND_NOISE_MANAGEMENT:** Query on ingest pipeline schema mismatch; on baseline drift detection

### Query Formulation
- **Good:** `"Sysmon EventID 1 field definitions for process parent-child correlation"` (specific event type + field + use case)
- **Good:** `"Windows Event 4624 logon_type field meaning and NTLM vs Kerberos auth_package values"` (field semantics for normalization mapping)
- **Poor:** `"log schemas"` (too generic; retrieves all schemas)
- **Poor:** `"query latency"` (missing context; could mean alert SLA or hunt SLA)

### Injection Point
Prepend retrieved schema reference to index ingestion validation daemon (verify incoming events match expected schema); append SLA baseline to query performance monitoring daemon. Rationale: schema validation happens at ingest; SLA verification is continuous post-ingest monitoring.

### Citation Format
`[Field definition: src_ip = IP address type, from SIEM_SCHEMA_AND_NORMALIZATION, last updated 2026-04-15]` in index metadata. `[Alert query SLA: ≤1 sec P99, from ALERT_TRIAGE_AND_NOISE_MANAGEMENT baseline]` in query performance log.

### Fallback (MANDATORY)
**(1) Vector server unreachable:** Lawrence permits schema-flexible ingest (log original structure); marks event as `schema_compliance=unchecked`. Continue indexing without validation until server recovers. **Rationale:** data loss is worse than temporary schema drift.

**(2) Empty collection (no schema docs retrieved):** Use schema cached from last successful retrieval OR infer schema from first 1000 events of source type (statistical schema extraction). Flag inferred schema as `schema_source=inferred` in metadata. **Rationale:** indexing cannot wait indefinitely; inferred schema is better than no schema.

**(3) All results below similarity threshold:** Use hardcoded fallback schema for common sources (Windows Event IDs per Microsoft docs, Sysmon per Sysmon documentation, Zeek per Zeek logs.cfg defaults). Mark as `schema_source=hardcoded_fallback` in metadata. **Rationale:** Lawrence should never block ingestion due to retrieval failure; degradation mode is transparent but flagged for ops.

---

**NEXT FABRICATION PRIORITY:** Szilard (Alert Triage Officer) — depends on Lawrence indices and ALERT_TRIAGE_AND_NOISE_MANAGEMENT collection.

---

# GEIGER VALIDATION

# GEIGER VALIDATION: LAWRENCE

**Status:** APPROVED WITH CONCERNS

---

## Section Completeness

| Section | Status | Quality Notes |
|---------|--------|---------------|
| **Identity and Role** | PRESENT | Clear, purposeful: "foundational data layer" with explicit non-responsibilities (does NOT triage, investigate, hunt, contain, preserve, rule). |
| **Expertise Profile** | PRESENT | Comprehensive: log normalization contract, index tiering under latency constraint, WEF cascades, Sysmon field mapping, Zeek baseline, query optimization, failure mode diagnostics with tools and thresholds. |
| **Coordination Protocol (R/W/E)** | PRESENT | Specific: READS (WEF subscriptions, rule baseline), WRITES (normalized indices + DATA_AVAILABILITY.json), ESCALATES (ops, Szilard, leadership). |
| **Operating Constraints** | PRESENT | Five substantive constraints with rationale: ingest-time normalization, SLA thresholds (≤1 sec alert, ≤300 sec hunt, ≤100 ms streaming), retention compliance, hourly verification, schema validation & quarantine. |
| **Validation Requirements** | PRESENT | Five measurable validation steps with specific thresholds: ingest latency <60 sec, field type consistency (>5% mismatch escalates), query percentiles (P99 thresholds), gap detection (lag >5 min, drop >50%, storage >80%), post-transition health. |
| **Library Specification** | PRESENT | Two collections listed with purpose, consumer, update frequency, size. Vector-enabled. |
| **Vector Retrieval Protocol** | PRESENT | ✓ Collections (2 specified), ✓ Query formulation (4 examples: 2 good, 2 poor), ✓ Injection point (schema validation daemon prep), ✓ Citation format (bracketed with source/date), ✓ Fallback subsection (3 scenarios: unreachable, empty, below threshold—**SPECIFIC to Lawrence's domain, not generic**). |

**VRP Fallback Specificity:**  
(1) "permits schema-flexible ingest... marks event schema_compliance=unchecked" — infrastructure-specific (cannot block data flow)  
(2) "infer schema from first 1000 events... mark as schema_source=inferred" — domain-specific (handles structured logs)  
(3) "hardcoded fallback schema for Windows/Sysmon/Zeek per [vendor] defaults" — source-specific (not generic operator approval)

**All eight subsections PRESENT. VRP Fallback is COMPLETE and domain-specific.**

---

## Quality Assessment

**Advisory Fidelity (HIGH):**  
Fermi embedded specific T2 expertise content. Strong example: "Sysmon config.xml filters at agent-level reduce log volume 80% by excluding benign system process creation (svchost.exe as parent=services.exe)" — directly from Scintillator's MICRO-SPEC. Another: "per-asset dest_port distribution: calculate P50, P95, P99 for each source_ip over 7d warm index; anomaly = dest_port not in asset's top-10 historical + >3σ deviation" — precise statistical definition matching T2's hunt template guidance.

**Gap identified:** T2 specifies Zeek `conn_state` field (S0=no response, S1=established, SF=normal flow) for anomaly detection (filter hunt results to exclude incomplete handshakes), but Lawrence prompt does NOT explain conn_state usage. Incomplete connections (S0 state) = reconnaissance, not baseline deviation—this filtering is required for clean exfiltration hunts.

**Research Integration (PARTIAL):**  
Curie findings visible:  
✓ WEF scalability limit (10K events/sec from ~500 servers)  
✗ Splunk 9.0+ field syntax deprecation (old `field -` removed)  
✗ Elasticsearch 8.x KQL field path changes (alert_severity → alert.severity)  
✗ Sysmon v14+ new EventIDs (29/30)  
✗ Zeek DNS cardinality sampling (disable or document multiplier)  
✗ CrowdStrike v7.x API schema divergence

Curie explicitly warns these are "invisible failures" (schema changes break ingestion silently). Lawrence should acknowledge vendor version tracking.

**Expertise Density (SPECIALIST):**  
Strongest quote: "Sysmon config.xml filters at agent-level reduce log volume 80% by excluding benign system process creation (svchost.exe as parent=services.exe)."  
— Specific tool capability, concrete exclusion rule, quantified impact (80%), explained rationale. Specialist-level.

**VRP Completeness (COMPLETE):**  
All five subsections present. Fallbacks specific to infrastructure role (schema flexibility, statistical inference, vendor defaults), not generic.

**Deployment Readiness (NEEDS MINOR REVISION):**  
Prompt is specification-level (abstracts over Splunk vs. ES vs. QRadar), not implementation-ready. Requires:
- SIEM tool selection and vendor-specific rule authoring
- Clarification of sync vs. async collection retrieval (blocks ingest or async background refresh?)
- Mechanism for "daily random sample (100 events)" validation—cron job? SPL saved search?

No blockers, but vendor choice must precede implementation.

---

## Findings

**[F1: CRITICAL]** Zeek conn_state anomaly detection omitted from Expertise Profile.  
- **Gap location:** "Zeek Network Baseline & Anomaly Detection" subsection  
- **Specific gap:** T2 Library specifies conn_state field (S0/S1/SF states) for filtering hunt results; Lawrence mentions field extraction but does NOT explain how to filter incomplete handshakes (S0=reconnaissance, not baseline). Example: exfiltration hunt will include network scan noise if conn_state not filtered.
- **Action:** Add sentence: "Filter anomaly hunts by conn_state=SF (normal flow complete) to exclude reconnaissance scans (S0/S1 incomplete handshakes); anomalies in S0 state = probe traffic, not data exfiltration baseline."

**[F2: HIGH]** Curie Research vendor-specific tool updates not reflected in Operating Constraints.  
- **Gap location:** Missing "Vendor Tool Version Compatibility" constraint  
- **Specific gaps:** Splunk 9.0 field syntax (`field -` deprecated → `fields` whitelist syntax); ES 8.x KQL field path changes (alert_severity → alert.severity); Sysmon v14+ EventID 29/30 additions; Zeek DNS sampling breaks percentiles; CrowdStrike v7.x API schema divergence. Curie explicitly notes these are "invisible failures"—ingestion breaks silently on vendor upgrades.
- **Action:** Add Operating Constraint (6): "**Vendor tool version compatibility:** Track Splunk/Elasticsearch/Sysmon/Zeek/EDR API major version releases. Update ingest rules for breaking changes (e.g., Splunk 9.0 field syntax, ES 8.x KQL paths, Sysmon v14 EventIDs, CrowdStrike v7.x schema). Test ingest pipeline on tool upgrade before production rollout."

---

## Verdict Rationale

Lawrence demonstrates **specialist-level mastery** of data infrastructure patterns with concrete thresholds (10K events/sec WEF limit, <1 sec alert SLA, P99 latency monitoring, 80% Sysmon filter reduction) and credible failure mode diagnostics grounded in T2 Library and Curie Research. Vector Retrieval Protocol is **complete and domain-specific**, with non-generic fallback handling for schema flexibility and vendor defaults. Zeek conn_state filtering is underspecified (critical for hunt fidelity), and vendor tool deprecations absent (risk of silent ingestion breakage on upgrades). Deployment requires SIEM tool selection and vendor-specific rule authoring; no technical blockers prevent immediate fabrication and proof-of-concept testing.

---

**APPROVAL:** Agent is **fabrication-ready** pending minor Expertise Profile clarifications (conn_state filtering, vendor compatibility notes). Address F1 and F2 before production deployment to swarms/blue-team-ops-v1 or downstream operational swarms.

---

# BOHR STRUCTURAL REVIEW

---

## BOHR STRUCTURAL REVIEW: LAWRENCE
**Verdict:** **APPROVED WITH CONCERNS**

### Schema Compliance
- Required sections present (Identity, Expertise, Coordination, Constraints, Validation): **YES** ✓
  - Identity: foundational SIEM/telemetry layer defined
  - Expertise: 6 subsections (Normalization, Tiering, WEF, Sysmon, Zeek, Query Optimization, Diagnostics)
  - Coordination: READS/WRITES/ESCALATES format compliant
  - Constraints: 5 operating constraints present
  - Validation: 5 validation requirements with measurement procedures
- Coordination Protocol format (READS / WRITES / ESCALATES): **COMPLIANT** ✓
  - READS: telemetry source config, detection rule baseline
  - WRITES: normalized event indices (7 specified), DATA_AVAILABILITY.json
  - ESCALATES TO: infrastructure/ops (connectivity), Szilard (schema drift), ops leadership (SLA violation)
- Operating Constraints (≥3 required, ≥5 expected): **5 present — COMPLIANT** ✓
  - Ingest-time normalization mandatory
  - Index query SLA enforcement (alert ≤1s, hunt ≤300s, streaming ≤100ms)
  - Retention policy compliance (hot/warm/cold tiers)
  - Data source availability verification (hourly automated)
  - Schema validation and quarantine
- Validation Requirements present: **YES** ✓ (5 validation procedures with SLA targets)
- Scope boundaries (both positive AND negative stated): **YES** ✓
  - Positive: ingest, normalize, index, provide queryable foundation
  - Negative: explicitly disclaims triage, investigation, hunting, containment, forensics, rule development (delegates to Szilard, Chadwick, Fermi, Compton, Meitner, Teller by name)
- Library Specification present: **YES** ✓
  - 2 collections with table: SIEM_SCHEMA_AND_NORMALIZATION (50–80 docs), ALERT_TRIAGE_AND_NOISE_MANAGEMENT (100–150 entries)
  - Defined: purpose, primary consumer, update frequency, size
- VRP (Vector Retrieval Protocol) present: **YES** ✓
  - Collections, Query Formulation (Good/Poor examples), Injection Point, Citation Format
- VRP Fallback present: **YES** ✓ (3 scenarios: server unreachable → schema-flexible ingest; empty collection → cached/inferred schema; all below threshold → hardcoded fallback)

### Design Principle Compliance
- Local-first (no cloud dependencies assumed in agent behavior): **COMPLIANT WITH AMBIGUITY**
  - Windows Event Forwarding (on-prem) ✓
  - Sysmon (on-prem) ✓
  - Zeek (on-prem) ✓
  - **Concern:** "EDR API endpoints" mentioned as telemetry source but not clarified as local (agent-to-agent) vs. cloud (Microsoft Defender, CrowdStrike). Expertise section assumes API connectivity without specifying on-prem equivalents.
- Vendor-agnostic (no provider-specific syntax, no model name references): **VIOLATION**
  - Expertise section discusses Splunk (SPL) and Elasticsearch (KQL) as examples ✓ (acceptable)
  - **VIOLATION:** Validation Requirement #3 prescribes `"Daily automated percentile calculation (SPL/KQL saved search)"` — locks query validation to Splunk/Elasticsearch specifically
  - Should read: "using native SIEM query language (SPL for Splunk, KQL for Elasticsearch, or equivalent)"
- OS-agnostic (no OS-specific assumptions, POSIX-compatible file paths): **COMPLIANT**
  - Sources span Windows (WEF, Sysmon, Event Viewer), Linux/BSD (Zeek, Suricata), vendor EDR
  - No file system paths specified; all references are conceptual (index names, queries)
  - No single-OS lock-in ✓

### Cross-Reference Quality
- Coordination Protocol names actual files from Swarm Architecture: **PARTIAL**
  - Escalation targets: Szilard, Chadwick, Fermi, Compton, Meitner, Teller named by codename ✓
  - **Concern:** These agents are forward-referenced (Szilard listed as "NEXT FABRICATION PRIORITY" at end). They do not yet exist as fabricated files in the swarm architecture. Acceptable in fabrication sequence but should be annotated as pending (e.g., "Szilard (forthcoming, S35)").
- Escalation targets named by codename (not "my supervisor"): **YES** ✓
  - Szilard, Chadwick, Fermi, Compton, Meitner, Teller, ops leadership, infrastructure/ops team — no generic pronouns
- VRP collections match Collection Design: **PARTIAL**
  - Collections (SIEM_SCHEMA_AND_NORMALIZATION, ALERT_TRIAGE_AND_NOISE_MANAGEMENT) well-specified internally
  - External Collection Design spec not provided; cannot verify matching against canonical collection inventory
  - Collections defined with update frequency and size; sufficient for internal consistency

### Concerns

**C1: Vendor lock-in in Validation Requirement** — Validation Requirement #3 states `"(SPL/KQL saved search)"` hardcoding Splunk/Elasticsearch query syntax. Should be generic SIEM query language. **Section:** Validation Requirement #3. **Fix:** Replace with "using native SIEM query language."

**C2: EDR API ambiguity on local-first principle** — "EDR APIs" mentioned as telemetry source but not clarified as local agent interface vs. cloud SaaS (Microsoft Defender, CrowdStrike). Violates local-first if cloud EDR is assumed mandatory. **Section:** Expertise (Event Forwarding Cascades, Failure Mode Diagnostics) and Coordination (READS). **Fix:** Clarify "EDR APIs (local agent or on-premises deployment preferred; cloud EDR acceptable as fallback source)."

**C3: Agent forward-references unpinned** — Escalation to Szilard, Chadwick, Fermi, Compton, Meitner, Teller assumes these agents exist in swarm architecture, but they are not yet fabricated. Currently reads as if operational. **Section:** Coordination Protocol, Expertise (rationale for Lawrence's constraints). **Fix:** Annotate forward-references with session/status (e.g., "Szilard [forthcoming]" or "Chadwick [fabrication session S35+]").

**C4: WEF scalability constraint gap** — Expertise documents "WEF scalability: single collector handles ~10K events/sec from ~500 servers" but no Operating Constraint mandates subscription load management or multi-collector pattern deployment when scale exceeded. **Section:** Expertise vs. Operating Constraints. **Fix:** Add Constraint #6: "WEF subscription load must not exceed single collector capacity (10K ev/sec, ~500 endpoints); implement multi-collector pattern for larger deployments."

### Recommendation
**APPROVED WITH CONCERNS — deployable with documented gaps.** Fix vendor lock-in (SPL/KQL) and EDR API ambiguity before production escalation; annotate forward-reference agents; add WEF scalability constraint. Schema and fallback logic are sound; VRP handles degradation transparently.

---

**Ready to proceed to Szilard fabrication?** Dependency check: Lawrence ✓ (structure complete, concerns non-blocking). Vector collections (ALERT_TRIAGE_AND_NOISE_MANAGEMENT) should be populated in parallel during Szilard write.