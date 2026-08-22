#!/usr/bin/env python3
"""Ujian NEGATIF semakan 8l/8p/8q/8r/8w/8x/8z/8m/10b — cabang GAGAL dikesan.

Semakan dalam semak.py mengunci format jumlah hadis, pemalar render,
peta kembali dan ujian visual skrin. Skrip ini memutasi keadaan secara
sengaja dan menyahkan SETIAP cabang GAGAL dikesan, kemudian memulihkan
fail byte-tepat (binari, bukan teks) supaya git TIDAK tercemar (baris
akhir / kandungan kekal sama). Bahagian 8p diuji melalui suntikan
atribut dalam ingatan (tiada sentuh fail).

  8z (semak_visual_rujukan):
    (1)  fail ujian dibuang           -> 'uji_visual_* dibuang: [...]'
    (2)  fail baharu luar senarai     -> 'uji_visual_* baharu belum
         dalam senarai semak: [...]'
    (3a) MANUAL_REFERENSI_DEV.md hilang -> 'MANUAL_REFERENSI_DEV.md
         TIADA' GAGAL BERSIH (bukan ranap FileNotFoundError)
    (3b) senarai semak dikosongkan    -> 'senarai semak pra-hantar
         TIADA sebut: [...]'

  8w (semak_kitab_shell):
    (4)  `_subtitle_hadis` dipulangkan ke pages_kitab.py
         -> '_subtitle_hadis masih ada dalam pages_kitab'
    (5)  literal `f"{total:,} hadis"` dibenamkan semula dalam
         `_render_kitab_shell` -> 'literal format total masih
         dibenamkan dalam render' / 'TIADA guna fungsi'

  8x (semak_kad_koleksi):
    (6)  `_label_kad_hadis` dipulangkan ke pages.py
         -> '_label_kad_hadis masih ada dalam pages.py'
    (7)  literal `f"{total:,} Hadis"` / `f"{n:,} Hadis"` dibenamkan
         semula dalam KitabCard -> 'literal label hadis masih
         dibenamkan dalam KitabCard' / 'TIADA guna _label_kiraan'

  8l (semak_carian_sibuk):
    (8)  uji_visual_carian.py hilang -> 'uji_visual_carian.py TIADA'
    (9)  penanda wajib hilang dari uji_visual_carian.py
         -> 'uji_visual_carian.py tidak konsisten: tiada [...]'

  8p (semak_peta_kembali):
    (10) BACK_PETA (atribut dalam ingatan) dengan page bukan kunci
         PAGES -> 'BUKAN kunci PAGES' (tiada sentuh fail)

  8q (semak_nav_sebelum_seterusnya):
    (11) literal `f"‹ No. {hid - 1}"` dibenamkan semula dalam
         `_render_detail` -> 'literal format label lama masih
         dibenamkan' / 'TIADA guna fungsi label'

  8r (semak_pemalar_render):
    (12) literal label Simpan dibenamkan semula dalam `_render_detail`
         -> 'literal label Simpan masih dibenamkan' /
         'TIADA guna _label_simpan'

  10b (semak_versi_changelog):
    (13) VERSI palsu "2.0" (suntikan dalam ingatan, tiada sentuh fail)
         -> 'VERSI dikunci 1.0 (edaran rasmi), sebenar'
    (14) CHANGELOG.md hilang -> 'CHANGELOG.md TIADA' GAGAL BERSIH
         (bukan ranap FileNotFoundError)
    (15) seksyen "## 1.1" dipadam dari CHANGELOG.md
         -> 'tiada seksyen versi: [...]'

  8m (semak_bahasa_dokumen):
    (16) satu kata Indonesia disuntik ke PADANAN_ARKIB.md
         -> 'PADANAN_ARKIB.md: kata Indonesia ...' dikesan
    (17) docstring fail .py sementara mengandungi kata Indonesia
         -> 'kata Indonesia ...' dikesan

  8k (semak_pemula — pramuat QThread dikunci):
    (18) sambungan `worker.finished.connect(self._mula_pramuat)` dibuang
         dari app_qt.py -> '_mula_pramuat/_on_pramuat_siap TIADA /
         tidak disambung' dikesan
    (19) `def _mula_pramuat` dibuang -> mesej sama dikesan
    (20) `def _on_pramuat_siap` dibuang -> mesej sama dikesan
    (21) `_pra_muat_model` (kaedah mati thread utama) dipulangkan
         -> 'kaedah mati _pra_muat_model kembali' dikesan

  8v (semak_elide_chip — _warna_cip ikut makna):
    (22) `_warna_cip` disuntik (dalam ingatan) memetakan SEMUA kes ke
         MERAH -> '_warna_cip: Sahih -> HIJAU' GAGAL dikesan
    (23) `_warna_cip` disuntik memetakan SEMUA ke None (neutral) ->
         '_warna_cip: Palsu -> MERAH' GAGAL dikesan

  10aa (semak_logo_palet — logo selaras palet):
    (24) `BUKU_TEAL` dalam scripts/bina_logo.py ditukar ke TEAL biru
         lama #7FC4DE -> 'logo buku (hijau mockup): ... != tema'
         dikesan
    (25) baris `#7FC4DE` disuntik ke bina_logo.py -> 'masih guna
         TEAL biru lama' dikesan
    (26) scripts/bina_logo.py dibuang -> 'scripts/bina_logo.py TIADA'
         GAGAL BERSIH (bukan ranap FileNotFoundError)

  12 (semak_sesi_terakhir — 'Sesi Terakhir' MULA_SINI seiring git log):
    (27) tarikh Sesi Terakhir ditukar ke bulan lalu -> 'KETINGGALAN
         git log' dikesan
    (28) hash commit yang disebut ditukar ke `fffffff` (tidak wujud)
         -> 'hash tidak wujud dalam git: fffffff' dikesan
    (29) MULA_SINI.md dibuang -> 'MULA_SINI.md TIADA' GAGAL BERSIH
         (bukan ranap FileNotFoundError)
    (30) tarikh commit terbaru dibuang dari TEKS ringkasan (tajuk
         kekal) -> 'tidak menyebut tarikh kerja terkini' dikesan

  13 (semak_kontras_tema — WCAG AA semua tema):
    (31) NEUTRAL TEXT_FAINT diturunkan ke #707070 (3.6:1) ->
         'bawah AA 4.5' dikesan

  15 (semak_ringkasan_keadaan — ringkasan satu muka seiring
      'Sesi Terakhir'):
    (34) kiraan commit dalam ringkasan diturunkan (35 → 34) manakala
         'Sesi Terakhir' kekal 35 -> 'ringkasan kiraan commit' dikesan

Setiap cabang dijalankan dalam try/finally dengan pemulihan automatik;
di hujung, skrip menyahkan SEMUA semakan
(8z/8w/8x/8l/8p/8q/8r/8m/8k/8v/10aa/10b/12/13/14/15) hijau semula DAN
kandungan fail bersih (sama dengan keadaan sebelum ujian).

    python uji_negatif_8z.py
"""

