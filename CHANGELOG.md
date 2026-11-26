# Changelog

All notable changes. Versions follow semver; one tag `vX.Y.Z` publishes the package, the hook rev and the Action.

## Unreleased

- Brand kit rebuilt with brandforge (hq#218): the mark is an open amber folder with a sheet and a check; masters hold
  light colours and `brand/generated/` holds the dark variants, the adaptive favicon, PNG and ICO icons, avatars,
  tokens, the manifest and the brand book; `brand/images/` holds the social card, hero and banner. `brandforge check
  --strict` passes with no warnings. The README lockup follows the colour scheme. The artwork and the name are all
  rights reserved by EvoCASLab (the code stays MIT).

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
