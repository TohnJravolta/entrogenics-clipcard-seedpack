---

dfm_id: "clinical-sbar"
title: "DFM: Clinical Ops / SBAR / QI — ClipCard (Risk & Recheck)"
version: "1.0"
domain: "Clinical Operations (SBAR, Handoffs, Quality Improvement)"
trigger_rule: "Use ClipCard when Impact(1–5) × Uncertainty(1–5) ≥ 18 OR any safety/legal/public/irreversible red flag (e.g., pediatric dosing, anticoagulation changes, procedure deviations)."
jargon_bridge:

* { clipcard_term: "Hazard", domain_term: "Clinical risk / failure mode", notes: "If X then Y harm in Z unit/patient group." }
* { clipcard_term: "Recheck Steward", domain_term: "Charge nurse / QI steward", notes: "Owns the reminder; not responsible for outcome alone." }
* { clipcard_term: "Authority Window", domain_term: "Trial dose/ward/time-box", notes: "Keep the intervention constrained (unit, dose range, time)." }
* { clipcard_term: "Two-Key / TTL", domain_term: "Double sign-off / time-limited order", notes: "Second checker (e.g., pharmacist/attending) and automatic sunset." }
* { clipcard_term: "Kill Criteria", domain_term: "Stop criteria (vitals/labs)", notes: "Observable thresholds that trigger immediate stop and notify." }
  metrics:
* { name: "near_miss_rate", definition: "Near-miss events logged per 100 SBAR handoffs for high-risk cases", target: "Increase vs. baseline (better detection)", method: "count near-miss / handoffs × 100" }
* { name: "preventable_escalations", definition: "Escalations judged preventable during RCA per 100 high-risk interventions", target: "Decrease vs. baseline", method: "RCA-labeled preventables / high-risk interventions × 100" }
* { name: "recheck_on_time", definition: "Share of ClipCard rechecks completed by due time or next operational period", target: "≥80%", method: "binary on-time flag per case → weekly proportion" }
  seeds:
* { seed_id: "seed.clinical.sbar.risk_block", seed_type: "text", language: "TEXT", summary: "SBAR add-on: R = Risk & Recheck block (copy/paste into handoff)" }
* { seed_id: "seed.clinical.smartphrase.epic", seed_type: "text", language: "TEXT", summary: "EHR SmartPhrase template for high-risk orders (double sign-off + stop criteria + recheck)" }
  license: "Docs/Templates: CC-BY-SA-4.0; Snippets/Code: MIT"
  contacts: []

---

# 1) Purpose & Trigger

**Trigger Rubrics (optional, 1–5):**
- **Reversibility:** 1 = trivial undo (toggle, no loss); 3 = rollback with brief impact/manual cleanup; 5 = irrecoverable or public/legal/clinical harm if wrong.
- **Coupling:** 1 = isolated component/unit; 3 = affects 1–2 dependent systems/wards; 5 = tightly coupled, cascades likely across systems/regions.
*Guidance:* You may trigger ClipCard if either score ≥ 4, even when `Impact×Uncertainty < 18`. Use sparingly to avoid fatigue.


Clinical environments run fast; small gaps compound into preventable harm. **ClipCard** is a one-page add-on used **only** when a handoff/intervention is both **high-impact** and **uncertain**. It forces seven elements in clinical language: **risk statement (hazard)**, **dated recheck or jump**, **steward (charge/QI)**, **authority window** (unit/dose/time bounds), **two-key/TTL** (double sign-off or time-limited order), **kill criteria** (vitals/lab redlines), and **evidence links** (guidelines, prior RCAs).

**Trigger:** `Impact × Uncertainty ≥ 18` **or** red flag (peds, anticoagulation, airway, high-alert meds, invasive procedures, public/legal risk).

# 2) Jargon Bridge

