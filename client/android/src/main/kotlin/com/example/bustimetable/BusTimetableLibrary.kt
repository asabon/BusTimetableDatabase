package com.example.bustimetable

/**
 * バス時刻表ライブラリのバージョン情報を提供するオブジェクト
 */
object BusTimetableLibrary {
    /**
     * ライブラリのバージョン文字列
     * 例: "1.0.0"
     */
    val VERSION: String = BuildConfig.LIBRARY_VERSION

    /**
     * ライブラリのバージョンコード
     * 例: 1
     */
    val VERSION_CODE: Int = BuildConfig.LIBRARY_VERSION_CODE

    /**
     * ライブラリの完全な情報を文字列で返す
     * 例: "BusTimetableLibrary v1.0.0 (1)"
     */
    fun getVersionInfo(): String {
        return "BusTimetableLibrary v$VERSION ($VERSION_CODE)"
    }
}
