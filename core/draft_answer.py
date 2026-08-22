#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draft answer composer for semantic search results.
Composes draft answers from semantic search results + exact matches.
"""

from typing import List, Dict, Optional
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from api.hadis_api import HadisAPI
from core.semantic_search import semantic_search, is_index_ready


def compose_draft_answer(
    query: str,
    api: HadisAPI,
    top_k: int = 5,
    min_score: float = 0.6,
    include_exact: bool = True,
    semantic_results: Optional[List[Dict]] = None,
) -> Dict:
    """
    Compose draft answer from semantic search + exact matches.

    `semantic_results`: hasil carian semantik yang SEDIA ADA (pra-kira).
    Jika diberikan, ia digunakan terus dan `semantic_search` TIDAK
    dijalankan semula -- mengelak dua akses serentak ke model torch
    (thread worker masih menamatkan run()) yang mencetuskan fail-fast
    0xC0000409.

    Returns:
        {
            'query': str,
            'semantic_results': [...],
            'exact_results': [...],
            'draft_answer': str,
            'sources': [...],
            'has_semantic_index': bool,
        }
    """
    result = {
        "query": query,
        "semantic_results": [],
        "exact_results": [],
        "draft_answer": "",
        "sources": [],
        "has_semantic_index": is_index_ready(),
    }

    # 1. Semantic search
    if semantic_results is not None:
        result["semantic_results"] = list(semantic_results)
    elif result["has_semantic_index"]:
        sem_results = semantic_search(query, top_k=top_k, min_score=min_score)
        result["semantic_results"] = sem_results

    # 2. Exact match (existing API search)
    # Nota: `search_hadis` mengambil parameter `limit` (bukan `per_page`)
    # dan memulangkan struktur `{"hadis": [...], "meta": {...}}` (bukan
    # `{"data": {"results": [...]}}`). Sebelum ini kedua-dua kesilapan
    # melempar TypeError yang ditangkap SENYAP oleh `except Exception`,
    # jadi `exact_results` sentiasa kosong dan bahagian "Carian Biasa
    # (Keyword)" dalam draf jawapan TIDAK pernah muncul. Betulkan kedua-
    # dua supaya bahagian itu benar-benar dipapar.
    if include_exact:
        try:
            exact = api.search_hadis(query, limit=5)
            if exact and exact.get("hadis"):
                result["exact_results"] = exact["hadis"][:5]
        except Exception:
            pass

    # 3. Compose draft answer
    result["draft_answer"] = _compose_answer_text(result, api)
    result["sources"] = _extract_sources(result)

    return result


def _compose_answer_text(result: Dict, api: HadisAPI) -> str:
    """Bangun teks jawapan draft."""
    parts = []
    query = result["query"]

    if not result["has_semantic_index"]:
        return (
            f"Carian untuk: \"{result['query']}\"\n\n"
            "⚠️ **Indeks carian semantik belum dibina.**\n"
            "Jalankan: `python scripts/build_faiss_index.py` untuk mengaktifkan carian makna (AI).\n\n"
            "Sementara itu, gunakan carian biasa (keyword) di bahagian atas."
        )

    sem = result["semantic_results"]
    exact = result["exact_results"]

    if not sem and not exact:
        return f"Tiada hadis dijumpai untuk: \"{query}\""

    parts.append(f"🔍 **Carian:** \"{query}\"\n")

    # Semantic results
    if sem:
        parts.append(f"🤖 **Carian Makna (AI)** — {len(sem)} hasil:\n")
        for i, r in enumerate(result["semantic_results"][:3], 1):
            hid = r["hadis_id"]
            coll = r["collection"]
            score = r["score"]
            parts.append(f"  {i}. {_collection_name(coll)} #{hid} — kecocokan: {score:.0%}")

    # Exact results
    if exact:
        parts.append(f"\n🔍 **Carian Biasa (Keyword)** — {len(exact)} hasil:\n")
        for i, h in enumerate(exact[:3], 1):
            hid = h.get("id") or h.get("hadis_id")
            coll = h.get("collection") or h.get("book")
            parts.append(f"  {i}. {_collection_name(coll)} #{hid}")

    # Ambil hadis teratas untuk preview
    top_hadis = None
    if sem:
        top = sem[0]
        top_hadis = api.get_hadis_by_id(top["collection"], top["hadis_id"])
    elif exact:
        top_hadis = api.get_hadis_by_id(exact[0].get("collection", "bukhari"), exact[0].get("id") or exact[0].get("hadis_id"))

    if top_hadis:
        parts.append(f"\n📖 **Preview Hadis Teratas:**\n")
        arab = top_hadis.get("arab", "")[:300]
        melayu = top_hadis.get("melayu", "")[:300]
        # Perenggan BERASINGAN (baris kosong antara) -- Markdown
        # menggabungkan baris bersebelahan menjadi satu perenggan, jadi
        # Arab dan Melayu akan bercantum pada baris yang sama.
        if arab:
            parts.append(f"**Arab:** {arab}...\n")
        if melayu:
            parts.append(f"**Melayu:** {melayu}...\n")

    parts.append(f"\n💡 **Cadangan:** Klik hadis di atas untuk lihat penuh dengan darjat, syarah, dan transliterasi.")
    if not result["has_semantic_index"]:
        parts.append(f"\n⚠️ Indeks semantik tidak aktif. Jalankan `python scripts/build_faiss_index.py`.")

    return "\n".join(parts)


def _extract_sources(result: Dict) -> List[Dict]:
    """Ekstrak sumber untuk rujukan."""
    sources = []
    for r in result["semantic_results"][:5]:
        sources.append({
            "type": "semantic",
            "collection": r["collection"],
            "hadis_id": r["hadis_id"],
            "score": r["score"],
        })
    for h in result["exact_results"][:5]:
        sources.append({
            "type": "exact",
            "collection": h.get("collection") or h.get("book"),
            "hadis_id": h.get("id") or h.get("hadis_id"),
        })
    return sources


def _collection_name(slug: str) -> str:
    names = {
        "bukhari": "Bukhari",
        "muslim": "Muslim",
        "abu-daud": "Abu Daud",
        "tirmidzi": "Tirmizi",
        "nasai": "Nasa'i",
        "ibnu-majah": "Ibnu Majah",
        "ahmad": "Ahmad",
        "darimi": "Darimi",
        "malik": "Malik",
    }
    return names.get(slug, slug.capitalize())


def get_hadis_details(api: HadisAPI, collection: str, hid: int) -> Optional[Dict]:
    """Dapatkan hadis penuh untuk dipaparkan."""
    return api.get_hadis_by_id(collection, hid)


def format_hadis_for_display(h: Dict, show_all_langs: bool = True) -> str:
    """Format hadis untuk paparan UI."""
    if not h:
        return "Hadis tidak dijumpai."

    parts = []
    coll = h.get("collection", "")
    hid = h.get("id") or h.get("hadis_id", "")
    parts.append(f"**{_collection_name(coll)} #{hid}**\n")

    if h.get("arab"):
        parts.append(f"**Arab:**\n{h['arab']}\n")

    if show_all_langs:
        for lang, label in [("melayu", "Melayu"), ("indonesia", "Indonesia"), ("english", "English")]:
            if h.get(lang):
                parts.append(f"**{label}:**\n{h[lang]}\n")

    if h.get("transliterasi"):
        parts.append(f"**Transliterasi:**\n{h['transliterasi']}\n")

    if h.get("darjat"):
        parts.append(f"**Darjat:** {h['darjat']}\n")

    if h.get("sema"):
        sema = h["sema"]
        if sema.get("tajuk"):
            parts.append(f"**Huraian SemakHadis:** {sema['tajuk']}")
        if sema.get("syarah"):
            parts.append(f"Syarah: {sema['syarah'][:200]}...")

    return "\n".join(parts)