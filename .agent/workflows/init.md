---
description: Initialize session by loading .antigravity.yml and creating rules summary
---

# Session Initialization

このワークフローは、会話開始時に `.antigravity.yml` を読み込み、ルールサマリーを作成します。

## 実行手順

1. `.antigravity.yml` を読み込む
2. `.work/cache/` ディレクトリが存在しない場合は作成
3. `.work/cache/rules_summary.md` にルールサマリーを作成（50行程度）
   - 各セクションの重要ルールのみを抽出
   - セクション構成:
     - 基本ルール (GEN, RULE)
     - プロジェクト理解 (PRJ)
     - パフォーマンス最適化 (PERF, CACHE, FILE, RESP, BATCH, HIST)
     - GitHub Issue 管理 (PLN, ISS, SYNC, PLAN, WORK, TSK)
     - データベースファイル取り扱い (DATA)
     - コーディング規約 (COD)
4. ユーザーに「.antigravity.yml を読み込み、サマリーを作成しました」と報告

## 完了条件

- `.work/cache/rules_summary.md` が作成されている
- ユーザーに完了報告をした
