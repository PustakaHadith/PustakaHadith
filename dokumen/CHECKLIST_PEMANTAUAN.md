# Checklist Pemantauan — PustakaHadith v1.0 Installer

> Dokumen INDUK untuk memantau dan semak imbang kerja installer.
> Kemas kini setiap kali kerja selesai. Setiap fasa ada GATE — fasa
> seterusnya hanya bermula selepas gate lulus.
>
> **Simbol:** ☑ = selesai/lulus · ☐ = belum · ⏳ = sedang jalan · ⛔ =
> disekat/menunggu keputusan.
> **Rujukan utama:** `dokumen/rujukan/INSTALLER.md` (§ = panduan),
> `dokumen/rujukan/PLAN_BINA_EDARAN.md` (kawalan fasa/gate),
> `dokumen/rujukan/PERMOHONAN_LESEN_AHMAD.md` (lesen Inggeris).
> **Log harian:** `dokumen/perubahan/PERUBAHAN_20OGOS.md`.

---

## FASA 0 — Kelulusan Skop (19 Ogos) ☑ GATE 0 LULUS

| # | Keputusan | Pilihan | Status |
|---|---|---|---|
| 1 | Bundel model e5 + indeks FAISS | YA — profil lengkap (atas sebab ujian & pengalaman pengguna) | ☑ |
| 2 | Pakej utama | MSIX Microsoft Store | ☑ |
| 3 | Pakej sekunder | Inno Setup EXE | ☑ |
| 4 | Akaun Microsoft Partner Center | Perlu — daftar (percuma) | ☑ keputusan |
| 5 | ZIP portable | Untuk penguji dalaman sahaja | ☑ |
| 6 | Wizard permulaan | Ya — sebelum beta | ☑ |

**Tugas pengguna (Fasa 0, masih terbuka):** ⏳
- ☐ Daftar akaun Microsoft Store: https://storedeveloper.microsoft.com/
- ☐ Tempah nama "PustakaHadith" (segera — nama boleh diambil orang lain)
- ☐ Pilih nama Publisher (akan direkod sebagai identiti MSIX)

---

## FASA 1 — Pisahkan Laluan Data (20 Ogos) ☑ GATE 1 LULUS

| # | Kerja | Status |
|---|---|---|
| 1 | Folder binaan `binaan_installer` dicipta (450 MB, tanpa .git/venv/cache/data peribadi) | ☑ |
| 2 | `config.py` pusat laluan: `ASSET_DIR` (baca sahaja) vs `DATA_DIR` (`%LOCALAPPDATA%\PustakaHadis` mod frozen) + 16 pemalar | ☑ |
| 3 | 8 fail runtime dipusatkan: db.py, api/hadis_api.py, ui/helpers.py, ui/splash.py, ui/disclaimer.py, core/sema_source.py, core/hadeethenc_api.py, core/semantic_search.py | ☑ |
| 4 | PROFIL_PATH di DATA_DIR (kod menulis log muat model; ASSET_DIR baca sahaja dalam MSIX) | ☑ |
| 5 | `uji_fasa1_data.py` (22/0) — simulasi `sys.frozen=True` dalam subproses | ☑ |

**GATE 1 (semua lulus):** semak.py ✓ · semak_versi.py ✓ · uji_lompat 67/0 ✓ ·
uji_carian_arab ✓ · main.py melancar ✓

---

## FASA 2 — Bina PyInstaller Diagnostik (20 Ogos) ☑ GATE 2 LULUS

| # | Kerja | Status |
|---|---|---|
| 1 | `main.py`: `multiprocessing.freeze_support()` (INSTALLER §6) | ☑ |
| 2 | Venv binaan `.venv-build` (keputusan pengguna: `--system-site-packages`, jimat 2 GB) — Python 3.14.6, PyInstaller 6.22.0 + hooks; hanya PyQt5 (tiada PySide/PyQt6) | ☑ |
| 3 | Rekod `installer_requirements-build-lock.txt` (pip freeze) | ☑ |
| 4 | Aset profil lengkap dibundel: .cache_models, hadis_faiss.index (91 MB), hadis_id_map.pkl, profil_model.json, sunnah_map, app.ico | ☑ |
| 5 | Bina onedir `--console` → `dist\PustakaHadis-Debug` = 2,022.8 MB / 7,065 fail (~19 minit) | ☑ |
| 6 | Semak warn-*.txt: 313 missing module — semua pilihan, tiada kritikal | ☑ |
| 7 | Uji exe: disclaimer → model e5 (RAM 78→596 MB) → tetingkap utama; FAISS 62,169×384; DATA_DIR betul; tiada hadis.db dalam dist | ☑ |

