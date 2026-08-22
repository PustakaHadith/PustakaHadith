"""Pembetulan istilah Indonesia yang tertinggal dalam terjemahan Melayu.

MASALAH
-------
Terjemahan Melayu hadis.my majoritinya betul (`solat`, `bahawa`,
`wuduk`, `Ramadan`), tetapi satu istilah tertinggal secara sistematik:

    "Shallallahu 'alaihi wasallam"     <- ejaan Indonesia

Diukur pada 400 hadis daripada 4 kitab:

    Shallallahu   456 kali
    kalian         10
    rakaat          9
    sujud           1

Istilah lain (`shalat`, `hadits`, `Ramadhan`, `adzan`, `bahwa`,
`dzikir`, `wudhu`) — **sifar**. Jadi masalahnya sempit dan boleh
dibetulkan dengan selamat.

RUJUKAN EJAAN
-------------
Dewan Bahasa dan Pustaka (PRPM, khidmat nasihat):

  "Sallallahualaihiwasallam ialah nama khas yang diambil daripada
   bahasa Arab, oleh itu ejaannya dimulakan dengan huruf besar dan
   kependekannya SAW."

Jadi: **Sallallahu** (tanpa `h` selepas `S`), bukan `Shallallahu`.

PRINSIP
-------
Pembetulan ini bersifat **paparan sahaja**. Teks asal dalam `hadis.db`
TIDAK diubah — kita tidak menulis semula sumber. Jika penilaian ini
didapati salah kemudian, cukup matikan fungsi ini.

Hanya ejaan diperbetul. Struktur ayat, pilihan perkataan, dan makna
terjemahan dibiarkan sepenuhnya. Kita membetulkan transliterasi Arab,
bukan menyunting terjemahan ulama.
"""

from __future__ import annotations

import re

# ── Selawat & taradhi ─────────────────────────────────────────────────
# Kunci: corak regex (case-sensitive di mana perlu). Nilai: ganti.
#
# Nota: `Shallallahu` -> `Sallallahu` sahaja. Kita TIDAK memendekkan
# kepada "SAW" walaupun DBP membenarkannya -- memendekkan mengubah
# rupa teks secara drastik dan sesetengah pembaca mahu bentuk penuh.
_SELAWAT = [
    # Shallallahu / Sallallaahu / Shollallahu -> Sallallahu
    (re.compile(r"\bS[h]?[ao]ll?all?a+hu\b"), "Sallallahu"),
    (re.compile(r"\bs[h]?[ao]ll?all?a+hu\b"), "sallallahu"),
    # Radhiyallahu -> Radiallahu  (DBP: tanpa 'h' selepas 'd')
    (re.compile(r"\bR[ao]dh[iy]+all?a+hu\b"), "Radiallahu"),
    (re.compile(r"\br[ao]dh[iy]+all?a+hu\b"), "radiallahu"),
]

# ── Istilah agama: ejaan Indonesia -> Melayu ──────────────────────────
# Setiap entri disahkan terhadap Kamus Dewan / kelaziman Malaysia.
# Sengaja TIDAK memasukkan kata yang maknanya boleh berubah.
_ISTILAH = [
    (re.compile(r"\bshalat\b", re.I), "solat"),
    (re.compile(r"\bsholat\b", re.I), "solat"),
    (re.compile(r"\bhadits\b", re.I), "hadis"),
    (re.compile(r"\bRamadhan\b"), "Ramadan"),
    (re.compile(r"\bramadhan\b"), "ramadan"),
    (re.compile(r"\badzan\b", re.I), "azan"),
    (re.compile(r"\bdzikir\b", re.I), "zikir"),
    (re.compile(r"\bwudhu\b", re.I), "wuduk"),
    (re.compile(r"\bshahih\b", re.I), "sahih"),
    (re.compile(r"\bmesjid\b", re.I), "masjid"),
    (re.compile(r"\bustadz\b", re.I), "ustaz"),
    (re.compile(r"\bbahwa\b"), "bahawa"),
    (re.compile(r"\bBahwa\b"), "Bahawa"),
]

# `kalian` -> `kamu semua` DITINGGALKAN dengan sengaja.
# "kalian" difahami sepenuhnya di Malaysia dan bukan salah ejaan;
# menggantinya mengubah gaya penterjemah, bukan membetulkan kesilapan.


# ── Simbol selawat ────────────────────────────────────────────────────
# U+FDFA ﷺ ialah ligatur "sallallahu alayhi wasallam". Ia RINGKAS tetapi
# selawat kekal PENUH -- bukan singkatan dua huruf seperti "SAW".
#
# Ini penting: Imam Ibn Salah (Muqaddimah) dan al-Sakhawi (Fath
# al-Mughith) menasihati penulis hadis supaya menulis selawat penuh
# setiap kali, dan menyingkatnya dikira `khilaf al-awla`. Ligatur
# TIDAK menyingkat -- ia satu titik kod yang mengandungi lafaz penuh.
#
# Risiko: banyak fon tiada glif ini dan memaparkan kotak tofu.
# `simbol_boleh_dipapar()` mesti disemak dahulu sebelum digunakan.
LIGATUR_SELAWAT = "\ufdfa"

