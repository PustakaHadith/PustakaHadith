# Log Sejarah Pembangunan — PustakaHadith

**Dokumen induk sejarah perjalanan pembuatan projek** (project development journey).
Semua perbincangan, keputusan dan perubahan direkodkan di sini secara beransur;
butiran harian lengkap berada di `dokumen/perubahan/PERUBAHAN_*.md` dan
`dokumen/sesi/sesi_index.md`. Fail ini adalah titik masuk (entry point) untuk
memahami keseluruhan perjalanan projek.

---

## 0. Profil Projek

- **Nama:** PustakaHadith — aplikasi desktop Windows berbahasa Melayu untuk
  pembacaan, carian dan kajian hadis.
- **Platform:** PyQt5 (Python 3.14), SQLite + FTS5, FAISS (carian semantik).
- **Pemilik / pembangun:** MUHAMAD KHAIRULLAH ABDUL WAHAB (PustakaHadith).
- **Sumber data:** API awam `https://service.hadis.my/api/v1` (hadis.my) +
  terjemahan Inggeris dari CDN Sunnah.com.
- **Sasaran edaran:** Microsoft Store (Fasa 5–7) + Setup EXE (Inno Setup).
- **Status semasa (27 Ogos 2026):** v1.0.0 — MSIX & Setup EXE sedia; menunggu
  kebenaran hadis.my sebelum bundel data ke dalam installer.

---

## 1. Fasa Awal — Reka Bentuk & Pembangunan Teras

- Pembinaan UI/UX asal, struktur tetingkap, navigasi kitab, carian, pemetaan
  kitab (sunnah_map), profil pembaca.
- Penyediaan pangkalan data `hadis.db` (muat turun + penyegerakan terjemahan
  Inggeris via `core/eng_source.py` → `simpan_bab`/`simpan_hadis`).
- Log harian: `dokumen/perubahan/PERUBAHAN_*.md` (11 Ogos – 31 Ogos).

## 2. Tema Aqua & Penyepaduan Visual (25 Ogos 2026)

- Tambah latar "globe" aqua (`latar_globe_dunia.png`, `latar_globe_timeline.png`)
  diserapkan ke `PustakaHadith.spec` `datas`.
- Bina semula dist + Setup EXE → `Output/PustakaHadith-Setup-1.0.0-x64.exe`
  **725.8 MB** dengan tema aqua.

## 3. Pembinaan MSIX & Gerbang Fasa 5C (26–27 Ogos 2026)

- Dibina MSIX dari dist onedir; uji `makeappx`/`signtool` (Windows SDK
  10.0.18362). MSIX diuji berjaya (Partner Center daftar).
- **Fasa 5C LULUS**: `dokumen/rujukan/DAFTAR_MSIX_STORE.md` dicipta.
- Semakan `CHECKLIST_PEMANTAUAN.md` dikemas kini: Fasa 5 ✓; bahagian terperinci
  Fasa 6/7 dibetulkan (commit `43ad8d2`) — daftar + identiti ☑, halangan lesen
  Ahmad dibuang; Fasa 5 → ☑ SELESAI (27 Ogos).

## 4. Regresi UI & Punca Akar (27 Ogos 2026)

- **Laporan:** detail-page tiada sidebar "Lompat No. hadis"; "lihat bab" buka
  halaman sama (tiada pemetaan bab).
- **Siasatan:** binaan dist/terpasang **tiada `hadis.db`**. `DATA_DIR` mod
  frozen = `%LOCALAPPDATA%\PustakaHadith`; folder itu kosong → `get_bab_list`
  pulangkan `[]` → tiada bab.
- **Fix segera (ujian setempat):** salin `hadis.db` + `hadis_faiss.index` +
  `hadis_id_map.pkl` ke `%LOCALAPPDATA%\PustakaHadith`; "PILIH BAB" muncul.
- Butiran: `dokumen/rujukan/PERBINCANGAN_BAB_NOMBOR_HADIS.md`.

## 5. Asal Senarai "Bab" & Isu Penomoran No. Hadis (27 Ogos 2026)

- **Asal bab:** `get_bab_list` (`hadis_api.py`) tanya jadual `bab` ← JSON CDN
  `metadata.sections` diproses `core/eng_source.py` `bina_bab`/`simpan_bab`
  (dipanggil `sync_english.py`). Nama bab adalah **Inggeris** (belum diterjemah
  Melayu). `ahmad` & `darimi` = **0** data bab.
- **Isu penomoran:** Bukhari #858 dalam app menunjukkan kandungan kanonik
  #909 (app jumlah 7008 vs kanonik sunnah.com 7563). Set data sumber guna
  edisi terjemahan berbeza per koleksi → nombor tak sepadan dengan sunnah.com /
  hadith.my.
- **Kesan:** "Lompat No.", penanda buku, sejarah bacaan, kiraan bab, rujukan
  kongsi semua salah berbanding sumber rujukan.
- **Pilihan (BELUM DIPUTUSKAN):**
  - **A (disyorkan):** Ganti semula kesemua 9 koleksi dari set data bernombor
    kanonik sunnah.com, bina semula DB + jalankan semua sync.
  - **B:** Kekal data, nyatakan jelas ia mengikut penomoran "edisi terjemahan".
  - **C:** Semak JSON sumber (tiada dalam repo) untuk medan nombor kanonik
    bagi pemetaan semula.

## 6. Gerbang Lesen hadis.my — TIDAK BUNDLE DATA (27 Ogos 2026)

- **Keputusan pengguna:** JANGAN bundel `hadis.db` / indeks FAISS ke installer
  sehingga dapat **kebenaran bertulis hadis.my** (data terbitan
  service.hadis.my). Binaan interim = **mod dalam talian sahaja**.
