# バージョン管理ガイド

このドキュメントでは、BusTimetableLibrary のバージョン管理について説明します。

## バージョン番号の構成

バージョン番号は **セマンティックバージョニング (Semantic Versioning)** に従います：

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: 互換性のない API 変更
- **MINOR**: 後方互換性のある機能追加
- **PATCH**: 後方互換性のあるバグ修正

### 例

- `1.0.0`: 初回リリース
- `1.0.1`: バグ修正
- `1.1.0`: 新機能追加（後方互換性あり）
- `2.0.0`: 破壊的変更（後方互換性なし）

## バージョンの更新方法

### 1. build.gradle.kts の更新

`client/android/build.gradle.kts` の先頭でバージョン番号を更新します：

```kotlin
// ライブラリバージョン
val libraryVersion = "1.0.1"  // ← ここを更新
val libraryVersionCode = 2     // ← インクリメント
```

**ルール**:
- `libraryVersion`: セマンティックバージョニングに従った文字列
- `libraryVersionCode`: リリースごとに必ず +1 する整数（1から開始）

### 2. ビルドとテスト

```bash
# テストを実行
./gradlew :client:android:testDebugUnitTest

# リリースビルド
./gradlew :client:android:assembleRelease
```

### 3. 成果物の確認

生成されたAARファイル名にバージョンが含まれていることを確認：

```
client/android/build/outputs/aar/bustimetable-library-1.0.1-release.aar
```

## アプリでのバージョン確認

ライブラリを使用するアプリ側では、以下の方法でバージョンを確認できます：

### 基本的な使い方

```kotlin
import com.example.bustimetable.BusTimetableLibrary

// バージョン文字列
val version = BusTimetableLibrary.VERSION  // "1.0.0"

// バージョンコード
val versionCode = BusTimetableLibrary.VERSION_CODE  // 1

// 完全な情報
val info = BusTimetableLibrary.getVersionInfo()  // "BusTimetableLibrary v1.0.0 (1)"
```

### 実用例

#### 1. アプリ起動時のログ出力

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        Log.i("BusTimetable", BusTimetableLibrary.getVersionInfo())
    }
}
```

#### 2. バグ報告に含める

```kotlin
fun createBugReport(error: Throwable): String {
    return """
        Library: ${BusTimetableLibrary.getVersionInfo()}
        Error: ${error.message}
        Device: ${Build.MODEL}
        Android: ${Build.VERSION.RELEASE}
    """.trimIndent()
}
```

#### 3. 最小バージョンチェック

```kotlin
fun checkLibraryVersion() {
    val requiredVersionCode = 2
    if (BusTimetableLibrary.VERSION_CODE < requiredVersionCode) {
        throw IllegalStateException(
            "BusTimetableLibrary v${BusTimetableLibrary.VERSION} is too old. " +
            "Please update to version code $requiredVersionCode or higher."
        )
    }
}
```

## バージョン履歴の管理

### CHANGELOG.md の作成（推奨）

`client/android/CHANGELOG.md` を作成し、各バージョンの変更内容を記録します：

```markdown
# Changelog

## [1.0.1] - 2025-12-08

### Fixed
- baseUrl のバグを修正

## [1.0.0] - 2025-12-07

### Added
- 初回リリース
- 時刻表検索機能
- バス停検索機能
- 自動更新機能
```

## リリースプロセス

1. **バージョン番号の決定**
   - 変更内容に応じて MAJOR.MINOR.PATCH を決定

2. **build.gradle.kts の更新**
   - `libraryVersion` を更新
   - `libraryVersionCode` をインクリメント

3. **CHANGELOG.md の更新**
   - 変更内容を記録

4. **テストの実行**
   ```bash
   ./gradlew :client:android:testDebugUnitTest
   ```

5. **リリースビルド**
   ```bash
   ./gradlew :client:android:clean :client:android:assembleRelease
   ```

6. **成果物の確認**
   - AARファイル名にバージョンが含まれているか確認
   - ファイルサイズが妥当か確認

7. **Git タグの作成**
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   git push origin v1.0.1
   ```

8. **GitHub Release の作成**
   - タグからリリースを作成
   - AARファイルを添付
   - CHANGELOG の内容を記載

## トラブルシューティング

### バージョン番号が反映されない

**原因**: Gradle のキャッシュが残っている

**解決策**:
```bash
./gradlew clean
./gradlew :client:android:assembleRelease
```

### BuildConfig が生成されない

**原因**: `buildFeatures { buildConfig = true }` が設定されていない

**解決策**: `build.gradle.kts` を確認し、以下が含まれているか確認：
```kotlin
buildFeatures {
    buildConfig = true
}
```

## 参考資料

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
