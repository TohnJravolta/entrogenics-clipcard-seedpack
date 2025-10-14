---

dfm_id: "civic-ics"
title: "DFM: Civic / NGO / Emergency Ops (ICS) — ClipCard (Risk & Recheck)"
version: "1.0"
domain: "Incident Command System (ICS), Emergency Ops, Civic/NGO Programs"
trigger_rule: "Use ClipCard when Impact(1–5) × Uncertainty(1–5) ≥ 18 OR any safety/public/irreversible red flag (e.g., life-safety exposure, public trust, critical logistics)."
jargon_bridge:

* { clipcard_term: "Hazard", domain_term: "Operational risk / mission failure mode", notes: "If X intervention runs, Y failure can occur in Z division/group." }
* { clipcard_term: "Recheck Steward", domain_term: "Ops Section Chief / Planner", notes: "Owns the recheck reminder at the next OP brief; team owns outcome." }
* { clipcard_term: "Authority Window", domain_term: "Experimental scope for one Operational Period", notes: "Bound by Division/Group, population, geography, and time." }
* { clipcard_term: "Two-Key / TTL", domain_term: "OPS + PLANS sign-off / demob time", notes: "Dual approval and automatic demobilization unless renewed." }
* { clipcard_term: "Kill Criteria", domain_term: "Demobilization triggers", notes: "Observable thresholds (safety, queues, stockouts) that stop/adjust ops." }
  metrics:
* { name: "near_miss_rate", definition: "Near-miss notes per Operational Period for high-risk interventions", target: "Increase vs. baseline (better detection)", method: "count near-miss / OP" }
* { name: "avoidable_reversals", definition: "Reversals/diversions judged avoidable by After-Action Review (AAR)", target: "Decrease vs. baseline", method: "proportion per OP with AAR tag" }
* { name: "recheck_on_time", definition: "Share of ClipCards rechecked at the scheduled OP briefing", target: "≥80%", method: "binary on-time flag per card" }
  seeds:
* { seed_id: "seed.civic.ics.risk_recheck", seed_type: "text", language: "TEXT", summary: "ICS block: Risk & Recheck with demobilization triggers (paste into ICS-202/204)" }
* { seed_id: "seed.civic.ics.opcalendar", seed_type: "text", language: "TEXT", summary: "Operational Period recheck calendar note for IAP" }
  license: "Docs/Templates: CC-BY-SA-4.0; Snippets/Code: MIT"
  contacts: []

---

# 1) Purpose & Trigger

**Trigger Rubrics (optional, 1–5):**
- **Reversibility:** 1 = trivial undo (toggle, no loss); 3 = rollback with brief impact/manual cleanup; 5 = irrecoverable or public/legal/clinical harm if wrong.
- **Coupling:** 1 = isolated component/unit; 3 = affects 1–2 dependent systems/wards; 5 = tightly coupled, cascades likely across systems/regions.
*Guidance:* You may trigger ClipCard if either score ≥ 4, even when `Impact×Uncertainty < 18`. Use sparingly to avoid fatigue.


Emergency operations move fast; uncertainty is high. **ClipCard** is a one-page add-on used **only** when an action is **high-impact** and **uncertain**. It forces ICS-friendly elements: **operational hazard**, **dated recheck at next OP brief (or jump)**, **steward** (OPS/PLANS), **authority window** (Div/Group/time/population), **two-key/TTL** (OPS+PLANS approval and auto-demob), **kill criteria** (demobilization triggers), and **evidence links** (IAP pages, maps, safety plans).

**Trigger:** `Impact × Uncertainty ≥ 18` **or** life-safety/public trust/irreversible harm risk.

# 2) Jargon Bridge

