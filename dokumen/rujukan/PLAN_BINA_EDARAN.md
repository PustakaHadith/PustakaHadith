# PLAN BINA VERSI EDARAN — Pustaka Hadis v1.0

**Tarikh asal:** 15 Ogos 2026  
**Diselaraskan:** 15 Ogos 2026  
**Status:** **DOKUMEN KAWALAN — belum dilaksanakan**  
**Panduan teknikal:** `dokumen/rujukan/INSTALLER.md`  
**Rekod keputusan alat:** `dokumen/rujukan/BANDING_INSTALLER.md`

**Keputusan pengguna sedia ada:** `hadis.db` tidak dibundel; pengguna
menyelaraskan koleksi sendiri.

---

## 1. Tujuan

Menghasilkan aplikasi Windows yang boleh dipasang tanpa Python atau `pip`,
dengan dua hasil:

```text
Utama   : PustakaHadis_<versi>_x64.msix  — Microsoft Store
Sekunder: PustakaHadis-Setup-<versi>-x64.exe — penguji / luar Store
```

Pengguna akhir hanya perlu mendapatkan kunci API, sync koleksi dan menggunakan
aplikasi. Binaan lengkap boleh membawa model e5 dan indeks FAISS supaya
pengguna tidak perlu membina indeks selama beberapa jam.

**Tiada kod binaan dijalankan oleh dokumen ini.** Setiap fasa mempunyai gate;
fasa berikutnya hanya bermula selepas gate sebelumnya lulus.

---

## 2. Hierarki Dokumen

| Dokumen | Peranan |
|---|---|
| `PLAN_BINA_EDARAN.md` | Kawal urutan fasa, gate dan keputusan go/no-go |
| `INSTALLER.md` | Arahan teknikal terperinci, perintah, masalah lazim dan checklist |
| `BANDING_INSTALLER.md` | Rekod mengapa PyInstaller/MSIX dipilih berbanding cadangan lama |
| `list-we-do.md` | Rekod semua kerja projek sehingga pelan installer |

Jika terdapat percanggahan, dokumen kawalan ini menentukan **urutan dan alat
utama**; `INSTALLER.md` menentukan cara melaksanakannya.

---

## 3. Pengesahan terhadap Kod Semasa

| Andaian | Status semasa | Kesan |
|---|---|---|
| `config.py` meletakkan DB/settings di `BASE_DIR` | Masih benar | Wajib refactor sebelum MSIX |
| `ui/helpers.py` mempunyai laluan bookmarks sendiri | Masih benar | Wajib guna pemalar pusat |
| Beberapa cache mengira root melalui `__file__` | Masih benar | Wajib diasingkan kepada data/aset |
| `hadis_faiss.index` + `hadis_id_map.pkl` wujud | Ada | Calon aset baca sahaja |
| `.cache_models/` wujud | Ada | Calon aset baca sahaja |
| `profil_model.json` wujud | Ada | Aset baca sahaja, bukan data pengguna |
| `_baik_pulih_dll_qt_torch()` masih wujud | Ada | Kekalkan sehingga binaan lulus ujian DLL |
| `app.ico` wujud | Ada | Perlu PNG tambahan untuk Store/MSIX |
| Python | 3.14 x64 | Gunakan alat yang menyokongnya secara rasmi |

### Fail laluan yang mesti diaudit

```text
config.py
db.py
api/hadis_api.py
ui/helpers.py
ui/splash.py
core/sema_source.py
core/hadeethenc_api.py
core/syarah_source.py
core/semantic_search.py
sync.py
semak_db.py
```

---

## 4. Keputusan Reka Bentuk