import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import semak

UJI = "uji_visual_ralat.py"
MAN = "dokumen/manual/MANUAL_REFERENSI_DEV.md"
DUMMY = "uji_visual_cuba.py"
KITAB = "ui/pages_kitab.py"
PAGES = "ui/pages.py"
UJI_CARIAN = "uji_visual_carian.py"
DETAIL = "ui/pages_detail.py"
TRANS = "dokumen/manual/TRANSFORMASI_DETAIL.md"
README_MD = "README.md"
CLOG = "dokumen/perubahan/CHANGELOG.md"
PADANAN = "dokumen/audit/PADANAN_ARKIB.md"
PROBE_PY = "_neg_8m_probe.py"
APP_QT = "ui/app_qt.py"
LOGO = "scripts/bina_logo.py"
MULA = "dokumen/manual/MULA_SINI.md"
THEME = "ui/theme.py"

PASS = 0
FAIL = 0


def lari(fn) -> list:
    """Jalankan fungsi semakan; pulang senarai mesej GAGAL sahaja."""
    semak.gagal = []
    # Pembilang semak #16 ialah global sepanjang proses — mesti ditetap
    # semula supaya panggilan bersendirian tidak melihat kiraan lama.
    semak.LULUS_CNT = 0
    semak.TAJUK_NAMA = []
    fn()
    return list(semak.gagal)


def jangka(nama: str, dikesan: bool, mesej):
    global PASS, FAIL
    if dikesan:
        PASS += 1
        print(f"  OK    {nama}")
    else:
        FAIL += 1
        print(f"  GAGAL {nama}  {mesej}")


def simpan_bytes(p: str) -> bytes:
    with open(p, "rb") as f:
        return f.read()


def tulis_bytes(p: str, b: bytes):
    with open(p, "wb") as f:
        f.write(b)


def ganti_teks(b: bytes, lama: str, baharu: str) -> bytes:
    """Ganti teks dalam kandungan UTF-8; kekalkan baris akhir asal."""
    return b.decode("utf-8").replace(lama, baharu).encode("utf-8")


def buang_pyc_theme():
    """Buang cache bytecode ui/theme.py.

    Windows mtime berbutir 2 saat — tulis semula fail dalam tetingkap
    yang sama tidak menukar mtime, jadi `import ui.theme` kekal
    memakai .pyc LAMA (daripada sumber bermutasi). Buang .pyc sebelum
    dan selepas mutasi supaya import sentiasa baca fail sebenar.
    """
    import glob
    for p in glob.glob(os.path.join("ui", "__pycache__", "theme*.pyc")):
        try:
            os.remove(p)
        except OSError:
            pass


# ═════════════════════════ 8z ══════════════════════════════════════
print("=" * 62)
print("  UJIAN NEGATIF — 8l/8p/8q/8r/8w/8x/8z + 10b")
print("=" * 62)

# ── 1. Fail ujian dibuang ──────────────────────────────────────────
simpan_uji = simpan_bytes(UJI)
os.rename(UJI, UJI + ".neg")
try:
    g = lari(semak.semak_visual_rujukan)
    jangka("8z: fail dibuang -> 'dibuang' dikesan",
           any("dibuang" in m and UJI in m for m in g), g)
finally:
    os.rename(UJI + ".neg", UJI)

