# Git 管理 (GIT)

## 基本方針
- コミットメッセージは日本語で記述すること。
- ブランチ名は半角英数字、ハイフン、スラッシュを使用すること（日本語禁止）。
- **commit および push 操作は原則としてユーザーが行う。エージェントは許可なくこれらの操作を実行してはならない。**

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
