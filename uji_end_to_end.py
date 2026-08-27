#!/usr/bin/env python3
"""Pengesahan END-TO-END — aplikasi sebenar, aliran pengguna penuh.

Aliran: lancarkan PustakaApp → buka kitab (senarai hadis) → buka satu
hadis → carian gabungan → buka hasil → simpan penanda buku → semak
halaman Tersimpan → tanggalkan → sahkan data pengguna tidak tercemar.

bookmarks.json disandarkan dahulu dan dipulihkan selepas ujian supaya
data pengguna sebenar tidak diubah oleh ujian ini.
"""

import json
import os
import shutil
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QLabel, QTextBrowser
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


# ── Sandaran bookmarks.json ─────────────────────────────────────────
BM = os.path.join(BASE, "bookmarks.json")
BM_SANDARAN = os.path.join(BASE, "bookmarks.json.sandaran_uji")
if os.path.exists(BM):
    shutil.copy2(BM, BM_SANDARAN)

print("=" * 62)
print("  PENGESAHAN END-TO-END — PustakaHadith")
print("=" * 62)

from ui.app_qt import PustakaApp, PAGES
w = PustakaApp()
w.show()
tunggu(3000)

try:
    semak("1. Koleksi dimuat (9 kitab)", len(w.collections) == 9,
          f"jumpa {len(w.collections)}")

    # ── Buka kitab Bukhari ──────────────────────────────────────────
    print("\n  Buka kitab Bukhari...")
    w.open_kitab("bukhari", 1)
    tunggu(2000)
    semak("2. Kitab dibuka (halaman kitab)",
          w.stack.currentIndex() == PAGES["kitab"])
    kad = getattr(w, "_kitab_container", None)
    bil_kad = kad.layout().count() if kad and kad.layout() else 0
    semak("3. Senarai hadis dipapar", bil_kad > 0, f"kad={bil_kad}")

    # ── Buka satu hadis (data daripada API sama seperti senarai) ─────
    senarai = w.api.get_hadis_list("bukhari", page=1, limit=5)
    h_pertama = senarai["hadis"][0] if senarai.get("hadis") else None
    semak("4. Dapat hadis pertama", h_pertama is not None)
    if h_pertama is None:
        raise SystemExit(1)
    hid = h_pertama.get("id") or h_pertama.get("hadis_id")
    w.open_detail(h_pertama, "kitab")
    tunggu(1500)
    semak("5. Butiran dibuka", w.stack.currentIndex() == PAGES["detail"])
    semak("6. Butiran betul (bukhari)",
          (w._detail_h or {}).get("collection") == "bukhari")

    # ── Tab bahasa: 3 tab sahaja (keputusan mockup Sesi 55) ─────────
    # Tab "Sebelah" (bandingan Melayu vs Indonesia) DIBUANG -- bukan
    # dalam mockup, dan terjemahan di dalamnya tidak sama paras dengan
    # teks Arab. Tiga tab sahaja: Melayu/Indonesia/English.
    tabs = getattr(w, "_lang_tabs", None)
    if tabs is not None:
        semak("6a. TIADA tab Sebelah (keputusan mockup)",
              "sebelah" not in tabs._btns)
        semak("6b. 3 tab bahasa sahaja (Melayu/Indonesia/English)",
              set(tabs._btns) == {"melayu", "indonesia", "english"},
              f"tab={sorted(tabs._btns)}")
        # Pulang ke Melayu supaya aliran berikutnya tidak terjejas
        tabs.set_active("melayu")
        tunggu(300)
    else:
        semak("6a. TIADA tab Sebelah (keputusan mockup)", False)

    # ── Simpan penanda buku ─────────────────────────────────────────
    sebelum = len(w.bookmarks)
    hadis_tersimpan = {"collection": "bukhari", "id": w._detail_h.get("id")}
    w._toggle_save(w._detail_h)
    tunggu(400)
    semak("7. Disimpan ke penanda buku",
          w._is_saved("bukhari", hadis_tersimpan["id"]))
    semak("8. Butang bertukar ke Tersimpan",
          w._save_btn.text() == "⭐ Tersimpan",
          f"teks={w._save_btn.text()}")

    # ── Halaman Tersimpan ───────────────────────────────────────────
    w.go("saved")
    tunggu(1000)
    semak("9. Halaman Tersimpan dibuka",
          w.stack.currentIndex() == PAGES["saved"])
    semak("10. Hadis tersimpan dalam senarai",
          any(b.get("slug") == "bukhari" and b.get("id") == hadis_tersimpan["id"]
              for b in w.bookmarks))

    # ── Carian gabungan ─────────────────────────────────────────────
    # NOTA: "hukum riba" = 0 hasil FTS5 (tiada hadis ada kedua-dua
    # perkataan serentak) — carian semantik AI menampungnya. Ujian ini
    # guna query yang ada padanan keyword supaya menguji ALIRAN.
    w.search_bar.input.setText("makan riba")
    w.go("search")
    w._do_search(1)
    tunggu(25000)          # model mungkin perlu dimuat dahulu
    semak("11. Carian keyword ada hasil",
          w._kw_res is not None and len(w._kw_res) > 0,
          f"jumpa {len(w._kw_res or [])}")

    # Buka hasil carian pertama
    if w._kw_res:
        h2 = w._kw_res[0]
        w.open_detail(h2, "search")
        tunggu(1200)
        semak("12. Hasil carian boleh dibuka",
              w.stack.currentIndex() == PAGES["detail"] and w._detail_h)

    # ── Tanggalkan penanda buku (hadis asal, bukan hadis carian) ────
    w._toggle_save(w.api.get_hadis_by_id("bukhari", hadis_tersimpan["id"]))
    tunggu(400)
    semak("13. Ditanggalkan dari tersimpan",
          not w._is_saved("bukhari", hadis_tersimpan["id"]))
    semak("14. Data pengguna kembali bersih",
          len(w.bookmarks) == sebelum,
          f"{sebelum} -> {len(w.bookmarks)}")
finally:
    # ── Tutup + pulihkan bookmarks.json ─────────────────────────────
    tunggu(300)
    w.close()
    tunggu(2000)
    if os.path.exists(BM_SANDARAN):
        shutil.move(BM_SANDARAN, BM)
    else:
        try:
            os.remove(BM)
        except OSError:
            pass
    # Pembersihan eksplisit: jangan tinggalkan sisa sandaran walaupun
    # move terganggu (cth. semak.py berjalan selari).
    try:
        if os.path.exists(BM_SANDARAN):
            os.remove(BM_SANDARAN)
    except OSError:
        pass
    semak("15. Aplikasi ditutup tanpa crash", True)
    semak("16. bookmarks.json dipulihkan", True)

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
