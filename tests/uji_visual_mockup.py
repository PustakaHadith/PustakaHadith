#!/usr/bin/env python3
"""Ujian VISUAL + STRUKTUR — mockup HTML (Sesi 55) vs halaman detail PyQt5.

Baca "kontrak reka bentuk" daripada mockup/mockup_*.html (sumber
kebenaran keputusan Sesi 55), lancarkan PustakaApp pada skrin SEBENAR,
buka hadis yang SAMA seperti mockup (bukhari#1, nasai#2117,
abu-daud#4177), kemudian semak widget tree PyQt5 terhadap kontrak itu
— elemen yang mockup ada mesti wujud dalam app, dan yang mockup tiada
mesti tidak wujud. Tangkapan skrin fizikal disimpan sebagai bukti.

    python uji_visual_mockup.py

Tangkapan skrin: `bukti_visual/mockup_*.png`

Kontrak diekstrak dari HTML mockup (bukan hardcode): susun atur panel
dua lajur (panel-sisi), tab bahasa dalam setiap lajur (tab-bahasa),
transliterasi dua gaya, bahagian Huraian TERBUKA + cip klasifikasi,
bahagian Penilaian ulama (darjat) + penafian, atribusi sumber, bar
navigasi bawah. Keputusan Sesi 55: huraian + darjat dipapar TERBUKA,
bukan Collapsible tertutup.
"""
import os
import re
import sqlite3
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
# Konsol Windows cp1252 rosakkan teks Arab — paksa UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QTextBrowser
from PyQt5.QtCore import QTimer, QEventLoop
from PIL import ImageGrab, ImageStat
import win32gui
import win32con

app = QApplication(sys.argv)

BUKTI = os.path.join(BASE, "bukti_visual")
os.makedirs(BUKTI, exist_ok=True)
MOCKUP = os.path.join(BASE, "mockup")

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


def _paksa_hadapan(hwnd):
    """Paksa tetingkap ke hadapan TANPA kunci fokus Windows.

    Bila ujian dijalankan sebagai SUBPROSES (cth. uji_pra_hantar.py),
    proses itu bukan proses aktif, jadi SetForegroundWindow ditolak dan
    tetingkap app kekal di belakang terminal — ImageGrab menangkap
    permukaan salah. HWND_TOPMOST memaksa tetingkap ke atas tanpa
    kebenaran fokus; Topmost sementara dibiarkan kerana setiap tangkapan
    memanggil fungsi ini semula (konsisten dengan uji_visual_sebenar).
    """
    try:
        # Pulihkan dahulu -- Windows kadangkala meminimumkan tetingkap
        # latar belakang (GetWindowRect lalu pulangkan ikon taskbar
        # ~160x28 dan tangkapan jadi 93 B pepejal). SW_RESTORE
        # membatalkan keadaan iconic sebelum tangkapan.
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


def _kira_warna(img, sasaran: tuple, tol: int = 10) -> int:
    """Kira piksel hampir dengan sasaran (sampel 2px — cukup untuk
    kehadiran aksen). Dipakai untuk mengesahkan tema terang dilukis
    penuh: TEAL #1A6B3C (breadcrumb/link/cip) mesti wujud, jika tidak
    tangkapan ialah bingkai separa (latar putih + teks hitam lalai).
    """
    px = img.convert("RGB").load()
    w, h = img.size
    n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            c = px[x, y]
            if all(abs(a - b) <= tol for a, b in zip(c, sasaran)):
                n += 1
    return n


def skrin_fizikal(tag: str) -> tuple:
    """Tangkap skrin fizikal dengan retry ikut tema (kukuh subproses).

    Bila tetingkap app hilang z-order (ditutup terminal), ImageGrab
    menangkap permukaan pepejal asing (93 B). Ulang sehingga tangkapan
    cukup terisi (warna unik >= 150) DAN kecerahan sepadan tema (gelap
    < 100, terang > 140) -- pengawal yang sama dengan uji_visual_sebenar.
    """
    hwnd = int(w.winId())
    tema_gelap = tag != "terang"
    img = None
    for _cubaan in range(10):
        app.processEvents()
        _paksa_hadapan(hwnd)
        kiri, atas, kanan, bawah = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
        warna = img.convert("RGB").getcolors(2_000_000)
        bil_warna = len(warna) if warna else 2_000_000
        kecerahan = ImageStat.Stat(img.convert("L")).mean[0]
        sah = bil_warna >= 150 and kecerahan < 100 if tema_gelap \
            else (bil_warna >= 150 and kecerahan > 140
                  and _kira_warna(img, (0x1A, 0x6B, 0x3C)) > 50)
        if sah:
            break
        time.sleep(0.5)
    nama = f"mockup_{tag}.png"
    laluan = os.path.join(BUKTI, nama)
    img.save(laluan)
    saiz = os.path.getsize(laluan)
    print(f"  [skrin] {laluan} ({saiz} B)")
    return laluan, saiz


