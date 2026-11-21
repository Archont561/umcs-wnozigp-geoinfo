---
id: doc-4
title: SPEC-LTX — LaTeX package contract
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-LTX — LaTeX package contract

**Status:** Draft  
**Version:** 0.1  
**Related tasks:** TASK-4, TASK-8, TASK-9  
**Milestone:** M-1, M-2

## Current scaffold

`packages/latex/main.tex` is a minimal compileable dummy. No `.cls` or `.sty` package is present. The dummy must not be copied into an academic submission as a template or compliance example.

## Proposed contract to resolve

- **Package form:** Decide between a document class, a style package, or a small collection of components after requirements review.
- **Document entry point:** Keep a minimal main file and separate reusable package sources; do not mix fixture text with reusable macros.
- **Language:** Polish is the primary target for student-facing labels. English-language abstract/title behavior requires a spec decision.
- **Engine matrix:** Evaluate pdfLaTeX, LuaLaTeX, and XeLaTeX. Tectonic is currently only a smoke-build tool; it does not establish native-engine compatibility.
- **Editor workflow:** Test Overleaf only after the engine and dependency set are known. Do not advertise compatibility before a clean import test.
- **Bibliography:** Defer citation and bibliography commands to SPEC-BIB; do not bake in BibLaTeX/Biber assumptions.
- **Assets:** No institutional mark, seal, or bundled font may be added without documented permission and provenance.

## Requirements

- **LTX-001:** A future package shall expose a documented entry point and stable configuration interface.
- **LTX-002:** Every non-standard dependency shall be inventoried with supported version and engine notes.
- **LTX-003:** Test fixtures shall remain separate from the distributable package files.
- **LTX-004:** The supported engine/editor matrix shall be evidence-backed and tested independently.
- **LTX-005:** Rendered output shall be checked against accepted source requirements; a successful compile alone is insufficient.

## Acceptance evidence

Before this specification is Approved, record: verified academic requirements; public API; supported engines and dependency versions; clean build procedure; output review; and user-facing limitations. See TASK-4 and TASK-8.
