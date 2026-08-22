# Manual Instalasi — Pustaka Hadis

> Panduan pemasangan, persediaan API, kemas kini, dan nyahpasang.
> Sesuai untuk pengguna akhir. Versi rujukan: **v1.0**.
>
> Cara penggunaan aplikasi: `dokumen/manual/MANUAL_PENGGUNAAN.md`.
> Perbandingan paparan hadis lama → baharu (dengan tangkap layar):
> `dokumen/manual/TRANSFORMASI_DETAIL.md`. Log perubahan harian terbaru
> (13 Ogos): `dokumen/perubahan/PERUBAHAN_13OGOS.md`.

---

## 1. Keperluan sistem

| Perkara | Keperluan |
|---|---|
| Sistem | Windows (7/10/11) |
| Python | 3.10 atau lebih baharu |
| Internet | Perlu untuk muat turun hadis dan masukkan kunci API |
| Ruang cakera | ~164 MB (hadis.db) + ruang untuk model & indeks carian makna (AI) |

**Pasang Python dahulu** jika belum ada:

1. Muat turun dari <https://python.org/downloads>
2. Semasa pasang, **WAJIB tandakan** kotak `[v] Add python.exe to PATH`
3. Selesai

---

## 2. Cara pasang

### Langkah 1 — JALANKAN `PASANG.bat`

```
1.  Klik dua kali    PASANG.bat
    Tunggu sehingga keluar "SIAP", tekan sebarang kekunci.
    (kali pertama ambil 1–3 minit — memasang PyQt5, requests, pyperclip)
```

Langkah ini dibuat **sekali seumur hidup**. Ia:

- Mencari Python dalam komputer
- Memasang keperluan (PyQt5, requests, pyperclip)
- Menyemak semuanya berfungsi
- Mencipta ikon **"Hadis"** di Desktop anda

### Langkah 2 — Buka aplikasi

```
2.  Klik dua kali ikon   Hadis   di Desktop
```

Atau, jika tiada ikon:

- Klik dua kali `JALANKAN.bat` dalam folder ini

Kali pertama dibuka, **skrin pemula (splash)** muncul dengan bar kemajuan
("Memeriksa indeks carian makna…", "Memuatkan model carian makna…" dsb.).
Tunggu sehingga "**Sedia! ✔**", kemudian klik untuk teruskan — model
carian makna sedia digunakan dan carian berjalan lebih laju.

### Langkah 3 — Masukkan kunci API

Buat pertama kali, aplikasi akan meminta kunci API (lihat bahagian 3
di bawah).

> **Ringkasnya:** klik ikon **⚙ gear** (atas kanan) → **Tetapan API** →
> tampal kunci → **Simpan & Uji**. Jika berjaya: `✓ Berjaya — 9 koleksi`.

---

## 3. Dapatkan kunci API hadis.my

Aplikasi menggunakan API percuma **hadis.my** untuk membaca data.
Anda perlu daftar sekali sahaja untuk mendapatkan kunci.

1. Buka <https://hadis.my>
2. Daftar / log masuk (menggunakan Google)
3. Cari bahagian **Developer / API** dan jana kunci API
   (bentuk: `HADIS_XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`)
4. Salin kunci itu

**Kuota percuma:** 200 permintaan sehari, reset setiap 12 malam.
Satu kunci cukup untuk kegunaan biasa membaca hadis.

---

## 4. Cara masukkan kunci API ke dalam aplikasi

1. Buka Pustaka Hadis
2. Klik ikon **⚙ gear** di penjuru atas kanan
3. Klik **Tetapan API** (di bahagian Sambungan panel)
4. Klik **Buka Kunci** pada medan kunci (kunci dipaparkan bertopeng
   untuk keselamatan)
5. Tampal kunci API anda
6. Klik **Simpan & Uji**
7. Status sepatutnya: `✓ Berjaya — 9 koleksi`

Kunci anda disimpan dalam `user_settings.json` dalam folder aplikasi —
tidak dihantar ke mana-mana kecuali hadis.my.

---

## 5. Kemas kini aplikasi

Apabila versi baharu diterima (sebagai `PustakaHadis.zip`):

1. Muat turun ZIP baharu
2. Seret ZIP itu **ke atas** fail `KEMASKINI.bat`
3. Atau jalankan: `KEMASKINI.bat` dengan laluan penuh ZIP
4. Fail lama akan diganti; **data anda (hadis.db, tanda buku,
   tetapan) tidak disentuh**

> **Setiap versi disahkan dahulu sebelum dihantar** — pautan
> "Baca penuh" sunnah.com diaudit terhadap halaman sebenar:
> `python semak.py --audit-sunnah=50` (50 sampel rawak, ~3 minit),
> kemudian `python semak.py` (gate penuh). Hanya versi yang lulus
> **SEMUA LULUS** diedarkan kepada anda. Hasil audit terkini
> (50/50, 11 Ogos 2026): `dokumen/audit/AUDIT_SUNNAH.md`.

