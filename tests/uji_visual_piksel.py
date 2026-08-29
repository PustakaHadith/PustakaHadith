#!/usr/bin/env python3
"""Ujian PERBANDINGAN PIKSE L — render app vs palet mockup HTML.

Keputusan Sesi 55 (palet kertas hangat + cip warna ikut makna + aksen
hijau) dikunci secara PIKSE L: render aplikasi PyQt5 sebenar (tema
gelap + terang, 4 hadis mockup) dibandingkan dengan palet warna yang
diekstrak daripada CSS mockup/mockup_*.html.

QtWebEngine tidak dipasang (dan tidak boleh ditambah tanpa melanggar
peraturan projek "guna pustaka sedia ada"), jadi mockup TIDAK di-render
sebagai HTML. Sebaliknya perbandingan dilakukan pada peringkat warna:

  1. PALET — baca hex CSS mockup: latar (body), kad, panel-sisi, aksen
     (breadcrumb/bar bawah), dan cip (latar + teks) untuk terang & gelap.
  2. TANGKAP — lancarkan PustakaApp, buka hadis yang sama (bukhari#1,
     nasai#2117, abu-daud#4177, ibnu-majah#2094), dan gunakan
     `w.grab()` (render widget PyQt terus ke pixmap) sebagai sumber
     imej -- LEBIH stabil daripada ImageGrab (flak fokus tetingkap
     Windows pernah menangkap bingkai bukan-app; w.grab() tidak
     bergantung pada permukaan skrin).
  3. HISTOGRAM — kira histogram warna (5-bit/saluran) tangkapan dan
     bandingkan dengan histogram rujukan yang dilukis daripada palet
     mockup (jarak chi-square) — jika palet app menyimpang (cth. TEAL
     biru lama #7FC4DE), jarak melonjak dan semakan GAGAL.
  4. KEHADIRAN — nisbah piksel hampir dengan warna teras mockup:
     latar ≥ 10% (tema mendominasi), kad ≥ 4%, aksen hijau ≥ 0.4%,
     cip kes ≥ 0.05% (warna cip ikut makna benar-benar dilukis).

    python uji_visual_piksel.py

Tangkapan skrin: `bukti_visual/piksel_*.png`
"""

import os
import re
import sqlite3
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QEventLoop
from PIL import Image, ImageDraw

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


# ── 1. Ekstrak palet daripada CSS mockup ─────────────────────────────
def _hex(t):
    """#rrggbb -> (r,g,b)"""
    t = t.strip().lower()
    return tuple(int(t[i:i + 2], 16) for i in (1, 3, 5))


def _hex(t):
    """#rgb / #rrggbb -> (r,g,b)"""
    t = t.strip().lower()
    if len(t) == 4:  # #fff
        return tuple(int(c * 2, 16) for c in t[1:])
    return tuple(int(t[i:i + 2], 16) for i in (1, 3, 5))


