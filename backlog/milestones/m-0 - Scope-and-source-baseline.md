---
id: m-0
title: "Scope, source evidence, and repository baseline"
---

## Goal

Establish a reviewable specification-first baseline before implementing either format. This milestone is not a delivery date and does not approve a package release.

## Grouped tasks

| Task | Work |
| --- | --- |
| TASK-0 | Scaffold the repository, dummy mains, specifications, and backlog structure. **Done** |
| TASK-1 | Verify the current official guidance and its cohort applicability. **Done** — 44-entry extraction in SPEC-SOURCE v0.3; target cohort set to 2026/27 (ADR-10); owner review (ADR-9). |
| TASK-2 | Confirm audience, scope, non-goals, and the first target profile. **Done** — SPEC-SCOPE v0.3 records the target profile, the institution/faculty split, and owner review. |
| TASK-3 | Decide license, ownership, and provenance for the supplied Vale rules and future assets. Repository work is MIT-licensed (ADR-7); preset terms remain open. |

## Exit criteria

The source register has reviewed evidence; scope and non-goals have an owner review; licensing and third-party reuse are either decided or explicitly gated. No package implementation is implied by completion of the scaffold task.

### Status as of 2026-11-21

| Criterion | State | Evidence |
| --- | --- | --- |
| Source register has reviewed evidence | **Met** | SPEC-SOURCE v0.3 records 44 extracted rules (SRC-001..SRC-044) with edition, URL, and section locators, excludes the superseded 2017 edition, and is reviewed by the repository owner under ADR-9. |
| Scope and non-goals have an owner review | **Met** | SPEC-SCOPE v0.3 states the target profile (WNoZiGP, Geoinformatyka), splits faculty from university rules, and records owner review. TASK-2 criteria 1 and 3 are closed against ADR-9. |
| Licensing and third-party reuse decided or explicitly gated | **Met** | Repository work is MIT (ADR-7); the supplied PLTechnical Vale preset remains gated as unreviewed for redistribution (ADR-4, ADR-5). |
| No package implementation implied | **Met** | `packages/` still holds dummy mains only; ADR-8 covers the build pipeline, not compliance. |

### What closed it, and what it does not mean

Both open items were closed by decision, not by new evidence:

- **ADR-9** makes the repository owner the sole reviewer. That satisfies the review criterion, but it is **single-person review**, not faculty endorsement. No faculty, supervisor, or student reviewer has signed the ledger.
- **ADR-10** sets the target cohort to the next academic period (2026/27), using the 2025/26 document as a proxy. The applicability answer is therefore **conditional**: the 2026/27 edition must be re-reviewed when published.

### Residual obligations carried into M-1

1. Re-review SPEC-SOURCE against the 2026/27 edition on publication.
2. Obtain Annexes 1–5, the normative form templates (SRC-041); without them a template can satisfy the prose rules but not the required forms. Annexes 1 and 2 are now partly located (SRC-045, SRC-046).

The faculty AI policy (SRC-039) is no longer a residual obligation: ADR-15 places it out of scope.

**Verdict: M-0 closed on 2026-11-21** with the review and cohort criteria met by ADR-9 and ADR-10 respectively. Closure records a reviewed evidence baseline; it approves no template, no engine, and no release, and it does not constitute institutional approval.
