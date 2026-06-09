---
name: modern-python-tooling
description: "Use when: working on modern Python projects, choosing or changing package management, virtual environments, dependency workflows, linting, formatting, type checking, uv, Ruff, ty, pyproject.toml, uv.lock, dependency-groups, or Python tool execution. For existing projects, preserve configured conventions unless migration is requested. For new or unconfigured concerns, prefer uv and Ruff, and consider ty for type checking."
argument-hint: "Python task or tooling question"
---

# Modern Python Tooling

Use this skill to work on Python projects with a modern, low-churn toolchain. The goal is not to evangelize tools blindly; it is to avoid outdated assumptions such as defaulting to `pip install`, hand-written virtual environments, or a `black` + `isort` + `flake8` stack when the project already has a configured toolchain. Only suggest migration when the user explicitly requests it; otherwise preserve the existing stack regardless of perceived benefit.

## References

- Use [commands](./references/commands.md) for uv, Ruff, and ty command examples.
- Use [Ruff templates](./references/ruff-templates.md) when adding or reviewing Ruff configuration.
- Use [ty templates](./references/ty-templates.md) when adding or reviewing ty configuration.
- If reference files are not accessible, use these inline defaults: `uv run pytest`, `uv run ruff check .`, `uv run ruff format .`, `uv run ty check`, `uv add <pkg>`, `uv add --group dev <pkg>`, and `uvx <tool>` for one-off tools.

## Core Principles

- Prefer simple, conventional project workflows over bespoke setup.
- Preserve the tools already used by the project unless the user explicitly asks for migration.
- For new Python projects, prefer `uv` for project/dependency/environment management and Ruff for linting/formatting.
- Treat ty as a strong modern candidate for new type-checking setups, but remember that ty is still beta and should not silently replace an existing checker.
- Make the smallest change needed for the user's request; do not broaden the diff with unrelated formatting, lint fixes, dependency upgrades, or migrations.

## Project Detection

Before changing dependencies, Python versions, linting, formatting, type checking, or editor integration, inspect the relevant project files for that concern:

1. Inspect project files when present:
	- `pyproject.toml`
	- `uv.lock`
	- `.python-version`
	- `.venv/`
	- `ruff.toml`
	- `.ruff.toml`
	- `ty.toml`
	- existing CI, task, or pre-commit configuration
2. Identify the active tools from configuration and lock files.
3. Follow existing conventions first.
4. Do not migrate package managers, linters, formatters, or type checkers unless the user asks.
5. If multiple package managers, formatters, linters, or type checkers are configured simultaneously, ask the user which is authoritative before making changes. Do not assume based on file age or completeness.
6. If no tool is configured for the requested concern, propose the modern default (`uv` for dependencies/environments, Ruff for linting/formatting, ty for type checking) and ask the user to confirm before installing or configuring it.

## Package and Environment Management with uv

### When uv Is Present

Treat a project as uv-managed when it has `uv.lock`, uv configuration in `pyproject.toml`, `.python-version` created for uv workflows, or project documentation/CI that uses `uv`.

In uv-managed projects:

- Prefer `uv` commands over `pip`, `pipx`, `poetry`, `pyenv`, manual `python -m venv`, or ad-hoc environment activation.
- Use `uv add` and `uv remove` for dependency changes.
- Use `uv add --dev` or `uv add --group <name>` for development dependencies, following existing dependency group structure.
- Use `uv sync` to install or refresh project dependencies.
- Use `uv run` for project-local commands such as tests, linters, formatters, scripts, and type checkers.
- Never edit `uv.lock` manually. Let `uv add`, `uv remove`, `uv lock`, `uv sync`, or `uv run` update it.
- Do not manually modify `.venv/` or install project dependencies into it with `uv pip install`; use `uv add` for project dependencies.
- If a uv command fails, surface the full error to the user and do not silently fall back to `pip` or manual virtual environment operations.

### New Projects