| ClipCard term    | Clinical/SBAR term                   | Notes                                                      |
| ---------------- | ------------------------------------ | ---------------------------------------------------------- |
| Hazard           | Clinical risk / failure mode         | “If weight not verified, peds dose may be 10×.”            |
| Recheck Steward  | Charge nurse / QI steward            | Owns the calendar/page; not the scapegoat.                 |
| Authority Window | Trial dose/ward/time-box             | Start on one ward, limited dose range, 12–24h time-box.    |
| Two-Key / TTL    | Double sign-off / time-limited order | Pharmacist + Attending; order auto-sunsets unless renewed. |
| Kill Criteria    | Stop criteria (vitals/labs)          | HR, MAP, SpO₂, INR, K⁺, EtCO₂ thresholds → stop & notify.  |
| Evidence Links   | Guideline, order set, prior RCA      | Stable links or snapshots in QI/EHR.                       |

# 3) Placement Patterns (Where it Clips On)

* **SBAR handoff:** add “R = Risk & Recheck” block (seed below).
* **High-alert med changes:** attach ClipCard to order/protocol note; set TTL + double sign-off.
* **Procedure deviations / temporary workflows:** add ClipCard to the deviation form; recheck at next huddle.

# 4) Seeds (Copy-Paste)

**Seed:** `seed.clinical.sbar.risk_block` — *SBAR “R = Risk & Recheck” add-on*

```TEXT
;; seed_id: seed.clinical.sbar.risk_block | seed_type: text | language: TEXT
### R = Risk & Recheck (ClipCard)
**Hazard** — If <weight not verified> then <peds dose 10×> [in <PICU>].  
**Recheck / Jump** — <2025-11-10T09:00:00Z> OR <alert: med_error_flag == true>  
**Recheck Steward (backup)** — <Charge RN> (<On-call Pharmacist>)  
**Authority Window** — <PICU only>, <dose capped per kg>, <time-box 24h>  
**Two-Key / TTL** — <Attending + Pharmacist co-sign>, TTL <24h>  
**Kill Criteria → Action** — If <SpO₂<90% or HR>160 or INR>3.5> → **Stop dose, notify Attending & Pharm, document**  
**Evidence Links** — <Peds dosing guideline>, <RCA-2024-17>, <Order set link/snapshot>
```

**Seed:** `seed.clinical.smartphrase.epic` — *EHR SmartPhrase for high-risk orders*

```TEXT
;; seed_id: seed.clinical.smartphrase.epic | seed_type: text | language: TEXT
.HIGHRISK_CLIPCARD
HAZARD: If {@TRIGGER} then {@FAILURE} [unit: {@UNIT}].
RECHECK: {@DATETIME_UTC} OR {@ALERT_CONDITION}
STEWARD: {@CHARGE_RN} (backup: {@PHARM})
AUTHORITY_WINDOW: unit={@UNIT}, dose={@DOSE_LIMIT}, timebox={@HOURS}h
TWO_KEY/TTL: signoff={@ATTENDING}+{@PHARM}; ttl={@HOURS}h
KILL_CRITERIA→ACTION:
- If {@VITALS_OR_LABS_REDLINE} → stop & notify Attending + Pharm; document.
EVIDENCE: {@GUIDELINE_LINK}; {@RCA_LINK}; {@ORDER_SET_LINK}
```

# 5) 1-Minute Audit (Pass/Fail)

* Hazard is **specific** (trigger → harm → unit/patient group).
* **Measurable** stop criteria with named **action**.
* **Dated recheck** or clear **alert jump**.
* **Steward named** (backup optional).
* **Authority window** bounded (unit/dose/time).
* **Evidence links** included (stable/snapshotted).

# 6) Metrics & Definitions

* **near_miss_rate:** near-miss events per 100 high-risk SBAR handoffs. *Target:* **↑** (better detection).
* **preventable_escalations:** RCA-labeled preventables per 100 high-risk interventions. *Target:* **↓**.
* **recheck_on_time:** % of ClipCards with recheck complete by due time or next op period. *Target:* **≥80%**.

# 7) Objections → Replies

* “It’s more paperwork.” → **Only** for high-risk; ~60–90 seconds; improves handoff clarity and RCA inputs.
* “We already double-check.” → ClipCard adds **dates, stop thresholds, and TTL** so the check is **timed and auditable**.
* “Stewards will get blamed.” → Policy: **team** owns outcomes; **steward** owns the reminder and paging flow (not culpability).

