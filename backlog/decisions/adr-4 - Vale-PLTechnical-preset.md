---
id: ADR-4
status: accepted
date: 2026-11-09
---

# ADR-4: Provision Vale from Conda and keep the PLTechnical rules local

## Context

The user supplied `Vale_PLTechnical_preset.zip.txt` and specified that Vale must be downloaded from Conda to apply the preset. The archive contains a local `.vale.ini`, five custom rules, and a README; it does not contain an explicit license file.

## Decision

1. Pin Vale `3.26.0` in the root Pixi Conda dependencies. Pixi provisions the `vale` executable; do not install a separate binary or add a package-local environment.
2. Store the supplied configuration and rules in root `.vale.ini` and `styles/PLTechnical/` so they work offline after the Vale executable is provisioned.
3. Run the repository lint with a warning-level threshold. Treat suggestions as review prompts, not automatic corrections.
4. Preserve the preset's stated limits and source references in SPEC-EDIT. Do not present it as an official language standard, a full grammar checker, or a compliance tool.
5. Do not redistribute the rules publicly until their ownership and license terms are reviewed; the attachment had no license file.

## Provenance (recorded 2026-11-22)

The maintainer states that the preset is custom-made from the Polish
plain-language guidance on `gov.pl`, and that **there is no second source** —
those pages are its only external basis. SPEC-EDIT records the five pages, and
one finding matters for this decision: **none of them states a licence**, and
none needs to, because what the preset takes from them is advice about writing
rather than text. The rule tokens and messages are original to this
repository.

That underwrites decision 5 — the rules can ship under MIT — and the author
confirmed it on 2026-11-22, stating that the rules were written by them from the
guidance. **Decision 5 is therefore satisfied and no longer gates anything.**

The confirmation is an assertion of authorship by the repository's own copyright
holder rather than third-party review, which is the single-person limitation ADR-9
already records for the evidence ledger. It is recorded as such in
[REVIEWERS](../docs/doc-9%20-%20REVIEWERS-%E2%80%94-Open-reviewer-questions.md)
under *Answered*: it is the best available evidence, and nothing inside this
repository could have produced better.

Separately, and regardless of licensing: the preset applies the guidance to
technical and academic prose, where several of its rules are wrong or
over-strict. SPEC-EDIT records which rules were weakened and why, including that
`UnitSpacing` — the only rule that can fail CI — has no basis in the guidance at
all.

## Consequences

- `pixi install --locked` retrieves Vale from the configured Conda channels. No `vale sync` is required for the local styles.
- Any rule changes require review, test examples, and an update to SPEC-EDIT.
- TASK-7 and TASK-3 track editorial-policy and redistribution review. The
  redistribution question (V-1) was answered on 2026-11-22 and is closed; see
  [REVIEWERS](../docs/doc-9%20-%20REVIEWERS-%E2%80%94-Open-reviewer-questions.md)
  under *Answered*. TASK-3's only remaining open criterion is U-1, which does
  not block a release (ADR-19).
- If the rules are ever found to contain transcribed third-party text, decision 5
  fails and the affected rules must be rewritten or removed. Nothing currently
  asserts that they do.
