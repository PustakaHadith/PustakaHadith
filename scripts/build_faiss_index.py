#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build FAISS index for semantic search on hadis database.

Menggunakan `intfloat/multilingual-e5-small` (model retrieval pelbagai bahasa)
dengan teks MATN MELAYU SAHAJA (sanad dibuang) + awalan `passage: ` seperti
yang dikehendaki model e5. Query di sisi carian perlu awalan `query: `.

Sebab perubahan (Sesi 20): indeks lama (gabungan arab+melayu+indonesia+english,
model MiniLM) memberi hasil tidak relevan — vektor kabur oleh bahasa campur dan
sanad panjang menguasai embedding. e5 + matn Melayu sahaja terbukti dalam ujian:
"apa hukum makan riba" -> hadis riba di kedudukan teratas (skor 0.82-0.84).

Usage:
    python scripts/build_faiss_index.py
    python scripts/build_faiss_index.py --model intfloat/multilingual-e5-small
    python scripts/build_faiss_index.py --batch-size 64 --device cpu
"""

import argparse
import os
import pickle
import sys
import sqlite3
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "hadis.db"
INDEX_PATH = BASE_DIR / "hadis_faiss.index"
MAP_PATH = BASE_DIR / "hadis_id_map.pkl"
MODEL_CACHE = BASE_DIR / ".cache_models"

# Model lalai: e5-small = keseimbangan kualiti vs kelajuan (3 jam pada 4 CPU).
# e5-large jauh lebih perlahan (~23 jam) dengan peningkatan kualiti marginal.
DEFAULT_MODEL = "intfloat/multilingual-e5-small"

# Penanda permulaan matn dalam teks Melayu (selepas sanad). Ditemui secara
# empirik daripada sampel hadis.my: matn bermula pada rujukan kepada Nabi/
# Rasulullah. Sanad penuh menguasai embedding dan menenggelamkan isi hadis.
PENANDA = (
    "daripada nabi shallallahu 'alaihi wasallam",
    "dari nabi shallallahu 'alaihi wasallam",
    "daripada rasulullah shallallahu 'alaihi wasallam",
    "dari rasulullah shallallahu 'alaihi wasallam",
    "bahawa nabi shallallahu 'alaihi wasallam",
    "nabi shallallahu 'alaihi wasallam bersabda",
    "rasulullah shallallahu 'alaihi wasallam bersabda",
    "bersabda rasulullah shallallahu 'alaihi wasallam",
    "nabi shallallahu 'alaihi wasallam bersabda",
    "dari nabi shallallahu alaihi wasallam",
    "daripada nabi shallallahu alaihi wasallam",
)

MAX_CHARS = 1000

# 55 hadis terjejas (terjemahan Melayu diperbaiki oleh hadis.my, Ogos 2026)
AFFECTED_IDS = [
    ("malik", 36), ("malik", 108), ("malik", 109), ("malik", 152), ("malik", 153),
    ("malik", 181), ("malik", 190), ("malik", 341), ("malik", 522), ("malik", 552),
    ("malik", 556), ("malik", 572), ("malik", 619), ("malik", 647), ("malik", 685),
    ("malik", 701), ("malik", 775), ("malik", 779), ("malik", 799), ("malik", 806),
    ("malik", 809), ("malik", 828), ("malik", 881), ("malik", 1082), ("malik", 1418),
    ("malik", 1513),
    ("bukhari", 3459), ("bukhari", 3477), ("bukhari", 4413), ("bukhari", 4604),
    ("bukhari", 4935), ("bukhari", 6236), ("bukhari", 6990),
    ("tirmidzi", 231), ("tirmidzi", 1341), ("tirmidzi", 1419), ("tirmidzi", 1922),
    ("tirmidzi", 2175), ("tirmidzi", 2711), ("tirmidzi", 2863), ("tirmidzi", 2877),
    ("tirmidzi", 3029), ("tirmidzi", 3031), ("tirmidzi", 3073), ("tirmidzi", 3116),
    ("tirmidzi", 3120), ("tirmidzi", 3270),
    ("ahmad", 4303), ("ahmad", 9358), ("ahmad", 10614), ("ahmad", 24278),
    ("darimi", 91), ("darimi", 478), ("darimi", 2133), ("darimi", 2608),
    ("nasai", 468),
]


def matn_melayu(teks):
    """Buang sanad daripada teks Melayu; pulangkan matn (isi hadis)."""
    if not teks:
        return ""
    t = " ".join(teks.split())
    low = t.lower()
    pos = -1
    for p in PENANDA:
        i = low.find(p)
        if i >= 0 and (pos < 0 or i < pos):
            pos = i
    matn = t[pos:] if pos >= 0 else t[-400:]
    return matn[:MAX_CHARS]


def get_hadis_texts(conn):
    """Ambil hadis_id, collection, dan teks melayu dari DB."""
    rows = conn.execute(
        "SELECT hadis_id, collection, melayu FROM hadis"
    ).fetchall()
    return rows


def build_texts(rows):
    """Bangun teks embedding: matn Melayu sahaja + awalan passage e5."""
    texts = []
    id_map = []
    for hid, coll, melayu in rows:
        matn = matn_melayu(melayu)
        texts.append(f"passage: {matn}")
        id_map.append((hid, coll))
    return texts, id_map


def build_index(model_name, batch_size, device):
    """Bangun FAISS index dari hadis.db."""
    print(f"Memuatkan model: {model_name}")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name, device=device, cache_folder=str(MODEL_CACHE))

    if not DB_PATH.exists():
        sys.exit(f"Pangkalan data tidak dijumpai: {DB_PATH}. Jalankan sync.py dahulu.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print("Mengambil hadis dari pangkalan data...")
    rows = get_hadis_texts(conn)
    print(f"Jumlah hadis: {len(rows)}")

    texts, id_map = build_texts(rows)
    kosong = sum(1 for t in texts if len(t) < 30)
    print(f"Teks matn kosong/pendek (<30 aksara): {kosong}")

    print("Mengekod teks...")
    import faiss
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    dim = embeddings.shape[1]
    print(f"Dimensi embedding: {dim}")
    print(f"Jumlah embedding: {embeddings.shape[0]}")

    print("Membina indeks FAISS...")
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype(np.float32))

    print(f"Menyimpan indeks ke {INDEX_PATH}")
    faiss.write_index(index, str(INDEX_PATH))

    print(f"Menyimpan peta ID ke {MAP_PATH}")
    with open(MAP_PATH, "wb") as f:
        pickle.dump(id_map, f)

    print("Selesai!")
    print(f"Indeks: {INDEX_PATH} ({INDEX_PATH.stat().st_size / 1e6:.1f} MB)")
    print(f"Peta: {MAP_PATH} ({MAP_PATH.stat().st_size / 1e6:.1f} MB)")
    print(f"Jumlah vektor: {index.ntotal}")


def update_selective(model_name, batch_size, device, update_ids=None):
    """Kemas kini vektor untuk hadis tertentu sahaja (~5 minit)."""
    import faiss

    if update_ids is None:
        update_ids = AFFECTED_IDS

    print(f"Memuatkan model: {model_name}")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name, device=device,
                                cache_folder=str(MODEL_CACHE))

    # Muat indeks sedia ada
    print(f"Memuatkan indeks sedia ada: {INDEX_PATH}")
    index = faiss.read_index(str(INDEX_PATH))

    print(f"Memuatkan peta ID: {MAP_PATH}")
    with open(MAP_PATH, "rb") as f:
        id_map = pickle.load(f)

    # Indeks carian: (hadis_id, collection) -> posisi dalam indeks
    map_idx = {}
    for i, (hid, coll) in enumerate(id_map):
        map_idx[(hid, coll)] = i

    # Ambil semua teks Melayu dari DB
    conn = sqlite3.connect(DB_PATH)
    all_rows = conn.execute(
        "SELECT hadis_id, collection, melayu FROM hadis").fetchall()
    conn.close()

    hadis_dict = {(r[0], r[1]): r[2] for r in all_rows}

    # Cari index & teks untuk hadis yang perlu dikemas kini
    texts = []
    valid_indices = []
    missing = []

    for coll, hid in update_ids:
        key = (hid, coll)
        if key in map_idx and key in hadis_dict:
            matn = matn_melayu(hadis_dict[key])
            texts.append(f"passage: {matn}")
            valid_indices.append(map_idx[key])
        else:
            missing.append(f"{coll}:{hid}")

    if missing:
        print(f"Amaran: {len(missing)} hadis tiada dalam peta: "
              f"{', '.join(missing[:10])}")

    print(f"hadis dikemas kini: {len(valid_indices)} / {len(update_ids)}")
    print(f"Teks diencode: {len(texts)}")

    if not texts:
        print("Tiada teks untuk dikemas kini.")
        return

    # Encode teks baharu
    print("Mengekod teks...")
    new_emb = model.encode(
        texts, batch_size=batch_size, show_progress_bar=True,
        convert_to_numpy=True, normalize_embeddings=True)

    # Dapatkan semua vektor sedia ada
    print("Mengambil vektor sedia ada...")
    all_vectors = index.reconstruct_n(0, index.ntotal).copy()

    # Ganti vektor untuk hadis yang dikemas kini
    print(f"Mengganti {len(valid_indices)} vektor...")
    for i, idx in enumerate(valid_indices):
        all_vectors[idx] = new_emb[i].astype(np.float32)

    # Bina indeks baru
    print("Membina indeks baru...")
    dim = all_vectors.shape[1]
    new_index = faiss.IndexFlatIP(dim)
    new_index.add(all_vectors)

    # Simpan
    print(f"Menyimpan indeks: {INDEX_PATH}")
    faiss.write_index(new_index, str(INDEX_PATH))

    print("\nSelesai!")
    print(f"  Jumlah vektor: {new_index.ntotal}")
    print(f"  Vektor dikemas kini: {len(valid_indices)}")


def main():
    parser = argparse.ArgumentParser(
        description="Bina indeks FAISS untuk carian makna hadis")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Nama model SentenceTransformer")
    parser.add_argument("--batch-size", type=int, default=64,
                        help="Saiz kelompok untuk pengekodan")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"],
                        help="Peranti untuk digunakan")
    parser.add_argument("--selective", action="store_true",
                        help="Kemas kini 55 hadis terjejas sahaja (~5 minit)")
    args = parser.parse_args()

    if args.selective:
        update_selective(args.model, args.batch_size, args.device)
    else:
        build_index(args.model, args.batch_size, args.device)


if __name__ == "__main__":
    main()
