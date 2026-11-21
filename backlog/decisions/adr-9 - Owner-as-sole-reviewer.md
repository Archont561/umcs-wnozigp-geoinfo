---
id: ADR-9
status: accepted
date: 2026-11-21
---

# ADR-9: Let the hosting repository's owner act as the only reviewer

## Context

M-0 requires an owner review of the extracted rules and the scope, and TASK-2 acceptance criterion 3 requires named reviewers for student-facing requirements. The scaffold left every reviewer slot unassigned, so the milestone could not close on evidence alone.

The repository owner asked what was needed to finish, was given two options — assign a named faculty or supervisor reviewer, or record the owner as sole reviewer — and selected the unnamed option.

## Decision

1. The repository owner (Archont561) is the sole reviewer of SPEC-SOURCE and SPEC-SCOPE for the purposes of the M-0 exit criteria.
2. Do not name a faculty member, supervisor, or student reviewer. No reviewer identity is invented.
3. Record this as a scope limitation, not as institutional validation. Owner review means the maintainer asserts the extraction is faithful to the cited document; it does not mean the faculty has endorsed the repository, the rules, or any template.
4. Keep the institutional authority with the faculty: the 2025/26 *Zasady dyplomowania* remains the normative source, and any divergence between this repository and that document is resolved in the document's favour.
5. Reopen this decision if a faculty or student reviewer is later assigned.

## Consequences

- M-0's review criteria can be satisfied by owner review, and TASK-2 criterion 3 can be closed against this decision.
- The repository states plainly that it is **not** institution-approved and has no external reviewer, so students must check the official faculty document before relying on any output.
- The review is single-person; a single-reviewer ledger is weaker evidence than an independent one, and this is recorded as a residual risk rather than hidden.
- Annexes 1–5 remain partly unobtained (SRC-041). Owner review does not supply them, and they stay open. The faculty AI policy (SRC-039) was dropped from scope by ADR-15 rather than left open.
