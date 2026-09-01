# SESI PEMBANGUNAN — PustakaHadith

## Tarikh
30 Ogos – 1 September 2026

## Matlamat
Bina & edar **PustakaHadith** v1.0 (PyQt5 + SQLite/FTS5 + FAISS, Windows).
Komunikasi dengan pengguna: **Bahasa Melayu**.

---

## Sesi 1 (30 Ogos): Page Carian = Senarai Hadis

### Perubahan
- Page Carian dipadankan **persis** dengan page **Senarai Hadis**:
  - Tajuk panel: **SENARAI CARIAN** (bukan "SENARAI DWIBAHASA").
  - Tiada chip Semua/Tersimpan/Belum, tiada butang kaedah (Kata/Makna/Kedua).
  - Tiada draf AI "kad carian", tiada LOMPAT NO. HADIS.
  - Sidebar: **BAB DALAM KEPUTUSAN** memanjang & kelihatan (`skrol` stretch=1, tiada cap 238).
  - Kad hasil **top-align** (`Qt.AlignTop`).
  - Butang susunan Nombor ↑/↓ kekal.

### Fail diubah
- `ui/pages_carian.py` — redesign panel & sidebar, buang draft/chips/go-box.
- `ui/widgets.py` — `hadith_card_dwibahasa` top-align kolum.
- `ui/workers.py` — SearchWorker ambil semua halaman (paginasi klien).

---

## Sesi 2 (31 Ogos): Sync & Bundel hadis.db

### Perubahan
1. **Sync 55 hadis terjemahan Melayu diperbaiki** dari hadis.my:
   - Padam 55 hadis lama dari DB.
   - `python sync.py --paksa malik bukhari tirmidzi ahmad darimi nasai` (555s, 56 rekod baharu).
   - 62,169 hadis lengkap dalam DB, kuota tinggal 9,518.

2. **Bundel hadis.db ke dalam EXE**:
   - `PustakaHadith.spec`: tambah `('hadis.db', '.')` ke datas.
   - `config.py`: tambah `_salin_db_bundel()` — salin dari bundle ke `%LOCALAPPDATA%` pada pertama kali jalan (frozen mode sahaja, skip jika sudah ada).
   - `python -m PyInstaller PustakaHadith.spec --noconfirm` — berjaya.
   - `dist\PustakaHadith\_internal\hadis.db` = 354 MB.

3. **FAISS index** — TIDAK dibina semula (ambil ~10 jam). 55 hadis = 0.09%, kesan minimum. Perlu rebuild kemudian.

### Nota penting
- EXE berjaya dilancarkan (PID 13096), pengguna sedang uji.
- hadis.db dibundel: pengguna baru terus boleh baca tanpa sync.
- Pengguna sedia ada: DB sedia ada di `%LOCALAPPDATA%` tidak ditulis ganti.

---

## Sesi 3 (1 September 2026): Selective FAISS & Build Final

### Perubahan
1. **Selective rebuild FAISS index** — berjaya dalam ~30 saat (bukan 10 jam):
   - Tambah `--selective` flag ke `scripts/build_faiss_index.py`.
   - Hanya 56 vektor dikemas kini (55 hadis terjejas + 1 lagi).
   - `AFFECTED_IDS` hardcoded dalam skrip.

2. **FAISS files ditambah ke .spec** — `hadis_faiss.index` (91 MB) + `hadis_id_map.pkl` (0.8 MB) sebelum ini TIADA dalam Release build.

3. **EXE dibina semula** — kini mengandungi:
   - `hadis.db` (354 MB) — 62,169 hadis dengan 55 pembaikan Melayu
   - `hadis_faiss.index` (91 MB) — indeks semantik terkini
   - `hadis_id_map.pkl` (0.8 MB) — peta ID

### Selesai Hari Ini
- ✅ Selective rebuild FAISS (30 saat)
- ✅ FAISS files ditambah ke .spec
- ✅ EXE dibina semula (dengan hadis.db + FAISS)
- ✅ EXE dilancarkan untuk uji

### TODO
1. **Inno Setup** — rebuild installer dengan hadis.db baharu.
2. **"paparan hadis on top jgn center"** — kad sudah top-align. Sahkan dengan pengguna.
3. Polish lain jika pengguna minta.

---

