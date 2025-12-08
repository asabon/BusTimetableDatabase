# 既存Androidアプリへのライブラリ移行ガイド

このガイドは、既存のAndroidアプリで独自にJSONパース処理を実装している場合に、神奈中バス時刻表ライブラリに移行する手順を説明します。

---

## 📋 前提条件

- ✅ 既存アプリには独自のJSONパース処理がある
- ✅ AARファイルはGitHub Actionsからダウンロード済み
- ✅ 別ワークスペースで作業を行う

---

## 📦 ステップ1: 必要なファイルを別ワークスペースにコピー

### 1-1. コピーするファイル一覧

別ワークスペース（アプリのリポジトリ）のルートに、以下のディレクトリを作成してファイルをコピーします：

```
[アプリのリポジトリ]/
├── docs/
│   └── library/
│       ├── INTEGRATION_GUIDE.md          ← コピー
│       ├── APP_INTEGRATION_CHECKLIST.md  ← コピー
│       ├── MIGRATION_GUIDE.md            ← コピー（このファイル）
│       ├── API_SPEC.md                   ← コピー
│       └── VERSION_MANAGEMENT.md         ← コピー（オプション）
└── app/
    └── libs/
        └── bustimetable-library.aar      ← GitHub Actionsからダウンロード
```

### 1-2. コピーコマンド（PowerShell）

```powershell
# アプリのリポジトリのパスを設定（例）
$APP_REPO = "D:\MyBusApp"

# ドキュメント用ディレクトリを作成
New-Item -ItemType Directory -Force -Path "$APP_REPO\docs\library"

# 必要なドキュメントをコピー
Copy-Item "c:\work\BusTimeTableDatabase\client\android\docs\INTEGRATION_GUIDE.md" "$APP_REPO\docs\library\"
Copy-Item "c:\work\BusTimeTableDatabase\client\android\docs\APP_INTEGRATION_CHECKLIST.md" "$APP_REPO\docs\library\"
Copy-Item "c:\work\BusTimeTableDatabase\client\android\docs\MIGRATION_GUIDE.md" "$APP_REPO\docs\library\"
Copy-Item "c:\work\BusTimeTableDatabase\client\android\docs\API_SPEC.md" "$APP_REPO\docs\library\"
Copy-Item "c:\work\BusTimeTableDatabase\client\android\docs\VERSION_MANAGEMENT.md" "$APP_REPO\docs\library\"

# app/libs ディレクトリを作成
New-Item -ItemType Directory -Force -Path "$APP_REPO\app\libs"

# GitHub ActionsからダウンロードしたAARファイルをコピー
# （ダウンロード先のパスは適宜変更してください）
Copy-Item "C:\Users\asabo\Downloads\bustimetable-library-1.0.0-release.aar" "$APP_REPO\app\libs\bustimetable-library.aar"
```

---

## 🤖 ステップ2: 別ワークスペースでAIに指示する内容

### 2-1. ワークスペースを開く

1. VS Code（またはAndroid Studio）で、アプリのリポジトリを開く
2. AIアシスタント（Antigravity）を起動

### 2-2. 最初の指示（コンテキスト共有）

以下のように指示してください：

```
神奈中バス時刻表ライブラリを既存のAndroidアプリに組み込んで、
既存のJSONパース処理をライブラリに置き換えたいです。

以下のドキュメントを参照してください：
- docs/library/INTEGRATION_GUIDE.md
- docs/library/API_SPEC.md
- docs/library/MIGRATION_GUIDE.md

現在の状況：
1. AARファイルは app/libs/bustimetable-library.aar に配置済み
2. 既存アプリには独自のJSONパース処理がある
3. その処理をライブラリのAPIに置き換えたい

まず、既存のJSONパース処理のコードを確認してもらえますか？
以下のファイルを見てください：
- [既存のJSONパース処理があるファイルのパス]
```

### 2-3. 段階的な指示の流れ

#### **Phase 1: 環境セットアップ**

```
ステップ1: ライブラリの組み込み

docs/library/APP_INTEGRATION_CHECKLIST.md の
「ステップ3: Gradle設定の更新」を参考に、
以下を実装してください：

1. build.gradle.kts にライブラリの依存関係を追加
2. 必要なプラグインと依存関係を追加
3. AndroidManifest.xml にインターネット権限を追加
4. Application クラスを作成してリポジトリを初期化

完了したらビルドして、エラーがないか確認してください。
```

#### **Phase 2: 既存コードの分析**

