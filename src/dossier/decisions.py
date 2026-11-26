"""`decisions`: the records in `docs/decisions/` follow the fixed format.

Checks per record: front matter with `id` equal to the file name, `status` from the fixed set, a real `date`,
`superseded_by` naming an existing record when superseded; the sections Context, Considered options, Decision
and Consequences; a Considered options table with at least two rows. It cannot check whether the reasons are
true.
"""

import re
from pathlib import Path

from dossier.model import Result
from dossier.util import fail, front_matter, ok, parse_date, sections, unknown

NAME = "decisions"
DIR = Path("docs/decisions")
ID = re.compile(r"^(D-\d{6}-[a-z0-9][a-z0-9-]*|\d{4}-[a-z0-9][a-z0-9-]*)$")
STATUSES = ("proposed", "accepted", "rejected", "deprecated", "superseded")
SECTIONS = ("Context", "Considered options", "Decision", "Consequences")
_MIN_OPTIONS = 2


def records(root: Path) -> list[Path]:
    """Record files, the generated README left out."""
    folder = root / DIR
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.md") if p.name.lower() != "readme.md")


def _table_rows(body: str) -> int:
    rows = [ln for ln in body.splitlines() if ln.lstrip().startswith("|")]
    # header and separator lines do not count
    return max(0, len(rows) - 2)


def _check_record(path: Path, ids: set[str]) -> list[str]:
    meta, body = front_matter(path.read_text(encoding="utf-8"))
    if meta is None:
        return ["no YAML front matter"]
    problems: list[str] = []
    rid = meta.get("id")
    if not isinstance(rid, str) or not ID.match(rid):
        problems.append(f"id {rid!r} is not D-YYMMDD-<slug>")
    elif rid != path.stem:
        problems.append(f"id {rid} differs from the file name")
    status = meta.get("status")
    if status not in STATUSES:
        problems.append(f"status {status!r} not in {', '.join(STATUSES)}")
    date = meta.get("date")
    if parse_date(str(date)) is None:
        problems.append(f"date {date!r} is not YYYY-MM-DD")
    if status == "superseded":
        by = meta.get("superseded_by")
        if not by:
            problems.append("superseded without superseded_by")
        elif str(by) not in ids:
            problems.append(f"superseded_by {by} is not a record")
    found = dict(sections(body, 2))
    problems.extend(f"no '## {s}' section" for s in SECTIONS if s not in found)
    if "Considered options" in found and _table_rows(found["Considered options"]) < _MIN_OPTIONS:
        problems.append("Considered options table has fewer than 2 rows")
    return problems


def check(root: Path) -> Result:
    """Every decision record has the fixed front matter, sections and options table."""
    files = records(root)
    if not files:
        return unknown(NAME, f"no records in {DIR}/")
    ids = {p.stem for p in files}
    broken = [f"{p.name}: {'; '.join(probs)}" for p in files if (probs := _check_record(p, ids))]
    if broken:
        return fail(NAME, f"{len(broken)} of {len(files)} record(s) broken: " + " | ".join(broken))
    return ok(NAME, f"{len(files)} record(s) follow the format")
