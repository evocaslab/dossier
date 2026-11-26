# User stories: demo

Reviewed against the code on 2026-11-20.

## Index

| Id | Goal | Actor | Status |
| --- | --- | --- | --- |
| US-1 | Greet the user | a user | built |

## US-1: Greet the user

```yaml
schema: 1
id: US-1
actor: a user
goal: be greeted
why: so that it feels friendly
status: built
accept:
  - gwt: Given the tool, when it runs, then it prints hello.
    test: test_missing
proof:
  cmd: demo hello
```

## US-2: Say goodbye

```yaml
schema: 1
id: US-2
actor: a user
goal: be sent off
status: planned
accept:
  - gwt: Given the tool, when it ends, then it prints bye.
```

## Retired

- US-2: 2026-11-01, dropped