```
ステップ2: 既存コードの分析

以下のファイルを分析して、ライブラリのAPIに置き換え可能な箇所を
リストアップしてください：

- [既存のJSONパース処理のファイル1]
- [既存のJSONパース処理のファイル2]
- [データモデルのファイル]

特に以下の処理を確認してください：
1. JSONのダウンロード処理
2. JSONのパース処理
3. データの保存・キャッシュ処理
4. 時刻表の検索処理
5. バス停の検索処理

それぞれについて、ライブラリのどのAPIで置き換えられるか提案してください。
```

#### **Phase 3: 移行計画の作成**

```
ステップ3: 移行計画の作成

既存コードの分析結果を元に、以下の移行計画を作成してください：

1. 置き換え対象のクラス・メソッドのリスト
2. 各クラス・メソッドをライブラリのどのAPIで置き換えるか
3. 移行の順序（依存関係を考慮）
4. 後方互換性の維持方法（段階的移行の場合）
5. テスト計画

計画を Markdown 形式で docs/migration_plan.md に出力してください。
```

#### **Phase 4: 実装**

```
ステップ4: 実装

docs/migration_plan.md に従って、以下の順序で実装してください：

1. [最初に置き換えるクラス名] をライブラリのAPIに置き換え
2. [次に置き換えるクラス名] をライブラリのAPIに置き換え
3. ...

各ステップで：
- 既存のコードをコメントアウト
- ライブラリのAPIを使った新しいコードを実装
- ビルドして動作確認
- 問題があれば修正

実装が完了したら、全体的な動作確認を行ってください。
```

#### **Phase 5: クリーンアップ**

```
ステップ5: クリーンアップ

1. 使用されなくなった既存のコードを削除
2. 不要な依存関係を削除
3. コードのリファクタリング
4. ドキュメントの更新

完了したら、最終的なビルドとテストを実行してください。
```

---

## 🔍 ステップ3: 既存コードの確認ポイント

AIに分析してもらう際、以下のポイントを確認してもらってください：

### 3-1. データダウンロード処理

**既存コードで確認すべき点：**
- どのURLからデータをダウンロードしているか
- ダウンロードの頻度・タイミング
- キャッシュの仕組み
- エラーハンドリング

**ライブラリでの置き換え：**
```kotlin
// 既存: 独自のダウンロード処理
// ↓
// 新規: ライブラリのAPI
repository.syncMetadata()  // メタデータの同期
repository.syncIfNeeded()  // 必要に応じて自動更新
```

### 3-2. JSONパース処理

