package com.example.bustimetable.exception

/**
 * ライブラリ共通の基底例外クラス
 */
open class BusTimetableException(message: String? = null, cause: Throwable? = null) : Exception(message, cause)

/**
 * 通信エラー（オフライン、タイムアウトなど）
 */
class BusTimetableNetworkException(message: String? = null, cause: Throwable? = null) : BusTimetableException(message, cause)

/**
 * データ破損、パースエラーなど
 */
class BusTimetableDataException(message: String? = null, cause: Throwable? = null) : BusTimetableException(message, cause)

/**
 * サーバー側のエラー（404 Not Foundなど）
 */
class BusTimetableServerException(val code: Int, message: String? = null, cause: Throwable? = null) : BusTimetableException(message, cause)
