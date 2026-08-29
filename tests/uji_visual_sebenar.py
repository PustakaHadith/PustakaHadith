#!/usr/bin/env python3
"""Pengesahan VISUAL SEBENAR — aplikasi dipaparkan pada skrin Windows.

Lancarkan `PustakaApp` (sama seperti main.py) TANPA offscreen supaya
tetingkap benar-benar dipaparkan. Buka hadis yang tiada SemakHadis
tetapi ada sandaran HadeethEnc, dan ambil tangkapan skrin FIZIKAL
(ImageGrab) untuk kedua-dua tema — teks sebenar kelihatan. Juga
sahkan simbol selawat ﷺ (lalai sejak Sesi 32) menggantikan frasa
"Sallallahu 'alaihi wasallam" dalam paparan Melayu pada skrin, dan
sahkan ketiga-tiga saiz fon lalai "Sederhana" (Sesi 33) — antara
muka, Arab, terjemahan (skala 1.0) — pada kod, app, dan skrin.
Sesi 34 pula: butang ↑ terapung + kotak carian nombor hadis pada
halaman senarai kitab DAN halaman Carian, serta ketiadaan kotak
"Pergi" pada pager — sumber, kelakuan app, dan skrin fizikal.
Simbol selawat ﷺ turut disahkan dalam transliterasi rumi (gaya
Melayu + akademik) DAN bentuk Arab "صلى الله عليه وسلم" yang
tertanam dalam teks Melayu — sumber regex + kelakuan app + skrin
fizikal.

    python uji_visual_sebenar.py

Tangkapan skrin: `bukti_visual/sebenar_*.png`
"""

import os
import re
import sqlite3
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QTextBrowser
from PyQt5.QtCore import QTimer, QEventLoop
from PIL import ImageGrab
import win32gui

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


_MD5_SKIN_SEBELUMNYA = [None]


