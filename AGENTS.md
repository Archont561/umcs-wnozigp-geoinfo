<!-- Generated file. Edit templates/AGENTS.md.j2, then run pixi run docs-write. -->

# Agent and maintainer instructions

## Product boundaries

- Treat this repository as a specification-first scaffold. The LaTeX and Typst `main` files are dummy smoke fixtures only.
- Do not imply UMCS endorsement, institutional approval, full compliance, or editor compatibility without verified evidence and an accepted decision.
- Do not add a public package implementation, official logo/seal, or publisher without a scoped task and decision.
- Keep CTAN and Typst registry decisions and author/contact details open until reviewed. The explicitly requested GitHub workflow publishes source-only archives for `v*` tags; do not push such a tag without explicit release authorization and provenance review.

## Specifications and backlog

- `backlog/docs/` is the normative home for product requirements. Maintain stable `SPEC-*` IDs in specification document titles/headings and mark them Draft until reviewed.
- Use the Backlog.md document commands (`backlog doc create`, `backlog doc update`, `backlog doc list`) to manage specification entries; do not edit their metadata files directly.
- Cite primary source, edition/date, section/page, applicability, and confidence for every institutional requirement. Unverified items stay open in SPEC-SOURCE and linked backlog tasks.
- `backlog/milestones/` groups task IDs. Keep dependencies and acceptance criteria on individual task records in `backlog/tasks/`.
- Record durable choices in `backlog/decisions/`. A decision must say what it does not authorize; do not silently infer distribution, third-party licensing, or compliance. The repository's own work is MIT-licensed per ADR-7; that grant does not extend to third-party assets.
- Generated `README.md` and `AGENTS.md` come from `templates/`; edit templates and regenerate via `pixi run docs-write`.

## Vale and writing checks

- Install Vale (`vale==3.26.0`) and rumdl through the root Pixi Conda environment. Use rumdl for Markdown linting via `.rumdl.toml`; do not reintroduce markdownlint-cli2.
- The provided PLTechnical style rules are local under `.vale/styles/`; no network style sync is needed.
- Keep the supplied rules' cautions: suggestions require human review, the sentence threshold is an editorial choice, and unit checking is partial. Vale is not a grammar or compliance oracle.
- Preserve the `.vale.ini` and attribution/specification when changing the rules. The MIT grant does not apply to the preset; keep its redistribution gate until its terms are reviewed.

## Tooling and validation

- Keep a single root Pixi manifest and lock. Do not add package-local environments.
- Keep format-specific tests under `packages/<name>/tests/`; `pixi run --locked test-smoke` runs both package-local BDD tests.
- Use Tasknest for per-format smoke builds and the root build aggregate. Preserve `dist/latex/main.pdf` and `dist/typst/main.pdf` paths.
- Manual builds and `test-smoke` stay outside the root `check` gate. The `v*` GitHub release workflow runs the checks and smoke tests before packaging source archives; it does not publish PDFs.
- Pixi Sandbox is a separate global tool, not a project dependency. Its reviewed bundle plan is `pixi-sandbox.toml` (`default` environment, `linux-64` only), with Pixi pinned to `0.84.1` for the publisher.
- The active `.github/workflows/publish-sandbox.yml` and `scripts/restore.sh` are generated. Keep the relock template at `scripts/relock-workflow.yml.template`, outside `.github/workflows/`; no PR-triggered lock-repair workflow is enabled because Pixi Sandbox 0.9.0 generates it with an incompatible `0.81.0` pin.
- To regenerate/check, preserve these custom paths: `pixi-sandbox init --project-root . --github-workflow-path .github/workflows/publish-sandbox.yml --relock-workflow-path scripts/relock-workflow.yml.template --relock-ci-workflow ci.yml --script-path scripts/restore.sh --config pixi-sandbox.toml` (add `--check` to verify without writing). Also validate with `pixi-sandbox plan --config pixi-sandbox.toml --json`.
- The publisher defaults to read-only permissions; its publish job writes the sandbox branch and its self-update job can open an upgrade PR. Matching manifest/lock pushes to `main` publish the branch; the weekly schedule is a self-update job, not a publish run.
- The generated restore launcher uses `--force` and may register per-user tools; set `PIXI_SANDBOX_USER_TOOLS=skip` when a restore must not modify user PATH.
- `pytest-bdd` verifies only the local smoke-build contract. Do not treat a passing PDF smoke test as visual or institutional validation.
- Run `pixi run --locked check`, package lints, and the relevant manual build after edits; report exactly what passed.
- Do not push commits or tags or create releases without explicit instruction. A matching tag push will trigger the configured GitHub source release.
