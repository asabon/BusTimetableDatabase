[![Release](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/release.yml/badge.svg?branch=main&event=push)](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/release.yml)
[![Check database](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/check_database.yml/badge.svg?branch=main&event=push)](https://github.com/asabon/BusTimeTableDatabase/actions/workflows/check_database.yml)

# ButTimeTableDatabase

## 概要

* json 形式で作成した、神奈中バスの時刻表データベース。
* 手作業での入力のため、自分が必要な部分しか入力してない。

## 目的

* 自作のバスの時刻表を扱うアプリから参照できるデータの構築。
* データを public リポジトリで公開することで自分以外の人にもデータ編集できるようにする。
* 最終的には自動的に最新の時刻表を取り込めるようにしたい・・・

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

## LICENSE

MIT License.
