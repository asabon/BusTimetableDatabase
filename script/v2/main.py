import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from script.common.web_access import get_data
from script.v2.busstop_database import BusStopDatabase
from script.v2.route_database import RouteDatabase
from script.v2.timetable import Timetable

route_id_list = [
    "0000803702",
    "0000800088",
    "0000800780",
    "0000803170",
    "0000803162",
    "0000802960",
    "0000803602",
    "0000800294",
    "0000801075",
    "0000801107",
    "0000802965",
    "0000802964",
    "0000801123",
    "0000803215",
    "0000803493",
    "0000803177",
    "0000801242",
    "0000801320",
    "0000802962",
    "0000802961",
    "0000803182",
    "0000802481",
    "0000802478",
    "0000802475",
    "0000803208",
    "0000803178",
    "0000802014",
    "0000802018",
    "0000802971",
    "0000803323",
    "0000803324",
    "0000803111",
    "0000802682",
    "0000803196",
    "0000802951",
    "0000803460",
    "0000803441",
    "0000802676",
    "0000802477",
    "0000803209",
    "0000802468",
    "0000803195",
    "0000802472",
    "0000802015",
    "0000802031",
    "0000800236",
    "0000802021",
    "0000802952",
    "0000802683",
    "0000803163",
    "0000800826"
]


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