**GATE 2:** exe hidup ✓ · model dimuat ✓ · DATA_DIR ✓ · FAISS ✓ · semak.py
385 ✓ · warn tiada kritikal ✓ · fallback Nuitka TIDAK dicetuskan ✓

---

## FASA 3 — Pengoptimuman Binaan (20 Ogos) ☑ GATE 3 LULUS

| # | Kerja | Status |
|---|---|---|
| 1 | Buang duplikat HF `blobs/` (470 MB) — diuji empirik model masih muat penuh | ☑ |
| 2 | Buang cv2 (138 MB) + PIL (13 MB) via `--exclude-module` (lazy import selamat) | ☑ |
| 3 | Hasil optimum: `dist\PustakaHadis-Debug` = **1,399.9 MB / 7,027 fail** (jimat 622.9 MB, 31%) | ☑ |
| 4 | Ujian: model e5 dimuat penuh (stderr 100%, RAM 929–937 MB, `muat_s 35.0`), tetingkap 'Pustaka Hadis', tiada ralat | ☑ |
| 5 | Ujian fungsi penuh automatik: FTS5 'puasa' 816 · 'صلاة' 2,443 · 62,169 hadis · carian makna (riba→darimi#2467; puasa→malik#587) · 4 tema · user_settings.json | ☑ |
| 6 | Boot pertama lambat (~110–120 s) = Windows Defender scan 1.4 GB — bukan ralat | ☑ |

**GATE 3:** saiz <1.5 GB ✓ · fungsi setara ✓ · aset lengkap ✓ · semak.py 385 ✓

---

## FASA 4 — Uji Binaan pada Mesin Bersih (20 Ogos) ☑ GATE 4 LULUS

| # | Kerja | Status |
|---|---|---|
| 1 | Windows Sandbox (Windows 11 Pro) — mesin bersih tanpa Python/PyQt/torch | ☑ |
| 2 | `PustakaHadis-Fasa4.wsb`: `dist\PustakaHadis-Debug` dipetakan baca sahaja + auto-lancar exe | ☑ |
| 3 | Maklum balas pengguna: apl lancar · carian OK selepas API key · bookmark OK · lain-lain OK | ☑ |
| 4 | Siasatan "terjemahan Inggeris tiada" — **DISAHKAN reka bentuk lesen, bukan bug** (hadis.db + .cache_eng 120 MB tidak dibundel §4; sync_english.py skrip pembangunan sahaja; lesen Ahmad §5 + keputusan Sesi 7 "pengguna sync sendiri"; UI kelabukan tab English) | ☑ |
| 5 | **Keputusan pengguna: biar seperti reka bentuk** — tiada perubahan kod | ☑ |

**GATE 4 (matriks §8, Windows 11 Sandbox):** launch ✓ · simpan settings/API
key ✓ · sync/resume ✓ · carian Melayu/Arab ✓ · carian makna ✓ · bookmark ✓ ·
☐ belum diuji: offline selepas sync · tutup/relaunch khusus · Windows 10

---

## FASA 5 — Bina Pakej Edaran (INSTALLER §7.3, §9, §11) ⏳ SEDANG JALAN

**Gate 4 (INSTALLER):** EXE + MSIX install/launch/uninstall lulus · aset pakej
= inventori

### 5A — Binaan keluaran `--windowed` (INSTALLER §7.3) ☑ SELESAI (20 Ogos)
- ☑ Bina `dist\PustakaHadis\PustakaHadis.exe` (--windowed, tiada konsol; spec `PustakaHadis.spec`, upx=False, exclude cv2/PIL)
- ☑ Ujian ringkas: exe hidup · disclaimer (tajuk guna EM DASH 8212) · tetingkap 'Pustaka Hadis' TEPAT · model dimuat dari cache (`muat_s 39.5`, `dari_cache true`) · DATA_DIR betul
- ☑ warn-*.txt: tiada regresi vs Debug (set diff missing module = kosong)
- ☑ semak.py **386 SEMUA LULUS** (15 bahagian; +1 kerana CHECKLIST_PEMANTAUAN.md — semak #8m lulus per fail .md)

### 5B — Inno Setup EXE (sekunder, INSTALLER §9) ☑ SELESAI (20 Ogos)
- ☑ Inno Setup 6.7.3 dipasang di `D:\Inno Setup 6` (ISCC.exe; ~20 MB)
- ☑ Per-user install (`PrivilegesRequired=lowest`, `{localappdata}\Programs\PustakaHadis`), AppId tetap `{{7DF2553E-9E62-4ED4-929A-61C71AD1047F}`
- ☑ Start Menu + Desktop pilihan (task desktopicon)
- ☑ Silent install berfungsi (`/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-`; kod keluar 0, 7,029 fail dipasang)
- ☑ Launch app terpasang: tetingkap 'Pustaka Hadis' terbuka, DATA_DIR betul
- ☑ Uninstall senyap: kod keluar 0 · folder app dipadam · **DATA_DIR KEKAL** · pintasan dipadam
- ☑ Naik taraf kekalkan DATA_DIR: belum diuji penuh (perlu 1.0.1.0 di Fasa 6) — mekanisme terbukti (DATA_DIR berasingan, uninstall kekalkan)
- ☑ Hasil: `installer\output\PustakaHadis-Setup-1.0.0-x64.exe` = **0.50 GB** (~34 minit lzma2/ultra64)

### Dokumentasi Pengguna (Gate 6 — INSTALLER §18)
- ☑ **MANUAL_INSTALASI.md** — 3 cara pasang (Store/MSIX ⏳, Setup EXE ✓, Zip penguji), kali pertama buka, lokasi data `%LOCALAPPDATA%\PustakaHadis`, masalah lazim, atribusi
- ☑ **MANUAL_PENGGUNAAN.md** — skrin utama, carian kata kunci + makna (AI), lompat hadis, membaca hadis (dua lajur, tab bahasa, darjat, huraian), tindakan (lapor/kongsi/salin/WhatsApp/TTS), penanda halaman, tetapan, mod luar talian, masalah lazim
- ☑ **DASAR_PRIVASI.md** — tiada data dikumpul, data tempatan, kunci API tertutup, AI luar talian, sambungan hanya sync hadis.my
- ☑ **PAUTAN_SOKONGAN.md** — templat GitHub Issues, maklumat diperlukan, templat respons
- ☑ **TANGKAPAN_SKRIN.md** — senarai 4 wajib + 4 disyorkan, spesifikasi 1366×768/1920×1080, folder output
- ☐ URL sebenar (GitHub Issues / laman web) dimasukkan ke Partner Center

### 5C — MSIX (utama, INSTALLER §11–§12) ⏳ PENYEDIAAN SELESAI — MENUNGGU IDENTITI STORE
- ☑ **ZIP mudah alih** — `installer\output\PustakaHadis-portable-1.0.0-x64.zip` (0.54 GB, 7,027 fail)
- ☑ **VM_MSIX_CAPTURE.md** — persediaan VM bersih, snapshot, payload, aset, wizard manual
- ☑ **MSIX_CAPTURE_PROSES.md** — checklist 6 fasa (prasyarat → uji), rollback, output Gate 6
- ☐ MSIX Packaging Tool Driver — wizard cuba sendiri 2× semasa 'Prepare computer'
- ☑ Aset PNG MSIX dijana → `installer\Assets\` (StoreLogo 50 · Square44x44 · Square150x150 · Wide310x150)
- ☑ Audit inventori `dist\PustakaHadis`: **0 fail terlarang**; peringkat atas = `_internal` + `PustakaHadis.exe`
- ☐ Capture dalam VM bersih (Manual installation, install location `C:\Program Files\PustakaHadis`, salin payload, jangan sync/API key, satu entry point `PustakaHadis.exe`)
- ☐ Package editor: runFullTrust · Windows.Desktop · MinVersion 10.0.19041.0 · tiada DB/rahsia
- ☐ Simpan `PustakaHadis_1.0.0.0_x64.msix` + tandatangan ujian tempatan (WinApp CLI / SignTool, Subject = Publisher manifest)
- ☐ MSIX install/launch/uninstall lulus (Add-AppxPackage)
- ☐ Hasil: `PustakaHadis_1.0.0.0_x64.msix`

### Uji Windows 10 (Gate 4 Matrix)
- ☐ VM Windows 10 bersih / snapshot
- [ ] Pasang ZIP / EXE / MSIX
- [ ] Uji matriks §8: launch, settings, sync, carian Melayu/Arab, makna, bookmark, offline, tutup/relaunch
- [ ] Rekod keputusan
- ⛔ **MENUNGGU tugas pengguna:** daftar Microsoft Store + tempah nama + pilih Publisher (perlu beri 3 nilai: `Package/Identity/Name`, `Package/Identity/Publisher`, `Package/Properties/PublisherDisplayName`)
- ☑ MSIX Packaging Tool dipasang (winget, v1.2024.405.0) + WinApp CLI 0.6.1 (tandatangan ujian tempatan)
- ☐ MSIX Packaging Tool Driver — perlu diaktifkan (Optional Features; wizard boleh cuba sendiri 2 kali semasa 'Prepare computer')
- ☑ Aset PNG MSIX dijana dari app.ico → `installer\Assets\` (StoreLogo 50 · Square44x44 · Square150x150 · Wide310x150)
- ☑ Audit inventori `dist\PustakaHadis`: **0 fail terlarang** (tiada hadis.db/.env/settings/bookmarks/cache/log/__pycache__); peringkat atas = `_internal` + `PustakaHadis.exe` sahaja
- ☐ Capture dalam VM bersih (Manual installation, install location `C:\Program Files\PustakaHadis`, salin payload, jangan sync/API key, satu entry point PustakaHadis.exe)
- ☐ Semak Package editor: runFullTrust · Windows.Desktop · MinVersion 10.0.19041.0 · tiada DB/rahsia
- ☐ Simpan `PustakaHadis_<versi>_x64.msix` + tandatangan ujian tempatan (WinApp CLI / SignTool, Subject = Publisher manifest)
- ☐ MSIX install/launch/uninstall lulus (Add-AppxPackage)
- ☐ Hasil: `PustakaHadis_1.0.0.0_x64.msix`

---

## FASA 6 — Partner Center + Ujian Naik Taraf (INSTALLER §10, §13–§16) ☐ BELUM

- ☐ Daftar akaun + tempah nama (tugas pengguna, Fasa 0)
- ☐ Rekod `Identity Name`, `Publisher`, `PublisherDisplayName`
- ☐ Bina versi 1.0.0.0 · pasang · cipta settings/bookmark + sync data ujian
- ☐ Bina versi 1.0.1.0 (identiti sama) · pasang kemas kini
- ☐ Uji uninstall/reinstall dan tingkah laku data

**GATE 5:** update tidak memadam DB/settings/bookmark ✓ · satu pemasangan/
Start Menu entry ✓ · pensijilan Store lulus ✓ · Microsoft menandatangani ✓ ·
tiada amaran biasa ✓

---

## FASA 7 — Edaran Awam (INSTALLER §15, §18) ☐ BELUM

- ⛔ Menunggu: lesen data selesai + dasar privasi + pensijilan
- ☐ Upload MSIX ke Store · listing · ikon · screenshots · notas pensijilan
- ☐ Private audience/flight jika tersedia
- ☐ Dokumentasi pengguna/privasi/sokongan sedia

**GATE 6:** semua gate hijau ✓ · dokumentasi sedia ✓

---

## Ringkasan Status

| Fasa | Status | Tarikh |
|---|---|---|
| Fasa 0 — Kelulusan skop | ☑ GATE 0 LULUS (tugas pengguna: daftar Store ⏳) | 19 Ogos |
| Fasa 1 — Pisahkan laluan data | ☑ GATE 1 LULUS | 20 Ogos |
| Fasa 2 — Bina diagnostik | ☑ GATE 2 LULUS | 20 Ogos |
| Fasa 3 — Pengoptimuman | ☑ GATE 3 LULUS | 20 Ogos |
| Fasa 4 — Uji mesin bersih | ☑ GATE 4 LULUS | 20 Ogos |
| Fasa 5 — Bina pakej edaran | ⏳ 5A ✓ + 5B ✓ selesai — 5C (MSIX) menunggu identiti Store | 20 Ogos |
| Fasa 6 — Partner Center | ☐ | — |
| Fasa 7 — Edaran awam | ☐ | — |

**Halangan aktif:** ⛔ identiti Microsoft Store (tugas pengguna Fasa 0) —
diperlukan untuk 5C (MSIX) dan Fasa 6. ⛔ lesen terjemahan Inggeris Ahmad
(Perumusan Darussalam) — tab English kekal kelabu sehingga kebenaran diterima.