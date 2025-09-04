# Contributing

Thanks for your interest in improving `reports_ai`! This is a concise guide for local setup and cutting releases.

## Development Setup

- Install deps: `uv sync --dev --group doc` (or `pip install -e .[dev,doc]`)
- Pre-commit: `pre-commit install` then `pre-commit run --all-files`
- Docs: `uv run python docs/make.py` (outputs to `docs/api/`)

## Running Tests

- If/when tests exist: `uv run pytest -q` (add `--cov=reports_ai` for coverage)

## Releasing (Tags)

We use tag-driven releases. CI builds artifacts, creates a GitHub Release, and publishes to PyPI.

1) Bump version in `pyproject.toml` under `[project] version`.
2) Commit the change: `git commit -am "chore(release): vX.Y.Z"`
3) Create an annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
4) Push the tag: `git push origin vX.Y.Z`

Requirements:
- Repo secret `PYPI_API_TOKEN` must be set for PyPI publishing.
- Python 3.11+; Django 4.2+ compatibility maintained.

Versioning: follow SemVer (MAJOR.MINOR.PATCH). Keep changes and notes concise in PRs.

