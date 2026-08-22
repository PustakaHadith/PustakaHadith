"""Sumber terjemahan Inggeris — fawazahmed0/hadith-api.

MASALAH YANG DISELESAIKAN
-------------------------
API hadis.my memberi Melayu + Indonesia sahaja. Percubaan awal memadan
terjemahan Inggeris ikut NOMBOR HADIS gagal: penomboran antara sumber
berbeza (Bukhari 7,008 vs 7,589).

PENYELESAIAN
------------
Sumber ini menyediakan edisi ARAB (`ara-*`) di samping Inggeris (`eng-*`),
dan kedua-duanya berkongsi penomboran yang SAMA. Disahkan untuk 7 kitab:
nombor `ara-*` == nombor `eng-*`, 100%.

Jadi teks Arab menjadi jambatan:

    hadis.my (arab)  --padan teks-->  ara-*  --nombor sama-->  eng-*

Kunci padanan ialah **teks Arab dinormalisasi**, BUKAN ID. Ini kekal
betul walaupun penomboran hadis.my berbeza sepenuhnya.

LESEN & ATRIBUSI
----------------
Data: https://github.com/fawazahmed0/hadith-api  (domain awam / Unlicense)
Terjemahan Inggeris berasal daripada sunnah.com.
UI mesti memaparkan atribusi apabila teks Inggeris dipapar.

KITAB TIDAK TERSEDIA
--------------------
`ahmad` (Musnad Ahmad) dan `darimi` — tiada dalam sumber ini.
Tab English mesti kekal kelabu untuk kedua-duanya; jangan berpura-pura.
"""

from __future__ import annotations

import json
import os
import unicodedata
import re
import sqlite3

CDN = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions"

# slug hadis.my -> slug sumber
PETA_KITAB = {
    "bukhari": "bukhari",
    "muslim": "muslim",
    "abu-daud": "abudawud",
    "tirmidzi": "tirmidhi",
    "nasai": "nasai",
    "ibnu-majah": "ibnmajah",
    "malik": "malik",
    # "ahmad", "darimi" -- tiada dalam sumber ini
}

TIADA_SUMBER = ("ahmad", "darimi")


# ---------------------------------------------------------------- normalisasi

# 0610-0614 simbol penghormatan/selawat Arab (U+0610 ARABIC SIGN
# SALLALLAHOU ALAYHE WA SALLAM dsb.) -- ditemui semasa audit GTAF §6b;
# 064B-0652 tashkeel · 0653-0655 maddah/hamzah · 0656-065F tanda tambahan
# 0670 alif khanjariyyah · 0640 tatweel · 06D6-06ED tanda mushaf
_DIAKRITIK = re.compile(
    r"[\u0610-\u0614\u064B-\u065F\u0670\u0640\u06D6-\u06ED]")
_BUKAN_ARAB = re.compile(r"[^\u0621-\u064A ]")
_RUANG = re.compile(r"\s+")

# Varian huruf bukan-Arab (Farsi/Urdu) yang kelihatan sama tetapi
# titik kod berbeza. Tanpa pemetaan ini, satu huruf sahaja memusnahkan
# padanan seluruh hadis.
_VARIAN = {
    "\u0649": "\u064A",  # alif maqsura -> ya
    "\u06CC": "\u064A",  # Farsi yeh    -> ya
    "\u064A": "\u064A",
    "\u06A9": "\u0643",  # Farsi keheh  -> kaf
    "\u06AA": "\u0643",
    "\u0629": "\u0647",  # ta marbuta   -> ha
    "\u0624": "\u0648",  # waw hamzah   -> waw
    "\u0626": "\u064A",  # ya hamzah    -> ya
    "\u0623": "\u0627", "\u0625": "\u0627", "\u0622": "\u0627",
    "\u0671": "\u0627",  # alif wasla
    "\u0675": "\u0627",
    "\u06CD": "\u064A",
}
_JADUAL_VARIAN = str.maketrans(_VARIAN)


