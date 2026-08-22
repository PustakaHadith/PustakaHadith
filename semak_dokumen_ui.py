#!/usr/bin/env python3
"""Semakan konsistensi DOKUMEN manual vs UI SEBENAR (offscreen).

Membuka PustakaApp dan mengesahkan setiap tuntutan dokumen
(`dokumen/manual/MULA_CEPAT.md` + `MANUAL_PENGGUNAAN.md`) terhadap UI
sebenar: bar navigasi, skrin utama, halaman kitab, halaman hadis,
carian, Tersimpan, panel Tetapan, dan skrin pemula. Angka data
(62,169 / 31,833 / 4,237 / 63,930) disemak terus dari hadis.db.

Tidak mengubah apa-apa (state memori sahaja; bookmarks.json tidak
disentuh).

    python semak_dokumen_ui.py
"""

import json
import os
import re
import sqlite3
import sys

os.environ["QT_QPA_PLATFORM"] = "offscreen"
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton,  # noqa: E402
                             QLineEdit)
from PyQt5.QtCore import QTimer, QEventLoop                      # noqa: E402

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


def teks_semua(wdg) -> str:
    """Kumpul teks semua QLabel/QPushButton/QLineEdit yang kelihatan."""
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


def sumber(fail: str) -> str:
    with open(os.path.join(BASE, fail), encoding="utf-8") as f:
        return f.read()


# ── Angka data dari DB (MULA_CEPAT §1) ─────────────────────────────
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
N_HADIS = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
N_KITAB = conn.execute("SELECT COUNT(*) FROM collections").fetchone()[0]
N_ENG = conn.execute("SELECT COUNT(*) FROM terjemahan_eng").fetchone()[0]
N_SEMA = conn.execute("SELECT COUNT(*) FROM semakhadis").fetchone()[0]
N_DARJAT = conn.execute("SELECT COUNT(*) FROM darjat").fetchone()[0]
SEMA_BUKHARI = [r[0] for r in conn.execute(
    "SELECT hadis_id FROM semakhadis WHERE collection='bukhari' ORDER BY RANDOM() LIMIT 3")]
HE_NO_SEMA = [r[0] for r in conn.execute(
    "SELECT h.hadis_id FROM hadethenc h LEFT JOIN semakhadis s "
    "ON s.collection=h.collection AND s.hadis_id=h.hadis_id "
    "WHERE h.collection='bukhari' AND s.hadis_id IS NULL LIMIT 3")]
# English per kitab (MANUAL §1: 7 kitab utama; Ahmad/Darimi tiada)
N_ENG_PER = {r[0]: r[1] for r in conn.execute(
    "SELECT collection, COUNT(*) FROM terjemahan_eng GROUP BY collection")}
conn.close()

print("=" * 62)
print("  SEMAKAN DOKUMEN vs UI SEBENAR")
print("=" * 62)

# ── A. Angka (MULA_CEPAT §1) ────────────────────────────────────────
print("\n  ── A. Angka data (MULA_CEPAT §1) ──")
semak("A1. 9 kitab hadis", N_KITAB == 9, f"jumpa {N_KITAB}")
semak("A2. 62,169 hadis", N_HADIS == 62169, f"jumpa {N_HADIS:,}")
semak("A3. 31,833 terjemahan Inggeris", N_ENG == 31833, f"jumpa {N_ENG:,}")
semak("A4. 4,237 huraian SemakHadis", N_SEMA == 4237, f"jumpa {N_SEMA:,}")
semak("A5. 63,930 darjat", N_DARJAT == 63930, f"jumpa {N_DARJAT:,}")
semak("A6. English 7 kitab utama (Ahmad/Darimi tiada)",
      set(N_ENG_PER) == {"bukhari", "muslim", "abu-daud", "tirmidzi",
                          "nasai", "ibnu-majah", "malik"}
      and all(N_ENG_PER[k] > 0 for k in N_ENG_PER),
      str(dict(N_ENG_PER)))
semak("A7. Berjalan pada Python 3.14 (MULA_CEPAT §1)",
      sys.version_info[:2] >= (3, 14), sys.version.split()[0])
import re as _re                                                   # noqa: E402
_pra = sumber("uji_pra_hantar.py")
_n_ujian = len(_re.findall(r"\(\"\d+\.", _pra))
semak("A8. Suite pra-hantar 14 ujian (MULA_CEPAT §1)",
      _n_ujian == 14 and "uji_tersimpan_sebenar.py" in _pra
      and "semak_dokumen_ui.py" in _pra
      and "uji_responsif_viewport.py" in _pra,
      f"jumpa {_n_ujian} senarai")

