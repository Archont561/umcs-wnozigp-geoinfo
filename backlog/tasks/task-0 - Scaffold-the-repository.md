---
id: TASK-0
title: "Scaffold specification-first repository"
status: Done
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - scope
  - tooling
dependencies: []
priority: high
ordinal: 0
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the initial local repository structure requested by the owner: compileable dummy mains, specification documents, Backlog.md milestones/tasks/decisions, root Pixi/Tasknest tooling, and the supplied Vale preset. Do not implement a user-facing thesis template or publish changes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create independent LaTeX and Typst dummy main files and smoke-build tasks.
- [x] #2 Add draft specifications, decisions, milestone pages, and linked backlog tasks.
- [x] #3 Provision Vale from the root Conda/Pixi environment and include the supplied local PLTechnical rules.
- [x] #4 Keep release, license, and institutional-compliance claims unresolved and explicit.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Clone the requested GitHub repository locally, preserve its existing history, add the scaffold, validate static checks and dummy builds, and leave changes uncommitted/unpushed for owner review.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Scaffold created in the local clone at `/home/user/umcs-wnozigp-geoinfo`. No commit or push was made. `main.tex` and `main.typ` are smoke fixtures, not templates. See ADR-1 through ADR-6 and SPEC-SCOPE through SPEC-QA.
<!-- SECTION:NOTES:END -->
