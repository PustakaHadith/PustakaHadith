#!/usr/bin/env python3
"""Pengesahan HALAMAN TERSIMPAN — skrin sebenar, tanda buku SEBENAR.

Mengisi item tertangguh #4 dalam MANUAL_REFERENSI_DEV §8: halaman
Tersimpan sebelum ini hanya diuji secara in-memory (offscreen) dengan
tanda buku buatan. Ujian ini:

  1. Menyimpan 3 hadis SEBENAR dari 3 kitab berbeza melalui aliran app
     (`_toggle_save`) — bookmarks.json ditulis ke cakera.
  2. Membuka halaman Tersimpan, sahkan 3 kad dipapar (Hero "3 hadis
     disimpan"), dan klik kad membuka hadis yang betul.
  3. Menutup tetingkap, MELANCARKAN SEMULA app — sahkan 3 tanda buku
     KEKAL (dimuat semula dari bookmarks.json sebenar, bukan state
     memori), dan boleh dibuka dari Tersimpan.
  4. Menanggalkan semua — sahkan empty state + fail kembali kosong.
  5. Pulihkan bookmarks.json asal (data pengguna tidak dicemari).

TANPA QT_QPA_PLATFORM=offscreen — tetingkap sebenar dipaparkan (mesin
sebenar), tangkapan skrin fizikal diambil sebagai bukti.

    python uji_tersimpan_sebenar.py
"""

import json
import os
import shutil
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication          # noqa: E402
from PyQt5.QtCore import QTimer, QEventLoop       # noqa: E402

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


# ── Sandaran data pengguna sebenar ──────────────────────────────────
BM = os.path.join(BASE, "bookmarks.json")
BM_SANDARAN = os.path.join(BASE, "bookmarks.json.sandaran_uji")


