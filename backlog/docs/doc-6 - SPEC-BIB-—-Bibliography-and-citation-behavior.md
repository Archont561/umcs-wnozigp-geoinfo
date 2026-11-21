---
id: doc-6
title: SPEC-BIB — Bibliography and citation behavior
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:37'
---

## SPEC-BIB — Bibliography and citation behavior

**Status:** Draft  
**Version:** 0.1  
**Related tasks:** TASK-6, TASK-8  
**Milestone:** M-1, M-3

## Purpose

Define a consistent, maintainable citation and bibliography experience without assuming that BibLaTeX/Biber, a particular citation style, or identical behavior across LaTeX and Typst is required by UMCS.

## Candidate options

| Format | Candidate approach | Unresolved questions |
| --- | --- | --- |
| LaTeX | BibLaTeX with Biber | Which citation style and language mappings? Which engines/editors support the selected toolchain? |
| Typst | Native bibliography support or a verified package | Does it satisfy the accepted institutional rules? Which syntax, sorting, localization, and CSL behavior are needed? |

These are options for investigation, not decisions or implemented features.

## Requirements

- **BIB-001:** Any supported citation workflow shall document adding a source, citing it, and generating the bibliography.
- **BIB-002:** Citation style and language behavior shall be reviewed against current faculty guidance.
- **BIB-003:** Tests shall cover representative books, articles, websites, Polish diacritics, and missing metadata.
- **BIB-004:** LaTeX and Typst behavior shall be tested separately; visual parity shall not be presumed.
- **BIB-005:** Sample references shall be synthetic or public-domain and contain no personal student data.

## Decision gate

TASK-6 will compare candidate workflows and record a decision before bibliography code is added to either dummy main.