def normalisasi(teks: str) -> str:
    """Turunkan teks Arab kepada bentuk boleh banding.

    Buang tashkeel, lipat variasi ortografi. Digunakan HANYA untuk
    memadan -- teks asal tidak pernah diubah.

    Nota: di sini `ة -> ه` DIBENARKAN kerana ini kunci padanan dalaman,
    bukan indeks carian pengguna. (Untuk carian FTS, jangan lipat --
    lihat sesi_index.md.)
    """
    if not teks:
        return ""
    # NFKC meleraikan bentuk persembahan Arab (U+FE70-FEFF) dan ligatur
    # seperti U+FDFA kepada huruf asas. Tanpa ia, teks daripada PDF atau
    # sumber lama gagal dipadan sepenuhnya.
    s = unicodedata.normalize("NFKC", teks)
    s = _DIAKRITIK.sub("", s)
    s = s.translate(_JADUAL_VARIAN)
    s = _BUKAN_ARAB.sub(" ", s)
    return _RUANG.sub(" ", s).strip()


# Panjang awalan sandaran. Diuji: 60 aksara MENYEBABKAN 591 padanan
# salah dalam Bukhari sahaja -- banyak hadis berkongsi sanad yang sama
# tetapi matn berbeza ("hadthana Abdullah bin Yusuf ... Malik ... Aishah").
# Pada 200 aksara tinggal 14; teks penuh 0.
AWALAN_SANDARAN = 200


def kunci_padanan(teks: str) -> str:
    """Kunci utama: teks penuh dinormalisasi.

    Diuji terhadap 7 kitab: teks penuh memberi SIFAR padanan salah,
    manakala awalan 60 aksara memberi 591 (Bukhari), 559 (Muslim),
    472 (Nasai) -- kerana ramai perawi berkongsi rantaian sanad yang
    sama sedangkan matn berbeza sepenuhnya.
    """
    return normalisasi(teks)


def kunci_sandaran(teks: str) -> str:
    """Kunci kedua: awalan panjang, untuk teks yang hujungnya berbeza.

    Sumber kadang menambah atau memotong penghujung riwayat. Digunakan
    HANYA jika kunci penuh gagal, dan hanya bila awalan itu unik dalam
    indeks -- lihat `bina_indeks`.
    """
    return normalisasi(teks)[:AWALAN_SANDARAN]


# ---------------------------------------------------------------- muat turun

def url_edisi(kod: str) -> str:
    return f"{CDN}/{kod}.min.json"


def muat_json(laluan: str) -> dict:
    with open(laluan, encoding="utf-8") as f:
        return json.load(f)


def bina_indeks(fail_ara: str) -> tuple[dict[str, int], dict[str, int]]:
    """Bina dua indeks daripada edisi ara-*.

    Pulangkan (indeks_penuh, indeks_awalan).

    `indeks_awalan` HANYA mengandungi awalan yang unik. Awalan yang
    dikongsi lebih daripada satu hadis dibuang sepenuhnya -- lebih baik
    tiada terjemahan daripada terjemahan hadis yang salah.
    """
    hadis = muat_json(fail_ara).get("hadiths", [])

    penuh: dict[str, int] = {}
    for h in hadis:
        k = kunci_padanan(h.get("text", ""))
        if k and k not in penuh:
            penuh[k] = h.get("hadithnumber")

    kira: dict[str, int] = {}
    for h in hadis:
        k = kunci_sandaran(h.get("text", ""))
        if k:
            kira[k] = kira.get(k, 0) + 1

    awalan: dict[str, int] = {}
    for h in hadis:
        k = kunci_sandaran(h.get("text", ""))
        if k and kira[k] == 1:          # buang yang berlanggar
            awalan[k] = h.get("hadithnumber")

    return penuh, awalan


def bina_eng(fail_eng: str) -> dict[int, str]:
    """Peta {nombor_hadis: teks_inggeris}, kosong dilangkau."""
    out: dict[int, str] = {}
    for h in muat_json(fail_eng).get("hadiths", []):
        t = (h.get("text") or "").strip()
        if t:
            out[h.get("hadithnumber")] = t
    return out


