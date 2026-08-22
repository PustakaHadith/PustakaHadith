"""Lapisan SQLite + FTS5 untuk hadis. Offline, tiada API key diperlukan."""

from __future__ import annotations

import os
import re
import sqlite3
import unicodedata

from config import DB_PATH  # noqa: E402  (laluan pusat, INSTALLER.md §3)

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


SCHEMA = """
-- WAL sengaja dikekalkan. Diuji Sesi 7:
--   baca sambil tulis : WAL 819 vs DELETE 405 bacaan / 2 saat
--   tulis/baca/carian : perbezaan boleh diabaikan
-- Fail -wal dan -shm hanya wujud semasa sambungan TERBUKA, dan
-- dibersihkan automatik pada penutupan bersih. Selepas crash ia
-- kekal, tetapi hilang sendiri apabila DB dibuka semula -- data
-- selamat (disahkan 2,000 baris utuh selepas proses dibunuh).
-- Ini penting kerana apl membaca melalui QThread worker sementara
-- sync.py mungkin sedang menulis.
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS collections (
    slug        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    author      TEXT,
    total_hadis INTEGER
);

CREATE TABLE IF NOT EXISTS hadis (
    rowid_pk   INTEGER PRIMARY KEY AUTOINCREMENT,
    collection TEXT NOT NULL REFERENCES collections(slug),
    hadis_id   INTEGER NOT NULL,
    arab       TEXT,
    arab_carian TEXT,          -- BAHARU: arab tanpa tashkeel, untuk FTS sahaja
    melayu     TEXT,
    indonesia  TEXT,
    UNIQUE(collection, hadis_id)
);

CREATE INDEX IF NOT EXISTS idx_hadis_col ON hadis(collection);

-- FTS5 luaran: index Melayu + Arab (tanpa tashkeel, lihat bersih_tashkeel())
CREATE VIRTUAL TABLE IF NOT EXISTS hadis_fts USING fts5(
    melayu, arab_carian,
    content='hadis',
    content_rowid='rowid_pk',
    tokenize='unicode61 remove_diacritics 2'
);

-- TRIGGER hadis_ai/ad/au TIDAK dicipta di sini (SCHEMA). Sebab:
-- DB lama (skema < 8) belum ada kolum `arab_carian` pada masa SCHEMA
-- dieksekusi -- CREATE TRIGGER yang merujuk new.arab_carian akan
-- GAGAL ("no such column"). Trigger dicipta dalam _backfill_arab_carian()
-- semasa migrasi ke skema 8 (kolum sudah wujud) -- selamat untuk DB
-- lama mahupun DB baharu.

-- Simpanan penanda/kegemaran pengguna
CREATE TABLE IF NOT EXISTS favorites (
    collection TEXT NOT NULL,
    hadis_id   INTEGER NOT NULL,
    note       TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (collection, hadis_id)
);
"""


