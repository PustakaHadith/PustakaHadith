#!/usr/bin/env python3
"""Ujian responsif viewport — 6 halaman × 4 saiz tetingkap pada DPI 150%.

Mengesahkan pembetulan `_paksa_saiz_halaman` (17 Ogos) STABIL selepas
tutup hari: selepas navigasi ATAU resize tetingkap, halaman dan viewport
QScrollArea TIDAK tertinggal pada geometri 640×480 dalam stack (kandungan
terpotong kanan, hbar tersembunyi oleh ScrollBarAlwaysOff) — merentas
6 halaman (utama, kitab, detail, carian, tersimpan, tetapan) × 4 saiz
tetingkap pada DPI 150% (QT_SCALE_FACTOR=1.5).

Semakan setiap (halaman, saiz):
  1. Halaman semasa == saiz stack (toleransi ±2px).
  2. Setiap viewport QScrollArea >= 80% lebar stack (tidak basi 640×480).
  3. Tiada skrol mengufuk (hbar.maximum() == 0).
  4. DESC_KLIP: label deskripsi kad kitab (halaman utama) tidak
     terpotong (tinggi label >= tinggi yang diperlukan teks).
  5. Tiada ranap (ujian berterusan).

Juga semakan "resize SAHAJA" pada permulaan setiap saiz (halaman semasa
daripada saiz sebelumnya — punca asal pepijat: resize tanpa navigasi).

    python uji_responsif_viewport.py

Penskalaan boleh diubah: `QT_SCALE_FACTOR=1.25 python
uji_responsif_viewport.py` (lalai 1.5 = DPI 150%).

Saiz fon app boleh diubah tanpa menyentuh fail pengguna:
`UJI_FONT_SCALE_IDX=2 python uji_responsif_viewport.py` (indeks
FONT_SCALES [0.85, 1.0, 1.15, 1.3, 1.5] — 2 = 1.15x ~ "fon 115%",
3 = 1.3x "fon 130%"). QT_FONT_DPI TIDAK menjejaskan app ini (semua
saiz fon ditetapkan sendiri dalam px stylesheet, bukan fon sistem).

Offscreen (QT_QPA_PLATFORM=offscreen) — tiada skrin fizikal diperlukan.
"""

import os
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_SCALE_FACTOR", "1.5")

from PyQt5.QtWidgets import QApplication, QLabel, QScrollArea      # noqa: E402
from PyQt5.QtCore import QTimer, QEventLoop                        # noqa: E402

app = QApplication(sys.argv)

from ui.app_qt import PustakaApp  # noqa: E402

# Halang pra-muat model torch dalam QThread: lambat (~30s) dan tiada
# kaitan dengan geometri viewport (preload diuji khusus oleh ujian
# lain). Ditampal pada KELAS supaya sambungan isyarat dalam __init__
# (worker.finished -> self._mula_pramuat) mengambil versi ini.
PustakaApp._mula_pramuat = lambda self: None

_idx_env = os.environ.get("UJI_FONT_SCALE_IDX")
if _idx_env is not None:
    # Ganti tetapan pengguna DALAM INGATAN sahaja (fail tidak disentuh):
    # PustakaApp baca font_scale_idx daripada user_settings.json — tampal
    # _read_json supaya ia memulangkan salinan dengan indeks baharu.
    import json as _json
    from ui import app_qt as _aq
    _asli = _aq._read_json
    _set = {}
    if os.path.exists(_aq.SETTINGS):
        with open(_aq.SETTINGS, encoding="utf-8") as _f:
            _set = _json.load(_f)
    _set["font_scale_idx"] = int(_idx_env)
    def _baca(_p, _l):
        if _p == _aq.SETTINGS:
            return _set
        return _asli(_p, _l)
    _aq._read_json = _baca

w = PustakaApp()

PASS = 0
FAIL = 0


