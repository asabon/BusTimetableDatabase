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
    destinations_list = data["destinations"]
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_timetable.py <file_path>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        result = check_timetable(file_path)
        sys.exit(result)
