#!/usr/bin/env python3
"""Pengesahan VISUAL SEBENAR — output _label_kiraan: banner kitab + kad koleksi.

Lancarkan `PustakaApp` pada skrin Windows TANPA offscreen, kemudian
sahkan pada WIDGET SEBENAR (bukan hanya unit semak.py 8w/8x) bahawa
fungsi kongsi `_label_kiraan(total, kata, fallback)` benar-benar
memformat paparan:

  (1) kad koleksi halaman utama — `_cnt` setiap `KitabCard` memapar
      "{total:,} Hadis" (koma ribuan, huruf besar) selepas muat data
      async, dan fallback "— Hadis" bila `set_total(None)`;
  (2) banner halaman kitab — subtitle `Hero` memapar "{total:,} hadis"
      (huruf kecil) untuk koleksi yang dimuat; kotak lompat kekal
      julat "0–N" (bukan koma ribuan);
  (3) skrin fizikal — tangkapan ImageGrab untuk kedua-dua tema
      disimpan dalam `bukti_visual/kiraan_*.png`.

Lapisan sumber + kelakuan app + skrin fizikal (corak sama
`uji_visual_sebenar.py`) mengesan regresi: kalau literal format
dipulangkan ke dalam render, atau kata/koma ribuan bertukar, salah
satu lapisan GAGAL.

    python uji_visual_kiraan.py

Tangkapan skrin: `bukti_visual/kiraan_*.png`
"""

import os
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer, QEventLoop
from PIL import ImageGrab
import win32gui

app = QApplication(sys.argv)

BUKTI = os.path.join(BASE, "bukti_visual")
os.makedirs(BUKTI, exist_ok=True)

PASS = 0
FAIL = 0


