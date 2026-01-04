# パフォーマンス最適化 (PERF)

## モード切り替え
- タスクの複雑度に応じて Planning / Fast モードを使い分ける。
- Artifact (task.md, plan.md) の更新は Planning モード必須。

## 効率的なファイル読み込み
- 大きなファイルは view_file_outline で構造を把握する。
- 必要な範囲のみ StartLine/EndLine で読み込む。

## キャッシュ
- セッション間の重要情報はエージェントの内部メモリや適切な永続化手段（必要に応じて提案）を活用する。
