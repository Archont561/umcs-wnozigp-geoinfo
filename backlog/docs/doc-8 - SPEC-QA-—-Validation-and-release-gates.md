---
id: doc-8
title: SPEC-QA — Validation and release gates
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:43'
---

## SPEC-QA — Validation and release gates

**Status:** Draft  
**Version:** 0.1  
**Related decisions:** ADR-1, ADR-3, ADR-5  
**Related tasks:** TASK-8–TASK-13  
**Milestone:** M-3, M-4

## Validation layers

1. **Static checks:** TOML formatting, rumdl Markdown lint, Vale, and source linters.
2. **Smoke builds:** Tectonic compiles `packages/latex/main.tex`; Typst compiles `packages/typst/main.typ`. Outputs go to ignored `dist/` paths.
3. **Behavior tests:** pytest-bdd tests under `packages/latex/tests/` and `packages/typst/tests/` run each package's Tasknest build and check its dummy PDF framing. These are build-pipeline tests, not template tests.
4. **Package tests:** Future tests shall verify each package API, dependencies, generated file structure, and import/install route after those contracts are approved.
5. **Visual/academic review:** Future rendered output must be reviewed against the accepted evidence matrix, including page geometry, pagination, typography, bilingual text, and representative edge cases.

## Requirements

- **QA-001:** Root `check` shall not silently run expensive manual builds.
- **QA-002:** A passing smoke build shall be reported only as compilation success.
- **QA-003:** Future visual tests shall record engine/compiler version, platform, fonts, and reference source.
- **QA-004:** No generated PDF, student document, or private data is a release artifact by default.
- **QA-005:** `.github/workflows/release.yml` shall attach only separate source archives for the LaTeX and Typst package directories when a `v*` tag is pushed; it shall run repository checks and package smoke tests before publication.

## Release decision gates

No CTAN or Typst registry submission is selected or approved. A GitHub tag-release workflow is configured at the user's request to publish source-only archives from `packages/latex/` and `packages/typst/`. A matching tag push is a publication action; the workflow configuration does not imply license clearance, UMCS approval, or package readiness. The current mains remain smoke placeholders. Resolve before pushing a release tag:

- third-party rule/font/logo provenance and any per-package license deviation from the repository MIT grant (ADR-7);
- supported artifact contents and whether the repository's package directories are appropriate for public distribution;
- student-facing and institutional review, plus independent human approval;
- a clean build, reproducible artifact inventory, checksums, and rollback/withdrawal procedure.

This draft does not establish institutional endorsement or full compliance.