def skrin_fizikal(tag: str) -> str:
    """Tangkap skrin fizikal; pulangkan laluan fail + semak variasi."""
    # Beri masa Qt melukis ke skrin, bawa tetingkap ke hadapan, dan
    # tangkap BBOX TETINGKAP (bukan skrin penuh) supaya semakan tema
    # mengukur kandungan app, bukan permukaan lain yang menutupnya.
    # Konsisten dengan ujian visual lain (bandingan/carian/kiraan/ralat).
    #
    # BINGKAI BASI (persekitaran): ImageGrab kadang-kadang pulangkan
    # imej SAMA dengan tangkapan sebelumnya walaupun UI berubah (cth.
    # tukar tema terang/gelap atau buka hadis lain) -- pernah membuat
    # 7 tangkapan dalam satu larian byte-identik. Paksa repaint + ulang
    # tangkapan sehingga imej berbeza daripada tangkapan sebelumnya
    # (atau had percubaan), supaya semakan kecerahan/tema benar-benar
    # mengukur kandungan semasa.
    import hashlib

    def _kecilkan(im):
        # Variasi warna (teks = banyak warna)
        kecil = im.resize((320, 200))
        # getdata() deprecated sejak Pillow 12 (dibuang Pillow 14) -- guna
        # get_flattened_data() dengan fallback untuk Pillow lama.
        pix = getattr(kecil, "get_flattened_data", kecil.getdata)()
        return pix

    import win32con

    def _paksa_hadapan(hwnd):
        """Paksa tetingkap ke hadapan TANPA kunci fokus Windows.

        Bila ujian dijalankan sebagai SUBPROSES (cth. uji_pra_hantar.py),
        proses itu bukan proses aktif, jadi SetForegroundWindow ditolak
        dan tetingkap app kekal di belakang terminal -- ImageGrab lalu
        menangkap permukaan salah (kecerahan tema lain). HWND_TOPMOST
        memaksa tetingkap ke atas tanpa kebenaran fokus, dan Topmost
        sementara dinyahselepas tangkapan supaya tidak kekal di atas.
        """
        try:
            # Pulihkan dahulu -- Windows kadangkala meminimumkan
            # tetingkap latar belakang (GetWindowRect lalu pulangkan
            # ikon taskbar ~160x28 dan tangkapan jadi 93 B pepejal).
            # SW_RESTORE membatalkan keadaan iconic sebelum tangkapan.
            # Corak sama dengan uji_visual_mockup (flak z-order
            # subproses).
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                                  0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                                  | win32con.SWP_SHOWWINDOW)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.BringWindowToTop(hwnd)
            time.sleep(0.3)
        except Exception:
            pass

    app.processEvents()
    time.sleep(0.2)
    hwnd = int(w.winId())
    # GetWindowRect dikira SEMULA dalam gelung cubaan (selepas
    # _paksa_hadapan yang melakukan SW_RESTORE) -- jika tetingkap
    # diminimumkan, rect pertama ialah ikon taskbar (~160x28) dan
    # tangkapan jadi 93 B pepejal walau 10 cubaan.
    _paksa_hadapan(hwnd)
    kiri, atas, kanan, bawah = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
    # Tema sebenar app -- kecerahan tangkapan MESTI sepadan, dan halaman
    # MESTI cukup terisi (warna unik >= 150 = kandungan dilukis penuh).
    # Jika tidak, tangkapan itu bingkai basi (persekitaran) atau halaman
    # separuh dilukis, dan perlu diulang.
    gelap = str(w.settings.get("theme", "neutral")).lower() in ("dark", "neutral")
    for _cuba in range(10):
        pix = _kecilkan(img)
        cerah = sum(sum(px[:3]) / 3 for px in pix) / (320 * 200)
        warna = set()
        for px in pix:
            warna.add((px[0] >> 4, px[1] >> 4, px[2] >> 4))
        md5 = hashlib.md5(img.tobytes()).hexdigest()
        padan = (cerah < 100) if gelap else (cerah > 140)
        cukup = len(warna) >= 150
        beza = _MD5_SKIN_SEBELUMNYA[0] is None or md5 != _MD5_SKIN_SEBELUMNYA[0]
        if padan and cukup and beza:
            break
        # Bingkai basi / belum dilukis -- paksa Windows mengecat semula.
        # repaint() sahaja TIDAK cukup pada sesetengah mesin; show/hide
        # semula memaksa redraw penuh. (Flak permulaan: tetingkap baharu
        # kadang-kadang belum dilukis bila tangkapan pertama berlaku.)
        w.repaint()
        app.processEvents()
        # Semakin banyak cubaan gagal, semakin kuat paksaan: repaint ->
        # hide/show -> TOPMOST (flak fokus subproses bila ujian berjalan
        # berturutan pantas).
        if _cuba == 3:
            w.hide()
            app.processEvents()
            time.sleep(0.3)
            w.show()
            w.raise_()
            w.activateWindow()
        _paksa_hadapan(hwnd)
        # Kira semula rect selepas SW_RESTORE/TOPMOST -- tetingkap yang
        # diminimumkan memberi rect ikon taskbar pada cubaan awal.
        kiri, atas, kanan, bawah = win32gui.GetWindowRect(hwnd)
        # POLL adaptif: grab berulang selang 0.15s sehingga bingkai
        # STABIL (dua grab berturut-turut sama) atau 0.6s tamat. Fix
        # 0.6s membazir ~0.45s setiap cubaan bila paparan kemas kini
        # cepat; poll memecah awal tanpa mengorbankan flak lambat.
        # (Diukur 17 Ogos: 58 tangkapan / 11 panggilan = ~5 cubaan/
        # panggilan pada paparan RDP -- bahagian berubah 172s vs 143s.
        # Elak fast-path t=0: grab pertama mungkin separa dilukis
        # selepas repaint/hide-show -- mesti disahkan stabil oleh grab
        # kedua sebelum disimpan.)
        t_habis = time.time() + 0.6
        img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
        while time.time() < t_habis:
            time.sleep(0.15)
            img_baru = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
            sama = img_baru.tobytes() == img.tobytes()
            img = img_baru
            if sama:
                break
    _MD5_SKIN_SEBELUMNYA[0] = md5
    pix = _kecilkan(img)
    nama = f"sebenar_{tag}.png"
    laluan = os.path.join(BUKTI, nama)
    img.save(laluan)
    saiz = os.path.getsize(laluan)
    warna = set()
    for px in pix:
        warna.add((px[0] >> 4, px[1] >> 4, px[2] >> 4))
    print(f"      -> {nama}  ({saiz} B, kecerahan {cerah:.0f}, "
          f"warna unik {len(warna)})")
    return laluan, saiz, cerah, len(warna)


# ── 1. Cari hadis TANPA SemakHadis TETAPI ADA HadeethEnc ────────────
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
calon = conn.execute("""
    SELECT h.collection, h.hadis_id, he.he_id
    FROM hadis h
    JOIN hadethenc he ON he.collection=h.collection AND he.hadis_id=h.hadis_id
    LEFT JOIN semakhadis s ON s.collection=h.collection AND s.hadis_id=h.hadis_id
    WHERE s.hadis_id IS NULL AND h.arab <> ''
    ORDER BY RANDOM() LIMIT 2
""").fetchall()
conn.close()

