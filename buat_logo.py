import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = r"C:\Windows\Fonts"
OUT = r"dokumen\surat\hadis.my\logo_pustakahadith.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

TEAL = "#5CBF85"
TEAL_LIGHT = "#7FD39A"
TEXT_MUTED = "#9C9589"

SCALE = 5  # resolusi tinggi

f_pustaka = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 21 * SCALE)  # weight 800
f_hadith = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuil.ttf"), 21 * SCALE)  # weight 300
f_ver = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 12 * SCALE)      # weight 400

t1, t2, t3 = "Pustaka", "Hadith", " v1.0.0"
w1, w2, w3 = (f_pustaka.getlength(t1), f_hadith.getlength(t2), f_ver.getlength(t3))
a1, d1 = f_pustaka.getmetrics()
a2, d2 = f_hadith.getmetrics()
a3, d3 = f_ver.getmetrics()
asc = max(a1, a2, a3)
desc = max(d1, d2, d3)
pad = 12 * SCALE

total_w = int(w1 + w2 + w3) + 2 * pad
total_h = asc + desc + 2 * pad

img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

x = pad
y_base = pad + asc
# Pustaka (bold teal)
d.text((x, y_base - a1), t1, font=f_pustaka, fill=TEAL)
x += w1
# Hadith (light teal)
d.text((x, y_base - a2), t2, font=f_hadith, fill=TEAL_LIGHT)
x += w2
# v1.0.0 (muted)
d.text((x, y_base - a3), t3, font=f_ver, fill=TEXT_MUTED)

img.save(OUT)
print("saved", OUT, img.size)