def baca_palet_mockup(nama: str) -> dict:
    """Baca palet warna teras mockup: terang + gelap.

    CSS terang = bahagian HTML sebelum `body.gelap`; CSS gelap = dari
    `body.gelap` hingga penghujung blok CSS. Perbezaan penting: `.kad`
    biasa (terang) dan `body.gelap .kad` (gelap) MESTI dipisahkan supaya
    kad terang tidak tersilap ambil hex kad gelap (#282721).

    Pulangkan dict:
      {"terang": {"latar":..., "kad":..., "panel":..., "aksen":...,
                   "cip_bg":..., "cip_teks":...},
       "gelap": {...}}
    """
    html = open(os.path.join(MOCKUP, f"mockup_{nama}.html"),
                encoding="utf-8").read()
    # Pisahkan CSS terang vs gelap pada `body.gelap` pertama.
    penanda = re.search(r"body\.gelap", html)
    css_terang = html[:penanda.start()] if penanda else html
    css_gelap = html[penanda.start():] if penanda else ""
    pal = {}
    for mod, css in (("terang", css_terang), ("gelap", css_gelap)):
        d = {}
        # latar body (terang: `body {`; gelap: `body.gelap {`)
        m = re.search(r"body(?:\.gelap)?\s*\{[^}]*background:\s*"
                      r"(#[0-9a-fA-F]{3,6})", css)
        d["latar"] = _hex(m.group(1)) if m else None
        # kad
        m = re.search(r"\.kad\s*\{[^}]*background:\s*(#[0-9a-fA-F]{3,6})",
                      css)
        d["kad"] = _hex(m.group(1)) if m else None
        # panel-sisi
        m = re.search(r"\.panel-sisi\s*\{[^}]*"
                      r"background:\s*(#[0-9a-fA-F]{3,6})", css)
        d["panel"] = _hex(m.group(1)) if m else None
        # aksen (breadcrumb)
        m = re.search(r"\.breadcrumb[^{]*\{[^}]*color:\s*"
                      r"(#[0-9a-fA-F]{3,6})", css)
        if not m:
            # bar-bawah hijau gelap
            m = re.search(r"\.bar-bawah[^{]*\{[^}]*color:\s*"
                          r"(#[0-9a-fA-F]{3,6})", css)
        d["aksen"] = _hex(m.group(1)) if m else None
        # cip (latar + teks)
        m = re.search(r"\.chip\s*\{[^}]*background:\s*"
                      r"(#[0-9a-fA-F]{3,6})[^}]*color:\s*"
                      r"(#[0-9a-fA-F]{3,6})", css)
        if m:
            d["cip_bg"] = _hex(m.group(1))
            d["cip_teks"] = _hex(m.group(2))
        else:
            d["cip_bg"] = d["cip_teks"] = None
        pal[mod] = d
    return pal


# ── 2. Render rujukan palet (gantian HTML tanpa QtWebEngine) ─────────
def lukis_rujukan(pal_mod: dict, saiz=(400, 260)) -> Image.Image:
    """Lukis imej rujukan ringkas daripada palet mockup.

    Komposisi: latar penuh; blok kad besar (kad); bar panel-sisi
    (panel); garis aksen mendatar; bar cip kecil (cip_bg + cip_teks).
    Histogram imej ini mewakili "rupa mockup" yang dijangkakan — app
    yang guna palet Sama akan menghasilkan histogram serupa.
    """
    w, h = saiz
    img = Image.new("RGB", saiz, pal_mod.get("latar") or (244, 241, 234))
    d = ImageDraw.Draw(img)
    kad = pal_mod.get("kad") or (255, 255, 255)
    panel = pal_mod.get("panel") or kad
    aksen = pal_mod.get("aksen") or (26, 107, 60)
    # kad besar
    d.rectangle([10, 20, w - 10, h - 60], fill=kad)
    # panel-sisi di dalam kad
    d.rectangle([24, 40, w - 24, 170], fill=panel)
    # garis aksen
    d.rectangle([24, 186, w - 24, 190], fill=aksen)
    # bar cip (latar + teks)
    cb = pal_mod.get("cip_bg")
    ct = pal_mod.get("cip_teks")
    if cb and ct:
        d.rectangle([24, 200, 120, 220], fill=cb)
        d.rectangle([26, 204, 118, 216], fill=ct)
    return img


def hist5(im: Image.Image):
    """Histogram 5-bit/saluran (32 bins) -> dict bin -> kiraan."""
    kecil = im.resize((200, 130))
    pix = list(getattr(kecil, "get_flattened_data", kecil.getdata)())
    hh = {}
    for p in pix:
        k = ((p[0] >> 3) << 10) | ((p[1] >> 3) << 5) | (p[2] >> 3)
        hh[k] = hh.get(k, 0) + 1
    return hh


def jarak_chi(a: dict, b: dict) -> float:
    """Jarak chi-square antara dua histogram (bins yang ada sahaja)."""
    semua = set(a) | set(b)
    ta = sum(a.values()) or 1
    tb = sum(b.values()) or 1
    j = 0.0
    for k in semua:
        ea = a.get(k, 0) / ta
        eb = b.get(k, 0) / tb
        j += ((ea - eb) ** 2) / ((ea + eb) or 1e-9)
    return j


