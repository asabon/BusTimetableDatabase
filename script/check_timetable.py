import json
import sys
import re


def check_timetable(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Check "date" field
        result = check_date(data)
        if result != 0:
            print(f"Error: {result}, File: {file_path}")
            return result
        # Check "name" field
        result = check_name(data)
        if result != 0:
            print(f"Error: {result}, File: {file_path}")
            return result
        # Check "destinations" field
        result = check_destinations(data)
        if result != 0:
            print(f"Error: {result}, File: {file_path}")
            return result
        # Check "weekday, saturday, holiday" field
        result = check_time(data, "weekday")
        if result != 0:
            print(f"Error: {result}, File: {file_path}")
            return result
        result = check_time(data, "saturday")
        if result != 0:
            print(f"Error: {result}, File: {file_path}")
            return result
        result = check_time(data, "holiday")
        if result != 0:
            print(f"Error: {result}, File: {file_path}")
            return result
    except FileNotFoundError:
        print(f"Error: 10000001, File: {file_path}")
        return 10000001
    except json.JSONDecodeError:
        print(f"Error: 10000002, File: {file_path}")
        return 10000002
    print(f"OK: {file_path}")
    return 0


# "date" フィールドのチェック
def check_date(data):
    if "date" not in data:
        # "date" フィールドが存在しなかった
        return 11000001
    date_string = data["date"]
    date_pattern = re.compile(r"^\d{4}/\d{2}/\d{2}$")
    if date_pattern.match(date_string) == None:
        # "date" フィールドの値が日付形式ではなかった
        return 11000002
    return 0


# "name" フィールドのチェック
def check_name(data):
    if "name" not in data:
        # "name" フィールドが存在しなかった
        return 12000001
    name_string = data["name"]
    if "name" == "":
        # "name" が空だった
        return 12000002
    return 0


# "destinations" フィールドのチェック
def check_destinations(data):
    if "destinations" not in data:
        # "destinations" フィールドが存在しなかった
        return 13000001
    if not isinstance(data["destinations"], list):
        # "destinations" フィールドが list 形式でない
        return 13000002
    if not data["destinations"]:
        # "destinations" フィールドが空っぽ
        return 13000003
    name_string = data["name"]
    for destination in data["destinations"]:
        if name_string == destination:
            # 自バス停が destinations に含まれている
            return 13000004
    return 0


# "weekday, saturday, holiday" フィールドのチェック
def check_time(data, field):
    if field not in data:
        # フィールドが存在しなかった
        return 14000001
    if not isinstance(data[field], list):
        # フィールドが list 形式でない
        return 14000002
    count = 0
    previousItem = ""
    for currentItem in data[field]:
        if count >= 1:
            previousTime = convert_time_to_int(previousItem)
            currentTime = convert_time_to_int(currentItem)
            if previousTime > currentTime:
                print(f"[Error] {field} [{count}] : {previousItem} -> {currentItem}")
                return 14000003
        # Prepare to next loop
        previousItem = currentItem
        count = count + 1
    return 0


def convert_time_to_int(time: str) -> int:
    if not re.match(r"^\d{2}:\d{2}$", time):
        raise ValueError(f"{time} is unexpected format.")
    hh, mm = map(int, time.split(":"))
    if not (0 <= hh <= 24 and 0 <= mm <= 59):
        raise ValueError(f"{time} is unexpected range.")
    return hh * 100 + mm


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_timetable.py <file_path>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        result = check_timetable(file_path)
        sys.exit(result)