def semak(nama: str, ok: bool, butir: str = ""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  OK    {nama}")
    else:
        FAIL += 1
        print(f"  GAGAL {nama}  {butir}")


def tunggu(ms: int):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


def skrin_fizikal(tag: str):
    """Tangkap tetingkap pada skrin fizikal; pulang laluan + saiz + warna."""
    app.processEvents()
    time.sleep(0.3)
    hwnd = int(w.winId())
    try:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        time.sleep(0.3)
    except Exception:
        pass
    kiri, atas, kanan, bawah = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
    nama = f"kiraan_{tag}.png"
    laluan = os.path.join(BUKTI, nama)
    img.save(laluan)
    saiz = os.path.getsize(laluan)
    kecil = img.resize((320, 200))
    # getdata() deprecated sejak Pillow 12 (dibuang Pillow 14) -- guna
    # get_flattened_data() dengan fallback untuk Pillow lama.
    pix = getattr(kecil, "get_flattened_data", kecil.getdata)()
    unik = len({(px[0] >> 4, px[1] >> 4, px[2] >> 4) for px in pix})
    print(f"  [skrin] {laluan} ({saiz} B, warna unik {unik})")
    return laluan, saiz, unik


print("=" * 62)
print("  UJIAN VISUAL — _label_kiraan: BANNER KITAB + KAD KOLEKSI")
print("=" * 62)

from ui.app_qt import PustakaApp
from ui.pages import _label_kiraan
from ui.pages_kitab import _julat_lompat

# ── 1. Sumber — pengawal regresi bebas daripada state app ───────────
src_pages = open(os.path.join(BASE, "ui", "pages.py"), encoding="utf-8").read()
src_kitab = open(os.path.join(BASE, "ui", "pages_kitab.py"),
                 encoding="utf-8").read()
semak("sumber pages.py: _label_kiraan wujud (koma ribuan + kata)",
      "def _label_kiraan" in src_pages and 'f"{total:,} {kata}"' in src_pages)
semak("sumber pages.py: _label_kad_hadis dibuang",
      "def _label_kad_hadis" not in src_pages
      and "_label_kad_hadis(" not in src_pages)
semak("sumber pages_kitab.py: banner + lompat guna fungsi kongsi",
      '_label_kiraan(total, "hadis", "")' in src_kitab
      and "_julat_lompat(total)" in src_kitab)
semak("sumber pages_kitab.py: _subtitle_hadis dibuang",
      "def _subtitle_hadis" not in src_kitab
      and "_subtitle_hadis(" not in src_kitab)

# ── 2. Lancar aplikasi SEBENAR ──────────────────────────────────────
print("\n  Lancarkan PustakaApp pada skrin sebenar...")
w = PustakaApp()
w.resize(1100, 760)
w.show()
tunggu(2500)

t0 = time.time()
while time.time() - t0 < 10 and not w.collections:
    tunggu(100)
semak("koleksi dimuat async", len(w.collections) >= 1,
      f"jumpa {len(w.collections)}")

# ── 3. Kad koleksi halaman utama ────────────────────────────────────
print("\n  ── KAD KOLEKSI (halaman utama) ──")
cards = getattr(w, "_kitab_cards", {}) or {}
semak("kad koleksi dipapar (_kitab_cards)", len(cards) >= 1,
      f"kad={len(cards)}")

padan = 0
diuji = 0
for slug, card in cards.items():
    total = w._total_of(slug)
    if not isinstance(total, int):
        continue
    diuji += 1
    jangka = _label_kiraan(total, "Hadis", "— Hadis")
    if card._cnt.text() == jangka:
        padan += 1
    else:
        semak(f"kad {slug}: teks = {jangka}", False,
              f"dapat {card._cnt.text()!r}")
semak(f"{diuji} kad padan _label_kiraan (koma ribuan + 'Hadis')",
      diuji >= 1 and padan == diuji, f"padan {padan}/{diuji}")

# Bukhari: nilai diketahui 7,008 dikunci terus (bebas daripada fungsi)
bukhari = cards.get("bukhari")
total_b = w._total_of("bukhari")
if bukhari is not None and isinstance(total_b, int):
    semak("kad Bukhari '7,008 Hadis' pada skrin (koma ribuan)",
          bukhari._cnt.text() == "7,008 Hadis",
          f"dapat {bukhari._cnt.text()!r}")

# Fallback async: set_total(None) -> '— Hadis' (koleksi belum dimuat)
if bukhari is not None and isinstance(total_b, int):
    bukhari.set_total(None)
    semak("fallback set_total(None) -> '— Hadis'",
          bukhari._cnt.text() == "— Hadis",
          f"dapat {bukhari._cnt.text()!r}")
    bukhari.set_total(total_b)
    semak("kad dipulihkan selepas fallback",
          bukhari._cnt.text() == "7,008 Hadis",
          f"dapat {bukhari._cnt.text()!r}")

# Tapak inline app_qt.py (audit Sesi 54: kekal, bukan fungsi kongsi)
jum = getattr(w, "_home_count", None)
jumlah = sum(v for v in (w._total_of(s) for s in cards)
             if isinstance(v, int))
jangka_rumah = f"{jumlah:,} hadis daripada {len(w.collections)} kitab"
if jum is not None:
    semak("rumah: jumlah gabungan guna koma ribuan",
          jum.text() == jangka_rumah, f"dapat {jum.text()!r}")

try:
    laluan, saiz, unik = skrin_fizikal("kad_gelap")
    semak("skrin kad (gelap) disimpan", saiz > 30000, f"saiz {saiz}")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")

# ── 4. Banner halaman kitab ─────────────────────────────────────────
print("\n  ── BANNER KITAB (halaman kitab) ──")
w.open_kitab("bukhari", 1)
t0 = time.time()
while time.time() - t0 < 10 and (
        not getattr(w, "_kitab_list", None)
        or w._kitab_list.count() <= 3):
    tunggu(100)
semak("senarai Bukhari dimuat (halaman kitab)", w._kitab_list.count() > 3,
      f"kad={w._kitab_list.count()}")

total = w._total_of("bukhari")
jangka_sub = _label_kiraan(total, "hadis", "")
hero = w._kitab_root.itemAt(0).widget() if w._kitab_root.count() else None
sub = None
if hero is not None:
    for lbl in hero.findChildren(QLabel):
        if lbl.objectName() == "faint" and lbl.text() == jangka_sub:
            sub = lbl
            break
semak("banner: subtitle Hero '7,008 hadis' (koma ribuan, huruf kecil)",
      sub is not None, f"jangka {jangka_sub!r}")

# Kotak lompat kekal julat, bukan koma ribuan (sempadan Sesi 54)
gb = getattr(w, "_kitab_go_box", None)
jangka_lompat = _julat_lompat(total)
semak("kotak lompat: placeholder julat '0–7008' (bukan koma)",
      gb is not None and gb.placeholderText() == jangka_lompat,
      f"dapat {gb.placeholderText()!r}")

try:
    laluan, saiz, unik = skrin_fizikal("banner_gelap")
    semak("skrin banner (gelap) disimpan", saiz > 30000, f"saiz {saiz}")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")

# ── 5. Tema terang ──────────────────────────────────────────────────
w.set_theme("light")
tunggu(800)
try:
    laluan, saiz, unik = skrin_fizikal("banner_terang")
    semak("skrin banner (terang) disimpan", saiz > 30000, f"saiz {saiz}")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")
w.go("home")
tunggu(800)
try:
    laluan, saiz, unik = skrin_fizikal("kad_terang")
    semak("skrin kad (terang) disimpan", saiz > 30000, f"saiz {saiz}")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")

w.close()
print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print(f"  Tangkapan skrin: {BUKTI}")
print("=" * 62)
sys.exit(1 if FAIL else 0)
