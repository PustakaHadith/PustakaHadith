#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji carian Arab tanpa tashkeel pada SALINAN hadis.db sebenar.

Letak di root projek dan jalankan:

    python uji_carian_arab.py

KESELAMATAN
-----------
- `hadis.db` asal dibuka baca sahaja.
- SQLite Backup API membuat salinan konsisten, termasuk keadaan WAL.
- Migrasi skema 8 dan semua INSERT/UPDATE/DELETE ujian berlaku pada fail
  sementara sahaja; fail sementara dipadam selepas ujian.
- Aplikasi sebaiknya ditutup semasa ujian supaya keputusan stabil.
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import db  # noqa: E402
try:
    from config import DB_PATH
except Exception:
    DB_PATH = str(BASE / "hadis.db")


def gagal(msg: str) -> None:
    raise AssertionError(msg)


def semak_struktur(conn: sqlite3.Connection, jumlah_asal: int) -> None:
    versi = conn.execute("PRAGMA user_version").fetchone()[0]
    if versi != db.SKEMA_VERSI or versi < 8:
        gagal(f"versi skema {versi}; jangkaan {db.SKEMA_VERSI} (minimum 8)")

    kolum = {r[1] for r in conn.execute("PRAGMA table_info(hadis)")}
    if "arab_carian" not in kolum:
        gagal("kolum hadis.arab_carian tiada")

    null = conn.execute(
        "SELECT COUNT(*) FROM hadis WHERE arab_carian IS NULL"
    ).fetchone()[0]
    if null:
        gagal(f"{null:,} baris arab_carian masih NULL")

    fts = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='hadis_fts'"
    ).fetchone()
    if not fts or "arab_carian" not in fts[0]:
        gagal("hadis_fts masih menggunakan kolum Arab lama")

    trigger = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger'"
    )}
    perlu = {"hadis_ai", "hadis_ad", "hadis_au"}
    if not perlu <= trigger:
        gagal(f"trigger FTS tiada: {sorted(perlu - trigger)}")

    jumlah = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    if jumlah != jumlah_asal:
        gagal(f"jumlah hadis berubah: {jumlah_asal:,} -> {jumlah:,}")

    print(f"  LULUS struktur: skema {versi}, {jumlah:,} hadis, 0 NULL, 3 trigger")


def semak_query(conn: sqlite3.Connection) -> None:
    pasangan = [
        ("كتب", "كَتَبَ"),
        ("نية", "نِيَّة"),
        ("الله", "اللَّهِ"),
    ]
    ada_hasil = False
    for tanpa, dengan in pasangan:
        a, ta = db.search(conn, tanpa, limit=50)
        b, tb = db.search(conn, dengan, limit=50)
        ida = [(r["collection"], r["hadis_id"]) for r in a]
        idb = [(r["collection"], r["hadis_id"]) for r in b]
        if ta != tb or ida != idb:
            gagal(
                f"hasil berbeza bagi {tanpa!r}/{dengan!r}: "
                f"jumlah {ta}/{tb}"
            )
        ada_hasil = ada_hasil or ta > 0
        print(f"  LULUS Arab {tanpa!r} = {dengan!r}: {ta:,} hasil")
    if not ada_hasil:
        gagal("semua query Arab ujian memberi 0 hasil")

    # Jangan lipat varian huruf dalam indeks carian pengguna.
    if db.bersih_tashkeel("نِيَّة") != "نية":
        gagal("bersih_tashkeel gagal membuang harakat")
    if db.bersih_tashkeel("نِيَّه") != "نيه":
        gagal("bersih_tashkeel telah melipat varian huruf secara tidak sengaja")
    if db.bersih_tashkeel("نِيَّة") == db.bersih_tashkeel("نِيَّه"):
        gagal("ة dan ه tidak sepatutnya dilipat dalam carian")
    print("  LULUS prinsip: harakat dibuang, ة dan ه tidak dilipat")

    for q in ("niat", "puasa", "hukum riba"):
        _, total = db.search(conn, q, limit=5)
        print(f"  Regresi BM {q!r}: {total:,} hasil")


def semak_trigger(conn: sqlite3.Connection) -> None:
    slug = "__uji_arab__"
    conn.execute(
        "INSERT OR IGNORE INTO collections(slug,name,total_hadis) VALUES(?,?,1)",
        (slug, "Ujian Arab"),
    )
    arab = "كَتَبَ زَيْدٌ الرِّسَالَةَ"
    conn.execute(
        "INSERT INTO hadis(collection,hadis_id,arab,arab_carian,melayu,indonesia) "
        "VALUES(?,?,?,?,?,?)",
        (slug, 1, arab, db.bersih_tashkeel(arab), "ujian", ""),
    )
    conn.commit()
    _, n = db.search(conn, "كتب", collection=slug)
    if n != 1:
        gagal(f"trigger INSERT gagal, jumlah={n}")

    baru = "ذَهَبَ زَيْدٌ إِلَى الْمَسْجِدِ"
    conn.execute(
        "UPDATE hadis SET arab=?,arab_carian=? WHERE collection=? AND hadis_id=1",
        (baru, db.bersih_tashkeel(baru), slug),
    )
    conn.commit()
    if db.search(conn, "كتب", collection=slug)[1] != 0:
        gagal("trigger UPDATE gagal membuang token lama")
    if db.search(conn, "ذهب", collection=slug)[1] != 1:
        gagal("trigger UPDATE gagal memasukkan token baharu")

    conn.execute("DELETE FROM hadis WHERE collection=?", (slug,))
    conn.execute("DELETE FROM collections WHERE slug=?", (slug,))
    conn.commit()
    if db.search(conn, "ذهب", collection=slug)[1] != 0:
        gagal("trigger DELETE gagal")
    print("  LULUS trigger FTS: INSERT, UPDATE dan DELETE")


def salin_db(sumber: Path, destinasi: Path) -> int:
    uri = f"file:{sumber.resolve().as_posix()}?mode=ro"
    src = sqlite3.connect(uri, uri=True)
    try:
        jumlah = src.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
        dst = sqlite3.connect(destinasi)
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
    return jumlah


def main() -> int:
    sumber = Path(DB_PATH)
    print("=" * 68)
    print("UJI CARIAN ARAB TANPA TASHKEEL — SALINAN DB SAHAJA")
    print("=" * 68)
    print(f"DB asal: {sumber}")
    if not sumber.exists():
        print("RALAT: hadis.db tidak dijumpai.")
        return 1

    with tempfile.TemporaryDirectory(prefix="pustaka_uji_arab_") as td:
        salinan = Path(td) / "hadis_uji.db"
        t0 = time.perf_counter()
        jumlah = salin_db(sumber, salinan)
        print(f"Salinan konsisten siap: {jumlah:,} hadis")
        print("DB asal kekal baca sahaja.")

        conn = db.init(str(salinan))
        try:
            semak_struktur(conn, jumlah)
            semak_query(conn)
            semak_trigger(conn)
        finally:
            conn.close()
        print(f"\nSEMUA UJIAN LULUS ({time.perf_counter() - t0:.2f}s)")
        print("Fail sementara akan dipadam. hadis.db asal TIDAK berubah.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"\nGAGAL: {exc}")
        print("hadis.db asal tidak diubah.")
        raise SystemExit(1)
