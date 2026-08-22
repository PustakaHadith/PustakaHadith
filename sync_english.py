"""Tarik terjemahan Inggeris dan padankan kepada hadis dalam hadis.db.

    python sync_english.py            # semua kitab yang ada sumber
    python sync_english.py bukhari    # satu kitab
    python sync_english.py --semak    # status sahaja, tiada muat turun

TIADA KUNCI API DIPERLUKAN. Sumber ialah fail JSON statik di CDN
jsDelivr, bukan API berkuota.

BAGAIMANA IA BERFUNGSI
----------------------
hadis.my tidak menyediakan Inggeris, dan penomborannya berbeza daripada
sumber luar. Jadi padanan dibuat melalui TEKS ARAB:

    hadis.db (arab)  --padan teks-->  ara-*  --nombor sama-->  eng-*

Jalankan `sync.py` DAHULU -- skrip ini memerlukan teks Arab dalam DB.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

try:
    from VERSI import VERSI
except Exception:            # fail lama tanpa VERSI.py
    VERSI = "LAMA-tidak-diketahui"

from config import DB_PATH                                     # noqa: E402
from core.eng_source import (                                  # noqa: E402
    JACCARD_MIN, PETA_KITAB, TIADA_SUMBER, _bina_indeks_kata, ambil, bina_bab,
    bina_darjat, bina_eng, bina_indeks_ind, bina_indeks_ind_kata, bina_indeks,
    muat_json, padan, pasang_skema, simpan, simpan_bab, simpan_darjat,
    url_edisi,
)
from db import init                                            # noqa: E402

CACHE = os.path.join(BASE, ".cache_eng")


def muat_turun(kod: str) -> str:
    """Muat turun edisi jika belum ada dalam cache. Pulangkan laluan fail."""
    os.makedirs(CACHE, exist_ok=True)
    laluan = os.path.join(CACHE, f"{kod}.json")
    if os.path.exists(laluan) and os.path.getsize(laluan) > 5000:
        return laluan

    url = url_edisi(kod)
    print(f"    muat turun {kod} ...", end="", flush=True)
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            data = r.read()
    except Exception as e:
        print(f" GAGAL ({e})")
        raise
    with open(laluan, "wb") as f:
        f.write(data)
    print(f" {len(data)/1048576:.1f} MB")
    return laluan


def sync_kitab(conn: sqlite3.Connection, slug: str) -> tuple[int, int, int]:
    """Pulangkan (dipadan, tiada_eng, gagal_padan)."""
    fz = PETA_KITAB.get(slug)
    if not fz:
        print(f"  {slug:12} tiada sumber Inggeris - dilangkau")
        return 0, 0, 0

    baris = conn.execute(
        "SELECT hadis_id, arab, COALESCE(indonesia,'') FROM hadis "
        "WHERE collection=? AND arab<>''", (slug,)).fetchall()
    if not baris:
        print(f"  {slug:12} tiada teks Arab dalam DB - jalankan sync.py dahulu")
        return 0, 0, 0

    try:
        # ara-*1 = teks sama seperti ara-* tetapi tanpa tashkeel penuh;
        # disahkan identik selepas normalisasi, dan failnya lebih kecil.
        f_ara = muat_turun(f"ara-{fz}1")
        f_eng = muat_turun(f"eng-{fz}")
    except Exception:
        return 0, 0, 0

    # Lapisan PERTAMA: teks Indonesia. Audit saksi bebas mendapati
    # hadis.my dan CDN berkongsi terjemahan Indonesia yang sama
    # (pertindihan purata 1.00), jadi ia kunci yang paling tepat.
    # Kegagalan muat turun tidak fatal -- lapisan Arab mengambil alih.
    try:
        f_ind = muat_turun(f"ind-{fz}")
        indeks_ind = bina_indeks_ind(f_ind)
        teks_ind = {h.get("hadithnumber"): (h.get("text") or "")
                    for h in muat_json(f_ind).get("hadiths", [])
                    if isinstance(h.get("hadithnumber"), int)}
        indeks_ind_kata = bina_indeks_ind_kata(teks_ind)
    except Exception:
        indeks_ind, teks_ind, indeks_ind_kata = {}, {}, {}

    penuh, awalan = bina_indeks(f_ara)
    eng = bina_eng(f_eng)
    # Nama bab + nombor buku CDN (dari metadata.sections CDN), direkod
    # serentak dengan terjemahan supaya UI boleh papar bab hadis.
    bab = bina_bab(f_ara)
    # Penilaian ulama moden (metadata CDN), direkod apa adanya.
    darjat = bina_darjat(f_ara)
    # Lapisan ke-3: padanan pertindihan kata. Menyelamatkan hadis yang
    # teksnya berbeza sedikit antara hadis.my dan sumber CDN.
    teks_ara = {h.get("hadithnumber"): h.get("text", "")
                for h in muat_json(f_ara).get("hadiths", [])
                if isinstance(h.get("hadithnumber"), int)}
    indeks_kata = _bina_indeks_kata(penuh, teks_ara)

    pasangan: list[tuple[int, str]] = []
    pasangan_bab: list[tuple[int, int, str]] = []
    pasangan_darjat: list[tuple[int, str, str]] = []
    kaedah_kira: dict[str, int] = {}
    tiada_eng = gagal = 0
    for hid, arab, ind in baris:
        no, kaedah = padan(arab or "", penuh, awalan, indeks_kata,
                           teks_sumber=teks_ara,
                           ind_hadis_my=ind, indeks_ind=indeks_ind,
                           indeks_ind_kata=indeks_ind_kata,
                           teks_ind=teks_ind)
        kaedah_kira[kaedah] = kaedah_kira.get(kaedah, 0) + 1
        if no is None:
            gagal += 1
            continue
        if no in bab:
            book, nama = bab[no]
            pasangan_bab.append((hid, book, nama))
        for nama_u, dar in darjat.get(no, []):
            pasangan_darjat.append((hid, nama_u, dar))
        teks = eng.get(no)
        if not teks:
            tiada_eng += 1
            continue
        pasangan.append((hid, teks))

    # BUANG dahulu, jangan hanya REPLACE.
    #
    # `simpan()` guna INSERT OR REPLACE: ia menimpa baris yang dipadan
    # semula, tetapi baris yang DAHULU dipadan dan kini ditolak (kerana
    # ambang Jaccard diperketat) akan KEKAL dalam DB dengan terjemahan
    # yang salah. Menjalankan semula sync tidak akan membersihkannya.
    # Padam per-kitab dahulu supaya keadaan akhir sentiasa mencerminkan
    # kod semasa. Begitu juga jadual bab dan darjat.
    try:
        conn.execute("DELETE FROM terjemahan_eng WHERE collection=?", (slug,))
        conn.execute("DELETE FROM bab WHERE collection=?", (slug,))
        conn.execute("DELETE FROM darjat WHERE collection=?", (slug,))
        conn.commit()
    except sqlite3.Error:
        pass

    simpan(conn, slug, pasangan)
    simpan_bab(conn, slug, pasangan_bab)
    simpan_darjat(conn, slug, pasangan_darjat)
    n = len(baris)
    pct = len(pasangan) * 100 // n if n else 0
    rinci = " ".join(f"{k}={v}" for k, v in sorted(kaedah_kira.items()))
    print(f"  {slug:12} {pct:3}%  {len(pasangan):,}/{n:,}"
          f"   tiada_eng={tiada_eng}  gagal={gagal}")
    print(f"  {'':12} kaedah: {rinci}")
    return len(pasangan), tiada_eng, gagal


def bina_peta_sunnah(conn: sqlite3.Connection,
                     sasaran: list[str]) -> int:
    """Bina sunnah_map/{slug}.json -- peta {hadis_id: {book, hadith}}.

    Pautan "Baca penuh" (sunnah.com) dalam kongsi WhatsApp dibina dengan
    format `sunnah.com/{slug}/{buku}/{hadith}` (rujukan DALAM-BUKU CDN).
    Format ini dipilih selepas audit (Sesi 36): nombor GLOBAL CDN
    (`hadithnumber`) TIDAK sepadan dengan URL sunnah.com untuk beberapa
    kitab (cth. Muslim #565 = Kitab Penyucian dalam CDN, tetapi
    sunnah.com:565 = hadis bawang putih Kitab Masjid), manakala rujukan
    dalam-buku `reference` CDN memang sistem sunnah.com sendiri
    ("In-book reference") dan padan dengan URL `/{buku}/{hadith}`.

    Penomboran hadis.my (hadis.db) berbeza daripada sumber luar, jadi
    padanan dibuat melalui teks dengan jentera yang sama seperti
    `sync_kitab` (lapisan Indonesia dahulu, kemudian Arab).

    Ahmad/darimi tiada sumber sunnah.com -- tiada fail dijana.
    """
    import json
    out = os.path.join(BASE, "sunnah_map")
    jumlah = 0
    for slug in sasaran:
        fz = PETA_KITAB.get(slug)
        if not fz:
            print(f"  {slug:12} tiada sumber sunnah.com -- dilangkau")
            continue
        f_ara = os.path.join(CACHE, f"ara-{fz}1.json")
        if not os.path.exists(f_ara):
            print(f"  {slug:12} cache {os.path.basename(f_ara)} tiada -- "
                  "jalankan sync_english.py dahulu")
            continue

        penuh, awalan = bina_indeks(f_ara)
        teks_ara = {h.get("hadithnumber"): h.get("text", "")
                    for h in muat_json(f_ara).get("hadiths", [])
                    if isinstance(h.get("hadithnumber"), int)}
        indeks_kata = _bina_indeks_kata(penuh, teks_ara)
        # Rujukan dalam-buku CDN {hadithnumber: (book, hadith)} -- inilah
        # sistem sunnah.com sendiri ("In-book reference").
        rujukan: dict[int, tuple[int, int]] = {}
        for h in muat_json(f_ara).get("hadiths", []):
            no = h.get("hadithnumber")
            ref = h.get("reference") or {}
            if (isinstance(no, int) and ref.get("book") and ref.get("hadith")):
                rujukan[no] = (int(ref["book"]), int(ref["hadith"]))
        indeks_ind: dict[str, int] = {}
        indeks_ind_kata: dict[str, set[int]] = {}
        teks_ind: dict[int, str] = {}
        f_ind = os.path.join(CACHE, f"ind-{fz}.json")
        if os.path.exists(f_ind):
            indeks_ind = bina_indeks_ind(f_ind)
            teks_ind = {h.get("hadithnumber"): (h.get("text") or "")
                        for h in muat_json(f_ind).get("hadiths", [])
                        if isinstance(h.get("hadithnumber"), int)}
            indeks_ind_kata = bina_indeks_ind_kata(teks_ind)

        baris = conn.execute(
            "SELECT hadis_id, arab, COALESCE(indonesia,'') FROM hadis "
            "WHERE collection=? AND arab<>''", (slug,)).fetchall()
        peta: dict[str, dict] = {}
        kaedah: dict[str, int] = {}
        for hid, arab, ind in baris:
            no, k = padan(arab or "", penuh, awalan, indeks_kata,
                          teks_sumber=teks_ara,
                          ind_hadis_my=ind, indeks_ind=indeks_ind,
                          indeks_ind_kata=indeks_ind_kata, teks_ind=teks_ind)
            kaedah[k] = kaedah.get(k, 0) + 1
            if no is not None and no in rujukan:
                book, hadith = rujukan[no]
                peta[str(hid)] = {"book": book, "hadith": hadith}

        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, f"{slug}.json"), "w",
                  encoding="utf-8") as f:
            json.dump(peta, f, ensure_ascii=False)
        n = len(peta)
        jumlah += n
        print(f"  {slug:12} {n}/{len(baris)} dipadan "
              f"({100*n/max(1, len(baris)):.1f}%) "
              f"kaedah={dict(sorted(kaedah.items()))}")
    return jumlah


def semak(conn: sqlite3.Connection) -> None:
    try:
        rows = dict(conn.execute(
            "SELECT collection, COUNT(*) FROM terjemahan_eng GROUP BY collection"))
    except sqlite3.Error:
        rows = {}
    arab = dict(conn.execute(
        "SELECT collection, COUNT(*) FROM hadis GROUP BY collection"))
    try:
        bab = dict(conn.execute(
            "SELECT collection, COUNT(*) FROM bab GROUP BY collection"))
    except sqlite3.Error:
        bab = {}
    try:
        darjat = dict(conn.execute(
            "SELECT collection, COUNT(*) FROM darjat GROUP BY collection"))
    except sqlite3.Error:
        darjat = {}

    print(f"\n  {'kitab':14}{'hadis':>9}{'english':>10}{'liputan':>10}"
          f"{'bab':>9}{'darjat':>9}")
    print("  " + "-" * 61)
    for slug in list(PETA_KITAB) + list(TIADA_SUMBER):
        a = arab.get(slug, 0)
        e = rows.get(slug, 0)
        if slug in TIADA_SUMBER:
            print(f"  {slug:14}{a:>9,}{'-':>10}{'tiada sumber':>10}{'-':>9}{'-':>9}")
        else:
            pct = f"{e*100//a}%" if a else "-"
            b = bab.get(slug, 0)
            dj = darjat.get(slug, 0)
            print(f"  {slug:14}{a:>9,}{e:>10,}{pct:>10}{b:>9,}{dj:>9,}")
    print("  " + "-" * 61)
    print(f"  {'JUMLAH':14}{sum(arab.values()):>9,}{sum(rows.values()):>10,}"
          f"{'':>10}{sum(bab.values()):>9,}{sum(darjat.values()):>9,}\n")


def main() -> int:
    arg = sys.argv[1:]
    mahu = [a for a in arg if not a.startswith("--")]

    conn = init(DB_PATH)
    pasang_skema(conn)

    if "--semak" in arg:
        semak(conn)
        return 0

    jum = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    if jum == 0:
        print("\n  hadis.db kosong. Jalankan dahulu:\n      python sync.py\n")
        return 1

    sasaran = mahu or list(PETA_KITAB)
    tak_kenal = [s for s in sasaran if s not in PETA_KITAB and s not in TIADA_SUMBER]
    if tak_kenal:
        print(f"\n  Slug tidak dikenali: {', '.join(tak_kenal)}")
        print(f"  Pilihan: {', '.join(PETA_KITAB)}\n")
        return 1

    if "--peta-sunnah" in arg:
        print(f"\n  PustakaHadith v{VERSI}")
        print("  Bina peta sunnah.com -> hadis.db (pautan 'Baca penuh')\n")
        jumlah = bina_peta_sunnah(conn, sasaran)
        print(f"\n  JUMLAH dipadan: {jumlah:,}\n")
        return 0

    print(f"\n  PustakaHadith v{VERSI}")
    print(f"  Padan terjemahan Inggeris untuk {len(sasaran)} kitab")
    print("  Tiada kunci API diperlukan (fail statik CDN)")
    print(f"  Jaccard dua hala: {JACCARD_MIN}  "
          f"(baris lama setiap kitab DIPADAM dahulu)\n")

    t_p = t_n = t_g = 0
    for slug in sasaran:
        p, n, g = sync_kitab(conn, slug)
        t_p += p
        t_n += n
        t_g += g

    print(f"\n  Selesai.")
    print(f"  Terjemahan disimpan : {t_p:,}")
    if t_n:
        print(f"  Sumber tiada teks   : {t_n:,}")
    if t_g:
        print(f"  Gagal dipadan       : {t_g:,}")
    print(f"\n  Cache: {CACHE}")
    print("  (boleh dipadam selepas siap - ~40 MB)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
