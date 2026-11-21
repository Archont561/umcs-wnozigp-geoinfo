---
id: TASK-6
title: "Decide bibliography and citation behavior"
status: In Progress
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
- [x] #1 Verified: the faculty prescribes no named standard but fixes both the entry syntax and the in-text forms (SRC-027..SRC-036). Recorded with the canonical examples and the details that rule out stock author-year styles.
- [x] #2 Compared on measured facts: biber and bibtex are absent from the environment, Tectonic embeds `tectonic-biber` support but the binary is missing, Typst 0.15.1 compiles Hayagriva YAML, and a custom CSL file loads from disk and alters output. The Biber dependency gap is recorded as the blocker.
- [x] #3 SPEC-BIB records all five: Polish collation, Polish labels with a Polish abstract for foreign-language theses, diacritic preservation, separate *netografia* with access dates and five-element in-text URLs, and omission rather than invented placeholders.
- [ ] #4 Approach selected in ADR-12 (repository-owned .bbx/.cbx and CSL), but **not approvable yet**: the chosen LaTeX path needs Biber, which the environment lacks. No bibliography command or dependency has been added to either main.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use source evidence and the approved LaTeX/Typst contracts. Prepare synthetic test references only after the style decision is recorded.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-21: SPEC-BIB rewritten to v0.2 and ADR-12 selects repository-owned styles per format. Still no `.bib` file, no style file, and no Biber task. Criterion 4 stays open pending the Biber dependency decision.
<!-- SECTION:NOTES:END -->
