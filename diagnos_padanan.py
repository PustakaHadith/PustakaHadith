"""Diagnosis kegagalan padanan teks Arab hadis.db <-> sumber CDN.

    python diagnos_padanan.py            # bukhari
    python diagnos_padanan.py muslim

Gunakan bila `sync_english.py` melaporkan banyak `gagal`. Skrip ini
TIDAK mengubah apa-apa -- ia hanya melaporkan MENGAPA padanan gagal,
supaya normalisasi boleh dilaraskan pada punca sebenar.

Laporan boleh disalin dan dihantar; ia tidak mengandungi kunci API.
"""

from __future__ import annotations

import os
import sys
import unicodedata
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from config import DB_PATH                                     # noqa: E402
from core.eng_source import (                                  # noqa: E402
    JACCARD_MIN, PETA_KITAB, _bina_indeks_kata, bina_indeks,
    kunci_sandaran, muat_json, normalisasi, padan,
)
from db import connect                                         # noqa: E402

CACHE = os.path.join(BASE, ".cache_eng")


def aksara_asing(teks: str, had: int = 12) -> list[tuple[str, int]]:
    """Aksara yang BUKAN huruf Arab asas atau ruang."""
    c = Counter(ch for ch in teks
                if not ("\u0621" <= ch <= "\u064A" or ch == " "))
    return c.most_common(had)


