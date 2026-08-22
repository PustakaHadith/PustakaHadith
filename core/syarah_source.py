"""Sumber syarah (huraian klasik) — OpenITI.

FASA 4 LAPISAN B
----------------
Lapisan A (Irsyad al-Hadith, Bahasa Melayu) ialah sumber utama tetapi
belum tersedia. Lapisan ini menyediakan syarah Arab klasik sebagai
rujukan PILIHAN untuk pengguna yang mampu membaca Arab.

UI mesti memaparkannya dalam bahagian tertutup (`Collapsible`), BUKAN
sebagai huraian utama. Sebabnya diukur, bukan diandaikan:

    tashkeel 0.00%   (diukur pada 309,912 huruf) -- Arab gundul
    median 1,971 aksara per seksyen              -- terlalu panjang
    Bukhari sahaja                               -- 67.1% liputan

PENOMBORAN HANYUT — PADANAN IKUT ID TIDAK SELAMAT
-------------------------------------------------
Penanda `# N` BUKAN nombor hadis Bukhari standard. Ia kiraan hadis
berjujukan dalam edisi Ibn Hajar: bermula sejajar (kedua-duanya mula
pada 1) lalu menyimpang apabila edisi berbeza pendapat tentang apa
yang dikira hadis berasingan.

Anjakan terbaik per julat, diukur dengan kata jarang matn:

       1-200   +0      (sejajar)
     600-800  -32
    2000-3500 -120
    5000-7000 -320

Dakwaan lama "disahkan 5/5" DIBATALKAN: ketiga-tiga hadis yang diuji
(#1 #2 #8) berada dalam julat 1-200 yang memang sejajar. Sampel dari
satu hujung julat memberi jawapan yang salah.

Padanan ikut TEKS juga gagal: 300 seksyen diuji, hanya 2 memberi nombor
yang sama, delta median 174 tanpa corak. Syarah memetik potongan sanad
(`قوله حدثنا الحميدي`), bukan matn.

`nisbah_keyakinan()` mengesan hanyut ini dan membatalkan sync.

REPO DIBUNDARKAN KE ATAS
------------------------
Ibn Hajar wafat 852H tetapi failnya berada dalam repo `0875AH`, bukan
`0850AH`. Percubaan awal mendapat 404 kerana andaian yang salah.

LESEN
-----
OpenITI: CC BY-NC-SA. Atribusi WAJIB dipaparkan; tiada penggunaan
komersial.
"""

from __future__ import annotations

import re
import sqlite3

# ---------------------------------------------------------------- katalog

KITAB_SYARAH: dict[str, dict] = {
    "fathbari": {
        "nama": "Fath al-Bari",
        "nama_ar": "فتح الباري",
        "pengarang": "Ibn Hajar al-'Asqalani (w. 852H)",
        "atas": "bukhari",
        "repo": "0875AH",
        "laluan": ("data/0852IbnHajarCasqalani/"
                   "0852IbnHajarCasqalani.FathBari/"
                   "0852IbnHajarCasqalani.FathBari.JK000166-ara1"),
        "format": "hash_n",          # penanda '# N'
        "saiz_mb": 30.5,
    },
}

RAW = "https://raw.githubusercontent.com/OpenITI/{repo}/master/{laluan}"

LESEN = ("OpenITI · CC BY-NC-SA · bukan untuk kegunaan komersial")


def url_kitab(kunci: str) -> str:
    k = KITAB_SYARAH[kunci]
    return RAW.format(repo=k["repo"], laluan=k["laluan"])


# ---------------------------------------------------------------- parser

_PAGE = re.compile(r"PageV\d+P\d+")
# Penanda muka surat manuskrip OpenITI: `ms00022`. Berbeza daripada
# `PageV..P..` ia menyelit DI TENGAH ayat Arab (10,952 kali dalam Fath
# al-Bari), memecahkan perkataan bersebelahan apabila teks dinormalisasi
# dan mencemarkan paparan pengguna dengan aksara Latin.
_MS = re.compile(r"\bms\d{3,}\b")
_HASH_N = re.compile(r"^# (\d+)\s", re.M)
_TASHKEEL = re.compile(r"[\u064B-\u0652\u0670\u0640]")


