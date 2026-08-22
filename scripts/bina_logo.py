#!/usr/bin/env python3
"""Penjana mockup logo 'Pustaka Hadis' — Konsep A (Buku Terbuka + Cahaya).

Lukis pada kanvas besar (2048) untuk anti-aliasing, kemudian
downsample ke saiz ikon. Hasilkan:
  - logo_mockup/pustaka_logo_1024.png   (skrin pemula / README)
  - logo_mockup/pustaka_logo_512.png    (splash)
  - logo_mockup/pustaka_logo_256.png    (ikon sumber)
  - logo_mockup/pustaka_logo.ico        (16..256, Windows)
  - logo_mockup/pustaka_logo.svg        (vektor rujukan)

Warna diambil daripada ui/theme.py supaya selaras dengan UI.
"""

import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "logo_mockup")
os.makedirs(OUT, exist_ok=True)

# ── Palet (dari ui/theme.py DARK — kertas hangat mockup, Sesi 55) ──
BG_GRAD_A = "#0F2417"   # TEAL_DARK
BG_GRAD_B = "#282721"   # CARD_BG
BUKU_TEAL = "#5CBF85"   # TEAL (hijau mockup)
BUKU_TEAL_TERANG = "#7FD39A"  # TEAL_LIGHT
CAHAYA = "#E0B35C"      # AMBER_TEXT
CAHAYA_PEKAT = "#E8B94C"
TULISAN = "#E8E4DA"     # TEXT_PRIMARY

N = 2048                # kanvas besar


def bulat_lukis(d, kotak, jejari):
    d.rounded_rectangle(kotak, radius=jejari, fill=None)


def lukis_cahaya(d, cx, cy, r, warna, terang):
    """Bintang cahaya 4 bucu — dua rombus silang. r = jejari luar."""
    # Rombus menegak (bucu atas-bawah + kiri-kanan)
    d.polygon([(cx, cy - r), (cx - r * 0.42, cy),
               (cx, cy + r), (cx + r * 0.42, cy)], fill=warna)
    d.polygon([(cx - r, cy), (cx, cy - r * 0.42),
               (cx + r, cy), (cx, cy + r * 0.42)], fill=terang)


def lukis_buku(d, cx, cy, w, h, warna, terang):
    """Buku terbuka: dua halaman berbentuk V. w = separuh lebar total."""
    # Bahagian kiri (halaman kiri — condong ke bawah-tengah)
    d.polygon([(cx, cy), (cx - w, cy - h * 0.42),
               (cx - w, cy + h * 0.58), (cx, cy + h * 0.62)],
              fill=warna)
    # Bahagian kanan
    d.polygon([(cx, cy), (cx + w, cy - h * 0.42),
               (cx + w, cy + h * 0.58), (cx, cy + h * 0.62)],
              fill=terang)
    # Tulang tengah (garis rendah buku)
    d.polygon([(cx - w * 0.10, cy), (cx + w * 0.10, cy),
               (cx + w * 0.10, cy + h * 0.62),
               (cx - w * 0.10, cy + h * 0.62)],
              fill=warna)


def bina() -> Image.Image:
    """Kembalikan ikon 2048px dengan latar rounded square teal."""
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Latar rounded square — kecerunan menegak TEAL_DARK -> CARD_BG
    j = 0.16 * N
    kotak = (j, j, N - j, N - j)
    jejari = 0.20 * N
    for y in range(int(kotak[1]), int(kotak[3])):
        t = (y - kotak[1]) / (kotak[3] - kotak[1])
        # lerp dua warna
        a = tuple(int(BG_GRAD_A[i:i+2], 16) for i in (1, 3, 5))
        b = tuple(int(BG_GRAD_B[i:i+2], 16) for i in (1, 3, 5))
        c = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
        d.rectangle([kotak[0], y, kotak[2], y], fill=(*c, 255))
    # Potong sudut rounded (lukis empat penjuru lutsinar)
    penutup = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(penutup)
    # Kami guna mask rounded untuk memotong selepas ini (lebih mudah).

    # ── Buku terbuka ────────────────────────────────────────────────
    cx = N / 2
    cy = N * 0.63
    bw = N * 0.34
    bh = N * 0.26
    lukis_buku(d, cx, cy, bw, bh, BUKU_TEAL, BUKU_TEAL_TERANG)

    # ── Cahaya ambar di atas ────────────────────────────────────────
    lukis_cahaya(d, cx, N * 0.33, N * 0.13, CAHAYA_PEKAT, CAHAYA)

    # Bulatan lembut belakang cahaya
    r = N * 0.06
    d.ellipse([cx - r, N * 0.33 - r, cx + r, N * 0.33 + r],
              fill=(255, 212, 79, 90))

    # ── Potong sudut rounded menggunakan mask ───────────────────────
    mask = Image.new("L", (N, N), 0)
    dm = ImageDraw.Draw(mask)
    dm.rounded_rectangle(kotak, radius=jejari, fill=255)
    img.putalpha(Image.composite(mask, Image.new("L", (N, N), 0), mask)
                 .point(lambda v: v if v < 256 else 255))

    # Siasat: putalpha dengan mask. Bina alpha final.
    alpha = img.getchannel("A")
    final_alpha = Image.new("L", (N, N), 0)
    ImageDraw.Draw(final_alpha).rounded_rectangle(kotak, radius=jejari,
                                                  fill=255)
    img.putalpha(final_alpha)
    return img


def utama():
    img = bina()
    for saiz, nama in ((1024, "pustaka_logo_1024.png"),
                       (512, "pustaka_logo_512.png"),
                       (256, "pustaka_logo_256.png"),
                       (128, "pustaka_logo_128.png"),
                       (64, "pustaka_logo_64.png"),
                       (48, "pustaka_logo_48.png"),
                       (32, "pustaka_logo_32.png"),
                       (16, "pustaka_logo_16.png")):
        p = os.path.join(OUT, nama)
        img.resize((saiz, saiz), Image.LANCZOS).save(p)
        print("  %4d  %s" % (saiz, p))

    # ICO — masukkan pelbagai saiz
    ico = os.path.join(OUT, "pustaka_logo.ico")
    img.resize((256, 256), Image.LANCZOS).save(
        ico, sizes=[(256, 256), (128, 128), (64, 64), (48, 48),
                    (32, 32), (24, 24), (16, 16)])
    print("  ICO  %s" % ico)

    # SVG vektor ringkas (rujukan) — bukan terbitan raster.
    svg = os.path.join(OUT, "pustaka_logo.svg")
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG_GRAD_A}"/>
      <stop offset="1" stop-color="{BG_GRAD_B}"/>
    </linearGradient>
  </defs>
  <rect x="41" y="41" width="174" height="174" rx="51" fill="url(#bg)"/>
  <!-- cahaya -->
  <ellipse cx="128" cy="84" rx="15" ry="15" fill="{CAHAYA}" opacity="0.35"/>
  <path d="M128 51 L133 75 L156 84 L133 93 L128 117 L123 93 L100 84 L123 75 Z" fill="{CAHAYA}"/>
  <!-- buku -->
  <path d="M128 150 L128 224 L67 201 L67 137 Z" fill="{BUKU_TEAL}"/>
  <path d="M128 150 L128 224 L189 201 L189 137 Z" fill="{BUKU_TEAL_TERANG}"/>
  <path d="M118 150 L138 150 L138 224 L118 224 Z" fill="{BUKU_TEAL}"/>
</svg>
'''
    with open(svg, "w", encoding="utf-8") as f:
        f.write(s)
    print("  SVG  %s" % svg)


if __name__ == "__main__":
    utama()
