# Perubahan 18 Ogos 2026

> Log ringkas perubahan pada 18 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md`. Versi apl kekal **1.0**.

## Kandungan sesi

- **Komit 1 — Buka rekod 18 Ogos.** Hari baharu dibuka selepas
  penutup penuh 17 Ogos (18 commit + 4 langkah-B, 22 sebenar − 4;
  komit penutup `6f8f1b8` difinalkan dalam baris langkah-B keempat).
  Pembukaan rekod:

  1. **sesi_index.md** — seksyen **SESI 18 OGOS 2026 (komit 1,
     sambungan 17 Ogos)** ditambah selepas PENUTUP HARI 17 Ogos;
     kiraan telus dikemas: 18 Ogos = **1 commit** (1 sebenar − 0
     langkah-B).
  2. **PERUBAHAN_18OGOS.md** — fail log harian baharu ini.
  3. **MULA_SINI.md** — 'Sesi Terakhir' → **18 Ogos 2026 (komit 1)** +
     ringkasan satu muka → **1 commit pada 18 Ogos** (sambungan 18
     commit 17 Ogos + 16 commit 16 Ogos + 36 commit 14 Ogos + 14
     commit 15 Ogos); pautan log harian → PERUBAHAN_18OGOS.md.
  4. **uji_negatif_8z.py** — mutasi #27/#30/#34/#36 disasarkan semula
     ke 18 Ogos (tajuk, intro "Kerja 18 Ogos", kiraan ringkasan,
     tarikh masa depan).

  Gate: semak.py SEMUA LULUS (16 semakan, #12/#14/#15/#16 hijau —
  #12 peraturan tarikh sistem: tajuk 18 Ogos tidak mendahului tarikh
  sistem 18 Ogos) · uji_negatif_8z **55/0** · semak_dokumen_ui
  110/0 · pokok kerja bersih.

- **Komit 2 — Audit konvensyen langkah-B (14–17 Ogos).** Setiap
  kiraan telus hari dibandingkan dengan git log sebenar (tarikh
  komit git). Dapatan:

  1. **14 Ogos = 36 commit** (44 sebenar − 8 langkah-B) — konsisten;
     44 komit bertarikh 14 Ogos dalam git, 8 komit MULA_SINI sahaja
     (kunci 'Sesi Terakhir') tidak dikira.
  2. **15 Ogos = 14 commit** (14 sebenar − 0 langkah-B) — konsisten;
     komit penutup 15 Ogos (`5c28571`) dibuat pada 16 Ogos dan dikira
     sebagai komit 1 hari 16 (didokumen dalam kiraan telus 16 Ogos).
  3. **16 Ogos = 16 commit** — TIDAK KONSISTEN sebelum ini: jadual
     kata "16 sebenar − 0 langkah-B" sedangkan git ada **18 komit**
     bertarikh 16 Ogos. Dua komit rekod sahaja tidak direkod:
     `f8dd057` (penutup sementara 13 commit) dan `2cb76b8` (rekod
     border warna kitab). DIBETULKAN → **18 sebenar − 2 langkah-B =**
     **16 kerja**; baris L ditambah dalam sesi_index PENUTUP 16 Ogos
     dan PERUBAHAN_16OGOS; kiraan telus dikemas di 3 lokasi.
  4. **17 Ogos = 18 commit** (22 sebenar − 4 langkah-B: `c97d028`,
     `bb97f42`, `c5142ef`, `6f8f1b8`) — konsisten, senarai langkah-B
     eksplisit.
  5. **18 Ogos = 2 commit** (2 sebenar − 0 langkah-B) — komit ini
     sendiri.

  Gate: semak.py SEMUA LULUS (393 semakan, #12/#15/#16 hijau) ·
  uji_negatif_8z **55/0** · semak_dokumen_ui 110/0 · pokok bersih.

- **Komit 3 — Ujian responsif viewport penuh (6 halaman × 4 saiz,
  DPI 150%) + pembetulan tajuk responsif detail.** Ujian baharu
  `uji_responsif_viewport.py` (offscreen, `QT_SCALE_FACTOR=1.5`,
  4 saiz 900×560..1366×768) mengesahkan pembetulan `_paksa_saiz_halaman`
  STABIL selepas tutup hari: halaman == saiz stack, viewport tidak
  tertinggal 640×480, hbar 0, DESC_KLIP 0, tiada ranap — 24 kombinasi
  halaman+saiz + 4 lulusan resize sahaja = **76/0**.

  Ujian MENDEDAHKAN dua kegagalan nyata (bukan regresi pembetulan
  viewport — itu stabil): panel dua lajur detail melimpah mendatar
  pada 900×560 (hbar 254) dan 1024×600 (hbar 130) @ DPI 150% — teks
  Arab (lajur kanan, RTL) terpotong oleh hbar tersembunyi. Punca
  (diukur): `tajuk_bar` satu baris (tajuk + 4 butang tindakan) mahu
  ~1210px, dan bar teks `Lapor ralat | Kongsi | Salin` mahu ~476px —
  kedua-duanya melebihi viewport kecil @ DPI 150%.

  **Pembetulan (ui/pages_detail.py):**

  1. `_kemas_tajuk_detail()` — baris tajuk RESPONSIF: lebar luas →
     satu baris (reka bentuk asal), lebar sempit → tajuk baris
     pertama (membalut) + butang baris kedua (kanan). Butang dipindah
     antara dua baris via addWidget auto-reparent; ambang DINAMIK
     (sizeHint tajuk + butang vs lebar tersedia dalam centered_column)
     jadi ikut DPI/fon secara automatik. Dipanggil pada render +
     resizeEvent `_detail_sa`.
  2. Bar teks `barTindakan` — `setWordWrap(True)` + `setMinimumWidth(0)`
     supaya lajur terjemahan boleh menguncup di bawah 476px.

  **Pengesahan:** uji_responsif_viewport **76/0** DPI 150% (dua baris
  @ 900/1024, satu baris @ 1240/1366 — tiada klip tajuk, hbar 0) +
  DPI 100% (tiada regresi susun atur lalai) · uji_visual_mockup
  130/0 (larian 2–3; larian 1 128/2 flak RDP persekitaran) ·
  uji_visual_sebenar **68/0** · semak.py 393/15 · uji_negatif_8z
  55/0 · semak_dokumen_ui 110/0.

- **Komit 4 — Suite rasmi 14 ujian + DPI 125%/175%.**
  `uji_responsif_viewport.py` didaftar sebagai **ujian #14** dalam
  `uji_pra_hantar.py` (7.2s dalam suite) — ujian responsif viewport
  kini sebahagian suite rasmi, bukan skrip kendiri. Perubahan:

  1. **uji_pra_hantar.py** — entri #14 + docstring (76/0).
  2. **semak_dokumen_ui.py** — semakan A8 "Suite pra-hantar 14 ujian"
     (13 → 14, mengesahkan kehadiran uji_responsif_viewport.py).
  3. **uji_responsif_viewport.py** — `QT_SCALE_FACTOR` boleh ganti
     (setdefault, lalai 1.5) + header mencetak DPI sebenar.
  4. **DPI 125% dan 175%** — kedua-dua **76/0**: ambang dinamik
     `_kemas_tajuk_detail` (sizeHint vs lebar tersedia) berfungsi
     merentas penskalaan, tiada klip tajuk/hbar.
  5. **Dokumen diselaraskan** — README (14 ujian − 13 suite),
     MULA_CEPAT (jadual), MANUAL_REFERENSI_DEV (3 sebutan),
     MULA_SINI (status 14/14 + ringkasan + blok 'Sesi Terakhir'),
     sesi_index (baris 4 + kiraan telus 4 commit), mutasi uji_negatif
     #30/#34 (3 → 4 commit).

  **Suite penuh muktamad: 14/14 SEMUA LULUS (465.3s)** — ujian #14
  7.2s; uji_visual_sebenar 105.8s; bina_tangkapan 33.2s; semak.py
  18.9s; uji_negatif 29.8s; dokumen_ui 9.8s. Tema pengguna dipulihkan
  ke `sistem` selepas suite (quirk suite).

- **Komit 5 — Audit fon besar + bungkusan responsif tab/butang.**
  Uji susun atur dengan saiz fon diperbesar (cth. 120%):

  1. **Pendekatan** — `QT_FONT_DPI` terbukti TIDAK menjejaskan app
     ini (semua saiz fon ditetapkan sendiri dalam px stylesheet, bukan
     fon sistem — diukur: h2 sizeHint 378×45 sama pada DPI 96 dan
     115). Gantian sebenar: `UJI_FONT_SCALE_IDX` (indeks FONT_SCALES
     [0.85, 1.0, 1.15, 1.3, 1.5] sedia ada) — ujian menampal
     `_read_json` DALAM INGATAN sahaja, fail user_settings.json tidak
     disentuh.
  2. **Dapatan** — fon 1.15×: 76/0 lulus. Fon 1.3×: **75/1** (hbar 8
     @ 900×560). Fon 1.5× (maksimum): **74/2** (hbar 133/122 @
     900/1024).
  3. **Punca** — pengikat lebar minimum pada fon besar: bar tab
     bahasa (LangTabs ~426px), tab ARAB/TRANSLITERASI (~319px), baris
     4 butang tindakan (~842px @ 1.5×), dan margin panel 24/18 —
     kesemuanya tidak boleh mengecut di bawah teks butang.
  4. **Pembetulan (corak sama `_kemas_tajuk_detail`):**
     - `LangTabs.kemas_lebar(lebar)` (ui/pages.py) — tab bungkus ke
       baris kedua bila lajur sempit (idempoten, butang dipindah
       antara layout).
     - `_kemas_tab_arab(lebar)` — ARAB/TRANSLITERASI bungkus ke baris
       kedua (masih kanan, cermin RTL).
     - `_kemas_butang_tindakan(lebar)` — 4 butang tindakan bungkus
       2+2 bila baris tidak muat.
     - `_kemas_panel_detail()` — ketatkan margin panel 24/18+18 →
       16/12+10 bila masih sempit.
     - **`_kemas_semua_detail()` (laluan reflow tertangguh)** —
       QTimer.singleShot(0) menjalankan reflow SELEPAS halaman
       dipaparkan. Punca sebenar flak 50%: QStackedWidget tidak
       mengubah saiz halaman tersembunyi, jadi `_render_detail`
       mengira reflow dengan geometri BASI (viewport besar dari saiz
       init) — baris tab/butang tidak membungkus walaupun saiz sebenar
       sempit; resizeEvent tidak selalu tiba. Laluan kedua selepas
       paparan menyelesaikan (6/6 larian stabil @ 1.5×).
  5. **Regresi dijumpai & dibaiki** — semasa mockup, tab 3 bahasa
     HILANG (mockup 126/4, dikesan juga oleh pengguna): tulis semula
     LangTabs memulakan `_n_baris1 = len(butang)` jadi `kemas_lebar`
     pertama pulang awal TANPA membina baris — butang wujud tetapi
     tidak dalam layout. Dibetulkan `_n_baris1 = 0` → mockup kembali
     **130/0**.
  6. **Pengesahan penuh** — semua 5 skala fon (0.85/1.0/1.15/1.3/
     1.5×) @ DPI 150% = **76/0** · DPI 100/125/175% = 76/0 ·
     uji_visual_mockup **130/0** · uji_visual_sebenar **68/0** ·
     uji_bandingan **55/0** · semak.py 393/15 · uji_negatif 55/0 ·
     semak_dokumen_ui 110/0.

- **Komit 6 — Tutup hari (langkah-B).** Baris 5 difinalkan
  (`19c4a44`); kiraan telus 18 Ogos → **5 kerja + 1 langkah-B**
  (6 sebenar − 1, komit ini sendiri). **Suite penuh muktamad: 14/14
  SEMUA LULUS (438.0s)** selepas komit 5 (responsif 7.0s, sebenar
  58.1s, piksel 98.1s, semak 16.3s, negatif 24.8s, dokumen_ui 9.7s).
  CHANGELOG entri 18 Ogos ditambah (log versi seiring log harian);
  MULA_SINI 'Sesi Terakhir' + ringkasan → **5 commit kerja + 1
  langkah-B** (sambungan 18 commit 17 Ogos + 16 commit 16 Ogos + 36
  commit 14 Ogos + 14 commit 15 Ogos); tema pengguna dipulihkan ke
  `sistem` selepas suite.

- **Komit 7 — Bar 'Lapor ralat | Kongsi | Salin' SEBARIS (selepas
  penutup, rekod dibuka semula).** Regresi komit 3/5: `wordWrap` +
  `setMinimumWidth(0)` membuat label QLabel tersekat pada 153px (saiz
  bergantung lebar semasa → titik tetap sempit) → bar membalut ke 4
  baris pada SEMUA saiz tetingkap dan DPI (dilaporkan pengguna).
  Dibetulkan: wordWrap dibuang (label kekal lebar semula jadi) dan bar
  dipindah dari dalam lajur terjemahan ke **aras panel** — lebar penuh
  di bawah dua lajur, jadi ia sentiasa muat sebaris. Struktur panel
  dikemas: VBox luar `pva` [lajur HBox + bar]; `_kemas_panel_detail`
  sasarkan `pva`, jarak lajur dibaca dari `_panel_lajur`. Disahkan:
  bar 476×20 sebaris + hbar 0 pada semua saiz (900–1366) × DPI
  100/150% · uji_responsif 76/0 semua skala fon · mockup 130/0 ·
  bandingan 55/0 · sebenar 68/0 · semak 393/15.

- **Komit 8 — Audit lebar minimum per halaman.** Mod `--minlebar`
  dalam `uji_responsif_viewport.py`: carian binari [900, 1400] lebar
  tetingkap terkecil bagi setiap 6 halaman yang masih tanpa skrol
  mengufuk tersembunyi (hbar == 0 + halaman == stack). Keputusan pada
  DPI 150% DAN DPI 150% + fon 1.5×: **semua 6 halaman = 900px** (lantai
  `setMinimumSize` app) — **TIADA titik pecah dalam julat disokong**;
  responsif lengkap 900→1366 selepas pembetulan komit 3–7.
  Penggunaan: `QT_SCALE_FACTOR=1.5 python uji_responsif_viewport.py
  --minlebar`.

- **Komit 9 — Baseline tangkapan + pengesahan muktamad (langkah-B
  #2).** Suite penuh selepas pembetulan bar: larian pertama GAGAL
  baseline `detail_terang_nasai4934.png` (nmad 0.026, bilang 7.17% —
  dijangkakan: bar kini sebaris di aras panel = perubahan visual);
  baseline dikemas `--kemas` (4 PNG detail). Larian kedua GAGAL
  transien semak 8j: muat cache 63.6s > 60s — OUTLIER persekitaran
  (7 larian sebelumnya 21–37s; import ST 51.7s di bawah beban), ukuran
  baharu **35.9s** kembali normal. Larian ketiga: **14/14 SEMUA LULUS
  (420.4s)**. Baseline dikemas (4 PNG) — kesan visual bar sebaris.

- **Komit 10 — Audit kiraan 18 Ogos + pendaftaran buka_hari.py
  (kerja #8).** Semak #9 mendapati `buka_hari.py` (skrip satu arahan
  buka rekod 19 Ogos) untracked → kiraan semakan 393→392 → semak
  #16 gagal. Dibetulkan: `buka_hari.py` didaftar dalam
  `DIBENARKAN_UNTRAKCED` (fail sah belum di-commit — konvensyen
  skrip baharu seperti uji_pra_hantar.py dahulu); kiraan semakan
  naik ke **394** → README + mutasi #35 diselaraskan (394→391).
  Audit penuh semua kiraan 18 Ogos merentas sesi_index / MULA_SINI /
  CHANGELOG / PER18: konsisten dengan git log (10 sebenar − 2 = 8
  kerja + 2 langkah-B); sebutan lama (5 kerja + 1 langkah-B, 15 Ogos
  13 commit, 393 semakan) disahkan sejarah sah. `buka_hari.py`
  dikemas: guard tarikh dinamik (bukan hash keras), kiraan 7→8.
  Gate: semak.py **394 semakan (15 bahagian) SEMUA LULUS** ·
  uji_negatif_8z **55/0** · semak_dokumen_ui 110/0.

## Status — HARI DITUTUP

18 Ogos DITUTUP — **8 commit kerja + 2 langkah-B** (10 sebenar − 2;
`a39f885` penutup + `c10986e` baseline; komit 7/8/10 selepas penutup,
rekod dibuka semula). Kiraan telus: 14 Ogos = 36 commit ·
15 Ogos = 14 commit · 16 Ogos = 16 commit (18 sebenar − 2 langkah-B)
· 17 Ogos = 18 commit (22 sebenar − 4 langkah-B) · 18 Ogos =
8 commit kerja + 2 langkah-B.
