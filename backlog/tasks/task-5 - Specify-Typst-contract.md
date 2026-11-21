---
id: TASK-5
title: "Specify the Typst package contract"
status: In Progress
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - typst
  - scope
dependencies:
  - TASK-1
  - TASK-2
priority: high
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define the future Typst API, minimum compiler version, dependencies, template entry point, editor workflow, and distribution policy before replacing the dummy `main.typ`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 SPEC-TYP v0.2 defines the package shape (`lib.typ`, one `umcs-thesis` entry point, configuration dictionary) and the function surface with source citations. **Not approved**: no package exists, Annexes 1-5 are unobtained, and no owner sign-off is recorded.
- [x] #2 Recorded separately: 0.15.1 is what this repository tests (pinned in pixi.toml); the future minimum is explicitly undecided because the package's feature use is unknown.
- [x] #3 No editor claim is made. No registry submission is configured and no `typst.toml` exists (ADR-12); the local-package path is the assumed development workflow and is marked untested.
- [x] #4 SPEC-TYP defines the path table (lib.typ vs main.typ vs tests), offline-only imports (TYP-002), a licence record per dependency (TYP-003), and a test plan using `typst query` for counter and source assertions. It also records that the release archive does not yet enforce the separation.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use verified requirements from TASK-1 and scope from TASK-2; coordinate citation behavior with TASK-6. Review registry naming only if the owner later chooses a registry.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-21: SPEC-TYP rewritten to v0.2 against the verified evidence. Verified in the restored sandbox that Typst 0.15.1 compiles the dummy, that Hayagriva YAML works, and that no Times New Roman font is available (31 bundled fonts, none metric-compatible). `packages/typst/main.typ` is still a dummy and no package exists. Criteria 2-4 met; criterion 1 awaits approval.
<!-- SECTION:NOTES:END -->