For new Python projects, prefer `uv init` and a `pyproject.toml`-based workflow unless the user requests another package manager.

Recommended defaults:

- Keep runtime dependencies in `project.dependencies`.
- Keep local development dependencies in `[dependency-groups]`, typically `dev`.
- Commit `uv.lock` for reproducible installs.
- Do not commit `.venv/`.

### Single-File Scripts

For single-file scripts, prefer PEP 723 inline metadata with `uv run script.py`; do not create a full project structure unless the user asks for a project.

### Running Tools

- Use `uv run <command>` when the tool needs the project environment or pinned project dependencies, such as `pytest`, Ruff configured as a project dependency, or type checkers.
- Use `uvx <tool>` only for one-off tools that do not need the project environment.
- Prefer `uv run ty check` over `uvx ty check` inside uv-managed projects when type checking should see installed project dependencies.
- Common forms: `uv run pytest`, `uv run ruff check .`, `uv run ruff format .`, `uv run ty check`, `uv add <pkg>`, `uv add --group dev <pkg>`, `uvx <tool>`.
- See [commands](./references/commands.md) for common command forms.

### Dependency Updates

- For targeted upgrades, prefer `uv lock --upgrade-package <package>`.
- Avoid broad `uv lock --upgrade` unless the user requests a full dependency refresh.
- If changing constraints in `pyproject.toml`, let uv update the lockfile.
- Do not hand-edit resolved versions in `uv.lock`.

## Linting and Formatting with Ruff

### When Ruff Is Present

Treat Ruff as present when configuration exists in `pyproject.toml`, `ruff.toml`, `.ruff.toml`, dependencies, CI, pre-commit hooks, or project documentation that prescribes Ruff as the lint/format tool, such as `CONTRIBUTING.md` instructions.

In Ruff projects:

- Prefer Ruff for linting, import sorting, and formatting.
- Do not introduce Black, isort, Flake8, or Pylint unless the project already uses them or the user asks.
- Use `ruff check` for linting.
- Use `ruff check --fix` only when the user explicitly requests fixes, or when the task is specifically to resolve lint errors in the files being modified.
- Use `ruff format` for formatting.
- Remember that Ruff formatting does not sort imports by itself; import sorting requires the `I` rules through `ruff check --select I --fix` or the project's configured lint rules.

Preferred commands in uv-managed projects:

- See [commands](./references/commands.md).

### New Projects

For new Python projects, prefer Ruff for both linting and formatting.

Use a modest, review-friendly rule set rather than `select = ["ALL"]` by default. A practical starting point is:

- `E` for pycodestyle errors
- `F` for Pyflakes
- `I` for import sorting
- `B` for flake8-bugbear
- `UP` for pyupgrade

Optionally add more categories only when the project needs them.

Use [Ruff templates](./references/ruff-templates.md) for starter configurations.

### Change Discipline with Ruff

- Do not run broad formatting or auto-fix commands for a small targeted code change unless necessary.
- Prefer file-scoped commands when only a few files are relevant.
- Avoid `--unsafe-fixes` unless the user explicitly asks or the risk is clearly reviewed.
- Avoid `--add-noqa` for normal fixes; it is primarily for migrations and can hide real issues.
- Do not change Ruff configuration just to silence unrelated diagnostics.

## Type Checking with ty

### When to Use ty

Use ty when:

- The project already includes ty in dependencies or configuration.
- The user asks for ty.
- You are setting up type checking for a new project and the user has not requested another checker.

For new projects, ty is a good modern candidate, especially alongside uv and Ruff. However, ty is still beta and uses `0.0.x` versioning, so keep the setup small, explicit, and easy to revise.

### When Not to Replace Existing Checkers

- Do not replace mypy, Pyright, basedpyright, or another existing type checker with ty unless the user requests migration.
- If an existing checker is configured, use it for validation unless asked to compare or migrate.
- If adding ty alongside another checker, make the overlap intentional and explain the reason.

