"""Konfigurasi aplikasi PustakaHadith.

KEUTAMAAN SUMBER API KEY (tinggi -> rendah):
  1. Pembolehubah persekitaran  HADIS_API_KEY
  2. Fail .env                  (HADIS_API_KEY=...)
  3. user_settings.json         (disimpan dari skrin Tetapan)
  4. Kosong -> UI mesti minta pengguna masukkan

JANGAN sekali-kali menulis kunci sebenar di dalam fail ini.
Fail ini SELAMAT untuk di-commit; .env dan user_settings.json TIDAK.

LALUAN DATA (Fasa 1 installer, 20 Ogos 2026):
  - ASSET_DIR  = folder aset baca sahaja (dibundel dalam pakej MSIX).
  - DATA_DIR   = folder data pengguna boleh tulis.
    Mod frozen (versi installer): %LOCALAPPDATA%\\PustakaHadith
    Mod pembangunan:              folder projek (tingkah laku tidak berubah).
  Semua fail boleh tulis (hadis.db, tetapan, bookmark, cache) mesti datang
  daripada DATA_DIR melalui pemalar pusat di bawah -- JANGAN kira laluan
  sendiri dalam modul lain (INSTALLER.md §3).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parent


def _data_dir() -> Path:
    """Folder data pengguna; dicipta jika belum wujud."""
    if getattr(sys, "frozen", False):
        asas = os.environ.get("LOCALAPPDATA")
        if not asas:
            asas = str(Path.home() / "AppData" / "Local")
        d = Path(asas) / "PustakaHadith"
    else:
        # Mod pembangunan kekal seperti sekarang: folder projek.
        d = ASSET_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


DATA_DIR = _data_dir()

# ---------- Tetapan awam (selamat di-commit) ----------
API_BASE_URL = "https://service.hadis.my/api/v1"
DEFAULT_COLLECTION = "bukhari"
DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100          # had keras pelayan; minta lebih tetap dapat 100
DEFAULT_LANG = "ms"         # 'ms' = arab+melayu, 'id' = arab+indonesia, None = semua

# Had pelayan (untuk paparan kuota pada UI)
RATE_LIMIT_PER_MIN = 60      # disahkan 2026-07-28
RATE_LIMIT_PER_DAY = 200     # disahkan 2026-07-28

# ---------- Boleh tulis -- data pengguna (DATA_DIR) ----------
DB_PATH = str(DATA_DIR / "hadis.db")
SETTINGS_PATH = str(DATA_DIR / "user_settings.json")
BOOKMARKS_PATH = str(DATA_DIR / "bookmarks.json")
READING_HISTORY_PATH = str(DATA_DIR / "reading_history.json")
ENV_PATH = str(DATA_DIR / ".env")
CACHE_SEMA = str(DATA_DIR / ".cache_sema")
CACHE_HE = str(DATA_DIR / ".cache_he")
CACHE_ENG = str(DATA_DIR / ".cache_eng")
CACHE_SYARAH = str(DATA_DIR / ".cache_syarah")
PROFIL_PATH = str(DATA_DIR / "profil_model.json")

# ---------- Baca sahaja -- aset aplikasi (ASSET_DIR) ----------
ICON_PATH = str(ASSET_DIR / "app.ico")
FAISS_INDEX = str(ASSET_DIR / "hadis_faiss.index")
FAISS_MAP = str(ASSET_DIR / "hadis_id_map.pkl")
MODEL_CACHE = str(ASSET_DIR / ".cache_models")
SUNNAH_MAP = str(ASSET_DIR / "sunnah_map")

VALID_SLUGS = (
    "bukhari", "muslim", "abu-daud", "tirmidzi", "nasai",
    "ibnu-majah", "ahmad", "darimi", "malik",
)

KEY_PREFIX = "HADIS_"


# ---------- Pemuat kunci ----------

def _from_env_file(path: str = ENV_PATH) -> str:
    """Baca HADIS_API_KEY dari fail .env ringkas (tanpa kebergantungan luar)."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                if k.strip() == "HADIS_API_KEY":
                    return v.strip().strip("'\"")
    except OSError:
        pass
    return ""


def _read_settings(path: str = SETTINGS_PATH) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _pick(d: dict, *names: str) -> str:
    """Ambil nilai pertama yang ada — sokong 'api_key' dan 'API Key'."""
    for n in names:
        v = d.get(n)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _from_settings(path: str = SETTINGS_PATH) -> str:
    return _pick(_read_settings(path), "api_key", "API Key", "apiKey")


def get_api_key() -> str:
    """Pulangkan API key mengikut keutamaan; '' jika tiada."""
    return (
        os.environ.get("HADIS_API_KEY", "").strip()
        or _from_env_file()
        or _from_settings()
    )


def get_base_url() -> str:
    """Benarkan penggantian URL melalui persekitaran atau tetapan pengguna."""
    env = os.environ.get("HADIS_API_URL", "").strip()
    if env:
        return env.rstrip("/")
    u = _pick(_read_settings(), "api_url", "API URL", "apiUrl")
    return u.rstrip("/") if u else API_BASE_URL


def get_setting(name: str, default=None):
    """Baca sebarang tetapan lain, cth. get_setting('font_scale_idx', 1)."""
    v = _read_settings().get(name)
    return default if v is None else v


def save_setting(name: str, value) -> None:
    d = _read_settings()
    d[name] = value
    _write_settings(d)


def _write_settings(data: dict, path: str = SETTINGS_PATH) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)          # tulis atomik — elak fail rosak
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def valid_key_format(key: str) -> bool:
    """Semakan bentuk: HADIS_XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"""
    if not key or not key.startswith(KEY_PREFIX):
        return False
    body = key[len(KEY_PREFIX):]
    parts = body.split("-")
    return (
        len(parts) == 5
        and [len(p) for p in parts] == [8, 4, 4, 4, 12]
        and all(c in "0123456789abcdefABCDEF" for p in parts for c in p)
    )


def mask_key(key: str) -> str:
    """Untuk log/paparan: HADIS_34A8****...****B52E6B"""
    if not key or len(key) < 14:
        return "(tiada)"
    return f"{key[:10]}{'*' * 8}{key[-6:]}"


def save_api_key(key: str, url: str = "", path: str = SETTINGS_PATH) -> None:
    """Simpan guna snake_case; buang kunci lama bergaya label supaya tak berkonflik."""
    d = _read_settings(path)
    for old in ("API Key", "apiKey", "API URL", "apiUrl"):
        d.pop(old, None)
    d["api_key"] = key.strip()
    d["api_url"] = (url or d.get("api_url") or API_BASE_URL).rstrip("/")
    _write_settings(d, path)


# Keserasian ke belakang: modul lama membaca config.API_KEY secara terus.
API_KEY = get_api_key()

if __name__ == "__main__":
    k = get_api_key()
    print(f"URL      : {get_base_url()}")
    print(f"API Key  : {mask_key(k)}")
    print(f"Format   : {'sah' if valid_key_format(k) else 'TIDAK SAH / tiada'}")
    print(f"DB       : {DB_PATH} ({'ada' if os.path.exists(DB_PATH) else 'tiada'})")
    print(f"Font idx : {get_setting('font_scale_idx', 1)}")
