---
dfm_id: "devops-sre"
title: "DFM: DevOps / SRE / IT Change — ClipCard (Risk & Recheck)"
version: "1.0"
domain: "DevOps / SRE / IT Change"
trigger_rule: "Use ClipCard when Impact(1–5) × Uncertainty(1–5) ≥ 18 OR any safety/legal/public/irreversible red flag."
jargon_bridge:
  - { clipcard_term: "Hazard", domain_term: "Risk of change / failure mode", notes: "What could go wrong, where, and how" }
  - { clipcard_term: "Recheck Steward", domain_term: "On-call / Change Owner", notes: "Owns the calendar ping, not the blame" }
  - { clipcard_term: "Authority Window", domain_term: "Limited rollout / feature flag scope", notes: "Deliberate blast radius control" }
  - { clipcard_term: "Two-Key / TTL", domain_term: "Dual approval / time-limited change", notes: "Big moves expire or need a buddy" }
  - { clipcard_term: "Kill Criteria", domain_term: "Rollback triggers / redlines", notes: "Observable thresholds → immediate rollback" }
metrics:
  - { name: "change_failure_rate", definition: "Failed changes / total changes in period (use DORA definition or your CAB label)", target: "Lower than baseline", method: "proportion vs. prior 4–8 weeks" }
  - { name: "mttr", definition: "Mean time to rollback/recover for failed changes", target: "Lower than baseline", method: "median preferred; robust to outliers" }
  - { name: "recheck_on_time", definition: "Share of ClipCard rechecks completed by due time", target: "≥80%", method: "binary on-time per card → daily/weekly proportion" }
seeds:
  - { seed_id: "seed.devops.clipcard.ci_gate", seed_type: "yaml", language: "YAML", summary: "GitHub Actions gate: on PRs labeled high-risk, require a *.clipcard.json file" }
  - { seed_id: "seed.devops.adr.block", seed_type: "text", language: "TEXT", summary: "ADR Risk & Recheck section you can paste into existing ADRs" }
license: "Docs/Templates: CC-BY-SA-4.0; Snippets/Code: MIT"
contacts: []
---

# 1) Purpose & Trigger

**Trigger Rubrics (optional, 1–5):**
- **Reversibility:** 1 = trivial undo (toggle, no loss); 3 = rollback with brief impact/manual cleanup; 5 = irrecoverable or public/legal/clinical harm if wrong.
- **Coupling:** 1 = isolated component/unit; 3 = affects 1–2 dependent systems/wards; 5 = tightly coupled, cascades likely across systems/regions.
*Guidance:* You may trigger ClipCard if either score ≥ 4, even when `Impact×Uncertainty < 18`. Use sparingly to avoid fatigue.

When a change is both **high-impact** and **uncertain**, add a one-page **ClipCard** to the ticket/ADR/PR.  
It forces seven things in DevOps terms: **risk statement (hazard)**, **dated recheck or jump**, **steward**, **authority window** (blast-radius limit), **two-key/TTL** (big changes need a buddy or expire), **kill criteria** (rollback triggers), and **evidence links** (load tests, past incidents).

**Trigger:** `Impact (1–5) × Uncertainty (1–5) ≥ 18` **OR** red flag (safety/legal/public/irreversible).

# 2) Jargon Bridge
| ClipCard term | DevOps/SRE term | Notes |
|---|---|---|
| Hazard | Risk of change / failure mode | “If X, then Y fails in Z region/service.” |
| Recheck Steward | On-call / Change Owner | Owns the reminder only; team owns the outcome. |
| Authority Window | Limited rollout / feature flag scope | e.g., 10% of users, 2 hours. |
| Two-Key / TTL | Dual approval / time-limited change | Approver A + B; auto-expire if not extended. |
| Kill Criteria | Rollback triggers / redlines | e.g., error_rate > 1%, SLO breach, spike in 5xx. |
| Evidence Links | Load test, runbooks, related incidents | Snapshot permalinks or artifact hashes. |

# 3) Placement Patterns (Where it Clips On)
- **Change ticket**: attach ClipCard text block; store machine copy as `TICKET-123.clipcard.json`.
- **ADR**: add “Risk & Recheck” section (seed below).
- **Incident PR**: include ClipCard in PR description; set recheck as a calendar invite or bot reminder.

# 4) Seeds (Copy-Paste)

