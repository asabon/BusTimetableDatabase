[![Release](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/release.yml/badge.svg?branch=main&event=push)](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/release.yml)
[![Check database](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/check_database.yml/badge.svg?branch=main&event=push)](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/check_database.yml)

# BusTimetableDatabase

## 概要

* json 形式で作成した、神奈中バスの時刻表データベース。
* データは神奈中のウェブサイトから取得。

## 目的

* 自作のバスの時刻表を扱うアプリから利用する。

## ディレクトリ構成

```text
+ database/
  + 神奈川中央交通/
    + 町12_木曽南団地_境川団地経由_町田ターミナル発
      + 02_町田バスセンター.json
    + ...
+ release/
  + database.zip
  + hash.txt
+ script/
```

## ファイル構造

```json
{
  "date": "2001/01/01",
  "name": "町田バスセンター",
  "position": "2番のりば",
  "system": "町12",
  "destinations": [
    "町田市役所市民ホール前",
    ...(省略)
  ],
  "weekday": [
    "17:48",
    ...(省略)
  ],
  "saturday": [],
  "holiday": [],
  "url": "https://...(省略)"
}
```

## 注意点

* 自分が必要な部分しか作成していない。

## LICENSE

MIT License.
