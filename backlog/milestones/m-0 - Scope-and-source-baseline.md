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
| TASK-1 | Verify the current official guidance and its cohort applicability. **In Progress (3/4)** — source set, 44-entry extraction, and conflict handling recorded in SPEC-SOURCE v0.2; reviewers unassigned. |
| TASK-2 | Confirm audience, scope, non-goals, and the first target profile. **In Progress (2/4)** — SPEC-SCOPE v0.2 records the target profile and the institution/faculty split; owner approval and reviewer assignment outstanding. |
| TASK-3 | Decide license, ownership, and provenance for the supplied Vale rules and future assets. Repository work is MIT-licensed (ADR-7); preset terms remain open. |

## Exit criteria

The source register has reviewed evidence; scope and non-goals have an owner review; licensing and third-party reuse are either decided or explicitly gated. No package implementation is implied by completion of the scaffold task.

### Status as of 2026-11-21

| Criterion | State | Evidence |
| --- | --- | --- |
| Source register has reviewed evidence | **Partly met** — evidence recorded, review not done | SPEC-SOURCE v0.2 lists 44 extracted rules (SRC-001..SRC-044) with edition, URL, and section locators, plus the superseded 2017 edition and its divergent figures. No named reviewer has signed it. |
| Scope and non-goals have an owner review | **Not met** | SPEC-SCOPE v0.2 states the target profile (WNoZiGP, Geoinformatyka, 2025/26 rules) and splits faculty from university rules. The ownership table leaves student-facing review unassigned, so TASK-2 acceptance criteria 1 and 3 remain open. |
| Licensing and third-party reuse decided or explicitly gated | **Met** | Repository work is MIT (ADR-7); the supplied PLTechnical Vale preset is explicitly gated as unreviewed for redistribution (ADR-4, ADR-5). |
| No package implementation implied | **Met** | `packages/` still holds dummy mains only; ADR-8 covers the build pipeline, not compliance. |

### Why this milestone stays open

Two exit criteria need a human, not more research:

1. **Reviewer assignment.** No faculty, supervisor, or student reviewer has confirmed the extracted rules or the scope.
2. **Cohort confirmation.** The 2025/26 document binds students who began thesis preparation in the 2025/26 summer semester. Whether it still governs a 2026/27 cohort, and whether a newer edition is due, is an owner question.

Also unresolved and blocking template work, though not the milestone exit itself: the normative Annexes 1–5 were referenced but not extracted (SRC-041), and the faculty AI policy cited by the source was not reproduced (SRC-039).

**Verdict: M-0 cannot be closed yet.** The research half is done and recorded; the approval half is not, and closing on evidence alone would contradict the milestone's own criteria.