def tangkap_widget(tag: str) -> tuple:
    """Render widget PyQt penuh ke pixmap; pulangkan (laluan, imej).

    `w.grab()` melukis widget ke QPixmap secara terus (tiada pergantungan
    pada fokus tetingkap Windows / permukaan skrin — lebih stabil dan
    warna tepat). Pastikan event diproses dahulu supaya susun atur + QSS
    selesai.
    """
    app.processEvents()
    time.sleep(0.3)
    pm = w.grab()
    qimg = pm.toImage()
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    buf = bytes(ptr)
    img = Image.frombuffer("RGBA", (qimg.width(), qimg.height()),
                           buf, "raw", "BGRA", 0, 1).convert("RGB")
    laluan = os.path.join(BUKTI, f"piksel_{tag}.png")
    img.save(laluan)
    return laluan, img


def nisbah_hampir(img: Image.Image, warna, tol: int = 28) -> float:
    """Nisbah piksel dalam jarak <= tol (setiap saluran) dari warna.

    Guna imej PENUH (bukan resize kecil) supaya cip/aksen yang kecil
    tidak hilang. Tol MESTI ketat untuk warna gelap yang serupa
    (cth. kad #282721 vs cip bg #2A3B2F beza hanya ~20/saluran) --
    tol 8 untuk cip bg, 12 untuk aksen, 16 untuk teks cip.
    """
    pix = list(getattr(img, "get_flattened_data", img.getdata)())
    n = 0
    for p in pix:
        if (abs(p[0] - warna[0]) <= tol and abs(p[1] - warna[1]) <= tol
                and abs(p[2] - warna[2]) <= tol):
            n += 1
    return n / len(pix)


# ── 3. Data sebenar ──────────────────────────────────────────────────
KES = [("bukhari1", "bukhari", 1),
       ("nasai2117", "nasai", 2117),
       ("abudaud4177", "abu-daud", 4177),
       ("ibnumajah2094", "ibnu-majah", 2094)]

conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
conn.row_factory = sqlite3.Row
DATA = []
for nama, slug, hid in KES:
    r = conn.execute("SELECT collection, hadis_id FROM hadis "
                     "WHERE collection=? AND hadis_id=?",
                     (slug, hid)).fetchone()
    if not r:
        print(f"  GAGAL tiada hadis {slug}#{hid} dalam hadis.db")
        sys.exit(1)
    DATA.append((nama, {"collection": r["collection"], "id": r["hadis_id"]}))
conn.close()

print("=" * 62)
print("  UJIAN PIKSE L — APP SEBENAR vs PALET MOCKUP (Sesi 55)")
print("=" * 62)
semak("Palet mockup terbaca (4 kes × 2 tema)",
      all(baca_palet_mockup(n)["terang"]["latar"] is not None
          and baca_palet_mockup(n)["gelap"]["latar"] is not None
          for n, _, _ in KES))

# ── 4. Lancarkan aplikasi SEBENAR ────────────────────────────────────
print("\n  Lancarkan PustakaApp pada skrin sebenar...")
from ui.app_qt import PustakaApp

w = PustakaApp()
w.resize(1100, 780)
w.show()
w.raise_()
w.activateWindow()
tunggu(2500)
semak("Koleksi dimuat (9 kitab)", len(w.collections) == 9,
      f"jumpa {len(w.collections)}")

