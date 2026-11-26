"""`freshness`: dated review lines in the dossier are recent.

Reads README.md, WHY.md, ARCHITECTURE.md and `docs/**/*.md` for:

- "Reviewed against the code on YYYY-MM-DD": fails when older than 90 days;
- the `Checked on` column of WHY.md's Compared with table: fails when a date is older than 180 days;
- any of those dates in the future (a typo).

"Not yet reviewed" is allowed (a new page). No dated line at all is `unknown`. It cannot check that the review
was real or that a generated file matches its generator (`contracts` re-renders declared generated files).
"""

import datetime as dt
import re
from pathlib import Path

from dossier.model import Result
from dossier.util import DATE, fail, ok, parse_date, rel, strip_fences, today, unknown

NAME = "freshness"
REVIEW_DAYS = 90
CHECKED_DAYS = 180
_REVIEWED = re.compile(r"Reviewed against the code on (\d{4}-\d{2}-\d{2})")


def _files(root: Path) -> list[Path]:
    files = [root / n for n in ("README.md", "WHY.md", "ARCHITECTURE.md") if (root / n).is_file()]
    if (root / "docs").is_dir():
        files.extend(sorted((root / "docs").rglob("*.md")))
    return files


def _checked_on_dates(lines: list[str]) -> list[str]:
    """Dates in the `Checked on` column of the first table that has one."""
    col: int | None = None
    out: list[str] = []
    for line in lines:
        if not line.lstrip().startswith("|"):
            if col is not None and out:
                break
            col = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if col is None:
            col = next((i for i, c in enumerate(cells) if c.lower() == "checked on"), None)
            continue
        if col < len(cells):
            out.extend(DATE.findall(cells[col]))
    return out


def _age_problem(where: str, text: str, limit: int, now: dt.date) -> str:
    date = parse_date(text)
    if date is None:
        return f"{where}: {text} is not a date"
    if date > now:
        return f"{where}: {text} is in the future"
    age = (now - date).days
    if age > limit:
        return f"{where}: {text} is {age} days old (limit {limit})"
    return ""


def check(root: Path) -> Result:
    """Review dates under 90 days, `Checked on` dates under 180 days."""
    now = today()
    problems: list[str] = []
    seen = 0
    for path in _files(root):
        text = path.read_text(encoding="utf-8")
        name = rel(root, path)
        for found in _REVIEWED.findall(text):
            seen += 1
            problems.append(_age_problem(f"{name} reviewed", found, REVIEW_DAYS, now))
        if path.name == "WHY.md":
            for found in _checked_on_dates(strip_fences(text)):
                seen += 1
                problems.append(_age_problem(f"{name} checked on", found, CHECKED_DAYS, now))
    problems = [p for p in problems if p]
    if not seen:
        return unknown(NAME, "no 'Reviewed against the code on' or 'Checked on' dates found")
    if problems:
        return fail(NAME, f"{len(problems)} stale: " + "; ".join(problems))
    return ok(NAME, f"{seen} dated line(s) are recent")
