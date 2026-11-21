---
id: TASK-13
title: "Approve release destinations and human gates"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - release
dependencies:
  - TASK-3
  - TASK-12
priority: high
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Determine whether either format should be distributed publicly and define the required ownership, licensing, artifact, and approval controls. No release route or publisher is currently selected.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Select or explicitly reject each destination and verify account ownership.
- [ ] #2 Approve licenses and source/asset provenance for every included file.
- [ ] #3 Define version/tag policy, artifact inventory, immutable checksums, and rollback process.
- [ ] #4 Define independent institutional/maintainer approval before publication.
- [ ] #5 Keep credentials, write permissions, and publisher disabled until all gates pass.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Review SPEC-QA and ADR-5 after implementation and provenance work. Record a new ADR only when the owner explicitly approves destinations and release controls.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
GitHub source repository exists, but no package release channel, license, registry, CTAN destination, or human release approval has been selected. No publisher is configured.
<!-- SECTION:NOTES:END -->