### Commands

Preferred commands in uv-managed projects:

- See [commands](./references/commands.md).

One-off trial outside a project:

- See [commands](./references/commands.md).

Direct commands when ty is already available in the active environment:

- See [commands](./references/commands.md).

### Configuration

Before changing ty behavior, inspect:

- `[tool.ty]` in `pyproject.toml`
- `ty.toml`
- editor settings, especially VS Code settings under `ty.*`
- existing type-checker configuration for mypy, Pyright, basedpyright, or Pylance

Important details:

- `ty.toml` takes precedence over `[tool.ty]` in `pyproject.toml` when both are in the same location.
- ty can infer the Python version from `project.requires-python` when no explicit version is set.
- ty needs the project environment to resolve third-party imports; in uv projects, prefer `uv run ty check`.
- Use [ty templates](./references/ty-templates.md) for starter configurations.

### VS Code Integration

When editing VS Code settings for ty:

- Be careful not to unintentionally disable the user's preferred Python language services.
- The ty VS Code extension can disable the Python extension language server to avoid two Python language servers.
- If the user wants ty only for type checking while keeping Pylance for hover, completion, and navigation, use settings like:
  - `"python.languageServer": "Pylance"`
  - `"ty.disableLanguageServices": true`
- Do not change editor settings unless the user asks or the task is specifically about editor integration.

## Configuration Guidance

### pyproject.toml First

Prefer `pyproject.toml` as the first place to inspect and configure Python project metadata and tool settings.

Common tables:

- `[project]`
- `[project.optional-dependencies]`
- `[dependency-groups]`
- `[tool.uv]`
- `[tool.ruff]`
- `[tool.ruff.lint]`
- `[tool.ruff.format]`
- `[tool.ty]`

### Dependency Groups

For development-only dependencies, prefer standardized dependency groups in new projects:

- `dev` for common development tools
- `lint` for linting and formatting tools when the project separates groups
- `types` for type-checking tools when the project separates groups

Respect existing `tool.uv.dev-dependencies` in older uv projects rather than forcing a migration.

### Python Version

- Check `project.requires-python` and `.python-version` before selecting tool target versions.
- For Ruff, align `target-version` with the supported Python range when configured.
- For ty, avoid duplicating Python version settings if `project.requires-python` is sufficient.

## Validation Workflow

Choose validation based on what changed: run Ruff lint on touched Python files; run Ruff format checks when formatting or style changed; run ty only if types, imports, public interfaces, or type-checker configuration changed; run tests only if logic, behavior, dependencies, or test files changed.

For uv + Ruff + ty projects, a typical validation sequence is:

1. Run Ruff lint checks.
2. Run Ruff format checks.
3. Run ty when configured or relevant.
4. Run tests when tests exist and are relevant.

Use [commands](./references/commands.md) for concrete command examples.

If a project uses a different test runner or task runner, follow the existing project commands instead.

## Migration Rules

Only propose or perform migrations when requested.

If the user asks to modernize tooling:

1. Inventory current package management, linting, formatting, type checking, CI, and editor setup.
2. Propose a minimal migration path.
3. Migrate one layer at a time:
	- package/environment management
	- linting/formatting
	- type checking
	- CI/editor integration
4. Keep each step separately testable.
5. Avoid combining dependency upgrades with tool migration unless necessary.

## Completion Checklist

Before finishing a Python tooling task that touches dependencies or tool configuration:

- Confirm the project toolchain was detected correctly.
- Confirm no lockfile or virtual environment was edited manually.
- Confirm validation commands used the project-preferred runner, especially `uv run` in uv-managed projects.
- Confirm the diff does not include unrelated formatting, lint fixes, dependency upgrades, or migrations.
- If ty was introduced or recommended, mention that it is beta and explain why it is appropriate.

For pure code changes, only confirm that no unrelated formatting, lint fixes, dependency changes, or tooling migrations were included.