# ── 2. Fail baharu di luar senarai tetap ───────────────────────────
open(DUMMY, "w", encoding="utf-8").write("# dummy ujian negatif\n")
try:
    g = lari(semak.semak_visual_rujukan)
    jangka("8z: fail baharu -> 'baharu belum dalam senarai' dikesan",
           any("baharu belum dalam senarai" in m and DUMMY in m for m in g),
           g)
finally:
    os.remove(DUMMY)

# ── 3a. MANUAL hilang (GAGAL bersih, bukan ranap) ──────────────────
simpan_man = simpan_bytes(MAN)
os.rename(MAN, MAN + ".neg")
try:
    try:
        g = lari(semak.semak_visual_rujukan)
        jangka("8z: manual hilang -> GAGAL bersih (bukan ranap)",
               any("MANUAL_REFERENSI_DEV.md TIADA" in m for m in g), g)
    except Exception as e:
        FAIL += 1
        print(f"  GAGAL 8z: manual hilang ranap: {type(e).__name__}: {e}")
finally:
    os.rename(MAN + ".neg", MAN)

# ── 3b. Senarai semak dikosongkan (nama fail dibuang) ──────────────
src = open(MAN, encoding="utf-8").read()
mula = src.find("## 9. Senarai semak sebelum hantar")
tamat = src.find("\n## ", mula + 1)
if mula == -1 or tamat == -1:
    FAIL += 1
    print("  GAGAL 8z: bahagian senarai semak tidak dijumpai dalam manual")
else:
    blok_baru = src[mula:tamat].replace("uji_visual_", "uji_XXXXX_")
    tulis_bytes(MAN, (src[:mula] + blok_baru + src[tamat:]).encode("utf-8"))
    try:
        g = lari(semak.semak_visual_rujukan)
        jangka("8z: senarai dikosongkan -> 'TIADA sebut' dikesan",
               any("TIADA sebut" in m for m in g), g)
    finally:
        tulis_bytes(MAN, simpan_man)   # pulih byte-tepat

# ═════════════════════════ 8w ══════════════════════════════════════
# ── 4. `_subtitle_hadis` dipulangkan ke pages_kitab.py ─────────────
simpan_kitab = simpan_bytes(KITAB)
tulis_bytes(KITAB, simpan_kitab + b"\n\ndef _subtitle_hadis(total):\n"
             b"    return \"\"\n")
try:
    g = lari(semak.semak_kitab_shell)
    jangka("8w: _subtitle_hadis dipulangkan -> 'masih ada' dikesan",
           any("_subtitle_hadis masih ada" in m for m in g), g)
finally:
    tulis_bytes(KITAB, simpan_kitab)

# ── 5. Literal format dibenamkan semula dalam _render_kitab_shell ──
tulis_bytes(KITAB, ganti_teks(
    simpan_kitab, '_label_kiraan(total, "hadis", "")',
    'f"{total:,} hadis"'))
try:
    g = lari(semak.semak_kitab_shell)
    jangka("8w: literal dibenamkan semula -> 'literal masih' dikesan",
           any("literal format total masih dibenamkan" in m for m in g)
           or any("TIADA guna fungsi" in m for m in g), g)
finally:
    tulis_bytes(KITAB, simpan_kitab)

# ═════════════════════════ 8x ══════════════════════════════════════
# ── 6. `_label_kad_hadis` dipulangkan ke pages.py ──────────────────
simpan_pages = simpan_bytes(PAGES)
tulis_bytes(PAGES, simpan_pages + b"\n\ndef _label_kad_hadis(total):\n"
             b"    return \"\"\n")
try:
    g = lari(semak.semak_kad_koleksi)
    jangka("8x: _label_kad_hadis dipulangkan -> 'masih ada' dikesan",
           any("_label_kad_hadis masih ada" in m for m in g), g)
finally:
    tulis_bytes(PAGES, simpan_pages)

# ── 7. Literal label dibenamkan semula dalam KitabCard ─────────────
mut_pages = ganti_teks(simpan_pages,
                       '_label_kiraan(total, "Hadis", "— Hadis")',
                       'f"{total:,} Hadis"')
mut_pages = ganti_teks(mut_pages,
                       '_label_kiraan(n, "Hadis", "— Hadis")',
                       'f"{n:,} Hadis"')
tulis_bytes(PAGES, mut_pages)
try:
    g = lari(semak.semak_kad_koleksi)
    jangka("8x: literal label dibenamkan semula -> dikesan",
           any("literal label hadis masih dibenamkan" in m for m in g)
           or any("TIADA guna _label_kiraan" in m for m in g), g)
finally:
    tulis_bytes(PAGES, simpan_pages)

# ═════════════════════════ 8l ══════════════════════════════════════
# ── 8. uji_visual_carian.py hilang ─────────────────────────────────
simpan_carian = simpan_bytes(UJI_CARIAN)
os.rename(UJI_CARIAN, UJI_CARIAN + ".neg")
try:
    g = lari(semak.semak_carian_sibuk)
    jangka("8l: uji_visual_carian hilang -> 'TIADA' dikesan",
           any("uji_visual_carian.py TIADA" in m for m in g), g)
