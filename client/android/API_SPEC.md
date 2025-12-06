# Android クライアントライブラリ API 仕様

## 概要

GitHub の `release/kanachu/v3` から時刻表データをダウンロードし、Android アプリで利用するための Kotlin ライブラリの API 仕様。
汎用的な設計とし、データソースを差し替えることで他社のバス時刻表にも対応可能とする。

## 主要 API

### 1. 時刻表検索 API

#### `getTimetableFromTo()`

出発バス停と到着バス停を指定して、該当する時刻表をマージして取得する。
必要なデータがローカルにない場合は自動的にダウンロードを試みる。

```kotlin
suspend fun getTimetableFromTo(
    fromBusstopIds: List<String>,  // 出発バス停IDのリスト（優先度順）
    toBusstopIds: List<String>,    // 到着バス停IDのリスト（優先度順）
    allowPartialResult: Boolean = true // データ不足時でも可能な範囲で結果を返すか
): MergedTimetable
```

**パラメータ**:
- `fromBusstopIds`: 出発バス停IDのリスト。複数指定可能。リストの先頭に近いほど優先度が高い。
- `toBusstopIds`: 到着バス停IDのリスト。複数指定可能。リストの先頭に近いほど優先度が高い。
- `allowPartialResult`: `true` (デフォルト) の場合、一部のデータが欠落していてもエラーにせず、取得できた範囲で結果を返す。

**戻り値**:
```kotlin
data class MergedTimetable(
    val weekday: List<TimetableEntry>,   // 平日の時刻表（時刻順ソート済み）
    val saturday: List<TimetableEntry>,  // 土曜の時刻表（時刻順ソート済み）
    val holiday: List<TimetableEntry>,   // 休日の時刻表（時刻順ソート済み）
    val dataStatus: DataStatus           // データの完全性ステータス
)

data class TimetableEntry(
    val time: String,              // 発車時刻 (例: "6:35")
    val routeId: String,           // 路線ID (例: "0000800009")
    val system: String,            // 系統名 (例: "厚74")
    val fromBusstopId: String,     // 実際の出発バス停ID
    val fromBusstopName: String,   // 実際の出発バス停名
    val toBusstopId: String,       // 実際の到着バス停ID
    val toBusstopName: String,     // 実際の到着バス停名
    val destination: String        // 最終目的地
)

sealed class DataStatus {
    // 全て最新、またはオフラインだが全て揃っている（理想的な状態）
    object Complete : DataStatus()

    // 一部の路線データが欠落しており、ダウンロードもできなかった
    // (結果リストには、存在する路線の時刻表のみが含まれる)
    data class MissingRoutes(val missingRouteIds: List<String>) : DataStatus()

    // 全てのデータは揃っているが、サーバー上に新しい更新があるのにダウンロードできなかった
    // (結果リストには、手元の古いデータに基づく時刻表が含まれる)
    data class Outdated(val outdatedRouteIds: List<String>) : DataStatus()
    
    // 欠落もあり、かつ古いデータも混ざっている複合ケース
    data class MissingAndOutdated(
        val missingRouteIds: List<String>,
        val outdatedRouteIds: List<String>
    ) : DataStatus()
}
```

**検索ロジック**:

1. 全路線を走査（`info.json` から）
2. 各路線の `busstops` リストに含まれる出発バス停と到着バス停を特定
3. **優先度ルール**: 同じ路線内に複数の出発バス停が含まれる場合、`fromBusstopIds` リストの先頭に近い（優先度が高い）バス停のみを採用
4. 同様に、複数の到着バス停が含まれる場合も、`toBusstopIds` リストの先頭に近いバス停を採用
5. 出発バス停のインデックス < 到着バス停のインデックス であることを確認（正しい方向）
6. **該当する路線がローカルにない場合、自動的にダウンロード**
7. 該当する路線の出発バス停の時刻表を取得
8. 全ての時刻表をマージし、時刻順にソート
9. 通信エラー等でダウンロードできなかった場合、`allowPartialResult` に応じて `DataStatus` を設定して返すか、例外を投げる

**使用例**:

