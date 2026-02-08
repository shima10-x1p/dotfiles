#!/usr/bin/env python3
"""Create and validate Agent Trace records using JSON Schema."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from jsonschema import FormatChecker
    from jsonschema.validators import validator_for
except ImportError as exc:  # pragma: no cover - depends on runtime env
    raise SystemExit(
        "Missing dependency: jsonschema. Install it first, for example: pip install jsonschema"
    ) from exc

VCS_TYPES = ("git", "jj", "hg", "svn")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Input file does not exist: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from None


def _write_json(data: Any, path: Path | None, pretty: bool) -> None:
    kwargs: dict[str, Any] = {"ensure_ascii": False}
    if pretty:
        kwargs["indent"] = 2
    text = json.dumps(data, **kwargs) + "\n"
    if path is None:
        sys.stdout.write(text)
        return
    path.write_text(text, encoding="utf-8")


def _now_rfc3339() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _default_schema_path() -> Path:
    return Path(__file__).resolve().parent.parent / "references" / "trace-record.schema.json"


def _format_json_pointer(path_items: list[Any]) -> str:
    if not path_items:
        return "$"

    pointer = "$"
    for item in path_items:
        if isinstance(item, int):
            pointer += f"[{item}]"
        else:
            pointer += f".{item}"
    return pointer


def _build_validator(schema_path: Path):
    schema = _load_json(schema_path)
    if not isinstance(schema, dict):
        raise ValueError(f"Schema must be a JSON object: {schema_path}")
    validator_cls = validator_for(schema)
    validator_cls.check_schema(schema)
    return validator_cls(schema, format_checker=_build_format_checker())


def _is_rfc3339_datetime(value: str) -> bool:
    if not RFC3339_RE.match(value):
        return False
    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return True


def _is_absolute_uri(value: str) -> bool:
    parsed = urlparse(value)
    if not parsed.scheme:
        return False
    if parsed.scheme == "urn":
        return bool(parsed.path)
    return bool(parsed.netloc or parsed.path)


def _build_format_checker() -> FormatChecker:
    checker = FormatChecker()

    @checker.checks("uuid")
    def check_uuid(value: object) -> bool:
        if not isinstance(value, str):
            return True
        try:
            uuid.UUID(value)
        except ValueError:
            return False
        return True

    @checker.checks("date-time")
    def check_datetime(value: object) -> bool:
        if not isinstance(value, str):
            return True
        return _is_rfc3339_datetime(value)

    @checker.checks("uri")
    def check_uri(value: object) -> bool:
        if not isinstance(value, str):
            return True
        return _is_absolute_uri(value)

    return checker


def validate_trace_record(record: Any, validator) -> list[str]:
    errors: list[str] = []
    for error in sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path)):
        location = _format_json_pointer(list(error.absolute_path))
        errors.append(f"{location}: {error.message}")
    return errors

def cmd_create(args: argparse.Namespace) -> int:
    record = _load_json(Path(args.input))
    if not isinstance(record, dict):
        print("Input JSON must be an object", file=sys.stderr)
        return 1

    record.setdefault("version", args.version)
    record.setdefault("id", args.id or str(uuid.uuid4()))
    record.setdefault("timestamp", args.timestamp or _now_rfc3339())

    if args.vcs_type or args.revision:
        if not (args.vcs_type and args.revision):
            print("Both --vcs-type and --revision are required together", file=sys.stderr)
            return 1
        record["vcs"] = {"type": args.vcs_type, "revision": args.revision}

    if args.tool_name or args.tool_version:
        tool: dict[str, Any] = {}
        if isinstance(record.get("tool"), dict):
            tool.update(record["tool"])
        if args.tool_name:
            tool["name"] = args.tool_name
        if args.tool_version:
            tool["version"] = args.tool_version
        record["tool"] = tool

    schema_path = Path(args.schema) if args.schema else _default_schema_path()
    validator = _build_validator(schema_path)
    errors = validate_trace_record(record, validator)
    if errors:
        print("Trace record validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else None
    _write_json(record, output, pretty=args.pretty)
    if output:
        print(f"Wrote trace record: {output}", file=sys.stderr)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    record = _load_json(Path(args.input))
    schema_path = Path(args.schema) if args.schema else _default_schema_path()
    validator = _build_validator(schema_path)
    errors = validate_trace_record(record, validator)
    if errors:
        print("Trace record validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print("Trace record is valid.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create and validate Agent Trace record JSON files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Generate a normalized trace record")
    create.add_argument("--input", required=True, help="Path to draft JSON file")
    create.add_argument("--output", help="Output path (default: stdout)")
    create.add_argument("--version", default="0.1.0", help="Trace spec version")
    create.add_argument("--id", help="Trace record UUID (default: auto-generate)")
    create.add_argument(
        "--timestamp",
        help="RFC3339 timestamp (default: current UTC time)",
    )
    create.add_argument(
        "--vcs-type",
        choices=sorted(VCS_TYPES),
        help="Version control system type",
    )
    create.add_argument("--revision", help="VCS revision identifier")
    create.add_argument("--tool-name", help="Trace generator tool name")
    create.add_argument("--tool-version", help="Trace generator tool version")
    create.add_argument(
        "--schema",
        help="Schema file path (default: references/trace-record.schema.json)",
    )
    create.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print output JSON",
    )
    create.set_defaults(func=cmd_create)

    validate = subparsers.add_parser("validate", help="Validate a trace record")
    validate.add_argument("--input", required=True, help="Path to trace JSON file")
    validate.add_argument(
        "--schema",
        help="Schema file path (default: references/trace-record.schema.json)",
    )
    validate.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
