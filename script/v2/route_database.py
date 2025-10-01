from bs4 import BeautifulSoup
import re

from script.common.web_access import get_data
from script.common.convert import to_half_width
import script.v2.json_editor

# バスの路線ごとの経路を管理するクラス
class RouteDatabase:
    # 初期化とjsonファイルのロード
    def __init__(self, json_path, route_url=None):
        # バス停のIDリスト
        # このリストの順番がバスの経路の順番になる
        self.busstops = []
        self.json_path = json_path
        self.json_editor = script.v2.json_editor.JsonEditor(json_path)
        self.busstops = self.json_editor.get_value("busstops")
        if not isinstance(self.busstops, list):
            self.busstops = []
        self.route_url = self.json_editor.get_value("route_url")
        if route_url is not None:
            self.route_url = route_url

    def update(self):
        route_html = get_data(self.route_url)
        busstops = self._parse_route_html(route_html)
        self.clear()
        for busstop in busstops:
            busstop_id = busstop["id"]
            busstop_name = to_half_width(busstop["name"])
            busstop_index = busstop["index"]
            self.add(busstop_index, busstop_id, busstop_name)

    # jsonファイルのセーブ
    def save(self):
        import os
        # ディレクトリがなければ作成
        dir_path = os.path.dirname(self.json_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        # busstopsを保存
        self.json_editor.set_value("busstops", self.busstops)
        # route_urlも保存
        self.json_editor.set_value("route_url", self.route_url)
        self.json_editor.save()

    # バス停リストのクリア
    def clear(self):
        self.busstops = []

    # バス停リストにバス停を追加
    def add(self, busstop_index, busstop_id, busstop_name):
        self.busstops.append({
            "index": busstop_index,
            "id": busstop_id,
            "name": busstop_name
        })

    # バス停リストを取得
    def get_list(self):
        return self.busstops

    # index を指定してバス停IDを取得
    def get(self, index):
        return self.busstops[index]

    # 個数を返す
    def get_num(self):
        return len(self.busstops)

    # HTMLデータを解析してバス停情報のリストを生成する
    def _parse_route_html(self, html_string):
        soup = BeautifulSoup(html_string, "html.parser")
        busstops = []
        for li in soup.find_all("li", id=re.compile(r"\d+-\d+")):
            li_id = li.get("id")
            if not li_id or "-" not in li_id:
                continue
            busstop_id, busstop_index = li_id.split("-")
            span = li.find("span", class_="busStopPoint")
            busstop_name = span.get_text() if span else ""
            a_tag = li.find("a", onClick=re.compile(r"move_center"))
            lat, lng = None, None
            if a_tag:
                on_click = a_tag.get("onClick", "")
                m = re.search(r"move_center\(([\d\.]+),\s*([\d\.]+),", on_click)
                if m:
                    lat, lng = m.group(1), m.group(2)
            busstops.append({
                "id": busstop_id,
                "index": busstop_index,
                "name": busstop_name,
                "lat": lat,
                "lng": lng
            })
        return busstops
