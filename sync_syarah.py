"""Muat turun syarah klasik (Fasa 4B) dan padankan ke hadis.db.

    python sync_syarah.py            # semua kitab syarah tersedia
    python sync_syarah.py fathbari   # satu kitab
    python sync_syarah.py --semak    # status sahaja

TIADA KUNCI API. Sumber ialah fail teks statik di GitHub (OpenITI).

Jalankan `sync.py` DAHULU -- skrip ini memerlukan teks Arab dalam DB
untuk mengesahkan penomboran.

AMARAN SAIZ
-----------
Fath al-Bari ialah 30.5 MB dimuat turun dan menambah ~17 MB kepada
hadis.db. Ia Arab GUNDUL (tashkeel 0.00%) dan hanya meliputi Bukhari.
Ini rujukan pilihan, bukan huraian utama.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

try:
    from VERSI import VERSI
except Exception:            # fail lama tanpa VERSI.py
    VERSI = "LAMA-tidak-diketahui"

from config import DB_PATH                                     # noqa: E402
from core.syarah_source import (  # noqa: E402
    NISBAH_MIN, nisbah_keyakinan,                               # noqa: E402
    KITAB_SYARAH, LESEN, hurai, sahkan_padanan, simpan, url_kitab,
)
from db import init                                            # noqa: E402

CACHE = os.path.join(BASE, ".cache_syarah")

# Di bawah ambang ini, penomboran dianggap TIDAK sejajar dan kita
# berhenti. Diukur pada data sebenar: penomboran betul memberi ~76%,
# penomboran teranjak memberi 14-22%. Ambang 50% memisahkan keduanya
# dengan selamat.
AMBANG_PADANAN = 0.50


def muat_turun(kunci: str) -> str:
    os.makedirs(CACHE, exist_ok=True)
    laluan = os.path.join(CACHE, f"{kunci}.txt")
    if os.path.exists(laluan) and os.path.getsize(laluan) > 100000:
        return laluan

    meta = KITAB_SYARAH[kunci]
    print(f"    muat turun {meta['nama']} (~{meta['saiz_mb']} MB) ...",
          end="", flush=True)
    try:
        with urllib.request.urlopen(url_kitab(kunci), timeout=600) as r:
            data = r.read()
    except Exception as e:
        print(f" GAGAL ({e})")
        raise
    try:
        with open(laluan, "wb") as f:
            f.write(data)
        saiz = os.path.getsize(laluan)
        if saiz < 100000:
            print(f" {len(data)/1048576:.1f} MB "
                  f"(AMARAN: cache hanya {saiz:,} bait)")
        else:
            print(f" {len(data)/1048576:.1f} MB  [cache disimpan]")
    except OSError as e:
        # Muat turun berjaya; hanya cache gagal. Jangan gagalkan sync --
        # tulis ke fail sementara supaya pemanggil tetap dapat laluan.
        print(f" {len(data)/1048576:.1f} MB  (cache GAGAL: {e})")
        import tempfile
        fd, laluan = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "wb") as f:
            f.write(data)
    return laluan


def sync_kitab(conn: sqlite3.Connection, kunci: str) -> int:
    meta = KITAB_SYARAH[kunci]
    slug = meta["atas"]

    ada = conn.execute("SELECT COUNT(*) FROM hadis WHERE collection=?",
                       (slug,)).fetchone()[0]
    if not ada:
        print(f"  {kunci:12} tiada hadis '{slug}' dalam DB "
              f"- jalankan sync.py dahulu")
        return 0

    try:
        laluan = muat_turun(kunci)
    except Exception:
        return 0

    with open(laluan, encoding="utf-8", errors="replace") as f:
        seksyen = hurai(f.read(), kunci)
    if not seksyen:
        print(f"  {kunci:12} parser tidak menemui seksyen - format berubah?")
        return 0

    # PENGAWAL: sahkan penomboran sejajar sebelum menyimpan apa-apa.
    # Tanpa ini, perubahan pada sumber boleh menyebabkan setiap hadis
    # dipasangkan dengan syarah yang SALAH -- bahaya untuk teks agama.
    r = nisbah_keyakinan(seksyen, conn, slug)
    # Papar SATU metrik sahaja. Versi lama mencampur kiraan sanad
    # (73/200) dengan skor kata-jarang (10%) -- dua benda berbeza pada
    # baris yang sama, dan pembaca menganggap 73/200 = 10%.
    print(f"  {kunci:12} skor sejajar {r['kadar']*100:.1f}%  vs  "
          f"kawalan {r['kawalan']*100:.1f}%   nisbah {r['nisbah']:.2f}x")
    if r["hanyut"]:
        anj = " ".join(f"{a:+d}" for _, _, a, _ in r["hanyut"])
        print(f"  {'':12} anjakan terbaik per julat: {anj}")
    if not r["stabil"]:
        print(f"  {'':12} DIBATALKAN - penomboran HANYUT merentas kitab.")
        print(f"  {'':12} Penanda '# N' dalam sumber ini TIDAK sejajar")
        print(f"  {'':12} dengan nombor hadis; ia kiraan hadis dalam bab.")
        print(f"  {'':12} Padanan ikut ID akan memberi syarah yang SALAH.")
        print(f"  {'':12} Tiada apa-apa disimpan.")
        return 0
    if not r["lulus"]:
        print(f"  {'':12} DIBATALKAN - nisbah di bawah {NISBAH_MIN}x.")
        print(f"  {'':12} Tiada apa-apa disimpan.")
        return 0

    had = conn.execute("SELECT MAX(hadis_id) FROM hadis WHERE collection=?",
                       (slug,)).fetchone()[0] or 0
    n = simpan(conn, slug, kunci, seksyen, had_id=had)
    liputan = (n / ada * 100) if ada else 0
    print(f"  {'':12} disimpan {n:,} seksyen "
          f"({liputan:.0f}% daripada {ada:,} hadis)")
    return n


def semak(conn: sqlite3.Connection) -> None:
    print(f"\n  {'kitab':14}{'atas':12}{'seksyen':>10}")
    print("  " + "-" * 38)
    for kunci, meta in KITAB_SYARAH.items():
        try:
            n = conn.execute(
                "SELECT COUNT(*) FROM syarah WHERE kitab=?", (kunci,)
            ).fetchone()[0]
        except sqlite3.Error:
            n = 0
        print(f"  {meta['nama']:14}{meta['atas']:12}{n:>10,}")
    print("  " + "-" * 38)
    print(f"  {LESEN}\n")


def main() -> int:
    arg = sys.argv[1:]
    mahu = [a for a in arg if not a.startswith("--")]

    conn = init(DB_PATH)

    if "--semak" in arg:
        semak(conn)
        return 0

    if conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0] == 0:
        print("\n  hadis.db kosong. Jalankan dahulu:\n      python sync.py\n")
        return 1

    sasaran = mahu or list(KITAB_SYARAH)
    tak_kenal = [k for k in sasaran if k not in KITAB_SYARAH]
    if tak_kenal:
        print(f"\n  Tidak dikenali: {', '.join(tak_kenal)}")
        print(f"  Pilihan: {', '.join(KITAB_SYARAH)}\n")
        return 1

    print(f"\n  PustakaHadith v{VERSI}")
    print(f"  Muat turun syarah untuk {len(sasaran)} kitab")
    print(f"  {LESEN}\n")

    jum = 0
    for kunci in sasaran:
        jum += sync_kitab(conn, kunci)

    print(f"\n  Selesai. {jum:,} seksyen syarah disimpan.")
    print(f"  Cache: {CACHE}  (boleh dipadam)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
