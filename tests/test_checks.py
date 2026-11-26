import datetime as dt
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from dossier import PACKAGE, __version__, freshness, scaffold
from dossier.checks import CHECKS
from dossier.cli import app
from dossier.model import Result, Status, exit_code

FIXTURES = Path(__file__).parent / "fixtures"
PINNED_TODAY = dt.date(2026, 11, 25)
runner = CliRunner()


@pytest.fixture(autouse=True)
def _pin_today(monkeypatch: pytest.MonkeyPatch) -> None:
    for module in (freshness, scaffold):
        monkeypatch.setattr(module, "today", lambda: PINNED_TODAY)


@pytest.mark.parametrize("name", sorted(CHECKS))
def test_pass_fixture_is_ok(name: str) -> None:
    assert CHECKS[name](FIXTURES / name / "pass").status is Status.OK


@pytest.mark.parametrize("name", sorted(CHECKS))
def test_fail_fixture_fails(name: str) -> None:
    assert CHECKS[name](FIXTURES / name / "fail").status is Status.FAIL


def test_links_fail_names_both_problems() -> None:
    msg = CHECKS["links"](FIXTURES / "links" / "fail").message
    assert "file not found" in msg
    assert "heading not found" in msg


def test_dossier_fail_names_missing_part_path_and_reason() -> None:
    msg = CHECKS["dossier"](FIXTURES / "dossier" / "fail").message
    assert "WHY.md not found" in msg or "exempt" in msg


def test_links_without_markdown_is_unknown(tmp_path: Path) -> None:
    assert CHECKS["links"](tmp_path).status is Status.UNKNOWN


def test_dossier_without_file_fails(tmp_path: Path) -> None:
    assert CHECKS["dossier"](tmp_path).status is Status.FAIL


def test_exit_code_unknown_is_not_a_pass() -> None:
    assert exit_code([Result("a", Status.OK, ""), Result("b", Status.UNKNOWN, "")]) == 2
    assert exit_code([Result("a", Status.UNKNOWN, ""), Result("b", Status.FAIL, "")]) == 1
    assert exit_code([Result("a", Status.OK, "")]) == 0
    assert exit_code([]) == 2


def test_version_prints_name_version_package_schema() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() == f"dossier {__version__} ({PACKAGE}; dossier.yaml schema 1, json schema 1)"


def test_cli_pass_exit_0_one_line_per_check() -> None:
    root = FIXTURES / "dossier" / "pass"
    result = runner.invoke(app, ["check", "dossier", "--root", str(root)])
    assert result.exit_code == 0
    assert result.output.startswith("ok")
    assert len(result.output.strip().splitlines()) == 1


def test_cli_fail_exit_1() -> None:
    result = runner.invoke(app, ["check", "links", "--root", str(FIXTURES / "links" / "fail")])
    assert result.exit_code == 1


def test_cli_unknown_exit_2(tmp_path: Path) -> None:
    result = runner.invoke(app, ["check", "links", "--root", str(tmp_path)])
    assert result.exit_code == 2
    assert result.output.startswith("unknown")


def test_cli_bad_check_name_exit_2() -> None:
    assert runner.invoke(app, ["check", "nope"]).exit_code == 2


def test_cli_json() -> None:
    result = runner.invoke(
        app, ["check", "front-door", "--json", "--root", str(FIXTURES / "front-door" / "pass")]
    )
    data = json.loads(result.output)
    assert data["schema_version"] == 1
    assert data["results"][0] == {
        "check": "front-door",
        "status": "ok",
        "message": data["results"][0]["message"],
    }
    assert data["exit_code"] == 0


def test_check_all_runs_every_check(tmp_path: Path) -> None:
    result = runner.invoke(app, ["check", "--root", str(tmp_path)])
    assert len(result.output.strip().splitlines()) == len(CHECKS)
    assert result.exit_code == 1
