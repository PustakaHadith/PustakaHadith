"""Muat turun semua hadis SemakHadis.com ke cache tempatan `.cache_sema/`.

    python scripts/muat_turun_sema.py          # muat turun semua
    python scripts/muat_turun_sema.py --semak  # status sahaja

TIADA KUNCI API. Sumber: https://semakhadis.com/api/hadith/hadith-search.json

API menghadkan 1,000 rekod bagi setiap query, jadi enumerasi dibuat
dengan mempersoal API menggunakan setiap huruf Arab (dan beberapa pasangan
huruf) supaya liputan bertindih dan lengkap; ID unik dinyahduplikasi.
Setiap rekod disimpan sebagai `.cache_sema/{id}.json`. Selepas muat turun,
jalankan `python sync_sema.py` untuk memadankan ke hadis.db.

Kandungan milik SemakHadis.com; UI memaparkan atribusi (LESEN).
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(BASE, ".cache_sema")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "https://semakhadis.com/api/hadith/hadith-search.json"
PAGE_SIZE = 1000
JEDA = 0.3  # saat antara permintaan (elak bebankan pelayan)

HURUF = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
GABUNGAN = ("ال", "عن", "في", "من", "بسم", "قال", "رسول", "الله",
            "صلى", "عليه", "سلام", "الحديث", "باب", "ابن")


def _dapat(paip) -> dict:
    req = urllib.request.Request(
        paip,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "Pustaka-Hadis/1.0 (muat turun huraian sema)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def semak() -> int:
    if not os.path.isdir(CACHE):
        return 0
    return len([f for f in os.listdir(CACHE) if f.endswith(".json")])


def _simpan(rek: dict) -> bool:
    if not rek.get("id"):
        return False
    laluan = os.path.join(CACHE, f"{rek['id']}.json")
    if os.path.exists(laluan):
        return False
    simpan = {k: v for k, v in rek.items() if k != "_formatted"}
    with open(laluan, "w", encoding="utf-8") as f:
        json.dump(simpan, f, ensure_ascii=False)
    return True


def muat_turun() -> int:
    os.makedirs(CACHE, exist_ok=True)
    dulu = semak()
    baru = 0

    queries = [h for h in HURUF] + list(GABUNGAN)
    for i, qs in enumerate(queries, 1):
        q = urllib.parse.urlencode({"query": qs, "page": 1,
                                    "page_size": PAGE_SIZE})
        try:
            d = _dapat(f"{URL}?{q}")
        except Exception as e:
            print(f"  query '{qs}' GAGAL: {e}", flush=True)
            continue
        ditulis = 0
        for rek in d.get("data", []):
            if _simpan(rek):
                ditulis += 1
                baru += 1
        print(f"  [{i}/{len(queries)}] query '{qs}': +{ditulis} baru "
              f"(jumlah {semak():,})", flush=True)
        if i != len(queries):
            time.sleep(JEDA)

    print(f"\n  Selesai. +{baru:,} baru (cache sedia ada {dulu:,}, "
          f"jumlah {semak():,}).")
    return baru


def main() -> int:
    if "--semak" in sys.argv[1:]:
        print(f"  Cache SemakHadis: {semak():,} fail di {CACHE}")
        return 0
    if "--saiz" in sys.argv[1:]:
        q = urllib.parse.urlencode({"query": "", "page": 1, "page_size": 1})
        d = _dapat(f"{URL}?{q}")
        print(f"  total_records={d['metadata']['total_records']}")
        return 0

    print(f"\n  Muat turun SemakHadis.com -> {CACHE}")
    print("  Sumber: SemakHadis.com (atribusi dipaparkan dalam UI)")
    print(f"  Query: {len(HURUF)} huruf Arab + {len(GABUNGAN)} pasangan\n")
    muat_turun()
    print("  Langkah seterusnya: python sync_sema.py\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
