---
id: TASK-6
title: "Decide bibliography and citation behavior"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - latex
  - typst
dependencies:
  - TASK-1
  - TASK-4
  - TASK-5
priority: medium
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Compare citation and bibliography options for both formats. Topics such as BibLaTeX/Biber are investigation inputs, not an existing decision or implemented workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Verify whether current faculty guidance prescribes a citation or bibliography style.
- [ ] #2 Compare supported LaTeX tools/engines and Typst-native or package options.
- [ ] #3 Record sorting, language, diacritics, web sources, and missing-field behavior in SPEC-BIB.
- [ ] #4 Approve an approach before adding bibliography commands or dependencies to either main.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use source evidence and the approved LaTeX/Typst contracts. Prepare synthetic test references only after the style decision is recorded.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
SPEC-BIB lists candidate options without selecting one. No `.bib` file or Biber task is configured yet.
<!-- SECTION:NOTES:END -->
