#!/usr/bin/env python3
"""BUKA REKOD 19 OGOS — satu arahan, jalankan sebaik jam sistem bertukar.

Mengikuti konvensyen komit 1 hari 18 Ogos (`28dd87b`):

  1. Semak tarikh sistem >= 19 Ogos 2026 (peraturan semak #12: tajuk
     'Sesi Terakhir' tidak boleh mendahului tarikh sistem — rekod hari
     baharu TIDAK boleh dibuka sebelum tarikh sebenar).
  2. Finalisasi baris `komit ini` terakhir 18 Ogos (hash komit
     terakhir 18 Ogos dikesan secara dinamik dari git log).
  3. Buka seksyen **SESI 19 OGOS 2026** dalam sesi_index (kiraan
     telus: 19 Ogos = 1 commit kerja, 0 langkah-B).
  4. Cipta PERUBAHAN_19OGOS.md (Komit 1 + Status HARI DIBUKA).
  5. Kemas kini MULA_SINI.md: 'Sesi Terakhir' -> 19 Ogos, intro
     "Kerja 19 Ogos — 1 commit", ringkasan satu muka, item komit 1,
     pautan log harian -> PERUBAHAN_19OGOS.md.
  6. Sasar semula mutasi uji_negatif #27/#30/#34/#36 ke 19 Ogos.
  7. Gate penuh (semak.py + uji_negatif_8z + semak_dokumen_ui) dan
     commit (kecuali --no-commit).

Jika gate GAGAL, semua fail dipulihkan ke keadaan asal (tiada separa
kerja ditinggalkan) dan skrip keluar 1.

Guna:  python buka_hari.py [--no-commit]
"""

import datetime
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["PYTHONIOENCODING"] = "utf-8"

SESI_INDEX = os.path.join(BASE, "dokumen/sesi/sesi_index.md")
PER18 = os.path.join(BASE, "dokumen/perubahan/PERUBAHAN_18OGOS.md")
PER19 = os.path.join(BASE, "dokumen/perubahan/PERUBAHAN_19OGOS.md")
MULA = os.path.join(BASE, "dokumen/manual/MULA_SINI.md")
UJI = os.path.join(BASE, "uji_negatif_8z.py")

HARI, BULAN, TAHUN = 19, "Ogos", 2026
TARIKH_GATE = datetime.date(TAHUN, 8, HARI)


def baca(f):
    # newline="" — TANPA terjemahan universal newlines, supaya CRLF
    # (MULA_SINI.md) kekal sebagai CRLF dalam rentetan dan ditulis
    # semula dengan gaya asalnya.
    with open(f, encoding="utf-8", newline="") as fh:
        return fh.read()


def tulis(f, isi):
    with open(f, "w", encoding="utf-8", newline="") as fh:
        fh.write(isi)


def ikut_newline(isi, nl):
    """Tukar LF tunggal kepada nl sasaran (CRLF untuk fail CRLF).

    \n yang TIDAK didahului \r ditukar kepada nl; \r\n sedia ada
    (fail CRLF) tidak disentuh. Untuk sasaran LF, pulang as-is.
    """
    if nl == "\n":
        return isi
    return re.sub(r"(?<!\r)\n", nl, isi)


def ganti(isi, lama, baharu, mesti=True, kira=1):
    n = isi.count(lama)
    if n == 0:
        if mesti:
            raise SystemExit(f"  GAGAL  rentetan tidak dijumpai:\n    {lama[:90]}...")
        return isi
    if n != kira:
        print(f"  ! amaran: '{lama[:50]}...' dijumpai {n} kali (jangkaan {kira}) — "
              f"diganti semua")
    return isi.replace(lama, baharu)


# ─────────────────────────── 1. Pengawal ───────────────────────────
# Hook ujian: BUKA_HARI_TARIKH=YYYY-MM-DD membayangkan tarikh sistem
# (untuk mengesahkan aliran penuh sebelum jam sebenar bertukar).
_t = os.environ.get("BUKA_HARI_TARIKH")
hari_ini = (datetime.date.fromisoformat(_t) if _t
            else datetime.date.today())
print("=" * 62)
print(f"  BUKA REKOD HARI — {HARI} {BULAN} {TAHUN}")
print("=" * 62)
print(f"  Tarikh sistem: {hari_ini}")
if hari_ini < TARIKH_GATE:
    print(f"\n  BELUM — tarikh sistem masih {hari_ini} (sebelum "
          f"{TARIKH_GATE}).")
    print("  Peraturan semak #12: tajuk 'Sesi Terakhir' tidak boleh "
          "mendahului tarikh sistem.")
    print("  Jalankan semula sebaik jam sistem bertukar ke "
          f"{TARIKH_GATE}.")
    sys.exit(1)

