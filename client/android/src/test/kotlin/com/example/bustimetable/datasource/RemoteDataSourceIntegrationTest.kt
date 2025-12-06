package com.example.bustimetable.datasource

import com.example.bustimetable.model.DownloadState
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Test
import java.io.File

/**
 * RemoteDataSource の統合テスト
 * 実際の HTTP 通信を行い、GitHub から正しくデータをダウンロードできることを確認する
 */
class RemoteDataSourceIntegrationTest {

    private val remoteDataSource = RemoteDataSource()

    @Test
    fun `info_json が実際にダウンロードできることを確認`() = runTest {
        // Arrange
        val tempFile = File.createTempFile("info", ".json")
        tempFile.deleteOnExit()

        // Act
        val states = remoteDataSource.downloadInfo(tempFile).toList()

        // Assert
        // 最後の状態が Completed であることを確認
        val lastState = states.last()
        assertTrue("最後の状態は Completed であるべき", lastState is DownloadState.Completed)

        // ファイルが存在し、内容があることを確認
        assertTrue("ダウンロードしたファイルが存在するべき", tempFile.exists())
        assertTrue("ファイルサイズが0より大きいべき", tempFile.length() > 0)

        // JSONとして最低限の構造を持っていることを確認
        val content = tempFile.readText()
        assertTrue("updated_at フィールドが含まれているべき", content.contains("\"updated_at\""))
        assertTrue("routes フィールドが含まれているべき", content.contains("\"routes\""))
        assertTrue("hash フィールドが含まれているべき", content.contains("\"hash\""))
    }

    @Test
    fun `busstops_json が実際にダウンロードできることを確認`() = runTest {
        // Arrange
        val tempFile = File.createTempFile("busstops", ".json")
        tempFile.deleteOnExit()

        // Act
        val states = remoteDataSource.downloadBusstops(tempFile).toList()

        // Assert
        val lastState = states.last()
        assertTrue("最後の状態は Completed であるべき", lastState is DownloadState.Completed)

        assertTrue("ダウンロードしたファイルが存在するべき", tempFile.exists())
        assertTrue("ファイルサイズが0より大きいべき", tempFile.length() > 0)

        // JSONとして最低限の構造を持っていることを確認
        val content = tempFile.readText()
        assertTrue("busstops フィールドが含まれているべき", content.contains("\"busstops\""))
    }

    @Test
    fun `存在する route の ZIP がダウンロードできることを確認`() = runTest {
        // Arrange
        // まず info.json をダウンロードして、実際に存在する route_id を取得
        val infoFile = File.createTempFile("info", ".json")
        infoFile.deleteOnExit()
        
        remoteDataSource.downloadInfo(infoFile).toList()
        
        // info.json から最初の route_id を抽出（簡易的なパース）
        val infoContent = infoFile.readText()
        val routeIdRegex = """"id"\s*:\s*"(\d+)"""".toRegex()
        val matchResult = routeIdRegex.find(infoContent)
        
        if (matchResult == null) {
            fail("info.json から route_id を取得できませんでした")
            return@runTest
        }
        
        val routeId = matchResult.groupValues[1]
        val zipFile = File.createTempFile("route_$routeId", ".zip")
        zipFile.deleteOnExit()

        // Act
        val states = remoteDataSource.downloadRoute(routeId, zipFile).toList()

        // Assert
        val lastState = states.last()
        assertTrue("最後の状態は Completed であるべき", lastState is DownloadState.Completed)

        assertTrue("ダウンロードしたファイルが存在するべき", zipFile.exists())
        assertTrue("ファイルサイズが0より大きいべき", zipFile.length() > 0)

        // ZIP ファイルのマジックナンバー（PK）を確認
        val header = zipFile.inputStream().use { it.readNBytes(2) }
        assertArrayEquals("ZIP ファイルのマジックナンバーが正しいべき", byteArrayOf(0x50, 0x4B), header)
    }

    @Test
    fun `存在しない URL へのアクセスは Error 状態を返すべき`() = runTest {
        // Arrange
        val invalidDataSource = RemoteDataSource("https://raw.githubusercontent.com/asabon/BusTimeTableDatabase/main/invalid_path")
        val tempFile = File.createTempFile("invalid", ".json")
        tempFile.deleteOnExit()

        // Act
        val states = invalidDataSource.downloadInfo(tempFile).toList()

        // Assert
        val lastState = states.last()
        assertTrue("最後の状態は Error であるべき", lastState is DownloadState.Error)
    }
}
