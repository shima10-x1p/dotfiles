# ty Configuration Templates

Use these as starting points when the user asks to add ty or when setting up type checking for a new Python project. ty is beta, so keep configuration explicit, modest, and easy to revise.

## Minimal pyproject.toml setup

```toml
[tool.ty.environment]
python-version = "3.12"

[tool.ty.src]
include = ["src", "tests"]

[tool.ty.terminal]
output-format = "concise"
```

## Prefer project.requires-python when available

If the project already declares a Python version range, avoid duplicating the setting unless there is a clear reason:

```toml
[project]
requires-python = ">=3.12"
```

ty can infer the Python version from `project.requires-python` when no explicit ty Python version is configured.

## ty.toml form

When using `ty.toml`, omit the `[tool.ty]` prefix:

```toml
[environment]
python-version = "3.12"

[src]
include = ["src", "tests"]

[terminal]
output-format = "concise"
```

`ty.toml` takes precedence over `[tool.ty]` in `pyproject.toml` when both are in the same directory.

## VS Code: ty for checking, Pylance for language services

Use this only when the user wants ty diagnostics while keeping Pylance for completion, hover, and navigation:

```json
{
  "python.languageServer": "Pylance",
  "ty.disableLanguageServices": true
}
```

## Guidance

- Prefer `uv run ty check` in uv-managed projects.
- Do not replace mypy, Pyright, basedpyright, or another configured type checker with ty unless the user requests migration.
- If introducing ty alongside another checker, explain the overlap and keep validation expectations clear.
- Do not change editor settings unless the task is specifically about editor integration.