# ── B. Lancar app + nav + utama (MANUAL §2.1-2.2, MULA_CEPAT §3) ────
print("\n  ── B. Nav + skrin utama (MANUAL §2.1-2.2) ──")
from ui.app_qt import PustakaApp, PAGES                      # noqa: E402

w = PustakaApp()
w.show()
tunggu(2500)

nav_teks = teks_semua(w)
for label in ("Utama", "Pencarian", "Tersimpan", "⚄  Rawak"):
    semak(f"B1. Nav '{label}'", label in nav_teks, f"tiada dalam nav")
from ui.widgets import GearButton                                  # noqa: E402
semak("B2. Nav ada gear (GearButton)",
      len(w.findChildren(GearButton)) > 0,
      f"jumpa {len(w.findChildren(GearButton))}")
semak("B3. 9 kad kitab di utama", len(w.collections) == 9)
semak("B4. Kotak carian di skrin utama",
      w.search_bar is not None and w.search_bar.input is not None)
semak("B5. Halaman utama aktif", w.stack.currentIndex() == PAGES["home"])

# ── C. Halaman kitab (MANUAL §2.3, MULA_CEPAT §3) ───────────────────
print("\n  ── C. Halaman kitab (MANUAL §2.3) ──")
w.open_kitab("bukhari", 1)
t0 = 0
import time                                                        # noqa: E402
t0 = time.time()
while time.time() - t0 < 10 and (not getattr(w, "_kitab_list", None)
                                 or w._kitab_list.count() <= 3):
    tunggu(100)
semak("C1. Senarai Bukhari dipapar", w._kitab_list.count() > 3,
      f"kad={w._kitab_list.count()}")
pager = getattr(w, "_kitab_pager", None)
semak("C2. Pager '‹ Sebelum' + 'Seterusnya ›'",
      pager is not None and "‹ Sebelum" in teks_semua(pager)
      and "Seterusnya ›" in teks_semua(pager))
gb = getattr(w, "_kitab_go_box", None)
ph = gb.placeholderText() if gb else ""
semak("C3. Kotak 'Lompat No. hadis' + placeholder julat",
      gb is not None and ph == "0–7008", f"placeholder={ph!r}")
semak("C4. Pintasan Ctrl+G wujud", hasattr(w, "_sc_lompat"))
semak("C5. Butang ↑ (backTop)",
      getattr(w, "_kitab_top_btn", None) is not None
      and w._kitab_top_btn.objectName() == "backTop")
semak("C6. 20 hadis per halaman lalai", w.per_page() == 20,
      f"per_page={w.per_page()}")

# ── D. Halaman hadis (MANUAL §2.4, MULA_CEPAT §3) ───────────────────
print("\n  ── D. Halaman hadis (MANUAL §2.4, MULA_CEPAT §3) ──")
h1 = w.api.get_hadis_by_id("bukhari", 1)
h1["collection"] = "bukhari"
w.open_detail(h1, "kitab")
tunggu(1200)
dh = w._detail_h or {}
det_teks = teks_semua(w)
semak("D1. Butang tajuk 💬 WhatsApp / 📋 Salin / 🔊 Dengar",
      "💬 WhatsApp" in det_teks and "📋 Salin" in det_teks
      and "🔊 Dengar" in det_teks)
semak("D2. Butang Simpan '☆ Simpan' (belum disimpan)",
      "☆ Simpan" in det_teks or "⭐ Tersimpan" in det_teks)
semak("D3. Tab ARAB + TRANSLITERASI",
      getattr(w, "_btn_arab", None) is not None
      and getattr(w, "_btn_translit", None) is not None
      and w._btn_arab.text() == "ARAB"
      and w._btn_translit.text() == "TRANSLITERASI")
# Dua lajur (RTL 14 Ogos): lajur terjemahan (kiri) + lajur Arab (kanan)
ar_x = getattr(w, "_ar_stack", None).x() if getattr(w, "_ar_stack", None) else None
tr_x = getattr(w, "_trans_box", None).x() if getattr(w, "_trans_box", None) else None
semak("D3b. Dua lajur RTL (terjemahan kiri, Arab kanan)",
      ar_x is not None and tr_x is not None and ar_x > tr_x,
      f"ar_x={ar_x}, tr_x={tr_x}")
