---
id: TASK-3
title: "Decide license and asset/preset provenance"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - release
  - tooling
dependencies:
  - TASK-2
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Resolve ownership and licensing for repository code, the supplied PLTechnical Vale preset, and any future fonts, logos, example text, or generated artifacts. No project license has been selected.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Identify the copyright holder and select a repository/package license explicitly.
- [ ] #2 Review the supplied Vale preset's redistribution rights; its archive has no license file.
- [ ] #3 Record provenance and license notices for every future non-original asset.
- [ ] #4 Add a LICENSE only after the owner approves the choice; do not infer MIT or another license.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Review the attachment and source references, collect ownership facts, and record a decision. Until then, keep the repository non-releasing and disclose the missing license status.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
ADR-5 keeps licensing unresolved. ADR-4 records the Vale provisioning choice and explicitly gates public redistribution of the rules.
<!-- SECTION:NOTES:END -->
