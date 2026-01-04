import urllib
import urllib.request
import ssl
import hashlib
import os
import datetime
import json

# このスクリプトと同じディレクトリに "cache" ディレクトリを作成しキャッシュデータを格納する
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache")
CACHE_EXPIRATION_DAYS = 7

# URLからキャッシュ用のファイル名を生成する
def get_cached_filename(url, cache_dir=CACHE_DIR):
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(cache_dir, f"{hashed_url}.txt")

def get_meta_filename(url, cache_dir=CACHE_DIR):
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(cache_dir, f"{hashed_url}.meta.json")

# URLにアクセスしてHTMLを取得する
# キャッシュにそのURLのデータがあったらそれを返す
# キャッシュを使う・使わないは force_update で指定可能
# - force_update: キャッシュを使わずに強制的に読み込みなおすかどうか
#   - True:  キャッシュを使わない
#   - False: キャッシュを使う
def get_data(url, force_update=False, cache_dir=CACHE_DIR, cache_expiration_days=CACHE_EXPIRATION_DAYS):
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = get_cached_filename(url, cache_dir=cache_dir)

    cache_valid = False

    if os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        last_modified = datetime.datetime.fromtimestamp(mtime)
        now = datetime.datetime.now()
        age = (now - last_modified).days
        cache_valid = age < cache_expiration_days

    # キャッシュが存在したらそれを読み込む
    if os.path.exists(cache_file) and cache_valid and not force_update:
        with open(cache_file, "r", encoding="utf-8") as f:
            # print(f"Cache file found: {cache_file}")
            return f.read()

    # ウェブアクセスしてデータを取得する
    meta_file = get_meta_filename(url, cache_dir=cache_dir)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # メタデータがあれば条件付きリクエスト用ヘッダーを追加
    if os.path.exists(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                if meta.get("etag"):
                    headers["If-None-Match"] = meta["etag"]
                if meta.get("last_modified"):
                    headers["If-Modified-Since"] = meta["last_modified"]
        except Exception:
            pass

    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    req = urllib.request.Request(url=url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=context) as f:
            result = f.read().decode()
            etag = f.headers.get("ETag")
            last_mod = f.headers.get("Last-Modified")

        # キャッシュに保存
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(result)
        
        # メタデータを保存
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump({"etag": etag, "last_modified": last_mod}, f, indent=4)

        # print(f"Cache file created: {cache_file}")
        return result
    except urllib.error.HTTPError as e:
        if e.code == 304:
            # print(f"304 Not Modified: {url}")
            # タイムスタンプを更新して延命
            if os.path.exists(cache_file):
                os.utime(cache_file, None)
                with open(cache_file, "r", encoding="utf-8") as f:
                    return f.read()
        print(f'HTTP Error: {e.code} {e.reason}')
        return None
    except urllib.error.URLError as e:
        print(f'URL Error: {e.reason}')
        return None
