# 時刻表データベース for v1

## 概要

## ディレクトリ・ファイル構成

`v1` に関連するものだけを抽出。

```text
+ database/
  + kanachu/
    + v1/
      + database/
        + 町03_玉川学園前駅行_原町田五丁目経由_町田バスセンター発/
          + 01_町田バスセンター.json
          + ...
          + route.json
        + ...      
+ releaes/
  + kanachu/
    + v1/
      + database.zip 
      + info.json
```

## ファイルフォーマット

### リリース情報ファイル

* リリース情報を `info.json` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v1/info.json

```json
{
  "hash": "1b3e4b505bb20eadff72f760f8328e505de5c6c65b12639eedf98d8ffc35eba5"
}
```

* hash
  * データベースのハッシュ値
  * この値が変わっていたら「データベースが更新された」とみなせる。

### リリースファイル

* `database/kanachu/v1` の内容を圧縮し、`database.zip` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v1/database.zip

### 路線情報ファイル

各路線ディレクトリ以下に、 `route.json` として配置されている。

```json
{
  "route": [
    "町田バスセンター",
    // ...
    "玉川学園前駅"
  ],
  "url": "https://www.kanachu.co.jp/dia/route/index/cid:0000803702/"
}
```

* route
  * 経由する順番に「バス停」の名称が並んでいる。
* url
  * この情報の取得元となるURL

### 時刻表ファイル

各路線ディレクトリ内に、`系統_バス停名.json` 形式のファイル名で配置されている。

```json
{
  "date": "2025/04/01",
  "name": "町田バスセンター",
  "position": "-",
  "system": "町03",
  "destinations": [
    "原町田五丁目",
    // ...
    "玉川学園前駅"
  ],
  "weekday": [
    "8:36",
    "9:55"
  ],
  "saturday": [],
  "holiday": [],
  "url": "https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:0000803702-2/node:00025625/kt:0/lname:/"
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
