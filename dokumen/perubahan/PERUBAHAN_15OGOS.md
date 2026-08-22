# Perubahan 15 Ogos 2026 — README diselaraskan + suite penuh akhir

> Log ringkas perubahan pada 15 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md` (entri "Penutup malam
> (15 Ogos)"). Versi apl kekal **1.0**.

## Kandungan sesi

- **README.md diselaraskan seiring semak #15** — kiraan
  `uji_negatif_8z` `45/0 — 30 cabang` → `52/0 — 34 cabang`;
  `370+ semakan` → `377 semakan (15 bahagian)`; komen semak.py
  kini sebut semak #15 ringkasan satu muka.
- **Suite penuh 13/13 SEMUA LULUS (458.5s)** — larian penuh ketiga
  berturut-turut dalam satu arahan; "OK tiada proses ujian yatim selepas
  suite". Pecahan: semak 19.6s · negatif 9.4s · mockup 33.4s · piksel
  66.2s · sebenar 137.7s · tukar_tema 66.6s · bandingan 7.9s · lompat
  6.2s · e2e 40.9s · baseline 29.0s · draf 1.9s · tersimpan 26.1s ·
  dokumen_ui 10.3s.
- **MULA_SINI 'Sesi Terakhir' + ringkasan dikemas ke 15 Ogos** — hari
  baharu bermula; kiraan 15 Ogos naik seiring komit kerja; kunci
  mutasi #30/#34 diselaraskan.
- **Tangkapan muktamad sistem + RTL** — app pada skrin sebenar, tema
  "sistem" → neutral; RTL Arab@(624,275) KANAN vs Terjemahan@(110,275)
  KIRI; 10/10 semakan; palet sepadan galeri (nmad 3.0–7.0).

## Kiraan commit

- 14 Ogos: **36 commit** (11 teras + 25 susulan; 44 sebenar − 8
  langkah-B).
- 15 Ogos setakat ini: **10 commit** (`250216d` + `3b81235` + komit
  penutup kiraan + CHANGELOG + rekod pengesahan + penutup hari +
  suite/saiz galeri + skaf 16 Ogos + ujian hidup muktamad + penutup
  hari rekod penuh 10 + plan edaran — kerja sebenar; langkah-B
  seterusnya tidak dikira).

## Gate

- semak.py SEMUA LULUS (15 semakan, #12 + #15 hijau) · uji_negatif_8z
  **52/0** · pokok kerja bersih.
## Susulan: suite penuh + pemeriksaan saiz galeri

- **Suite penuh 13/13 SEMUA LULUS (478.7s)** — larian penuh keempat
  berturut-turut dalam satu arahan, pengesahan dua hala orphan OK.
- **Pemeriksaan saiz galeri tema**: keputusan — **TIADA tangkapan
  semula perlu**. Galeri `dokumen/imej/tema_*.png` (1116×788) dirakam
  pada saiz tetingkap RASMI tetap `w.resize(1100, 780)` (bukan skrin
  penuh); saiz skrin pengguna berbeza-beza jadi tiada saiz sepadan
  universal. `bina_tangkapan` (ujian #10) lulus **7/7 sepadan baseline**
  — kod semasa konsisten; pengesahan muktamad palet nmad 3.0–7.0.
  Menangkap semula hanya menukar saiz tanpa nilai tambah.
## Susulan: ujian hidup muktamad (tema sistem + RTL) 3/3

- **App dibuka pada mesin sebenar** — `PustakaApp`, tema `sistem`
  (Windows gelap → **Neutral**, PAGE_BG `#1F1F1F`); hadis `bukhari 1`
  dibuka terus; tangkapan `bukti_visual/sah_hidup_final_{home,detail}.png`.
- **RTL pada widget fizikal**: Arab@(554,275) di KANAN vs
  Terjemahan@(104,275) di KIRI — baris sama (y=275) ✓
- **Palet neutral tulen** (sisihan RGB 0.9 < 25) pada home + detail ✓
- **Seiring galeri**: beza palet-skala home 5.1 / detail 8.4
  (dalam julat jangkaan 3–9 — hadis berbeza dipaparkan, saiz
  1100×749 vs galeri 1116×788) ✓
- Tiada kod diubah — app berfungsi seperti disahkan; skrip ujian
  sementara dibuang selepas larian.
## Penutup hari 15 Ogos — rekod penuh 10 commit + audit §8 + plan edaran

- **Audit baki tertangguh §8 (task 2)** — disahkan TIADA item baharu
  diperlukan sebelum pengedaran: item 1–6 DITUTUP 14 Ogos; #7 kunci
  API kekal AKTIF sengaja; #8 liputan SemakHadis ialah siling (audit
  penuh, tiada sumber BM terbuka lain). Jurang Tafsir 843 dipantau.
  Aplikasi SIAP & DISAHKAN untuk langkah pengedaran.
