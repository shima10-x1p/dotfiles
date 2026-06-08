---
name: split-agent-tasks
description: 要件、設計メモ、handoff、ADR、Issue、PR、実装計画を、複数のAIエージェントへ渡せる日本語のTASK-XXX形式に分割する。タスク分解、実装タスク化、作業スコープ整理、Required inputs/Optional inputs/Acceptance criteria/Test plan/AI instructions付きのタスク仕様作成、model-task-routerの判定結果をTask levelへ反映したい場合に使う。
---

# Split Agent Tasks

要件や設計情報を、実装エージェントがそのまま着手できる粒度のタスク仕様へ分割する。

出力は日本語を基本とする。コード識別子、ファイル名、モデル名、コマンド、固有名詞は原文のまま保持する。

## Workflow

1. 入力から目的、背景、制約、変更対象、触ってはいけない領域、完了条件、検証方法、依存関係を抽出する。
2. 独立して実装・レビュー・検証できる単位へ分割する。
3. 各タスクへ `TASK-001` から連番を付け、短い ASCII slug を付ける。
4. 各タスクの `Task level` を決める。
5. 下のテンプレートを使い、各タスクを自己完結した指示として書く。
6. 不明点があっても、致命的でなければ `Context`、`Requirements`、`Acceptance criteria`、または `Remaining issues` に `要確認` として明記して分解を進める。

## Splitting Rules

- 1タスクは1つの主目的に絞る。
- 依存順に並べる。基盤整備、設計確認、実装、テスト、移行、ドキュメントの順が自然ならその順にする。
- 同じファイルを複数タスクで触る場合は、競合しない順序と責務を `Context` に書く。
- 複数エージェントで並列実行できるタスクは、重ならない `Scope` に分ける。
- 調査だけで終わるタスクと、実装まで行うタスクを混ぜない。
- 大きすぎるタスクは、準備、実装、検証、移行のように分ける。
- 小さすぎるタスクは、同じ目的・同じ変更領域・同じ検証で完了できるなら統合する。

## Task Level

`Task level` には、タスク分割時のサイズ判断と `model-task-router` の結果を入れる。

- `Size`: 作業量と変更範囲で `Small`、`Medium`、`Large` のどれかを選ぶ。
- `Suggested model`: `model-task-router` の `判定` を転記する。未実行の場合は、このスキル内で同じ判断軸を使って暫定値を書く。
- `Escalate to <model name> if`: `model-task-router` の `Codex に上げる条件` または `最上位モデルに上げる条件` から、このタスクで実装者が判断停止すべき条件を3項目前後に整理する。

サイズの目安:

- `Small`: 変更範囲が明確で、主に単純作業、局所修正、テスト追加、ドキュメント更新。
- `Medium`: 複数ファイルを読み、既存設計に合わせた実装判断が必要。
- `Large`: 複数領域にまたがる、設計判断が残る、移行や互換性、運用影響を伴う。

モデル判定の目安:

- `GPT-5.4 mini`: Scope、手順、完了条件が明確で、失敗時の影響が低く、検証しやすい。
- `GPT-5.3-Codex`: コードベース調査、既存パターンへの適合、実装判断が必要。
- `GPT-5.4以上の最上位モデル`: 曖昧さの整理、設計判断、セキュリティ、認証、認可、課金、DB、移行、本番影響、公開API破壊、検証困難な変更を含む。

## Required and Optional Inputs

- `Required inputs` には、実装前に必ず読むべきファイル、ADR、handoff、Issue、仕様、既存実装を入れる。
- `Optional inputs` には、必要になった場合だけ読む補助情報を入れる。
- Required inputs を増やしすぎない。実装者が最初に読むべき最小セットにする。
- Optional inputs は、調査範囲を広げるためではなく、詰まった時の参照先として置く。

## Scope Rules

- `Change` には、このタスクで変更してよいファイルまたはディレクトリだけを書く。
- `Do not change` には、触ると責務が広がる領域、後続タスクに回す内容、破壊してはいけない前提を書く。
- Scope が曖昧な場合は、推測で広げず、狭めに切る。
- 後続タスクの先取りは禁止事項として `Non-goals` にも書く。

## Output Rules

- ユーザーがファイル作成を求めていなければ、Markdown本文としてタスク一覧を出す。
- ユーザーが保存先を指定した場合だけファイルへ書く。
- タスク数が多い場合でも、各タスクは実装者が単独で読めるようにする。
- `Result` は実装後に記入する欄なので、初期出力では見出しと空の箇条書きを残す。

## Template

各タスクは次の形式で出力する。

````markdown
# TASK-XXX: <Task title>

Slug: <task-slug>

## Task level

* Size: <Small | Medium | Large>
* Suggested model: <model-task-routerの判定または暫定判定>
* Escalate to <model name> if:

  * <上位モデルに渡す条件>
  * <判断が難しくなる条件>
  * <変更範囲が広がる条件>

## Goal

<このタスクで達成したいことを日本語で書く。>

<必要なら、このタスクが後続作業のための準備なのか、単体で完結する実装なのかも書く。>

## Scope

### Change

* `<変更してよいファイルまたはディレクトリ>`
* `<変更してよいファイルまたはディレクトリ>`

### Do not change

* `<変更してはいけないファイルまたはディレクトリ>`
* `<このタスクでは触れない実装領域>`
* `<後続タスクに回す内容>`

## Context

<現在の状態、背景、設計判断、関連するADRやhandoffの要点を書く。>

<実装者が「なぜこの変更が必要なのか」を理解できる程度に書く。>

## Required inputs

* `<必ず読むファイル>`
* `<必ず読むファイル>`

## Optional inputs

必要な場合のみ読む。

* `<補助的に読むファイル>`
* `<補助的に読むファイル>`

## Requirements

* <満たすべき具体的な要件>
* <命名、依存関係、TargetFramework、パッケージ方針など>
* <既存方針に合わせるべき点>
* <変更してはいけない前提>

## Non-goals

* <このタスクではやらないこと>
* <実装を先取りしないこと>
* <設計変更を広げないこと>

## Acceptance criteria

* [ ] <完了判定できる条件>
* [ ] <完了判定できる条件>
* [ ] <ビルド・テスト・手動確認など>

## Test plan

```bash
<実行するコマンド>
<実行するコマンド>
```

Manual checks:

* <手動で確認すること>
* <差分確認で見ること>
* <意図しない変更がないこと>

## AI instructions

* 最初に実装方針を5行以内で提示する
* Scope外のファイルを変更しない
* Optional inputs は必要になるまで読まない
* このタスクの Non-goals に含まれる実装を始めない
* 既存の命名・構成・SDK-style project conventions に従う
* 変更範囲が広がる場合は、実装を止めて理由を報告する
* ビルドが2回失敗した場合は、推測で直し続けず、原因候補を整理して報告する

## Result

実装後に記入する。

### Changed files

*

### Summary

*

### Test result

* [ ] Restore:
* [ ] Build:
* [ ] Test:
* [ ] Manual check:

### Remaining issues

*
````
