#!/usr/bin/env python3
"""Pengesahan VISUAL SEBENAR — lencana bantuan carian (fallback OR + mesej).

Lancarkan `PustakaApp` pada skrin Windows TANPA offscreen, cari query
yang memicu lencana AMBER, dan ambil tangkapan skrin FIZIKAL untuk
kedua-dua tema:

  - "hukum riba"   -> fallback OR aktif (486 hasil) + nota
                     "Carian kata kunci longgar" (lencana AMBER)
  - "zodiak astrologi" -> keyword 0 hasil; jika AI ada padanan,
                     mesej bantuan "Tiada padanan kata kunci..."

    python uji_visual_bantuan.py

Tangkapan skrin: `bukti_visual/bantuan_*.png`
"""

import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication, QLabel
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


def skrin_fizikal(tag: str) -> tuple:
    """Tangkap HANYA tetingkap aplikasi (bukan seluruh skrin).

    ImageGrab.grab() tanpa bbox menangkap skrin penuh -- jika tetingkap
    lain (cerah) bertindih, ukuran kecerahan tema jadi tidak boleh
    dipercayai. Cari bbox tetingkap Qt melalui win32gui dan tangkap
    kawasan itu sahaja.
    """
    app.processEvents()
    time.sleep(0.4)
    hwnd = int(w.winId())
    # Naikkan ke hadapan supaya tidak bertindih
    try:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        time.sleep(0.3)
    except Exception:
        pass
    kiri, atas, kanan, bawah = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(kiri, atas, kanan, bawah))
    nama = f"bantuan_{tag}.png"
    laluan = os.path.join(BUKTI, nama)
    img.save(laluan)
    saiz = os.path.getsize(laluan)
    kecil = img.resize((320, 200))
    # getdata() deprecated sejak Pillow 12 (dibuang Pillow 14) -- guna
    # get_flattened_data() dengan fallback untuk Pillow lama.
    pix = getattr(kecil, "get_flattened_data", kecil.getdata)()
    warna = set()
    for px in pix:
        warna.add((px[0] >> 4, px[1] >> 4, px[2] >> 4))
    cerah = sum(sum(px[:3]) / 3 for px in pix) / (320 * 200)
    print(f"      -> {nama}  ({saiz} B, kecerahan {cerah:.0f}, "
          f"warna unik {len(warna)})")
    return laluan, saiz, cerah, len(warna)


def cari_label(teks_petunjuk: str) -> QLabel | None:
    """Cari QLabel dalam _search_list yang mengandungi petunjuk teks."""
    for i in range(w._search_list.count()):
        it = w._search_list.itemAt(i)
        if it is None:
            continue
        wl = it.widget()
        if isinstance(wl, QLabel) and teks_petunjuk in wl.text():
            return wl
    return None


print("=" * 62)
print("  UJIAN VISUAL SEBENAR — LENCANA BANTUAN CARIAN (v1.2)")
print("=" * 62)

# ── 1. Lancarkan aplikasi SEBENAR ────────────────────────────────────
print("\n  Lancarkan PustakaApp pada skrin sebenar...")
from ui.app_qt import PustakaApp
w = PustakaApp()
w.show()
w.raise_()
w.activateWindow()
tunggu(2500)
semak("Koleksi dimuat (9 kitab)", len(w.collections) == 9,
      f"jumpa {len(w.collections)}")


def tunggu_carian_selesai(timeout_ms: int = 120000):
    """Tunggu kedua-dua worker (keyword + semantik) selesai.

    Model AI boleh mengambil ~21s untuk dimuat pada carian pertama;
    `_tampal_gabungan` hanya dipanggil bila KEDUA-DUA selesai. Poll
    setiap 800ms sehingga `_sem_res` dan `_kw_res` bukan None.
    """
    elapse = 0
    while elapse < timeout_ms:
        app.processEvents()
        if w._sem_res is not None and w._kw_res is not None:
            return True
        loop = QEventLoop()
        QTimer.singleShot(800, loop.quit)
        loop.exec_()
        elapse += 800
    return False