## Sesi 3 (31 Ogos): Betulkan Ralat Carian Jelajah Kitab

### Ralat
- Taip "400" pada Jelajah Kitab → tidak lompat terus ke hadis no. 400.
- Butang **‹ Kembali** dari detail hadis pergi ke halaman Utama, bukan Jelajah Kitab.
- Tiada butang × (clear) pada medan carian Jelajah Kitab.

### Punca
1. `keyPressEvent` pada `pages_rak.py` intercept Enter key dan panggil `open_kitab()` — BUKAN `_rak_hantar_carian()`. Berlaku walaupun QLineEdit carian ada focus.
2. `_buka_hadis_terus` dipanggil dengan `dari="home"` — sebab itu Kembali pergi ke Utama.
3. `BACK_PETA` tidak mempunyai entri `"rak"`.

### Perubahan
- **`ui/pages_rak.py:524`** — `keyPressEvent` tambah semak `QApplication.focusWidget()`. Jika QLineEdit ada focus, Enter tidak di-intercept.
- **`ui/pages_rak.py:337`** — `dari="home"` → `dari="rak"`.
- **`ui/pages_detail.py:69`** — tambah `"rak": ("Jelajah Kitab", "rak")` ke `BACK_PETA`.
- **`ui/pages_rak.py:315`** — `self._rak_carian.setClearButtonEnabled(True)` — butang × pada medan carian.

### Fail diubah
- `ui/pages_rak.py` — `keyPressEvent`, `_rak_hantar_carian`, `_rak_carian`.
- `ui/pages_detail.py` — `BACK_PETA`.

### Status
- ✅ Compile OK
- ✅ Apl dilancarkan untuk uji

---

## Sesi 4 (31 Ogos): UI & Crash Fix

### Perubahan
1. **Butang × clear pada medan carian Jelajah Kitab** — `setClearButtonEnabled(True)` pada `_rak_carian`.
2. **LOMPAT NO. HADIS dipindah dari sidebar ke banner** — buang go box dari sidebar (`_kitab_sidebar`), tambah teks "LOMPAT NO. HADIS" di bawah search bar dalam `_kitab_banner`. Go box tersembunyi (hidden) kekal untuk Ctrl+G.
3. **Crash fix: QCheckBox deleted** — `pages_tersimpan.py` `_sejarah_pilih_semua`, `_sejarah_kemas_buang`, `_sejarah_buang_pilih` — tambah `try/except RuntimeError` untuk handle widget yang sudah dihapuskan.
4. **EXE rebuild** — berjaya ke `D:\PustakaQH_dist\PustakaHadith\` (folder dist asar lock oleh Windows Defender).

### Status
- ✅ Compile OK
- ✅ Apl dilancarkan untuk uji
- ⏳ Inno Setup — belum dipasang pada PC ini
- ⏳ Folder `dist\PustakaHadith` — lock oleh Windows Defender, perlu copy dari `D:\PustakaQH_dist\` selepas scan selesai

### Fail diubah
- `ui/pages_rak.py` — `_rak_carian.setClearButtonEnabled(True)`
- `ui/pages_kitab.py` — `_kitab_banner()` (LOMPAT teks), `_kitab_sidebar()` (buang go box)
- `ui/pages_tersimpan.py` — try/except RuntimeError pada 3 kaedah sejarah

---

## Fail Utama
| Fail | Fungsi |
|---|---|
| `ui/pages_carian.py` | Page Carian (diperbaharui) |
| `ui/pages_rak.py` | Jelajah Kitab (keyPressEvent, carian, clear) |
| `ui/pages_kitab.py` | Senarai Hadis (banner, LOMPAT, sidebar) |
| `ui/pages_detail.py` | Detail hadis (BACK_PETA) |
| `ui/pages_tersimpan.py` | Tersimpan/Sejarah (crash fix) |
| `ui/widgets.py` | Kad hadis (top-align) |
| `ui/workers.py` | SearchWorker |
| `config.py` | `_salin_db_bundel()` — salin DB pada startup |
| `PustakaHadith.spec` | PyInstaller datas (termasuk hadis.db) |
| `sync.py` | Sync dari hadis.my API |
| `SESI.md` | Fail ini |

## Cara Lari
- **SUMBER**: `JALANKAN.bat` (pythonw main.py) — nampak perubahan segera.
- **EXE (backup)**: `D:\PustakaQH_dist\PustakaHadith\PustakaHadith.exe` — binaan terkini 31 Ogos.
- **EXE (dist asar)**: `dist\PustakaHadith\PustakaHadith.exe` — mungkin versi lama (lock).
- **Jangan** guna EXE lama (beku 28 Aug) untuk uji perubahan terkini.

## Nota Penting
- **JANGAN commit** melainkan pengguna minta.
- Pengguna mudah frustrasi jika edit salah page atau tak ikut arahan literal.
- Komunikasi: **Bahasa Melayu**.
- **Windows Defender** sering lock fail `.pyd`/`.dll` selepas PyInstaller build — guna `--distpath` ke folder berbeza jika `dist\` lock.
- **FAISS index** telah di-selective-rebuild (56 vektor diganti). `scripts/build_faiss_index.py` `--selective`.
- Fakta carian: `search_hadis(q)` → keys `['arab','book','collection','id','indonesia','melayu','nama_bab']`; dedupe `hid = h.get("hadis_id") or h.get("id")`.
- **GitHub push berjaya** — 103 commits di-push ke `https://github.com/PustakaHadith/PustakaHadith` (token lama tiada `workflow` scope, token baru diberi oleh pengguna).
- **Inno Setup** belum dipasang pada PC ini.

