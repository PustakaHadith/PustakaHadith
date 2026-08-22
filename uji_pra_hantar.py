#!/usr/bin/env python3
"""UJIAN PRA-HANTAR automatik — selesaikan suite penuh dengan satu arahan.

Menjalankan SEMUA ujian secara berurutan (model carian dimuat sekali,
jadi ujian seterusnya pantas), menangkap output setiap ujian, dan
melaporkan ringkasan. Berhenti awal (exit 1) apabila satu ujian gagal
-- jangan teruskan supaya punca regresi jelas.

    python uji_pra_hantar.py [--teruskan]

Urutan (model dimalat sekali pada ujian pertama yang memerlukannya):

  1. semak.py                     (semakan statik + data, SEMUA LULUS)
  2. uji_negatif_8z.py            (kepekaan mutasi, 45/0)
  3. uji_visual_mockup.py         (kontrak 4 mockup vs app, 130/0)
  4. uji_visual_piksel.py         (perbandingan piksel palet, 53/0)
  5. uji_visual_sebenar.py        (skrin fizikal, 65/0)
  6. uji_tukar_tema.py            (tema gelap/terang, 19/19)
  7. uji_bandingan.py             (3 tab bahasa + sama paras, 55/0)
  8. uji_lompat_fungsi.py         (lompat hadis, 48/0)
  9. uji_end_to_end.py            (aliran penuh, 18/0)
 10. bina_tangkapan_dokumentasi.py (baseline dokumen, 7/7)
 11. uji_draf_jawapan.py          (draf AI: exact_results + Carian Biasa, 9/0)
 12. uji_tersimpan_sebenar.py     (halaman Tersimpan, tanda buku SEBENAR, 20/0)
 13. semak_dokumen_ui.py          (audit dokumen manual vs UI sebenar, 109/0)
 14. uji_responsif_viewport.py     (6 halaman × 4 saiz, DPI 150%, 76/0)

`--teruskan`: jangan berhenti bila gagal; jalankan semua dan laporkan.

Skrip TIDAK mengubah apa-apa fail (setiap ujian memulihkan sendiri).
Tidak seperti ujian visual lain, skrip ini sendiri TIDAK membuka
tetingkap -- ia melancarkan ujian sebagai subproses.
"""

import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["PYTHONIOENCODING"] = "utf-8"

UJIAN = [
    ("1. semak.py", ["python", "semak.py"], 300),
    ("2. uji_negatif_8z.py", ["python", "-u", "uji_negatif_8z.py"], 240),
    ("3. uji_visual_mockup.py", ["python", "-u", "uji_visual_mockup.py"], 300),
    ("4. uji_visual_piksel.py", ["python", "-u", "uji_visual_piksel.py"], 300),
    ("5. uji_visual_sebenar.py", ["python", "-u", "uji_visual_sebenar.py"], 300),
    ("6. uji_tukar_tema.py", ["python", "-u", "uji_tukar_tema.py"], 300),
    ("7. uji_bandingan.py", ["python", "-u", "uji_bandingan.py"], 400),
    ("8. uji_lompat_fungsi.py", ["python", "-u", "uji_lompat_fungsi.py"], 400),
    ("9. uji_end_to_end.py", ["python", "-u", "uji_end_to_end.py"], 300),
    ("10. bina_tangkapan_dokumentasi.py",
     ["python", "-u", "bina_tangkapan_dokumentasi.py"], 240),
    ("11. uji_draf_jawapan.py", ["python", "-u", "uji_draf_jawapan.py"], 120),
    ("12. uji_tersimpan_sebenar.py",
     ["python", "-u", "uji_tersimpan_sebenar.py"], 180),
    ("13. semak_dokumen_ui.py", ["python", "-u", "semak_dokumen_ui.py"], 120),
    ("14. uji_responsif_viewport.py",
     ["python", "-u", "uji_responsif_viewport.py"], 180),
]

teruskan = "--teruskan" in sys.argv
log_dir = os.path.join(BASE, "bukti_visual")
os.makedirs(log_dir, exist_ok=True)


SASARAN_ORPHAN = ("uji_", "semak.py", "semak_dokumen_ui.py",
                   "bina_tangkapan_dokumentasi.py", "profil_semak.py")


def _cari_orphan() -> list:
    """Pulangkan [(pid, cmdline)] proses ujian YATIM dalam BASE.

    Kriteria sama untuk pembersihan awal DAN semakan akhir (pengesahan
    dua hala): skrip UJIAN projek dalam BASE (`uji_*`, `semak.py`,
    `bina_tangkapan_dokumentasi.py`, dsb.) — BUKAN `main.py`/`sync.py`
    (app/tugas pengguna) dan BUKAN proses semasa. psutil pilihan:
    tiada psutil -> senarai kosong (suite tetap jalan).
    """
    try:
        import psutil
    except ImportError:
        return []
    dapati = []
    for proc in psutil.process_iter(["pid", "name", "cmdline", "cwd"]):
        try:
            if proc.info["pid"] == os.getpid():
                continue
            nama = (proc.info["name"] or "").lower()
            if not nama.startswith("python"):
                continue
            cmd = " ".join(proc.info["cmdline"] or [])
            cwd = proc.info["cwd"] or ""
            if cwd != BASE or not any(s in cmd for s in SASARAN_ORPHAN):
                continue
            dapati.append((proc.info["pid"], cmd))
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
            continue
    return dapati


