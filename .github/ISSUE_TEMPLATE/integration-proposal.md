name: Integration Proposal (Seed)
description: Propose a new ClipCard integration (CI/Jira/EHR/ICS/etc.)
title: "Integration: <tool> — <domain>"
labels: ["integration","help-wanted"]
body:
  - type: input
    id: tool
    attributes:
      label: Tool / Platform
      placeholder: "GitHub Actions, GitLab, Jira, Epic, ICS form, etc."
  - type: textarea
    id: summary
    attributes:
      label: Summary
      placeholder: "What the integration does and how to use it"
  - type: textarea
    id: snippet
    attributes:
      label: Snippet (code/config)
      placeholder: "Paste YAML/JSON/TEXT with seed header lines"

---

