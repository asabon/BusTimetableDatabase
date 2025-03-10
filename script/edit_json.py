import json
import sys

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"error {e}")
        return None


def write_json_file(file_path, json_data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"error {e}")


def get_value_from_json(json_data, key):
    return json_data.get(key, "")


def set_value_in_json(json_data, key, value):
    json_data[key] = value
    return json_data


def update_json_file(file_path, key, value):
    json_data = read_json_file(file_path)
    if json_data is None:
        json_data = {} # ファイルが存在しなかったら新規作成
    set_value_in_json(json_data, key, value)
    write_json_file(file_path, json_data)
    return


if __name__ == '__main__':
    if len(sys.argv > 1):
        command = sys.argv[1]
    else:
        print("Usage: python edit_json.py <parameters>")
        print("  The <parameters> are below.")
        print("    - update <file_path> <key> <value>")
        sys.exit(1)
    if command == "update":
        if len(sys.argv == 5):
            file_path = sys.argv[2]
            key = sys.argv[3]
            value = sys.argv[4]
            update_json_file(file_path, key, value)
        else:
            sys.exit(2)
    else:
        print("Error: Command unknown")
        sys.exit(3)
