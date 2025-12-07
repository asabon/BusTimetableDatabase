# Android Client Library for BusTimeTableDatabase

神奈中バス時刻表データベース v3 用の Android クライアントライブラリです。

## 概要

このライブラリは、GitHub の `release/kanachu/v3` から時刻表データをダウンロードし、Android アプリで利用するための Kotlin ライブラリです。

### 主な機能

- **オンデマンドダウンロード**: 初回起動時はメタデータのみをダウンロードし、路線データは必要になった時に自動的にダウンロード
- **自動更新**: 最後の同期から24時間以上経過している場合、自動的にデータを更新
- **差分更新**: ハッシュ値を使って変更があった路線のみを再ダウンロード
- **時刻表検索**: 複数の出発地・到着地を指定して、該当する時刻表をマージして取得

## セットアップ

### 依存関係

```kotlin
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
}
```

### 初期化

```kotlin
val repository = BusTimetableRepository(context)

// 初回起動時: メタデータをダウンロード
lifecycleScope.launch {
    repository.syncMetadata().collect { state ->
        when (state) {
            is DownloadState.Progress -> {
                // 進捗表示
            }
            is DownloadState.Completed -> {
                // ダウンロード完了
            }
            is DownloadState.Error -> {
                // エラー処理
            }
        }
    }
}
```

## 使用例

### 時刻表の検索

```kotlin
// 複数の出発地から複数の到着地への時刻表を検索
val timetable = repository.getTimetableFromTo(
    fromBusstopIds = listOf("00128390", "00128389"),
    toBusstopIds = listOf("00128256", "00128257")
)

// 平日の時刻表を表示
timetable.weekday.forEach { entry ->
    println("${entry.time} - ${entry.system} (${entry.fromBusstopName} → ${entry.toBusstopName})")
}

// データの完全性をチェック
when (timetable.dataStatus) {
    is DataStatus.Complete -> { /* 正常 */ }
    is DataStatus.MissingRoutes -> { /* 一部の路線が欠落 */ }
    is DataStatus.Outdated -> { /* データが古い */ }
}
```

### バス停の検索

```kotlin
// バス停名で検索
val busstops = repository.findBusstopsByName("厚木")

// バス停IDで検索
val busstop = repository.findBusstopById("00128390")
```

### 定期的な同期

```kotlin
// 1日1回の自動更新チェック
repository.syncIfNeeded().collect { state ->
    // 必要に応じて更新
}
```

## API 仕様

詳細な API 仕様については、[API_SPEC.md](API_SPEC.md) を参照してください。

## データ構造

このライブラリが扱うデータ構造の詳細については、プロジェクトルートの [`docs/v3/README.md`](../../docs/v3/README.md) を参照してください。

## 開発者向け情報
 
 ### 必要環境
 
 - JDK 17
 
 ### ビルドとテスト
 
 プロジェクトルート (`c:\work\BusTimeTableDatabase`) からコマンドを実行してください。
 
 #### ユニットテストの実行
 
 ```bash
 ./gradlew :client:android:testDebugUnitTest
 ```
 
 #### AAR (Android Archive) のビルド
 
 ```bash
 ./gradlew :client:android:assembleRelease
 ```
 
 ### 成果物の出力先
 
 ビルドが成功すると、成果物は以下のディレクトリに出力されます。
 
 - **AAR ファイル**: `client/android/build/outputs/aar/`
   - `bustimetable-library-release.aar`
 - **テストレポート**: `client/android/build/reports/tests/testDebugUnitTest/index.html`
 
 ## ライセンス
 
 このプロジェクトのライセンスについては、リポジトリルートの LICENSE ファイルを参照してください。
