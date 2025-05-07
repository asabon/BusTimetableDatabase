import sys
import os
import json
import re

def create_template(filepath, name, system, course_id, index, node_id):
    with open(filepath, "w", encoding="utf-8") as template_json:
        data = {
            "date": "-",
            "name": name,
            "position": "-",
            "system": system,
            "destinations": [],
            "weekday": [],
            "saturday": [],
            "holiday": [],
            "url": f"https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:{course_id}-{index}/node:{node_id}/kt:0/lname:/"
        }
        json.dump(data, template_json, indent=2, ensure_ascii=False)


def generate_template(dir_path, busstops_path):
    matched = re.search(f"^([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+\d+)_", os.path.basename(dir_path))
    system = matched[1]
    route_json_path = os.path.join(dir_path, "route.json")
    with open(route_json_path, "r", encoding="utf-8") as route_json:
        route_data = json.load(route_json)
        route_url = route_data.get("url")
        matched2 = re.search(r"cid:(\d+)/", route_url)
        course_id = matched2[1]
        route_list = route_data.get("route")
        route_list.pop() # 最後のバス停は到着のみで時刻表は存在しないため削除する
    with open(busstops_path, "r", encoding="utf-8") as busstops_json:
        busstops_data = json.load(busstops_json)
        busstops_list = busstops_data.get("busstops")
    id = 1
    for route in route_list:
        filename = f"{id:02}_{route}.json"
        id = id + 1
        matchedId = 0
        for busstops in busstops_list:
            if route == busstops["name"]:
                matchedId = busstops["node_id"]
        if matchedId != 0:
            #print(f"filename: {filename}")
            #print(f"node_id: {matchedId}")
            filepath = os.path.join(dir_path, filename)
            if os.path.exists(filepath):
                # 更新
                print(f"Update {filepath}")
            else:
                # 新規作成
                print(f"Create {filepath} as node_id:{matchedId}")
                create_template(filepath, route, system, course_id, id, matchedId)

def generate_template_in_directory(root_path, busstops_path):
    for rootdir, dirs, files in os.walk(root_path):
        for dir in dirs:
            sub_dir_path = os.path.join(rootdir, dir)
            generate_template(sub_dir_path, busstops_path)


if __name__ == "__main__":
    root_path = sys.argv[1]
    busstops_path = sys.argv[2]
    generate_template_in_directory(root_path, busstops_path)
