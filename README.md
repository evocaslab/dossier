# dossier

dossier checks that a repo carries the documents that explain it: the README front door, links, the parts listed in
`dossier.yaml`, decision records, user stories, review dates, the changelog and the import rules.

<img src="brand/logo-full-en.svg" alt="dossier: a folder with a check mark" height="64">

- **What.** A command (`dossier check`) that prints one line per check: `ok`, `fail` or `unknown`.
- **Why.** Docs rot without a check. Each rule here is plain text matching, with no LLM and no network, so it runs in
  CI and in a commit hook in seconds. A check that cannot tell says `unknown`, which never passes.
- **How.** Add `dossier.yaml`, run `dossier check`, and use `dossier new <part>` for the files you lack.

Status: `0.1.1`, private until it goes public (see [CHANGELOG.md](CHANGELOG.md)).

## Use

```bash
uvx --from . dossier check            # all checks, one line each: ok / fail / unknown
uvx --from . dossier check links --json
dossier --version                     # name, version, package and schemas
```

Exit 0 all ok, 1 a check failed, 2 a check could not tell (`unknown` is never a pass) or bad usage.

As one self-contained file: copy [standalone/dossier.py](standalone/dossier.py) (pinned to this release's tag) into
any repo and run `uv run --script dossier.py check`.

As a prek or pre-commit hook:

```yaml
- repo: https://github.com/evocaslab/dossier
  rev: v0.1.1
  hooks: [{id: dossier}]
```

As a GitHub Action (pin the tag's commit SHA; the comment names the tag):

```yaml
- uses: evocaslab/dossier@<40-char sha> # v0.1.1
  with:
    check: "" # one check, or empty for all
```

## `dossier.yaml`

```yaml
schema: 1
kind: cli            # cli | library | web | service
parts:               # identity purpose reasoning design contract trust help agents
  purpose:
    present: [README.md, WHY.md]
  identity:
    exempt: no brand yet
```

Optional keys: `generated: [{path, cmd}]` (a file that must equal the command's output) and `boundaries: {cmd}`
(an import-rule tool). Commands are lists of words, run without a shell; a missing tool is `unknown`.

Checks:

- `front-door`: README title and opening sentence.
- `links`: relative links and anchors in README, ARCHITECTURE and `docs/`.
- `dossier`: every part the kind requires is listed with existing paths, or exempt with a reason.
- `decisions`: records in `docs/decisions/` have the front matter, sections and an options table of 2+ rows.
- `stories`: `docs/user-stories.md` has one keyed yaml block per entry, Given/when/then lines, tests that exist
  for `built` entries, an exact Index and no reused retired id.
- `freshness`: "Reviewed against the code on DATE" at most 90 days old; WHY.md `Checked on` dates at most 180.
- `contracts`: CHANGELOG.md names the declared version; `generated:` files equal a fresh render.
- `boundaries`: the declared boundary tool (or import-linter) passes.

## Start the files

```bash
dossier new purpose          # WHY.md; also: dossier reasoning design contract trust help agents
dossier new reasoning --slug pick-a-db
```

Writes templates that pass their own checks; keeps an existing file unless `--force` (exit 1 when one was kept).
`identity` has no template: the brand kit comes from brandforge. `--dry-run` prints what it would write.

## Use with AI agents

The skill [skills/dossier/SKILL.md](skills/dossier/SKILL.md) tells an agent how to run the checks and fill the parts
(minimum tool version 0.1.0). Install it with `npx skills add evocaslab/dossier` once the repo is public; until then,
copy the folder into your agent's skills directory. `dossier agent-help` prints the commands, flags, exit codes and
the `--json` shape (`schema_version` 1) on one plain-text page.

## Docs map

| Part | Where |
| --- | --- |
| Identity | exempt: no brand kit yet |
| Purpose | this README, [WHY.md](WHY.md) |
| Reasoning | [docs/decisions/](docs/decisions/) |
| Design | [ARCHITECTURE.md](ARCHITECTURE.md), [docs/user-stories.md](docs/user-stories.md) |
| Contract | [Use](#use), [CHANGELOG.md](CHANGELOG.md) |
| Trust | [SECURITY.md](SECURITY.md), [LICENSE](LICENSE) |
| Help | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Agents | [AGENTS.md](AGENTS.md), [skills/dossier/SKILL.md](skills/dossier/SKILL.md) |

## Develop

```bash
uv sync && uv run ruff check . && uv run ruff format --check . && uv run pytest && uv run dossier check
```
