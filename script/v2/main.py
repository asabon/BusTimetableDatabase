import sys
import os
import json
from bs4 import BeautifulSoup

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, PROJECT_ROOT)

from script.common.web_access import get_data
from script.v2.busstop_database import BusStopDatabase
from script.v2.route_database import RouteDatabase
from script.v2.timetable import Timetable

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
            index_str = str(busstop["index"]).zfill(2)
            timetable = Timetable(
                file_path = f"database/kanachu/v2/database/{route_id}/{index_str}.json", 
                system = system,
                route_id = route_id, 
                busstop_index = busstop["index"],
                busstop_id = busstop["id"], 
                busstop_name = busstop["name"],
                busstop_names = busstops,
                busstop_position = position)

            if not timetable.update():
                # 更新されていなかった場合はその路線の他の時刻表も更新する必要がないとみなしてループ終了
                break
            timetable.save()
        route_db.save()
    busstop_db.save()

    # https://www.kanachu.co.jp/dia/diagram/timetable/cs:0000800088-2/nid:00025625/dts:1758996000
    # https://www.kanachu.co.jp/dia/diagram/timetable01/cs:0000800088-2/rt:0/nid:00025625/dts:1758996000

def update_route_ids_list():
    # route_ids.json を自動生成する関数
    # 既存の route_ids.json を上書きする
    import re

    base_url_list = [
        'https://www.kanachu.co.jp/dia/diagram/search?k=%E7%94%BA%E7%94%B0%E3%83%90%E3%82%B9%E3%82%BB%E3%83%B3%E3%82%BF%E3%83%BC&rt=0&t=0&sdid=00025625',
    ]

    for base_url in base_url_list:
        html = get_data(base_url)
        soup = BeautifulSoup(html, 'html.parser')
        route_ids = set()

        for a_tag in soup.find_all('a', href=True):
            match = re.search(r'/dia/route/index/cid:(\d{10})/', a_tag['href'])
            if match:
                route_ids.add(match.group(1))

        route_ids_list = sorted(route_ids)

        route_ids_path = os.path.join(os.path.dirname(__file__), "route_ids.json")
        with open(route_ids_path, 'w', encoding='utf-8') as f:
            json.dump(route_ids_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_route_ids_list()
    main()
