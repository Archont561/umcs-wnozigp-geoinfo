---
id: ADR-6
status: accepted
date: 2026-11-09
---

# ADR-6: Use one root Pixi environment and Tasknest task graph

## Context

The repository needs Vale from Conda, two format smoke builds, and generated documentation without duplicating developer environments.

## Decision

1. Maintain one root `pixi.toml` and `pixi.lock` for Conda, PyPI, and repository tools.
2. Install Vale from Conda in that root environment; keep PLTechnical style files in the repository.
3. Use one Tasknest build tool per format and a root aggregate depending on both.
4. Keep smoke builds and pytest-bdd build scenarios opt-in and outside the root `check` gate; CI runs them in a separate `smoke` job so the aggregate gate stays fast and network-light (see ADR-8).
5. Keep user-facing template tests distinct from scaffold smoke tests. The latter only test the build pipeline.

## Consequences

- Use `pixi run --locked build-latex`, `build-typst`, and `build` from the repository root.
- Use `pixi run --locked lint-vale` to apply the local preset with the Conda-provisioned Vale executable.
- A first Tectonic run may download TeX resources; an offline build claim requires separate evidence.
