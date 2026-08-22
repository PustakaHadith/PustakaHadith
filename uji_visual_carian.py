#!/usr/bin/env python3
"""Pengesahan VISUAL — indikator jam berputar semasa carian.

Lancarkan `PustakaApp`, buka halaman Carian, dan sahkan:

  (1) struktur — label jam + QTimer (120ms) + 12 muka jam wujud;
  (2) BUKTI RENDER — pin dua muka jam 🕐 vs 🕛 dan bandingkan piksel
      pada RENDER TETINGKAP sebenar (`w.grab()`): muka jam mesti
      dilukis BERBEZA. Ini bebas timing carian dan bebas masalah
      tangkapan skrin fizikal (tetingkap hadapan/DPI/occlusion).
      Tangkapan skrin fizikal (`ImageGrab`) disimpan sebagai ARTIFAK
      sahaja — di sesetengah persekitaran tetingkap tidak dapat
      diambil secara fizikal walau SetForegroundWindow;
  (3) KITARAN HIDUP carian sebenar ("hukum riba") — jam kelihatan
      semasa carian berjalan, disembunyikan selepas selesai, hasil
      dipapar, teks status bertukar ke keputusan.

Nota mesin tanpa indeks carian makna: carian mungkin selesai
serta-merta — semakan "jam kelihatan" mungkin terlepas (nota, bukan
gagal); semakan struktur + render tetap berjalan.

    python uji_visual_carian.py

Tangkapan skrin: `bukti_visual/carian_jam_*.png`
"""
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QBuffer, QIODevice, QPoint, QRect, QTimer, QEventLoop
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


def qimg_png(qimg) -> bytes:
    """QImage -> bait PNG (untuk perbandingan piksel)."""
    buf = QBuffer()
    buf.open(QIODevice.WriteOnly)
    qimg.save(buf, "PNG")
    return bytes(buf.data())


def tangkap_skrin_fizikal(tag: str):
    """Tangkap tetingkap pada skrin fizikal (artifak sahaja, tidak diuji)."""
    app.processEvents()
    time.sleep(0.25)
    hwnd = int(w.winId())
    try:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        time.sleep(0.2)
    except Exception:
        pass
    kiri, atas, kanan, bawah = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
    nama = f"carian_jam_{tag}.png"
    laluan = os.path.join(BUKTI, nama)
    img.save(laluan)
    print(f"  [artifak skrin] {laluan} ({os.path.getsize(laluan)} B)")


print("=" * 62)
print("  UJIAN VISUAL — JAM BERPUTAR SEMASA CARIAN")
print("=" * 62)

from ui.app_qt import PustakaApp
from ui.helpers import PAGES

w = PustakaApp()
w.resize(1100, 760)
w.show()
tunggu(2500)

# ── 1. Struktur (sentiasa dijalankan) ────────────────────────────
w.go("search")
tunggu(600)
semak("halaman Carian dibuka", w.stack.currentIndex() == PAGES["search"],
      f"idx={w.stack.currentIndex()}")

ada_label = isinstance(getattr(w, "_carian_sibuk", None), QLabel)
semak("label jam wujud (_carian_sibuk)", ada_label)
ada_timer = isinstance(getattr(w, "_carian_timer", None), QTimer)
semak("QTimer wujud (_carian_timer)", ada_timer)
if ada_timer:
    semak("selang QTimer = 120ms", w._carian_timer.interval() == 120,
          f"interval={w._carian_timer.interval()}")
semak("12 muka jam (🕐..🕛)", len(getattr(w, "_jam", [])) == 12,
      f"len={len(getattr(w, '_jam', []))}")

if not ada_label or not ada_timer:
    print("\n  Label/timer TIADA — henti")
    print(f"\n  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
    print("=" * 62)
    sys.exit(1)

# ── 2. Bukti render tetingkap: pin 🕐 vs 🕛 ───────────────────────
print("\n  Pin muka jam 🕐 vs 🕛 dan bandingkan render tetingkap...")
w._carian_timer.stop()
w._carian_sibuk.show()

pos = w._carian_sibuk.mapTo(w, QPoint(0, 0))
pad = 8
reg = QRect(pos.x() - pad, pos.y() - pad,
            w._carian_sibuk.width() + 2 * pad,
            w._carian_sibuk.height() + 2 * pad)

w._carian_sibuk.setText("🕐")
app.processEvents()
tunggu(150)
r1 = w.grab().toImage().copy(reg)
try:
    tangkap_skrin_fizikal("pin1")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")

w._carian_sibuk.setText("🕛")
app.processEvents()
tunggu(150)
r2 = w.grab().toImage().copy(reg)
try:
    tangkap_skrin_fizikal("pin2")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")

semak("muka jam 🕐 vs 🕛 berbeza pada render tetingkap",
      qimg_png(r1) != qimg_png(r2))

# Pulihkan: sembunyikan jam manual sebelum carian sebenar
w._carian_sibuk.hide()

# ── 3. Kitaran hidup carian sebenar ───────────────────────────────
print("\n  Hantar carian 'hukum riba' (kata kunci + makna AI)...")
w.search_bar.input.setText("hukum riba")
w._do_search(1)
app.processEvents()

# Poll sehingga 2s: adakah jam kelihatan dalam tingkap sibuk?
nampak = False
t_mula = time.time()
while time.time() - t_mula < 2.0:
    if w._carian_sibuk.isVisible():
        nampak = True
        break
    app.processEvents()
    time.sleep(0.03)
semak("jam kelihatan semasa carian berjalan", nampak)

if nampak:
    t1 = w._carian_sibuk.text()
    tunggu(250)
    t2 = w._carian_sibuk.text()
    semak("jam berputar (teks label berubah)", t1 != t2, f"{t1} -> {t2}")
else:
    print("  [nota] carian selesai terlalu pantas — putaran tidak dapat "
          "disampel (struktur/render sudah disahkan)")

# Tunggu carian selesai (semantik 1-30s)
deadline = time.time() + 90
while time.time() < deadline and w._carian_sibuk.isVisible():
    app.processEvents()
    time.sleep(0.2)
tunggu(400)
semak("jam disembunyikan selepas carian selesai",
      not w._carian_sibuk.isVisible())
semak("hasil carian dipapar", w._search_list.count() > 0,
      f"count={w._search_list.count()}")
info = w.search_info.text()
semak("teks status = keputusan (bukan 'Mencari')", "Mencari" not in info,
      info[:60])
try:
    tangkap_skrin_fizikal("selesai")
except Exception as e:
    print(f"  [nota] tangkapan fizikal gagal: {e}")

w.close()
print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print(f"  Tangkapan skrin: {BUKTI}")
print("=" * 62)
sys.exit(1 if FAIL else 0)
