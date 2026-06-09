---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Coding Conventions

## Core Principles

- Prioritize readability, clarity, and maintainability over cleverness.
- Write idiomatic Python that is simple to understand and easy to change.
- Prefer small, focused functions over large functions with many responsibilities.
- Make behavior explicit when handling errors, edge cases, or external dependencies.

## Type Hints

- Add type hints to public functions, methods, and complex internal functions.
- Prefer modern built-in generic types such as `list[str]`, `dict[str, int]`, and `tuple[int, ...]`.
- Use types from `typing` when needed, such as `Any`, `Callable`, `Iterable`, `Protocol`, or `TypedDict`.
- Avoid overly broad types when a more precise type is practical.

## Docstrings <MUST>

- Write docstrings for modules, classes, functions, and methods.
- Use Google Style docstrings.
- Keep docstrings concise. Explain what the object does, its arguments, return value, raised exceptions, and important side effects.
- Do not write docstrings that merely repeat the function name or obvious type hints.
- Always write a docstring for every class and function, even private ones.
- Please refer to the following sample for function docstrings.
- Please write the docstring in Japanese.
- In all cases, you must include a docstring that conforms to the example below. Omitting a docstring is not permitted.

Example:

```python
def calculate_area(radius: float) -> float:
    """円の面積を計算する。

    Args:
        radius (float): 円の半径。非負である必要があります。

    Returns:
        float: 円の面積。

    Raises:
        ValueError: `radius` が負の場合。
    """
    if radius < 0:
        raise ValueError("radius must be non-negative")

    return math.pi * radius**2
```

## Comments

- Use comments to explain why something is done, not what the code plainly says.
- Add short comments for non-obvious business rules, workarounds, performance trade-offs, or edge-case handling.
- Avoid redundant comments that restate the code.

## Code Style and Formatting

- Follow PEP 8 and write code that is compatible with common formatters such as Black and Ruff.
- Use 4 spaces for indentation.
- Keep line length reasonable; prefer Black's default of 88 characters unless the project config says otherwise.
- Use clear, descriptive names for variables, functions, classes, and modules.
- Separate functions and classes with blank lines according to PEP 8.
- Place module imports at the top of the file and group them in this order:
  1. Standard library
  2. Third-party packages
  3. Local application imports

## Error Handling and Edge Cases

- Handle expected error cases explicitly.
- Raise specific exceptions with helpful messages.
- Avoid bare `except:` clauses.
- Consider common edge cases, including empty inputs, invalid values, missing data, and large inputs.
- Validate inputs at system boundaries, such as API handlers, CLI entry points, and file/database access layers.

## External Dependencies

- Use external libraries only when they make the code clearer, safer, or significantly simpler.
- When introducing a new dependency, make its purpose clear in the surrounding code or documentation.
- Keep dependency-specific logic isolated when practical.

## Algorithms and Complex Logic

- For algorithmic or complex logic, include a short explanation of the approach before or near the implementation.
- Prefer readable intermediate variables over dense one-liners.
- Split complex logic into helper functions when it improves understanding.

## Testing

- MUST USE pytest for unit testing. 
- Write unit tests for critical behavior, edge cases, and bug fixes.
- Prefer focused tests that verify one behavior at a time.
- Name test functions descriptively, such as `test_calculate_area_rejects_negative_radius`.
- Include tests for invalid inputs, empty inputs, and boundary values when relevant.
- Use test docstrings only when the purpose of the test is not clear from its name.

## Copilot Behavior

- Make the smallest change that satisfies the user's request.
- Do not modify unrelated files, functions, imports, formatting, or behavior.
- Do not refactor existing code unless the user explicitly asks for refactoring.
- When generating new code, include only the code necessary for the requested change unless tests or examples are explicitly requested.
- When modifying existing code, preserve the surrounding style and project conventions.
- Do not add excessive comments, broad rewrites, or unrelated restructuring.
- Prefer small, reviewable changes.