- `PustakaHadith.spec` `datas` **dikembalikan** (buang `hadis.db`,
  `hadis_faiss.index`, `hadis_id_map.pkl`). `installer/PustakaHadith.iss`
  menyalin `dist\PustakaHadith\*` → `{app}` = `%LOCALAPPDATA%\PustakaHadith`.
- Surat permohonan sedia: `dokumen/surat/hadis.my/SURAT_HADISMY.md` (API) &
  `dokumen/surat/kebenaran/SURAT_SEMAKHADIS.md` (SemakHadis). Status: perlu
  dapatkan persetujuan sebelum bundel.
- Catatan: `PustakaHadith.spec` & `installer/PustakaHadith.iss` di-gitignore
  (baris 55–65) — konfig binaan sengaja tidak di-commit.

---

## 7. Susunan Dokumentasi (27 Ogos 2026)

Struktur kategori baharu (lihat `dokumen/STRUKTUR_DOSUMENTASI.md`):

- `dokumen/sejarah_pembangunan/` — log ini (sejarah perjalanan projek).
- `dokumen/surat/kebenaran/` — surat kebenaran/lesen (hadis.my, SemakHadis, Ahmad).
- `dokumen/surat/sokongan/` — dasar privasi & pautan sokongan Store.
- `dokumen/perbincangan/` — rekod perbincangan (bab & nombor hadis).
- `dokumen/penerbitan/` — tangkapan skrin & proses MSIX/Store.
- `dokumen/perubahan/` — log harian perubahan.
- `dokumen/sesi/` — indeks sesi kerja.
- `dokumen/rujukan/` — panduan rujukan (MSIX Store, pelan bina edaran).
- `dokumen/manual/` — manual pengguna & pembangun.
- `dokumen/audit/` — audit padanan arkib & Ahmad Digital.

---

## 8. Item Terbuka (Open Items)

1. **Nombor hadis (Bukhari 858 = kanonik 909):** putuskan A / B / C.
2. **Kebenaran hadis.my:** hantar & dapatkan persetujuan bertulis sebelum
   bundel data ke installer.
3. **Fasa 6/7 (Store rasmi):** menunggu `DASAR_PRIVASI.md` + `PAUTAN_SOKONGAN.md`
   + `TANGKAPAN_SKRIN.md` lengkap (kini di `surat/sokongan/` & `penerbitan/`).
4. **Bina semula dist** (online-only, tanpa hadis.db) — ditangguh atas arahan
   pengguna (binaan sebelum ini dibatalkan).
5. **Penterjemahan nama bab** (Inggeris → Melayu) untuk `ahmad`/`darimi` (0 bab).
6. **`uji_visual_kiraan.py`** — re-baseline (perlu skrin fizikal + DB penuh).

## 9. Penyediaan Surat & Dokumen Sokongan hadis.my (27 Ogos 2026)

- Kemaskini `dokumen/surat/hadis.my/SURAT_HADISMY.md`: tarikh → 27 Ogos,
  tambah **Tangkapan Skrin** (6 imej), **Status Semasa** (build interim
  online-only menunggu kebenaran), dan senarai Lampiran yang merujuk fail sebenar.
- Tangkapan skrin dijana secara deterministik (`tangkap_layar.py` memandu
  `PustakaApp` via `go()` / `open_kitab()` / `open_by_ref()` + `QWidget.grab()`):
  `dokumen/penerbitan/tangkapan/01_utama.png` … `06_simpan_sejarah.png`.
- Kemaskini `dokumen/surat/sokongan/DASAR_PRIVASI.md` (tarikh, seksyen
  "Pembundelan Snapshot Data", baiki footer) & `PAUTAN_SOKONGAN.md` (footer).
- Semua fail di atas dirujuk merentas satu sama lain untuk penghantaran kepada
  hadis.my.

## 10. Kemaskini Manual Pengguna (27 Ogos 2026)

- `dokumen/manual/MANUAL_PENGGUNAAN.md`: betulkan jadual kiraan kitab kepada
  nombor sebenar apl (Bukhari 7,008 … jumlah 62,169) + nota penomboran sumber;
  kemaskini navigasi (Jelajah Kitab → Rak Digital), seksyen "Meneroka mengikut
  Bab", "Keperluan Data & Mod Luar Talian" (sync API perlu; bundel menunggu
  kebenaran hadis.my), jelaskan tab English = Musnad Ahmad, baiki footer.

## 11. Folder hadis.my & PDF + Logo (27 Ogos 2026)

- Cipta `dokumen/surat/hadis.my/` khusus emel & surat kepada hadis.my; pindah
  `SURAT_HADISMY.md` + `EMEL_HADISMY.md` ke sana (kemas rujukan di STRUKTUR,
  MANUAL, LOG).
- Janakan **logo PustakaHadith** (`logo_PustakaHadith.png`, 965×261, transparent)
  guna `buat_logo.py`: "Pustaka" Segoe UI Bold #5CBF85, "Hadith" Light
  #7FD39A, "v1.0.0" #9C9589 — sepadan header apl.
- Tukar dokumen ke **PDF**. Cuba pertama (`buat_pdf.py`, xhtml2pdf) hasil
  berterabur; ganti dengan `buat_pdf2.py` (reportlab platypus) — susun atur
  bersih & dipaginkan: `SURAT_HADISMY_kemas.pdf` (6 tangkapan skrin + logo),
  `EMEL_HADISMY.pdf` (+logo), `DASAR_PRIVASI.pdf`, `PAUTAN_SOKONGAN.pdf`.
  (`SURAT_HADISMY.pdf` lama terkunci dalam pelihat PDF; akan diganti bila
  ditutup.)

---

*Log ini dikemas kini setiap sesi kerja. Sila rujuk fail kategori di atas untuk
butiran penuh setiap topik.*
