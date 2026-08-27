# Manual Rujukan Developer — Pustaka Hadith

> **Satu dokumen rujukan utama.** Meringkaskan segala keputusan, aliran
> modul, senarai semak, dan status. Guna dokumen ini sebagai titik mula
> untuk sebarang sesi pembangunan; baca `dokumen/manual/MULA_SINI.md` untuk peraturan
> keras dan `dokumen/sesi/sesi_index.md` untuk arkib penuh.
>
> Versi: **v1.0** (11 Ogos 2026)

---

## 1. Keadaan workspace

| Perkara | Nilai |
|---|---|
| Nama | Pustaka Hadith — koleksi 9 kitab hadis |
| Root | `D:\Pustaka Quran Hadis\hadis\` — **workspace Developer** |
| Status | **BUKAN untuk pengguna akhir lagi** — semakan developer belum selesai |
| Versi | v1.0 (`VERSI.py`) |
| ZIP | `PustakaHadis.zip` (arkib pembangunan; bukan pakej edaran) |
| Tech | Python 3.14 + PyQt5 (Qt 5.15.2) · requests · pyperclip |
| UI | Bahasa Melayu (loghat Malaysia) |
| API | `https://service.hadis.my/api/v1` (X-API-Key) |
| DB | `hadis.db` SQLite — 62,169 hadis, ~164 MB (138 MB selepas VACUUM) |

**Keputusan pengguna 31 Jul (selepas ZIP dibina):** folder `hadis/`
ialah workspace Developer. Banyak penambahbaikan tertangguh akan
dilakukan apabila developer menjalankan app untuk semakan. Manual
pengguna akhir: `dokumen/manual/manual/manual/MANUAL_INSTALASI.md` (pemasangan) + `dokumen/manual/manual/manual/MANUAL_PENGGUNAAN.md` (cara guna).

---

## 2. Struktur fail

```
hadis/
├── main.py                 # Entry point PyQt5
├── config.py               # API key/URL, default, pemuat kunci
├── db.py                   # Schema SQLite, SKEMA_VERSI, migrasi
├── VERSI.py                # Versi + senarai CIRI (semak_versi.py)
├── requirements.txt        # PyQt5, requests, pyperclip
│
├── api/
│   ├── hadis_api.py        # Lapisan API + rate limit
├── core/
│   ├── phase1_extract.py   # Ekstrak arab+ms+id (API)
│   ├── phase2_transliterasi.py
│   ├── phase3_translate.py # (placeholder — selesai via sync_english)
│   ├── sema_source.py      # SemakHadis: padanan matn + huraian BM (aktif)
│   ├── syarah_source.py    # Fath al-Bari (Fasa 4B — dibatalkan)
│   ├── hadeethenc_api.py   # HadeethEnc cache + padanan matn (arsip)
│   └── padan.py            # 5-lapisan padanan (JANGAN susun semula)
├── ui/
│   ├── app_qt.py           # Inti PustakaApp (504 baris — Sesi 30 refactor)
│   ├── helpers.py          # Fungsi bebas tanpa state Qt (Sesi 30)
│   ├── pages.py            # Hero, SearchBar, KitabCard, Pager, LangTabs
│   ├── widgets.py          # ClickCard, hadith_card, FilterChips, Toast
│   ├── theme.py            # Palet terang/gelap, QSS, _THEMED_MODULES
│   ├── settings_panel.py   # Panel gelongsor (Tema, Saiz, Sambungan)
│   ├── workers.py          # QThread workers
│   ├── pages_kitab.py      # Mixin PagesKitab (Sesi 30)
│   ├── pages_carian.py     # Mixin PagesCarian (Sesi 30)
│   ├── pages_detail.py     # Mixin PagesDetail (Sesi 30)
│   ├── pages_tersimpan.py  # Mixin PagesTersimpan (Sesi 30)
│   ├── pages_tetapan.py    # Mixin PagesTetapan (Sesi 30)
│   └── pages_home.py       # Mixin PagesHome (Sesi 30)
├── utils/
│   ├── transliteration.py  # Arab → Rumi
│   ├── bahasa.py           # betulkan_melayu, simbol_boleh_dipapar
│   └── ...
│
├── *.py                    # Skrip utiliti (lihat §7)
├── *.bat / *.ps1           # Pemasangan, kemaskini, nyahpasang (CRLF!)
├── hadis.db                # 62,169 hadis — dijana, tidak dibundel
├── user_settings.json      # Tetapan + kunci API (tidak dalam ZIP arkib)
├── bookmarks.json          # Tanda buku pengguna (tidak dalam ZIP arkib)
├── .env                    # HADIS_API_KEY (tidak dalam ZIP arkib)
├── .cache_eng/ .cache_he/ .cache_syarah/   # cache muat turun
└── *.md                    # Dokumentasi (lihat §12)
```

---

## 3. Status fasa

