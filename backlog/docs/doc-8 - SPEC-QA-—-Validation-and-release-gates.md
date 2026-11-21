---
id: doc-8
title: SPEC-QA — Validation and release gates
type: specification
created_date: '2026-11-21 18:33'
updated_date: '2026-11-21 18:43'
---

## SPEC-QA — Validation and release gates

**Status:** Draft (matrix defined, implementation partial)  
**Version:** 0.2  
**Related decisions:** ADR-1, ADR-3, ADR-5, ADR-7, ADR-8, ADR-9, ADR-11, ADR-12  
**Related tasks:** TASK-7–TASK-13  
**Related evidence:** SPEC-SOURCE v0.3, SPEC-LTX v0.2, SPEC-TYP v0.2, SPEC-BIB v0.2  
**Milestone:** M-2, M-3, M-4

## Purpose

Say which checks exist, which are planned, who owns each, and — critically — what a green run actually proves. The repository has repeatedly had a green `check` that compiled nothing; this matrix exists to stop that class of false confidence.

## Check levels

| Level | Name | What it proves | Runs |
| --- | --- | --- | --- |
| **L0** | Static | Structure and syntax are well-formed | Every `pixi run check` |
| **L1** | Tooling unit | The repository's own Python tools behave | Planned |
| **L2** | Smoke compile | A dummy main compiles | CI `smoke` job (ADR-8) |
| **L3** | Package compile | The real class/template compiles | Planned |
| **L4** | BDD behaviour | Named scenarios execute against a build | Dummy only today |
| **L5** | Structural assertion | Rendered output meets specific rules | Planned, feasible |
| **L6** | Visual review | A human accepts the layout | Manual |
| **L7** | Academic review | A human accepts academic correctness | Manual |

The distinction between L2 and L3 matters most: L2 proves the pipeline, L3 proves the deliverable. Today only L2 exists, and no requirement may be closed on L2 evidence.

## L0 — implemented now

| Tool | Scope | Gate |
| --- | --- | --- |
| `alint` | Repository structure, 13 rules | blocking |
| `taplo` | TOML formatting | blocking |
| `rumdl` | Markdown lint, 47 files | blocking |
| `chktex` | LaTeX source lint (dummy) | blocking |
| `typstyle` | Typst formatting (dummy) | blocking |
| `vale` | Polish editorial preset, 44 files | blocking at warning level |
| `tasknest check` | Task discovery | blocking |
| `docs-check` | Generated README/AGENTS freshness | blocking |
| `pixi lock --check` | Lock consistency | blocking |

**What L0 does not prove:** that any document renders correctly, that any rule from SPEC-SOURCE is satisfied, or that either package exists. Vale's role is limited by EDIT-001: it suggests, it never rewrites.

## L5 — the leverage point

Structural assertions are cheap and turn review questions into tests. Both formats expose a introspection route that is verified to work in this environment:

| Format | Mechanism | Verified |
| --- | --- | --- |
| Typst | `typst query` on labelled elements | Yes — `typst query` runs here |
| LaTeX | `\typeout` of computed values, then grep the log | Standard, not yet exercised |

Typst compiles text to paths in SVG, so PDF *text* extraction is unreliable for assertions; querying the typed document tree is the correct route. Recorded because the obvious approach (diff the PDF text) does not work here.

## Supported platforms, engines, compilers

| Item | Declared | Tested | Evidence |
| --- | --- | --- | --- |
| Platform `linux-64` | Yes | **Yes** | CI `ubuntu-24.04`, sandbox restore |
| Platform `linux-aarch64` | Yes (`pixi.toml`) | **No** | never run |
| Platform `osx-64`, `osx-arm64` | Yes | **No** | never run |
| Platform `win-64` | Yes | **No** | never run |
| Tectonic 0.17.0 | Yes | **Dummy only** | CI `smoke`, ADR-8 |
| Typst 0.15.1 | Yes | **Dummy only** | CI `smoke`; `typst query` verified locally |
| XeLaTeX | Candidate | **No** | not installed |
| LuaLaTeX | Candidate | **No** | not installed |
| pdfLaTeX | Candidate | **No** | not installed |
| Biber / BibTeX | Required by ADR-12 LaTeX path | **No** | absent from the environment |
| Overleaf | No claim | **No** | never tested (ADR-11) |

A platform or engine appears as "supported" only after a run is recorded against it. Declaring five platforms in `pixi.toml` is not evidence of four of them working.

## Traceability matrix

Every requirement maps to at least one check. `—` means no check exists yet, which is itself the finding.

### Scope — SPEC-SCOPE

