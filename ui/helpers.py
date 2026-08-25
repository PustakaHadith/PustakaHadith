"""Helper bebas Pustaka Hadis — tiada state Qt, tiada gandingan UI.

Dipisahkan dari `ui/app_qt.py` (Sesi 30 refactor). Semua fungsi di sini
tulen dan boleh diuji unit. app_qt.py mengimport semula nama-nama ini
(`from ui.helpers import ...`) supaya `ui.app_qt._parse_lompat` dsb.
kekal wujud untuk pemanggil luaran (uji_lompat.py, settings_panel.py).

Peraturan tema: JANGAN import warna dari `ui.theme` di sini — modul ini
TIDAK didaftar dalam `_THEMED_MODULES`, jadi apply_theme() tidak
menyalin nilai ke ruang namanya. Satu-satunya import theme ialah
`COLLECTION_META` (metadata kitab, bukan warna) yang tidak pernah
berubah ikut tema.
"""

from __future__ import annotations

import json
import os
import re

from config import (                                       # noqa: E402
    BOOKMARKS_PATH, READING_HISTORY_PATH, SETTINGS_PATH, SUNNAH_MAP,
)
from ui.theme import COLLECTION_META  # metadata kitab -- BUKAN warna

# Laluan pusat daripada config.py (INSTALLER.md §3): data pengguna di
# DATA_DIR (mod frozen: %LOCALAPPDATA%\PustakaHadis), peta sunnah di ASSET_DIR.
SETTINGS = SETTINGS_PATH
BOOKMARKS = BOOKMARKS_PATH

PAGES = {"home": 0, "kitab": 1, "detail": 2, "search": 3,
         "saved": 4, "settings": 5}

# lang= API: 'ms' arab+melayu, 'id' arab+indonesia, None semua
LANG_PARAM = {"bm_only": "ms", "ind_only": "id", "both": None}

# Had panjang mesej WhatsApp -- pautan wa.me yang terlalu panjang sukar
# dihantar. Had keselamatan untuk kongsi "Ringkas" (petikan Arab +
# terjemahan penuh + pautan "Baca penuh").
# 2000 terlalu ketat (8,243 hadis / 13% terpotong terjemahan); 5000 masih
# memotong hujung terjemahan apabila petikan Arab panjang (Sesi 36 pilihan
# pengguna b.2). Dinaikkan ke 6000 -- Ringkas hanya 125 hadis (0.2%)
# terjemahan hujungnya terpotong.
_HAD_WA = 6000

# Petikan Arab dalam kongsi "Ringkas" (Sesi 36) -- had ~10 baris (~700
# aksara, sepadan titik potong contoh pengguna Bukhari No. 3) supaya
# KEDUA-DUA Arab dan terjemahan kelihatan dalam gelembung WhatsApp;
# `_HAD_WA` dinaikkan selari supaya terjemahan penuh tetap sampai. Potong
# pada sempadan perkataan; "…" ditambah bila terpotong.
_HAD_PETIK_RINGKAS = 700

# Label tajuk tab bahasa. Dipakai oleh PagesDetail (_switch_lang dsb.).
# NOTA: app_qt.py TIDAK mengimport semula ini -- tiada pemanggil luar
# untuk LANG_LABEL/_ATRIBUSI_*; ia milik PagesDetail sahaja.
LANG_LABEL = {"melayu": "BAHASA MELAYU", "indonesia": "BAHASA INDONESIA",
              "english": "ENGLISH"}
# Atribusi wajib untuk terjemahan Inggeris -- sumber luaran yang dipadan
# melalui teks Arab. Pemalar tunggal supaya paparan bahasa tunggal dan
# tab bandingan tidak hanyut.
_ATRIBUSI_INGGERIS = ("Sumber: sunnah.com melalui "
                      "fawazahmed0/hadith-api · dipadan "
                      "automatik melalui teks Arab")
# Atribusi wajib untuk huraian SemakHadis dan HadeethEnc -- kandungan
# milik sumber masing-masing. Pemalar tunggal supaya semua paparan
# konsisten dan semakan semak.py boleh mengunci teksnya.
_ATRIBUSI_SEMA = "Sumber: SemakHadis.com"
_ATRIBUSI_HE = ("Huraian ringkas oleh HadeethEnc.com (projek IslamHouse) "
                "untuk hadis berkenaan. Kandungan tidak diubah.")

