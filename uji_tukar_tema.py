#!/usr/bin/env python3
"""Ujian tukar tema berulang (gelap→terang→gelap) + carian setiap kali.

Tujuan: `set_theme` membina SEMULA seluruh UI (53 panggilan setStyleSheet
inline). Ujian ini menukar tema 4 kali dan membuat carian gabungan selepas
setiap pertukaran, memantau:
  - tiada pengecualian semasa set_theme
  - carian masih berfungsi selepas pembinaan semula
  - kedudukan pengguna (halaman butiran) dipulihkan
  - bilangan widget tidak membengkak (kebocoran = widget lama tidak dibuang)
"""

import os
import sqlite3
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer, QEventLoop

app = QApplication(sys.argv)

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


def kira_label(w) -> int:
    """Bilangan QLabel dalam pokok — penunjuk kebocoran widget."""
    return len(w.findChildren(QLabel))


# ── 1. Sediakan data + lancar aplikasi ──────────────────────────────
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
calon = conn.execute(
    "SELECT h.collection, h.hadis_id FROM hadis h "
    "JOIN hadethenc he ON he.collection=h.collection AND he.hadis_id=h.hadis_id "
    "LEFT JOIN semakhadis s ON s.collection=h.collection AND s.hadis_id=h.hadis_id "
    "WHERE s.hadis_id IS NULL LIMIT 1"
).fetchone()
conn.close()

print("=" * 62)
print("  UJIAN TUKAR TEMA BERULANG + CARIAN")
print("=" * 62)

from ui.app_qt import PustakaApp
w = PustakaApp()
w.show()
tunggu(3000)
semak("Koleksi dimuat (9 kitab)", len(w.collections) == 9,
      f"jumpa {len(w.collections)}")

from ui.widgets import Collapsible

# Buka butiran dahulu supaya "kedudukan pengguna" = halaman butiran
h = w.api.get_hadis_by_id(calon["collection"], calon["hadis_id"])
h["collection"] = calon["collection"]
w.open_detail(h, "home")
tunggu(1500)
bil_label_asal = kira_label(w)
print(f"  Label sebelum kitaran tema: {bil_label_asal}")

# ── 2. Kitaran tema: 5 tema (neutral lalai + kertas + 2 terang +
#    'sistem' ikut Windows) + carian setiap kali ─────────────────────
tema = ["neutral", "lightneutral", "light", "dark", "sistem",
        "neutral", "lightneutral", "light", "dark", "sistem"]
for i, t in enumerate(tema, 1):
    print(f"\n  Kitaran {i}: tukar ke '{t}'...")
    try:
        w.set_theme(t)
    except Exception as e:
        semak(f"kitaran {i}: set_theme('{t}') tanpa ralat", False, str(e))
        continue
    tunggu(1200)
    semak(f"kitaran {i}: tema = '{t}'",
          w.settings.get("theme") == t,
          f"sebenarnya {w.settings.get('theme')}")

    # Halaman butiran dipulihkan selepas pembinaan semula?
    idx = w.stack.currentIndex()
    from ui.app_qt import PAGES
    semak(f"kitaran {i}: berada di halaman butiran (2)",
          idx == PAGES["detail"], f"index={idx}")
    if idx == PAGES["detail"] and w._detail_h:
        dh = w._detail_h
        semak(f"kitaran {i}: data butiran kekal ({dh.get('collection')} #{dh.get('id')})",
              dh.get("id") == h.get("id"))

    # Carian selepas pembinaan semula
    w.search_bar.input.setText("kelebihan bersedekah")
    w.go("search")
    w._do_search(1)
    tunggu(3000)
    semak(f"kitaran {i}: carian keyword ada hasil",
          w._kw_res is not None and len(w._kw_res) > 0,
          f"jumpa {len(w._kw_res or [])}")

    # Kembali ke butiran untuk kitaran seterusnya
    w.open_detail(w.api.get_hadis_by_id(calon["collection"], calon["hadis_id"]),
                  "home")
    tunggu(800)

# ── 3. Kebocoran widget ─────────────────────────────────────────────
bil_label_akhir = kira_label(w)
print(f"\n  Label selepas 4 kitaran: {bil_label_akhir} "
      f"(asal {bil_label_asal})")
semak("Tiada kebocoran widget (label tidak membengkak)",
      bil_label_akhir <= bil_label_asal * 3,
      f"{bil_label_asal} -> {bil_label_akhir}")

# ── 4. Tutup bersih ─────────────────────────────────────────────────
tunggu(300)
w.close()
tunggu(2000)
semak("Aplikasi ditutup tanpa crash", True)

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