| Fasa | Fungsi | Status |
|---|---|---|
| 1 | Ekstrak Arab + Melayu + Indonesia | ✅ SIAP (100%) |
| 2 | Transliterasi Arab → Rumi | ✅ SIAP + Collapsible di UI |
| 3 | Terjemahan Inggeris | ✅ SIAP — 31,833 terjemahan (98%), diaudit |
| 4 | Huraian auto (HadeethEnc + nota topik) | ⚫ DIBUANG 3 Ogos 2026 (Sesi 18.9) — kekeliruan dengan SemakHadis |
| 4A | Huraian Irsyad al-Hadith | ⚫ DITUTUP 31 Jul — lesen "Hak Cipta Terpelihara" |
| 4B | Huraian Fath al-Bari | ⚫ DIBATALKAN buat sementara — penomboran hanyut |

**Lapisan huraian dalam UI (selepas Sesi 18.9):**
1. **SemakHadis** (Collapsible "Huraian (SemakHadis · status)") — 4,237 padanan,
   tajuk + status + terjemahan + takhrij + komentar, atribusi "Sumber: SemakHadis.com"
2. **Syarah klasik Arab** + **darjat** — sumber asal
3. Huraian auto Fasa 4 (status `auto`/`dari_sumber` + `phase4_exegesis.py`)
   **DIBUANG** — UI tidak lagi memaparkan nota topik generik. Data HadeethEnc
   (jadual `hadethenc`, `.cache_he/`, `sync_hadeethenc.py`) kekal sebagai arsip.

---

## 4. Fakta API hadis.my

```
Base    : https://service.hadis.my/api/v1
Header  : X-API-Key
Kuota   : Basic 200/hari · Developer 10,000/hari   Reset 12AM MY
Throttle: 1.1s  →  622 permintaan ≈ 12 minit
```

- `/hadis/search` → `data.results` (BUKAN `data.hadis`)
- Senarai guna `per_page` (maks 100), bukan `limit`
- `meta` di **top-level**, bukan dalam `data`
- `lang=ms|id` sahaja; nilai lain diabaikan senyap
- **Enumerasi mesti guna `language=en`** — `ms` mengubah paginasi
  (senarai dan `one` pakai logik berbeza → 404 palsu). Butiran §2
  `dokumen/perubahan/PERUBAHAN_31JUL.md`.
- Slug (9): `bukhari muslim abu-daud tirmidzi nasai ibnu-majah ahmad darimi malik`
- Kunci format: `HADIS_XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` (`config.valid_key_format`)
- Keutamaan kunci: env `HADIS_API_KEY` → `.env` → `user_settings.json`
- **JANGAN** tulis kunci sebenar dalam `config.py` atau dokumen

---

## 5. hadis.db

```
62,169 hadis · ~164 MB (138 MB selepas VACUUM)
FTS5 index — carian 0.03 ms
journal_mode = WAL — KEKALKAN (2x lebih laju baca-sambil-tulis)
SKEMA_VERSI dalam db.py; migrasi automatik dalam init()
```

- Fail `-wal`/`-shm` bukan sampah — jangan tukar ke DELETE
- Tambah jadual baharu? Naikkan `SKEMA_VERSI` + tambah ke `MIGRASI`
- Migrasi mesti kekalkan data pengguna (favorit, tetapan) — semak #6
  dalam `semak.py`
- `sync.py` (Fasa 1): ambil semua 62,169 hadis dari API
- `sync_english.py` (Fasa 3): ~31,833 tersimpan, 98%
- `sync_hadeethenc.py` (Fasa 4): arsip — tidak dipapar UI (huraian auto dibuang)
- `sync_syarah.py` (Fasa 4B): selamat dijalankan — ia batal sendiri

---

## 6. Padanan — peraturan yang JANGAN dilanggar

### Fasa 3 (English) — kunci padanan ialah INDONESIA, bukan Arab

```
hadis.my (indonesia) --padan--> ind-* --nombor sama--> eng-*
hadis.my (arab)      --sandaran--> ara-*    (bila indonesia tiada)
```

Turutan 5 lapisan (`core/padan.py`) — JANGAN susun semula:

| # | kaedah | kunci | ambang |
|---|---|---|---|
| 1 | `indo` | teks Indonesia dinormalisasi | tepat |
| 2 | `indo~` | token Indonesia | JACCARD_IND 0.95 |
| 3 | `penuh` | teks Arab penuh | tepat |
| 4 | `awalan` | 200 aksara Arab | mesti UNIK |
| 5 | `kata` | token Arab jarang | JACCARD_MIN 0.90 dua hala |

- **JANGAN** buang pengesahan dua hala pada `kata` — 35.3% positif palsu
- **JANGAN** `INSERT OR REPLACE` sahaja — `DELETE` per-kitab dahulu
- 7 kitab ada; `ahmad` & `darimi` TIADA di CDN
- Audit mesti guna bukti BEBAS: `audit_eng.py` (bukan `diagnos_padanan.py`)

### Huraian auto (Fasa 4) — DIBUANG 3 Ogos 2026

- **Keputusan pengguna (Sesi 18.9):** huraian auto (HadeethEnc + nota topik
  generik `auto`) dibuang SEPENUHNYA daripada UI — bertumpuk dan mengelirukan
  berbanding huraian asli SemakHadis. `core/phase4_exegesis.py`,
  `ui/workers.PipelineWorker`, butang "📖 Huraian" dan halaman pipeline
  dibuang. JANGAN hidupkan semula tanpa sebab baharu.