print("=" * 62)
print("  UJIAN VISUAL SEBENAR — SANDRAN HADEETHENC")
print("=" * 62)
semak("Cukup calon hadis tanpa sema + ada HE", len(calon) >= 1,
      f"jumpa {len(calon)}")
if not calon:
    sys.exit(1)

# ── 2. Lancarkan aplikasi SEBENAR (tetingkap dipaparkan) ────────────
print("\n  Lancarkan PustakaApp pada skrin sebenar...")
from ui.app_qt import PustakaApp
w = PustakaApp()
w.show()
w.raise_()
w.activateWindow()
tunggu(2500)
semak("Koleksi dimuat (9 kitab)", len(w.collections) == 9,
      f"jumpa {len(w.collections)}")

from ui.widgets import Collapsible


def buka_dan_skrin(slug, hid, tag):
    """Buka hadis, sahkan sandaran HE, tangkap skrin fizikal."""
    h = w.api.get_hadis_by_id(slug, hid)
    h["collection"] = slug
    w.open_detail(h, "home")
    tunggu(1200)

    dh = w._detail_h or {}
    he = dh.get("he") or {}
    sema = dh.get("sema") or {}
    print(f"\n  [{tag}] {slug} #{hid} — "
          f"sema={'ADA' if sema else 'tiada'}  "
          f"he={'ADA' if he else 'TIADA'}  (he_id={he.get('he_id')})")
    semak(f"{tag}: sema tiada (kes sandaran)", not sema)
    semak(f"{tag}: huraian HadeethEnc ada",
          bool(he and (he.get("hadeeth") or he.get("explanation"))))

    kol_he = None
    for col_w in w.findChildren(Collapsible):
        t = getattr(col_w, "_tajuk", "") or ""
        if "HadeethEnc" in t:
            kol_he = col_w
            break
    semak(f"{tag}: Collapsible HadeethEnc dipapar", kol_he is not None)

    if kol_he is not None and not getattr(kol_he, "_dibina", False):
        kol_he._toggle()
        tunggu(400)
        # Kembali ke atas supaya panel HE kelihatan dalam skrin
        w._detail_sa.verticalScrollBar().setValue(0)
        tunggu(400)

    # Skrin fizikal (teks sebenar!)
    laluan, saiz, cerah, unik = skrin_fizikal(tag)
    semak(f"{tag}: tangkapan skrin sebenar disimpan", saiz > 30000,
          f"saiz {saiz}")
    semak(f"{tag}: teks kelihatan ({unik} warna unik)", unik > 40,
          f"warna unik {unik}")
    if tag.startswith("gelap"):
        semak(f"{tag}: tema gelap (kecerahan < 100)", cerah < 100,
              f"{cerah:.0f}")
    else:
        semak(f"{tag}: tema terang (kecerahan > 140)", cerah > 140,
              f"{cerah:.0f}")


# ── 3. Tema gelap ───────────────────────────────────────────────────
print("\n  ── TEMA GELAP ──")
r = calon[0]
buka_dan_skrin(r["collection"], r["hadis_id"], "gelap")

# Skrol sedikit untuk lihat panel huraian dalam skrin
w._detail_sa.verticalScrollBar().setValue(300)
tunggu(500)
skrin_fizikal("gelap_skrol")

# ── 4. Tema terang ──────────────────────────────────────────────────
print("\n  ── TEMA TERANG ──")
w.set_theme("light")
tunggu(1500)
w._detail_sa.verticalScrollBar().setValue(0)
tunggu(500)
r = calon[1] if len(calon) > 1 else calon[0]
buka_dan_skrin(r["collection"], r["hadis_id"], "terang")
w._detail_sa.verticalScrollBar().setValue(300)
tunggu(500)
skrin_fizikal("terang_skrol")

# ── 5. Kembali ke gelap ─────────────────────────────────────────────
w.set_theme("dark")
tunggu(600)

# ── 6. Simbol selawat ﷺ (lalai) ─────────────────────────────────────
# Sesi 32: `simbol_selawat` kini lalai True -- paparan Melayu mengganti
# frasa "Sallallahu 'alaihi wasallam" dengan ligatur U+FDFA ﷺ. Semakan
# ini mengesan regresi lalai (dikembalikan ke False) atau frasa yang
# tidak diganti pada skrin sebenar.
print("\n  ── SIMBOL SELAWAT ﷺ ──")