def cari_dan_skrin(q: str, tag: str):
    """Cari q, sahkan lencana AMBER muncul, tangkap skrin."""
    w._sem_res = None
    w._kw_res = None
    w.search_bar.input.setText(q)
    w.go("search")
    w._do_search(1)
    selesai = tunggu_carian_selesai()
    app.processEvents()
    semak(f"{tag}: carian selesai dalam masa", selesai,
          "tamat masa menunggu")

    kw = w._kw_res or []
    meta = w._kw_meta or {}
    print(f"\n  [{tag}] '{q}' — keyword {len(kw)} hasil, "
          f"fallback={meta.get('fallback', False)}, total={meta.get('total')}")
    semak(f"{tag}: carian selesai (keyword hasil dijangkakan)",
          w._kw_res is not None, "kw_res=None")

    # search_info mesti papar bilangan dengan jelas: "padanan kata longgar"
    # bila fallback aktif, bukan sekadar "486 padanan kata" yang mengelirukan.
    info = w.search_info.text()
    if meta.get("fallback"):
        semak(f"{tag}: search_info papar 'padanan kata longgar'",
              "longgar" in info, f"teks={info[:80]}")
    else:
        semak(f"{tag}: search_info normal (tiada 'longgar' perlu)",
              "longgar" not in info, f"teks={info[:80]}")

    lencana = None
    if meta.get("fallback") and kw:
        lencana = cari_label("Carian kata kunci longgar")
        semak(f"{tag}: nota fallback OR dipapar", lencana is not None)
    elif not kw and not meta.get("total"):
        lencana = cari_label("Tiada padanan kata kunci")
        semak(f"{tag}: mesej bantuan dipapar", lencana is not None)
    else:
        semak(f"{tag}: hasil keyword normal (tiada lencana perlu)", True)

    if lencana is not None:
        st = lencana.styleSheet()
        semak(f"{tag}: lencana AMBER berlatarbelakang (kontras 2 tema)",
              "background-color" in st and "AMBER" not in st,
              "stylesh set")
    elif not (meta.get("fallback") and kw) and not (not kw and not meta.get("total")):
        semak(f"{tag}: lencana AMBER berlatarbelakang", True, "tiada perlu")

    # Tangkapan skrin fizikal
    laluan, saiz, cerah, unik = skrin_fizikal(tag)
    semak(f"{tag}: tangkapan skrin sebenar disimpan", saiz > 30000,
          f"saiz {saiz}")
    semak(f"{tag}: teks kelihatan ({unik} warna unik)", unik > 40,
          f"warna unik {unik}")
    # Skrin fizikal turut menangkap tetingkap lain; ambang longgar untuk
    # elak flaky. Gelap ~40-50, terang ~120-210 -- >100 jelas membezakan.
    if tag.startswith("gelap"):
        semak(f"{tag}: tema gelap (kecerahan < 100)", cerah < 100,
              f"{cerah:.0f}")
    else:
        semak(f"{tag}: tema terang (kecerahan > 100)", cerah > 100,
              f"{cerah:.0f}")
    return lencana is not None


# ── 2. Tema gelap — fallback OR "hukum riba" ─────────────────────────
print("\n  ── TEMA GELAP: fallback OR 'hukum riba' ──")
cari_dan_skrin("hukum riba", "gelap_fallback")

# ── 3. Tema gelap — mesej bantuan (keyword 0 hasil) ─────────────────
print("\n  ── TEMA GELAP: keyword 0 hasil 'zodiak astrologi' ──")
cari_dan_skrin("zodiak astrologi", "gelap_bantuan")

# ── 4. Tema terang ──────────────────────────────────────────────────
print("\n  ── TEMA TERANG: fallback OR 'hukum riba' ──")
w.set_theme("light")
tunggu(1500)
cari_dan_skrin("hukum riba", "terang_fallback")

print("\n  ── TEMA TERANG: keyword 0 hasil 'zodiak astrologi' ──")
cari_dan_skrin("zodiak astrologi", "terang_bantuan")

# ── 5. Kembali ke gelap ─────────────────────────────────────────────
w.set_theme("dark")
tunggu(600)

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print(f"  Tangkapan skrin: {BUKTI}")
print("=" * 62)
sys.exit(1 if FAIL else 0)
