---
id: TASK-4
title: "Specify the LaTeX package contract"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - latex
  - scope
dependencies:
  - TASK-1
  - TASK-2
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define the future LaTeX API, supported engines/editors, dependencies, build instructions, bibliography interaction, and package boundaries before replacing the dummy `main.tex`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Complete SPEC-LTX with approved API and input/output behavior.
- [ ] #2 Decide the engine matrix and test plan; distinguish Tectonic smoke builds from native engine support.
- [ ] #3 State Overleaf/editor compatibility precisely and support it with tests, or make no compatibility claim.
- [ ] #4 Define future fixture/package separation and runtime dependency policy.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use verified requirements from TASK-1 and scope from TASK-2; consult TASK-6 for citation behavior. Record unresolved tradeoffs rather than coding around them.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
SPEC-LTX is drafted. `packages/latex/main.tex` is only a compileable dummy. No class/style API exists.
<!-- SECTION:NOTES:END -->
