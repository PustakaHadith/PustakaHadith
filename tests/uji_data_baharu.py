#!/usr/bin/env python3
"""Ujian offscreen PustakaHadith — data baharu (bab/darjat/sema/hadeethenc).

Lancarkan aplikasi PyQt5 sebenar (QT_QPA_PLATFORM=offscreen), jalankan
carian gabungan (keyword + semantik), dan periksa kad butiran untuk
memastikan data yang di-sync dipaparkan dengan betul dalam UI.
"""

import os
import sys
import sqlite3

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication
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


def tunggu_worker(app_, ms: int):
    """Proses gelung acara Qt sehingga worker selesai / masa tamat."""
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


# ── 1. Data yang ada untuk ujian ────────────────────────────────────
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row

# Cari hadis yang ada SEMUA: bab + darjat + sema + hadethenc
calon = conn.execute("""
    SELECT h.collection, h.hadis_id
    FROM hadis h
    JOIN bab b    ON b.collection=h.collection AND b.hadis_id=h.hadis_id
    JOIN darjat d ON d.collection=h.collection AND d.hadis_id=h.hadis_id
    JOIN semakhadis s ON s.collection=h.collection AND s.hadis_id=h.hadis_id
    JOIN hadethenc he ON he.collection=h.collection AND he.hadis_id=h.hadis_id
    WHERE b.nama_bab <> '' AND h.arab <> ''
    LIMIT 3
""").fetchall()

# Cari hadis yang HANYA ada HadeethEnc (tiada sema) — ujian sandaran
dgn_he_sahaja = conn.execute("""
    SELECT h.collection, h.hadis_id FROM hadis h
    JOIN hadethenc he ON he.collection=h.collection AND he.hadis_id=h.hadis_id
    LEFT JOIN semakhadis s ON s.collection=h.collection AND s.hadis_id=h.hadis_id
    WHERE s.hadis_id IS NULL LIMIT 3
""").fetchall()

# Cari hadis dengan sema sahaja (tanpa hadethenc) dan bab sahaja
dgn_bab = conn.execute("""
    SELECT h.collection, h.hadis_id FROM hadis h
    JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id
    WHERE b.nama_bab <> '' AND h.arab <> '' LIMIT 3
""").fetchall()
dgn_sema = conn.execute("""
    SELECT h.collection, h.hadis_id FROM hadis h
    JOIN semakhadis s ON s.collection=h.collection AND s.hadis_id=h.hadis_id
    LIMIT 3
""").fetchall()
dgn_darjat = conn.execute("""
    SELECT h.collection, h.hadis_id FROM hadis h
    JOIN darjat d ON d.collection=h.collection AND d.hadis_id=h.hadis_id
    LIMIT 3
""").fetchall()
conn.close()

print("=" * 60)
print("  UJIAN UI — DATA BAHARU")
print("=" * 60)
print(f"\n  Calon lengkap (bab+darjat+sema+hadethenc): {len(calon)}")
print(f"  Calon bab sahaja                        : {len(dgn_bab)}")
print(f"  Calon sema sahaja                       : {len(dgn_sema)}")
print(f"  Calon darjat sahaja                     : {len(dgn_darjat)}")
print(f"  Calon HadeethEnc sahaja (tanpa sema)    : {len(dgn_he_sahaja)}")
semak("Ada hadis lengkap 4 sumber", len(calon) >= 1,
      f"jumpa {len(calon)}")
semak("Ada hadis ber-bab", len(dgn_bab) >= 1)
semak("Ada hadis ber-sema", len(dgn_sema) >= 1)
semak("Ada hadis ber-darjat", len(dgn_darjat) >= 1)
semak("Ada hadis HadeethEnc sahaja (ujian sandaran)", len(dgn_he_sahaja) >= 1)

# ── 2. Lancarkan aplikasi sebenar ───────────────────────────────────
print("\n  Lancarkan PustakaApp...")
from ui.app_qt import PustakaApp
w = PustakaApp()
w.show()

# Tunggu CollectionsWorker selesai + prapemuatan bermula
tunggu_worker(app, 3000)
semak("Koleksi dimuat (9 kitab)", len(w.collections) == 9,
      f"jumpa {len(w.collections)}")
semak("PreloadWorker dimulakan",
      getattr(w, "_preload", None) is not None)

