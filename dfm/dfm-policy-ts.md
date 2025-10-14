---

dfm_id: "policy-ts"
title: "DFM: Policy / Trust & Safety — ClipCard (Risk & Recheck)"
version: "1.0"
domain: "Policy, Trust & Safety, Governance"
trigger_rule: "Use ClipCard when Impact(1–5) × Uncertainty(1–5) ≥ 18 OR any safety/legal/public/irreversible red flag (e.g., rights risk, systemic bias, irreversible user harm)."
jargon_bridge:

* { clipcard_term: "Hazard", domain_term: "Harm/rights risk (FP/FN scenarios)", notes: "If rule X launches, then Y group faces Z harm." }
* { clipcard_term: "Recheck Steward", domain_term: "Policy Owner", notes: "Owns the recheck reminder; team owns outcomes." }
* { clipcard_term: "Authority Window", domain_term: "Pilot scope / staged rollout", notes: "Who is included, where, how long; reversible by design." }
* { clipcard_term: "Two-Key / TTL", domain_term: "Legal+Policy dual approval / Sunset date", notes: "Big changes need both sign-offs and an automatic review by a date." }
* { clipcard_term: "Kill Criteria", domain_term: "Pause/rollback thresholds (appeals/incidents)", notes: "Observable triggers to halt and reassess." }
  metrics:
* { name: "wrongful_action_rate", definition: "Verified wrongful enforcement actions per 10,000 decisions", target: "Decrease vs. baseline", method: "proportion with 95% CI" }
* { name: "appeal_rate", definition: "Appeals per 1,000 enforcement actions (or policy decisions)", target: "Decrease vs. baseline (or stable with improved precision)", method: "proportion with trend check" }
* { name: "review_on_time", definition: "Share of ClipCard policy reviews completed by TTL date", target: "≥80%", method: "binary on-time flag → weekly proportion" }
  seeds:
* { seed_id: "seed.policy.ttl.twokey.card", seed_type: "text", language: "TEXT", summary: "Policy ClipCard with TTL, Two-Key sign-off, and measurable kill criteria" }
* { seed_id: "seed.policy.memo.block", seed_type: "text", language: "TEXT", summary: "Policy Change Memo section: Risk & Recheck block to paste into templates" }
  license: "Docs/Templates: CC-BY-SA-4.0; Snippets/Code: MIT"
  contacts: []

---

# 1) Purpose & Trigger

**Trigger Rubrics (optional, 1–5):**
- **Reversibility:** 1 = trivial undo (toggle, no loss); 3 = rollback with brief impact/manual cleanup; 5 = irrecoverable or public/legal/clinical harm if wrong.
- **Coupling:** 1 = isolated component/unit; 3 = affects 1–2 dependent systems/wards; 5 = tightly coupled, cascades likely across systems/regions.
*Guidance:* You may trigger ClipCard if either score ≥ 4, even when `Impact×Uncertainty < 18`. Use sparingly to avoid fatigue.


High-impact policy changes and enforcement rules carry rights risk and reputational/legal exposure. **ClipCard** is a one-page add-on used **only** when a policy decision is both **high-impact** and **uncertain**. It forces: **harm/rights risk (hazard)**, **dated review (recheck) or jump**, **steward (policy owner)**, **authority window** (pilot scope/staged rollout), **two-key/TTL** (Legal + Policy approvals; time-boxed sunset), **kill criteria** (appeal/incident thresholds), and **evidence links** (risk assessments, legal memos, user research).

**Trigger:** `Impact × Uncertainty ≥ 18` **or** red flag (rights risk, systemic bias, legal/public/irreversible harm).

# 2) Jargon Bridge

| ClipCard term    | Policy/T&S term                    | Notes                                                                |
| ---------------- | ---------------------------------- | -------------------------------------------------------------------- |
| Hazard           | Harm/rights risk (FP/FN scenarios) | “If we broaden rule X, FN for hate increases; FP for satire spikes.” |
| Recheck Steward  | Policy Owner                       | Owns the reminder; not a scapegoat.                                  |
| Authority Window | Pilot scope / staged rollout       | Region, cohort %, languages; reversible.                             |
| Two-Key / TTL    | Legal + Policy approvals / Sunset  | Dual sign-off; renewal requires review.                              |
| Kill Criteria    | Pause/rollback thresholds          | Appeals/day > N, complaint spike, incident class ≥ S2.               |
| Evidence Links   | Risk assess, legal memo, URX       | Stable links or snapshots (hash/version).                            |

