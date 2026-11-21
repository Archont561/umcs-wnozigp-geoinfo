---
id: doc-5
title: SPEC-TYP — Typst package contract
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-TYP — Typst package contract

**Status:** Draft  
**Version:** 0.1  
**Related tasks:** TASK-5, TASK-8, TASK-9  
**Milestone:** M-1, M-2

## Current scaffold

`packages/typst/main.typ` is a compileable dummy using built-in Typst features. There is no registry manifest or reusable thesis package yet. The dummy is only a build fixture.

## Proposed contract to resolve

- **Package shape:** Decide whether the deliverable is a set of helper functions, a template entry point, or both.
- **Compiler:** Select and test a minimum version only after syntax and package behavior are reviewed.
- **Package dependencies:** Prefer built-in features unless external packages are justified, licensed, and pinned.
- **Typography/layout:** Define format-specific values only from verified sources; do not assume exact parity with LaTeX.
- **Editor support:** Do not claim Overleaf support for Typst. Document the actual tested editor/compiler setup.
- **Distribution:** Keep registry and package-name decisions open until account ownership, naming, license, assets, and release gates are approved.

## Requirements

- **TYP-001:** The reusable entry point and configuration fields shall be documented before implementation.
- **TYP-002:** A tested compiler version shall be recorded separately from the future minimum supported version.
- **TYP-003:** Any imported third-party package shall have a dependency and license record.
- **TYP-004:** Smoke fixtures shall be separate from any future package offering.
- **TYP-005:** Academic behavior shall be validated against SPEC-SOURCE; successful compilation is not a compliance claim.

## Acceptance evidence

Before this specification is Approved, record the API, compiler policy, registry/editor decision, dependency inventory, source-level tests, visual review, and explicit limitations. See TASK-5 and TASK-8.
