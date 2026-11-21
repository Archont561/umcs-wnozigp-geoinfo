---
id: ADR-17
status: accepted
date: 2026-11-21
---

# ADR-17: Fold photographs into figures, add listings, drop two annex indexes

## Context

SRC-021 records that the faculty document names **three** illustration classes — tables, figures (*ryciny*) and photographs (*fotografie*) — each numbered independently with its own index. SRC-023 requires a separate "Spis fotografii", and SRC-025 a "Spis załączników" listing every annex with its title.

The repository owner directed on 2026-11-21 that the package instead:

- keep only **Rycina/Rysunek**, **Tabela** and **Listing**;
- give **listings** their own independent numbering;
- have **no** "Spis fotografii" and **no** "Spis załączników";
- number annexes with references, not an index.

This is a departure from the source, not a reading of it. It is recorded here rather than absorbed silently into the specification, because a student relying on the package needs to know which requirement it deliberately does not satisfy.

## Decision

1. **Remove the photograph class.** `photograph(...)` and `list-of-photographs()` are deleted. A photo is inserted with `figure-with-source` and numbered with the figures.
2. **Add a listing class.** `listing(...)` and `list-of-listings()` carry their own counter, with the caption above the block the way a table's is.
3. **Remove `list-of-annexes()`.** Annexes keep their own numbering and their "Załącznik N" page header (SRC-024), but there is no index of them (contrary to SRC-025).
4. **Provide `annex-ref(n)`** so a chapter can still point at an annex, e.g. "patrz załącznik 2".
5. **State the deviation in SPEC-TYP** and in the package README, naming SRC-021, SRC-023 and SRC-025, so it is visible to anyone comparing the output with the faculty document.

## Consequences

- The rendered document no longer matches the faculty text on three points. A student submitting it as-is would be missing an index the faculty asks for.
- The counters remain **independent and tested**: one table, two figures, one listing in the demo, and a scenario asserts that no photograph counter exists.
- Two classes now share the "caption below" rule (figures) and two share "caption above" (tables, listings), so the layout code is simpler than the three-class model it replaces.
- `annex-ref` is a plain text helper, not a live `ref`. Typst refuses to reference a label applied to a multi-element function result, and every single-element wrapper either floated the content or rejected the page break. The cost is that renaming or reordering annexes does not renumber existing references.
- Reversing this needs a new ADR; restoring the photograph class is not a refactor, it is a scope decision.

## What this does not authorize

It does not approve the package for submission, does not claim SRC-021, SRC-023 or SRC-025 compliance, and does not change the evidence ledger — SRC-021 and SRC-023 stay recorded exactly as the faculty wrote them.
