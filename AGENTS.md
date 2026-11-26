# dossier: instructions for AI agents

Python 3.12+ uv project, Typer CLI, package `evocaslab-dossier`, commands `dossier` and `evocaslab-dossier`.

## Gate

```bash
just q-check
```

It runs `uv sync`, ruff (format and lint), basedpyright, pytest and `dossier check`, the same steps as
`.github/workflows/ci.yml`.

Ruff selects `ALL`; fix findings instead of adding ignores. The repo checks itself: `dossier check` must exit 0.

## Rules

- Checks are deterministic: no LLM, no network; a missing tool or input is `unknown`
  ([D-261124-deterministic-checks](docs/decisions/D-261124-deterministic-checks.md)).
- Commands run only when the checked repo declares them, as argv with no shell and a timeout.
- Keep the import layers in `pyproject.toml` (`[tool.importlinter]`); see [ARCHITECTURE.md](ARCHITECTURE.md).
- A new check: follow [CONTRIBUTING.md](CONTRIBUTING.md#adding-a-check).
- A `built` user story names tests that exist; update `docs/user-stories.md` when behaviour changes.
- Every release: bump `version` in `pyproject.toml`, add the `## X.Y.Z - date` heading in `CHANGELOG.md`, tag `vX.Y.Z`.
- Work in a worktree under `.worktrees/`; the backlog for this repo lives in HQ (`evocaslab/hq`, `docs/backlog/`).

## Using the tool in other repos

See [skills/dossier/SKILL.md](skills/dossier/SKILL.md).