finally:
    os.rename(UJI_CARIAN + ".neg", UJI_CARIAN)

# ── 9. Penanda wajib hilang dari uji_visual_carian.py ──────────────
tulis_bytes(UJI_CARIAN, ganti_teks(simpan_carian,
                                   "_carian_sibuk", "jam_sibuk"))
try:
    g = lari(semak.semak_carian_sibuk)
    jangka("8l: penanda wajib hilang -> 'tidak konsisten' dikesan",
           any("tidak konsisten" in m for m in g), g)
finally:
    tulis_bytes(UJI_CARIAN, simpan_carian)

# ═════════════════════════ 8p ══════════════════════════════════════
# ── 10. BACK_PETA (dalam ingatan) dengan page bukan kunci PAGES ────
import ui.pages_detail as pd_detail
asli_peta = dict(pd_detail.BACK_PETA)
pd_detail.BACK_PETA = {"home": ("Utama", "bukan_halaman"),
                       "search": ("Hasil carian", "search"),
                       "saved": ("Tersimpan", "saved"),
                       "kitab": ("Senarai kitab", "kitab")}
try:
    g = lari(semak.semak_peta_kembali)
    jangka("8p: page bukan kunci PAGES -> 'BUKAN kunci' dikesan",
           any("BUKAN kunci PAGES" in m for m in g), g)
finally:
    pd_detail.BACK_PETA = asli_peta

# ═════════════════════════ 8q ══════════════════════════════════════
# ── 11. Literal label lama dibenamkan semula dalam _render_detail ──
simpan_detail = simpan_bytes(DETAIL)
tulis_bytes(DETAIL, ganti_teks(simpan_detail,
                               "lbl_sebelum = _label_sebelum(hid)",
                               'lbl_sebelum = f"‹ No. {hid - 1}"'))
try:
    g = lari(semak.semak_nav_sebelum_seterusnya)
    jangka("8q: literal label lama dibenamkan -> dikesan",
           any("literal format label lama masih" in m for m in g)
           or any("TIADA guna fungsi label" in m for m in g), g)
finally:
    tulis_bytes(DETAIL, simpan_detail)

# ═════════════════════════ 8r ══════════════════════════════════════
# ── 12. Literal label Simpan dibenamkan semula dalam _render_detail ─
tulis_bytes(DETAIL, ganti_teks(simpan_detail,
                               "_label_simpan(saved)",
                               '"⭐ Tersimpan" if saved else "☆ Simpan"'))
try:
    g = lari(semak.semak_pemalar_render)
    jangka("8r: literal label Simpan dibenamkan -> dikesan",
           any("literal label Simpan masih dibenamkan" in m for m in g)
           or any("TIADA guna _label_simpan" in m for m in g), g)
finally:
    tulis_bytes(DETAIL, simpan_detail)

# ═════════════════════════ 10b ═════════════════════════════════════
# ── 13. VERSI bukan 1.0 (suntikan dalam ingatan, tiada sentuh fail) ─
import types as _types
import VERSI as _versi_asli
versi_palsu = _types.ModuleType("VERSI")
versi_palsu.VERSI = "2.0"
versi_palsu.CIRI = getattr(_versi_asli, "CIRI", ())
sys.modules["VERSI"] = versi_palsu
try:
    g = lari(semak.semak_versi_changelog)
    jangka("10b: VERSI 2.0 -> 'dikunci 1.0' dikesan",
           any("VERSI dikunci 1.0" in m for m in g), g)
finally:
    sys.modules["VERSI"] = _versi_asli

# ── 14. CHANGELOG.md hilang (GAGAL bersih, bukan ranap) ─────────────
simpan_clog = simpan_bytes(CLOG)
os.rename(CLOG, CLOG + ".neg")
try:
    try:
        g = lari(semak.semak_versi_changelog)
        jangka("10b: CHANGELOG hilang -> 'TIADA' dikesan",
               any("CHANGELOG.md TIADA" in m for m in g), g)
    except Exception as e:
        FAIL += 1
        print(f"  GAGAL 10b: CHANGELOG hilang ranap: "
              f"{type(e).__name__}: {e}")
finally:
    os.rename(CLOG + ".neg", CLOG)

# ── 15. Seksyen versi dipadam dari CHANGELOG.md ─────────────────────
# Padam header seksyen dalam KEDUA-DUA gaya baris (LF/CRLF): dengan
# core.autocrlf=true, fail .md bekerja-copy boleh jadi CRLF dan
# ganti_teks LF tidak padan -> mutasi palsu (pepijat terpendam).
_header_1_1 = "## 1.1 — 7 Ogos 2026".encode("utf-8")
tulis_bytes(CLOG, simpan_clog.replace(_header_1_1 + b"\r\n", b"")
                          .replace(_header_1_1 + b"\n", b""))
try:
    g = lari(semak.semak_versi_changelog)
    jangka("10b: seksyen 1.1 dipadam -> 'tiada seksyen' dikesan",
           any("tiada seksyen versi" in m and "1.1" in m for m in g), g)
finally:
    tulis_bytes(CLOG, simpan_clog)

