#!/usr/bin/env python3
"""Ujian runtime: `compose_draft_answer` + bahagian "Carian Biasa (Keyword)".

Sesi 55 (13 Ogos): bahagian "🔍 Carian Biasa (Keyword)" dalam kotak
Jawapan Draf AI tidak pernah muncul walaupun kodnya wujud. Punca: dua
kesilapan dalam `compose_draft_answer` -- `api.search_hadis` dipanggil
dengan `per_page=5` (parameter sebenar ialah `limit`) dan hasil dibaca
dari `exact["data"]["results"]` (struktur pulangan sebenar ialah
`{"hadis": [...], "meta": {...}}`). Kedua-duanya melempar TypeError yang
ditangkap SENYAP oleh `except Exception`, jadi `exact_results` sentiasa
kosong.

Ujian ini mengunci regresi:
  1. `exact_results` terisi (dan hasil itu benar-benar wujud dalam DB).
  2. Bahagian "Carian Biasa (Keyword)" wujud dalam teks jawapan draf
     (bila indeks semantik sedia -- tanpa indeks, `_compose_answer_text`
     pulang awal dengan mesej "indeks belum dibina").
  3. Corak LAMA (`per_page=5` / `exact["data"]["results"]`) tidak
     kembali dalam `core/draft_answer.py`.

`semantic_results=[]` dihantar supaya `semantic_search` TIDAK dijalankan
(mengelak muat model torch yang perlahan) -- ujian ini tentang padanan
TEPAT (keyword), bukan semantik.
"""
import os
import sys
import sqlite3

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from api.hadis_api import HadisAPI
from core.draft_answer import compose_draft_answer
from core.semantic_search import is_index_ready

PASS, FAIL = 0, 0


def semak(nama: str, ok: bool, butir: str = ""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  OK    {nama}")
    else:
        FAIL += 1
        print(f"  GAGAL {nama}  {butir}")


api = HadisAPI()
r = compose_draft_answer("solat", api, semantic_results=[])
jawapan = r["draft_answer"]

# 1. exact_results terisi (hasil padanan tepat dari search_hadis)
semak("exact_results terisi (>=1 hasil)", len(r["exact_results"]) >= 1,
      f"{len(r['exact_results'])} hasil")
if r["exact_results"]:
    h = r["exact_results"][0]
    semak("hasil exact ada medan id + collection",
          bool(h.get("id")) and bool(h.get("collection")),
          f"{h.get('collection')}#{h.get('id')}")
    # Hasil bukan rekaan -- sahkan wujud dalam hadis.db
    c = sqlite3.connect(os.path.join(BASE, "hadis.db"))
    ada = c.execute(
        "SELECT COUNT(*) FROM hadis WHERE collection=? AND hadis_id=?",
        (h["collection"], h["id"])).fetchone()[0]
    c.close()
    semak("hasil exact wujud dalam DB", ada == 1,
          f"collection={h['collection']} id={h['id']} ada={ada}")

# 2. Bahagian "Carian Biasa (Keyword)" dalam jawapan draf
semak("'Carian Biasa (Keyword)' wujud dalam jawapan draf",
      "Carian Biasa (Keyword)" in jawapan)
semak("jawapan menyebut bilangan hasil exact",
      f"{len(r['exact_results'])} hasil" in jawapan,
      jawapan[:150].replace("\n", " | "))
if r["exact_results"]:
    h0 = r["exact_results"][0]
    semak("jawapan menyebut hadis exact pertama",
          f"#{h0.get('id')}" in jawapan, jawapan[:150].replace("\n", " | "))

# 3. Corak LAMA tidak kembali (sandaran statik pada sumber)
src = open(os.path.join(BASE, "core", "draft_answer.py"),
           encoding="utf-8").read()
semak("tiada per_page=5 dalam core/draft_answer.py", "per_page=5" not in src)
semak("tiada exact['data']['results'] dalam core/draft_answer.py",
      'exact["data"]["results"]' not in src)
semak("guna search_hadis(query, limit=5)",
      "search_hadis(query, limit=5)" in src)

print(f"\n  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
print("=" * 60)
sys.exit(0 if FAIL == 0 else 1)
