import json
import sys
import ssl
import urllib.request
import urllib.error
import re
import os

def get_data(url):
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    req = urllib.request.Request(url=url)
    try:
        with urllib.request.urlopen(req, context=context) as f:
            result = f.read().decode()
            # print("data is ...")
            # print(result)
        return result
    except urllib.error.URLError as e:
        print(f'Error: {e.reason}')
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
    print("file: " + file_path)

    # Get data from json file
    json_data = read_json_file(file_path)
    update_date_json = get_value_from_json(json_data, "date")

    # Get URL from json data
    url = get_value_from_json(json_data, "url")
    if url == "":
        print("No URL")

    # Get data from internet
    data_string = get_data(url)
    if data_string == None:
        print("[Error] The data can't get from internet")
        sys.exit(2)

    data_list = data_string.split("\n")

    # for Debug
    for j in range(0, 30):
        print("data_list[" + str(j) + "] : " + data_list[j])

    pattern = r'\d{4}/\d{2}/\d{2}'
    match = re.search(pattern, data_list[0])
    if match:
        update_date_web = match.group()
    else:
        update_date_web = ""
        print("Can't get update date")
        sys.exit(3)

    if (update_date_json != update_date_web):
        print("Need to update")
        num =  int(data_list[14])
        timetable_weekday = []
        timetable_saturday = []
        timetable_holiday = []
        print("update: " + update_date_web)
        for i in range(num):
            timetable_item = str(data_list[16 + (i * 15)]) + ":" + str(data_list[16 + ((i * 15) + 1)]).zfill(2)
            day_type = data_list[16 + ((i * 15) + 2)]
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


def generate_in_directory(subdirectory_path):
    for entry in os.listdir(subdirectory_path):
        file_path = os.path.join(subdirectory_path, entry)
        if os.path.isfile(file_path) and file_path.endswith('.json'):
            generate(file_path)


def generate_all(directory_path):
    for entry in os.listdir(directory_path):
        subdirectory_path = os.path.join(directory_path, entry)
        if os.path.isdir(subdirectory_path):
            generate_in_directory(subdirectory_path)


if __name__ == '__main__':
    directory_path = sys.argv[1]
    generate_all(directory_path)