- **Plan bina versi edaran (task 3) — dokumentasi DAHULU, tiada
  binaan** — `dokumen/rujukan/PLAN_BINA_EDARAN.md` baharu untuk
  semakan pengguna: pengesahan reka bentuk INSTALLER.md terhadap kod
  semasa (15 Ogos — semua andaian masih sah: config.py/ui.helpers.py
  guna BASE_DIR, indeks FAISS + model + app.ico ada), keputusan
  reka bentuk, 7 fasa pelaksanaan dengan gate, kaedah & perkakas
  (Nuitka, venv bersih, Inno Setup, GitHub Releases), risiko &
  mitigasi, dan keputusan yang diperlukan pengguna sebelum mula
  (sahkan plan, saiz pilihan C, akaun GitHub, ZIP mudah alih).
- **Gate:** semak.py SEMUA LULUS · uji_negatif_8z 52/0 · kunci mutasi
  #30/#34 diselaraskan ke 10 commit · pokok kerja bersih.

## Susulan 15 Ogos — Gabung ZIP Pembetulan Luaran (①–④)

- **Latar:** pengguna membawa `Pustaka_Hadis_Pembetulan_Lengkap/` (ZIP
  pembetulan 13–15 Ogos dari Drive). Perbandingan: 1/6 pembetulan kod
  sudah wujud di root (draft_answer), 4 belum (RandomWorker,
  SemanticWorker, _page_settings, diakritik), skema 8 belum.
- **Digabung (keputusan "buat 1 ~ 4"):**
  ① RandomWorker `str(e)` → `terjemah_ralat(e)` (ui/workers.py);
  ② SemanticWorker → kelas `_Base` di ui/workers.py + import dalam
  pages_carian.py (closeEvent comment dikemas; semak_dokumen_ui E5
  diselaraskan);
  ③ `_page_settings` dibuang dari `_build()` (ui/app_qt.py);
  ④ `_DIAKRITIK` + `\u0610-\u0614` (core/eng_source.py) — audit
  audit_eng.py --semua: 30,547/30,541/6, identik GTAF §6b.
- **Status:** ditanda dalam list-we-do.md seksyen K (5 DIGABUNG, 3
  BELUM). Folder ditambah .gitignore + _SKIP_FOLDER semak.py (bahan
  luaran 12MB — kod pendua + OCR cache; bukan kod projek).
- **Gate:** semak.py SEMUA LULUS · uji_negatif_8z 52/0 · semak_dokumen_ui
  110/0 · gate_pantas SEMUA LULUS · uji_data_baharu 18/18 · mockup
  130/0. Kiraan 15 Ogos = **12 commit**; mutasi #30/#34 diselaraskan.

## Susulan 15 Ogos — Gabung Skema 8 + Dokumen Audit (⑤⑥, komit ke-13)

- **Latar:** kesinambungan gabung ZIP (①–④ komit ke-11/12). Pengguna
  mengarahkan "semua" — baki penggabungan dilaksanakan.
- **⑤ Skema 8 + `arab_carian` (carian Arab tanpa tashkeel):**
  - diff bersih disahkan: folder `db.py`/`sync.py` = root + skema 8
    sahaja (tiada percabangan lain) → port terus.
  - `db.py`: `SKEMA_VERSI=8`, `bersih_tashkeel()`, kolum `arab_carian`,
    FTS5 indeks `arab_carian`, trigger dipindah ke `_backfill_arab_carian()`
    (elak "no such column" pada DB lama), self-heal migrasi terganggu,
    normalisasi query `_to_match_query()`.
  - `sync.py`: `simpan()` isi `arab_carian` bagi rekod baharu.
  - `uji_carian_arab.py` disalin dari ZIP + dijalankan pada SALINAN
    konsisten DB sebenar (SQLite Backup API, DB asal baca sahaja):
    **SEMUA LULUS (74.67s)** — 62,169 hadis, skema 8, 0 NULL, 3 trigger,
    `كتب`=`كَتَبَ` 767 · `نية`=`نِيَّة` 10 · `الله`=`اللَّهِ` 60,211 ·
    regresi BM `niat`/`puasa`/`hukum riba` 115/911/486 · trigger
    INSERT/UPDATE/DELETE lulus.
  - **Migrasi produksi:** backup `hadis.db.sebelum_carian_arab.bak`
    (gitignored) → `db.init()` → versi 8, arab_carian 0 NULL →
    `semak_db.py` JUMLAH 62,169 → carian sebenar `كتب`=767,
    `نِيَّة`=10, `niat`=115, `puasa`=911.
- **⑥ Dokumen audit disalin** ke `dokumen/audit/`: GTAF.md,
  AHMAD_DIGITAL.md, AHMAD_HOCR.md, AHMAD_HOCR_SAMPEL_5.json,
  TERJEMAHAN_AHMAD_DARIMI.md, CARIAN_ARAB.md + `dokumen/rujukan/`:
  DRAF_carian_arab.md, PERMOHONAN_LESEN_AHMAD.md. Satu kata Indonesia
  dalam AHMAD_HOCR.md dibetulkan ke Melayu Malaysia (semak 8m).
