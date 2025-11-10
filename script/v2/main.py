import sys
import os
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, PROJECT_ROOT)

from script.common.web_access import get_data
from script.v2.busstop_database import BusStopDatabase
from script.v2.route_database import RouteDatabase
from script.v2.timetable import Timetable

def main():
    route_id_list = load_route_ids()
    busstop_db = load_busstop_db()
    for route_id in route_id_list:
        process_route(route_id, busstop_db)
    busstop_db.save()

def load_busstop_db() -> BusStopDatabase:
    db = BusStopDatabase(f"database/kanachu/v2/database/busstops.json")
    db.load()
    return db

def process_route(route_id: str, busstop_db: BusStopDatabase):
    route_json_path = f"database/kanachu/v2/database/{route_id}/route.json"
    route_url = f"https://www.kanachu.co.jp/dia/route/index/cid:{route_id}/"
    route_db = RouteDatabase(route_json_path, route_url)
    route_db.update()
    system = route_db.get_system()
    busstops = route_db.get_list()
    # 各バス停ごとに時刻表を更新
    for i, busstop in enumerate(busstops):
        # バス停情報をDBに登録・更新
        busstop_db.set(
            id = busstop["id"], 
            lat = busstop["lat"], 
            lng = busstop["lng"],
            name = busstop["name"]
            # position はここでは設定しない(デフォルトの "-" が設定される)
        )
        # position は、別途、人が調査して設定している。
        # それをここで読み出している。
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

        if not timetable.is_updated():
            # 更新されていなかった場合はその路線の他の時刻表も更新する必要がないとみなしてループ終了
            break

        timetable.save()
    route_db.save()

def load_route_ids() -> list[str]:
    route_ids_path = os.path.join(os.path.dirname(__file__), "route_ids.json")
    if not os.path.exists(route_ids_path):
        logger.error(f"Required file not found: {route_ids_path}")
        raise FileNotFoundError(f"Required file not found: {route_ids_path}")

    try:
        with open(route_ids_path, 'r', encoding='utf-8') as f:
            route_id_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        logger.error(f"Error loading route IDs from {route_ids_path}: {e}")
        raise RuntimeError(f"Failed to load route IDs from {route_ids_path}: {e}")

    if not (isinstance(route_id_list, list) and all(isinstance(x, str) for x in route_id_list)):
        logger.error(f"Invalid format in {route_ids_path}: must be a JSON array of strings")
        raise ValueError(f"{route_ids_path} must contain a JSON array of strings")
    
    return route_id_list

def update_route_ids_list():
    # route_ids.json を自動生成する関数
    # 既存の route_ids.json を上書きする
    import re

    locations = [
        {"sdid": "00025625", "name": '町田バスセンター'},
        {"sdid": "00129356", "name": '町田市役所市民ホール前'},
        {"sdid": "00129246", "name": '淵野辺駅北口'},
    ]

    base_url_list = [
        f'https://www.kanachu.co.jp/dia/diagram/search?k={quote(loc["name"])}&rt=0&t=0&sdid={loc["sdid"]}'
        for loc in locations
    ]

    route_ids = set()

    for base_url in base_url_list:
        html = get_data(base_url)
        soup = BeautifulSoup(html, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            match = re.search(r'/dia/route/index/cid:(\d{10})/', a_tag['href'])
            if match:
                route_ids.add(match.group(1))

    route_ids_list = sorted(route_ids)

    route_ids_path = os.path.join(os.path.dirname(__file__), "route_ids.json")
    with open(route_ids_path, 'w', encoding='utf-8') as f:
        json.dump(route_ids_list, f, indent=4, ensure_ascii=False)

def cleanup_obsolete_route_dirs():
    route_ids = load_route_ids()
    base_dir = os.path.join("database/kanachu/v2/database")
    existing_dirs = [
        name for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name)) and name.isdigit() and len(name) == 10
    ]

    obsolete_dirs = [d for d in existing_dirs if d not in route_ids]
    for d in obsolete_dirs:
        dir_path = os.path.join(base_dir, d)
        try:
            # ディレクトリごと削除（中身も含めて）
            import shutil
            shutil.rmtree(dir_path)
            logger.info(f"Removed obsolete route directory: {dir_path}")
        except Exception as e:
            logger.warning(f"Failed to remove {dir_path}: {e}")

if __name__ == "__main__":
    # 路線IDリストを更新
    update_route_ids_list()
    # 使われなくなった路線ディレクトリを削除
    cleanup_obsolete_route_dirs()
    # 路線ごとにメイン処理を実施
    main()
