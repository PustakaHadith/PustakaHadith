# Bina tangkapan skrin dokumentasi transformasi paparan detail (Sesi 55).
#
# Mod LALAI (ujian regresi visual): jana semua tangkapan ke folder
# sementara, bandingkan piksel-demi-piksel dengan `dokumen/imej/`, dan
# GAGAL (exit 1) jika mana-mana tangkapan menyimpang melebihi ambang.
# Ini mengunci rupa paparan detail — perubahan reka bentuk yang tidak
# disengajakan akan dikesan.
#
# Mod `--kemas` (kemas kini baseline dengan sengaja): simpan terus ke
# `dokumen/imej/` selepas perubahan reka bentuk yang SAH.
#
# Tangkapan yang dijana:
#   - nasai#4934 gelap/terang   (hadis sama dengan tangkapan lama 7 Ogos)
#   - bukhari#1 gelap           (kes darjat KOSONG — "Tiada penilaian ulama")
#   - nasai#2117 gelap skrol    (viewport di bawah — darjat TERBUKA)
#   - cip pastel TERANG         (Huraian: hijau/merah/amber)
import os
import sys
import tempfile
import time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")

import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QEventLoop
from PIL import Image

from ui.app_qt import PustakaApp
from ui.widgets import Collapsible

KEMAS = "--kemas" in sys.argv
IMEJ = os.path.join("dokumen", "imej")

# Ambang regresi (ditala pada lantai hingar render widget sebenar):
#   NMAD  = purata beza mutlak dinormal (0–1). 0.02 = 2% keamatan.
#   BILANG = pecahan piksel yang beza > TOL_PX pada mana-mana saluran.
#            Teks AA (anti-alias) berubah sedikit antara larian; 2.5%
#            memberi ruang tanpa membiarkan perubahan besar (susun atur,
#            palet, kandungan) lulus.
AMBANG_NMAD = 0.02
AMBANG_BILANG = 0.025
TOL_PX = 12
# Satu baris teks boleh balut berbeza antara larian (layout bistable
# ~42px — muat fon). Bandingan mencari anjakan menegak terbaik dalam
# julat ini; regresi sebenar (warna/palette/kehilangan seksyen) tetap
# dikesan kerana beza bukan sekadar peralihan baris.
AMBANG_ANJAK = 60

app = QApplication(sys.argv)
w = PustakaApp()
w.resize(1100, 780)
w.show()


