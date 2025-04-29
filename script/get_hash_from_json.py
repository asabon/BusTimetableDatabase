import json
import sys

def get_hash_from_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    hash_value = data.get("hash")
    return hash_value

if __name__ == "__main__":
    filepath = sys.argv[1]
    hash_value = get_hash_from_json(filepath)
    print(hash_value)
