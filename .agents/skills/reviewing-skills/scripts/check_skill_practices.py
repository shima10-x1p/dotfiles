#!/usr/bin/env python3
"""Check a skill folder against practical skill-authoring best practices."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_LINES = 500

NAME_RE = re.compile(r"^[a-z0-9-]+$")
XML_TAG_RE = re.compile(r"<[^>]+>")
WINDOWS_PATH_RE = re.compile(r"\b[^/\s]+\\[^/\s]+\b")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FIRST_PERSON_RE = re.compile(r"\b(i|we|our|us|my)\b", re.IGNORECASE)
SECOND_PERSON_RE = re.compile(r"\b(you|your|yours)\b", re.IGNORECASE)
WHEN_TO_USE_HINT_RE = re.compile(r"\b(use when|when|if)\b", re.IGNORECASE)
TIME_SENSITIVE_RE = re.compile(
    r"\b(today|tomorrow|yesterday|currently|as of)\b|20\d{2}(?:[-/.](?:0[1-9]|1[0-2]))?",
    re.IGNORECASE,
)


@dataclass
class Issue:
    severity: str
    rule: str
    file: str
    line: int
    message: str
    fix: str


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(text: str, needle: str) -> int:
    for index, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return index
    return 1


def extract_frontmatter(skill_md_text: str) -> tuple[str | None, str]:
    if not skill_md_text.startswith("---\n"):
        return None, skill_md_text
    end = skill_md_text.find("\n---", 4)
    if end == -1:
        return None, skill_md_text
    frontmatter = skill_md_text[4:end]
    body = skill_md_text[end + 4 :].lstrip("\n")
    return frontmatter, body


def parse_frontmatter(frontmatter_text: str) -> dict[str, Any]:
    if yaml:
        parsed = yaml.safe_load(frontmatter_text)
        return parsed if isinstance(parsed, dict) else {}

    # Fallback parser when pyyaml is unavailable.
    parsed: dict[str, Any] = {}
    for raw in frontmatter_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip("'\"")
    return parsed


def add_issue(
    issues: list[Issue],
    severity: str,
    rule: str,
    file: Path,
    line: int,
    message: str,
    fix: str,
) -> None:
    issues.append(
        Issue(
            severity=severity,
            rule=rule,
            file=str(file),
            line=line,
            message=message,
            fix=fix,
        )
    )


def resolve_link_path(base_file: Path, link: str) -> Path | None:
    trimmed = link.split("#", 1)[0].split("?", 1)[0].strip()
    if not trimmed or "://" in trimmed or trimmed.startswith("mailto:"):
        return None
    return (base_file.parent / trimmed).resolve()


def find_md_links(md_file: Path) -> list[tuple[str, int]]:
    text = load_text(md_file)
    results: list[tuple[str, int]] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        link = match.group(1).strip()
        if not link.lower().endswith(".md") and ".md#" not in link.lower():
            continue
        line = text.count("\n", 0, match.start()) + 1
        results.append((link, line))
    return results


def check_frontmatter(skill_md: Path, issues: list[Issue]) -> dict[str, Any] | None:
    text = load_text(skill_md)
    frontmatter_text, body = extract_frontmatter(text)
    if frontmatter_text is None:
        add_issue(
            issues,
            "error",
            "frontmatter.format",
            skill_md,
            1,
            "SKILL.md must start with YAML frontmatter delimited by --- lines.",
            "Add valid YAML frontmatter containing name and description.",
        )
        return None

    frontmatter = parse_frontmatter(frontmatter_text)
    if not frontmatter:
        add_issue(
            issues,
            "error",
            "frontmatter.parse",
            skill_md,
            1,
            "Frontmatter could not be parsed into key-value fields.",
            "Fix YAML syntax so name and description can be parsed.",
        )
        return None

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not name.strip():
        add_issue(
            issues,
            "error",
            "frontmatter.name.required",
            skill_md,
            1,
            "Frontmatter name is missing or empty.",
            "Set name to a lowercase hyphenated value.",
        )
    else:
        name = name.strip()
        if len(name) > MAX_NAME_LENGTH:
            add_issue(
                issues,
                "error",
                "frontmatter.name.length",
                skill_md,
                find_line(text, f"name: {name}"),
                f"Name is too long ({len(name)} > {MAX_NAME_LENGTH}).",
                "Shorten name to 64 characters or fewer.",
            )
        if not NAME_RE.match(name):
            add_issue(
                issues,
                "error",
                "frontmatter.name.format",
                skill_md,
                find_line(text, f"name: {name}"),
                "Name must contain only lowercase letters, digits, and hyphens.",
                "Normalize name to lowercase hyphen-case.",
            )
        if "anthropic" in name or "claude" in name:
            add_issue(
                issues,
                "error",
                "frontmatter.name.reserved",
                skill_md,
                find_line(text, f"name: {name}"),
                "Name contains reserved terms (anthropic/claude).",
                "Rename the skill to avoid reserved terms.",
            )
        if XML_TAG_RE.search(name):
            add_issue(
                issues,
                "error",
                "frontmatter.name.xml",
                skill_md,
                find_line(text, f"name: {name}"),
                "Name must not contain XML-like tags.",
                "Remove angle-bracket tags from name.",
            )

    if not isinstance(description, str) or not description.strip():
        add_issue(
            issues,
            "error",
            "frontmatter.description.required",
            skill_md,
            1,
            "Frontmatter description is missing or empty.",
            "Write a non-empty description that states what the skill does and when to use it.",
        )
    else:
        description = description.strip()
        line = find_line(text, "description:")
        if len(description) > MAX_DESCRIPTION_LENGTH:
            add_issue(
                issues,
                "error",
                "frontmatter.description.length",
                skill_md,
                line,
                f"Description is too long ({len(description)} > {MAX_DESCRIPTION_LENGTH}).",
                "Shorten description to 1024 characters or fewer.",
            )
        if XML_TAG_RE.search(description):
            add_issue(
                issues,
                "error",
                "frontmatter.description.xml",
                skill_md,
                line,
                "Description must not contain XML-like tags.",
                "Remove angle-bracket tags from description.",
            )
        if FIRST_PERSON_RE.search(description) or SECOND_PERSON_RE.search(description):
            add_issue(
                issues,
                "warning",
                "frontmatter.description.person",
                skill_md,
                line,
                "Description appears to use first/second-person phrasing.",
                "Rewrite description in third-person style.",
            )
        if not WHEN_TO_USE_HINT_RE.search(description):
            add_issue(
                issues,
                "warning",
                "frontmatter.description.trigger",
                skill_md,
                line,
                "Description may not clearly state when the skill should be used.",
                "Add explicit trigger wording such as 'Use when ...'.",
            )

    body_lines = body.splitlines()
    if len(body_lines) > MAX_SKILL_LINES:
        add_issue(
            issues,
            "warning",
            "skill.body.length",
            skill_md,
            1,
            f"SKILL.md body exceeds {MAX_SKILL_LINES} lines ({len(body_lines)} lines).",
            "Move detailed content to references files and link from SKILL.md.",
        )

    return frontmatter


def check_markdown_paths(skill_root: Path, issues: list[Issue]) -> None:
    md_files = list(skill_root.rglob("*.md"))
    for md_file in md_files:
        text = load_text(md_file)
        for index, line in enumerate(text.splitlines(), start=1):
            if WINDOWS_PATH_RE.search(line):
                add_issue(
                    issues,
                    "warning",
                    "paths.windows_style",
                    md_file,
                    index,
                    "Detected Windows-style path with backslashes.",
                    "Use forward slashes in documented paths.",
                )


def check_reference_depth(skill_root: Path, issues: list[Issue]) -> None:
    skill_md = (skill_root / "SKILL.md").resolve()
    if not skill_md.exists():
        return

    first_level_files: list[Path] = []
    for link, line in find_md_links(skill_md):
        resolved = resolve_link_path(skill_md, link)
        if resolved is None:
            continue
        if not resolved.exists():
            add_issue(
                issues,
                "warning",
                "references.missing",
                skill_md,
                line,
                f"Linked markdown file is missing: {link}",
                "Fix broken link or create the referenced file.",
            )
            continue
        if resolved != skill_md:
            first_level_files.append(resolved)

    for first_level in first_level_files:
        for link, line in find_md_links(first_level):
            nested = resolve_link_path(first_level, link)
            if nested is None:
                continue
            if nested.exists():
                add_issue(
                    issues,
                    "warning",
                    "references.nested_depth",
                    first_level,
                    line,
                    "Reference file links to another markdown file (more than one level deep).",
                    "Link that file directly from SKILL.md as well.",
                )


def check_reference_toc(skill_root: Path, issues: list[Issue]) -> None:
    refs_dir = skill_root / "references"
    if not refs_dir.exists():
        return

    for ref_file in refs_dir.rglob("*.md"):
        lines = load_text(ref_file).splitlines()
        if len(lines) <= 100:
            continue
        header = "\n".join(lines[:40]).lower()
        if "table of contents" not in header and "contents" not in header and "目次" not in header:
            add_issue(
                issues,
                "warning",
                "references.toc",
                ref_file,
                1,
                "Reference file exceeds 100 lines without an obvious table of contents near the top.",
                "Add a short table of contents section near the start of the file.",
            )


def check_time_sensitive_content(skill_root: Path, issues: list[Issue]) -> None:
    for md_file in skill_root.rglob("*.md"):
        text = load_text(md_file)
        for index, line in enumerate(text.splitlines(), start=1):
            if TIME_SENSITIVE_RE.search(line):
                add_issue(
                    issues,
                    "info",
                    "content.time_sensitive",
                    md_file,
                    index,
                    "Detected potentially time-sensitive wording.",
                    "Prefer versioned 'legacy pattern' sections over date-dependent instructions.",
                )


def run_checks(skill_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    skill_md = skill_root / "SKILL.md"

    if not skill_root.exists() or not skill_root.is_dir():
        add_issue(
            issues,
            "error",
            "skill.path.invalid",
            skill_root,
            1,
            "Provided skill path does not exist or is not a directory.",
            "Pass a valid skill directory path.",
        )
        return issues

    if not skill_md.exists():
        add_issue(
            issues,
            "error",
            "skill.skill_md.missing",
            skill_root,
            1,
            "SKILL.md not found.",
            "Create SKILL.md with valid frontmatter and instructions.",
        )
        return issues

    check_frontmatter(skill_md, issues)
    check_markdown_paths(skill_root, issues)
    check_reference_depth(skill_root, issues)
    check_reference_toc(skill_root, issues)
    check_time_sensitive_content(skill_root, issues)
    return issues


def sort_issues(issues: list[Issue]) -> list[Issue]:
    severity_order = {"error": 0, "warning": 1, "info": 2}
    return sorted(
        issues,
        key=lambda item: (
            severity_order.get(item.severity, 99),
            item.file,
            item.line,
            item.rule,
        ),
    )


def print_markdown(issues: list[Issue]) -> None:
    if not issues:
        print("No issues found.")
        return
    for idx, issue in enumerate(issues, start=1):
        print(f"{idx}. [{issue.severity}] {issue.rule}")
        print(f"   - File: {issue.file}:{issue.line}")
        print(f"   - Message: {issue.message}")
        print(f"   - Fix: {issue.fix}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a skill folder against skill-authoring best practices."
    )
    parser.add_argument("skill_path", help="Path to the target skill directory")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable markdown",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(args.skill_path).resolve()
    issues = sort_issues(run_checks(skill_root))

    if args.json:
        payload = [asdict(issue) for issue in issues]
        print(json.dumps(payload, indent=2))
    else:
        print_markdown(issues)

    has_error = any(issue.severity == "error" for issue in issues)
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
