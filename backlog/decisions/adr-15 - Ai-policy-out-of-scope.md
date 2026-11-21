---
id: ADR-15
status: accepted
date: 2026-11-21
---

# ADR-15: The faculty AI policy is out of scope

## Context

The faculty *Zasady dyplomowania* permits the use of AI tools in a thesis, but delegates the conditions to a separate faculty policy that it does not reproduce (SRC-039). That policy was carried as an open obligation from M-0 into M-1 and appeared as an open question in SPEC-SCOPE and SPEC-LTX.

The obligation was never satisfiable from the material at hand: no such policy has been located among the faculty pages reviewed, and the guidelines only assert that one exists. Carrying it forward made an unowned item look like a scheduled dependency.

## Decision

1. **Do not pursue the faculty AI policy.** It is out of scope for the template and is no longer a tracked obligation.
2. **Delete the obligation** from the M-0 residual list, from M-1, and from the SPEC-SCOPE open questions.
3. **Close SPEC-LTX open question 6 as "no".** Neither package offers a declaration or disclosure environment. A template is not the right place to assert how a student declared their tool use: the wording belongs to the faculty form, and a class that emitted its own declaration would invent institutional text.
4. **Keep SRC-039 as recorded evidence**, because it is a true statement about the source and removing it would misrepresent the document. Change only its disposition: from *open — obtain* to *recorded, deliberately not pursued*.
5. **State the boundary wherever AI is mentioned**: this repository says nothing about whether a thesis produced with its help satisfies the faculty's AI rules, and a student must settle that with their supervisor.

## Consequences

- M-1 no longer carries an item it cannot close, and the residual-obligation list contains only things a maintainer can actually do.
- The repository is silent on AI-use compliance. That silence is now a recorded decision rather than an oversight, and it must not be read as permission.
- If a student later needs the declaration text, it arrives as a faculty-supplied asset with provenance recorded per ADR-7, not as an invented template feature.
- Reopening this requires a new ADR; a pull request adding a declaration environment without one contradicts a written decision.

## What this does not authorize

It does not authorize the use of AI tools in a thesis, does not claim that any output complies with the unexamined policy, and does not mark SRC-039 as verified.
