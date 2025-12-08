# Android アプリへの組み込みチェックリスト

このチェックリストは、神奈中バス時刻表ライブラリを別のAndroidアプリに組み込む際の手順を示します。

## 📋 事前準備

- [ ] JDK 17 がインストールされている
- [ ] Android Studio がインストールされている（Arctic Fox 2020.3.1 以降）
- [ ] 対象アプリのリポジトリをクローン済み

## 🔨 ステップ1: AARファイルのビルド

### このリポジトリで実行:

```powershell
cd c:\work\BusTimeTableDatabase
.\gradlew :client:android:assembleRelease
```

- [ ] ビルドが成功した
- [ ] AARファイルが生成された: `client/android/build/outputs/aar/bustimetable-library-1.0.0-release.aar`
- [ ] ファイルサイズを確認（正常にビルドされているか）

## 📦 ステップ2: AARファイルのコピー

### 対象アプリのリポジトリで実行:

```powershell
# app/libs ディレクトリを作成（存在しない場合）
mkdir app\libs

# AARファイルをコピー
copy c:\work\BusTimeTableDatabase\client\android\build\outputs\aar\bustimetable-library-1.0.0-release.aar app\libs\bustimetable-library.aar
```

- [ ] `app/libs/` ディレクトリが作成された
- [ ] AARファイルがコピーされた
- [ ] ファイル名を `bustimetable-library.aar` に変更した

## ⚙️ ステップ3: Gradle設定の更新

### 3-1. プロジェクトレベルの `build.gradle.kts` (または `build.gradle`)

```kotlin
plugins {
    // 既存のプラグイン...
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.22" apply false
}
```

- [ ] Kotlin Serialization プラグインを追加した

### 3-2. アプリモジュールの `build.gradle.kts` (または `build.gradle`)

#### プラグイン追加:
```kotlin
plugins {
    // 既存のプラグイン...
    id("org.jetbrains.kotlin.plugin.serialization")
}
```

#### Android設定:
```kotlin
android {
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    
    kotlinOptions {
        jvmTarget = "17"
    }
}
```

#### 依存関係追加:
```kotlin
dependencies {
    // ライブラリのAAR
    implementation(files("libs/bustimetable-library.aar"))
    
    // 必須の依存関係
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("androidx.core:core-ktx:1.12.0")
}
```

- [ ] プラグインを追加した
- [ ] Java 17 の設定を追加した
- [ ] AAR の依存関係を追加した
- [ ] 必須ライブラリの依存関係を追加した

### 3-3. AndroidManifest.xml

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

- [ ] インターネット権限を追加した

### 3-4. Gradle Sync

- [ ] Android Studio で「Sync Now」をクリックした
- [ ] エラーなくSyncが完了した

## 🎯 ステップ4: Application クラスの作成

### `MyApplication.kt` を作成:

```kotlin
package com.example.yourapp  // あなたのパッケージ名に変更

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

- [ ] Application クラスを作成した
- [ ] パッケージ名を適切に変更した

### AndroidManifest.xml で指定:

```xml
<application
    android:name=".MyApplication"
    ...>
    ...
</application>
```

- [ ] Application クラスを指定した

## 🧪 ステップ5: 動作確認

### 5-1. ビルド確認

```powershell
.\gradlew assembleDebug
```

- [ ] ビルドが成功した
- [ ] エラーメッセージがない

### 5-2. 簡単な動作テスト

MainActivity などで以下のコードを追加:

```kotlin
import androidx.lifecycle.lifecycleScope
import com.example.bustimetable.BusTimetableLibrary
import kotlinx.coroutines.launch
import android.util.Log

class MainActivity : AppCompatActivity() {
    
    private val repository by lazy {
        (application as MyApplication).busTimetableRepository
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // バージョン確認
        Log.i("BusTimetable", BusTimetableLibrary.getVersionInfo())
        
        // メタデータ同期テスト
        lifecycleScope.launch {
            repository.syncMetadata().collect { state ->
                Log.d("BusTimetable", "Sync state: $state")
            }
        }
    }
}
```

- [ ] コードを追加した
- [ ] アプリを実行した
- [ ] Logcat でバージョン情報が表示された
- [ ] メタデータの同期が開始された

## 📝 ステップ6: 実装

### 基本的な使い方の実装:

参考: `INTEGRATION_GUIDE.md` の「基本的な使い方」セクション

- [ ] 時刻表検索機能を実装した
- [ ] バス停検索機能を実装した
- [ ] 定期同期機能を実装した
- [ ] エラーハンドリングを実装した
- [ ] 進捗表示を実装した

## 🚀 ステップ7: リリース準備

### ProGuard/R8 設定:

`proguard-rules.pro` に以下を追加:

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

- [ ] ProGuard ルールを追加した
- [ ] リリースビルドが成功した
- [ ] リリースビルドで動作確認した

## ✅ 完了

すべてのチェックが完了したら、ライブラリの組み込みは完了です！

## 📚 参考資料

- [統合ガイド](INTEGRATION_GUIDE.md) - 詳細な手順とサンプルコード
- [API仕様書](API_SPEC.md) - APIの詳細仕様
- [README](README.md) - ライブラリの概要

## 🆘 トラブルシューティング

問題が発生した場合は、`INTEGRATION_GUIDE.md` の「トラブルシューティング」セクションを参照してください。

## 📞 サポート

問題が解決しない場合は、GitHub Issues で報告してください:
https://github.com/asabon/BusTimeTableDatabase/issues