tabs = getattr(w, "_lang_tabs", None)
if tabs is not None:
    semak("D4. 3 tab bahasa (Melayu/Indonesia/English)",
          set(tabs._btns) == {"melayu", "indonesia", "english"},
          f"tab={sorted(tabs._btns)}")
    semak("D5. TIADA tab 'Sebelah'", "sebelah" not in tabs._btns)
else:
    semak("D4. 3 tab bahasa", False); semak("D5. TIADA tab Sebelah", False)
bt = w.findChild(QLabel, "barTindakan")
bar_teks = bt.text() if bt else ""
semak("D6. Bar teks 'Lapor ralat | Kongsi | Salin'",
      bt is not None and "Lapor ralat" in bar_teks and "Kongsi" in bar_teks
      and "Salin" in bar_teks and "|" in bar_teks,
      bar_teks[:80] if bt else "tiada widget barTindakan")
semak("D7. Kongsi buka WhatsApp (sumber)", "wa.me" in sumber("ui/helpers.py")
      or "_share_bahasa_semasa" in sumber("ui/pages_detail.py"))

# Menu Salin 3 pilihan -- semak sumber (label tepat)
src_detail = sumber("ui/pages_detail.py")
semak("D8. Menu Salin 3 pilihan (label tepat)",
      "Salin Arab sahaja" in src_detail
      and "Salin terjemahan (bahasa semasa)" in src_detail
      and "Salin Arab + terjemahan semasa" in src_detail)
semak("D9. Lapor ralat buka sunnah.com",
      "sunnah.com" in src_detail or "sunnah_url" in src_detail)

# Huraian SemakHadis + Darjat
from ui.widgets import Collapsible                              # noqa: E402

def _cari_collapsible(mengandungi: str):
    for c in w.findChildren(Collapsible):
        if mengandungi in getattr(c, "_tajuk", ""):
            return c
    return None

if SEMA_BUKHARI:
    hs = w.api.get_hadis_by_id("bukhari", SEMA_BUKHARI[0])
    hs["collection"] = "bukhari"
    w.open_detail(hs, "kitab")
    tunggu(1200)
    semak("D10. Huraian (SemakHadis) dipapar utk hadis bersema",
          _cari_collapsible("Huraian (SemakHadis") is not None)
else:
    semak("D10. Huraian (SemakHadis)", False, "tiada calon")
semak("D11. Darjat ulama dipapar",
      bool(dh.get("darjat")) or any(
          "Darjat" in t or "Penilaian" in t for t in teks_semua(w).split("\n")))

# HadeethEnc sandaran (MANUAL §1) -- hadis tanpa sema tetapi ada HE
if HE_NO_SEMA:
    hhe = w.api.get_hadis_by_id("bukhari", HE_NO_SEMA[0])
    hhe["collection"] = "bukhari"
    w.open_detail(hhe, "kitab")
    tunggu(1200)
    semak("D12. Huraian HadeethEnc sandaran dipapar (tiada sema)",
          _cari_collapsible("Huraian (HadeethEnc") is not None)
else:
    semak("D12. Huraian HadeethEnc sandaran", False, "tiada calon HE")

# Cip warna ikut makna (MANUAL §2.4) + menu klik kanan + backTop detail
semak("D13. Cip warna ikut makna (hijau/merah/amber)",
      "GREEN_BG" in src_detail and "RED_BG" in src_detail
      and "AMBER_BG" in src_detail
      and "palsu" in src_detail.lower() and "lemah" in src_detail.lower())
semak("D14. Klik kanan 'Salin semua'", "Salin semua" in sumber("ui/widgets.py"))
semak("D15. Butang ↑ detail (backTop)",
      getattr(w, "_detail_top_btn", None) is not None
      and w._detail_top_btn.objectName() == "backTop")

# ── E. Carian (MANUAL §2.5, MULA_CEPAT §3) ──────────────────────────
print("\n  ── E. Carian (MANUAL §2.5) ──")
from ui.helpers import _parse_lompat                            # noqa: E402
semak("E1. 'bukhari 433' lompat terus", _parse_lompat("bukhari 433")
      == ("bukhari", 433), str(_parse_lompat("bukhari 433")))
semak("E2. 'B433' lompat terus", _parse_lompat("B433") == ("bukhari", 433),
      str(_parse_lompat("B433")))
