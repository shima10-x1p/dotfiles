# Modern Python Tooling Commands

Use these commands as references. Prefer project-specific commands from documentation, CI, task runners, or existing scripts when they exist.

## uv

### Project setup

- `uv init`
- `uv init <name>`
- `uv python pin <version>`

### Dependencies

- `uv add <package>`
- `uv add --dev <package>`
- `uv add --group <group> <package>`
- `uv remove <package>`
- `uv sync`
- `uv lock`
- `uv lock --check`
- `uv lock --upgrade-package <package>`

### Running project commands

- `uv run python main.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run ty check`

### One-off tools

- `uvx ruff check`
- `uvx ty check`

Use `uvx` only when the tool does not need the project environment. Use `uv run` for project-local tools and anything that must resolve installed project dependencies.

## Ruff

- `uv run ruff check .`
- `uv run ruff check --fix .`
- `uv run ruff check --select I --fix .`
- `uv run ruff format .`
- `uv run ruff format --check .`

Avoid `--unsafe-fixes` unless explicitly requested or carefully reviewed.

## ty

- `uv run ty check`
- `uv run ty check <path>`
- `uvx ty check`
- `ty check`
- `ty server`

Inside uv-managed projects, prefer `uv run ty check` so ty can resolve the project environment.
