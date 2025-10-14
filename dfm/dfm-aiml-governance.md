---

dfm_id: "ai-ml-governance"
title: "DFM: AI / ML Governance & Alignment Ops — ClipCard (Risk & Recheck)"
version: "1.0"
domain: "Model Release, Safety Evaluation, Policy & Risk Boards"
trigger_rule: "Use ClipCard when Impact(1–5) × Uncertainty(1–5) ≥ 18 OR any safety/legal/public/irreversible red flag (e.g., privacy leakage, bio/dual-use, bias/rights risk, financial harm, safety-critical integration)."
jargon_bridge:

* { clipcard_term: "Hazard", domain_term: "Model risk / eval failure mode", notes: "If X scenario occurs, Y harm in Z user/domain." }
* { clipcard_term: "Recheck Steward", domain_term: "Release Manager / Safety Reviewer", notes: "Owns the review reminder; team owns outcomes." }
* { clipcard_term: "Authority Window", domain_term: "Staged release / limited users / guarded capability", notes: "Who gets access, where, for how long; reversible by design." }
* { clipcard_term: "Two-Key / TTL", domain_term: "Safety + Product approvals / sunset timer", notes: "Dual sign-off and timed re-review requirement." }
* { clipcard_term: "Kill Criteria", domain_term: "Redline metrics / rollback triggers", notes: "Observable thresholds (abuse, privacy, bias) that halt exposure." }
  metrics:
* { name: "post_release_incidents", definition: "Safety incidents per 10k interactions (validated reports, bug bounty, incident triage)", target: "Decrease vs. baseline or ≤ policy threshold", method: "rate with 95% CI" }
* { name: "eval_escape_rate", definition: "Known eval failure patterns observed post-release (e.g., jailbreaks hitting redlines) per 10k interactions", target: "≈ 0 (at or below tolerance)", method: "rate; anomaly detection on drift" }
* { name: "review_on_time", definition: "Share of ClipCard-scheduled reviews completed by TTL date", target: "≥80%", method: "binary on-time flag → weekly proportion" }
  seeds:
* { seed_id: "seed.aiml.release.clipcard", seed_type: "json", language: "JSON", summary: "Model release ClipCard exemplar with eval gates, authority window, and kill criteria" }
* { seed_id: "seed.aiml.ci_eval_gate", seed_type: "yaml", language: "YAML", summary: "CI gate: require *.clipcard.json + passing eval summary on high-risk releases" }
* { seed_id: "seed.aiml.modelcard.block", seed_type: "text", language: "TEXT", summary: "Model Card ‘Risk & Recheck’ add-on (paste into existing Model Card template)" }
  license: "Docs/Templates: CC-BY-SA-4.0; Snippets/Code: MIT"
  contacts: []

---

# 1) Purpose & Trigger

**Trigger Rubrics (optional, 1–5):**
- **Reversibility:** 1 = trivial undo (toggle, no loss); 3 = rollback with brief impact/manual cleanup; 5 = irrecoverable or public/legal/clinical harm if wrong.
- **Coupling:** 1 = isolated component/unit; 3 = affects 1–2 dependent systems/wards; 5 = tightly coupled, cascades likely across systems/regions.
*Guidance:* You may trigger ClipCard if either score ≥ 4, even when `Impact×Uncertainty < 18`. Use sparingly to avoid fatigue.


Model releases and capability unlocks can create irreversible harm. **ClipCard** is a one-page add-on used **only** when a change is **high-impact** and **uncertain**. In AI/ML terms it forces: **risk statement (hazard)**, **dated re-review (recheck) or jump condition**, **steward** (Release Manager/Safety), **authority window** (staged exposure/guardrails), **two-key/TTL** (dual approvals and sunset), **kill criteria** (redline metrics → rollback), and **evidence links** (eval reports, red-team results, model card snapshot).

**Trigger:** `Impact × Uncertainty ≥ 18` **or** red flag (privacy leakage, bio/dual-use enabling, discriminatory bias, child safety, financial/medical harm, critical infra).

# 2) Jargon Bridge

| ClipCard term    | AI/ML Governance term                 | Notes                                                                   |
| ---------------- | ------------------------------------- | ----------------------------------------------------------------------- |
| Hazard           | Model risk / eval failure mode        | “If prompt X, model leaks PII; if tool Y, enables actionable dual-use.” |
| Recheck Steward  | Release Manager / Safety Reviewer     | Owns the review reminder; not a scapegoat.                              |
| Authority Window | Staged release / guarded capability   | % users, regions, capability flags, rate limits, eval-only sandboxes.   |
| Two-Key / TTL    | Safety + Product approvals / sunset   | Renewal requires evidence at TTL.                                       |
| Kill Criteria    | Redline metrics / rollback triggers   | Abuse > threshold, PII leak > 0, bias drift, tool-call anomalies.       |
| Evidence Links   | Eval report, red-team log, model card | Stable permalinks or snapshots (versioned).                             |

# 3) Placement Patterns (Where it Clips On)

