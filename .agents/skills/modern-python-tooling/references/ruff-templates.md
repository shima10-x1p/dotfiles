# Ruff Configuration Templates

Use these as starting points for new projects or explicit tooling setup requests. Do not overwrite an existing Ruff configuration without preserving project conventions.

## Minimal balanced Ruff setup

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # Pyflakes
    "I",   # import sorting
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## Slightly broader but still review-friendly setup

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # Pyflakes
    "I",    # import sorting
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
    "RUF",  # Ruff-specific rules
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## Guidance

- Do not use `select = ["ALL"]` as a default; it tends to create noisy diffs and can enable new rules on upgrade.
- Run lint fixes before formatting when import sorting is needed: `ruff check --select I --fix`, then `ruff format`.
- Avoid formatter-conflicting lint rules unless the project already handles them intentionally.
- Prefer file-scoped commands for targeted edits.
- Do not add Black, isort, Flake8, or Pylint to a Ruff project unless the user asks or the project already uses them.
