---
id: TASK-3
title: "Decide license and asset/preset provenance"
status: To Do
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - release
  - tooling
dependencies:
  - TASK-2
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Resolve ownership and licensing for repository code, the supplied PLTechnical Vale preset, and any future fonts, logos, example text, or generated artifacts. The repository's own work is now MIT-licensed (ADR-7); third-party preset reuse is still unreviewed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Identify the copyright holder and select a repository/package license explicitly. MIT for the repository (ADR-7) and for each package (ADR-14), holder Archont561.
- [x] #2 Reviewed and confirmed: the author states the rules were written by them from the gov.pl plain-language
  guidance, its only source (SPEC-EDIT). That guidance states no licence and needs none — the rules take advice,
  not text — so the five files are MIT with the repository. Self-asserted authorship, recorded as V-1's answer
  (ADR-4); the single-person limitation is ADR-9's.
- [ ] #3 Record provenance and license notices for every future non-original asset.
- [x] #4 Add a LICENSE only after the owner approves the choice; do not infer MIT or another license. Added after explicit owner instruction.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Review the attachment and source references, collect ownership facts, and record a decision. Until then, keep the repository non-releasing and disclose the missing license status.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Criterion 2 closed on 2026-11-22: the author states the rules were written by
them from the gov.pl guidance, the preset's only source. V-1 in
[REVIEWERS](../docs/doc-9%20-%20REVIEWERS-%E2%80%94-Open-reviewer-questions.md)
is answered and retired. Criterion 3 is the remaining open one and it is a
question to a party outside this repository: **U-1** (may the UMCS logotype be
redistributed). It no longer blocks a release, because ADR-19 removed the bundled
mark.

ADR-14 mirrors MIT into each package so standalone tarballs carry terms. ADR-7 selects MIT for original repository code and documentation, superseding ADR-5's licensing point. ADR-4 records the Vale provisioning choice. Its gate on redistributing the supplied rules is lifted: with the gov.pl pages as the preset's only source and no text taken from them, MIT covers the five rule files (V-1, answered 2026-11-22).
<!-- SECTION:NOTES:END -->
