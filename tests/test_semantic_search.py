"""Ujian Fasa 2: core.semantic_search (model & FAISS di-mock).

Tidak muat turun model ~1GB atau index sebenar. Hanya sahkan:
  - query dihantar ke encoder dengan awalan _QUERY_PREFIX (wajib e5-small)
  - hasil dipetakan dari id_map mengikut indeks FAISS.
"""
import numpy as np
import core.semantic_search as ss


def test_semantic_search_guna_prefix_dan_pulang_hasil(monkeypatch):
    dipanggil = {}

    class FakeModel:
        def encode(self, texts, convert_to_numpy=True, normalize_embeddings=True):
            dipanggil["teks"] = texts[0]
            return np.array([[0.1] * 384], dtype=np.float32)

    class FakeIndex:
        def search(self, vec, k):
            return np.array([[0.95]]), np.array([[0]])

    monkeypatch.setattr(ss, "_load_model", lambda *a, **k: FakeModel())
    monkeypatch.setattr(ss, "_load_index", lambda *a, **k: FakeIndex())
    monkeypatch.setattr(ss, "_load_id_map", lambda *a, **k: [(1, "bukhari")])
    monkeypatch.setattr(ss, "_FAISS_READY", True, raising=False)

    res = ss.semantic_search("solat", top_k=5)
    assert res
    assert res[0]["hadis_id"] == 1
    assert res[0]["collection"] == "bukhari"
    assert dipanggil["teks"].startswith(ss._QUERY_PREFIX)


def test_semantic_search_query_kosong(monkeypatch):
    monkeypatch.setattr(ss, "_FAISS_READY", True, raising=False)
    assert ss.semantic_search("   ") == []
