# Trace Record Spec Quick Reference

Use this file when building or reviewing Agent Trace JSON payloads.
Canonical validation source: `trace-record.schema.json` in the same directory.

## Required Top-Level Fields

| Field | Type | Notes |
| --- | --- | --- |
| `version` | string | Semantic version (for example `0.1.0`) |
| `id` | string | UUID |
| `timestamp` | string | RFC3339 date-time |
| `files` | array | One or more file entries |

Optional top-level fields: `vcs`, `tool`, `metadata`.

## `vcs` Field

`vcs` (when present) must include:
- `type`: one of `git`, `jj`, `hg`, `svn`
- `revision`: non-empty VCS-specific identifier

## File / Conversation / Range Structure

Each `files[]` item:
- `path`: repository-relative file path
- `conversations`: array

Each `conversations[]` item:
- `ranges`: array (required)
- `url`: absolute URI (optional)
- `contributor`: contributor object (optional)
- `related`: array of `{type, url}` objects (optional)

Each `ranges[]` item:
- `start_line`: integer, minimum `1`
- `end_line`: integer, minimum `1`, and `>= start_line`
- `content_hash`: optional string
- `contributor`: optional override object

## Contributor Types

Allowed `contributor.type` values:
- `human`
- `ai`
- `mixed`
- `unknown`

`model_id` is optional but recommended for AI, with `provider/model-name` style.

## Minimal Valid Example

```json
{
  "version": "0.1.0",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "files": [
    {
      "path": "src/app.ts",
      "conversations": [
        {
          "contributor": { "type": "ai" },
          "ranges": [{ "start_line": 1, "end_line": 50 }]
        }
      ]
    }
  ]
}
```

## Draft Input Pattern for `trace_record_tool.py create`

Provide at least `files` in the input file. `create` auto-fills missing:
- `id`
- `timestamp`
- `version` (default `0.1.0`)

Add `--vcs-type` and `--revision` when tying the record to a specific commit/change.

## Validation Behavior in This Skill

- Default validation is JSON Schema-based and follows `trace-record.schema.json`.
- Additional stricter profile rules (for example, forcing non-empty arrays) are not enforced by default.

## Common Validation Failures

- `id must be a valid UUID string`
  - Fix: use generated UUID format `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- `timestamp must be an RFC3339 date-time string`
  - Fix: use UTC format like `YYYY-MM-DDTHH:MM:SSZ`.
- `'ranges' is a required property`
  - Fix: include a `ranges` field in every conversation object.
- `end_line must be >= start_line`
  - Fix: correct line order in the range.
