#!/usr/bin/env python3
"""GATE PANTAS — semakan pantas sebelum setiap commit kecil (~45 saat).

Menjalankan dua gate teras dengan satu arahan: semak.py (semua semakan
statik + data) dan uji_negatif_8z (kepekaan mutasi). Ditambah semakan
pokok kerja BERSIH (fail tidak di-commit boleh menandakan kerja separa).
Suite penuh 13 ujian tetap perlu dijalankan sebelum hantar besar:
`python uji_pra_hantar.py`.

    python gate_pantas.py

Urutan:
  1. git status --porcelain — pokok kerja bersih (amaran jika tidak)
  2. semak.py            (semakan statik + data, SEMUA LULUS)
  3. uji_negatif_8z.py   (kepekaan mutasi, 47/0)

Keluar 0 jika semua lulus; 1 jika mana-mana gagal.
"""

import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["PYTHONIOENCODING"] = "utf-8"

GATE = [
    ("1. semak.py", ["python", "semak.py"]),
    ("2. uji_negatif_8z.py", ["python", "-u", "uji_negatif_8z.py"]),
]

print("=" * 62)
print("  GATE PANTAS — Pustaka Hadis (semak.py + uji_negatif_8z)")
print("=" * 62)

gagal = False

# 0. Pokok kerja bersih — amaran (bukan GAGAL: kerja separa sah semasa
#    menulis; tetapi gate dijalankan selepas commit biasanya bersih).
try:
    r = subprocess.run(["git", "status", "--porcelain"], cwd=BASE,
                       capture_output=True, text=True, encoding="utf-8")
    belum = [b for b in (r.stdout or "").splitlines() if b.strip()]
    if belum:
        print(f"  ! {len(belum)} fail belum di-commit (kerja separa?) — "
              f"contoh: {belum[0]}")
    else:
        print("  OK     pokok kerja bersih")
except Exception:
    print("  ! git status gagal (di luar repo?) — langkau")

t0 = __import__("time").perf_counter()
for nama, cmd in GATE:
    print(f"\n  ── {nama} ──")
    t1 = __import__("time").perf_counter()
    try:
        r = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
        ok = r.returncode == 0
    except subprocess.TimeoutExpired:
        ok = False
        print("  GAGAL  masa tamat (300s)")
    tempoh = __import__("time").perf_counter() - t1
    if ok:
        print(f"  OK     {nama} ({tempoh:.1f}s)")
    else:
        gagal = True
        print(f"  GAGAL  {nama} ({tempoh:.1f}s)")
        baris = (r.stdout or "").splitlines()
        for b in reversed(baris):
            if any(k in b for k in ("KEPUTUSAN", "GAGAL", "KEGAGALAN",
                                    "SEMUA", "Traceback")):
                print(f"         {b.strip()}")
                break

jumlah = __import__("time").perf_counter() - t0
print(f"\n  Jumlah masa: {jumlah:.1f}s")
if gagal:
    print("  KEPUTUSAN: GAGAL — betulkan dahulu sebelum commit")
    sys.exit(1)
print("  KEPUTUSAN: SEMUA LULUS — selamat di-commit (suite penuh untuk hantar besar)")
sys.exit(0)
