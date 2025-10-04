import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from script.common.web_access import get_data
from script.v2.busstop_database import BusStopDatabase
from script.v2.route_database import RouteDatabase
from script.v2.timetable import Timetable

route_id_list = [
    "0000800088",
    "0000803196",
    "0000801123"
]


def main():
    busstop_db = BusStopDatabase(f"database/kanachu/v2/database/busstops.json")
    busstop_db.load()
    busstop_db.clear()
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
            busstop_db.set(busstop["id"], busstop["name"], busstop["lat"], busstop["lng"])

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
                busstop_names = route_db.get_list())
            timetable.update()
            timetable.save()
        route_db.save()
    busstop_db.save()

    # https://www.kanachu.co.jp/dia/diagram/timetable/cs:0000800088-2/nid:00025625/dts:1758996000
    # https://www.kanachu.co.jp/dia/diagram/timetable01/cs:0000800088-2/rt:0/nid:00025625/dts:1758996000

if __name__ == "__main__":
    main()
