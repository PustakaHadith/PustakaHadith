"""Tarikh Hijri (kalendar Islam tabular/Kuwaiti) + nama bulan.

Item 8 (Sesi 36): paparan tarikh baris "HARI INI" halaman Utama —
pilihan Melayu, Masihi, Hijri, atau Hijri + Melayu (Tetapan →
Paparan tarikh, kunci `tarikh_paparan`).

Algoritma tabular (Kuwaiti) — standard ringkas tanpa kebergantungan
luar; boleh berbeza ±1 hari dengan kalendar Umm al-Qura rasmi
(pengisytiharan rukyah bulan).
"""

from __future__ import annotations

import datetime

BULAN_HIJRI = (
    "Muharram", "Safar", "Rabiulawal", "Rabiulakhir",
    "Jumadilawal", "Jumadilakhir", "Rejab", "Syaaban",
    "Ramadan", "Syawal", "Zulqaedah", "Zulhijah",
)

BULAN_MELAYU = (
    "Januari", "Februari", "Mac", "April", "Mei", "Jun",
    "Julai", "Ogos", "September", "Oktober", "November", "Disember",
)


def _jd_masihi(tahun: int, bulan: int, hari: int) -> int:
    """Julian Day daripada tarikh Masihi (Gregorian)."""
    a = (14 - bulan) // 12
    y = tahun + 4800 - a
    m = bulan + 12 * a - 3
    return (hari + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100
            + y // 400 - 32045)


def ke_hijri(tarikh: datetime.date) -> tuple[int, int, int]:
    """Masihi → (tahun, bulan 1-12, hari) Hijri — algoritma tabular."""
    jd = _jd_masihi(tarikh.year, tarikh.month, tarikh.day)
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + \
        (l // 5670) * ((43 * l) // 15238)
    l = (l - ((30 - j) // 15) * ((17719 * j) // 50)
         - (j // 16) * ((15238 * j) // 43) + 29)
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    return y, m, d


def teks_hijri(tarikh: datetime.date) -> str:
    """'14 Rabiulawal 1448H'."""
    y, m, d = ke_hijri(tarikh)
    return f"{d} {BULAN_HIJRI[m - 1]} {y}H"


def teks_melayu(tarikh: datetime.date) -> str:
    """'26 September 2026' — nama bulan Bahasa Melayu."""
    return f"{tarikh.day} {BULAN_MELAYU[tarikh.month - 1]} {tarikh.year}"