# 3) Placement Patterns (Where it Clips On)

* **Policy Change Memo:** add Risk & Recheck block (seed below).
* **Safety Review / Launch Gate:** include ClipCard summary at the top; TTL visible.
* **Enforcement Pilots:** attach ClipCard to pilot plan; recheck at TTL or jump.

# 4) Seeds (Copy-Paste)

**Seed:** `seed.policy.ttl.twokey.card` — *Policy ClipCard with TTL & Two-Key*

```TEXT
;; seed_id: seed.policy.ttl.twokey.card | seed_type: text | language: TEXT
### Policy ClipCard — Risk & Recheck
**Hazard** — If <policy X broadened> then <FP satire takedowns +20%> and <FN hate> [in <ES/PT markets>].  
**Recheck / Jump** — <2025-12-15T00:00:00Z> OR <appeals_rate_7d > 1.5× baseline>  
**Recheck Steward (backup)** — <Policy Owner> (<Safety Reviewer>)  
**Authority Window** — <ES/PT only>, <10% cohort>, <news vertical excluded>, duration <30d>  
**Two-Key / TTL** — Approvals: <Policy Lead> + <Legal Counsel>; TTL <30d> (auto-sunset if not renewed)  
**Kill Criteria → Action** — If <verified_wrongful_rate ≥ 0.8/10k OR S2 incident occurs> → **Pause policy & convene review within 48h**  
**Evidence Links** — <Risk Assessment v1.2>, <Legal Memo #LM-2025-41>, <URX study link/snapshot>, <Bias eval dashboards>
```

**Seed:** `seed.policy.memo.block` — *Policy Change Memo: Risk & Recheck section*

```TEXT
;; seed_id: seed.policy.memo.block | seed_type: text | language: TEXT
## Risk & Recheck (ClipCard)
**Hazard** — If <decision> then <harm/rights risk> [scope: <region/cohort/domain>].  
**Authority Window** — <pilot/staged rollout parameters (who/where/how long)>  
**Two-Key / TTL** — <dual approvers> ; TTL <days> (auto-sunset unless renewed after review)  
**Kill Criteria → Action** — If <appeals/incident threshold> then <pause/rollback + convene review in N hours>  
**Recheck / Jump** — <date/time UTC> OR <jump condition (e.g., appeals_rate_7d > threshold)>  
**Steward (backup)** — <policy owner> (<legal/safety co-steward>)  
**Evidence** — <risk assess, legal memo, user research, eval dashboards (stable/snapshotted)>
```

# 5) 1-Minute Audit (Pass/Fail)

* Hazard **specific** to cohorts/contexts; names FP/FN pattern.
* **Measurable** kill criteria with immediate action.
* **Dated recheck** or **jump**.
* **Steward named** (backup optional).
* **Authority window** bounded (scope/time).
* **Evidence links** included (stable/snapshotted).

# 6) Metrics & Definitions

* **wrongful_action_rate:** verified wrongful enforcement per 10k decisions. *Target:* **↓ vs baseline**.
* **appeal_rate:** appeals per 1k enforcements (or decisions). *Target:* **↓** or **stable with better precision**.
* **review_on_time:** % of TTL reviews completed by due date. *Target:* **≥80%**.

# 7) Objections → Replies

* “We already do reviews.” → This **time-boxes** the review (TTL), **dual-signs** high-risk calls, and defines **pre-agreed pause triggers**.
* “This slows urgent harm response.” → Use **authority window** to ship a **small, reversible pilot** fast; TTL ensures a scheduled revisit.
* “Creates legal exposure.” → **Pre-commit** to criteria and documentation reduces arbitrariness risk; dual approvals distribute accountability.

# 8) Field Drill (15 minutes)

