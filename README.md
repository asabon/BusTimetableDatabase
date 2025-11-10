# BusTimetableDatabase

## 概要
* json 形式で作成した、神奈中バスの時刻表データベース。
* データは神奈中バスのウェブサイトから取得。(Webスクレイピング)

## 目的
* 自作のバスの時刻表を扱うアプリから利用する。
* その一方で、同じようなことを実現したい誰かの役に立てたら・・・という思いから公開。

## 注意点
* データは神奈中バスのウェブサイトから取得しているため、ウェブサイトの構造変更によりデータ取得ができなくなる可能性がある。
* データの正確性については保証しない。

## ディレクトリ構成

```text
+ .github/
  + workflows/
  + copilot-instructions.md : Copilot カスタムインストラクション
+ ci/                       : GitHub Actions から呼ばれる Danger の設定ファイル群
+ database/
  + kanachu/
    + v1/                   : 旧バージョン（アプリが新バージョンに移行したら削除予定）
    + v2/                   : 新バージョン（アプリ対応中）
+ release/                  : リリースディレクトリ。database の内容が .zip 化されて置かれている。
  + kanachu/
    + v1/                   : 旧バージョン（アプリが新バージョンに移行したら削除予定）
    + v2/                   : 新バージョン（アプリ対応中）
+ script/
  + common/
  + v1/
  + v2/
+ test/
+ LICENSE
+ README.md
+ requirements.txt
```

---
### v1

#### データベースディレクトリ

```text
+ database/
  + kanachu/
    + v1/
      + database/
        + 町03_玉川学園前駅行_原町田五丁目経由_町田バスセンター発/  : 路線ディレクトリ
          + 01_町田バスセンター.json
          + ...
          + route.json
        + ...      
```

##### 路線情報ファイル

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

##### 時刻表ファイル

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

#### リリースディレクトリ

```text
+ releaes/
  + kanachu/
    + v1/
      + database.zip
      + info.json
```

##### リリース情報ファイル

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

##### リリースファイル

* `database/kanachu/v1` の内容を圧縮し、`database.zip` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v1/database.zip

---
### v2

#### データベースディレクトリ

```text
+ database/
  + kanachu/
    + v2/
      + database/
        + 0000800088: 路線ディレクトリ
          + 01.json
          + ...
          + route.json
        + ...      
```

##### 路線情報ファイル

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

##### 時刻表ファイル

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

#### リリースディレクトリ

```text
+ releaes/
  + kanachu/
    + v2/
      + database.zip
      + info.json
```

##### リリース情報ファイル

* リリース情報を `info.json` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v2/info.json

```json
{
  "hash": "1b3e4b505bb20eadff72f760f8328e505de5c6c65b12639eedf98d8ffc35eba5"
}
```

* hash
  * データベースのハッシュ値
  * この値が変わっていたら「データベースが更新された」とみなせる。

##### リリースファイル

* `database/kanachu/v2` の内容を圧縮し、`database.zip` として配置。
* アプリからは、以下の URL で取得することを期待。
  * https://github.com/asabon/BusTimeTableDatabase/raw/main/release/kanachu/v2/database.zip

## LICENSE

MIT License.