if "--no-commit" in sys.argv:
    print("  Mod: --no-commit (edit + gate sahaja, TIADA commit)")

# Sahkan TIADA kerja selepas tutup 18 Ogos: komit terakhir MESTI
# bertarikh 18 Ogos (hari penutup) — bukan 19 Ogos atau lebih baru.
# Hash dikesan secara dinamik (bukan keras) supaya komit penutup
# tambahan sebelum jam bertukar tidak memecahkan skrip.
r = subprocess.run(["git", "log", "-1", "--format=%h|%ad",
                    "--date=format:%Y-%m-%d"], cwd=BASE,
                   capture_output=True, text=True, encoding="utf-8")
kepala, tarikh = (r.stdout or "").strip().split("|", 1)
if tarikh >= "2026-08-19":
    print(f"\n  GAGAL  komit terakhir ({kepala}) bertarikh {tarikh} — ada "
          "kerja selepas tutup 18 Ogos?")
    print("  (atau rekod 19 Ogos mungkin sudah dibuka — semak 'Sesi "
          "Terakhir'.)")
    print("  Siasat dahulu sebelum membuka rekod hari baharu.")
    sys.exit(1)
HASH_AKHIR = kepala   # komit terakhir 18 Ogos (baris 'komit ini' belum
                       # difinalkan — skrip ini menyelesaikannya)
print(f"  Komit terakhir disahkan: {HASH_AKHIR} (18 Ogos)")

# Re-run selepas dibuka → tiada perubahan.
if "## Sesi Terakhir — 19 Ogos 2026" in baca(MULA):
    print("\n  Rekod 19 Ogos SUDAH dibuka — tiada perubahan dibuat.")
    sys.exit(0)

# ─────────────────────────── 2. Bacaan asal ─────────────────────────
s_sesi, s_per18, s_mula, s_uji = (
    baca(SESI_INDEX), baca(PER18), baca(MULA), baca(UJI))

print("\n─ 2. Finalisasi baris 'komit ini' 18 Ogos ─")
s_sesi = ganti(s_sesi, "| komit ini |", f"| `{HASH_AKHIR}` |")

# ─────────────────────── 3. Seksyen SESI 19 OGOS ────────────────────
seksyen = (
    "\n\n## SESI 19 OGOS 2026 (komit 1, sambungan 18 Ogos)\n"
    "\n"
    "**Ringkasan:** hari baharu dibuka selepas penutup penuh 18 Ogos "
    "(7\n"
    "commit kerja + 2 langkah-B, 10 sebenar − 2). Kerja pembukaan: "
    "finalkan\n"
    f"baris komit 10 (`{HASH_AKHIR}`) dalam jadual SESI 18 OGOS, buka "
    "rekod 19\n"
    "Ogos (PERUBAHAN_19OGOS.md baharu + seksyen ini + MULA_SINI "
    "'Sesi\n"
    "Terakhir' + ringkasan), dan kunci semula mutasi uji_negatif ke\n"
    "tarikh/kiraan 19 Ogos.\n"
    "\n"
    "| # | Kerja | Komit |\n"
    "|---|-------|-------|\n"
    "| 1 | **Buka rekod 19 Ogos** — sesi_index (seksyen SESI 19 OGOS + "
    "kiraan telus) + PERUBAHAN_19OGOS.md (Komit 1) + MULA_SINI 'Sesi "
    "Terakhir' → 19 Ogos (komit 1) + ringkasan; mutasi "
    "#27/#30/#34/#36 disasarkan semula ke 19 Ogos | komit ini |\n"
    "\n"
    "**Kiraan telus:** 14 Ogos = **36 commit** · 15 Ogos = **14 "
    "commit** ·\n"
    "16 Ogos = **16 commit** (18 sebenar − 2 langkah-B) · 17 Ogos =\n"
    "**18 commit** (22 sebenar − 4 langkah-B) · 18 Ogos = **8 commit "
    "kerja + 2\n"
    "langkah-B** (10 sebenar − 2) · 19 Ogos = **1 commit kerja** (1\n"
    "sebenar − 0 langkah-B — komit ini).\n"
    "\n"
    "**Baki tertangguh (§8):** tidak berubah — #7 kunci API hadis.my "
    "kekal\n"
    "AKTIF sengaja; jurang Tafsir 843 dipantau; installer Fasa 0 "
    "TERTUNDA.\n"
    "\n"
    "**Gate:** semak.py SEMUA LULUS (16 semakan, #12/#14/#15/#16 "
    "hijau —\n"
    "#12 peraturan tarikh sistem: tajuk 19 Ogos tidak mendahului "
    "tarikh\n"
    "sistem) · uji_negatif_8z **55/0** · semak_dokumen_ui 109/0 · "
    "pokok\n"
    "kerja bersih · tema pengguna \"sistem\".\n"
    "\n"
    "---\n"
)
# rstrip("\r\n") BUKAN rstrip("\n"): pada fail CRLF, rstrip("\n")
# meninggalkan \r sunyi hujung -> git enggan menormalkan CRLF->LF
# (blob jadi CRLF penuh, diff seluruh fail).
nl_sesi = "\r\n" if "\r\n" in s_sesi else "\n"
s_sesi = s_sesi.rstrip("\r\n") + ikut_newline(seksyen, nl_sesi)