| Req | Check | Level | Owner | Status |
| --- | --- | --- | --- | --- |
| SCOPE-001 (separate deliverables) | alint: both package dirs exist; release archives stay separate | L0 | maintainer | **Passing** |
| SCOPE-002 (rules link to evidence) | Manual: every coded rule cites SPEC-SOURCE | L7 | reviewer | Open |
| SCOPE-003 (dummies marked as fixtures) | rumdl/Vale on the fixture header comments | L0 | maintainer | **Passing** |
| SCOPE-004 (release needs gates) | TASK-13 checklist before any tag | L7 | owner | Open |
| SCOPE-005 (faculty vs university rules) | Manual review of SPEC-SOURCE classification | L7 | reviewer | Open |

### LaTeX — SPEC-LTX

| Req | Check | Level | Owner | Status |
| --- | --- | --- | --- | --- |
| LTX-001 (documented entry point) | Compile a fixture using the class | L3 | maintainer | Planned |
| LTX-002 (dependency inventory) | Manual against SPEC-LTX table | L7 | reviewer | Open |
| LTX-003 (fixtures separate) | Assert the release archive excludes `tests/` and `main.tex` | L1 | maintainer | **Fixed — enforced in `release.yml`** |
| LTX-004 (engine matrix evidence) | Run the matrix, record results | L3 | maintainer | Open |
| LTX-005 (output vs requirements) | Visual comparison to SPEC-SOURCE | L6 | reviewer | Planned |
| LTX-006 (single title-page command) | `\typeout` field list, grep log | L5 | maintainer | Planned |
| LTX-007 (source per float) | Grep fixtures for `\figsource`/`\tabsource` count vs float count | L5 | maintainer | Planned |
| LTX-008 (abstract limit) | Fixture with 4001 characters must warn; 4501 must fail | L3 | maintainer | Planned |
| LTX-009 (no unsupported claim) | Manual review of README/release notes | L7 | reviewer | Open |

### Typst — SPEC-TYP

| Req | Check | Level | Owner | Status |
| --- | --- | --- | --- | --- |
| TYP-001 (entry point, reject unknown keys) | Compile a fixture; a bad key must error | L3 | maintainer | Planned |
| TYP-002 (offline build) | Build with network disabled | L3 | maintainer | Planned |
| TYP-003 (dependency licence record) | Manual against the dependency table | L7 | reviewer | Open |
| TYP-004 (fixtures separate) | Same archive assertion as LTX-003 | L1 | maintainer | **Fixed — enforced in `release.yml`** |
| TYP-005 (minimum version tested) | Matrix run on the declared minimum | L3 | maintainer | Blocked: undecided |
| TYP-006 (font substitution documented) | grep the docs for the substitution note | L1 | maintainer | Planned |
| TYP-007 (independent counters) | `typst query` the three counters | L5 | maintainer | Planned, feasible |

### Bibliography — SPEC-BIB

| Req | Check | Level | Owner | Status |
| --- | --- | --- | --- | --- |
| BIB-001 (workflow documented) | Manual: README shows add/cite/render | L7 | reviewer | Open |
| BIB-002 (style reviewed vs guidance) | Manual comparison to SRC-027..036 | L7 | reviewer | Open |
| BIB-003 (test coverage of cases) | Fixtures: book, article, web, diacritics, missing field | L3 | maintainer | Planned |
| BIB-004 (no parity presumption) | Manual: no test compares the two outputs | L7 | reviewer | Open |
| BIB-005 (synthetic references) | grep fixtures; no real names or student data | L1 | maintainer | Planned |
| BIB-006 (styles in-repo, offline) | Build with network disabled | L3 | maintainer | Planned |
| BIB-007 (punctuation assertion) | Extracted text match for four entry types | L5 | maintainer | Planned |
| BIB-008 (in-text forms) | Fixtures for `za:` and `1999a` | L5 | maintainer | Planned |

### Editorial — SPEC-EDIT

| Req | Check | Level | Owner | Status |
| --- | --- | --- | --- | --- |
| EDIT-001 (human judgment) | Vale runs with `--no-exit` on the demo only; no auto-rewrite task | L0 | maintainer | **Passing** |
| EDIT-002 (rules version-controlled) | alint: `.vale/styles/PLTechnical` exists | L0 | maintainer | **Passing** |
| EDIT-003 (test cases) | Fixtures for clean text, alerts, code spans, unit spacing | L1 | maintainer | Planned |
| EDIT-004 (preset licence review) | Manual — **still open** (ADR-4, ADR-5) | L7 | owner | Open |

### Quality gates — this document

| Req | Check | Level | Owner | Status |
| --- | --- | --- | --- | --- |
| QA-001 (check stays cheap) | Assert `check` has no build dependencies | L1 | maintainer | **Passing by construction** |
| QA-002 (smoke reported as compile-only) | Review CI job names and docs wording | L7 | reviewer | **Passing** |
| QA-003 (record environment for visual tests) | Template requires engine, version, platform, fonts | L6 | reviewer | Planned |
| QA-004 (no PDFs as artifacts) | Assert `.gitignore` and release assets | L1 | maintainer | **Passing** |
| QA-005 (release archives) | Inspect the release workflow | L1 | maintainer | **Passing config, never executed** |
| QA-011 (licence in every artifact) | Release job asserts `LICENSE` is inside each tarball | L1 | maintainer | **Passing, verified by simulation** |