def _norm_arab(s):
    # Buang tashkeel (diakritik Arab) supaya carian frasa teguh -- teks
    # DB guna "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ" (dengan diakritik).
    return re.sub(r"[\u064B-\u065F\u0670]", "", s or "")


conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
calon_sel = conn.execute("""
    SELECT collection, hadis_id, melayu, arab FROM hadis
    WHERE melayu LIKE '%allallahu%' AND melayu LIKE '%alaihi%'
    ORDER BY RANDOM() LIMIT 60
""").fetchall()
conn.close()
# Pilih hadis yang teks Arabnya TULIS selawat penuh -- diperlukan oleh
# semakan transliterasi rumi di bawah (transliterasi ialah terjemahan
# teks Arab, bukan teks Melayu).
sel = next((r for r in calon_sel
           if "صلى الله عليه وسلم" in _norm_arab(r["arab"])), None)
semak("Hadis dengan frasa selawat dijumpai", sel is not None)
if sel is None:
    sys.exit(1)

# Uji lalai melalui kelakuan SEBENAR `_papar_melayu` -- bukan fallback
# settings (yang kosong pada mesin tanpa user_settings.json). Kalau
# sesiapa mengembalikan lalai ke False dalam pages_detail.py, frasa
# ini kekal rumi dan semakan GAGAL.
lalai_t = w._papar_melayu("Rasulullah Sallallahu 'alaihi wasallam bersabda")
semak("lalai simbol_selawat = True (frasa diganti oleh _papar_melayu)",
      "\ufdfa" in lalai_t)
semak("glif ﷺ tersedia dalam fon sistem", bool(w._ada_glif_selawat))

h = w.api.get_hadis_by_id(sel["collection"], sel["hadis_id"])
h["collection"] = sel["collection"]
w.open_detail(h, "home")
tunggu(1500)

ada = False
for tb in w.findChildren(QTextBrowser):
    if "\ufdfa" in tb.toPlainText():
        ada = True
        break
semak("teks dipapar mengandungi ﷺ (widget UI)", ada)

# Skrin fizikal bukti (tema gelap)
laluan, saiz, cerah, unik = skrin_fizikal("selawat")
semak("skrin selawat disimpan", saiz > 30000, f"saiz {saiz}")

# ── 6b. Transliterasi rumi juga guna ﷺ ─────────────────────────────
# Sesi 34 lanjutan: selawat dalam transliterasi rumi (gaya Melayu
# "salla Allahu 'alayhi wa-sallama" + akademik "ṣallā Allāhu ʿalayhi
# wasallama") turut diganti dengan ligatur ﷺ bila simbol_selawat
# aktif -- konsisten dengan paparan Melayu. Semakan sumber + kelakuan
# app + skrin fizikal mengesan regresi (pembuangan guna_simbol_selawat
# dalam _bina_translit, atau regex yang tidak lagi terima bentuk
# sebenar output transliterasi).
print("\n  ── TRANSLITERASI RUMI + ﷺ ──")

# Sumber pages_detail.py -- pengawal regresi bebas daripada state app
src_detail = open(os.path.join(BASE, "ui", "pages_detail.py"),
                  encoding="utf-8").read()
m_tr = re.search(r"def _bina_translit.*?(?=\n    def )", src_detail, re.S)
blok = m_tr.group(0) if m_tr else ""
semak("sumber: _bina_translit guna guna_simbol_selawat + gating",
      "guna_simbol_selawat(teks)" in blok
      and 'settings.get("simbol_selawat", True)' in blok
      and "_ada_glif_selawat" in blok)

# Sumber utils/bahasa.py -- regex mesti terima bentuk KES penuh
# (damma "u" pada Allāhu + fatha "a" pada sallama), bukan hanya
# bentuk pausal. Ini pengawal punca regresi sebenar.
src_bahasa = open(os.path.join(BASE, "utils", "bahasa.py"),
                  encoding="utf-8").read()
semak("sumber bahasa.py: regex selawat rumi terima bentuk kes "
      "(All[āa]h[u]? + sallam[a]?)",
      "[Aa]ll[āa]h[u]?" in src_bahasa and "sallam[a]?" in src_bahasa)

# Kelakuan app -- pilih tab TRANSLITERASI dalam lajur Arab (keputusan
# Sesi 55: transliterasi bukan lagi Collapsible berasingan, ia tab dalam
# lajur Arab). Kandungan dibina MALAS; pilih tab dahulu, kemudian baca
# teks rumi dari halaman stack transliterasi.
semak("tab TRANSLITERASI dalam lajur Arab wujud",
      getattr(w, "_btn_translit", None) is not None)