def bersih(teks: str) -> str:
    """Buang penanda muka surat dan sambungan baris OpenITI.

    `~~` menandakan sambungan baris fizikal, bukan perenggan baharu --
    menggantinya dengan ruang mengekalkan ayat utuh. Membuang SELURUH
    baris yang mengandungi `PageV..P..` akan memadamkan teks Arab
    (401 baris hilang dalam parser lama pengguna); jadi buang penanda
    itu sahaja.
    """
    t = _PAGE.sub(" ", teks or "")
    t = _MS.sub(" ", t)
    t = t.replace("~~", " ")
    return re.sub(r"\s+", " ", t).strip()


def buang_header(teks: str) -> str:
    tanda = "#META#Header#End#"
    return teks.split(tanda, 1)[1] if tanda in teks else teks


def hurai_hash_n(teks: str) -> dict[int, str]:
    """Pecahkan format `# N` kepada {nombor_hadis: syarah}.

    Nombor pertama menang jika berulang -- seksyen kemudian dengan
    nombor sama biasanya rujukan silang, bukan syarah utama.
    """
    badan = buang_header(teks)
    bahagian = re.split(_HASH_N, badan)
    keluar: dict[int, str] = {}
    # bahagian = [sebelum, no1, teks1, no2, teks2, ...]
    for i in range(1, len(bahagian) - 1, 2):
        try:
            no = int(bahagian[i])
        except ValueError:
            continue
        if no in keluar:
            continue
        isi = bersih(bahagian[i + 1])
        if isi:
            keluar[no] = isi
    return keluar


def hurai(teks: str, kunci: str) -> dict[int, str]:
    fmt = KITAB_SYARAH[kunci]["format"]
    if fmt == "hash_n":
        return hurai_hash_n(teks)
    raise ValueError(f"format tidak disokong: {fmt}")


# ---------------------------------------------------------------- sahkan

def _norm(teks: str) -> str:
    t = _TASHKEEL.sub("", teks or "")
    t = re.sub(r"[أإآٱ]", "ا", t)
    t = t.replace("ى", "ي").replace("ؤ", "و").replace("ئ", "ي").replace("ة", "ه")
    return re.sub(r"\s+", " ", t).strip()


def sahkan_padanan(seksyen: dict[int, str], conn: sqlite3.Connection,
                   slug: str, sampel: int = 200) -> tuple[int, int]:
    """Sahkan penomboran sejajar dengan hadis sebenar dalam DB.

    Pulangkan (padan, disemak) untuk paparan. Untuk keputusan
    TERIMA/TOLAK gunakan `nisbah_keyakinan()` -- lihat nota di sana.

    Sampel diambil MERENTAS seluruh julat, bukan N hadis pertama.
    Diukur pada Fath al-Bari: 80 hadis pertama memberi 76%, sedangkan
    kadar sebenar merentas kitab ialah 10-29%. Syarah paling terperinci
    pada awal kitab, jadi sampel awal memberi gambaran yang PALSU.
    """
    p, n, _ = _skor_anjakan(seksyen, conn, slug, 0, sampel)
    return p, n


