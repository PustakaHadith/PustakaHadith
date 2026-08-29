"""Diagnosis penomboran syarah pada data hadis.db SEBENAR.

    python diagnos_syarah.py

Menjawab satu soalan: adakah penanda `# N` dalam sumber syarah sejajar
dengan nombor hadis dalam DB anda, dan jika tidak -- adakah sisihan itu
MALAR (boleh dibetulkan dengan satu anjakan) atau HANYUT (tidak boleh).

Tidak mengubah apa-apa. Tiada kunci API.

Mengapa ini perlu: ujian terdahulu menggunakan CDN `ara-bukhari` sebagai
proksi kerana sandbox tiada hadis.db. Proksi itu mempunyai 7,554 hadis
dengan penomboran sendiri; hadis.my ada 7,008. Corak hanyut yang diukur
pada proksi TIDAK semestinya corak pada data sebenar.
"""

from __future__ import annotations

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
from core.syarah_source import (                              # noqa: E402
    KITAB_SYARAH, _skor_julat, hurai,
)
from db import connect                                        # noqa: E402

CACHE = os.path.join(BASE, ".cache_syarah")


def main() -> int:
    kunci = sys.argv[1] if len(sys.argv) > 1 else "fathbari"
    meta = KITAB_SYARAH.get(kunci)
    if not meta:
        print(f"\n  '{kunci}' tiada dalam katalog.\n")
        return 1
    slug = meta["atas"]

    # Muat turun sendiri jika cache tiada. Bergantung pada cache
    # `sync_syarah.py` bermakna diagnostik gagal tepat pada masa ia
    # paling diperlukan (bila sync dibatalkan).
    fail = os.path.join(CACHE, f"{kunci}.txt")
    if not (os.path.exists(fail) and os.path.getsize(fail) > 100000):
        try:
            from sync_syarah import muat_turun
            fail = muat_turun(kunci)
        except Exception as e:
            print(f"\n  Tidak dapat memperoleh fail syarah: {e}\n")
            return 1

    conn = connect(DB_PATH)
    baris = conn.execute(
        "SELECT hadis_id, arab FROM hadis WHERE collection=? AND arab<>'' "
        "ORDER BY hadis_id", (slug,)).fetchall()
    if not baris:
        print(f"\n  Tiada hadis '{slug}' dalam DB.\n")
        return 1
    teks = {hid: arab for hid, arab in baris}

    with open(fail, encoding="utf-8", errors="replace") as f:
        seksyen = hurai(f.read(), kunci)

    ids = sorted(teks)
    print("\n" + "=" * 66)
    print(f"  DIAGNOSIS PENOMBORAN SYARAH — {kunci}   (v{VERSI})")
    print("=" * 66)
    print(f"\n  hadis.db '{slug}' : {len(ids):,} hadis "
          f"(id {ids[0]}..{ids[-1]})")
    print(f"  seksyen syarah   : {len(seksyen):,}")
    print("  Metrik: pecahan kata JARANG matn yang muncul dalam syarah.")
    print("  (kata sanad diabaikan -- ia memadan walaupun nombor salah)\n")

    # Imbasan HALUS: langkah kecil, julat luas.
    n = len(ids)
    print("-" * 66)
    print("  ANJAKAN TERBAIK PER JULAT (imbasan halus)")
    print("-" * 66)
    print(f"\n  {'julat hadis':>18} | {'anjakan':>8} | {'skor':>7} | "
          f"{'skor@0':>7}")
    print("  " + "-" * 52)

    anjakan_ditemui = []
    for i in range(8):
        lo = ids[min(n - 1, i * n // 8)]
        hi = ids[min(n - 1, (i + 1) * n // 8 - 1)]
        s0 = _skor_julat(teks, seksyen, lo, hi, 0, had=150)
        terbaik, skor = 0, s0
        for off in list(range(-60, 61, 2)) + list(range(-400, 401, 20)):
            v = _skor_julat(teks, seksyen, lo, hi, off, had=150)
            if v > skor:
                terbaik, skor = off, v
        anjakan_ditemui.append(terbaik)
        print(f"  {lo:7,}-{hi:<9,} | {terbaik:+8} | {skor*100:6.2f}% | "
              f"{s0*100:6.2f}%")

    print("\n" + "-" * 66)
    julat_anj = max(anjakan_ditemui) - min(anjakan_ditemui)
    sifar = sum(1 for a in anjakan_ditemui if abs(a) <= 4)
    print(f"  Anjakan: min {min(anjakan_ditemui):+d}  "
          f"max {max(anjakan_ditemui):+d}  julat {julat_anj}")
    print(f"  Julat yang sejajar (|anjakan| <= 4): {sifar}/8")
    print()

    if sifar >= 7:
        print("  KEPUTUSAN: penomboran SEJAJAR. Padanan ikut ID selamat.")
    elif julat_anj <= 8:
        m = sorted(anjakan_ditemui)[len(anjakan_ditemui) // 2]
        print(f"  KEPUTUSAN: sisihan MALAR ({m:+d}). Boleh dibetulkan")
        print(f"             dengan satu anjakan tetap.")
    else:
        print("  KEPUTUSAN: penomboran HANYUT. Padanan ikut ID TIDAK")
        print("             selamat -- syarah salah akan dipasangkan")
        print("             pada sebahagian besar kitab.")
    print("=" * 66 + "\n")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
