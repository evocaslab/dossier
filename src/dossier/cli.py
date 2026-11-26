"""Typer entry point: `dossier check [NAME] [--root DIR] [--json]`."""

import json
from pathlib import Path
from typing import Annotated

import typer

from dossier import NAME, PACKAGE, __version__, config, scaffold
from dossier.checks import CHECKS
from dossier.model import Result, exit_code

JSON_SCHEMA_VERSION = 1
app = typer.Typer(no_args_is_help=True, add_completion=False, help="Check that a repo carries its dossier.")


def _version(value: bool) -> None:  # noqa: FBT001
    if value:
        typer.echo(
            f"{NAME} {__version__} ({PACKAGE}; {config.FILE_NAME} schema {config.SCHEMA}, "
            f"json schema {JSON_SCHEMA_VERSION})"
        )
        raise typer.Exit


@app.callback()
def main(
    *,
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=_version, is_eager=True, help="Print name, version, package and schemas."
        ),
    ] = False,
) -> None:
    """Check that a repo carries its dossier."""
    _ = version


def _render_json(root: Path, results: list[Result], code: int) -> str:
    return json.dumps(
        {
            "schema_version": JSON_SCHEMA_VERSION,
            "tool": NAME,
            "version": __version__,
            "root": str(root),
            "exit_code": code,
            "results": [{"check": r.check, "status": r.status.value, "message": r.message} for r in results],
        },
        indent=2,
    )


@app.command()
def check(
    name: Annotated[
        str | None, typer.Argument(help=f"One check ({', '.join(CHECKS)}); default: all.")
    ] = None,
    *,
    root: Annotated[Path, typer.Option(exists=True, file_okay=False, help="Repo root.")] = Path(),
    as_json: Annotated[bool, typer.Option("--json", help="Machine-readable output.")] = False,
) -> None:
    """Run the checks: one line each (ok, fail, unknown). Exit 0 all ok, 1 a fail, 2 an unknown."""
    if name is not None and name not in CHECKS:
        msg = f"unknown check '{name}'; choose from {', '.join(CHECKS)}"
        raise typer.BadParameter(msg, param_hint="NAME")
    selected = [name] if name else list(CHECKS)
    root = root.resolve()
    results = [CHECKS[n](root) for n in selected]
    code = exit_code(results)
    if as_json:
        typer.echo(_render_json(root, results, code))
    else:
        for r in results:
            typer.echo(r.line())
    raise typer.Exit(code)


@app.command()
def new(  # noqa: PLR0913 (one keyword per CLI option)
    part: Annotated[
        str, typer.Argument(help=f"Part to write: {', '.join(scaffold.PARTS)}.", show_default=False)
    ],
    *,
    root: Annotated[Path, typer.Option(exists=True, file_okay=False, help="Repo root.")] = Path(),
    slug: Annotated[
        str, typer.Option(help="Slug of a new decision record (part reasoning).")
    ] = "first-decision",
    force: Annotated[bool, typer.Option(help="Overwrite files that exist.")] = False,
    dry_run: Annotated[bool, typer.Option(help="Print what would be written; write nothing.")] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Machine-readable output.")] = False,
) -> None:
    """Write the template files of a part. Exit 0 all written, 1 a file existed (kept), 2 bad usage."""
    if part in scaffold.NOT_TEMPLATED:
        msg = f"{part}: {scaffold.NOT_TEMPLATED[part]}"
        raise typer.BadParameter(msg, param_hint="PART")
    if part not in scaffold.PARTS:
        msg = f"unknown part '{part}'; choose from {', '.join(scaffold.PARTS)}"
        raise typer.BadParameter(msg, param_hint="PART")
    results = scaffold.write(part, root, slug=slug, force=force, dry_run=dry_run)
    code = 0 if all(r.written for r in results) else 1
    done = "would write" if dry_run else "wrote"
    if as_json:
        typer.echo(
            json.dumps(
                {
                    "schema_version": JSON_SCHEMA_VERSION,
                    "tool": NAME,
                    "version": __version__,
                    "part": part,
                    "dry_run": dry_run,
                    "exit_code": code,
                    "files": [
                        {"path": str(r.path), "action": done if r.written else "kept"} for r in results
                    ],
                },
                indent=2,
            )
        )
    else:
        for r in results:
            typer.echo(f"{done} {r.path}" if r.written else f"exists {r.path} (kept; --force)")
    raise typer.Exit(code)


AGENT_HELP = """\
dossier {version}: check that a repo carries the documents that explain it. No LLM, no network.

COMMANDS
  dossier check [NAME] [--root DIR] [--json]
      Run all checks, or one: {checks}.
      One line per check: "<status> <check>: <message>", status ok | fail | unknown.
  dossier new PART [--root DIR] [--slug SLUG] [--force] [--dry-run] [--json]
      Write the templates of a part: {parts}.
      Keeps an existing file unless --force. --dry-run writes nothing. --slug names a decision record.
  dossier agent-help
      This page.
  dossier --version
      Name, version, package and schema versions.

EXIT CODES
  check: 0 all ok; 1 a check failed; 2 a check could not tell (unknown is never a pass) or bad usage.
  new:   0 all written; 1 a file existed and was kept; 2 bad usage (unknown part, identity).

JSON (schema_version {schema})
  check --json: {{"schema_version", "tool", "version", "root", "exit_code",
                 "results": [{{"check", "status", "message"}}]}}
  new --json:   {{"schema_version", "tool", "version", "part", "dry_run", "exit_code",
                 "files": [{{"path", "action": "wrote" | "would write" | "kept"}}]}}

INPUT
  dossier.yaml (schema {config_schema}): schema, kind (cli | library | web | service),
  parts (each: present: [paths] or exempt: reason),
  optional generated: [{{path, cmd}}] and boundaries: {{cmd}}.
  Commands are argv lists, run without a shell in the repo root, with a timeout;
  a command that is not installed gives unknown.

NOTES
  Files are read as data. Checking a repo runs only the commands that repo declares.
"""


@app.command("agent-help")
def agent_help() -> None:
    """Print a plain-text page for AI agents: commands, flags, exit codes, JSON shape."""
    typer.echo(
        AGENT_HELP.format(
            version=__version__,
            checks=", ".join(CHECKS),
            parts=", ".join(scaffold.PARTS),
            schema=JSON_SCHEMA_VERSION,
            config_schema=config.SCHEMA,
        ),
        nl=False,
    )
