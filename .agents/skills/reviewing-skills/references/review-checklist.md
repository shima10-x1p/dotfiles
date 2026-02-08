# Skill Review Checklist

Use this checklist for manual review after running automated checks.

## 1. Metadata Quality

- `name` uses lowercase letters, digits, and hyphens only.
- `name` is 64 characters or fewer.
- `name` does not contain reserved terms like `anthropic` or `claude`.
- `description` is specific and non-empty.
- `description` includes both:
  - What the skill does.
  - When the skill should be used (trigger context).
- `description` is written in third-person style.

## 2. SKILL.md Quality

- Instructions are concise and avoid obvious background explanations.
- Body stays within 500 lines, or details are moved to references files.
- Main workflow is explicit and sequential for fragile tasks.
- Guidance matches required freedom level:
  - High freedom for flexible reasoning tasks.
  - Low freedom for fragile and sequence-dependent operations.

## 3. Progressive Disclosure

- `SKILL.md` gives overview and links to deeper docs only when needed.
- Reference files are linked directly from `SKILL.md` (one level deep).
- Reference files longer than 100 lines have a table of contents.
- Directory/file names are descriptive (`reference/finance.md` style, not `file1.md`).

## 4. Workflow and Feedback Loops

- Multi-step tasks include a clear checklist or ordered steps.
- Validation steps are present before irreversible or risky operations.
- Iterative loop exists when quality depends on verification:
  - Validate -> Fix -> Re-run validation.

## 5. Script and Tooling Quality

- Scripts handle expected errors explicitly.
- Constants and defaults are justified; avoid unexplained magic numbers.
- Required dependencies are stated explicitly.
- Instructions clearly say whether a script should be executed or read.
- Paths use forward slashes, not backslashes.

## 6. Content Risks and Anti-Patterns

- Avoid time-sensitive instructions unless moved to a legacy/history section.
- Keep terminology consistent within the skill.
- Avoid overwhelming users with many equivalent options.
- Include concrete examples when output style is important.

## 7. Testing Evidence

- At least three representative evaluation scenarios are defined.
- Skill behavior is verified on intended model tiers (if applicable).
- Real usage feedback or iteration notes are captured.

## Severity Guidance

- `high`: Breaks triggering, structure validity, or safety/reliability guarantees.
- `medium`: Causes confusion, quality regression, or likely misuse.
- `low`: Improves maintainability, readability, or discoverability.