**Seed:** `seed.devops.clipcard.ci_gate` — _GitHub Actions: require a ClipCard for high-risk PRs_
```YAML
# seed_id: seed.devops.clipcard.ci_gate
# seed_type: yaml
# language: YAML
name: clipcard-check
on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]
jobs:
  require-clipcard-on-high-risk:
    if: contains(github.event.pull_request.labels.*.name, 'high-risk')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Find ClipCard JSON
        id: find
        run: |
          MATCHES=$(git ls-files '*.clipcard.json' | wc -l | tr -d ' ')
          echo "count=${MATCHES}" >> $GITHUB_OUTPUT
      - name: Fail if missing
        if: steps.find.outputs.count == '0'
        run: |
          echo "::error::High-risk PR requires a *.clipcard.json (see templates)."
          exit 1
      # Optional: basic JSON sanity (jq)
      - name: Validate JSON presence of required fields
        if: steps.find.outputs.count != '0'
        run: |
          for f in $(git ls-files '*.clipcard.json'); do
            jq -e 'has("hazard") and has("recheck") and has("steward") and has("authority_window") and has("kill_criteria")' "$f" >/dev/null || { echo "::error file=$f::Missing required fields"; exit 2; }
          done
````

**Seed:** `seed.devops.adr.block` — *ADR “Risk & Recheck” section*

```TEXT
;; seed_id: seed.devops.adr.block | seed_type: text | language: TEXT
## Risk & Recheck (ClipCard)
**Hazard** — If <trigger> then <failure> [in <service/region>].  
**Recheck / Jump** — <date/time UTC or alert condition>  
**Recheck Steward (backup)** — <name/role> (<backup>)  
**Authority Window** — <scope % / duration> (+ auto-pause/rollback?)  
**Two-Key / TTL** — <approver A> + <approver B>, TTL <hours> (or N/A)  
**Kill Criteria → Action** — If <observable threshold> then <immediate rollback>  
**Evidence Links** — <load test, runbook, prior incident, dashboards>
```

# 5) 1-Minute Audit (Pass/Fail)

* Hazard is **specific** (trigger → failure → where).
* **Measurable** kill criteria & **immediate action**.
* **Dated recheck** or a clear **jump trigger** (alert).
* **Steward named** (backup optional).
* **Authority window** set (scope/time).
* **Evidence links** present (stable/snapshotted).

# 6) Metrics & Definitions

* **change_failure_rate**: failed changes/total changes per week. *Target:* lower than baseline.
* **mttr**: median time from incident start to rollback/recovery. *Target:* lower than baseline.
* **recheck_on_time**: % ClipCards with recheck completed by due time. *Target:* ≥80%.

# 7) Objections → Replies

* “We already have templates.” → ClipCard adds a **dated recheck** + **rollback triggers**; 60–90 seconds on only high-risk items.
* “Extra process slows us down.” → It **shrinks blast radius** and **catches rollbacks sooner**; low-risk flow is untouched.
* “This will scapegoat the steward.” → Policy: **team owns outcomes; steward owns the calendar ping**. It’s blame-safe.

# 8) Field Drill (15 minutes)

1. Pick one high-risk change slated this week.
2. Fill the ADR block + machine JSON exemplar (Appendix B).
3. Put the recheck on a shared calendar; wire one kill criterion to an alert.
4. After deployment, note if any redlines hit; execute rollback if so.
5. Log whether recheck was on time; share a one-line field note.

# 9) Notebook Placeholders (for Post-Process)

* **NOTEBOOK_PLACEHOLDER:** `clipcard_devops_sim.ipynb` — Monte Carlo of rollout sizes vs. rollback thresholds; outputs expected incident reduction and MTTR deltas given authority windows.
* **NOTEBOOK_PLACEHOLDER:** `clipcard_field_eval_devops.ipynb` — Reads weekly change logs + ClipCard logs; computes CFR, MTTR, and recheck_on_time with CIs vs. pre-period baseline.
* **NOTEBOOK_PLACEHOLDER:** `clipmap_viz_devops.ipynb` — Graph of hazard→recheck→outcome over time; highlights repeated failure modes.

# 10) Glossary & Roles (Blame-Safe)

* **Team** owns the outcome; **Steward** owns the reminder.
* **Change Owner**: submits ClipCard; **Approvers (Two-Key)**: dual sign-off on high-impact actions; **On-call**: executes kill criteria when redlines trigger.

## Appendix A — Human Template (ClipCard.md, DevOps)

```TEXT
**Hazard**: If <new job mis-parses CSV> then <double-charges> [in <EU billing>].
**Recheck / Jump**: 2025-11-10T17:00:00Z OR alert:billing_errors>50/min
**Recheck Steward (backup)**: Ops On-Call (Billing Lead)
**Authority Window**: 10% users, 2h, auto-pause on alert
**Two-Key / TTL**: EngMgr + SRELead, TTL 4h
**Kill Criteria → Action**:
- If error_rate > 1% → rollback
- If any double_charge → rollback
**Evidence Links**:
- Load test report: <link/snapshot>
- Incident INC-2045: <link>
- Runbook: <link>
```

## Appendix B — Machine Template (ClipCard.json exemplar, DevOps)

```json
{
  "id": "BILLING-CHANGE-2049",
  "linked_item": "JIRA-BILL-123",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If new billing job mis-parses CSV, then double-charges occur in EU region.",
  "recheck": { "due_time": "2025-11-10T17:00:00Z", "jump_trigger": "alert:billing_errors>50/min" },
  "steward": { "primary": "Ops On-Call", "backup": "Billing Lead" },
  "authority_window": { "scope_limit": "10% users", "time_limit": "2h", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["EngMgr","SRELead"], "ttl_hours": 4 },
  "kill_criteria": [
    { "condition": "error_rate > 0.01", "action": "rollback" },
    { "condition": "any_double_charge == true", "action": "rollback" }
  ],
  "evidence_links": [
    { "name": "Load Test", "url": "https://example.com/perf.pdf" },
    { "name": "Incident INC-2045", "url": "https://example.com/inc-2045" },
    { "name": "Runbook", "url": "https://example.com/runbook" }
  ]
}
```

---



# Insert immediately under "1) Purpose & Trigger"
ClipCard is an engineered defense against local-minima failure modes (ETTO). It adds bounded authority, pre-agreed kill criteria, and a dated recheck only when risk is high, preserving speed elsewhere.  
**Trigger (expanded):** Use ClipCard when `Impact×Uncertainty ≥ 18` OR `reversibility ≥ 4` OR `coupling ≥ 4` OR `equity_rights_sensitivity = true` OR any safety/legal/public/irreversible red flag.

---



**Privacy:** Redact PHI/PII in evidence. You may include hashes/permits instead of snapshots.
