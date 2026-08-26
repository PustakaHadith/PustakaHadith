"""HadisAPI — service.hadis.my, dengan mod offline SQLite pilihan.

Disahkan terhadap API sebenar:
  /collections                    -> data.collections  (list)
  /collections/{slug}             -> data.collection   (dict)
  /collections/{slug}/hadis       -> data.hadis + meta  | param: per_page (maks 100)
  /collections/{slug}/hadis/{id}  -> data.hadis        (dict)
  /hadis/search                   -> data.results      | param: q, collection, per_page
  /hadis/random                   -> data.hadis        (list)

Param `lang` (disahkan berfungsi pada SEMUA endpoint hadis):
  lang=ms  -> arab + melayu     (jimat ~30% bandwidth)
  lang=id  -> arab + indonesia
  (tiada)  -> arab + melayu + indonesia
  Nilai tidak sah (cth. 'melayu', 'en', 'ar') diabaikan senyap -> semua medan.

Had SEBENAR: 60 permintaan/minit, 200/hari (disahkan 2026-07-28).
Sync penuh 62,169 hadis = 622 request -> perlu 4 hari, atau naik taraf pelan.
"""

from __future__ import annotations

import os
import random
import re
import sqlite3
import time

import requests

try:
    from config import API_BASE_URL, DB_PATH, DEFAULT_PER_PAGE  # noqa: E402
except ImportError:
    API_BASE_URL = "https://service.hadis.my/api/v1"
    DEFAULT_PER_PAGE = 20
    import os as _os
    DB_PATH = _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
        "hadis.db")

MAX_PER_PAGE = 100  # minta lebih tetap dapat 100, tanpa amaran

VALID_SLUGS = {
    "bukhari", "muslim", "abu-daud", "tirmidzi", "nasai",
    "ibnu-majah", "ahmad", "darimi", "malik",
}

# Hanya nilai ini diterima pelayan; lain-lain diabaikan senyap.
VALID_LANGS = {"ms", "id"}

_FTS_SPECIAL = re.compile(r'["*()^:{}\[\]]')


def bina_huraian_he(conn, slug: str, hadis_id: int) -> dict | None:
    """Bina dict huraian HadeethEnc untuk UI daripada padanan + cache.

    Fungsi peringkat modul (corak sama seperti `core.sema_source.ambil`)
    supaya boleh diuji oleh semak_versi (hasattr modul) dan dipanggil
    oleh kedua-dua mod dalam talian / luar talian. Pulangkan None jika
    tiada padanan atau cache tidak wujud.
    """
    try:
        from core.hadeethenc_api import ambil, huraian
        r = ambil(conn, slug, hadis_id)
        if not r:
            return None
        he_id, jaccard, kaedah = r
        d = huraian(he_id)
        if not d:
            return None
        return {
            "he_id": he_id, "jaccard": jaccard, "kaedah": kaedah,
            "tajuk": d.get("title") or "",
            "hadeeth": d.get("hadeeth") or "",
            "grade": d.get("grade") or "",
            "explanation": d.get("explanation") or "",
            "hints": d.get("hints") or [],
        }
    except Exception:
        return None


class HadisAPIError(Exception):
    """Ralat am — mesej sudah dalam BM, selamat dipapar pada UI."""


class RateLimitExceeded(HadisAPIError):
    pass


class AuthError(HadisAPIError):
    pass


class NotFound(HadisAPIError):
    pass


