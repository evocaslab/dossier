"""`stories`: `docs/user-stories.md` follows the keyed-block form.

Checks: each `## <ID>: <goal>` heading has exactly one fenced `yaml` block whose `id` equals it; ids unique
and `^[A-Z]{2,4}-[0-9]+$`; a retired id (listed under `## Retired`) is never used again; required keys (id,
actor, goal, status, accept with at least one line); `status` in built, partial, planned, gap; each `gwt`
starts with Given and has when and then; in a `built` entry every line names a `test` that exists in a tracked
test file; `proof.screen` names an existing file; the Index table lists exactly the entries.

It cannot check whether a test passes or means the line, whether the actor is real, or whether `proof.cmd`
works.
"""

import re
from pathlib import Path

import yaml

from dossier.model import Result
from dossier.util import FENCE, HEADING, fail, ok, unknown

NAME = "stories"
PAGE = Path("docs/user-stories.md")
ID = re.compile(r"^[A-Z]{2,4}-[0-9]+$")
ENTRY = re.compile(r"^([A-Z]{2,4}-[0-9]+):\s*(.+)$")
STATUSES = ("built", "partial", "planned", "gap")
REQUIRED = ("id", "actor", "goal", "status", "accept")
_TEST_FILE = re.compile(r"(^test_.*\.py$|_test\.(py|go|rs)$|\.(test|spec)\.[cm]?[jt]sx?$)")
_TEST_DIRS = ("tests", "test", "__tests__", "spec")
_SKIP_DIRS = {".git", ".venv", "node_modules", "target", "dist", "build", ".worktrees"}


def _blocks(lines: list[str]) -> list[str]:
    """Contents of fenced ```yaml blocks in `lines`."""
    out: list[str] = []
    inside = False
    is_yaml = False
    current: list[str] = []
    for line in lines:
        if FENCE.match(line):
            if not inside:
                is_yaml = line.strip().lstrip("`~").strip() in {"yaml", "yml"}
                current = []
            elif is_yaml:
                out.append("\n".join(current))
            inside = not inside
            continue
        if inside:
            current.append(line)
    return out


def _split(text: str) -> tuple[dict[str, list[str]], list[str], list[str], list[str]]:
    """Entries by id (their lines), the Index lines, the Retired lines, and malformed `##` headings."""
    entries: dict[str, list[str]] = {}
    index: list[str] = []
    retired: list[str] = []
    bad: list[str] = []
    target: list[str] | None = None
    fenced = False
    dupes: list[str] = []
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
        m = None if fenced else HEADING.match(line)
        if m and len(m.group(1)) == 2:  # noqa: PLR2004 - level-2 headings
            title = m.group(2)
            e = ENTRY.match(title)
            if title == "Index":
                target = index
            elif title == "Retired":
                target = retired
            elif e:
                if e.group(1) in entries:
                    dupes.append(e.group(1))
                target = entries.setdefault(e.group(1), [])
            else:
                bad.append(title)
                target = None
            continue
        if m and len(m.group(1)) == 1:
            target = None
            continue
        if target is not None:
            target.append(line)
    bad.extend(f"{d} (duplicate)" for d in dupes)
    return entries, index, retired, bad


def _test_names(root: Path) -> str:
    """All text of tracked-looking test files, for a name search."""
    chunks: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or _SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        in_test_dir = any(part in _TEST_DIRS for part in path.relative_to(root).parts[:-1])
        if _TEST_FILE.search(path.name) or (in_test_dir and path.suffix in {".py", ".rs", ".ts", ".js"}):
            try:
                chunks.append(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, OSError):
                continue
    return "\n".join(chunks)


def _test_exists(name: str, corpus: str) -> bool:
    q = re.escape(name)
    pattern = rf"(\bdef\s+{q}\s*\(|\bfn\s+{q}\s*\(|\b(it|test)\s*\(\s*['\"`]{q}['\"`])"
    return re.search(pattern, corpus) is not None


