"""Sumber huraian Bahasa Melayu — SemakHadis.com.

MASALAH YANG DISELESAIKAN
-------------------------
Fasa 4 (Huraian) memerlukan syarah Bahasa Melayu yang sebenar. HadeethEnc
memberi 310 hadis sahaja; Irsyad al-Hadith lesennya tertutup. SemakHadis.com
mengumpul hadis sahih/hasan (Muttafaq 'alayh, Sahih, Hasan) dengan komentar
Bahasa Melayu penuh + status hadis, dikumpulkan pasukan penyemak hadis.

PENYELESAIAN
------------
SemakHadis.com menyediakan API carian terbuka (tiada kunci):
  GET https://semakhadis.com/api/hadith/hadith-search.json?query=...
Balasan JSON mengandungi `data[]` dengan `arabic_text`, `malay_text`
(terjemahan BM), `malay_commentary` (komentar BM), `intro_commentary`
(takhrij) dan `classification` (Sahih/Hasan/Daif/...).

Kunci padanan ialah **teks Arab dinormalisasi**, BUKAN ID, kerana
penomboran SemakHadis berbeza sepenuhnya daripada hadis.my.

LESEN & ATRIBUSI
----------------
Kandungan milik SemakHadis.com (tahqiq pasukan pengumpul). Lesen semula
data tidak dinyatakan secara eksplisit oleh laman; UI MESTI memaparkan
atribusi kepada SemakHadis.com. Hanya padanan yang JELAS (Jaccard >= 0.55,
calon kedua tidak rapat) diterima — lebih baik tiada daripada salah.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
sys.path.insert(0, ROOT)

from core.eng_source import normalisasi  # noqa: E402
from core.hadeethenc_api import _matn    # noqa: E402
from config import CACHE_SEMA            # noqa: E402

# Cache JSON setiap hadis SemakHadis: {CACHE_SEMA}/{id}.json
# Laluan pusat (INSTALLER.md §3): DATA_DIR dalam mod frozen.
CACHE = CACHE_SEMA

# Penanda permulaan matn umum. SemakHadis menyimpan matn SAHAJA (tanpa
# sanad), manakala hadis.db menyimpan sanad + matn penuh. AWALAN ini
# dibuang supaya padanan membandingkan matn yang setanding.
AWALAN = (
    "سمعت رسول الله صلي الله عليه وسلم يقول",
    "سمعت رسول الله صلي الله عليه وسلم",
    "قال رسول الله صلي الله عليه وسلم",
    "قال رسول الله صلي الله عليه",
    "عن النبي صلي الله عليه وسلم قال",
    "عن النبي صلي الله عليه وسلم",
    "قال النبي صلي الله عليه وسلم",
    "قال رسول الله",
    "قال النبي",
)

# Ambang Jaccard matn. Diukur pada padanan yang disemak manual:
#   betul  0.55 - 1.00
#   salah  < 0.50
# Calon kedua yang terlalu rapat DITOLAK.
JACCARD_MATN = 0.55

LESEN = "Sumber: SemakHadis.com"


def _norm(teks: str) -> str:
    t = normalisasi(teks)
    return re.sub(r"[\u064e\u064f\u0650\u0651\u064b\u064c\u064d\u0652\u0670]", "", t)


def matn_bersih(matn: str) -> str:
    """Buang penanda umum dari awal matn -- tinggalkan isi hadis."""
    if not matn:
        return ""
    t = _norm(matn)
    for a in AWALAN:
        b = _norm(a)
        if t.startswith(b):
            t = t[len(b):].strip()
            break
    return t


def _jaccard_set(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------- cache

def _rosak(laluan: str) -> bool:
    try:
        with open(laluan, encoding="utf-8") as f:
            d = json.load(f)
        return not isinstance(d, dict) or not d.get("id")
    except (OSError, ValueError):
        return True


def bina_indeks(cache_dir: str = CACHE) -> dict:
    """Bina indeks daripada cache tempatan.

    Pulangkan dict:
        data    : {sema_id: data_asal}
        matn    : {sema_id: set kata matn ternormalisasi}
        indeks  : {kata: set[sema_id]}  (indeks terbalik)
    """
    data: dict[str, dict] = {}
    matn: dict[str, set[str]] = {}
    peta: dict[str, set[str]] = {}

    for nama in sorted(os.listdir(cache_dir)):
        if not nama.endswith(".json"):
            continue
        laluan = os.path.join(cache_dir, nama)
        if _rosak(laluan):
            continue
        try:
            with open(laluan, encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, ValueError):
            continue
        sid = d.get("id")
        ar = d.get("arabic_text") or ""
        if not sid or not ar:
            continue
        data[sid] = d
        kata = set(_norm(ar).split())
        matn[sid] = kata
        for w in kata:
            if len(w) >= 3:
                peta.setdefault(w, set()).add(sid)

    return {"data": data, "matn": matn, "indeks": peta}


def padan(arab: str, indeks: dict) -> tuple[str, float] | None:
    """Cari ID SemakHadis bagi satu teks Arab hadis.my.

    Pulangkan (sema_id, jaccard_matn) atau None.
    """
    if not arab:
        return None
    set_soalan = set(matn_bersih(_matn(arab)).split())
    if not set_soalan:
        return None

    skor: dict[str, int] = {}
    for w in set_soalan:
        if len(w) >= 3 and w in indeks["indeks"]:
            for sid in indeks["indeks"][w]:
                skor[sid] = skor.get(sid, 0) + 1
    if not skor:
        return None

    calon = sorted(skor.items(), key=lambda x: -x[1])[:30]
    hasil: list[tuple[str, float]] = []
    for sid, _ in calon:
        s = _jaccard_set(set_soalan, indeks["matn"].get(sid, set()))
        hasil.append((sid, s))
    hasil.sort(key=lambda x: -x[1])
    sid0, s0 = hasil[0]
    if s0 < JACCARD_MATN:
        return None
    # Tolak bila calon kedua (matn BERBEZA) terlalu rapat.
    for sid, s in hasil[1:3]:
        if s >= s0 - 0.05 and _jaccard_set(set_soalan, indeks["matn"].get(sid, set())) < 0.9:
            return None
    return sid0, s0


# ---------------------------------------------------------------- DB

def pasang_skema(conn: sqlite3.Connection) -> None:
    from db import migrasi
    migrasi(conn)


def simpan(conn: sqlite3.Connection,
           pasangan: list[tuple]) -> int:
    """Simpan (collection, hadis_id, sema_id, jaccard, klasifikasi,
    tajuk, malay_text, intro, syarah) untuk satu collection."""
    if not pasangan:
        return 0
    cur = conn.executemany(
        "INSERT OR REPLACE INTO semakhadis"
        "(collection, hadis_id, sema_id, jaccard, klasifikasi, tajuk, "
        "malay_text, intro, syarah) VALUES (?,?,?,?,?,?,?,?,?)", pasangan)
    conn.commit()
    return cur.rowcount or 0


def ambil(conn: sqlite3.Connection, slug: str,
          hadis_id: int) -> dict | None:
    try:
        r = conn.execute(
            "SELECT sema_id, jaccard, klasifikasi, tajuk, malay_text, "
            "intro, syarah FROM semakhadis "
            "WHERE collection=? AND hadis_id=?", (slug, hadis_id)).fetchone()
    except Exception:
        return None
    if not r:
        return None
    return {"sema_id": r[0], "jaccard": r[1], "klasifikasi": r[2],
            "tajuk": r[3], "malay_text": r[4], "intro": r[5],
            "syarah": r[6], "lesen": LESEN}
