"""Reader for `dossier.yaml` (schema 1)."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

SCHEMA = 1
KINDS = ("cli", "library", "web", "service")
PARTS = ("identity", "purpose", "reasoning", "design", "contract", "trust", "help", "agents")
# Parts a kind must list (present, or exempt with a reason). Every kind needs all eight today;
# the table is per kind so a later release can relax one without changing the reader.
REQUIRED: dict[str, tuple[str, ...]] = dict.fromkeys(KINDS, PARTS)
FILE_NAME = "dossier.yaml"


class ConfigError(Exception):
    """`dossier.yaml` is missing or malformed; the message says what to fix."""


@dataclass(frozen=True)
class Part:
    """One declared part: paths that exist, or an exemption with its reason."""

    name: str
    present: tuple[str, ...] = ()
    exempt: str = ""


@dataclass(frozen=True)
class Generated:
    """A file the repo renders from its code: `cmd` (argv, no shell) prints its content."""

    path: str
    cmd: tuple[str, ...]


@dataclass(frozen=True)
class Dossier:
    """The parsed file."""

    kind: str
    parts: dict[str, Part] = field(default_factory=dict)
    generated: tuple[Generated, ...] = ()
    boundaries: tuple[str, ...] = ()


def _argv(raw: object, where: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not raw or not all(isinstance(w, str) and w for w in raw):
        msg = f"{where}: `cmd` must be a non-empty list of words (no shell)"
        raise ConfigError(msg)
    return tuple(raw)


def _parse_generated(raw: object) -> tuple[Generated, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        msg = "`generated` must be a list of {path, cmd}"
        raise ConfigError(msg)
    out: list[Generated] = []
    for i, item in enumerate(raw, start=1):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            msg = f"generated entry {i} needs `path` and `cmd`"
            raise ConfigError(msg)
        out.append(Generated(item["path"], _argv(item.get("cmd"), f"generated entry {i}")))
    return tuple(out)


def _parse_boundaries(raw: object) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, dict):
        msg = "`boundaries` must be a mapping with `cmd`"
        raise ConfigError(msg)
    return _argv(raw.get("cmd"), "boundaries")


def _parse_part(name: str, raw: object) -> Part:
    if not isinstance(raw, dict):
        msg = f"part '{name}' must be a mapping with `present` or `exempt`"
        raise ConfigError(msg)
    present, exempt = raw.get("present"), raw.get("exempt")
    if (present is None) == (exempt is None):
        msg = f"part '{name}' needs exactly one of `present` and `exempt`"
        raise ConfigError(msg)
    if present is not None:
        if not isinstance(present, list) or not present or not all(isinstance(p, str) for p in present):
            msg = f"part '{name}': `present` must be a non-empty list of paths"
            raise ConfigError(msg)
        return Part(name, present=tuple(present))
    if not isinstance(exempt, str) or not exempt.strip():
        msg = f"part '{name}': `exempt` needs a reason"
        raise ConfigError(msg)
    return Part(name, exempt=exempt.strip())


def load(root: Path) -> Dossier:
    """Read and validate `<root>/dossier.yaml`."""
    path = root / FILE_NAME
    if not path.is_file():
        msg = f"{FILE_NAME} not found"
        raise ConfigError(msg)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        msg = f"{FILE_NAME} is not valid YAML: {exc}"
        raise ConfigError(msg) from exc
    if not isinstance(data, dict):
        msg = f"{FILE_NAME} must be a mapping"
        raise ConfigError(msg)
    if data.get("schema") != SCHEMA:
        msg = f"schema must be {SCHEMA}, got {data.get('schema')!r}"
        raise ConfigError(msg)
    kind = data.get("kind")
    if kind not in KINDS:
        msg = f"kind must be one of {', '.join(KINDS)}, got {kind!r}"
        raise ConfigError(msg)
    raw_parts = data.get("parts")
    if not isinstance(raw_parts, dict):
        msg = "`parts` must be a mapping"
        raise ConfigError(msg)
    unknown = sorted(set(raw_parts) - set(PARTS))
    if unknown:
        msg = f"unknown part(s): {', '.join(map(str, unknown))} (known: {', '.join(PARTS)})"
        raise ConfigError(msg)
    return Dossier(
        kind=kind,
        parts={n: _parse_part(n, r) for n, r in raw_parts.items()},
        generated=_parse_generated(data.get("generated")),
        boundaries=_parse_boundaries(data.get("boundaries")),
    )
