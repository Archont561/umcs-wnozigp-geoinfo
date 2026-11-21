---
id: TASK-8
title: "Define the validation and test matrix"
status: Done
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
- [x] #1 SPEC-QA v0.2 defines eight check levels, an owner for each, and a matrix covering all 43 requirement IDs. TASK-7's documentation tasks are complete, so the matrix is no longer blocked; the two items still open (Polish-language review, preset licence) are tracked there, not here.
- [x] #2 Recorded in a tested-versus-declared table: linux-64 is tested, the other four declared platforms are not; Tectonic and Typst are tested against the dummy only; XeLaTeX/LuaLaTeX/pdfLaTeX and Biber are absent. QA-008 forbids claiming an untested combination.
- [x] #3 Representative content enumerated against SRC-014..SRC-035. Baselines defined as structural assertions first, normalised text extraction second, human review with a recorded environment line third; byte-comparison of PDFs explicitly rejected (QA-010).
- [x] #4 CI policy states the one approved exception (ADR-8's smoke job) and that multi-engine matrix runs stay opt-in. QA-001 is verified: the `check` task has 11 dependencies and none of them builds.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Map each requirement in SPEC-SCOPE, SPEC-LTX, SPEC-TYP, and SPEC-BIB to a test or manual review. Include Vale's limited role and visual review criteria.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-21: SPEC-QA rewritten to v0.2 with the traceability matrix. Two findings are recorded as failing checks: LTX-003 and TYP-004, because the release archive ships `tests/` and `main.*` with the package (confirmed by simulation), and QA-009 now requires the archive to exclude them. One fix in `release.yml` closes both. Criteria 2-4 met; criterion 1 blocked on TASK-7.
<!-- SECTION:NOTES:END -->