def connect(path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------- migrasi
#
# SKEMA_VERSI dinaikkan setiap kali struktur DB berubah. `init()`
# menjalankan migrasi yang tertinggal secara automatik, jadi pengguna
# sedia ada tidak perlu memadam hadis.db mereka.
#
# Sejarah:
#   0 -> 1  asas: collections, hadis, hadis_fts, favorites
#   1 -> 2  terjemahan_eng  (Fasa 3 - Inggeris dipadan ikut teks Arab)
#   2 -> 3  syarah          (Fasa 4B - Fath al-Bari, dipadan ikut nombor)
#   3 -> 4  hadethenc       (Fasa 4 - HadeethEnc, dipadan ikut teks Arab)
#   4 -> 5  bab             (Fasa 3 - nama bab + nombor buku CDN,
#                            dipadan ikut nombor edisi yang sama dengan
#                            terjemahan_eng)
#   5 -> 6  darjat          (Fasa 3 - penilaian ulama moden daripada
#                            metadata CDN, papar mentah tanpa tafsiran)
#   6 -> 7  semakhadis      (Fasa 4 - huraian Bahasa Melayu daripada
#                            SemakHadis.com, dipadan ikut teks Arab;
#                            jadual menyimpan data lengkap + skor padanan)
#   7 -> 8  arab_carian     (lajur baharu: arab tanpa tashkeel untuk FTS5;
#                            fix carian Arab tanpa harakat -- GTAF.md §4-5)
#
SKEMA_VERSI = 8


MIGRASI: dict[int, str] = {
    2: """
    CREATE TABLE IF NOT EXISTS terjemahan_eng (
        collection TEXT NOT NULL,
        hadis_id   INTEGER NOT NULL,
        english    TEXT NOT NULL,
        sumber     TEXT DEFAULT 'fawazahmed0/hadith-api',
        PRIMARY KEY (collection, hadis_id)
    );
    """,
    3: """
    CREATE TABLE IF NOT EXISTS syarah (
        collection TEXT NOT NULL,
        hadis_id   INTEGER NOT NULL,
        kitab      TEXT NOT NULL,      -- cth 'fathbari'
        pengarang  TEXT,
        teks       TEXT NOT NULL,      -- Arab, tanpa baris
        PRIMARY KEY (collection, hadis_id, kitab)
    );
    CREATE INDEX IF NOT EXISTS idx_syarah_ref
        ON syarah(collection, hadis_id);
    """,
    4: """
    CREATE TABLE IF NOT EXISTS hadethenc (
        collection TEXT NOT NULL,
        hadis_id   INTEGER NOT NULL,
        he_id      INTEGER NOT NULL,   -- id hadis HadeethEnc
        jaccard    REAL NOT NULL,      -- skor padanan matn
        kaedah     TEXT NOT NULL,      -- 'penuh' | 'matn'
        PRIMARY KEY (collection, hadis_id)
    );
    CREATE INDEX IF NOT EXISTS idx_hadethenc_he ON hadethenc(he_id);
    """,
    5: """
    CREATE TABLE IF NOT EXISTS bab (
        collection TEXT NOT NULL,
        hadis_id   INTEGER NOT NULL,
        book       INTEGER NOT NULL,   -- nombor buku CDN (reference.book)
        nama_bab   TEXT,               -- nama bab (metadata.sections, EN)
        PRIMARY KEY (collection, hadis_id)
    );
    CREATE INDEX IF NOT EXISTS idx_bab_col ON bab(collection);
    """,
    6: """
    CREATE TABLE IF NOT EXISTS darjat (
        collection TEXT NOT NULL,
        hadis_id   INTEGER NOT NULL,
        nama_ulama TEXT NOT NULL,      -- nama ulama moden, apa adanya
        darjat     TEXT NOT NULL,      -- teks darjat, apa adanya
        PRIMARY KEY (collection, hadis_id, nama_ulama)
    );
    CREATE INDEX IF NOT EXISTS idx_darjat_col ON darjat(collection);
    """,
    7: """
    CREATE TABLE IF NOT EXISTS semakhadis (
        collection TEXT NOT NULL,
        hadis_id   INTEGER NOT NULL,
        sema_id    TEXT NOT NULL,      -- id hadis SemakHadis.com
        jaccard    REAL NOT NULL,      -- skor padanan matn
        klasifikasi TEXT,              -- Sahih/Hasan/Daif/...
        tajuk      TEXT,               -- tajuk BM
        malay_text TEXT,               -- terjemahan BM
        intro      TEXT,               -- intro_commentary (takhrij)
        syarah     TEXT,               -- malay_commentary (komentar BM)
        PRIMARY KEY (collection, hadis_id)
    );
    CREATE INDEX IF NOT EXISTS idx_semakhadis_sema ON semakhadis(sema_id);
    """,
    8: """
    -- Tiada SQL di sini: kolum arab_carian + bina semula hadis_fts
    -- dikendalikan dalam _backfill_arab_carian() (Python) -- ALTER
    -- TABLE ADD COLUMN akan GAGAL pada DB baharu yang sudah mencipta
    -- kolum melalui SCHEMA, jadi semakan PRAGMA table_info perlu.
    """,
}


def versi(conn: sqlite3.Connection) -> int:
    return conn.execute("PRAGMA user_version").fetchone()[0]


def migrasi(conn: sqlite3.Connection, senyap: bool = True) -> int:
    """Jalankan migrasi yang tertinggal. Pulangkan bilangan dijalankan.

    Selamat dipanggil berulang kali -- migrasi yang sudah dijalankan
    dilangkau berdasarkan PRAGMA user_version.
    """
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

    # PRAGMA tidak menerima parameter terikat
    conn.execute(f"PRAGMA user_version={SKEMA_VERSI}")
    conn.commit()
    return dijalankan


def _fts_perlu_bina_semula(conn: sqlite3.Connection) -> bool:
    """FTS5 perlu dibina semula jika definisi lama (belum guna
    arab_carian) atau indeks KOSONG sedangkan jadual hadis berisi
    (kes migrasi terganggu: proses dibunuh semasa INSERT SELECT --
    user_version sudah 8 tetapi hadis_fts_data hampir kosong).
    """
    fts = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='hadis_fts'"
    ).fetchone()
    if fts is None:
        return True
    if "arab_carian" not in fts[0]:
        return True
    n_fts = conn.execute("SELECT count(*) FROM hadis_fts_data").fetchone()[0]
    n_hadis = conn.execute("SELECT count(*) FROM hadis").fetchone()[0]
    return n_hadis > 0 and n_fts < 10


