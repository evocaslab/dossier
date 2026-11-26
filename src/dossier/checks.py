"""The checks. Each takes the repo root and returns one `Result`. No network, no LLM."""

import re
from collections.abc import Callable
from pathlib import Path

from dossier import boundaries, config, contracts, decisions, freshness, stories
from dossier.model import Result, Status
from dossier.util import HEADING as _HEADING
from dossier.util import fail as _fail
from dossier.util import ok as _ok
from dossier.util import strip_fences as _strip_fences

FIRST_SCREEN_LINES = 40
_MIN_PROSE_WORDS = 5
_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://")


def front_door(root: Path) -> Result:
    """README exists and its first screen has a title and a real sentence."""
    name = "front-door"
    readme = root / "README.md"
    if not readme.is_file():
        return _fail(name, "README.md not found")
    lines = _strip_fences(readme.read_text(encoding="utf-8"))[:FIRST_SCREEN_LINES]
    if not any(line.startswith("# ") for line in lines):
        return _fail(name, f"no `# ` title in the first {FIRST_SCREEN_LINES} lines of README.md")
    prose = [ln for ln in lines if ln.strip() and not ln.lstrip().startswith(("#", "|", "[", "!", "<", ">"))]
    if not any(len(ln.split()) >= _MIN_PROSE_WORDS for ln in prose):
        return _fail(name, "the first screen of README.md has no sentence saying what the repo is")
    return _ok(name, "README.md has a title and an opening sentence")


def _slug(heading: str) -> str:
    """GitHub-style anchor for a heading."""
    text = re.sub(r"[`*_]", "", heading.lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.strip().replace(" ", "-")


def _anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    anchors: set[str] = set()
    for line in _strip_fences(path.read_text(encoding="utf-8")):
        m = _HEADING.match(line)
        if m:
            base = _slug(m.group(2))
            n = seen.get(base, 0)
            seen[base] = n + 1
            anchors.add(base if n == 0 else f"{base}-{n}")
    return anchors


def _markdown_files(root: Path) -> list[Path]:
    files = [p for p in (root / "README.md", root / "ARCHITECTURE.md") if p.is_file()]
    docs = root / "docs"
    if docs.is_dir():
        files.extend(sorted(docs.rglob("*.md")))
    return files


def _check_target(source: Path, target: str) -> str:
    """Empty string when the link resolves, else the reason."""
    path_part, _, fragment = target.partition("#")
    dest = source if not path_part else (source.parent / path_part)
    if not dest.exists():
        return "file not found"
    if fragment and dest.suffix == ".md" and dest.is_file() and fragment.lower() not in _anchors(dest):
        return "heading not found"
    return ""


def links(root: Path) -> Result:
    """Relative links (and `#fragments`) in README, ARCHITECTURE and docs/ resolve."""
    name = "links"
    files = _markdown_files(root)
    if not files:
        return Result(name, Status.UNKNOWN, "no README.md, ARCHITECTURE.md or docs/*.md to check")
    broken: list[str] = []
    count = 0
    for md in files:
        for line in _strip_fences(md.read_text(encoding="utf-8")):
            for target in _LINK.findall(line):
                if target.startswith(_SKIP_SCHEMES):
                    continue
                count += 1
                problem = _check_target(md, target)
                if problem:
                    broken.append(f"{md.relative_to(root)}: {target} ({problem})")
    if broken:
        return _fail(name, f"{len(broken)} broken: " + "; ".join(broken))
    return _ok(name, f"{count} relative link(s) in {len(files)} file(s) resolve")


def dossier(root: Path) -> Result:
    """`dossier.yaml` lists every part its kind requires, with existing paths or a reason."""
    name = "dossier"
    try:
        doc = config.load(root)
    except config.ConfigError as exc:
        return _fail(name, str(exc))
    problems: list[str] = [
        f"required part '{req}' is not listed" for req in config.REQUIRED[doc.kind] if req not in doc.parts
    ]
    for part in doc.parts.values():
        problems.extend(
            f"part '{part.name}': {rel} not found" for rel in part.present if not (root / rel).exists()
        )
    if problems:
        return _fail(name, "; ".join(problems))
    exempt = sum(1 for p in doc.parts.values() if p.exempt)
    return _ok(name, f"kind {doc.kind}: {len(doc.parts) - exempt} part(s) present, {exempt} exempt")


CHECKS: dict[str, Callable[[Path], Result]] = {
    "front-door": front_door,
    "links": links,
    "dossier": dossier,
    "decisions": decisions.check,
    "stories": stories.check,
    "freshness": freshness.check,
    "contracts": contracts.check,
    "boundaries": boundaries.check,
}
