"""`contracts`: what a user relies on matches the code.

- `CHANGELOG.md` has a `##` heading for the version the package declares (`pyproject.toml`, `Cargo.toml` or
  `package.json`); no version source is `unknown`.
- Every `generated:` entry in `dossier.yaml` (`path` plus `cmd`, a list of words, run without a shell in the
  repo root, 60 s timeout) prints exactly the file's content: a reference page or schema that equals a fresh
  render. A command that is not installed is `unknown`.

It runs only the commands the repo itself declares. It cannot check that the changelog entry describes the
change, or semantic-version breaks (use cargo-semver-checks, oasdiff or api-extractor for those).
"""

import json
import shutil
import subprocess
import tomllib
from pathlib import Path

from dossier import config
from dossier.model import Result
from dossier.util import fail, ok, unknown

NAME = "contracts"
TIMEOUT_S = 60


def declared_version(root: Path) -> tuple[str, str] | None:
    """(version, source file) from the first manifest that has one."""
    py = root / "pyproject.toml"
    if py.is_file():
        version = tomllib.loads(py.read_text(encoding="utf-8")).get("project", {}).get("version")
        if isinstance(version, str):
            return version, py.name
    cargo = root / "Cargo.toml"
    if cargo.is_file():
        data = tomllib.loads(cargo.read_text(encoding="utf-8"))
        version = data.get("package", {}).get("version") or data.get("workspace", {}).get("package", {}).get(
            "version"
        )
        if isinstance(version, str):
            return version, cargo.name
    pkg = root / "package.json"
    if pkg.is_file():
        version = json.loads(pkg.read_text(encoding="utf-8")).get("version")
        if isinstance(version, str):
            return version, pkg.name
    return None


def _changelog(root: Path) -> tuple[list[str], list[str]]:
    """(problems, unknowns) for the changelog."""
    found = declared_version(root)
    if found is None:
        return [], ["no version in pyproject.toml, Cargo.toml or package.json"]
    version, source = found
    log = root / "CHANGELOG.md"
    if not log.is_file():
        return [f"CHANGELOG.md not found (version {version} in {source})"], []
    heads = [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln.startswith("## ")]
    if not any(version in h for h in heads):
        return [f"CHANGELOG.md has no '## ' heading for {version} ({source})"], []
    return [], []


def _generated(root: Path, entries: tuple[config.Generated, ...]) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    unknowns: list[str] = []
    for entry in entries:
        exe = shutil.which(entry.cmd[0], path=None)
        if exe is None:
            unknowns.append(f"{entry.path}: command {entry.cmd[0]} not installed")
            continue
        try:
            run = subprocess.run(  # noqa: S603 - argv from the repo's own dossier.yaml, no shell
                [exe, *entry.cmd[1:]],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_S,
                check=False,
            )
        except subprocess.TimeoutExpired:
            unknowns.append(f"{entry.path}: {' '.join(entry.cmd)} timed out")
            continue
        if run.returncode != 0:
            problems.append(f"{entry.path}: {' '.join(entry.cmd)} exited {run.returncode}")
            continue
        target = root / entry.path
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current is None:
            problems.append(f"{entry.path}: not found (regenerate with {' '.join(entry.cmd)})")
        elif current.rstrip() != run.stdout.rstrip():
            problems.append(f"{entry.path}: differs from {' '.join(entry.cmd)}")
    return problems, unknowns


def check(root: Path) -> Result:
    """Check the changelog names the declared version and generated files equal a fresh render."""
    entries: tuple[config.Generated, ...] = ()
    try:
        entries = config.load(root).generated
    except config.ConfigError as exc:
        if (root / config.FILE_NAME).is_file():
            return fail(NAME, f"{config.FILE_NAME}: {exc}")
    log_problems, log_unknowns = _changelog(root)
    gen_problems, gen_unknowns = _generated(root, entries)
    problems, unknowns = log_problems + gen_problems, log_unknowns + gen_unknowns
    if problems:
        return fail(NAME, "; ".join(problems + unknowns))
    if unknowns:
        return unknown(NAME, "; ".join(unknowns))
    return ok(NAME, f"changelog names the version; {len(entries)} generated file(s) current")