def _backfill_arab_carian(conn: sqlite3.Connection, senyap: bool = True) -> None:
    """Isi arab_carian untuk baris sedia ada + bina semula hadis_fts.

    Dipanggil SEKALI semasa migrasi ke skema 8. Selamat dijalankan
    berulang (backfill hanya kena baris arab_carian IS NULL).

    NOTA: MIGRASI[8] sengaja TIDAK menjalankan ALTER TABLE -- DB baharu
    (dicipta terus dengan SCHEMA v8) sudah ada kolum arab_carian, jadi
    ALTER akan lempar "duplicate column name". Semakan PRAGMA di sini
    mengendalikan kedua-dua kes (DB lama v7: kolum tiada -> ALTER).
    """
    # 1. Pastikan kolum wujud (skip jika SCHEMA v8 sudah cipta)
    kolum = {r[1] for r in conn.execute("PRAGMA table_info(hadis)")}
    if "arab_carian" not in kolum:
        conn.execute("ALTER TABLE hadis ADD COLUMN arab_carian TEXT")

    conn.create_function("bersih_tashkeel_sql", 1, bersih_tashkeel)
    n = conn.execute(
        "UPDATE hadis SET arab_carian = bersih_tashkeel_sql(arab) "
        "WHERE arab_carian IS NULL"
    ).rowcount
    if not senyap:
        print(f"  arab_carian diisi untuk {n:,} baris")

    # hadis_fts lama (jika wujud dari skema < 8) masih rujuk kolum 'arab'
    # mentah -- gantikan definisi jadual & bina semula index dari awal.
    # Termasuk kes migrasi terganggu: definisi sudah baharu tetapi indeks
    # KOSONG (proses dibunuh semasa INSERT SELECT) -- bina semula juga.
    if _fts_perlu_bina_semula(conn):
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

    # DB BAHARU (dicipta terus dengan SCHEMA v8): hadis_fts sudah guna
    # arab_carian jadi blok bina-semula di atas dilangkau, tetapi SCHEMA
    # TIDAK mencipta trigger (elak gagal pada DB lama -- lihat komen
    # SCHEMA). Pastikan trigger wujud di sini -- IF NOT EXISTS no-op
    # untuk DB yang sudah lengkap.
    conn.executescript("""
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
    """)
    conn.commit()


