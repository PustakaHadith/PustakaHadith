"""Sumber huraian Melayu — HadeethEnc.com (hadis sahih + penjelasan ringkas).

MASALAH YANG DISELESAIKAN
-------------------------
Fasa 4 (Huraian) sebelum ini hanya mampu memberi nota automatik berasaskan
topik (`status="auto"`). Pengguna mahukan huraian ulama yang sebenar, tetapi
Fath al-Bari penomborannya hanyut (lihat core/syarah_source.py).

PENYELESAIAN
------------
HadeethEnc.com menyediakan terjemahan Melayu + penjelasan ringkas (explanation
+ hints) untuk ~2,328 hadis sahih. Tiada kunci API; muat turun sekali dan
simpan ke cache tempatan:

    hadis.db (arab)  --padan teks-->  cache HadeethEnc (hadeeth_ar)  --sumber-->
                                        explanation/hints (Melayu)

Kunci padanan ialah **teks Arab dinormalisasi**, BUKAN ID, kerana penomboran
tidak sepadan langsung antara hadis.my dan HadeethEnc.

LESEN & ATRIBUSI
----------------
Kandungan adalah milik HadeethEnc.com (projek IslamHouse). UI MESTI memaparkan
atribusi. Syarat: tiada pengubahsuaian, penambahan atau pemadaman kandungan,
dan rujuk penerbit + sumber (HadeethEnc.com).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
sys.path.insert(0, ROOT)

from core.eng_source import normalisasi  # noqa: E402
from config import CACHE_HE              # noqa: E402

API = "https://hadeethenc.com/api/v1"
USER_AGENT = "Pustaka-Hadis/1.0 (+https://hadeethenc.com)"

# Cache JSON setiap hadis HadeethEnc: {CACHE_HE}/{id}.json
# Laluan pusat (INSTALLER.md §3): DATA_DIR dalam mod frozen.
CACHE = CACHE_HE
SENARAI = os.path.join(CACHE, "senarai_id.json")

# Penanda permulaan matn (selepas sanad). Ditemui secara empirik: sanad
# hadis.my dan HadeethEnc berbeza sepenuhnya, tetapi matn selepas penanda
# ini hampir sama. Padanan Jaccard pada MATN (bukan teks penuh) memberi
# skor 0.87-1.00 untuk hadis betul vs 0.04-0.48 untuk calon salah.
_PENANDA_MATN = (
    "\u0642\u0627\u0644 \u0631\u0633\u0648\u0644 \u0627\u0644\u0644\u0647",   # قال رسول الله
    "\u0633\u0645\u0639\u062a \u0631\u0633\u0648\u0644 \u0627\u0644\u0644\u0647",  # سمعت رسول الله
    "\u0642\u0627\u0644 \u0627\u0644\u0646\u0628\u064a",                          # قال النبي
    "\u0639\u0646 \u0627\u0644\u0646\u0628\u064a",                                # عن النبي
    "\u0642\u0627\u0644 \u0635\u0644\u0649 \u0627\u0644\u0644\u0647",             # قال صلى الله
    "\u0642\u0627\u0644\u0631\u0633\u0648\u0644",                                 # قالرسول
)

# Ambang Jaccard matn. Diukur (Bukhari #1,2,8,20,50):
#     betul  0.62 - 1.00
#     salah  0.04 - 0.48
# Margin ini besar; 0.55 selamat di tengah. Padanan yang tidak jelas (dua
# calon berbeza hampir sama skor) DITOLAK -- lebih baik tiada daripada salah.
JACCARD_MATN = 0.55


def _http(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------- muat turun

def url_one(he_id: int) -> str:
    return f"{API}/hadeeths/one/?id={he_id}&language=ms"


def url_list(category_id: int, page: int = 1, per_page: int = 100,
             language: str = "en") -> str:
    """Senarai hadis bagi satu kategori.

    PENTING: `language` mesti `en` untuk enumerasi. Dengan `ms`, API
    MENYEMBUNYIKAN hadis yang tiada terjemahan Melayu (paginasi berbeza:
    8 vs 100 item bagi kategori yang sama). Tapisan sebenar dilakukan
    pada medan `translations[]` -- hanya simpan ID yang ada `"ms"`.
    """
    return f"{API}/hadeeths/list/?language={language}&category_id={category_id}" \
           f"&per_page={per_page}&page={page}"


def senarai_id() -> list[int]:
    """Baca senarai ID unik daripada cache. Bangkitkan jika tiada."""
    with open(SENARAI, encoding="utf-8") as f:
        return json.load(f)


def muat_turun_semua(hadis_id: list[int] | None = None,
                     had: int = 80, jeda: float = 0.15) -> tuple[int, int]:
    """Muat turun `one` untuk setiap ID ke .cache_he/{id}.json.

    Setiap ID mesti ADA terjemahan ms (lihat `senarai_id` -- ditapis
    daripada `translations[]`). Jika tidak, `one?language=ms` membalas
    404 WALAUPUN hadis itu wujud dalam bahasa lain.

    Skrip boleh dihentikan dan dijalankan semula -- fail yang sudah sah
    dikekalkan. Pulangkan (dimuat, dilangkau).
    """
    os.makedirs(CACHE, exist_ok=True)
    ids = hadis_id if hadis_id is not None else senarai_id()
    dimuat = dilangkau = 0
    for i, hid in enumerate(ids, 1):
        laluan = os.path.join(CACHE, f"{hid}.json")
        if (os.path.exists(laluan) and os.path.getsize(laluan) > 500
                and not _rosak(laluan)):
            dilangkau += 1
            continue
        try:
            data = _http(url_one(hid))
        except Exception as e:
            print(f"    [{i}/{len(ids)}] id={hid} GAGAL ({e})")
            time.sleep(1.0)
            continue
        with open(laluan, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        dimuat += 1
        if dimuat % had == 0 or i == len(ids):
            print(f"    [{i}/{len(ids)}] dimuat={dimuat} dilangkau={dilangkau}")
        time.sleep(jeda)
    return dimuat, dilangkau


def senarai_id_ms() -> list[int]:
    """Enumerasi penuh daripada API: semua kategori, tapis yang ada "ms".

    Menulis semula .cache_he/senarai_id.json supaya hanya hadis dengan
    terjemahan Melayu yang disimpan. Diukur: ~147 daripada ~40,000 hadis
    HadeethEnc diterjemah ke bahasa Melayu.
    """
    ids: set[int] = set()
    cats = _http(f"{API}/categories/list/?language=en")
    for j, c in enumerate(cats, 1):
        cat = int(c["id"])
        page = 1
        while True:
            d = _http(url_list(cat, page, 100, "en"))
            data = d.get("data", [])
            if not data:
                break
            for x in data:
                if "ms" in (x.get("translations") or []):
                    ids.add(int(x["id"]))
            page += 1
            time.sleep(0.05)
        print(f"  [{j}/{len(cats)}] cat={cat} unik={len(ids)}", flush=True)
    hasil = sorted(ids)
    os.makedirs(CACHE, exist_ok=True)
    with open(SENARAI, "w", encoding="utf-8") as f:
        json.dump(hasil, f, ensure_ascii=False)
    print(f"  JUMLAH dengan terjemahan ms: {len(hasil)}")
    return hasil


def _rosak(laluan: str) -> bool:
    try:
        with open(laluan, encoding="utf-8") as f:
            d = json.load(f)
        return not isinstance(d, dict) or not d.get("hadeeth_ar")
    except (OSError, ValueError):
        return True


# ---------------------------------------------------------------- indeks

def _matn(teks: str) -> str:
    """Ambil matn: teks selepas penanda permulaan matn yang TERAKHIR."""
    if not teks:
        return ""
    t = normalisasi(teks)
    pos = -1
    for p in _PENANDA_MATN:
        i = t.find(p)
        if i > pos:
            pos = i
    return t[pos:] if pos >= 0 else t


def bina_indeks(cache_dir: str = CACHE) -> dict:
    """Bina indeks daripada fail cache.

    Pulangkan dict:
        teks    : {he_id: teks_arab_dinormalisasi}
        matn    : {he_id: matn_dinormalisasi}
        indeks  : {kata_jarang: set[he_id]}  (indeks terbalik)
        kira    : {kata: bilangan_hadis}
    """
    teks, matn = {}, {}
    kira: dict[str, int] = {}
    peta: dict[str, set[int]] = {}

    for nama in sorted(os.listdir(cache_dir)):
        if not nama.endswith(".json"):
            continue
        hid = nama[:-5]
        if not hid.isdigit():
            continue
        hid = int(hid)
        laluan = os.path.join(cache_dir, nama)
        if _rosak(laluan):
            continue
        try:
            with open(laluan, encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, ValueError):
            continue
        ar = normalisasi(d.get("hadeeth_ar") or "")
        if not ar:
            continue
        teks[hid] = ar
        mt = _matn(ar)
        matn[hid] = mt
        for w in set(mt.split()):
            if len(w) < 4:
                continue
            kira[w] = kira.get(w, 0) + 1
            peta.setdefault(w, set()).add(hid)

    had = max(3, len(teks) // 20)
    indeks = {w: v for w, v in peta.items() if kira[w] <= had}
    return {"teks": teks, "matn": matn, "indeks": indeks, "kira": kira}


def _jaccard_set(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def padan(arab: str, indeks: dict) -> tuple[int, float, str] | None:
    """Cari ID HadeethEnc bagi satu teks Arab hadis.my.

    Pulangkan (he_id, jaccard_matn, kaedah) atau None.

    Kaedah:
        "penuh" -> kunci teks penuh sama (jarang)
        "matn"  -> padanan Jaccard matn sahaja
    """
    if not arab:
        return None
    na = normalisasi(arab)

    # Lapisan 1: teks penuh sama -- pantas dan tepat.
    for hid, t in indeks["teks"].items():
        if t == na:
            return hid, 1.0, "penuh"

    # Lapisan 2: indeks kata jarang matn.
    # Sesi 18.5: ambang `len(kata) < 4` diturunkan. Matn pendek
    # (cth. "اسلمت على ما سلف من خير") hanya ada 1-3 kata jarang dan
    # ditolak sebelum ini -- 25 hadis HE tidak dipadan walaupun Jaccard
    # tinggi. Pengesahan Jaccard dua hala + semakan calon kedua kekal.
    set_soalan = set(_matn(arab).split())
    kata = [w for w in set_soalan if len(w) >= 4 and w in indeks["indeks"]]
    if not kata:
        return None
    skor: dict[int, int] = {}
    for w in kata:
        for hid in indeks["indeks"][w]:
            skor[hid] = skor.get(hid, 0) + 1
    if not skor:
        return None

    # Hanya calon yang benar-benar bertindih layak disemak Jaccard penuh.
    calon = sorted(skor.items(), key=lambda x: -x[1])[:20]
    terbaik, n1 = calon[0]
    if n1 / len(kata) < 0.35:
        return None

    # Pengesahan dua hala pada MATN -- sanad tidak dikira.
    hasil: list[tuple[int, float]] = []
    for hid, _ in calon:
        s = _jaccard_set(set_soalan, set(indeks["matn"].get(hid, "").split()))
        hasil.append((hid, s))
    hasil.sort(key=lambda x: -x[1])
    hid0, s0 = hasil[0]
    if s0 < JACCARD_MATN:
        return None
    # Jangan terima bila calon kedua (matn BERBEZA) terlalu rapat.
    for hid, s in hasil[1:]:
        if s >= s0 - 0.05:
            if _jaccard_set(set_soalan, set(indeks["matn"].get(hid, "").split())) < 0.9:
                return None          # dua matn berbeza -- tidak selamat
    return hid0, s0, "matn"


# ---------------------------------------------------------------- huraian

def huraian(he_id: int, cache_dir: str = CACHE) -> dict | None:
    """Baca huraian daripada cache. Pulangkan field asal API."""
    laluan = os.path.join(cache_dir, f"{he_id}.json")
    if not os.path.exists(laluan) or _rosak(laluan):
        return None
    try:
        with open(laluan, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------- skema DB

def pasang_skema(conn) -> None:
    """Pastikan jadual hadethenc wujud (migrasi 4)."""
    from db import migrasi
    migrasi(conn)


def simpan(conn, pasangan: list[tuple[int, int, float, str]]) -> int:
    """Simpan (hadis_id, he_id, jaccard, kaedah) untuk satu collection."""
    if not pasangan:
        return 0
    cur = conn.executemany(
        "INSERT OR REPLACE INTO hadethenc(collection, hadis_id, he_id, "
        "jaccard, kaedah) VALUES (?,?,?,?,?)", pasangan)
    conn.commit()
    return cur.rowcount or 0


def ambil(conn, slug: str, hadis_id: int) -> tuple[int, float, str] | None:
    try:
        r = conn.execute(
            "SELECT he_id, jaccard, kaedah FROM hadethenc "
            "WHERE collection=? AND hadis_id=?", (slug, hadis_id)).fetchone()
    except Exception:
        return None
    return (r[0], r[1], r[2]) if r else None
