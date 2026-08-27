# Perubahan 27 Ogos 2026

## Pembinaan & Gerbang Lesen
- MSIX dibina; **Fasa 5C LULUS**; `dokumen/rujukan/DAFTAR_MSIX_STORE.md` dicipta.
- `CHECKLIST_PEMANTAUAN.md` dikemas kini: Fasa 5 ✓; bahagian Fasa 6/7
  dibetulkan (commit `43ad8d2`) — daftar + identiti ☑, halangan lesen Ahmad
  dibuang; Fasa 5 → ☑ SELESAI (27 Ogos).
- Surat `PERMOHONAN_LESEN_AHMAD.md` **DITUTUP** (Ahmad dikecualikan kekal).

## Siasatan Regresi UI & Data
- **Punca akar:** binaan dist/terpasang **tiada `hadis.db`**
  (`DATA_DIR = %LOCALAPPDATA%\PustakaHadith` kosong) → `get_bab_list` pulang
  `[]` → tiada bab / "lihat bab" buka halaman sama.
- Fix segera (ujian setempat): salin `hadis.db` + `hadis_faiss.index` +
  `hadis_id_map.pkl` ke `%LOCALAPPDATA%\PustakaHadith`.
- `PustakaHadith.spec` `datas` **dikembalikan** (buang `hadis.db`/faiss/index)
  — **JANGAN bundel data hadis.my sehingga kebenaran bertulis**.
  `installer/PustakaHadith.iss` salin `dist\PustakaHadith\*` → `{app}` =
  `%LOCALAPPDATA%\PustakaHadith`.

## Perbincangan Bab & Nombor Hadis
- `dokumen/rujukan/PERBINCANGAN_BAB_NOMBOR_HADIS.md` (`82cb845`, `e1104df`):
  asal senarai Bab (jadual `bab` ← metadata CDN → `core/eng_source.py`
  `bina_bab`/`simpan_bab`); isu penomoran **Bukhari #858 = kanonik #909**
  (app 7,008 vs 7,563); pilihan **A/B/C tertangguh**.

## Penyusunan Dokumentasi
- Cipta kategori: `sejarah_pembangunan/`, `surat/kebenaran/`,
  `surat/sokongan/`, `perbincangan/`, `penerbitan/`; pindah fail + kemas
  rujukan merentas `*.md` (`be0af4f`); `.gitignore` PII
  (`bf9c0680-...json`, `6eb5fff`).

## Manual, Surat & PDF hadis.my
- `MANUAL_PENGGUNAAN.md` dikemas kini (nombor kitab sebenar, navigasi,
  keperluan data/sync, bab) + 6 tangkapan skrin (`d030151`).
- `SURAT_HADISMY.md` + `EMEL_HADISMY.md` dikemas kini; 6 tangkapan skrin
  dijana (`tangkap_layar.py` pandu `PustakaApp`); `DASAR_PRIVASI` /
  `PAUTAN_SOKONGAN` dikemaskini (`d7ee299`, `9dee026`).
- Cipta `dokumen/surat/hadis.my/`: pindah SURAT + EMEL; logo
  `logo_PustakaHadith.png` (Segoe UI Bold #5CBF85 / Light #7FD39A / muted
  #9C9589, `buat_logo.py`); tukar ke **PDF** (xhtml2pdf berterabur →
  reportlab `buat_pdf2.py`): `SURAT_HADISMY_kemas.pdf`, `EMEL_HADISMY.pdf`,
  `DASAR_PRIVASI.pdf`, `PAUTAN_SOKONGAN.pdf` (`999a27e`, `1fa9a44`).

## Status / Tertangguh
- Nombor hadis (A/B/C) **belum diputuskan**.
- Kebenaran **hadis.my** diperlukan sebelum bundel data.
- Build dist (online-only) ditangguh atas arahan pengguna.
- `SURAT_HADISMY.pdf` asal terkunci dalam pelihat PDF; versi bersih =
  `SURAT_HADISMY_kemas.pdf` (ganti bila ditutup).

## Penyeragaman Jenama `PustakaHadith` (petang)
- Arahan pengguna: **"semua mesti kekal guna `PustakaHadith`"** (satu
  perkataan, 't' betul) — pembetulan dari `Pustaka Hadis` / `PustakaHadis`.
- Skrip ganti massa (`fix_brand2.py`) seragamkan **601 kemunculan / 96 fail**
  merentas dokumen + sumber: `Pustaka Hadis` / `PUSTAKA HADIS` / `Pustaka Hadith`
  (berjarak) / `PustakaHadis` (camelCase salah) → **`PustakaHadith`**.
- Fail binaan dinamakan semula: `PustakaHadis-Debug.spec` →
  `PustakaHadith-Debug.spec`, `PustakaHadis-Fasa4.wsb` →
  `PustakaHadith-Fasa4.wsb`.
- Sumber kemaskini: `config.py` (`DATA_DIR = %LOCALAPPDATA%\PustakaHadith`),
  `ui/app_qt.py` (tajuk tetingkap), `installer/msix_identity.txt`,
  `installer/PustakaHadith.iss`, pelbagai `*.bat`/`*.ps1`/`*.py`.
- PDF hadis.my dijana semula: `EMEL_HADISMY.pdf`, `DASAR_PRIVASI.pdf`,
  `PAUTAN_SOKONGAN.pdf` (guna `buat_pdf2.py`). Domain `hadis.my` (261)
  **tidak disentuh**.
- Commit `e9ff349`.
- **Tertangguh:** `SURAT_HADISMY.pdf` & `SURAT_HADISMY_kemas.pdf` masih
  terkunci dalam pelihat → belum dijana semula; perlu tutup pelihat.
- Binaan seterusnya (exe/MSIX) akan keluar sebagai `PustakaHadith` (tiada
  rebuild dibuat buat masa ini).
