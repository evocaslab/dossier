# Changelog

All notable changes. Versions follow semver; one tag `vX.Y.Z` publishes the package, the hook rev and the Action.

## 0.1.1 - 2026-11-26

Ready to go public; no change to the checks.

- Brand kit (`brand/`, `BRAND.md`): folder-with-check mark, lockups, favicon, colours; the dossier's identity part
  points to it.
- `pyproject.toml` declares the license (`MIT`, `LICENSE`).
- The boundaries command runs through uv (`uv run --frozen lint-imports`), so a global `dossier` install can check this
  repo too.
- `just q-bulwark`: the bulwark public-preset scan.

## 0.1.0 - 2026-11-26

Bootstrap release ([D-261126-self-check-bootstrap](docs/decisions/D-261126-self-check-bootstrap.md)).

- `dossier check` with the checks front-door, links, dossier, decisions, stories, freshness, contracts, boundaries;
  text and `--json` output; exit 0 / 1 / 2.
- `dossier new <part>` writes templates that pass their own checks.
- `dossier --version` prints name, version, package and the `dossier.yaml` and JSON schema versions.
- The prek hook id `dossier` and a composite GitHub Action.
