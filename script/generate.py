import sys
import re
import os
from edit_json import read_json_file
from edit_json import write_json_file
from edit_json import get_value_from_json
from edit_json import set_value_in_json
from web_access import get_data


def generate(file_path, force_update):
    print("file: " + file_path)

    # Get data from json file
    json_data = read_json_file(file_path)
    update_date_json = get_value_from_json(json_data, "date")

    # Get URL from json data
    url = get_value_from_json(json_data, "url")
    if url == "":
        print("=> No URL")
        return 1

    # Get data from internet
    data_string = get_data(url)
    if data_string == None:
        print("[Error] The data can't get from internet")
        sys.exit(2)

    data_list = data_string.split("\n")

    # for Debug
    #for j in range(0, 30):
    #    print("data_list[" + str(j) + "] : " + data_list[j])

    pattern = r'\d{4}/\d{2}/\d{2}'
    match = re.search(pattern, data_list[0])
    if match:
        update_date_web = match.group()
    else:
        update_date_web = ""
        print("Can't get update date")
        return 2

    print("local: " + update_date_json + ", web: " + update_date_web)
    if force_update == True:
        update_date_json = "-"
    if (update_date_json != update_date_web):
        print("=> Need to update")
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
            print("type: " + day_type + ", item : " + timetable_item)
            if day_type == '0':
                timetable_weekday.append(timetable_item)
            elif day_type == '1':
                timetable_saturday.append(timetable_item)
            elif day_type == '2':
                timetable_holiday.append(timetable_item)
            else:
                sys.exit(3)
        sorted_timetable_weekday = sort_time_list(timetable_weekday)
        sorted_timetable_saturday = sort_time_list(timetable_saturday)
        sorted_timetable_holiday = sort_time_list(timetable_holiday)
        set_value_in_json(json_data, "date", update_date_web)
        set_value_in_json(json_data, "weekday", sorted_timetable_weekday)
        set_value_in_json(json_data, "saturday", sorted_timetable_saturday)
        set_value_in_json(json_data, "holiday", sorted_timetable_holiday)
        write_json_file(file_path, json_data)
    else:
        print("=> No need to update")
    return 0


def sort_time_list(time_list):
    return sorted(time_list, key=lambda time: int(time.split(":")[0]) * 60 + int(time.split(":")[1]))


def generate_in_directory(subdirectory_path, force_update):
    for entry in os.listdir(subdirectory_path):
        file_path = os.path.join(subdirectory_path, entry)
        if entry != "route.json" and os.path.isfile(file_path) and file_path.endswith('.json'):
            result = generate(file_path, force_update)


def generate_all(directory_path, force_update):
    for entry in os.listdir(directory_path):
        subdirectory_path = os.path.join(directory_path, entry)
        if os.path.isdir(subdirectory_path):
            result = generate_in_directory(subdirectory_path, force_update)


def str_to_bool(value):
    return value.lower() in ("true", "1", "t", "y", "yes")


if __name__ == '__main__':
    directory_path = sys.argv[1]
    force_update = str_to_bool(sys.argv[2])
    generate_all(directory_path, force_update)
