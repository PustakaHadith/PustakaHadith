# SESI PEMBANGUNAN — PustakaHadith

## Tarikh
30 Ogos – 2 September 2026

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
- ✅ Upload ke Microsoft Store — selesai (menunggu review Microsoft)
- ⏳ Inno Setup — belum rebuild (lihat Sesi 6)

### Fail baru/diubah
- `D:\PustakaQH_dist\PustakaHadith\AppxManifest.xml` — MSIX manifest
- `D:\PustakaQH_dist\PustakaHadith-v1.0.0.msix` — MSIX package (1.1 GB)
- `D:\PustakaQH_dist\PustakaHadith.pfx` — sijil lama (tidak digunakan)

### Nota Penting Tambahan
- **MSIX terlalu besar** kerana `.cache_models` (941MB) + `torch` (361MB). Pertimbang buang untuk kecilkan saiz.
- **SDK 10.0.18362.0** terlalu lama untuk MSIX sign. Perlu Windows 11 SDK jika mahu sign local.
- **Partner Center** diperlukan untuk upload — `https://partner.microsoft.com/dashboard`

---

## Sesi 6 (1 September): MSIX Upload & Landing Page

### Perubahan
1. **MSIX upload ke Microsoft Store — SELESAI** ✅ (pengguna sahkan). Menunggu review Microsoft.
2. **Landing page promosi dibina** (di luar projek):
   - Lokasi: `D:\Pustaka Quran Hadis\landing-page\` (`index.html` + `img/`)
   - Tema **Aqua Glass** ikut `ui/theme.py` (AQUA), mockup & latar globe dari `PustakaHadith_UIUX`
   - Kandungan diselaraskan dengan `dokumen/rujukan/DEKLARASI.md` (positioning, statistik, batasan, atribusi)
   - Jenama "Pustaka/Hadith" ikut `ui/app_qt.py:286-287` (TEAL 800 / TEAL_LIGHT 300)
   - Atribusi sumber: hadis.my, domain awam (sunnah.com); hubungan komersial: `pustakahadith@outlook.com`
   - Ikut GitHub: `https://github.com/opencodemk/PustakaHadith`
   - Tajuk tarikan: "Aplikasi Desktop Carian Hadis — Percuma & Luar Talian" + 3 ayat tarikan di bahagian sesuai
   - Telah di-upload ke **pustakahadith.site.je** (hosting ada perlindungan anti-bot JS)
3. **Inno Setup dipastikan SUDAH dipasang** — `D:\Inno Setup 6\ISCC.exe` wujud. Nota SESI lama "belum dipasang" adalah silap.
4. **FAISS rebuild** — anggaran masa disemak: full ~3 jam (4 CPU, ikut script) hingga ~10 jam (rekod SESI 2); selective ~30 saat.

### Fail baru/diubah
- `D:\Pustaka Quran Hadis\landing-page\index.html` + `img/` — landing page (di luar repo)
- `SESI.md` — fail ini

### Seterusnya (Esok) — TODO
1. **Bina Inno Setup installer terkini** (~33 minit) — `iscc "D:\Inno Setup 6\ISCC.exe" installer\PustakaHadith.iss` supaya EXE mengandungi hadis.db (55 fix) + FAISS files. EXE sedia ada (26 Ogos) masih versi lama.
2. **Pautkan landing page ke pautan muat turun sebenar** — arahkan butang "Muat Turun" ke GitHub Releases / EXE terkini.
3. **Verify landing page pada pustakahadith.site.je** — buka dalam pelayar sebenar (anti-bot JS); pastikan semua imej & pautan berfungsi.
4. **Sahkan "paparan hadis on top jgn center"** dengan pengguna (kad sudah top-align, Sesi 1).
5. **Butiran listing Microsoft Store** — mengisi deskripsi/screenshot/kategori jika belum lengkap; pantau status review.
6. **Full FAISS rebuild** — TIDAK mendesak (56/62,169 vektor sahaja berubah). Lakukan hanya jika struktur indeks/model berubah.
7. **Pertimbang kecilkan MSIX** — buang `.cache_models` (941 MB) supaya pakej Store lebih ringan.

---

## Sesi 7 (2 September): Inno Setup Rebuild