* **Release notes / launch PR:** add the ClipCard summary; attach machine JSON exemplar.
* **Model Card:** paste “Risk & Recheck” block (seed below) with TTL and kill criteria.
* **Safety Review packet:** include ClipCard on the cover page with authority window and two-key approvers.

# 4) Seeds (Copy-Paste)

**Seed:** `seed.aiml.release.clipcard` — *Model release ClipCard exemplar (JSON)*

```json
// seed_id: seed.aiml.release.clipcard
// seed_type: json
// language: JSON
{
  "id": "LLM-RELEASE-042",
  "linked_item": "RELEASE-NOTE-2025-11-15",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If advanced tool-use is enabled for general users, prompt-injection and PII exfiltration may increase in EN markets.",
  "recheck": { "due_time": "2025-12-15T00:00:00Z", "jump_trigger": "abuse_rate_24h > 1.3 * baseline OR pii_leak_count_24h >= 1" },
  "steward": { "primary": "Release Manager", "backup": "Safety Reviewer" },
  "authority_window": { "scope_limit": "EN markets; 5% cohort; no API; no unvetted tools", "time_limit": "30d", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["Head of Product","Head of Safety"], "ttl_hours": 720 },
  "kill_criteria": [
    { "condition": "pii_leak_count_24h >= 1", "action": "Disable tool-use for cohort; rotate keys; incident review within 24h" },
    { "condition": "jailbreak_hit_rate_24h > 0.5%", "action": "Tighten guardrails; reduce cohort to 1%; block risky tools" },
    { "condition": "bias_drift_score > 2.0 SD from baseline", "action": "Rollback capability; run targeted re-evals" }
  ],
  "evidence_links": [
    { "name": "Eval Report v0.9 (Safety/Bias/PII)", "url": "https://example.org/evals/llm-042.pdf" },
    { "name": "Red-team Findings (Nov 2025)", "url": "https://example.org/redteam/rt-nov25" },
    { "name": "Model Card Snapshot", "url": "https://example.org/modelcard/llm-042" }
  ]
}
```

**Seed:** `seed.aiml.ci_eval_gate` — *CI gate for high-risk model releases (GitHub Actions example)*

```YAML
# seed_id: seed.aiml.ci_eval_gate
# seed_type: yaml
# language: YAML
name: eval-and-clipcard-check
on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]
jobs:
  require-clipcard-and-eval:
    if: contains(github.event.pull_request.labels.*.name, 'high-risk')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Ensure ClipCard JSON present
        id: card
        run: |
          COUNT=$(git ls-files '*release*.clipcard.json' '*.clipcard.json' | wc -l | tr -d ' ')
          echo "count=${COUNT}" >> $GITHUB_OUTPUT
          if [ "$COUNT" = "0" ]; then
            echo "::error::High-risk PR requires a ClipCard JSON (see templates)."
            exit 1
          fi
      - name: Validate ClipCard fields
        run: |
          for f in $(git ls-files '*release*.clipcard.json' '*.clipcard.json'); do
            jq -e 'has("hazard") and has("recheck") and has("steward") and has("authority_window") and has("kill_criteria") and (.kill_criteria|length>0)' "$f" >/dev/null || { echo "::error file=$f::Missing required fields"; exit 2; }
          done
      - name: Check eval summary thresholds (mock example)
        run: |
          if [ ! -f evals/summary.json ]; then
            echo "::error::Missing evals/summary.json with pass/fail indicators."
            exit 3
          fi
          JAILBREAK=$(jq -r '.jailbreak_hit_rate' evals/summary.json)
          PII=$(jq -r '.pii_leak_count' evals/summary.json)
          BIAS=$(jq -r '.bias_drift_sd' evals/summary.json)
          awk "BEGIN{exit !($JAILBREAK <= 0.005 && $PII == 0 && $BIAS <= 2.0)}" || { echo "::error::Eval thresholds not met (see policy)."; exit 4; }
```

**Seed:** `seed.aiml.modelcard.block` — *Model Card “Risk & Recheck” section*

```TEXT
;; seed_id: seed.aiml.modelcard.block | seed_type: text | language: TEXT
## Risk & Recheck (ClipCard)
**Hazard** — If <capability/policy> then <harm> [in <user/domain/market>].  
**Authority Window** — <cohort %, regions, tool flags, rate limits, sandbox>  
**Two-Key / TTL** — Approvers: <Safety> + <Product>; TTL <days>  
**Kill Criteria → Action** — If <redline metric(s)> then <rollback/disable> within <N> hours  
**Recheck / Jump** — <date UTC> OR <condition (e.g., pii_leak_count_24h ≥ 1)>  
**Steward (backup)** — <Release Manager> (<Safety Reviewer>)  
**Evidence** — Eval report, red-team log, model card snapshot (stable links)
```

# 5) 1-Minute Audit (Pass/Fail)

* Hazard names **capability → harm → scope**.
* **Measurable** redlines + explicit **rollback actions**.
* **Dated re-review** or **jump**.
* **Steward named** (backup optional).
* **Authority window** bounded (cohort/region/capability/time).
* **Evidence links** present and **versioned**.

# 6) Metrics & Definitions