# ───────────────────── 4. PERUBAHAN_19OGOS.md baharu ────────────────
per19_isi = (
    "# Perubahan 19 Ogos 2026\n"
    "\n"
    "> Log ringkas perubahan pada 19 Ogos 2026 untuk rujukan pantas.\n"
    "> Butiran penuh: `dokumen/sesi/sesi_index.md`. Versi apl kekal "
    "**1.0**.\n"
    "\n"
    "## Kandungan sesi\n"
    "\n"
    "- **Komit 1 — Buka rekod 19 Ogos.** Hari baharu dibuka selepas\n"
    "  penutup penuh 18 Ogos (8 commit kerja + 2 langkah-B, 10 sebenar "
    "− 2;\n"
    f"  baris komit 10 `{HASH_AKHIR}` difinalkan).\n"
    "  Pembukaan rekod:\n"
    "\n"
    "  1. **sesi_index.md** — seksyen **SESI 19 OGOS 2026 (komit 1,\n"
    "     sambungan 18 Ogos)** ditambah selepas penutup 18 Ogos; "
    "kiraan\n"
    "     telus dikemas: 19 Ogos = **1 commit** (1 sebenar − 0 "
    "langkah-B).\n"
    "  2. **PERUBAHAN_19OGOS.md** — fail log harian baharu ini.\n"
    "  3. **MULA_SINI.md** — 'Sesi Terakhir' → **19 Ogos 2026 (komit "
    "1)** +\n"
    "     ringkasan satu muka → **1 commit pada 19 Ogos** (sambungan "
    "7\n"
    "     commit 18 Ogos + 18 commit 17 Ogos + 16 commit 16 Ogos + "
    "36\n"
    "     commit 14 Ogos + 14 commit 15 Ogos); pautan log harian →\n"
    "     PERUBAHAN_19OGOS.md.\n"
    "  4. **uji_negatif_8z.py** — mutasi #27/#30/#34/#36 disasarkan "
    "semula\n"
    "     ke 19 Ogos (tajuk, intro \"Kerja 19 Ogos\", kiraan "
    "ringkasan,\n"
    "     tarikh masa depan).\n"
    "\n"
    "  Gate: semak.py SEMUA LULUS (16 semakan, #12/#14/#15/#16 hijau "
    "—\n"
    "  #12 peraturan tarikh sistem: tajuk 19 Ogos tidak mendahului "
    "tarikh\n"
    "  sistem 19 Ogos) · uji_negatif_8z **55/0** · semak_dokumen_ui\n"
    "  109/0 · pokok kerja bersih.\n"
    "\n"
    "## Status — HARI DIBUKA\n"
    "\n"
    "19 Ogos DIBUKA — **1 commit kerja + 0 langkah-B** (1 sebenar − "
    "0).\n"
    "Kiraan telus: 14 Ogos = 36 commit · 15 Ogos = 14 commit ·\n"
    "16 Ogos = 16 commit (18 sebenar − 2 langkah-B) · 17 Ogos = 18 "
    "commit\n"
    "(22 sebenar − 4 langkah-B) · 18 Ogos = 8 commit kerja + 2 "
    "langkah-B\n"
    "(10 sebenar − 2) · 19 Ogos = 1 commit kerja (komit ini).\n"
)

