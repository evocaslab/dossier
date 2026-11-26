"""`boundaries`: the layering rules the repo declares hold.

Runs the repo's boundary tool and reports its result:

- `boundaries: {cmd: [...]}` in `dossier.yaml` (any tool: dependency-cruiser, a crate-graph test, a script);
- else import-linter (`lint-imports`) when `.importlinter` or `[tool.importlinter]` in `pyproject.toml`
  exists.

No rules declared, or the tool not installed, is `unknown`. It cannot check that the rules match
ARCHITECTURE.md.
"""

import shutil
import subprocess
import tomllib
from pathlib import Path

from dossier import config
from dossier.model import Result
from dossier.util import fail, ok, unknown

NAME = "boundaries"
TIMEOUT_S = 300
_TAIL_LINES = 3


def _import_linter(root: Path) -> bool:
    if (root / ".importlinter").is_file():
        return True
    py = root / "pyproject.toml"
    if py.is_file():
        return "importlinter" in tomllib.loads(py.read_text(encoding="utf-8")).get("tool", {})
    return False


def command(root: Path) -> tuple[str, ...] | None:
    """Return the boundary command for this repo, or None when none is declared."""
    try:
        declared = config.load(root).boundaries
    except config.ConfigError:
        declared = ()
    if declared:
        return declared
    if _import_linter(root):
        return ("lint-imports",)
    return None


def check(root: Path) -> Result:
    """Check that the declared boundary tool passes."""
    cmd = command(root)
    if cmd is None:
        return unknown(
            NAME, "no boundary rules: add `boundaries: {cmd: [...]}` to dossier.yaml or import-linter"
        )
    exe = shutil.which(cmd[0])
    if exe is None:
        return unknown(NAME, f"{cmd[0]} not installed")
    try:
        run = subprocess.run(  # noqa: S603 - argv from the repo's own config, no shell
            [exe, *cmd[1:]], cwd=root, capture_output=True, text=True, timeout=TIMEOUT_S, check=False
        )
    except subprocess.TimeoutExpired:
        return unknown(NAME, f"{' '.join(cmd)} timed out after {TIMEOUT_S} s")
    if run.returncode != 0:
        tail = " | ".join((run.stdout + run.stderr).strip().splitlines()[-_TAIL_LINES:])
        return fail(NAME, f"{' '.join(cmd)} exited {run.returncode}: {tail}")
    return ok(NAME, f"{' '.join(cmd)} passed")
