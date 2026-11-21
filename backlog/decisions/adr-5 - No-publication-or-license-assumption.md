---
id: ADR-5
status: accepted
date: 2026-11-09
---

> **Partially superseded by [ADR-7](adr-7%20-%20MIT-license.md).** Point 3's licensing question is decided: the repository's own work is MIT-licensed. The publication, registry, and third-party-reuse boundaries below still apply.

# ADR-5: Keep publication disabled and licensing unresolved

## Context

The repository currently contains dummy mains, draft specifications, and user-supplied editorial rules. No license choice, package owner/contact, destination account, asset-provenance review, or release approval was supplied for this repository.

## Decision

1. Do not add a license identifier, CTAN or Typst registry manifest, release workflow, credentials, or publisher by inference.
2. Keep the current GitHub repository as a source workspace only; do not push generated artifacts or create releases without explicit instruction.
3. Require a separate decision for software license and third-party preset reuse before any public package offering.
4. Keep TASK-13 open until channels, ownership, rights, versioning, immutable artifacts, and human approval gates are resolved.

## Consequences

- No `LICENSE` file was present at the time of this decision. ADR-7 later added an MIT license for original repository work only.
- The public repository scaffold remains non-releasing; all PDFs and test outputs stay in ignored `dist/`.
