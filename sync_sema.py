"""Padan hadis hadis.db kepada SemakHadis.com dan simpan ke jadual `semakhadis`.

    python sync_sema.py            # semua hadis
    python sync_sema.py --semak    # status sahaja

TIADA KUNCI API DIPERLUKAN -- semua muat turun SemakHadis disimpan dalam
cache tempatan `.cache_sema/` (2,372 hadis sahih-relevan: Muttafaq 'alayh,
Sahih, Hasan).

BAGAIMANA IA BERFUNGSI
----------------------
hadis.my dan SemakHadis.com tidak berkongsi penomboran. Padanan dibuat
melalui MATN Arab yang dinormalisasi (sanad + penanda umum ditanggalkan),
dengan pengesahan Jaccard + tolak calon kedua rapat -- lihat
`core/sema_source.padan()`.

    hadis.db (arab)  --padan matn-->  .cache_sema/{id}.json

Jalankan `sync.py` dahulu (DB perlu teks Arab).
"""

from __future__ import annotations

import os
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

try:
    from VERSI import VERSI
except Exception:            # fail lama tanpa VERSI.py
    VERSI = "LAMA-tidak-diketahui"

from config import DB_PATH                                     # noqa: E402
from core.sema_source import (                                 # noqa: E402
    CACHE, ambil, bina_indeks, padan, pasang_skema, simpan,
)
from db import init                                            # noqa: E402

KITAB = ["bukhari", "muslim", "abu-daud", "tirmidzi", "nasai",
         "ibnu-majah", "ahmad", "darimi", "malik"]


def sync_kitab(conn: sqlite3.Connection, slug: str,
               indeks: dict) -> tuple[int, int, int]:
    """Pulangkan (dipadan, tiada_arab, gagal_padan)."""
    baris = conn.execute(
        "SELECT hadis_id, arab FROM hadis "
        "WHERE collection=? AND arab<>''", (slug,)).fetchall()
    if not baris:
        print(f"  {slug:12} tiada teks Arab dalam DB - jalankan sync.py dahulu")
        return 0, 0, 0

    pasangan: list[tuple] = []
    tiada_arab = gagal = 0
    data = indeks["data"]
    for hid, arab in baris:
        r = padan(arab or "", indeks)
        if r is None:
            gagal += 1
            continue
        sid, jaccard = r
        d = data[sid]
        klas = (d.get("classification") or {}).get("name", "") or ""
        pasangan.append((slug, hid, sid, jaccard, klas,
                         d.get("title") or "", d.get("malay_text") or "",
                         d.get("intro_commentary") or "",
                         d.get("malay_commentary") or ""))

    # BUANG dahulu, jangan hanya REPLACE. Sebab sama seperti
    # sync_english.py: padanan yang dahulu sah tetapi kini ditolak
    # (ambang diperketat) akan kekal jika hanya INSERT OR REPLACE.
    try:
        conn.execute("DELETE FROM semakhadis WHERE collection=?", (slug,))
        conn.commit()
    except sqlite3.Error:
        pass

    simpan(conn, pasangan)
    n = len(baris)
    pct = len(pasangan) * 100 // n if n else 0
    print(f"  {slug:12} {pct:3}%  {len(pasangan):,}/{n:,}"
          f"   tiada_arab={tiada_arab}  gagal_padan={gagal}")
    return len(pasangan), tiada_arab, gagal


def semak(conn: sqlite3.Connection) -> None:
    try:
        rows = dict(conn.execute(
            "SELECT collection, COUNT(*) FROM semakhadis GROUP BY collection"))
    except sqlite3.Error:
        rows = {}
    arab = dict(conn.execute(
        "SELECT collection, COUNT(*) FROM hadis GROUP BY collection"))

    print(f"\n  {'kitab':14}{'hadis':>9}{'semakhadis':>12}{'liputan':>10}")
    print("  " + "-" * 44)
    for slug in KITAB:
        a = arab.get(slug, 0)
        e = rows.get(slug, 0)
        pct = f"{e*100/a:.1f}%" if a else "-"
        print(f"  {slug:14}{a:>9,}{e:>12,}{pct:>10}")
    print("  " + "-" * 44)
    print(f"  {'JUMLAH':14}{sum(arab.values()):>9,}{sum(rows.values()):>12,}\n")


def main() -> int:
    arg = sys.argv[1:]

    conn = init(DB_PATH)
    pasang_skema(conn)

    if "--semak" in arg:
        semak(conn)
        return 0

    jum = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    if jum == 0:
        print("\n  hadis.db kosong. Jalankan dahulu:\n      python sync.py\n")
        return 1

    indeks = bina_indeks()
    if len(indeks["data"]) < 50:
        print("\n  Cache SemakHadis belum lengkap "
              f"({len(indeks['data'])} hadis). Jalankan dahulu skrip muat turun.")
        return 1

    print(f"\n  PustakaHadith v{VERSI}")
    print(f"  Padan {jum:,} hadis kepada SemakHadis.com "
          f"({len(indeks['data'])} hadis sumber, cache tempatan)")
    print(f"  Jaccard matn: 0.55  (baris lama setiap kitab DIPADAM dahulu)\n")

    t_p = t_a = t_g = 0
    for slug in KITAB:
        p, a, g = sync_kitab(conn, slug, indeks)
        t_p += p
        t_a += a
        t_g += g

    print(f"\n  Selesai.")
    print(f"  Padanan disimpan   : {t_p:,}")
    if t_a:
        print(f"  Tiada teks Arab    : {t_a:,}")
    if t_g:
        print(f"  Gagal dipadan       : {t_g:,}")
    print(f"\n  Cache: {CACHE}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
