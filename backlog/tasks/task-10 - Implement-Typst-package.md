---
id: TASK-10
title: "Implement Typst package after specification approval"
status: In Progress
assignee: []
created_date: '2026-11-09 00:00'
updated_date: '2026-11-21 00:00'
labels:
  - typst
dependencies:
  - TASK-1
  - TASK-2
  - TASK-5
  - TASK-8
priority: medium
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace or extend the dummy Typst main only after its public contract, source requirements, compiler policy, and acceptance criteria are approved.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The implementation traces to accepted SPEC-SOURCE and SPEC-TYP requirements. `lib.typ` cites `SRC-001`–`SRC-026` at the point each rule is implemented, and the public API table in SPEC-TYP matches the exported functions one-for-one.
- [x] #2 Compiler minimum, imported packages, and user instructions are documented and tested. `typst.toml` declares `compiler = "0.15.1"`, which is the version actually run (TYP-005). No third-party package is imported, so TYP-003 is satisfied trivially. `packages/typst/README.md` documents the API, the limitations and the local `--package-path` workflow.
- [x] #3 Fixtures and maintainer-only outputs are excluded from any package offer. The release tarball was built locally and inspected: it contains `lib.typ`, `typst.toml`, `README.md` and `LICENSE` only. `release.yml` now asserts the presence of `lib.typ` and `typst.toml`, not just the absence of fixtures.
- [ ] #4 Human review confirms rendered output; smoke compilation alone is insufficient. **Still open, and not mine to close**: the pages were rendered and inspected by the agent that wrote the code, which is not independent review. The faculty question that stands behind it is **F-1** in [REVIEWERS](../docs/doc-9%20-%20REVIEWERS-%E2%80%94-Open-reviewer-questions.md).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Wait for M-0, M-1, and M-2 decisions; implement in small increments with source tests and a reviewable visual fixture. Do not add a registry manifest until the owner approves a destination and package name.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
No reusable Typst package exists. `packages/typst/main.typ` was a dummy smoke fixture.

2026-11-21: `packages/typst/lib.typ` now implements the SPEC-TYP contract: the `umcs-thesis` show rule, `coverpage`, `contents`, `abstract` with the 4000-character limit enforced at compile time, the three illustration wrappers with mandatory sources, the per-type indexes, `appendix`/`appendices`/`list-of-annexes`, `equation-numbered`, and `front-matter-heading`. Nine BDD scenarios read the document's own metadata via `typst query`, so SRC-021 (three independent counters), SRC-022 (every illustration has a source) and SRC-013 (front matter does not consume a chapter number) are assertions rather than checkboxes.

Three defects were found by rendering rather than by compiling, which is why criterion 4 matters: captions printed literal brackets, the appendix body was silently dropped (a code-mode block returns only its last expression), and front matter consumed chapter numbers so "Wstęp" became chapter 2. All three are fixed and each now has a scenario.

Approximations remain and are marked in the source: the font is TeX Gyre Termes rather than Times New Roman (TYP-006) — a Times clone, so the *shape* matches, but it is narrower and the body now fits about 92 characters per line where SRC-002 asks for ~70, which a test pins as a recorded deviation — and which SRC-002 + SRC-003 make unavoidable at 12 pt with 2.5 cm margins (see SPEC-SOURCE's conflicts section; the same arithmetic puts ~39 lines on a page against the source's ~30); several spacings are converted from "line spaces" to em units; and the annex label is right-aligned in the text block rather than placed in the page margin.
<!-- SECTION:NOTES:END -->
