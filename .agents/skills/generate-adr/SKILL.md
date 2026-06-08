---
name: generate-adr
description: Create, review, split, and maintain Japanese Architectural Decision Records (ADRs). Use this skill when asked to document architectural or technical decisions, generate ADR files, review ADR quality, or split a large decision into focused ADRs.
---

# ADR Generator

Use this skill to create, review, and maintain Architectural Decision Records (ADRs).

The ADR output must be written in Japanese by default. Keep established technical terms, product names, library names, API names, and code identifiers in their original spelling when that is clearer.

## Core Principles

* Write one ADR for one architectural or technical decision.
* If the requested decision contains multiple independent topics, split it into multiple ADRs.
* Keep each ADR concise enough to be read and reviewed easily.
* Prefer several focused ADRs over one overly long ADR.
* Cross-reference related ADRs when decisions depend on each other.
* Do not hide trade-offs. Document both benefits and drawbacks.
* Use the current repository state as the source of truth.
* Avoid placeholders. If important information is unknown, ask for it before finalizing, or clearly mark the item as unresolved when drafting.

## When to Split ADRs

Split the ADR when the input includes decisions that can be accepted, rejected, implemented, or superseded independently.

Examples:

* Database selection and authentication strategy should be separate ADRs.
* API versioning and deployment strategy should be separate ADRs.
* Frontend state management and backend caching should be separate ADRs.
* Migration policy and monitoring strategy may be separate ADRs if each has its own alternatives and consequences.

When splitting, create a short plan first:

1. List the detected topics.
2. Propose one ADR title per topic.
3. Explain briefly why the split is useful.
4. Then create the ADR files.

## Required Inputs

Before creating an ADR, gather or infer the following information from the user request, repository files, issue, PR, or conversation context:

* Decision title
* Context: problem, constraints, requirements, and background
* Decision: chosen solution and rationale
* Alternatives considered
* Stakeholders: people, roles, or teams affected by the decision
* Status: default to `Proposed` unless specified

If required information is missing and cannot be inferred safely, ask a focused question before finalizing the ADR.

## ADR Numbering

1. Check the `/docs/adr/` directory for existing ADR files.
2. Determine the next sequential 4-digit ADR number.

   * Example: `0001`, `0002`, `0003`
3. If `/docs/adr/` does not exist, start with `0001`.
4. If creating multiple ADRs, assign consecutive numbers in the order of dependency or logical reading order.

## File Location

Save ADR files under:

```text
/docs/adr/
```

## File Naming

Use this naming convention:

```text
adr-NNNN-title-slug.md
```

Examples:

```text
adr-0001-database-selection.md
adr-0002-authentication-strategy.md
adr-0003-api-versioning.md
```

Slug rules:

* Use lowercase ASCII when practical.
* Replace spaces with hyphens.
* Remove symbols and punctuation.
* Keep the slug concise, ideally 3 to 5 words.
* Use stable English technical terms when they are clearer than romanized Japanese.

## ADR Template

Create each ADR using the following Markdown structure.

```markdown
---
title: "ADR-NNNN: [意思決定のタイトル]"
status: "Proposed"
date: "YYYY-MM-DD"
authors: "[関係者名または役割]"
tags: ["architecture", "decision"]
supersedes: ""
superseded_by: ""
---

# ADR-NNNN: [意思決定のタイトル]

## Status

Proposed

## Context

[この意思決定が必要になった背景を書く。問題、制約、事業要件、技術要件、既存構成、運用上の事情を簡潔に説明する。]

## Decision

[採用する方針を明確に書く。なぜその方針を選ぶのか、判断の軸も説明する。]

## Consequences

### Positive

- **POS-001**: [良い影響、利点、改善点]
- **POS-002**: [保守性、性能、拡張性、運用性などへの効果]
- **POS-003**: [設計原則やチーム方針との整合]

### Negative

- **NEG-001**: [トレードオフ、制約、欠点]
- **NEG-002**: [複雑性、技術的負債、移行コスト]
- **NEG-003**: [将来発生しうるリスク]

## Alternatives Considered

### [代替案名]

- **ALT-001**: **Description**: [代替案の概要]
- **ALT-002**: **Rejection Reason**: [採用しなかった理由]

### Do Nothing

- **ALT-003**: **Description**: 現状維持する。
- **ALT-004**: **Rejection Reason**: [現状維持では問題が解決しない理由]

## Implementation Notes

- **IMP-001**: [実装時に注意すること]
- **IMP-002**: [移行手順、ロールアウト方針]
- **IMP-003**: [監視、検証方法、成功条件]

## References

- **REF-001**: [関連ADR、Issue、PR、設計資料]
- **REF-002**: [外部ドキュメント、標準、参考資料]
```

## Writing Guidelines

* Use clear, plain Japanese.
* Avoid vague expressions such as “いい感じに”, “適切に”, “必要に応じて” unless they are immediately defined.
* Prefer concrete consequences over abstract claims.
* Include at least one positive consequence and one negative consequence.
* Include at least one rejected alternative.
* Include “Do Nothing” as an alternative when it is meaningful.
* Keep each coded item short. If one item becomes long, split it.
* Do not turn the ADR into an implementation manual. Put detailed procedures in separate documentation and reference them.
* If several implementation steps are necessary, keep only the decision-relevant notes in the ADR.
* Use `Proposed` for new ADRs unless the user or repository context indicates another status.

## Review Checklist

Before finalizing, verify:

* [ ] The ADR number is sequential.
* [ ] The file name follows `adr-NNNN-title-slug.md`.
* [ ] The file is saved under `/docs/adr/`.
* [ ] The ADR is written in Japanese.
* [ ] The ADR covers only one main topic.
* [ ] Large or independent topics have been split into separate ADRs.
* [ ] The front matter is complete.
* [ ] The status is appropriate.
* [ ] The date uses `YYYY-MM-DD`.
* [ ] The context explains why the decision is needed.
* [ ] The decision is stated clearly.
* [ ] Positive and negative consequences are both documented.
* [ ] Alternatives include rejection reasons.
* [ ] Implementation notes are actionable but not overly detailed.
* [ ] References point to related ADRs, issues, PRs, or documents where available.
* [ ] Coded items use the correct format, such as `POS-001`, `NEG-001`, `ALT-001`, `IMP-001`, and `REF-001`.
* [ ] The ADR is concise enough for review.
