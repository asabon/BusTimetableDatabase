from script.common.edit_json import read_json_file
from script.common.edit_json import write_json_file
from script.common.edit_json import set_value_in_json
from script.common.edit_json import get_value_from_json
from script.v2.json_editor import JsonEditor

class BusStopDatabase:
    def __init__(self, file_path):
        self.editor = JsonEditor(file_path)

    def load(self):
        self.editor.json_data = self.editor.load()
        if self.editor.get_value("busstops") == "":
            self.editor.set_value("busstops", [])
    
    def save(self):
        self.editor.save()

    def dump(self):
        print(self.json_data)

    def clear(self):
        self.editor.json_data = {}
        self.editor.set_value("busstops", [])

    def get_num(self):
        busstops = self.editor.get_value("busstops")
        return len(busstops)

    def get_id_by_index(self, index):
        return self.editor.get_value(f"busstops.{index}.node_id")

    def get_name_by_index(self, index):
        return self.editor.get_value(f"busstops.{index}.name")

    def get_id_by_name(self, name):
        busstops = self.editor.get_value("busstops")
        for busstop in busstops:
            if busstop in busstops:
                if busstop.get("name") == name:
                    return busstop.get("node_id")
        return None

    def sort(self):
        busstops = self.editor.get_value("busstops")
        sorted_data = sorted(busstops, key=lambda x:int(x["node_id"]))
        self.editor.set_value("busstops", sorted_data)

    def set(self, id, name, lat="", lng=""):
        busstops = self.editor.get_value("busstops")
        if busstops == "":
            busstops = []

        index = next(
            (
                i for i, item in enumerate(busstops)
                if str(item["node_id"]) == str(id) and str(item["lat"]) == str(lat) and str(item["lng"]) == str(lng)
            ), 
            None
        )

        if index is not None:
            # 一致した場合、名前が変わっていたら更新
            if busstops[index]["name"] != name:
                busstops[index]["name"] = name
                busstops[index]["position"] = ""
        else:
            # 一致しなかった場合は新規追加
            busstops.append(
                {
                    "node_id": id,
                    "lat": lat,
                    "lng": lng,
                    "name": name,
                    "position": ""
                }
            )
        self.editor.set_value("busstops", busstops)
        self.sort()
