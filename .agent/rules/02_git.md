# Git 運用ルール

このプロジェクトでエージェントが Git 操作を行う際の統一ルールです。

## 1. コミットメッセージ
- **形式**: [Conventional Commits](https://www.conventionalcommits.org/) (`<type>: <description>`)
- **Type**: `feat`, `fix`, `docs`, `refactor`, `chore` など
- **言語**: description は**日本語**で、簡潔かつ具体的に記述してください。
- **注意**: コミットメッセージにはプレフィックスを付けますが、最終的なリリースノートには **PR タイトル** が使用されます。[GitHub 運用ルール](./03_github.md#3-pull-request-pr-の作成) との違いに注意してください。

## 2. コミットの粒度
- 1つのコミットには、1つの論理的な変更のみを含めてください。
- 異なる目的を持つ修正は、個別にコミットしてください。

## 3. ブランチ作成
- 新しいタスクを開始する際は、必ず **`main` ブランチを最新にしてから、`main` から作業用ブランチを派生**させてください。
- GitHub Issue 番号を付与したブランチを作成してください。
- **推奨手順**: GitHub CLI (`gh issue develop`) を使用してブランチを作成すると、GitHub 上で Issue とブランチが直接紐付けられます。
  - **重要**: `--name` オプションには、必ず **"Issue番号-説明"** の形式を指定してください。
  - **コマンド例**: `gh issue develop <Issue番号> --name "<Issue番号>-kebab-case-description" --checkout`
- **命名規則**: `<Issue番号>-<kebab-case-description>`
- **アンチパターン**: `gh issue develop 17 --name "refactor-agent"` とすると、ブランチ名が `refactor-agent` になり番号が抜けるため**NG**です。
- **禁止事項**: 以下の行為は厳禁です。
  - **`main` ブランチへの直接 push**: すべての変更(ドキュメント修正を含む)は必ず作業ブランチを作成し、PR を経由してください。
  - **ブランチ名への日本語(全角文字)の使用**: 必ず英語(小文字のケバブケース)を使用してください。
    - **正**: `9-implement-discount-calculator`
    - **誤**: `9-割引計算機能の実装`

## 4. 物理的なブランチ保護 (Git Hooks)

誤って `main` ブランチに直接操作を行うことを防ぐため、リポジトリに Git Hooks を導入しています。

### セットアップ
プロジェクトをクローンした直後や、フックが機能していない場合は以下のコマンドを実行してフックを有効化してください。
```powershell
& git config core.hooksPath .hooks
```

### 機能
- **pre-commit**: `main` ブランチでの `git commit` を阻止します。
- **pre-push**: `main` ブランチからの `git push` を阻止します。

## 5. 実行権限と承認

### 許可が必要な操作 (SafeToAutoRun: false)
以下の破壊的または共有を伴う操作は、必ずユーザーの明示的な許可を得てから実行してください。
- `git commit`
- `git push`
- `git pull`
- `git branch -d / -D`

### 許可なしで実行可能な操作 (SafeToAutoRun: true)
以下の読み取り専用または非破壊的な操作は、ユーザーの承認なしに実行できます。
- `git status` / `git status --porcelain`
- `git log`
- `git diff`
- `git show`
- `git branch` (一覧表示)
- `git fetch origin`
- `git remote prune origin`
- `git remote -v`
