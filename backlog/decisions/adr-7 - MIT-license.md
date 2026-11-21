---
id: ADR-7
status: accepted
date: 2026-11-21
---

# ADR-7: License the repository under MIT

## Context

ADR-5 deliberately left the repository without a license until the owner chose one. The owner has now selected the MIT license for the repository's own code and documentation.

## Decision

1. Add a root `LICENSE` file containing the MIT license text, with the copyright holder `Archont561` and the year 2026.
2. Apply MIT to the tools, tests, specifications, and scaffolding authored for this repository.
3. Keep the licensing of third-party material separate. The supplied PLTechnical Vale preset was distributed without a license file, so MIT does not relicense it; ADR-4's redistribution gate stays in force.
4. Do not infer license identifiers for external dependencies, fonts, institution logos, or student work. Continue to record provenance for those assets.

## Consequences

- Every file in this repository that is original work is MIT-licensed unless a file or directory states otherwise.
- `LICENSE` does not resolve the Vale preset's redistribution terms, package registry ownership, or release approval; TASK-3 and SPEC-QA's release gates remain partly open.
- The release workflow may now ship a `LICENSE` alongside the source archives, but it still does not establish institutional approval or template readiness.