def _gwt_ok(text: str) -> bool:
    low = text.lower()
    return text.startswith("Given ") and " when " in low and " then " in low


def _check_accept(sid: str, data: dict[str, object], root: Path, corpus: str | None) -> list[str]:
    problems: list[str] = []
    accept = data.get("accept")
    if not isinstance(accept, list) or not accept:
        return [f"{sid}: accept needs at least one line"]
    for i, line in enumerate(accept, start=1):
        if not isinstance(line, dict) or not isinstance(line.get("gwt"), str):
            problems.append(f"{sid}: accept line {i} has no gwt")
            continue
        if not _gwt_ok(line["gwt"]):
            problems.append(f"{sid}: accept line {i} is not Given / when / then")
        test = line.get("test")
        if data.get("status") == "built":
            if not isinstance(test, str) or not test:
                problems.append(f"{sid}: built, but accept line {i} names no test")
            elif corpus is not None and not _test_exists(test, corpus):
                problems.append(f"{sid}: test {test} not found in the test files")
    proof = data.get("proof")
    if isinstance(proof, dict) and isinstance(proof.get("screen"), str):
        screen = proof["screen"]
        if "/" in screen and not (root / screen.split("#")[0]).exists():
            problems.append(f"{sid}: proof.screen {screen} not found")
    return problems


def _check_entry(sid: str, lines: list[str], root: Path, corpus: str | None) -> list[str]:
    blocks = _blocks(lines)
    if len(blocks) != 1:
        return [f"{sid}: {len(blocks)} yaml blocks, want 1"]
    try:
        data = yaml.safe_load(blocks[0])
    except yaml.YAMLError:
        return [f"{sid}: yaml block does not parse"]
    if not isinstance(data, dict):
        return [f"{sid}: yaml block is not a mapping"]
    problems = [f"{sid}: no {k}" for k in REQUIRED if k not in data]
    if data.get("id") != sid:
        problems.append(f"{sid}: block id {data.get('id')!r} differs from the heading")
    if data.get("status") not in STATUSES:
        problems.append(f"{sid}: status {data.get('status')!r} not in {', '.join(STATUSES)}")
    return problems + _check_accept(sid, data, root, corpus)


def _index_ids(lines: list[str]) -> set[str]:
    ids: set[str] = set()
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and cells and ID.match(cells[0]):
            ids.add(cells[0])
    return ids


def check(root: Path) -> Result:
    """`docs/user-stories.md` has one valid keyed block per entry, an exact Index, and no reused id."""
    page = root / PAGE
    if not page.is_file():
        return unknown(NAME, f"{PAGE} not found")
    entries, index, retired, bad = _split(page.read_text(encoding="utf-8"))
    if not entries:
        return fail(NAME, f"{PAGE} has no `## US-n: <goal>` entries")
    problems = [f"heading '{t}' is not `<ID>: <goal>`, Index or Retired" for t in bad]
    built = any("status: built" in "\n".join(lines) for lines in entries.values())
    corpus = _test_names(root) if built else None
    for sid, lines in entries.items():
        problems.extend(_check_entry(sid, lines, root, corpus))
    listed = _index_ids(index)
    if listed != set(entries):
        missing, extra = sorted(set(entries) - listed), sorted(listed - set(entries))
        problems.append(f"Index differs from the entries (missing {missing}, extra {extra})")
    # The first id on a Retired line is the retired one; later ids are the reason ("merged into US-1").
    retired_ids = {m.group(0) for line in retired if (m := re.search(r"[A-Z]{2,4}-[0-9]+", line))}
    reused = sorted(set(entries) & retired_ids)
    problems.extend(f"{r} is retired but used again" for r in reused)
    if problems:
        return fail(NAME, f"{len(problems)} problem(s): " + "; ".join(problems))
    return ok(NAME, f"{len(entries)} stor(y/ies) valid, Index matches")