def semak(nama: str, ok: bool, butir: str = ""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
        print(f"  GAGAL {nama}  {butir}")


def tunggu(ms: int):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


# Satu hadis sebenar untuk halaman detail (dari hadis.db — sama seperti
# ujian visual lain; tidak bergantung pada rangkaian).
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
r = conn.execute(
    "SELECT collection, hadis_id, arab, melayu, indonesia "
    "FROM hadis WHERE arab<>'' AND melayu<>'' "
    "ORDER BY hadis_id LIMIT 1").fetchone()
e = conn.execute("SELECT english FROM terjemahan_eng "
                 "WHERE collection=? AND hadis_id=?",
                 (r["collection"], r["hadis_id"])).fetchone()
conn.close()
H = {"collection": r["collection"], "id": r["hadis_id"], "arab": r["arab"],
     "melayu": r["melayu"], "indonesia": r["indonesia"],
     "english": e["english"] if e else None, "nama_bab": None}

SAIZ = [(900, 560), (1024, 600), (1240, 730), (1366, 768)]
PAGES = ["home", "kitab", "detail", "search", "saved", "settings"]

w.show()
w.raise_()
tunggu(500)


def buka(key: str):
    if key == "detail":
        w.open_detail(H, "home")
    elif key == "kitab":
        w.open_kitab("bukhari", 1)
    else:
        w.go(key)


def semak_geometri(label: str):
    stack = w.stack
    s = stack.size()
    pg = stack.currentWidget()
    if pg is None:
        semak(f"{label}: halaman semasa wujud", False)
        return
    lebar_ok = abs(pg.width() - s.width()) <= 2
    tinggi_ok = abs(pg.height() - s.height()) <= 2
    semak(f"{label}: halaman == saiz stack", lebar_ok and tinggi_ok,
          f"pg={pg.width()}x{pg.height()} stack={s.width()}x{s.height()}")

    sa_list = [sa for sa in pg.findChildren(QScrollArea)
               if sa.viewport() is not None]
    for i, sa in enumerate(sa_list):
        vp = sa.viewport()
        semak(f"{label} sa{i}: viewport >= 80% stack (tidak 640x480)",
              vp.width() >= s.width() * 0.8,
              f"vp={vp.width()}x{vp.height()} stack={s.width()}x{s.height()}")
        hbar = sa.horizontalScrollBar().maximum()
        semak(f"{label} sa{i}: tiada skrol mengufuk (hbar 0)", hbar == 0,
              f"hbar={hbar}")

    # DESC_KLIP: label 'faint' halaman utama = deskripsi kad kitab
    # (dipendekkan ke satu baris 16 Ogos supaya tidak terpotong pada
    # saiz kad < 124px). Jika teks dibalut > tinggi tersedia -> klip.
    if label.startswith("home"):
        for lb in pg.findChildren(QLabel):
            if (lb.objectName() == "faint" and lb.text().strip()
                    and lb.isVisible() and lb.parentWidget() is not None):
                perlu = lb.sizeHint().height()
                ada = lb.height()
                semak(f"{label} desc: tidak terpotong", ada >= perlu - 3,
                      f"h={ada} sizeHint={perlu} teks={lb.text()[:40]!r}")


_skala = float(os.environ.get("QT_SCALE_FACTOR", "1.5"))

# ── Mod audit: lebar minimum setiap halaman tanpa hbar ─────────────
# `--minlebar` mengukur (carian binari) lebar tetingkap terkecil bagi
# SETIAP halaman yang masih tanpa skrol mengufuk tersembunyi — titik
# pecah responsif sebenar pada DPI semasa. Julat [900, 1400]: app
# setMinimumSize 900x560; CONTENT_MAX_W 1080 + GUTTER.
if "--minlebar" in sys.argv:
    def _tiada_hbar():
        pg = w.stack.currentWidget()
        if pg is None:
            return False
        s = w.stack.size()
        if abs(pg.width() - s.width()) > 2:
            return False
        for sa in pg.findChildren(QScrollArea):
            if sa.viewport() is None:
                continue
            if sa.horizontalScrollBar().maximum() != 0:
                return False
        return True

    print("=" * 62)
    print(f"  AUDIT LEBAR MINIMUM — 6 halaman (DPI "
          f"{int(round(_skala * 100))}%)")
    print("=" * 62)
    for key in PAGES:
        w.resize(1400, 700)
        tunggu(120)
        app.processEvents()
        buka(key)
        tunggu(120)
        app.processEvents()
        if not _tiada_hbar():
            print(f"  {key}: TIDAK muat walaupun 1400px")
            continue
        lo, hi = 900, 1400
        while lo < hi:
            mid = (lo + hi) // 2
            w.resize(mid, 700)
            tunggu(120)
            app.processEvents()
            buka(key)
            tunggu(120)
            app.processEvents()
            if _tiada_hbar():
                hi = mid
            else:
                lo = mid + 1
        print(f"  {key}: lebar minimum = {lo}px")
    w.close()
    print("\n" + "=" * 62)
    print("  AUDIT LEBAR MINIMUM SELESAI")
    print("=" * 62)
    sys.exit(0)

print("=" * 62)
print(f"  UJIAN RESPONSIF VIEWPORT — 6 halaman × 4 saiz "
      f"(DPI {int(round(_skala * 100))}%)")
print("=" * 62)
for saiz in SAIZ:
    w.resize(*saiz)
    tunggu(120)
    app.processEvents()
    # (a) resize SAHAJA — halaman semasa daripada saiz sebelumnya tidak
    #     boleh kekal basi (punca asal pepijat 640×480).
    semak_geometri(f"resize {saiz[0]}x{saiz[1]} (semasa)")
    # (b) navigasi ke setiap halaman pada saiz ini
    for key in PAGES:
        buka(key)
        tunggu(120)
        app.processEvents()
        semak_geometri(f"{key} @ {saiz[0]}x{saiz[1]}")

w.close()
print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
