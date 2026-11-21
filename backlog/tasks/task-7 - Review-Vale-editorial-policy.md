---
id: TASK-7
title: "Review Vale preset and editorial policy"
status: To Do
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
- [ ] #1 Confirm the enabled rules and severity threshold with Polish-language reviewers.
- [ ] #2 Add positive/negative examples for suggestions, unit spacing, code spans, and URLs.
- [ ] #3 Confirm license/provenance before public redistribution; the supplied archive has no license file.
- [ ] #4 Document how maintainers override alerts without weakening the project-wide checks silently.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Run the local Vale binary against a reviewed Polish sample, inspect JSON findings, and update SPEC-EDIT and ADR-4 with the accepted policy.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Vale `3.26.0` is pinned from Conda in `pixi.toml`. The user-provided `.vale.ini` and five `PLTechnical` rules are installed locally; the root task uses a warning threshold. Review remains open.
<!-- SECTION:NOTES:END -->
