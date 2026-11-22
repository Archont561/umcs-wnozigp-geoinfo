---
id: TASK-7
title: "Review Vale preset and editorial policy"
status: In Progress
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - tooling
  - scope
dependencies:
  - TASK-3
priority: medium
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Review the supplied PLTechnical Vale preset, its rule scope, sample behavior, and reuse rights. Vale is installed from Conda through root Pixi; the style files are local.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Rules and thresholds are documented and measured (SPEC-EDIT v0.2, ADR-13), but **no Polish-language reviewer has confirmed them**. Owner review under ADR-9 covers the repository, not Polish linguistic judgement, so this stays open.
- [x] #2 `examples/vale/rule-cases.md` adds all four with stated expected counts, plus a clean control. Verified: 14 findings, and the fixture's own first draft was corrected against the run when it disagreed.
- [x] #3 Closed 2026-11-22. Provenance documented in SPEC-EDIT and ADR-4: the preset is written by the repository
  owner from the gov.pl plain-language guidance, its only source, which states no licence and needs none. The five
  rule files are MIT with the repository, and the author confirmed the authorship that makes that so (V-1).
- [x] #4 SPEC-EDIT documents four override methods, names the one that is repository-wide, and ADR-13 requires an ADR for any threshold change.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Run the local Vale binary against a reviewed Polish sample, inspect JSON findings, and update SPEC-EDIT and ADR-4 with the accepted policy.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-21: measured all five rules against the fixtures. Found that UnitSpacing flags `20°C` even though its message calls `°` an exception, and that headings are scanned as sentences (so each phrase yields two findings). Both recorded. Criteria 2, 3 and 4 met; 1 still needs a Polish-language reviewer. 2026-11-22: criterion 3 closed once the author confirmed writing the rules from gov.pl guidance, its only source; a dead VerbPhrases pattern was found and fixed while re-measuring the rules against the provenance. Criterion 1 (a Polish-language reviewer) remains the only open one.
<!-- SECTION:NOTES:END -->
