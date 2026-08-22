"""Terjemahan — pengumpul sumber.

STATUS: tidak dipanggil oleh pipeline sejak Fasa 1-3 dibuang daripada
halaman Huraian. Dikekalkan kerana ia satu-satunya tempat logik
"kitab mana tiada terjemahan Inggeris" (`TIADA_ENGLISH`) wujud, dan
mudah disambung semula jika UI perlu melaporkan status terjemahan.

Terjemahan sebenar dipapar terus oleh `ui/app_qt.py:_switch_lang`.


PERANAN
-------
Fasa ini TIDAK menterjemah. Ia mengumpul dan menggabungkan terjemahan
manusia daripada beberapa sumber, kemudian melaporkan asal-usul setiap
satu dengan jujur.

    Melayu     : hadis.my            (liputan 100%)
    Indonesia  : hadis.my            (liputan 100%)
    Inggeris   : sunnah.com melalui fawazahmed0/hadith-api
                 -- dipadan melalui TEKS ARAB, bukan nombor hadis

MENGAPA TIDAK PADAN IKUT NOMBOR
-------------------------------
Penomboran berbeza antara sumber (Bukhari 7,008 vs 7,589). Memadan ikut
ID akan memberi terjemahan hadis yang SALAH -- bahaya untuk aplikasi
agama. Sebaliknya `sync_english.py` memadan teks Arab yang dinormalisasi,
kemudian menyimpan hasilnya dalam jadual `terjemahan_eng`.

Diuji terhadap 7 kitab, 10,500 sampel: 0 padanan salah.

KITAB TANPA INGGERIS
--------------------
`ahmad` dan `darimi` tiada dalam sumber luar. Fasa ini memulangkan rentetan
kosong dan UI mesti memaparkan "tidak tersedia" -- jangan berpura-pura.
"""

from __future__ import annotations

SUMBER = {
    "melayu": "hadis.my",
    "indonesia": "hadis.my",
    "english": "sunnah.com / fawazahmed0-hadith-api",
}

# Kitab yang memang tiada terjemahan Inggeris dalam sumber semasa.
TIADA_ENGLISH = ("ahmad", "darimi")


def _kosong() -> dict:
    return {
        "malay": "", "indonesia": "", "english": "",
        "status": "kosong", "sources": {}, "tersedia": [], "tiada": [],
        # `nota` mesti sentiasa wujud -- pemanggil menganggapnya ada.
        "nota": "",
    }


def translate(text: str = "", hadis: dict | None = None, **kw) -> dict:
    """Kumpul terjemahan sedia ada daripada objek hadis.

    Args:
        text:  diabaikan (kekal untuk keserasian tandatangan lama)
        hadis: dict hadis daripada API/DB -- sumber sebenar.
               Medan `english` diisi oleh HadisAPI daripada jadual
               `terjemahan_eng` jika `sync_english.py` telah dijalankan.

    Returns:
        dict dengan `status`:
            "kosong"       -- tiada apa-apa terjemahan
            "dari_sumber"  -- ada sekurang-kurangnya satu terjemahan
        dan senarai `tersedia` / `tiada` supaya UI boleh melaporkan
        keadaan sebenar tanpa meneka.
    """
    h = hadis or {}
    slug = (h.get("collection") or "").strip()

    ms = (h.get("melayu") or "").strip()
    idn = (h.get("indonesia") or "").strip()
    en = (h.get("english") or "").strip()

    if not (ms or idn or en):
        out = _kosong()
        out["tiada"] = ["melayu", "indonesia", "english"]
        return out

    tersedia = [k for k, v in
                (("melayu", ms), ("indonesia", idn), ("english", en)) if v]
    tiada = [k for k, v in
             (("melayu", ms), ("indonesia", idn), ("english", en)) if not v]

    sources = {}
    if ms:
        sources["malay"] = SUMBER["melayu"]
    if idn:
        sources["indonesia"] = SUMBER["indonesia"]
    if en:
        sources["english"] = SUMBER["english"]

    nota = ""
    if not en:
        if slug in TIADA_ENGLISH:
            nota = ("Terjemahan Inggeris tiada untuk kitab ini dalam "
                    "sumber semasa.")
        else:
            nota = ("Terjemahan Inggeris belum dimuat turun. "
                    "Jalankan: python sync_english.py")

    return {
        "malay": ms,
        "indonesia": idn,
        "english": en,
        "status": "dari_sumber",
        "sources": sources,
        "tersedia": tersedia,
        "tiada": tiada,
        "nota": nota,
    }