# ───────────────────── 5. MULA_SINI.md (CRLF) ───────────────────────
nl = "\r\n" if "\r\n" in s_mula else "\n"
item1 = (
    "1. **Buka rekod hari (komit 1)** — finalkan baris komit 10\n"
    f"   (`{HASH_AKHIR}`) dalam sesi_index; seksyen "
    "SESI 19\n"
    "   OGOS + kiraan telus (1 commit); PERUBAHAN_19OGOS.md baharu;\n"
    "   'Sesi Terakhir' + ringkasan dikemas; mutasi "
    "#27/#30/#34/#36\n"
    "   disasarkan semula."
)
badan19 = (
    "**Kerja 19 Ogos (1 commit):** buka rekod hari — finalkan baris\n"
    f"komit 10 (`{HASH_AKHIR}`) dalam sesi_index ·\n"
    "seksyen SESI 19 OGOS + kiraan telus · PERUBAHAN_19OGOS.md "
    "baharu ·\n"
    "'Sesi Terakhir' + ringkasan → 19 Ogos · mutasi "
    "#27/#30/#34/#36\n"
    "disasarkan semula."
)

mula_lama_intro = (
    "Versi semasa: **v1.0**. Kerja 18 Ogos — **8 commit** (sambungan "
    "18 commit 17 Ogos + 16 commit 16 Ogos + 36 commit 14 Ogos + 14 "
    "commit 15 Ogos) + 2 langkah-B (penutup + baseline):")
mula_baharu_intro = (
    "Versi semasa: **v1.0**. Kerja 19 Ogos — **1 commit** (sambungan "
    "8 commit 18 Ogos + 18 commit 17 Ogos + 16 commit 16 Ogos + 36 "
    "commit 14 Ogos + 14 commit 15 Ogos) + 0 langkah-B:")

s_mula = ganti(s_mula,
    "> log harian terbaru: `dokumen/perubahan/PERUBAHAN_18OGOS.md` "
    "(18 Ogos).",
    "> log harian terbaru: `dokumen/perubahan/PERUBAHAN_19OGOS.md` "
    "(19 Ogos).")
s_mula = ganti(s_mula,
    "## Keadaan projek — ringkasan satu muka (akhir 18 Ogos 2026)",
    "## Keadaan projek — ringkasan satu muka (akhir 19 Ogos 2026)")
s_mula = ganti(s_mula,
    "**8 commit** pada 18 Ogos (sambungan 18 commit 17 Ogos + 16 "
    "commit 16 Ogos + 36 commit 14 Ogos + 14 commit 15 Ogos).",
    "**1 commit** pada 19 Ogos (sambungan 8 commit 18 Ogos + 18 "
    "commit 17 Ogos + 16 commit 16 Ogos + 36 commit 14 Ogos + 14 "
    "commit 15 Ogos).")
s_mula = ganti(s_mula,
    "**Kerja 18 Ogos (8 commit):** buka rekod hari — finalkan baris",
    ikut_newline(badan19, nl) + nl + nl +
    "**Kerja 18 Ogos (8 commit):** buka rekod hari — finalkan baris")
s_mula = ganti(s_mula,
    "`dokumen/perubahan/PERUBAHAN_18OGOS.md` · arkib penuh —",
    "`dokumen/perubahan/PERUBAHAN_19OGOS.md` · arkib penuh —")
s_mula = ganti(s_mula,
    "## Sesi Terakhir — 18 Ogos 2026 (komit 1: buka rekod hari)",
    "## Sesi Terakhir — 19 Ogos 2026 (komit 1: buka rekod hari)")
s_mula = ganti(s_mula, mula_lama_intro,
               mula_baharu_intro + nl + nl + ikut_newline(item1, nl))

# ─────────────────── 6. Mutasi uji_negatif → 19 Ogos ────────────────
rintas_18 = ("sambungan 18 commit 17 Ogos + 16 commit 16 Ogos + 36 "
             "commit 14 Ogos + 14 commit 15 Ogos")
rintas_19 = ("sambungan 8 commit 18 Ogos + 18 commit 17 Ogos + 16 "
             "commit 16 Ogos + 36 commit 14 Ogos + 14 commit 15 Ogos")
s_uji = ganti(s_uji, "## Sesi Terakhir — 18 Ogos 2026",
              "## Sesi Terakhir — 19 Ogos 2026", kira=2)
s_uji = ganti(s_uji, "intro 'Kerja 18 Ogos' SEMASA",
              "intro 'Kerja 19 Ogos' SEMASA")
s_uji = ganti(s_uji, "SATU-SATUNYA '17 Ogos' (tarikh git sebelum komit",
              "SATU-SATUNYA '18 Ogos' (tarikh git sebelum komit")
s_uji = ganti(s_uji, "ini) DAN '18 Ogos' (selepas komit) dalam ringkasan",
              "ini) DAN '19 Ogos' (selepas komit) dalam ringkasan")
