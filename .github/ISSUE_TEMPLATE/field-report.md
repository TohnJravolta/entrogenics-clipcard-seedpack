name: Field Report (ClipCard)
description: Share anonymized results from a real trial of ClipCard.
title: "Field Report: <domain> — <artifact/ref>"
labels: ["field-report"]
body:
  - type: input
    id: domain
    attributes:
      label: Domain
      placeholder: "DevOps/SRE | Clinical | Policy/T&S | Industrial/Aviation | Civic/ICS | AI/ML"
  - type: input
    id: artifact
    attributes:
      label: Artifact / Reference
      placeholder: "Ticket/ADR/SBAR/Memo/MOC/ICS/Release etc."
  - type: textarea
    id: clipcard
    attributes:
      label: ClipCard snapshot (redact sensitive)
      description: Paste the human template and/or JSON (with redactions).
  - type: checkboxes
    id: metrics
    attributes:
      label: Outcomes observed
      options:
        - label: Recheck completed on time
        - label: Near-miss captured
        - label: Rollback/kill triggered
        - label: No effect observed
  - type: textarea
    id: notes
    attributes:
      label: Notes & lessons
      placeholder: "What worked, what didn’t, what you'd change"

---



# Add this checkbox to the "Outcomes observed" section (keep existing options)
- label: Framed outcome via Executive Counter-Incentive (Containment / Due Diligence / Reliable Sensing)

---