- **Status list-we-do.md:** #9/#10 skema 8 + dokumen audit ditanda
  DIGABUNG; INSTALLER.md kekal BELUM (PLAN_BINA_EDARAN.md projek utama
  sudah menggantikannya sebagai pelan semasa).
- **Gate:** semak.py SEMUA LULUS · uji_negatif_8z 52/0 · semak_dokumen_ui
  110/0 · gate_pantas SEMUA LULUS (32.4s) · uji_data_baharu 18/18 ·
  mockup 130/0. Kiraan 15 Ogos = **13 commit**; mutasi #30/#34
  diselaraskan. Sisa: INSTALLER.md perbandingan (pelan edaran baharu
  sudah ada), langkah-B #7 kunci API.

## Susulan 15 Ogos — Ujian hidup carian Arab + suite penuh + banding INSTALLER (komit ke-14)

- **Ujian hidup app (tema sistem):** carian Arab tanpa tashkeel di UI
  SEBENAR disahkan 9/9 — `كتب`=767 (sama dengan `كَتَبَ`), `نية`=10,
  `puasa`=911, tema sistem→Neutral. Tangkapan: bukti_visual/carian_arab_*.
  Skema 8 berfungsi hujung-ke-hujung dalam app.
- **Suite penuh 13/13 SEMUA LULUS (502.1s)** — dengan skema 8 hidup:
  semak 22.6s · negatif 13.0s · mockup 42.3s · piksel 68.2s · sebenar
  155.0s · tukar_tema 71.3s · bandingan 10.7s · lompat 6.8s · e2e 41.4s
  · baseline 29.4s · draf 1.8s · tersimpan 26.4s · dokumen_ui 10.0s +
  "tiada proses ujian yatim selepas suite".
- **Perbandingan INSTALLER.md (dua versi):** `dokumen/rujukan/
  BANDING_INSTALLER.md` baharu — ZIP (15 Ogos, 897 baris) = PyInstaller
  6.22 + MSIX/Store; projek utama (11 Ogos, 590 baris + PLAN 15 Ogos) =
  Nuitka + GitHub Releases. Persamaan disahkan: %LOCALAPPDATA%, hadis.db
  tidak dibundel, x64, tiada sijil. Nilai ZIP (masalah lazim §17, checklist
  §18, urutan §19, ujian naik taraf §16) dikenal pasti untuk diserap ke
  Fasa 2. **Alat bina = keputusan terbuka** — uji diagnostik kedua-duanya,
  jangan kunci berdasarkan dokumen. list-we-do.md: INSTALLER.md ditanda
  DIBANDINGKAN.
- **Gate:** suite penuh 13/13 · gate_pantas SEMUA LULUS. Kiraan 15 Ogos =
  **14 commit**; mutasi #30/#34 diselaraskan.

## Penutup hari 15 Ogos — rekod penuh 14 commit (penutup akhir)

- **Hari ditutup dengan rekod penuh** — **14 commit** (14 sebenar − 0
  langkah-B; komit rekod penutup 15 Ogos ini ialah komit pertama
  16 Ogos — hari 16 Ogos bermula dengan rekod penutup ini). Kiraan semua
  dokumen diselaraskan ke 14: MULA_SINI ringkasan == 'Sesi Terakhir'
  intro (semak #15 hijau); mutasi #30/#34 kekal sasarkan 14; rujukan
  lain (12/13 commit) ialah sejarah berketarikh — kekal.
- **Rekod penuh dalam sesi_index** — seksyen `PENUTUP HARI — 15 Ogos
  2026 (14 commit)` dengan jadual 14 baris: README diselaraskan
  (`250216d`) → Sesi Terakhir 15 Ogos (`3b81235`) → kiraan 3 + mutasi
  (`e205db3`) → CHANGELOG (`3ad97c5`) → pengesahan muktamad RTL
  (`dcd85aa`) → penutup 6 (`07f2b0f`) → suite 478.7s + saiz galeri
  (`d0dd727`) → skaf 16 Ogos + pintasan (`829bc08`) → ujian hidup RTL
  3/3 (`837c53d`) → penutup 10 + plan edaran (`79617fe`) → gabung ZIP
  ①–④ (`329bbbb` + `20a2f11`) → gabung skema 8 + audit (`45a1813`) →
  ujian hidup carian Arab + suite 13/13 + banding INSTALLER (`da1834c`).
- **Status Fasa 2 (bina diagnostik, tidak dikira):** PyInstaller siap di
  disk (app dibuka tanpa crash; `main.py` tiada `freeze_support()`);
  bina Nuitka BELUM — ditangguh. Alat bina kekal TERBUKA
  (BANDING_INSTALLER.md).
- **Gate akhir:** semak.py SEMUA LULUS · uji_negatif_8z 52/0 ·
  semak_dokumen_ui 110/0 · gate_pantas SEMUA LULUS · pokok bersih ·
  tema "sistem" · kiraan 15 Ogos = **14 commit**.