---

## 6. Penyelesaian masalah

| Masalah | Penyelesaian |
|---|---|
| Ikon "Hadis" tidak jalan | Klik dua kali `BUAT_PINTASAN.bat` — cuba cipta semula ikon |
| Masih tidak jalan | Klik dua kali `JALANKAN.bat` untuk buka terus |
| Masalah berterusan | Klik dua kali `NYAHPEPIJAT.bat` — tetingkap kekal terbuka, paparkan mesej ralat; salin dan hantar kepada pembangun |
| "Python tidak dijumpai" | Pasang Python dari python.org dan tandakan **Add to PATH** |
| Kunci API ditolak | Semak kunci anda di hadis.my; semak kuota (200/hari) — reset 12 malam |
| Sambungan gagal | Periksa internet; semak ejaan kunci |

---

## 7. Nyahpasang

Klik dua kali `BUANG.bat`. Ia akan bertanya:

1. **Buang data anda?** (hadis.db, tetapan, tanda buku) — tekan `Y`
   jika mahu buang semua, atau `ENTER` untuk simpan
2. **Tanggal PyQt5 dari Python?** — `Y` hanya jika tiada program lain
   guna PyQt5 (disarankan `ENTER` untuk simpan)
3. Taip **BUANG** untuk sahkan

Selepas selesai, padam folder aplikasi secara manual.

---

## 8. Privasi

- Semua data hadis disimpan **secara tempatan**
- Kunci API dihantar hanya ke `service.hadis.my`
- Tiada pengumpulan data, tiada iklan, tiada pelacakan
- Aplikasi ini bukan aplikasi rasmi hadis.my; kandungan hadis dan
  terjemahan ialah hak milik sumber masing-masing

---

## 9. Kandungan ZIP edaran (senarai rasmi)

`PustakaHadis.zip` (v1.0, 13 Ogos 2026) mengandungi **120 fail**
(dibina daripada `git ls-files`, tolak folder dev dan data):

| Bahagian | Bilangan | Peranan |
|---|---|---|
| Akar — pelancar, semak, ujian | 51 | `main.py`, `launcher.py`, `config.py`, `db.py`, `VERSI.py`, `requirements.txt`, `app.ico`, `.env.example`, skrip `*.bat`/`*.ps1`, `semak*.py`, `audit_eng.py`, `diagnos_*.py`, `profil_semak.py`, `bina_tangkapan_dokumentasi.py`, 15 ujian `uji_*.py`, dokumen akar |
| `api/` | 2 | `hadis_api.py` — API hadis.my |
| `core/` | 9 | Logik teras: carian semantik, draf jawapan AI, transliterasi, terjemahan, sumber SemakHadis/syarah/HadeethEnc |
| `ui/` | 16 | Antara muka PyQt5 (halaman, widget, tema, pekerja) |
| `utils/` | 3 | Bantuan: bahasa, transliterasi |
| `scripts/` | 3 | Alat dev: bina logo, bina indeks carian makna, muat turun huraian |
| `dokumen/` | 46 | Manual (5), log perubahan (7), rujukan (10), sesi (1), audit (4), imej tangkap layar (19) |

**Senarai penuh fail (130):**