if getattr(w, "_btn_translit", None) is not None:
    w._set_arab_tab("transliterasi")
    tunggu(800)
    tb_rumi = [tb for tb in w._translit_page.findChildren(QTextBrowser)
               if tb.toPlainText().strip()]
    rumi = "\n".join(tb.toPlainText() for tb in tb_rumi)
    semak("rumi dibina (2 gaya: Melayu + akademik)",
          len(tb_rumi) >= 2, f"browser={len(tb_rumi)}")
    semak("rumi mengandungi ﷺ (ligatur selawat)", "\ufdfa" in rumi)
    semak("rumi TIADA frasa selawat penuh (salla/ṣallā Allāh)",
          not re.search(r"[sṣ]all[āa]?\s+[Aa]ll[āa]h", rumi))
    # Skrin fizikal bukti: skrol tab transliterasi ke dalam pandangan
    w._detail_sa.ensureWidgetVisible(w._translit_page)
    tunggu(400)
    laluan, saiz, cerah, unik = skrin_fizikal("translit_selawat")
    semak("skrin transliterasi disimpan", saiz > 30000, f"saiz {saiz}")

# ── 6c. Selawat Arab "صلى الله عليه وسلم" dalam teks Melayu ────────
# Sesi 34 lanjutan: 9,733 baris hadis.melayu tertanam selawat dalam
# teks ARAB penuh -- regex sebelum ini hanya Latin, jadi bentuk Arab
# kekal penuh walaupun rumi di sebelahnya ditukar ﷺ. Kini alternatif
# Arab ditambah; semakan sumber + kelakuan mengunci regresi.
print("\n  ── SELAWAT ARAB + ﷺ ──")

semak("sumber bahasa.py: regex ada alternatif Arab (صلى الله عليه وسلم)",
      "ص[\\u064B-\\u065F\\u0670]*ل" in src_bahasa
      and "س[\\u064B-\\u065F\\u0670]*س?" in src_bahasa)

conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
ar_sel = conn.execute("""
    SELECT collection, hadis_id, melayu FROM hadis
    WHERE melayu LIKE '%صلى الله عليه وسلم%'
    ORDER BY RANDOM() LIMIT 1
""").fetchone()
conn.close()
semak("hadis dengan selawat Arab dijumpai", ar_sel is not None)
if ar_sel is not None:
    # Fungsi penukaran pada DATA SEBENAR (bukan contoh binaan)
    t = w._papar_melayu(ar_sel["melayu"])
    semak("selawat Arab ditukar oleh _papar_melayu (data sebenar)",
          "\ufdfa" in t and "صلى الله عليه وسلم" not in t)
    # Paparan UI sebenar -- buka hadis dan semak browser terjemahan
    h = w.api.get_hadis_by_id(ar_sel["collection"], ar_sel["hadis_id"])
    h["collection"] = ar_sel["collection"]
    w.open_detail(h, "home")
    tunggu(1200)
    ada = False
    for tb in w._trans_box.findChildren(QTextBrowser):
        if "\ufdfa" in tb.toPlainText():
            ada = True
            break
    semak("UI papar ﷺ untuk hadis selawat Arab", ada)
    w._detail_sa.verticalScrollBar().setValue(0)
    tunggu(300)
    laluan, saiz, cerah, unik = skrin_fizikal("selawat_arab")
    semak("skrin selawat Arab disimpan", saiz > 30000, f"saiz {saiz}")

# ── 7. Saiz fon lalai SEDERHANA ─────────────────────────────────────
# Sesi 33: ketiga-tiga saiz fon (antara muka, Arab, terjemahan) lalai
# "Sederhana" (indeks 1, skala 1.0). Sebelum ini saiz teks Arab lalai
# "Besar" (indeks 2) sejak komit pertama. Semakan sumber + kelakuan
# app mengesan regresi lalai (dikembalikan ke 2) walaupun
# user_settings.json menyimpan nilai lama.
print("\n  ── SAIZ FON LALAI SEDERHANA ──")

from ui.theme import FONT_SCALES, FONT_SCALE_LABELS

semak("peta skala: indeks 1 = 'Sederhana' = 1.0",
      FONT_SCALE_LABELS[1] == "Sederhana" and FONT_SCALES[1] == 1.0,
      f"{FONT_SCALE_LABELS[1]} / {FONT_SCALES[1]}")