def main() -> int:
    slug = sys.argv[1] if len(sys.argv) > 1 else "bukhari"
    fz = PETA_KITAB.get(slug)
    if not fz:
        print(f"\n  '{slug}' tiada sumber Inggeris.")
        print(f"  Pilihan: {', '.join(PETA_KITAB)}\n")
        return 1

    f_ara = os.path.join(CACHE, f"ara-{fz}1.json")
    if not os.path.exists(f_ara):
        print(f"\n  Cache tiada: {f_ara}")
        print("  Jalankan dahulu: python sync_english.py\n")
        return 1

    conn = connect(DB_PATH)
    baris = conn.execute(
        "SELECT hadis_id, arab FROM hadis WHERE collection=? AND arab<>'' "
        "ORDER BY hadis_id LIMIT 500", (slug,)).fetchall()
    if not baris:
        print(f"\n  Tiada hadis '{slug}' dalam DB. Jalankan sync.py dahulu.\n")
        return 1

    penuh, awalan = bina_indeks(f_ara)
    teks_ara = {h.get("hadithnumber"): h.get("text", "")
                for h in muat_json(f_ara).get("hadiths", [])
                if isinstance(h.get("hadithnumber"), int)}
    ik = _bina_indeks_kata(penuh, teks_ara)

    print("\n" + "=" * 62)
    print(f"  DIAGNOSIS PADANAN — {slug}")
    print("=" * 62)
    # Cap versi: tanpa ini, menjalankan salinan LAMA menghasilkan
    # laporan yang kelihatan sah dan tiada cara membezakannya.
    print(f"\n  Jaccard dua hala : {JACCARD_MIN}")
    print(f"\n  Sampel DB      : {len(baris)} hadis")
    print(f"  Indeks sumber  : {len(penuh):,} penuh · {len(awalan):,} awalan")
    print(f"  Kata jarang    : {len(ik):,}")

    kaedah = Counter()
    gagal = []
    for hid, arab in baris:
        no, cara = padan(arab, penuh, awalan, ik, teks_sumber=teks_ara)
        kaedah[cara] += 1
        if cara == "gagal" and len(gagal) < 3:
            gagal.append((hid, arab))

    print("\n  Kaedah padanan:")
    for k in ("penuh", "awalan", "kata", "gagal"):
        v = kaedah.get(k, 0)
        print(f"    {k:8} {v:>5}  ({v/len(baris)*100:5.1f}%)")

    berjaya = len(baris) - kaedah.get("gagal", 0)
    print(f"\n  JUMLAH BERJAYA : {berjaya}/{len(baris)} "
          f"= {berjaya/len(baris)*100:.1f}%")

    # ---- audit KUALITI lapisan `kata` -------------------------------
    # Kiraan sahaja tidak memberitahu sama ada padanan `kata` itu
    # rapat atau nyaris-nyaris lulus ambang. Padanan pada Jaccard 0.99
    # praktikalnya pasti; pada 0.90 ia di birai. Taburan ini
    # menunjukkan berapa banyak yang bergantung pada birai itu.
    jacs = []
    for hid, arab in baris:
        no, cara = padan(arab, penuh, awalan, ik, teks_sumber=teks_ara)
        if cara != "kata" or no is None:
            continue
        a = set(normalisasi(arab).split())
        b = set(normalisasi(teks_ara.get(no, "")).split())
        if a or b:
            jacs.append(len(a & b) / max(1, len(a | b)))
    if jacs:
        print("\n  Kualiti padanan `kata` (Jaccard sebenar):")
        bin_ = [("1.00  identik    ", lambda j: j >= 0.999),
                ("0.97-1.00 sgt rapat", lambda j: 0.97 <= j < 0.999),
                ("0.94-0.97 rapat   ", lambda j: 0.94 <= j < 0.97),
                ("0.90-0.94 BIRAI   ", lambda j: j < 0.94)]
        for nama, uji in bin_:
            v = sum(1 for j in jacs if uji(j))
            bar = "#" * int(v / max(1, len(jacs)) * 30)
            print(f"    {nama} {v:>4}  ({v/len(jacs)*100:5.1f}%) {bar}")
        birai = sum(1 for j in jacs if j < 0.94)
        print(f"\n    Purata Jaccard: {sum(jacs)/len(jacs):.3f}")
        # Nota: "birai" TIDAK bermakna salah. Diuji dengan teks yang
        # sengaja diusik 12%: 60% padanan jatuh di bawah 0.94 namun
        # ketepatan kekal 100%. Perbezaan tanda baca dan riwayat
        # dipendekkan memang menghasilkan Jaccard 0.90-0.94 secara sah.
        # Bilangan ini untuk PEMANTAUAN, bukan penggera.
        print(f"    {birai} padanan dalam julat 0.90-0.94.")
        print("    (julat ini normal: beza tanda baca / riwayat "
              "dipendekkan)")

    # ---- bandingkan satu hadis yang PADAN, untuk lihat beza halus ----
    print("\n" + "-" * 62)
    print("  PERBANDINGAN AKSARA (hadis pertama dalam DB)")
    print("-" * 62)
    hid, arab = baris[0]
    print(f"\n  hadis.db #{hid}")
    print(f"    mentah : {arab[:70]}")
    print(f"    normal : {normalisasi(arab)[:70]}")
    print(f"    asing  : {aksara_asing(arab)}")

    src = teks_ara.get(hid)
    if src:
        print(f"\n  sumber CDN #{hid}")
        print(f"    mentah : {src[:70]}")
        print(f"    normal : {normalisasi(src)[:70]}")
        print(f"    asing  : {aksara_asing(src)}")
        a, b = normalisasi(arab), normalisasi(src)
        print(f"\n    normalisasi sama? {a == b}")
        if a != b:
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print(f"    beza pertama pada aksara {i}:")
                    print(f"      DB  U+{ord(x):04X} {unicodedata.name(x,'?')}")
                    print(f"      CDN U+{ord(y):04X} {unicodedata.name(y,'?')}")
                    print(f"      konteks DB : ...{a[max(0,i-25):i+25]}...")
                    print(f"      konteks CDN: ...{b[max(0,i-25):i+25]}...")
                    break
            else:
                print(f"    panjang berbeza: DB={len(a)} CDN={len(b)}")

    # ---- contoh yang gagal ----
    if gagal:
        print("\n" + "-" * 62)
        print("  CONTOH GAGAL PADAN")
        print("-" * 62)
        for hid, arab in gagal:
            n = normalisasi(arab)
            print(f"\n  #{hid}  ({len(n)} aksara selepas normalisasi)")
            print(f"    {n[:100]}")
            print(f"    asing: {aksara_asing(arab, 8)}")
            ada_sumber = hid in teks_ara
            print(f"    nombor {hid} wujud dlm sumber? {ada_sumber}")
            if ada_sumber:
                print(f"    sumber: {normalisasi(teks_ara[hid])[:100]}")

    print("\n" + "=" * 62)
    if kaedah.get("gagal", 0) > len(baris) * 0.1:
        print("  Liputan rendah. Salin laporan ini untuk analisis lanjut.")
    else:
        print("  Liputan baik.")
    print("=" * 62 + "\n")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
