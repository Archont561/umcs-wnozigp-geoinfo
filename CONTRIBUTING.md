# Contributing to the scaffold

This repository is specification-first. The `main.tex` and `main.typ` files are dummy smoke fixtures, not template implementations. Before adding behavior, update the relevant specification document entry under `backlog/docs/`, create or update a Backlog.md task, and record durable decisions in an ADR.

## Setup

Requires Pixi `0.84.1` in the manifest range and network access for first-time package provisioning. Vale and rumdl are installed by Pixi from Conda; the PLTechnical Vale rules are already local in this repository.

```sh
pixi install --locked
pixi run --locked bun-install
pixi run --locked check
```

## Checks and builds

```sh
pixi run --locked lint-markdown
pixi run --locked lint-vale
pixi run --locked lint-latex
pixi run --locked lint-typst
pixi run --locked test-smoke
```

Format-specific pytest-bdd tests live under `packages/latex/tests/` and `packages/typst/tests/`. `test-smoke` runs both tests; each invokes its package-specific Tasknest build and validates that format's dummy PDF. CI runs it in a separate `smoke` job next to the static `check` job, so a dummy main that stops compiling fails the pull request. A first Tectonic build downloads its bundle and is the slow run. To build each format directly:

```sh
pixi run --locked build-latex
pixi run --locked build-typst
```

The LaTeX smoke build uses Tectonic. It may download TeX resources the first time. The smoke PDFs are local verification artifacts under ignored `dist/`; they are not package releases.

The GitHub workflow at `.github/workflows/release.yml` runs on `v*` tags, verifies the repository and both package smoke tests, then attaches separate source archives for `packages/latex/` and `packages/typst/` with a `SHA256SUMS` manifest. Pushing a matching tag publishes a GitHub Release. The workflow does not establish third-party provenance or institutional approval; review those release gates, and confirm the MIT grant holds for every shipped file, before pushing a tag.

## Pixi sandbox

The `pixi-sandbox.toml` plan packages the root `default` environment for `linux-64` into `sandbox/developer-linux-64`. The globally installed `pixi-sandbox` CLI (0.9.0 from Prefix channel `archont561/archont561`) is separate from the project's locked environment.

- `.github/workflows/publish-sandbox.yml` publishes on matching manifest/lock changes to `main` or a manual dispatch with `upgrade` left blank. The weekly schedule runs the Pixi Sandbox self-update job; it does not publish a transport branch. Permissions are read-only by default; the publish job writes the branch, while the self-update job has the write scopes needed to open an upgrade PR.
- No lock-repair workflow is active. Pixi Sandbox 0.9.0 generates one pinned to Pixi 0.81.0, incompatible with this project's `requires-pixi`; its generator template is kept at `scripts/relock-workflow.yml.template`, outside `.github/workflows/`.
- `scripts/restore.sh` fetches and restores the branch into the current checkout.

Check the config and generated files with:

```sh
pixi-sandbox init --project-root . --github-workflow-path .github/workflows/publish-sandbox.yml --relock-workflow-path scripts/relock-workflow.yml.template --relock-ci-workflow ci.yml --script-path scripts/restore.sh --config pixi-sandbox.toml --check
pixi-sandbox plan --config pixi-sandbox.toml --json
```

Use the same `init` arguments without `--check` to regenerate generator-owned files. The restore launcher uses `--force` and may register user-level Pixi tools; set `PIXI_SANDBOX_USER_TOOLS=skip` to avoid user PATH changes. The first restore fetch requires access to `origin`.

## Specification and backlog workflow

1. List existing specification entries with `pixi run --locked bunx --no-install backlog doc list --plain`; search before creating a duplicate.

2. Use `backlog doc create "<title>" --type specification` or `backlog doc update <doc-id>` to add or revise a specification. Keep its stable `SPEC-*` ID in the document title/heading, state assumptions and evidence, and leave unresolved requirements marked Draft. Use the Backlog.md CLI rather than editing document metadata files directly.

3. Add a task under `backlog/tasks/` with dependencies and testable acceptance criteria.

4. Add the task ID to the appropriate `backlog/milestones/` page.

5. Record a durable choice under `backlog/decisions/` when one is made. Do not decide publication or third-party licensing by implication; original repository work is MIT-licensed per ADR-7 and mirrored in each package per ADR-14, and that grant does not extend to supplied or third-party assets.

6. Regenerate root overview documents after changing their templates:

   ```sh
   pixi run --locked docs-write
   pixi run --locked docs-check
   ```

The selected 2025/26 source is only a starting point. Verify the version applicable to the target student cohort before encoding a rule. Smoke tests, Vale findings, or draft specifications do not establish institutional compliance.