# Lalai KOD -- baca sumber app_qt.py (bebas daripada user_settings.json).
# Inilah pengawal regresi sebenar: kalau sesiapa mengembalikan lalai
# arabic_font_idx ke 2, semakan ini GAGAL walaupun settings fail kosong.
src_app = open(os.path.join(BASE, "ui", "app_qt.py"),
               encoding="utf-8").read()


def _lalai_kod(fail, kunci):
    m = re.search(rf'settings\.get\("{kunci}", (\d+)\)', fail)
    return m.group(1) if m else None


lalai = {k: _lalai_kod(src_app, k)
         for k in ("font_scale_idx", "arabic_font_idx",
                    "translation_font_idx")}
semak("lalai kod app_qt.py: ui=1, ar=0 (Kecil), tr=1",
      lalai == {"font_scale_idx": "1", "arabic_font_idx": "0",
                "translation_font_idx": "1"}, str(lalai))

# Butang "Set Semula" dalam settings_panel.py juga pulang ke 1,1,1
src_panel = open(os.path.join(BASE, "ui", "settings_panel.py"),
                 encoding="utf-8").read()
m_r = re.search(r"a\.ui_idx, a\.ar_idx, a\.tr_idx = (\d+), (\d+), (\d+)",
                src_panel)
semak("set semula settings_panel.py: 1, 0, 1",
      bool(m_r) and m_r.groups() == ("1", "0", "1"),
      m_r.groups() if m_r else "tiada padanan")

# Kelakuan app sebenar -- skala yang DIPAKAI semasa render
semak("app memuat saiz Kecil utk Arab (skala 0.85), ui/tr Sederhana",
      w.ui_idx == 1 and w.ar_idx == 0 and w.tr_idx == 1
      and w.ar_scale == 0.85 and w.tr_scale == 1.0,
      f"ui={w.ui_idx} ar={w.ar_idx} tr={w.tr_idx}")

# Panel Tetapan sebenar -- stepper papar "Sederhana", bukti fizikal
w.settings_panel.open_panel()
tunggu(400)
label_fon = {k: w.settings_panel._stepper_labels[k].text()
             for k in ("ar", "tr")}
semak("panel Tetapan papar 'Kecil' utk ar, 'Sederhana' utk tr",
      label_fon["ar"] == "Kecil" and label_fon["tr"] == "Sederhana",
      str(label_fon))

laluan, saiz, cerah, unik = skrin_fizikal("fon_sederhana")
semak("skrin fon disimpan", saiz > 30000, f"saiz {saiz}")
w.settings_panel.close_panel()
tunggu(400)

# Set Semula fizikal: tukar saiz Arab ke Besar (2), panggil _reset(),
# sahkan pulang ke Kecil (0) + stepper papar "Kecil" (Sesi 55 lanjutan).
w.settings_panel.open_panel()
tunggu(300)
w.ar_idx = 2
w.settings["arabic_font_idx"] = 2
w.settings_panel.sync()
tunggu(200)
semak("sebelum Set Semula: Arab papar 'Besar'",
      w.settings_panel._stepper_labels["ar"].text() == "Besar",
      w.settings_panel._stepper_labels["ar"].text())
w.settings_panel._reset()
tunggu(300)
semak("Set Semula pulang Arab ke Kecil (ar_idx=0, skala 0.85)",
      w.ar_idx == 0 and w.ar_scale == 0.85,
      f"ar_idx={w.ar_idx} skala={w.ar_scale}")
semak("Set Semula: stepper Arab papar 'Kecil' semula",
      w.settings_panel._stepper_labels["ar"].text() == "Kecil",
      w.settings_panel._stepper_labels["ar"].text())
w.settings_panel.close_panel()
tunggu(300)

# ── 8. Butang ↑ terapung + kotak carian nombor hadis ────────────────
# Sesi 34: halaman senarai kitab kini ada (a) butang ↑ terapung di sudut
# kanan-bawah yang muncul bila pengguna skrol ke bawah dan skrol lancar
# kembali ke hadis pertama, dan (b) kotak "Lompat No. hadis" di atas
# senarai dengan placeholder kabur julat sebenar (cth. "0–7008" untuk
# Bukhari) yang lompat terus ke hadis (sah julat + skrol ke kad).
# Semakan sumber + kelakuan app + skrin fizikal mengesan regresi.
print("\n  ── BUTANG ↑ + KOTAK NOMBOR HADIS ──")