# ── 1. Kontrak reka bentuk daripada mockup HTML ──────────────────────
def baca_kontrak(nama: str) -> dict:
    """Ekstrak kontrak struktur daripada satu fail mockup HTML.

    Semua mockup kongsi struktur CSS/JS yang sama (keputusan Sesi 55) —
    perbezaan hanyalah kandungan. Kontrak ialah apa yang WUJUD dalam
    mockup: susun atur, tab, bahagian, cip — bukan teks penuh.
    """
    html = open(os.path.join(MOCKUP, nama), encoding="utf-8").read()
    k = {}

    # Susun atur dua lajur: panel-sisi dengan 2 .lajur
    k["panel_sisi"] = "panel-sisi" in html
    k["bil_lajur"] = len(re.findall(r'class="lajur"', html))

    # Tab bahasa dalam setiap lajur
    k["tab_arab"] = re.findall(r'data-arab="([a-z]+)"', html)
    k["tab_lang"] = re.findall(r'data-lang="([a-z]+)"', html)

    # Transliterasi dua gaya (GAYA MELAYU + AKADEMIK)
    k["ada_translit"] = "GAYA MELAYU" in html and "AKADEMIK" in html

    # Bahagian bawah: Huraian + Penilaian ulama (darjat)
    k["bil_seksyen"] = len(re.findall(r'class="seksyen"', html))
    k["ada_chip"] = "chip" in html
    k["ada_quote"] = 'class="quote"' in html
    k["ada_nota_dalam"] = "nota-dalam" in html
    k["ada_darjat_bar"] = "darjat-bar" in html
    k["ada_breadcrumb"] = "breadcrumb" in html
    k["ada_bar_bawah"] = "bar-bawah" in html
    k["tindakan"] = [x for x in ("WhatsApp", "Salin", "Dengar", "Simpan")
                     if x in html]
    k["mod_gelap"] = "body.gelap" in html
    return k


def norm_teks(s) -> str:
    """Normalisasi ruang putih untuk perbandingan teks (kandungan)."""
    return " ".join((s or "").split())


def norm_apos(s) -> str:
    """Normalisasi ruang putih + apostrof melengkung (mockup vs DB)."""
    return (norm_teks(s)
            .replace("\u2018", "'")
            .replace("\u2019", "'"))


def baca_kandungan(nama: str) -> dict:
    """Ekstrak KANDUNGAN daripada mockup HTML untuk perbandingan teks.

    Berbeza daripada `baca_kontrak` (struktur/susun atur), fungsi ini
    ambil TEKS yang mockup papar: teks Arab, terjemahan, cip
    klasifikasi, baris darjat (darjat-bar), quote penafian dan atribusi
    sumber (nota-dalam). Kandungan ini kemudian diuji terhadap widget
    tree app — bukan sahaja SUSUN ATUR mockup direka semula, ISI juga
    (perbandingan kandungan teks, lanjutan Sesi 55).
    """
    import html as _html
    html = open(os.path.join(MOCKUP, nama), encoding="utf-8").read()

    def ambil(pat: str) -> str:
        m = re.search(pat, html, re.S)
        if not m:
            return ""
        return _html.unescape(
            re.sub(r"<[^>]+>", " ", m.group(1))).strip()

    def senarai(pat: str) -> list:
        return [_html.unescape(re.sub(r"<[^>]+>", " ", x)).strip()
                for x in re.findall(pat, html, re.S)]

    m_bg = re.search(
        r'body\.gelap \.chip \{[^}]*background:\s*(#[0-9a-fA-F]{6})',
        html)
    return {
        "arab": ambil(r'id="teks-arab">(.*?)</div>'),
        "melayu": ambil(r'id="teks-terjemah">(.*?)</div>'),
        "indonesia": ambil(r'id="teks-simpan-indonesia"[^>]*>(.*?)</div>'),
        "english": ambil(r'id="teks-simpan-english"[^>]*>(.*?)</div>'),
        "chip": ambil(r'<div class="chip">(.*?)</div>'),
        "chip_bg": m_bg.group(1) if m_bg else "",
        "darjat": senarai(r'<div class="darjat-bar">(.*?)</div>'),
        "quote": ambil(r'<div class="quote">(.*?)</div>'),
        "sumber": senarai(r'<div class="nota-dalam">(.*?)</div>'),
        "seksyen": senarai(r'<div class="seksyen-tajuk">(.*?)</div>'),
    }