def _skor_anjakan(seksyen: dict[int, str], conn: sqlite3.Connection,
                  slug: str, anjakan: int,
                  sampel: int) -> tuple[int, int, int]:
    """Kadar padanan bila syarah digeser sebanyak `anjakan`.

    Anjakan bukan-sifar ialah KAWALAN NEGATIF: ia sepatutnya memberi
    kadar yang jauh lebih rendah. Jika tidak, metrik itu tidak
    membezakan apa-apa dan tidak boleh dipercayai.
    """
    baris = conn.execute(
        "SELECT hadis_id, arab FROM hadis WHERE collection=? AND arab<>'' "
        "ORDER BY hadis_id", (slug,)).fetchall()
    if not baris:
        return 0, 0, 0
    # Ambil merentas SELURUH julat, bukan N pertama.
    langkah = max(1, len(baris) // (sampel * 3))
    baris = baris[::langkah]

    padan = disemak = 0
    for hid, arab in baris:
        if disemak >= sampel:
            break
        isi = seksyen.get(hid + anjakan)
        if not isi:
            continue
        kata = [w for w in _norm(arab).split()[:30]
                if len(w) > 3 and w not in _LAZIM]
        if len(kata) < 2:
            continue
        disemak += 1
        n = _norm(isi)[:4000]
        if sum(1 for w in kata if w in n) >= max(2, len(kata) // 4):
            padan += 1
    return padan, disemak, len(baris)


# Kata yang muncul dalam hampir setiap sanad. Ia memadan walaupun
# nombor SALAH, jadi tidak membezakan apa-apa.
_LAZIM = {"حدثنا", "حدثني", "اخبرنا", "قال", "قالت", "الله", "رسول",
          "النبي", "عليه", "وسلم", "صلي", "عنه", "عنها", "بن", "ابن",
          "عن", "ابي", "ابو"}

# Berapa kali ganda anjakan-sifar mesti mengatasi kawalan negatif.
NISBAH_MIN = 1.8


def diagnos_hanyut(seksyen: dict[int, str], conn: sqlite3.Connection,
                   slug: str) -> list[tuple[int, int, int, float]]:
    """Kesan sama ada penomboran HANYUT merentas kitab.

    Pulangkan [(lo, hi, anjakan_terbaik, skor)] per julat.

    Ini soalan yang paling penting bagi syarah. Penomboran boleh
    sejajar sempurna pada permulaan kitab dan hanyut secara progresif
    selepas itu -- tepat apa yang berlaku pada Fath al-Bari:

        1-200      anjakan  +0    (sejajar)
        200-400    anjakan  -4
        400-600    anjakan -12
        600-800    anjakan -32
        2000-3500  anjakan -120
        5000-7000  anjakan -320

    Pengawal yang hanya menyemak N hadis PERTAMA akan melaporkan
    "76% -- selamat" dan menyimpan syarah yang salah untuk 95%
    daripada kitab.
    """
    baris = conn.execute(
        "SELECT hadis_id, arab FROM hadis WHERE collection=? AND arab<>'' "
        "ORDER BY hadis_id", (slug,)).fetchall()
    if not baris:
        return []
    teks = {hid: arab for hid, arab in baris}
    ids = sorted(teks)
    hasil = []
    n = len(ids)
    for i in range(0, 6):
        lo = ids[min(n - 1, i * n // 6)]
        hi = ids[min(n - 1, (i + 1) * n // 6 - 1)]
        skor0 = _skor_julat(teks, seksyen, lo, hi, 0)
        terbaik, skor_terbaik = 0, skor0
        for off in range(-400, 401, 20):
            if off == 0:
                continue
            v = _skor_julat(teks, seksyen, lo, hi, off)
            # Hanya isytihar hanyut jika anjakan lain MENGATASI DENGAN
            # JELAS. Bunyi rawak boleh memberi anjakan palsu skor
            # sedikit lebih tinggi; memerlukan 1.5x mengelakkannya.
            if v > skor_terbaik and v > skor0 * 1.5:
                terbaik, skor_terbaik = off, v
        hasil.append((lo, hi, terbaik, skor_terbaik))
    return hasil


def _skor_julat(teks: dict[int, str], seksyen: dict[int, str],
                lo: int, hi: int, anjakan: int, had: int = 120) -> float:
    """Purata pecahan kata JARANG matn yang muncul dalam syarah.

    Kata sanad (`حدثنا`, `قال`, nama perawi biasa) sengaja TIDAK
    digunakan: ia muncul dalam hampir setiap syarah dan memberi skor
    tinggi walaupun nombornya salah. Diukur: metrik berasaskan sanad
    memberi 1.21x bagi penomboran betul dan 1.20x bagi penomboran
    yang digeser 50 -- iaitu tidak membezakan APA-APA.
    """
    # Sampel MERENTAS julat dengan langkah tetap, bukan N pertama.
    # Mengambil N pertama ialah ralat yang sama seperti pengawal lama:
    # syarah paling terperinci pada permulaan kitab, jadi sampel awal
    # memberi skor yang tidak mewakili keseluruhan.
    calon = [h for h in range(lo, hi + 1) if h in teks]
    if not calon:
        return 0.0
    langkah = max(1, len(calon) // (had * 2))
    nilai = []
    for hid in calon[::langkah]:
        isi = seksyen.get(hid + anjakan)
        if not isi:
            continue
        kata = [w for w in set(_norm(teks[hid]).split())
                if len(w) > 4 and w not in _LAZIM]
        if len(kata) < 3:
            continue
        sy = set(_norm(isi).split())
        nilai.append(sum(1 for w in kata if w in sy) / len(kata))
        if len(nilai) >= had:
            break
    return (sum(nilai) / len(nilai)) if nilai else 0.0


def nisbah_keyakinan(seksyen: dict[int, str], conn: sqlite3.Connection,
                     slug: str, sampel: int = 200) -> dict:
    """Pengawal penomboran BERASASKAN PERBANDINGAN + pengesanan hanyut.

    MENGAPA BUKAN AMBANG MUTLAK
    ---------------------------
    Kadar padanan mutlak bergantung pada betapa kerap syarah memetik
    teks hadis -- ciri PENULISAN pengarang, bukan bukti penomboran.

    APA YANG SEBENARNYA DISEMAK
    ---------------------------
    1. Anjakan sifar mesti mengatasi anjakan kawalan (nisbah).
    2. Anjakan terbaik mesti KEKAL sifar merentas seluruh kitab.
       Jika ia beralih dari julat ke julat, penomboran HANYUT dan
       padanan ikut ID tidak selamat walaupun nisbah kelihatan baik.
    """
    # Guna metrik KATA JARANG MATN, bukan kata sanad. Metrik sanad
    # diukur memberi 1.21x bagi penomboran betul dan 1.20x bagi yang
    # digeser 50 -- ia tidak membezakan apa-apa dan pernah menyebabkan
    # sumber yang sah ditolak.
    baris = conn.execute(
        "SELECT hadis_id, arab FROM hadis WHERE collection=? AND arab<>'' "
        "ORDER BY hadis_id", (slug,)).fetchall()
    teks = {hid: arab for hid, arab in baris}
    if not teks:
        return {"padan": 0, "disemak": 0, "kadar": 0.0, "kawalan": 0.0,
                "nisbah": 0.0, "hanyut": [], "stabil": False,
                "lulus": False}
    lo, hi = min(teks), max(teks)
    kadar0 = _skor_julat(teks, seksyen, lo, hi, 0, had=sampel * 3)
    kawalan = [_skor_julat(teks, seksyen, lo, hi, off, had=sampel * 3)
               for off in (-2, -1, 1, 2)]
    purata_kawalan = (sum(kawalan) / len(kawalan)) if kawalan else 0.0
    p0, n0, _ = _skor_anjakan(seksyen, conn, slug, 0, sampel)
    nisbah = (kadar0 / purata_kawalan) if purata_kawalan > 0 else (
        99.0 if kadar0 > 0 else 0.0)

    hanyut = diagnos_hanyut(seksyen, conn, slug)
    anjakan = [a for _, _, a, _ in hanyut]
    # MAJORITI julat mesti sejajar, bukan semua. Julat dengan sedikit
    # syarah menghasilkan bunyi rawak; menuntut 6/6 sempurna menolak
    # sumber yang sah (disahkan dengan kawalan positif tiruan).
    sejajar = sum(1 for a in anjakan if abs(a) <= 20)
    stabil = bool(anjakan) and sejajar >= max(1, int(len(anjakan) * 0.8))

    return {
        "padan": p0, "disemak": n0, "kadar": kadar0,
        "kawalan": purata_kawalan, "nisbah": nisbah,
        "hanyut": hanyut, "stabil": stabil,
        "lulus": bool(n0 >= 30 and nisbah >= NISBAH_MIN and stabil),
    }


# ---------------------------------------------------------------- DB

def simpan(conn: sqlite3.Connection, slug: str, kunci: str,
           seksyen: dict[int, str], had_id: int = 0) -> int:
    """Simpan syarah. `had_id` menapis nombor di luar julat kitab."""
    meta = KITAB_SYARAH[kunci]
    baris = [(slug, no, kunci, meta["pengarang"], teks)
             for no, teks in seksyen.items()
             if no >= 1 and (not had_id or no <= had_id)]
    if not baris:
        return 0
    conn.executemany(
        "INSERT OR REPLACE INTO syarah"
        "(collection, hadis_id, kitab, pengarang, teks) VALUES (?,?,?,?,?)",
        baris)
    conn.commit()
    return len(baris)


def ambil(conn: sqlite3.Connection, slug: str, hadis_id: int) -> list[dict]:
    """Semua syarah untuk satu hadis. Senarai kosong jika tiada."""
    try:
        rows = conn.execute(
            "SELECT kitab, pengarang, teks FROM syarah "
            "WHERE collection=? AND hadis_id=?", (slug, hadis_id)).fetchall()
    except sqlite3.Error:
        return []          # jadual belum dicipta
    keluar = []
    for kitab, pengarang, teks in rows:
        meta = KITAB_SYARAH.get(kitab, {})
        keluar.append({
            "kitab": kitab,
            "nama": meta.get("nama", kitab),
            "nama_ar": meta.get("nama_ar", ""),
            "pengarang": pengarang or meta.get("pengarang", ""),
            "teks": teks,
            "lesen": LESEN,
        })
    return keluar
