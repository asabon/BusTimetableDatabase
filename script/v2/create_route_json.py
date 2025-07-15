import re
import unicodedata
from common.web_access import get_data
from common.edit_json import update_json_file
from common.convert import to_half_width

def to_halfwidth_except_katakana_list(strings):
    katakana_pattern = re.compile(r'[\u30A0-\u30FF]+')
    return [
        ''.join(
            c if katakana_pattern.match(c) else unicodedata.normalize('NFKC', c)
            for c in string
        ) for string in strings
    ]

def to_halfwidth_list(strings):
    return [unicodedata.normalize('NFKC', c) for c in strings]

def get_busstop(data_string):
    matches = re.findall(r'<span class="busStopPoint">([^<]*)</span></a><a href="/dia/diagram/timetable/cs:[0-9]+-([0-9]+)/nid:([0-9]+)/dts:([0-9]+)">', data_string)
    return matches

def create_route_json(route_path, route_url):
    print(f"create_route_json() -> File:{route_path}, URL:{route_url}")
    #print(f"  route_path: {route_path}")
    #print(f"  route_url:  {route_url}")
    data_string = get_data(route_url)
    data_list = data_string.split("\n")
    for data in data_list:
        if re.match(r"^\s*<li id=\"\d+-\d+\">.*</li>\s*$", data) != None:
            route = get_busstop(data)
            busstop_name_list = []
            for busstop in route:
                #print(f"{busstop[1]}: name: {busstop[0]}, id: {busstop[2]}")
                busstop_name = to_half_width(busstop[0])
                busstop_name_list.append(busstop_name)
            update_json_file(route_path, "route", busstop_name_list)
            update_json_file(route_path, "url", route_url)
    return

if __name__ == "__main__":
    output = sys.argv[1]
    url = sys.argv[2]
    create_route_json(output, url)
    # シンプルなサンプル
    #create_route_json("./temp/route_0000800088.json", "https://www.kanachu.co.jp/dia/route/index/cid:0000800088/")
    # ／を含んだバス停がある
    #create_route_json("./temp/route_0000801075.json", "https://www.kanachu.co.jp/dia/route/index/cid:0000801075/")