```kotlin
// 例: 複数の出発地から複数の到着地への時刻表を検索
val timetable = repository.getTimetableFromTo(
    fromBusstopIds = listOf("00128390", "00128389", "00128388"),
    toBusstopIds = listOf("00128256", "00128257")
)

// ステータスチェック
when (timetable.dataStatus) {
    is DataStatus.Complete -> { /* 正常表示 */ }
    is DataStatus.MissingRoutes -> { showWarning("一部の路線が表示されていません") }
    is DataStatus.Outdated -> { showWarning("データが古い可能性があります") }
    // ...
}

// 平日の時刻表を表示
timetable.weekday.forEach { entry ->
    println("${entry.time} - ${entry.system} (${entry.fromBusstopName} → ${entry.toBusstopName})")
}
```

---

## その他の基本 API

### データ同期・ダウンロード（Flow 対応）

進捗状況をリアルタイムに取得するため、ダウンロード系 API は `Flow` を返す。

```kotlin
// ダウンロードの状態
sealed class DownloadState {
    object Idle : DownloadState()
    data class Progress(
        val percentage: Int?,      // わかれば 0-100、わからなければ null (不確定)
        val currentBytes: Long,    // 受信済みバイト数
        val totalBytes: Long?,     // 全体バイト数 (不明なら null)
        val message: String        // ユーザー向けメッセージ
    ) : DownloadState()
    data class Completed(val result: Any?) : DownloadState()
    data class Error(val exception: Throwable) : DownloadState()
}

// メタデータのみ同期（初回起動時）
fun syncMetadata(): Flow<DownloadState>

// 必要に応じて同期（1日1回の自動更新）
fun syncIfNeeded(): Flow<DownloadState>

// ダウンロード済み路線の更新チェックと同期
fun syncDownloadedRoutes(): Flow<DownloadState>

// 特定路線を明示的にダウンロード
fun downloadRoute(routeId: String): Flow<DownloadState>
```

**`syncIfNeeded()` の動作**:
- 最後の同期から24時間以上経過している場合のみ、ダウンロード済み路線を更新
- それ以外の場合は `DownloadState.Completed` を即座に流して終了（通信なし）

### データ取得

```kotlin
// メタ情報取得
suspend fun getInfo(): Info

// バス停一覧取得
suspend fun getBusstops(): List<Busstop>

// 路線情報取得
suspend fun getRoute(routeId: String): RouteDetail

// 時刻表取得（路線ID + バス停インデックス）
suspend fun getTimetable(routeId: String, index: Int): Timetable
```

### バス停検索

```kotlin
// バス停名からバス停情報を検索（部分一致）
suspend fun findBusstopsByName(name: String): List<Busstop>

// バス停IDからバス停情報を取得
suspend fun findBusstopById(busstopId: String): Busstop?
```

---

## 例外クラス

エラーハンドリングを容易にするため、独自の例外クラスを定義する。

- `BusTimetableNetworkException`: 通信エラー（オフライン、タイムアウトなど）
- `BusTimetableDataException`: データ破損、パースエラーなど
- `BusTimetableServerException`: サーバー側のエラー（404 Not Foundなど）

---

## 実装上の注意点

1. **非同期処理**: すべての API は `suspend fun` または `Flow` として実装し、Kotlin Coroutines で非同期実行
2. **オンデマンドダウンロード**: 
    - 初回起動時はメタデータ（info.json, busstops.json）のみダウンロード
    - 路線データは必要になった時に自動的にダウンロード
    - ダウンロード済みの路線はローカルにキャッシュ
3. **自動更新**: 
    - `syncIfNeeded()` は最後の同期から24時間以上経過している場合のみ実行
4. **差分更新**: ハッシュ値を使って変更があったダウンロード済み路線のみを再ダウンロード
5. **透過的なダウンロード**: `getTimetableFromTo()` などのAPI呼び出し時、必要な路線が自動的にダウンロードされ、常に最新のキャッシュデータが返される
6. **エラーハンドリング**: 定義した独自例外を使用し、呼び出し元で適切な処理ができるようにする

