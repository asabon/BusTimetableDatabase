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


def update_route(file_path):
    with open(file_path, "r", encoding="utf-8") as route_json:
        route_data = json.load(route_json)
        url = route_data.get("url")
        if url != None:
            print(url)
            data_string = get_data(url)
            data_list = data_string.split("\n")
            for data in data_list:
                if re.match(r"^\s*<li id=\"\d+-\d+\">.*</li>\s*$", data) != None:
                    route = get_busstop(data)
                    print(f"{route}")
                    route_data["route"] = route
        else:
            print("URL is NOT exist.")
    with open(file_path, "w", encoding="utf-8") as route_json:
        json.dump(route_data, route_json, indent=2, ensure_ascii=False)
    

def do_process(dir_path):
    #print(f"Process to {dir_path}")
    route_json_path = os.path.join(dir_path, "route.json")
    if os.path.exists(route_json_path):
        #print(f"Check route.json")
        update_route(route_json_path)
    else:
        print(f"route_json_path is NOT exist.")

if __name__ == "__main__":
    rootdir = os.path.join("..", "database", "神奈川中央交通")
    for root, dirs, files in os.walk(rootdir):
        for dir_name in dirs:
            sub_dir_path = os.path.join(root, dir_name)
            do_process(sub_dir_path)