1. Pick one upcoming policy change with public/rights risk.
2. Fill the memo block + set **TTL 30d** and **Two-Key** approvers.
3. Choose **two kill criteria** (e.g., appeals_rate_7d, verified_wrongful_rate, S-class incidents).
4. Put the recheck on the **policy calendar**; wire a **jump** if thresholds trip.
5. After TTL or jump, record outcomes and share an anonymized field note.

# 9) Notebook Placeholders (for Post-Process)

* **NOTEBOOK_PLACEHOLDER:** `clipcard_policy_sim.ipynb` — Simulate pilot scope/thresholds vs. pause frequency; estimate wrongful_action_rate and appeal_rate deltas under varying authority windows.
* **NOTEBOOK_PLACEHOLDER:** `clipcard_field_eval_policy.ipynb` — Ingest enforcement logs + ClipCards; compute metrics with CIs vs. pre-period baseline; segmented regression for step changes.
* **NOTEBOOK_PLACEHOLDER:** `clipmap_viz_policy.ipynb` — Visualize hazard→recheck→outcome across regions/cohorts; surface recurrent harm modes.

# 10) Glossary & Roles (Blame-Safe)

* **Team** owns outcomes; **Steward (Policy Owner)** owns the reminder and ceremony.
* **Two-Key:** Legal + Policy (or Safety + Policy) for high-impact changes.
* **TTL:** automatic sunset; renewal requires review and updated evidence.

## Appendix A — Human Template (ClipCard.md, Policy/T&S)

```TEXT
**Hazard**: If <expand hate classifier to memes> then <FP satire takedowns +FN coded hate> [scope: EN–US 10%].
**Recheck / Jump**: 2025-12-15T00:00:00Z OR appeals_rate_7d > 1.5× baseline
**Recheck Steward (backup)**: Policy Owner (Safety Reviewer)
**Authority Window**: EN–US only; 10% cohort; exclude news/politics; 30d pilot
**Two-Key / TTL**: Policy Lead + Legal Counsel; TTL 30d
**Kill Criteria → Action**:
- If verified_wrongful_rate ≥ 0.8/10k → Pause policy; convene review ≤48h
- If S2 incident (external harm report substantiated) → Pause immediately; notify exec/legal
**Evidence Links**: Risk Assessment v1.2; Legal Memo LM-2025-41; URX bias study snapshot; Eval dashboard permalink
```

## Appendix B — Machine Template (ClipCard.json exemplar, Policy/T&S)

```json
{
  "id": "POLICY-PILOT-ENUS-003",
  "linked_item": "POLICY-MEMO-2025-12-X",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If we expand the hate meme classifier, false positives on satire may increase while coded hate false negatives persist in EN–US.",
  "recheck": { "due_time": "2025-12-15T00:00:00Z", "jump_trigger": "appeals_rate_7d > 1.5 * baseline" },
  "steward": { "primary": "Policy Owner", "backup": "Safety Reviewer" },
  "authority_window": { "scope_limit": "EN–US 10% cohort; exclude news/politics", "time_limit": "30d", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["Policy Lead","Legal Counsel"], "ttl_hours": 720 },
  "kill_criteria": [
    { "condition": "verified_wrongful_rate_per_10k >= 0.8", "action": "Pause policy; convene review within 48h" },
    { "condition": "incident_severity >= 2", "action": "Immediate pause; notify exec/legal" }
  ],
  "evidence_links": [
    { "name": "Risk Assessment v1.2", "url": "https://example.org/risk-assess-1-2" },
    { "name": "Legal Memo LM-2025-41", "url": "https://example.org/legal-memo" },
    { "name": "URX Bias Study", "url": "https://example.org/urx-bias" },
    { "name": "Eval Dashboard", "url": "https://example.org/eval-dash" }
  ]
}
```

---



# Insert immediately under "1) Purpose & Trigger"
ClipCard is an engineered defense against local-minima failures in policy and T&S. It creates a bounded pilot (authority window), explicit pause triggers, and a dated TTL review.  
**Trigger (expanded):** Use when `Impact×Uncertainty ≥ 18` OR `reversibility ≥ 4` OR `coupling ≥ 4` OR `equity_rights_sensitivity = true` OR any safety/legal/public/irreversible red flag.

---



**Privacy:** Redact PHI/PII in evidence. You may include hashes/permits instead of snapshots.
