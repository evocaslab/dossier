# Quality: format, lint, types, tests. `q-check` is the gate, the same steps as .github/workflows/ci.yml.

# Format the code.
[group('quality')]
q-fmt:
    uv run ruff format .

# Check format and lint rules.
[group('quality')]
q-lint:
    uv run ruff format --check .
    uv run ruff check .

# Type-check with basedpyright (errors fail; warnings are reported).
[group('quality')]
q-types:
    uv run basedpyright

# Run the tests.
[group('quality')]
q-test:
    uv run pytest -q

# The repo checks its own dossier (import layers included).
[group('quality')]
q-dossier:
    uv run dossier check

# Bulwark public-preset scan; needs `bulwark` on PATH and BULWARK_RULES (fix findings or record them)
[group('quality')]
q-bulwark:
    bulwark scan static . --rules "${BULWARK_RULES:?set BULWARK_RULES to the bulwark rules directory}" --preset public --format result

# The gate: sync, lint, types, tests, own dossier.
[group('quality')]
q-check:
    uv sync --quiet
    just q-lint
    just q-types
    just q-test
    just q-dossier