_FRASA_SELAWAT = re.compile(
    # Bentuk Melayu: "Sallallahu 'alaihi wasallam" (ejaan DBP).
    # Apostrof boleh ASCII ' atau petik melengkung ‘ ’ (U+2018/U+2019)
    # -- data hadis.my guna kedua-duanya; regex lama hanya terima ASCII
    # jadi 3,693 "Sallallahu ‘alaihi wasallam" tertinggal (Sesi 34 lanjutan).
    r"\bS[h]?[ao]ll?all?a+hu\s+[‘’'ʻʼ]?[Aa]laihi\s+wa\s?sallam\b"
    # Bentuk rumi (transliterasi): akademik "ṣallā Allāhu ʿalayhi
    # wasallama" dan gaya Melayu "salla Allahu 'alayhi wa-sallama".
    # Damma "u" pada Allāh dan fatha "a" pada sallama ialah bentuk
    # SEBENAR output transliterasi (bukan pausal) -- regex mesti
    # terima kedua-duanya (dengan atau tanpa) supaya ﷺ tidak tertinggal.
    r"|"
    r"\b[ṣs]all[āa]?\s+[Aa]ll[āa]h[u]?\s+[ʿ'ʻ’ʼ]alayhi\s+wa[- ]?sallam[a]?\b"
    # Bentuk ARAB penuh tertanam dalam teks Melayu: "صلى الله عليه
    # وسلم" (9,733 baris hadis.melayu). Toleransi tashkeel antara
    # huruf; varian typo DB "وسسلم" (dua س) turut diterima. Tiada
    # sempadan kata -- frasa ini tidak wujud sebagai serpihan
    # perkataan lain.
    r"|"
    # Setiap huruf diikuti tashkeel pilihan (termasuk SELEPAS huruf
    # akhir -- damma pada Allāh, kasra pada ʿalayhi, fatha pada m).
    r"ص[\u064B-\u065F\u0670]*ل[\u064B-\u065F\u0670]*ى"
    r"[\u064B-\u065F\u0670]*\s+"
    r"الل[\u064B-\u065F\u0670]*ه[\u064B-\u065F\u0670]*\s+"
    r"ع[\u064B-\u065F\u0670]*ل[\u064B-\u065F\u0670]*ي"
    r"[\u064B-\u065F\u0670]*ه[\u064B-\u065F\u0670]*\s+"
    r"و[\u064B-\u065F\u0670]*س[\u064B-\u065F\u0670]*س?"
    r"[\u064B-\u065F\u0670]*ل[\u064B-\u065F\u0670]*م"
    r"[\u064B-\u065F\u0670]*",
    re.I)


def simbol_boleh_dipapar(nama_fon: str = "") -> bool:
    """Semak sama ada fon boleh memaparkan ligatur ﷺ.

    Tanpa semakan ini pengguna nampak kotak kosong (tofu) dan
    menyangka apl rosak. Pulangkan False jika Qt tiada.
    """
    try:
        from PyQt5.QtGui import QFont, QFontMetrics
    except Exception:
        return False
    calon = [nama_fon] if nama_fon else []
    calon += ["Traditional Arabic", "Amiri", "Scheherazade New",
              "Segoe UI", "Arial", ""]
    for nama in calon:
        try:
            fm = QFontMetrics(QFont(nama) if nama else QFont())
            if fm.inFont(LIGATUR_SELAWAT):
                return True
        except Exception:
            continue
    return False


def guna_simbol_selawat(teks: str) -> str:
    """Ganti frasa selawat dengan ligatur Arab ﷺ.

    Merangkumi bentuk rumi (Melayu + transliterasi) DAN bentuk Arab
    penuh "صلى الله عليه وسلم" yang tertanam dalam teks Melayu.
    Panggil `simbol_boleh_dipapar()` DAHULU. Jika fon tiada glif,
    jangan guna fungsi ini -- teks penuh lebih baik daripada tofu.
    """
    if not teks:
        return teks or ""
    return _FRASA_SELAWAT.sub(LIGATUR_SELAWAT, teks)


def betulkan_melayu(teks: str, istilah: bool = True) -> str:
    """Betulkan ejaan Indonesia dalam teks terjemahan Melayu.

    Args:
        teks:    terjemahan Melayu daripada hadis.my
        istilah: jika False, hanya selawat/taradhi dibetulkan

    Returns:
        Teks yang dibetulkan. Input kosong dipulangkan seadanya.
    """
    if not teks:
        return teks or ""
    out = teks
    for rx, ganti in _SELAWAT:
        out = rx.sub(ganti, out)
    if istilah:
        for rx, ganti in _ISTILAH:
            out = rx.sub(ganti, out)
    return out