### Perubahan
1. **Inno Setup installer dibina semula** — `iscc` dari `D:\Inno Setup 6\ISCC.exe`:
   - Disemak dahulu: `dist\PustakaHadith` versi 31 Ogos **TIADA** hadis.db/FAISS; binaan lengkap berada di **`D:\PustakaQH_dist\PustakaHadith`** (hadis.db 354 MB + hadis_faiss.index 91 MB + hadis_id_map.pkl 0.8 MB).
   - **`installer/PustakaHadith.iss`** — `Source` ditukar dari `..\dist\PustakaHadith\*` → `D:\PustakaQH_dist\PustakaHadith\*`.
   - Compile berjaya dalam **2204 saat (~37 minit)**.
   - **`Output\PustakaHadith-Setup-1.0.0-x64.exe`** = **0.79 GB** (naik dari 0.73 GB 26 Ogos kerana kini termasuk hadis.db + FAISS).
   - SHA256: `77DFE153CDB0C2A47FE286F3478BBE62D0EA8A926596A25F00BD093AAB784BE3`

### Fail diubah
- `installer/PustakaHadith.iss` — Source ke `D:\PustakaQH_dist\PustakaHadith\*`
- `Output/PustakaHadith-Setup-1.0.0-x64.exe` — binaan baharu

