---
id: ADR-13
status: accepted
date: 2026-11-21
---

# ADR-13: Keep the Vale gate at warning level in the task, not in `.vale.ini`

## Context

The PLTechnical preset has two severities: suggestions (four rules) and warnings (UnitSpacing). `.vale.ini` sets `MinAlertLevel = suggestion`, while the `lint-vale` Pixi task passes `--minAlertLevel=warning`.

That split is deliberate but undocumented, and it means a maintainer could change the gate's meaning by editing either file. TASK-7 acceptance criterion 4 asks how an alert can be overridden "without weakening the project-wide checks silently".

## Decision

1. Keep `MinAlertLevel = suggestion` in `.vale.ini`, so the preset stays usable for a full advisory review.
2. Keep `--minAlertLevel=warning` in the `lint-vale` task, so the blocking gate ignores suggestions.
3. Treat any change to either value as a **policy change requiring an ADR**, not an edit (recorded as EDIT-006).
4. Document the three local overrides — rewriting the sentence, an inline code span, and a per-path `.vale.ini` section — as the preferred ways to silence a single finding.
5. Require that the preset is never described as checking thesis prose, because there is no LaTeX or Typst extractor (EDIT-007).

## Consequences

- A contributor can silence one finding in one file without weakening anything else.
- The gate is insensitive to suggestions by design, so "Vale passes" means "no UnitSpacing warnings", not "the prose is clean". SPEC-EDIT states this because the distinction is easy to over-read.
- Changing the threshold now requires a written decision, which is more friction than a one-line edit — and that friction is the point.
- Vale remains advisory for the four suggestion rules; it cannot block a pull request on style, only on unit spacing.
