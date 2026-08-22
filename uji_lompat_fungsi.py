#!/usr/bin/env python3
"""Ujian fungsi Lompat ke Hadis dalam app sebenar (offscreen).

Sahkan rantaian lengkap: _parse_lompat -> _lompat_ke -> _load_kitab_page
-> skrol ke kad sasaran, dan _buka_hadis_terus (nombor sahaja).

Sesi 38/39: carian khusus (nama kitab + nombor) daripada halaman UTAMA
(_from_home_search, dari='home') dan halaman Carian juga terus ke
butiran, bukan senarai kitab. Sesi 40b/40c: butang Kembali dari butiran
menuju ke halaman asal yang betul — 'home' -> Utama, 'search' ->
Hasil carian (bukan destinasi silap). NOTA: QTimer mod offscreen tidak
menunggu masa sebenar, jadi tunggu_sedia() (polling) digunakan untuk
semua peringkat muatan — elak flaky semakan sebelum worker/layout
selesai.
"""

import os
import sys
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QEventLoop, QTimer
app = QApplication(sys.argv)


def tunggu(ms: int):
    """Tunggu ms milisaat dengan event loop aktif (proses isyarat Qt).

    NOTA: QTimer dalam mod offscreen TIDAK menunggu masa sebenar
    (dicetuskan serta-merta), jadi `tunggu` tidak menjamin masa sebenar
    — ia hanya memberi peluang kepada event loop memproses worker.
    Gunakan `tunggu_sedia` untuk keadaan yang perlu menunggu muatan.
    """
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


def tunggu_sedia(syarat, masa_maks: float = 8.0, selang: float = 0.05):
    """Polling sehingga `syarat()` benar (dengan had masa).

    QTimer offscreen tidak menunggu masa sebenar, jadi menunggu muatan
    dengan singleShot tetap TIDAK boleh dipercayai — kadang-kadang
    semakan berjalan sebelum worker/layout selesai dan scrollbar masih
    max=0. Polling dengan processEvents sehingga syarat dipenuhi (atau
    had masa tamat) menghilangkan flaky itu.
    """
    t0 = time.monotonic()
    while time.monotonic() - t0 < masa_maks:
        if syarat():
            return True
        app.processEvents()
        time.sleep(selang)
    return False

from ui.app_qt import PustakaApp, _parse_lompat
from ui.helpers import BOOKMARKS, _write_json
from ui.theme import COLLECTION_META

t0 = time.time()


def ts():
    return "%.2f" % (time.time() - t0)


PASS = 0
FAIL = 0


