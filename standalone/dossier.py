#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["evocaslab-dossier @ git+https://github.com/evocaslab/dossier@v0.1.1"]
# ///
"""The dossier CLI as one self-contained file: copy it anywhere, run `uv run --script dossier.py check`.

The pin is the release tag of the same version (a test keeps it equal to pyproject.toml); no install step.
"""

from dossier.cli import app

if __name__ == "__main__":
    app()
