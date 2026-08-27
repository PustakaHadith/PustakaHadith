# Perubahan 14 Ogos 2026 — Semakan mesin sebenar (4 item tertangguh)

> Log ringkas perubahan pada 14 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md` (entri "Semakan mesin
> sebenar (14 Ogos)"). Versi apl kekal **1.0**.

## Kandungan sesi

1. **Ujian mesin sebenar — suite pra-hantar penuh (11 ujian)** — semua
   dijalankan pada mesin sebenar (Windows, skrin fizikal): semak.py
   SEMUA LULUS · uji_negatif_8z 40/0 · uji_visual_mockup 130/0 ·
   uji_visual_piksel 53/0 · **uji_visual_sebenar 68/0 (skrin sebenar,
   tetingkap benar-benar dipapar)** · uji_tukar_tema 19/0 ·
   uji_bandingan 55/0 · uji_lompat_fungsi 48/0 · uji_end_to_end 18/0 ·
   bina_tangkapan_dokumentasi 7/7 · uji_draf_jawapan 9/0.
2. **Halaman Tersimpan — ujian baharu dengan tanda buku SEBENAR**
   (`uji_tersimpan_sebenar.py`, 20/0, daftar sebagai ujian #12 dalam
   `uji_pra_hantar.py`) — simpan 3 hadis sebenar dari 3 kitab,
   bookmarks.json ditulis ke cakera, halaman Tersimpan memapar 3 kad,
   klik kad membuka hadis betul (paparan terbalik: terbaru dahulu),
   **restart app → tanda buku kekal dari cakera**, buka dari
   Tersimpan selepas restart, tanggalkan semua → empty state + fail
   kosong, data pengguna dipulihkan.
3. **`diagnos_syarah.py` pada data sebenar** — hadis.db (7,008
   Bukhari) + Fath al-Bari (5,075 seksyen): penomboran **HANYUT**
   (anjakan +2 → +120 → −400, julat 520; 1/8 julat sejajar sahaja).
   Mengesahkan keputusan 31 Jul: padanan ikut ID tidak selamat,
   Fasa 4B kekal dibatalkan.
4. **Pipeline end-to-end — install → API → baca → tersimpan**
   (`uji_pipeline_api.py`, 18/0) — semua kebergantungan
   requirements.txt diimport (Python 3.14); API HIDUP service.hadis.my
   dengan kunci developer (use_db=False): /collections (9 kitab),
   senarai hadis lang=ms, hadis tunggal 3 bahasa, carian "zakat",
   kuota harian dibaca dari header; hadis API dibuka dalam app sebenar
   (Arab + terjemahan dipapar); disimpan → halaman Tersimpan →
   ditanggalkan; bookmarks.json dipulihkan.
5. **Semakan konsistensi dokumen manual vs UI sebenar** (offscreen) —
   skrip audit baharu `semak_dokumen_ui.py` (**74 semakan, 0 gagal**):
   setiap tuntutan `MULA_CEPAT.md` + `manual/manual/MANUAL_PENGGUNAAN.md` disahkan
   terhadap UI sebenar — angka data dari hadis.db (62,169 / 31,833 /
   4,237 / 63,930 / English 7 kitab sahaja), nav + gear, kad kitab,
   halaman kitab (pager, kotak Lompat, Ctrl+G, backTop, 20/halaman),
   halaman hadis (butang tajuk, tab ARAB/TRANSLITERASI + 3 bahasa,
   **dua lajur sebelah-menyebelah**, bar teks `Lapor ralat | Kongsi |
   Salin`, menu Salin 3 pilihan, klik kanan "Salin semua", huraian
   SemakHadis/HadeethEnc, darjat, cip warna ikut makna, backTop),
   carian (format lompat, 2 enjin, draf AI, jam berputar, notis
   longgar, backTop), Tersimpan (empty state, hero, backTop), panel
   Tetapan (5 bahagian + 8 label), splash (Sedia! ✔, klik langkau),
   deklarasi "Faham", fail pemasangan, Python 3.14, suite 12 ujian.

## Ujian baharu

| Fail | Bilangan | Daftar |
|---|---|---|
| `uji_tersimpan_sebenar.py` | 20/0 | `uji_pra_hantar.py` #12 |
| `uji_pipeline_api.py` | 18/0 | berasingan (perlu kunci API hidup + internet; tidak digate) |
| `semak_dokumen_ui.py` | 74/0 | audit; tidak digate |

## Sesi sambungan: sync penuh dari mula (item tertangguh #2) ✅

`sync.py --paksa` dijalankan pada mesin sebenar dengan kunci developer
(env var sahaja):

| Kitab | Muka surat | Keputusan |
|---|---|---|
| malik + darimi | 16 + 34 | 100% (56s) |
| tirmidzi + ibnu-majah | 39 + 44 | 100% (120s) |
| abu-daud + nasai | 46 + 57 | 100% (130s) |
| bukhari + muslim | 71 + 54 | 100% (143s) |
| ahmad | 264 | 100% (299s) |

- Jumlah: **622 muka surat, ~12.5 minit, 639 permintaan**, kuota
  9,999 → 9,360
- **"Rekod baharu: 0"** setiap kitab — `INSERT OR IGNORE` mengesahkan
  muat turun semula sepadan TEPAT dengan DB sedia ada (tiada data
  berubah, tiada duplikat)
- Pengesahan penjajaran:
  - 62,169 hadis unik (9 kitab), 0 duplikat, 0 arab/melayu/indonesia
    kosong, julat id kontigu 1..N setiap kitab
  - Indeks carian FTS: 62,169 = 62,169 (sejajar)
  - **Perbandingan teks API vs DB: 45/45 padan** (5 hadis rawak setiap
    kitab — arab + melayu + indonesia, selepas normalkan tashkeel)

Item #2 tertangguh kini DITUTUP.

## Sesi sambungan: padanan `ara-*` penuh pada hadis.db sebenar (#3) ✅

**Arahan pengguna:** "Sahkan padanan lapisan ara-* pada hadis.db sebenar
(bukan proksi CDN) untuk menutup item tertangguh #3".

Sebelum ini (Sesi 18.13) item 3 hanya disahkan pada **sampel 500 hadis
Bukhari** (90.8%). Kini pengesahan PENUH:

1. **Padan semua hadis** (baca-sahaja, 32,439 hadis 7 kitab dengan
   sumber): **31,952 berjaya (98.5%)**, gagal 487 (perbezaan edisi
   teks Arab — bukan pepijat padanan; padan rekod Fasa 3)
   - Taburan kaedah: indo 23,383 (73.2%) · indo~ 6,941 (21.7%) ·
     **penuh 877 + awalan 235 + kata 516 = 1,628 (5.1%) lapisan
     `ara-*`** mengisi celah Indonesia
   - 31,952 − 119 (eng tiada di CDN) = **31,833 = tepat jadual
     tersimpan**; 0 entri english basi
2. **Audit bebas** (`audit_eng.py --semua`): 30,541/30,547 disahkan
   (100.0%), 6 disyaki = **positif palsu saksi** (penomboran `ind-*`
   hanyut dari `ara-*`) — boleh dihasilkan semula, sama seperti
   siasatan 31 Jul
3. **`sync_english.py` dari mula** pada hadis.db sebenar:
   **31,833 deterministik** (per-kitab: bukhari 6,964 · muslim 5,149 ·
   abu-daud 4,558 · tirmidzi 3,742 · nasai 5,560 · ibnu-majah 4,314 ·
   malik 1,546; tiada_eng 119; gagal 487) — bab 31,325, darjat 63,930
   ditulis semula sama

Item #3 tertangguh kini DITUTUP.

## Sesi sambungan: audit liputan SemakHadis (#8) 📊

**Arahan pengguna:** "Audit liputan SemakHadis 4,237/62,169 dan
senaraikan kitab/bab yang paling banyak tertinggal untuk mencari sumber
BM terbuka lain". Dokumen penuh: `dokumen/audit/AUDIT_SEMAKHADIS.md`.

Keputusan ringkas:

- Liputan: **4,237/62,169 (6.8%)**, 2,263 sema_id unik; cache sumber
  `.cache_sema/` sudah penuh (2,372) — siling dalam sumber ini
- Per kitab: tirmidzi **1.6%** (terendah) · darimi 4.4% · ahmad/nasai
  6.2% · malik 7.6% · abu-daud 7.7% · muslim 8.0% · ibnu-majah 9.4% ·
  bukhari **10.2%** (terbaik)
- 393 bab (7 kitab): **103 bab (26%) liputan 0%**; hanya 3 bab >50%
- Jurang terbesar: Tafsir (bukhari 65: 441 + tirmidzi 47: 402) · Hajj
  (~1,564 merentas 5 kitab) · Solat (~1,371: abu-daud 549 + ibnu-majah
  549 + tirmidzi 273); bab sifar mutlak: tirmidzi 43/14, nasai 26,
  malik 31/36/28
- ahmad (26,363): seragam 5–9% tiap desil; darimi: puncak 13.0%
  (id 1,347–1,684), terendah 0.9% (2,693–3,030)
- Keutamaan sumber BM baharu ikut jurang: (1) tafsir per-hadis,
  (2) syarah bab ibadah (hajj/solat), (3) sumber khusus Tirmidzi,
  (4) struktur Musnad untuk Ahmad

Item #8 ialah siling sumber (bukan pepijat) — audit ini menyediakan
peta keutamaan bila sumber BM terbuka baharu ditemui.

## Sesi sambungan: siasatan sumber tafsir/syarah BM per-hadis 📖

**Arahan pengguna:** "Siasat sama ada tafsir BM per-hadis terbuka wujud
(cth. Al-Muyassar BM, Tafsir Kemenag API) yang boleh menutup jurang
Tafsir 843 hadis". Dokumen penuh: `dokumen/audit/SIASATAN_TAFSIR_BM.md`.

**KEPUTUSAN: TIADA sumber BM per-hadis terbuka menutup jurang Tafsir
843.**

- **MyHadith JAKIM — status BERUBAH** (31 Jul = "Transport error",
  kini boleh diakses + ada API berkuasa kunci; kandungan per-hadis:
  Arab, terjemahan, Pengajaran, Asbab al-Wurud, status) — TETAPI
  koleksi separa (Bukhari 17 kitab sahaja, Tirmidzi 14, dll.) dan
  **TIADA kitab Tafsir** dalam mana-mana koleksi; hak cipta JAKIM
- **Tafsir al-Muyassar BM** — tafsir QURAN (buku, hak cipta), bukan
  syarah hadis
- **Tafsir Kemenag API (LPMQ)** — tafsir QURAN Indonesia (bukan BM),
  perlu daftar; bukan huraian hadis
- **IslamHouse Malay** — kategori "Syarah Hadis" per-hadis (ID
  344947) TIADA dalam versi Melayu (hanya buku); wujud Arab/Indonesia
- **kitabhadis.com** — belum lengkap, tiada syarah; **myway.my** —
  komersial (AI); **api.hadis.my** — tiada medan syarah;
  **surah.my** — 503 (turun)

Cadangan: kekal siling SemakHadis (satu-satunya sumber BM sah lesen);
tafsir ayat BM boleh jadi konteks ayat tambahan HANYA jika lesen +
pemetaan hadis→ayat selesai (bukan huraian hadis); pantau MyHadish
(penambahan kitab Tafsir) + IslamHouse Melayu.

## Sesi sambungan: dokumen "Mula Cepat" untuk pengguna 🚀

**Arahan pengguna:** "Sediakan versi ringkasan 'Mula Cepat' untuk
pengguna: apa yang sudah disahkan, bagaimana menjalankan app, dan
cara memulakan carian".

- Fail baharu: `dokumen/manual/MULA_CEPAT.md` — ringkasan pengguna:
  (1) jadual pengesahan (62,169 data penuh, English 31,833 audit
  100%, SemakHadis 4,237 + darjat 63,930, Tersimpan, carian, suite
  12 ujian), (2) cara jalankan (ikon "Hadis" / PASANG.bat /
  JALANKAN.bat / kunci API), (3) cara carian (buka kitab, lompat
  nombor, Pencarian kata kunci + AI, format `bukhari 433`), (4)
  rujukan lanjut
- `MULA_SINI.md` — rujukan log harian dikemas ke PERUBAHAN_14OGOS.md
  + pautan MULA_CEPAT.md

## Nota

- `uji_pipeline_api.py` tidak dimasukkan ke `uji_pra_hantar.py` —
  ia memerlukan internet + kunci API hidup; gate pra-hantar mesti
  berfungsi luar talian.
- Kunci API dibaca dari `kunci_terdedah.txt` (gitignored) dalam memori
  sahaja — tiada kunci ditulis ke `user_settings.json`.

## Sesi lanjutan: semakan dokumen manual vs UI sebenar ✅

Permintaan: "Semak semula konsistensi semua dokumen manual
(MULA_CEPAT, MANUAL_PENGGUNAAN, MULA_SINI) terhadap UI sebenar dengan
ujian offscreen".

**Skrip audit baharu: `semak_dokumen_ui.py` — 74 semakan, 0 gagal.**

Pendekatan:
1. **Katalog tuntutan** — setiap ayat fakta dalam `MULA_CEPAT.md` +
   `manual/manual/MANUAL_PENGGUNAAN.md` disenaraikan (angka data, label butang, tab,
   pintasan, tingkah laku). `MULA_SINI.md` ialah dokumen developer
   (rekod sejarah, bukan tuntutan UI) — dikecualikan, tetapi rujukan
   failnya disahkan wujud.
2. **Semak sumber** untuk tuntutan statik (label, pintasan, baris teks)
   dan **UI hidup offscreen** untuk tuntutan dinamik (widget wujud,
   teks dipapar, geometri dua lajur).

Semakan baharu yang ditambah semasa audit (tidak ada dalam versi 54/0
awal):
- **D3b — dua lajur sebelah-menyebelah** (geometri: lajur Arab x <
  lajur terjemahan x)
- **D13 — cip warna ikut makna** (hijau/merah/amber dalam `_warna_cip`)
- **D14 — klik kanan "Salin semua"** (`_CopyMenuFilter`)
- **D15 — butang ↑ detail** (backTop)
- **E7–E9 — draf jawapan AI, jam berputar 🕐→🕛, notis carian longgar**
- **F3 — butang ↑ Tersimpan**
- **G5 — 8 label panel Tetapan** (Saiz antara muka, Saiz teks Arab,
  Saiz terjemahan, Fon Arab, Bahasa dimuat, Selawat, Tetapan API,
  Tentang Pustaka Hadis)
- **H4 — deklarasi larian pertama dengan butang "Faham"**
- **A6–A8 — English 7 kitab sahaja (Ahmad/Darimi 0), Python 3.14,
  suite pra-hantar 12 ujian**

Pengesahan penting: semua tuntutan dokumen **TEPAT** dengan UI sebenar
— tiada dokumen yang ketinggalan kod (cth. bar `Lapor ralat | Kongsi |
Salin` sebagai teks, 3 tab bahasa tanpa tab Sebelah, tab
ARAB/TRANSLITERASI, justify + panel transliterasi di atas, cip warna,
huraian SemakHadis + darjat terbuka).

## Penutup hari — semakan #12 dikunci + suite 12/12 (petang 14 Ogos) ✅

**Semakan #12 semak.py — "'Sesi Terakhir' MULA_SINI seiring git log"**
(`80b7abf` + `564dba7`): bahagian 'Sesi Terakhir' dalam MULA_SINI.md
tidak boleh ketinggalan daripada git log. 4 peraturan:

1. **Tarikh tajuk** `## Sesi Terakhir — ...` ≥ tarikh commit git
   terbaru (kadar hari)