---

## Sesi 5 (1 September): MSIX Package untuk Microsoft Store

### Matlamat
Bina MSIX package untuk upload ke Microsoft Store.

### Perubahan
1. **MSIX pack berjaya** — `makeappx pack` dengan timeout 30 minit:
   - `D:\PustakaQH_dist\PustakaHadith-v1.0.0.msix` = **1.1 GB**
   - Mengandungi: `hadis.db` (371 MB), `.cache_models` (941 MB), `torch` (361 MB), `hadis_faiss.index` (95 MB), PyQt5, dan semua dependencies.

2. **AppxManifest.xml** — dikonfigur untuk Microsoft Store:
   - Identity: `PustakaHadith`, Publisher: `CN=opencodemk`
   - TargetDeviceFamily: Windows.Desktop 10.0.17763.0+
   - Capabilities: `runFullTrust`
   - Resources: ms, ar, en-US

3. **Sijil code signing** — dibuat dengan `New-SelfSignedCertificate -Type CodeSigningCert`:
   - Thumbprint: `46A04D1A9AED7E5D4A8525523F102CFA077005EA`
   - **Isu**: `signtool.exe` SDK 10.0.18362.0 tidak support sign MSIX ("file format not recognized")
   - `Set-AuthenticodeSignature` juga tidak support MSIX
   - **Penyelesaian**: MSIX tidak perlu sign local — Microsoft sign semasa submission di Partner Center

4. **GitHub push berjaya** — semua commits di-push ke `https://github.com/PustakaHadith/PustakaHadith`

### Status
- ✅ MSIX pack berjaya (1.1 GB)
- ✅ AppxManifest.xml dikonfigur
- ✅ GitHub push selesai
- ❌ MSIX sign — SDK lama tidak support (tidak perlu untuk Store upload)
- ⏳ Upload ke Microsoft Store — perlu akaun Partner Center ($19 USD)
- ⏳ Inno Setup — belum dipasang

### Fail baru/diubah
- `D:\PustakaQH_dist\PustakaHadith\AppxManifest.xml` — MSIX manifest
- `D:\PustakaQH_dist\PustakaHadith-v1.0.0.msix` — MSIX package (1.1 GB)
- `D:\PustakaQH_dist\PustakaHadith.pfx` — sijil lama (tidak digunakan)

### Nota Penting Tambahan
- **MSIX terlalu besar** kerana `.cache_models` (941MB) + `torch` (361MB). Pertimbang buang untuk kecilkan saiz.
- **SDK 10.0.18362.0** terlalu lama untuk MSIX sign. Perlu Windows 11 SDK jika mahu sign local.
- **Partner Center** diperlukan untuk upload — `https://partner.microsoft.com/dashboard`

### Seterusnya (Esok)
1. Dapatkan / sahkan akaun Partner Center
2. Upload MSIX ke Microsoft Store
3. Isi butiran listing (deskripsi, screenshot, kategori)
4. Submit untuk review