def semak(nama, ok, butir=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  OK    {nama}")
    else:
        FAIL += 1
        print(f"  GAGAL {nama}  {butir}")


w = PustakaApp()
# Papar + saiz sebenar supaya layout QScrollArea selesai (offscreen
# tanpa show() meninggalkan viewport tanpa julat skrol yang sah).
w.show()
w.resize(1000, 800)
print(f"[{ts()}] BUILD OK")


def jalankan():
    print("=== Parser lompat (fungsi tulen) ===")
    semak("bukhari 433", _parse_lompat("bukhari 433") == ("bukhari", 433))
    semak("B433", _parse_lompat("B433") == ("bukhari", 433))
    semak("b:433", _parse_lompat("b:433") == ("bukhari", 433))
    semak("abu daud 10", _parse_lompat("abu daud 10") == ("abu-daud", 10))
    semak("433 default muslim", _parse_lompat("433", "muslim") == ("muslim", 433))
    semak("hukum riba bukan lompat", _parse_lompat("hukum riba") is None)
    semak("m 5 ambigu bukan lompat", _parse_lompat("m 5") is None)

    print("=== _kira_halaman_lompat (offline) ===")
    page, total = w._kira_halaman_lompat("bukhari", 433)
    semak(f"bukhari 433 -> page {page}, total {total}",
          page >= 1 and total > 0, f"dapat page={page} total={total}")
    r = w._sahkan_lompat("bukhari", 999999, "Sahih al-Bukhari")
    semak("bukhari 999999 ditolak (di luar julat)", r is None, f"dapat {r!r}")

    print("=== _lompat_ke (senarai kitab, skrol ke kad) ===")
    w._kitab_go_to_hid = None
    # #500 dipilih kerana halamannya (25) panjang — kandungan melebihi
    # viewport, jadi skrol ke sasaran benar-benar diuji (Sesi 36).
    w._lompat_ke("bukhari", 500)
    # Tunggu sehingga halaman dimuat DAN layout selesai (scrollbar
    # berjulat). Polling, bukan singleShot tetap — QTimer offscreen
    # tidak menunggu masa sebenar (flaky tanpa ini).
    sedia = tunggu_sedia(lambda: w._kitab_list.count() > 0
                         and w._kitab_sa.verticalScrollBar().maximum() > 0)
    semak("halaman kitab dimuat + layout selesai", sedia)
    periksa_kitab()


def _kad_kelihatan(w, hid):
    """Benarkah kad hid kelihatan dalam viewport skrol (Sesi 36).

    Skrol ke sasaran pernah rosak senyap: setValue dipanggil sebelum
    julat scrollbar wujud (layout belum selesai) jadi terampas ke 0 dan
    kad sasaran langsung tidak kelihatan. Semakan ini mengunci bahawa
    kad yang dilompat benar-benar berada dalam viewport.
    """
    bar = w._kitab_sa.verticalScrollBar()
    vh = w._kitab_sa.viewport().height()
    for i in range(w._kitab_list.count()):
        it = w._kitab_list.itemAt(i)
        c = it.widget() if it else None
        if c is not None and getattr(c, "_hid", None) == hid:
            y = c.mapTo(w._kitab_sa.widget(), c.rect().topLeft()).y()
            yv = y - bar.value()
            return 0 <= yv < vh, f"y_visible={yv}, viewport={vh}, scroll={bar.value()}"
    return False, f"kad {hid} tiada dalam senarai"


def _periksa_kembali(dari_carian: str, label_jangkaan: str,
                    indeks_jangkaan: int, bukan_indeks: int,
                    bukan_label: str):
    """Butang Kembali dari butiran -> halaman asal yang betul.

    `_render_detail` memilih back[_detail_from]: 'home' -> Utama
    (go('home')), 'search' -> Hasil carian (go('search')). Semak
    tooltip ("Kembali ke {label_jangkaan}") + destinasi sebenar selepas
    klik, dan pastikan ia BUKAN destinasi yang salah — regresi yang
    membawa pengguna ke halaman kosong/keliru (Sesi 40b/40c).
    """
    bb = [b for b in w._detail_bar.findChildren(QPushButton)
          if "Kembali" in b.text()]
    semak(f"butang Kembali wujud ('{dari_carian}')", bool(bb))
    if not bb:
        return
    semak(f"tooltip Kembali -> {label_jangkaan} ('{dari_carian}')",
          bb[0].toolTip() == f"Kembali ke {label_jangkaan}",
          f"tooltip={bb[0].toolTip()!r}")
    bb[0].click()
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == indeks_jangkaan)
    semak(f"Kembali -> {label_jangkaan} ('{dari_carian}')", sedia,
          f"index={w.stack.currentIndex()}")
    semak(f"Kembali BUKAN ke {bukan_label} ('{dari_carian}')",
          w.stack.currentIndex() != bukan_indeks,
          f"index={w.stack.currentIndex()}")


