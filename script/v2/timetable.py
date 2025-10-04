from script.common.web_access import get_data
import script.v2.json_editor
import sys
import re

class Timetable:
    def __init__(self, file_path, system, route_id, busstop_index, busstop_id, busstop_name, busstop_names, busstop_position):
        self.file_path = file_path
        self.route_id = route_id
        self.date = ""
        self.busstop_index = busstop_index
        self.busstop_id = busstop_id
        self.busstop_name = busstop_name
        self.busstop_position = busstop_position
        # self.destinations = busstop_names[int(busstop_index):]
        self.destinations = [stop["name"] for stop in busstop_names[int(busstop_index):]]
        self.system = system
        self.timetable = {}
        self.url = f"https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:{self.route_id}-{self.busstop_index}/node:{self.busstop_id}/kt:0/lname:/"
        print(f"filename = {file_path}")
        self.json_editor = script.v2.json_editor.JsonEditor(file_path)

    def update(self):
        before_date = self.json_editor.get_value("date")
        timetable_html = get_data(self.url)
        self._parse_timetable_html(timetable_html)
        after_date = self.date
        if before_date != after_date:
            # データが更新された
            return True
        else:
            # データは更新されなかった
            return False

    def save(self):
        import os
        # ディレクトリがなければ作成
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(self.file_path):
            # 新規作成時のテンプレート
            self.json_editor.set_value("date", "")
            self.json_editor.set_value("name", "")
            self.json_editor.set_value("position", "")
            self.json_editor.set_value("system", "")
            self.json_editor.set_value("destinations", [])
            self.json_editor.set_value("weekday", [])
            self.json_editor.set_value("saturday", [])
            self.json_editor.set_value("holiday", [])
            self.json_editor.set_value("url", "")
        self.json_editor.set_value("date", self.date)
        self.json_editor.set_value("name", self.busstop_name)
        self.json_editor.set_value("position", self.busstop_position)
        self.json_editor.set_value("system", self.system)
        self.json_editor.set_value("destinations", self.destinations)
        self.json_editor.set_value("weekday", self.timetable[0])
        self.json_editor.set_value("saturday", self.timetable[1])
        self.json_editor.set_value("holiday", self.timetable[2])
        self.json_editor.set_value("url", self.url)
        self.json_editor.save()
        return

    def _parse_timetable_html(self, html):
        data_list = html.split("\n")
        pattern = r'\d{4}/\d{2}/\d{2}'
        match = re.search(pattern, data_list[0])
        if match:
            self.date = match.group()
            print("Update date: " + self.date)
        num =  int(data_list[14])
        timetable_weekday = []
        timetable_saturday = []
        timetable_holiday = []
        for i in range(num):
            hour = int(data_list[16 + (i * 15)])
            minute = int(data_list[16 + (i * 15) + 1])
            day_type = data_list[16 + ((i * 15) + 2)]
            if (hour < 0) or (hour > 24):
                print("[Error] num = " + str(num) + ", i = " + str(i) + ", hour = " + str(hour))
                print(data_list)
                sys.exit(4)
            if (minute < 0) or (minute > 59):
                print("[Error] num = " + str(num) + ", i = " + str(i) + ", minute = " + str(minute))
                print(data_list)
                sys.exit(5)
            timetable_item = str(hour) + ":" + str(minute).zfill(2)
            #print("type: " + day_type + ", item : " + timetable_item)
            if day_type == '0':
                timetable_weekday.append(timetable_item)
            elif day_type == '1':
                timetable_saturday.append(timetable_item)
            elif day_type == '2':
                timetable_holiday.append(timetable_item)
            else:
                sys.exit(3)
        self.timetable[0] = self.sort_time_list(timetable_weekday)
        self.timetable[1] = self.sort_time_list(timetable_saturday)
        self.timetable[2]= self.sort_time_list(timetable_holiday)
        print(f"name: {self.busstop_name} ({self.busstop_id})")
        print(f"weekday: {self.timetable[0]}")
        print(f"saturday: {self.timetable[1]}")
        print(f"holiday: {self.timetable[2]}")
        return []

    def sort_time_list(self, time_list):
        return sorted(time_list, key=lambda time: int(time.split(":")[0]) * 60 + int(time.split(":")[1]))
