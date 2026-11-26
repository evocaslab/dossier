# User stories: dossier

Reviewed against the code on 2026-11-26.

One entry per goal a person or agent reaches with dossier, the Given/When/Then lines that confirm it, and the test
and command that prove it. Status: `built` (every line names a test that exists), `partial`, `planned`, `gap`.

## Index

| Id | Goal | Actor | Status |
| --- | --- | --- | --- |
| US-1 | see which dossier parts fail | maintainer | built |
| US-2 | read the results in a script | CI job or agent | built |
| US-3 | start the missing files | maintainer of a new repo | built |
| US-4 | know the version and schemas | consumer pinning the tool | built |
| US-5 | run it as a hook or an Action | consumer repo | partial |

## US-1: see which dossier parts fail

```yaml
schema: 1
id: US-1
actor: maintainer
goal: see which dossier parts fail
why: so that a gap is fixed before it is merged
status: built
accept:
  - gwt: Given a repo whose parts all pass, when dossier check runs, then it prints one line per check and exits 0.
    test: test_cli_pass_exit_0_one_line_per_check
  - gwt: Given a repo with a failing part, when dossier check runs, then it exits 1.
    test: test_cli_fail_exit_1
  - gwt: Given a check that cannot tell, when dossier check runs, then it says unknown and exits 2.
    test: test_cli_unknown_exit_2
proof:
  cmd: uv run dossier check
```

## US-2: read the results in a script

```yaml
schema: 1
id: US-2
actor: CI job or agent
goal: read the results in a script
why: so that a dashboard or a bot can act on each line
status: built
accept:
  - gwt: Given any repo, when dossier check --json runs, then it prints the schema version, the tool, the exit code and one result per check.
    test: test_cli_json
proof:
  cmd: uv run dossier check --json
```

## US-3: start the missing files

```yaml
schema: 1
id: US-3
actor: maintainer of a new repo
goal: start the missing files
why: so that the first dossier passes its own checks
status: built
accept:
  - gwt: Given an empty repo, when dossier new runs for a part, then it writes the files, and a second run keeps them and exits 1.
    test: test_new_writes_then_keeps
  - gwt: Given a bare repo, when dossier new runs for every part and then dossier check, then no check fails.
    test: test_runs_in_a_bare_temp_repo
  - gwt: Given the identity part, when dossier new runs, then it refuses with exit 2.
    test: test_new_refuses_untemplated_part
proof:
  cmd: uv run dossier new purpose --root /tmp/demo
```

## US-4: know the version and schemas

```yaml
schema: 1
id: US-4
actor: consumer pinning the tool
goal: know the version and schemas
why: so that a pin and a dossier.yaml can be matched
status: built
accept:
  - gwt: Given the installed tool, when dossier --version runs, then it prints the name, version, package and both schema versions.
    test: test_version_prints_name_version_package_schema
proof:
  cmd: uv run dossier --version
```

## US-5: run it as a hook or an Action

```yaml
schema: 1
id: US-5
actor: consumer repo
goal: run it as a hook or an Action
why: so that the check gates commits and pull requests
status: partial
accept:
  - gwt: Given a repo that lists the dossier hook id, when a commit is made, then dossier check runs and a fail stops the commit.
  - gwt: Given a workflow that uses the Action at a tag's SHA, when it runs, then it fails the job on a fail or an unknown.
proof:
  cmd: prek run dossier --all-files
```

## Retired

None.
