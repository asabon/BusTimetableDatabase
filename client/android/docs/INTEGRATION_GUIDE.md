# Android アプリへのライブラリ組み込みガイド

このガイドでは、神奈中バス時刻表データベース Android クライアントライブラリを、あなたの Android アプリに組み込む手順を説明します。

## 目次

1. [前提条件](#前提条件)
2. [方法1: AARファイルを使った組み込み（推奨）](#方法1-aarファイルを使った組み込み推奨)
3. [方法2: ソースコードを直接組み込む](#方法2-ソースコードを直接組み込む)
4. [初期設定](#初期設定)
5. [基本的な使い方](#基本的な使い方)
6. [トラブルシューティング](#トラブルシューティング)

---

## 前提条件

### 必要な環境

- **Android Studio**: Arctic Fox (2020.3.1) 以降
- **Kotlin**: 1.9.0 以降
- **minSdk**: 26 (Android 8.0) 以降
- **compileSdk**: 34 以降
- **Java**: JDK 17

### 必要な権限

アプリの `AndroidManifest.xml` にインターネット権限を追加してください：

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

## 方法1: AARファイルを使った組み込み（推奨）

この方法は、ライブラリをバイナリとして組み込むため、最もシンプルで推奨される方法です。

### ステップ1: AARファイルのビルド

このリポジトリのルートディレクトリで以下のコマンドを実行します：

```bash
cd c:\work\BusTimeTableDatabase
./gradlew :client:android:assembleRelease
```

ビルドが成功すると、以下の場所にAARファイルが生成されます：

```
client/android/build/outputs/aar/bustimetable-library-1.0.0-release.aar
```

> **注**: ファイル名にはバージョン番号（例: `1.0.0`）が含まれます。バージョンは `client/android/build.gradle.kts` で管理されています。

### ステップ2: AARファイルをプロジェクトにコピー

生成された `bustimetable-library-1.0.0-release.aar` を、あなたのAndroidプロジェクトの `app/libs/` ディレクトリにコピーします。

```bash
# 例: あなたのプロジェクトが D:\MyApp にある場合
copy client\android\build\outputs\aar\bustimetable-library-1.0.0-release.aar D:\MyApp\app\libs\bustimetable-library.aar
```

`app/libs/` ディレクトリが存在しない場合は作成してください。

### ステップ3: build.gradle.kts の設定

あなたのアプリモジュールの `build.gradle.kts` (または `build.gradle`) に以下を追加します：

#### Kotlin DSL (build.gradle.kts) の場合:

```kotlin
android {
    // ... 既存の設定 ...

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    // ライブラリのAAR
    implementation(files("libs/bustimetable-library.aar"))
    
    // 必須の依存関係
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("androidx.core:core-ktx:1.12.0")
    
    // ... その他の依存関係 ...
}
```

#### Groovy DSL (build.gradle) の場合:

```groovy
android {
    // ... 既存の設定 ...

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    
    kotlinOptions {
        jvmTarget = '17'
    }
}

dependencies {
    // ライブラリのAAR
    implementation files('libs/bustimetable-library.aar')
    
    // 必須の依存関係
    implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'androidx.core:core-ktx:1.12.0'
    
    // ... その他の依存関係 ...
}
```

### ステップ4: Kotlin Serialization プラグインの追加

プロジェクトレベルの `build.gradle.kts` (または `build.gradle`) に、Kotlin Serialization プラグインを追加します：

#### Kotlin DSL の場合:

```kotlin
plugins {
    // ... 既存のプラグイン ...
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.22" apply false
}
```

アプリモジュールの `build.gradle.kts` にも追加：

```kotlin
plugins {
    // ... 既存のプラグイン ...
    id("org.jetbrains.kotlin.plugin.serialization")
}
```

#### Groovy DSL の場合:

```groovy
plugins {
    // ... 既存のプラグイン ...
    id 'org.jetbrains.kotlin.plugin.serialization' version '1.9.22' apply false
}
```

アプリモジュールの `build.gradle` にも追加：

```groovy
plugins {
    // ... 既存のプラグイン ...
    id 'org.jetbrains.kotlin.plugin.serialization'
}
```

### ステップ5: Gradle Sync

Android Studio で「Sync Now」をクリックするか、以下のコマンドを実行します：

```bash
./gradlew --refresh-dependencies
```

---

## 方法2: ソースコードを直接組み込む

この方法は、ライブラリのソースコードを直接プロジェクトに含める場合に使用します。

### ステップ1: ライブラリモジュールをコピー

`client/android` ディレクトリ全体を、あなたのプロジェクトにコピーします：

```bash
# 例: あなたのプロジェクトが D:\MyApp にある場合
xcopy /E /I c:\work\BusTimeTableDatabase\client\android D:\MyApp\bustimetable-library
```

### ステップ2: settings.gradle.kts の設定

プロジェクトルートの `settings.gradle.kts` (または `settings.gradle`) に、モジュールを追加します：

```kotlin
include(":app")
include(":bustimetable-library")
```

### ステップ3: 依存関係の追加

アプリモジュールの `build.gradle.kts` に依存関係を追加：

```kotlin
dependencies {
    implementation(project(":bustimetable-library"))
    // ... その他の依存関係 ...
}
```

### ステップ4: Gradle Sync

Android Studio で「Sync Now」をクリックします。

---

## 初期設定

### Application クラスでの初期化（推奨）

アプリの `Application` クラスで、ライブラリのインスタンスを初期化します：

```kotlin
import android.app.Application
import com.example.bustimetable.repository.BusTimetableRepository

class MyApplication : Application() {
    
    lateinit var busTimetableRepository: BusTimetableRepository
        private set
    
    override fun onCreate() {
        super.onCreate()
        
        // リポジトリの初期化
        busTimetableRepository = BusTimetableRepository(applicationContext)
    }
}
```

`AndroidManifest.xml` で Application クラスを指定：

```xml
<application
    android:name=".MyApplication"
    ...>
    ...
</application>
```

### Activity/Fragment での使用

```kotlin
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    
    private val repository: BusTimetableRepository by lazy {
        (application as MyApplication).busTimetableRepository
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // 初回起動時: メタデータをダウンロード
        lifecycleScope.launch {
            repository.syncMetadata().collect { state ->
                when (state) {
                    is DownloadState.Progress -> {
                        // 進捗表示
                        Log.d("Download", state.message)
                    }
                    is DownloadState.Completed -> {
                        // ダウンロード完了
                        Log.d("Download", "Metadata sync completed")
                    }
                    is DownloadState.Error -> {
                        // エラー処理
                        Log.e("Download", "Error: ${state.exception.message}")
                    }
                    else -> {}
                }
            }
        }
    }
}
```

---

## 基本的な使い方

### 0. ライブラリのバージョン確認

ライブラリのバージョンを確認するには、`BusTimetableLibrary` オブジェクトを使用します：

```kotlin
import com.example.bustimetable.BusTimetableLibrary

// バージョン文字列を取得
val version = BusTimetableLibrary.VERSION  // 例: "1.0.0"

// バージョンコードを取得
val versionCode = BusTimetableLibrary.VERSION_CODE  // 例: 1

// 完全なバージョン情報を取得
val versionInfo = BusTimetableLibrary.getVersionInfo()  // 例: "BusTimetableLibrary v1.0.0 (1)"

// ログに出力
Log.d("Library", "Using $versionInfo")
```

**使用例: アプリ起動時にバージョンをログ出力**

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        
        // ライブラリバージョンをログに出力
        Log.i("BusTimetable", BusTimetableLibrary.getVersionInfo())
    }
}
```

**使用例: バグ報告時にバージョンを含める**

```kotlin
fun reportBug(errorMessage: String) {
    val report = """
        Error: $errorMessage
        Library Version: ${BusTimetableLibrary.VERSION}
        Library Version Code: ${BusTimetableLibrary.VERSION_CODE}
        Device: ${Build.MODEL}
        Android: ${Build.VERSION.RELEASE}
    """.trimIndent()
    
    // バグ報告システムに送信
    sendBugReport(report)
}
```

### 1. 時刻表の検索

```kotlin
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

lifecycleScope.launch {
    try {
        // 複数の出発地から複数の到着地への時刻表を検索
        val timetable = repository.getTimetableFromTo(
            fromBusstopIds = listOf("00128390", "00128389"),
            toBusstopIds = listOf("00128256", "00128257")
        )
        
        // データの完全性をチェック
        when (timetable.dataStatus) {
            is DataStatus.Complete -> {
                // 正常: すべてのデータが最新
                showTimetable(timetable)
            }
            is DataStatus.MissingRoutes -> {
                // 一部の路線が欠落
                val missing = (timetable.dataStatus as DataStatus.MissingRoutes).missingRouteIds
                showWarning("一部の路線が表示されていません: $missing")
                showTimetable(timetable)
            }
            is DataStatus.Outdated -> {
                // データが古い
                showWarning("データが古い可能性があります")
                showTimetable(timetable)
            }
            is DataStatus.MissingAndOutdated -> {
                // 複合的な問題
                showWarning("データに問題があります")
                showTimetable(timetable)
            }
        }
        
    } catch (e: BusTimetableNetworkException) {
        // ネットワークエラー
        showError("ネットワークエラーが発生しました")
    } catch (e: BusTimetableDataException) {
        // データエラー
        showError("データの読み込みに失敗しました")
    }
}

private fun showTimetable(timetable: MergedTimetable) {
    // 平日の時刻表を表示
    timetable.weekday.forEach { entry ->
        println("${entry.time} - ${entry.system} (${entry.fromBusstopName} → ${entry.toBusstopName})")
    }
}
```

### 2. バス停の検索

```kotlin
lifecycleScope.launch {
    // バス停名で検索（部分一致）
    val busstops = repository.findBusstopsByName("厚木")
    busstops.forEach { busstop ->
        println("${busstop.name} (ID: ${busstop.id})")
    }
    
    // バス停IDで検索
    val busstop = repository.findBusstopById("00128390")
    busstop?.let {
        println("バス停: ${it.name}")
    }
}
```

### 3. 定期的な同期（1日1回の自動更新）

```kotlin
lifecycleScope.launch {
    // アプリ起動時に実行
    repository.syncIfNeeded().collect { state ->
        when (state) {
            is DownloadState.Progress -> {
                // 更新中
                showProgressBar(state.percentage)
            }
            is DownloadState.Completed -> {
                // 更新完了（または更新不要）
                hideProgressBar()
            }
            is DownloadState.Error -> {
                // エラー（オフラインなど）
                // 既存のデータで動作を継続
                hideProgressBar()
            }
            else -> {}
        }
    }
}
```

### 4. 進捗表示の実装例

```kotlin
import com.example.bustimetable.model.DownloadState
import kotlinx.coroutines.flow.Flow

suspend fun downloadWithProgress(
    downloadFlow: Flow<DownloadState>,
    onProgress: (Int?, String) -> Unit,
    onComplete: () -> Unit,
    onError: (Throwable) -> Unit
) {
    downloadFlow.collect { state ->
        when (state) {
            is DownloadState.Idle -> {
                // 待機中
            }
            is DownloadState.Progress -> {
                // 進捗更新
                onProgress(state.percentage, state.message)
            }
            is DownloadState.Completed -> {
                // 完了
                onComplete()
            }
            is DownloadState.Error -> {
                // エラー
                onError(state.exception)
            }
        }
    }
}

// 使用例
lifecycleScope.launch {
    downloadWithProgress(
        downloadFlow = repository.syncMetadata(),
        onProgress = { percentage, message ->
            progressBar.progress = percentage ?: 0
            statusText.text = message
        },
        onComplete = {
            Toast.makeText(this@MainActivity, "同期完了", Toast.LENGTH_SHORT).show()
        },
        onError = { exception ->
            Toast.makeText(this@MainActivity, "エラー: ${exception.message}", Toast.LENGTH_LONG).show()
        }
    )
}
```

---

## トラブルシューティング

### ビルドエラー: "Unresolved reference: BusTimetableRepository"

**原因**: ライブラリが正しく組み込まれていない、または Gradle Sync が完了していない。

**解決策**:
1. Android Studio で「File」→「Sync Project with Gradle Files」を実行
2. `build.gradle.kts` の依存関係が正しく記述されているか確認
3. `libs/` ディレクトリに AAR ファイルが存在するか確認

### ビルドエラー: "kotlinx.serialization.SerializationException"

**原因**: Kotlin Serialization プラグインが適用されていない。

**解決策**:
1. プロジェクトレベルとアプリモジュールレベルの両方で、Kotlin Serialization プラグインを追加
2. Gradle Sync を実行

### 実行時エラー: "java.net.UnknownHostException"

**原因**: インターネット権限が付与されていない、またはネットワークに接続されていない。

**解決策**:
1. `AndroidManifest.xml` に `INTERNET` 権限を追加
2. デバイスがインターネットに接続されているか確認
3. エミュレータの場合、ネットワーク設定を確認

### データが取得できない

**原因**: メタデータの同期が完了していない。

**解決策**:
1. アプリ起動時に必ず `syncMetadata()` を実行
2. `syncMetadata()` が完了してから `getTimetableFromTo()` を呼び出す

```kotlin
lifecycleScope.launch {
    // まずメタデータを同期
    repository.syncMetadata().collect { state ->
        if (state is DownloadState.Completed) {
            // 同期完了後に時刻表を取得
            val timetable = repository.getTimetableFromTo(
                fromBusstopIds = listOf("00128390"),
                toBusstopIds = listOf("00128256")
            )
            showTimetable(timetable)
        }
    }
}
```

### ProGuard/R8 の設定

リリースビルドで ProGuard/R8 を使用する場合、以下のルールを `proguard-rules.pro` に追加してください：

```proguard
# Kotlin Serialization
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt

-keepclassmembers class kotlinx.serialization.json.** {
    *** Companion;
}
-keepclasseswithmembers class kotlinx.serialization.json.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
-keepnames class okhttp3.internal.publicsuffix.PublicSuffixDatabase

# BusTimetable Library
-keep class com.example.bustimetable.model.** { *; }
-keep class com.example.bustimetable.repository.** { *; }
```

---

## 参考資料

- [API 仕様書](API_SPEC.md)
- [README](../README.md)
- [データ構造ドキュメント](../../../docs/v3/README.md)

---

## サポート

問題が発生した場合は、GitHub Issues で報告してください：
https://github.com/asabon/BusTimeTableDatabase/issues