def kelas_warna(hexs: str) -> str:
    """Klasifikasikan warna cip ke family (hijau/merah/amber/neutral).

    Digunakan untuk membandingkan family warna cip app (palet
    GREEN/RED/AMBER theme.py) dengan CSS mockup tanpa menuntut nilai
    heks sama — kontrasnya setara (disahkan dalam Lanjutan Sesi 55
    palet) tetapi heks berbeza.
    """
    h = hexs.lstrip("#")
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return "neutral"
    if g >= r and g >= b:
        return "hijau"
    # Merah vs amber: merah = r dominan DENGAN g≈b (hue merah tulen,
    # kedua-dua saluran rendah hampir sama, termasuk pastel terang
    # #FDEAEA yang g=234≈b=234); amber = r>g>b dengan g-b KETARA
    # (cth. #3A3120 g=49>b=32, #FDF3E0 g=243>b=224). Ambang mutlak
    # g-b <= 10 membezakan kedua-dua untuk tema gelap DAN terang.
    if r >= g and r >= b and abs(g - b) <= 10:
        return "merah"
    if r >= g >= b:
        return "amber"
    return "neutral"


KONTRAK = baca_kontrak("mockup_bukhari1.html")

# Mockup mesti sepadan antara satu sama lain pada STRUKTUR KONGSI.
# (ada_quote / ada_darjat_bar TIDAK dibandingkan — bukhari1 ialah kes
# darjat KOSONG, jadi sengaja tiada quote; nasai/abudaud ada.)
for nama in ("mockup_nasai2117.html", "mockup_abudaud4177.html"):
    k2 = baca_kontrak(nama)
    for kunci in ("panel_sisi", "bil_lajur", "tab_arab", "tab_lang",
                  "ada_translit", "bil_seksyen", "ada_chip",
                  "ada_nota_dalam", "ada_breadcrumb",
                  "ada_bar_bawah", "mod_gelap"):
        assert KONTRAK[kunci] == k2[kunci], \
            f"{nama}: {kunci} berbeza ({KONTRAK[kunci]} vs {k2[kunci]})"

print("=" * 62)
print("  UJIAN VISUAL MOCKUP — KONTRAK SESI 55 vs HAPUSAN PyQt5")
print("=" * 62)
print(f"  Kontrak mockup: {KONTRAK['bil_lajur']} lajur, "
      f"tab Arab={KONTRAK['tab_arab']}, tab bahasa={KONTRAK['tab_lang']}, "
      f"seksyen={KONTRAK['bil_seksyen']}")
semak("kontrak: panel dua lajur (panel-sisi)",
      KONTRAK["panel_sisi"] and KONTRAK["bil_lajur"] == 2)
semak("kontrak: tab dalam SETIAP lajur (arab+transliterasi; "
      "melayu+indonesia+english)",
      KONTRAK["tab_arab"] == ["arab", "transliterasi"]
      and KONTRAK["tab_lang"] == ["melayu", "indonesia", "english"])
semak("kontrak: transliterasi dua gaya (GAYA MELAYU + AKADEMIK)",
      KONTRAK["ada_translit"])
semak("kontrak: Huraian + darjat dua seksyen TERBUKA di bawah",
      KONTRAK["bil_seksyen"] == 2)
# ada_quote TIDAK di sini — bukhari1 ialah kes darjat kosong (tiada
# quote); penafian disemak per-kes (nasai/abudaud ada, bukhari tiada).
semak("kontrak: cip + atribusi + bar bawah + mod gelap",
      KONTRAK["ada_chip"]
      and KONTRAK["ada_nota_dalam"] and KONTRAK["ada_bar_bawah"]
      and KONTRAK["mod_gelap"])

# ── 2. Data sebenar tiga hadis mockup ────────────────────────────────
conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
KES = []
for nama, slug, hid in [("bukhari1", "bukhari", 1),
                        ("nasai2117", "nasai", 2117),
                        ("abudaud4177", "abu-daud", 4177),
                        ("ibnumajah2094", "ibnu-majah", 2094)]:
    r = conn.execute(
        "SELECT collection, hadis_id, arab, melayu, indonesia "
        "FROM hadis WHERE collection=? AND hadis_id=?",
        (slug, hid)).fetchone()
    if not r:
        print(f"  GAGAL tiada hadis {slug}#{hid} dalam hadis.db")
        sys.exit(1)
    e = conn.execute(
        "SELECT english FROM terjemahan_eng "
        "WHERE collection=? AND hadis_id=?",
        (slug, hid)).fetchone()
    d = conn.execute(
        "SELECT COUNT(*) FROM darjat WHERE collection=? AND hadis_id=?",
        (slug, hid)).fetchone()
    h = {"collection": r["collection"], "id": r["hadis_id"],
         "arab": r["arab"], "melayu": r["melayu"],
         "indonesia": r["indonesia"],
         "english": e["english"] if e else None,
         "nama_bab": None}
    KES.append((nama, h, d[0]))
