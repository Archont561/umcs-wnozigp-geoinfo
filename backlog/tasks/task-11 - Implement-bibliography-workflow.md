---
id: TASK-11
title: "Implement approved bibliography workflow"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - latex
  - typst
dependencies:
  - TASK-6
  - TASK-9
  - TASK-10
priority: medium
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement bibliography support only after a citation workflow is selected and its behavior is specified independently for both formats.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Follow the accepted SPEC-BIB decision and accepted source requirements. The processor is fixed by ADR-16: `.bst` through Tectonic's embedded BibTeX for LaTeX, CSL for Typst.
- [ ] #2 Test Polish names/diacritics, sorting, incomplete references, and representative source types.
- [ ] #3 Record external tools, package versions, and editor/engine constraints.
- [ ] #4 Provide no fake or unlicensed example records.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Complete TASK-6 first. Implement separate LaTeX and Typst workflows with fixtures and regression checks; document differences instead of forcing parity.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
No `.bib` database, `.bst`, CSL file or bibliography command has been implemented. The processor question is closed: Biber is not installable here, so ADR-16 selects BibTeX on Tectonic's embedded engine. This task no longer waits on a dependency, only on writing the style files and measuring their output.
<!-- SECTION:NOTES:END -->
