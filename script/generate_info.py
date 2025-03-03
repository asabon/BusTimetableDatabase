import sys
from edit_json import read_json_file
from edit_json import write_json_file
from edit_json import get_value_from_json
from edit_json import set_value_in_json


def generate_info(file_path, hash):
    json_data = read_json_file(file_path)
    if json_data is None:
        json_data = {} # ファイルが存在しなかったら新規作成
    set_value_in_json(json_data, "hash", hash)
    write_json_file(file_path, json_data)
    return


if __name__ == '__main__':
    file_path = sys.argv[1]
    hash = sys.argv[2]
    generate_info(file_path, hash)