def init(path: str = DB_PATH) -> sqlite3.Connection:
    """Buka DB, cipta skema asas, dan jalankan migrasi tertinggal."""
    conn = connect(path)
    conn.executescript(SCHEMA)

    # DB sedia ada dari sebelum sistem versi diperkenalkan akan
    # melaporkan user_version=0. Jadual asas sudah ada (CREATE IF NOT
    # EXISTS di atas), jadi mula migrasi dari versi 1.
    if versi(conn) == 0:
        conn.execute("PRAGMA user_version=1")
        conn.commit()

    migrasi(conn)

    # Self-heal: jika migrasi sebelum ini terganggu (proses dibunuh
    # semasa bina semula FTS5), hadis_fts mungkin kosong walaupun
    # user_version sudah 8 -- baiki setiap kali dibuka. Kos: 2 COUNT
    # ringkas (< 10 ms); _backfill sendiri idempoten.
    if _fts_perlu_bina_semula(conn):
        _backfill_arab_carian(conn, senyap=False)
    return conn


# ---------- pertanyaan untuk UI ----------


def list_collections(conn) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT slug, name, author, total_hadis FROM collections ORDER BY rowid"
    ).fetchall()


def get_page(conn, collection: str, page: int = 1, per_page: int = 50):
    off = (page - 1) * per_page
    rows = conn.execute(
        "SELECT hadis_id, collection, arab, melayu, indonesia FROM hadis "
        "WHERE collection=? ORDER BY hadis_id LIMIT ? OFFSET ?",
        (collection, per_page, off),
    ).fetchall()
    total = conn.execute(
        "SELECT COUNT(*) FROM hadis WHERE collection=?", (collection,)
    ).fetchone()[0]
    return rows, total


def get_one(conn, collection: str, hadis_id: int):
    return conn.execute(
        "SELECT hadis_id, collection, arab, melayu, indonesia FROM hadis "
        "WHERE collection=? AND hadis_id=?",
        (collection, hadis_id),
    ).fetchone()


_FTS_SPECIAL = re.compile(r'["*()^:{}\[\]]')


def _to_match_query(q: str, gabung: str = "AND") -> str:
    """Tukar input pengguna kepada query FTS5 yang selamat (elak SQL/FTS syntax error).

    `gabung` = "AND" (semua perkataan wajib) atau "OR" (mana-mana satu)
    untuk fallback bila AND pulang 0 hasil. Perkataan akhir dibenarkan
    prefix match dalam kedua-dua mod.

    Query pengguna dibersihkan tashkeel dahulu -- index hadis_fts kini
    simpan `arab_carian` (tanpa harakat), jadi query bertashkeel penuh
    tidak akan sepadan tanpa langkah ini. Selamat untuk teks bukan-Arab
    (regex tashkeel tak sepadan apa-apa dalam BM/ID).
    """
    q = bersih_tashkeel(q)      # BARIS BAHARU (skema 8): selamat utk semua query
    terms = _terms(q)
    if not terms:
        return ""
    # Setiap perkataan wajib ada; perkataan akhir dibenarkan prefix match
    parts = [f'"{t}"' for t in terms[:-1]] + [f'"{terms[-1]}"*']
    return f" {gabung} ".join(parts)


def _terms(q: str) -> list[str]:
    """Perkataan bersih daripada input pengguna (selepas buang aksara FTS)."""
    return [t for t in _FTS_SPECIAL.sub(" ", q).strip().split() if t]


def pembobotan_fallback(query: str) -> tuple[str, list[str]]:
    """Klausa ORDER BY + argumen LIKE untuk ranking fallback OR.

    BM25 semata-mata memberi berat kepada term jarang, jadi hadis dengan
    SATU perkataan jarang boleh naik melebihi hadis dengan SEMUA perkataan
    padan. Bonus: +1 bagi setiap perkataan yang wujud dalam teks Melayu
    (LIKE, parameter terikat -- selamat dari SQL injection; `%`/`_` dalam
    input bertindak sebagai wildcard, diterima). `_`/`%` tidak dibuang
    supaya konsisten dengan token FTS5; `%term%` ialah full scan tetapi
    hanya pada laluan fallback yang jarang.

    Pulangkan (klausa ORDER BY, argumen LIKE) untuk disisip dalam query.
    """
    bonus, like_args = [], []
    for t in _terms(query):
        bonus.append("(CASE WHEN h.melayu LIKE ? THEN 1 ELSE 0 END)")
        like_args.append(f"%{t}%")
    padanan = " + ".join(bonus)
    return f"({padanan}) DESC, bm25(hadis_fts, 10.0, 1.0) ASC", like_args


