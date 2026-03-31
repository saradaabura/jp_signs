"""
Only Windows!
It will not work in non-Windows environments such as Linux.


LinuxなどのWindows以外の環境では動かない。

日本語版で!
"""
import os
from PIL import Image, ImageFont, ImageDraw
import requests

"""
Pillowインストールしてから
"""

# --- 設定 ---
FONT_PATH = "C:/Windows/Fonts/msgothic.ttc" # 好きなフォントに変更できる(UDフォントが見やすいと思う)
FONT_SIZE = 14
CHAR_SIZE = 16
OUTPUT_DIR = "textures"
# modのtexturesに保存する

# 日本のひらがな・カタカナ・記号・英数字・常用漢字をダウンロードする
url = "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/refs/heads/release/2.7/ppocr/utils/dict/japan_dict.txt"
response = requests.get(url)
joyo_filename = "jouyou.txt"
if response.status_code == 200:
    with open(joyo_filename, "w", encoding="utf-8") as f:
        f.write(response.text)
    print("ダウンロードしたよ")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


with open(joyo_filename, "r", encoding="utf-8") as f:
    for char in f:
        char = char.strip()# 改行文字削除
        if not char: # 空行は飛ばす
            continue
        img = Image.new("RGBA", (CHAR_SIZE, CHAR_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), char, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((CHAR_SIZE - w) / 2, (CHAR_SIZE - h) / 2 - 2), char, font=font, fill=(255, 255, 255, 255))
        
        # ここ大事!
        code_hex = "{:x}".format(ord(char))
        filename = f"jp_f_{code_hex}.png" 
        img.save(os.path.join(OUTPUT_DIR, filename))

# カスタム・追加用テクスチャ生成
CHAR_LIST = " 　"# strで
"""
空白(スペース)などのテクスチャをここで作る（何もない画像だが）
"""
for char in CHAR_LIST:
    img = Image.new("RGBA", (CHAR_SIZE, CHAR_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((CHAR_SIZE - w) / 2, (CHAR_SIZE - h) / 2 - 2), char, font=font, fill=(255, 255, 255, 255))
    code_hex = "{:x}".format(ord(char))
    filename = f"jp_f_{code_hex}.png"
    img.save(os.path.join(OUTPUT_DIR, filename))
print("ジェネレーティド!")
