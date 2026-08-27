# Changelog — Pustaka Hadith

> Log perubahan versi aplikasi. Cap versi tunggal: `VERSI.py`.
> Butiran penuh setiap sesi: `dokumen/sesi/sesi_index.md`. Rujukan ringkas sesi
> 11 Ogos 2026: `dokumen/perubahan/PERUBAHAN_11OGOS.md`; sesi 12 Ogos 2026:
> `dokumen/perubahan/PERUBAHAN_12OGOS.md`; sesi 13 Ogos 2026:
> `dokumen/perubahan/PERUBAHAN_13OGOS.md` (buang tab Sebelah + teks sama paras +
> pembetulan draf jawapan AI). Perbandingan paparan hadis lama →
> baharu (Sesi 55, dengan tangkap layar): `dokumen/manual/TRANSFORMASI_DETAIL.md`.

## 1.0 (ditetapkan semula) — 11 Ogos 2026

Versi aplikasi **ditetapkan semula ke 1.0** (dahulu 1.3) kerana edaran
ini belum dilancarkan secara rasmi. Pernyataan "versi semasa v1.3"
dalam dokumen dikemas ke v1.0; penanda sejarah (README
`(v1.1/v1.2/v1.3)`, komen `CIRI` dalam VERSI.py, log sesi) dikekalkan
sebagai rekod.

Disahkan pada skrin sebenar (11 Ogos 2026): header app memapar `v1.0`,
skrin pemula memapar `Versi 1.0 — carian kata kunci + makna (AI)`,
tangkapan `bukti_visual/versi_1_0.png`. Status: **rasmi (official)**.

Kerja Sesi 54 turut disertakan: penyatuan `_label_kiraan` (banner +
kad koleksi), semakan statik 8w/8x/8y/8z, ujian visual skrin sebenar
138/138, ujian negatif 21/21, pembetulan `getdata()` dan bbox
tangkapan.

Kerja Sesi 55 (12 Ogos 2026) turut disertakan: perbandingan 4 mockup
halaman detail (bukhari1/nasai2117/abudaud4177/ibnumajah2094) →
susun atur dua lajur Arab|terjemahan + tab per lajur + huraian/darjat
TERBUKA + cip warna ikut makna (hijau/merah/amber); **palet kertas
hangat mockup DITERIMA PAKAI** (teks sekunder dituna untuk AA); nama
"Sahih al-Bukhari" + prefix "Bab:"; penstabilan tangkapan skrin
(`uji_visual_sebenar.py` 65/0); kod mati `_pra_muat_model` dibuang
(penggantinya `PreloadWorker` QThread dikunci oleh semak.py 8k). Ujian:
semak.py SEMUA LULUS, mockup 130/0, bandingan 48/48, lompat 48/48,
end-to-end 18/18, tema 19/19.

### Kemas kini 13 Ogos 2026 (masih v1.0) — perubahan pengguna

- **Draf jawapan AI: bahagian "🔍 Carian Biasa (Keyword)" kini dipapar.**
  Sebelum ini bahagian ini tidak pernah muncul walaupun carian makna
  berjaya — dua ralat dalam `compose_draft_answer` (parameter `per_page`
  → `limit`, dan bacaan `data.results` → `hadis`) melempar TypeError
  yang ditangkap senyap, jadi senarai padanan kata kunci sentiasa
  kosong. Kini jawapan draf memaparkan senarai hadis padanan kata
  kunci + pratonton hadis teratas.
- **Tab "Sebelah" dibuang.** Paparan hadis kini 3 tab bahasa sahaja
  (Melayu | Indonesia | English), sepadan dengan reka bentuk mockup.
  Fungsi "Salin semua bahasa" (milik tab itu) turut dibuang; tindakan
  salin/kongsi kekal di bar tajuk + menu klik kanan.
- **Teks terjemahan sama paras dengan teks Arab.** Teks terjemahan kini
  sentiasa bermula pada baris yang sama dengan teks Arab di lajur kiri,
  walau apa keadaan — sebelum ini ia boleh jatuh ke tengah menegak bila
  teks Arab lebih panjang daripada terjemahan.
- **Saiz lalai teks Arab = Kecil** (0.85×) supaya lajur kiri padat dan
  terjemahan kekal separas; butang "Set Semula" dalam Tetapan kembali
  ke saiz ini.
- **Baris "BAHASA MELAYU" + butang 📋 Salin/💬 Kongsi di bawah tab
  dibuang** — paparan bahasa tunggal kini TAB + teks sahaja (tindakan
  kekal di bar tajuk + menu klik kanan).