```
# Akar — pelancar & skrip utama (51)
.env.example          .gitignore            BACA_SAYA.txt
BUANG.bat             BUANG.ps1             BUAT_PINTASAN.bat
JALANKAN.bat          KEMASKINI.bat         NYAHPEPIJAT.bat
PASANG.bat            PINDAH_DATA.ps1       README.md
VERSI.py              app.ico               audit_eng.py
bina_tangkapan_dokumentasi.py               config.py
db.py                 diagnos_padanan.py    diagnos_syarah.py
launcher.py           main.py               pintasan.ps1
profil_semak.py       requirements.txt      semak.py
semak_db.py           semak_kunci.py        semak_versi.py
sync.py               sync_english.py       sync_hadeethenc.py
sync_sema.py          sync_syarah.py
uji_bandingan.py      uji_data_baharu.py    uji_draf_jawapan.py
uji_end_to_end.py     uji_lompat.py         uji_lompat_fungsi.py
uji_negatif_8z.py     uji_pra_hantar.py     uji_splash.py
uji_tukar_tema.py     uji_visual_bantuan.py uji_visual_carian.py
uji_visual_kiraan.py  uji_visual_mockup.py  uji_visual_piksel.py
uji_visual_ralat.py   uji_visual_sebenar.py

# API hadis.my (2)
api/__init__.py   api/hadis_api.py

# Logik teras (9)
core/__init__.py               core/draft_answer.py
core/eng_source.py             core/hadeethenc_api.py
core/phase2_transliterasi.py   core/phase3_translate.py
core/sema_source.py            core/semantic_search.py
core/syarah_source.py

# Antara muka PyQt5 (16)
ui/__init__.py   ui/app_qt.py   ui/deklarasi.py   ui/helpers.py
ui/pages.py      ui/pages_carian.py   ui/pages_detail.py
ui/pages_home.py ui/pages_kitab.py    ui/pages_tersimpan.py
ui/pages_tetapan.py  ui/settings_panel.py  ui/splash.py
ui/theme.py      ui/widgets.py   ui/workers.py

# Bantuan (3)
utils/__init__.py   utils/bahasa.py   utils/transliteration.py

# Alat dev (3)
scripts/bina_logo.py   scripts/build_faiss_index.py
scripts/muat_turun_sema.py

# Dokumen (36)
dokumen/manual/MANUAL_INSTALASI.md
  dokumen/manual/MANUAL_PENGGUNAAN.md
  dokumen/manual/MANUAL_REFERENSI_DEV.md
  dokumen/manual/MULA_SINI.md
  dokumen/manual/TRANSFORMASI_DETAIL.md
dokumen/perubahan/CHANGELOG.md
  dokumen/perubahan/PERUBAHAN_30JUL.md
  dokumen/perubahan/PERUBAHAN_31JUL.md
  dokumen/perubahan/PERUBAHAN_7OGOS.md
  dokumen/perubahan/PERUBAHAN_11OGOS.md
  dokumen/perubahan/PERUBAHAN_12OGOS.md
  dokumen/perubahan/PERUBAHAN_13OGOS.md
dokumen/rujukan/ANALISA_6OGOS.md
  dokumen/rujukan/DEKLARASI.md
  dokumen/rujukan/INSTALLER.md
  dokumen/rujukan/ISU_TERJEMAHAN_MELAYU.md
  dokumen/rujukan/PANDANGAN_RISIKO.md
  dokumen/rujukan/PERMOHONAN_LESEN_SEMAKHADIS.md
  dokumen/rujukan/RANCANGAN_4FASA.md
  dokumen/rujukan/RANCANGAN_REFACTOR.md
  dokumen/rujukan/REVOKE_KUNCI.md
  dokumen/rujukan/SUMBER_hadis-my.md
dokumen/sesi/sesi_index.md
dokumen/audit/AUDIT_SUNNAH.md
  dokumen/audit/DAPATAN_WEB.md
  dokumen/audit/DORAR_NET.md
  dokumen/audit/PADANAN_ARKIB.md
dokumen/imej/baru_detail_gelap_bukhari1.png
  dokumen/imej/baru_detail_gelap_nasai4934.png
  dokumen/imej/baru_detail_gelap_skrol_nasai2117.png
  dokumen/imej/baru_detail_terang_cip_amber_ibnumajah2094.png
  dokumen/imej/baru_detail_terang_cip_hijau_nasai2117.png
  dokumen/imej/baru_detail_terang_cip_merah_abudaud4177.png
  dokumen/imej/baru_detail_terang_nasai4934.png
  dokumen/imej/lama_detail_gelap_nasai4934.png
  dokumen/imej/lama_detail_terang_nasai4934.png
  dokumen/imej/tema_home_neutral.png
  dokumen/imej/tema_home_kertas.png
  dokumen/imej/tema_home_neutral_terang.png
  dokumen/imej/tema_home_terang.png
  dokumen/imej/tema_home_sistem.png
  dokumen/imej/tema_detail_neutral.png
  dokumen/imej/tema_detail_kertas.png
  dokumen/imej/tema_detail_neutral_terang.png
  dokumen/imej/tema_detail_terang.png
  dokumen/imej/tema_detail_sistem.png
```

> **TIDAK dibundel dalam ZIP** (dicipta/diisi semasa penggunaan):
> `hadis.db` (+ `-wal`/`-shm`), `hadis_faiss.index`, `hadis_id_map.pkl`,
> `sunnah_map/`, `bookmarks.json`, `user_settings.json`, `profil_model.json`,
> `.env`, `.env.local`, `kunci_terdedah.txt`, `.cache_*`, `__pycache__/`,
> kunci API, dan mockup HTML pembangunan (`mockup/`). Folder dev
> (`_arkib/`, `bukti_visual/`, `.agents/`, `.opencode/`, `.freebuff/`)
> dan fail konfigurasi AI (`opencode.json`) tidak masuk ZIP.

---

## 10. Pengesahan edaran

Setiap `PustakaHadis.zip` disahkan sebelum dihantar, termasuk ujian
dari folder bernama dengan ruang (13 Ogos 2026):

1. `python semak_versi.py` — semua 23 ciri v1.0 hadir
2. `python semak.py` — **SEMUA LULUS** (0 GAGAL)
3. App `ui.app_qt` melancar (VERSI 1.0)

Jika anda mahu menyemak sendiri selepas ekstrak: jalankan `python
semak_versi.py` kemudian `python semak.py` dalam folder aplikasi.
