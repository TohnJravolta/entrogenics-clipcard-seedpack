Advanced context fields (`telos`, `cycle_phase`, `risk_factors`) are **optional** (see `schema/clipcard.schema.v1e.json`).

> **ClipCard in one sentence:** an **engineering control surface** against the physics of organizational failure, not a checklist.  
It adds a tiny, blame-safe ritual **only when risk is high**: Authority Window, Two-Key + TTL, Kill Criteria, Dated Recheck, and Evidence snapshots. The result is **contained liability, reliable sensing, and higher long-term velocity**.  
See the formal narrative: `docs/ClipCard_Framework_Packet.md` (executive framing) and `docs/executive-brief.md` (1-pager).

---

# Entrogenics Seed Pack — ClipCard (Risk & Recheck)
A tiny, blame-safe ritual for high-risk decisions that clips onto existing ops artifacts.  
This repo contains **6 Domain Field Manuals (DFMs)** and copy-paste **Seeds** so teams can try ClipCard in 60–90 seconds—no new tools, no consulting, no DMs.

## What is ClipCard?
When a decision is **big** and **iffy**, add one page with:
- **Hazard** (specific failure mode)
- **Recheck** (dated or jump condition) + **Steward** (reminder owner)
- **Authority Window** (limited scope/time)
- **Two-Key / TTL** (dual approval or time-boxed)
- **Kill Criteria** (observable thresholds → action)
- **Evidence Links** (stable/snapshotted)

**Trigger:** only when `Impact(1–5) × Uncertainty(1–5) ≥ 18` or **red-flag** (safety/legal/public/irreversible).

## Try it in 4 steps
1) Pick your domain (see `dfm/`).  
2) Copy the **Seed** into your existing artifact (ticket, SBAR, memo, ICS, model card, etc.).  
3) Put the **Recheck** on a shared calendar; wire one **Kill** trigger to an alert/telemetry.  
4) After the recheck/trigger, open a **Field Report** issue (template included).

## Domains
- `dfm/dfm-devops-sre.md` — Change tickets, ADRs, incident PRs  
- `dfm/dfm-clinical-sbar.md` — SBAR handoffs, high-alert meds, procedure deviations  
- `dfm/dfm-policy-ts.md` — Policy changes, T&S launches, enforcement pilots  
- `dfm/dfm-industrial-aviation.md` — MOC deviations, overrides, flight ops waivers  
- `dfm/dfm-civic-ics.md` — ICS objectives/assignments, OP brief rechecks  
- `dfm/dfm-aiml-governance.md` — Model releases, eval boards, safety sign-off

## Metrics (pick ≤3)
- **On-time Rechecks** (target ≥80%)
- **Near-Miss Capture** (should ↑)
- **False Approvals / Reversions / Incidents** (should ↓)
- Domain-specific extras inside each DFM

## Blame-safe policy
Team owns outcomes. **Steward** owns the calendar ping/ceremony (not a scapegoat).

## Contribute
- Open a **Field Report** (template in `.github/ISSUE_TEMPLATE/`).  
- PR new **Seeds / integrations** (CI, Jira, EHR, ICS forms, etc.).  
- Add examples in `examples/`.

## License
Docs & templates: **CC-BY-SA-4.0**  
Snippets & code: **MIT**

---


## Notebooks
See [docs/notebook-index.md](docs/notebook-index.md) for domain notebooks (sim/eval/agent/viz).
