# Architecture of dossier

Reviewed against the code on 2026-11-26.

## Context

A maintainer, a CI job or a commit hook runs `dossier check` in a repo. dossier reads files under the repo root and,
only when the repo's `dossier.yaml` or `pyproject.toml` declares one, runs a command there (`generated:` renderers,
the `boundaries` tool). It writes nothing during a check; `dossier new` writes template files.

## Containers

One Python package, `src/dossier/`, in layers (import-linter enforces them, `[tool.importlinter]` in `pyproject.toml`):

| Layer | Modules | Role |
| --- | --- | --- |
| entry | `cli.py`, `__main__.py` | Typer commands `check` and `new`, text and `--json` output, exit codes |
| registry | `checks.py`, `scaffold.py` | `CHECKS` maps a name to a check; `scaffold` writes templates from `templates/` |
| checks | `decisions.py`, `stories.py`, `freshness.py`, `contracts.py`, `boundaries.py` | one check each, `check(root) -> Result` |
| base | `config.py`, `util.py` | `dossier.yaml` reader; result helpers, fences, headings, front matter, dates |
| model | `model.py` | `Result`, `Status`, the exit code rule |

`front-door`, `links` and `dossier` live in `checks.py` itself.

## Invariants

- A check never writes and never uses the network ([D-261124-deterministic-checks](docs/decisions/D-261124-deterministic-checks.md)).
- A missing input or tool gives `unknown`; `unknown` exits 2 and is never a pass.
- Commands come only from the repo's own files, as argv lists with no shell, with a timeout.

## Where to start reading

- `src/dossier/checks.py`: the list of checks and the three first ones.
- `src/dossier/model.py`: what a result line is and how the exit code is chosen.
- `tests/fixtures/<check>/{pass,fail}`: one small repo per outcome.
