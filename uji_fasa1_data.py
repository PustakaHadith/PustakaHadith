"""Ujian Fasa 1 installer — pemisahan laluan data (INSTALLER.md §3).

Mensimulasikan sys.frozen=True dalam SUBPROSES supaya proses ujian ini
tidak terjejas, dan mengesahkan TIADA fail baharu ditulis ke folder
aplikasi (ASSET_DIR):

  1. Mod pembangunan (lalai): DATA_DIR == ASSET_DIR (folder projek).
  2. Mod frozen (simulasi):   DATA_DIR == %LOCALAPPDATA%\\PustakaHadith.
  3. Pemalar boleh tulis (DB/SETTINGS/BOOKMARKS/ENV/CACHE/PROFIL) di DATA_DIR.
  4. Pemalar aset (ICON/FAISS/MODEL/SUNNAH) di ASSET_DIR.
  5. Tiada fail baharu di ASSET_DIR selepas larian frozen.

Larian: python uji_fasa1_data.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402

LULUS = 0
GAGAL = 0
SENARAI_GAGAL: list[str] = []


def semak(nama: str, ok: bool) -> None:
    global LULUS, GAGAL
    LULUS += 1 if ok else 0
    if ok:
        print(f"  OK    {nama}")
    else:
        GAGAL += 1
        SENARAI_GAGAL.append(nama)
        print(f"  GAGAL {nama}")


def senarai_fail(folder: Path) -> set:
    """Fail projek sahaja; __pycache__ dikecualikan (hasil Python biasa)."""
    return {p.relative_to(folder) for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


# ---------- 1. Mod pembangunan ----------
semak("mod pembangunan: DATA_DIR == ASSET_DIR (folder projek)",
      config.DATA_DIR == config.ASSET_DIR)
semak("mod pembangunan: DB_PATH di ASSET_DIR",
      Path(config.DB_PATH).parent == config.ASSET_DIR)
semak("mod pembangunan: SETTINGS_PATH di ASSET_DIR",
      Path(config.SETTINGS_PATH).parent == config.ASSET_DIR)
semak("mod pembangunan: BOOKMARKS_PATH di ASSET_DIR",
      Path(config.BOOKMARKS_PATH).parent == config.ASSET_DIR)

# ---------- 2. Mod frozen (subproses) ----------
harap_data = Path(
    os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
) / "PustakaHadith"

kod = (
    "import sys\n"
    "sys.frozen = True\n"
    "import config\n"
    "print(config.DATA_DIR)\n"
    "print(config.DB_PATH)\n"
    "print(config.SETTINGS_PATH)\n"
    "print(config.BOOKMARKS_PATH)\n"
    "print(config.ENV_PATH)\n"
    "print(config.CACHE_SEMA)\n"
    "print(config.CACHE_HE)\n"
    "print(config.CACHE_ENG)\n"
    "print(config.CACHE_SYARAH)\n"
    "print(config.PROFIL_PATH)\n"
    "print(config.ASSET_DIR)\n"
    "print(config.ICON_PATH)\n"
    "print(config.FAISS_INDEX)\n"
    "print(config.FAISS_MAP)\n"
    "print(config.MODEL_CACHE)\n"
    "print(config.SUNNAH_MAP)\n"
)

sebelum = senarai_fail(ROOT)
hasil = subprocess.run(
    [sys.executable, "-c", kod],
    capture_output=True, text=True, cwd=str(ROOT), timeout=60,
)
selepas = senarai_fail(ROOT)

if hasil.returncode != 0:
    semak("mod frozen: config dimuat tanpa ralat", False)
    print(hasil.stderr)
else:
    semak("mod frozen: config dimuat tanpa ralat", True)
    baris = [b for b in hasil.stdout.splitlines() if b.strip()]

    def pada_data(p: str) -> bool:
        return Path(p).parent == harap_data

    def pada_aset(p: str) -> bool:
        return Path(p).parent == ROOT

    semak("mod frozen: DATA_DIR == %LOCALAPPDATA%\\PustakaHadith",
          baris[0] == str(harap_data))
    semak("mod frozen: DB_PATH di DATA_DIR", pada_data(baris[1]))
    semak("mod frozen: SETTINGS_PATH di DATA_DIR", pada_data(baris[2]))
    semak("mod frozen: BOOKMARKS_PATH di DATA_DIR", pada_data(baris[3]))
    semak("mod frozen: ENV_PATH di DATA_DIR", pada_data(baris[4]))
    semak("mod frozen: CACHE_SEMA di DATA_DIR", pada_data(baris[5]))
    semak("mod frozen: CACHE_HE di DATA_DIR", pada_data(baris[6]))
    semak("mod frozen: CACHE_ENG di DATA_DIR", pada_data(baris[7]))
    semak("mod frozen: CACHE_SYARAH di DATA_DIR", pada_data(baris[8]))
    semak("mod frozen: PROFIL_PATH di DATA_DIR", pada_data(baris[9]))
    semak("mod frozen: ASSET_DIR == folder projek", Path(baris[10]) == ROOT)
    semak("mod frozen: ICON_PATH di ASSET_DIR", pada_aset(baris[11]))
    semak("mod frozen: FAISS_INDEX di ASSET_DIR", pada_aset(baris[12]))
    semak("mod frozen: FAISS_MAP di ASSET_DIR", pada_aset(baris[13]))
    semak("mod frozen: MODEL_CACHE di ASSET_DIR", pada_aset(baris[14]))
    semak("mod frozen: SUNNAH_MAP di ASSET_DIR", pada_aset(baris[15]))

# ---------- 3. Tiada fail baharu di ASSET_DIR ----------
baharu = selepas - sebelum
semak("tiada fail baharu di ASSET_DIR selepas simulasi frozen", not baharu)

# ---------- Ringkasan ----------
print("=" * 60)
if GAGAL:
    print(f"  KEPUTUSAN: {LULUS} lulus, {GAGAL} gagal")
    for g in SENARAI_GAGAL:
        print(f"    - {g}")
    sys.exit(1)
print(f"  KEPUTUSAN: {LULUS} lulus, 0 gagal")
print("=" * 60)