# ═════════════════════════ 8m ══════════════════════════════════════
# ── 16. Kata Indonesia disuntik ke PADANAN_ARKIB.md ─────────────────
simpan_padan = simpan_bytes(PADANAN)
tulis_bytes(PADANAN, simpan_padan + b"\n# ujian negatif 8m: proyek\n")
try:
    g = lari(semak.semak_bahasa_dokumen)
    jangka("8m: kata Indonesia dalam PADANAN_ARKIB.md -> 'kata Indonesia' dikesan",
           any("PADANAN_ARKIB.md" in m and "kata Indonesia" in m
               and "proyek" in m for m in g), g)
finally:
    tulis_bytes(PADANAN, simpan_padan)

# ── 17. Docstring fail .py sementara dengan kata Indonesia ──────────
tulis_bytes(PROBE_PY, ('def _probe_8m():\n'
                       '    """Docstring: proyek ini bersih."""\n'
                       '    return 0\n').encode("utf-8"))
try:
    g = lari(semak.semak_bahasa_dokumen)
    jangka("8m: kata Indonesia dalam docstring .py -> dikesan",
           any(PROBE_PY in m and "kata Indonesia" in m
               and "proyek" in m for m in g), g)
finally:
    os.remove(PROBE_PY)

# ═════════════════════════ 8k ══════════════════════════════════════
# Semakan 8k (semak_pemula) mengunci pramuat model melalui
# PreloadWorker (QThread) selepas CollectionsWorker -- BUKAN kaedah
# lama thread utama. Setiap cabang GAGAL mesti dikesan.
simpan_qt = simpan_bytes(APP_QT)

# ── 18. Sambungan _mula_pramuat dibuang ────────────────────────────
tulis_bytes(APP_QT, ganti_teks(
    simpan_qt, "worker.finished.connect(self._mula_pramuat)",
    "worker.finished.connect(self._abaikan_sambungan)"))
try:
    g = lari(semak.semak_pemula)
    jangka("8k: sambungan _mula_pramuat dibuang -> 'TIADA / tidak disambung' dikesan",
           any("_mula_pramuat/_on_pramuat_siap TIADA" in m for m in g), g)
finally:
    tulis_bytes(APP_QT, simpan_qt)

# ── 19. Kaedah _mula_pramuat dibuang ────────────────────────────────
# NOTA: nama pengganti TIDAK boleh mengandungi substring `_mula_pramuat`
# (semakan 8k gunakan `"def _mula_pramuat" in src`), jadi guna nama
# yang berbeza sepenuhnya.
tulis_bytes(APP_QT, ganti_teks(simpan_qt,
                               "def _mula_pramuat(self):",
                               "def _mula_preload(self):"))
try:
    g = lari(semak.semak_pemula)
    jangka("8k: _mula_pramuat dibuang -> 'TIADA / tidak disambung' dikesan",
           any("_mula_pramuat/_on_pramuat_siap TIADA" in m for m in g), g)
finally:
    tulis_bytes(APP_QT, simpan_qt)

# ── 20. Kaedah _on_pramuat_siap dibuang ─────────────────────────────
tulis_bytes(APP_QT, ganti_teks(simpan_qt,
                               "def _on_pramuat_siap(self, ok: bool):",
                               "def _on_preload_siap(self, ok: bool):"))
try:
    g = lari(semak.semak_pemula)
    jangka("8k: _on_pramuat_siap dibuang -> 'TIADA / tidak disambung' dikesan",
           any("_mula_pramuat/_on_pramuat_siap TIADA" in m for m in g), g)
finally:
    tulis_bytes(APP_QT, simpan_qt)

# ── 21. Kaedah mati _pra_muat_model dipulangkan ─────────────────────
tulis_bytes(APP_QT, simpan_qt + b"\n\ndef _pra_muat_model(self):\n"
             b"    return None\n")
try:
    g = lari(semak.semak_pemula)
    jangka("8k: _pra_muat_model dipulangkan -> 'kaedah mati kembali' dikesan",
           any("kaedah mati _pra_muat_model kembali" in m for m in g), g)
finally:
    tulis_bytes(APP_QT, simpan_qt)

# ═════════════════════════ 8v ══════════════════════════════════════
# Semakan 8v (semak_elide_chip) mengunci `_warna_cip`: klasifikasi
# ikut makna (hijau/merah/amber/neutral). Mutasi dalam ingatan (sama
# corak 8p) supaya tiada sentuh fail.
import ui.pages_detail as pd_detail

# ── 22. _warna_cip memetakan SEMUA kes ke MERAH ─────────────────────
asli_warna = pd_detail._warna_cip
pd_detail._warna_cip = lambda teks: (0x3B, 0x25, 0x23, 0x5C, 0x3A, 0x42,
                                      0xE0, 0x8A, 0x80)
try:
    g = lari(semak.semak_elide_chip)
    jangka("8v: _warna_cip semua-MERAH -> 'Sahih -> HIJAU' GAGAL dikesan",
           any("_warna_cip: Sahih -> HIJAU" in m for m in g), g)
finally:
    pd_detail._warna_cip = asli_warna

# ── 23. _warna_cip memetakan SEMUA ke None (neutral) ────────────────
pd_detail._warna_cip = lambda teks: None
try:
    g = lari(semak.semak_elide_chip)
    jangka("8v: _warna_cip semua-None -> 'Palsu -> MERAH' GAGAL dikesan",
           any("_warna_cip: Palsu -> MERAH" in m for m in g), g)