def periksa_kitab():
    n = w._search_list.count() if hasattr(w, "_search_list") else -1
    # Halaman kitab: senarai kad dalam _kitab_list
    kad = w._kitab_list.count()
    meta = COLLECTION_META["bukhari"]
    print(f"    (kitab aktif={w._kitab_slug}, kad={kad}, go_to={w._kitab_go_to_hid})")
    semak("halaman kitab bukhari dibuka", w._kitab_slug == "bukhari")
    semak("senarai kad tidak kosong", kad > 0)
    sasaran = [getattr(w._kitab_list.itemAt(i).widget(), "_hid", None)
               for i in range(w._kitab_list.count())
               if w._kitab_list.itemAt(i) is not None
               and w._kitab_list.itemAt(i).widget() is not None]
    semak("kad 500 ada dalam senarai", 500 in sasaran,
          f"id teratas: {sasaran[:5]}")
    semak("go_to dibersihkan selepas skrol", w._kitab_go_to_hid is None)
    ok, butir = _kad_kelihatan(w, 500)
    semak("kad 500 benar-benar kelihatan selepas lompat", ok, butir)
    bar = w._kitab_sa.verticalScrollBar()
    # Halaman 25 panjang — kandungan melebihi viewport, jadi skrol
    # WAJIB bergerak untuk mendedahkan kad #500 (diukur y=2910,
    # viewport 738). Jika skrol rosak senyap (setValue terampas ke 0),
    # semakan ini akan GAGAL.
    semak("scrollbar bergerak ke sasaran (halaman panjang)",
          bar.maximum() > 0 and bar.value() > 0,
          f"value={bar.value()}, max={bar.maximum()}")

    print("=== _buka_hadis_terus (nombor sahaja) ===")
    w._detail_from = None
    w._buka_hadis_terus("bukhari", 1, dari="search")
    # Tunggu butiran dibuka (open_detail -> go('detail'))
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2)
    semak("butiran hadis dibuka (PAGES['detail'])", sedia,
          f"index={w.stack.currentIndex()}")
    semak("_detail_from = search", getattr(w, "_detail_from", None) == "search")
    # Kembali dari butiran yang dibuka melalui halaman CARIAN
    # (dari='search') -> halaman Carian (PAGES['search'] = 3), BUKAN
    # Utama (PAGES['home'] = 0). Regresi: back["search"] menuju ke
    # Carian, jadi pengguna yang memulakan carian di sana tidak hilang
    # konteks hasil carian.
    _periksa_kembali("bukhari 1 (search)", "Hasil carian", 3, 0,
                     "halaman Utama")

    print("=== Carian khusus dari halaman UTAMA (dari='home') ===")
    # Aliran pengguna sebenar: taip 'bukhari 500' dalam bar carian
    # halaman Utama -> _from_home_search -> _buka_hadis_terus dengan
    # dari='home' (Sesi 38). Mesti terus ke butiran, BUKAN senarai
    # kitab, dan butang Kembali menuju ke Utama.
    w.go("home")
    w.home_search.input.setText("bukhari 500")
    w._from_home_search()
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == 500)
    semak("carian khusus Utama: butiran No. 500 dibuka", sedia,
          f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")
    semak("carian khusus Utama bukan halaman kitab",
          w.stack.currentIndex() != 1, f"index={w.stack.currentIndex()}")
    semak("_detail_from = home",
          getattr(w, "_detail_from", None) == "home",
          f"dari={w._detail_from}")
    _periksa_kembali("bukhari 500", "Utama", 0, 3, "halaman Carian")

    # Nombor SAHAJA dari Utama juga terus ke butiran (dari='home')
    w.go("home")
    w.home_search.input.setText("433")
    if w.home_search.chips:
        w.home_search.chips.set_active("bukhari", emit=False)
    w._from_home_search()
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == 433)
    semak("nombor sahaja Utama: butiran No. 433 dibuka", sedia,
          f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")
    semak("_detail_from = home (nombor sahaja)",
          getattr(w, "_detail_from", None) == "home",
          f"dari={w._detail_from}")
    _periksa_kembali("433", "Utama", 0, 3, "halaman Carian")

    print("=== Butang Sebelum/Seterusnya (bar navigasi bawah) ===")
    # Logik label diuji unit (semak.py 8q); di sini tingkah laku SEBENAR
    # pada butiran: No. 1 (hadis pertama) TIADA butang Sebelum, No. 2
    # ada '‹ No. 1', dan klik Seterusnya membuka hadis seterusnya.

    def _butang_bawah(teks):
        return [b for b in w._detail_bar.findChildren(QPushButton)
                if b.text() == teks]

    # No. 1: tiada pendahulu -> tiada butang Sebelum; Seterusnya ada.
    w._buka_hadis_terus("bukhari", 1, dari="search")
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == 1)
    semak("butiran No. 1 dibuka", sedia,
          f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")
    sb1 = [b for b in w._detail_bar.findChildren(QPushButton)
           if b.text().startswith("‹ No.")]
    semak("No. 1: TIADA butang Sebelum (hadis pertama)", not sb1,
          f"jumpa {[b.text() for b in sb1]}")
    semak("No. 1: butang Seterusnya 'No. 2 ›' ada",
          bool(_butang_bawah("No. 2 ›")))

    # No. 2: Sebelum '‹ No. 1' ADA; Seterusnya 'No. 3 ›' ada.
    w._buka_hadis_terus("bukhari", 2, dari="search")
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == 2)
    semak("butiran No. 2 dibuka", sedia,
          f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")
    semak("No. 2: butang Sebelum '‹ No. 1' ada",
          bool(_butang_bawah("‹ No. 1")),
          f"jumpa {[b.text() for b in sb1]}")
    ns2 = _butang_bawah("No. 3 ›")
    semak("No. 2: butang Seterusnya 'No. 3 ›' ada", bool(ns2))

    # Klik Seterusnya -> muat async -> butiran No. 3 dibuka.
    if ns2:
        ns2[0].click()
        sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                             and (w._detail_h or {}).get("id") == 3)
        semak("klik Seterusnya -> butiran No. 3 dibuka", sedia,
              f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")

    print("=== Butang Simpan/Tersimpan (togol penanda buku) ===")
    # Logik label diuji unit (semak.py 8r); di sini tingkah laku SEBENAR:
    # klik Simpan menukar label kepada '⭐ Tersimpan' DAN menambah ke
    # penanda buku; klik kedua mengembalikan label + membuangnya.
    # Keadaan awal dipaksa bersih (bukhari#2 dibuang dahulu) supaya
    # deterministik; penanda buku asal dipulihkan selepas ujian.
    asal_bm = list(w.bookmarks)
    w.bookmarks = [b for b in w.bookmarks
                   if not (b.get("slug") == "bukhari" and b.get("id") == 2)]
    w._buka_hadis_terus("bukhari", 2, dari="search")
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == 2)
    semak("butiran No. 2 dibuka (ujian Simpan)", sedia,
          f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")
    semak("butang Simpan mula '☆ Simpan' (belum disimpan)",
          w._save_btn.text() == "☆ Simpan", f"teks={w._save_btn.text()!r}")
    w._save_btn.click()
    semak("klik Simpan -> label '⭐ Tersimpan'",
          w._save_btn.text() == "⭐ Tersimpan", f"teks={w._save_btn.text()!r}")
    bm_ada = any(b.get("slug") == "bukhari" and b.get("id") == 2
                 for b in w.bookmarks)
    semak("penanda buku ditambah (bukhari#2)", bm_ada,
          f"bookmarks={[(b.get('slug'), b.get('id')) for b in w.bookmarks]}")
    w._save_btn.click()
    semak("klik kedua -> label '☆ Simpan' semula",
          w._save_btn.text() == "☆ Simpan", f"teks={w._save_btn.text()!r}")
    bm_tiada = not any(b.get("slug") == "bukhari" and b.get("id") == 2
                       for b in w.bookmarks)
    semak("penanda buku dibuang (kembali asal)", bm_tiada)
    # Pulihkan penanda buku asal (memori + fail)
    w.bookmarks = asal_bm
    _write_json(BOOKMARKS, asal_bm)
    w.close()
    QTimer.singleShot(100, app.quit)


QTimer.singleShot(100, jalankan)
app.exec_()
print("=" * 60)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 60)
sys.exit(1 if FAIL else 0)
