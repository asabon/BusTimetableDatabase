import os
import json
import zipfile
import random

def main():
    # リリースディレクトリへのパス
    # このスクリプトがプロジェクトルートまたは script/v3/ から実行されることを想定しています
    # 別の場所から実行する場合は base_path を調整してください
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../release/kanachu/v3"))
    
    print(f"データ確認先: {base_path}")
    
    if not os.path.exists(base_path):
        print("エラー: リリースディレクトリが見つかりません。")
        return

    # 1. info.json の読み込み
    info_path = os.path.join(base_path, "info.json")
    if not os.path.exists(info_path):
        print("エラー: info.json が見つかりません。")
        return
        
    with open(info_path, 'r', encoding='utf-8') as f:
        info_data = json.load(f)
        
    print("-" * 20)
    print("INFO.JSON 概要")
    print(f"更新日: {info_data.get('updated_at')}")
    print(f"データセットハッシュ: {info_data.get('hash')}")
    print(f"総ルート数: {len(info_data.get('routes', []))}")
    print("-" * 20)

    # 2. busstops.json の読み込み
    busstops_path = os.path.join(base_path, "busstops.json")
    if os.path.exists(busstops_path):
        with open(busstops_path, 'r', encoding='utf-8') as f:
            busstops_data = json.load(f)
        print("BUSSTOPS.JSON 概要")
        stops_list = busstops_data.get("busstops", [])
        print(f"総バス停数: {len(stops_list)}")
        # 例として最初のバス停を表示
        if stops_list:
            first_stop = stops_list[0]
            print(f"バス停サンプル: {first_stop.get('name')} (ID: {first_stop.get('node_id')})")
    else:
        print("警告: busstops.json が見つかりません。")
    print("-" * 20)

    # 3. ランダムなルートzipファイルの検査
    routes = info_data.get('routes', [])
    if routes:
        sample_route = random.choice(routes)
        route_id = sample_route['id']
        zip_filename = f"{route_id}.zip"
        zip_path = os.path.join(base_path, zip_filename)
        
        print(f"ルート検査: {route_id}")
        print(f"Zipファイル: {zip_filename}")
        
        if os.path.exists(zip_path):
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    file_list = zf.namelist()
                    print(f"Zip内のファイル: {file_list}")
                    
                    # Zip内の route.json を読み込んでみる
                    route_json_name = f"{route_id}/route.json"
                    if route_json_name in file_list:
                        with zf.open(route_json_name) as f:
                            route_content = json.load(f)
                            route_name = route_content.get('name') or route_content.get('system', 'N/A')
                            print(f"ルート名: {route_name}")
                            stops = route_content.get('busstops', [])
                            print(f"ルート内のバス停数: {len(stops)}")
                    else:
                        print(f"警告: {route_json_name} がZip内に見つかりません。")
            except Exception as e:
                print(f"Zipファイルの読み込みエラー: {e}")
        else:
            print(f"エラー: Zipファイル {zip_filename} が見つかりません。")
    else:
        print("info.json にルートが見つかりません。")
    print("-" * 20)

if __name__ == "__main__":
    main()
