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

## Consequences

- `pixi install --locked` retrieves Vale from the configured Conda channels. No `vale sync` is required for the local styles.
- Any rule changes require review, test examples, and an update to SPEC-EDIT.
- TASK-7 and TASK-3 track editorial-policy and redistribution review.
