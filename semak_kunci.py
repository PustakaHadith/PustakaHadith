"""Semak status kunci API — yang terdedah dan yang sedang digunakan.

    python semak_kunci.py

Menguji sama ada kunci lama yang terdedah masih diterima pelayan,
dan sama ada kunci semasa anda berfungsi.

Skrip ini TIDAK mencetak kunci penuh. Ia menggunakan satu permintaan
ringan setiap kunci (/collections).

Lihat REVOKE_KUNCI.md untuk cara membatalkan kunci.
"""

from __future__ import annotations

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import requests                                                # noqa: E402

from config import get_api_key, get_base_url, mask_key         # noqa: E402

# Kunci yang diketahui terdedah dalam perbualan. Disenaraikan supaya
# statusnya boleh disahkan; ia BUKAN rahsia lagi -- itulah masalahnya.
#
# Kunci sebenar disimpan DALAM fail `kunci_terdedah.txt` (satu per baris),
# yang TIDAK di-commit (lihat .gitignore). Jika fail tiada, senarai
# kosong -- skrip tetap berjalan untuk kunci semasa. Ini memastikan kunci
# API tidak pernah masuk ke dalam sejarah git.
_KUNCI_FILE = os.path.join(BASE, "kunci_terdedah.txt")


def _baca_kunci_terdedah() -> list[str]:
    if not os.path.exists(_KUNCI_FILE):
        return []
    try:
        with open(_KUNCI_FILE, encoding="utf-8") as f:
            return [baris.strip() for baris in f
                    if baris.strip() and not baris.strip().startswith("#")]
    except OSError:
        return []


KUNCI_TERDEDAH = _baca_kunci_terdedah()


def uji(kunci: str, base: str, timeout: int = 20) -> tuple[str, str]:
    """Pulangkan (status, butiran). Tidak mencetak kunci."""
    try:
        r = requests.get(f"{base.rstrip('/')}/collections",
                         headers={"X-API-Key": kunci,
                                  "Accept": "application/json"},
                         timeout=timeout)
    except requests.exceptions.RequestException as e:
        return "RALAT", f"tidak dapat hubungi pelayan: {type(e).__name__}"

    if r.status_code in (401, 403):
        return "DITOLAK", f"HTTP {r.status_code} — kunci tidak sah lagi"
    if r.status_code == 429:
        return "AKTIF", "HTTP 429 — kunci SAH tetapi kuota habis"
    if r.status_code == 200:
        baki = r.headers.get("x-ratelimit-daily-remaining", "?")
        return "AKTIF", f"HTTP 200 — kuota harian tinggal {baki}"
    return "?", f"HTTP {r.status_code}"


def main() -> int:
    base = get_base_url()
    print("\n" + "=" * 60)
    print("  SEMAKAN KUNCI API")
    print("=" * 60)
    print(f"\n  Pelayan: {base}")

    # ---- kunci terdedah ----
    print("\n  Kunci yang terdedah dalam perbualan")
    print("  " + "-" * 56)
    masih_hidup = 0
    for k in KUNCI_TERDEDAH:
        status, butir = uji(k, base)
        if status == "AKTIF":
            masih_hidup += 1
        tanda = {"DITOLAK": "  OK  ", "AKTIF": " BAHAYA",
                 "RALAT": "  ?   "}.get(status, "  ?   ")
        print(f"  {tanda} {mask_key(k):28} {status:8} {butir}")

    # ---- kunci semasa ----
    print("\n  Kunci yang sedang digunakan apl")
    print("  " + "-" * 56)
    semasa = get_api_key()
    if not semasa:
        print("         (tiada kunci disimpan)")
        print("         gear → Tetapan API untuk memasukkannya")
    elif semasa in KUNCI_TERDEDAH:
        print(f"   BAHAYA {mask_key(semasa)}")
        print("         Apl masih menggunakan kunci yang TERDEDAH.")
        print("         Ganti selepas revoke — lihat REVOKE_KUNCI.md")
    else:
        status, butir = uji(semasa, base)
        tanda = "  OK  " if status == "AKTIF" else " GAGAL"
        print(f"  {tanda} {mask_key(semasa):28} {status:8} {butir}")

    # ---- rumusan ----
    print("\n" + "=" * 60)
    if masih_hidup:
        print(f"  {masih_hidup} kunci terdedah MASIH AKTIF.")
        print("  Sesiapa yang ada kunci itu boleh habiskan kuota anda.")
        print("\n  Langkah: buka REVOKE_KUNCI.md")
        print("           atau terus ke developer.hadis.my/dashboard/keys")
    else:
        print("  Semua kunci terdedah sudah tidak sah. Selamat.")
    print("=" * 60 + "\n")
    return 1 if masih_hidup else 0


if __name__ == "__main__":
    sys.exit(main())
