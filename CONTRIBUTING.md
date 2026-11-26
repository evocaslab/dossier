# Contributing

## Set up and check

```bash
uv sync
uv run ruff check . && uv run ruff format --check . && uv run pytest && uv run dossier check
```

All four must pass; CI runs the same.

## Adding a check

1. A module in `src/dossier/` with `NAME` and `check(root) -> Result`; register it in `CHECKS` (`checks.py`).
2. Fixtures `tests/fixtures/<name>/pass` and `fail`; the parametrized tests pick them up.
3. A missing input or tool returns `unknown`, never `ok`.
4. The repo's own dossier passes the new rule in the same change.
5. A line in `CHANGELOG.md` and the check list in `README.md`.

## Questions

Open an issue. Larger changes: an issue first, then a decision record in `docs/decisions/`.