# Pautan "Baca penuh" (sunnah.com) untuk kongsi WhatsApp. Penomboran
# hadis.my (hadis.db) BERBEZA daripada sunnah.com, jadi pautan dibina
# melalui peta {hadis_id: {book, hadith}} yang dijana oleh
# `sync_english.py --peta-sunnah` (guna semula padanan teks
# Arab/Indonesia sync_english). URL guna rujukan DALAM-BUKU CDN
# (sunnah.com/{slug}/{book}/{hadith}) -- bukan nombor global, kerana
# penomboran global CDN tidak sepadan dengan URL sunnah.com untuk
# beberapa kitab (disahkan audit Sesi 36). Ahmad dan darimi tiada
# sumber sunnah.com -- tiada pautan.
_SUNNAH_SLUG = {
    "bukhari": "bukhari",
    "muslim": "muslim",
    "abu-daud": "abudawud",
    "tirmidzi": "tirmidhi",
    "nasai": "nasai",
    "ibnu-majah": "ibnmajah",
    "malik": "malik",
}
_SUNNAH_MAP: dict[str, dict] = {}


def _muat_peta_sunnah(slug: str) -> dict:
    """Muat sunnah_map/{slug}.json; cache dalam memori. Kosong jika tiada."""
    if slug not in _SUNNAH_MAP:
        peta = {}
        try:
            with open(os.path.join(SUNNAH_MAP, f"{slug}.json"),
                      encoding="utf-8") as f:
                peta = json.load(f)
        except Exception:
            peta = {}
        _SUNNAH_MAP[slug] = peta
    return _SUNNAH_MAP[slug]


def sunnah_url(slug: str, hadis_id: int) -> str:
    """Pautan 'Baca penuh' sunnah.com, atau '' bila tiada padanan.

    Format sunnah.com/{slug}/{buku}/{hadith} (rujukan dalam-buku CDN,
    sistem sunnah.com sendiri). Contoh: https://sunnah.com/muslim/2/32
    """
    sun = _SUNNAH_SLUG.get(slug)
    if not sun:
        return ""
    r = _muat_peta_sunnah(slug).get(str(hadis_id))
    if not isinstance(r, dict):
        return ""
    book, hadith = r.get("book"), r.get("hadith")
    if not book or not hadith:
        return ""
    return f"https://sunnah.com/{sun}/{book}/{hadith}"


# Carian pantas "lompat ke hadis": peta nama kitab (dinormalkan) -> slug.
# Termasuk nama paparan COLLECTION_META dan ejaan biasa pengguna.
_ALIAS_KITAB = {
    "bukhari": "bukhari", "al-bukhari": "bukhari",
    "sahih-bukhari": "bukhari", "shahih-bukhari": "bukhari",
    "imam-bukhari": "bukhari",
    "muslim": "muslim", "sahih-muslim": "muslim",
    "shahih-muslim": "muslim", "imam-muslim": "muslim",
    "abu-daud": "abu-daud", "abudaud": "abu-daud",
    "abu-dawud": "abu-daud", "sunan-abu-daud": "abu-daud",
    "sunan-abu-dawud": "abu-daud",
    "tirmidzi": "tirmidzi", "tirmizi": "tirmidzi",
    "tirmidhi": "tirmidzi", "turmudzi": "tirmidzi",
    "jami-at-tirmidzi": "tirmidzi", "jami-tirmidzi": "tirmidzi",
    "nasai": "nasai", "nasa-i": "nasai", "nasaii": "nasai",
    "an-nasai": "nasai", "sunan-an-nasai": "nasai",
    "sunan-nasai": "nasai",
    "ibnu-majah": "ibnu-majah", "ibn-majah": "ibnu-majah",
    "ibnumajah": "ibnu-majah", "sunan-ibnu-majah": "ibnu-majah",
    "ahmad": "ahmad", "musnad-ahmad": "ahmad",
    "imam-ahmad": "ahmad",
    "darimi": "darimi", "ad-darimi": "darimi", "darmi": "darimi",
    "musnad-darimi": "darimi", "sunan-darimi": "darimi",
    "malik": "malik", "muwatta": "malik", "muwatta-malik": "malik",
    "imam-malik": "malik",
}