- Data HadeethEnc (jadual `hadethenc`, `.cache_he/`, `sync_hadeethenc.py`)
  kekal sebagai **arsip** — tidak dipapar UI.
- `core/hadeethenc_api.py` KEKAL — `_matn` masih dipakai `core/sema_source`.
- Padanan lama HadeethEnc: matn sahaja (sanad ditanggalkan), Jaccard 0.55.

### Fasa 4B (Fath al-Bari) — DIBATALKAN

- Penanda `# N` BUKAN nombor hadis Bukhari — kiraan berjujukan yang
  hanyut progresif (-0, -32, -120, -320)
- **JANGAN** simpan syarah ikut padanan ID · **JANGAN** percaya sampel
  hujung julat (76% → 13% sebenar)

### Fasa 4A (Irsyad) — DITUTUP

- Lesen TERTUTUP ("Hak Cipta Terpelihara © 2024 JMWP")
- **JANGAN guna, jangan simpan.** Tiada sumber BM lain sah
  (jadual penuh: `dokumen/perubahan/PERUBAHAN_31JUL.md` §13)

---

## 7. Skrip utiliti

| Skrip | Fungsi |
|---|---|
| `semak.py` | 10+ semakan pra-hantar. Keluar 0 = selamat hantar |
| `semak_versi.py` | Sahkan versi + semua CIRI wujud |
| `semak_kunci.py` | Uji kunci API terhadap pelayan |
| `semak_db.py` | Semak integriti hadis.db |
| `audit_eng.py` | Audit terjemahan Inggeris dengan bukti bebas |
| `diagnos_padanan.py` | Diagnos padanan Arab (bukti tidak bebas) |
| `diagnos_syarah.py` | Diagnos padanan syarah (belum dijalankan pada data sebenar) |
| `sync.py` | Fasa 1: muat turun 62,169 hadis |
| `sync_english.py` | Fasa 3: padan + simpan terjemahan Inggeris |
| `sync_hadeethenc.py` | Fasa 4: arsip HadeethEnc (tidak dipapar UI) |
| `sync_syarah.py` | Fasa 4B: batal sendiri (jangan dibuka semula) |
| `sync_sema.py` | SemakHadis: 4,237 padanan matn + huraian BM |

### .bat (semua WAJIB CRLF — rujuk peraturan #5)

| Fail | Fungsi |
|---|---|
| `PASANG.bat` | Cari Python → pip install → sahkan → cipta pintasan |
| `JALANKAN.bat` | Pelancar sandaran (pythonw main.py) |
| `BUAT_PINTASAN.bat` | Cipta semula ikon "Hadis" |
| `NYAHPEPIJAT.bat` | Diagnos: versi, modul, fail, cuba jalankan (kekal buka) |
| `KEMASKINI.bat` | Ekstrak ZIP dengan `-Force` (seret ZIP ke atasnya) |
| `BUANG.bat` | Nyahpasang: pintasan + pilihan data + pilihan PyQt5 |
| `pintasan.ps1` | Logik cipta pintasan (dipanggil PASANG) |
| `PINDAH_DATA.ps1` | Pindah data antara lokasi |

---

## 8. Penambahbaikan tertangguh (selepas semakan app)

Semua ini akan dilakukan apabila developer **menjalankan app untuk
semakan**. Belum selesai / belum disahkan:

1. **Ujian mesin sebenar** — ✅ **DITUTUP 14 Ogos 2026** — suite
   pra-hantar 11 ujian dijalankan pada mesin sebenar, SEMUA LULUS
   (termasuk uji_visual_sebenar 68/0 dengan tetingkap fizikal)
2. **Sync penuh** — ✅ **DITUTUP 14 Ogos 2026** — `sync.py --paksa`
   dijalankan pada mesin sebenar, semua 9 kitab 100% (622 muka
   surat, 12.5 min, 639 permintaan); "Rekod baharu: 0" = data API
   sepadan tepat dengan DB sedia ada; pengesahan: 62,169 unik, 0
   duplikat, 0 teks kosong, julat id kontigu, FTS 62,169 = 62,169,
   perbandingan teks API vs DB 45/45 padan
3. **Padanan `ara-*`** — ✅ **DITUTUP 14 Ogos 2026** — pengesahan
   PENUH pada hadis.db sebenar (32,439 hadis, 7 kitab): 31,952
   padan (98.5%), lapisan Arab (penuh 877 + awalan 235 + kata 516 =
   1,628, 5.1%) mengisi celah Indonesia; 0 entri basi; audit bebas
   30,541/30,547 (100.0%, 6 disyaki = positif palsu saksi ind-*
   hanyut, sama seperti 31 Jul); sync_english.py dari mula =
   31,833 deterministik (gagal 487 padan rekod Fasa 3)
4. **Halaman Tersimpan** — ✅ **DITUTUP 14 Ogos 2026** —
   `uji_tersimpan_sebenar.py` 20/0: simpan 3 hadis sebenar (3 kitab),
   tulis cakera, restart → kekal, buka dari Tersimpan, tanggalkan,
   pulihkan; daftar ujian #12 dalam uji_pra_hantar.py
