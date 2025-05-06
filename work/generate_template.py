import os
import re
import json

def generate(file_name):
    name = file_name.split("_")[0]
    position = file_name.split("_")[1]
    print("====================================")
    print(f"file_name: {file_name}")
    print(f"name:      {name}")
    print(f"position:  {position}")
    pattern = r"<th class=\"row02\" id=\"rid_\d+\" >([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+\d+)</th><td class=\"size01-2\">([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)</td><td class=\"size02-2\">([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)\(([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)\)</td><td class=\"size07\" id=\"sid_\d+\"><input type=\"hidden\" id=\"officekey\d+\" value=\"\d+\" /><input type=\"hidden\" id=\"office\d+\" value=\"\d+-\d+\" /><input type=\"checkbox\" name=\"timeTable\d+\" id=\"cb_\d+\" class=\"timeTable01\"  onclick=\"cbox_chenge\('(\d+)','(\d+-\d+)','(\d+)','.*?','(\d+)'\);\" />"
    try:
        with open(f"input/{file_name}", "r", encoding="utf-8") as file:
            text = file.read()
            matches = re.findall(pattern, text)
            for match in matches:
                print( " -----")
                print(f"  name:      {name}")
                print(f"  position:  {position}")
                print(f"  system:    {match[0]}")
                print(f"  dest:      {match[1]}")
                print(f"  via:       {match[2]}経由")
                print(f"  from:      {match[3]}")
                print(f"  url:       https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:{match[5]}/node:{match[6]}/kt:{match[4]}/lname:/dts:{match[7]}")
                output_directory = os.path.join("..", "database", "神奈川中央交通", f"{match[0]}_{match[1]}_{match[2]}経由_{match[3]}")
                route_file = os.path.join(output_directory, "route.json")
                with open(route_file, "r", encoding="utf-8") as route_json:
                    route_data = json.load(route_json)
                    route_list = route_data["route"]
                    count = 0
                    route_index = 0
                    destinations = []
                    for route in route_list:
                        count = count + 1
                        if route == name:
                            route_index = count
                        if (route_index != 0) and (route_index != count):
                            destinations.append(route)
                output_file = os.path.join(output_directory, f"{route_index:02}_{name}.json")
                data = {
                    "date": "-",
                    "name": name,
                    "position": position,
                    "system": match[0],
                    "destinations": destinations,
                    "weekday": [],
                    "saturday": [],
                    "holiday": [],
                    "url": f"https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:{match[5]}/node:{match[6]}/kt:{match[4]}/lname:/dts:{match[7]}"
                }
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")

if __name__ == "__main__":
    print("Start: generate_template.py")
    directory = "input"
    for file_name in os.listdir(directory):
        file_path = os.path.join("input", file_name)
        if os.path.isfile(file_path):
            generate(file_name)




#<th class="row02" id="rid_0" >町12</th><td class="size01-2">木曽南団地行</td><td class="size02-2">境川団地(町田ターミナル発)</td><td class="size07" id="sid_0"><input type="hidden" id="officekey0" value="0" /><input type="hidden" id="office0" value="01251-22" /><input type="checkbox" name="timeTable0" id="cb_0" class="timeTable01"  onclick="cbox_chenge('0','0000800088-2','00025625','木','1746468000');" />
#<th class="row02" id="rid_1" >町12</th><td class="size01-2">木曽南団地行</td><td class="size02-2">境川団地(町田バスセンター発)</td><td class="size07" id="sid_1"><input type="hidden" id="officekey1" value="0" /><input type="hidden" id="office1" value="01251-22" /><input type="checkbox" name="timeTable1" id="cb_1" class="timeTable01"  onclick="cbox_chenge('1','0000800780-1','00025625','木','1746468000');" />
#<th class="row02" id="rid_2" >町17</th><td class="size01-2">淵野辺駅北口行</td><td class="size02-2">木曽南団地(町田バスセンター発)</td><td class="size07" id="sid_2"><input type="hidden" id="officekey2" value="2" /><input type="hidden" id="office2" value="01251-22" /><input type="checkbox" name="timeTable2" id="cb_2" class="timeTable01"  onclick="cbox_chenge('2','0000801123-1','00025625','フ','1746468000');" />
#<th class="row02" id="rid_3" >町78</th><td class="size01-2">野津田車庫行</td><td class="size02-2">木曽南団地(町田バスセンター発)</td><td class="size07" id="sid_3"><input type="hidden" id="officekey3" value="3" /><input type="hidden" id="office3" value="01251-22" /><input type="checkbox" name="timeTable3" id="cb_3" class="timeTable01"  onclick="cbox_chenge('3','0000800826-1','00025625','','1746468000');" />