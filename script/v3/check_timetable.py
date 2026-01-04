import json
import re
import os
import argparse
from typing import List

# 指定されたディレクトリ以下にある timetable のフォーマットチェック
# チェックコードは validate_timetable() を使用
# ディレクトリは複数階層を想定し、再帰呼び出しを使って対応
# 基本的にはディレクトリ以下のすべての json ファイルをチェックするが、
# その際にチェック対象から除外する json ファイル名を ignore_list にて指定
# 戻り値: 検出したエラーの個数
def check_timetable_by_directory(directory_path: str, ignore_list: List[str]) -> int:
    error_count = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json") and file not in ignore_list:
                file_path = os.path.join(root, file)
                error_count += check_timetable_by_file(file_path)
    return error_count

# 指定された json ファイルの timetable のフォーマットチェック
# チェックコードは validate_timetable() を使用
# 戻り値: 検出したエラーの個数
def check_timetable_by_file(file_path):
    print(f"Check {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return 1
    
    errors = validate_timetable(data)
    if errors:
        print("フォーマットチェックに失敗しました:")
        for err in errors:
            print(f" - {err}")
    return len(errors)

# json 形式の timetable のフォーマットチェック
# 戻り値: 検出したエラー内容のリスト
def validate_timetable(data: dict) -> List[str]:
    errors = []

    # 1. date の形式チェック（YYYY/MM/DD）
    date = data.get("date", "")
    date_pattern = r'^\d{4}/\d{2}/\d{2}$'
    if not re.match(date_pattern, str(date)):
        errors.append(f"date の形式が不正です (値: '{date}', 期待値: 'YYYY/MM/DD')")

    # 2. name が空文字列でないか
    name = data.get("name", "")
    if not isinstance(name, str) or name.strip() == "":
        errors.append(f"name が空、または文字列ではありません (値: '{name}')")

    # 3. system が空文字列でないか
    system = data.get("system", "")
    if not isinstance(system, str) or system.strip() == "":
        errors.append(f"system が空、または文字列ではありません (値: '{system}')")

    # 4. destinations が1つ以上の文字列で構成された配列か
    destinations = data.get("destinations", [])
    if not isinstance(destinations, list) or len(destinations) < 1:
        errors.append(f"destinations が1つ以上の要素を持つ配列ではありません (要素数: {len(destinations) if isinstance(destinations, list) else 'N/A'})")
    elif not all(isinstance(d, str) and d.strip() != "" for d in destinations):
        invalid_items = [d for d in destinations if not (isinstance(d, str) and d.strip() != "")]
        errors.append(f"destinations に不正な要素が含まれています (不正な要素: {invalid_items})")

    return errors

# route.json のフォーマットチェック
# 戻り値: 検出したエラー内容のリスト
def validate_route(data: dict) -> List[str]:
    errors = []

    # 1. system が空文字列でないか
    system = data.get("system", "")
    if not isinstance(system, str) or system.strip() == "":
        errors.append(f"system が空、または文字列ではありません (値: '{system}')")

    # 2. busstops が1つ以上の要素を持つ配列か
    busstops = data.get("busstops", [])
    if not isinstance(busstops, list) or len(busstops) < 1:
        errors.append(f"busstops が1つ以上の要素を持つ配列ではありません (要素数: {len(busstops) if isinstance(busstops, list) else 'N/A'})")
    
    # 3. route_url が正しい形式か
    route_url = data.get("route_url", "")
    if not isinstance(route_url, str) or not route_url.startswith("https://"):
        errors.append(f"route_url が不正です (値: '{route_url}')")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Timetable JSON フォーマットチェック")
    parser.add_argument("--mode", choices=["file", "directory"], required=True, help="チェックモード: file または directory")
    parser.add_argument("--path", required=True, help="対象のファイルまたはディレクトリのパス")
    parser.add_argument("--ignore", default="", help="除外する JSON ファイル名（カンマ区切り）")

    args = parser.parse_args()

    if args.mode == "file":
        error_count = check_timetable_by_file(args.path)
    elif args.mode == "directory":
        ignore_list = [name.strip() for name in args.ignore.split(",") if name.strip()]
        error_count = check_timetable_by_directory(args.path, ignore_list)

    print(f"検出されたエラー数: {error_count}")
    exit(error_count)
