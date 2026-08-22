# Rekod Reka Bentuk — Carian Arab Tanpa Tashkeel (`db.py` Skema 7→8)

> **Status 15 Ogos 2026:** pelaksanaan sudah wujud dalam `db.py` dan `sync.py`
> versi Drive terkini. Ia lulus ujian migrasi sintetik dan salinan konsisten
> DB Windows sebenar 62,169 hadis, termasuk trigger, idempoten, DB baharu dan
> pemulihan migrasi terganggu. Dokumen ini dikekalkan sebagai rekod reka bentuk.
> Keputusan muktamad direkod dalam `dokumen/audit/CARIAN_ARAB.md`.
>
> Rujukan: `dokumen_GTAF_penilaian.md` §4–5 (punca masalah + bukti ujian).

---

## Ringkasan Masalah

`hadis_fts` index kolum `arab` **mentah** (bertashkeel penuh). `tokenize='unicode61
remove_diacritics 2'` **tidak** buang harakat Arab (disahkan ujian empirikal — cuma
berkesan untuk aksen Latin). Akibatnya: carian Arab tanpa tashkeel (cara biasa orang
taip) **tidak** menjumpai hadis walaupun perkataan wujud tepat.

## Prinsip Pembetulan

1. Tambah lajur **baharu** `arab_carian` (tashkeel dibuang SAHAJA — **tiada** lipatan
   varian huruf `ة→ه` dsb., ikut Peraturan #3 `MULA_SINI.md`)
2. Index `arab_carian` dalam `hadis_fts` — **gantikan** `arab` mentah
3. Normalisasi query pengguna dengan fungsi **sama** sebelum `MATCH`
4. Paparan (`h.arab` asal) **tidak disentuh** — pengguna tetap nampak tashkeel penuh

---

## 1. Fungsi Baharu (letak di atas `SCHEMA` dalam `db.py`)

```python
import unicodedata

# Julat tashkeel/harakat Arab SAHAJA -- sengaja TIDAK melipat varian huruf
# (ة->ه, أ/إ/آ->ا dsb.) kerana itu memecahkan carian pengguna (MULA_SINI.md #3:
# "JANGAN lipat ة->ه dalam indeks carian -- نية jadi نيه -- tidak wujud").
# Julat asas sama seperti core/eng_source.py::_DIAKRITIK, disalin (bukan
# diimport) supaya db.py kekal tanpa kebergantungan pada core/ -- lapisan
# data mentah tidak sepatutnya bergantung pada lapisan padanan sumber luar.
#
# TAMBAHAN (14 Ogos 2026, dokumen/audit/GTAF.md §normalisasi): \u0610-\u0614
# ialah titik kod Unicode TERSENDIRI untuk simbol selawat/rahimahullah
# tertanam ("ARABIC SIGN SALLALLAHOU ALAYHE WA SALLAM" dll) -- BUKAN sama
# dengan LIGATUR_SELAWAT (\ufdfa) yang sudah dikendali utils/bahasa.py.
# Ditemui semasa kaji kod GTAF/text-matcher (Java, normalize()). Risiko
# rendah (jarang digunakan sumber data semasa) tetapi kos tambah = sifar.
_TASHKEEL = re.compile(
    r"[\u0610-\u0614\u064B-\u065F\u0670\u0640\u06D6-\u06ED]"
)


def bersih_tashkeel(teks: str | None) -> str:
    """Buang harakat Arab SAHAJA -- untuk indeks & carian FTS.

    BUKAN untuk padanan sumber (lihat core/eng_source.py::normalisasi()
    untuk keperluan itu -- fungsi itu turut melipat varian huruf, sesuai
    untuk padanan dalaman tetapi memecahkan carian pengguna).

    Diuji (dokumen_GTAF_penilaian.md §4): `remove_diacritics=2` bawaan
    SQLite TIDAK berkesan untuk harakat Arab (U+064B-U+065F) -- hanya
    aksen Latin (café/résumé). Fungsi ini menggantikannya di peringkat
    Python sebelum data masuk index / sebelum query dihantar ke MATCH.
    """
    if not teks:
        return teks or ""
    s = unicodedata.normalize("NFKC", teks)
    return _TASHKEEL.sub("", s)
```

---

## 2. Kemas Kini `SCHEMA` (pemasangan baharu)

```python
SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS collections ( ... );   -- tidak berubah

CREATE TABLE IF NOT EXISTS hadis (
    rowid_pk     INTEGER PRIMARY KEY AUTOINCREMENT,
    collection   TEXT NOT NULL REFERENCES collections(slug),
    hadis_id     INTEGER NOT NULL,
    arab         TEXT,
    arab_carian  TEXT,          -- BAHARU: arab tanpa tashkeel, untuk FTS sahaja
    melayu       TEXT,
    indonesia    TEXT,
    UNIQUE(collection, hadis_id)
);

CREATE INDEX IF NOT EXISTS idx_hadis_col ON hadis(collection);

-- FTS5: 'arab_carian' GANTIKAN 'arab' mentah -- lihat bersih_tashkeel()
CREATE VIRTUAL TABLE IF NOT EXISTS hadis_fts USING fts5(
    melayu, arab_carian,
    content='hadis',
    content_rowid='rowid_pk',
    tokenize='unicode61 remove_diacritics 2'
);

CREATE TRIGGER IF NOT EXISTS hadis_ai AFTER INSERT ON hadis BEGIN
    INSERT INTO hadis_fts(rowid, melayu, arab_carian)
        VALUES (new.rowid_pk, new.melayu, new.arab_carian);
END;
CREATE TRIGGER IF NOT EXISTS hadis_ad AFTER DELETE ON hadis BEGIN
    INSERT INTO hadis_fts(hadis_fts, rowid, melayu, arab_carian)
        VALUES('delete', old.rowid_pk, old.melayu, old.arab_carian);
END;
CREATE TRIGGER IF NOT EXISTS hadis_au AFTER UPDATE ON hadis BEGIN
    INSERT INTO hadis_fts(hadis_fts, rowid, melayu, arab_carian)
        VALUES('delete', old.rowid_pk, old.melayu, old.arab_carian);
    INSERT INTO hadis_fts(rowid, melayu, arab_carian)
        VALUES (new.rowid_pk, new.melayu, new.arab_carian);
END;
...
"""
```

**PENTING:** `sync.py` (Fasa 1, isi data baharu) mesti dikemas kini supaya setiap
`INSERT`/`UPDATE` ke jadual `hadis` turut isi `arab_carian = bersih_tashkeel(arab)` —
jika tidak, hadis **baharu** selepas migrasi tidak akan boleh dicari dalam Arab.

---

## 3. Migrasi (`MIGRASI` dict, `SKEMA_VERSI = 8`)

```python
SKEMA_VERSI = 8   # dari 7

MIGRASI: dict[int, str] = {
    # ... 2-7 kekal tidak berubah ...
    8: """
    ALTER TABLE hadis ADD COLUMN arab_carian TEXT;
    """,
}
```

**Masalah:** SQL sahaja tak boleh isi `arab_carian` sebab perlu fungsi Python
(`bersih_tashkeel`) bukan fungsi SQL terbina. `migrasi()` sedia ada guna
`conn.executescript(skrip)` (SQL tulen) — perlu langkah tambahan **selepas**
`ALTER TABLE` untuk backfill + bina semula index. Cadangan ubah fungsi `migrasi()`:

```python
def migrasi(conn: sqlite3.Connection, senyap: bool = True) -> int:
    """Jalankan migrasi yang tertinggal. Pulangkan bilangan dijalankan."""
    ada = versi(conn)
    if ada >= SKEMA_VERSI:
        return 0

    dijalankan = 0
    for v in range(ada + 1, SKEMA_VERSI + 1):
        skrip = MIGRASI.get(v)
        if skrip:
            conn.executescript(skrip)
            dijalankan += 1
            if not senyap:
                print(f"  migrasi skema -> versi {v}")

        # Langkah Python selepas migrasi 8: backfill arab_carian +
        # bina semula index FTS5 (kolum indeks berubah dari 'arab' ke
        # 'arab_carian' -- data lama dalam hadis_fts masih rujuk kolum
        # lama, mesti dibina semula sepenuhnya).
        if v == 8:
            _backfill_arab_carian(conn, senyap)

    conn.execute(f"PRAGMA user_version={SKEMA_VERSI}")
    conn.commit()
    return dijalankan


def _backfill_arab_carian(conn: sqlite3.Connection, senyap: bool = True) -> None:
    """Isi arab_carian untuk baris sedia ada + bina semula hadis_fts.

    Dipanggil SEKALI semasa migrasi ke skema 8. Selamat dijalankan
    berulang (backfill hanya kena baris arab_carian IS NULL).
    """
    conn.create_function("bersih_tashkeel_sql", 1, bersih_tashkeel)
    n = conn.execute(
        "UPDATE hadis SET arab_carian = bersih_tashkeel_sql(arab) "
        "WHERE arab_carian IS NULL"
    ).rowcount
    if not senyap:
        print(f"  arab_carian diisi untuk {n:,} baris")

    # hadis_fts lama (jika wujud dari skema < 8) masih rujuk kolum 'arab'
    # mentah -- gantikan definisi jadual & bina semula index dari awal.
    fts_lama_wujud = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='hadis_fts'"
    ).fetchone()
    if fts_lama_wujud and "arab_carian" not in fts_lama_wujud[0]:
        conn.executescript("""
            DROP TRIGGER IF EXISTS hadis_ai;
            DROP TRIGGER IF EXISTS hadis_ad;
            DROP TRIGGER IF EXISTS hadis_au;
            DROP TABLE IF EXISTS hadis_fts;
        """)
        # SCHEMA (dieksekusi semula oleh init() selepas migrasi()) akan
        # cipta semula hadis_fts + trigger dengan definisi baharu.
        # Isi terus dari data sedia ada:
        conn.execute("""
            CREATE VIRTUAL TABLE hadis_fts USING fts5(
                melayu, arab_carian,
                content='hadis', content_rowid='rowid_pk',
                tokenize='unicode61 remove_diacritics 2'
            )
        """)
        conn.execute("""
            INSERT INTO hadis_fts(rowid, melayu, arab_carian)
            SELECT rowid_pk, melayu, arab_carian FROM hadis
        """)
        conn.executescript("""
            CREATE TRIGGER hadis_ai AFTER INSERT ON hadis BEGIN
                INSERT INTO hadis_fts(rowid, melayu, arab_carian)
                    VALUES (new.rowid_pk, new.melayu, new.arab_carian);
            END;
            CREATE TRIGGER hadis_ad AFTER DELETE ON hadis BEGIN
                INSERT INTO hadis_fts(hadis_fts, rowid, melayu, arab_carian)
                    VALUES('delete', old.rowid_pk, old.melayu, old.arab_carian);
            END;
            CREATE TRIGGER hadis_au AFTER UPDATE ON hadis BEGIN
                INSERT INTO hadis_fts(hadis_fts, rowid, melayu, arab_carian)
                    VALUES('delete', old.rowid_pk, old.melayu, old.arab_carian);
                INSERT INTO hadis_fts(rowid, melayu, arab_carian)
                    VALUES (new.rowid_pk, new.melayu, new.arab_carian);
            END;
        """)
    conn.commit()
```

**Nota prestasi:** 62,169 baris — `UPDATE ... bersih_tashkeel_sql(arab)` dengan fungsi
Python custom akan lambat berbanding SQL tulen (anggaran beberapa saat, bukan minit —
selamat untuk migrasi sekali sahaja semasa pelancaran app, bukan setiap carian).

---

## 4. Normalisasi Query Pengguna (`_to_match_query`)

Query pengguna (Arab, dengan/tanpa tashkeel) mesti dibersihkan **sebelum** dihantar
ke FTS5, sebab index kini cuma simpan bentuk tanpa tashkeel:

```python
def _to_match_query(q: str, gabung: str = "AND") -> str:
    """... (dokstring sedia ada) ..."""
    q = bersih_tashkeel(q)      # BARIS BAHARU -- selamat untuk teks bukan-Arab
                                 # (regex tashkeel tak sepadan apa-apa dalam BM/ID)
    terms = _terms(q)
    if not terms:
        return ""
    parts = [f'"{t}"' for t in terms[:-1]] + [f'"{terms[-1]}"*']
    return f" {gabung} ".join(parts)
```

Satu baris sahaja — `bersih_tashkeel()` selamat dipanggil pada **semua** query
(Melayu/Indonesia/Arab) sebab regex tashkeel tidak sepadan apa-apa watak Latin.

**PENTING:** `api/hadis_api.py::search_hadis()` **import terus** `_to_match_query` dan
`pembobotan_fallback` dari `db.py` (`from db import _to_match_query`) — pembetulan
di atas **automatik** terpakai di situ juga, **tiada perubahan** perlu pada
`hadis_api.py`.

---

## 5. Senarai Fail Terjejas

| Fail | Perubahan |
|---|---|
| `db.py` | `bersih_tashkeel()` baharu, `SCHEMA` (lajur + FTS5), `SKEMA_VERSI` 7→8, `MIGRASI[8]`, `migrasi()` + `_backfill_arab_carian()` baharu, `_to_match_query()` 1 baris |
| `sync.py` | Setiap `INSERT`/`UPDATE` ke `hadis` isi `arab_carian = bersih_tashkeel(arab)` |
| `api/hadis_api.py` | **Tiada perubahan** (import terus dari `db.py`) |
| `semak.py` | Cadangan: tambah semakan baharu — `arab_carian` tiada NULL, carian `"كتب"` jumpa hadis mengandungi `"كَتَبَ"` |

---

## 6. Cadangan Ujian Pengesahan

```bash
python semak_db.py     # sahkan skema versi 8, lajur arab_carian wujud
python semak.py        # semua 169+ semakan lulus

# Ujian manual (python -c):
python -c "
import db
conn = db.init()
rows, total = db.search(conn, 'كتب')   # tanpa tashkeel
print('Jumlah hasil:', total)
assert total > 0, 'GAGAL: carian Arab tanpa tashkeel masih 0 hasil'
print('LULUS')
"
```

**Ujian regresi wajib:** pastikan carian Melayu/Indonesia sedia ada (`niat`, `puasa`,
`hukum riba`) masih berfungsi seperti biasa selepas perubahan — `bersih_tashkeel()`
sepatutnya tidak menyentuh teks bukan-Arab langsung.

---

*Draf ini belum dijalankan pada `hadis.db` sebenar. Sila sandarkan `hadis.db` sebelum
uji migrasi — walaupun `migrasi()` direka selamat-diulang, ini perubahan struktur FTS5
pertama seumur projek dan patut disemak manual dahulu.*
