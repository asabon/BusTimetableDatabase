package com.example.bustimetable.datasource

import android.content.Context
import com.example.bustimetable.exception.BusTimetableDataException
import com.example.bustimetable.model.*
import kotlinx.serialization.json.Json
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.util.zip.ZipInputStream

class LocalDataSource(private val context: Context) {

    private val json = Json { ignoreUnknownKeys = true }
    private val cacheDir: File by lazy { File(context.filesDir, "bustimetable_v3") }

    init {
        if (!cacheDir.exists()) {
            cacheDir.mkdirs()
        }
    }

    // --- Info (Metadata) ---

    fun saveInfo(info: Info) {
        val file = File(cacheDir, "info.json")
        file.writeText(json.encodeToString(Info.serializer(), info))
    }

    fun getInfo(): Info? {
        val file = File(cacheDir, "info.json")
        if (!file.exists()) return null
        return try {
            json.decodeFromString(Info.serializer(), file.readText())
        } catch (e: Exception) {
            throw BusTimetableDataException("Failed to parse info.json", e)
        }
    }

    // --- Busstops ---

    fun saveBusstops(busstops: List<Busstop>) {
        val file = File(cacheDir, "busstops.json")
        val busstopList = BusstopList(busstops)
        file.writeText(json.encodeToString(BusstopList.serializer(), busstopList))
    }

    fun getBusstops(): List<Busstop>? {
        val file = File(cacheDir, "busstops.json")
        if (!file.exists()) return null
        return try {
            val busstopList = json.decodeFromString(BusstopList.serializer(), file.readText())
            busstopList.busstops
        } catch (e: Exception) {
            throw BusTimetableDataException("Failed to parse busstops.json", e)
        }
    }

    // --- Routes ---

    fun saveRoute(routeId: String, routeDetail: RouteDetail) {
        val routeDir = File(cacheDir, "routes/$routeId")
        if (!routeDir.exists()) routeDir.mkdirs()
        val file = File(routeDir, "route.json")
        file.writeText(json.encodeToString(RouteDetail.serializer(), routeDetail))
    }

    fun getRoute(routeId: String): RouteDetail? {
        val file = File(cacheDir, "routes/$routeId/route.json")
        android.util.Log.d("LocalDataSource", "getRoute($routeId): Looking for ${file.absolutePath}")
        android.util.Log.d("LocalDataSource", "File exists: ${file.exists()}")
        if (!file.exists()) {
            val routeDir = File(cacheDir, "routes/$routeId")
            if (routeDir.exists()) {
                val filesInDir = routeDir.listFiles()?.joinToString(", ") { it.name } ?: "no files"
                android.util.Log.d("LocalDataSource", "Route dir exists but route.json not found. Files: $filesInDir")
            } else {
                android.util.Log.d("LocalDataSource", "Route directory does not exist: ${routeDir.absolutePath}")
            }
            return null
        }
        return try {
            json.decodeFromString(RouteDetail.serializer(), file.readText())
        } catch (e: Exception) {
            throw BusTimetableDataException("Failed to parse route.json for $routeId", e)
        }
    }
    
    fun isRouteExists(routeId: String): Boolean {
        return File(cacheDir, "routes/$routeId/route.json").exists()
    }

