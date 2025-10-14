---

dfm_id: "industrial-aviation"
title: "DFM: Industrial / Aviation / Safety Management — ClipCard (Risk & Recheck)"
version: "1.0"
domain: "Industrial Operations, Process Safety, Aviation SMS/MOC"
trigger_rule: "Use ClipCard when Impact(1–5) × Uncertainty(1–5) ≥ 18 OR any safety/legal/public/irreversible red flag (e.g., temporary procedure deviations, maintenance overrides, flight ops waivers)."
jargon_bridge:

* { clipcard_term: "Hazard", domain_term: "Hazard / FMEA mode", notes: "If deviation X, then failure Y at node Z." }
* { clipcard_term: "Recheck Steward", domain_term: "Shift Lead / Safety Engineer", notes: "Owns the recheck reminder; team owns outcome." }
* { clipcard_term: "Authority Window", domain_term: "Time-boxed deviation (MOC)", notes: "Where/when/how the deviation is contained." }
* { clipcard_term: "Two-Key / TTL", domain_term: "Independent verification / demob time", notes: "Second checker and automatic end of deviation." }
* { clipcard_term: "Kill Criteria", domain_term: "Alarm thresholds / stop rules", notes: "Observable limits that force immediate safe action." }
  metrics:
* { name: "deviation_incidents", definition: "Incidents during temporary deviations (per 1k operating hours or flight cycles)", target: "Decrease vs. baseline", method: "rate with 95% CI" }
* { name: "closeout_on_time", definition: "Share of MOC deviations closed by planned demobilization time", target: "≥85%", method: "binary on-time flag → weekly/monthly proportion" }
* { name: "near_miss_rate", definition: "Near-miss events recorded per 1k hours/cycles during deviations", target: "Increase vs. baseline (better detection)", method: "rate with trend" }
  seeds:
* { seed_id: "seed.industrial.micro_moc.insert", seed_type: "text", language: "TEXT", summary: "Micro-MOC ClipCard insert for temporary deviations (copy into MOC form/waiver)" }
* { seed_id: "seed.industrial.alarm.binding", seed_type: "yaml", language: "YAML", summary: "Generic alarm binding: kill-criteria → alerts/actions (adapt to DCS/SCADA/SMS)" }
  license: "Docs/Templates: CC-BY-SA-4.0; Snippets/Code: MIT"
  contacts: []

---

# 1) Purpose & Trigger

**Trigger Rubrics (optional, 1–5):**
- **Reversibility:** 1 = trivial undo (toggle, no loss); 3 = rollback with brief impact/manual cleanup; 5 = irrecoverable or public/legal/clinical harm if wrong.
- **Coupling:** 1 = isolated component/unit; 3 = affects 1–2 dependent systems/wards; 5 = tightly coupled, cascades likely across systems/regions.
*Guidance:* You may trigger ClipCard if either score ≥ 4, even when `Impact×Uncertainty < 18`. Use sparingly to avoid fatigue.


Temporary deviations (maintenance overrides, procedure waivers, off-nominal ops) concentrate risk. **ClipCard** is a one-page add-on used **only** when a deviation is **high-impact** and **uncertain**. It forces: **hazard** (FMEA mode), **dated recheck or jump**, **steward** (shift lead/safety), **authority window** (bounded where/when/how), **two-key/TTL** (independent verify; auto demob), **kill criteria** (alarm redlines → safe action), and **evidence links** (P&IDs, MEL/CDL, safety case).

**Trigger:** `Impact × Uncertainty ≥ 18` **or** red flag (personnel safety, environmental release, airworthiness, regulatory/public risk).

# 2) Jargon Bridge

| ClipCard term    | Industrial/Aviation term              | Notes                                           |
| ---------------- | ------------------------------------- | ----------------------------------------------- |
| Hazard           | Hazard / FMEA mode                    | “If bypass PSV-203, then overpressure at V-12.” |
| Recheck Steward  | Shift Lead / Safety Engineer          | Owns reminder & roll-call; not a scapegoat.     |
| Authority Window | Time-boxed deviation (MOC)            | Unit/line/airframe + duration + scope.          |
| Two-Key / TTL    | Independent verification / Demob time | Separate engineer/inspector; auto close.        |
| Kill Criteria    | Alarm thresholds / stop rules         | e.g., P≥8.5 bar, T≥220°C, vibration>RMSx.       |
| Evidence Links   | P&ID/MEL/Risk register                | Stable drawings, hazard logs, safety case.      |

# 3) Placement Patterns (Where it Clips On)

