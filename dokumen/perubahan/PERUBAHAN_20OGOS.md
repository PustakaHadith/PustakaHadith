# Perubahan 20 Ogos 2026 — Folder Binaan Installer

> Log ringkas perubahan pada 20 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md`. Versi apl kekal **1.0**.
> FOLDER INI (`binaan_installer`) ialah salinan kerja installer —
> BUKAN repo git dan BUKAN folder utama `hadis` (developer workplace
> tidak disentuh; tiada komit di sini).

## Keputusan pengguna 20 Ogos

- Bekerja di **folder berasingan** untuk installer: `D:\Pustaka Quran
  Hadis\binaan_installer\` — salin sumber yang perlu (tanpa `.git`,
  venv, cache pengguna, data peribadi); folder utama `hadis` kekal
  bersih.
- Fasa 1 — **Pisahkan Laluan Data** selesai dan Gate LULUS.
- Fasa 2 — **Bina PyInstaller Diagnostik** selesai dan Gate LULUS.
- Fasa 3 — **Pengoptimuman Binaan** selesai dan Gate LULUS.

## Kerja Fasa 1 — Pisahkan Laluan Data (Gate LULUS)

1. **Folder binaan dicipta** — `binaan_installer` (450 MB): semua fail
   kod + dokumen + hadis.db + aset FAISS/model; tanpa `.git`, venv,
   cache, `dist`/`build`, data peribadi (user_settings, bookmarks,
   .env, kunci). README binaan = 385 semakan (semak #12 git + #9 cache
   pengguna dilangkau — bukan repo git; +1 selepas PERUBAHAN_20OGOS.md).

2. **`config.py` menjadi pusat laluan** (INSTALLER.md §3.1):
   - `ASSET_DIR` — aset baca sahaja (app.ico, hadis_faiss.index,
     hadis_id_map.pkl, .cache_models, sunnah_map).
   - `DATA_DIR` — data pengguna boleh tulis; mod pembangunan =
     folder projek (tingkah laku TIDAK berubah), mod frozen =
     `%LOCALAPPDATA%\PustakaHadis`.
   - Pemalar baharu: `BOOKMARKS_PATH`, `CACHE_SEMA`, `CACHE_HE`,
     `CACHE_ENG`, `CACHE_SYARAH`, `PROFIL_PATH`, `ICON_PATH`,
     `FAISS_INDEX`, `FAISS_MAP`, `MODEL_CACHE`, `SUNNAH_MAP`.

3. **Fail dipusatkan ke pemalar config**:
   - `db.py` — DB_PATH daripada config (import, bukan kira sendiri).
   - `api/hadis_api.py` — DB_PATH daripada config.
   - `ui/helpers.py` — SETTINGS/BOOKMARKS = config; sunnah_map =
     `SUNNAH_MAP`.
   - `ui/splash.py` — baca tema daripada `SETTINGS_PATH`.
   - `ui/disclaimer.py` — `_SETTINGS` daripada `SETTINGS_PATH`.
   - `core/sema_source.py` — CACHE = `CACHE_SEMA`.
   - `core/hadeethenc_api.py` — CACHE = `CACHE_HE`.
   - `core/semantic_search.py` — INDEX/MAP/MODEL/PROFIL daripada
     config; `rebuild_index` guna `ASSET_DIR`.
   - `core/syarah_source.py` — TIADA laluan cache (hanya URL OpenITI);
     tiada perubahan diperlukan (disahkan audit).
   - `sync.py`, `semak_db.py`, `semak_versi.py` — sudah import
     `DB_PATH` daripada config; tiada perubahan.

4. **Penyesuaian daripada INSTALLER.md §3.1:** `PROFIL_PATH`
   (`profil_model.json`) diletakkan di **DATA_DIR**, bukan ASSET_DIR —
   sebab kod menulis fail log masa muat model pada setiap larian;
   ASSET_DIR baca sahaja dalam MSIX akan mematikan rekod ini.

5. **Ujian baharu `uji_fasa1_data.py` (22/0)** — mensimulasikan
   `sys.frozen=True` dalam subproses: DATA_DIR ==
   `%LOCALAPPDATA%\PustakaHadis`; semua pemalar boleh tulis di DATA_DIR;
   semua aset di ASSET_DIR; TIADA fail baharu ditulis ke ASSET_DIR
   semasa larian frozen.

## Gate Fasa 1 (semua LULUS di folder binaan)

| Ujian | Keputusan |
|---|---|
| `semak.py` | SEMUA LULUS — 385 semakan (15 bahagian) |
| `semak_versi.py` | OK |
| `uji_lompat.py` | 67 lulus, 0 gagal |
| `uji_carian_arab.py` | SEMUA UJIAN LULUS |
| `main.py` | melancar tanpa ralat (offscreen) |
| `uji_fasa1_data.py` | 22 lulus, 0 gagal |

## Kerja Fasa 2 — Bina PyInstaller Diagnostik (Gate LULUS)

1. **`main.py` — sokongan frozen** (INSTALLER.md §6): tambah
   `import multiprocessing` + `multiprocessing.freeze_support()` pada
   permulaan `main()` (torch/sentence-transformers boleh guna
   multiprocessing). Sintaks disahkan; `uji_lompat.py` kekal 67/0.

2. **Venv binaan** — keputusan pengguna: guna `--system-site-packages`
   (jimat muat turun torch ~2GB; pakej sistem sedia ada dipinjam).
   - `py -3.14 -m venv --system-site-packages .venv-build` (Python
     3.14.6 x64).
   - Disahkan: torch 2.13.0+cpu, faiss, sentence_transformers, PyQt5
     5.15.11 tersedia; TIADA PySide/PyQt6 (satu binding Qt sahaja).
   - PyInstaller 6.22.0 + pyinstaller-hooks-contrib dipasang.
   - Rekod binaan: `installer_requirements-build-lock.txt` (pip freeze).

3. **Aset profil lengkap dibundel** (keputusan Fasa 0 + INSTALLER §4):
   - `.cache_models/` (model e5, 941 MB) disalin dari folder utama —
     mengandungi duplikat HF (snapshots + blobs = 2×460 MB); boleh
     dioptimumkan pada Fasa 3.
   - `hadis_faiss.index` (91.1 MB), `hadis_id_map.pkl` (0.8 MB),
     `profil_model.json`, `sunnah_map/` (1.1 MB), `app.ico`.
   - JANGAN bundel (disahkan tiada dalam dist): hadis.db*, .env,
     user_settings.json, bookmarks.json, .cache_sema/.he/.eng/.syarah.

4. **Arahan binaan** (INSTALLER §7.1 + profil lengkap):

   ```powershell
   python -m PyInstaller --noconfirm --clean --onedir --console `
     --name PustakaHadis-Debug --icon app.ico `
     --add-data "app.ico;." --add-data "sunnah_map;sunnah_map" `
     --add-data ".cache_models;.cache_models" `
     --add-data "hadis_faiss.index;." --add-data "hadis_id_map.pkl;." `
     --add-data "profil_model.json;." `
     --collect-all sentence_transformers --collect-all transformers `
     --collect-all tokenizers --collect-all faiss `
     --copy-metadata sentence-transformers --copy-metadata transformers `
     --copy-metadata torch main.py
   ```

   Masa binaan ~19 minit. Hasil: `dist\PustakaHadis-Debug\` =
   **2,022.8 MB, 7,065 fail** (terbesar: model.safetensors 460 MB,
   torch_cpu.dll 298 MB, hadis_faiss.index 93 MB, cv2 87 MB — cv2
   ditarik oleh transformers, bukan keperluan; boleh kecilkan Fasa 3).
   Tiada UPX (boleh rosakkan DLL Qt/torch).

5. **Semakan `warn-*.txt`** — 1,144 baris, 313 "missing module" unik;
   SEMUA ialah modul pilihan (torch distributed/xla/npu/ao/coreml,
   accelerate, bitsandbytes, botocore, datasets, dll). TIADA amaran
   untuk modul yang benar-benar digunakan (PyQt5, requests, pyperclip,
   tqdm, faiss, sentence_transformers, transformers, tokenizers).
   Nota: missing `torch._C.*` adalah normal (dalam _C.pyd).

## Kerja Fasa 3 — Pengoptimuman Binaan (Gate LULUS)

1. **Buang duplikat HF cache (jimat 470 MB)** — `.cache_models` HF
   standard ada `snapshots/` (fail fizikal penuh) + `blobs/` (salinan
   kedua 470 MB). `blobs/` dipindah → diuji model masih muat (uji
   empirik: SentenceTransformer muat OK, encode OK, 384 dimensi) →
   `blobs/` dipadam kekal. Pakej kini hanya SATU model.safetensors.

2. **Buang cv2 + PIL (jimat 151 MB)** — cv2 (138 MB) ditarik oleh
   transformers (video_utils.py + image_processing untuk model
   vision/OCR — TIDAK digunakan oleh aplikasi teks); PIL (13 MB) juga
   pilihan. Disahkan: aplikasi TIDAK import cv2/PIL; import cv2 dalam
   transformers ialah lazy import (dalam fungsi, bukan aras modul) —
   selamat. Tambah `--exclude-module cv2 --exclude-module PIL`.

3. **Hasil binaan optimum:** `dist\PustakaHadis-Debug` =
   **1,399.9 MB (1.4 GB) / 7,027 fail** — jimat **622.9 MB (31%)**
   daripada 2,022.8 MB. Semua aset lengkap; TIADA hadis.db*/settings/
   bookmarks/cache dalam pakej.

4. **Ujian binaan optimum (semua LULUS):**
   - Model e5 dimuat SEPENUHNYA (stderr: `Loading weights: 100%
     199/199`; RAM naik 78 → 929–937 MB; `profil_model.json` dikemas
     dengan `muat_s: 35.0, dari_cache: true`).
   - Tetingkap utama **'Pustaka Hadith'** terbuka (MainWindowTitle
     tepat).
   - Tiada traceback/ralat (stderr kosong selain progress loading).
   - DATA_DIR `%LOCALAPPDATA%\PustakaHadis` digunakan.
   - `warn-*.txt`: 313 missing module (semua pilihan) + excluded
     cv2/PIL — tiada amaran untuk modul sebenar.
   - Catatan: boot pertama lambat (~110–120 s) kerana Windows Defender
     mengimbas 1.4 GB pakej — bukan ralat aplikasi; larian seterusnya
     lebih cepat.

## Ujian fungsi penuh (Fasa 3 — automatik pada rantai binaan)

Ujian fungsi teras dijalankan pada rantai yang SAMA dengan exe
(hadis.db binaan + .cache_models tanpa blobs + indeks FAISS + id_map
dari `dist\_internal`):

| Ujian | Keputusan |
|---|---|
| Carian Melayu 'puasa' | 816 hasil |
| Carian Arab 'صلاة' (tanpa tashkeel) | 2,443 hasil |
| Jumlah hadis | 62,169 |
| Model e5 dimuat (tanpa blobs) | 32.8 s, 384 dimensi |
| Indeks FAISS dimuat | 62,169 vektor × 384 |
| Encode soalan | 1.93 s |
| Carian makna 'hukum riba dalam islam' | Hadis muamalat: darimi #2467, malik #1152, nasai #4505 (skor 0.87–0.88) |
| Carian makna 'kelebihan puasa ramadhan' | Hadis puasa: malik #587, darimi #1698, ahmad #23097 (skor 0.86) |
| Tema dark/light/neutral/lightneutral | Semua dipanggil tanpa ralat, palet berbeza |
| user_settings.json (DATA_DIR) | Dibaca: disclaimer_dibaca, deklarasi_dibaca, theme |
| Exe tetingkap utama | 'Pustaka Hadith' terbuka, model dimuat penuh |

Kesimpulan: fungsi AI (carian makna), carian teks (FTS5), tema, dan
pemisahan data (DATA_DIR) SEMUA berfungsi pada rantai binaan Fasa 3.

## Kerja Fasa 4 — Uji Binaan pada Mesin Bersih (Gate LULUS)

1. **Windows Sandbox tersedia** (Windows 11 Pro, `Containers-Disposable
   ClientVM` Enabled, `WindowsSandbox.exe` wujud) — mesin bersih sebenar
   tanpa Python/PyQt/torch.

2. **Fail `PustakaHadis-Fasa4.wsb` dicipta** — memetakan
   `dist\PustakaHadis-Debug` (baca sahaja) ke Desktop Sandbox +
   LogonCommand auto-lancar exe. Sandbox boot OK (vmmemWindowsSandbox
   2.5 GB, tetingkap 'Windows Sandbox' kelihatan).

3. **Ujian pengguna dalam Sandbox — maklum balas:**
   - ✅ Apl berjalan lancar
   - ✅ Carian OK selepas API key dipasang
   - ✅ Bookmark OK
   - ✅ Lain-lain OK setakat ini
   - ❌ **Terjemahan Inggeris tiada** (tab English kelabu)

4. **Siasatan terjemahan Inggeris — DISAHKAN reka bentuk lesen, bukan
   bug:**
   - INSTALLER §4 "Jangan bundel": `hadis.db` + `.cache_eng` (120.3 MB,
     28 fail JSON CDN) TIDAK dibundel dalam pakej edaran.
   - Aplikasi edaran tidak memuat turun/padan Inggeris: `sync_english.py`
     ialah skrip pembangunan (baca `.cache_eng` CDN → padan teks Arab →
     tulis jadual `terjemahan_eng` dalam hadis.db); UI TIDAK memanggilnya.
   - DB binaan pembangunan ada 31,833 terjemahan (7 daripada 9 kitab;
     ahmad + darimi tiada sumber) — tetapi pengguna akhir tidak menerima
     jadual ini kerana DB tidak dibundel dan tidak dimuat turun.
   - UI kelabukan tab English bila tiada data (`ui/pages.py` `set_available`).
   - Keputusan lesen `PERMOHONAN_LESEN_AHMAD.md` §5: terjemahan Inggeris
     Musnad Ahmad TIDAK boleh diedarkan sehingga kebenaran Darussalam
     diterima. Keputusan Sesi 7: "pengguna sync sendiri" (ZIP tiada DB).
   - **Keputusan pengguna (20 Ogos): biar seperti reka bentuk — tiada
     perubahan kod.** Inggeris kembali bila DB pengguna diisi
     `terjemahan_eng` atau keputusan lesen diubah.

5. **Gate Fasa 4 (matriks INSTALLER §8) — LULUS** pada Windows 11
   Sandbox: launch pengguna biasa ✅, simpan settings/API key ✅, sync/
   resume ✅, carian Melayu/Arab ✅, carian makna ✅, bookmark ✅.
   Belum diuji: offline selepas sync, tutup/relaunch khusus, Windows 10.

## Kerja Fasa 5A — Binaan Keluaran `--windowed` (20 Ogos)

1. **Checklist pemantauan dicipta** — `dokumen/CHECKLIST_PEMANTAUAN.md`
   (Fasa 0–7 + gate + tugas pengguna + halangan; semak imbang kerja).
   Kiraan semak.py naik 385 → **386** (semak #8m lulus per fail .md);
   README binaan dikemas kini.

2. **Spec keluaran `PustakaHadis.spec`** — salinan spec Debug dengan:
   `name='PustakaHadis'`, `console=False` (windowed), `upx=False`
   (keputusan tiada UPX); kekal exclude cv2/PIL + collect-all + aset.

3. **Bina (~21 minit)** — `dist\PustakaHadis` = **1,399.9 MB / 7,027
   fail** (sama dengan Debug — hanya konsol ditanggalkan).

4. **warn-PustakaHadis.txt** — set diff vs warn Debug: **kosong**
   (tiada missing module baharu/hilang; semua pilihan).

5. **Ujian exe windowed (semua LULUS):**
   - Proses hidup selepas 3 s; disclaimer 'Pustaka Hadith — Makluman'
     muncul (~6–12 s; tajuk guna EM DASH U+2014, bukan sempang);
   - Enter lulus disclaimer → tetingkap utama **'Pustaka Hadith'**
     (padanan tepat) terbuka; model dimuat dari cache dibundel
     (`profil_model.json` kemasukan baharu: `muat_s 39.5`,
     `import_s 35.0`, `dari_cache true` — model TIDAK dimuat turun);
   - DATA_DIR `%LOCALAPPDATA%\PustakaHadis` — user_settings.json
     (`disclaimer_dibaca:true`) + profil_model.json dikemas kini;
   - Tiada konsol muncul (windowed berfungsi).
   - Nota ujian: skrip uji GUI mula gagal kerana (a) `$script:found`
     vs `$found` skop dalam fungsi PowerShell; (b) padanan tajuk tepat
     gagal — tajuk disclaimer guna em dash. Diselesaikan.

6. **Gate 5A:** binaan windowed ✓ · ujian ringkas ✓ · warn tiada
   regresi ✓ · semak.py 386 SEMUA LULUS ✓. Langkah seterusnya: 5B
   (Inno Setup EXE).

## Kerja Fasa 5B — Inno Setup EXE (20 Ogos)

1. **Inno Setup 6.7.3 dipasang** — muat turun dari GitHub
   (`is-6_7_3`, 10.1 MB; URL tag guna garis bawah, bukan titik);
   dipasang senyap ke **`D:\Inno Setup 6`** (bukan C:) — ISCC.exe
   wujud, ~20 MB sahaja.

2. **`installer\PustakaHadis.iss`** — ikut INSTALLER §9:
   `PrivilegesRequired=lowest`, `DefaultDirName={localappdata}\Programs\
   PustakaHadis`, AppId tetap `{{7DF2553E-9E62-4ED4-929A-61C71AD1047F}`
   (direkod, jangan tukar), task desktopicon, `ArchitecturesAllowed/
   InstallIn64BitMode=x64compatible`, `lzma2/ultra64` + solid.

3. **Bina (~34 minit)** — `installer\output\
   PustakaHadis-Setup-1.0.0-x64.exe` = **0.50 GB** (mampat baik;
   anggaran awal 1.2–1.5 GB tidak tepat — lzma2/ultra64 + solid).

4. **Uji silent install + uninstall (semua LULUS):**
   - `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-` → kod keluar 0;
     7,029 fail dipasang ke `%LOCALAPPDATA%\Programs\PustakaHadis`;
     pintasan Start Menu 'Pustaka Hadith' wujud;
   - Launch app terpasang → tetingkap 'Pustaka Hadith' terbuka; DATA_DIR
     betul (user_settings.json);
   - Uninstall senyap (`unins000.exe /VERYSILENT`) → kod keluar 0;
     folder app dipadam; **DATA_DIR `%LOCALAPPDATA%\PustakaHadis`
     KEKAL** (tidak dipadam — betul); pintasan Start Menu dipadam.
   - Naik taraf kekalkan DATA_DIR: mekanisme terbukti (DATA_DIR
     berasingan dari folder app); ujian penuh 1.0.0→1.0.1 di Fasa 6.

5. **Gate 5B:** per-user ✓ · AppId tetap ✓ · Start Menu + Desktop
   pilihan ✓ · silent install ✓ · uninstall lulus ✓ · DATA_DIR kekal ✓ ·
   hasil setup 0.50 GB ✓. Langkah seterusnya: 5C (MSIX — menunggu
   identiti Microsoft Store).

## Kerja Fasa 5C — Penyediaan MSIX (20 Ogos)

Penyediaan yang boleh dilakukan tanpa identiti Partner Center:

1. **Alatan dipasang:** MSIX Packaging Tool (winget, v1.2024.405.0) +
   WinApp CLI 0.6.1 (tandatangan ujian tempatan, INSTALLER §13). Nota:
   MSIX Packaging Tool Driver (Optional Features) belum aktif di mesin
   ini — wizard boleh cuba sendiri 2 kali semasa 'Prepare computer',
   atau aktifkan di VM bersih.

2. **Aset PNG MSIX dijana** dari `app.ico` (256×256 RGBA) → `installer\
   Assets\`: `StoreLogo.png` 50×50, `Square44x44Logo.png` 44×44,
   `Square150x150Logo.png` 150×150, `Wide310x150Logo.png` 310×150
   (ikon dipusatkan 85% dalam ruang wide). PIL 12.2.0 dari venv binaan.

3. **Audit inventori `dist\PustakaHadis`:** 0 fail terlarang (tiada
   hadis.db*/.env/user_settings.json/bookmarks.json/.cache_sema|he|eng|
   syarah/*.bak/__pycache__/log audit). Folder peringkat atas =
   `_internal` + `PustakaHadis.exe` sahaja — bersih untuk capture.

4. **Menunggu pengguna (⛔):** daftar akaun Microsoft Store
   (https://storedeveloper.microsoft.com/) + tempah nama "Pustaka
 Hadith" + pilih nama Publisher. Selepas itu berikan 3 nilai:
   `Package/Identity/Name`, `Package/Identity/Publisher`,
   `Package/Properties/PublisherDisplayName` (INSTALLER §10).

5. **Langkah 5C seterusnya (selepas identiti):** capture dalam VM bersih
   (Manual installation, install location `C:\Program Files\
   PustakaHadis`, salin payload, jangan sync/API key, satu entry point
   `PustakaHadis.exe`); semak Package editor (runFullTrust,
   Windows.Desktop, MinVersion 10.0.19041.0, tiada DB/rahsia); simpan
   `PustakaHadis_1.0.0.0_x64.msix`; tandatangan ujian tempatan (WinApp
   CLI/SignTool, Subject = Publisher manifest); uji Add-AppxPackage
   install/launch/uninstall.

## Kerja Dokumentasi Pengguna — Manual (20 Ogos)

Dokumentasi pengguna untuk binaan edaran dicipta (Gate 6, INSTALLER
§18 — "dokumentasi pengguna/privasi/sokongan sedia"):

1. **`dokumen/manual/manual/manual/MANUAL_INSTALASI.md`** — keperluan (Windows 10/11 x64,
   tiada Python); 3 cara pasang: Microsoft Store (MSIX — status:
   sedang disediakan), pemasang EXE (`PustakaHadis-Setup-1.0.0-x64.exe`,
   per-user, naik taraf tidak padam data, nyahpasang tidak padam data),
   Zip mudah alih (penguji dalaman, ekstrak penuh dahulu, jalan
   `PustakaHadis.exe`); kali pertama buka (splash + notis + Tetapan
   API hadis.my); lokasi data `%LOCALAPPDATA%\PustakaHadis` (hadis.db,
   user_settings.json, bookmarks.json — jangan padam); masalah lazim
   (lambat kali pertama, tab English kelabu, mod luar talian); sumber &
   atribusi.

2. **`dokumen/manual/manual/manual/MANUAL_PENGGUNAAN.md`** — pengenalan 9 kitab + 62,169
   hadis; skrin utama (carian, kitab, gear, bintang, dadu rawak);
   carian kata kunci + carian makna (AI, soalan penuh); lompat terus
   hadis (433 / bukhari 433 / B433 / b:433 / Ctrl+G); membaca hadis
   (dua lajur: Arab|Transliterasi kanan, Melayu|Indonesia|English kiri;
   darjat ulama; huraian SemakHadis; syarah); bar tindakan (Lapor
   ralat / Kongsi WhatsApp / Salin 3 pilihan / 🔊 TTS / navigasi
   hadis jiran); penanda halaman; tetapan (tema, fon/saiz, bahasa,
   transliterasi, API dengan kunci bertopeng + pengesahan); mod luar
   talian (data tempatan, carian makna setempat); masalah lazim;
   sumber & atribusi.

3. **`dokumen/surat/sokongan/surat/sokongan/surat/sokongan/DASAR_PRIVASI.md`** — tiada data peribadi dikumpul,
   tiada telemetri/analitik, data hanya tempatan (`%LOCALAPPDATA%\
   PustakaHadis`), kunci API tertutup, carian makna AI sepenuhnya luar
   talian, sambungan hanya untuk sync hadis.my, hak padam/akses/portabiliti.

4. **`dokumen/surat/sokongan/surat/sokongan/surat/sokongan/PAUTAN_SOKONGAN.md`** — cadangan GitHub Issues, maklumat
   diperlukan (URL, e-mel, laman web), templat respons sokongan.

5. **`dokumen/penerbitan/penerbitan/penerbitan/TANGKAPAN_SKRIN.md`** — senarai 4 wajib (skrin utama,
   butiran hadis, carian makna, tetapan) + 4 disyorkan (penanda halaman,
   splash, lompat hadis, tema), spesifikasi 1366×768/1920×1080 PNG,
   folder `installer\StoreAssets\Screenshots\`.

6. **Status:** manual sedia untuk Gate 6; URL sebenar (GitHub Issues /
   laman web) dimasukkan ke Partner Center selepas identiti Store.

## Kerja Persediaan MSIX Lanjutan (20 Ogos — Selepas Sesi)

1. **ZIP mudah alih** — `installer\output\PustakaHadis-portable-1.0.0-x64.zip`
   (0.54 GB, 7,027 fail) dicipta dari `dist\PustakaHadis` untuk
   penguji dalaman (keputusan Fasa 0).

2. **penerbitan/penerbitan/VM_MSIX_CAPTURE.md** — dokumentasi penuh persediaan VM bersih:
   spesifikasi VM, pemasangan alatan (winget MSIX Packaging Tool +
   WinApp CLI), salin payload + aset PNG, cipta snapshot wajib,
   wizard Manual installation, capture hanya buka/tutup aplikasi (tiada
   sync/API key), Package Editor semak (runFullTrust, Windows.Desktop,
   MinVersion 10.0.19041.0, 4 PNG, tiada DB/rahsia), simpan + tandatangan
   ujian (winappcert + SignTool), uji Add-AppxPackage, rollback ke
   snapshot.

3. **penerbitan/penerbitan/MSIX_CAPTURE_PROSES.md** — checklist 6 fasa (prasyarat → uji)
   dengan status kotak semak, output diperlukan untuk Gate 6 (MSIX,
   sijil ujian, tangkapan skrin, URL privasi/sokongan).

4. **CHECKLIST_PEMANTAUAN.md** dikemas kini: 5C diperluas dengan item
   ZIP, VM docs, proses capture; dokumentasi pengguna ditanda ☑;
   ditambah seksyen "Uji Windows 10 (Gate 4 Matrix)" ⏳.

5. **MSIX Packaging Tool Driver** — carian Optional Features tidak
   dijumpai (mungkin dipasang bersama alatan MSIX / wizard cuba
   sendiri 2×).

## Kerja Lazy Loading (21 Ogos — Pelaksanaan)

Mengatasi keluhan pengguna: "tak boleh kah untuk kali ke 2 dan
seterusnya semasa apl dilancarkan ianya dijalankan dilatar? pengguna
akan bosan menunggu melihat ia memuat model setiap kali hendak guna?"

**Arsitek Baharu: Lazy Loading + Smart Splash**

| Sebelum | Selepas |
|---|---|
| Disclaimer → Splash model ~30s → UI | Disclaimer → UI **langsung** (< 3s) |
| Model dimuat startup (PreloadWorker) | Model dimuat **hanya pada carian makna pertama** |
| Splash model tidak boleh diklik (ada skip) | Tidak ada splash model — splash hanya untuk notis |

**Fail Diubah:**
- `main.py` — tanggal splash model loading; startup: Disclaimer → UI
- `ui/app_qt.py` — tanggalkan `_mula_pramuat()`, `_on_pramuat_siap()`,
  `kemajuan_pramuat`, `siap_pramuat`, `_model_sedia`, `_preload`
- `ui/workers.py` — `SemanticWorker`: tambah signal
  `model_loading_started(int token)` dipancar **sebelum** muat model
- `ui/pages_carian.py` — tangani signal → papar inline
  "🤖 Memuatkan model AI…" di indikator carian
- `semak.py` — semakan #8k dikemas kini untuk arsitek Lazy Loading
- `README.md` — kiraan semakan 393 → **392**

**Verifikasi:**
- `semak.py` 392/392 LULUS
- `uji_lompat.py` 67/0 LULUS
- PustakaApp: preload methods removed ✅
- SemanticWorker: `model_loading_started` signal ✅
- main.py: no splash preload ✅
- pages_carian.py: inline loading handler ✅

**Build Baharu (Lazy Loading):**
- `dist\PustakaHadis` 1.36 GB (windowed, tiada splash model)
- `installer\output\PustakaHadis-portable-1.0.0-x64.zip` 0.4 GB
- `installer\output\PustakaHadis-Setup-1.0.0-x64.exe` 0.48 GB

---

## Ringkasan Hari Ini (21 Ogos)

| Item | Status |
|---|---|
| Fasa 4 (Sandbox) | ✅ LULUS |
| Fasa 5A (Windowed) | ✅ LULUS — `dist\PustakaHadis` 1.36 GB (Lazy Load) |
| Fasa 5B (Inno EXE) | ✅ LULUS — 0.48 GB setup (Lazy Load) |
| Fasa 5C (MSIX) | ⏳ Penyediaan siap, menunggu identiti Store |
| ZIP Portable | ✅ 0.4 GB (Lazy Load) |
| **Lazy Loading + Smart Splash** | ✅ **SELESAI** |
| Manual Instalasi | ✅ |
| Manual Penggunaan | ✅ |
| Dasar Privasi | ✅ |
| Pautan Sokongan | ✅ (templat) |
| Tangkapan Skrin | ✅ (senarai) |
| VM/Proses Capture | ✅ (dokumen) |
| Uji Windows 10 | ⏳ Belum |
| semak.py | **392 LULUS** |

## Gate Fasa 2 (semua LULUS di folder binaan)

| Ujian | Keputusan |
|---|---|
| Binaan PyInstaller onedir --console | Selesai tanpa ralat (~19 minit) |
| `warn-*.txt` | Tiada amaran kritikal (313 pilihan sahaja) |
| Exe dilancarkan | HIDUP — tetingkap 'Pustaka Hadith - Makluman' muncul |
| Disclaimer diluluskan (Enter) | user_settings.json `disclaimer_dibaca:true` ditulis |
| Model e5 dimuat | RAM naik 78 → 596 MB; tetingkap utama 'Pustaka Hadith' terbuka |
| DATA_DIR frozen | `%LOCALAPPDATA%\PustakaHadis` — user_settings.json + profil_model.json ditulis DI SINI |
| Folder EXE bersih | Tiada hadis.db dalam dist — data dipisah (Fasa 1 berfungsi dalam binaan sebenar) |
| Aset dalam `_internal\` | app.ico, sunnah_map, .cache_models, hadis_faiss.index, hadis_id_map.pkl, profil_model.json SEMUA ADA |
| Indeks FAISS binaan | Dimuat: 62,169 vektor × 384 dimensi (id_map 62,169) |
| `semak.py` | SEMUA LULUS — 385 semakan (15 bahagian) |

Ujian manual untuk pengguna (INSTALLER §7.2): tema gelap/cerah, API
key, sync, carian Melayu/Arab, carian makna, rawak/bookmarks/huraian/
salin, tutup/buka semula, mod luar talian, pengguna biasa — boleh
dijalankan pada mesin pembangun bila selesa.

## Langkah seterusnya

- **Fasa 5B — Inno Setup EXE** (INSTALLER §9): per-user install
  (`PrivilegesRequired=lowest`), AppId tetap, Start Menu + Desktop
  pilihan, silent install, naik taraf kekalkan DATA_DIR. Hasil:
  `PustakaHadis-Setup-1.0-x64.exe`.
- **Fasa 5C — MSIX utama** (INSTALLER §11–§12): MSIX Packaging Tool
  dalam VM bersih, identiti Partner Center, x64, runFullTrust; MSIX
  install/launch/uninstall lulus; aset pakej = inventori.
- **Fasa 0 tugas pengguna:** daftar akaun Microsoft Store
  (https://storedeveloper.microsoft.com/) + tempah nama "Pustaka
 Hadith" + pilih nama Publisher — WAJIB sebelum 5C/6 (identiti MSIX).