| ClipCard term    | ICS/Civic term                          | Notes                                                                   |
| ---------------- | --------------------------------------- | ----------------------------------------------------------------------- |
| Hazard           | Operational risk / mission failure mode | “If we open Site C with limited staff, crowding & heat exposure spike.” |
| Recheck Steward  | OPS Section Chief / Planner             | Owns recheck during OP briefing; not a scapegoat.                       |
| Authority Window | Experimental scope (one OP)             | Div/Group, geofence, hours, population cap.                             |
| Two-Key / TTL    | OPS + PLANS approval / demob time       | Renewal only after recheck.                                             |
| Kill Criteria    | Demobilization triggers                 | Queue length, stockouts, incident class, safety reports.                |
| Evidence Links   | IAP (ICS-202/204/205/206), maps         | Stable IAP links, snapshots.                                            |

# 3) Placement Patterns (Where it Clips On)

* **ICS-202 (Incident Objectives):** add a “Risk & Recheck (ClipCard)” box referencing Div/Group actions.
* **ICS-204 (Assignment List):** attach ClipCard to specific Div/Group tasking; show TTL/demob and kill triggers.
* **OP Brief:** steward reads rechecks due; renew/demob decisions recorded in IAP.

# 4) Seeds (Copy-Paste)

**Seed:** `seed.civic.ics.risk_recheck` — *ICS “Risk & Recheck” block (paste into ICS-202/204)*

```TEXT
;; seed_id: seed.civic.ics.risk_recheck | seed_type: text | language: TEXT
### Risk & Recheck (ClipCard)
**Hazard** — If <open Cooling Center C with reduced staff> then <queueing + heat exposure> [Div: South, Groups S1–S2].  
**Recheck / Jump** — <Next OP Brief: 2025-11-10T14:00Z> OR <median_queue_time > 30m OR <any heat-illness incident>  
**Recheck Steward (backup)** — OPS Chief (Planning Section Chief)  
**Authority Window** — South Division only; capacity cap 150 ppl/hr; hours 10:00–18:00; resources: 1 RN, 2 volunteers  
**Two-Key / TTL** — Approvals: OPS + PLANS; TTL: this OP only (auto-demob unless renewed)  
**Kill Criteria → Action** — If <median_queue_time > 30m OR water_stockout == true OR safety_incident_class ≥ S2> → **Temporarily close Center C; redirect to B; request Logistics surge; announce via PIO**  
**Evidence Links** — IAP: ICS-202 Obj v3; ICS-204 South Div v2; ICS-205 comms; ICS-206 med plan; Map tile S-12
```

**Seed:** `seed.civic.ics.opcalendar` — *Operational Period recheck calendar note (IAP footer)*

```TEXT
;; seed_id: seed.civic.ics.opcalendar | seed_type: text | language: TEXT
Recheck Calendar — ClipCard items due this OP: 
- Center C capacity trial (South Div) — readout at OP Brief 2025-11-10T14:00Z (OPS steward)
- Mobile clinic shift extension (West Div) — jump if on-scene treatment > 12/hr (PLANS backup)
```

# 5) 1-Minute Audit (Pass/Fail)

* Hazard names **action → failure → where (Div/Group)**.
* **Measurable** demob triggers and a **clear action**.
* **Dated recheck** at OP brief or **jump** condition.
* **Steward named** (backup optional).
* **Authority window** bounded (area/pop/time/resources).
* **Evidence links** present (IAP pages, maps, plans).

# 6) Metrics & Definitions

* **near_miss_rate:** near-miss notes per OP tied to ClipCard actions. *Target:* **↑ detection**.
* **avoidable_reversals:** reversals/diversions judged avoidable in AAR. *Target:* **↓ vs baseline**.
* **recheck_on_time:** % of ClipCards rechecked at scheduled OP brief. *Target:* **≥80%**.

# 7) Objections → Replies

* “We’re already swamped.” → ClipCard is **one box**, **one OP**, only for high-risk steps; it **pre-sets demob triggers** to reduce chaos.
* “We have the IAP already.” → This **binds** IAP objectives to **timed rechecks** and **kill triggers** so adaptation is deliberate.
* “This will get someone blamed.” → Policy: **team outcome**; **steward** runs the recheck ritual—**not** a scapegoat.

# 8) Field Drill (15 minutes)