def search(conn, query: str, collection: str | None = None,
           limit: int = 50, offset: int = 0):
    """Carian offline dengan ranking BM25 + petikan bertanda.

    Fallback OR: FTS5 AND memerlukan SEMUA perkataan hadir (kes "hukum
    riba" pulang 0 hasil walaupun setiap perkataan wujud berasingan).
    Bila AND pulang 0 hasil dan ada >1 perkataan, cuba OR supaya kad
    keyword tetap dipapar.

    Ranking pembobotan (fallback sahaja): BM25 semata-mata boleh letak
    hadis dengan SATU perkataan jarang di atas hadis dengan SEMUA
    perkataan -- hadis yang padan lebih banyak perkataan mesti dahulu.
    """

    m = _to_match_query(query)
    if not m:
        return [], 0

    def _kira(m: str) -> int:
        where = "hadis_fts MATCH ?"
        args: list = [m]
        if collection:
            where += " AND h.collection = ?"
            args.append(collection)
        return conn.execute(
            f"SELECT COUNT(*) FROM hadis_fts JOIN hadis h "
            f"ON h.rowid_pk=hadis_fts.rowid WHERE {where}", args
        ).fetchone()[0]

    # Fallback OR: kira AND dahulu; jika 0 dan ada >1 perkataan (query
    # OR berbeza), cuba OR. Kira dahulu, SELECT sekali sahaja.
    fallback = False
    total = _kira(m)
    if total == 0 and _to_match_query(query, "OR") != m:
        m = _to_match_query(query, "OR")
        fallback = True
        total = _kira(m)

    where = "hadis_fts MATCH ?"
    args: list = [m]
    if collection:
        where += " AND h.collection = ?"
        args.append(collection)

    if fallback:
        # Pembobotan: hadis dengan SEMUA perkataan padan naik ke atas,
        # bukan semata-mata perkataan paling jarang (tingkah laku BM25).
        order, like_args = pembobotan_fallback(query)
        args = args + like_args
    else:
        order = "bm25(hadis_fts, 10.0, 1.0)"

    sql = f"""
        SELECT h.hadis_id, h.collection, h.arab, h.melayu, h.indonesia,
               snippet(hadis_fts, 0, '<b>', '</b>', ' … ', 12) AS petikan,
               bm25(hadis_fts, 10.0, 1.0) AS skor
        FROM hadis_fts
        JOIN hadis h ON h.rowid_pk = hadis_fts.rowid
        WHERE {where}
        ORDER BY {order}
        LIMIT ? OFFSET ?
    """
    rows = conn.execute(sql, (*args, limit, offset)).fetchall()
    return rows, total


def random_hadis(conn, collection: str | None = None, count: int = 1):
    if collection:
        return conn.execute(
            "SELECT hadis_id, collection, arab, melayu, indonesia FROM hadis "
            "WHERE collection=? ORDER BY RANDOM() LIMIT ?",
            (collection, count),
        ).fetchall()
    return conn.execute(
        "SELECT hadis_id, collection, arab, melayu, indonesia FROM hadis "
        "ORDER BY RANDOM() LIMIT ?",
        (count,),
    ).fetchall()


# ---------- kegemaran ----------


def add_favorite(conn, collection: str, hadis_id: int, note: str = ""):
    conn.execute(
        "INSERT OR REPLACE INTO favorites(collection, hadis_id, note) VALUES (?,?,?)",
        (collection, hadis_id, note),
    )
    conn.commit()


def remove_favorite(conn, collection: str, hadis_id: int):
    conn.execute(
        "DELETE FROM favorites WHERE collection=? AND hadis_id=?", (collection, hadis_id)
    )
    conn.commit()


def list_favorites(conn):
    return conn.execute(
        "SELECT h.hadis_id, h.collection, h.arab, h.melayu, h.indonesia, f.note "
        "FROM favorites f JOIN hadis h "
        "ON h.collection=f.collection AND h.hadis_id=f.hadis_id "
        "ORDER BY f.created_at DESC"
    ).fetchall()
