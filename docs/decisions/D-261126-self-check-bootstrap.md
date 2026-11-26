---
id: D-261126-self-check-bootstrap
status: accepted
date: 2026-11-26
reopen_when: v0.1.0 is tagged and published; then CI switches to the previous release as the gating self-check
---

# The repo checks itself from its own tree until the first release

## Context

The HQ practice `tool-pins-and-toolsets.md` (rule 3) says a tool checks itself with its previous release, and the
candidate's own check is required on the release tag. dossier has no release yet, so there is nothing to pin (rule 9,
bootstrap). Item: HQ backlog B-261124-dossier-own-dossier.

## Drivers

- The repo passes its own check from the first commit.
- No pin on an unreleased SHA.

## Considered options

| Option | Fits the drivers | Cost | Hard to undo | Evidence |
| --- | --- | --- | --- | --- |
| **`uv run dossier check` from the tree in CI and on the tag, until v0.1.0 exists** (chosen) | yes | a bug can hide itself until the next release | no | `.github/workflows/ci.yml` |
| Pin a commit SHA of main as "previous" | no: rule 1 forbids unreleased pins | none | no | `tool-pins-and-toolsets.md` |
| No self-check until a release | no | none | no | - |

## Decision

In the context of a tool with no release, facing the need to gate on itself, we chose the tree's own check over an
unreleased pin, to keep rule 1, accepting one bootstrap round without the previous-release gate.

## Consequences

- Good: the dossier is checked from the start.
- Bad: until v0.1.0 a broken check can pass its own repo; review covers it.

## Confirmation

The `dossier check` step in `.github/workflows/ci.yml` and `release.yml`.

## Sources

- HQ practice `tool-pins-and-toolsets.md`, read 2026-11-26
