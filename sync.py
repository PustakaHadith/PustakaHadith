"""Tarik hadis dari service.hadis.my ke hadis.db tempatan.

    python sync.py                 # semua kitab, ikut keutamaan
    python sync.py bukhari muslim  # kitab tertentu sahaja
    python sync.py --semak         # tunjuk status, tiada muat turun
    python sync.py --paksa         # abaikan cache, tarik semula

KUNCI API
---------
Skrip ini TIDAK menerima kunci sebagai argumen baris arahan -- argumen
kekal dalam sejarah shell dan senarai proses. Ia dibaca oleh
`config.get_api_key()` mengikut keutamaan:

    1. user_settings.json   (gear -> Tetapan API dalam apl)
    2. .env                 (HADIS_API_KEY=...)
    3. pembolehubah persekitaran HADIS_API_KEY

Ketiga-tiga sudah tersenarai dalam .gitignore.

BOLEH DISAMBUNG
---------------
Kemajuan disimpan dalam hadis.db itu sendiri. Jika terputus -- rangkaian
mati, kuota habis, Ctrl+C -- jalankan semula. Ia menyambung dari muka
surat terakhir yang lengkap, bukan mula semula.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from api.hadis_api import (                                    # noqa: E402
    AuthError, HadisAPI, HadisAPIError, MAX_PER_PAGE, RateLimitExceeded,
)
from config import DB_PATH, get_api_key                        # noqa: E402
from db import bersih_tashkeel, init                            # noqa: E402


# Kitab paling kerap dicari didahulukan. Jika sync terputus di
# pertengahan, pengguna sekurang-kurangnya sudah ada yang penting.
KEUTAMAAN = [
    "bukhari", "muslim",                          # Sahihain
    "abu-daud", "tirmidzi", "nasai", "ibnu-majah",  # empat Sunan
    "malik", "ahmad", "darimi",
]


def susun(slugs: list[str]) -> list[str]:
    """Susun ikut KEUTAMAAN; yang tidak tersenarai diletak di belakang."""
    urutan = {s: i for i, s in enumerate(KEUTAMAAN)}
    return sorted(slugs, key=lambda s: urutan.get(s, 999))


def kiraan(conn: sqlite3.Connection) -> dict[str, int]:
    return {r[0]: r[1] for r in conn.execute(
        "SELECT collection, COUNT(*) FROM hadis GROUP BY collection")}


def simpan(conn: sqlite3.Connection, slug: str, items: list[dict]) -> int:
    """Tulis satu muka surat. INSERT OR IGNORE -> ulang jalan selamat."""
    baris = []
    for h in items:
        hid = h.get("id") or h.get("hadis_id")
        if hid is None:
            continue
        arab = h.get("arab") or ""
        baris.append((
            h.get("collection") or slug,
            int(hid),
            arab,
            bersih_tashkeel(arab),   # arab_carian: tanpa tashkeel untuk FTS5
            h.get("melayu") or "",
            h.get("indonesia") or "",
        ))
    if not baris:
        return 0
    cur = conn.executemany(
        "INSERT OR IGNORE INTO hadis(collection, hadis_id, arab, arab_carian, "
        "melayu, indonesia) VALUES (?,?,?,?,?,?)", baris)
    conn.commit()
    return cur.rowcount if cur.rowcount and cur.rowcount > 0 else 0


def sync_kitab(api: HadisAPI, conn: sqlite3.Connection, slug: str,
               paksa: bool = False) -> tuple[int, bool]:
    """Pulangkan (bilangan_baharu, patut_berhenti)."""
    ada = conn.execute("SELECT COUNT(*) FROM hadis WHERE collection=?",
                       (slug,)).fetchone()[0]

    try:
        d = api.get_hadis_list(slug, page=1, limit=MAX_PER_PAGE)
    except HadisAPIError as e:
        print(f"  {slug:12} GAGAL - {e}")
        return 0, isinstance(e, (AuthError, RateLimitExceeded))

    meta = d.get("meta") or {}
    total = int(meta.get("total") or 0)
    akhir = int(meta.get("last_page") or 1)

    if total and ada >= total and not paksa:
        print(f"  {slug:12} lengkap ({ada:,})")
        return 0, False

    # Sambung dari muka surat penuh terakhir. Muka surat separa akan
    # ditulis semula -- selamat kerana INSERT OR IGNORE.
    mula = 1 if paksa else max(1, (ada // MAX_PER_PAGE) + 1)
    if mula > 1:
        print(f"  {slug:12} sambung dari muka surat {mula}/{akhir}  ({ada:,} sedia ada)")

    baharu = 0
    for ms in range(mula, akhir + 1):
        try:
            if ms == 1:
                items = d.get("hadis") or []
            else:
                items = (api.get_hadis_list(slug, page=ms,
                                            limit=MAX_PER_PAGE).get("hadis") or [])
        except RateLimitExceeded as e:
            print(f"\n  {slug:12} kuota habis pada muka surat {ms} - {e}")
            return baharu, True
        except HadisAPIError as e:
            print(f"\n  {slug:12} ralat muka surat {ms} - {e}")
            return baharu, False

        baharu += simpan(conn, slug, items)

        siap = min(ms * MAX_PER_PAGE, total or ms * MAX_PER_PAGE)
        pct = (siap * 100 // total) if total else 0
        baki = api.daily_remaining
        bakis = f"  kuota {baki:,}" if isinstance(baki, int) else ""
        print(f"\r  {slug:12} {pct:3}%  {siap:,}/{total:,}{bakis}   ",
              end="", flush=True)

        # Berhenti awal jika kuota hampir habis -- biar baki untuk
        # penggunaan biasa apl hari ini.
        if isinstance(baki, int) and baki <= 3:
            print(f"\n  {slug:12} berhenti awal, kuota tinggal {baki}")
            return baharu, True

    print()
    return baharu, False


def semak(conn: sqlite3.Connection) -> None:
    import db as _db
    k = kiraan(conn)
    jum = sum(k.values())
    try:
        print(f"\n  Versi skema DB : {_db.versi(conn)} "
              f"(terkini {_db.SKEMA_VERSI})")
    except Exception:
        pass
    print(f"\n  {'kitab':14}{'dalam DB':>12}")
    print("  " + "-" * 26)
    for slug in KEUTAMAAN:
        n = k.get(slug, 0)
        tanda = " " if n else " (kosong)"
        print(f"  {slug:14}{n:>12,}{tanda}")
    lain = {s: n for s, n in k.items() if s not in KEUTAMAAN}
    for slug, n in lain.items():
        print(f"  {slug:14}{n:>12,}")
    print("  " + "-" * 26)
    print(f"  {'JUMLAH':14}{jum:>12,}\n")


def main() -> int:
    arg = [a for a in sys.argv[1:]]
    mod_semak = "--semak" in arg
    paksa = "--paksa" in arg
    mahu = [a for a in arg if not a.startswith("--")]

    conn = init(DB_PATH)

    if mod_semak:
        semak(conn)
        return 0

    kunci = get_api_key()
    if not kunci:
        print("\n  Kunci API tidak dijumpai.\n")
        print("  Letakkan kunci di salah satu tempat berikut:")
        print("    1. Buka apl -> ikon gear -> Tetapan API")
        print("    2. Fail .env dalam folder ini:")
        print("         HADIS_API_KEY=HADIS_xxxxxxxx")
        print("    3. Pembolehubah persekitaran HADIS_API_KEY\n")
        print("  Jangan taip kunci sebagai argumen baris arahan --")
        print("  ia kekal dalam sejarah shell.\n")
        return 1

    # use_db=False PENTING: jika tidak, HadisAPI akan membaca hadis.db
    # sebagai sumber offline dan sync hanya menyalin data kepada dirinya.
    api = HadisAPI(api_key=kunci, use_db=False)

    try:
        kitab = api.get_collections()
    except AuthError as e:
        print(f"\n  Kunci API ditolak: {e}")
        print("  Semak semula kunci dalam Tetapan API.\n")
        return 1
    except HadisAPIError as e:
        print(f"\n  Tidak dapat menghubungi pelayan: {e}\n")
        return 1

    sah = [c.get("slug") for c in kitab if c.get("slug")]
    conn.executemany(
        "INSERT OR REPLACE INTO collections(slug,name,author,total_hadis) "
        "VALUES (?,?,?,?)",
        [(c.get("slug"), c.get("name") or c.get("slug"),
          c.get("author"), c.get("total_hadis") or 0) for c in kitab])
    conn.commit()

    if mahu:
        tak_kenal = [s for s in mahu if s not in sah]
        if tak_kenal:
            print(f"\n  Slug tidak dikenali: {', '.join(tak_kenal)}")
            print(f"  Pilihan: {', '.join(sah)}\n")
            return 1
        sasaran = susun(mahu)
    else:
        sasaran = susun(sah)

    sebelum = sum(kiraan(conn).values())
    baki0 = api.daily_remaining
    print(f"\n  Sync {len(sasaran)} kitab -> hadis.db")
    if isinstance(baki0, int):
        print(f"  Kuota harian tersedia: {baki0:,}")
    print(f"  Sedia ada dalam DB   : {sebelum:,}\n")

    t0 = time.time()
    jumlah_baharu = 0
    berhenti = False

    try:
        for slug in sasaran:
            baharu, stop = sync_kitab(api, conn, slug, paksa=paksa)
            jumlah_baharu += baharu
            if stop:
                berhenti = True
                break
    except KeyboardInterrupt:
        print("\n\n  Dihentikan oleh pengguna.")
        berhenti = True

    # Optimumkan indeks carian hanya jika ada data baharu.
    if jumlah_baharu:
        try:
            conn.execute("INSERT INTO hadis_fts(hadis_fts) VALUES('optimize')")
            conn.commit()
        except sqlite3.Error:
            pass

    selepas = sum(kiraan(conn).values())
    print(f"\n  Selesai dalam {time.time() - t0:.0f}s")
    print(f"  Rekod baharu    : {jumlah_baharu:,}")
    print(f"  Jumlah dalam DB : {selepas:,}")
    if isinstance(api.daily_remaining, int):
        print(f"  Kuota tinggal   : {api.daily_remaining:,}")

    if berhenti:
        print("\n  Sync belum lengkap. Jalankan semula untuk menyambung:")
        print("      python sync.py\n")
        return 2

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