class HadisAPI:
    def __init__(self, api_key: str = "", db_path: str = DB_PATH, use_db: bool = True):
        self.base_url = API_BASE_URL.rstrip("/")
        self._db_path = db_path
        self._last_request = 0.0
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})

        # Kuota terkini (dari header respons) — boleh dipapar pada UI
        self.rate_remaining: int | None = None
        self.daily_remaining: int | None = None

        # Mod offline
        self.conn: sqlite3.Connection | None = None
        if use_db and os.path.exists(db_path):
            try:
                c = sqlite3.connect(db_path, check_same_thread=False)
                c.row_factory = sqlite3.Row
                if c.execute("SELECT COUNT(*) FROM hadis").fetchone()[0] > 0:
                    self.conn = c
                    # Jalankan migrasi skema yang tertinggal (cth. jadual
                    # `bab`, `darjat`) supaya query tidak ralat "no such table".
                    try:
                        from db import migrasi
                        migrasi(c)
                    except Exception:
                        pass
            except Exception:
                self.conn = None

    @property
    def offline(self) -> bool:
        return self.conn is not None

    def set_key(self, api_key: str) -> None:
        self.session.headers.update({"X-API-Key": api_key})

    # ---------- teras rangkaian ----------

    def _throttle(self) -> None:
        elapsed = time.time() - self._last_request
        if elapsed < 1.1:   # 1.1s ≈ 54 req/min, di bawah had 60
            time.sleep(1.1 - elapsed)
        self._last_request = time.time()

    def _request(self, path: str, params: dict | None = None) -> dict:
        """Pulangkan payload JSON penuh, atau lempar subkelas HadisAPIError."""
        url = f"{self.base_url}{path}"
        last_err = "Gagal menghubungi pelayan."

        for attempt in range(3):
            self._throttle()
            try:
                resp = self.session.get(url, params=params, timeout=20)
            except requests.Timeout:
                last_err = "Sambungan tamat masa."
                time.sleep((attempt + 1) * 2)
                continue
            except requests.ConnectionError:
                last_err = "Tiada sambungan internet."
                time.sleep((attempt + 1) * 2)
                continue

            self._read_quota(resp)

            if resp.status_code == 429:
                # Cuba semula DULU; hanya menyerah selepas percubaan terakhir
                if attempt < 2:
                    wait = float(resp.headers.get("Retry-After", 0)) or \
                           (attempt + 1) * 2 + random.uniform(0, 1)
                    time.sleep(wait)
                    continue
                raise RateLimitExceeded(
                    self._msg(resp, "Had permintaan dicapai. Cuba sebentar lagi.")
                )

            if resp.status_code == 401:
                raise AuthError(self._msg(resp, "API key tidak sah."))
            if resp.status_code == 403:
                raise AuthError(self._msg(resp, "Akses ditolak."))
            if resp.status_code == 404:
                raise NotFound(self._msg(resp, "Tidak dijumpai."))

            if resp.status_code >= 500:
                last_err = f"Ralat pelayan ({resp.status_code})."
                time.sleep((attempt + 1) * 2)
                continue

            try:
                data = resp.json()
            except ValueError:
                raise HadisAPIError("Respons pelayan tidak sah.")

            if not data.get("success"):
                raise HadisAPIError(data.get("message", "Ralat API."))
            return data

        raise HadisAPIError(last_err)

    @staticmethod
    def _msg(resp, fallback: str) -> str:
        try:
            return resp.json().get("message") or fallback
        except Exception:
            return fallback

    def _read_quota(self, resp) -> None:
        h = resp.headers
        try:
            if "x-ratelimit-remaining" in h:
                self.rate_remaining = int(h["x-ratelimit-remaining"])
            if "x-ratelimit-daily-remaining" in h:
                self.daily_remaining = int(h["x-ratelimit-daily-remaining"])
        except (TypeError, ValueError):
            pass

    @staticmethod
    def _norm_lang(lang: str | None) -> str | None:
        """Terima 'ms'/'melayu'/'my'/'id'/'indonesia'; pulangkan 'ms'/'id'/None."""
        if not lang:
            return None
        l = lang.strip().lower()
        if l in ("ms", "my", "melayu", "malay", "bm"):
            return "ms"
        if l in ("id", "indonesia", "indonesian"):
            return "id"
        return None

    @staticmethod
    def _row(r: sqlite3.Row, lang: str | None = None) -> dict:
        d = {"id": r["hadis_id"], "collection": r["collection"], "arab": r["arab"]}
        if lang == "ms":
            d["melayu"] = r["melayu"]
        elif lang == "id":
            d["indonesia"] = r["indonesia"]
        else:
            d["melayu"] = r["melayu"]
            d["indonesia"] = r["indonesia"]
        # Nama bab (Fasa 3) -- hadir hanya jika query menggabung jadual bab.
        try:
            if "book" in r.keys():
                d["book"] = r["book"]
                d["nama_bab"] = r["nama_bab"]
        except Exception:
            pass
        return d



    def _english(self, slug: str, hadis_id: int) -> str:
        """Ambil terjemahan Inggeris dari jadual terjemahan_eng.

        Jadual ini diisi oleh `sync_english.py` melalui padanan teks
        Arab (hadis.my tidak menyediakan Inggeris, dan penomboran
        sumber luar berbeza). Jika jadual tiada, pulangkan kosong --
        UI akan papar "tidak tersedia" dengan jujur.
        """
        if not self.conn:
            return ""
        try:
            r = self.conn.execute(
                "SELECT english FROM terjemahan_eng "
                "WHERE collection=? AND hadis_id=?", (slug, hadis_id)).fetchone()
        except sqlite3.Error:
            return ""          # jadual belum dicipta
        return (r[0] if r else "") or ""

    def _english_luar(self, slug: str, hadis_id: int) -> str:
        """Baca terjemahan_eng walaupun dalam mod dalam talian."""
        if self.conn:
            return self._english(slug, hadis_id)
        if not os.path.exists(self._db_path):
            return ""
        try:
            c = sqlite3.connect(self._db_path)
            r = c.execute("SELECT english FROM terjemahan_eng "
                          "WHERE collection=? AND hadis_id=?",
                          (slug, hadis_id)).fetchone()
            c.close()
        except sqlite3.Error:
            return ""
        return (r[0] if r else "") or ""

    def _sema(self, slug: str, hadis_id: int) -> dict | None:
        """Huraian SemakHadis (BM) daripada jadual semakhadis."""
        if not self.conn:
            return None
        try:
            from core.sema_source import ambil
            return ambil(self.conn, slug, hadis_id)
        except Exception:
            return None

    def _sema_luar(self, slug: str, hadis_id: int) -> dict | None:
        """Baca huraian SemakHadis walaupun dalam mod dalam talian."""
        if self.conn:
            return self._sema(slug, hadis_id)
        if not os.path.exists(self._db_path):
            return None
        try:
            c = sqlite3.connect(self._db_path)
            from core.sema_source import ambil
            r = ambil(c, slug, hadis_id)
            c.close()
            return r
        except Exception:
            return None

    def _he(self, slug: str, hadis_id: int) -> dict | None:
        """Huraian HadeethEnc (BM) — sandaran bila SemakHadis tiada."""
        if not self.conn:
            return None
        return bina_huraian_he(self.conn, slug, hadis_id)

    def _he_luar(self, slug: str, hadis_id: int) -> dict | None:
        """Baca huraian HadeethEnc walaupun dalam mod dalam talian."""
        if self.conn:
            return self._he(slug, hadis_id)
        if not os.path.exists(self._db_path):
            return None
        try:
            c = sqlite3.connect(self._db_path)
            try:
                return bina_huraian_he(c, slug, hadis_id)
            finally:
                c.close()
        except Exception:
            return None

    def _darjat(self, slug: str, hadis_id: int) -> list[dict]:
        """Penilaian ulama moden, papar mentah tanpa tafsiran (Sesi 14).

        Susunan baris ialah susunan simpanan (CDN) -- TIADA susunan
        keutamaan. Papar semua nama + teks apa adanya.
        """
        if not self.conn:
            return []
        try:
            rows = self.conn.execute(
                "SELECT nama_ulama, darjat FROM darjat "
                "WHERE collection=? AND hadis_id=? ORDER BY rowid",
                (slug, hadis_id)).fetchall()
        except sqlite3.Error:
            return []          # jadual belum dicipta
        return [{"nama": r["nama_ulama"], "darjat": r["darjat"]} for r in rows]

    def _darjat_luar(self, slug: str, hadis_id: int) -> list[dict]:
        """Baca darjat walaupun dalam mod dalam talian."""
        if self.conn:
            return self._darjat(slug, hadis_id)
        if not os.path.exists(self._db_path):
            return []
        try:
            c = sqlite3.connect(self._db_path)
            rows = c.execute(
                "SELECT nama_ulama, darjat FROM darjat "
                "WHERE collection=? AND hadis_id=? ORDER BY rowid",
                (slug, hadis_id)).fetchall()
            c.close()
        except sqlite3.Error:
            return []
        return [{"nama": r[0], "darjat": r[1]} for r in rows]

    # ---------- kaedah awam ----------

    def get_collections(self) -> list[dict]:
        if self.conn:
            rows = self.conn.execute(
                "SELECT slug,name,author,total_hadis FROM collections ORDER BY rowid"
            ).fetchall()
            if rows:
                return [dict(r) for r in rows]
        return self._request("/collections")["data"]["collections"]

    def get_collection_info(self, slug: str) -> dict | None:
        if self.conn:
            r = self.conn.execute(
                "SELECT slug,name,author,total_hadis FROM collections WHERE slug=?",
                (slug,),
            ).fetchone()
            if r:
                return dict(r)
            return None
        try:
            return self._request(f"/collections/{slug}")["data"]["collection"]
        except NotFound:
            return None

    def get_bab_list(self, slug: str) -> list[dict]:
        """Senarai buku/kitab dalam koleksi + kiraan hadis (DB tempatan).

        Sidebar "PILIH BAB" halaman Senarai Hadis (26 Ogos). nama_bab
        diambil MIN() (nama seksyen pertama buku itu — Inggeris apa
        adanya dari CDN, pola sama kad hadis). Tiada DB / tiada jadual
        bab / ralat → [] (UI sembunyi bahagian bab).
        """
        if not self.conn:
            return []
        try:
            rows = self.conn.execute(
                "SELECT b.book, MIN(b.nama_bab) AS nama_bab, COUNT(*) AS kiraan "
                "FROM bab b WHERE b.collection=? AND b.book IS NOT NULL "
                "GROUP BY b.book ORDER BY b.book", (slug,)).fetchall()
        except Exception:
            return []
        return [{"book": r["book"], "nama_bab": r["nama_bab"],
                 "kiraan": r["kiraan"]} for r in rows]

    def get_hadis_list(self, slug: str, page: int = 1,
                       limit: int = DEFAULT_PER_PAGE,
                       lang: str | None = None, book=None, order: str = "asc",
                       ids: list | None = None,
                       exclude_ids: list | None = None) -> dict:
        """Pulangkan {'hadis': [...], 'meta': {...}}. lang='ms' jimat ~30% data.

        Param halaman Senarai Hadis (26 Ogos) — DB tempatan SAHAJA;
        mod dalam talian (tiada conn) param diabaikan dan UI menyahaktif
        kawalan berkaitan:
          book       → b.book=? (tapis bab/kitab dalam koleksi)
          order      → "desc" susunan hadis_id menurun ("asc" lalai)
          ids        → hadis_id IN (...) — penapis "Tersimpan";
                       senarai KOSONG → pulangkan hasil kosong
          exclude_ids→ hadis_id NOT IN (...) — penapis "Belum dibaca"
        """
        limit = max(1, min(limit, MAX_PER_PAGE))
        lang = self._norm_lang(lang)

        if self.conn:
            syarat = ["h.collection=?"]
            params: list = [slug]
            if book is not None:
                syarat.append("b.book=?")
                params.append(book)
            if ids is not None:
                if not ids:
                    return {"hadis": [],
                            "meta": {"current_page": page, "per_page": limit,
                                     "total": 0, "last_page": 1}}
                syarat.append(
                    f"h.hadis_id IN ({','.join('?' * len(ids))})")
                params.extend(int(i) for i in ids)
            if exclude_ids:
                syarat.append(
                    f"h.hadis_id NOT IN ({','.join('?' * len(exclude_ids))})")
                params.extend(int(i) for i in exclude_ids)
            urutan = "DESC" if order == "desc" else "ASC"
            where = " AND ".join(syarat)
            rows = self.conn.execute(
                "SELECT h.hadis_id,h.collection,h.arab,h.melayu,h.indonesia,"
                "b.book,b.nama_bab FROM hadis h "
                "LEFT JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id "
                f"WHERE {where} ORDER BY h.hadis_id {urutan} LIMIT ? OFFSET ?",
                (*params, limit, (page - 1) * limit),
            ).fetchall()
            total = self.conn.execute(
                f"SELECT COUNT(*) FROM hadis h "
                "LEFT JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id "
                f"WHERE {where}", params).fetchone()[0]
            return {"hadis": [self._row(r, lang) for r in rows],
                    "meta": {"current_page": page, "per_page": limit, "total": total,
                             "last_page": max(1, -(-total // limit))}}

        params = {"page": page, "per_page": limit}
        if lang:
            params["lang"] = lang
        d = self._request(f"/collections/{slug}/hadis", params)
        if order == "desc":
            d["data"]["hadis"] = list(reversed(d["data"]["hadis"]))
        return {"hadis": d["data"]["hadis"], "meta": d.get("meta", {})}

    def get_hadis_by_id(self, slug: str, hadis_id: int,
                        lang: str | None = None) -> dict | None:
        lang = self._norm_lang(lang)
        if self.conn:
            r = self.conn.execute(
                "SELECT h.hadis_id,h.collection,h.arab,h.melayu,h.indonesia,"
                "b.book,b.nama_bab FROM hadis h "
                "LEFT JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id "
                "WHERE h.collection=? AND h.hadis_id=?", (slug, hadis_id),
            ).fetchone()
            if not r:
                return None
            d = self._row(r, lang)
            en = self._english(slug, hadis_id)
            if en:
                d["english"] = en
            d["darjat"] = self._darjat(slug, hadis_id)
            d["sema"] = self._sema(slug, hadis_id)
            return d
        try:
            params = {"lang": lang} if lang else None
            h = self._request(f"/collections/{slug}/hadis/{hadis_id}",
                              params)["data"]["hadis"]
            h.setdefault("collection", slug)
            # Inggeris disimpan tempatan walaupun hadis datang dari API.
            # Buka DB atas permintaan -- mod dalam talian tidak
            # menyimpannya sebagai self.conn.
            if not h.get("english"):
                en = self._english_luar(slug, hadis_id)
                if en:
                    h["english"] = en
            h["darjat"] = self._darjat_luar(slug, hadis_id)
            h["sema"] = self._sema_luar(slug, hadis_id)
            return h
        except NotFound:
            return None

    # Alias untuk keserasian ke belakang
    get_single_hadis = get_hadis_by_id

    def search_hadis(self, query: str, slug: str | None = None, page: int = 1,
                     limit: int = DEFAULT_PER_PAGE,
                     lang: str | None = None) -> dict:
        """Carian. `slug` menapis ikut kitab (API menyokongnya)."""
        limit = max(1, min(limit, MAX_PER_PAGE))
        lang = self._norm_lang(lang)

        if self.conn:
            from db import _to_match_query
            if not _to_match_query(query):
                return {"hadis": [], "meta": {"total": 0, "last_page": 1}}

            def _kira(m: str) -> int:
                where, args = "hadis_fts MATCH ?", [m]
                if slug:
                    where += " AND h.collection=?"
                    args.append(slug)
                return self.conn.execute(
                    f"SELECT COUNT(*) FROM hadis_fts JOIN hadis h "
                    f"ON h.rowid_pk=hadis_fts.rowid WHERE {where}", args
                ).fetchone()[0]

            # Fallback OR (kes "hukum riba"): FTS5 AND memerlukan SEMUA
            # perkataan hadir. Bila AND pulang 0 hasil dan ada >1 perkataan,
            # cuba OR supaya kad keyword tetap dipapar. `fallback` ditanda
            # dalam meta (hanya jika OR benar-benar pulang hasil) supaya UI
            # boleh papar nota "carian longgar". Kira dahulu, SELECT sekali.
            fallback = False
            m = _to_match_query(query)                 # AND (lalai)
            total = _kira(m)
            if total == 0 and _to_match_query(query, "OR") != m:
                m = _to_match_query(query, "OR")
                total = _kira(m)
                fallback = total > 0

            where, args = "hadis_fts MATCH ?", [m]
            if slug:
                where += " AND h.collection=?"
                args.append(slug)
            if fallback:
                # Pembobotan: hadis dengan SEMUA perkataan padan di atas
                # (BM25 asal boleh letak hadis satu-perkataan-jarang dahulu).
                from db import pembobotan_fallback
                order, like_args = pembobotan_fallback(query)
                args = args + like_args
            else:
                order = "bm25(hadis_fts,10.0,1.0)"
            rows = self.conn.execute(
                f"SELECT h.hadis_id,h.collection,h.arab,h.melayu,h.indonesia,"
                f"b.book,b.nama_bab FROM hadis_fts "
                f"JOIN hadis h ON h.rowid_pk=hadis_fts.rowid "
                f"LEFT JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id "
                f"WHERE {where} ORDER BY {order} LIMIT ? OFFSET ?",
                (*args, limit, (page - 1) * limit),
            ).fetchall()
            meta = {"current_page": page, "per_page": limit, "total": total,
                    "last_page": max(1, -(-total // limit))}
            if fallback:
                meta["fallback"] = True
            return {"hadis": [self._row(r, lang) for r in rows], "meta": meta}

        params = {"q": query, "page": page, "per_page": limit}
        if slug:
            params["collection"] = slug
        if lang:
            params["lang"] = lang
        d = self._request("/hadis/search", params)
        return {"hadis": d["data"].get("results", []), "meta": d.get("meta", {})}

    def get_random_hadis(self, collection: str | None = None, count: int = 1,
                         lang: str | None = None) -> list[dict]:
        lang = self._norm_lang(lang)
        if self.conn:
            if collection:
                rows = self.conn.execute(
                    "SELECT h.hadis_id,h.collection,h.arab,h.melayu,h.indonesia,"
                    "b.book,b.nama_bab FROM hadis h "
                    "LEFT JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id "
                    "WHERE h.collection=? ORDER BY RANDOM() LIMIT ?",
                    (collection, count)
                ).fetchall()
            else:
                rows = self.conn.execute(
                    "SELECT h.hadis_id,h.collection,h.arab,h.melayu,h.indonesia,"
                    "b.book,b.nama_bab FROM hadis h "
                    "LEFT JOIN bab b ON b.collection=h.collection AND b.hadis_id=h.hadis_id "
                    "ORDER BY RANDOM() LIMIT ?", (count,)
                ).fetchall()
            return [self._row(r, lang) for r in rows]

        params = {"count": count}
        if collection:
            params["collection"] = collection
        if lang:
            params["lang"] = lang
        h = self._request("/hadis/random", params)["data"].get("hadis", [])
        return h if isinstance(h, list) else [h]

    def max_hadis_id(self, slug: str) -> int:
        """Sempadan atas untuk butang 'Seterusnya'."""
        if self.conn:
            r = self.conn.execute(
                "SELECT MAX(hadis_id) FROM hadis WHERE collection=?", (slug,)
            ).fetchone()[0]
            return r or 0
        try:
            for c in self.get_collections():
                if c["slug"] == slug:
                    return c.get("total_hadis", 0)
        except HadisAPIError:
            pass
        return 0