**既存コードで確認すべき点：**
- どのJSONファイルをパースしているか（info.json, busstops.json, routes/*.json）
- データモデルの構造
- パースエラーのハンドリング

**ライブラリでの置き換え：**
```kotlin
// 既存: 独自のJSONパース
// ↓
// 新規: ライブラリが自動的にパース
// データモデルは com.example.bustimetable.model.* を使用
```

### 3-3. 時刻表検索処理

**既存コードで確認すべき点：**
- 検索条件（出発地、目的地）
- 検索ロジック
- 結果のフォーマット

**ライブラリでの置き換え：**
```kotlin
// 既存: 独自の検索ロジック
// ↓
// 新規: ライブラリのAPI
val timetable = repository.getTimetableFromTo(
    fromBusstopIds = listOf("00128390"),
    toBusstopIds = listOf("00128256")
)
```

### 3-4. バス停検索処理

**既存コードで確認すべき点：**
- 検索方法（名前検索、ID検索）
- 検索結果の使用方法

**ライブラリでの置き換え：**
```kotlin
// 既存: 独自の検索ロジック
// ↓
// 新規: ライブラリのAPI
val busstops = repository.findBusstopsByName("厚木")
val busstop = repository.findBusstopById("00128390")
```

---

## 📝 ステップ4: 移行時の注意点

### 4-1. データモデルの変更

既存のデータモデルとライブラリのデータモデルが異なる場合：

**オプション1: ライブラリのモデルをそのまま使用（推奨）**
```kotlin
// 既存のUIコードを、ライブラリのモデルに合わせて修正
import com.example.bustimetable.model.*
```

**オプション2: アダプターパターンで変換**
```kotlin
// 既存のモデルを維持し、ライブラリのモデルから変換
fun MergedTimetable.toExistingModel(): ExistingTimetableModel {
    return ExistingTimetableModel(
        // 変換処理
    )
}
```

### 4-2. 非同期処理の変更

既存のコードが異なる非同期処理を使用している場合：

**既存: RxJava の場合**
```kotlin
// ライブラリのFlowをRxJavaに変換
repository.syncMetadata()
    .asObservable()  // または適切な変換
```

**既存: LiveData の場合**
```kotlin
// ライブラリのFlowをLiveDataに変換
repository.syncMetadata()
    .asLiveData()
```

### 4-3. エラーハンドリングの統一

ライブラリの例外を既存のエラーハンドリングに統合：

```kotlin
try {
    val timetable = repository.getTimetableFromTo(...)
} catch (e: BusTimetableNetworkException) {
    // 既存のネットワークエラー処理に統合
    handleNetworkError(e)
} catch (e: BusTimetableDataException) {
    // 既存のデータエラー処理に統合
    handleDataError(e)
}
```

---

## 🧪 ステップ5: テスト計画

### 5-1. 単体テスト

既存の単体テストを更新：
```kotlin
// 既存のテストをライブラリのAPIに合わせて修正
@Test
fun testTimetableSearch() {
    // モックの設定
    // ライブラリのAPIを使ったテスト
}
```

### 5-2. 統合テスト

実際のデータでの動作確認：
- [ ] メタデータのダウンロード
- [ ] 時刻表の検索
- [ ] バス停の検索
- [ ] データの更新

### 5-3. UIテスト

既存のUIテストが正常に動作するか確認：
- [ ] 検索画面
- [ ] 結果表示画面
- [ ] エラー表示

---

## 📊 ステップ6: 移行完了チェックリスト

- [ ] ライブラリの組み込みが完了
- [ ] 既存のJSONダウンロード処理を削除
- [ ] 既存のJSONパース処理を削除
- [ ] 既存の検索処理をライブラリのAPIに置き換え
- [ ] データモデルの移行が完了
- [ ] エラーハンドリングの統合が完了
- [ ] 単体テストが全て通過
- [ ] 統合テストが全て通過
- [ ] UIテストが全て通過
- [ ] ビルドサイズの変化を確認
- [ ] パフォーマンスの変化を確認
- [ ] ドキュメントの更新

---

## 🆘 トラブルシューティング

### 問題: ビルドエラーが発生する

**確認事項：**
1. `docs/library/APP_INTEGRATION_CHECKLIST.md` の手順を全て実行したか
2. Gradle Sync が完了しているか
3. 依存関係のバージョンが正しいか

### 問題: データが取得できない

**確認事項：**
1. `syncMetadata()` を実行したか
2. インターネット接続があるか
3. エラーログを確認

### 問題: 既存のコードとの互換性がない

**対処法：**
1. アダプターパターンで変換層を作成
2. 段階的に移行（既存コードとライブラリを並行稼働）
3. AIに具体的なコードを見せて相談

---

## 📚 参考資料

- `docs/library/INTEGRATION_GUIDE.md` - 詳細な統合手順
- `docs/library/API_SPEC.md` - APIの詳細仕様
- `docs/library/APP_INTEGRATION_CHECKLIST.md` - チェックリスト

---

## 💡 ヒント

### AIとの効果的なコミュニケーション

1. **具体的なファイルパスを示す**
   ```
   ❌ 「既存のコードを見てください」
   ✅ 「app/src/main/java/com/example/myapp/data/TimetableParser.kt を見てください」
   ```

2. **段階的に進める**
   ```
   ❌ 「全部置き換えてください」
   ✅ 「まず TimetableParser クラスだけを置き換えてください」
   ```

3. **エラーは全文を共有**
   ```
   ❌ 「ビルドエラーが出ました」
   ✅ 「以下のビルドエラーが出ました：[エラーメッセージ全文]」
   ```

4. **ドキュメントを参照させる**
   ```
   ✅ 「docs/library/API_SPEC.md の getTimetableFromTo の使い方を参考に実装してください」
   ```

---

## 🎯 成功のポイント

1. **段階的に進める**: 一度に全てを置き換えず、機能ごとに移行
2. **テストを書く**: 各段階でテストを実行して動作を確認
3. **ドキュメントを活用**: AIにドキュメントを参照させる
4. **既存コードを保持**: 完全に動作確認できるまで既存コードを削除しない
5. **AIに質問**: 不明点があれば具体的に質問する

---

## 📞 サポート

問題が発生した場合は、以下の情報と共に質問してください：

1. 実行しようとしていた操作
2. エラーメッセージ（全文）
3. 関連するコードのスニペット
4. 既に試した解決方法

GitHub Issues:
https://github.com/asabon/BusTimeTableDatabase/issues
