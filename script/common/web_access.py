import urllib
import urllib.request
import ssl
import hashlib
import os

# このスクリプトと同じディレクトリに "cache" ディレクトリを作成しキャッシュデータを格納する
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, "cache")

# URLからキャッシュ用のファイル名を生成する
def get_cached_filename(url):
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hashed_url}.txt")

# URLにアクセスしてHTMLを取得する
# キャッシュにそのURLのデータがあったらそれを返す
# キャッシュを使う・使わないは force_update で指定可能
# - force_update: キャッシュを使わずに強制的に読み込みなおすかどうか
#   - True:  キャッシュを使わない
#   - False: キャッシュを使う
def get_data(url, force_update=False):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = get_cached_filename(url)

    # キャッシュが存在したらそれを読み込む
    if os.path.exists(cache_file) and not force_update:
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()

    # ウェブアクセスしてデータを取得する
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    req = urllib.request.Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=context) as f:
            result = f.read().decode()

        # キャッシュに保存
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(result)

        return result
    except urllib.error.HTTPError as e:
        print(f'HTTP Error: {e.code} {e.reason}')
        return None
    except urllib.error.URLError as e:
        print(f'URL Error: {e.reason}')
        return None
