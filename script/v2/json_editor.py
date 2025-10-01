import json

class JsonEditor():
    def __init__(self, file_path):
        self.file_path = file_path
        self.json_data = self.load()

    # JSONファイルを読み込む
    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # JSONファイルに書き込む
    def save(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, ensure_ascii=False, indent=4)
                # ファイルの最後に改行を追加
                f.write('\n')
        except Exception as e:
            print(f"Error saving JSON: {e}")

    # 階層キーで値を取得する
    # "." で階層を指定できる（例: "parent.child.name"）
    # 数値で配列のインデックスも指定できる（例: "items.2.name"）
    def get_value(self, key):
        keys = key.split(".")
        d = self.json_data
        for k in keys:
            if isinstance(d, dict) and k in d:
                # Keyが辞書に存在する場合
                d = d[k]
            elif isinstance(d, list) and k.isdigit():
                idx = int(k)
                if 0 <= idx < len(d):
                    d = d[idx]
                else:
                    # インデックスが範囲外の場合は空文字を返す
                    return ""
            else:
                # Keyが存在しない場合は空文字を返す
                return ""
        return d

    # 階層キーで値をセットする
    def set_value(self, key, value):
        keys = key.split(".")
        d = self.json_data
        for i, k in enumerate(keys[:-1]):
            next_k = keys[i+1]
            if isinstance(d, dict):
                if k not in d:
                    # 次のキーが数字ならリスト、そうでなければ辞書
                    d[k] = [] if next_k.isdigit() else {}
                d = d[k]
            elif isinstance(d, list) and k.isdigit():
                idx = int(k)
                while len(d) <= idx:
                    d.append({} if not next_k.isdigit() else [])
                d = d[idx]
            else:
                return self.json_data
        last_k = keys[-1]
        if isinstance(d, dict):
            d[last_k] = value
        elif isinstance(d, list) and last_k.isdigit():
            idx = int(last_k)
            while len(d) <= idx:
                d.append(None)
            d[idx] = value
        return self.json_data