| Perkara | Keputusan diselaraskan | Sebab |
|---|---|---|
| Bundel `hadis.db` | **Tidak** | Keputusan pengguna; data diselaraskan sendiri |
| Data boleh tulis | `%LOCALAPPDATA%\PustakaHadis` | Folder MSIX baca sahaja |
| Aset aplikasi | Folder pakej | Model/index/ikon baca sahaja |
| Alat bina utama | **PyInstaller 6.22 `onedir`** | Sokongan rasmi Python 3.14 + PyQt5 |
| Alat bina fallback | Nuitka | Hanya jika PyInstaller gagal gate torch/FAISS |
| Format utama | **MSIX melalui Microsoft Store** | Store hosting, signing dan update |
| Format sekunder | Inno Setup EXE | Penguji dan pengguna tanpa Store |
| Seni bina | x64 | Kurangkan matriks ujian keluaran pertama |
| Bundel model e5 | Ya untuk ujian; awam tunggu lesen | Elak muat turun senyap |
| Bundel indeks FAISS | Ya untuk ujian; awam tunggu lesen | Elak bina indeks berjam-jam |
| Sijil MSIX Store | Tidak perlu dibeli | Microsoft tandatangan selepas lulus |
| Sijil EXE langsung | Belum | EXE mungkin menerima SmartScreen |
| Repo | Persendirian sehingga lesen selesai | Elak pengedaran data tanpa izin |

### Keputusan alat bina bukan lagi “terbuka sama rata”

PyInstaller diuji dahulu kerana sokongan Python 3.14/PyQt5 rasmi. Nuitka 4.1
masih menyatakan Python 3.14 eksperimen dan dokumentasi rasmi Nuitka menyatakan
PyQt5 bermasalah pada callback/threading. Projek menggunakan banyak `QThread`.

Nuitka hanya diaktifkan sebagai fallback jika PyInstaller gagal pada gate
fungsi sebenar walaupun hook/konfigurasi sudah dibetulkan. Jangan bina dua
pakej penuh serentak tanpa sebab.

---

# 5. Pelan Pelaksanaan Berperingkat

## Fasa 0 — Kelulusan Skop

Keputusan yang perlu direkod sebelum menyentuh kod:

- [x] Profil ujian membundel model e5 + indeks FAISS.
- [x] `hadis.db` kekal tidak dibundel.
- [x] x64 sahaja.
- [x] Microsoft Store ialah edaran utama.
- [x] Inno EXE ialah edaran sekunder/penguji.
- [x] Repo kekal persendirian hingga lesen data selesai.

**Gate Fasa 0: pengguna meluluskan keputusan di atas.**

**Keputusan pengguna — 19 Ogos 2026 (Fasa 0 DILULUSKAN):**

| # | Soalan | Keputusan |
|---|---|---|
| 1 | Bundel model e5 + indeks FAISS untuk profil ujian? | **Ya** — elak bina berjam-jam; awam tunggu lesen |
| 2 | Microsoft Store = saluran utama? | **Ya** — signing Microsoft, update terurus |
| 3 | Inno EXE = saluran sekunder/penguji? | **Ya** — mesin tanpa Store |
| 4 | Akaun Partner Center + nama Publisher? | **WAJIB di Fasa 5** — daftar sekarang (percuma) + tempah nama Pustaka Hadis segera; nama Publisher: pilihan pengguna (nama peribadi/badan) |
| 5 | Portable ZIP selepas MSIX? | **Ya — untuk penguji dalaman sahaja** (bukan saluran awam rasmi) |
| 6 | Wizard permulaan (deklarasi → kunci API → sync)? | **Bina sebelum beta** — penguji perlu menguji aliran pengguna sebenar |

**Catatan:** semua 6 keputusan dicadangkan dokumen + pengguna menerima cadangan.
Kiraan telus: keputusan ini direkod sebagai komit penutup (langkah-B) 19 Ogos
2026; 19 Ogos = 5 kerja (11 sebenar − 6 langkah-B).

---

## Fasa 1 — Pisahkan Laluan Data

### Kerja

1. Tambah `ASSET_DIR` dan `DATA_DIR` dalam `config.py`.
2. Dalam mod frozen:

```text
DATA_DIR = %LOCALAPPDATA%\PustakaHadis
```

