# Git 管理

## 基本方針
- **`github-dev-flow` スキルの手順に従うこと。**
- コミットメッセージは日本語で記述すること。
- ブランチ名は半角英数字、ハイフン、スラッシュを使用すること（日本語禁止）。
- **push 操作は原則としてスキルの手順（PR作成直前）においてのみ実行する。** それ以外のタイミングでの自動 push は避けること。

## 自動実行可能な参照系コマンド (SafeToAutoRun=true)
以下の参照系コマンドは、ユーザーの事前承認なしで自動実行してよい。
- git status
- git log
- git diff
- git show
- git branch
- git remote -v
- git config --list

## ユーザー確認が必要な操作
- ファイルの変更、ステージング (git add)。
- ブランチの作成・切り替え・削除。
- 破壊的操作 (git reset --hard, git clean 等)。
