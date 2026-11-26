"""Helpers shared by the checks: results, Markdown fences and headings, front matter, dates."""

import datetime as dt
import re
from pathlib import Path

import yaml

from dossier.model import Result, Status

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def ok(check: str, message: str) -> Result:
    """Return an `ok` line."""
    return Result(check, Status.OK, message)


def fail(check: str, message: str) -> Result:
    """Return a `fail` line."""
    return Result(check, Status.FAIL, message)


def unknown(check: str, message: str) -> Result:
    """Return an `unknown` line: the check could not tell; never a pass."""
    return Result(check, Status.UNKNOWN, message)


def today() -> dt.date:
    """Today's date in UTC; tests pin it."""
    return dt.datetime.now(dt.UTC).date()


def parse_date(text: str) -> dt.date | None:
    """Parse a `YYYY-MM-DD` date; None when it is not a real date."""
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        return None


def strip_fences(text: str) -> list[str]:
    """Lines of `text` outside fenced code blocks."""
    out: list[str] = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced:
            out.append(line)
    return out


def front_matter(text: str) -> tuple[dict[str, object] | None, str]:
    """Split a `---` YAML front matter block from the body; None when absent or not a mapping."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:i]))
            except yaml.YAMLError:
                return None, text
            body = "\n".join(lines[i + 1 :])
            return (data if isinstance(data, dict) else None), body
    return None, text


def headings(text: str, level: int) -> list[str]:
    """Titles of the headings of exactly `level` outside fences, in order."""
    out: list[str] = []
    for line in strip_fences(text):
        m = HEADING.match(line)
        if m and len(m.group(1)) == level:
            out.append(m.group(2))
    return out


def sections(text: str, level: int) -> list[tuple[str, str]]:
    """(title, body) per heading of `level`; a body runs to the next heading of that level or higher."""
    out: list[tuple[str, list[str]]] = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
        m = None if fenced else HEADING.match(line)
        if m and len(m.group(1)) <= level:
            if len(m.group(1)) == level:
                out.append((m.group(2), []))
            else:
                out.append(("", []))
            continue
        if out:
            out[-1][1].append(line)
    return [(title, "\n".join(body)) for title, body in out if title]


def rel(root: Path, path: Path) -> str:
    """`path` relative to `root`, for messages."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