def _bersihkan_orphan() -> int:
    """Bunuh proses ujian YATIM (larian tergantung) sebelum suite mula.

    Bila induk uji_pra_hantar dibunuh (tool timeout dsb.), subproses
    ujian Windows terus hidup (~1 GB setiap satu — model AI dimuat) dan
    memperlahankan larian seterusnya sehingga "hang" di Loading weights.
    """
    dibunuh = []
    for pid, cmd in _cari_orphan():
        try:
            import psutil
            psutil.Process(pid).kill()
            dibunuh.append(f"{pid}: {cmd}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
            continue
    if dibunuh:
        print(f"  * {len(dibunuh)} proses ujian yatim dibunuh (larian "
              f"tergantung sebelum ini):")
        for d in dibunuh:
            print(f"    - {d}")
    return len(dibunuh)


def _semak_orphan_selepas() -> int:
    """Pengesahan DUA HALA: selepas suite, tiada proses ujian yatim patut tinggal.

    Subproses ujian yang bersih mesti keluar sendiri; apa-apa yang tinggal
    menunjukkan ujian tidak memulihkan keadaan (regresi) atau subproses
    menggantung dan terselamat daripada timeout.
    """
    dapati = _cari_orphan()
    if dapati:
        print(f"  GAGAL  {len(dapati)} proses ujian yatim MASIH TINGGAL "
              f"selepas suite:")
        for pid, cmd in dapati:
            print(f"    - {pid}: {cmd}")
    else:
        print("  OK     tiada proses ujian yatim selepas suite")
    return len(dapati)


if "--bersihkan" in sys.argv:
    n = _bersihkan_orphan()
    print(f"  Bersih selesai: {n} proses yatim dibunuh")
    sys.exit(0)

print("=" * 62)
print("  UJIAN PRA-HANTAR — Pustaka Hadis")
print("=" * 62)
_bersihkan_orphan()

hasil = []
gagal_ada = False
t0 = time.perf_counter()
for nama, cmd, had in UJIAN:
    print(f"\n  ── {nama} ──")
    log = os.path.join(log_dir,
                       f"pra_hantar_{cmd[-1].replace('.py', '')}.log")
    t1 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=had)
        tempoh = time.perf_counter() - t1
        ok = r.returncode == 0
    except subprocess.TimeoutExpired:
        tempoh = time.perf_counter() - t1
        ok = False
        print(f"  GAGAL  {nama} — MASA TAMAT ({had}s)")
        with open(log, "w", encoding="utf-8") as f:
            f.write("[TIMEOUT]\n")
        hasil.append((nama, ok, tempoh, log))
        gagal_ada = True
        if not teruskan:
            break
        continue
    except Exception as e:
        tempoh = time.perf_counter() - t1
        ok = False
        print(f"  GAGAL  {nama} — {type(e).__name__}: {e}")
        hasil.append((nama, ok, tempoh, log))
        gagal_ada = True
        if not teruskan:
            break
        continue

    with open(log, "w", encoding="utf-8", errors="replace") as f:
        f.write(r.stdout or "")
        f.write(r.stderr or "")
    if ok:
        print(f"  OK     {nama} ({tempoh:.1f}s) — log: {log}")
    else:
        print(f"  GAGAL  {nama} ({tempoh:.1f}s) — log: {log}")
        # Papar baris keputusan / kegagalan terakhir dari output
        baris = (r.stdout or "").splitlines()
        for b in reversed(baris):
            if any(k in b for k in ("KEPUTUSAN", "GAGAL", "KEGAGALAN",
                                    "SEMUA", "Traceback")):
                print(f"         {b.strip()}")
                break
    hasil.append((nama, ok, tempoh, log))
    if not ok:
        gagal_ada = True
        if not teruskan:
            break

# Pengesahan DUA HALA: bersihkan pada mula, sahkan BERSIH pada akhir.
print()
sisa = _semak_orphan_selepas()
if sisa:
    gagal_ada = True

jumlah = time.perf_counter() - t0
print("\n" + "=" * 62)
print("  RINGKASAN PRA-HANTAR")
print("=" * 62)
for nama, ok, t, log in hasil:
    print(f"  {'OK    ' if ok else 'GAGAL '}{nama:26s} {t:6.1f}s")
print(f"\n  Jumlah masa: {jumlah:.1f}s")
print("  Log: bukti_visual/pra_hantar_*.log")
if gagal_ada:
    print("  KEPUTUSAN: GAGAL — jangan hantar sebelum dibaiki")
    sys.exit(1)
print("  KEPUTUSAN: SEMUA LULUS — selamat dihantar")
sys.exit(0)