## Summary of the matrix

| Status | Count |
| --- | --- |
| Passing | 9 |
| Passing (newly) | 2 — LTX-003 and TYP-004, closed by the archive fix |
| Planned | 18 |
| Open / manual | 12 |
| Blocked | 1 (TYP-005, minimum version undecided) |

The two former failures were one defect seen from two sides: `release.yml` now excludes `main.*` and `tests/` and asserts the exclusion after writing each archive, so a regression fails the release job instead of shipping silently.

## Representative content and baselines

Fixtures must cover, at minimum:

- Polish diacritics in body text, headings, captions and the bibliography (`SRC-035`).
- A table with a source line and no empty cells (`SRC-015`–`SRC-017`).
- A figure with a source line and a scale (`SRC-018`, `SRC-019`).
- At least one photograph, to exercise the third counter (`SRC-021`).
- An equation in chapter 2, expecting `(2.1.)` (`SRC-026`).
- Three or more authors, an edited volume, a same-year pair, a web source (`SRC-029`–`SRC-033`).
- A record with a missing field, to prove nothing invents a placeholder.
- A 4000-character abstract boundary case (`SRC-014`).

**Baseline policy.** Byte-identical PDF comparison is rejected: PDFs embed creation timestamps and object IDs, so every rebuild differs. Instead:

1. **Preferred:** structural assertions (L5) on values extracted from the log or document tree.
2. **Fallback:** a normalised text extraction compared line by line, with the extraction tool and its version recorded (QA-003).
3. **Visual:** human review with a recorded environment line: engine, version, platform, font list, and the source commit.

A visual baseline is a screenshot plus its environment record. Without the environment line it is not evidence.

## Owners

| Role | Who | Scope |
| --- | --- | --- |
| Automated checks | Maintainer (Archont561) | L0, L1, L3, L5 |
| Review | Repository owner as sole reviewer (ADR-9) | L6, L7 |
| Institutional acceptance | **None assigned** | outside this repository |

Every "Open" item above is owned by the same single reviewer, which is a concentration risk recorded in ADR-9 and repeated here.

## CI policy

ADR-8 approved one exception to QA-001: the `smoke` job runs `test-smoke` in parallel with `check`, so a broken dummy fails a pull request. Beyond that:

- Expensive matrix runs (multiple engines, multiple platforms) stay **opt-in**, triggered manually or on a tag.
- No CI job may compile the *package* until the package exists.
- Adding a build to CI requires an ADR, not a workflow edit.

## Release decision gates

No CTAN or Typst registry submission is selected or approved (ADR-12 leaves registry naming undecided). A GitHub tag-release workflow publishes source-only archives for `v*` tags. A tag push is a publication action and does not imply licence clearance, UMCS approval, or package readiness. Resolve before pushing a tag:

- third-party rule/font/logo provenance and any per-package licence deviation from MIT (ADR-7, ADR-14);
- supported artifact contents — the archive now excludes fixtures (LTX-003, TYP-004), though the package itself does not exist yet;
- student-facing and institutional review, plus independent human approval;
- a clean build, reproducible artifact inventory, checksums, and a rollback/withdrawal procedure.

## Requirements

- **QA-001:** Root `check` shall not silently run expensive manual builds.
- **QA-002:** A passing smoke build shall be reported only as compilation success.
- **QA-003:** Future visual tests shall record engine/compiler version, platform, fonts, and reference source.
- **QA-004:** No generated PDF, student document, or private data is a release artifact by default.
- **QA-005:** `.github/workflows/release.yml` shall attach only separate source archives for the LaTeX and Typst package directories when a `v*` tag is pushed; it shall run repository checks and package smoke tests before publication.
- **QA-006:** Every requirement in SPEC-SCOPE, SPEC-LTX, SPEC-TYP and SPEC-BIB shall map to at least one named check level, and the mapping shall be maintained in this document.
- **QA-007:** A requirement shall not be marked satisfied on L2 evidence, because a smoke compile proves the pipeline and not the deliverable.
- **QA-008:** Platform and engine support shall be claimed only for combinations with a recorded run.
- **QA-009:** Release archives shall exclude test fixtures, so LTX-003 and TYP-004 are mechanically enforced.
- **QA-010:** PDF byte-comparison shall not be used as a regression gate.
- **QA-011:** Every published artifact shall contain its own licence file, asserted by the release job rather than assumed (ADR-14).

This draft does not establish institutional endorsement or full compliance.
