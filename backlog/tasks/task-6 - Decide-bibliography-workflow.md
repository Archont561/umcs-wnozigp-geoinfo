---
id: TASK-6
title: "Decide bibliography and citation behavior"
status: In Progress
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-21 00:00'
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
- [x] #4 Approach selected: repository-owned styles per format, processor chosen on measured availability. ADR-12 picked `.bbx`/`.cbx` + Biber and was blocked; ADR-16 replaces the LaTeX half with a repository-owned `.bst` run by Tectonic's embedded BibTeX engine, because no `biber` package or `tectonic-biber` binary exists and sandbox egress cannot add one. Typst stays Hayagriva + CSL. No bibliography command has been added to either main.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use source evidence and the approved LaTeX/Typst contracts. Prepare synthetic test references only after the style decision is recorded.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-21: SPEC-BIB rewritten to v0.2 and ADR-12 selects repository-owned styles per format. Still no `.bib` file and no style file.

2026-11-21 (later): the Biber dependency question is answered by measurement, not preference. conda-forge has no `biber` feedstock and no `biber` output in `feedstock-outputs`; `tectonic-biber` has no release asset; sandbox egress reaches neither `conda.anaconda.org` nor `prefix.dev`. ADR-16 adopts BibTeX via Tectonic's embedded engine, which needs no new dependency. Criterion 4 is therefore met, and TASK-11's blocker is removed.
<!-- SECTION:NOTES:END -->
