# Evaluation Scenarios

Use these scenarios to validate behavior of the `reviewing-skills` workflow.

## Scenario 1: Healthy Skill Baseline

- Goal: Confirm the reviewer reports no false-positive critical issues on a valid skill.
- Input:
  - Target contains valid frontmatter, direct reference links, and concise workflow steps.
- Expected result:
  - Automated checks: no `error` issues.
  - Manual review: at most low-severity polish items.

## Scenario 2: Broken Frontmatter

- Goal: Confirm metadata violations are detected and prioritized.
- Input:
  - Target `SKILL.md` has missing or invalid YAML frontmatter, or invalid `name`.
- Expected result:
  - Automated checks include `frontmatter.*` errors.
  - Final report lists frontmatter findings before lower-severity items.

## Scenario 3: Progressive Disclosure Violations

- Goal: Confirm reference hygiene issues are surfaced.
- Input:
  - Target links to missing markdown files or deeper-than-allowed nested references.
- Expected result:
  - Automated checks include `references.missing` or `references.nested_depth`.
  - Report includes concrete link or structure fixes.

## Execution Notes

- Run automated checks with:
  - `uv run scripts/check_skill_practices.py <target-skill-path>`
  - Fallback: `python3 scripts/check_skill_practices.py <target-skill-path>`
- For each scenario, capture:
  - Command and exit code
  - Count by severity (`error`, `warning`, `info`)
  - One-sentence conclusion on whether behavior matched expectation
