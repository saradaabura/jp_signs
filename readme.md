# このMODについて
Lua部分はGeminiが,Python部分は私(saradaabura)が作成した。

minecloniaで日本語を打つことができる看板が追加されるMOD。
# 動作確認
- Mineclonia 0.120.1
- Luanti 5.15 x64
- Luanti dev-5.16
# 問題
- ~~(さっきも書いたけど)漢字使えない~~
- ~~濁点・半濁点も不完全~~
**常用漢字を"https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/ppocr/utils/dict/japan_dict.txt"から取得するようにしたので、一般的な漢字はサポート**
- メディアたくさん→ロード時間かかる(約4400個のファイル,計660KB)

# To Do
- 対応する文字を増やす
- バリエーションを増やす(看板自体のテクスチャ)

# 使い方
### とりあえず使いたい方は,,,
- 左のReleaseから```jp_signs.7z```or```jp_signs.zip```をダウンロードする。
- 展開し、luanti内のmodsフォルダにコピー・移動
- ワールド設定でこのModを有効にする

### 他の文字にも対応させたい場合
- このリポジトリをクローンする。
- texture_generate_Program内のmain.pyを編集し、追加したい文字入れる(main.py要参照)
- main.pyを実行する
- texture_generate_Program/textures内の画像データをtextures(modの,リポジトリ直下の)にコピーする(カレントディレクトリがtexture_generate_Programの場合)
- texturesフォルダ,init.lua mod_confを一つのフォルダにまとめる(以下のような構成)
```
jp_signs
|
|--textures(コピーされた)
|--init.lua
|--mod.conf
```
- Luanti内のmodsフォルダにjp_signsをコピーする
- ワールド設定でこのmodを有効にする

**試していないのでわからないですが、これによって他の文字(=日本語以外の文字。ハングルとか)にも対応できるかもしれないです。**