# Sumber pages_kitab.py -- pengawal regresi sebenar (bebas daripada
# state app). Kalau sesiapa membuang butang/kotak ini, semakan GAGAL.
src_kitab = open(os.path.join(BASE, "ui", "pages_kitab.py"),
                 encoding="utf-8").read()
semak("sumber: butang ↑ dengan objectName backTop",
      'QPushButton("↑")' in src_kitab
      and 'setObjectName("backTop")' in src_kitab)
semak("sumber: kaedah _kemas_butang_atas + _skrol_atas_lancar",
      "def _kemas_butang_atas" in src_kitab
      and "def _skrol_atas_lancar" in src_kitab)
semak("sumber: kotak nombor _kitab_go_box + _hantar_go_box + julat db",
      "_kitab_go_box" in src_kitab
      and "def _hantar_go_box" in src_kitab
      and "max_hadis_id" in src_kitab)

# Buka halaman kitab Bukhari -- senarai 20 hadis (lalai per_page=20)
w.open_kitab("bukhari", 1)
t0 = time.time()
while time.time() - t0 < 10 and (
        not getattr(w, "_kitab_list", None)
        or w._kitab_list.count() <= 3):
    tunggu(100)
semak("senarai Bukhari dimuat (halaman kitab)", w._kitab_list.count() > 3,
      f"kad={w._kitab_list.count()}")

# Butang ↑: tunjuk di bawah skrol, sembunyi di atas, skrol lancar.
# DIUJI DAHULU (sebelum kotak lompat yang mencetuskan muat semula)
# supaya scrollbar dalam keadaan STABIL -- muat halaman baharu semasa
# ujian butang akan reset value ke 0 (perlumbaan) dan menyembunyikan
# butang walaupun setValue(max) sudah dipanggil.
b = getattr(w, "_kitab_top_btn", None)
bar = w._kitab_sa.verticalScrollBar()
semak("butang ↑ wujud (objectName backTop)",
      b is not None and b.objectName() == "backTop")
# Tunggu susun atur selesai supaya scrollbar ada julat SEBENAR (>=500,
# melebihi ambang 250px butang). `bar.setValue(maximum)` dengan max
# kecil tidak mencetuskan valueChanged yang mencukupi -- butang tidak
# akan dikemas walaupun senarai sudah penuh kemudian.
t0 = time.time()
while time.time() - t0 < 10 and bar.maximum() < 500:
    tunggu(100)
semak("scrollbar senarai ada julat (max >= 500)", bar.maximum() >= 500,
      f"max={bar.maximum()}")
bar.setValue(bar.maximum())
tunggu(200)
semak("butang ↑ kelihatan bila skrol ke bawah", b.isVisible(),
      f"value={bar.value()} max={bar.maximum()} hidden={b.isHidden()}")
laluan, saiz, cerah, unik = skrin_fizikal("butang_atas")
semak("skrin butang ↑ disimpan", saiz > 30000, f"saiz {saiz}")
bar.setValue(0)
tunggu(200)
semak("butang ↑ disembunyikan di atas", not b.isVisible())
bar.setValue(bar.maximum())
tunggu(100)
w._skrol_atas_lancar()
# Animasi ~250ms. Mesin sibuk (flaky timing yang diketahui, sama seperti
# uji_visual_bantuan) kadang melambatkan timer; beri masa luas dan
# mulakan semula jika nilai tersangkut (tidak berubah dalam 300ms).
# Regresi sebenar (animasi tidak berfungsi langsung) tetap GAGAL selepas
# tamat masa 6s.
t0 = time.time()
while time.time() - t0 < 6 and bar.value() != 0:
    lama = bar.value()
    tunggu(300)
    if bar.value() == lama and bar.value() != 0:
        w._skrol_atas_lancar()
semak("skrol lancar pulang ke atas (nilai 0)", bar.value() == 0,
      f"value={bar.value()}")

# Kotak carian nombor hadis (selepas ujian butang -- lompat mencetuskan
# muat semula halaman 351, jadi jangan biarkan ia bersaing dengan skrol)
gb = getattr(w, "_kitab_go_box", None)
ph = gb.placeholderText() if gb else ""
semak("kotak carian nombor wujud", gb is not None)
semak("placeholder kabur '0–7008' (julat Bukhari)", ph == "0–7008",
      f"dapat {ph!r}")

# Lompat SAH: 7008 (hadis terakhir) -> terus buka detail + kotak kosong
gb.setText("7008")
w._hantar_go_box()
semak("kotak dikosongkan selepas lompat", gb.text() == "")
# Lompat TIDAK SAH: luar julat -> ditolak + toast ralat
gb.setText("999999")
w._hantar_go_box()
semak("nombor luar julat ditolak + toast ralat",
      w.toast.isVisible())