def _bina_indeks_kata(sumber: dict[str, int],
                      teks_asal: dict[int, str]) -> dict[str, set[int]]:
    """Indeks terbalik: kata jarang -> nombor hadis yang mengandunginya.

    Digunakan oleh lapisan ketiga padanan. Kata yang muncul dalam
    lebih 5% hadis dibuang -- ia tidak membezakan apa-apa dan hanya
    melambatkan carian.
    """
    kira: dict[str, int] = {}
    peta: dict[str, set[int]] = {}
    for no, t in teks_asal.items():
        for w in set(normalisasi(t).split()):
            if len(w) < 4:
                continue
            kira[w] = kira.get(w, 0) + 1
            peta.setdefault(w, set()).add(no)
    had = max(3, len(teks_asal) // 20)
    return {w: v for w, v in peta.items() if kira[w] <= had}


# Ambang Jaccard untuk pengesahan dua hala lapisan `kata`.
#
# MENGAPA WUJUD
# -------------
# `padan_kata` mengira skor SEHALA: berapa banyak kata soalan dijumpai
# pada calon. Hadis yang TIADA langsung dalam sumber tetap mendapat
# skor tinggi apabila ia berkongsi sanad panjang dengan hadis lain --
# rantaian perawi sahaja boleh menjadi 80% daripada teks pendek.
#
# Diukur (Bukhari, 600 hadis dikeluarkan daripada indeks lalu dicari
# semula; jawapan BETUL ialah "tiada padanan"):
#     tanpa Jaccard   212/600 = 35.3% DIPADAN SALAH
#     Jaccard 0.75     56/600 =  9.3%
#     Jaccard 0.90     31/600 =  5.2%
#     Jaccard 0.95     25/600 =  4.2%
# Padanan BETUL yang hilang pada setiap ambang: SIFAR (448/600 kekal).
#
# 0.90 dipilih: membuang 85% positif palsu pada kos sifar. Daripada 31
# yang tinggal, 22 ialah teks yang normalisasinya IDENTIK (pendua tulen
# dalam Bukhari -- terjemahannya memang betul) dan hanya 9 benar-benar
# tersalah = 1.5%.
JACCARD_MIN = 0.90


def padan_kata(arab: str, indeks_kata: dict[str, set[int]],
               min_skor: float = 0.55,
               teks_sumber: dict[int, str] | None = None,
               jaccard_min: float = JACCARD_MIN) -> int | None:
    """Padanan longgar melalui pertindihan kata jarang.

    Lapisan terakhir, untuk teks yang berbeza sedikit antara sumber
    (ejaan, tanda baca, riwayat dipendekkan). Hanya diterima jika
    seorang calon jelas mengatasi yang kedua -- jika dua calon hampir
    sama baik, kita TOLAK. Lebih baik tiada terjemahan daripada
    terjemahan hadis yang salah.

    `teks_sumber` membolehkan pengesahan dua hala (Jaccard). Tanpa ia
    fungsi kekal berkelakuan lama -- tetapi jangan bergantung pada itu
    untuk data sebenar; lihat nota JACCARD_MIN.
    """
    set_soalan = set(normalisasi(arab).split())
    kata = [w for w in set_soalan if len(w) >= 4]
    kata = [w for w in kata if w in indeks_kata]
    if len(kata) < 4:
        return None
    skor: dict[int, int] = {}
    for w in kata:
        for no in indeks_kata[w]:
            skor[no] = skor.get(no, 0) + 1
    if not skor:
        return None
    tersusun = sorted(skor.items(), key=lambda x: -x[1])
    terbaik, n1 = tersusun[0]
    if n1 / len(kata) < min_skor:
        return None
    if len(tersusun) > 1 and tersusun[1][1] >= n1 * 0.85:
        return None          # dua calon terlalu rapat -- tidak selamat

    # Pengesahan DUA HALA. Skor di atas hanya bertanya "berapa banyak
    # kata soalan ada pada calon". Ia buta terhadap kata pada calon yang
    # TIADA pada soalan -- itulah yang membenarkan hadis asing lulus.
    if teks_sumber is not None:
        lain = teks_sumber.get(terbaik)
        if not lain:
            return None
        set_calon = set(normalisasi(lain).split())
        kesatuan = set_soalan | set_calon
        if not kesatuan:
            return None
        if len(set_soalan & set_calon) / len(kesatuan) < jaccard_min:
            return None
    return terbaik


# ---------------------------------------------- padanan melalui Indonesia
#
# PENEMUAN (audit saksi bebas, 26,911 hadis, 7 kitab)
# ---------------------------------------------------
# Audit membandingkan `hadis.db.indonesia` dengan CDN `ind-*` dan
# mendapat purata pertindihan 1.00 -- BUKAN 0.85 seperti dijangka
# bagi dua terjemahan bebas. Sebabnya: kedua-duanya berasal daripada
# terjemahan Indonesia yang SAMA.
#
# Implikasinya besar. Teks Indonesia ialah kunci padanan yang jauh
# lebih kukuh daripada Arab:
#   - Arab hadis.my bertashkeel penuh, CDN tidak      -> perlu normalisasi berat
#   - Arab berkongsi sanad panjang antara hadis       -> mudah tersalah padan
#   - Indonesia hampir identik aksara demi aksara     -> hampir tiada kekaburan
#
# Jadi cuba Indonesia DAHULU. Lapisan Arab kekal sebagai sandaran
# untuk hadis yang tiada teks Indonesia (Muslim: 2,636 kosong dalam
# CDN, Bukhari: 731).
_BUKAN_HURUF_ID = re.compile(r"[^a-z0-9 ]+")


def kunci_indonesia(teks: str) -> str:
    """Normalisasi teks Indonesia untuk padanan tepat.

    Buang kurungan perawi `[...]`, tanda baca, dan beza saiz huruf.
    hadis.my dan CDN kadang berbeza pada kurungan sahaja.
    """
    if not teks:
        return ""
    s = unicodedata.normalize("NFKC", teks).lower()
    s = s.replace("[", " ").replace("]", " ")
    s = _BUKAN_HURUF_ID.sub(" ", s)
    return _RUANG.sub(" ", s).strip()


def bina_indeks_ind(fail_ind: str) -> dict[str, int]:
    """Indeks {teks_indonesia_dinormalisasi: nombor}.

    Kunci yang BERLANGGAR dibuang sepenuhnya -- lebih baik jatuh ke
    lapisan Arab daripada memilih antara dua calun secara rambang.
    """
    hadis = muat_json(fail_ind).get("hadiths", [])
    kira: dict[str, int] = {}
    for h in hadis:
        k = kunci_indonesia(h.get("text", ""))
        if k:
            kira[k] = kira.get(k, 0) + 1
    out: dict[str, int] = {}
    for h in hadis:
        k = kunci_indonesia(h.get("text", ""))
        if k and kira[k] == 1:
            out[k] = h.get("hadithnumber")
    return out


# Ambang padanan KABUR Indonesia. Diuji ala-yatim (500 hadis dibuang
# daripada indeks, jawapan betul = "tiada"):
#     tirmidzi  0 positif palsu, 100% betul
#     bukhari  40 positif palsu -- 39 daripadanya teks IDENTIK
#              (pendua tulen; terjemahannya tetap betul), 1 tersalah
# 0.95 dipilih: ketat tetapi tidak menolak riwayat yang sah berbeza
# pada tanda baca atau kurungan perawi sahaja.
JACCARD_IND = 0.95
_MIN_TOKEN_IND = 4


def _token_ind(teks: str) -> set[str]:
    """Token bermakna daripada teks Indonesia.

    Kata henti dan istilah yang muncul dalam hampir setiap hadis
    dibuang -- tanpa itu dua hadis tidak berkaitan pun bertindih pada
    "telah, kepada, kami, Rasulullah".
    """
    if not teks:
        return set()
    s = _BUKAN_HURUF_ID.sub(" ", unicodedata.normalize("NFKC", teks).lower())
    return {w for w in s.split() if len(w) > 3 and w not in _HENTI_IND}


_HENTI_IND = {
    "yang", "dari", "dan", "itu", "ini", "pada", "dengan", "untuk",
    "telah", "tidak", "dia", "aku", "kami", "kamu", "kalian", "mereka",
    "adalah", "akan", "sudah", "bahwa", "bahawa", "ada", "oleh", "atau",
    "maka", "jika", "kalau", "saya", "kepada", "dalam", "seorang",
    "orang", "berkata", "katanya", "kata", "menceritakan", "kepadaku",
    "mengabarkan", "haddatsana", "hadits", "hadis", "allah",
    "rasulullah", "nabi", "shallallahu", "sallallahu", "alaihi",
    "wasallam", "radhiyallahu", "radiallahu", "anhu", "anha",
    "bin", "binti", "abu", "ibnu", "ibn", "abi", "sesungguhnya",
    "kemudian", "lalu", "ketika", "seperti", "juga", "saw", "swt",
}


def bina_indeks_ind_kata(indeks_ind_teks: dict[int, str]) -> dict[str, set[int]]:
    """Indeks terbalik token Indonesia -> nombor hadis."""
    kira: dict[str, int] = {}
    peta: dict[str, set[int]] = {}
    for no, t in indeks_ind_teks.items():
        for w in _token_ind(t):
            kira[w] = kira.get(w, 0) + 1
            peta.setdefault(w, set()).add(no)
    had = max(3, len(indeks_ind_teks) // 20)
    return {w: v for w, v in peta.items() if kira[w] <= had}


def padan_ind_kabur(teks: str, indeks_kata_ind: dict[str, set[int]],
                    teks_ind: dict[int, str]) -> int | None:
    """Padanan Indonesia yang toleran terhadap perbezaan kecil.

    hadis.my dan CDN berkongsi terjemahan yang sama, tetapi kadang
    berbeza pada tanda baca, kurungan perawi, atau potongan riwayat --
    cukup untuk memusnahkan padanan tepat. Lapisan ini menyelamatkannya
    tanpa jatuh ke teks Arab yang jauh lebih mudah tersalah.
    """
    tk = [w for w in _token_ind(teks) if w in indeks_kata_ind]
    if len(tk) < _MIN_TOKEN_IND:
        return None
    skor: dict[int, int] = {}
    for w in tk:
        for no in indeks_kata_ind[w]:
            skor[no] = skor.get(no, 0) + 1
    if not skor:
        return None
    tersusun = sorted(skor.items(), key=lambda x: -x[1])
    terbaik, n1 = tersusun[0]
    if n1 / len(tk) < 0.5:
        return None
    a = _token_ind(teks)
    b = _token_ind(teks_ind.get(terbaik, ""))
    if not a or not b:
        return None
    if len(a & b) / len(a | b) < JACCARD_IND:
        return None
    return terbaik


def padan(arab_hadis_my: str, penuh: dict[str, int],
          awalan: dict[str, int] | None = None,
          indeks_kata: dict[str, set[int]] | None = None,
          teks_sumber: dict[int, str] | None = None,
          ind_hadis_my: str = "",
          indeks_ind: dict[str, int] | None = None,
          indeks_ind_kata: dict[str, set[int]] | None = None,
          teks_ind: dict[int, str] | None = None) -> tuple[int | None, str]:
    """Cari nombor edisi bagi satu hadis hadis.my.

    Pulangkan (nombor, kaedah). Kaedah: "indo", "penuh", "awalan",
    "kata", atau "gagal". Sengaja memulangkan kaedah supaya kualiti
    padanan boleh diaudit dan dipaparkan kepada pengguna jika perlu.

    Turutan sengaja: Indonesia DAHULU. Audit saksi bebas menunjukkan
    teks Indonesia hadis.my dan CDN berkongsi asal yang sama, jadi
    padanannya hampir tepat -- manakala teks Arab berkongsi sanad
    panjang dan lebih mudah tersalah.
    """
    if ind_hadis_my:
        if indeks_ind:
            ki = kunci_indonesia(ind_hadis_my)
            if ki in indeks_ind:
                return indeks_ind[ki], "indo"
        # Padanan tepat gagal pada perbezaan remeh (tanda baca,
        # kurungan perawi). Cuba kabur SEBELUM jatuh ke Arab -- diukur
        # pada Tirmidzi: 0% positif palsu berbanding lapisan Arab yang
        # bergantung pada sanad dikongsi.
        if indeks_ind_kata and teks_ind:
            no = padan_ind_kabur(ind_hadis_my, indeks_ind_kata, teks_ind)
            if no is not None:
                return no, "indo~"

    k = kunci_padanan(arab_hadis_my)
    if k in penuh:
        return penuh[k], "penuh"
    if awalan:
        ka = kunci_sandaran(arab_hadis_my)
        if ka in awalan:
            return awalan[ka], "awalan"
    if indeks_kata:
        no = padan_kata(arab_hadis_my, indeks_kata, teks_sumber=teks_sumber)
        if no is not None:
            return no, "kata"
    return None, "gagal"


# ---------------------------------------------------------------- skema DB

def pasang_skema(conn: sqlite3.Connection) -> None:
    """Pastikan jadual terjemahan_eng wujud.

    Skema sebenar kini dimiliki oleh `db.MIGRASI[2]` -- satu sumber
    kebenaran. Fungsi ini kekal untuk keserasian dan sebagai jaring
    keselamatan jika DB dibuka tanpa melalui `db.init()`.
    """
    from db import migrasi
    migrasi(conn)


def simpan(conn: sqlite3.Connection, slug: str,
           pasangan: list[tuple[int, str]]) -> int:
    if not pasangan:
        return 0
    cur = conn.executemany(
        "INSERT OR REPLACE INTO terjemahan_eng(collection, hadis_id, english) "
        "VALUES (?,?,?)",
        [(slug, hid, teks) for hid, teks in pasangan])
    conn.commit()
    return cur.rowcount or 0


def ambil(conn: sqlite3.Connection, slug: str, hadis_id: int) -> str:
    try:
        r = conn.execute(
            "SELECT english FROM terjemahan_eng WHERE collection=? AND hadis_id=?",
            (slug, hadis_id)).fetchone()
    except sqlite3.Error:
        return ""
    return (r[0] if r else "") or ""


def bina_bab(fail_ara: str) -> dict[int, tuple[int, str]]:
    """Peta {hadithnumber: (book, nama_bab)} daripada metadata CDN.

    `metadata.sections` CDN ialah {nombor buku: nama bab Inggeris};
    `reference.book` pada setiap hadis menunjuk ke bab itu. Hadis yang
    tiada nombor buku (book=0) tidak direkod.
    """
    d = muat_json(fail_ara)
    sections = (d.get("metadata") or {}).get("sections") or {}
    out: dict[int, tuple[int, str]] = {}
    for h in d.get("hadiths", []):
        no = h.get("hadithnumber")
        if not isinstance(no, int):
            continue
        book = (h.get("reference") or {}).get("book")
        if not book:
            continue
        out[no] = (int(book), sections.get(str(book), ""))
    return out


def simpan_bab(conn: sqlite3.Connection, slug: str,
               pasangan: list[tuple[int, int, str]]) -> int:
    """Simpan (hadis_id, book, nama_bab). Pulangkan bilangan baris."""
    if not pasangan:
        return 0
    cur = conn.executemany(
        "INSERT OR REPLACE INTO bab(collection, hadis_id, book, nama_bab) "
        "VALUES (?,?,?,?)",
        [(slug, hid, book, nama) for hid, book, nama in pasangan])
    conn.commit()
    return cur.rowcount or 0


def bina_darjat(fail_ara: str) -> dict[int, list[tuple[str, str]]]:
    """Peta {hadithnumber: [(nama_ulama, darjat), ...]} daripada CDN.

    `grades` CDN ialah senarai objek `{"name": ulama, "grade": darjat}`
    -- penilaian ulama MODEN, bukan hukm. Semua ulama dirakam apa adanya
    (Sesi 14: papar mentah, tiada tafsiran, tiada susunan keutamaan).
    """
    d = muat_json(fail_ara)
    out: dict[int, list[tuple[str, str]]] = {}
    for h in d.get("hadiths", []):
        no = h.get("hadithnumber")
        g = h.get("grades")
        if not isinstance(no, int) or not g:
            continue
        out[no] = [(str(x.get("name", "")).strip(), str(x.get("grade", "")).strip())
                   for x in g if isinstance(x, dict)]
    return out


def simpan_darjat(conn: sqlite3.Connection, slug: str,
                  pasangan: list[tuple[int, str, str]]) -> int:
    """Simpan (hadis_id, nama_ulama, darjat). Pulangkan bilangan baris."""
    if not pasangan:
        return 0
    cur = conn.executemany(
        "INSERT OR REPLACE INTO darjat(collection, hadis_id, nama_ulama, darjat) "
        "VALUES (?,?,?,?)",
        [(slug, hid, nama, dar) for hid, nama, dar in pasangan])
    conn.commit()
    return cur.rowcount or 0
