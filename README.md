# BusTimetableDatabase

## 概要
* json 形式で作成した、神奈中バスの時刻表データベース。
* データは神奈中バスのウェブサイトから取得。(Webスクレイピング)
* GitHub Actions を使って定期的に更新する。

## 目的
* 自作のバスの時刻表を扱うアプリから利用することを主目的としている。
* その一方で、同じようなことを実現したい誰かの役に立てたら・・・という思いから公開。

## 注意点
* データは神奈中バスのウェブサイトから取得している。
* そのため、神奈中バスのウェブサイトの構造変更によりデータ取得ができなくなる可能性がある。
* データの正確性については保証しない。

## ディレクトリ構成

```text
+ .github/
  + workflows/              : GitHub Actions を使った CI/CD 用ワークフロー
  + copilot-instructions.md : Copilot カスタムインストラクション
+ ci/                       : GitHub Actions から参照される設定ファイル置き場
+ database/                 : データベースディレクトリ
+ release/                  : リリースディレクトリ
+ script/                   : スクリプトディレクトリ
+ test/                     : テストスクリプトディレクトリ
+ LICENSE                   : ライセンスファイル(MIT)
+ README.md                 : このファイル
+ requirements.txt          : pip 設定ファイル
```

### database

* 時刻表データが json 形式で格納されている。
* 詳細は、 docs/ 以下を参照。

### release

* database ディレクトリの時刻表データが zip 形式で圧縮した状態で格納されている。
* 詳細は、 docs/ 以下を参照。

## LICENSE

MIT License.
