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

That underwrites decision 5 — the rules can ship under MIT — but it is a
maintainer's reading rather than a licence text, so it is put to the author for
confirmation as V-1 in the reviewer ledger. If the tokens turn out to be
transcribed from a third party's list, decision 5's basis fails and the rules
must be rewritten or removed.

Separately, and regardless of licensing: the preset applies the guidance to
technical and academic prose, where several of its rules are wrong or
over-strict. SPEC-EDIT records which rules were weakened and why, including that
`UnitSpacing` — the only rule that can fail CI — has no basis in the guidance at
all.

## Consequences

- `pixi install --locked` retrieves Vale from the configured Conda channels. No `vale sync` is required for the local styles.
- Any rule changes require review, test examples, and an update to SPEC-EDIT.
- TASK-7 and TASK-3 track editorial-policy and redistribution review. The
  redistribution question is put to the preset's author as **V-1** in [REVIEWERS](../docs/doc-9%20-%20REVIEWERS-%E2%80%94-Open-reviewer-questions.md).
