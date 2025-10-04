from script.common.edit_json import read_json_file
from script.common.edit_json import write_json_file
from script.common.edit_json import set_value_in_json
from script.common.edit_json import get_value_from_json

class BusStopDatabase:
    # 初期化
    def __init__(self, file_path):
        self.file_path = file_path

    # ファイルからデータを読み出して self.json_data に格納
    def load(self):
        self.json_data = read_json_file(self.file_path)
        print(f"load completed: {self.file_path}")
    
    # self.json_data をファイルに保存
    def save(self):
        write_json_file(self.file_path, self.json_data)

    # self.json_data を画面に出力する
    def dump(self):
        print(self.json_data)

    def clear(self):
        self.json_data = {}
        set_value_in_json(self.json_data, "busstops", [])

    # item 数を返す
    def get_num(self):
        busstops = get_value_from_json(self.json_data, "busstops")
        return len(busstops)

    # index を指定して id を取得する
    def get_id_by_index(self, index):
        busstops = get_value_from_json(self.json_data, "busstops")
        busstop_id = get_value_from_json(busstops[index], "node_id")
        return busstop_id

    # 名前を指定して id を取得する
    def get_id_by_name(self, name):
        busstops = get_value_from_json(self.json_data, "busstops")
        for busstop in busstops:
            busstop_name = get_value_from_json(busstop, "name")
            busstop_id = get_value_from_json(busstop, "node_id")
            if busstop_name == name:
                return busstop_id
        return None

    # index を指定して名前を取得する    
    def get_name_by_index(self, index):
        busstops = get_value_from_json(self.json_data, "busstops")
        busstop_name = get_value_from_json(busstops[index], "name")
        return busstop_name

    # self.json_data の "busstops" 内のアイテムをソートする
    def sort(self):
        busstops = get_value_from_json(self.json_data, "busstops")
        sorted_data = sorted(busstops, key=lambda x:int(x["node_id"]))
        set_value_in_json(self.json_data, "busstops", sorted_data)

    # データを登録する
    # - すでに同じ id が登録されている場合、名前を変更する
    def set(self, id, name, lat="", lng=""):
        busstops = get_value_from_json(self.json_data, "busstops")
        index = next((i for i, item in enumerate(busstops) if int(item["node_id"]) == id), None)
        if index != None:
            busstops[index]["name"] = name
        else:
            busstops.append(
                {
                    "name": name,
                    "node_id": id,
                    "lat": lat,
                    "lng": lng
                }
            )
        set_value_in_json(self.json_data, "busstops", busstops)
        # id の昇順にソートする
        self.sort()
