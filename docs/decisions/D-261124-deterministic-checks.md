---
id: D-261124-deterministic-checks
status: accepted
date: 2026-11-24
reopen_when: a check needs judgment that text matching cannot give and a false pass would be cheap
---

# Checks are deterministic: no LLM, no network, `unknown` never passes

## Context

dossier runs in CI and in commit hooks of many repos (HQ backlog B-261124-dossier-tool-repo, request
R-2611241001-7c25). A check that sometimes passes and sometimes fails on the same tree, or that needs a network or a
model key, would be turned off.

## Drivers

- Same tree, same lines.
- Runs offline and in seconds.
- A gap is never reported as a pass.

## Considered options

| Option | Fits the drivers | Cost | Hard to undo | Evidence |
| --- | --- | --- | --- | --- |
| **Text matching only; run only commands the repo declares; `unknown` when a tool or input is missing** (chosen) | yes | some checks stay shallow | no | `src/dossier/util.py`, `boundaries.py`, `contracts.py` |
| An LLM judges the docs | no: not repeatable, needs a key | per-run cost | no | HQ practice `docs-checks-in-ci.md` |
| Missing tool counts as a pass | no: hides gaps | none | no | - |

## Decision

In the context of a docs check that gates CI, facing flaky or costly judgment, we chose text matching plus the repo's
own declared commands over an LLM judge, to achieve repeatable lines, accepting that content quality stays a review
matter.

## Consequences

- Good: exit codes are stable; the tool runs with no secrets.
- Bad: "is this reason true" and "does this test mean this line" are not checked.

## Confirmation

Tests in `tests/` pin every check's ok, fail and unknown lines; `test_missing_tool_is_unknown`.

## Sources

- HQ practices `docs-checks-in-ci.md` and `repo-dossier.md`, read 2026-11-24