* **MOC / Deviation form:** paste Micro-MOC insert; attach machine JSON; set demob date/time.
* **Permit-to-Work / LOTO:** reference ClipCard kill criteria and authority window on the permit.
* **Flight Ops Waiver / MEL dispatch:** include ClipCard; set TTL to next maintenance window; two-key = Captain + Maintenance Control.

# 4) Seeds (Copy-Paste)

**Seed:** `seed.industrial.micro_moc.insert` — *Micro-MOC ClipCard block (text for forms/waivers)*

```TEXT
;; seed_id: seed.industrial.micro_moc.insert | seed_type: text | language: TEXT
### Micro-MOC ClipCard — Risk & Recheck
**Hazard** — If <bypass PSV-203> then <overpressure> [node: V-12, train A].  
**Recheck / Jump** — <2025-11-10T14:00Z> OR <PI-V12 > 8.3 bar for 2 min>  
**Recheck Steward (backup)** — <Shift Lead> (<Safety Eng>)  
**Authority Window** — <Train A only>, <max 12h>, <rate limited 60%>, boundary valves <closed>  
**Two-Key / TTL** — IV by <Process Eng B>; TTL <12h> (auto demob if not renewed)  
**Kill Criteria → Action** — If <PI-V12 ≥ 8.5 bar OR TI-V12 ≥ 220°C OR vib_RMS > threshold> → **Trip feed pump P-3; open vent per SOP-V12; notify CCR; start controlled shutdown**  
**Evidence Links** — <P&ID-V12-revK>, <HAZOP-node-V12-2024>, <Relief study-PSV-203>, <SOP-V12-shutdown>
```

**Seed:** `seed.industrial.alarm.binding` — *Generic alarm binding (adapt to DCS/SCADA/SMS)*

```YAML
# seed_id: seed.industrial.alarm.binding
# seed_type: yaml
# language: YAML
clipcard_id: MOC-DEV-PSV203-A12
bindings:
  - tag: PI-V12
    threshold: { op: ">=", value: 8.5, unit: "bar", dwell_sec: 30 }
    action:
      - type: "command"
        target: "FEED_PUMP_P3"
        cmd: "TRIP"
      - type: "procedure"
        doc: "SOP-V12-shutdown"
        step: "Open vent; begin controlled shutdown"
      - type: "notify"
        channels: ["CCR","ShiftLead","SafetyEng"]
        message: "Kill criteria met (PI-V12 ≥ 8.5 bar, 30s). Execute shutdown."
  - tag: TI-V12
    threshold: { op: ">=", value: 220, unit: "C", dwell_sec: 60 }
    action:
      - type: "notify"
        channels: ["CCR","ShiftLead"]
        message: "Temperature high at V-12; prepare trip per ClipCard."
  - tag: VIB-P3
    threshold: { op: ">", value: 12.0, unit: "mm/s RMS", dwell_sec: 20 }
    action:
      - type: "command"
        target: "FEED_PUMP_P3"
        cmd: "TRIP"
meta:
  authority_window:
    scope: "Train A only"
    time_limit: "12h"
    auto_demob: true
  two_key:
    required: true
    approvers: ["ProcessEngB","ShiftLead"]
  audit:
    evidence: ["P&ID-V12-revK","HAZOP-node-V12-2024","Relief-Study-PSV203"]
```

# 5) 1-Minute Audit (Pass/Fail)

* Hazard is **specific** (deviation → failure → node/asset).
* **Measurable** kill criteria and **explicit safe action**.
* **Dated recheck** or clear **jump** (alarm).
* **Steward named** (backup optional).
* **Authority window** bounded (unit/airframe/time).
* **Evidence links** present (stable/snapshotted).

# 6) Metrics & Definitions

* **deviation_incidents:** incidents during active deviations per 1k hours/cycles. *Target:* **↓ vs baseline**.
* **closeout_on_time:** % deviations closed by planned demob/TTL. *Target:* **≥85%**.
* **near_miss_rate:** near-misses logged per 1k hours/cycles during deviations. *Target:* **↑ detection**.

# 7) Objections → Replies

* “We already have MOC.” → ClipCard is the **lightweight insert inside MOC**: adds **dated recheck**, **auto demob (TTL)**, and **pre-agreed kill actions**.
* “Too many alarms already.” → Use **dwell times** and **authority windows** to reduce noise; ClipCard binds alarms to **specific safe actions**.
* “This will slow operations.” → Only for high-risk deviations; **time-boxed** by default; lowers incident probability and impact.

