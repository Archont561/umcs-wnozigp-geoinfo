---
id: doc-2
title: SPEC-SCOPE — Project scope and boundaries
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:45'
---

## SPEC-SCOPE — Project scope and boundaries

**Status:** Draft  
**Version:** 0.1  
**Related decisions:** ADR-1, ADR-2  
**Milestone:** M-0

## Purpose

Specify a future library of separate LaTeX and Typst thesis-writing aids for students in UMCS WNoZiGP Geoinformatics. The repository starts with compileable dummy mains and a plan for evidence-backed requirements. No user-facing template is implemented yet.

## Intended audience

- Students preparing a thesis in the target program, after the current cohort rules are verified.
- Maintainers reviewing academic requirements, package APIs, builds, and editorial guidance.

## Goals

1. Maintain separate format-specific specifications and sources.
2. Trace institutional requirements to a dated primary source and applicable cohort.
3. Provide small, reproducible smoke builds before implementing template features.
4. Support Polish technical prose review with a conservative, human-reviewed Vale preset.
5. Keep citations, bibliography behavior, engine support, licensing, and distribution explicit.

## Non-goals for the scaffold

- It is not a complete thesis template or a substitute for current faculty instructions.
- It does not imply UMCS affiliation, endorsement, or compliance.
- It does not promise Typst compatibility with Overleaf or any particular LaTeX editor.
- It does not choose a citation style, bibliography workflow, license, or package registry, nor approve package-release readiness. A user-requested GitHub workflow publishes source-only archives for `v*` tags; this does not grant license clearance or institutional approval.
- It does not bundle logos, seals, fonts, student data, or other unreviewed assets.

## Requirements

- **SCOPE-001:** LaTeX and Typst sources shall remain separate deliverables with independent contracts.
- **SCOPE-002:** Each coded institutional rule shall link to evidence in SPEC-SOURCE.
- **SCOPE-003:** Dummy mains and their generated PDFs shall be identified as smoke fixtures, not product examples.
- **SCOPE-004:** Public-release claims require explicit decisions and review gates in SPEC-QA.

## Open questions

- Which academic-year document applies to each target cohort?
- Is the target Geoinformatics program a narrow first release or one profile among several?
- Which requirements are institution-wide versus faculty/program-specific?
- Who approves student-facing behavior and public releases?
