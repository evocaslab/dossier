import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from dossier import __version__, freshness, scaffold
from dossier.checks import CHECKS
from dossier.cli import app
from dossier.model import Status

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


@pytest.fixture(autouse=True)
def _pin_today(monkeypatch: pytest.MonkeyPatch) -> None:
    for module in (freshness, scaffold):
        monkeypatch.setattr(module, "today", lambda: dt.date(2026, 11, 25))


def _msg(name: str) -> str:
    return CHECKS[name](FIXTURES / name / "fail").message


def test_decisions_fail_names_each_problem() -> None:
    msg = _msg("decisions")
    assert "differs from the file name" in msg
    assert "status 'maybe'" in msg
    assert "fewer than 2 rows" in msg


def test_stories_fail_names_each_problem() -> None:
    msg = _msg("stories")
    assert "test test_missing not found" in msg
    assert "Index differs" in msg
    assert "US-2 is retired but used again" in msg


def test_stories_bad_gwt_and_two_blocks(tmp_path: Path) -> None:
    page = tmp_path / "docs" / "user-stories.md"
    page.parent.mkdir()
    page.write_text(
        "# S\n\n## Index\n\n| Id | Goal |\n| --- | --- |\n| US-1 | g |\n\n## US-1: g\n\n"
        "```yaml\nid: US-1\nactor: a\ngoal: g\nstatus: planned\naccept:\n  - gwt: it works\n```\n\n"
        "```yaml\nid: US-1\n```\n",
        encoding="utf-8",
    )
    assert "2 yaml blocks" in CHECKS["stories"](tmp_path).message
    page.write_text(page.read_text(encoding="utf-8").split("\n\n```yaml\nid: US-1\n```")[0], encoding="utf-8")
    result = CHECKS["stories"](tmp_path)
    assert result.status is Status.FAIL
    assert "not Given / when / then" in result.message


def test_freshness_fail_names_age_and_future() -> None:
    msg = _msg("freshness")
    assert "days old" in msg
    assert "in the future" in msg


def test_contracts_fail_names_changelog_and_stale_file() -> None:
    msg = _msg("contracts")
    assert "no '## ' heading for 1.2.4" in msg
    assert "docs/hello.txt: differs" in msg


@pytest.mark.parametrize("name", ["decisions", "stories", "freshness", "contracts", "boundaries"])
def test_empty_repo_is_unknown(name: str, tmp_path: Path) -> None:
    assert CHECKS[name](tmp_path).status is Status.UNKNOWN


def test_missing_tool_is_unknown(tmp_path: Path) -> None:
    (tmp_path / "dossier.yaml").write_text(
        "schema: 1\nkind: cli\nparts: {}\nboundaries:\n  cmd: [no-such-tool-xyz]\n"
        "generated:\n  - path: a.txt\n    cmd: [no-such-tool-xyz]\n",
        encoding="utf-8",
    )
    assert CHECKS["boundaries"](tmp_path).status is Status.UNKNOWN
    assert CHECKS["contracts"](tmp_path).status is Status.UNKNOWN


@pytest.mark.parametrize("part", sorted(scaffold.PARTS))
def test_new_writes_then_keeps(part: str, tmp_path: Path) -> None:
    first = runner.invoke(app, ["new", part, "--root", str(tmp_path)])
    assert first.exit_code == 0, first.output
    assert first.output.startswith("wrote")
    again = runner.invoke(app, ["new", part, "--root", str(tmp_path)])
    assert again.exit_code == 1
    assert again.output.startswith("exists")
    forced = runner.invoke(app, ["new", part, "--root", str(tmp_path), "--force"])
    assert forced.exit_code == 0


def test_new_reasoning_uses_slug_and_passes(tmp_path: Path) -> None:
    runner.invoke(app, ["new", "reasoning", "--root", str(tmp_path), "--slug", "pick-yaml"])
    assert (tmp_path / "docs" / "decisions" / "D-261125-pick-yaml.md").is_file()
    assert CHECKS["decisions"](tmp_path).status is Status.OK


def test_new_dry_run_writes_nothing_and_json(tmp_path: Path) -> None:
    dry = runner.invoke(app, ["new", "design", "--root", str(tmp_path), "--dry-run", "--json"])
    assert dry.exit_code == 0, dry.output
    data = json.loads(dry.output)
    assert data["schema_version"] == 1
    assert data["dry_run"] is True
    assert [f["action"] for f in data["files"]] == ["would write", "would write"]
    assert not any(tmp_path.iterdir())
    runner.invoke(app, ["new", "design", "--root", str(tmp_path)])
    kept = json.loads(runner.invoke(app, ["new", "design", "--root", str(tmp_path), "--json"]).output)
    assert kept["exit_code"] == 1
    assert {f["action"] for f in kept["files"]} == {"kept"}


def test_agent_help_lists_commands_exit_codes_and_json() -> None:
    result = runner.invoke(app, ["agent-help"])
    assert result.exit_code == 0
    page = result.output
    assert len(page.splitlines()) < 150
    for word in ("dossier check", "dossier new", "EXIT CODES", "schema_version", *CHECKS, *scaffold.PARTS):
        assert word in page


def test_standalone_script_pins_this_version() -> None:
    script = (Path(__file__).parents[1] / "standalone" / "dossier.py").read_text(encoding="utf-8")
    assert f"evocaslab/dossier@v{__version__}" in script


@pytest.mark.parametrize("part", ["identity", "nope"])
def test_new_refuses_untemplated_part(part: str, tmp_path: Path) -> None:
    assert runner.invoke(app, ["new", part, "--root", str(tmp_path)]).exit_code == 2


def test_runs_in_a_bare_temp_repo(tmp_path: Path) -> None:
    """The installed tool, as a subprocess, in a repo with no HQ files: templates pass their own checks."""
    (tmp_path / "README.md").write_text(
        "# demo\n\nDemo is a small tool that prints a greeting for the user.\n", encoding="utf-8"
    )
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.3.0"\n', encoding="utf-8"
    )
    tool = [sys.executable, "-m", "dossier"]
    for part in scaffold.PARTS:
        subprocess.run([*tool, "new", part], cwd=tmp_path, check=True, capture_output=True)  # noqa: S603
    run = subprocess.run(  # noqa: S603
        [*tool, "check", "--json"], cwd=tmp_path, capture_output=True, text=True, check=False
    )
    data = json.loads(run.stdout)
    status = {r["check"]: r["status"] for r in data["results"]}
    assert status.pop("boundaries") == "unknown"
    assert set(status.values()) == {"ok"}, data["results"]
    assert run.returncode == 2
