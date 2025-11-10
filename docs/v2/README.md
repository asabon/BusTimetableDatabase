# 時刻表データベース for v2

## 概要

## ディレクトリ・ファイル構成

`v2` に関連するものだけを抽出。

```text
+ .github/
  + workflows/
    + generate_v2.yml
    + release_v2.yml
+ database/
  + kanachu/
    + v2/
      + database/
        + 0000800088/       : 路線ディレクトリ(内容は後述)
        + ...
        + busstops.json     : バス停一覧
+ release/
  + kanachu/
    + v2/
      + database.zip        : database/kanachu/v2/database 以下を zip 圧縮。
      + info.json           : database/kanachu/v2/database のハッシュ値。
+ script/
  + common/
  + v2/
```

---
## 各ファイルについて

### リリース情報ファイル(info.json)

* リリース情報を `info.json` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v2/info.json

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

* `database/kanachu/v2` の内容を圧縮し、`database.zip` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v2/database.zip

### バス停一覧

`busstops.json` として配置されている。

```json
{
    "busstops": [
        {
            "node_id": "00019243",
            "lat": "35.538771",
            "lng": "139.490282",
            "name": "堀の内(横浜市青葉区)",
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

### 経路情報ファイル

各路線ディレクトリ以下に、 `route.json` として配置されている。

```json
{
    "system": "町12",
    "busstops": [
        {
            "index": "1",
            "id": "00129544",
            "name": "町田ターミナル",
            "lat": "35.540084",
            "lng": "139.449491"
        },
        //...
    ],
    "route_url": "https://www.kanachu.co.jp/dia/route/index/cid:0000800088/"
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

```json
{
    "date": "2025/04/01",
    "name": "町田ターミナル",
    "position": "-",
    "system": "町12",
    "destinations": [
        "町田バスセンター",
        //...
        "木曽南団地"
    ],
    "weekday": [
        "17:44",
        //...
        "20:55"
    ],
    "saturday": [
        "9:51",
        //...
        "20:40"
    ],
    "holiday": [],
    "url": "https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:0000800088-1/node:00129544/kt:0/lname:/"
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

---
