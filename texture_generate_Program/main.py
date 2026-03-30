"""
Only Windows!
It will not work in non-Windows environments such as Linux.

Also, it will not work on English versions of Windows (due to missing fonts).

LinuxなどのWindows以外の環境では動かない。
また、英語版Windowsでも動かない。(フォントがないため)

日本語版で!
"""
import os
from PIL import Image, ImageFont, ImageDraw
"""
Pillowインストールしてから
"""

# --- 設定 ---
FONT_PATH = "C:/Windows/Fonts/msgothic.ttc" 
FONT_SIZE = 14
CHAR_SIZE = 16
OUTPUT_DIR = "textures"
#このディレクトリのtexturesに保存される!

# 英語大小、ひらがな大小、カタカナ大小、数字、記号
CHAR_LIST = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
    "ぁぃぅぇぉっゃゅょ"
    "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    "ァィゥェォッャュョ"
    "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
    #"ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ"
    "！？。、「」ー"
)
#たぶんここに追加すれば他の文字も追加できる?

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

for char in CHAR_LIST:
    img = Image.new("RGBA", (CHAR_SIZE, CHAR_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((CHAR_SIZE - w) / 2, (CHAR_SIZE - h) / 2 - 2), char, font=font, fill=(255, 255, 255, 255))
    
    # 【重要】文字をUnicodeの16進数に変換してファイル名にする
    code_hex = "{:x}".format(ord(char))
    filename = f"jp_f_{code_hex}.png"
    img.save(os.path.join(OUTPUT_DIR, filename))

print("生成完了！")
