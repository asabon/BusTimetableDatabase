import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from script.common.web_access import get_data
from script.v2.busstop_database import BusStopDatabase
from script.v2.route_database import RouteDatabase
from script.v2.timetable import Timetable
import json

# Load route ID list from external JSON so other scripts can modify it.
# This file is required: if it's missing or invalid, raise an error to fail fast.
route_ids_path = os.path.join(os.path.dirname(__file__), "route_ids.json")
if not os.path.exists(route_ids_path):
    raise FileNotFoundError(f"Required file not found: {route_ids_path}")

try:
    with open(route_ids_path, 'r', encoding='utf-8') as f:
        route_id_list = json.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load route IDs from {route_ids_path}: {e}")

if not (isinstance(route_id_list, list) and all(isinstance(x, str) for x in route_id_list)):
    raise ValueError(f"{route_ids_path} must contain a JSON array of strings")


def main():
    busstop_db = BusStopDatabase(f"database/kanachu/v2/database/busstops.json")
    busstop_db.load()
    # 手修正しているデータ ("position") があるため、すでに存在するデータは毎回クリアしない
    # busstop_db.clear()
    for route_id in route_id_list:
        route_json_path = f"database/kanachu/v2/database/{route_id}/route.json"
        route_url = f"https://www.kanachu.co.jp/dia/route/index/cid:{route_id}/"
        route_db = RouteDatabase(route_json_path, route_url)
        route_db.update()
        system = route_db.get_system()
        # print(f"=== Route ID: {route_id}, Bus Stops: {route_db.get_num()} ===")
        busstops = route_db.get_list()
        for i, busstop in enumerate(busstops):
            # ID の登録は全部行う
            busstop_db.set(
                id = busstop["id"], 
                lat = busstop["lat"], 
                lng = busstop["lng"],
                name = busstop["name"]
            )
            position = busstop_db.get_position(
                id = busstop["id"],
                lat = busstop["lat"],
                lng = busstop["lng"],
                name = busstop["name"]
            )

            if i == len(busstops) - 1:
                # 最後の要素は到着するだけで時刻表を持たないのでスキップ
                break
            timetable = Timetable(
                file_path = f"database/kanachu/v2/database/{route_id}/{busstop['index'].zfill(2)}.json", 
                system = system,
                route_id = route_id, 
                busstop_index = busstop["index"],
                busstop_id = busstop["id"], 
                busstop_name = busstop["name"],
                busstop_names = route_db.get_list(),
                busstop_position = position)

            result = timetable.update()
            if result == False:
                # 更新されていなかった場合はその路線の他の時刻表も更新する必要がないとみなしてループ終了
                break
            timetable.save()
        route_db.save()
    busstop_db.save()

    # https://www.kanachu.co.jp/dia/diagram/timetable/cs:0000800088-2/nid:00025625/dts:1758996000
    # https://www.kanachu.co.jp/dia/diagram/timetable01/cs:0000800088-2/rt:0/nid:00025625/dts:1758996000

if __name__ == "__main__":
    main()
