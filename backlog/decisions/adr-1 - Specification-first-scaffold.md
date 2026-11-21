---
id: ADR-1
status: accepted
date: 2026-11-09
---

# ADR-1: Use a specification-first repository scaffold

## Context

The GitHub repository began with only a title README. The user requested a whole-repository scaffold with dummy main documents, specifications, Backlog.md tasks, decisions, and milestones.

## Decision

1. Treat `specifications/` as the normative product-planning source. Mark requirements Draft until the relevant evidence and review are complete.
2. Keep LaTeX and Typst as separate targets with separate contracts.
3. Provide only compileable dummy mains at this stage. Do not implement template layout behavior before requirements are verified and scoped.
4. Use Backlog.md milestone files to group task IDs; task files retain dependencies, priorities, and acceptance criteria.
5. Keep release, institutional compliance, and package support claims out of the scaffold until separately approved.

## Consequences

- `main.tex` and `main.typ` exist for smoke-build verification, not for student use.
- Specifications and tasks are intentionally incomplete; open questions are explicit.
- A successful build does not imply a complete or compliant template.
