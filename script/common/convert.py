import unicodedata

# 文字列内の英数字と記号を半角に変換して戻り値として返す（全角カタカナはそのまま）
# 引数がリストの場合は、リストの個々のアイテムに対して処理を実行する
def to_half_width(text):
    if isinstance(text, list):
        return [to_half_width(item) for item in text]
    return ''.join(unicodedata.normalize('NFKC', char) for char in text)

# ファイル名に使えない文字列は半角に変換せず、それ以外は半角にする（全角カタカナはそのまま）
def to_safe_half_width(text):
    unsafe_chars = {
        "/": "／",
        "\\": "￥",
        ":": "：",
        "*": "＊",
        "?": "？",
        "<": "＜",
        ">": "＞",
        "|": "｜"
    }

    if isinstance(text, list):
        return [to_safe_half_width(item) for item in text]

    converted_text = to_half_width(text)
    return ''.join(unsafe_chars[char] if char in unsafe_chars else char for char in converted_text)