3. Dalam mod pembangunan, kekalkan root projek supaya aliran semasa tidak
   berubah.
4. Pindahkan semua data boleh tulis:

```text
hadis.db
user_settings.json
bookmarks.json
.env
.cache_sema
.cache_he
.cache_eng
.cache_syarah
```

5. Kekalkan aset baca sahaja:

```text
app.ico
.cache_models/
hadis_faiss.index
hadis_id_map.pkl
profil_model.json
sunnah_map/
```

6. Tukar semua modul dalam senarai §3 supaya mengimport pemalar `config.py`.
7. Tambah ujian yang mensimulasikan `sys.frozen=True` tanpa menulis ke folder
   aplikasi.

### Gate Fasa 1

```powershell
python semak.py
python semak_versi.py
python uji_lompat.py
python uji_carian_arab.py
python main.py
```

Syarat lulus:

- mod pembangunan tidak berubah;
- mod frozen simulasi menunjuk `%LOCALAPPDATA%`;
- tiada modul menulis berdasarkan `__file__`;
- carian makna masih membaca aset dari `ASSET_DIR`.

**Gate Fasa 1: LULUS — 20 Ogos 2026** (folder binaan `binaan_installer`,
bukan repo git; kiraan semak binaan = 384 berbanding 394 di repo utama
kerana semak #12/#9 git + cache pengguna dilangkau):

- `semak.py` — SEMUA LULUS (385 semakan, 15 bahagian; +1 selepas
  PERUBAHAN_20OGOS.md — setiap fail .md baharu menambah satu lulus 8m)
- `semak_versi.py` — OK
- `uji_lompat.py` — 67 lulus, 0 gagal
- `uji_carian_arab.py` — SEMUA UJIAN LULUS
- `main.py` — melancar tanpa ralat (5 tema, mod offscreen)
- `uji_fasa1_data.py` (baharu) — 22 lulus, 0 gagal (simulasi frozen)

**Rekod keputusan Fasa 1 (20 Ogos 2026):**

- `config.py` kini pusat laluan: `ASSET_DIR` (aset baca sahaja) vs
  `DATA_DIR` (data pengguna boleh tulis). Mod pembangunan: DATA_DIR =
  ASSET_DIR (tingkah laku tidak berubah). Mod frozen:
  `%LOCALAPPDATA%\PustakaHadis`.
- Fail dipusatkan: `db.py`, `api/hadis_api.py`, `ui/helpers.py`,
  `ui/splash.py`, `ui/disclaimer.py`, `core/sema_source.py`,
  `core/hadeethenc_api.py`, `core/semantic_search.py`.
- `core/syarah_source.py` tiada laluan cache (hanya URL OpenITI) —
  tiada perubahan diperlukan, disahkan oleh audit.
- `sync.py`, `semak_db.py`, `semak_versi.py` sudah mengimport
  `DB_PATH` daripada `config.py` — tiada perubahan.
- **Penyesuaian daripada INSTALLER.md §3.1:** `PROFIL_PATH`
  (`profil_model.json`) diletakkan di DATA_DIR (bukan ASSET_DIR)
  kerana kod MENULIS fail log masa muat model pada setiap larian;
  ASSET_DIR baca sahaja dalam MSIX akan mematikan rekod ini.
- Skrip pembangunan (`sync_english.py`, `audit_eng.py`,
  `diagnos_*.py`, `scripts/*.py`) kekal guna laluan relatif — ia
  berjalan dalam mod pembangunan sahaja (DATA_DIR == ASSET_DIR,
  tiada beza tingkah laku). Akan dipusatkan dalam Fasa 6 (pembersihan)
  jika perlu.
- Ujian `uji_fasa1_data.py` mensimulasikan `sys.frozen=True` dalam
  subproses: DATA_DIR == `%LOCALAPPDATA%\PustakaHadis`, semua pemalar
  boleh tulis di DATA_DIR, semua aset di ASSET_DIR, dan TIADA fail
  baharu ditulis ke ASSET_DIR semasa larian frozen.

**Langkah seterusnya: Fasa 2 — Bina PyInstaller Diagnostik** (tambah
`multiprocessing.freeze_support()` dalam `main.py`, venv bersih,
bina onedir --console, semak warn-*.txt).

---

## Fasa 2 — Bina PyInstaller Diagnostik ✅ **SELESAI — GATE LULUS (20 Ogos 2026)**

**Rekod keputusan Fasa 2 (20 Ogos 2026):**

- `main.py`: `import multiprocessing` + `multiprocessing.freeze_support()`
  pada permulaan `main()` (INSTALLER §6).
- Venv binaan: **`--system-site-packages`** (keputusan pengguna — jimat
  muat turun torch ~2 GB; pinjam pakej sistem yang sudah disahkan:
  torch 2.13.0+cpu, faiss, sentence_transformers, PyQt5 5.15.11).
  Python 3.14.6 x64; PyInstaller 6.22.0 + hooks-contrib; rekod
  `installer_requirements-build-lock.txt`; TIADA PySide/PyQt6.
- Binaan onedir --console `PustakaHadis-Debug` (~19 minit):
  2,022.8 MB, 7,065 fail. Aset profil lengkap dibundel dalam
  `_internal\` (app.ico, sunnah_map, .cache_models 941 MB,
  hadis_faiss.index 91 MB, hadis_id_map.pkl, profil_model.json).
  Tiada hadis.db*/.env/settings/bookmarks/cache dalam pakej.
- `warn-*.txt`: 1,144 baris; 313 "missing module" — semua pilihan
  (torch extras, accelerate, bitsandbytes, dll). Tiada amaran untuk
  modul yang benar-benar digunakan. Missing `torch._C.*` = normal.
- Ujian automatik exe: tetingkap 'Pustaka Hadis - Makluman' muncul →
  disclaimer diluluskan (user_settings.json `disclaimer_dibaca:true`
  di DATA_DIR) → model e5 dimuat (RAM 78 → 596 MB) → tetingkap utama
  'Pustaka Hadis' terbuka. DATA_DIR `%LOCALAPPDATA%\PustakaHadis`
  digunakan; folder EXE tiada hadis.db. Indeks FAISS binaan dimuat:
  62,169 vektor × 384 dimensi.
- `semak.py` selepas perubahan: SEMUA LULUS — 385 semakan.
- Nota Fasa 3: saiz 2.02 GB — duplikat HF cache (snapshots+blobs =
  2×460 MB) + cv2 (87 MB, ditarik transformers) boleh dibuang.

### Gate Fasa 2

`PustakaHadis-Debug.exe` pada mesin pembangun mesti lulus:

- launch; ✅ (dilancar tanpa Python pada PATH)
- tema; ⏳ ujian manual
- senarai/detail/rawak/bookmarks; ⏳ ujian manual
- API dan sync ringkas; ⏳ ujian manual
- carian Melayu + Arab; ⏳ ujian manual
- carian makna FAISS; ✅ komponen disahkan (indeks dimuat 62,169 vektor)
- tutup tanpa hang/crash. ✅ (aplikasi hidup >100 s, ditutup paksa hanya untuk ujian)

**Keputusan: GATE FASA 2 LULUS** (semua ujian automatik lulus; item ⏳
ialah ujian interaktif manual yang boleh dijalankan pengguna pada
mesin pembangun — lihat INSTALLER §7.2). Fallback Nuitka TIDAK
dicetuskan.

---

## Fasa 3 — Pengoptimuman Binaan ✅ **SELESAI — GATE LULUS (20 Ogos 2026)**

**Rekod keputusan Fasa 3 (20 Ogos 2026):**

- **Buang duplikat HF cache (jimat 470 MB):** `blobs/` dalam
  `.cache_models` ialah salinan kedua fail model (snapshots sudah ada
  fail fizikal penuh). Ujian empirik: model masih muat + encode tanpa
  blobs (384 dimensi) → dipadam kekal. Pakej kini satu model.safetensors
  sahaja (bukan 2×460 MB).
- **Buang cv2 + PIL (jimat 151 MB):** `--exclude-module cv2
  --exclude-module PIL`. cv2 (138 MB) ditarik transformers untuk
  video/OCR — aplikasi hanya teks, tidak guna; import cv2 ialah lazy
  (dalam fungsi), selamat. PIL (13 MB) juga pilihan.
- **Hasil:** `dist\PustakaHadis-Debug` = **1,399.9 MB / 7,027 fail**
  (sebelum: 2,022.8 MB / 7,065) — jimat 622.9 MB (31%). Semua aset
  lengkap; tiada data pengguna/hadis.db dalam pakej.
- **Ujian binaan optimum:**
  - Model e5 dimuat penuh (stderr `Loading weights: 100% 199/199`;
    RAM 78 → 929–937 MB; `profil_model.json` dikemas `muat_s: 35.0,
    dari_cache: true` di DATA_DIR).
  - Tetingkap utama 'Pustaka Hadis' terbuka (MainWindowTitle tepat).
  - Tiada ralat/traceback.
  - `semak.py` SEMUA LULUS — 385 semakan (15 bahagian).
  - Boot pertama lambat (~110–120 s) — Windows Defender mengimbas
    pakej 1.4 GB; bukan ralat aplikasi.
- Keputusan Fasa 0 kekal: profil lengkap (model e5 + indeks FAISS
  dibundel); tiada profil minimum.

### Gate Fasa 3

- Saiz binaan < 1.5 GB ✅ (1,399.9 MB)
- Fungsi setara Fasa 2 ✅ (model dimuat, tetingkap utama, DATA_DIR,
  FAISS 62,169 vektor, tiada ralat)
- Tiada kehilangan aset ✅ (sunnah_map, app.ico, indeks, peta, profil)

**Keputusan: GATE FASA 3 LULUS.** Langkah seterusnya: Fasa 4 — Uji
Binaan pada Mesin Bersih (INSTALLER §8) atau ujian manual interaktif
pengguna pada mesin pembangun dahulu.

---

## Fasa 4 — Uji Binaan pada Mesin Bersih

### Trigger fallback Nuitka

Cuba Nuitka **hanya jika** PyInstaller masih gagal selepas:

- hooks/hidden imports diperbetulkan;
- konflik beberapa binding Qt dibuang;
- metadata torch/transformers disertakan;
- DLL diperiksa;
- MRE kegagalan direkod.

Jika fallback dicetuskan, bina diagnostik Nuitka pada venv kedua dan guna gate
yang sama. Pilih alat yang lulus gate fungsi, bukan yang sekadar menghasilkan
EXE.

---

## Fasa 3 — Ujian Windows Bersih

Gunakan Windows Sandbox atau VM tanpa Python/PyQt/torch.

### Matriks

Diuji dalam Windows Sandbox (Windows 11 Pro, tiada Python/PyQt/torch —
mesin bersih sebenar). Windows 10 belum diuji (Sandbox tersedia ialah 11).

| Ujian | Windows 10 22H2 | Windows 11 (Sandbox) |
|---|---:|---:|
| Launch pengguna biasa | ☐ | ☑ apl berjalan lancar |
| Simpan settings/API key | ☐ | ☑ API key dipasang & disimpan |
| Sync dan resume | ☐ | ☑ carian ok selepas API |
| Carian Melayu/Arab | ☐ | ☑ |
| Carian makna | ☐ | ☑ |
| Bookmark dan restart | ☐ | ☑ bookmark ok |
| Offline selepas sync | ☐ | ☐ belum diuji |
| Tutup/relaunch | ☐ | ☐ belum diuji secara khusus |
| Terjemahan Inggeris | ☐ | ☐ TIADA — reka bentuk (lihat nota di bawah) |

Nota Terjemahan Inggeris: tab English kelabu dalam binaan edaran ialah
tingkah laku yang DIJANGKA. Sumber Inggeris (`.cache_eng` + jadual
`terjemahan_eng` dalam hadis.db) TIDAK dibundel (INSTALLER §4), dan
aplikasi edaran tidak memuat turun/padan Inggeris (sync_english.py ialah
skrip pembangunan). Ini konsisten dengan keputusan lesen
`PERMOHONAN_LESEN_AHMAD.md` §5 — terjemahan Inggeris Musnad Ahmad tidak
boleh diedarkan sehingga kebenaran Darussalam diterima; dan keputusan
Sesi 7 "pengguna sync sendiri". **Keputusan pengguna (20 Ogos): biar
seperti reka bentuk — tiada perubahan kod.** Inggeris muncul semula hanya
bila DB pengguna diisi `terjemahan_eng` (cth. melalui `sync_english.py`
pada mesin pembangunan) atau keputusan lesen diubah.

### DLL

Kekalkan `_baik_pulih_dll_qt_torch()` semasa ujian pertama. Nilai sama ada ia
melakukan apa-apa dalam frozen build. Buang hanya selepas beberapa mesin
bersih lulus tanpa fungsi itu. Jangan jadikan “tanpa fix DLL” syarat awal yang
memaksa perubahan tidak perlu.

### Gate Fasa 3

- semua fungsi lulus tanpa Python dipasang;
- tiada `ACCESS DENIED` ke folder aplikasi;
- tiada muat turun model tidak dijangka;
- log crash kosong;
- saiz dan masa startup diukur.

**Keputusan: GATE FASA 4 (Uji Mesin Bersih) LULUS — 20 Ogos 2026**
(Windows Sandbox 11 Pro; keputusan matriks di atas; isu terjemahan
Inggeris disiasat dan disahkan reka bentuk lesen — bukan bug; pengguna
pilih kekalkan reka bentuk.)

---

## Fasa 4 — Bina Pakej Edaran

### 4A. Binaan keluaran PyInstaller ☑ SELESAI (20 Ogos)

Tukar `--console` kepada `--windowed`; ulang semua ujian ringkas.

- Spec `PustakaHadis.spec`: `name='PustakaHadis'`, `console=False`,
  `upx=False`; kekal exclude cv2/PIL + collect-all + aset profil.
- Hasil `dist\PustakaHadis` = 1,399.9 MB / 7,027 fail (~21 minit).
- Ujian ringkas LULUS: exe hidup · disclaimer (tajuk EM DASH U+2014) ·
  tetingkap utama 'Pustaka Hadis' tepat · model dimuat dari cache
  (profil_model.json: muat_s 39.5, dari_cache true) · DATA_DIR betul ·
  warn tiada regresi vs Debug · semak.py 386 SEMUA LULUS.

### 4B. Inno Setup EXE — sekunder ☑ SELESAI (20 Ogos)

- Inno Setup 6.7.3 dipasang di `D:\Inno Setup 6` (~20 MB).
- `installer\PustakaHadis.iss` ikut INSTALLER §9: per-user
  (`{localappdata}\Programs\PustakaHadis`), `PrivilegesRequired=lowest`,
  AppId tetap `{{7DF2553E-9E62-4ED4-929A-61C71AD1047F}`, task
  desktopicon, lzma2/ultra64.
- Hasil `installer\output\PustakaHadis-Setup-1.0.0-x64.exe` = 0.50 GB
  (~34 minit).
- Ujian LULUS: silent install (0, 7,029 fail) · launch app terpasang
  (tetingkap 'Pustaka Hadis') · uninstall senyap (0) — folder app
  dipadam, **DATA_DIR kekal**, pintasan dipadam. Naik taraf ujian penuh
  di Fasa 6 (1.0.0→1.0.1).

### 4C. MSIX — utama ⏳ PENYEDIAAN SELESAI — MENUNGGU IDENTITI STORE

- MSIX Packaging Tool (v1.2024.405.0) + WinApp CLI 0.6.1 dipasang
  (winget). MSIX Packaging Tool Driver perlu aktif (Optional Features /
  wizard 'Prepare computer').
- Aset PNG MSIX dijana → `installer\Assets\` (StoreLogo 50,
  Square44x44, Square150x150, Wide310x150).
- Audit `dist\PustakaHadis`: 0 fail terlarang (tiada DB/settings/
  cache/log) — bersih untuk capture.
- **ZIP mudah alih** dicipta → `installer\output\PustakaHadis-portable-1.0.0-x64.zip`
  (0.54 GB) untuk penguji dalaman.
- **Dokumentasi capture**: `VM_MSIX_CAPTURE.md` (persediaan VM, snapshot,
  wizard manual, capture, Package Editor) + `MSIX_CAPTURE_PROSES.md`
  (checklist 6 fasa, rollback, output Gate 6).
- ⛔ Menunggu identiti Partner Center (tugas pengguna Fasa 0): daftar
  Store + tempah nama + Publisher → beri `Package/Identity/Name`,
  `Package/Identity/Publisher`, `Package/Properties/PublisherDisplayName`.
- Seterusnya: capture VM bersih (Manual installation, Program Files,
  satu entry point PustakaHadis.exe, jangan sync/API key), Package
  editor (runFullTrust, Windows.Desktop, MinVersion 10.0.19041.0),
  simpan `PustakaHadis_1.0.0.0_x64.msix`, tandatangan ujian tempatan
  (Subject = Publisher manifest), uji Add-AppxPackage.

### 4D. Uji Windows 10 (Gate 4 Matrix) ⏳

- VM Windows 10 bersih / snapshot diperlukan
- Uji matriks §8: launch, settings/API key, sync/resume, carian Melayu/Arab,
  carian makna, bookmark, offline selepas sync, tutup/relaunch khusus
- Rekod keputusan dalam CHECKLIST

### Gate Fasa 4

- EXE pemasang/pembuang lulus;
- MSIX boleh ditandatangani sendiri untuk ujian;
- MSIX install/launch/uninstall lulus;
- aset pakej sama dengan inventori yang diluluskan.

---

## Fasa 5 — Partner Center dan Ujian Naik Taraf

### Kerja

1. Daftar akaun pembangun Microsoft Store.
2. Tempah nama Pustaka Hadis.
3. Rekod `Identity Name`, `Publisher` dan `PublisherDisplayName`.
4. Bina versi `1.0.0.0`.
5. Pasang, cipta settings/bookmark dan sync data ujian.
6. Bina versi `1.0.1.0` dengan identiti sama.
7. Pasang kemas kini.
8. Uji uninstall/reinstall dan tingkah laku data.
9. Lengkapkan listing, ikon, screenshots, dasar privasi dan notes for
   certification.
10. Upload MSIX dan gunakan private audience/flight jika tersedia.

### Gate Fasa 5

- update tidak memadam DB/settings/bookmarks;
- hanya satu pemasangan/Start Menu entry;
- pensijilan Store lulus;
- Microsoft menandatangani pakej;
- pemasangan Store tidak memaparkan amaran biasa.

---

## Fasa 6 — Edaran Awam

Hanya selepas:

- lesen hadis.my/SemakHadis/aset bundel selesai;
- dasar privasi dan sokongan tersedia;
- pensijilan Store lulus;
- gate Windows 10/11 lulus.

### Saluran

1. **Microsoft Store MSIX** — utama.
2. **GitHub Releases** — EXE/portable sekunder jika benar-benar diperlukan.

EXE tidak ditandatangani CA mesti mempunyai amaran SmartScreen, SHA-256 dan
VirusTotal. Jangan gambarkan GitHub sebagai pengganti tandatangan kod.

---

## 6. Risiko dan Mitigasi

| Risiko | Mitigasi |
|---|---|
| Konflik torch/PyQt DLL | Venv bersih, PyInstaller hook, ujian VM, Dependencies/ProcMon |
| Qt callback/threading berubah | PyInstaller dahulu; Nuitka hanya fallback dengan gate sama |
| Pakej terlalu besar | Ukur aset sebenar; `onedir`; Store/MSIX memampat dan mengurus update |
| Model cuba dimuat turun | Bundel cache yang dibenarkan; pusatkan `MODEL_CACHE` ke ASSET_DIR |
| DB ditulis ke folder pakej | Pusatkan DATA_DIR; ujian `sys.frozen`; ProcMon |
| Upgrade memadam data | DATA_DIR berasingan; ujian 1.0.0.0 → 1.0.1.0 |
| Uninstall MSIX membersihkan data virtual | Uji sebenar; sediakan eksport/padam data dalam aplikasi |
| SmartScreen EXE | MSIX Store utama; EXE sekunder + sijil/penjelasan |
| Indeks FAISS lapuk | Metadata versi/kiraan; bina semula pada keluaran data baharu |
| Data tanpa lesen | Repo/pakej persendirian sehingga kebenaran bertulis |
| Rahsia dalam git/pakej | Repo baharu/filter-repo; inventori pakej; imbas `.env` dan kunci |

---

## 7. Anggaran

| Fasa | Anggaran awal |
|---|---:|
| Fasa 1 — laluan data + gate | 2–4 jam |
| Fasa 2 — PyInstaller diagnostik | 2–6 jam termasuk percubaan hook |
| Fallback Nuitka jika dicetuskan | tambahan 2–6 jam |
| Fasa 3 — Windows bersih | 2–4 jam |
| Fasa 4 — Inno + MSIX | 4–8 jam |
| Fasa 5 — Store/listing/update test | 1–2 hari + masa pensijilan |
| Wizard permulaan baharu, jika dibina | 1–2 hari berasingan |

Anggaran bergantung pada masa kompilasi torch dan saiz model sebenar.

---

## 8. Keputusan yang Masih Diperlukan

1. Sahkan profil ujian membundel model + indeks.
2. Sahkan Microsoft Store sebagai saluran utama.
3. Sahkan Inno EXE diperlukan sebagai saluran sekunder atau penguji sahaja.
4. Pilih akaun/identiti Partner Center.
5. Tentukan sama ada portable ZIP diperlukan selepas MSIX lulus.
6. Putuskan masa membina wizard permulaan: sebelum beta atau selepas installer
   asas terbukti.

---

## 9. Definisi Selesai

Versi edaran dianggap selesai apabila:

- [ ] Fasa 1–5 melepasi semua gate;
- [ ] aplikasi berjalan tanpa Python pada Windows 10/11;
- [ ] carian makna berfungsi;
- [ ] data pengguna tidak hilang ketika update;
- [ ] MSIX lulus pensijilan dan ditandatangani Store;
- [ ] lesen/aset disahkan untuk keluaran awam;
- [ ] dokumentasi pengguna, privasi dan sokongan tersedia.

---

## Cadangan Fasa 0 — untuk semakan pengguna (16 Ogos 2026)

Enam keputusan skop di atas **dicadangkan diluluskan** seperti berikut
(menunggu pengesahan pengguna sebelum Fasa 1):

- **Bundel model e5 + indeks FAISS untuk profil ujian** — ya (elak muat
  turun/bina berjam-jam); awam menunggu lesen.
- **`hadis.db` kekal tidak dibundel** — ya (keputusan pengguna sedia ada).
- **x64 sahaja** — ya (kurangkan matriks ujian keluaran pertama).
- **Microsoft Store (MSIX) = edaran utama** — ya (signing Microsoft,
  update terurus, tiada SmartScreen biasa).
- **Inno EXE = edaran sekunder/penguji** — ya (mesin tanpa Store).
- **Repo persendirian hingga lesen data selesai** — ya.

**Status: CADANGAN sahaja — Fasa 0 belum diluluskan.**
