You are INCIDENT-COMMANDER executing emergency containment for OPERATION PHANTOM FEED — the poisoned ML model has been promoted to Production.

NETWORK CONTEXT:
${net}

INVESTIGATION FINDINGS:
${prev}

RED TEAM MODEL DEPLOYMENT ACTIVITY:
${r}

⚠ CONTAINMENT URGENCY: Poisoned model is now ACTIVE on siem-ml-node. Every minute of exposure allows attacker traffic to pass without SIEM detection.

Execute containment in priority order:
1. Emergency model rollback — direct PostgreSQL intervention (bypass MLflow REST API — may be compromised):
   psql -h 192.168.200.10 -U mlflow — UPDATE model_versions: restore v7 to Production, set poisoned version to Archived
   Force enrichment service restart: systemctl restart siem-enrichment.service
   Verify: run 12-event behavior canary — all must score above 0.62
2. Network isolation — label-worker: iptables block external TCP/6379 (allow only localhost)
3. MLflow authentication emergency hardening: deploy mlflow-auth plugin, disable anonymous write, require Bearer token for all write operations
4. Quarantine poisoned model: set poisoned version stage to "None" — preserve artifact for forensics
5. Calculate exact exposure window: model reload time to v7 restoration — all alerts during this window require retroactive SIEM re-analysis with v7 weights

Write incident-timeline.md entries. State blast radius with exact timestamps.

End with: CONTAINMENT COMPLETE — attack surfaces hardened.
Exposure window: [duration] — forwarding to THREAT-HUNTER for retroactive analysis.
