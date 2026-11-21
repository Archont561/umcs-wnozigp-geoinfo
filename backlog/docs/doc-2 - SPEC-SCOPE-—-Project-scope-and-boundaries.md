---
id: doc-2
title: SPEC-SCOPE — Project scope and boundaries
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 20:11'
---

## SPEC-SCOPE — Project scope and boundaries

**Status:** Draft (scope confirmed from verified evidence; owner review outstanding)  
**Version:** 0.2  
**Related decisions:** ADR-1, ADR-2, ADR-7  
**Related evidence:** SPEC-SOURCE (verified 2025/26 faculty rules)  
**Milestone:** M-0

## Purpose

Specify a future library of separate LaTeX and Typst thesis-writing aids for students in UMCS WNoZiGP Geoinformatics. The repository starts with compileable dummy mains and an evidence-backed requirement set. No user-facing template is implemented yet.

## Evidence base for this scope

This scope is grounded in SPEC-SOURCE, which records the *Zasady dyplomowania na WNoZiGP UMCS 2025/2026* reviewed on 2026-11-21. Every scope statement below is either traceable to that ledger or marked as a maintainer choice.

## Intended audience

- Students preparing a licencjacka, inżynierska, or magisterska thesis under the WNoZiGP rules recorded in SPEC-SOURCE.
- Maintainers reviewing academic requirements, package APIs, builds, and editorial guidance.

## First target profile

- **Unit:** Wydział Nauk o Ziemi i Gospodarki Przestrzennej (WNoZiGP), UMCS Lublin.
- **Programme:** Geoinformatyka.
- **Rule edition:** WNoZiGP 2025/2026, per SPEC-SOURCE.
- **Thesis types:** all three named in the source — licencjacka (first cycle), inżynierska (first cycle, engineering), magisterska (second cycle). Whether the first release supports all three or only one is deliberately **not** decided here; that is a maintainer choice recorded in TASK-9/TASK-10, not an institutional requirement.
- **Language:** Polish is the default. The source permits a foreign-language thesis with approval, and then requires the title, captions, and abstract translated into Polish (SRC-037); that is a template concern, not a first-release commitment.

## Goals

1. Maintain separate format-specific specifications and sources.
2. Trace institutional requirements to a dated primary source and applicable cohort — now demonstrated by SPEC-SOURCE's 44-entry ledger.
3. Provide small, reproducible smoke builds before implementing template features.
4. Support Polish technical prose review with a conservative, human-reviewed Vale preset.
5. Keep citations, bibliography behavior, engine support, licensing, and distribution explicit.

## Non-goals for the scaffold

- It is not a complete thesis template or a substitute for current faculty instructions.
- It does not imply UMCS affiliation, endorsement, or compliance.
- It does not promise Typst compatibility with Overleaf or any particular LaTeX editor.
- It does not choose a citation style, bibliography workflow, or package registry, nor approve package-release readiness. A user-requested GitHub workflow publishes source-only archives for `v*` tags; this does not grant license clearance or institutional approval.
- It does not bundle logos, seals, fonts, student data, or other unreviewed assets.

## Requirements

- **SCOPE-001:** LaTeX and Typst sources shall remain separate deliverables with independent contracts. They also make **separate support claims**: a working LaTeX build says nothing about Typst, and vice versa. The source document itself names only Word, OpenOffice Writer, and LibreOffice Writer (SRC-040), so no claim of official format acceptance is made for either engine.
- **SCOPE-002:** Each coded institutional rule shall link to evidence in SPEC-SOURCE.
- **SCOPE-003:** Dummy mains and their generated PDFs shall be identified as smoke fixtures, not product examples.
- **SCOPE-004:** Public-release claims require explicit decisions and review gates in SPEC-QA.
- **SCOPE-005:** Institutional and faculty-level rules shall be distinguished. Everything currently recorded in SPEC-SOURCE is faculty-level (WNoZiGP). University-wide instruments the source points at — the UMCS study regulations, Rector's Order 57/2015 (APD), and the antiplagiarism order 5/2019 — are referenced but not yet reviewed, and must not be treated as satisfied.

## Ownership and review

| Role | Status |
| --- | --- |
| Institutional/faculty rules | Faculty of WNoZiGP as publisher of the source; no individual faculty reviewer has confirmed this scope |
| Student-facing behaviour | **Unassigned** — no student or supervisor reviewer has been identified |
| Technical maintainer | Repository owner (Archont561) |
| Release approval | Unassigned; gated by TASK-13 and SPEC-QA |

## Open questions

These block nothing that is recorded, but they must be answered before any template implementation is called correct.

1. **Cohort window.** The source binds students who began thesis preparation in the 2025/26 summer semester. Does it still bind a 2026/27 cohort, and will a newer edition appear? Owner question for TASK-2.
2. **Annexes 1–5.** The normative layout forms (title page, contents, illustrations, citations, bibliography) are referenced by the source but their exact designs were not extracted (SRC-041). Without them the template can satisfy the prose rules but not the normative forms.
3. **Faculty AI policy.** The source permits AI tools under a faculty policy it does not reproduce (SRC-039).
4. **Institution-wide versus faculty-specific.** Only faculty-level rules are recorded so far; SCOPE-005 lists the university instruments still unreviewed.
5. **Scope width.** Is Geoinformatyka a narrow first release or one profile among several WNoZiGP programmes?
6. **Reviewer assignment.** Who approves student-facing behaviour, per the ownership table above?

## What this scope does not authorize

Recording these rules does not approve a template, a release, an engine, or a bibliography workflow. The repository still ships only dummy mains; CI compiling them (ADR-8) proves the pipeline, not compliance.
