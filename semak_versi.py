"""Sahkan fail dalam folder ini benar-benar versi terkini.

    python semak_versi.py

Jalankan ini SEBELUM apa-apa skrip lain selepas mengekstrak ZIP.
Ia menangkap ralat pemasangan yang paling mahal: mengekstrak ke lokasi
yang salah supaya fail lama kekal dan setiap laporan kelihatan sah.
"""

from __future__ import annotations

import importlib
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def main() -> int:
    print()
    print("=" * 60)
    print("  SEMAKAN VERSI PEMASANGAN")
    print("=" * 60)
    print(f"\n  Folder: {BASE}")

    try:
        from VERSI import CIRI, VERSI
    except Exception:
        print("\n  VERSI.py TIADA.")
        print("  Fail ini versi LAMA (sebelum 2026.07.30-3).")
        print("\n  Ekstrak semula PustakaHadith.zip ke folder INI.")
        print("  ZIP tidak mempunyai folder bersarang -- isinya patut")
        print("  mendarat terus di sini (config.py, core/, ui/ ...).\n")
        return 1

    print(f"  Versi : {VERSI}\n")

    # Amaran struktur: folder bersarang bermakna ekstrak salah tempat.
    bersarang = os.path.join(BASE, "hadis")
    if os.path.isdir(bersarang) and os.path.exists(
            os.path.join(bersarang, "config.py")):
        print("  AMARAN: folder `hadis/` bersarang dijumpai.")
        print("  Anda mungkin telah mengekstrak ZIP lama ke dalam folder")
        print("  ini. Skrip berjalan dari SINI, jadi fail dalam")
        print("  `hadis/` DIABAIKAN. Padamkannya untuk mengelak keliru.\n")

    gagal = []
    for modul, nama in CIRI:
        try:
            m = importlib.import_module(modul)
        except Exception as e:
            gagal.append(f"{modul}: {e}")
            continue
        if not hasattr(m, nama):
            gagal.append(f"{modul}.{nama} TIADA")

    if gagal:
        print(f"  {len(gagal)} ciri hilang -- fail ini LAMA:\n")
        for g in gagal:
            print(f"    - {g}")
        print("\n  Ekstrak semula ZIP ke folder INI dan jalankan lagi.\n")
        return 1

    # JANGAN kata "TERKINI" -- skrip ini tidak tahu apa versi terbaru
    # yang wujud. Ia hanya boleh sahkan ciri yang DIKETAHUINYA hadir.
    # Mengaku lebih daripada itu menyembunyikan pemasangan lapuk.
    print(f"  Semua {len(CIRI)} ciri v{VERSI} hadir.\n")
    print("  PENTING: skrip ini TIDAK tahu versi terbaru yang wujud.")
    print(f"  Banding '{VERSI}' dengan versi ZIP terakhir yang diberi.")
    print("  Jika berbeza, ekstrak semula -- lihat arahan di bawah.\n")
    print("  Windows: Expand-Archive TANPA -Force akan GAGAL pada")
    print("  fail sedia ada dan meninggalkan kod lama:")
    print('    Expand-Archive -Path "$HOME\\Downloads\\PustakaHadith.zip" `')
    print(f'      -DestinationPath "{BASE}" -Force\n')
    # Kod terkini di folder BAHARU tetapi hadis.db di folder LAMA ialah
    # kegagalan senyap: aplikasi kelihatan kosong tanpa sebab jelas.
    try:
        from config import DB_PATH
        if not os.path.exists(DB_PATH):
            print("  AMARAN: hadis.db TIADA di sebelah kod ini.")
            print(f"  Dijangka: {DB_PATH}")
            print("  Jika anda pernah sync dalam folder LAIN, pindahkan")
            print("  datanya (jangan sync semula 12 minit):")
            print('      .\\PINDAH_DATA.ps1 "D:\\laluan\\folder\\lama"')
            print()
    except Exception:
        pass

    print("  Seterusnya:")
    print("    python semak.py            # ujian automatik")
    print("    python sync_english.py     # padan terjemahan")
    print("    python audit_eng.py --semua")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