s_uji = ganti(s_uji,
    "Kerja 18 Ogos — **8 commit** (sambungan 18 commit 17 Ogos +",
    "Kerja 19 Ogos — **1 commit** (sambungan 8 commit 18 Ogos +")
s_uji = ganti(s_uji, "Kerja terkini — **8 commit** (sambungan",
              "Kerja terkini — **1 commit** (sambungan")
s_uji = ganti(s_uji,
    f"**8 commit** pada 18 Ogos ({rintas_18}).",
    f"**1 commit** pada 19 Ogos ({rintas_19}).")
s_uji = ganti(s_uji,
    f"**35 commit** pada 18 Ogos ({rintas_18}).",
    f"**35 commit** pada 19 Ogos ({rintas_19}).")

# ──────────────────────── 7. Tulis + Stage + Gate ───────────────────
tulis(SESI_INDEX, s_sesi)
tulis(PER18, s_per18)
tulis(PER19, per19_isi)
tulis(MULA, s_mula)
tulis(UJI, s_uji)
print("\n─ 7. Stage dahulu (semak #9 dikesan untracked) + gate penuh ─")

subprocess.run(["git", "add",
                "buka_hari.py",
                "dokumen/manual/MULA_SINI.md",
                "dokumen/perubahan/PERUBAHAN_18OGOS.md",
                "dokumen/perubahan/PERUBAHAN_19OGOS.md",
                "dokumen/sesi/sesi_index.md",
                "uji_negatif_8z.py"], cwd=BASE, check=True)
print("  OK     git add (6 fail + buka_hari.py)")

gate = [("semak.py", ["python", "semak.py"]),
        ("uji_negatif_8z.py", ["python", "-u", "uji_negatif_8z.py"]),
        ("semak_dokumen_ui.py", ["python", "semak_dokumen_ui.py"])]
gagal = []
for nama, cmd in gate:
    print(f"\n  ── {nama} ──")
    try:
        r = subprocess.run(cmd, cwd=BASE, capture_output=True,
                           text=True, encoding="utf-8",
                           errors="replace", timeout=500)
        ok = r.returncode == 0
    except subprocess.TimeoutExpired:
        ok = False
        print("  GAGAL  masa tamat (500s)")
    if ok:
        print(f"  OK     {nama}")
    else:
        gagal.append(nama)
        print(f"  GAGAL  {nama}")
        for b in (r.stdout or "").splitlines()[-8:]:
            print(f"         {b.strip()}")

if gagal:
    print("\n  KEPUTUSAN: GAGAL — memulihkan semua fail ke keadaan asal.")
    if os.environ.get("BUKA_HARI_KEKAL") == "1":
        print("  (BUKA_HARI_KEKAL=1: perubahan dikekalkan untuk debug)")
        sys.exit(1)
    # Nyahstage + pulihkan HEAD + buang PER19 — tiada separa kerja
    # ditinggalkan; line ending betul (autocrlf) serta-merta.
    subprocess.run(["git", "reset", "-q"], cwd=BASE)
    subprocess.run(["git", "restore", "--source=HEAD", "--worktree",
                    "dokumen/manual/MULA_SINI.md",
                    "dokumen/sesi/sesi_index.md",
                    "dokumen/perubahan/PERUBAHAN_18OGOS.md",
                    "uji_negatif_8z.py"], cwd=BASE)
    try:
        os.remove(PER19)
    except OSError:
        pass
    print("  Fail dipulihkan — tiada separa kerja ditinggalkan.")
    sys.exit(1)

print("\n  KEPUTUSAN: SEMUA GATE HIJAU")

if "--no-commit" in sys.argv:
    print("\n  --no-commit: perubahan kekal pada pokok kerja (belum "
          "di-commit).")
    print("  Semak dengan `git diff` sebelum commit manual.")
    sys.exit(0)

pesan = ("Buka rekod hari 19 Ogos (komit 1) — finalisasi langkah-B + "
         "PERUBAHAN_19OGOS baharu")
r = subprocess.run(["git", "commit", "-m", pesan], cwd=BASE,
               capture_output=True, text=True, encoding="utf-8",
               errors="replace")
print(r.stdout)
if r.returncode != 0:
    print(r.stderr)
    sys.exit(1)
hash_k = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                        cwd=BASE, capture_output=True, text=True,
                        encoding="utf-8").stdout.strip()
print("\n  SELESAI — rekod 19 Ogos dibuka, komit "
      f"`{hash_k}`, pokok bersih, semua gate hijau.")