### Kemas kini 14 Ogos 2026 (masih v1.0) — pengesahan mesin sebenar + tema + RTL

- **4 item tertangguh §8 disahkan pada mesin sebenar** — suite
  pra-hantar penuh, `uji_tersimpan_sebenar` 20/0 (tanda buku SEBENAR),
  `diagnos_syarah` (Fath al-Bari hanyut → Fasa 4B kekal dibatalkan),
  `uji_pipeline_api` 18/0 (API HIDUP, kunci memori sahaja).
- **Sync penuh dari mula** — 62,169 hadis sejajar API (622 muka surat,
  45/45 padan teks), 0 duplikat; `sync_english.py` 31,833 deterministik.
- **Padanan ara-* penuh** — 31,952/32,439 (98.5%) + audit bebas 100%.
- **Audit liputan SemakHadis** — 4,237/62,169 (6.8%), jurang terbesar
  Tafsir 843 (tiada sumber BM per-hadis terbuka).
- **5 tema, semua ≥ WCAG AA** — 🌙 Neutral lalai (gelap neutral) · 📜
  Kertas · ☀ Neutral terang · ☀ Terang · 🌓 Ikut sistem (ikut mod
  Windows, QTimer 2s); semak #13 kontras 72 pasangan dikunci.
- **Susun atur RTL** — Arab di KANAN, terjemahan di KIRI (demi status
  hadis rujukan); semakan geometri + audit dokumen dikunci (semak
  #14, uji_negatif_8z 52/0).
- **Pengukuhan suite** — `gate_pantas.py` (~35s) · pembersihan + semak
  dua hala proses ujian yatim · bandingan piksel Numpy (~13× lebih
  pantas) · semak #12 'Sesi Terakhir' seiring git log.

### Kemas kini 15 Ogos 2026 (masih v1.0) — penutup semak #15

- **Semak #15 semak.py: ringkasan satu muka seiring 'Sesi Terakhir'**
  — ringkasan 'Keadaan projek' di bahagian paling atas MULA_SINI tidak
  boleh ketinggalan (tarikh + kiraan commit mesti sama dengan 'Sesi
  Terakhir'); dikunci `uji_negatif_8z` **52/0 (34 cabang)**.
- **README.md diselaraskan** — 377 semakan (15 bahagian), kiraan mutasi
  52/0 — 34 cabang, komen semak #15.
- **Suite penuh 13/13 SEMUA LULUS (458.5s)** — larian penuh ketiga
  berturut-turut, pengesahan dua hala orphan OK.

### Kemas kini 16 Ogos 2026 (masih v1.0) — reka bentuk halaman utama

- **Kad kitab 100→114px (eksperimen grid)** — dua lajur mustahil dalam
  gate 730px (kad perlu ~50px); varian C 3×3 kekal, kad +14%;
  hero compact + tajuk ketat + jarak grid 6→5. Desc 4 kitab (Bukhari,
  Muslim, Malik, Ahmad) terpotong 2 baris → dipendekkan satu baris
  (DESC_KLIP 0 dalam 5 tema).
- **Border kad ikut warna kitab** — 2px keliling warna kitab (Bukhari
  hijau, Muslim biru, dsb. 9 kitab) + hover cerah/gelap + glow ikut
  warna (`8b760c8`); hover timbul kad diperkuat.
- **Hover timbul dibaiki** — efek pada pembungkus lutsinar bukan kad
  QSS; ranap klik kad dibaiki (efek bayang dibuang sebelum navigasi).
- **Hari ditutup 16 commit** — rekod penuh `PERUBAHAN_16OGOS.md`;
  mutasi uji_negatif dikunci; suite penuh lulus.

### Kemas kini 17 Ogos 2026 (masih v1.0) — responsif penuh + ujian dioptimumkan

- **Pepijat viewport tersekat dibaiki** — selepas `setCurrentIndex`
  atau resize tetingkap, halaman bukan-semasa boleh kekal 640×480
  dalam stack 1024px → kandungan terpotong di kanan. `_paksa_saiz_halaman()`
  (halaman == stack + nudge bila viewport basi <80%; hook resizeEvent
  stack). Diuji 24/24 (6 halaman × 4) pada 1024×600 + DPI 150% — tiada
  skrol mengufuk, skrol papan kekunci/roda/Tab OK (`5d6a786`).
- **Uji_visual_sebenar dioptimumkan (~2× lebih laju)** — gelung
  tangkapan skrin bertukar daripada sleep tetap 0.6s ke **poll stabil**
  (dua grab berturut-turut sama; had 0.6s kekal untuk paparan lambat).
  Bersendirian 143–172s → **71.8s (68/0)**; dalam suite **74.2s**.
  Jumlah suite penuh **485.1s → 401.8s** (13/13 SEMUA LULUS).
- **Galeri 5 tema dikemas ke kad 114px** — `dokumen/imej/tema_{home,detail}_*.png`
  (10 imej) memaparkan reka bentuk halaman utama semasa; galeri
  MANUAL_PENGGUNAAN §3 TEMA otomatis seiring (`6d1f094`).
- **MULA_CEPAT versi pengguna dikemas** — §1 5 tema ≥ WCAG AA + galeri
  visual + paparan responsif (1024×600, DPI 125%/150%); §3 baharu
  'Tukar tema (5 pilihan)'; **§4 baharu 'Penyelesaian masalah (ringkas)'**
  untuk pengguna awam (ikon tiada, kunci API, lambat buka, saiz fon,
  tema Ikut sistem, carian kosong) (`7679ec9` + `e885503`).
- **README '377 semakan' → 391 semakan** — kiraan semak.py semasa
  selepas `_SKIP_FOLDER` prun arkib/venv (16 Ogos) mengubah skop imbas
  (`6b8aeb8`).
- **Hari ditutup 18 commit + 4 langkah-B** — kiraan telus (22 sebenar
  − 4 langkah-B); suite muktamad **387.5s** (rantaian 485.1→401.8→
  387.5s; larian terakhir 453.0s dengan semak #12 tarikh sistem);
  semak #16 kiraan README automatik (392 semakan, 15 bahagian),
  peraturan tarikh sistem dalam semak #12 (rekod tidak mendahului
  tarikh sebenar), uji_negatif **55/0 — 36 cabang**; 3 langkah-B
  pembetulan rekod (c97d028/bb97f42/c5142ef) — rekod hari
  diselaraskan ke jam sistem; rekod penuh
  `dokumen/perubahan/PERUBAHAN_17OGOS.md`; entri 16 Ogos ditambah
  kemudian (`e60a74d`) supaya log versi tiada jurang.

### Kemas kini 18 Ogos 2026 (masih v1.0) — suite 14 ujian + responsif fon besar

- **Ujian #14 responsif viewport didaftar** — `uji_responsif_viewport.py`
  (6 halaman × 4 saiz, DPI 150%) sebahagian suite rasmi (`0a872b0`);
  semak_dokumen_ui A8 mengesahkan 14 ujian; suite penuh pertama
  **14/14 SEMUA LULUS (465.3s)**.
- **Responsif fon besar (aksesibiliti)** — audit saiz fon 120–150%:
  QT_FONT_DPI tidak menjejaskan app (fon px sendiri); `UJI_FONT_SCALE_IDX`
  (FONT_SCALES 0.85–1.5×) sebagai gantian sebenar. Fon 1.3× mula
  75/1 dan 1.5× 74/2 → DIBETULKAN (`19c4a44`): baris tab bahasa
  (Melayu/Indonesia/English), tab ARAB/TRANSLITERASI dan 4 butang
  tindakan kini bungkus ke baris kedua bila sempit; panel ketatkan
  margin bila perlu; **laluan reflow tertangguh** (`_kemas_semua_detail`,
  singleShot 0) menyelesaikan punca sebenar: QStackedWidget tidak
  mengubah saiz halaman tersembunyi jadi render mengira reflow dengan
  geometri basi. Disahkan: semua 5 skala fon @ DPI 150% + DPI
  100/125/175% = **76/0**; mockup 130/0; sebenar 68/0; bandingan 55/0.
- **Bar 'Lapor ralat | Kongsi | Salin' SEBARIS** (`4e16fdf`) —
  regresi wordWrap membuat bar membalut ke 4 baris pada semua saiz;
  dibetulkan: wordWrap dibuang + bar dipindah ke aras panel (lebar
  penuh) — sebaris 476×20 + hbar 0 semua saiz/DPI.
- **Audit lebar minimum** (`--minlebar` dalam uji_responsif_viewport)
  — semua 6 halaman = 900px (lantai tetingkap app) pada DPI 150% +
  fon 1.5×; tiada titik pecah dalam julat disokong.
- **Audit kiraan + pendaftaran buka_hari.py (komit 10)** — semak
  #9 `buka_hari.py` (skrip buka rekod 19 Ogos) didaftar dalam
  `DIBENARKAN_UNTRAKCED`; kiraan semakan 393→**394** (README +
  mutasi #35 diselaraskan); audit semua kiraan 18 Ogos merentas 4
  dokumen konsisten dengan git log; guard buka_hari.py dinamik.
- **Hari ditutup 8 commit kerja + 2 langkah-B** (10 sebenar − 2) —
  suite muktamad **14/14 SEMUA LULUS (420.4s)** selepas pembetulan
  bar; 4 baseline PNG dikemas (kesan visual bar sebaris); rekod penuh
  `dokumen/perubahan/PERUBAHAN_18OGOS.md`.

### Kemas kini 19 Ogos 2026 (masih v1.0) — 2 tema Neutral + disclaimer + Tentang table

- **Tema dikurangkan kepada 2 Neutral** (`b292515`) — gelap + terang
  sahaja; Kertas/Terang/Ikut sistem dibuang; butang 'Saiz antara
  muka' dibuang dari panel Tetapan; `semak_dokumen_ui` 110→109.
- **Carian nombor hadis pada halaman kitab buka detail terus**
  (`b292515`) — tiada lagi senarai perantara.
- **Dialog disclaimer setiap larian** — `ui/disclaimer.py` baharu;
  papar SEBELUM splash (fix pythonw.exe: `setQuitOnLastWindowClosed
  (False)` + 200ms delay, `6c9f855`); selepas muat model pada mulanya
  (`e6d867b`); tajuk splash/disclaimer/header disepadankan (Pustaka
  bold teal + Hadis light teal + v1.0).
- **Tentang Pustaka Hadith table** (`5dd6990`) — QTableWidget 2 lajur
  untuk Kandungan + Sumber dan atribusi; grid line, padding, warna
  tema; hyperlink pautan HTML dalam sel.
- **Gate semak.py dibaiki** — semakan atribusi 8aa diselaraskan ke
  format jadual Tentang (label sel kiri + nama sumber vs DEKLARASI.md
  ayat penuh); kiraan semakan diselaraskan ke **394** (README +
  ringkasan MULA_SINI + mutasi #35); mutasi #27/#30/#34/#36 disasarkan
  semula ke 19 Ogos; `PERUBAHAN_19OGOS.md` dicipta (log harian belum
  wujud).
- **Hari dibuka semula — 5 commit kerja** (penutup `55c17f4` tidak
  dikira); gate: semak.py 394 semakan SEMUA LULUS · uji_negatif_8z
  55/0 · semak_dokumen_ui 109/0.

## 1.3 — 7 Ogos 2026

Ditanda pada `760e71b` (Sesi 28). Ciri utama era 1.3 (Sesi 28–53):

- Skrin pemula (splash) dengan fasa pramuat + bar kemajuan.
- Salin/Kongsi semua bahasa — petikan Arab penuh + terjemahan bahasa
  semasa; kongsi WhatsApp.
- Lompat terus ke hadis (`bukhari 433`, `B433`, `Ctrl+G`) + kotak
  Pergi.
- Indikator carian: jam berputar 🕐→🕛 semasa carian kata kunci.
- Simbol selawat ﷺ lalai dalam paparan Melayu + transliterasi rumi.
- Lalai saiz fon "Sederhana" (antara muka, Arab, terjemahan).
- Butang ↑ terapung + kotak carian nombor hadis pada senarai kitab.
- Refactor Sesi 30: `app_qt.py` (2,428 → 504 baris inti) dipecah ke
  mixin `ui/pages_*.py`.
- Ujian visual skrin sebenar (6 fail) + semakan statik semak.py.

## 1.2 — 7 Ogos 2026

Ditanda pada `cb8f766`. Ciri utama:

- Fallback OR carian kata kunci bila FTS5 AND 0 hasil + pembobotan
  ranking (hadis dengan SEMUA perkataan di atas).
- Mesej bantuan bila kata kunci tiada hasil.
- Pengesahan visual + ujian penuh tema.

## 1.1 — 7 Ogos 2026

Ditanda pada `c3249bf`. Ciri utama:

- Integrasi HadeethEnc sebagai sandaran huraian (atribusi IslamHouse).
- Ujian UI + dokumentasi Sesi 22 (git, sync data).

## 1.0 — 7 Ogos 2026

Ditanda pada `2970234` (komit pertama). Keluaran pertama Pustaka
Hadis Hadith: koleksi kitab hadis lengkap, carian kata kunci FTS5 + carian
semantik FAISS, huraian SemakHadis/syarah, tema gelap/terang,
penanda buku (Tersimpan), tetapan bahasa + saiz fon, cap versi
`VERSI.py`.

## Nota

- Versi dinaik taraf melalui `VERSI.py` sahaja; semakan `semak.py`
  seksyen 10 membaca cap itu secara dinamik.
- "1.0" kini muncul dua kali: keluaran pertama (7 Ogos) dan edaran
  semasa (11 Ogos, ditetapkan semula dari 1.3).
