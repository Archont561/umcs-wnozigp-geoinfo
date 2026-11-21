---
id: ADR-14
status: accepted
date: 2026-11-21
---

# ADR-14: Ship MIT with each package, not only at the repository root

## Context

ADR-7 licensed the repository's original work under MIT with a single root `LICENSE`. The release workflow publishes the LaTeX and Typst package directories as **standalone tarballs**. A consumer who downloads only such a tarball has no licence text and therefore no stated terms, because the root `LICENSE` is not inside it.

## Decision

1. Add `packages/latex/LICENSE` and `packages/typst/LICENSE`, each a verbatim copy of the root MIT text with the same copyright holder.
2. Keep the root `LICENSE` as the repository-wide statement; the per-package files do not replace it.
3. Require every package tarball to contain its `LICENSE`, and assert this in the release workflow so a missing licence fails the release instead of shipping unlicensed.
4. Record the licence in each package's README.
5. Do **not** add a `license` field to a package manifest that does not exist yet. `packages/typst/typst.toml` will carry `license: "MIT"` when the package is implemented (TASK-10); `package.json` stays `private` because it is tooling, not a published package.

## Consequences

- Every published artifact carries its own terms; no consumer has to guess.
- Three copies of the same text must stay in sync. This is deliberate: a tarball that omits its licence is worse than a duplicated file. TASK-8's matrix records the check.
- The MIT grant still covers original work only. It does not extend to the supplied PLTechnical Vale rules (ADR-4, ADR-5), to any institutional marks or fonts, or to third-party dependencies, and neither package bundles any of those today.
- If a package ever needs different terms — a font licence, for example — that becomes a new ADR, not a local edit.
