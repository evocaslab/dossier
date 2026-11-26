"""`dossier new <part>`: write a part's template files, never over an existing file unless forced."""

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from string import Template

from dossier.contracts import declared_version
from dossier.util import today

DEFAULT_VERSION = "0.1.0"

# part -> (template file, destination); `{id}` in a destination is the decision id.
PARTS: dict[str, tuple[tuple[str, str], ...]] = {
    "dossier": (("dossier.yaml", "dossier.yaml"),),
    "purpose": (("WHY.md", "WHY.md"),),
    "reasoning": (("decision.md", "docs/decisions/{id}.md"),),
    "design": (("ARCHITECTURE.md", "ARCHITECTURE.md"), ("user-stories.md", "docs/user-stories.md")),
    "contract": (("CHANGELOG.md", "CHANGELOG.md"),),
    "trust": (("SECURITY.md", "SECURITY.md"),),
    "help": (("CONTRIBUTING.md", "CONTRIBUTING.md"),),
    "agents": (("AGENTS.md", "AGENTS.md"),),
}
NOT_TEMPLATED = {
    "identity": "the brand kit is built by brandforge, not from a template",
}


@dataclass(frozen=True)
class Written:
    """One destination and whether it was written or left alone."""

    path: Path
    written: bool


def decision_id(slug: str) -> str:
    """`D-YYMMDD-<slug>` for today."""
    return f"D-{today():%y%m%d}-{slug}"


def write(
    part: str, root: Path, *, slug: str = "first-decision", force: bool = False, dry_run: bool = False
) -> list[Written]:
    """Write the templates of `part` under `root`; existing files are kept unless `force`.

    With `dry_run` nothing is written; `written` then says what a real run would write.
    """
    found = declared_version(root)
    values = {
        "name": root.resolve().name,
        "date": today().isoformat(),
        "id": decision_id(slug),
        "version": found[0] if found else DEFAULT_VERSION,
    }
    out: list[Written] = []
    for template, dest in PARTS[part]:
        target = root / dest.format(id=values["id"])
        if target.exists() and not force:
            out.append(Written(target, written=False))
            continue
        if dry_run:
            out.append(Written(target, written=True))
            continue
        text = files("dossier").joinpath("templates", template).read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(Template(text).safe_substitute(values), encoding="utf-8")
        out.append(Written(target, written=True))
    return out
