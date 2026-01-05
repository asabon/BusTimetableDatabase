---
description: .agent/AGENT.md を読み込んでエージェントを初期化する手順
---

# /init ワークフロー

このワークフローは、会話開始時に `.agent/AGENT.md` を読み込み、基本ルールを適用します。

## 実行手順

1. `.agent/AGENT.md` を読み込む。
2. ユーザーに「.agent/AGENT.md を読み込みました」と報告する。

## 完了条件

- ユーザーに完了報告をした。