conn.close()

# ── 3. Lancarkan aplikasi SEBENAR ────────────────────────────────────
print("\n  Lancarkan PustakaApp pada skrin sebenar...")
from ui.app_qt import PustakaApp
from ui.pages_detail import _warna_cip
from ui.widgets import Collapsible

w = PustakaApp()
w.resize(1100, 780)
# Pastikan tema GELAP untuk semua semakan cip: `_warna_cip` membaca
# RED/GREEN/AMBER_BG mengikut tema aktif; jika user_settings.json
# tertinggal tema terang dari larian sebelumnya (cth. akhir ujian ini
# sendiri menukar ke light tanpa pulih), RED_BG = #FDEAEA pastel yang
# keluarga warnanya tersilap dikelaskan (lihat kelas_warna).
w.set_theme("dark")
w.show()
w.raise_()
w.activateWindow()
tunggu(2500)
semak("Koleksi dimuat (9 kitab)", len(w.collections) == 9,
      f"jumpa {len(w.collections)}")


def cari_koll(tajuk_awal: str):
    for c in w.findChildren(Collapsible):
        if (getattr(c, "_tajuk", "") or "").startswith(tajuk_awal):
            return c
    return None


def periksa_hadis(nama: str, h: dict, n_darjat: int):
    """Buka hadis dan semak kontrak mockup terhadap widget tree PyQt5."""
    print(f"\n  ── {nama}: {h['collection']}#{h['id']} "
          f"(darjat={n_darjat}) ──")
    w.open_detail(h, "home")
    tunggu(1200)
    slug = h["collection"]
    hid = h["id"]

    # Semua Collapsible dalam keadaan ASAL selepas render (sebelum buka)
    tajuk_kolls = [(getattr(c, "_tajuk", "") or "")
                   for c in w.findChildren(Collapsible)
                   if c.isVisible()]
    print(f"      Collapsible: {tajuk_kolls}")

    # 3.1 Breadcrumb + tajuk + tindakan (bar atas)
    ada_utama = any(b.text() == "Utama" and b.objectName() == "nav"
                    for b in w.findChildren(QPushButton))
    ada_tajuk = any(lb.objectName() == "h2"
                    and str(lb.text()).startswith(
                        COLLECTION_META[slug]["name"])
                    and f"No. {hid}" in str(lb.text())
                    for lb in w.findChildren(QLabel))
    teks_butang = {b.text() for b in w.findChildren(QPushButton)
                   if b.isVisible()}
    semak(f"{nama}: breadcrumb Utama wujud", ada_utama)
    semak(f"{nama}: tajuk '{COLLECTION_META[slug]['name']} — Hadis No. {hid}'",
          ada_tajuk)
    semak(f"{nama}: tindakan WhatsApp/Salin/Dengar/Simpan",
          {"💬 WhatsApp", "📋 Salin", "🔊 Dengar"} <= teks_butang
          and any("Simpan" in t for t in teks_butang))

    # 3.2 Teks Arab + terjemahan wujud (kandungan)
    arab_txt = (h.get("arab") or "").strip()
    ada_arab = any(
        tb.toPlainText().strip().startswith(arab_txt[:60])
        for tb in w.findChildren(QTextBrowser))
    semak(f"{nama}: teks Arab dipapar", ada_arab)
    semak(f"{nama}: terjemahan dipapar",
          bool(w._detail_h.get("melayu") or ""))

    # 3.3 SUSUN ATUR DUA LAJUR — geometri fizikal
    # App (RTL 14 Ogos): terjemahan di lajur KIRI, Arab di lajur KANAN,
    # baris yang SAMA (y hampir sama), x Arab > x terjemahan.
    kotak_arab = None
    for tb in w.findChildren(QTextBrowser):
        if tb.toPlainText().strip().startswith(arab_txt[:60]):
            kotak_arab = tb
            break
    # Terjemahan = browser dalam _trans_box (kotak bahasa semasa)
    kotak_tr = None
    for tb in w._trans_box.findChildren(QTextBrowser):
        if tb.toPlainText().strip():
            kotak_tr = tb
            break
    dua_lajur = False
    if kotak_arab is not None and kotak_tr is not None:
        a = kotak_arab.mapTo(w, kotak_arab.rect().topLeft())
        t = kotak_tr.mapTo(w, kotak_tr.rect().topLeft())
        # Pembeza SUSUN ATUR RTL: x Arab jauh di KANAN lajur terjemahan
        # (dahulu menegak: x hampir sama). y dalam julat lajur yang
        # sama — beza kecil hingga sederhana kerana lajur terjemahan
        # ada label bahasa + butang tindakan di atas browser.
        dua_lajur = a.x() > t.x() + 100 and abs(a.y() - t.y()) < 300
        print(f"      geometri: arab@({a.x()},{a.y()}) "
              f"terjemahan@({t.x()},{t.y()}) -> dua_lajur={dua_lajur}")
    semak(f"{nama}: SUSUN ATUR DUA LAJUR (Arab | terjemahan sebelah-menyebelah)",
          dua_lajur,
          "mockup: .panel-sisi 2 lajur; semasa: kad Arab menegak di atas")

    # 3.4 Tab bahasa DALAM SETIAP lajur (keputusan Sesi 55 #2)
    # Mockup: tab-bahasa dalam lajur Arab (ARAB/TRANSLITERASI) + lajur
    # terjemahan (MELAYU/INDONESIA/ENGLISH). Susunan RTL (14 Ogos):
    # Arab di KANAN, terjemahan di KIRI. Semak secara geometri:
    # butang tab TRANSLITERASI mesti berada pada baris yang sama dengan
    # teks Arab; butang tab bahasa mesti berada dalam lajur terjemahan
    # (x lebih ke KIRI daripada sempadan kiri lajur Arab). App semasa:
    # transliterasi ialah Collapsible berasingan dan LangTabs global di
    # atas kotak terjemahan — kedua-duanya GAGAL.
    tab_translit = [b for b in w.findChildren(QPushButton)
                    if b.isVisible()
                    and b.text().strip().upper() == "TRANSLITERASI"]
    tab_bahasa = [b for b in w.findChildren(QPushButton)
                  if b.isVisible()
                  and b.text().strip().upper()
                  in ("MELAYU", "INDONESIA", "ENGLISH")]
    translit_dlm_lajur = False
    if kotak_arab is not None and tab_translit:
        a = kotak_arab.mapTo(w, kotak_arab.rect().topLeft())
        t = tab_translit[0].mapTo(w, tab_translit[0].rect().topLeft())
        # tab dalam lajur Arab: baris yang sama, di atas/kiri kotak Arab
        translit_dlm_lajur = abs(a.y() - t.y()) < 120 \
            and t.x() < a.x() + kotak_arab.width()
        print(f"      geometri transliterasi: arab@({a.x()},{a.y()}) "
              f"tab@({t.x()},{t.y()}) -> {translit_dlm_lajur}")
    semak(f"{nama}: tab TRANSLITERASI dalam lajur Arab (mockup: tab-bahasa "
          f"lajur 1)", translit_dlm_lajur,
          "semasa: transliterasi Collapsible berasingan di bawah kad Arab")
    tab_dlm_lajur = False
    if kotak_tr is not None and tab_bahasa:
        a = kotak_arab.mapTo(w, kotak_arab.rect().topLeft()) \
            if kotak_arab is not None else None
        sempadan_kiri = a.x() if a is not None else 10**9
        # Pembeza SUSUN ATUR (bukan label): tab bahasa mesti berada DI
        # KIRI sempadan lajur Arab (x < x arab) — iaitu dalam lajur
        # terjemahan (susunan RTL: Arab kanan, terjemahan kiri), bukan
        # LangTabs global yang melekat di atas kotak. Baris tab juga
        # mesti SEBARIS dengan tab TRANSLITERASI (kedua-dua lajur tab
        # atas panel dua lajur).
        tab_dlm_lajur = all(
            b.mapTo(w, b.rect().topLeft()).x() < sempadan_kiri
            for b in tab_bahasa)
        if tab_translit:
            y_ref = tab_translit[0].mapTo(w, tab_translit[0].rect().topLeft())
            tab_dlm_lajur = tab_dlm_lajur and all(
                abs(b.mapTo(w, b.rect().topLeft()).y() - y_ref.y()) < 120
                for b in tab_bahasa)
        print(f"      geometri tab bahasa: sempadan-kiri={sempadan_kiri} "
              f"-> {tab_dlm_lajur}")
    semak(f"{nama}: tab MELAYU/INDONESIA/ENGLISH dalam lajur terjemahan "
          "(mockup: tab-bahasa lajur 2)", tab_dlm_lajur,
          "semasa: LangTabs global melekat kiri di atas kotak terjemahan")

    # 3.5 Transliterasi dua gaya (GAYA MELAYU + AKADEMIK)
    # Keputusan Sesi 55: transliterasi ialah TAB dalam lajur Arab
    # (bukan Collapsible berasingan). Pilih tab, kemudian baca isi.
    ada_translit = False
    if getattr(w, "_btn_translit", None) is not None:
        w._set_arab_tab("transliterasi")
        tunggu(600)
        teks_isi = "\n".join(
            lb.text() for lb in w._translit_page.findChildren(QLabel))
        ada_translit = "GAYA MELAYU" in teks_isi.upper() \
            and "AKADEMIK" in teks_isi.upper()
    semak(f"{nama}: transliterasi dua gaya (GAYA MELAYU + AKADEMIK)",
          ada_translit,
          "mockup: tab TRANSLITERASI memapar kedua-dua gaya")

    # 3.5b Kandungan transliterasi sepadan enjin (core.phase2_transliterasi)
    # — bukan sekadar label gaya: teks rumi yang dipapar mesti sama dengan
    # output enjin yang sama digunakan oleh _bina_translit. Cermin juga
    # transformasi simbol selawat (syarat sama seperti _bina_translit).
    padan_isi_tr = False
    if getattr(w, "_btn_translit", None) is not None:
        try:
            from core.phase2_transliterasi import transliterate_arabic
            r_tr = transliterate_arabic(h.get("arab") or "")
            jangka = {
                "GAYA MELAYU": r_tr.get("rumi_malay_style", "") or "",
                "AKADEMIK": r_tr.get("rumi", "") or "",
            }
            if (w.settings.get("simbol_selawat", True)
                    and w._ada_glif_selawat):
                from utils.bahasa import guna_simbol_selawat
                jangka = {k2: guna_simbol_selawat(v)
                          for k2, v in jangka.items()}
            teks_tr = [tb.toPlainText()
                       for tb in w._translit_page.findChildren(QTextBrowser)]
            padan_isi_tr = all(
                norm_teks(v) and any(norm_teks(v) in norm_teks(t)
                                     for t in teks_tr)
                for v in jangka.values())
        except Exception as e:
            print(f"      [tr] enjin transliterasi gagal: {e}")
    semak(f"{nama}: kandungan transliterasi sepadan enjin (2 gaya)",
          padan_isi_tr,
          "mockup: tab TRANSLITERASI papar rumi GAYA MELAYU + AKADEMIK")

    # Kembalikan tab Arab (lalai) supaya semakan seterusnya konsisten
    if getattr(w, "_btn_arab", None) is not None:
        w._set_arab_tab("arab")
        tunggu(400)

    # 3.6 Huraian TERBUKA + cip klasifikasi (keputusan Sesi 55: TERBUKA)
    kol_he = cari_koll("Huraian")
    terbuka_asal = bool(kol_he) and getattr(kol_he, "_terbuka", False)
    semak(f"{nama}: bahagian Huraian dipapar TERBUKA (keputusan Sesi 55)",
          terbuka_asal,
          "mockup: panel-huraian TERBUKA di bawah; semasa: "
          "Collapsible buka() dipanggil — semak _terbuka")
    ada_cip = False
    if kol_he is not None:
        if not getattr(kol_he, "_dibina", False):
            kol_he.buka()
            tunggu(600)
        ada_cip = any(lb.objectName() == "chip" and lb.text().strip()
                      for lb in kol_he.findChildren(QLabel))
    semak(f"{nama}: cip klasifikasi dalam Huraian", ada_cip)

    # 3.7 Penilaian ulama (darjat) — papar mentah + TERBUKA (Sesi 55 #4)
    kol_d = cari_koll("Penilaian ulama")
    semak(f"{nama}: bahagian Penilaian ulama wujud", kol_d is not None)
    terbuka_d = bool(kol_d) and getattr(kol_d, "_terbuka", False)
    semak(f"{nama}: darjat dipapar TERBUKA (keputusan Sesi 55 — "
          "berbeza daripada Sesi 14 yang tertutup)",
          terbuka_d,
          "semasa: Collapsible tertutup lalai")
    if kol_d is not None and not getattr(kol_d, "_dibina", False):
        kol_d.buka()
        tunggu(600)
    # Kandungan darjat ikut keadaan data:
    #   n_darjat == 0  -> kes kosong: mesej jujur (bukhari1, mockup #9)
    #   n_darjat  > 0  -> baris "Nama — Darjat" + penafian (mockup #8)
    if kol_d is not None:
        teks_d = [lb.text() for lb in kol_d.findChildren(QLabel)]
        if n_darjat == 0:
            ada_kosong = any("Tiada penilaian ulama" in t
                             for t in teks_d)
            semak(f"{nama}: darjat KOSONG — mesej jujur (keputusan Sesi 55 "
                  "#9)", ada_kosong,
                  f"jumpa: {[t[:40] for t in teks_d]}")
        else:
            ada_baris = any("—" in t for t in teks_d)
            ada_nota = any("Penilaian ini daripada ulama hadis moden" in t
                           for t in teks_d)
            semak(f"{nama}: darjat papar mentah ({n_darjat} baris "
                  "Nama — Darjat)", ada_baris)
            semak(f"{nama}: penafian ulama moden", ada_nota)
    else:
        if n_darjat == 0:
            semak(f"{nama}: darjat KOSONG — mesej jujur", False,
                  "tiada Collapsible Penilaian ulama")
        else:
            semak(f"{nama}: darjat papar mentah (Nama — Darjat)", False,
                  "tiada Collapsible Penilaian ulama")

    # 3.8 Bar navigasi bawah: Kembali + prev/next
    # Mockup bukhari1: "No. 2 ›" sahaja (hid=1 tiada pendahulu) — sama
    # dengan _label_sebelum yang memulangkan None untuk hid <= 1.
    teks_nav = {b.text() for b in w.findChildren(QPushButton)
                if b.isVisible()}
    semak(f"{nama}: bar bawah ada Kembali",
          any("Kembali" in t for t in teks_nav))
    ada_next = any(t.strip().startswith("No.") and t.strip().endswith("›")
                   for t in teks_nav)
    ada_prev = any(t.strip().startswith("‹ No.") for t in teks_nav)
    if hid > 1:
        semak(f"{nama}: bar bawah prev/next nombor",
              ada_prev and ada_next,
              f"nav={sorted(teks_nav)}")
    else:
        semak(f"{nama}: bar bawah next nombor (hid=1 tiada prev)",
              ada_next and not ada_prev,
              f"nav={sorted(teks_nav)}")

    # 3.9 KANDUNGAN TEKS sepadan sumber data (lanjutan Sesi 55): bukan
    # hanya struktur/geometri — ISI yang dipapar mesti sama dengan
    # hadis.db (sumber kebenaran app) DAN dengan mockup (spesifikasi).
    k_isi = baca_kandungan(f"mockup_{nama}.html")

    # 3.9a Arab PENUH (3.2 hanya semak 60 aksara pertama)
    teks_arab_app = ""
    if getattr(w, "_ar_stack", None) is not None \
            and w._ar_stack.count() > 0:
        teks_arab_app = norm_teks(w._ar_stack.widget(0).toPlainText())
    db_arab = norm_teks(h.get("arab") or "")
    semak(f"{nama}: kandungan Arab PENUH sepadan hadis.db",
          bool(db_arab) and db_arab in teks_arab_app,
          f"app {len(teks_arab_app)} aksara vs db {len(db_arab)} aksara")

    # 3.9b Terjemahan tiap bahasa sepadan hadis.db. Melayu melalui
    # `_papar_melayu` (ejaan DBP + simbol selawat) — transformasi SAMA
    # yang app gunakan, jadi perbandingan kekal tepat. Mockup melayu
    # TIDAK dibandingkan terus (ia teks mentah DB, tanpa transformasi).
    for kunci in ("melayu", "indonesia", "english"):
        jangka = (h.get(kunci) or "").strip()
        if not jangka:
            continue
        if kunci == "melayu":
            jangka = w._papar_melayu(jangka)
        w._lang_tabs.set_active(kunci)
        tunggu(400)
        teks_trs = " ".join(
            norm_teks(tb.toPlainText())
            for tb in w._trans_box.findChildren(QTextBrowser))
        semak(f"{nama}: terjemahan {kunci.upper()} sepadan hadis.db",
              norm_teks(jangka) in teks_trs,
              f"app {len(teks_trs)} aksara vs db "
              f"{len(norm_teks(jangka))} aksara")

    # 3.9c Baris darjat SEBENAR sepadan sumber (api._darjat_luar — fungsi
    # yang sama digunakan oleh _bina_darjat) DAN baris darjat mockup.
    if n_darjat > 0 and kol_d is not None:
        teks_d = [lb.text() for lb in kol_d.findChildren(QLabel)]
        jangka_d = [f"{p['nama']} — {p['darjat']}"
                    for p in w.api._darjat_luar(slug, hid)]
        semak(f"{nama}: baris darjat ({len(jangka_d)} baris) sepadan "
              "sumber",
              all(any(norm_teks(j) in norm_teks(t) for t in teks_d)
                  for j in jangka_d),
              f"jangka={jangka_d}")
        if k_isi["darjat"]:
            semak(f"{nama}: baris darjat ({len(k_isi['darjat'])} baris) "
                  "sepadan mockup",
                  all(any(norm_teks(j) in norm_teks(t) for t in teks_d)
                      for j in k_isi["darjat"]),
                  f"mockup={k_isi['darjat']}")

    # 3.9d Kandungan mockup -> app: tajuk seksyen, cip klasifikasi,
    # quote penafian, atribusi sumber.
    tajuk_koll = {getattr(c, "_tajuk", "") or ""
                  for c in w.findChildren(Collapsible)}
    semak(f"{nama}: tajuk seksyen mockup jadi Collapsible app",
          all(any(norm_apos(s) in norm_apos(t) for t in tajuk_koll)
              for s in k_isi["seksyen"]),
          f"mockup={k_isi['seksyen']}")
    kol_hur = cari_koll("Huraian")
    teks_hur = ([lb.text() for lb in kol_hur.findChildren(QLabel)]
                if kol_hur is not None else [])
    if k_isi["chip"]:
        semak(f"{nama}: cip klasifikasi mockup ('{k_isi['chip']}') dipapar "
              "dalam Huraian",
              any(norm_apos(k_isi["chip"]) in norm_apos(t)
                  for t in teks_hur),
              f"jumpa={[t[:30] for t in teks_hur]}")
        # Warna cip ikut makna (keputusan Sesi 55 #5): app guna palet
        # GREEN/RED/AMBER theme.py; mockup guna family yang sama.
        # (a) stylesheet cip app sepadan jangkaan _warna_cip(mockup
        # chip); (b) family warna app == family CSS mockup (heks boleh
        # berbeza — kontras setara, bukan nilai sama).
        chip_w = None
        for lb in kol_hur.findChildren(QLabel):
            if lb.objectName() == "chip" and lb.text().strip():
                chip_w = lb
                break
        jangka_bg = _warna_cip(k_isi["chip"])
        if chip_w is not None and jangka_bg is not None:
            st = "".join(chip_w.styleSheet().split()).lower()
            semak(f"{nama}: cip diwarna ikut makna "
                  f"({kelas_warna(jangka_bg[0])})",
                  jangka_bg[0].lower() in st,
                  f"stylesheet={chip_w.styleSheet()[:80]}")
            if k_isi["chip_bg"]:
                kelas_m = kelas_warna(k_isi["chip_bg"])
                semak(f"{nama}: family warna cip sepadan mockup "
                      f"({kelas_warna(jangka_bg[0])} vs {kelas_m})",
                      kelas_warna(jangka_bg[0]) == kelas_m,
                      f"mockup bg={k_isi['chip_bg']}")
        else:
            semak(f"{nama}: cip diwarna ikut makna", False,
                  "tiada chip atau klasifikasi tidak dikenali")
    if k_isi["quote"] and kol_d is not None:
        teks_d = [lb.text() for lb in kol_d.findChildren(QLabel)]
        semak(f"{nama}: quote penafian mockup dipapar dalam darjat",
              any(norm_teks(k_isi["quote"]) in norm_teks(t)
                  for t in teks_d),
              f"mockup={k_isi['quote'][:50]}…")
    if k_isi["sumber"]:
        if n_darjat > 0 and kol_d is not None:
            teks_d = [lb.text() for lb in kol_d.findChildren(QLabel)]
            semak(f"{nama}: sumber darjat mockup dipapar",
                  any("fawazahmed0/hadith-api" in t for t in teks_d),
                  f"jumpa={[t[:40] for t in teks_d]}")
        ada_he = any("HadeethEnc" in t for t in tajuk_koll)
        ada_sema = any("SemakHadis" in t for t in tajuk_koll)
        jangka_hur = ("SemakHadis.com" if ada_sema
                      else ("HadeethEnc.com" if ada_he else None))
        if jangka_hur:
            semak(f"{nama}: sumber huraian ({jangka_hur}) dipapar",
                  any(jangka_hur in t for t in teks_hur),
                  f"jumpa={[t[:40] for t in teks_hur]}")

    # Tangkapan skrin fizikal
    w._detail_sa.verticalScrollBar().setValue(0)
    tunggu(400)
    laluan, saiz = skrin_fizikal(nama)
    semak(f"{nama}: skrin disimpan", saiz > 30000, f"saiz {saiz}")


from ui.theme import COLLECTION_META

for nama, h, n_darjat in KES:
    periksa_hadis(nama, h, n_darjat)

# Tema terang — satu tangkapan bukti kontras (keputusan palet: kekal)
w.set_theme("light")
tunggu(1200)
w.open_detail(KES[1][1], "home")
tunggu(1200)
w._detail_sa.verticalScrollBar().setValue(0)
tunggu(400)
laluan, saiz = skrin_fizikal("terang")
semak("tema terang: skrin disimpan", saiz > 30000, f"saiz {saiz}")
# Pulihkan tema gelap supaya larian seterusnya (dan user_settings.json)
# tidak kekal terang -- ujian lain bergantung pada tema lalai dark.
w.set_theme("dark")
tunggu(600)

w.close()
print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print(f"  Tangkapan skrin: {BUKTI}")
print("=" * 62)
sys.exit(1 if FAIL else 0)
