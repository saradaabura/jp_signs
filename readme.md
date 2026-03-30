# このMODについて
AI(Gemini)によって作られました

minecloniaで日本語を打つことができる看板が追加されるMOD。漢字は対応していないが、ひらがなが使える。
# 動作確認
- Mineclonia 0.120.1
- Luanti 5.15 x64
- Luanti dev-5.16
# 問題
- (さっきも書いたけど)漢字使えない
- 濁点・半濁点も不完全

# To Do
- 対応する文字を増やす
- バリエーションを増やす

# 使い方
### ひらがなだけ確実に使えればいい場合
- 左のReleaseから```jp_signs.7z```をダウンロードする。
- 展開し、luanti内のmodsフォルダにコピー・移動
- ワールド設定でこのModを有効にする

### 他の文字にも対応させたい場合
- このリポジトリをクローンする。
- texture_generate_Program内のmain.pyを編集し、追加したい文字入れる(main.py要参照)
- main.pyを実行する
- texture_generate_Program/textures内の画像データをtextures(modの,リポジトリ直下の)にコピーする
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