def tunggu(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


def _bina_koll_terbuka():
    """Paksa bina kandungan semua Collapsible TERBUKA (bina lazai).

    Tanpa ini, kandungan Huraian/darjat dibina bila-bila masa (lazy) —
    saiz halaman berubah antara larian (cth. bukhari#1 1241 vs 1286) dan
    ujian regresi jadi tidak menentu. Selepas ini saiz stabil: kandungan
    penuh sentiasa wujud sebelum grab.
    """
    for c in w.findChildren(Collapsible):
        if getattr(c, "_terbuka", False) and not getattr(c, "_dibina", False):
            c.buka()
            tunggu(500)


def _grab_stabil(fn) -> "QPixmap":
    """Grab berulang sehingga stabil (dua grab berturut-turut sama).

    Susun atur halaman kadangkala masih berubah selepas open_detail
    (muat fon, bina lazai) — satu baris teks berbeza = ~42px tinggi.
    Tunggu sehingga dua grab berturut-turut IDENTIK, maksimum 8 cubaan.
    """
    img = fn()
    for _ in range(8):
        tunggu(400)
        app.processEvents()
        img2 = fn()
        if img.toImage() == img2.toImage():
            return img2
        img = img2
    return img


def grab_penuh(nama: str, kol: str, hid: int):
    """Keseluruhan kandungan halaman (bukan viewport) — semua bahagian kelihatan."""
    w.open_detail({"collection": kol, "id": hid}, "home")
    tunggu(1800)
    _bina_koll_terbuka()
    w._detail_sa.verticalScrollBar().setValue(0)
    img = _grab_stabil(lambda: w._detail_sa.widget().grab())
    img.save(nama)
    print(f"disimpan {nama} ({img.width()}x{img.height()})")


def grab_viewport(nama: str, kol: str, hid: int):
    """Tingkap sebenar DISCROLL ke bawah — apa yang pengguna lihat selepas skrol."""
    w.open_detail({"collection": kol, "id": hid}, "home")
    tunggu(1800)
    _bina_koll_terbuka()
    w._detail_sa.verticalScrollBar().setValue(
        w._detail_sa.verticalScrollBar().maximum())
    img = _grab_stabil(lambda: w.grab())
    img.save(nama)
    print(f"disimpan {nama} ({img.width()}x{img.height()})")


def grab_cip(nama: str, kol: str, hid: int):
    """Cip klasifikasi dalam bahagian Huraian — bingkai rapat (Collapsible)."""
    w.open_detail({"collection": kol, "id": hid}, "home")
    tunggu(1800)
    kol_he = next((c for c in w.findChildren(Collapsible)
                   if (getattr(c, "_tajuk", "") or "").startswith("Huraian")),
                  None)
    if kol_he is None:
        print(f"TIADA Huraian untuk {kol}#{hid}")
        return
    if not getattr(kol_he, "_dibina", False):
        kol_he.buka()
        tunggu(700)
    img = kol_he.grab()
    img.save(nama)
    print(f"disimpan {nama} ({img.width()}x{img.height()})")


def _metrik(a: np.ndarray, b: np.ndarray) -> tuple:
    """NMAD + pecahan piksel berbeza; a.shape == b.shape == (h, w, 3).

    Vektor Numpy bagi gelung Python asal (14 Ogos): sama formula
    (max beza saluran, jumlah dinormal 255, pecahan piksel > TOL_PX)
    tetapi ~100x lebih pantas — offset-scan 42px (78M piksel) kini
    saat, bukan minit.
    """
    d = np.abs(a - b).max(axis=2)
    n = d.size
    return (float(d.sum()) / (n * 255.0), int((d > TOL_PX).sum()) / n)


def banding(baru: str, lama: str) -> dict:
    """Bandingkan dua imej; pulangkan metrik {nmad, bilang, saiz_ok}.

    Jika saiz tinggi berbeza <= AMBANG_ANJAK (satu baris teks bistable),
    cari anjakan menegak terbaik yang meminimumkan beza. Jika beza
    melebihi AMBANG_ANJAK atau lebar berbeza -> GAGAL terus.
    """
    a = np.asarray(Image.open(baru).convert("RGB"), dtype=np.int16)
    b = np.asarray(Image.open(lama).convert("RGB"), dtype=np.int16)
    if a.shape == b.shape:
        nmad, bilang = _metrik(a, b)
        return {"nmad": nmad, "bilang": bilang, "saiz_ok": True}
    if a.shape[1] != b.shape[1] or abs(a.shape[0] - b.shape[0]) > AMBANG_ANJAK:
        return {"nmad": 1.0, "bilang": 1.0, "saiz_ok": False}
    # Imej lebih tinggi dulu; bandingkan kawasan atas imej pendek dengan
    # setiap anjakan (0..beza tinggi) pada imej tinggi; ambil terbaik.
    tinggi, pendek = (a, b) if a.shape[0] >= b.shape[0] else (b, a)
    h_min = pendek.shape[0]
    w_ = a.shape[1]
    best = None
    for off in range(0, abs(a.shape[0] - b.shape[0]) + 1):
        d = np.abs(pendek - tinggi[off:off + h_min, :, :]).max(axis=2)
        n = w_ * h_min
        m = (float(d.sum()) / (n * 255.0), int((d > TOL_PX).sum()) / n)
        if best is None or m[0] < best[0]:
            best = m
    return {"nmad": best[0], "bilang": best[1], "saiz_ok": True}


SENARAI_GELAP = [
    ("baru_detail_gelap_nasai4934.png", grab_penuh, ("nasai", 4934)),
    ("baru_detail_gelap_bukhari1.png", grab_penuh, ("bukhari", 1)),
    ("baru_detail_gelap_skrol_nasai2117.png", grab_viewport,
     ("nasai", 2117)),
]
SENARAI_TERANG = [
    ("baru_detail_terang_nasai4934.png", grab_penuh, ("nasai", 4934)),
    ("baru_detail_terang_cip_hijau_nasai2117.png", grab_cip,
     ("nasai", 2117)),
    ("baru_detail_terang_cip_merah_abudaud4177.png", grab_cip,
     ("abu-daud", 4177)),
    ("baru_detail_terang_cip_amber_ibnumajah2094.png", grab_cip,
     ("ibnu-majah", 2094)),
]


def _jana_satu(p: str, nama: str):
    """Jana SEMULA SATU tangkapan (retry) dengan tema yang betul.

    Retry berlaku selepas tema dipulihkan ke dark, jadi tangkapan terang
    perlu set light dahulu. Regresi sebenar tetap GAGAL pada cubaan
    kedua kerana kandungan/palet yang salah kekal salah.
    """
    for entri in SENARAI_TERANG:
        if entri[0] == nama:
            w.set_theme("light")
            tunggu(1200)
            entri[1](p, *entri[2])
            w.set_theme("dark")
            tunggu(600)
            return
    for entri in SENARAI_GELAP:
        if entri[0] == nama:
            w.set_theme("dark")
            tunggu(800)
            entri[1](p, *entri[2])
            return
    print(f"  [retry] TIADA entri untuk {nama}")


def _senarai_tangkapan(sasaran: str):
    """Jana semua tangkapan ke folder `sasaran`; pulangkan senarai fail."""
    w.set_theme("dark")
    tunggu(800)
    for nama, fn, args in SENARAI_GELAP:
        fn(os.path.join(sasaran, nama), *args)

    w.set_theme("light")
    tunggu(1500)
    for nama, fn, args in SENARAI_TERANG:
        fn(os.path.join(sasaran, nama), *args)

    # Pulihkan tema gelap supaya user_settings.json kekal konsisten.
    w.set_theme("dark")
    tunggu(800)
    return [e[0] for e in SENARAI_GELAP + SENARAI_TERANG]


if KEMAS:
    sasaran = IMEJ
    _senarai_tangkapan(sasaran)
    print(f"KEMAS: baseline dikemas dalam {IMEJ}")
else:
    # Ujian regresi: jana ke folder sementara, bandingkan dengan baseline.
    with tempfile.TemporaryDirectory(prefix="tangkapan_baru_") as tmp:
        senarai = _senarai_tangkapan(tmp)
        gagal = []
        for nama in senarai:
            baru = os.path.join(tmp, nama)
            lama = os.path.join(IMEJ, nama)
            if not os.path.exists(lama):
                gagal.append((nama, "TIADA baseline dalam dokumen/imej/"))
                print(f"  GAGAL {nama}: baseline tiada")
                continue
            m = banding(baru, lama)
            # Retry tunggal: tangkapan sekali-sekala menangkap bingkai
            # separa (bina/paint), bukan regresi sebenar — jana semula
            # tangkapan itu sekali dan banding lagi. Regresi sebenar
            # tetap GAGAL pada cubaan kedua.
            if not (m["saiz_ok"] and m["nmad"] < AMBANG_NMAD
                    and m["bilang"] < AMBANG_BILANG):
                print(f"  [retry] {nama}: jana semula (nmad={m['nmad']:.4f})")
                os.remove(baru)
                _jana_satu(baru, nama)
                m = banding(baru, lama)
            ok = m["saiz_ok"] and m["nmad"] < AMBANG_NMAD \
                and m["bilang"] < AMBANG_BILANG
            status = "OK  " if ok else "GAGAL"
            print(f"  {status} {nama}: nmad={m['nmad']:.4f} "
                  f"bilang={m['bilang']*100:.2f}% "
                  f"saiz={'sama' if m['saiz_ok'] else 'BERBEZA'}")
            if not ok:
                gagal.append((nama, f"nmad={m['nmad']:.4f} "
                                    f"bilang={m['bilang']*100:.2f}%"))
        if gagal:
            print(f"\n  {len(gagal)} tangkapan menyimpang dari baseline — "
                  "rupa berubah tanpa kebenaran.")
            print("  Gunakan `--kemas` SAHAJA selepas perubahan reka bentuk "
                  "yang sah.")
            sys.exit(1)
        print(f"\n  SEMUA {len(senarai)} tangkapan sepadan baseline — "
              "rupa paparan detail kekal.")
