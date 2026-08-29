#!/usr/bin/env python3
"""Ujian offscreen: tab bahasa 3 (mockup Sesi 55) + teks SAMA PARAS.

Sahkan: (1) TIADA tab "Sebelah" (bandingan) -- 3 tab sahaja
(Melayu/Indonesia/English), keputusan mockup; (2) paparan tunggal =
TAB + teks sahaja (tiada label/butang di bawah tab); (3) teks
terjemahan SAMA PARAS dengan teks Arab di lajur kiri; (4) hadis
panjang kekal separas + skala Arab Kecil.

NOTA: QTimer dalam mod offscreen TIDAK menunggu masa sebenar
(dicetuskan serta-merta), jadi tunggu_sedia() (polling dengan
processEvents) digunakan untuk semua peringkat muatan — konsisten
dengan uji_lompat_fungsi.py, elak flaky semakan sebelum worker/layout
selesai.
"""
import os
import sys
import time
import sqlite3

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer, QEventLoop

app = QApplication(sys.argv)

PASS, FAIL = 0, 0


def semak(nama, ok, butir=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  OK    {nama}")
    else:
        FAIL += 1
        print(f"  GAGAL {nama}  {butir}")


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
    semakan berjalan sebelum worker/layout selesai. Polling dengan
    processEvents sehingga syarat dipenuhi (atau had masa tamat)
    menghilangkan flaky itu.
    """
    t0 = time.monotonic()
    while time.monotonic() - t0 < masa_maks:
        if syarat():
            return True
        app.processEvents()
        time.sleep(selang)
    return False


# Ujian ini menjangka tetapan LALAI (saiz Arab Kecil, ar_idx=0).
# user_settings.json sedia ada mungkin menyimpan nilai lama (cth.
# ar_idx=3 daripada ujian lain) yang menjadikan semakan skala GAGAL
# walaupun kod betul. Sandarkan + pulihkan seperti corak semak.py.
_ASAL_SETTINGS = None
if os.path.exists("user_settings.json"):
    try:
        with open(
                os.path.join(BASE, "user_settings.json"),
                encoding="utf-8") as _fh:
            _ASAL_SETTINGS = _fh.read()
    except OSError:
        _ASAL_SETTINGS = None


def _pulihkan_settings():
    if _ASAL_SETTINGS is not None:
        with open(os.path.join(BASE, "user_settings.json"), "w",
                  encoding="utf-8") as _fh:
            _fh.write(_ASAL_SETTINGS)
    elif os.path.exists(os.path.join(BASE, "user_settings.json")):
        os.remove(os.path.join(BASE, "user_settings.json"))


# Paksa app guna tetapan LALAI semasa ujian (fail sedia ada mungkin
# menyimpan ar_idx=3 daripada ujian lain) -- lalai kod ar=0 (Arab
# Kecil, 0.85). PENTING: tulis semula fail (bukan buang) dengan
# `deklarasi_dibaca: true` -- jika fail tiada, app mencipta semula
# tanpa bendera itu dan dialog deklarasi MODAL muncul, menyekat ujian
# offscreen (gejala "hang" yang pernah direkodkan). Dipulihkan di
# akhir ujian.
with open(os.path.join(BASE, "user_settings.json"), "w",
          encoding="utf-8") as _fh:
    _fh.write('{\n  "deklarasi_dibaca": true,\n'
              '  "theme": "dark",\n  "arabic_font_idx": 0,\n'
              '  "font_scale_idx": 1,\n  "translation_font_idx": 1,\n'
              '  "language_pref": "both",\n  "per_page": 20\n}\n')


from ui.app_qt import PustakaApp
from ui.helpers import _HAD_WA

# Bina hadis ujian dengan kedua-dua bahasa terus dalam DB
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
ada2 = conn.execute(
    "SELECT COUNT(*) FROM hadis WHERE melayu IS NOT NULL AND "
    "indonesia IS NOT NULL AND length(melayu)>50 AND length(indonesia)>50"
).fetchone()[0]
conn.close()

print("Lancarkan PustakaApp (offscreen)...")
w = PustakaApp()
w.resize(1100, 760)
w.show()
# Tunggu data koleksi dimuat (CollectionsWorker async). Polling, bukan
# singleShot tetap — QTimer offscreen tidak menunggu masa sebenar.
tunggu_sedia(lambda: len(w.collections) > 0)

# Cari satu hadis yang ada kedua-dua bahasa
c = sqlite3.connect(os.path.join(BASE, "hadis.db"))
c.row_factory = sqlite3.Row
r = c.execute(
    "SELECT collection, hadis_id, arab, melayu, indonesia FROM hadis "
    "WHERE melayu IS NOT NULL AND indonesia IS NOT NULL AND "
    "length(melayu)>50 AND length(indonesia)>50 LIMIT 1"
).fetchone()
c.close()

if not r:
    print("  GAGAL tiada hadis dengan kedua-dua bahasa dalam DB")
    sys.exit(1)

slug, hid = r["collection"], r["hadis_id"]
h = {
    "collection": slug, "id": hid, "arab": r["arab"],
    "melayu": r["melayu"], "indonesia": r["indonesia"],
    "english": None, "nama_bab": None,
}
print(f"  hadis ujian: {slug}#{hid}")

w.open_detail(h, "home")
# Butiran dibuka secara sinkron oleh open_detail; tunggu_sedia mengunci
# halaman benar-benar di butiran (bukti rantaian, bukan masa tetap).
sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                     and (w._detail_h or {}).get("id") == hid)
semak("halaman butiran dibuka (PAGES['detail'])", sedia,
      f"index={w.stack.currentIndex()}")# 1. Tab bahasa: 3 tab sahaja (keputusan mockup Sesi 55). Tab
#    "Sebelah" (bandingan Melayu vs Indonesia) DIBUANG -- ia bukan
#    dalam mockup, dan teks terjemahan di dalamnya tidak sama paras
#    dengan teks Arab di lajur kiri.
tabs = w._lang_tabs
semak("TIADA tab Sebelah (keputusan mockup)", "sebelah" not in tabs._btns)
semak("3 tab sahaja (Melayu/Indonesia/English)",
      set(tabs._btns) == {"melayu", "indonesia", "english"},
      f"tab={sorted(tabs._btns)}")

# 2. Tab lalai = Melayu; teks terjemahan dipapar dalam paparan tunggal
from PyQt5.QtWidgets import QFrame, QTextBrowser, QPushButton
sedia = tunggu_sedia(lambda: tabs.active() == "melayu")
semak("tab lalai Melayu", sedia, f"aktif={tabs.active()}")
tbs = [x.toPlainText() for x in w._trans_box.findChildren(QTextBrowser)
       if x.toPlainText().strip()]
semak("teks Melayu dipapar dalam paparan tunggal",
      r["melayu"][:20] in (tbs[0] if tbs else ""),
      (tbs[0][:30] if tbs else "tiada"))

# 3. Tukar ke Indonesia -- teks Indonesia dipapar
w._lang_tabs.set_active("indonesia")
sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "indonesia")
semak("tab Indonesia aktif", sedia, f"aktif={w._lang_tabs.active()}")
tbs_i = [x.toPlainText()
         for x in w._trans_box.findChildren(QTextBrowser)
         if x.toPlainText().strip()]
semak("teks Indonesia dipapar",
      r["indonesia"][:20] in (tbs_i[0] if tbs_i else ""),
      (tbs_i[0][:30] if tbs_i else "tiada"))
w._lang_tabs.set_active("melayu")

# 4. Nyahdaya bahasa yang tiada data -- uji LangTabs terus
w._lang_tabs.set_available({"melayu"})
semak("Indonesia nyahdaya bila tiada data",
      not w._lang_tabs._btns["indonesia"].isEnabled())
semak("English nyahdaya bila tiada data",
      not w._lang_tabs._btns["english"].isEnabled())
semak("tab aktif kekal Melayu", w._lang_tabs.active() == "melayu",
      f"aktif={w._lang_tabs.active()}")
w._lang_tabs.set_available({"melayu", "indonesia", "english"})

# 5. TIADA butang "Salin semua bahasa" -- ia milik tab Sebelah yang
#    dibuang; tindakan kekal di bar tajuk + menu klik kanan.
def _butang(teks):
    return [b for b in w._trans_box.findChildren(QPushButton)
            if teks in b.text()]


semak("TIADA butang 'Salin semua bahasa' (tab Sebelah dibuang)",
      not _butang("Salin semua bahasa"))

# 5b. "Kongsi semua bahasa" DIBUANG (Sesi 34) -- kongsi WhatsApp ikut
# bahasa semasa sahaja.
butang_kongsi = _butang("Kongsi semua bahasa")
semak("butang Kongsi semua bahasa dibuang", not butang_kongsi)

# 6. Tab English -- terjemahan Inggeris dipapar dalam paparan tunggal
#    (terjemahan dalam jadual berasingan `terjemahan_eng` -- join
#    melalui collection+hadis_id).
c2 = sqlite3.connect(os.path.join(BASE, "hadis.db"))
c2.row_factory = sqlite3.Row
r_eng = c2.execute(
    "SELECT h.collection, h.hadis_id, h.arab, h.melayu, h.indonesia, "
    "t.english FROM hadis h JOIN terjemahan_eng t "
    "ON t.collection=h.collection AND t.hadis_id=h.hadis_id "
    "WHERE h.melayu IS NOT NULL AND h.indonesia IS NOT NULL "
    "AND length(h.melayu)>50 AND length(h.indonesia)>50 "
    "AND length(t.english)>50 LIMIT 1").fetchone()
c2.close()
if r_eng:
    h3 = {"collection": r_eng["collection"], "id": r_eng["hadis_id"],
          "arab": r_eng["arab"], "melayu": r_eng["melayu"],
          "indonesia": r_eng["indonesia"], "english": r_eng["english"],
          "nama_bab": None}
    w.open_detail(h3, "home")
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == r_eng["hadis_id"])
    semak("halaman butiran (english) dibuka", sedia,
          f"index={w.stack.currentIndex()}")
    w._lang_tabs.set_active("english")
    sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "english")
    semak("tab English aktif", sedia, f"aktif={w._lang_tabs.active()}")
    tbs3 = [x.toPlainText()
            for x in w._trans_box.findChildren(QTextBrowser)
            if x.toPlainText().strip()]
    semak("teks English dipapar dalam paparan tunggal",
          any(r_eng["english"][:20] in t for t in tbs3),
          f"jumpa {len(tbs3)} browser")
else:
    print("  [skip] tiada hadis dengan english dalam DB")

# 7. Paparan bahasa tunggal = TAB + teks sahaja (keputusan mockup Sesi 55).
#    Label 'BAHASA MELAYU' dan butang Salin/Kongsi di bawah tab TIDAK
#    wujud -- ia menolak teks terjemahan ke bawah sehingga tidak sama
#    paras dengan teks Arab. Tindakan kekal di bar tajuk (Kongsi =
#    WhatsApp bahasa semasa, Salin) dan menu klik kanan.
w._lang_tabs.set_active("melayu")
sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "melayu")
semak("tab Melayu aktif", sedia, f"aktif={w._lang_tabs.active()}")
semak("TIADA label 'BAHASA ...' di bawah tab (keputusan mockup)",
      not any(lb.text().startswith("BAHASA ")
              for lb in w._trans_box.findChildren(QLabel)))
semak("TIADA butang '💬 Kongsi' di bawah tab (kongsi di bar tajuk)",
      not _butang("💬 Kongsi"))

# 7d. Bar tindakan bawah TERJEMAHAN sebagai TEKS (bukan butang) --
#    tiru sunnah.com 'Report Error | Share | Copy'. Keputusan pengguna
#    (13 Ogos, diulang): "saya mahu text sahaja bukan button" + menu
#    Salin 3 pilihan MESTI berfungsi. Bar = QLabel pautan teks, BUKAN
#    QPushButton.
_butang_semua = [b.text() for b in w.findChildren(QPushButton)]
semak("bar tindakan TEKS 'Lapor ralat | Kongsi | Salin' di bawah terjemahan",
      any("Lapor ralat" in lb.text() and "Kongsi" in lb.text()
          and "Salin" in lb.text() and "|" in lb.text()
          for lb in w.findChildren(QLabel)),
      "cari QLabel barTindakan")
semak("bar tindakan BUKAN butang (tiada QPushButton Lapor/Kongsi/Salin)",
      not any(b.text() in ("Lapor ralat", "Kongsi", "Salin")
              for b in w.findChildren(QPushButton)))
# Menu Salin -- 3 pilihan dibina (ujian unit tanpa exec) DAN _salin_ke
# benar-benar menyalin ke papan klip (fungsi, bukan label sahaja).
aksi = []
class _MenuMahu:
    def __init__(self, parent=None): pass
    def addAction(self, teks, fn=None): aksi.append((teks, fn))
    def exec_(self, pos): pass
from unittest.mock import patch
with patch("ui.pages_detail.QMenu", _MenuMahu):
    w._menu_salin()
semak("menu Salin ada 3 pilihan (Arab/terjemahan/Arab+terjemahan)",
      len(aksi) == 3 and "Salin Arab sahaja" in aksi[0][0]
      and "Salin terjemahan" in aksi[1][0]
      and "Salin Arab + terjemahan semasa" in aksi[2][0],
      f"aksi={[a[0] for a in aksi]}")
QApplication.clipboard().setText("")
w._salin_ke("teks ujian salin", "mesej")
semak("_salin_ke menyalin ke papan klip (berfungsi)",
      QApplication.clipboard().text() == "teks ujian salin",
      f"klip={QApplication.clipboard().text()!r}")
# Pilihan ke-3: Arab + terjemahan bahasa SEMASA (tanpa rujukan).
QApplication.clipboard().setText("")
w._lang_tabs.set_active("indonesia")
tunggu_sedia(lambda: w._lang_tabs.active() == "indonesia")
w._salin_arab_terjemahan()
klip3 = QApplication.clipboard().text()
klip_ok3 = (r["arab"].strip() in klip3
            and "No." not in klip3.splitlines()[0]
            and (r["indonesia"] or "").strip() in klip3)
semak("pilihan ke-3 salin Arab + terjemahan semasa (Indonesia)",
      klip_ok3, f"klip3={klip3[:60]!r}")
# Pulihkan tab Melayu (semakan seterusnya menjangka bahasa semasa = Melayu).
w._lang_tabs.set_active("melayu")
tunggu_sedia(lambda: w._lang_tabs.active() == "melayu")

# 7e. Transliterasi: panel dijajarkan ke ATAS (keputusan pengguna 13
#    Ogos: "transliterasi jgn center vertical. top vertical.") --
#    elak Qt memusatkan panel dalam lajur yang lebih tinggi. Model
#    transliterasi (torch) TIDAK dimuat -- mock sahaja, supaya ujian
#    deterministik dan cepat.
import core.phase2_transliterasi as _pt
_pt.transliterate_arabic = lambda arab: {
    "rumi_malay_style": "haddathana al-humaydiyyu",
    "rumi": "ḥaddathanā al-ḥumaydiyyu"}
w._set_arab_tab("transliterasi")
sedia = tunggu_sedia(lambda: w._translit_dibina and any(
    "haddathana" in tb.toPlainText()
    for tb in w.findChildren(QTextBrowser)))
semak("transliterasi dibina (mock)", sedia,
      "model transliterasi tidak dimuat")
_pag = w._ar_stack.currentWidget()
_pan = next((f for f in _pag.findChildren(QFrame)
             if f.objectName() == "panel"), None)
if _pan is not None:
    _y = _pan.mapTo(_pag, _pan.rect().topLeft()).y()
    semak("panel transliterasi di ATAS lajur (bukan pusat menegak)",
          _y <= 30, f"y={_y}")
else:
    semak("panel transliterasi di ATAS lajur (bukan pusat menegak)",
          False, "panel tiada")
w._set_arab_tab("arab")   # pulihkan tab Arab (semakan paras seterusnya)
# Fungsi _teks_bahasa_semasa kekal (diguna bar tajuk Kongsi/WhatsApp).
teks1 = w._teks_bahasa_semasa()
semak("_teks_bahasa_semasa ada label [TERJEMAHAN]",
      "[TERJEMAHAN]" in teks1, teks1[:40])
semak("_teks_bahasa_semasa ada petikan Arab (tanpa label [ARAB])",
      "[ARAB]" not in teks1 and r["arab"][:20] in teks1, teks1[:40])
semak("mesej sertakan Arab PENUH (tiada teks 'Read more' literal)",
      r["arab"].strip() in teks1 and "Read more" not in teks1,
      teks1[:60])
semak("_teks_bahasa_semasa ada teks Melayu",
      r["melayu"][:20] in teks1, teks1[:40])
# Paras: teks Arab dan terjemahan MESTI sama paras (keputusan mockup).
tb_arab = w._ar_stack.currentWidget()
tb_tr = next((tb for tb in w._trans_box.findChildren(QTextBrowser)
              if tb.toPlainText().strip()), None)
if tb_arab is not None and tb_tr is not None:
    a = tb_arab.mapTo(w, tb_arab.rect().topLeft()).y()
    t = tb_tr.mapTo(w, tb_tr.rect().topLeft()).y()
    semak("paras teks Arab == paras terjemahan (beza < 40px)",
          abs(a - t) < 40, f"arab@{a} terjemahan@{t}")
else:
    semak("paras teks Arab == paras terjemahan", False,
          "browser arab/terjemahan tidak dijumpai")
semak("had aksara bahasa semasa (untuk WhatsApp)",
      len(w._teks_bahasa_semasa(had=_HAD_WA)) <= _HAD_WA + 1)
if r_eng:
    w._lang_tabs.set_active("english")
    sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "english")
    semak("tab English aktif", sedia, f"aktif={w._lang_tabs.active()}")
    teks_eng = w._teks_bahasa_semasa()
    semak("_teks_bahasa_semasa ikut tab English (label [TERJEMAHAN])",
          "[TERJEMAHAN]" in teks_eng and "[ENGLISH]" not in teks_eng
          and r_eng["english"][:20] in teks_eng, teks_eng[:40])

# 7c. Kongsi WhatsApp TERUS guna format "Ringkas" (Sesi 36 -- keputusan
# pengguna: TIADA menu pilihan). Kedua-dua Arab + terjemahan kelihatan,
# dengan pautan "Baca penuh" sunnah.com.
w._lang_tabs.set_active("melayu")
sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "melayu")
semak("tab Melayu aktif sebelum kongsi Ringkas", sedia)
teks_ringkas = w._teks_kongsi_ringkas()
semak("kongsi Ringkas: petikan Arab + [TERJEMAHAN], tiada 'Read more' literal",
      "[TERJEMAHAN]" in teks_ringkas and r["arab"][:20] in teks_ringkas
      and "Read more" not in teks_ringkas, teks_ringkas[:40])
semak("kongsi Ringkas ada pautan 'Baca penuh' sunnah.com",
      "Baca penuh: https://sunnah.com/" in teks_ringkas, teks_ringkas[-90:])

# 8. Carian KHUSUS (kitab + nombor) -> TERUS ke butiran, bukan senarai
#    (Sesi 38). "bukhari 500" bukan carian umum -- pengguna mahukan
#    hadis itu; detail page dibuka terus. Muatan melalui open_by_ref
#    (worker async) — tunggu_sedia sehingga butiran No. 500 dibuka.
w.search_bar.input.setText("bukhari 500")
w._hantar_carian()
sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                     and (w._detail_h or {}).get("id") == 500)
semak("carian 'bukhari 500' terus ke halaman butiran", sedia,
      f"index={w.stack.currentIndex()}, hid={(w._detail_h or {}).get('id')}")
semak("carian 'bukhari 500' bukan senarai kitab",
      w.stack.currentIndex() != 1, f"index={w.stack.currentIndex()}")
semak("kad yang dibuka ialah No. 500",
      getattr(w, "_detail_hid", None) == 500 or
      (w.stack.currentIndex() == 2 and
       w._detail_from == "search"), f"hid={getattr(w, '_detail_hid', None)}")

# 8c. Toast maklum balas "Membuka…" pada carian khusus (Sesi 38):
#    dipapar SEGERA (sinkron dalam _buka_hadis_terus) dengan teks
#    betul, sebelum muatan async selesai. NOTA: QTimer dalam mod
#    offscreen TIDAK menunggu masa sebenar (dipercepatkan), jadi
#    tempoh minimum 1800ms tidak boleh diuji di sini -- semak
#    mekanismenya secara unit (ms=0 -> tiada auto-hide timer).
w.search_bar.input.setText("bukhari 500")
w._hantar_carian()
semak("toast 'Membuka' dipapar sejurus selepas carian khusus",
      w.toast.isVisible() and "📖 Membuka" in w.toast.text(),
      f"visible={w.toast.isVisible()}, teks={w.toast.text()!r}")
semak("toast 'Membuka' ada nama kitab + nombor",
      "Sahih al-Bukhari No. 500" in w.toast.text(),
      f"teks={w.toast.text()!r}")
semak("masa mula toast dicatat (jaminan minimum 1800ms)",
      getattr(w, "_buka_toast_t0", None) is not None)
# Unit: show_msg ms=0 tidak menjadualkan auto-hide (kekal sehingga
# hide() eksplisit); ms>0 menjadualkan timer yang DIBATALKAN apabila
# toast baharu dipapar (pepijat timer lama menutup toast baharu).
semak("toast ms=0 tiada auto-hide timer", w.toast._hide_timer is None)
w.toast.show_msg("uji", 5000)
semak("toast ms>0 ada auto-hide timer", w.toast._hide_timer is not None)
w.toast.show_msg("ganti", 0)
semak("toast baharu batalkan timer lama", w.toast._hide_timer is None)

# 8b. Carian UMUM kekal senarai hasil (bukan detail). Enjin kata kunci
#    async (SearchWorker) — polling sehingga hasil diterima.
w.search_bar.input.setText("hukum riba")
w._hantar_carian()
sedia = tunggu_sedia(lambda: w._search_q == "hukum riba"
                     and w._kw_res is not None, masa_maks=15.0)
semak("carian umum: enjin kata kunci selesai", sedia,
      f"_kw_res={w._kw_res}")
semak("carian umum 'hukum riba' ke halaman carian (senarai hasil)",
      w.stack.currentIndex() == 0 or
      (w._search_q == "hukum riba"),
      f"index={w.stack.currentIndex()}, _search_q={getattr(w, '_search_q', None)}")

# 8d. Teks Arab Kecil (Sesi 55 lanjutan): pada HADIS PANJANG, lajur
#    terjemahan mesti kekal sama paras dengan teks Arab (top-aligned),
#    dan skala Arab ialah Kecil (0.85) -- bukan Sederhana (1.0).
c3 = sqlite3.connect(os.path.join(BASE, "hadis.db"))
rp = c3.execute(
    "SELECT collection, hadis_id, arab, melayu FROM hadis "
    "WHERE length(arab)>1500 AND length(melayu)>1500 LIMIT 1").fetchone()
c3.close()
if rp:
    hp = {"collection": rp[0], "id": rp[1], "arab": rp[2],
          "melayu": rp[3], "indonesia": "", "english": "",
          "nama_bab": None}
    w.open_detail(hp, "home")
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == hp["id"])
    semak("hadis panjang dibuka", sedia,
          f"index={w.stack.currentIndex()}")
    semak("hadis panjang: skala Arab Kecil (0.85)",
          w.ar_idx == 0 and w.ar_scale == 0.85,
          f"ar_idx={w.ar_idx} skala={w.ar_scale}")
    tb_ar_p = w._ar_stack.currentWidget()
    tb_tr_p = next((tb for tb in w._trans_box.findChildren(QTextBrowser)
                    if tb.toPlainText().strip()), None)
    if tb_ar_p is not None and tb_tr_p is not None:
        a2 = tb_ar_p.mapTo(w, tb_ar_p.rect().topLeft()).y()
        t2 = tb_tr_p.mapTo(w, tb_tr_p.rect().topLeft()).y()
        semak("hadis panjang: paras Arab == paras terjemahan (beza < 40px)",
              abs(a2 - t2) < 40, f"arab@{a2} terjemahan@{t2}")
    else:
        semak("hadis panjang: browser Arab/terjemahan dijumpai", False)
    teks_melayu_p = (w._detail_h.get("melayu") or "").strip()
    semak("hadis panjang: teks Melayu penuh dipapar",
          teks_melayu_p[:20] in
          (tb_tr_p.toPlainText() if tb_tr_p is not None else ""),
          teks_melayu_p[:20])
else:
    print("  [skip] tiada hadis panjang (>1500 aksara) dalam DB")

# 8e. ARAB JAUH LEBIH PANJANG daripada terjemahan (kes centering Qt,
#     Sesi 55): bila lajur Arab lebih tinggi, ruang menegak berlebihan
#     dalam kotak terjemahan MESTI tinggal DI BAWAH teks, bukan
#     memusatkannya -- tanpa AlignTop + addStretch, Qt memusatkan teks
#     terjemahan ke tengah (tidak sama paras dengan Arab). Ukur
#     KEDUA-DUA top dalam langkah yang SAMA (panel bergerak bersama).
c4 = sqlite3.connect(os.path.join(BASE, "hadis.db"))
rq = c4.execute(
    "SELECT collection, hadis_id, arab, melayu, indonesia FROM hadis "
    "WHERE melayu IS NOT NULL AND length(melayu)>100 "
    "AND length(arab) > 3*length(melayu) "
    "AND length(arab) > 1500 LIMIT 1").fetchone()
c4.close()
if rq:
    hq = {"collection": rq[0], "id": rq[1], "arab": rq[2],
          "melayu": rq[3], "indonesia": rq[4] or "",
          "english": "", "nama_bab": None}
    w.open_detail(hq, "home")
    sedia = tunggu_sedia(lambda: w.stack.currentIndex() == 2
                         and (w._detail_h or {}).get("id") == hq["id"])
    semak("hadis arab>>terjemahan dibuka", sedia,
          f"index={w.stack.currentIndex()}")

    def ukur_paras(tag):
        ar = w._ar_stack.currentWidget()
        tr = next((tb for tb in w._trans_box.findChildren(QTextBrowser)
                   if tb.toPlainText().strip()), None)
        if ar is None or tr is None:
            semak(f"{tag}: browser Arab/terjemahan dijumpai", False)
            return
        a = ar.mapTo(w, ar.rect().topLeft()).y()
        t = tr.mapTo(w, tr.rect().topLeft()).y()
        semak(f"{tag}: paras Arab == paras terjemahan (beza < 40px)",
              abs(a - t) < 40, f"arab@{a} terjemahan@{t}")

    ukur_paras("arab>>terjemahan (melayu lalai)")
    w._lang_tabs.set_active("indonesia")
    sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "indonesia")
    ukur_paras("arab>>terjemahan (indonesia)")
    w._lang_tabs.set_active("melayu")
    sedia = tunggu_sedia(lambda: w._lang_tabs.active() == "melayu")
    ukur_paras("arab>>terjemahan (kembali melayu)")
else:
    print("  [skip] tiada hadis dengan arab >> melayu dalam DB")

w.close()
_pulihkan_settings()
print(f"\n  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 60)
sys.exit(0 if FAIL == 0 else 1)
