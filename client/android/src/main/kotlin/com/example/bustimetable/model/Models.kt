package com.example.bustimetable.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

// --- JSON Data Models ---

@Serializable
data class Info(
    @SerialName("updated_at") val updatedAt: String,
    val hash: String,
    val busstops: InfoBusstops,
    val routes: List<InfoRoute>
)

@Serializable
data class InfoBusstops(
    val hash: String
)

@Serializable
data class InfoRoute(
    val id: String,
    val hash: String,
    val busstops: List<String>
)

@Serializable
data class BusstopList(
    val busstops: List<Busstop>
)

@Serializable
data class Busstop(
    @SerialName("node_id") val nodeId: String,
    val name: String,
    val lat: String,
    val lng: String,
    val position: String
)

@Serializable
data class RouteDetail(
    val system: String,
    val busstops: List<RouteBusstop>,
    @SerialName("route_url") val routeUrl: String
)

@Serializable
data class RouteBusstop(
    val index: String,
    val id: String,
    val name: String,
    val lat: String,
    val lng: String
)

@Serializable
data class Timetable(
    val date: String,
    val name: String,
    val id: String,
    val position: String,
    val system: String,
    val destinations: List<String>,
    val weekday: List<String>,
    val saturday: List<String>,
    val holiday: List<String>,
    val url: String
)

// --- API Result Models ---

data class MergedTimetable(
    val weekday: List<TimetableEntry>,
    val saturday: List<TimetableEntry>,
    val holiday: List<TimetableEntry>,
    val dataStatus: DataStatus
)

data class TimetableEntry(
    val time: String,
    val routeId: String,
    val system: String,
    val fromBusstopId: String,
    val fromBusstopName: String,
    val toBusstopId: String,
    val toBusstopName: String,
    val destination: String
)

sealed class DataStatus {
    object Complete : DataStatus()
    data class MissingRoutes(val missingRouteIds: List<String>) : DataStatus()
    data class Outdated(val outdatedRouteIds: List<String>) : DataStatus()
    data class MissingAndOutdated(
        val missingRouteIds: List<String>,
        val outdatedRouteIds: List<String>
    ) : DataStatus()
}

// --- Progress Reporting ---

sealed class DownloadState {
    object Idle : DownloadState()
    data class Progress(
        val percentage: Int?,
        val currentBytes: Long,
        val totalBytes: Long?,
        val message: String
    ) : DownloadState()
    data class Completed(val result: Any?) : DownloadState()
    data class Error(val exception: Throwable) : DownloadState()
}
