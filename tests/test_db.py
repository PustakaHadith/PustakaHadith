"""Ujian Fasa 2: db.search / get_page / get_one / random_hadis / list_collections.

Guna DB SQLite :memory: dengan skema penuh (db.init) + FTS5 diisi semula
melalui _backfill_arab_carian. Tidak bergantung pada hadis.db sebenar.
"""
import pytest
import db
from db import init, get_page, get_one, random_hadis, list_collections, search


@pytest.fixture
def conn():
    c = init(":memory:")
    c.execute(
        "INSERT INTO collections(slug,name,author,total_hadis) VALUES (?,?,?,?)",
        ("bukhari", "Sahih al-Bukhari", "al-Bukhari", 2),
    )
    rows = [
        ("bukhari", 1, "صلاة الخمس", "melayu solat satu", "indo",
         db.bersih_tashkeel("صلاة الخمس")),
        ("bukhari", 2, "زكاة المال", "melayu zakat dua", "indo",
         db.bersih_tashkeel("زكاة المال")),
    ]
    c.executemany(
        "INSERT INTO hadis(collection,hadis_id,arab,melayu,indonesia,arab_carian) "
        "VALUES (?,?,?,?,?,?)",
        rows,
    )
    # init() sudah jalankan _backfill_arab_carian() yang mencipta trigger
    # hadis_ai/ad/au -> FTS5 (hadis_fts) diisi automatik bila hadis dimasuk.
    # Tidak panggil semula (create_function akan error: fungsi sudah wujud).
    yield c
    c.close()


def test_list_collections(conn):
    cols = list_collections(conn)
    assert len(cols) == 1
    assert cols[0]["slug"] == "bukhari"


def test_get_page(conn):
    rows, total = get_page(conn, "bukhari", 1, 50)
    assert total == 2
    assert len(rows) == 2


def test_get_one(conn):
    r = get_one(conn, "bukhari", 1)
    assert r["hadis_id"] == 1
    assert "صلاة" in r["arab"]


def test_random_hadis(conn):
    res = random_hadis(conn, "bukhari", 1)
    assert len(res) == 1


def test_search_jumpa(conn):
    res, total = search(conn, "صلاة")
    assert total >= 1
    assert any(r["hadis_id"] == 1 for r in res)


def test_search_tiada(conn):
    res, total = search(conn, "xyzqwertytiadaditema")
    assert total == 0
    assert res == []
