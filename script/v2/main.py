import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from script.common.web_access import get_data
from script.v2.busstop_database import BusStopDatabase
from script.v2.route_database import RouteDatabase

route_id_list = [
    "0000800088"
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
        print(f"=== Route ID: {route_id}, Bus Stops: {route_db.get_num()} ===")
        for busstop in route_db.get_list():
            busstop_db.set(busstop["id"], busstop["name"])
            timetable_url = f"https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:{route_id}-{busstop["index"]}/node:{busstop["id"]}/kt:0/lname:/"
            timetable_html = get_data(timetable_url)
        route_db.save()
    busstop_db.save()

    # https://www.kanachu.co.jp/dia/diagram/timetable/cs:0000800088-2/nid:00025625/dts:1758996000
    # https://www.kanachu.co.jp/dia/diagram/timetable01/cs:0000800088-2/rt:0/nid:00025625/dts:1758996000

if __name__ == "__main__":
    main()
