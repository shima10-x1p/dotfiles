---
name: reviewing-skills
description: Reviews an existing skill for compliance with skill-authoring best practices, including metadata quality, progressive disclosure, workflow clarity, and script reliability. Use when creating or updating a skill and needing a prioritized gap report with concrete fixes.
---

# Reviewing Skills

## Overview

Review a target skill folder and report whether it follows best practices. Combine deterministic checks from `scripts/check_skill_practices.py` with manual review using [review-checklist](references/review-checklist.md).

## Prerequisites

- `uv` is the default runner for executing scripts.
- `python3` can be used as a fallback when `uv` is unavailable.
- `PyYAML` is optional; `scripts/check_skill_practices.py` has a built-in fallback parser when the package is not installed.

## Inputs

Collect these inputs before starting:
- Target skill directory path
- Scope of review: full review or metadata-only quick pass
- Optional constraints from the user (for example, strict 500-line cap or strict naming conventions)

## Review Workflow

Copy this checklist and mark progress:

```text
Review progress:
- [ ] Step 1: Inventory skill files
- [ ] Step 2: Run automated checks
- [ ] Step 3: Perform manual quality review
- [ ] Step 4: Produce findings-first report
- [ ] Step 5: Validate fixes and re-run checks (required)
```

### Step 1: Inventory skill files

Inspect the target folder and confirm presence of:
- `SKILL.md` (required)
- `agents/openai.yaml` (recommended for UI metadata)
- `scripts/`, `references/`, `assets/` (optional, if relevant)

If `SKILL.md` is missing, stop and report a blocking issue.

### Step 2: Run automated checks

Run these commands from the `reviewing-skills` directory.

Run (recommended):

```bash
uv run scripts/check_skill_practices.py <target-skill-path>
```

Fallback:

```bash
python3 scripts/check_skill_practices.py <target-skill-path>
```

The script checks objective rules such as frontmatter constraints, line budget, Windows-style paths, nested reference depth, and missing table of contents in long reference files.

### Step 3: Perform manual quality review

Use [review-checklist](references/review-checklist.md) for qualitative review:
- Conciseness and signal-to-noise quality
- Appropriate degrees of freedom
- Workflow clarity and validation loops
- Clarity of triggers in `description`
- Examples, terminology consistency, and anti-patterns
- Coverage against representative scenarios in [evals](references/evals.md)

Mark each issue with severity:
- `high`: likely to break triggering, safety, or reliability
- `medium`: quality regression or confusion risk
- `low`: polish or maintainability improvement

### Step 4: Produce findings-first report

Return findings first, ordered by severity, with file references.

For Japanese review output with checklist tracking, use:
- [review-feedback-template-ja](references/review-feedback-template-ja.md)

Use this format:

```markdown
Findings
1. [high] <short title>
   - Evidence: <path:line>
   - Why it matters: <impact>
   - Fix: <concrete edit>

2. [medium] <short title>
   - Evidence: <path:line>
   - Why it matters: <impact>
   - Fix: <concrete edit>

Open Questions
1. <question if information is missing>

Summary
- Passed checks: <count>
- Failed checks: <count>
- Manual risks: <count>
```

If no issues are found, state that explicitly and include residual risks (for example, "multi-model testing evidence not provided").

### Step 5: Validate fixes and re-run checks (required)

If you propose any concrete fix:
- Apply the fix (or provide exact patch-ready edits).
- Re-run automated checks on the updated target.
- Re-review affected checklist items.
- Include a diff summary in the report with changed files and key line-level edits.

When no fix is applied, explicitly state that no re-run diff is available.
