#!/usr/bin/env python3
"""Ujian parser 'lompat ke hadis' — _parse_lompat / _slug_dari_awalan.

Melindungi regresi ejaan kitab & format lompat pada bar carian:
  'bukhari 433', 'bukhari:433', 'B433', 'bukhari433', 'b 433', '433'.
Tiada GUI diperlukan (offscreen). Jalankan:
    python uji_lompat.py
Keluar 0 jika semua lulus, 1 jika ada kegagalan.
"""

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

from ui.app_qt import _parse_lompat, _slug_dari_awalan

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


# ── Kes yang PATUT padan: (q, default_slug, jangkaan (slug, nombor)) ─
LULUS = [
    # nama penuh + nombor
    ("bukhari 433", None, ("bukhari", 433)),
    ("sahih bukhari 433", None, ("bukhari", 433)),
    ("shahih bukhari 433", None, ("bukhari", 433)),
    ("Sahih Bukhari 433", None, ("bukhari", 433)),
    ("abu daud 10", None, ("abu-daud", 10)),
    ("sunan abu dawud 5", None, ("abu-daud", 5)),
    ("tirmidzi 2", None, ("tirmidzi", 2)),
    ("jami at-tirmidzi 2", None, ("tirmidzi", 2)),
    ("nasa'i 5", None, ("nasai", 5)),
    ("sunan an-nasai 5", None, ("nasai", 5)),
    ("ibnu majah 3", None, ("ibnu-majah", 3)),
    ("Muwatta' Malik 12", None, ("malik", 12)),
    ("musnad ahmad 999", None, ("ahmad", 999)),
    ("muslim 5", None, ("muslim", 5)),
    ("muslim 0005", None, ("muslim", 5)),
    # pemisah titik bertindih
    ("bukhari:433", None, ("bukhari", 433)),
    ("b:433", None, ("bukhari", 433)),
    ("T:3", None, ("tirmidzi", 3)),
    ("bukhari : 433", None, ("bukhari", 433)),
    ("abu-daud:100", None, ("abu-daud", 100)),
    # tanpa pemisah (huruf + digit)
    ("B433", None, ("bukhari", 433)),
    ("bukhari433", None, ("bukhari", 433)),
    ("t5", None, ("tirmidzi", 5)),
    ("n10", None, ("nasai", 10)),
    ("i3", None, ("ibnu-majah", 3)),
    ("d7", None, ("darimi", 7)),
    # awalan ringkas UNIK (dengan ruang)
    ("b 433", None, ("bukhari", 433)),
    ("ab 5", None, ("abu-daud", 5)),
    ("musl 5", None, ("muslim", 5)),
    ("ma 5", None, ("malik", 5)),
    ("muw 5", None, ("malik", 5)),
    ("ah 5", None, ("ahmad", 5)),
    ("dar 7", None, ("darimi", 7)),
    # nombor sahaja — kitab lalai daripada pemanggil
    ("433", "muslim", ("muslim", 433)),
]

# ── Kes yang PATUT jatuh ke carian biasa (None) ────────────────────
# (q, default_slug)
BUKAN_LULUS = [
    ("433", None),                  # tiada kitab lalai -> bukan lompat
    ("cari sholat", None),
    ("10 hadis tentang sholat", None),
    ("bukhari 10 hadis", None),     # nombor bukan token terakhir
    ("433 bukhari", None),
    ("bukhari 433 555", None),      # nama + nombor + lebihan -> tiada padan
    ("bukhari", None),              # tiada nombor
    ("", "bukhari"),
    ("sahih 433", None),            # 'sahih' sahaja ambigu
    ("hukum riba", None),
    ("hukum: riba", None),
    ("hadis 10", None),
    # awalan AMBIGU — elak tekaan silap
    ("m 5", None),                  # muslim / malik
    ("a 5", None),                  # ahmad / abu-daud
    ("mu 5", None),                 # muslim / malik / musnad-*
    ("mus 5", None),                # muslim + musnad ahmad/darimi
    ("s 5", None),                  # sahih-* / sunan-* / shahih-*
]

# ── Awalan ringkas (_slug_dari_awalan): unik -> slug, ambigu -> None ─
AWALAN = {
    "b": "bukhari", "t": "tirmidzi", "n": "nasai",
    "i": "ibnu-majah", "d": "darimi",
    "ab": "abu-daud", "musl": "muslim", "ma": "malik",
    "muw": "malik", "ah": "ahmad", "dar": "darimi",
    "m": None, "a": None, "mu": None, "mus": None, "s": None,
}

print("=" * 62)
print("  UJIAN PARSER LOMPAT KE HADIS (_parse_lompat)")
print("=" * 62)

print("\n  1. Format lompat yang patut padan")
for q, d, exp in LULUS:
    got = _parse_lompat(q, default_slug=d)
    semak(f"{q!r} -> {exp[0]} {exp[1]}", got == exp, f"dapat {got!r}")

print("\n  2. Bukan lompat -> kekal carian biasa")
for q, d in BUKAN_LULUS:
    got = _parse_lompat(q, default_slug=d)
    semak(f"{q!r} -> None", got is None, f"dapat {got!r}")

print("\n  3. Awalan ringkas (_slug_dari_awalan)")
for awal, exp in AWALAN.items():
    got = _slug_dari_awalan(awal)
    semak(f"awalan {awal!r} -> {exp}", got == exp, f"dapat {got!r}")

print("\n" + "=" * 62)
print(f"  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 62)
sys.exit(1 if FAIL else 0)
