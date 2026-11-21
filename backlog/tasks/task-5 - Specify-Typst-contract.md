---
id: TASK-5
title: "Specify the Typst package contract"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - typst
  - scope
dependencies:
  - TASK-1
  - TASK-2
priority: high
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define the future Typst API, minimum compiler version, dependencies, template entry point, editor workflow, and distribution policy before replacing the dummy `main.typ`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Complete SPEC-TYP with approved API and package shape.
- [ ] #2 Distinguish tested compiler version from the future minimum supported version.
- [ ] #3 Review editor/package distribution requirements; do not claim Overleaf support without evidence.
- [ ] #4 Define fixture/package separation, imports, dependency policy, and test plan.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use verified requirements from TASK-1 and scope from TASK-2; coordinate citation behavior with TASK-6. Review registry naming only if the owner later chooses a registry.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
SPEC-TYP is drafted. `packages/typst/main.typ` is a dummy, not a package entrypoint. No registry manifest is present.
<!-- SECTION:NOTES:END -->