5. **`diagnos_syarah.py`** — ✅ **DITUTUP 14 Ogos 2026** — dijalankan
   pada hadis.db sebenar (7,008 Bukhari + 5,075 seksyen Fath al-Bari):
   penomboran **HANYUT** (julat 520, 1/8 sejajar) — padanan ikut ID
   tidak selamat, Fasa 4B kekal dibatalkan
6. **Pipelin semakan end-to-end** — ✅ **DITUTUP 14 Ogos 2026** —
   `uji_pipeline_api.py` 18/0: install (kebergantungan OK) → API HIDUP
   (kunci developer, use_db=False) → baca → tersimpan
7. **Kunci API** — kekal AKTIF sengaja (pelan developer); guna semula:
   `dokumen/rujukan/REVOKE_KUNCI.md`
8. **Liputan SemakHadis** — 4,237/62,169 (6.8%) hadis popular sahaja;
   siling tetap selagi tiada sumber BM terbuka lain. **AUDIT PENUH
   14 Ogos 2026** (`dokumen/audit/AUDIT_SEMAKHADIS.md`): tirmidzi
   1.6% terendah → bukhari 10.2%; 103/393 bab (26%) liputan 0%;
   jurang terbesar Tafsir (843), Hajj (~1,564), Solat (~1,371);
   keutamaan sumber baharu: tafsir per-hadis → syarah ibadah →
   khusus Tirmidzi → Musnad Ahmad

---

## 8A. Pandangan & risiko (tambah Sesi 29, 7–8 Ogos 2026)

Hasil analisis keseluruhan projek. Bukan senarai tugasan wajib — konteks
untuk sesi akan datang supaya keputusan diambil sedar risiko.

### 1. `ui/app_qt.py` terlalu besar (~100 KB / 2,428 baris)

Setiap ciri baharu ditambah ke satu fail yang terus membesar. Risiko:
- Sukar dibaca/diurus; konflik edit meningkat
- Peraturan MULA_SINI #4 ("jangan buang import 'unused' dalam `ui/*.py` —
  ia sasaran `apply_theme()`") menjadikan refactor berisiko

Cadangan: pecah halaman search/detail/kitab ke modul berasingan (corak
`ui/pages.py` sudah ada). Lakukan SELEPAS ujian mesin sebenar, bukan kini.

**✅ SELESAI 8 Ogos 2026 (Sesi 30):** refactor 5 langkah selesai —
`ui/helpers.py` + 6 mixin halaman; `app_qt.py` 2,428 → 504 baris inti.
Rujuk `dokumen/rujukan/RANCANGAN_REFACTOR.md` + sesi_index Sesi 30.

### 2. Salinan `app_qt.py` dalam folder arkib/sandaran

Wujud di `sandaran_1300/`, `sandaran_1302/`, `tampalan_preload/`.
Risiko: tersilap edit salinan lama dan menganggap ia kod aktif.

Pengawal: semak.py mengimport daripada `ui/app_qt.py` (aktif). Semua
salinan arkib dalam `.gitignore`? Perlu sahkan — jika terjejak, padam.

### 3. Dokumentasi ketinggalan versi

- `dokumen/manual/MANUAL_REFERENSI_DEV.md` masih "v1.0", `dokumen/manual/MULA_SINI.md` kini v1.3
- `dokumen/sesi/sesi_index.md` kini lengkap hingga Sesi 29 (dikemas)

Cadangan: kemas kini `dokumen/manual/MANUAL_REFERENSI_DEV.md` §1 (versi) + peta dokumen §12
apabila menutup sesi, supaya tiada dokumen bercanggah.

**✅ DITUTUP 8 Ogos 2026 (Sesi 30):** `dokumen/manual/MANUAL_REFERENSI_DEV.md` v1.3,
`dokumen/sesi/sesi_index.md` lengkap hingga Sesi 30, peta dokumen §12 kini termasuk
`dokumen/rujukan/RANCANGAN_REFACTOR.md`.

### 4. Skrip ujian: crash 0xC0000409 palsu daripada pengekodan emoji

Penyiasatan Sesi 29 membuktikan crash `EXIT=-1073740791` (0xC0000409)
dalam skrip ujian `uji_cari_*.py` ialah fail-fast daripada `print()` emoji
(🤖 dalam `search_info.text()`) ke stdout cp1252 dalam gelung acara Qt —
BUKAN bug aplikasi (QThread/torch/pra-muat). try/except tidak menangkapnya.

Risiko berulang: crash disalah anggap sebagai bug sebenar dan menghabiskan
masa siasatan. Pengawal: semua skrip ujian baharu MESTI set
`sys.stdout.reconfigure(encoding="utf-8")` atau `PYTHONIOENCODING=utf-8`.

### 5. Lesen SemakHadis belum disahkan bertulis

SemakHadis.com tidak menyatakan lesen semula data secara eksplisit
(direkod sejak Sesi 18.8). Atribusi dipaparkan. Risiko: isu hak cipta
sebelum edaran komersial. Tindakan: dapatkan kebenaran bertulis sebelum
pengedaran komersial.

### 6. Kunci API kekal AKTIF dalam repo