* **post_release_incidents:** validated incident reports per 10k interactions. *Target:* ≤ threshold or **↓ vs baseline**.
* **eval_escape_rate:** rate of known eval failure patterns occurring post-release. *Target:* **≈ 0** at tolerance.
* **review_on_time:** % of TTL reviews completed by due date. *Target:* **≥80%**.

# 7) Objections → Replies

* “We already run evals.” → ClipCard **binds evals to a dated review and rollback triggers**; not more tests—**more accountability**.
* “This slows feature velocity.” → **Staged authority window** allows fast, **reversible** exposure; low-risk work is untouched.
* “Stewards will get blamed.” → Policy: **team owns outcomes; steward owns the reminder** (ceremony), not culpability.

# 8) Field Drill (15 minutes)

1. Choose one upcoming **high-risk** capability (e.g., tool-use, untrusted plug-ins).
2. Fill the Model Card block; attach JSON ClipCard to the release PR.
3. Enable CI gate for high-risk label; set **two-key** approvers and **TTL 30d**.
4. Wire **one** kill criterion to telemetry (e.g., PII detector, abuse monitor).
5. At TTL (or on jump), review data and post a one-line field note (rollback? redlines? on-time review?).

# 9) Notebook Placeholders (for Post-Process)

* **NOTEBOOK_PLACEHOLDER:** `clipcard_aiml_sim.ipynb` — Simulate cohort size × authority windows × redlines; estimate expected incident reduction and false positive burden.
* **NOTEBOOK_PLACEHOLDER:** `clipcard_field_eval_aiml.ipynb` — Ingest release telemetry + ClipCards; compute incident rate, eval_escape_rate, review_on_time vs. pre-period with CIs; optional ITS.
* **NOTEBOOK_PLACEHOLDER:** `clipmap_viz_aiml.ipynb` — Hazard→recheck→outcome graph by capability; highlight recurrent failure patterns.

# 10) Glossary & Roles (Blame-Safe)

* **Team** owns the outcome; **Steward** (Release/Safety) owns the review cadence.
* **Two-Key:** Safety + Product (or Legal for rights-sensitive changes).
* **TTL:** automatic sunset unless renewed **after** evidence review.

## Appendix A — Human Template (ClipCard.md, AI/ML)

```TEXT
**Hazard**: If <enable code-exec tool> then <prompt-injection → data exfil> [scope: EN users; IDE plug-in].
**Recheck / Jump**: 2025-12-15T00:00:00Z OR pii_leak_count_24h ≥ 1
**Recheck Steward (backup)**: Release Manager (Safety Reviewer)
**Authority Window**: 5% EN users; API off; rate limit 10/min; sandbox tools only
**Two-Key / TTL**: Head of Safety + Head of Product; TTL 30d
**Kill Criteria → Action**:
- If pii_leak_count_24h ≥ 1 → Disable tool; rotate keys; incident review ≤24h
- If jailbreak_hit_rate_24h > 0.5% → Reduce cohort to 1%; tighten filters
**Evidence Links**: Eval Report v0.9; Red-team Nov 2025; Model Card snapshot
```

## Appendix B — Machine Template (ClipCard.json exemplar, AI/ML)

```json
{
  "id": "CAP-ENABLE-PLUGINS-007",
  "linked_item": "PR-4821",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If code-execution plugins are enabled broadly, prompt-injection may lead to data exfiltration for EN users.",
  "recheck": { "due_time": "2025-12-15T00:00:00Z", "jump_trigger": "pii_leak_count_24h >= 1 OR jailbreak_hit_rate_24h > 0.5" },
  "steward": { "primary": "Release Manager", "backup": "Safety Reviewer" },
  "authority_window": { "scope_limit": "EN users 5%; API disabled; sandboxed plugins; rate=10/min", "time_limit": "30d", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["Head of Safety","Head of Product"], "ttl_hours": 720 },
  "kill_criteria": [
    { "condition": "pii_leak_count_24h >= 1", "action": "Disable plugins; rotate credentials; incident review ≤24h" },
    { "condition": "jailbreak_hit_rate_24h > 0.5", "action": "Reduce cohort to 1%; tighten guardrails; re-evaluate" }
  ],
  "evidence_links": [
    { "name": "Eval Report v0.9", "url": "https://example.org/eval-plugins" },
    { "name": "Red-team Nov 2025", "url": "https://example.org/redteam-nov25" },
    { "name": "Model Card Snapshot", "url": "https://example.org/modelcard-plugins" }
  ]
}
```

```
::contentReference[oaicite:0]{index=0}
```


# Insert immediately under "1) Purpose & Trigger"
ClipCard is an engineered defense against local-minima failures in AI/ML governance: staged exposure, dual approvals, and redline metrics tied to rollback.  
**Trigger (expanded):** Use when `Impact×Uncertainty ≥ 18` OR `reversibility ≥ 4` OR `coupling ≥ 4` OR `equity_rights_sensitivity = true` OR any safety/legal/public/irreversible red flag.

---



**Privacy:** Redact PHI/PII in evidence. You may include hashes/permits instead of snapshots.
