#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic search module for hadis using FAISS + SentenceTransformers.
Provides semantic search capabilities on top of exact keyword matching.

PENTING: Semua import berat (faiss, sentence_transformers) dibuat secara
lazy supaya UI boleh dimuatkan tanpa kegagalan jika pakej tidak dipasang.
"""

import os
import pickle
import threading
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import config  # laluan pusat (INSTALLER.md §3): aset vs data pengguna

BASE_DIR = Path(config.ASSET_DIR)
INDEX_PATH = Path(config.FAISS_INDEX)
MAP_PATH = Path(config.FAISS_MAP)
MODEL_CACHE = Path(config.MODEL_CACHE)

# e5-small (Sesi 20): model retrieval pelbagai bahasa yang jauh lebih baik
# daripada MiniLM untuk padanan maksud. Indeks dibina dengan awalan
# "passage: "; query di sisi carian mesti awalan "query: ".
_DEFAULT_MODEL = "intfloat/multilingual-e5-small"
_DEFAULT_DEVICE = "cpu"
_QUERY_PREFIX = "query: "

_model = None
_index = None
_id_map = None

# Fail profil masa muat model -- dibaca semak.py untuk mengesan regresi
# prestasi (cth. muat tiba-tiba >60s selepas perubahan kod). Setiap
# larian bersih yang memuat model menulis satu rekod. Fail log ini boleh
# ditulis, jadi laluannya di DATA_DIR (bukan ASSET_DIR baca sahaja).
PROFIL_PATH = Path(config.PROFIL_PATH)


def _simpan_profil(muat_s: float, import_s: float, dari_cache: bool = True) -> None:
    """Rekod masa muat model ke PROFIL_PATH (fail log JSON).

    Satu objek JSON bagi setiap larian (senarai). Gagal senyap -- profil
    ialah alat diagnostik, bukan fungsi kritikal. Tarikh tidak disertakan
    kerana masa sistem tidak stabil; cukup rekod berjujukan.

    `dari_cache` membezakan muat dari cache (stabil, ~24s) daripada muat
    turun pertama dari HF Hub (boleh beberapa minit, bukan regresi) --
    semak.py 8j menggunakan bendera ini untuk elak palsu positif.
    """
    import json as _json
    try:
        rekod = {"muat_s": round(muat_s, 1), "import_s": round(import_s, 1),
                 "dari_cache": bool(dari_cache)}
        sedia = []
        if PROFIL_PATH.exists():
            try:
                sedia = _json.loads(PROFIL_PATH.read_text(encoding="utf-8"))
            except Exception:
                sedia = []
        if not isinstance(sedia, list):
            sedia = []
        sedia.append(rekod)
        PROFIL_PATH.write_text(
            _json.dumps(sedia[-20:], ensure_ascii=False, indent=1),
            encoding="utf-8")
    except Exception:
        pass

# Kunci muat model. Tanpa ini, `PreloadWorker` dan `SemanticWorker` boleh
# memuat model SERENTAK -- dua inisialisasi torch pada masa sama
# mencetuskan fail-fast 0xC0000409 (PERUBAHAN_7OGOS.md).
#
# Dengan kunci: worker kedua menunggu yang pertama selesai, kemudian
# mendapati `_model` sudah ada dan terus menggunakannya.
_model_lock = threading.Lock()

_FAISS_READY = True
try:
    import faiss  # noqa: F401
    import numpy as np
except Exception:
    _FAISS_READY = False


def faiss_available() -> bool:
    """Semak sama ada faiss boleh dimuat."""
    return _FAISS_READY


def torch_available() -> bool:
    """Semak sama ada sentence_transformers (torch) boleh dimuat."""
    try:
        from sentence_transformers import SentenceTransformer  # noqa: F401
        return True
    except Exception:
        return False


def _load_model(model_name: str = _DEFAULT_MODEL, device: str = _DEFAULT_DEVICE):
    """Muat model (dicache global). Selamat dipanggil dari banyak thread.

    PENTING: model MESTI dimuat DAN di-encode dalam QThread yang sama
    jenisnya. Diukur (PERUBAHAN_7OGOS.md): muat dalam thread utama +
    encode dalam QThread menyebabkan fail-fast 0xC0000409. Muat dalam
    QThread + encode dalam QThread adalah selamat.
    """
    global _model
    # Semakan pantas tanpa kunci -- kes biasa (model sudah dimuat).
    if _model is not None:
        return _model

    # Elak amaran tokenizer berulang (TIDAK tetapkan HF_HUB_OFFLINE:
    # cabang except di bawah perlu muat turun dari HF Hub bila model
    # belum dicache -- offline mematahkan fallback itu). Diukur (Sesi
    # 25): import sentence_transformers ~19s (torch 4s + transformers
    # ~15s) -- had persekitaran Windows/antivirus, bukan kod aplikasi.
    # Masa muat stabil 24.5s; 80s dalam ujian awal ialah transien
    # (larian pertama + antivirus mengimbas DLL).
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    with _model_lock:
        # Semak semula: thread lain mungkin sudah memuatnya semasa kita
        # menunggu kunci.
        if _model is not None:
            return _model

        import time as _time
        _t0 = _time.time()
        from sentence_transformers import SentenceTransformer
        _import_s = _time.time() - _t0
        MODEL_CACHE.mkdir(exist_ok=True)
        cache_folder = str(MODEL_CACHE)
        _dari_cache = True
        try:
            # Muat terus daripada cache tanpa semakan HF Hub -- jauh lebih
            # pantas (~5s) berbanding semakan metadata setiap kali (~45s).
            _model = SentenceTransformer(
                _DEFAULT_MODEL, device=_DEFAULT_DEVICE,
                cache_folder=cache_folder, local_files_only=True)
        except Exception:
            # Model belum dicache: benarkan muat turun dari HF Hub. Tandai
            # `dari_cache=False` supaya semak.py 8j tidak menganggap muat
            # turun pertama (minit) sebagai regresi prestasi.
            _dari_cache = False
            _model = SentenceTransformer(
                _DEFAULT_MODEL, device=_DEFAULT_DEVICE,
                cache_folder=cache_folder)
        _simpan_profil(_time.time() - _t0, _import_s, _dari_cache)
    return _model


def _load_index():
    global _index
    if not _FAISS_READY:
        raise RuntimeError("Pakej faiss tidak dipasang. Jalankan: pip install faiss-cpu")
    # Semakan pantas tanpa kunci -- kes biasa (indeks sudah dimuat).
    if _index is not None:
        return _index
    with _model_lock:
        # Semak semula: thread lain mungkin sudah memuatnya semasa kita
        # menunggu kunci. `faiss.read_index` serentak dari dua QThread
        # (PreloadWorker + SemanticWorker) mencetuskan fail-fast
        # 0xC0000409 -- oleh itu guna kunci yang sama seperti model.
        if _index is not None:
            return _index
        if not os.path.exists(str(INDEX_PATH)):
            raise FileNotFoundError(
                "Indeks FAISS tidak dijumpai. Jalankan: "
                "python scripts/build_faiss_index.py"
            )
        import faiss
        _index = faiss.read_index(str(INDEX_PATH))
    return _index


def _load_id_map() -> List[Tuple[int, str]]:
    global _id_map
    # Semakan pantas tanpa kunci -- kes biasa (peta sudah dimuat).
    if _id_map is not None:
        return _id_map
    with _model_lock:
        # Semak semula: kunci yang sama mengelak pembacaan pkl serentak
        # dari dua QThread (fail-fast 0xC0000409).
        if _id_map is not None:
            return _id_map
        map_path = MAP_PATH
        if not map_path.exists():
            raise FileNotFoundError(
                "Peta ID tidak dijumpai. Jalankan: "
                "python scripts/build_faiss_index.py"
            )
        with open(map_path, "rb") as f:
            _id_map = pickle.load(f)
    return _id_map


def semantic_search(
    query: str,
    top_k: int = 10,
    min_score: float = 0.6,
    model_name: str = _DEFAULT_MODEL,
) -> List[Dict]:
    """
    Carian semantik hadis berdasarkan makna soalan.

    Args:
        query: Soalan/user query (Melayu, Arab, Indonesia, English)
        top_k: Jumlah hasil teratas
        min_score: Threshold minimum cosine similarity (0-1)
        model_name: Model SentenceTransformer

    Returns:
        List of dict: [{'hadis_id': int, 'collection': str, 'score': float}, ...]
    """
    if not _FAISS_READY:
        return []
    if not query or not query.strip():
        return []

    import numpy as np

    model = _load_model()
    index = _load_index()
    id_map = _load_id_map()

    query_vec = model.encode([_QUERY_PREFIX + query.strip()], convert_to_numpy=True, normalize_embeddings=True)
    scores, indices = index.search(query_vec.astype(np.float32), top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1 or score < min_score:
            continue
        hid, coll = id_map[idx]
        results.append({
            "hadis_id": int(hid),
            "collection": coll,
            "score": float(score),
        })

    return results


def is_index_ready() -> bool:
    """Semak sama ada index dan map sedia untuk digunakan."""
    return INDEX_PATH.exists() and MAP_PATH.exists()


def get_index_stats() -> Dict:
    """Dapatkan statistik index."""
    if not is_index_ready():
        return {"ready": False}
    try:
        index = _load_index()
        id_map = _load_id_map()
        return {
            "ready": True,
            "total_vectors": index.ntotal,
            "dimension": index.d,
            "total_hadis": len(id_map),
        }
    except Exception as e:
        from utils.bahasa import terjemah_ralat
        return {"ready": False, "error": terjemah_ralat(e)}


def rebuild_index(model_name: str = _DEFAULT_MODEL, batch_size: int = 64, device: str = "cpu"):
    """Bangun semula index (panggil build_faiss_index.py)."""
    import subprocess
    import sys
    script = BASE_DIR / "scripts" / "build_faiss_index.py"
    cmd = [sys.executable, str(script), "--model", model_name, "--batch-size", str(batch_size), "--device", device]
    subprocess.run(cmd, check=True)
    # Clear cache
    global _model, _index, _id_map
    _model = None
    _index = None
    _id_map = None