# Skrin fizikal kotak nombor di atas senarai (tema gelap)
bar.setValue(0)
tunggu(300)
laluan, saiz, cerah, unik = skrin_fizikal("kotak_nombor")
semak("skrin kotak nombor disimpan", saiz > 30000, f"saiz {saiz}")

# ── 9. Butang ↑ Carian + ketiadaan kotak Pergi pager ────────────────
# Sesi 34: (a) halaman hasil Carian kini ada butang ↑ terapung (corak
# sama halaman kitab — objectName "backTop"), dan (b) kotak
# "No. hadis… / Pergi" pada pager bawah DIBUANG — lompat nombor hanya
# melalui kotak atas senarai. Semakan sumber + kelakuan + skrin fizikal
# mengesan regresi (butang dibuang, atau kotak Pergi dipulangkan).
print("\n  ── BUTANG ↑ CARIAN + TIADA KOTAK PERGI ──")

# Sumber pages_carian.py — pengawal regresi butang carian
src_carian = open(os.path.join(BASE, "ui", "pages_carian.py"),
                  encoding="utf-8").read()
semak("sumber carian: butang ↑ dengan objectName backTop",
      'QPushButton("↑")' in src_carian
      and 'setObjectName("backTop")' in src_carian)
semak("sumber carian: kaedah _kemas_butang_atas_carian "
      "+ _skrol_atas_lancar_carian",
      "def _kemas_butang_atas_carian" in src_carian
      and "def _skrol_atas_lancar_carian" in src_carian)

# Sumber pages.py + pages_kitab.py — kotak Pergi pager MESTI tiada
src_pages = open(os.path.join(BASE, "ui", "pages.py"),
                 encoding="utf-8").read()
semak("sumber pages.py: kotak Pergi pager dibuang (tiada go_input/on_go_to)",
      "go_input" not in src_pages and "on_go_to" not in src_pages)
semak("sumber pages_kitab.py: tiada on_go_to",
      "on_go_to" not in src_kitab)

# Kelakuan: pager kitab tidak lagi ada kotak Pergi
pager = getattr(w, "_kitab_pager", None)
semak("pager kitab tiada go_input/go_btn",
      pager is not None
      and not hasattr(pager, "go_input")
      and not hasattr(pager, "go_btn"))

# Carian sebenar untuk senarai panjang
w.go("search")
w.search_bar.input.setText("sholat")
w._do_search(1)
t0 = time.time()
while time.time() - t0 < 30 and w._search_list.count() <= 3:
    tunggu(100)
semak("hasil carian dimuat (halaman carian)", w._search_list.count() > 3,
      f"kad={w._search_list.count()}")
tunggu(500)

b = getattr(w, "_search_top_btn", None)
bar = w._search_sa.verticalScrollBar()
semak("butang ↑ carian wujud (objectName backTop)",
      b is not None and b.objectName() == "backTop")
t0 = time.time()
while time.time() - t0 < 10 and bar.maximum() < 500:
    tunggu(100)
semak("scrollbar hasil ada julat (max >= 500)", bar.maximum() >= 500,
      f"max={bar.maximum()}")
bar.setValue(bar.maximum())
tunggu(200)
semak("butang ↑ carian KELIHATAN bila skrol ke bawah", b.isVisible(),
      f"value={bar.value()} max={bar.maximum()} hidden={b.isHidden()}")
laluan, saiz, cerah, unik = skrin_fizikal("butang_atas_carian")
semak("skrin butang ↑ carian disimpan", saiz > 30000, f"saiz {saiz}")
bar.setValue(0)
tunggu(200)
semak("butang ↑ carian DISEMBUNYIKAN di atas", not b.isVisible())

# Skrol lancar — gelung ulang-mula sama seperti seksyen 8 (flaky timing
# mesin sibuk yang diketahui)
bar.setValue(bar.maximum())
tunggu(100)
w._skrol_atas_lancar_carian()
t0 = time.time()
while time.time() - t0 < 6 and bar.value() != 0:
    lama = bar.value()
    tunggu(300)
    if bar.value() == lama and bar.value() != 0:
        w._skrol_atas_lancar_carian()
semak("skrol lancar carian pulang ke atas (nilai 0)", bar.value() == 0,
      f"value={bar.value()}")

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print(f"  Tangkapan skrin: {BUKTI}")
print("=" * 62)
sys.exit(1 if FAIL else 0)