### Status
- ✅ Inno Setup EXE terkini (hadis.db 55 fix + FAISS) dibina
- ✅ Pautan muat turun di landing page diarah ke GitHub Releases (TODO #2, Sesi 8)
- ⏳ Verify landing page di live site (TODO #3)

---

## Sesi 8 (2 September): Muat Turun Sebenar + Fix Proses Kekal Selepas Tutup

### Perubahan
1. **Setup EXE & Portable 7z di-upload ke GitHub Release v1.0.0** (akaun PustakaHadith, token PAT user):
   - `PustakaHadith-Setup-1.0.0-x64.exe` **806.6 MB**
   - `PustakaHadith-portable-1.0.0-x64.7z` **802.1 MB** (dari dist lengkap 2.18 GB, 7z `-mx=5 -mmt=4`)
   - Penerangan release dikemas kini (Setup EXE bukan lagi "coming soon")

2. **Landing page dikemas kini** — kad Setup EXE & Portable ZIP→7z jadi **SIAP** (bukan SEGERA), butang aktif; nota "0.8–1.1 GB". Deploy FTP berjaya (saiz server 37,732 bytes = sepadan).

3. **Fix: proses kekal berjalan selepas tutup apl** — pengguna dapati `PustakaHadith.exe` (PID 6820) kekal di latar walaupun window ditutup.
   - Punca: `main.py:126` menetapkan `app.setQuitOnLastWindowClosed(False)` — tinggalan zaman splash (PERUBAHAN_19OGOS.md komit 3), tetapi zaman sekarang (Lazy Loading) tiada lagi `splash.close() → singleShot(0)`, jadi flag itu hanya menyebabkan `app.exec_()` tidak berhenti bila window utama ditutup.
   - Fix: tambah `QApplication.quit()` di hujung `closeEvent` (`ui/app_qt.py:198`) — keluar eksplisit selepas worker dibatalkan.
   - Disahkan: ujian offscreen `setQuitOnLastWindowClosed(False)` + `w.close()` → `exec_` keluar segera (kod 0), padahal sebelum ini akan tergantung.
   - ⚠️ EXE/7z/release yang sedia ada BELUM mengandungi fix ini — perlu rebuild PyInstaller + 7z + upload semula jika mahu.

### Fail diubah
- `ui/app_qt.py` — `closeEvent()` tambah `QApplication.quit()`
- `landing-page/index.html` — kad muat turun aktif, nota saiz
- `installer/PustakaHadith.iss` — Source ke `D:\PustakaQH_dist\PustakaHadith\*` (Sesi 7)
- `landing-page/SESI.md` — rekod Sesi 4

### Status
- ✅ Release v1.0.0 lengkap (EXE + 7z + MSIX)
- ✅ Landing page live dengan pautan sebenar
- ✅ Fix proses kekal (dalam kod sumber)
- ✅ **Rebuild EXE/7z** — fix proses kekal kini dalam edaran (Sesi 9)
- ⏳ Peperiksaan visual landing page (anti-bot JS — perlu pelayar)

---

## Sesi 9 (2 September): Rebuild Edaran — Fix Proses Kekal

### Perubahan
1. **PyInstaller rebuild** — `python -m PyInstaller PustakaHadith.spec --noconfirm --distpath D:\PustakaQH_dist\PustakaHadith_v2`:
   - EXE 85.3 MB + hadis.db (353.9 MB) + hadis_faiss.index (91.1 MB) + hadis_id_map.pkl (0.8 MB)
   - Disahkan lengkap (7080 fail build vs 7082 termasuk 2 fail MSIX: AppxManifest.xml + PustakaHadith.png yang bukan sebahagian build)
   - Folder semasa disandarkan ke `PustakaHadith_sep2026`; v2 digelar rasmi `D:\PustakaQH_dist\PustakaHadith`; 2 fail MSIX disalin semula

2. **Portable 7z dibina semula** — `Output\PustakaHadith-portable-1.0.0-x64.7z` **802.1 MB**
   - SHA256: `86DFC8D5A5148EA30D6D9651BAAF5F5559B45CE5E7D13D6937D3F32292F543DD`

3. **Inno Setup dibina semula** — `Output\PustakaHadith-Setup-1.0.0-x64.exe` **806.6 MB** (2263 saat ~38 minit)
   - SHA256: `804A15DA69C771A128F32C86CA06F472D0CFE6C5D205FA89D06C696B49D76624`

4. **Upload ke GitHub Release v1.0.0 (clobber)** — keduanya diganti dengan versi fix closeEvent (updated 2026-09-02):
   - `PustakaHadith-portable-1.0.0-x64.7z` 802.1 MB
   - `PustakaHadith-Setup-1.0.0-x64.exe` 806.6 MB
   - `PustakaHadith-v1.0.0.msix` 1093.7 MB (tidak disentuh — MSIX Store lama)

### Fail diubah
- `ui/app_qt.py` — `closeEvent()` + `QApplication.quit()` (fix, dari Sesi 8)
- `D:\PustakaQH_dist\PustakaHadith\` — binaan baharu (rasmi)
- `Output/PustakaHadith-Setup-1.0.0-x64.exe` + `Output/PustakaHadith-portable-1.0.0-x64.7z` — baharu
- `D:\PustakaQH_dist\PustakaHadith_sep2026\` — sandaran binaan 31 Ogos

### Status
- ✅ Semua edaran (EXE + 7z) mengandungi fix proses kekal
- ⚠️ MSIX Store kekal versi 1 Sep (tanpa fix) — pembetulan perlu submit pakej MSIX baru jika mahu
- ⏳ Peperiksaan visual landing page (perlu pengguna — anti-bot JS)

---

## Sesi 10 (2 September): Susun Semula Folder Induk "Pustaka"

### Perubahan
Semua folder projek disatukan ke **`D:\Pustaka Quran Hadis\Pustaka\`**:

| Folder | Lokasi baharu |
|---|---|
| Repo utama (git) | `D:\Pustaka Quran Hadis\Pustaka\PustakaHadith\` |
| Landing page | `D:\Pustaka Quran Hadis\Pustaka\landing-page\` |
| Imej sumber | `D:\Pustaka Quran Hadis\Pustaka\img\` |
| UIUX | `D:\Pustaka Quran Hadis\Pustaka\PustakaHadith_UIUX\` |
| Binaan & MSIX | `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\` |

### Fail binaan dikemas kini (laluan lama → baharu)
- `installer/PustakaHadith.iss` — Source → `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith\*`
- `installer/build_msix.ps1` — `$root` → `D:\Pustaka Quran Hadis\Pustaka\PustakaHadith`

### Catatan
- Repo utama dipindah (isi + `.git`) — git sah, log dipelihara; folder lama `D:\Pustaka Quran Hadis\PustakaHadith` dipadam.
- Dokumen sejarah (PADANAN_ARKIB, MANUAL_REFERENSI_DEV, MULA_SINI, SESI lama) kekal rujukan lama — rekod masa lalu.

## Sesi 11 (2 September): Landing Page Dwibahasa Melayu/Inggeris

### Perubahan
- `landing-page/index.html` ditulis semula dengan sistem dwibahasa satu halaman (toggle MS | EN).
- Bahasa lalai auto-detect pelayar (`navigator.language`), pilihan manual diingati (`localStorage.ph-lang`).
- Meta dinamik (`title`, `og:*`, `twitter:*`) bertukar mengikut bahasa; nama Latin kitab kekal.
- **Semakan mudah alih** (render Chromium sebenar, emulasi 320–1366px): tiada limpahan mendatar; menu burger hidup `<980px`.
- **2 pembetulan**: `.hubungi-grid` ≤600px → `minmax(0,1fr)`; `}` penutup `@media(max-width:600px)` yang tercicir dikembalikan (176/176 seimbang).
- Deployed ke `pustakahadith.site.je` — hash SHA-256 sepadan (61,248 B); semakan visual pengguna OK.

### Catatan
- Butiran penuh: `..\landing-page\SESI.md` (Sesi 11) & `docs\superpowers\specs\2026-09-02-landing-dwibahasa-design.md`.
- Tiada perubahan kod apl; semata-mata landing page.
- **Belum di-commit**: `SESI.md` (ubah suai) + `docs/superpowers/specs/2026-09-02-landing-dwibahasa-design.md` (fail baru, untracked) — sedia untuk komit Sesi 11.

---

## Sesi 12 (3 September): Migrasi Hosting ke Netlify + Redirect site.je

### Perubahan
1. **Berpindah dari hosting FTP profreehost (`pustakahadith.site.je`) ke Netlify**:
   - Landing page dwibahasa penuh (dengan imej) kini live di **`https://pustakahadith.netlify.app`** (HTTP 200 semua aset).
   - Site Netlify: `pustakahadith`, account slug `pustakahadith`, site ID `4af95b07-c40d-4005-855b-2fd0ce95745e`.
   - Specifics: deploy ZIP via API menggunakan `tar.exe -a -c -f` (bukan `Compress-Archive`) supaya path guna **forward slash** `img/` (backslash → imej 404); header `Content-Type: application/zip`; `POST .../sites/{id}/deploys`; deploy `6a9949c23ab1c51f2f6c9a81` state `ready`.

2. **Custom domain `pustakahadith.site.je`** — dikunci "owned by another account" (profreehost), tidak boleh diimport ke Netlify via API (endpoint `/v1` 404 untuk bring-your-own domain; mesti UI dashboard). Pengguna memilih **'Kekal profreehost, redirect (Recommended)'**.

3. **Redirect `pustakahadith.site.je` → Netlify** (dua lapis, disahkan bertukar oleh pengguna):
   - `index.php` — **301 header redirect** ke `https://pustakahadith.netlify.app/`.
   - `index.html` — **meta-refresh (0s) + JS `window.location.replace()`** ke Netlify.
   - Nota: `.htaccess` (mod_rewrite) **tidak dibaca** oleh profreehost (AllowOverride tak dilaksanakan) — sebab itu guna PHP + HTML redirect.

4. **Kemas kini Netlify**:
   - Site lama `lovely-kitten-9baf06` (`d3d1a031`) dipadam (HTTP 204).
   - Auto-deploy Git **dihentikan** (`build_settings.stop_builds = True`) supaya deploy manual tidak ditimpa.

### Catatan / cabaran
- **Anti-bot profreehost**: semua permintaan HTTP ke `site.je` dipapar challenge JS (`aes.js`, cookie `__test`, redirect `?i=1`); semakan automatik dari luar tidak berfungsi — mesti semakan pelayar manusia.
- **Server mengekod semula imej `.webp`/`.png`** (dimensi sama, fail sah, saiz berbeza) — `index.html` hash sepadan tetapi imej tidak.
- **Netlify Credit-based**: site baharu **private by default** (tukar Public di dashboard); site terhenti bila kredit habis, reset bulan depan.

### Status
- ✅ Landing page penuh live di Netlify (`pustakahadith.netlify.app`)
- ✅ Redirect `site.je` → Netlify berfungsi (disahkan pengguna dalam pelayar)
- ✅ Auto-deploy Git dihentikan; site lama dipadam
- ⏳ MSIX Store kekal versi tertunggak (tanpa fix `closeEvent`) — perlu akaun Partner Center/user

### Fail diubah/dicipta
- `landing-page/index.html` + `img/` — sumber deploy Netlify (tiada perubahan kandungan).
- `C:\Users\MKAW\AppData\Local\Temp\opencode\ph-redirect.php` — `index.php` 301 redirect (di-upload ke server).
- `C:\Users\MKAW\AppData\Local\Temp\opencode\ph-redir-index.html` — `index.html` meta-refresh + JS redirect (di-upload ke server, ganti landing page lama).

### Kemas kini lanjutan (sama sesi, selepas push)
- ✅ **Site Netlify `pustakahadith` ditukar ke Public** (dilakukan user di dashboard Netlify) — disahkan akses pelawat luar: HTTP 200, landing page penuh 61,968 B (bukan halaman log masuk).
- Commits dipush: `91ec05f` (Sesi 12 migrasi+redirect). Push semula guna URL dgn token tertanam (cara `-c http.extraheader` ditolak "invalid credentials").
- Token PAT: `ghp_...idDpG` masih sah utk push; remote bersih tanpa token.

### Keputusan muktamad domain (4 September)
- **`pustakahadith.site.je` tidak lagi digunakan sebagai titik akses utama.** Punca: (1) TLD `.je` (Jersey) **tidak disokong Netlify** sebagai custom domain (endpoint `/v1/sites/{id}/domains` POST → 404; sama juga Sesi 12, bukan masalah "owned by another account" semata), dan (2) anti-bot profreehost kini menyekat akses walaupun dalam pelayar (HTTP 200 dgn challenge JS `aes.js`/`__test`/`?i=1`, bukan redirect).
- **Keputusan user: terus guna `https://pustakahadith.netlify.app`** sebagai URL rasmi landing page (sudah live, Public, lengkap). Jika mahu URL sendiri pada masa depan, perlu beli domain (`.com`/`.my`/`.net` dll) yang disokong Netlify.
- Fail redirect `index.php`/`index.html` di profreehost **dibiarkan** (tidak bernilai kerana anti-bot; tidak mendatangkan mudarat). Auto-deploy Git Netlify kekal dihentikan (deploy manual sahaja).

### Pembaikan 404 (4 September)
**Gejala:** `https://pustakahadith.netlify.app/` mula pulangkan 404 walaupun sebelum ini HTTP 200. `index.html` & imej semua 404.

**Punca:** Auto-deploy Git Netlify **aktif semula** (`stop_builds=false` — set kemungkinan dibatalkan bila site ditukar ke Public di dashboard). Ia me-deploy commit repo terbaru `2d7b0c0` (kod apl Python + SESI.md, **tiada `index.html` di root**) → `/` jadi 404.

**Diagnosis utama:**
- Deploy `6a9aae06` (git `2d7b0c0`, commit "Sesi 12: Keputusan muktamad domain") = 404 (tiada index.html).
- `6a9949c2` (deploy ZIP landing page Sesi 12) = **HTTP 200, 61,248 B** — masih bagus.
- **Deploy ZIP baharu hari ini `6a9ab1fa` = 404 (3,449 B)** — gubahan ZIP tidak sama dgn Sesi 12 (`tar.exe -a`), walaupun `index.html` + `img/` ada dlm arkib. Pelajaran: sentiasa sahkan deploy ZIP via preview URL (`https://{deploy_id}--{site}.netlify.app`) sebelum dijadikan current.

**Pembaikan:**
1. **Restore deploy `6a9949c2`** sebagai current — `POST /sites/{id}/deploys/{did}/restore` → published (11:59:24). `/`, `index.html`, `img/app-home.webp` semua HTTP 200 (61,968 B / 91,856 B).
2. **Hentikan auto-deploy Git secara kekal** — `PATCH /sites/{id}` `{"build_settings":{"stop_builds":true}}` → disahkan `stop_builds=True` (5 minit kemudian masih True). Notifikasi Netlify diterima: "Builds are now stopped... Netlify will never build your project."

**Status:** ✅ Landing page live semula (HTTP 200). ✅ Auto-deploy dihentikan (tidak menimpa lagi). Deploy masa depan = manual sahaja (CLI/API).

---

## Sesi 13 (5 September): Pengecilan MSIX — Dedup Blobs (Slim MSIX)

### Matlamat
Kecilkan pakej Microsoft Store (MSIX 1,093.7 MB). User memilih pendekatan **"Dedup blobs"** (buang pendua dalam `.cache_models`).

### Punca saiz
- `.cache_models/` (941 MB) mengandungi **duplikasi**: `blobs/` (470 MB) + `snapshots/` (470 MB) — fail model yang SAMA wujud dua kali (format cache HuggingFace).
- App memuat model AI melalui `snapshots` (`local_files_only=True`, `semantic_search.py` → `MODEL_CACHE`), jadi `blobs` tidak diperlukan.

### Pengujian
- Muat model tanpa `blobs` **BERJAYA**: cache_test 7.2s, staging 7.6s, encode → (1, 384) dims, `HF_HUB_OFFLINE=1`.

### Ujian pemasangan (MSIX slim) — BERJAYA
- Mesin: Windows 11 Pro 24H2 (build 26100), **Developer Mode AKTIF** (`AllowDevelopmentWithoutDevLicense=0x1`); SDK Windows terkini 10.0.18362.0 (signtool TIDAK support sign MSIX).
- `makeappx unpack` MSIX slim → OK (exit 0, 7078 entri).
- `Add-AppxPackage -Register AppxManifest.xml` → **Status Ok** `PUSTAKAHADITH.PustakaHadith_1.0.0.0_neutral__a8vs82dc5casm`.
- Lancar via **AUMID** (`shell:AppsFolder`) → proses terhasil (PID 9976, 82.2 MB) — aktivasi pakej penuh berfungsi. (Nota: `explorer shell:appsFolder\AUMID` sahaja tidak aktif; guna `Get-StartApps` AppID sebaliknya.)
- Nota: MSIX tidak ditandatangani (SDK lama); pendaftaran melalui Developer Mode bypass tanda tangan untuk ujian. Untuk pengguna biasa di PC lain → mesti melalui Microsoft Store (Microsoft sign semasa submission).
- **Pembersihan selepas ujian**: `Remove-AppxPackage` (pakej dikeluarkan), folder `C:\Users\MKAW\AppData\Local\Temp\opencode\msix_test` dipadam, tiada sisa di `%LOCALAPPDATA%\Packages`. Sistem kembali bersih.
- **GitHub Release v1.0.0 dikemas kini (5 Sep)**:
  - `PustakaHadith-v1.0.0-slim.msix` (814.8 MB) di-upload — menggantikan `PustakaHadith-v1.0.0.msix` lama (1,093.7 MB, tanpa fix) yang dipadam. Upload API ~32 minit (mustahil DISTINGUISH `-InFile`); saiz disahkan sepadan (854,378,662 B); pautan download OK (HTTP 200).
  - Release body dikemas kini (aset semasa: Setup EXE 806.6 MB, 7z 802.1 MB, MSIX slim 814.8 MB; nota fix closeEvent + dedup blobs).
  - **7z & Setup EXE tidak berubah** — dist tidak berubah sejak Sesi 9.

### Tindakan
1. Staging: `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\msix_staging` — disalin dari dist 2 Sept (2,229 MB) → **1,759 MB** selepas buang `blobs` (`.cache_models` 941 → 470 MB).
2. `Assets/` (4 logo) + `AppxManifest.xml` disalin ke staging.
3. `makeappx pack` → **`PustakaHadith-v1.0.0-slim.msix` = 814.8 MB** (1,093.7 → 814.8 MB, **jimat ~279 MB / ~25.5%**).

### Kandungan disahkan
- `model.safetensors` **448.8 MB** dalam `snapshots/.../` — **tiada `blobs/`**.
- `hadis.db` 353.9 MB, `hadis_faiss.index` 91.1 MB, `PustakaHadith.exe` 85.3 MB — utuh.
- AppxManifest: Identity `PUSTAKAHADITH.PustakaHadith`, Publisher `CN=1084A5A8-F66F-4B6D-A3EF-455CCC63CDD2`, Version `1.0.0.0`, `runFullTrust`, Windows.Desktop `10.0.17763.0+`.

### Implikasi / Kebaikan
- **~279 MB lebih kecil (~25.5%)** — muat turun Store lebih ringan, kurang ruang cakera.
- **AI carian makna luar talian kekal berfungsi** — model dibaca via snapshots (bukan blobs).
- **Bonus**: berasaskan dist 2 Sept → MSIX baharu ini *termasuk* fix `closeEvent` (MSIX Store lama 1 Sep TIDAK ada fix).
- **Nota sebelum upload Store**: padankan Identity/Version dengan listing Partner Center (Microsoft mungkin set semula identity semasa submission).

### FAISS — Jawapan (item 2)
- **Full rebuild**: ~3 jam (script, 4 CPU) hingga ~10 jam (rekod Sesi 2) — perlu hanya jika struktur indeks/model/teks berubah meluas.
- **Selective rebuild**: ~30 saat–5 minit (Sesi 3) — sudah dilaksanakan untuk 55 hadis terjejas.
- **Status: TIDAK perlu full rebuild sekarang** — hanya 55/62,169 vektor (0.09%) berubah; selective sudah tampung.

### Fail berkaitan
- `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\msix_staging\` — staging bersih (sumber pack)
- `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-v1.0.0-slim.msix` — MSIX baharu
- `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-v1.0.0.msix` — MSIX lama (1,093.7 MB)
- `..\landing-page\SESI.md` — rekod Sesi 13 (pengecilan MSIX)
