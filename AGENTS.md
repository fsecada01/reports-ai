# Repository Guidelines

This repository contains a reusable Django app, `reports_ai`, for generating AI-assisted summaries from Git history. Use the guidance below to work consistently and safely.

## Project Structure & Module Organization

- `reports_ai/`: Django app (admin, apps, models, forms, tasks, views, urls).
- `reports_ai/services/`: Integration helpers (e.g., `llm_service.py`).
- `reports_ai/templates/reports_ai/`: Django templates.
- `reports_ai/migrations/`: App migrations.
- `docs/`: Lightweight docs and pdoc config (`docs/settings.py`).
- `run_pdoc.py`: Generates API docs to `docs/api/`.
- `.env.example`: Reference for required environment variables.
- Build artifacts: `build/`, `reports_ai.egg-info/` (do not edit).

## Build, Test, and Development Commands

- Setup (uv): `uv sync --dev --extra doc` — install dev and docs extras.
- Lint: `uv run ruff check .` — static analysis per `pyproject.toml`.
- Format: `uv run black .` and `uv run isort .` — code formatting/imports.
- Docs: `uv run python run_pdoc.py` — generate API docs to `docs/api/`.
- Alternative pip setup: `pip install -e .[dev,doc]` if uv is unavailable.
- Pre-commit: `pre-commit install` then `pre-commit run --all-files` — enforce lint/format on staged files.

## Coding Style & Naming Conventions

- Python: 4-space indent; max line length 80 (Black/Ruff configured).
- Tools: Black, Isort (profile=black), Ruff (rules E,W,F,I,C,B; ignore E501).
- Names: modules/functions `snake_case`; classes `CamelCase`; constants `UPPER_SNAKE_CASE`.
- Templates: place under `reports_ai/templates/reports_ai/` with descriptive names.
 - Pre-commit: hooks run Ruff, Black, and Isort on commit.

## Testing Guidelines

- Current status: no formal test suite. Prefer `pytest` + `pytest-django` when adding tests.
- Layout: `tests/` at repo root; files as `test_*.py`.
- Scope: unit-test services (e.g., `services/`), model behavior, and admin actions.
- Run: `uv run pytest` (or `pytest`). Target ≥80% coverage for new/changed code.

## Commit & Pull Request Guidelines

- Commits: follow Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `refactor:`). Use imperative mood; keep scope small.
- PRs: include summary, rationale, linked issues, screenshots of admin UI when relevant, and docs updates. Note breaking changes and rollout steps.

## Security & Configuration Tips

- Never commit secrets; copy `.env.example` to `.env` locally and set `REPORTS_AI_*` variables.
- For docs generation/imports, `docs/settings.py` provides safe defaults; do not use in production.
- Ensure `REPORTS_AI_CLONE_PATH` is writable and cleaned up in development.
- Providers: for `REPORTS_AI_LLM_PROVIDER=anthropic` or `google`, install `langchain-anthropic` or `langchain-google-genai` respectively.
