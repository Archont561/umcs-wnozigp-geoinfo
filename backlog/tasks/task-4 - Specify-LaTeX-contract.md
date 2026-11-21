---
id: TASK-4
title: "Specify the LaTeX package contract"
status: In Progress
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-09 00:00'
labels:
  - latex
  - scope
dependencies:
  - TASK-1
  - TASK-2
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define the future LaTeX API, supported engines/editors, dependencies, build instructions, bibliography interaction, and package boundaries before replacing the dummy `main.tex`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 SPEC-LTX v0.2 defines the API (options, `\umcssetup` keys, structure commands, floats, equations) with source citations per element. **Not approved**: the API is proposed, Annexes 1-5 are unobtained, and the owner has not signed it off.
- [x] #2 Engine matrix recorded: Tectonic is smoke-only evidence (ADR-8), XeLaTeX/LuaLaTeX/pdfLaTeX are candidates with their Times-font constraints stated, and no engine is claimed as supported. The test plan is defined in SPEC-LTX and owned by TASK-8.
- [x] #3 No editor compatibility claim is made, per ADR-11. SPEC-LTX records the conditions a future Overleaf test must satisfy before any claim.
- [x] #4 SPEC-LTX defines the path table separating `umcswnozigp.cls` from fixtures and tests, plus a five-point dependency policy with an anticipated dependency table. It also records that the release archive does not yet enforce the separation.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Use verified requirements from TASK-1 and scope from TASK-2; consult TASK-6 for citation behavior. Record unresolved tradeoffs rather than coding around them.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-11-21: SPEC-LTX rewritten to v0.2 against the verified SRC-001..SRC-044 evidence, with ADR-11 choosing a document class and declining engine/editor claims. `packages/latex/main.tex` is still only a compileable dummy and no class exists. Criteria 2-4 met; criterion 1 awaits approval and the normative annexes.
<!-- SECTION:NOTES:END -->
