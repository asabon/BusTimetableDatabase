package com.example.bustimetable.repository

import android.content.Context
import com.example.bustimetable.datasource.LocalDataSource
import com.example.bustimetable.datasource.RemoteDataSource
import com.example.bustimetable.model.*
import io.mockk.*
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import java.io.File

class BusTimetableRepositoryTest {

    private lateinit var context: Context
    private lateinit var localDataSource: LocalDataSource
    private lateinit var remoteDataSource: RemoteDataSource
    private lateinit var repository: BusTimetableRepository

    @Before
    fun setup() {
        context = mockk(relaxed = true)
        every { context.applicationContext } returns context
        
        // Use a temp directory for cacheDir to ensure file operations work
        val tempDir = java.nio.file.Files.createTempDirectory("bustimetable_test").toFile()
        tempDir.deleteOnExit()
        every { context.cacheDir } returns tempDir
        
        localDataSource = mockk(relaxed = true)
        remoteDataSource = mockk(relaxed = true)
        repository = BusTimetableRepository(context, localDataSource, remoteDataSource)
    }

    @Test
    fun `getTimetableFromTo returns merged timetable when data exists`() = runTest {
        // Arrange
        val routeId = "route1"
        val fromBusstopId = "stop1"
        val toBusstopId = "stop2"
        
        val infoRoute = InfoRoute(routeId, "hash1", listOf("stop1", "stop2"))
        val infoBusstops = InfoBusstops("hash_busstops")
        val info = Info("2023-10-27", "hash_all", infoBusstops, listOf(infoRoute))
        
        val busstop1 = Busstop(fromBusstopId, "Stop 1", "35.0", "139.0", "pos1")
        val busstop2 = Busstop(toBusstopId, "Stop 2", "35.1", "139.1", "pos2")
        val busstops = listOf(busstop1, busstop2)
        
        val routeBusstop1 = RouteBusstop("1", fromBusstopId, "Stop 1", "35.0", "139.0")
        val routeBusstop2 = RouteBusstop("2", toBusstopId, "Stop 2", "35.1", "139.1")
        val routeDetail = RouteDetail("System A", listOf(routeBusstop1, routeBusstop2), "http://route.url")
        
        val timetable = Timetable(
            date = "2023-10-01",
            name = "Stop 1",
            id = fromBusstopId,
            position = "pos1",
            system = "System A",
            destinations = listOf("Dest A"),
            weekday = listOf("10:00", "11:00"),
            saturday = listOf("10:30"),
            holiday = listOf("11:30"),
            url = "http://timetable.url"
        )

        coEvery { localDataSource.getInfo() } returns info
        coEvery { localDataSource.getBusstops() } returns busstops
        coEvery { localDataSource.getRoute(routeId) } returns routeDetail
        coEvery { localDataSource.getTimetable(routeId, "1") } returns timetable

        // Act
        val result = repository.getTimetableFromTo(
            listOf(fromBusstopId),
            listOf(toBusstopId)
        )

        // Assert
        assertEquals(DataStatus.Complete, result.dataStatus)
        assertEquals(2, result.weekday.size)
        assertEquals("10:00", result.weekday[0].time)
        assertEquals("Stop 1", result.weekday[0].fromBusstopName)
        assertEquals("Stop 2", result.weekday[0].toBusstopName)
    }

    @Test
    fun `syncIfNeeded performs sync when data is outdated`() = runTest {
        // Arrange
        val lastSyncTime = System.currentTimeMillis() - (25 * 60 * 60 * 1000) // 25 hours ago
        coEvery { localDataSource.getLastSyncTime() } returns lastSyncTime
        coEvery { remoteDataSource.downloadInfo(any()) } returns flowOf(DownloadState.Completed(null))
        coEvery { remoteDataSource.downloadBusstops(any()) } returns flowOf(DownloadState.Completed(null))
        
        // Pre-create dummy files for syncMetadata to read
        val tempDir = context.cacheDir // This returns the tempDir set in setup
        val dummyInfoJson = """{"updated_at":"2023-10-27","hash":"hash","busstops":{"hash":"h"},"routes":[]}"""
        File(tempDir, "info.json").writeText(dummyInfoJson)
        
        val dummyBusstopsJson = """{"busstops":[]}"""
        File(tempDir, "busstops.json").writeText(dummyBusstopsJson)
        
        // Mock syncDownloadedRoutes behavior
        val infoRoute = InfoRoute("route1", "hash1", listOf("stop1"))
        val infoBusstops = InfoBusstops("hash_busstops")
        val info = Info("date", "hash", infoBusstops, listOf(infoRoute))
        coEvery { localDataSource.getInfo() } returns info

        // Act
        val results = repository.syncIfNeeded().toList()

        // Assert
        assertTrue(results.last() is DownloadState.Completed)
        coVerify { remoteDataSource.downloadInfo(any()) }
        coVerify { remoteDataSource.downloadBusstops(any()) }
        coVerify { localDataSource.saveLastSyncTime(any()) }
    }
    
    @Test
    fun `syncIfNeeded skips sync when data is fresh`() = runTest {
        // Arrange
        val lastSyncTime = System.currentTimeMillis() - (1 * 60 * 60 * 1000) // 1 hour ago
        coEvery { localDataSource.getLastSyncTime() } returns lastSyncTime

        // Act
        val results = repository.syncIfNeeded().toList()

        // Assert
        assertTrue(results.last() is DownloadState.Completed)
        coVerify(exactly = 0) { remoteDataSource.downloadInfo(any()) }
    }
}
