# 「ウマ娘」イベント選択肢検索ツールを作る！

[Qiita 「画像認識ウマ娘イベント選択肢チェッカー」をPythonで作るチュートリアル](https://qiita.com/Cartelet/items/9affdd7440c218bc080d)  
↑こちらの記事を参考に作らせて頂きました  

普段PC版でよく愛馬の育成するのですが、真剣に評価ランク上げようとするとイベントの選択肢の各効果を調べる必要があります。ゲーム画面の隣に攻略サイトのWebブラウザを待機させ、イベント発生ごとに検索する…意外と面倒。こんな悩みを解決するのに丁度よいのでは！？作るしかない(#^.^#)

# プログラムの実行環境

`Python 3.6`

## 使用ライブラリ

- python ライブラリ
  - pyautogui
  - opencv-python
  - numpy
  - PIL
  - pyocr
  - PySimpleGUI
- OCR
  - Tesseract

### Conda環境を利用したセットアップ例
```
# create conda env
conda install python=3.6
conda create --name uma python=3.6
conda activate uma

# install libs
pip install \
  pyautogui \
  opencv-python \
  numpy \
  pyocr \
  pysimplegui

# start application
python app.py
```

## OCRツールの用意

オープンソフトで有名な[Tesseract](https://github.com/tesseract-ocr/tesseract)を利用。日本語を識別するため、適宜[GitHubリポジトリ](https://github.com/tesseract-ocr/tessdata)から学習モデルを取得すること。その他、詳細は[公式のドキュメント](https://tesseract-ocr.github.io/tessdoc/)

# データの用意
## イベントデータ
当然ですが、検索するイベントのデータが必要です。ここでは、参考先でも言及があったとおり[GameWith ウマ娘攻略wiki](https://gamewith.jp/uma-musume)にあるイベント選択肢チェッカーなる便利サイトから拝借。該当ページでは`js`ファイルに直書きされたデータを利用しているようで、developerツールで覗いてごにょごにょすると見つけられます。  

ちょちょっと修正してjsonで保存。  
`event.json`  
```json
[
  {
    "e": "今日も、明日からも",
    "n": "スペシャルウィーク",
    ....
    "choices": [
      {
        "n": "じゃあ追加トレーニングだ",
        "t": "スピード+20[br]ランダムで『注目株』取得"
      },
      .....
    ]
  },
  ....
]
```

## 育成ウマ娘・サポートカードのアイコン画像
同名のイベントを区別するため、イベントのキャラクターを識別する機能があります。キャラクターの識別に利用するテンプレート画像を用意する必要がありますが、同じく[GameWith ウマ娘攻略wiki](https://gamewith.jp/uma-musume)から拝借。どうやらガチャ画像として使われている様子。  
`icon/*.png`

# プログラムの内容
PC版「ウマ娘・プリティーダービー」の画面をキャプチャしてOCRでUIの文字を認識し、イベントを検索して選択肢の各効果を表示します。

ここまでは参考で紹介されていた通り。以下は追加の実装要素。

1. PySimpleGUIを用いて簡単なUIを実装  
  イベントを検出すると、選択肢の詳細をフローティングウィンドウをゲーム画面脇に表示します。
2. イベントのキャラクターを識別して高精度にイベントを認識  
  複数サポートカード・育成ウマ娘の同名のイベントを区別します。  
  `icon/*.png`に用紙したアイコン画像をテンプレートにイベントがどのウマ娘のものか判定する単純ですが安定・高速の実装です。