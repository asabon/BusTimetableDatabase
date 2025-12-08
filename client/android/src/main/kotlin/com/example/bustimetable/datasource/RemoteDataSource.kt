package com.example.bustimetable.datasource

import com.example.bustimetable.exception.BusTimetableNetworkException
import com.example.bustimetable.exception.BusTimetableServerException
import com.example.bustimetable.model.DownloadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.IOException

class RemoteDataSource(
    private val baseUrl: String = "https://raw.githubusercontent.com/asabon/BusTimeTableDatabase/main/release/kanachu/v3"
) {
    private val client = OkHttpClient()

    /**
     * ファイルをダウンロードし、進捗を Flow で通知する
     */
    fun downloadFile(url: String, destination: File): Flow<DownloadState> = flow {
        emit(DownloadState.Idle)
        
        val request = Request.Builder().url(url).build()
        
        try {
            val response = client.newCall(request).execute()
            
            if (!response.isSuccessful) {
                throw BusTimetableServerException(
                    code = response.code,
                    message = "Server returned ${response.code} for $url"
                )
            }
            
            val body = response.body ?: throw BusTimetableNetworkException("Empty response body")
            val contentLength = body.contentLength()
            val totalBytes = if (contentLength > 0) contentLength else null
            
            destination.parentFile?.mkdirs()
            destination.outputStream().use { output ->
                body.byteStream().use { input ->
                    val buffer = ByteArray(8192)
                    var bytesRead: Int
                    var totalBytesRead = 0L
                    
                    while (input.read(buffer).also { bytesRead = it } != -1) {
                        output.write(buffer, 0, bytesRead)
                        totalBytesRead += bytesRead
                        
                        val percentage = if (totalBytes != null && totalBytes > 0) {
                            ((totalBytesRead * 100) / totalBytes).toInt()
                        } else {
                            null
                        }
                        
                        emit(DownloadState.Progress(
                            percentage = percentage,
                            currentBytes = totalBytesRead,
                            totalBytes = totalBytes,
                            message = "Downloading ${destination.name}..."
                        ))
                    }
                }
            }
            
            emit(DownloadState.Completed(destination))
        } catch (e: IOException) {
            emit(DownloadState.Error(BusTimetableNetworkException("Network error while downloading $url", e)))
        } catch (e: Exception) {
            emit(DownloadState.Error(e))
        }
    }.flowOn(Dispatchers.IO)

    /**
     * メタデータファイル (info.json) をダウンロード
     */
    fun downloadInfo(destination: File): Flow<DownloadState> {
        return downloadFile("$baseUrl/info.json", destination)
    }

    /**
     * バス停一覧 (busstops.json) をダウンロード
     */
    fun downloadBusstops(destination: File): Flow<DownloadState> {
        return downloadFile("$baseUrl/busstops.json", destination)
    }

    /**
     * 路線データ (ZIP) をダウンロード
     */
    fun downloadRoute(routeId: String, destination: File): Flow<DownloadState> = flow {
        android.util.Log.d("RemoteDataSource", "Downloading route $routeId to ${destination.absolutePath}")
        val url = "$baseUrl/routes/$routeId.zip"
        android.util.Log.d("RemoteDataSource", "Download URL: $url")

        downloadFile(url, destination).collect {
            emit(it)
        }

        if (destination.exists()) {
            android.util.Log.d("RemoteDataSource", "Download completed. File size: ${destination.length()} bytes")
        } else {
            android.util.Log.w("RemoteDataSource", "Download flow finished but file not found: ${destination.absolutePath}")
        }
    }
}
