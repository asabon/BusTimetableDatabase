# 別ワークスペースへの移行 - クイックスタート

既存のAndroidアプリに神奈中バス時刻表ライブラリを組み込むための、最短手順ガイドです。

---

## 📦 準備（このリポジトリで実行）

### 1. GitHub Actions から AAR をダウンロード

1. https://github.com/asabon/BusTimeTableDatabase/actions にアクセス
2. 最新の成功した "Android Library CI" ワークフローを選択
3. "Artifacts" セクションから `client-android-release` をダウンロード
4. ZIPを解凍して `bustimetable-library-1.0.0-release.aar` を取得

### 2. ファイルをアプリのワークスペースにコピー

以下のコマンドを実行（パスは適宜変更してください）：

```powershell
# このリポジトリのルートで実行
cd c:\work\BusTimeTableDatabase

# スクリプトを実行
.\scripts\copy-to-app-workspace.ps1 `
    -AppRepoPath "D:\MyBusApp" `
    -AarFilePath "C:\Users\asabo\Downloads\bustimetable-library-1.0.0-release.aar"
```

**コピーされるファイル:**
- `docs/library/INTEGRATION_GUIDE.md` - 詳細な統合手順
- `docs/library/APP_INTEGRATION_CHECKLIST.md` - チェックリスト
- `docs/library/MIGRATION_GUIDE.md` - 移行ガイド（このファイル）
- `docs/library/API_SPEC.md` - API仕様書
- `docs/library/VERSION_MANAGEMENT.md` - バージョン管理
- `docs/library/README.md` - ライブラリの概要
- `app/libs/bustimetable-library.aar` - ライブラリ本体

---

## 🚀 作業開始（アプリのワークスペースで実行）

### 1. ワークスペースを開く

```powershell
# VS Code でアプリのリポジトリを開く
cd D:\MyBusApp
code .
```

### 2. AI に最初の指示を出す

VS Code で Antigravity を起動し、以下のように指示してください：

```
神奈中バス時刻表ライブラリを既存のAndroidアプリに組み込んで、
既存のJSONパース処理をライブラリに置き換えたいです。

以下のドキュメントを参照してください：
- docs/library/MIGRATION_GUIDE.md
- docs/library/INTEGRATION_GUIDE.md
- docs/library/API_SPEC.md

現在の状況：
1. AARファイルは app/libs/bustimetable-library.aar に配置済み
2. 既存アプリには独自のJSONパース処理がある
3. その処理をライブラリのAPIに置き換えたい

まず、docs/library/MIGRATION_GUIDE.md の
「ステップ2: 別ワークスペースでAIに指示する内容」の
「Phase 1: 環境セットアップ」から始めてください。
```

### 3. 段階的に進める

AI の指示に従って、以下の順序で作業を進めます：

1. **Phase 1: 環境セットアップ** - ライブラリの組み込み
2. **Phase 2: 既存コードの分析** - 置き換え対象の特定
3. **Phase 3: 移行計画の作成** - 具体的な手順の策定
4. **Phase 4: 実装** - 実際の置き換え作業
5. **Phase 5: クリーンアップ** - 不要コードの削除

---

## 📋 主要な置き換えパターン

### パターン1: JSONダウンロード処理

**既存コード（例）:**
```kotlin
class TimetableDownloader {
    suspend fun downloadTimetable(url: String): String {
        // OkHttpなどでダウンロード
    }
}
```

**ライブラリでの置き換え:**
```kotlin
// Application クラスで初期化
val repository = BusTimetableRepository(applicationContext)

// 使用時
repository.syncMetadata().collect { state ->
    when (state) {
        is DownloadState.Completed -> {
            // ダウンロード完了
        }
        // ...
    }
}
```

### パターン2: JSONパース処理

**既存コード（例）:**
```kotlin
class TimetableParser {
    fun parse(json: String): TimetableData {
        // JSONをパース
    }
}
```

**ライブラリでの置き換え:**
```kotlin
// ライブラリが自動的にパース
// データモデルは com.example.bustimetable.model.* を使用
```

### パターン3: 時刻表検索

**既存コード（例）:**
```kotlin
class TimetableSearcher {
    fun search(from: String, to: String): List<Timetable> {
        // 検索ロジック
    }
}
```

**ライブラリでの置き換え:**
```kotlin
val timetable = repository.getTimetableFromTo(
    fromBusstopIds = listOf("00128390"),
    toBusstopIds = listOf("00128256")
)
```

### パターン4: バス停検索

**既存コード（例）:**
```kotlin
class BusstopSearcher {
    fun searchByName(name: String): List<Busstop> {
        // 検索ロジック
    }
}
```

**ライブラリでの置き換え:**
```kotlin
val busstops = repository.findBusstopsByName("厚木")
```

---

## 🎯 重要なポイント

### ✅ DO（推奨）

1. **段階的に進める** - 一度に全てを置き換えない
2. **テストを書く** - 各段階でテストを実行
3. **ドキュメントを参照** - AI にドキュメントを見せる
4. **既存コードを保持** - 動作確認できるまで削除しない

### ❌ DON'T（非推奨）

1. **一度に全て置き換える** - リスクが高い
2. **テストなしで進める** - バグの原因
3. **ドキュメントを読まない** - 非効率
4. **既存コードをすぐ削除** - ロールバックできない

---

## 🆘 よくある質問

### Q1: 既存のデータモデルを維持したい

**A:** アダプターパターンで変換層を作成できます。詳細は `docs/library/MIGRATION_GUIDE.md` の「4-1. データモデルの変更」を参照。

### Q2: 既存のコードと並行稼働させたい

**A:** 可能です。フィーチャーフラグなどで切り替えながら段階的に移行できます。

### Q3: ビルドエラーが出た

**A:** `docs/library/APP_INTEGRATION_CHECKLIST.md` の手順を全て実行したか確認してください。

### Q4: データが取得できない

**A:** `syncMetadata()` を実行してから `getTimetableFromTo()` を呼び出してください。

---

## 📞 サポート

問題が発生した場合は、以下の情報と共に AI に質問してください：

1. 実行しようとしていた操作
2. エラーメッセージ（全文）
3. 関連するコードのスニペット
4. 既に試した解決方法

または、GitHub Issues で報告：
https://github.com/asabon/BusTimeTableDatabase/issues

---

## 📚 参考資料

- `docs/library/MIGRATION_GUIDE.md` - 詳細な移行ガイド
- `docs/library/INTEGRATION_GUIDE.md` - 統合手順
- `docs/library/API_SPEC.md` - API仕様書
- `docs/library/APP_INTEGRATION_CHECKLIST.md` - チェックリスト

---

**準備ができたら、アプリのワークスペースで AI に指示を出してください！** 🚀