2. **Teks ringkasan mesti menyebut tarikh kerja terkini** — bukan
   hanya tajuk (mencegah tajuk dinaik tarikh tanpa meringkaskan kerja
   hari itu; baris tajuk dikecualikan daripada semakan)
3. **Semua hash commit yang disebut mesti wujud** dalam sejarah git
4. **Sekurang-kurangnya satu hash daripada 10 commit terbaru** disebut

Tiada git (edaran ZIP) → semakan dilangkau supaya gate kekal berfungsi
di luar repo.

**Dikunci oleh `uji_negatif_8z` — kini 45/0 (30 cabang, 4 khusus #12):**
- tarikh lapuk → `KETINGGALAN git log`
- hash rekaan `fffffff` → `hash tidak wujud dalam git`
- MULA_SINI.md dibuang → `TIADA` (GAGAL bersih, bukan ranap)
- tarikh dibuang dari teks ringkasan → `tidak menyebut tarikh kerja
  terkini` (cabang baharu, `564dba7`)

Pulihan byte-tepat disahkan selepas setiap mutasi.

**Suite rasmi `uji_pra_hantar.py` — 12/12 SEMUA LULUS (418.3s):**
semak #12 lulus dalam log rasmi (`pra_hantar_semak.log`) +
`uji_negatif_8z` 45/0 (`pra_hantar_uji_negatif_8z.log`).

**README.md dikemas** (`b546912`): semakan #12 didokumenkan dalam komen
semak.py · kiraan semakan 139 → 370+ · `uji_negatif_8z` 45/0 + suite
12 ujian ditambah ke senarai ujian · **tuntutan lapuk tab Sebelah /
'Salin semua bahasa' (dibuang Sesi 55) diganti** dengan tab dua lajur
semasa + bar teks `Lapor ralat | Kongsi | Salin`.

Juga dikemas petang ini: `MULA_SINI.md` Sesi Terakhir (§#12) + §5
senarai sesi + senarai semak, `MANUAL_REFERENSI_DEV.md` (senarai suite
12 ujian + uji_negatif 45/0).

Commit petang 14 Ogos: `82cb4c1` · `c0b8020` · `f359ea9` · `80b7abf` ·
`564dba7` · `b546912` — jumlah hari ini: **14 commit**.

## Sesi lanjutan: konsistensi rentas dokumen (README · MULA_CEPAT · instalasi)

1. **MULA_CEPAT.md diaudit** — tiada percanggahan dengan README/manual
   kecuali URL kunci API: `developer.hadis.my/dashboard/keys`
   (tidak disahkan) diganti dengan arahan selaras MANUAL_INSTALASI:
   daftar di <https://hadis.my> → **Developer / API**.
2. **manual/manual/MANUAL_INSTALASI.md + BACA_SAYA.txt disahkan vs skrip .bat
   sebenar** — SEMUA tuntutan padan: PASANG.bat (4 langkah, "SIAP",
   pintasan "Hadis" via pintasan.ps1, gear → Tetapan API) ·
   BUAT_PINTASAN/JALANKAN/NYAHPEPIJAT · BUANG.bat (2 soalan + taip
   BUANG) · KEMASKINI.bat (seret ZIP) · pintasan.ps1 (Hadis.lnk
   Desktop + Start Menu) · "✓ Berjaya — N koleksi" (settings_panel.py
   padan 9 koleksi).
3. **Semakan J/K ditambah ke `semak_dokumen_ui.py`** (74 → **110
   semakan, 0 gagal**) — frasa kunci Ciri-ciri mesti wujud dalam
   KEDUA-DUA dokumen supaya tidak hanyut: J: README ↔
   MANUAL_PENGGUNAAN (12 frasa: TRANSLITERASI, tab bahasa, bar teks,
   menu Salin, sama paras, dua lajur, 62,169, 4,237) · K: MULA_CEPAT
   ↔ README (12 frasa: + 63,930, bukhari 433). Juga semakan I diperluas
   (8 tuntutan .bat). Kes negatif disahkan: frasa dibuang → GAGAL
   dikesan.

## Pengesahan akhir (petang) — suite 12/12 + audit SUMBER_hadis-my

- **`uji_pra_hantar.py` penuh dijalankan SEMULA** selepas perubahan
dokumen: **12/12 SEMUA LULUS (389.2s)** — semak.py #12 (14.7s),
uji_negatif_8z 45/0 (10.9s), dan semua 10 suite lain lulus. (Nota:
pada masa ini `semak_dokumen_ui.py` dengan semakan J/K masih skrip
berasingan — dijalankan manual → **110/0**; **selepas ini ia digate
sebagai ujian #13**, lihat bahagian penutup.)
- **`dokumen/rujukan/SUMBER_hadis-my.md` diaudit** — konsisten:
  Base URL `service.hadis.my/api/v1` + header `X-API-Key` padan
  `api/hadis_api.py`; portal `developer.hadis.my/dashboard` sah (ia
  sumber asal URL MULA_CEPAT yang diganti tadi); bentuk kunci
  `HADIS_…` padan kunci sebenar (42 aksara); 9 koleksi = 62,169 padan
  hadis.db; pelan Developer 10,000/hari padan kuota sync.

## Sesi lanjutan (malam): tema NEUTRAL lalai + WCAG AA dikunci

Keputusan pengguna untuk pengguna awam (selepas perbandingan kontras
sebenar: Windows gelap 16.5:1 vs kertas hangat 13.3:1; tier malap lama
4.25:1 GAGAL AA):

1. **Palet NEUTRAL baharu (lalai)** — `ui/theme.py`: gelap neutral gaya
   Windows (PAGE_BG `#1F1F1F`, CARD_BG `#252526`, teks putih `#FFFFFF`,
   sekunder `#C6C6C6`, tiada hue hangat); aksen TEAL hijau kekal.
   `settings.get("theme", "neutral")` di app_qt/settings_panel/splash —
   pemasangan baharu terus Neutral.
2. **3 pilihan TEMA** — panel Tetapan: ☀ Terang · 🌙 Neutral (lalai) ·
   📜 Kertas (kertas hangat sedia ada). Tema "dark" disimpan sebagai
   pilihan "Kertas" supaya pengguna sedia ada tidak kehilangan pilihan.
3. **Kontras diperbaiki** — tier malap kertas hangat (TEXT_MUTED
   `#8F8878`→`#9C9589`, TEXT_FAINT `#6F6A5E`→`#928D80`) + pemalar modul
   diselaraskan; light FAINT `#6D6858`; neutral semua tier ≥ 4.5:1.
4. **Semakan #13 semak.py: kontras WCAG AA** — 54 pasangan warna (3
   tema × [4 tier teks × 3 permukaan + 3 semantik + 3 TEAL]) semua
   ≥ 4.5:1; sebarang warna baharu bawah AA → GAGAL.
5. **Dikunci `uji_negatif_8z` 47/0** — cabang mutasi #31: NEUTRAL
   TEXT_FAINT diturunkan ke `#707070` → dikesan "bawah AA 4.5".
   Pepijat ditemui: cache `.pyc` Windows (mtime 2 saat) membuat import
   baca salinan lama bermutasi → `buang_pyc_theme()` sebelum/semasa
   pulihan.
6. **Ujian dikemas** — uji_tukar_tema 6 kitaran (neutral+dark+light)
   27/0; semak 6 (apl melancar) kini 3 tema; semak 10aa (logo) kekal
   pada palet kertas (CURRENT_THEME lalai modul); semak_dokumen_ui G2
   label 3 butang tema 110/0; uji_visual_sebenar gelap = dark|neutral.
7. **Dokumen** — MANUAL_PENGGUNAAN TEMA (3 pilihan, neutral lalai),
   MANUAL_REFERENSI_DEV (47 lulus, 31 cabang). user_settings.json
   pengguna TIDAK disentuh (data peribadi, gitignore) — pilihan "dark"
   kekal sehingga pengguna pilih 🌙 Neutral.

## Sesi lanjutan (malam): tema NEUTRAL TERANG + panel TEMA 2×2

1. **Palet `lightneutral` baharu** — pasangan terang kepada NEUTRAL:
   PAGE_BG `#F4F4F4`, CARD_BG `#FFFFFF`, HEADER `#ECECEC`, teks
   `#1A1A1A`/`#444444`/`#595959`/`#6B6B6B` — kelabu/putih TULEN, tiada
   hue hangat. Semua 18 pasangan ≥ 4.5:1 (paling ketat FAINT pada
   HEADER 4.51:1) — semak kontras #13 kini **72 pasangan (4 tema)**.
2. **Panel Tetapan TEMA = grid 2×2** — 🌙 Neutral (lalai) · 📜 Kertas ·
   ☀ Neutral terang · ☀ Terang. Susun atur QGridLayout (butang kertas
   hangat terang kekal "☀ Terang" supaya pengguna sedia ada tidak
   keliru). `QGridLayout` ditambah ke import settings_panel.
3. **Ujian dikemas** — semak 6 (apl melancar) 4 tema · semak #13
   (kontras) 4 tema · uji_tukar_tema 8 kitaran **35/0** ·
   semak_dokumen_ui G2 label 4 butang · uji_negatif_8z kekal **47/0**
   (cabang #31 masih mengunci NEUTRAL TEXT_FAINT — unik dalam theme.py).
4. **Dokumen** — MANUAL_PENGGUNAAN TEMA 4 pilihan.

## Sesi lanjutan (malam): tema "Ikut sistem" (ikuti mod gelap Windows)

1. **`windows_gelap()`** (`ui/theme.py`) — baca registry Windows
   `AppsUseLightTheme` (0 = gelap) melalui `winreg`; gagal → lalai
   gelap supaya app tidak memilih terang tanpa sengaja.
2. **`tema_efektif(kunci)`** — selesaikan "sistem" → `neutral`
   (Windows gelap) atau `lightneutral` (Windows terang); kunci tidak
   sah → `neutral`. `apply_theme()` kini menyelesaikan secara dalaman,
   jadi splash/panel/app semua serasi dengan "sistem".
3. **Pemantau 2 saat** (`app_qt._semak_tema_sistem`) — QTimer baca
   registry; bila palet efektif berbeza daripada semasa, `set_theme(
   "sistem", paksa=True)` bina semula UI. Tiada kesan bila tema bukan
   "sistem". `set_theme` dapat parameter `paksa` (elak guard kunci sama).
4. **Panel TEMA = grid 2×2 + 🌓 Ikut sistem** span penuh di bawah
   (5 butang). Toast tema dibetulkan: guna `is_dark()` (palet efektif)
   bukan nama kunci — sebelum ini lightneutral memapar "Tema gelap".
5. **Ujian**: semak 6 (apl melancar) 5 mod termasuk sistem · uji_tukar_tema
   10 kitaran **43/0** · simulasi flip Windows (monkeypatch
   `windows_gelap`) → neutral→lightneutral, kunci kekal "sistem" ·
   uji_negatif_8z 47/0 · semak_dokumen_ui G2 label 5 butang 110/0.
6. **Dokumen** — MANUAL_PENGGUNAAN TEMA 5 pilihan.

## Penutup ciri tema — ujian flip Windows HIDUP + 2 saat (malam)

1. **Ujian flip hidup** — Windows sebenar ditukar ke mod terang
   (registry `AppsUseLightTheme`/`SystemUsesLightTheme` = 1 +
   broadcast WM_SETTINGCHANGE) dengan app berjalan pada tema
   "sistem": app bertukar automatik **neutral (#1F1F1F) →
   lightneutral (#F4F4F4)**; Windows dipulihkan ke gelap (asal)
   selepas ujian. Tangkapan: `bukti_visual/sistem_{gelap,terang}.png`.
2. **Selang pemantau 10 s → 2 s** (`7ed0eda`) — QTimer `_semak_tema_sistem`
   kini 2 s; ujian flip diukur semula: bertukar **dalam 1.0 s**.
3. **Keadaan akhir ciri tema (14 Ogos)** — 5 pilihan TEMA (🌙 Neutral
   lalai · 📜 Kertas · ☀ Neutral terang · ☀ Terang · 🌓 Ikut sistem);
   semua tier teks ≥ 4.5:1 (semak #13, 72 pasangan); suite rasmi
   **13/13 SEMUA LULUS (449.1s)** selepas perubahan 2 s.

## Penutup hari (malam) — status akhir 14 Ogos

- **24 commit** hari ini (11 teras + 13 susulan) — daripada semakan
  mesin sebenar 4 item tertangguh hingga sesi tema lengkap.
- Ciri tema siap: **5 pilihan TEMA**, semua tier ≥ WCAG AA (semak
  #13, 72 pasangan), 🌓 Ikut sistem diuji hidup (flip Windows,
  bertukar 1.0 s).
- Gate penuh: suite rasmi **13/13 SEMUA LULUS** berulang kali
  (terakhir 449.1s), `semak.py` SEMUA LULUS, `uji_negatif_8z` 47/0.
- Pokok kerja bersih. Baki tertangguh §8: hanya **#7 kunci API**
  (kekal AKTIF sengaja).

## Galeri 5 tema dalam manual (malam)

1. **10 tangkapan skrin tema** disalin ke `dokumen/imej/`
   (`tema_{home,detail}_{neutral,kertas,neutral_terang,terang,sistem}.png`)
   — halaman sama (Utama + Abu Daud #3982) untuk perbandingan adil.
2. **MANUAL_PENGGUNAAN TEMA** — seksyen "Rujukan visual (5 tema)":
   dua jadual markdown 5 lajur (Utama + Detail) dengan pautan
   `../imej/...`.
3. **MANUAL_INSTALASI** — senarai ZIP dikemas: dokumen 36 → 46,
   imej 9 → 19, jumlah **120 → 130 fail**.
4. Nota: `semak_bersih` menandai imej baharu sebelum di-commit
   (gate berfungsi); user_settings.json dipulihkan ke "sistem"
   (kesan sampingan set_theme skrip tangkapan).

## MANUAL_REFERENSI_DEV §12A — imej tangkap layar didokumenkan

- Seksyen **12A. Imej tangkap layar — dokumen/imej/ (19 fail)**:
  tiga kumpulan (baseline regresi 7 · rujukan LAMA 2 · galeri tema
  10) + jadual asal & pengesahan.
- **Proses kemas kini galeri tema** — 4 langkah (set_theme 5 tema,
  halaman sama 1100×780, nama mesti padan rujukan manual, kemas kini
  senarai ZIP + semak_bersih).
- Baris `dokumen/imej/` ditambah ke Peta dokumen (§12).

## Susun atur RTL — Arab di KANAN, terjemahan di KIRI (malam)

- **Keputusan:** demi menghormati status hadis rujukan, teks Arab asal
  mesti di sebelah KANAN (aliran baca kanan-ke-kiri) dan terjemahan di
  KIRI — susun atur dua lajur dicerminkan.
- **Pelaksanaan:** `ui/pages_detail.py` — lajur Arab dipindah ke kanan
  (`kol_kanan`), terjemahan ke kiri (`kol_kiri`); tab ARAB ditanda
  `alignment` kanan mengikut aliran RTL; bar tindakan teks kekal di
  bawah terjemahan.
- **Pengesahan geometri dikemas:** `semak_dokumen_ui` D3b (Arab kanan,
  terjemahan kiri) + `uji_visual_mockup` (arab x > terjemahan x);
  `semak_dokumen_ui` 110/0 · `uji_bandingan` lulus.
- **Dokumen diselaraskan:** README (baris Tab bahasa dua lajur),
  MULA_CEPAT, MANUAL_PENGGUNAAN §2.4 — semua kini "Arab kanan,
  terjemahan kiri (susunan RTL, 14 Ogos)".
- **Imej:** baseline `bina_tangkapan_dokumentasi.py --kemas` (7) +
  **10 imej galeri tema ditangkap semula** (`_rakam_tema_rtl.py`,
  halaman sama Abu Daud #3982, 1100×780) — disahkan 963–1,426 warna
  unik setiap tangkapan.

## Penutup hari — semak #14 audit RTL dikunci + suite akhir (malam)

- **Semakan #14 semak.py: audit susun atur RTL dokumen** — sebarang
  tuntutan susun atur lama ("Arab di kiri", "terjemahan di kanan",
  "lajur kiri membawa teks Arab", "terjemahan > x Arab", dsb.) dalam
  TRANSFORMASI_DETAIL.md / manual/manual/MANUAL_PENGGUNAAN.md → GAGAL. Nota sejarah
  berpetik (rujukan "Arab kiri / terjemahan kanan" dalam nota RTL)
  tidak dipadan (corak khusus tanpa "di"/"membawa").
- **Dikunci uji_negatif_8z 49/0 (32 cabang)** — mutasi #32: "Arab di
  kiri" disuntik ke TRANSFORMASI_DETAIL → dikesan; semakan #14 dalam
  senarai pasca-pulihan.
- **Suite penuh AKHIR 13/13 SEMUA LULUS (463.6s)** — semak 32.0s ·
  negatif 12.1s · mockup 36.6s · piksel 73.9s · sebenar 110.4s ·
  tukar_tema 73.1s · bandingan 6.1s · lompat 6.2s · e2e 41.3s ·
  baseline 29.6s · draf 1.5s · tersimpan 27.6s · dokumen_ui 10.0s;
  "OK tiada proses ujian yatim selepas suite" — pengesahan dua hala.
- **Ringkasan akhir hari**: 35 commit (11 teras + 24 susulan), 5 tema
  semua ≥ WCAG AA, RTL (Arab kanan), Numpy, gate pantas, semak #14,
  suite 13/13.

## Susulan (malam): ringkasan satu muka dipindah ke atas + semak #15 dikunci

- **Ringkasan satu muka 'Keadaan projek'** dipindah dari §5 ke bahagian
  PALING ATAS MULA_SINI (sebelum 'Sesi Terakhir') — perkara pertama
  dibaca sesi AI baharu, selesai tanpa arkib penuh. Seksyen sendiri
  `## Keadaan projek — ringkasan satu muka (akhir 14 Ogos 2026)` +
  pautan silang ke dokumen berkaitan. §5 kini nota penunjuk sahaja.
- **Semak #15 `semak_ringkasan_keadaan`** — ringkasan seiring 'Sesi
  Terakhir': tarikh tajuk == tarikh Sesi Terakhir, kiraan commit sama.
  Dikunci `uji_negatif_8z` **52/0** (34 cabang, mutasi #34).
- Gate: semak.py SEMUA LULUS (15 semakan) · uji_negatif_8z 52/0.