semak("E3. 'bukhari:433' lompat terus", _parse_lompat("bukhari:433")
      == ("bukhari", 433))
semak("E4. Nombor sahaja guna kitab lalai", _parse_lompat("433", "bukhari")
      == ("bukhari", 433))
src_carian = sumber("ui/pages_carian.py")
src_workers = sumber("ui/workers.py")
semak("E5. Dua enjin carian: kata kunci (SearchWorker) + makna AI "
      "(SemanticWorker)",
      "SearchWorker(self.api" in src_carian
      and "SemanticWorker" in src_carian
      and "class SemanticWorker(_Base)" in src_workers)
semak("E6. Butang ↑ carian (backTop)",
      getattr(w, "_search_top_btn", None) is not None
      and w._search_top_btn.objectName() == "backTop")
semak("E7. Draf jawapan AI dipapar di atas hasil",
      "compose_draft_answer" in src_carian
      and "draft_widget" in src_carian)
semak("E8. Jam berputar 🕐→🕛 semasa carian",
      "self._jam" in src_carian and "🕐" in src_carian)
semak("E9. Notis carian longgar", "longgar" in src_carian)

# ── F. Tersimpan (MANUAL §2.6, MULA_CEPAT §3) ───────────────────────
print("\n  ── F. Tersimpan (MANUAL §2.6) ──")
w.go("saved")
tunggu(600)
sav_teks = teks_semua(w)
semak("F1. Empty state 'Belum ada hadis tersimpan'",
      "Belum ada hadis tersimpan" in sav_teks)
semak("F2. Hero 'Hadis Tersimpan'", "Hadis Tersimpan" in sav_teks)
semak("F3. Butang ↑ Tersimpan (backTop)",
      getattr(w, "_tersimpan_top_btn", None) is not None
      and w._tersimpan_top_btn.objectName() == "backTop")

# ── G. Panel Tetapan (MANUAL §3, MULA_CEPAT §2) ─────────────────────
print("\n  ── G. Panel Tetapan (MANUAL §3) ──")
w.settings_panel.open_panel()
tunggu(400)
set_teks = teks_semua(w.settings_panel)
for bhg in ("TEMA", "PAPARAN", "BACAAN", "SAMBUNGAN", "TENTANG"):
    semak(f"G1. Bahagian '{bhg}'", bhg in set_teks, f"tiada dalam panel")
semak("G2. Butang tema 2 pilihan (Neutral / Neutral terang)",
      "🌙  Neutral" in set_teks
      and "☀  Neutral terang" in set_teks)
semak("G3. 'Hadis per halaman' dalam Bacaan", "Hadis per halaman" in set_teks)
labels = getattr(w.settings_panel, "_stepper_labels", None)
if labels:
    t = {k: v.text() for k, v in labels.items()}
    semak("G4. Stepper fon 'Kecil'/'Sederhana'/'Besar'",
          all(v in ("Kecil", "Sederhana", "Besar") for v in t.values()),
          str(t))
else:
    semak("G4. Stepper fon", False)
for lbl in ("Saiz teks Arab", "Saiz terjemahan",
            "Fon Arab", "Bahasa dimuat", "Selawat", "Tetapan API",
            "Tentang PustakaHadith"):
    semak(f"G5. Label Tetapan '{lbl}'", lbl in set_teks, f"tiada dalam panel")
w.settings_panel.close_panel()
tunggu(300)

# ── H. Skrin pemula (MANUAL §1, MULA_CEPAT §2) ──────────────────────
print("\n  ── H. Skrin pemula (MANUAL §1) ──")
src_splash = sumber("ui/splash.py")
semak("H1. Splash papar 'Sedia! ✔'", "Sedia! ✔" in src_splash)
semak("H2. Splash boleh diklik (langkau)", "diklik" in src_splash
      and "pyqtSignal" in src_splash)
src_dek = sumber("ui/deklarasi.py")
semak("H4. Deklarasi larian pertama dengan butang 'Faham'",
      "Faham" in src_dek and "DEKLARASI_FLAG" in src_dek)
semak("H3. Splash ada bar kemajuan", "set_fasa" in src_splash
      or "kemajuan" in src_splash)

# ── I. Pemasangan (MULA_CEPAT §2, BACA_SAYA, MANUAL_INSTALASI) ──────
print("\n  ── I. Pemasangan (fail + tuntutan .bat) ──")
for fail in ("PASANG.bat", "BUAT_PINTASAN.bat", "JALANKAN.bat",
             "NYAHPEPIJAT.bat", "BUANG.bat", "KEMASKINI.bat",
             "BACA_SAYA.txt", "pintasan.ps1"):
    semak(f"I1. Fail {fail} wujud", os.path.exists(os.path.join(BASE, fail)))

