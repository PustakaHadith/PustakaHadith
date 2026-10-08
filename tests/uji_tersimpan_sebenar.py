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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
# NOTA: nama sandaran mesti UNIK antara ujian — uji_end_to_end pernah
# kongsi nama `sandaran_uji` dan bila dua ujian berjalan serentak,
# sandaran berebut -> fail pengguna terakhir dipadam (kehilangan data
# 7 Okt 2026). JANGAN tukar balik ke nama sama.
BM_SANDARAN = os.path.join(BASE, "bookmarks.json.sandaran_tsk")


def baca_fail() -> list:
    try:
        with open(BM, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def tulis_fail(data: list):
    with open(BM, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if os.path.exists(BM_SANDARAN):
    # Sisa larian terdahulu yang gagal pulih — sandaran = salinan
    # terakhir diketahui baik; pulihkan SEBELUM menulis apa-apa
    # (jangan ditimbus dgn salinan baru).
    try:
        if os.path.exists(BM):
            os.remove(BM)
        shutil.move(BM_SANDARAN, BM)
    except OSError:
        pass
if os.path.exists(BM):
    shutil.copy2(BM, BM_SANDARAN)

# Asingkan: mula dgn bookmarks KOSONG. Ujian ini membina 3 entri sendiri
# dan menyemak KIRAAN tepat ("3 kad", meta "3 tersimpan") — keadaan awal
# bergantung data pengguna (bookmark sedia ada) membuatkanya gagal.
# Sandaran asal dipulihkan dalam finally (laluan pulih sama).
tulis_fail([])

print("=" * 62)
print("  PENGESAHAN HALAMAN TERSIMPAN — tanda buku SEBENAR")
print("=" * 62)

from ui.app_qt import PustakaApp, PAGES          # noqa: E402
from ui.widgets import ClickCard                  # noqa: E402

# Tutup tetingkap JANGAN panggil QApplication.quit() (lihat closeEvent):
# quit() luar exec_ meracuni QEventLoop seterusnya → fasa restart (w2)
# kehilangan timer + isyarat worker (kad tak terpapar, klik tak buka
# butiran). Apl sebenar tak terjejas — flag ni hanya ujian.
PustakaApp.ujian_mode = True

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
              w._is_saved(slug, hid)
              and "Tersimpan" in w._save_btn_icon.toolTip(),
              w._save_btn_icon.toolTip())

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
        """Kad dalam _saved_list SAHAJA — bukan semua ClickCard app.

        findChildren(ClickCard) mengira kad dari halaman lain yang masih
        wujud dalam pokok widget (termasuk widget tak terus papar) →
        kiraan membengkak (7 unjuran utk 3 bookmark) dan kad[0] boleh
        jadi kad asing yang tidak membuka butiran.
        """
        lst = getattr(w, "_saved_list", None)
        if lst is None:
            return []
        out = []
        for i in range(lst.count()):
            wd = lst.itemAt(i).widget()
            if isinstance(wd, ClickCard) and wd.isVisible():
                out.append(wd)
        return out

    kad = _kad_simpan()
    semak("4. Halaman Tersimpan dipapar (PAGES['saved'])",
          w.stack.currentIndex() == PAGES["saved"])
    semak("5. Meta banner '3 tersimpan'",
          # Banner kini "Simpan & Sejarah" + meta "{n} tersimpan ·
          # {n} dibaca" (teks lama "3 hadis disimpan" basi selepas
          # redesign halaman). Kiraan dibaca TIDAK disemak kerana
          # bergantung sejarah bacaan pengguna.
          "3 tersimpan" in _teks_halaman(w))
    semak("6. 3 kad hadis dipapar", len(kad) == 3, f"kad={len(kad)}")

    # Klik kad pertama -> hadis terbuka (aliran sebenar)
    if kad:
        kad[0].clicked.emit()
        t0 = time.time()
        while time.time() - t0 < 8 and \
                w.stack.currentIndex() != PAGES["detail"]:
            tunggu(100)
        semak("7. Klik kad membuka halaman detail",
              w.stack.currentIndex() == PAGES["detail"])
        # Kad dipapar TERBALIK (terbaru dahulu) -- kad[0] = abu-daud #1
        semak("7a. Hadis dibuka betul (abu-daud #1 — terbaru dahulu)",
              (w._detail_h or {}).get("collection") == "abu-daud"
              and (w._detail_h or {}).get("id") == 1,
              str({k: (w._detail_h or {}).get(k)
                   for k in ("collection", "id")}))
    else:
        semak("7. Klik kad membuka halaman detail", False,
              "tiada kad untuk klik")
        semak("7a. Hadis dibuka betul (abu-daud #1 — terbaru dahulu)",
              False, "tiada kad")

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
    # Scoped ikut _saved_list (lihat nota _kad_simpan) — findChildren
    # merentas seluruh pokok widget dan pernah gagal utk instance w2.
    lst2 = getattr(w2, "_saved_list", None)
    kad2 = []
    if lst2 is not None:
        for i in range(lst2.count()):
            wd = lst2.itemAt(i).widget()
            if isinstance(wd, ClickCard) and wd.isVisible():
                kad2.append(wd)
    semak("9. Selepas restart: 3 kad Tersimpan dipapar", len(kad2) == 3,
          f"kad={len(kad2)}")
    if len(kad2) >= 2:
        kad2[1].clicked.emit()      # muslim #1
        t0 = time.time()
        while time.time() - t0 < 8 and \
                w2.stack.currentIndex() != PAGES["detail"]:
            tunggu(100)
        semak("10. Buka dari Tersimpan selepas restart (muslim #1)",
              (w2._detail_h or {}).get("collection") == "muslim"
              and (w2._detail_h or {}).get("id") == 1,
              str({k: (w2._detail_h or {}).get(k)
                   for k in ("collection", "id")}))
    else:
        # Jangan IndexError — 9 sudah GAGAL; kaskad menutup ujian awal
        # dan menghalang seksyen akhir (pulih/cleanup) daripada berjalan.
        semak("10. Buka dari Tersimpan selepas restart (muslim #1)", False,
              f"kad={len(kad2)} — tak cukup kad untuk klik")

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

    # Tangkapan skrin bukti (halaman kosong). Utama: tangkap fizikal
    # tetingkap (win32gui + PIL). Fallback: render Qt `grab()` bila modul
    # tiada — requirements.txt TIDAK senaraikan PIL/pywin32, jadi venv
    # bersih takkan boleh import; PNG bukti tetap dijana.
    laluan_bukti = os.path.join(BUKTI, "tersimpan_sebenar.png")
    try:
        try:
            import win32gui
            from PIL import ImageGrab
            w2.raise_()
            w2.activateWindow()
            tunggu(600)
            kiri, atas, kanan, bawah = win32gui.GetWindowRect(
                int(w2.winId()))
            ImageGrab.grab(bbox=(kiri, atas, kanan, bawah)).save(
                laluan_bukti)
            kaedah = "fizikal"
        except ImportError:
            w2.grab().save(laluan_bukti)
            kaedah = "qt-grab (PIL/pywin32 tiada)"
        ok = (os.path.exists(laluan_bukti)
              and os.path.getsize(laluan_bukti) > 0)
        semak("13. Tangkapan skrin bukti disimpan", ok, kaedah)
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
    # Pulih dgn cubaan berulang: fail yang baru ditulis selalu dipegang
    # sebentar oleh imbasan AV/index Windows (WinError 32). JANGAN buang
    # sandaran bila pemulihan gagal — sandaran = satu-satunya salinan
    # (pembersihan buta pernah memadam data pengguna, 7 Okt 2026).
    pulih = False
    for _cuba in range(40):
        try:
            if os.path.exists(BM_SANDARAN):
                if os.path.exists(BM):
                    os.remove(BM)
                shutil.move(BM_SANDARAN, BM)
            else:
                try:
                    os.remove(BM)
                except OSError:
                    pass
            pulih = True
            break
        except OSError:
            tunggu(500)
    if pulih:
        try:
            if os.path.exists(BM_SANDARAN):
                os.remove(BM_SANDARAN)
        except OSError:
            pass
    semak("14. bookmarks.json dipulihkan (data pengguna selamat)",
          pulih)

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
