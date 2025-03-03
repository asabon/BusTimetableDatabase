import json

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