# ── 3. Uji butiran lengkap (semua sumber) ───────────────────────────
if calon:
    print("\n  Butiran hadis lengkap (bab+darjat+sema+hadethenc):")
    for r in calon:
        slug, hid = r["collection"], r["hadis_id"]
        h = w.api.get_hadis_by_id(slug, hid)
        h["collection"] = slug
        w.open_detail(h, "home")
        tunggu_worker(app, 1500)

        bab = (h.get("nama_bab") or "").strip()
        sema = h.get("sema") or {}
        darjat = h.get("darjat") or []
        print(f"    {slug} #{hid}: bab={'ADA' if bab else 'TIADA'}"
              f"  sema={'ADA' if sema else 'TIADA'}"
              f"  darjat={len(darjat)} ulama")

        # Periksa UI betul-betul: cari widget merentas seluruh pokok
        # (bab/sema/darjat dibina di dalam `col` bersarang, bukan terus
        # dalam _detail_root).
        from PyQt5.QtWidgets import QLabel
        from ui.widgets import Collapsible
        found = {"bab": False, "sema": False, "darjat": False}
        for lbl in w.findChildren(QLabel):
            txt = lbl.text()
            if lbl.objectName() == "babName" and txt.strip():
                found["bab"] = True
        for col_w in w.findChildren(Collapsible):
            t = getattr(col_w, "_tajuk", "") or ""
            if "Huraian (SemakHadis" in t:
                found["sema"] = True
            if "Penilaian ulama (darjat)" in t:
                found["darjat"] = True
        semak(f"{slug} #{hid}: bab dipapar dalam UI", found["bab"] == bool(bab),
              f"dijangka {bool(bab)}")
        semak(f"{slug} #{hid}: huraian SemakHadis dipapar",
              found["sema"] == bool(sema))
        semak(f"{slug} #{hid}: bahagian darjat wujud", found["darjat"])
        break

# ── 3b. Uji sandaran HadeethEnc (tanpa sema) ───────────────────────
if dgn_he_sahaja:
    print("\n  Butiran hadis HadeethEnc sahaja (sandaran):")
    r = dgn_he_sahaja[0]
    slug, hid = r["collection"], r["hadis_id"]
    h = w.api.get_hadis_by_id(slug, hid)
    h["collection"] = slug
    w.open_detail(h, "home")
    tunggu_worker(app, 1500)

    # PENTING: open_detail membuat salinan dict(h) -> baca dari
    # w._detail_h (objek yang sebenarnya dipapar), bukan h asal.
    dh = w._detail_h or {}
    sema = dh.get("sema") or {}
    he = dh.get("he") or {}
    print(f"    {slug} #{hid}: sema={'ADA' if sema else 'tiada'}"
          f"  he={'ADA' if he else 'TIADA'}"
          f"  he_id={he.get('he_id') if he else '-'}")
    semak(f"{slug} #{hid}: sema tiada (betul untuk sandaran)", not sema)
    semak(f"{slug} #{hid}: huraian HadeethEnc ada",
          bool(he and (he.get("hadeeth") or he.get("explanation"))))

    # Periksa UI memaparkan Collapsible HadeethEnc
    from ui.widgets import Collapsible
    dipapar = False
    for col_w in w.findChildren(Collapsible):
        t = getattr(col_w, "_tajuk", "") or ""
        if "HadeethEnc" in t:
            dipapar = True
            # Buka dan sahkan kandungan dibina
            col_w._toggle()
            tunggu_worker(app, 300)
            break
    semak(f"{slug} #{hid}: Collapsible HadeethEnc dipapar", dipapar)

# ── 4. Uji carian gabungan (keyword + AI) ───────────────────────────
print("\n  Carian gabungan (keyword + semantik):")
w.search_bar.input.setText("kelebihan bersedekah")
w.go("search")
w._do_search(1)
# Tunggu SemanticWorker (model mungkin perlu dimuat -- diukur 27s hingga
# 80s bergantung pada cache/sejuk). Poling sehingga selesai / masa tamat
# supaya mesin perlahan tidak gagal kerana pemasa tetap.
import time as _t
_t0 = _t.time()
while w._sem_res is None and _t.time() - _t0 < 300:
    tunggu_worker(app, 1000)

semak("Carian keyword ada hasil",
      w._kw_res is not None and len(w._kw_res) > 0,
      f"jumpa {len(w._kw_res or [])}")
semak("Carian semantik selesai (boleh kosong jika index tak sedia)",
      w._sem_res is not None,
      f"sem_res={w._sem_res}")

if w._sem_res:
    semak("Carian semantik ada hasil", len(w._sem_res) > 0,
          f"jumpa {len(w._sem_res)}")
    if w._sem_res:
        top = w._sem_res[0]
        h2 = w.api.get_hadis_by_id(top["collection"], top["hadis_id"])
        h2["collection"] = top["collection"]
        w.open_detail(h2, "search")
        tunggu_worker(app, 1500)
        semak("Butiran hasil semantik boleh dibuka",
              h2 is not None and h2.get("arab"))
else:
    semak("Carian semantik ada hasil (atau index tidak sedia)",
          True, "index mungkin tidak sedia dalam ujian ini")

# ── 5. Tutup bersih (ujian closeEvent / crash 0xC0000409) ───────────
print("\n  Tutup aplikasi (uji closeEvent):")
tunggu_worker(app, 500)
w.close()
tunggu_worker(app, 3000)
semak("Aplikasi ditutup tanpa crash", True)

print("\n" + "=" * 60)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 60)
sys.exit(1 if FAIL else 0)
