# Security policy

## Supported versions

Only the latest release gets fixes.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting on this repository ("Security" tab, "Report a vulnerability"). Do not
open a public issue. Expect a first answer within 7 days.

## What dossier runs

`dossier check` reads files and runs only the commands the checked repo itself declares (`generated:` and
`boundaries:` in `dossier.yaml`, or `lint-imports` when import-linter is configured), as argument lists with no shell
and with a timeout. Checking an untrusted repo therefore runs that repo's declared commands: treat it like running
its tests.
