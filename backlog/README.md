# Backlog

Backlog.md is the execution tracker and document registry. Normative product requirements are Backlog document entries under `docs/`; decisions live in `decisions/`. Milestones group task IDs and state phase goals, not dates or release commitments. ADR-1 and ADR-4 describe the original scaffold layout; the current specification and Vale-rule locations are `docs/` and root `.vale/styles/`, respectively. ADR-5 records the prior default against inferred publication; the explicitly requested `v*` workflow now publishes only source archives and does not resolve license or approval gates.

- `docs/` — draft specifications and the specification index; manage entries with `backlog doc` commands.
- `milestones/` — grouped delivery phases.
- `tasks/` — individual work items with acceptance criteria and dependencies.
- `decisions/` — accepted or proposed durable choices.

List tasks with `pixi run --locked backlog-list` and documents with `pixi run --locked bunx --no-install backlog doc list --plain` after installing the root environment. Keep milestone membership explicit in each milestone page and in the related task description. Do not mark an implementation task complete merely because a dummy main compiles.