p_passang = sumber("PASANG.bat")
p_buat = sumber("BUAT_PINTASAN.bat")
p_jalan = sumber("JALANKAN.bat")
p_pepijat = sumber("NYAHPEPIJAT.bat")
p_buang = sumber("BUANG.bat")
p_kemas = sumber("KEMASKINI.bat")
p_pintasan = sumber("pintasan.ps1")
baca = sumber("BACA_SAYA.txt")

semak("I2. PASANG.bat: 'SIAP' + pintasan.ps1 + Tetapan API",
      "SIAP" in p_passang and "pintasan.ps1" in p_passang
      and "Tetapan API" in p_passang)
semak("I3. BUAT_PINTASAN.bat panggil pintasan.ps1", "pintasan.ps1" in p_buat)
semak("I4. JALANKAN.bat jalankan main.py", "main.py" in p_jalan)
semak("I5. NYAHPEPIJAT.bat: tetingkap kekal terbuka + ralat penuh",
      "TIDAK akan tutup" in p_pepijat and "main.py" in p_pepijat)
semak("I6. BUANG.bat: 2 soalan + taip BUANG",
      "Buang juga data" in p_buang and "Tanggal PyQt5" in p_buang
      and "Taip BUANG" in p_buang)
semak("I7. KEMASKINI.bat: terima laluan ZIP", "ZIP" in p_kemas)
semak("I8. pintasan.ps1 cipta 'Hadis.lnk' Desktop + Start Menu",
      "Hadis.lnk" in p_pintasan and "Desktop" in p_pintasan
      and "Start Menu" in p_pintasan)
semak("I9. BACA_SAYA.txt: PASANG 'SIAP' + ikon Hadis + BUANG",
      "PASANG.bat" in baca and "SIAP" in baca and "Hadis" in baca
      and "BUANG.bat" in baca and "NYAHPEPIJAT.bat" in baca)

# ── J. README Ciri-ciri ↔ MANUAL_PENGGUNAAN tidak hanyut (14 Ogos) ──
print("\n  ── J. Konsistensi README ↔ MANUAL_PENGGUNAAN ──")
README_ISI = sumber("README.md")
MANUAL_ISI = sumber("dokumen/manual/MANUAL_PENGGUNAAN.md")
# Frasa kunci Ciri-ciri mesti wujud dalam KEDUA-DUA dokumen supaya
# tuntutan ciri (tab, bar teks, angka) tidak hanyut antara satu sama
# lain. Perubahan ciri mesti disusuli di kedua-duanya.
_J_FRASA = ("TRANSLITERASI", "Melayu", "Indonesia", "English",
            "Lapor ralat", "Kongsi", "Salin",
            "Arab + terjemahan semasa", "sama paras", "dua lajur",
            "62,169", "4,237")
for frasa in _J_FRASA:
    semak(f"J1. '{frasa}' dalam README + MANUAL_PENGGUNAAN",
          frasa in README_ISI and frasa in MANUAL_ISI,
          f"README:{frasa in README_ISI} MANUAL:{frasa in MANUAL_ISI}")

# ── K. MULA_CEPAT ringkasan ↔ README tidak hanyut (14 Ogos) ──────────
print("\n  ── K. Konsistensi MULA_CEPAT ↔ README ──")
MULA_ISI = sumber("dokumen/manual/MULA_CEPAT.md")
# Ringkasan Mula Cepat mesti mengekalkan tuntutan kunci yang sama
# dengan README (angka data + ciri teras). Ringkasan tidak perlu
# 'sama paras'/'dua lajur' — ia guna 'Lajur kiri/kanan'.
_K_FRASA = ("TRANSLITERASI", "Melayu", "Indonesia", "English",
            "Lapor ralat", "Kongsi", "Salin",
            "Arab + terjemahan semasa", "62,169", "4,237", "63,930",
            "bukhari 433")
for frasa in _K_FRASA:
    semak(f"K1. '{frasa}' dalam MULA_CEPAT + README",
          frasa in MULA_ISI and frasa in README_ISI,
          f"MULA_CEPAT:{frasa in MULA_ISI} README:{frasa in README_ISI}")

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