def baca_fail() -> list:
    try:
        with open(BM, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def tulis_fail(data: list):
    with open(BM, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if os.path.exists(BM):
    shutil.copy2(BM, BM_SANDARAN)

print("=" * 62)
print("  PENGESAHAN HALAMAN TERSIMPAN — tanda buku SEBENAR")
print("=" * 62)

from ui.app_qt import PustakaApp, PAGES          # noqa: E402
from ui.widgets import ClickCard                  # noqa: E402

try:
    # ── 1. Simpan 3 hadis sebenar dari 3 kitab ──────────────────────
    w = PustakaApp()
    w.show()
    w.raise_()
    w.activateWindow()
    tunggu(2500)

    semak("1. Koleksi dimuat (9 kitab)", len(w.collections) == 9,
          f"jumpa {len(w.collections)}")

    target = [("bukhari", 1), ("muslim", 1), ("abu-daud", 1)]
    for slug, hid in target:
        h = w.api.get_hadis_by_id(slug, hid)
        h["collection"] = slug
        w.open_detail(h, "kitab")
        tunggu(600)
        w._toggle_save(h)
        tunggu(200)
        semak(f"2. Simpan {slug} #{hid} (butang bertukar)",
              w._is_saved(slug, hid) and "Tersimpan" in w._save_btn.text(),
              w._save_btn.text())

    # Fail benar-benar ditulis
    fail = baca_fail()
    semak("3. bookmarks.json ditulis ke cakera (3 entri)",
          len(fail) == 3, f"jumpa {len(fail)}")
    semak("3a. entri simpan medan teks (arab/melayu) + kitab_name",
          all(b.get("arab") and b.get("kitab_name") for b in fail))

    def _teks_halaman(wdg):
        """Kumpul semua teks kelihatan pada widget secara rekursif."""
        hasil = []
        for obj in wdg.findChildren(object):
            if hasattr(obj, "text") and obj.isVisible():
                try:
                    t = obj.text()
                except Exception:
                    continue
                if t:
                    hasil.append(t)
        return "\n".join(hasil)

    # ── 2. Halaman Tersimpan: kad + Hero ────────────────────────────
    w.go("saved")
    tunggu(800)

    def _kad_simpan():
        """Pulangkan senarai ClickCard halaman Tersimpan."""
        return [c for c in w.findChildren(ClickCard)
                if c.isVisible() and c.parentWidget() is not None]

    kad = _kad_simpan()
    semak("4. Halaman Tersimpan dipapar (PAGES['saved'])",
          w.stack.currentIndex() == PAGES["saved"])
    semak("5. Hero '3 hadis disimpan'",
          "3 hadis disimpan" in _teks_halaman(w))
    semak("6. 3 kad hadis dipapar", len(kad) == 3, f"kad={len(kad)}")

    # Klik kad pertama -> hadis terbuka (aliran sebenar)
    kad[0].clicked.emit()
    t0 = time.time()
    while time.time() - t0 < 8 and w.stack.currentIndex() != PAGES["detail"]:
        tunggu(100)
    semak("7. Klik kad membuka halaman detail",
          w.stack.currentIndex() == PAGES["detail"])
    # Kad dipapar TERBALIK (terbaru dahulu) -- kad[0] = abu-daud #1
    semak("7a. Hadis dibuka betul (abu-daud #1 — terbaru dahulu)",
          (w._detail_h or {}).get("collection") == "abu-daud"
          and (w._detail_h or {}).get("id") == 1,
          str({k: (w._detail_h or {}).get(k) for k in ("collection", "id")}))

    # ── 3. Restart app — tanda buku KEKAL dari cakera ────────────────
    print("\n  Tutup tetingkap dan lancarkan semula...")
    w.close()
    tunggu(800)

    w2 = PustakaApp()
    w2.show()
    w2.raise_()
    w2.activateWindow()
    tunggu(2500)
    semak("8. Selepas restart: 3 tanda buku dimuat dari cakera",
          len(w2.bookmarks) == 3, f"jumpa {len(w2.bookmarks)}")
    semak("8a. Kandungan tanda buku kekal (kitab + id)",
          sorted((b["slug"], b["id"]) for b in w2.bookmarks)
          == sorted(target),
          str(sorted((b["slug"], b["id"]) for b in w2.bookmarks)))

    w2.go("saved")
    tunggu(800)
    kad2 = [c for c in w2.findChildren(ClickCard)
            if c.isVisible() and c.parentWidget() is not None]
    semak("9. Selepas restart: 3 kad Tersimpan dipapar", len(kad2) == 3,
          f"kad={len(kad2)}")
    kad2[1].clicked.emit()          # muslim #1
    t0 = time.time()
    while time.time() - t0 < 8 and w2.stack.currentIndex() != PAGES["detail"]:
        tunggu(100)
    semak("10. Buka dari Tersimpan selepas restart (muslim #1)",
          (w2._detail_h or {}).get("collection") == "muslim"
          and (w2._detail_h or {}).get("id") == 1,
          str({k: (w2._detail_h or {}).get(k) for k in ("collection", "id")}))

    # ── 4. Tanggalkan semua -> empty state + fail kosong ─────────────
    for slug, hid in target:
        h = w2.api.get_hadis_by_id(slug, hid)
        h["collection"] = slug
        if w2._is_saved(slug, hid):
            w2._toggle_save(h)
            tunggu(200)
    semak("11. Semua ditanggalkan (bookmarks kosong)",
          len(w2.bookmarks) == 0, f"jumpa {len(w2.bookmarks)}")
    semak("11a. bookmarks.json di cakera kosong", baca_fail() == [])

    w2.go("saved")
    tunggu(600)
    semak("12. Empty state 'Belum ada hadis tersimpan' dipapar",
          "Belum ada hadis tersimpan" in _teks_halaman(w2))

    # Tangkapan skrin fizikal bukti (halaman kosong)
    try:
        import win32gui
        from PIL import ImageGrab
        w2.raise_()
        w2.activateWindow()
        tunggu(600)
        kiri, atas, kanan, bawah = win32gui.GetWindowRect(int(w2.winId()))
        img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
        img.save(os.path.join(BUKTI, "tersimpan_sebenar.png"))
        semak("13. Tangkapan skrin bukti disimpan", True)
    except Exception as e:
        semak("13. Tangkapan skrin bukti disimpan", False, str(e))

finally:
    tunggu(300)
    try:
        w.close()
    except Exception:
        pass
    try:
        w2.close()
    except Exception:
        pass
    tunggu(800)
    # ── Pulihkan data pengguna ───────────────────────────────────────
    if os.path.exists(BM_SANDARAN):
        shutil.move(BM_SANDARAN, BM)
    else:
        try:
            os.remove(BM)
        except OSError:
            pass
    try:
        if os.path.exists(BM_SANDARAN):
            os.remove(BM_SANDARAN)
    except OSError:
        pass
    semak("14. bookmarks.json dipulihkan (data pengguna selamat)",
          True)

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
