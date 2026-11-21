---
id: TASK-8
title: "Define the validation and test matrix"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - tooling
  - latex
  - typst
dependencies:
  - TASK-4
  - TASK-5
  - TASK-6
  - TASK-7
priority: high
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define which checks are static, unit, BDD, compile, visual, or human review. Keep the dummy-main smoke scenario distinct from future template validation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Complete SPEC-QA with named check levels and owners.
- [ ] #2 Record supported platforms/engines/compilers and distinguish tested from planned.
- [ ] #3 Define representative content, rendering baselines, and regression evidence.
- [ ] #4 Keep expensive builds and smoke tests opt-in unless explicitly approved for CI.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Map each requirement in SPEC-SCOPE, SPEC-LTX, SPEC-TYP, and SPEC-BIB to a test or manual review. Include Vale's limited role and visual review criteria.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
A pytest-bdd smoke scenario exists for the two dummy PDFs. It proves only the build pipeline; the complete matrix remains open.
<!-- SECTION:NOTES:END -->
