---
name: agent-trace-record
description: Generates and validates Agent Trace JSON Trace Records (v0.1.0 style) from coding-agent activity. Apply this skill when tasks require mapping changed file ranges to conversation URLs, contributor type (human/ai/mixed/unknown), model IDs, VCS revisions, and tool metadata, or converting AI coding logs into interoperable Agent Trace records.
---

# Agent Trace Record

## Overview

Build standards-aligned Agent Trace records and catch schema mistakes before storing or sharing traces. `scripts/trace_record_tool.py` validates against `references/trace-record.schema.json` by default.

## Inputs

Collect the following before generating a record:
- VCS context: `vcs.type` and `vcs.revision` for the snapshot the ranges refer to
- Tool context: generator tool `name` and `version`
- File attribution: per file, per conversation, and per line range mapping
- Contributor info: `type` (`human|ai|mixed|unknown`) and optional `model_id`
- Optional links and metadata: `conversation.url`, `related[]`, and vendor metadata

## Workflow

Copy this checklist and mark progress:

```text
Trace build progress:
- [ ] Step 1: Build attribution draft input
- [ ] Step 2: Generate normalized trace record
- [ ] Step 3: Validate and fix schema issues
- [ ] Step 4: Save using project storage strategy
```

### Step 1: Build attribution draft input

Create a draft JSON that already includes `files[].path`, `conversations[]`, and `ranges[]`.

Use this minimal draft shape:

```json
{
  "files": [
    {
      "path": "src/app.ts",
      "conversations": [
        {
          "url": "https://api.example.com/v1/conversations/abc",
          "contributor": {
            "type": "ai",
            "model_id": "anthropic/claude-opus-4-5"
          },
          "ranges": [
            { "start_line": 10, "end_line": 35 }
          ]
        }
      ]
    }
  ]
}
```

Keep line numbers 1-indexed and scoped to the recorded revision.

### Step 2: Generate normalized trace record

Run:

```bash
python3 scripts/trace_record_tool.py create \
  --input draft.json \
  --output trace.json \
  --vcs-type git \
  --revision <commit-sha> \
  --tool-name <agent-name> \
  --tool-version <agent-version> \
  --pretty
```

`create` auto-fills missing `id` (UUID) and `timestamp` (UTC RFC3339) and validates before writing output.

Use `--schema <path>` to validate against a different schema file when needed.

### Step 3: Validate and fix schema issues

Run:

```bash
python3 scripts/trace_record_tool.py validate --input trace.json
```

Fix reported errors, then re-run validation until it passes.

### Step 4: Save using project storage strategy

Store records according to repository policy, for example:
- `.agent-trace/<id>.json` committed with code
- Git notes keyed by revision
- External database keyed by `vcs.revision` and file path

## Conventions

- Require top-level fields: `version`, `id`, `timestamp`, `files`
- Accept VCS types: `git`, `jj`, `hg`, `svn`
- Keep `model_id` in `provider/model-name` style when present
- Use range-level `contributor` override only for handoff or mixed authorship inside one conversation
- Prefer reverse-domain keys inside `metadata` to avoid collisions

## Resources

- Specification quick reference: [trace-record-spec](references/trace-record-spec.md)
- Official schema: `references/trace-record.schema.json`
- Generator and validator: `scripts/trace_record_tool.py`