# 8) Field Drill (15 minutes)

1. Pick one **high-alert** case (e.g., anticoagulation change).
2. Fill the SBAR “R = Risk & Recheck” block + set TTL/sign-off.
3. Put recheck on the **unit calendar**; wire one redline to pager/alert.
4. After 24h, note redlines and whether recheck occurred on time.
5. Share an anonymized field note: near-miss? stop event? on-time recheck?

# 9) Notebook Placeholders (for Post-Process)

* **NOTEBOOK_PLACEHOLDER:** `clipcard_clinical_sim.ipynb` — Simulate high-alert med deviations with/without ClipCard; estimate reduction in preventable escalations under varying authority windows.
* **NOTEBOOK_PLACEHOLDER:** `clipcard_field_eval_clinical.ipynb` — Ingest SBAR logs + ClipCards; compute near_miss_rate, preventable_escalations, recheck_on_time with CIs vs. baseline.
* **NOTEBOOK_PLACEHOLDER:** `clipmap_viz_clinical.ipynb` — Visualize hazard→recheck→outcome sequences across units; surface recurring failure modes.

# 10) Glossary & Roles (Blame-Safe)

* **Team** owns outcomes; **Steward** (Charge/QI) owns the reminder/page cadence.
* **Two-Key**: Attending + Pharmacist (or relevant pair).
* **TTL**: time-limited orders auto-expire unless renewed post-recheck.

## Appendix A — Human Template (ClipCard.md, Clinical)

```TEXT
**Hazard**: If <weight not verified> then <peds dose 10×> [unit: PICU].
**Recheck / Jump**: 2025-11-10T09:00:00Z OR alert: med_error_flag == true
**Recheck Steward (backup)**: Charge RN (On-call Pharmacist)
**Authority Window**: PICU only; dose capped per kg; time-box 24h
**Two-Key / TTL**: Attending + Pharmacist; TTL 24h
**Kill Criteria → Action**:
- If SpO₂<90% or HR>160 or INR>3.5 → Stop dose; notify Attending + Pharm; document.
**Evidence Links**: Peds dosing guideline; RCA-2024-17; Order set snapshot
```

## Appendix B — Machine Template (ClipCard.json exemplar, Clinical)

```json
{
  "id": "PICU-ANTICOAG-0007",
  "linked_item": "SBAR-2025-11-09-PICU",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If weight not verified, pediatric anticoagulation dose may be 10× in PICU.",
  "recheck": { "due_time": "2025-11-10T09:00:00Z", "jump_trigger": "alert: med_error_flag == true" },
  "steward": { "primary": "Charge RN", "backup": "On-call Pharmacist" },
  "authority_window": { "scope_limit": "PICU only", "time_limit": "24h", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["Attending", "Pharmacist"], "ttl_hours": 24 },
  "kill_criteria": [
    { "condition": "SpO2 < 90", "action": "Stop dose; notify Attending + Pharm; document" },
    { "condition": "HR > 160", "action": "Stop dose; notify Attending + Pharm; document" },
    { "condition": "INR > 3.5", "action": "Stop dose; notify Attending + Pharm; document" }
  ],
  "evidence_links": [
    { "name": "Peds Dosing Guideline", "url": "https://example.org/peds-dose" },
    { "name": "RCA-2024-17", "url": "https://example.org/rca-2024-17" },
    { "name": "Order Set Snapshot", "url": "https://example.org/orderset" }
  ]
}
```

---



# Insert immediately under "1) Purpose & Trigger"
ClipCard is an engineered defense against local-minima failure modes (ETTO) in clinical operations. It adds bounded authority, explicit stop rules, and a dated recheck only for high-risk cases.  
**Trigger (expanded):** Use when `Impact×Uncertainty ≥ 18` OR `reversibility ≥ 4` OR `coupling ≥ 4` OR `equity_rights_sensitivity = true` OR any safety/legal/public/irreversible red flag. Add a de-identification note to evidence links.

---



**Privacy:** Redact PHI/PII in evidence. You may include hashes/permits instead of snapshots.
