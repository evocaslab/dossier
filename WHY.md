# Why dossier

For maintainers who want a repo's explaining documents to stay present and current, dossier is a CI check that names
each missing or stale part in one line. Unlike a general repo linter, it knows the parts a repo of each kind needs
(purpose, reasoning, design, contract, trust, help, agents) and checks their content form, not only that a file exists.

## Why use it

- One command covers the README front door, links and anchors, decision records, user stories tied to real test
  names, review dates, the changelog version and import rules.
- Deterministic: no LLM and no network, so the same tree gives the same lines, in CI and in a commit hook.
- `unknown` is never a pass: a missing tool or input is named, not hidden.

## When not to use it

- You only need to know that standard files exist (LICENSE, SECURITY.md): OpenSSF Scorecard or a repo template does it.
- You check external URLs: use lychee; dossier checks only relative links.
- Your docs live in a wiki or a docs site outside the repo.

## Compared with

| Alternative | Best at | Pick it instead when | Checked on |
| --- | --- | --- | --- |
| OpenSSF Scorecard | security practices of a repo (branch protection, pinned deps, a security policy, a license), scored 0-10 per check | you need a supply-chain score, not doc content | 2026-11-26: "OpenSSF Scorecard checks list" |
| repolinter (TODO Group) | rule sets for files that must exist, with fixes | you want one existence rule set for many repos; its upkeep is unclear (forks call it archived, a 2025 push is listed) | 2026-11-26: "todogroup repolinter archived" |
| lychee | fast link checks, external URLs included | broken external links are the problem | 2026-11-26: "lychee link checker markdown CI github action" |
| doing it by hand | no new tool | one small repo, reviewed often | 2026-11-26 |

## Decisions

See [docs/decisions/](docs/decisions/).

## Sources

- <https://github.com/ossf/scorecard>, read 2026-11-26
- <https://github.com/todogroup/repolinter>, <https://codeberg.org/damian-buho/repolinter>, read 2026-11-26
- <https://github.com/lycheeverse/lychee>, read 2026-11-26
- HQ practices `repo-dossier.md`, `docs-checks-in-ci.md`, `tool-pins-and-toolsets.md` (evocaslab/hq)
