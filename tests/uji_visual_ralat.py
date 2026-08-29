#!/usr/bin/env python3
"""Pengesahan VISUAL SEBENAR — toast ralat diterjemah ke Bahasa Melayu.

Lancarkan `PustakaApp` pada skrin Windows TANPA offscreen, picu ralat
runtime melalui worker sebenar (CollectionsWorker dengan API tiruan yang
membangkitkan ralat), dan sahkan toast memaparkan mesej MELAYU (bukan
Inggeris mentah) + tangkapan skrin fizikal.

Rantaian yang diuji: worker.exception -> workers.terjemah_ralat(e) ->
failed.emit -> app_qt._on_error -> toast.show_msg.

    python uji_visual_ralat.py

Tangkapan skrin: `bukti_visual/ralat_*.png`
"""

import os
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication
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
    """Tangkap HANYA tetingkap aplikasi (bukan seluruh skrin)."""
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
    nama = f"ralat_{tag}.png"
    laluan = os.path.join(BUKTI, nama)
    img.save(laluan)
    print(f"  [skrin] {laluan} ({os.path.getsize(laluan)} B)")
    return laluan


class ApiRalat:
    """API tiruan yang membangkitkan ralat pada setiap panggilan."""

    def __init__(self, e):
        self._e = e

    def get_collections(self):
        raise self._e


# ── Lancar aplikasi ─────────────────────────────────────────────────
print("Lancarkan PustakaApp (tema gelap)...")
from ui.app_qt import PustakaApp
from ui.workers import CollectionsWorker
from utils.bahasa import terjemah_ralat

w = PustakaApp()
w.resize(1100, 760)
w.show()

# Tunggu koleksi dimuat dahulu (supaya tidak bersaing dengan toast ujian)
tunggu(2500)

# ── Kes ujian: (label, ralat, frasa Melayu jangkaan, frasa Inggeris asal) ──
KES = [
    ("connection_refused",
     ConnectionError("Connection refused"),
     "Sambungan ditolak oleh pelayan", "Connection refused"),
    ("no_such_table",
     __import__("sqlite3").OperationalError("no such table: hadis_fts"),
     "Jadual tidak wujud", "no such table"),
    ("http_500",
     Exception("500 Server Error: Internal Server Error"),
     "Ralat pelayan", "Server Error"),
    ("json_decode",
     Exception("Expecting value: line 1 column 1 (char 0)"),
     "Respons pelayan tidak sah", "Expecting value"),
]

for label, e, frasa_my, frasa_en in KES:
    # Terjemahan unit: ralat mentah -> mesej Melayu
    terjemah = terjemah_ralat(e)
    semak(f"{label}: terjemah_ralat -> Melayu",
          frasa_my.lower() in terjemah.lower() and
          frasa_en.lower() not in terjemah.lower(),
          f"-> {terjemah!r}")

    # Rantaian penuh: worker sebenar -> failed.emit -> _on_error -> toast
    wk = CollectionsWorker(ApiRalat(e))
    wk.failed.connect(w._on_error)
    wk.start()
    tunggu(1200)          # biar toast muncul
    teks_toast = w.toast.text()
    semak(f"{label}: toast memapar Melayu",
          frasa_my.lower() in teks_toast.lower() and
          frasa_en.lower() not in teks_toast.lower(),
          f"toast={teks_toast!r}")
    skrin_fizikal(label)
    tunggu(2500)          # biar toast lama hilang sebelum kes seterusnya
    wk.wait(5000)

# ── Ulang satu kes pada tema terang ─────────────────────────────────
w.set_theme("light")
tunggu(800)
wk = CollectionsWorker(ApiRalat(ConnectionError("Connection refused")))
wk.failed.connect(w._on_error)
wk.start()
tunggu(1200)
semak("tema terang: toast memapar Melayu",
      "Sambungan ditolak oleh pelayan" in w.toast.text(),
      f"toast={w.toast.text()!r}")
skrin_fizikal("connection_refused_light")
wk.wait(5000)

w.close()
print(f"\n  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 60)
sys.exit(0 if FAIL == 0 else 1)