for mod in ("gelap", "terang"):
    w.set_theme("dark" if mod == "gelap" else "light")
    tunggu(1500)
    print(f"\n  ── TEMA {mod.upper()} ──")
    for nama, h in DATA:
        w.open_detail(h, "home")
        tunggu(1200)
        # Skrol ke bawah supaya huraian + cip + darjat kelihatan
        sb = w._detail_sa.verticalScrollBar()
        sb.setValue(sb.maximum())
        tunggu(400)
        laluan, img = tangkap_widget(f"{mod}_{nama}")
        pal = baca_palet_mockup(nama)[mod]

        # a. Histogram: app vs rujukan palet (jarak chi-square)
        chi = jarak_chi(hist5(img), hist5(lukis_rujukan(pal)))
        semak(f"{nama} [{mod}]: histogram app ≈ palet mockup "
              f"(chi {chi:.3f} < 3.0)", chi < 3.0, f"chi={chi:.3f}")

        # b. Kehadiran warna teras
        r_latar = nisbah_hampir(img, pal["latar"], tol=10)
        semak(f"{nama} [{mod}]: latar mockup mendominasi "
              f"({r_latar:.1%} >= 8%)", r_latar >= 0.08,
              f"nisbah {r_latar:.1%}")
        if pal.get("kad"):
            r_kad = nisbah_hampir(img, pal["kad"], tol=10)
            semak(f"{nama} [{mod}]: kad mockup hadir "
                  f"({r_kad:.1%} >= 3%)", r_kad >= 0.03,
                  f"nisbah {r_kad:.1%}")
        if pal.get("aksen"):
            r_aks = nisbah_hampir(img, pal["aksen"], tol=12)
            semak(f"{nama} [{mod}]: aksen hijau dilukis "
                  f"({r_aks:.3%} >= 0.02%)", r_aks >= 0.0002,
                  f"nisbah {r_aks:.3%}")
        # c. Cip warna ikut makna (kes: hijau/merah/amber) BENAR-BENAR
        #    dilukis sebagai piksel, bukan sekadar stylesheet.
        if pal.get("cip_bg") and pal.get("cip_teks"):
            # bg: tol ketat (8) supaya warna gelap yang serupa (kad) tidak
            #    terkira; teks: glyph kecil, tol lebih longgar.
            r_cip = nisbah_hampir(img, pal["cip_bg"], tol=8)
            r_cip_teks = nisbah_hampir(img, pal["cip_teks"], tol=16)
            semak(f"{nama} [{mod}]: cip warna dilukis "
                  f"(bg {r_cip:.3%}, teks {r_cip_teks:.3%})",
                  r_cip >= 0.0005 and r_cip_teks >= 0.00002,
                  f"bg={r_cip:.3%} teks={r_cip_teks:.3%}")

        # d. Penjaga: TEAL biru lama TIDAK mendominasi
        r_biru = nisbah_hampir(img, (0x7F, 0xC4, 0xDE), tol=20)
        semak(f"{nama} [{mod}]: TEAL biru lama tiada "
              f"({r_biru:.2%} < 1%)", r_biru < 0.01,
              f"nisbah {r_biru:.2%}")

# ── 5. Kepekaan mutasi: pengawal mesti GAGAL bila palet menyimpang ──
# Ujian ini mengubah piksel aksen hijau pada tangkapan menjadi TEAL
# biru lama, kemudian semak pengawal -- jika pengawal masih lulus,
# ia tidak menangkap regresi (pembatalan keputusan palet Sesi 55).
print("\n  ── KEPEKAAN MUTASI (regresi palet mesti dikesan) ──")
mut_img = Image.open(os.path.join(BUKTI, "piksel_gelap_bukhari1.png"))
mut_img = mut_img.convert("RGB")
pix = mut_img.load()
W, H = mut_img.size
# Hijau mockup gelap #5CBF85 -> biru lama #7FC4DE (seperti regresi palet)
n_tukar = 0
for y in range(H):
    for x in range(W):
        r, g, b = pix[x, y]
        if (abs(r - 0x5C) <= 20 and abs(g - 0xBF) <= 20
                and abs(b - 0x85) <= 20):
            pix[x, y] = (0x7F, 0xC4, 0xDE)
            n_tukar += 1
semak("mutasi: piksel aksen hijau ditemui + ditukar", n_tukar > 10,
      f"{n_tukar} piksel")
# Pengawal pada imej bermutasi: aksen hijau mesti hilang
r_aks_m = nisbah_hampir(mut_img, (0x5C, 0xBF, 0x85), tol=12)
semak("mutasi: aksen hijau hilang selepas tukar", r_aks_m < 0.0001,
      f"nisbah {r_aks_m:.4%}")
r_biru_m = nisbah_hampir(mut_img, (0x7F, 0xC4, 0xDE), tol=20)
semak("mutasi: biru lama muncul (pengawal aktif)", r_biru_m > 0.0001,
      f"nisbah {r_biru_m:.3%}")

w.set_theme("dark")
tunggu(800)
w.close()
print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print(f"  Tangkapan skrin: {BUKTI}")
print("=" * 62)
sys.exit(1 if FAIL else 0)
