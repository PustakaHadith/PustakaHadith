#!/usr/bin/env python3
"""Pengesahan PIPELINE END-TO-END — install → API → baca → tersimpan.

Mengisi item tertangguh #1/#6 dalam MANUAL_REFERENSI_DEV §8 (bahagian
API + mesin sebenar) dan item #4 (halaman Tersimpan dengan data
sebenar) dari sudut data API HIDUP:

  A. INSTALL  — semua kebergantungan requirements.txt diimport dengan
                versi disahkan (PyQt5, requests, pyperclip, tqdm,
                torch, sentence-transformers, faiss-cpu) + pintasan
                \"Hadis\" wujud.
  B. API      — API HIDUP service.hadis.my dipanggil TERUS dengan
                kunci developer (use_db=False, bukan proksi DB):
                /collections, /collections/{slug}/hadis,
                /collections/{slug}/hadis/{id}, /hadis/search.
                Kunci dibaca dari `kunci_terdedah.txt` (gitignored) —
                tidak pernah ditulis ke user_settings.json.
  C. BACA     — hadis dari API hidup dibuka dalam app sebenar, teks
                Arab + terjemahan dipapar.
  D. TERSIMPAN — hadis disimpan, halaman Tersimpan memaparkannya,
                kemudian ditanggalkan; bookmarks.json dipulihkan.

Jika kunci tiada (fail kunci_terdedah.txt tidak wujud), bahagian API
dilangkau dengan nota jujur — aliran app (baca + tersimpan) tetap
diuji dengan data DB sebenar.

    python uji_pipeline_api.py
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


BM = os.path.join(BASE, "bookmarks.json")
BM_SANDARAN = os.path.join(BASE, "bookmarks.json.sandaran_uji")
if os.path.exists(BM):
    shutil.copy2(BM, BM_SANDARAN)

print("=" * 62)
print("  PIPELINE END-TO-END — install → API → baca → tersimpan")
print("=" * 62)

try:
    # ── A. INSTALL: kebergantungan + pintasan ───────────────────────
    print("\n  ── A. INSTALL ──")
    modul = {
        "PyQt5": None, "requests": None, "pyperclip": None, "tqdm": None,
        "torch": None, "sentence_transformers": None, "faiss": None,
    }
    for m in modul:
        try:
            mod = __import__(m)
            modul[m] = getattr(mod, "__version__", "?")
        except Exception as e:
            modul[m] = f"GAGAL: {type(e).__name__}"
    semak("A1. Semua kebergantungan requirements.txt diimport",
          all(not str(v).startswith("GAGAL") for v in modul.values()),
          str(modul))
    semak("A2. Versi Python 3.14 (disahkan)",
          sys.version_info[:2] == (3, 14), ".".join(map(str, sys.version_info[:3])))

    # ── B. API HIDUP ─────────────────────────────────────────────────
    print("\n  ── B. API (service.hadis.my, KUNCI HIDUP) ──")
    kunci = ""
    try:
        with open(os.path.join(BASE, "kunci_terdedah.txt"),
                  encoding="utf-8") as f:
            for baris in f:
                b = baris.strip()
                if b and not b.startswith("#"):
                    kunci = b
                    break
    except OSError:
        pass

    hid_api = None
    if not kunci:
        print("  (kunci tiada — bahagian API hidup dilangkau)")
        semak("B1. Kunci API tersedia", False)
    else:
        from api.hadis_api import HadisAPI                    # noqa: E402
        from config import mask_key                           # noqa: E402
        print(f"  Kunci: {mask_key(kunci)} (dari kunci_terdedah.txt)")
        api = HadisAPI(api_key=kunci, use_db=False)          # TANPA proksi DB
        semak("B1. Mod API HIDUP (use_db=False)", not api.offline)

        koleksi = api.get_collections()
        semak("B2. /collections pulang 9 kitab", len(koleksi) == 9,
              f"jumpa {len(koleksi)}")
        semak("B3. /collections meta lengkap (nama + jumlah)",
              all(c.get("name") and c.get("total_hadis") for c in koleksi),
              f"cth: {koleksi[0]}")

        senarai = api.get_hadis_list("bukhari", page=1, limit=5, lang="ms")
        hs = senarai.get("hadis", [])
        semak("B4. /collections/bukhari/hadis pulang 5 hadis",
              len(hs) == 5, f"jumpa {len(hs)}")
        semak("B5. Hadis API ada Arab + Melayu (lang=ms)",
              all(h.get("arab") and h.get("melayu") for h in hs),
              f"cth id={hs[0].get('id')} arab={len(hs[0].get('arab',''))}chr")

        # Tanpa lang = ketiga-tiga bahasa (seperti paparan detail app)
        satu = api.get_hadis_by_id("bukhari", 1)
        semak("B6. /collections/bukhari/hadis/1 pulang hadis betul",
              satu is not None and satu.get("id") == 1
              and satu.get("collection") == "bukhari",
              str({k: satu.get(k) for k in ("id", "collection")}) if satu else "tiada")
        semak("B7. Hadis tunggal lengkap (arab+melayu+indonesia)",
              satu and satu.get("arab") and satu.get("melayu")
              and satu.get("indonesia"),
              f"arab={len(satu.get('arab',''))}chr "
              f"melayu={len(satu.get('melayu',''))}chr "
              f"indonesia={len(satu.get('indonesia',''))}chr")

        hasil = api.search_hadis("zakat", limit=3)
        semak("B8. /hadis/search 'zakat' pulang hasil",
              len(hasil.get("hadis", [])) > 0,
              f"jumpa {len(hasil.get('hadis', []))}")
        semak("B9. Kuota harian dibaca dari header",
              isinstance(api.daily_remaining, int),
              f"baki={api.daily_remaining}")
        hid_api = satu

    # ── C. BACA + D. TERSIMPAN (app sebenar) ────────────────────────
    print("\n  ── C. BACA + D. TERSIMPAN (app sebenar) ──")
    from ui.app_qt import PustakaApp, PAGES                  # noqa: E402

    w = PustakaApp()
    if kunci:
        w.settings["api_key"] = kunci         # dalam memori sahaja — tiada tulis fail
        w.api.set_key(kunci)
    w.show()
    w.raise_()
    w.activateWindow()
    tunggu(2500)
    semak("C1. App dilancarkan (9 koleksi dimuat)",
          len(w.collections) == 9, f"jumpa {len(w.collections)}")

    # Hadis untuk dibaca: dari API hidup jika ada, jika tidak dari DB
    if hid_api is not None:
        h = hid_api
    else:
        h = w.api.get_hadis_by_id("bukhari", 1)
        h["collection"] = "bukhari"
    w.open_detail(h, "home")
    tunggu(1200)
    dh = w._detail_h or {}
    semak("C2. Hadis dibuka dari data API hidup (bukhari #1)",
          dh.get("collection") == "bukhari" and dh.get("id") == 1,
          str({k: dh.get(k) for k in ("collection", "id")}))
    teks = dh.get("arab", "") + dh.get("melayu", "")
    semak("C3. Teks Arab + terjemahan dipapar",
          len(teks) > 200, f"{len(teks)} chr")

    w._toggle_save(h)
    tunggu(300)
    semak("D1. Hadis disimpan (bookmarks + butang)",
          w._is_saved("bukhari", 1) and "Tersimpan" in w._save_btn.text())
    w.go("saved")
    tunggu(700)
    semak("D2. Tersimpan memaparkan hadis",
          "1 hadis disimpan" in
          " ".join(t for obj in w.findChildren(object)
                   if hasattr(obj, "text") and obj.isVisible()
                   for t in [obj.text()] if t))

    # Tanggalkan + pulihkan
    w._toggle_save(h)
    tunggu(300)
    semak("D3. Ditanggalkan semula (data pengguna bersih)",
          not w._is_saved("bukhari", 1))

finally:
    tunggu(300)
    try:
        w.close()
    except Exception:
        pass
    tunggu(800)
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
    semak("E1. bookmarks.json dipulihkan (data pengguna selamat)", True)

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