def _normalis_kitab(nama: str) -> str:
    """'Sahih al-Bukhari' / 'abu daud' -> 'sahih-al-bukhari' / 'abu-daud'."""
    return re.sub(r"[^a-z0-9]+", "-", nama.lower()).strip("-")


def _slug_dari_awalan(awalan: str):
    """Pulangkan slug jika awalan padan SATU kitab sahaja, else None.

    'b' -> bukhari, 't' -> tirmidzi, 'ab' -> abu-daud. 'm'/'a' ambigu
    (muslim/malik, ahmad/abu-daud) -> None supaya jatuh ke carian biasa.
    """
    padan = set()
    for slug, meta in COLLECTION_META.items():
        for nama in (slug, meta.get("short", ""), meta.get("name", "")):
            if _normalis_kitab(nama).startswith(awalan):
                padan.add(slug)
    return padan.pop() if len(padan) == 1 else None


def _parse_lompat(q, default_slug=None):
    """Tafsir carian sebagai lompat terus ke hadis.

    Format diterima:
      'bukhari 433' / 'sahih bukhari 433'   nama kitab + nombor
      'bukhari:433' / 'b:433'               pemisah titik bertindih
      'B433' / 'bukhari433'                 awalan/huruf + nombor
      '433'                                 nombor sahaja
    Nama kitab boleh ringkas ('b', 'mu', 'ab') selagi padan UNIK;
    `default_slug` dipakai bila tiada nama ('433' sahaja -- chip kitab
    terpilih atau kitab terakhir dibuka). Pulangkan (slug, nombor) atau
    None untuk carian biasa.
    """
    # ':' dijadikan ruang supaya 'bukhari:433' mengalir melalui laluan
    # token yang sama dengan 'bukhari 433' (titik bertindih tidak pernah
    # wujud dalam nama kitab, dan FTS5 menganggap ':' aksara khas).
    s = (q or "").replace(":", " ").strip().lower()
    if not s:
        return None
    tokens = s.split()
    if tokens[-1].isdigit():
        # 'bukhari 433' / 'bukhari:433' / '433' -- nombor token terakhir
        nombor = int(tokens[-1])
        nama = " ".join(tokens[:-1])
    else:
        # 'B433' / 'bukhari433' -- huruf + digit tanpa pemisah.
        # Nombor MESTI di hujung; 'bukhari 10 hadis' / '433 bukhari'
        # tiada padanan di sini mahupun di bawah -> carian biasa.
        m = re.fullmatch(r"([a-z]+)(\d+)", s)
        if not m:
            return None
        nama, nombor_s = m.groups()
        nombor = int(nombor_s)
    if nama:
        slug = _ALIAS_KITAB.get(_normalis_kitab(nama))
        if slug is None:
            slug = _slug_dari_awalan(_normalis_kitab(nama))
    else:
        slug = default_slug
    if slug is None:
        return None
    return slug, nombor


def _read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path, data):
    try:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        pass


# ── Sejarah bacaan (25 Ogos 2026 — panel "Sambung perjalanan ilmu") ──
# Data pengguna ringan di DATA_DIR (pola sama bookmarks.json): senarai
# hadis yang dibuka, terbaharu di depan, nyah-duplikasi ikut (slug,n).
# Cap 50 entri — cukup untuk "terakhir dibaca" tanpa membesar tanpa had.
# Tulis atomik melalui _write_json. Gagal senyap: sejarah ialah keselesaan,
# bukan fungsi kritikal — jangan sesekali ganggu aliran bacaan.

READING_HISTORY = READING_HISTORY_PATH
_HAD_SEJARAH = 50


def read_history() -> list:
    return _read_json(READING_HISTORY, [])


def record_reading(slug: str, n: int, label: str = "") -> None:
    """Rekod hadis dibuka — dipanggil automatik dari render detail."""
    if not slug or not isinstance(n, int):
        return
    senarai = [e for e in read_history()
               if not (e.get("slug") == slug and e.get("n") == n)]
    senarai.insert(0, {"slug": slug, "n": n, "label": label or ""})
    _write_json(READING_HISTORY, senarai[:_HAD_SEJARAH])


def _clear(layout):
    while layout.count():
        it = layout.takeAt(0)
        w = it.widget()
        if w:
            w.setParent(None)
            w.deleteLater()
        elif it.layout():
            _clear(it.layout())


def click_sound():
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_OK)
    except Exception:
        pass
