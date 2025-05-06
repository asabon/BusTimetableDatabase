# 使い方
# ルートディレクトリにて、以下のコマンドで実行
# > python script/update_route.py
import os
import json
import re
import unicodedata
from web_access import get_data

def to_halfwidth_list(strings):
    return [unicodedata.normalize('NFKC', c) for c in strings]


def get_busstop(data_string):
    matches = re.findall(r"<span class=\"busStopPoint\">(.*?)</span>", data_string)
    converted_data = to_halfwidth_list(matches)
    return converted_data

def get_node_id(data_string):
    match = re.search(r"^https://.*?/node:(\d+)/.*?", data_string)
    return match[1]

# 各ディレクトリの route.json を更新する
def update_route(file_path):
    with open(file_path, "r", encoding="utf-8") as route_json:
        route_data = json.load(route_json)
        url = route_data.get("url")
        if url != None:
            #print(url)
            data_string = get_data(url)
            data_list = data_string.split("\n")
            for data in data_list:
                if re.match(r"^\s*<li id=\"\d+-\d+\">.*</li>\s*$", data) != None:
                    route = get_busstop(data)
                    #print(f"{route}")
                    route_data["route"] = route
        else:
            print("URL is NOT exist.")
    with open(file_path, "w", encoding="utf-8") as route_json:
        json.dump(route_data, route_json, indent=2, ensure_ascii=False)

def update_destinations(file_path, route_json_path):
    #print(f"file_path:       {file_path}")
    #print(f"route_json_path: {route_json_path}")
    with open(route_json_path, "r", encoding="utf-8") as route_json:
        route_data = json.load(route_json)
        route_list = route_data.get("route")
    if route_list == None:
        print(f"{route_json_path} is empty.")
        return
    with open(file_path, "r", encoding="utf-8") as busstop_json:
        busstop_data = json.load(busstop_json)
        name = busstop_data.get("name")
        isMatched = False
        new_dest_list = []
        for route in route_list:
            if isMatched:
                new_dest_list.append(route)
            if name == route:
                isMatched = True
        busstop_data["destinations"] = new_dest_list
    with open(file_path, "w", encoding="utf-8") as busstop_json:
        json.dump(busstop_data, busstop_json, indent=2, ensure_ascii=False)


def update_nodes(file_path, busstops_path):
    with open(file_path, "r", encoding="utf-8") as busstop_json:
        busstop_data = json.load(busstop_json)
        db_name = busstop_data.get("name")
        url = busstop_data.get("url")
        db_node = get_node_id(url)
    with open(busstops_path, "r", encoding="utf-8") as busstops_json:
        busstops_data = json.load(busstops_json)
        isMatched = False
        busstops = busstops_data.get("busstops")
        for it in busstops:
            it_name = it.get("name")
            it_node = it.get("node_id")
            #print(f"name: {it_name}")
            #print(f"node_id: {it_node}")
            if (db_name == it_name):
                if (db_node == it_node):
                    isMatched = True
                else:
                    print( "node_id is NOT matched")
                    print(f"  name: {db_name}")
                    print(f"    - {db_node}")
                    print(f"    - {it_node}")
        if isMatched == False:
            data = {
                "name": db_name,
                "node_id": db_node
            }
            busstops.append(data)
        busstops_data["busstops"] = busstops
    with open(busstops_path, "w", encoding="utf-8") as busstops_json:
        json.dump(busstops_data, busstops_json, indent=2, ensure_ascii=False)


def do_process(dir_path):
    print(f"Process to {dir_path}")
    route_json_path = os.path.join(dir_path, "route.json")
    busstops_json_path = os.path.join(dir_path, "..", "busstops.json")
    if os.path.exists(route_json_path):
        # ディレクトリ内の route.json を更新する
        update_route(route_json_path)
        # ディレクトリ内の各バス停の destinations を更新する
        for root, dirs, files in os.walk(dir_path):
            for file_name in files:
                if file_name != "route.json":
                    file_path = os.path.join(root, file_name)
                    update_destinations(file_path, route_json_path)
                    update_nodes(file_path, busstops_json_path)
    else:
        print(f"route_json_path is NOT exist.")

if __name__ == "__main__":
    rootdir = os.path.join("database", "神奈川中央交通")
    for root, dirs, files in os.walk(rootdir):
        for dir_name in dirs:
            sub_dir_path = os.path.join(root, dir_name)
            do_process(sub_dir_path)
