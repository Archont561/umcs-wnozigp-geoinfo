---
id: ADR-10
status: accepted
date: 2026-11-21
---

# ADR-10: Target the next academic period, not the 2025/26 cohort

## Context

The verified source, *Zasady dyplomowania na WNoZiGP UMCS 2025/2026*, states its own applicability: the thesis-preparation rules bind students who began preparing a thesis in the 2025/26 summer semester, and the examination rules apply from the 2025/26 winter session.

That leaves the repository's future users unaddressed. A template first developed now would be used by students writing theses in the 2026/27 period, which the 2025/26 document does not itself govern. The owner was asked whether the target cohort is the 2025/26 cohort or the next academic period, and selected the next period.

## Decision

1. The intended cohort for the first template release is **the next academic period (2026/27)**, not the 2025/26 cohort.
2. Treat the 2025/26 document as the best available proxy for the next period's rules, not as authority over it.
3. Re-verify against the 2026/27 edition when it is published. Any requirement that changes must be updated in SPEC-SOURCE before the template claims to serve that cohort.
4. Do not claim that the current extraction is valid for the 2026/27 cohort as published. The claim is that its requirements will be re-checked against the next edition.
5. If the 2026/27 edition differs materially from the 2025/26 document, supersede this decision rather than patching silently.

## Consequences

- SPEC-SOURCE's applicability note now reads: evidence from 2025/26, target cohort 2026/27, re-verification pending.
- M-0's cohort question is answered as a decision, but it is a *conditional* answer: the evidence base is provisional until the next edition exists. This is recorded as a risk, not a closure.
- TASK-1 gains a follow-up obligation: re-review on publication of the 2026/27 rules.
- Students reading the repository are told the rules were verified against 2025/26 and must confirm the current edition themselves.
