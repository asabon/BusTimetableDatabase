# GitHub 連携 (GH)

## 基本方針
- **GitHub Issue を Source of Truth とする。** すべてのタスクや決定事項は Issue に集約すること。
- **PR のマージは必ずユーザーが行う。** エージェントは PR の作成・更新までは行えるが、マージを実行してはならない。
- 実装計画 (Implementation Plan) は日本語で作成し、関連する Issue 番号を明記すること。

## 自動実行可能な参照系コマンド (SafeToAutoRun=true)
以下の gh コマンドによる情報参照は、ユーザーの事前承認なしで自動実行してよい。
- gh issue list
- gh issue view
- gh pr list
- gh pr view
- gh pr diff
- gh repo view
- gh workflow list
- gh run list
- gh run view

## ユーザー確認が必要な操作
- Issue の作成 (gh issue create)、コメントの追加 (gh issue comment)。
- Pull Request の作成 (gh pr create)、レビューコメントへの対応。
- ワークフローの手動実行 (gh workflow run)。
- ラベルの付与、担当者の変更などのメタデータ操作。