finally:
    pd_detail._warna_cip = asli_warna

# ═════════════════════════ 10aa ════════════════════════════════════
# Semakan 10aa (semak_logo_palet) mengunci bina_logo.py selaras palet.
simpan_logo = simpan_bytes(LOGO)

# ── 24. BUKU_TEAL ditukar ke TEAL biru lama ─────────────────────────
tulis_bytes(LOGO, ganti_teks(simpan_logo,
                             'BUKU_TEAL = "#5CBF85"',
                             'BUKU_TEAL = "#7FC4DE"'))
try:
    g = lari(semak.semak_logo_palet)
    jangka("10aa: BUKU_TEAL biru -> 'logo buku != tema' dikesan",
           any("logo buku (hijau mockup)" in m and "!=" in m for m in g),
           g)
finally:
    tulis_bytes(LOGO, simpan_logo)

# ── 25. Baris #7FC4DE disuntik ke bina_logo.py ──────────────────────
tulis_bytes(LOGO, simpan_logo + b"\n# ujian negatif 10aa: warna = \"#7FC4DE\"\n")
try:
    g = lari(semak.semak_logo_palet)
    jangka("10aa: #7FC4DE disuntik -> 'masih guna TEAL biru lama' dikesan",
           any("TEAL biru lama" in m and "#7FC4DE" in m for m in g), g)
finally:
    tulis_bytes(LOGO, simpan_logo)

# ── 26. bina_logo.py dibuang (GAGAL bersih, bukan ranap) ────────────
os.rename(LOGO, LOGO + ".neg")
try:
    try:
        g = lari(semak.semak_logo_palet)
        jangka("10aa: bina_logo.py hilang -> 'TIADA' GAGAL bersih",
               any("scripts/bina_logo.py TIADA" in m for m in g), g)
    except Exception as e:
        FAIL += 1
        print(f"  GAGAL 10aa: bina_logo.py hilang ranap: "
              f"{type(e).__name__}: {e}")
finally:
    os.rename(LOGO + ".neg", LOGO)

# Semakan 12 (semak_sesi_terakhir) mengunci MULA_SINI.md 'Sesi Terakhir'
# seiring git log (14 Ogos 2026).
simpan_mula = simpan_bytes(MULA)

# ── 27. Tarikh Sesi Terakhir ditukar ke bulan lalu ──────────────────
tulis_bytes(MULA, ganti_teks(simpan_mula,
                             "## Sesi Terakhir — 19 Ogos 2026 (5 commit)",
                             "## Sesi Terakhir — 13 Ogos 2026"))
try:
    g = lari(semak.semak_sesi_terakhir)
    jangka("12: tarikh Sesi Terakhir lapuk -> 'KETINGGALAN git log' dikesan",
           any("KETINGGALAN git log" in m for m in g), g)
finally:
    tulis_bytes(MULA, simpan_mula)

# ── 28. Hash commit disebut ditukar ke fffffff (tidak wujud) ────────
tulis_bytes(MULA, ganti_teks(simpan_mula, "1b1390c", "fffffff"))
try:
    g = lari(semak.semak_sesi_terakhir)
    jangka("12: hash fffffff -> 'hash tidak wujud dalam git' dikesan",
           any("hash tidak wujud" in m and "fffffff" in m for m in g), g)
finally:
    tulis_bytes(MULA, simpan_mula)

# ── 29. MULA_SINI.md dibuang (GAGAL bersih, bukan ranap) ────────────
os.rename(MULA, MULA + ".neg")
try:
    try:
        g = lari(semak.semak_sesi_terakhir)
        jangka("12: MULA_SINI.md hilang -> 'TIADA' GAGAL bersih",
               any("MULA_SINI.md TIADA" in m for m in g), g)
    except Exception as e:
        FAIL += 1
        print(f"  GAGAL 12: MULA_SINI.md hilang ranap: "
              f"{type(e).__name__}: {e}")
finally:
    os.rename(MULA + ".neg", MULA)

# ── 30. Tarikh kerja dibuang dari TEKS ringkasan (tajuk kekal) ───────
# Rentetan sasaran = intro 'Kerja 19 Ogos' SEMASA (satu baris — fail
# MULA_SINI ialah CRLF, jadi rentetan berbilang baris dengan \n tidak
# padan). Ia menyebut SATU-SATUNYA '18 Ogos' (tarikh git sebelum komit
# ini) DAN '19 Ogos' (selepas komit) dalam ringkasan — menukarnya
# menghilangkan tarikh git dalam kedua-dua keadaan. Nota: bila intro
# berubah, mutasi ini juga perlu diubah (mengunci kedua-duanya).
# Ringkasan kini menyebut '19 Ogos' di beberapa tempat (intro, komit 5,
# kiraan telus) — SEMUA dibuang supaya simulasi "ringkasan lapuk"
# kekal sah (sebutan '18 Ogos'/'17 Ogos' dll. tidak memenuhi semakan:
# semakan mencari tarikh git terkini sahaja).
tulis_bytes(MULA, ganti_teks(
    ganti_teks(
        ganti_teks(
            ganti_teks(simpan_mula,
                "Kerja 19 Ogos — **5 commit** (sambungan 8+2LB 18 Ogos +",
                "Kerja terkini — **5 commit** (sambungan"),
            "semula ke rentetan 19 Ogos (5 commit)",
            "semula ke rentetan semasa (5 commit)"),
        "(log harian 19 Ogos belum wujud)",
        "(log harian belum wujud)"),
    "· 19 Ogos = **5 commit**.",
    "· hari ini = **5 commit**."))