1. Identify one high-risk action in the next OP (e.g., new site opening, route change).
2. Paste the block into ICS-204 for the relevant Div/Group; fill fields.
3. Put the recheck on the OP brief agenda; share kill triggers with Div/Group.
4. Run the OP; demob/renew per criteria.
5. Log a one-line field note (near-miss, demob event, on-time recheck).

# 9) Notebook Placeholders (for Post-Process)

* **NOTEBOOK_PLACEHOLDER:** `clipcard_ics_sim.ipynb` — Simulate queue dynamics/stockouts vs. authority windows; estimate demob-trigger frequency and avoided incidents.
* **NOTEBOOK_PLACEHOLDER:** `clipcard_field_eval_ics.ipynb` — Ingest IAP/204 logs + ClipCards; compute near_miss_rate, avoidable_reversals, recheck_on_time vs. pre-ClipCard OPs.
* **NOTEBOOK_PLACEHOLDER:** `clipmap_viz_ics.ipynb` — Map hazard→recheck→outcome across Divisions; highlight recurrent failure modes.

# 10) Glossary & Roles (Blame-Safe)

* **Team** owns outcomes; **Steward** (OPS/PLANS) owns the recheck ritual.
* **Two-Key:** OPS + PLANS approvals for high-impact actions.
* **TTL/Demob:** actions auto-demobilize unless renewed **after** recheck.

## Appendix A — Human Template (ClipCard.md, ICS/Civic)

```TEXT
**Hazard**: If <open Center C with reduced staff> then <queueing + heat exposure> [Div: South, Groups S1–S2].
**Recheck / Jump**: Next OP Brief 2025-11-10T14:00Z OR median_queue_time > 30m
**Recheck Steward (backup)**: OPS Chief (Planning Section Chief)
**Authority Window**: South Div only; cap 150 ppl/hr; hours 10:00–18:00
**Two-Key / TTL**: OPS + PLANS; TTL this OP only
**Kill Criteria → Action**:
- If median_queue_time > 30m OR water_stockout == true → Close Center C; redirect to B; request Logistics surge; announce via PIO.
**Evidence Links**: IAP 202/204/205/206; Map S-12 (snapshot)
```

## Appendix B — Machine Template (ClipCard.json exemplar, ICS/Civic)

```json
{
  "id": "ICS-OP-SOUTH-CC-001",
  "linked_item": "ICS-204-South-2025-11-10",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If Cooling Center C opens with reduced staff, queueing and heat exposure may rise in South Division (Groups S1–S2).",
  "recheck": { "due_time": "2025-11-10T14:00:00Z", "jump_trigger": "median_queue_time > 30m OR heat_illness_incident >= 1" },
  "steward": { "primary": "Operations Section Chief", "backup": "Planning Section Chief" },
  "authority_window": { "scope_limit": "South Division; cap 150 ppl/hr; hours 10:00–18:00", "time_limit": "1 OP", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["OPS","PLANS"], "ttl_hours": 12 },
  "kill_criteria": [
    { "condition": "median_queue_time_minutes > 30", "action": "Close Center C; redirect to Center B; Logistics surge; PIO announcement" },
    { "condition": "water_stockout == true", "action": "Temporarily close; resupply; notify OPS" }
  ],
  "evidence_links": [
    { "name": "ICS-202 Objectives v3", "url": "https://example.org/iap-202" },
    { "name": "ICS-204 South v2", "url": "https://example.org/iap-204-south" },
    { "name": "ICS-206 Medical Plan", "url": "https://example.org/iap-206" },
    { "name": "Map S-12", "url": "https://example.org/map-s12" }
  ]
}
```

---



# Insert immediately under "1) Purpose & Trigger"
ClipCard is an engineered defense against local-minima failures in ICS: bounded OP experiments, explicit demob triggers, and dated rechecks at OP brief.  
**Trigger (expanded):** Use when `Impact×Uncertainty ≥ 18` OR `reversibility ≥ 4` OR `coupling ≥ 4` OR any safety/public/irreversible red flag. Include PIO template for public notices on demob.

---



**Privacy:** Redact PHI/PII in evidence. You may include hashes/permits instead of snapshots.
