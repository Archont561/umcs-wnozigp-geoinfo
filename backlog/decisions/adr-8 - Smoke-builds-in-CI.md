---
id: ADR-8
status: accepted
date: 2026-11-21
---

# ADR-8: Compile both dummy mains in CI

## Context

`pixi run check` is a static gate: structure, TOML, Tasknest discovery, generated docs, rumdl, Vale, chktex, and typstyle. It compiles nothing. The dummy mains were therefore only ever proven to compile by a manual local `test-smoke`, so a main that stopped compiling would still merge with a green check.

A local smoke run also turned out to be environment-dependent: Tectonic fetches its TeX bundle from `relay.fullyjustified.net` on first use, which a network-restricted workspace may not reach, leaving the LaTeX main unverified even when the source is fine.

## Decision

1. Add a `smoke` job to `.github/workflows/ci.yml`, triggered on the same events as `check`, running `pixi run --locked test-smoke`.
2. Keep it a separate job rather than a `check` dependency, preserving ADR-6 point 4: the aggregate gate stays fast and free of third-party downloads.
3. Let the GitHub-hosted runner supply the network that Tectonic needs. Do not vendor a TeX bundle into the sandbox pack or the repository for this purpose.
4. Treat a failing `smoke` job as a blocking check on pull requests, alongside `check`.

## Consequences

- Both dummy mains are compiled on every push to `main` and every pull request; a broken main fails CI instead of merging unnoticed.
- The first run after a lockfile change re-downloads the Tectonic bundle and is slower; the job carries a 25-minute timeout for that.
- The job proves the build pipeline only. It does not establish font compliance, visual equivalence, engine/editor compatibility, or academic correctness, and neither job publishes a PDF.
- A workspace that cannot reach the Tectonic relay still cannot compile the LaTeX main locally; CI is now the authority for that claim.