try:
    g = lari(semak.semak_sesi_terakhir)
    jangka("12: tarikh kerja hilang dari teks ringkasan -> "
           "'tidak menyebut tarikh kerja terkini' dikesan",
           any("tidak menyebut tarikh kerja terkini" in m for m in g), g)
finally:
    tulis_bytes(MULA, simpan_mula)

# ── 31. Kontras tema jatuh bawah AA (WCAG) ──────────────────────────
# NEUTRAL TEXT_FAINT diturunkan ke #707070 (~3.6:1 pada PAGE_BG) —
# semakan 13 mesti dikesan. Baris sasaran = kunci NEUTRAL sahaja
# (DARK #928D80, LIGHT #6D6858 berbeza), jadi ganti selamat.
simpan_theme = simpan_bytes(THEME)
tulis_bytes(THEME, ganti_teks(
    simpan_theme,
    '"TEXT_FAINT": "#8E8E8E",',
    '"TEXT_FAINT": "#707070",'))
try:
    # ui.theme mungkin sudah ter-cache (semak 10aa import modul) —
    # buang dari sys.modules + .pyc supaya semakan baca FAIL yang
    # dimutasi, bukan salinan lama (ingatan atau bytecode).
    sys.modules.pop("ui.theme", None)
    buang_pyc_theme()
    g = lari(semak.semak_kontras_tema)
    jangka("13: kontras bawah AA (neutral TEXT_FAINT #707070) -> "
           "'bawah AA 4.5' dikesan",
           any("bawah AA 4.5" in m for m in g), g)
finally:
    tulis_bytes(THEME, simpan_theme)
    sys.modules.pop("ui.theme", None)   # pulih juga cache modul
    buang_pyc_theme()                    # dan cache bytecode

# ── 32. Susun atur RTL lama dibenamkan semula dalam dokumen ────────
# "Arab di kiri" (susun atur lama) disuntik ke TRANSFORMASI_DETAIL.md —
# semakan 14 mesti dikesan. Rentetan sasaran = baris RTL semasa.
simpan_trans = simpan_bytes(TRANS)
tulis_bytes(TRANS, ganti_teks(
    simpan_trans,
    "keadaan semasa ialah Arab kanan, terjemahan kiri.",
    "keadaan semasa ialah Arab di kiri, terjemahan di kanan."))
try:
    g = lari(semak.semak_rtl_dokumen)
    jangka("14: tuntutan susun atur lama dalam dokumen -> "
           "'14: Audit susun atur RTL' dikesan",
           any("Arab di kiri" in m for m in g), g)
finally:
    tulis_bytes(TRANS, simpan_trans)

# ── 33. Susun atur RTL lama dibenamkan semula dalam README ─────────
# "Arab di kiri" disuntik ke README.md (baris RTL semasa) — semakan 14
# mesti dikesan pada README juga.
simpan_readme = simpan_bytes(README_MD)
tulis_bytes(README_MD, ganti_teks(
    simpan_readme,
    "susunan RTL (Arab di kanan, terjemahan di kiri",
    "susunan RTL (Arab di kiri, terjemahan di kanan"))
try:
    g = lari(semak.semak_rtl_dokumen)
    jangka("14: tuntutan susun atur lama dalam README -> "
           "'README.md:' dikesan",
           any("README.md:" in m for m in g), g)
finally:
    tulis_bytes(README_MD, simpan_readme)

# ── 34. Ringkasan satu muka ketinggalan 'Sesi Terakhir' (kiraan) ────
# Kiraan commit dalam ringkasan diturunkan (5 → 35) manakala 'Sesi
# Terakhir' kekal 5 — semakan 15 mesti dikesan. Rentetan sasaran =
# baris kiraan ringkasan SEMASA; bila ia berubah, mutasi ini juga
# perlu diubah (mengunci kedua-duanya).
tulis_bytes(MULA, ganti_teks(
    simpan_mula,
    "**5 commit** pada 19 Ogos (sambungan 8+2LB 18 Ogos + 18 commit 17 Ogos + 16 commit 16 Ogos + 36 commit 14 Ogos + 14 commit 15 Ogos).",
    "**35 commit** pada 19 Ogos (sambungan 8+2LB 18 Ogos + 18 commit 17 Ogos + 16 commit 16 Ogos + 36 commit 14 Ogos + 14 commit 15 Ogos)."))
try:
    g = lari(semak.semak_ringkasan_keadaan)
    jangka("15: ringkasan kiraan commit tidak sepadan 'Sesi Terakhir' -> "
           "'ringkasan kiraan commit' dikesan",
           any("ringkasan kiraan commit" in m for m in g), g)
