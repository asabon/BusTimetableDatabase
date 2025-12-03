package com.example.bustimetable.repository

import android.content.Context
import com.example.bustimetable.datasource.LocalDataSource
import com.example.bustimetable.datasource.RemoteDataSource
import com.example.bustimetable.exception.BusTimetableDataException
import com.example.bustimetable.model.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.last
import java.io.File

class BusTimetableRepository(context: Context) {
    
    private val localDataSource = LocalDataSource(context)
    private val remoteDataSource = RemoteDataSource()
    private val context = context.applicationContext

    // --- Sync APIs ---

    /**
     * メタデータのみ同期（初回起動時）
     */
    fun syncMetadata(): Flow<DownloadState> = flow {
        emit(DownloadState.Progress(null, 0, null, "Downloading metadata..."))
        
        // Download info.json
        val infoFile = File(context.cacheDir, "info.json")
        remoteDataSource.downloadInfo(infoFile).collect { state ->
            emit(state)
            if (state is DownloadState.Completed) {
                // Parse and save to local storage
                val info = kotlinx.serialization.json.Json.decodeFromString<Info>(infoFile.readText())
                localDataSource.saveInfo(info)
            }
        }
        
        // Download busstops.json
        val busstopsFile = File(context.cacheDir, "busstops.json")
        remoteDataSource.downloadBusstops(busstopsFile).collect { state ->
            emit(state)
            if (state is DownloadState.Completed) {
                // busstops.json has a root object with "busstops" key
                val busstopList = kotlinx.serialization.json.Json.decodeFromString<BusstopList>(busstopsFile.readText())
                localDataSource.saveBusstops(busstopList.busstops)
            }
        }
        
        emit(DownloadState.Completed(null))
    }

    /**
     * 必要に応じて同期（1日1回の自動更新）
     */
    fun syncIfNeeded(): Flow<DownloadState> = flow {
        val lastSyncTime = localDataSource.getLastSyncTime()
        val currentTime = System.currentTimeMillis()
        
        if (currentTime - lastSyncTime > 24 * 60 * 60 * 1000) {
            emit(DownloadState.Progress(null, 0, null, "Starting daily sync..."))
            
            // Sync metadata
            syncMetadata().collect { state ->
                if (state !is DownloadState.Completed) emit(state)
            }
            
            // Sync downloaded routes
            syncDownloadedRoutes().collect { state ->
                if (state !is DownloadState.Completed) emit(state)
            }
            
            localDataSource.saveLastSyncTime(currentTime)
            emit(DownloadState.Completed(null))
        } else {
            emit(DownloadState.Completed(null))
        }
    }

    /**
     * ダウンロード済み路線の更新チェックと同期
     */
    fun syncDownloadedRoutes(): Flow<DownloadState> = flow {
        val info = localDataSource.getInfo() ?: return@flow
        
        for (routeInfo in info.routes) {
            if (localDataSource.isRouteExists(routeInfo.id)) {
                val localHash = localDataSource.getRouteHash(routeInfo.id)
                if (localHash != routeInfo.hash) {
                    emit(DownloadState.Progress(null, 0, null, "Updating route ${routeInfo.id}..."))
                    downloadRoute(routeInfo.id).collect { state ->
                        if (state !is DownloadState.Completed) emit(state)
                    }
                }
            }
        }
        emit(DownloadState.Completed(null))
    }

    /**
     * 特定路線を明示的にダウンロード
     */
    fun downloadRoute(routeId: String): Flow<DownloadState> = flow {
        val routeZip = File(context.cacheDir, "$routeId.zip")
        remoteDataSource.downloadRoute(routeId, routeZip).collect { state ->
            emit(state)
            if (state is DownloadState.Completed) {
                try {
                    localDataSource.unzipRoute(routeId, routeZip)
                    // Delete zip file after extraction to save space
                    routeZip.delete()
                    
                    // Update hash
                    val info = localDataSource.getInfo()
                    val routeInfo = info?.routes?.find { it.id == routeId }
                    if (routeInfo != null) {
                        localDataSource.saveRouteHash(routeId, routeInfo.hash)
                    }
                } catch (e: Exception) {
                    emit(DownloadState.Error(e))
                }
            }
        }
    }

    // --- Search API ---

