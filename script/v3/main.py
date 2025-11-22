import sys
import os
import re
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote
from collections import deque

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, PROJECT_ROOT)

from script.common.web_access import get_data
from script.v3.busstop_database import BusStopDatabase
from script.v3.route_database import RouteDatabase
from script.v3.timetable import Timetable

def main():
    route_id_list = load_route_ids()
    busstop_db = load_busstop_db()
    for route_id in route_id_list:
        process_route(route_id, busstop_db)
    busstop_db.save()

def load_busstop_db() -> BusStopDatabase:
    db = BusStopDatabase(f"database/kanachu/v3/database/busstops.json")
    db.load()
    return db

def process_route(route_id: str, busstop_db: BusStopDatabase):
    route_json_path = f"database/kanachu/v3/database/{route_id}/route.json"
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
            file_path = f"database/kanachu/v3/database/{route_id}/{index_str}.json", 
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
    route_ids_path = os.path.join("database/kanachu/v3/database", "route_ids.json")
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

# sdid とバス停名から路線IDリストを取得する関数
def get_route_ids_list(sdid: str, name: str) -> list[str]:
    route_ids = set()
    url = f'https://www.kanachu.co.jp/dia/diagram/search?k={quote(name)}&rt=0&t=0&sdid={sdid}'
    html = get_data(url)
    soup = BeautifulSoup(html, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        match = re.search(r'/dia/route/index/cid:(\d{10})/', a_tag['href'])
        if match:
            route_ids.add(match.group(1))
    return sorted(route_ids)

# 路線IDからバス停リストを取得する関数
def get_busstops_list(route_id: str) -> list[str]:
    url = f"https://www.kanachu.co.jp/dia/route/index/cid:{route_id}/"
    html = get_data(url)
    soup = BeautifulSoup(html, "html.parser")
    system = get_system_from_route_html(html)
    busstops = []
    for li in soup.find_all("li", id=re.compile(r"\d+-\d+")):
        li_id = li.get("id")
        if not li_id or "-" not in li_id:
            continue

        busstop_id, busstop_index = li_id.split("-")

        # バス停名の取得
        span = li.find("span", class_="busStopPoint")
        busstop_name = span.get_text() if span else ""

        # onClick属性を持つaタグを明示的に探す
        #a_tag = li.find("a", onClick=re.compile(r"move_center"))
        a_tag = li.find("a", attrs={"onclick": re.compile(r"move_center")} )
        lat, lng = None, None
        if a_tag:
            on_click = a_tag.get("onclick", "")
            m = re.search(r"move_center\(([\d.]+),\s*([\d.]+),", on_click)
            if m:
                lat, lng = m.group(1), m.group(2)
        else:
            print("[Error] tag is NOT found.")
        busstops.append({
            "id": busstop_id,
            "index": busstop_index,
            "name": busstop_name,
            "lat": lat,
            "lng": lng
        })
    return busstops

def get_system_from_route_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # h2 タグのテキストを取得
    target_h2 = soup.find("div", class_="hGroup201").find("h2")
    text = target_h2.get_text(strip=True) if target_h2 else ""

    # 正規表現で「漢字1文字＋数字1〜2桁」を抽出
    match = re.search(r"[一-龯]{1}\d{1,2}", text)
    if match:
        return match.group()
    else:
        return None

def update_route_ids_list():
    base_locations = [
        {"sdid": "00025625", "name": '町田バスセンター'},
    ]
    processed_sdid = set()
    queue = deque(base_locations)
    all_route_ids = set()
    queue_idx = 0
    while queue:
        # queue から1つ取り出して処理
        base_location = queue.popleft()
        sdid = base_location["sdid"]
        name = base_location["name"]
        queue_idx += 1
        print(f"[{queue_idx}/{len(queue)}] process sdid={sdid}, name={name}")
        route_ids = get_route_ids_list(sdid, name)
        all_route_ids.update(route_ids)
        for route_id in route_ids:
            busstops = get_busstops_list(route_id)
            for busstop in busstops:
                new_sdid = busstop["id"]
                new_name = busstop["name"]
                if new_sdid not in processed_sdid:
                    processed_sdid.add(new_sdid)
                    # queue に追加
                    queue.append({"sdid": new_sdid, "name": new_name})
                    print(f"    append sdid={new_sdid}, name={new_name}")
    route_ids_path = os.path.join("database/kanachu/v3/database", "route_ids.json")
    with open(route_ids_path, 'w', encoding='utf-8') as f:
        json.dump(sorted(all_route_ids), f, indent=4, ensure_ascii=False)

def cleanup_obsolete_route_dirs():
    route_ids = load_route_ids()
    base_dir = os.path.join("database/kanachu/v3/database")
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

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update Kanachu Bus Timetable Database v3')
    parser.add_argument('--update-list', action='store_true', help='Update route ID list and cleanup obsolete directories')
    args = parser.parse_args()

    if args.update_list:
        # 路線IDリストを更新
        update_route_ids_list()
        # 使われなくなった路線ディレクトリを削除
        cleanup_obsolete_route_dirs()
    else:
        # 路線ごとにメイン処理を実施
        main()