    fun unzipRoute(routeId: String, zipFile: File) {
        val routeDir = getRouteDir(routeId)
        // Clear existing files
        routeDir.deleteRecursively()
        routeDir.mkdirs()

        android.util.Log.d("LocalDataSource", "Unzipping route $routeId from ${zipFile.absolutePath} to ${routeDir.absolutePath}")
        android.util.Log.d("LocalDataSource", "ZIP file exists: ${zipFile.exists()}, size: ${zipFile.length()} bytes")

        try {
            var fileCount = 0
            ZipInputStream(FileInputStream(zipFile)).use { zis ->
                var entry = zis.nextEntry
                while (entry != null) {
                    val file = File(routeDir, entry.name)
                    android.util.Log.d("LocalDataSource", "Extracting: ${entry.name} -> ${file.absolutePath}, isDirectory: ${entry.isDirectory}")
                    if (entry.isDirectory) {
                        file.mkdirs()
                    } else {
                        file.parentFile?.mkdirs()
                        FileOutputStream(file).use { fos ->
                            val buffer = ByteArray(8192)
                            var len: Int
                            while (zis.read(buffer).also { len = it } > 0) {
                                fos.write(buffer, 0, len)
                            }
                        }
                        android.util.Log.d("LocalDataSource", "Extracted file: ${file.name}, size: ${file.length()} bytes")
                        fileCount++
                    }
                    entry = zis.nextEntry
                }
            }
            android.util.Log.d("LocalDataSource", "Unzip completed. Extracted $fileCount files")
            val routeJsonFile = File(routeDir, "route.json")
            if (routeJsonFile.exists()) {
                android.util.Log.d("LocalDataSource", "route.json verified at ${routeJsonFile.absolutePath}, size: ${routeJsonFile.length()} bytes")
            } else {
                val filesInDir = routeDir.listFiles()?.joinToString(", ") { it.name } ?: "no files"
                android.util.Log.e("LocalDataSource", "route.json not found after unzip for route $routeId. Files in dir: $filesInDir")
                throw BusTimetableDataException("route.json not found after unzip for route $routeId. Files in dir: $filesInDir")
            }
        } catch (e: Exception) {
            android.util.Log.e("LocalDataSource", "Failed to unzip route $routeId", e)
            throw BusTimetableDataException("Failed to unzip route $routeId: ${e.message}", e)
        }
    }

    fun getTimetable(routeId: String, index: String): Timetable? {
        // Filename is like "01.json" or "1.json". The index from RouteBusstop is a string.
        // Usually it is padded or not? The example shows "01.json".
        // Let's try to match the filename.
        // The index in RouteBusstop is "1".
        // The file in example is "01.json".
        // I should probably try both or check if padding is needed.
        // Based on docs/v3/README.md: "01.json : 時刻表データ(ファイル名はインデックス)"
        // And "index: 順序 (1から始まる連番) -> {index}.json のファイル名に対応"
        // It says "{index}.json". If index is "1", file is "1.json"?
        // But the example file list shows "01.json".
        // Let's assume it might be zero-padded to 2 digits if < 10.
        
        val routeDir = getRouteDir(routeId)
        var file = File(routeDir, "$index.json")
        if (!file.exists()) {
            // Try zero padded
            val paddedIndex = index.padStart(2, '0')
            file = File(routeDir, "$paddedIndex.json")
        }
        
        if (!file.exists()) return null
        
        return try {
            json.decodeFromString(Timetable.serializer(), file.readText())
        } catch (e: Exception) {
            throw BusTimetableDataException("Failed to parse timetable $index for route $routeId", e)
        }
    }

    // --- Helper ---
    
    fun getRouteDir(routeId: String): File {
        val dir = File(cacheDir, "routes/$routeId")
        if (!dir.exists()) dir.mkdirs()
        return dir
    }
    
    fun clearCache() {
        cacheDir.deleteRecursively()
        cacheDir.mkdirs()
    }

    // --- Preferences (Sync Time & Hashes) ---

    private val prefs by lazy {
        context.getSharedPreferences("bustimetable_v3_prefs", Context.MODE_PRIVATE)
    }

    fun saveLastSyncTime(time: Long) {
        prefs.edit().putLong("last_sync_time", time).apply()
    }

    fun getLastSyncTime(): Long {
        return prefs.getLong("last_sync_time", 0L)
    }

    fun saveRouteHash(routeId: String, hash: String) {
        prefs.edit().putString("route_hash_$routeId", hash).apply()
    }

    fun getRouteHash(routeId: String): String? {
        return prefs.getString("route_hash_$routeId", null)
    }
}