# 8) Field Drill (15 minutes)

1. Select one **active deviation** or a planned **temporary override**.
2. Paste Micro-MOC block into the MOC; fill hazards, TTL, kill criteria, evidence.
3. Bind **one** kill criterion to an alert/procedure; brief crew on action.
4. Put recheck on the control room calendar (roll-call).
5. After TTL, record on-time closeout and any near-miss/trigger event; post anonymized field note.

# 9) Notebook Placeholders (for Post-Process)

* **NOTEBOOK_PLACEHOLDER:** `clipcard_industrial_sim.ipynb` — Simulate deviation duration × authority window × kill-criterion dwell; estimate expected reduction in incident probability and consequence.
* **NOTEBOOK_PLACEHOLDER:** `clipcard_field_eval_industrial.ipynb` — Ingest deviation/MOC logs + ClipCards; compute deviation_incidents, closeout_on_time, near_miss_rate vs. pre-period with CIs.
* **NOTEBOOK_PLACEHOLDER:** `clipmap_viz_industrial.ipynb` — Hazard→recheck→outcome graph by unit/airframe; surfaces recurrent failure modes.

# 10) Glossary & Roles (Blame-Safe)

* **Team** owns outcomes; **Steward** (Shift Lead/Safety) owns the calendar/roll-call.
* **Two-Key**: Independent verification by a separate engineer/inspector.
* **TTL/Demob**: Deviation auto-ends unless renewed **after** recheck.

## Appendix A — Human Template (ClipCard.md, Industrial/Aviation)

```TEXT
**Hazard**: If <MEL item APU bleed valve INOP> then <packs overheat risk> [tail: N123AB].
**Recheck / Jump**: 2025-11-10T18:00Z OR EICAS: DUCT TEMP HIGH (2× in 10 min)
**Recheck Steward (backup)**: Maintenance Control (Captain)
**Authority Window**: Route KJFK→KBOS only; max 2 legs; MEL constraints applied
**Two-Key / TTL**: Captain + Maint Control; TTL end of day (local)
**Kill Criteria → Action**:
- If DUCT TEMP HIGH repeats 2×/10 min → Return to gate/divert; execute QRH; notify MCC
**Evidence Links**: MEL ref APU-BLD-01; QRH page 5-23; Dispatch release; Logbook snapshot
```

## Appendix B — Machine Template (ClipCard.json exemplar, Industrial/Aviation)

```json
{
  "id": "MOC-DEV-PSV203-A12",
  "linked_item": "MOC-2025-11-09-TrainA",
  "impact": 5,
  "uncertainty": 4,
  "hazard": "If PSV-203 is bypassed, overpressure may occur at vessel V-12 (Train A).",
  "recheck": { "due_time": "2025-11-10T14:00:00Z", "jump_trigger": "PI-V12 >= 8.3 bar for 120s" },
  "steward": { "primary": "Shift Lead", "backup": "Safety Engineer" },
  "authority_window": { "scope_limit": "Train A only; rate limited to 60%", "time_limit": "12h", "auto_pause": true },
  "two_key_ttl": { "required": true, "approvers": ["ProcessEngB","ShiftLead"], "ttl_hours": 12 },
  "kill_criteria": [
    { "condition": "PI-V12 >= 8.5 bar for 30s", "action": "Trip FEED_PUMP_P3; open vent per SOP-V12; notify CCR; start controlled shutdown" },
    { "condition": "TI-V12 >= 220 C for 60s", "action": "Notify CCR; prepare shutdown per SOP" }
  ],
  "evidence_links": [
    { "name": "P&ID-V12-revK", "url": "https://example.org/pid-v12-revk" },
    { "name": "HAZOP-node-V12-2024", "url": "https://example.org/hazop-v12-2024" },
    { "name": "Relief Study PSV-203", "url": "https://example.org/relief-psv203" },
    { "name": "SOP-V12-shutdown", "url": "https://example.org/sop-v12" }
  ]
}
```

---



# Insert immediately under "1) Purpose & Trigger"
ClipCard is an engineered defense against local-minima failures in MOC/SMS: bounded deviation, dual control, and wired kill criteria with dwell.  
**Trigger (expanded):** Use when `Impact×Uncertainty ≥ 18` OR `reversibility ≥ 4` OR `coupling ≥ 4` OR any safety/legal/public/irreversible red flag. Require evidence snapshots and alarm dwell defaults.

---



**Privacy:** Redact PHI/PII in evidence. You may include hashes/permits instead of snapshots.
