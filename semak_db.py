"""Laporkan kandungan hadis.db yang sedang digunakan.

    python semak_db.py

Menjawab: adakah kod yang saya jalankan ini melihat data saya?

Mengekstrak ZIP ke folder baharu memberi kod terkini tetapi
meninggalkan `hadis.db` di folder lama. Aplikasi kelihatan kosong dan
puncanya tidak jelas. Skrip ini menunjukkan laluan sebenar DB yang
digunakan, bukan yang disangka.
"""

from __future__ import annotations

import os
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

try:
    from VERSI import VERSI
except Exception:
    VERSI = "LAMA-tidak-diketahui"

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from config import DB_PATH                                    # noqa: E402


def main() -> int:
    print()
    print("=" * 62)
    print(f"  KANDUNGAN hadis.db   (v{VERSI})")
    print("=" * 62)
    print(f"\n  Kod  : {BASE}")
    print(f"  DB   : {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print("\n  DB TIADA pada laluan itu.\n")
        print("  `config.py` mengira DB_PATH relatif kepada folder kod:")
        print("      DB_PATH = os.path.join(BASE_DIR, 'hadis.db')")
        print("  Jadi hadis.db mesti berada BERSEBELAHAN kod ini.\n")
        print("  Jika anda pernah menjalankan sync dalam folder lain,")
        print("  pindahkan datanya:")
        print('      .\\PINDAH_DATA.ps1 "D:\\laluan\\folder\\lama"\n')
        return 1

    saiz = os.path.getsize(DB_PATH)
    print(f"  Saiz : {saiz:,} bait ({saiz/1048576:.1f} MB)\n")

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        jum = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    except sqlite3.Error as e:
        print(f"  Tidak dapat membaca jadual `hadis`: {e}\n")
        conn.close()
        return 1

    if jum == 0:
        print("  DB WUJUD tetapi KOSONG. Jalankan: python sync.py\n")
        conn.close()
        return 1

    try:
        eng = dict(conn.execute(
            "SELECT collection, COUNT(*) FROM terjemahan_eng "
            "GROUP BY collection"))
    except sqlite3.Error:
        eng = {}
    try:
        syr = conn.execute("SELECT COUNT(*) FROM syarah").fetchone()[0]
    except sqlite3.Error:
        syr = 0
    try:
        he = dict(conn.execute(
            "SELECT collection, COUNT(*) FROM hadethenc "
            "GROUP BY collection"))
    except sqlite3.Error:
        he = {}

    rows = conn.execute(
        "SELECT collection, COUNT(*) FROM hadis GROUP BY collection "
        "ORDER BY collection").fetchall()

    print(f"  {'kitab':14}{'hadis':>9}{'english':>10}{'hdeethenc':>11}"
          f"{'liputan':>10}")
    print("  " + "-" * 54)
    for slug, n in rows:
        e = eng.get(slug, 0)
        h = he.get(slug, 0)
        pct = f"{e * 100 // n}%" if n else "-"
        print(f"  {slug:14}{n:>9,}{e:>10,}{h:>11,}{pct:>10}")
    print("  " + "-" * 54)
    print(f"  {'JUMLAH':14}{jum:>9,}{sum(eng.values()):>10,}{sum(he.values()):>11,}")
    print(f"\n  Syarah : {syr:,} seksyen")
    print(f"  HadeethEnc (huraian) : {sum(he.values()):,} padanan")

    try:
        bm = conn.execute("SELECT COUNT(*) FROM bookmarks").fetchone()[0]
        print(f"  Tanda buku : {bm:,}")
    except sqlite3.Error:
        pass

    print()
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