def kira_istilah(teks: str) -> dict[str, int]:
    """Kira istilah Indonesia yang dijumpai. Untuk diagnosis/audit."""
    hasil: dict[str, int] = {}
    for rx, ganti in _SELAWAT + _ISTILAH:
        n = len(rx.findall(teks or ""))
        if n:
            hasil[ganti] = hasil.get(ganti, 0) + n
    return hasil


# ── Terjemahan ralat runtime ─────────────────────────────────────────
# Mesej ralat daripada sqlite3/requests/OSError lahir dalam Bahasa
# Inggeris ("database is locked", "Connection refused", "No such file
# or directory"). Pengguna tidak sepatutnya melihat teks ini dalam
# toast. `terjemah_ralat()` memetakan corak biasa ke frasa Melayu;
# mesej yang tiada padanan dipulangkan seadanya supaya maklumat
# teknikal tidak hilang.
_RALAT_RUNTIME: list[tuple[str, str]] = [
    # sqlite3
    ("database is locked", "Pangkalan data sedang dikunci oleh aplikasi lain."),
    ("open database file", "Fail pangkalan data tidak dapat dibuka."),
    ("attempt to write a readonly database",
     "Pangkalan data hanya boleh dibaca."),
    ("sql logic error", "Ralat logik SQL."),
    ("no such table", "Jadual tidak wujud dalam pangkalan data."),
    ("no such column", "Lajur tidak wujud dalam pangkalan data."),
    ("database disk image is malformed", "Fail pangkalan data rosak."),
    ("disk i/o error", "Ralat baca/tulis pangkalan data."),
    # requests / rangkaian
    ("connection refused", "Sambungan ditolak oleh pelayan."),
    ("connection aborted", "Sambungan tergendala."),
    ("timed out", "Sambungan tamat masa."),
    ("max retries exceeded", "Gagal menghubungi pelayan."),
    ("name or service not known", "Nama pelayan tidak dikenali."),
    ("network is unreachable", "Rangkaian tidak dapat dicapai."),
    ("connection reset", "Sambungan ditamatkan oleh pelayan."),
    # HTTP / API
    ("http error 500", "Ralat pelayan (HTTP 500). Cuba sebentar lagi."),
    ("http error 502", "Ralat pelayan (HTTP 502). Cuba sebentar lagi."),
    ("http error 503", "Pelayan sibuk (HTTP 503). Cuba sebentar lagi."),
    ("server error", "Ralat pelayan. Cuba sebentar lagi."),
    ("expecting value", "Respons pelayan tidak sah (bukan JSON)."),
    ("json decode", "Respons pelayan tidak sah (bukan JSON)."),
    ("invalid json", "Respons pelayan tidak sah (bukan JSON)."),
    # faiss / torch
    ("no module named 'faiss'",
     "Pakej faiss tidak dipasang. Jalankan: pip install faiss-cpu"),
    ("cuda out of memory", "Memori GPU tidak mencukupi."),
    ("found no nvidia driver", "Pemacu GPU NVIDIA tidak dijumpai."),
    # OSError / sistem
    ("no such file or directory", "Fail atau folder tidak dijumpai."),
    ("permission denied", "Kebenaran ditolak."),
    ("broken pipe", "Sambungan putus."),
    ("out of memory", "Memori tidak mencukupi."),
]

# Perkataan Melayu yang hampir tidak wujud dalam mesej ralat Inggeris
# -- cukup untuk membezakan "Gagal menghubungi pelayan" (sudah Melayu)
# daripada "Connection refused" (mentah).
_KATA_MELAYU = ("tidak ", "tiada ", "gagal", "sila ", "cuba ", "ralat",
                "sambungan", "permintaan", "pelayan", "ditolak",
                "tamat masa", "dijumpai")


def _sudah_melayu(teks: str) -> bool:
    return any(k in teks for k in _KATA_MELAYU)


def terjemah_ralat(e) -> str:
    """Terjemah mesej ralat runtime (sqlite3/requests/OSError) ke Melayu.

    Args:
        e: pengecualian atau mesej ralat mentah (str).

    Returns:
        Mesej yang boleh dipapar pengguna. Corak biasa (pangkalan data,
        rangkaian, sistem fail) dipetakan ke frasa Melayu; mesej yang
        tiada padanan dipulangkan seadanya supaya maklumat tidak hilang.
    """
    msg = str(e) if not isinstance(e, str) else e
    msg = msg.strip()
    if not msg:
        return "Ralat tidak diketahui."
    low = msg.lower()
    # Mesej yang sudah Melayu (cth. daripada HadisAPIError) kekal.
    if _sudah_melayu(low):
        return msg
    for corak, ganti in _RALAT_RUNTIME:
        if corak in low:
            return ganti
    return msg