Sengaja (keputusan pengguna 31 Jul, pelan developer). Risiko penyalahgunaan
kuota. Pengawal: `dokumen/rujukan/REVOKE_KUNCI.md` — jangan masukkan kunci baru ke kod.

### 7. SemakHadis liputan terhad (3.3%)

4,237/62,169 hadis popular sahaja. Siling tetap selagi tiada sumber BM
terbuka lain yang sah (Fasa 4A ditutup atas lesen).

---

## 9. Senarai semak sebelum hantar

**Satu arahan:** `python semak.py`

**Pra-hantar penuh (Sesi 50):** `python semak.py --audit-sunnah=50`
mengaudit pautan "Baca penuh" sunnah.com terhadap halaman sebenar
(50 sampel rawak, ~3 minit), kemudian `python semak.py` untuk gate
penuh. Hanya lulus SEMUA LULUS yang dihantar.

**Ujian negatif 8z (Sesi 54+55, +semakan 12 pada 14 Ogos):**
`python uji_negatif_8z.py` — selepas `semak.py` lulus, sahkan semakan
8z/8w/8x/8l/8p/8q/8r/8m/8k/8v/10aa/10b/12 benar-benar mengesan
cabang GAGAL (cth. fail ujian dibuang, fail baharu luar senarai, kata
Indonesia disuntik ke PADANAN_ARKIB.md, manual hilang, senarai semak
dikosongkan, sambungan/kaedah pramuat 8k dibuang atau
`_pra_muat_model` dipulangkan, `_warna_cip` semua MERAH/None, logo
TEAL biru, bina_logo hilang, tarikh 'Sesi Terakhir' MULA_SINI.md
ketinggalan git log / hash disebut tidak wujud / MULA_SINI.md hilang /
tarikh kerja dibuang dari teks ringkasan, kontras tema jatuh bawah AA
[#707070], susun atur RTL lama dibenamkan semula dalam dokumen
[#32: "Arab di kiri" dalam TRANSFORMASI_DETAIL, #33: dalam README],
ringkasan satu muka ketinggalan 'Sesi Terakhir' [#34: kiraan commit
dalam ringkasan diturunkan]); sasaran 0 gagal (52 lulus, 34 cabang).
Semakan #15 `semak_ringkasan_keadaan` mengunci ringkasan satu muka
'Keadaan projek' (atas MULA_SINI) seiring 'Sesi Terakhir': tajuk
bertarikh sama + kiraan commit sama — ringkasan ialah perkara pertama
dibaca sesi AI baharu, tidak boleh ketinggalan seperti 'Sesi Terakhir'
(semak #12). Skrip memulihkan
fail byte-tepat — tiada fail tercemar;
tiada tetingkap dibuka (bukan ujian visual).

**Ujian pra-hantar automatik (Sesi 55, 14 ujian setakat 18 Ogos):**
`python uji_pra_hantar.py` — selesaikan suite PENUH dengan satu arahan:
semak.py → uji_negatif_8z → uji_visual_mockup → uji_visual_piksel →
uji_visual_sebenar → uji_tukar_tema → uji_bandingan → uji_lompat_fungsi
→ uji_end_to_end → bina_tangkapan_dokumentasi (regresi tangkapan
dokumen) → uji_draf_jawapan (draf AI: exact_results + bahagian "Carian
Biasa (Keyword)") → uji_tersimpan_sebenar (tanda buku sebenar, ujian
#12, ditambah 14 Ogos) → semak_dokumen_ui (audit dokumen manual vs UI
sebenar, 110/0, ujian #13, digate 14 Ogos) → uji_responsif_viewport
(responsif viewport 6 halaman × 4 saiz, ujian #14, ditambah 18 Ogos).
Berhenti awal bila gagal (`--teruskan` untuk jalankan semua); log
setiap ujian ke `bukti_visual/pra_hantar_*.log`; sasaran SEMUA LULUS.
Nota: ujian skrin sebenar (sebenar/mockup) mesti dapat fokus tetingkap
dalam subproses — `_paksa_hadapan` guna HWND_TOPMOST untuk atasi
foreground-lock Windows.

**Pembersihan proses yatim (14 Ogos):** bila induk suite dibunuh (tool
timeout dsb.), subproses ujian Windows terus hidup (~1 GB setiap satu —
model AI dimuat) dan memperlahankan larian seterusnya sehingga "hang"
di Loading weights. `_cari_orphan()` menyenaraikan proses sedemikian:
skrip UJIAN projek dalam BASE (`uji_*`, `semak.py`, `semak_dokumen_ui`,
`bina_tangkapan_dokumentasi`, `profil_semak`) — **BUKAN** `main.py`/
`sync.py` (app/tugas pengguna) dan BUKAN proses semasa; psutil pilihan
(tiada psutil → langkau). `_bersihkan_orphan()` membunuhnya dan
dijalankan automatik pada permulaan suite; `python uji_pra_hantar.py
--bersihkan` memanggilnya sahaja (alat penyelenggaraan). **Pengesahan
dua hala**: selepas suite, `_semak_orphan_selepas()` mengesahkan TIADA
proses yatim tinggal — jika ada, suite GAGAL (ujian tidak memulihkan
keadaan / subproses menggantung terselamat timeout).

**Gate pantas harian (14 Ogos):** `python gate_pantas.py` — semakan
pantas (~35s) sebelum setiap commit kecil: (0) pokok kerja bersih
(amaran jika belum di-commit), (1) `semak.py`, (2) `uji_negatif_8z`.
Bukan pengganti suite penuh `uji_pra_hantar.py` (14 ujian) — itu untuk
hantar besar.

**Profil masa semak.py (Sesi 55):** `python profil_semak.py` — ukur
tempoh SETIAP fungsi semakan (kenal pasti regresi prestasi); `--penuh`
sertakan audit sunnah. Tidak mengubah apa-apa.

**Semakan dokumen manual vs UI (14 Ogos 2026):** `python
semak_dokumen_ui.py` — offscreen, 74 semakan. Mengesahkan SETIAP
tuntutan `dokumen/manual/MULA_CEPAT.md` + `manual/manual/MANUAL_PENGGUNAAN.md`
terhadap UI sebenar: angka data dari hadis.db (62,169 · 9 kitab ·
31,833 english · 4,237 SemakHadis · 63,930 darjat · English 7 kitab
sahaja), nav + gear, skrin utama, halaman kitab (pager, kotak Lompat,
Ctrl+G, backTop, 20/halaman), halaman hadis (butang tajuk, tab
ARAB/TRANSLITERASI + 3 bahasa, **dua lajur geometri**, bar `Lapor
ralat | Kongsi | Salin` teks, menu Salin 3 pilihan, klik kanan "Salin
semua", huraian SemakHadis/HadeethEnc, darjat, cip warna ikut makna),
carian (format lompat, 2 enjin, draf AI, jam berputar, notis longgar),
Tersimpan, panel Tetapan (5 bahagian + 8 label), splash, deklarasi
"Faham", 4 fail .bat, Python 3.14, suite 14 ujian. Tidak mengubah
apa-apa (bookmarks.json tidak disentuh); digate sebagai ujian #13
dalam uji_pra_hantar.py (14 Ogos).

**Ujian visual skrin (Sesi 54):** jalankan selepas `semak.py` lulus,
pada skrin fizikal (bukan offscreen) — sasaran 0 gagal setiap satu,
tangkapan dalam `bukti_visual/`:

- `python uji_visual_kiraan.py` — output `_label_kiraan`: kad koleksi
  (`7,008 Hadis` + fallback `— Hadis`) + banner kitab (`7,008 hadis`,
  kotak lompat `0–7008`) — 18 semakan.
- `python uji_visual_mockup.py` — kontrak mockup Sesi 55 vs halaman
  detail PyQt5 (bukhari#1/nasai#2117/abu-daud#4177): susun atur dua
  lajur, tab per lajur (ARAB/TRANSLITERASI + MELAYU/INDONESIA/ENGLISH),
  huraian + darjat TERBUKA, cip, penafian, bar bawah — 60 semakan.
  Fail mockup: `mockup/` (sumber kebenaran kontrak).
- `python uji_visual_piksel.py` — perbandingan PIKSE L app vs palet
  mockup Sesi 55: histogram chi-square + kehadiran warna teras (latar,
  kad, aksen hijau, cip ikut kes) + kepekaan mutasi (regresi palet biru
  mesti dikesan) — 53 semakan, 4 hadis × 2 tema.
- `python uji_visual_sebenar.py` — sandaran HadeethEnc, selawat ﷺ,
  saiz fon lalai, butang ↑ + kotak nombor — 65 semakan.
- `python uji_visual_bantuan.py` — fallback carian OR + mesej bantuan,
  kedua-dua tema — 33 semakan.
- `python uji_visual_carian.py` — jam berputar semasa carian (12 semakan).
- `python uji_bandingan.py` — tab bahasa 3 sahaja (mockup Sesi 55) +
  teks terjemahan sama paras dengan Arab (offscreen).
- `python uji_visual_ralat.py` — toast ralat diterjemah ke Melayu
  (4 semakan).
- `python uji_lompat.py` — parser 'lompat ke hadis' sahaja (ejaan
  kitab & format: `bukhari 433`, `B433`, `b:433`) — 67 semakan,
  offscreen, pantas. Versi penuh (parser + halaman + skrol + buka
  butiran) ialah `uji_lompat_fungsi.py` dalam suite pra-hantar.
- `python uji_data_baharu.py` — data baharu dalam UI (bab/darjat/
  sema/hadeethenc): carian gabungan keyword+semantik offscreen, kad
  butiran memaparkan data yang di-sync — 18 semakan.

| # | Semakan | Menangkap |
|---|---|---|
| 1 | Sintaks Python | fail rosak |
| 2 | Import modul teras | import yang tidak wujud |
| 3 | Warna sebagai nilai lalai | pepijat tema berulang |
| 4 | `.bat`/`.ps1` CRLF + ASCII | pepijat Windows berulang |
| 5 | `Join-Path $env:` tanpa pengawal | pepijat PowerShell berulang |
| 6 | Migrasi DB (data kekal) | kehilangan data pengguna |
| 7 | Apl melancar, kedua-dua tema | pepijat tema/UI |
| 8 | Transliterasi (12 kes) | jalalah, shadda, tanwin, syamsiyyah |
| 9 | Syarah: parser + pengawal | penomboran sumber berubah |
| 10 | Folder bersih | `__pycache__`, DB ujian |

Keluar 0 = selamat hantar. Keluar 1 = jangan hantar.
Guna folder bernama **ada ruang** (`D:\Pustaka Quran Hadis`) — banyak
pepijat hanya muncul di situ.

---

## 10. Tiga corak pepijat BERULANG

### A. Nilai dinilai pada masa import → terkunci selama-lamanya

```python
def text_browser(text="", color=TEXT_SECONDARY):   # SALAH
```
```python
def text_browser(text="", color=None):             # BETUL
    if color is None:
        import ui.theme as _t
        color = _t.THEMES[_t.CURRENT_THEME]["TEXT_SECONDARY"]
```
Imbas dengan AST sebelum hantar — cari `def f(x=WARNA)`.

### B. Pembolehubah persekitaran null → `Join-Path` melontar

Sudah berlaku 3 kali (`$env:WINDIR`, `$env:APPDATA` ×2). Simpan ke
pembolehubah dan periksa dahulu sebelum `Test-Path`.

### C. Andaian tidak diuji menghentikan segalanya

- *"English mustahil"* → silap; ada jambatan `ara-*`
- *"Fath al-Bari tiada dalam OpenITI"* → silap; Ibn Hajar di `0875AH`
- **Uji terhadap data sebenar SEBELUM membuat kesimpulan.**

---

## 11. Pepijat Qt yang sudah dibetulkan — jangan "perbaiki" semula

- `setAlignment()` mesti **sebelum** `setPlainText()`
- JANGAN `setDefaultTextOption`/`WrapAtWordBoundaryOrAnywhere`/
  `setTextWidth()` pada dokumen hidup — merosakkan bidi
- Auto-tinggi: ukur pada `document().clone()`
- `QSizePolicy.Maximum` menegak = halaman kosong. Guna `Minimum`.
- Menu klik-kanan perlu eventFilter + pasang pada `viewport()` juga

---

## 12. Peta dokumen

| Dokumen | Isi |
|---|---|
| **`dokumen/manual/MANUAL_REFERENSI_DEV.md`** | Dokumen ini — rujukan utama |
| `dokumen/manual/manual/manual/MANUAL_INSTALASI.md` | Manual pemasangan pengguna (keperluan, pasang, kunci API, kemas kini, nyahpasang) |
| `dokumen/manual/manual/manual/MANUAL_PENGGUNAAN.md` | Manual cara guna aplikasi (antara muka, carian, tetapan) |
| `dokumen/manual/TRANSFORMASI_DETAIL.md` | Transformasi paparan detail LAMA → BARU (Sesi 55) + tangkapan skrin (lama vs baru) |
| `dokumen/manual/MULA_SINI.md` | 6 peraturan keras + senarai semak + fakta (baca dahulu) |
| `dokumen/rujukan/RANCANGAN_4FASA.md` | Keputusan fasa, keutamaan paparan, isu belum selesai |
| `dokumen/perubahan/PERUBAHAN_30JUL.md` | Perubahan 30 Jul (Sesi 6–9) |
| `dokumen/perubahan/PERUBAHAN_31JUL.md` | Perubahan 31 Jul (Sesi 10–11, HadeethEnc, keluaran) |
| `dokumen/sesi/sesi_index.md` | Arkib penuh (Sesi 1–30) |
| `dokumen/perubahan/CHANGELOG.md` | Log perubahan versi aplikasi mengikut tarikh (1.0–1.3 + reset; 11 Ogos 2026) |
| `dokumen/audit/AUDIT_SUNNAH.md` | Hasil audit pautan "Baca penuh" sunnah.com (50/50, 11 Ogos 2026) |
| `dokumen/audit/DAPATAN_WEB.md` | Dapatan siasatan web (sunnah.com, dorar.net, SemakHadis — bab 1–10) |
| `dokumen/audit/PADANAN_ARKIB.md` | Jejak padanan 11 dokumen arkib ↔ dokumen projek + penilaian penyelamatan (11 Ogos 2026) |
| `dokumen/rujukan/INSTALLER.md` | Reka bentuk installer (Nuitka, Inno Setup, `%LOCALAPPDATA%`, bundel indeks FAISS, wizard) — belum dilaksanakan |
| `dokumen/rujukan/SUMBER_hadis-my.md` | Sumber teras hadis.my/hadith.my + draf permohonan bundel + lampiran 55 hadis (belum dihantar) |
| `dokumen/surat/kebenaran/PERMOHONAN_LESEN_SEMAKHADIS.md` | Permohonan SemakHadis (DM dihantar, e-mel siap — aktif, belum dijawab) |
| `dokumen/rujukan/ISU_TERJEMAHAN_MELAYU.md` | 80 hadis matn tidak diterjemah + senarai ID penuh untuk laporan hadis.my |
| `dokumen/audit/DORAR_NET.md` | Penilaian terperinci Dorar + sunnah.com (robots.txt, keputusan pautan keluar, nota kaki penangguhan) |
| `dokumen/rujukan/ANALISA_6OGOS.md` | Analisis 7 kekurangan v1.0 (5 selesai, 2 terbuka — lesen SemakHadis + model/installer) |
| `dokumen/perubahan/PERUBAHAN_7OGOS.md` | Perubahan 7 Ogos (siasatan + pembaikan crash carian gabungan) |
| `dokumen/perubahan/PERUBAHAN_11OGOS.md` | Perubahan 11 Ogos (Sesi 54 — penyatuan label, semakan statik, ujian visual, versi 1.0) |
| `dokumen/perubahan/PERUBAHAN_12OGOS.md` | Perubahan 12 Ogos (Sesi 55 — 4 mockup halaman detail, dua lajur, palet hangat, cip warna, finalise) |
| `dokumen/perubahan/PERUBAHAN_13OGOS.md` | Perubahan 13 Ogos (Sesi 55 lanjutan — buang tab Sebelah + teks sama paras, lalai Arab Kecil, pembetulan draf jawapan AI) |
| `dokumen/rujukan/DEKLARASI.md` | Deklarasi Pustaka Hadith (skrin permulaan + Tentang; Versi 1.0 rasmi) |
| `README.md` | Pintu masuk repositori (akar projek) |
| `dokumen/rujukan/PANDANGAN_RISIKO.md` | Analisis keseluruhan + risiko (7–8 Ogos; risiko #1–3 ditutup) |
| `dokumen/rujukan/RANCANGAN_REFACTOR.md` | Pelan pecahan `ui/app_qt.py` — 5 langkah SELESAI (8 Ogos) |
| `dokumen/rujukan/REVOKE_KUNCI.md` | Panduan batalkan kunci API terdedah |
| `BACA_SAYA.txt` | Ringkasan pengguna dalam folder ZIP |
| `dokumen/imej/` | Tangkap layar — baseline regresi (7), rujukan LAMA (2), galeri 5 tema (10) — lihat §12A |

---

## 12A. Imej tangkap layar — `dokumen/imej/` (19 fail)

Tiga kumpulan imej dalam `dokumen/imej/` — semua dirujuk oleh dokumen
manual dan dibundel dalam ZIP edaran (senarai rasmi: `manual/manual/MANUAL_INSTALASI.md`
seksyen 9, **130 fail** — imej 19):

| Kumpulan | Fail | Asal & pengesahan |
|---|---|---|
| **Baseline regresi (7)** | `baru_detail_*` (gelap 3 + terang 4) | Dijana & dibandingkan oleh `bina_tangkapan_dokumentasi.py` — `SENARAI_GELAP`/`SENARAI_TERANG` (Sesi 55); regresi: `python bina_tangkapan_dokumentasi.py`, kemas selepas perubahan reka bentuk SAH: `--kemas` |
| **Rujukan LAMA (2)** | `lama_detail_*` (gelap + terang) | Tangkapan 7 Ogos, rujukan perbandingan LAMA→BARU dalam `TRANSFORMASI_DETAIL.md` — bukan sebahagian regresi |
| **Galeri tema (10)** | `tema_{home,detail}_{neutral,kertas,neutral_terang,terang,sistem}.png` | Tangkapan 14 Ogos — halaman SAMA (Utama + Detail Abu Daud #3982, 1100×780) untuk perbandingan adil 5 tema; dirujuk oleh `manual/manual/MANUAL_PENGGUNAAN.md` seksyen TEMA → "Rujukan visual (5 tema)" via `../imej/`. Susun atur semasa: **RTL — Arab di kanan, terjemahan di kiri** (14 Ogos); bila susun atur berubah, tangkap semula |

**Proses kemas kini galeri tema** (bukan sebahagian suite — tiada regresi):
1. Lancarkan `PustakaApp` (skrin sebenar), `set_theme()` setiap 5 tema
   (`neutral` · `dark` · `lightneutral` · `light` · `sistem`), buka
   halaman yang SAMA, tangkap tetingkap 1100×780 (ImageGrab, bbox
   `GetWindowRect`). Tangkapan mesti menggambarkan susun atur semasa
   (selepas RTL: Arab di kanan).
2. Salin ke `dokumen/imej/tema_*.png` — NAMA MESTI padan rujukan
   manual (jangan ubah nama fail sahaja tanpa kemas kini
   `manual/manual/MANUAL_PENGGUNAAN.md`).
3. Kemas kini `manual/manual/MANUAL_INSTALASI.md` senarai ZIP (kiraan dokumen/imej
   + jumlah fail) — semakan `semak_bersih` semak.py menandai imej
   baharu sehingga di-commit.
4. Imej galeri TIDAK dikunci semak kontras/baseline — ia dokumentasi
   pengguna; pastikan halaman sama supaya perbandingan adil.

---

## 13. Cara bekerja dengan pengguna

- Bahasa Melayu Malaysia, bukan Indonesia
- `"sama"` = masalah berterusan **atau** hasil betul — **tanya, jangan teka**
- Bila diminta *"analisis sahaja"* — jangan ubah kod
- Pengguna mahu "download dan jalan" — hantar ZIP siap-jalan
- Projek sebenar di `D:\Pustaka Quran Hadis` — tidak boleh dicapai
  dari sandbox; fail di sini ialah binaan semula
