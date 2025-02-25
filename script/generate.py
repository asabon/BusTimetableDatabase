import requests
import json
import sys
import ssl
import urllib.request
import urllib.error


def get_dummy_data():
    return "head 2024/07/07 0 0 0 0 0 0 0 0 0 0 0 0 - 42 0 6 39 0 0 0 01 0 0 0 0 0 0 0 0 heso 6 49 1 0 0 49 0 0 0 0 0 0 0 0 heso 6 49 2 0 0 49 0 0 0 0 0 0 0 0 heso 7 34 0 0 0 34 0 0 0 0 0 0 0 0 heso 7 54 2 0 0 54 0 0 0 0 0 0 0 0 heso 8 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 8 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 9 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 9 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 9 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 10 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 10 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 10 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 11 39 0 0 0 39 0 0 0 0 0 0 0 0 heso 11 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 11 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 12 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 12 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 12 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 13 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 13 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 13 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 14 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 14 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 14 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 15 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 15 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 15 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 16 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 16 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 16 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 17 54 0 0 0 54 0 0 0 0 0 0 0 0 heso 17 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 17 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 18 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 18 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 18 6 2 0 0 06 0 0 0 0 0 0 0 0 heso 19 18 0 0 0 18 0 0 0 0 0 0 0 0 heso 19 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 19 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 20 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 20 3 2 0 0 03 0 0 0 0 0 0 0 0 heso end"

def get_data3(url):
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    req = urllib.request.Request(url=url)
    try:
        with urllib.request.urlopen(req, context=context) as f:
            result = f.read().decode()
            print("data is ...")
            print(result)
        return result
    except urllib.error.URLError as e:
        print(f'Error: {e.reason}')
        return None

def get_data2(url):
    context = ssl.create_default_context()
    req = urllib.request.Request(url=url)
    try:
        with urllib.request.urlopen(req, context=context) as f:
            result = f.read().decode()
        return result
    except urllib.error.URLError as e:
        print(f'Error: {e.reason}')
        return None

def get_data(url):
    # url_dummy = 'https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:0000803215-11/node:00129495/kt:0/lname:/dts:1740420000'
    response = requests.get(url)
    if response.status_code == 200:
        print("Success!")
        print("response.text")
        print(response.text)
        print("response.content")
        print(response.content)
        return response.content
    else:
        print("Failed to retrieve the page")
        print(f"Status code: {response.status_code}")
        return None


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"error {e}")
        return None


def write_json_file(file_path, json_data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"error {e}")


def get_value_from_json(json_data, key):
    return json_data.get(key, "")


def set_value_in_json(json_data, key, value):
    json_data[key] = value
    return json_data


def generate(file_path):
    # Get data from json file
    json_data = read_json_file(file_path)
    update_date_json = get_value_from_json(json_data, "date")

    # Get URL from json data
    url = get_value_from_json(json_data, "url")
    if url == "":
        print("No URL")
        sys.exit(1)

    # Get data from internet
    data_string = get_data3(url)
    if data_string == None:
        print("[Error] The data can't get from internet")
        sys.exit(2)

    data_list = data_string.split()

    # for Debug
    for j in range(16, 30):
        print("data_list[" + str(j) + "] : " + data_list[j])

    # Judge to update
    update_date_web = data_list[2]
    if (update_date_json != update_date_web):
        print("Need to update")
        num =  int(data_list[16])
        timetable_weekday = []
        timetable_saturday = []
        timetable_holiday = []
        print("update: " + update_date_web)
        for i in range(num):
            timetable_item = str(data_list[18 + (i * 15)]) + ":" + str(data_list[18 + ((i * 15) + 1)])
            day_type = data_list[18 + ((i * 15) + 2)]
            print("type: " + day_type + ", item : " + timetable_item)
            if day_type == '0':
                timetable_weekday.append(timetable_item)
            elif day_type == '1':
                timetable_saturday.append(timetable_item)
            elif day_type == '2':
                timetable_holiday.append(timetable_item)
            else:
                sys.exit(3)
        set_value_in_json(json_data, "date", update_date_web)
        set_value_in_json(json_data, "weekday", timetable_weekday)
        set_value_in_json(json_data, "saturday", timetable_saturday)
        set_value_in_json(json_data, "holiday", timetable_holiday)
        write_json_file(file_path, json_data)
    else:
        print("No need to update")


if __name__ == '__main__':
    file_path = sys.argv[1]
    generate(file_path)