finally:
    tulis_bytes(MULA, simpan_mula)

# ── 35. Kiraan semakan README lapuk (skop imbas berubah) ────────────
# Kiraan dalam README diturunkan (394 → 391) — semakan 16 mesti
# dikesan. Semak #16 hanya bermakna dalam LARIAN PENUH (ia membaca
# kiraan lulus() seluruh semak.py), jadi mutasi ini menjalankan
# `python semak.py` sebagai subproses (~30s). Rentetan sasaran =
# tuntutan kiraan README SEMASA; bila ia berubah, mutasi ini juga
# perlu diubah (mengunci kedua-duanya).
tulis_bytes(README_MD, ganti_teks(
    simpan_readme,
    "# 394 semakan (15 bahagian) + versi",
    "# 391 semakan (15 bahagian) + versi"))
try:
    k = subprocess.run([sys.executable, "semak.py"], cwd=BASE,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=400)
    jangka("16: kiraan semakan README lapuk -> 'kemas kini README' dikesan",
           "kemas kini README" in k.stdout + k.stderr, k.stdout[-400:])
finally:
    tulis_bytes(README_MD, simpan_readme)

# ── 36. Tarikh Sesi Terakhir mendahului tarikh sistem ───────────────
# Tajuk 'Sesi Terakhir' ditukar ke masa depan (1 Januari 2099) —
# semakan 12 mesti dikesan (rekod dibuka sebelum tarikh sebenar).
# Tarikh jauh dipilih supaya mutasi kekal sah walaupun tarikh sistem
# berjalan (tidak lapuk seperti 'hari esok').
tulis_bytes(MULA, ganti_teks(simpan_mula,
                             "## Sesi Terakhir — 19 Ogos 2026 (5 commit)",
                             "## Sesi Terakhir — 1 Januari 2099"))
try:
    g = lari(semak.semak_sesi_terakhir)
    jangka("12: tarikh Sesi Terakhir mendahului sistem -> "
           "'mendahului tarikh sistem' dikesan",
           any("mendahului tarikh sistem" in m for m in g), g)
finally:
    tulis_bytes(MULA, simpan_mula)

# ═════════════════════════ Sahkan pulihan ══════════════════════════
bersih = (simpan_bytes(UJI) == simpan_uji
          and simpan_bytes(MAN) == simpan_man
          and simpan_bytes(KITAB) == simpan_kitab
          and simpan_bytes(PAGES) == simpan_pages
          and simpan_bytes(UJI_CARIAN) == simpan_carian
          and simpan_bytes(DETAIL) == simpan_detail
          and simpan_bytes(CLOG) == simpan_clog
          and simpan_bytes(PADANAN) == simpan_padan
          and simpan_bytes(APP_QT) == simpan_qt
          and simpan_bytes(LOGO) == simpan_logo
          and simpan_bytes(THEME) == simpan_theme
          and simpan_bytes(TRANS) == simpan_trans
          and simpan_bytes(README_MD) == simpan_readme
          and pd_detail.BACK_PETA == asli_peta
          and pd_detail._warna_cip == asli_warna
          and simpan_bytes(MULA) == simpan_mula
          and not os.path.exists(DUMMY)
          and not os.path.exists(PROBE_PY)
          and not os.path.exists(UJI + ".neg")
          and not os.path.exists(MAN + ".neg")
          and not os.path.exists(UJI_CARIAN + ".neg")
          and not os.path.exists(CLOG + ".neg")
          and not os.path.exists(LOGO + ".neg")
          and not os.path.exists(MULA + ".neg")
          and not os.path.exists(THEME + ".neg")
          and os.path.exists(MULA))
if bersih:
    PASS += 1
    print("  OK    pulihan byte-tepat (8 fail + atribut, kandungan kekal)")
else:
    FAIL += 1
    print("  GAGAL pulihan byte-tepat")

for nama, fn in (("8z", semak.semak_visual_rujukan),
                 ("8w", semak.semak_kitab_shell),
                 ("8x", semak.semak_kad_koleksi),
                 ("8l", semak.semak_carian_sibuk),
                 ("8p", semak.semak_peta_kembali),
                 ("8q", semak.semak_nav_sebelum_seterusnya),
                 ("8r", semak.semak_pemalar_render),
                 ("8m", semak.semak_bahasa_dokumen),
                 ("8k", semak.semak_pemula),
                 ("8v", semak.semak_elide_chip),
                 ("10aa", semak.semak_logo_palet),
                 ("10b", semak.semak_versi_changelog),
                 ("12", semak.semak_sesi_terakhir),
                 ("13", semak.semak_kontras_tema),
                 ("14", semak.semak_rtl_dokumen),
                 ("15", semak.semak_ringkasan_keadaan),
                 ("16", semak.semak_kiraan_readme)):
    g = lari(fn)
    if g:
        FAIL += 1
        print(f"  GAGAL {nama} selepas pulihan masih menanda: {g}")
    else:
        PASS += 1
        print(f"  OK    {nama} hijau selepas pulihan")

print(f"\n  KEPUTUSAN: {PASS} lulus, {FAIL} gagal")
sys.exit(1 if FAIL else 0)
