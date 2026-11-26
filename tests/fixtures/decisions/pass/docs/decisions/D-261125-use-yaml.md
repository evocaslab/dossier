---
id: D-261125-use-yaml
status: accepted
date: 2026-11-25
reopen_when: never
---

# Use YAML for the config

## Context

The tool needs a config file.

## Drivers

- easy to read

## Considered options

| Option | Fits the drivers | Cost | Hard to undo | Evidence |
| --- | --- | --- | --- | --- |
| **YAML** (chosen) | yes | low | no | documented |
| TOML | partly | low | no | guessed |

## Decision

In the context of config, facing readability, we chose YAML over TOML, to achieve comments, accepting indentation.

## Consequences

- Good: readable.

## Confirmation

review only

## Sources

- none
