---
id: ADR-2
status: accepted
date: 2026-11-09
---

# ADR-2: Keep LaTeX and Typst as separate product targets

## Context

The repository description covers both LaTeX and Typst. Their compiler, editor, bibliography, dependency, and distribution models differ and have not yet been approved.

## Decision

1. Keep format-specific source, package contracts, build tasks, and future validation separate.
2. Share only repository-level specifications, evidence, and quality policies where the requirements truly overlap.
3. Do not assume visual parity, common APIs, the same bibliography implementation, or compatibility with the same editors.
4. Do not claim Typst support in Overleaf. Test LaTeX editor workflows only after the engine and dependencies are decided.

## Consequences

- `packages/latex/main.tex` and `packages/typst/main.typ` remain separate smoke fixtures.
- Future implementation tasks must reference SPEC-LTX or SPEC-TYP and state format-specific acceptance evidence.