    /**
     * 出発バス停と到着バス停を指定して、該当する時刻表をマージして取得する
     */
    suspend fun getTimetableFromTo(
        fromBusstopIds: List<String>,
        toBusstopIds: List<String>,
        allowPartialResult: Boolean = true
    ): MergedTimetable {
        val info = localDataSource.getInfo() 
            ?: throw BusTimetableDataException("Metadata not found. Please call syncMetadata() first.")
        
        val busstops = localDataSource.getBusstops()
            ?: throw BusTimetableDataException("Busstops not found. Please call syncMetadata() first.")
        
        val busstopMap = busstops.associateBy { it.nodeId }
        
        val weekdayEntries = mutableListOf<TimetableEntry>()
        val saturdayEntries = mutableListOf<TimetableEntry>()
        val holidayEntries = mutableListOf<TimetableEntry>()
        
        val missingRoutes = mutableListOf<String>()
        val outdatedRoutes = mutableListOf<String>()
        
        // Search through all routes
        for (routeInfo in info.routes) {
            val route = localDataSource.getRoute(routeInfo.id)
            
            if (route == null) {
                // Route not downloaded yet
                if (allowPartialResult) {
                    missingRoutes.add(routeInfo.id)
                    continue
                } else {
                    // Try to download
                    try {
                        downloadRoute(routeInfo.id).last()
                        // Retry getting route
                        val downloadedRoute = localDataSource.getRoute(routeInfo.id)
                            ?: throw BusTimetableDataException("Failed to load route after download: ${routeInfo.id}")
                        processRoute(routeInfo.id, downloadedRoute, fromBusstopIds, toBusstopIds, busstopMap, weekdayEntries, saturdayEntries, holidayEntries)
                    } catch (e: Exception) {
                        if (allowPartialResult) {
                            missingRoutes.add(routeInfo.id)
                        } else {
                            throw e
                        }
                    }
                }
            } else {
                // Route exists, process it
                processRoute(routeInfo.id, route, fromBusstopIds, toBusstopIds, busstopMap, weekdayEntries, saturdayEntries, holidayEntries)
            }
        }
        
        // Sort by time
        weekdayEntries.sortBy { it.time }
        saturdayEntries.sortBy { it.time }
        holidayEntries.sortBy { it.time }
        
        // Determine data status
        val dataStatus = when {
            missingRoutes.isEmpty() && outdatedRoutes.isEmpty() -> DataStatus.Complete
            missingRoutes.isNotEmpty() && outdatedRoutes.isEmpty() -> DataStatus.MissingRoutes(missingRoutes)
            missingRoutes.isEmpty() && outdatedRoutes.isNotEmpty() -> DataStatus.Outdated(outdatedRoutes)
            else -> DataStatus.MissingAndOutdated(missingRoutes, outdatedRoutes)
        }
        
        return MergedTimetable(weekdayEntries, saturdayEntries, holidayEntries, dataStatus)
    }

    private fun processRoute(
        routeId: String,
        route: RouteDetail,
        fromBusstopIds: List<String>,
        toBusstopIds: List<String>,
        busstopMap: Map<String, Busstop>,
        weekdayEntries: MutableList<TimetableEntry>,
        saturdayEntries: MutableList<TimetableEntry>,
        holidayEntries: MutableList<TimetableEntry>
    ) {
        // Find highest priority from/to busstops in this route
        var fromIndex = -1
        var fromId: String? = null
        var fromBusstopIndexInRoute = -1 // The index property in RouteBusstop
        
        for (id in fromBusstopIds) {
            // Find the busstop in the route's busstop list
            // route.busstops is List<RouteBusstop>
            val index = route.busstops.indexOfFirst { it.id == id }
            if (index >= 0) {
                fromIndex = index
                fromId = id
                fromBusstopIndexInRoute = index
                break
            }
        }
        
        var toIndex = -1
        var toId: String? = null
        
        for (id in toBusstopIds) {
            val index = route.busstops.indexOfFirst { it.id == id }
            if (index >= 0 && index > fromIndex) {
                toIndex = index
                toId = id
                break
            }
        }
        
        if (fromIndex < 0 || toIndex < 0 || fromIndex >= toIndex) {
            // This route doesn't match the criteria
            return
        }
        
        // Load timetable for the departure busstop
        val fromRouteBusstop = route.busstops[fromBusstopIndexInRoute]
        val timetable = localDataSource.getTimetable(routeId, fromRouteBusstop.index) ?: return
        
        val fromBusstopName = busstopMap[fromId]?.name ?: "Unknown"
        val toBusstopName = busstopMap[toId]?.name ?: "Unknown"
        val destination = timetable.destinations.joinToString("・")
        
        // Helper to add entries
        fun addEntries(times: List<String>, targetList: MutableList<TimetableEntry>) {
            for (time in times) {
                targetList.add(
                    TimetableEntry(
                        time = time,
                        routeId = routeId,
                        system = timetable.system,
                        fromBusstopId = fromId!!,
                        fromBusstopName = fromBusstopName,
                        toBusstopId = toId!!,
                        toBusstopName = toBusstopName,
                        destination = destination
                    )
                )
            }
        }
        
        addEntries(timetable.weekday, weekdayEntries)
        addEntries(timetable.saturday, saturdayEntries)
        addEntries(timetable.holiday, holidayEntries)
    }

    // --- Data Retrieval APIs ---

    suspend fun getInfo(): Info {
        return localDataSource.getInfo() 
            ?: throw BusTimetableDataException("Metadata not found")
    }

    suspend fun getBusstops(): List<Busstop> {
        return localDataSource.getBusstops() 
            ?: throw BusTimetableDataException("Busstops not found")
    }

    suspend fun getRoute(routeId: String): RouteDetail {
        return localDataSource.getRoute(routeId) 
            ?: throw BusTimetableDataException("Route not found: $routeId")
    }

    suspend fun findBusstopsByName(name: String): List<Busstop> {
        val busstops = getBusstops()
        return busstops.filter { it.name.contains(name, ignoreCase = true) }
    }

    suspend fun findBusstopById(busstopId: String): Busstop? {
        val busstops = getBusstops()
        return busstops.find { it.nodeId == busstopId }
    }
}
