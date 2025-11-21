# 時刻表データベース for v3

## 概要

v3 データベースの仕様について記載する。

## ディレクトリ・ファイル構成

`v3` に関連するものだけを抽出。

```text
+ database/
  + kanachu/
    + v3/
      + database/
        + 0000800009/       : 路線ディレクトリ(フォルダ名は路線ID)
          + route.json      : 路線情報
          + 01.json         : 時刻表データ(ファイル名はインデックス)
          + ...
        + ...
        + busstops.json     : バス停一覧
        + route_ids.json    : 路線ID一覧
+ release/
  + kanachu/
    + v3/
      + database.zip        : database/kanachu/v3/database 以下を zip 圧縮。
      + info.json           : database/kanachu/v3/database のハッシュ値。
```

---
## 各ファイルについて

### リリース情報ファイル(info.json)

* リリース情報を `info.json` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v3/info.json

* ファイルの中身は以下のようになっている。
    ```json
    {
      "hash": "1b3e4b505bb20eadff72f760f8328e505de5c6c65b12639eedf98d8ffc35eba5"
    }
    ```
    * hash
      * データベースのハッシュ値
      * この値が変わっていたら「データベースが更新された」とみなせる。

### リリースファイル(database.zip)

* `database/kanachu/v3/database` の内容を圧縮し、`database.zip` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v3/database.zip

### バス停一覧(busstops.json)

`busstops.json` として配置されている。

```json
{
    "busstops": [
        {
            "node_id": "00019206",
            "lat": "35.542788",
            "lng": "139.496985",
            "name": "中恩田橋",
            "position": "-"
        },
        //...
    ]
}
```

* node_id
  * バス停ID
* lat
  * 緯度
* lng
  * 経度
* name
  * バス停名称
* position
  * バス停の位置を表す補足情報
  * ウェブサイトから得られる情報と、そうでないものがある
  * そうでないものは、主観で設定している

### 路線ID一覧(route_ids.json)

`route_ids.json` として配置されている。
データベースに含まれる全ての路線IDのリスト。

```json
[
    "0000800009",
    "0000800012",
    //...
]
```

### 路線情報ファイル(route.json)

各路線ディレクトリ以下に、 `route.json` として配置されている。

```json
{
    "system": "厚74",
    "busstops": [
        {
            "index": "1",
            "id": "00128390",
            "name": "長坂(厚木市)",
            "lat": "35.523287",
            "lng": "139.351671"
        },
        //...
    ],
    "route_url": "https://www.kanachu.co.jp/dia/route/index/cid:0000800009/"
}
```

* system
  * 系統名
* busstops
  * 経由する順番に「バス停」の情報が並んでいる。
  * バス停情報
    * index: 順番
    * id: バス停ID
    * name: バス停名
    * lat: このバス停の経度
    * lng: このバス停の緯度
* route_url
  * この情報の取得元となるURL

### 時刻表ファイル

各路線ディレクトリ内に、`数値(index).json` 形式のファイル名で配置されている。
ファイル名の数値は、`route.json` の `busstops` 内の `index` と対応している。

```json
{
    "date": "2020/11/16",
    "name": "長坂(厚木市)",
    "position": "-",
    "system": "厚74",
    "destinations": [
        "長坂下",
        "上依知中央",
        //...
    ],
    "weekday": [
        "6:35",
        "6:55"
    ],
    "saturday": [],
    "holiday": [],
    "url": "https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:0000800009-1/node:00128390/kt:0/lname:/"
}
```

* date
  * 時刻表更新日
* name
  * バス停名
* position
  * 同じ名前のバス停が複数個所にある場合の位置を識別する情報
  * 神奈中データベースからは取得しておらず、手作業で管理している
  * 該当するデータがない場合は `-` を設定している
* system
  * 系統
* destinations
  * 該当のバス停から経由するバス停を順に並べている
* weekday, saturday, holiday
  * それぞれ「平日」「土曜」「休日」の時刻表データ
  * `H:MM` 形式の文字列として格納
* url
  * この時刻表データの取得元となるURL
