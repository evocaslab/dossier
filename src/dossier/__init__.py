"""Dossier: checks that a repo carries the documents that explain it."""

from importlib.metadata import PackageNotFoundError, version

PACKAGE = "evocaslab-dossier"
NAME = "dossier"

try:
    __version__ = version(PACKAGE)
except PackageNotFoundError:  # pragma: no cover - running from a bare source tree
    __version__ = "0.0.0"
