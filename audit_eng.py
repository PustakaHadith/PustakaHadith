"""Audit KETEPATAN padanan Inggeris menggunakan bukti BEBAS.

MASALAH YANG DISELESAIKAN
-------------------------
`diagnos_padanan.py` melaporkan berapa banyak hadis DIPADAN. Ia tidak
boleh memberitahu sama ada padanan itu BETUL -- ia menilai padanan
teks Arab dengan membandingkan teks Arab, iaitu berhujah dalam bulatan.

Skrip ini menggunakan saksi ketiga. Sumber CDN menyediakan terjemahan
INDONESIA (`ind-*`) yang berkongsi penomboran dengan `ara-*` dan
`eng-*`. hadis.db juga menyimpan terjemahan Indonesia daripada
hadis.my -- sumber yang SAMA SEKALI berlainan.

    hadis.db (arab)  --padanan kita-->  nombor CDN
    hadis.db (indonesia)  vs  ind-{kitab}[nombor CDN]

Jika padanan betul, dua teks Indonesia daripada dua sumber bebas
sepatutnya serupa. Jika padanan salah, ia bercerita tentang hadis
yang berbeza dan pertindihan katanya runtuh.

Ini mengesan kesilapan yang tidak dapat dilihat oleh padanan Arab,
kerana bukti itu tidak pernah digunakan untuk membuat padanan.

    python audit_eng.py            # bukhari
    python audit_eng.py malik
    python audit_eng.py --semua

Tiada kunci API. Tidak mengubah apa-apa dalam DB.

KETERBATASAN DIKETAHUI (Sesi 10, audit penuh pertama)
-----------------------------------------------------
`ind-*` dan `ara-*` TIDAK sentiasa berkongsi penomboran: hadis tanpa
terjemahan Indonesia ditinggalkan, jadi nombor selepas kekosongan itu
hanyut. Audit pada lapisan Arab (`penuh`/`awalan`/`kata`) membaca
`ind_cdn[no]` dan boleh menandakan hadis yang sebenarnya PADAN dengan
betul sebagai "disyaki". Disahkan 31 Jul: 6 kes sedemikian — semuanya
positif palsu (teks Arab sama, saksi Indonesia tersasar). Pembaikan:
jajarkan `ara-*` dan `ind-*` ikut padanan teks dahulu, bukan nombor.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

try:
    from VERSI import VERSI
except Exception:            # fail lama tanpa VERSI.py
    VERSI = "LAMA-tidak-diketahui"

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from config import DB_PATH                                     # noqa: E402
from core.eng_source import (                                  # noqa: E402
    CDN, JACCARD_MIN, PETA_KITAB, _bina_indeks_kata, bina_indeks,
    muat_json, padan,
)
from db import connect                                         # noqa: E402

CACHE = os.path.join(BASE, ".cache_eng")

# Ambang pertindihan teks Indonesia di bawahnya padanan disyaki.
# Dua terjemahan bebas bagi hadis yang SAMA tetap berbeza perkataan
# (gaya penterjemah), jadi ambang ini sengaja longgar -- ia mencari
# keruntuhan, bukan perbezaan kecil.
SYAK = 0.30

_BUKAN_HURUF = re.compile(r"[^a-z0-9\u00c0-\u024f ]+")
# Kata henti Indonesia/Melayu + istilah yang muncul dalam hampir
# setiap hadis. Tanpa ini, dua hadis yang tiada kaitan pun
# bertindih pada "dari, telah, bahwa, Allah, Rasulullah".
_HENTI = {
    "yang", "dari", "dan", "itu", "ini", "pada", "dengan", "untuk",
    "telah", "tidak", "dia", "aku", "kami", "kamu", "kalian", "mereka",
    "adalah", "akan", "sudah", "bahwa", "bahawa", "ada", "oleh", "atau",
    "maka", "jika", "kalau", "saya", "kepada", "dalam", "seorang",
    "orang", "berkata", "katanya", "kata", "menceritakan", "kepadaku",
    "kepada", "kami", "haddatsana", "hadits", "hadis", "allah",
    "rasulullah", "nabi", "shallallahu", "sallallahu", "alaihi",
    "wasallam", "wa", "radhiyallahu", "radiallahu", "anhu", "anha",
    "bin", "binti", "abu", "ibnu", "ibn", "abi", "dia", "ia", "kepada",
    "sesungguhnya", "kemudian", "lalu", "ketika", "seperti", "juga",
    "saw", "swt",
}


def tokens(teks: str) -> set[str]:
    if not teks:
        return set()
    s = _BUKAN_HURUF.sub(" ", teks.lower())
    return {w for w in s.split() if len(w) > 3 and w not in _HENTI}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def turun(kod: str) -> str | None:
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, f"{kod}.json")
    if os.path.exists(f) and os.path.getsize(f) > 1000:
        return f
    url = f"{CDN}/{kod}.min.json"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"    gagal muat turun {kod}: {e}")
        return None
    with open(f, "wb") as fh:
        fh.write(data)
    return f


def audit(conn, slug: str) -> tuple[int, int, int]:
    """Pulangkan (disemak, disahkan, disyaki)."""
    fz = PETA_KITAB.get(slug)
    if not fz:
        return 0, 0, 0

    f_ara = turun(f"ara-{fz}")
    f_ind = turun(f"ind-{fz}")
    if not f_ara or not f_ind:
        print(f"  {slug:12} sumber tidak lengkap — dilangkau")
        return 0, 0, 0

    ind_cdn = {h.get("hadithnumber"): (h.get("text") or "")
               for h in muat_json(f_ind).get("hadiths", [])}
    try:
        from core.eng_source import bina_indeks_ind
        indeks_ind = bina_indeks_ind(f_ind)
        from core.eng_source import bina_indeks_ind_kata
        _ti = {h.get("hadithnumber"): (h.get("text") or "")
               for h in muat_json(f_ind).get("hadiths", [])
               if isinstance(h.get("hadithnumber"), int)}
        indeks_ind_kata = bina_indeks_ind_kata(_ti)
    except Exception:
        indeks_ind, _ti, indeks_ind_kata = {}, {}, {}

    penuh, awalan = bina_indeks(f_ara)
    teks_ara = {h.get("hadithnumber"): h.get("text", "")
                for h in muat_json(f_ara).get("hadiths", [])
                if isinstance(h.get("hadithnumber"), int)}
    ik = _bina_indeks_kata(penuh, teks_ara)

    baris = conn.execute(
        "SELECT hadis_id, arab, indonesia FROM hadis "
        "WHERE collection=? AND arab<>'' AND indonesia<>'' "
        "ORDER BY hadis_id", (slug,)).fetchall()
    if not baris:
        print(f"  {slug:12} tiada baris dengan teks Indonesia")
        return 0, 0, 0

    per_kaedah: dict[str, list[float]] = {}
    syak_contoh: list[tuple[int, int, str, float]] = []
    n_semak = n_sah = n_syak = 0

    for hid, arab, ind_db in baris:
        no, kaedah = padan(arab or "", penuh, awalan, ik,
                           teks_sumber=teks_ara,
                           ind_hadis_my=ind_db, indeks_ind=indeks_ind,
                           indeks_ind_kata=indeks_ind_kata, teks_ind=_ti)
        if no is None:
            continue
        lawan = ind_cdn.get(no)
        if not lawan:
            continue
        # `indo` dipadan MENGGUNAKAN teks Indonesia, jadi mengauditnya
        # dengan teks Indonesia ialah hujah berpusing. Ia dikira untuk
        # kelengkapan tetapi bukan bukti bebas -- ditandakan begitu.
        j = jaccard(tokens(ind_db), tokens(lawan))
        per_kaedah.setdefault(kaedah, []).append(j)
        n_semak += 1
        if j < SYAK:
            n_syak += 1
            if len(syak_contoh) < 3:
                syak_contoh.append((hid, no, kaedah, j))
        else:
            n_sah += 1

    if not n_semak:
        print(f"  {slug:12} tiada pertindihan untuk diaudit")
        return 0, 0, 0

    pct = n_sah * 100 / n_semak
    print(f"  {slug:12} {pct:5.1f}% disahkan   "
          f"{n_sah:,}/{n_semak:,}   disyaki={n_syak:,}")
    for k in ("indo", "indo~", "penuh", "awalan", "kata"):
        v = per_kaedah.get(k)
        if not v:
            continue
        buruk = sum(1 for x in v if x < SYAK)
        nota = "  (bukan bukti bebas)" if k.startswith("indo") else ""
        print(f"  {'':12}   {k:7} n={len(v):5}  "
              f"purata={sum(v)/len(v):.2f}  disyaki={buruk:4} "
              f"({buruk/len(v)*100:4.1f}%){nota}")
    for hid, no, kaedah, j in syak_contoh:
        print(f"  {'':12}   ? hadis.db #{hid} -> CDN #{no} "
              f"({kaedah}, tindihan {j:.2f})")
    return n_semak, n_sah, n_syak


def main() -> int:
    arg = sys.argv[1:]
    if "--semua" in arg:
        sasaran = list(PETA_KITAB)
    else:
        mahu = [a for a in arg if not a.startswith("--")]
        sasaran = mahu or ["bukhari"]

    conn = connect(DB_PATH)
    jum = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    if jum == 0:
        print("\n  hadis.db kosong. Jalankan dahulu: python sync.py\n")
        return 1

    print("\n" + "=" * 66)
    print(f"  AUDIT KETEPATAN PADANAN — saksi bebas  (v{VERSI})")
    print("=" * 66)
    print(f"\n  Jaccard padanan : {JACCARD_MIN}")
    print(f"  Ambang syak     : {SYAK} pertindihan kata Indonesia")
    print("  Membandingkan   : hadis.db.indonesia  vs  CDN ind-*\n")

    t_s = t_o = t_y = 0
    for slug in sasaran:
        a, b, c = audit(conn, slug)
        t_s += a
        t_o += b
        t_y += c

    print("\n" + "=" * 66)
    if t_s:
        print(f"  Disemak   : {t_s:,}")
        print(f"  Disahkan  : {t_o:,} ({t_o/t_s*100:.1f}%)")
        print(f"  Disyaki   : {t_y:,} ({t_y/t_s*100:.1f}%)")
        print()
        if t_y / t_s > 0.10:
            print("  Kadar syak TINGGI. Padanan perlu diperketat.")
        else:
            print("  Kadar syak boleh diterima.")
    print("=" * 66 + "\n")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
