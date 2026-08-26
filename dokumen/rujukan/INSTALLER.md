# Panduan Langkah demi Langkah — Installer Windows dan MSIX

**Tarikh kemas kini:** 15 Ogos 2026  
**Aplikasi:** Pustaka Hadis  
**Sasaran:** Windows 10 22H2 / Windows 11, x64  
**Status:** Panduan teknikal; belum dibina pada mesin Windows bersih  
**Dokumen kawalan/gate:** `PLAN_BINA_EDARAN.md`  
**Rekod keputusan alat:** `BANDING_INSTALLER.md`

Jika terdapat percanggahan, ikut urutan dan keputusan alat dalam
`PLAN_BINA_EDARAN.md`; gunakan dokumen ini untuk langkah pelaksanaan.

---

## 0. Keputusan Utama

| Perkara | Keputusan |
|---|---|
| Format binaan Python | **PyInstaller 6.22 `onedir`** |
| Sebab | Sokongan rasmi Python 3.14 + PyQt5; lebih stabil daripada Nuitka untuk keadaan projek semasa |
| Format edaran utama | **MSIX melalui Microsoft Store** |
| Tandatangan Store | Microsoft menandatangani semula MSIX selepas pensijilan |
| Edaran terus dari web | Pilihan kedua sahaja; EXE/MSI perlu sijil CA untuk mengelakkan amaran |
| `hadis.db` | **Tidak dibundel** — keputusan pengguna |
| Model + indeks FAISS | Boleh dibundel untuk ujian persendirian; edaran awam tunggu izin data |
| Seni bina | x64 sahaja untuk keluaran pertama |
| Mod PyInstaller | `onedir`, bukan `onefile` — permulaan lebih cepat dan tiada ekstrak hampir 1 GB setiap pelancaran |
| Data boleh tulis | `%LOCALAPPDATA%\PustakaHadis` |
| Aset baca sahaja | Folder pakej PyInstaller/MSIX |

### Mengapa bukan Nuitka sekarang?

Nuitka 4.1 mempunyai sokongan Python 3.14 yang masih ditanda eksperimen dan
halaman rasminya mengakui PyQt5 mempunyai isu callback/threading. Pustaka Hadis
menggunakan banyak `QThread`, torch dan sentence-transformers. PyInstaller
6.22 pula menyokong Python 3.8–3.15 dan menyenaraikan PyQt5 sebagai pakej yang
dibundel secara rasmi.

Nuitka boleh dinilai semula selepas Python 3.14/PyQt5 benar-benar stabil, tetapi
jangan jadikan ia penghalang untuk keluaran pertama.

---

## 1. Dua Laluan Edaran

### Laluan A — Disyorkan: Microsoft Store + MSIX

Kelebihan:

- hosting binari oleh Microsoft;
- tandatangan kod percuma oleh Store;
- tiada amaran SmartScreen untuk pemasangan Store;
- kemas kini automatik;
- nyahpasang bersih;
- package flighting dan analitik Partner Center.

### Laluan B — Tambahan: Inno Setup EXE

Sesuai untuk:

- penguji dalaman;
- pengguna tanpa Microsoft Store;
- bahan input kepada MSIX Packaging Tool.

Kekurangan:

- Microsoft Store **tidak** menandatangani semula EXE/MSI;
- EXE yang diedar terus memerlukan sijil Authenticode CA atau mungkin mendapat
  amaran SmartScreen;
- pembangun perlu mengurus kemas kini sendiri.

**Kesimpulan:** bina kedua-duanya jika perlu, tetapi jadikan **MSIX Store**
sebagai saluran awam utama.

---

## 1a. Workflow Lengkap — dari Fasa 0 hingga Edaran Awam

Peta aliran penuh. Setiap fasa mempunyai **gate**; fasa seterusnya hanya
bermula selepas gate sebelumnya lulus. Dokumen kawalan fasa/gate:
`PLAN_BINA_EDARAN.md`; panduan pelaksanaan: dokumen ini.

```text
FASA 0 — Kelulusan pengguna (6 keputusan skop)
   │   jawab: bundel model? Store utama? Inno sekunder?
   │          akaun Partner Center? portable ZIP? wizard permulaan?
   ▼
   GATE 0: pengguna meluluskan semua keputusan
   │
FASA 1 — Pisahkan laluan data (§3)
   │   config.py: ASSET_DIR + DATA_DIR; audit 11 fail; ujian sys.frozen
   ▼
   GATE 1: semak.py + semak_versi.py + uji_lompat.py + main.py — semua lulus
   │
FASA 2 — Bina PyInstaller diagnostik (§5–§7)
   │   venv 3.14 bersih; main.py freeze_support(); onedir --console;
   │   --collect-all sentence_transformers/transformers/tokenizers/faiss
   ▼
   GATE 2: PustakaHadis-Debug.exe lulus semua fungsi pada mesin pembangun
   │        (gagal selepas pembetulan munasabah → FALLBACK Nuitka, §4)
   │
FASA 3 — Ujian Windows bersih (§8)
   │   Windows Sandbox/VM tanpa Python; matriks 8 ujian × Win10/Win11
   ▼
   GATE 3: semua fungsi lulus; tiada ACCESS DENIED; saiz/startup diukur
   │
FASA 4 — Bina pakej edaran (§7.3, §9, §11)
   │   4A: binaan --windowed keluaran
   │   4B: Inno Setup EXE (sekunder, per-user)
   │   4C: MSIX (utama) — Packaging Tool, VM bersih, identiti Store
   ▼
   GATE 4: EXE + MSIX install/launch/uninstall lulus; aset pakej = inventori
   │
FASA 5 — Partner Center + ujian naik taraf (§10, §13–§16)
   │   daftar akaun; tempah nama; rekod identiti; 1.0.0.0 → 1.0.1.0
   ▼
   GATE 5: update tidak memadam DB/settings/bookmark; pensijilan lulus;
   │        Microsoft menandatangani pakej; tiada amaran biasa
   │
FASA 6 — Edaran awam (§15, §18)
   │   hanya selepas: lesen data selesai + dasar privasi + pensijilan
   ▼
   GATE 6: semua gate hijau; dokumentasi pengguna/privasi/sokongan sedia
```

### Jadual langkah — kerja, output, gate, rujukan

| Langkah | Kerja utama | Output | Gate | Rujukan § |
|---|---|---|---|---|
| Fasa 0 | Jawab 6 keputusan skop | Keputusan direkod | Pengguna luluskan | PLAN §8, PERBANDINGAN §4 |
| Fasa 1 | `ASSET_DIR`/`DATA_DIR` dalam config.py; audit 11 fail | Semua data boleh tulis ke `%LOCALAPPDATA%` | Gate 1 lulus | §3 |
| Fasa 2 | venv bersih; `freeze_support()`; bina debug | `dist\PustakaHadis-Debug\*.exe` | Gate 2 lulus | §5–§7 |
| Fallback | Jika PyInstaller gagal gate fungsi | Bina Nuitka di venv kedua | Gate 2 sama | §4, BANDING §4 |
| Fasa 3 | Uji pada Windows 10/11 bersih | Matriks ujian penuh | Gate 3 lulus | §8 |
| Fasa 4A | Bina `--windowed` | `dist\PustakaHadis\PustakaHadis.exe` | Gate 4 lulus | §7.3 |
| Fasa 4B | Inno Setup EXE | `PustakaHadis-Setup-<versi>-x64.exe` | Gate 4 lulus | §9 |
| Fasa 4C | MSIX manual dalam VM bersih | `PustakaHadis_<versi>_x64.msix` | Gate 4 lulus | §11–§12 |
| Fasa 5 | Daftar Store; tempah nama; ujian naik taraf | Identiti + pakej 1.0.0.0/1.0.1.0 | Gate 5 lulus | §10, §13–§16 |
| Fasa 6 | Upload; listing; pensijilan | MSIX diterbitkan Store | Gate 6 lulus | §15, §18 |

### Keputusan Fasa 0 (perlu dijawab sebelum Fasa 1)

| # | Soalan | Cadangan dokumen |
|---|---|---|
| 1 | Bundel model e5 + indeks FAISS untuk profil ujian? | Ya (elak bina berjam-jam); awam tunggu lesen |
| 2 | Microsoft Store = saluran utama? | Ya (signing Microsoft, update terurus) |
| 3 | Inno EXE = saluran sekunder/penguji? | Ya (mesin tanpa Store) |
| 4 | Akaun Partner Center + nama Publisher? | Perlu dipilih pengguna |
| 5 | Portable ZIP selepas MSIX? | Belum diputuskan |
| 6 | Wizard permulaan: sebelum beta atau selepas? | Belum diputuskan |

### Peraturan aliran

1. **Tiada lompat fasa** — setiap gate mesti hijau sebelum fasa seterusnya.
2. **Satu alat utama pada satu masa** — PyInstaller dahulu; Nuitka hanya
   fallback ber-gate, jangan bina dua pakej penuh serentak tanpa sebab.
3. **Data pengguna tidak pernah masuk pakej** — hadis.db, `.env`, settings,
   bookmarks dan cache kekal di luar pakej (§4).
4. **Repo persendirian hingga lesen data selesai** — binaan ujian boleh
   dibuat sekarang, tetapi JANGAN terbitkan awam sebelum kebenaran bertulis.
5. **Ukur, bukan anggar** — saiz, masa startup dan tingkah laku DLL mesti
   diukur pada binaan sebenar; jangan gunakan angka lama (787 MB / 520 MB)
   sebagai bukti tanpa artifak binaan.
6. **Data kekal selepas naik taraf** — ujian 1.0.0.0 → 1.0.1.0 wajib (§16).

---

## 2. Syarat Sebelum Binaan

Jangan terus menjalankan PyInstaller. Selesaikan dahulu:

- [ ] Tutup semua aplikasi/proses Pustaka Hadis.
- [ ] `python semak.py` lulus.
- [ ] `python semak_versi.py` lulus.
- [ ] `python uji_lompat.py` lulus.
- [ ] Carian Arab skema 8 lulus.
- [ ] Tiada kunci API, `.env`, DB pengguna atau fail sandaran dalam pakej.
- [ ] Laluan data pengguna telah dipisahkan daripada folder aplikasi (§3).
- [ ] Lesen data yang akan dibundel telah diluluskan.
- [ ] Nama produk dan identiti Store telah ditempah dalam Partner Center.

### Binaan persendirian vs keluaran awam

Binaan teknikal dan ujian persendirian boleh dimulakan sekarang. **Jangan
terbitkan kepada umum** sehingga kebenaran hadis.my, SemakHadis dan mana-mana
teks terjemahan yang dibundel sudah jelas.

---

## 3. WAJIB — Pisahkan Data Pengguna daripada Aset Aplikasi

MSIX memasang aplikasi dalam `C:\Program Files\WindowsApps`, yang baca sahaja.
Kod semasa masih mempunyai beberapa laluan berdasarkan `__file__`, termasuk
`hadis.db`, `user_settings.json`, bookmarks dan cache. Ia mesti diperbetulkan
sebelum MSIX.

### 3.1 Corak pusat dalam `config.py`

Gunakan satu sumber kebenaran:

```python
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Folder aset yang dibundel. Dalam PyInstaller 6 onedir, __file__ bagi modul
# akar menunjuk ke folder data dalaman yang boleh dibaca.
ASSET_DIR = Path(__file__).resolve().parent


def _data_dir() -> Path:
    if getattr(sys, "frozen", False):
        asas = os.environ.get("LOCALAPPDATA")
        if not asas:
            asas = str(Path.home() / "AppData" / "Local")
        d = Path(asas) / "PustakaHadis"
    else:
        # Mod pembangunan kekal seperti sekarang.
        d = ASSET_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


DATA_DIR = _data_dir()

# Boleh tulis — tidak boleh berada dalam pakej MSIX.
DB_PATH       = str(DATA_DIR / "hadis.db")
SETTINGS_PATH = str(DATA_DIR / "user_settings.json")
BOOKMARKS_PATH = str(DATA_DIR / "bookmarks.json")
ENV_PATH      = str(DATA_DIR / ".env")
CACHE_SEMA    = str(DATA_DIR / ".cache_sema")
CACHE_HE      = str(DATA_DIR / ".cache_he")
CACHE_ENG     = str(DATA_DIR / ".cache_eng")
CACHE_SYARAH  = str(DATA_DIR / ".cache_syarah")

# Baca sahaja — dibundel bersama aplikasi.
ICON_PATH     = str(ASSET_DIR / "app.ico")
FAISS_INDEX   = str(ASSET_DIR / "hadis_faiss.index")
FAISS_MAP     = str(ASSET_DIR / "hadis_id_map.pkl")
MODEL_CACHE   = str(ASSET_DIR / ".cache_models")
MODEL_PROFILE = str(ASSET_DIR / "profil_model.json")
SUNNAH_MAP    = str(ASSET_DIR / "sunnah_map")
```

### 3.2 Fail yang perlu menggunakan pemalar pusat

Audit dan ubah sekurang-kurangnya:

| Fail | Laluan yang perlu dipusatkan |
|---|---|
| `db.py` | `DB_PATH` |
| `api/hadis_api.py` | `DB_PATH` |
| `ui/helpers.py` | settings + bookmarks + `sunnah_map` |
| `ui/splash.py` | settings |
| `core/sema_source.py` | `.cache_sema` |
| `core/hadeethenc_api.py` | `.cache_he` |
| `core/syarah_source.py` | `.cache_syarah` |
| `core/semantic_search.py` | model, indeks, peta, profil |
| `sync.py` | `DB_PATH` |
| `semak_db.py` | `DB_PATH` |

Cari semua laluan yang masih bebas:

```powershell
Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern `
  'hadis\.db|user_settings\.json|bookmarks\.json|\.cache_|hadis_faiss|hadis_id_map|profil_model'
```

Semua fail boleh tulis mesti datang daripada `config.py`. Aset baca sahaja
boleh datang daripada `ASSET_DIR`.

### 3.3 Perhatian nyahpasang MSIX

MSIX tidak menjalankan wizard nyahpasang tersuai. Jangan bergantung pada dialog
“simpan atau buang data” seperti Inno Setup. Sediakan dalam aplikasi:

- butang **Eksport tanda buku/tetapan**;
- butang **Padam semua data tempatan**;
- paparan lokasi data;
- amaran sebelum padam.

Uji sama ada `%LOCALAPPDATA%\PustakaHadis` kekal selepas uninstall pada pakej
sebenar. Jangan menjanjikan pengekalan sehingga ujian itu dibuat kerana MSIX
boleh memvirtualkan lokasi AppData.

---

## 4. Tentukan Kandungan Pakej

### Jangan bundel

```text
hadis.db
hadis.db-wal
hadis.db-shm
.env
user_settings.json
bookmarks.json
.cache_sema
.cache_he
.cache_eng
.cache_syarah
*.bak
log audit
__pycache__
```

### Bundel bagi profil lengkap

```text
app.ico
hadis_faiss.index
hadis_id_map.pkl
profil_model.json
.cache_models/
sunnah_map/
```

**Syarat:** indeks dan model hanya boleh diedarkan selepas lesen data/model
disahkan. Jika belum, buat profil binaan minimum tanpa aset tersebut untuk
ujian UI/installer.

### Semak saiz

```powershell
Get-ChildItem hadis_faiss.index, hadis_id_map.pkl, profil_model.json | `
  Select-Object Name,Length
Get-ChildItem .cache_models -Recurse | Measure-Object Length -Sum
```

Rekod saiz sebenar dalam nota keluaran; jangan bergantung pada anggaran lama.

---

## 5. Sediakan Mesin Binaan Windows

Gunakan mesin/VM Windows x64 bersih. PyInstaller bukan cross-compiler.

### 5.1 Pasang alat

- CPython 3.14 x64 daripada python.org;
- Git;
- Windows SDK terkini;
- Inno Setup 6 (untuk EXE pilihan);
- MSIX Packaging Tool;
- Windows Sandbox atau VM ujian.

Pasang MSIX Packaging Tool:

```powershell
winget install "MSIX Packaging Tool"
```

### 5.2 Cipta persekitaran maya bersih

Dari root projek:

```powershell
py -3.14 -m venv .venv-build
.\.venv-build\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
pip install pyinstaller==6.22.0 pyinstaller-hooks-contrib
```

Jika model XLM-R memerlukannya dan belum dipasang:

```powershell
pip install sentencepiece
```

Sahkan hanya satu binding Qt dipasang:

```powershell
pip list | Select-String 'PyQt|PySide'
```

Keputusan sepatutnya hanya PyQt5. PyInstaller tidak membenarkan beberapa
binding Qt dibundel serentak.

Simpan rekod binaan:

```powershell
python --version
python -m PyInstaller --version
pip freeze > installer\requirements-build-lock.txt
```

---

## 6. Tambah Sokongan Frozen pada Entry Point

Torch/sentence-transformers mungkin menggunakan multiprocessing. Tambah pada
`main.py`:

```python
import multiprocessing


def main():
    multiprocessing.freeze_support()
    # kod QApplication sedia ada...
```

Jangan gunakan `launcher.py` sebagai entry point. Ia melancarkan
`[sys.executable, "main.py"]`, yang tidak sesuai selepas dibekukan.
Gunakan `main.py` terus.

Fungsi `_baik_pulih_dll_qt_torch()` mungkin tidak menemui `site-packages`
dalam binaan frozen. Jangan buang dahulu; uji carian makna pada binaan. Jika
konflik DLL masih berlaku, selesaikan di peringkat fail PyInstaller, bukan
dengan mengubah folder pakej ketika aplikasi berjalan.

---

## 7. Bina EXE PyInstaller `onedir`

### 7.1 Binaan diagnostik pertama

Binaan pertama patut mempunyai konsol supaya traceback boleh dilihat:

```powershell
Remove-Item -Recurse -Force build,dist -ErrorAction SilentlyContinue

python -m PyInstaller `
  --noconfirm `
  --clean `
  --onedir `
  --console `
  --name PustakaHadis-Debug `
  --icon app.ico `
  --add-data "app.ico;." `
  --add-data "sunnah_map;sunnah_map" `
  --collect-all sentence_transformers `
  --collect-all transformers `
  --collect-all tokenizers `
  --collect-all faiss `
  --copy-metadata sentence-transformers `
  --copy-metadata transformers `
  --copy-metadata torch `
  main.py
```

Jika profil lengkap telah dibenarkan, tambah:

```powershell
  --add-data ".cache_models;.cache_models" `
  --add-data "hadis_faiss.index;." `
  --add-data "hadis_id_map.pkl;." `
  --add-data "profil_model.json;." `
```

Jangan guna UPX pada binaan pertama; ia boleh merosakkan DLL Qt/torch.

### 7.2 Uji binaan diagnostik

```powershell
.\dist\PustakaHadis-Debug\PustakaHadis-Debug.exe
```

Uji:

- aplikasi dibuka tanpa Python pada `PATH`;
- tema gelap/cerah;
- API key disimpan dalam `%LOCALAPPDATA%\PustakaHadis`;
- sync mencipta DB di lokasi data, bukan folder EXE;
- carian Melayu dan Arab;
- carian makna FAISS;
- rawak, bookmarks, huraian dan salin teks;
- tutup/buka semula;
- mod luar talian;
- jalankan sebagai pengguna biasa, bukan Administrator.

Semak amaran:

```powershell
Get-Content .\build\PustakaHadis-Debug\warn-PustakaHadis-Debug.txt
```

Jangan abaikan amaran modul yang benar-benar digunakan.

### 7.3 Binaan keluaran tanpa konsol

Selepas diagnostik lulus, tukar:

```text
--console  ->  --windowed
--name PustakaHadis-Debug  ->  --name PustakaHadis
```

Jalankan arahan sama. Hasil:

```text
dist\PustakaHadis\PustakaHadis.exe
```

### 7.4 Mengapa bukan `--onefile`?

Pakej torch/Qt/model besar akan diekstrak ke folder sementara pada setiap
pelancaran, memperlahankan startup dan menambah beban antivirus. MSIX sendiri
sudah menjadi unit pemasangan tunggal; `onedir` ialah payload yang sesuai.

---

## 8. Uji pada Windows Bersih

Gunakan Windows Sandbox atau VM tanpa Python/PyQt/torch.

Salin seluruh folder:

```text
dist\PustakaHadis\
```

Bukan EXE sahaja.

### Matriks minimum

| Ujian | Windows 10 x64 | Windows 11 x64 |
|---|---:|---:|
| Launch pengguna biasa | ☐ | ☐ |
| Simpan tetapan/API key | ☐ | ☐ |
| Sync sambung semula | ☐ | ☐ |
| Carian Arab tanpa tashkeel | ☐ | ☐ |
| Carian makna | ☐ | ☐ |
| Restart aplikasi | ☐ | ☐ |
| Offline selepas sync | ☐ | ☐ |
| Nyahpasang/naik taraf | ☐ | ☐ |

Gunakan ProcMon jika berlaku `ACCESS DENIED`. Sebarang tulisan ke folder EXE
ialah bug yang mesti dibaiki sebelum MSIX.

---

## 9. Pilihan EXE — Inno Setup

Buat `installer\PustakaHadis.iss`:

```ini
#define MyAppName "Pustaka Hadis"
#define MyAppVersion "1.0.0"
#define MyAppExeName "PustakaHadis.exe"

[Setup]
AppId={{7DF2553E-9E62-4ED4-929A-61C71AD1047F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={localappdata}\Programs\PustakaHadis
DefaultGroupName=Pustaka Hadis
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=output
OutputBaseFilename=PustakaHadis-Setup-{#MyAppVersion}-x64
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "..\dist\PustakaHadis\*"; DestDir: "{app}"; `
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Pustaka Hadis"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Pustaka Hadis"; Filename: "{app}\{#MyAppExeName}"; `
    Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Cipta pintasan Desktop"; `
    GroupDescription: "Pilihan tambahan:"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Buka Pustaka Hadis"; `
    Flags: nowait postinstall skipifsilent
```

**AppId mesti kekal sama** untuk semua versi. GUID contoh di atas boleh
digunakan jika belum pernah ada AppId rasmi, tetapi rekodkan dan jangan tukar.

Bina:

```powershell
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" `
  ".\installer\PustakaHadis.iss"
```

Uji silent install kerana MSIX Packaging Tool memerlukannya:

```powershell
.\installer\output\PustakaHadis-Setup-1.0.0-x64.exe `
  /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-
```

EXE ini sesuai untuk penguji. Jangan edarkan awam tanpa memahami isu
SmartScreen/tandatangan.

---

## 10. Daftar Microsoft Store dan Tempah Identiti

> **Panduan langkah demi langkah penuh:** `dokumen/rujukan/DAFTAR_MSIX_STORE.md`
> (tugas pengguna — akaun, pengesahan, tempah nama, salin 3 nilai
> identiti). Seksyen ini ringkasan sahaja.

1. Buka `https://storedeveloper.microsoft.com/`.
2. Daftar akaun pembangun (Individual memadai untuk apl percuma) dan
   lengkapkan pengesahan identiti (telefon + e-mel; kad mungkin untuk
   pengesahan $0–1 — yuran $19/$99 dibuang 2026).
3. Partner Center → **Apps and games** → **Create app** (MSIX or PWA app).
4. Tempah nama **`PustakaHadith`** (tanpa jarak; paparan boleh "Pustaka
   Hadis").
5. **Product management → Product identity** → salin TEPAT:

```text
Package/Identity/Name              = PustakaHadith
Package/Identity/Publisher         = CN=..., O=...   (dari Partner Center)
Package/Properties/PublisherDisplayName = PustakaHadith
```

6. Simpan ke `installer/msix_identity.txt` dan serahkan ke pembangun.
   Jangan reka sendiri `Publisher` — mesti sepadan tepat dengan Partner
   Center, jika tidak `Add-AppxPackage` gagal dan upload Store ditolak.

Versi MSIX mesti empat bahagian:

```text
1.0.0.0
1.0.1.0
1.1.0.0
```

Setiap kemas kini mesti mempunyai versi lebih tinggi dan identiti pakej sama.

---

## 11. Hasilkan MSIX dengan MSIX Packaging Tool

### 11.1 Persekitaran penukaran

Guna VM/snapshot Windows bersih. Jangan tangkap pakej pada mesin harian kerana
Windows Update, antivirus, cache dan program lain boleh termasuk dalam hasil.

1. Ambil snapshot VM.
2. Pasang MSIX Packaging Tool.
3. Jangan pasang Pustaka Hadis terlebih dahulu.
4. Pastikan tiada `hadis.db`, API key atau data pengguna dalam VM.

### 11.2 Jalankan wizard — kaedah manual disyorkan

Oleh sebab kita mempunyai payload `onedir`, elakkan menangkap uninstaller dan
registry Inno ke dalam MSIX. MSIX sendiri mengurus pemasangan/nyahpasang.

1. Buka **MSIX Packaging Tool**.
2. Pilih **Application package**.
3. Pilih **Create package on this computer** atau VM jauh.
4. Benarkan Packaging Tool Driver jika diminta.
5. Pada pemilihan installer, biarkan medan installer **kosong** untuk
   **Manual installation**.
6. Isi maklumat pakej:
   - Package name: nilai `Package/Identity/Name` Partner Center;
   - Publisher: nilai `Package/Identity/Publisher` Partner Center;
   - Display name: `Pustaka Hadis`;
   - Publisher display name: nilai Partner Center;
   - Version: `1.0.0.0`;
   - Architecture: x64;
   - Install location: `C:\Program Files\PustakaHadis`.
7. Mulakan proses capture.
8. Dalam PowerShell pentadbir, salin payload ketika capture aktif:

```powershell
New-Item -ItemType Directory -Force "C:\Program Files\PustakaHadis"
Copy-Item ".\dist\PustakaHadis\*" `
  "C:\Program Files\PustakaHadis" -Recurse -Force
```

9. Jangan salin `hadis.db`, `.env`, settings, bookmarks, log atau cache
   pengguna.
10. Jangan buka wizard API, jangan sync dan jangan masukkan kunci ketika
    capture. Data itu tidak boleh masuk ke pakej.
11. Teruskan wizard. Pada pengesanan entry point, pilih:

```text
C:\Program Files\PustakaHadis\PustakaHadis.exe
```

12. Semak Package editor:
    - satu aplikasi sahaja;
    - tiada uninstaller/helper sebagai entry point;
    - ikon betul;
    - tiada DB, `.env`, settings, cache atau log;
    - capability `runFullTrust` untuk desktop Win32;
    - TargetDeviceFamily `Windows.Desktop`;
    - MinVersion disyorkan `10.0.19041.0`.
13. Simpan pakej MSIX.

### Alternatif: tukar Inno Setup EXE kepada MSIX

Jika mahu proses berasaskan installer, pilih EXE §9 dan gunakan argumen:

```text
/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-
```

Namun installer §9 memasang per-pengguna ke LocalAppData. Untuk capture MSIX
yang bersih, gunakan skrip Inno **berasingan** yang memasang ke Program Files,
atau pilih kaedah manual di atas. Jangan campurkan profil installer web dengan
profil capture tanpa menguji struktur VFS yang dihasilkan.

---

## 12. Ikon/Aset MSIX

Sediakan PNG, bukan ICO sahaja:

```text
Assets\StoreLogo.png       50x50
Assets\Square44x44Logo.png 44x44
Assets\Square150x150Logo.png 150x150
Assets\Wide310x150Logo.png 310x150
```

Gunakan latar telus jika sesuai. Pastikan imej tajam pada skala 100%, 150%,
200% dan 400% jika Packaging Tool menjana varian.

Aset Store berasingan daripada `app.ico` dalam EXE.

---

## 13. Tandatangan untuk Ujian Tempatan

### Store

Pakej untuk Store tidak memerlukan sijil CA anda. Microsoft menandatangani
pakej selepas pensijilan.

### Ujian sebelum Store

MSIX tempatan mesti ditandatangani dan sijil mesti dipercayai pada mesin ujian.
Cara moden:

```powershell
winget install -e --id Microsoft.WinAppCLI --source winget
winapp cert generate --manifest .\AppxManifest.xml `
  --output .\devcert.pfx --install
winapp sign .\PustakaHadis_1.0.0.0_x64.msix --cert .\devcert.pfx
```

WinApp CLI masih boleh berubah; jika gagal, gunakan PowerShell + SignTool
mengikut panduan Microsoft. `Subject` sijil mesti sama tepat dengan Publisher
manifest.

**Jangan edarkan sijil PFX atau kata laluannya.** Untuk penguji, eksport `.cer`
(public key) sahaja dan pasang ke `TrustedPeople`.

Pasang pakej ujian:

```powershell
Add-AppxPackage .\PustakaHadis_1.0.0.0_x64.msix
```

---

## 14. Uji MSIX

Selepas dipasang:

- launch dari Start Menu;
- `PustakaHadis.exe` tidak meminta Administrator;
- lokasi aplikasi baca sahaja;
- DB/settings berada di data pengguna;
- sync boleh disambung selepas app ditutup paksa;
- carian makna tidak crash akibat DLL;
- buka pautan web berfungsi;
- update `1.0.0.0 → 1.0.1.0` mengekalkan data;
- uninstall bersih;
- pasang semula dan periksa tingkah laku data pengguna;
- uji pada Windows 10 dan Windows 11.

Jalankan Windows App Certification Kit jika tersedia. WACK tempatan kini
bersifat pilihan/deprecated, tetapi masih berguna; pensijilan sebenar dilakukan
semasa submission Partner Center.

---

## 15. Hantar ke Microsoft Store

Partner Center → produk Pustaka Hadis → submission baharu.

Lengkapkan:

1. **Packages** — muat naik `.msix`/`.msixbundle`.
2. **Properties** — kategori Education/Books & Reference yang sesuai.
3. **Age ratings** — jawab soal selidik IARC.
4. **Store listings**:
   - Bahasa Melayu;
   - penerangan ringkas/panjang;
   - ikon;
   - sekurang-kurangnya 4 tangkapan skrin;
   - nota bahawa data awal perlu diselaraskan;
   - pautan sokongan;
   - URL dasar privasi.
5. **Pricing and availability** — percuma.
6. **Notes for certification**:
   - aplikasi ialah PyQt5 Win32 full-trust;
   - API key disimpan setempat;
   - langkah mendapatkan kunci ujian;
   - cara mencapai semua fungsi;
   - nyatakan carian makna mungkin memerlukan aset/model;
   - beri akaun/kunci ujian jika polisi membenarkan, jangan letak rahsia kekal.
7. Semak lesen dan atribusi semua data.
8. Klik **Submit to Store**.

Pensijilan boleh mengambil sehingga kira-kira tiga hari bekerja. Jika gagal,
baca laporan, baiki dan hantar submission baharu.

Selepas lulus, Microsoft menandatangani pakej dengan sijil yang dipercayai dan
menerbitkannya tanpa amaran pemasangan biasa.

---

## 16. Ujian Naik Taraf Wajib

Sebelum keluaran awam:

1. Pasang MSIX `1.0.0.0`.
2. Masukkan tetapan palsu dan satu bookmark.
3. Sync beberapa halaman.
4. Bina `1.0.1.0` dengan identiti sama.
5. Pasang kemas kini.
6. Sahkan:
   - settings kekal;
   - bookmark kekal;
   - DB kekal;
   - FTS masih berfungsi;
   - model/index boleh dibaca;
   - hanya satu entri Start Menu.
7. Cuba downgrade — sepatutnya ditolak kecuali mekanisme downgrade sengaja
   dikonfigurasi.

Jangan tukar `Identity Name`, `Publisher`, `Application Id` atau seni bina
antara versi.

---

## 17. Masalah Lazim

### `No module named ...`

Tambah modul kepada `--hidden-import` atau `--collect-all`, kemudian bina
semula dari venv bersih.

### Qt platform plugin `windows` tiada

Pastikan hanya PyQt5 dipasang dan hook PyInstaller terkini. Jangan salin plugin
Qt daripada pemasangan Python lain.

### `WinError 1114` / `c10.dll`

Konflik runtime PyQt5/torch. Periksa DLL yang dibundel dengan Process Monitor
atau Dependencies. Gunakan runtime MSVC yang lebih baharu dan jangan ubah
folder pakej ketika runtime.

### Model cuba muat turun semasa launch

`.cache_models` tidak dibundel atau kod masih menunjuk folder data yang salah.
Betulkan `MODEL_CACHE` kepada `ASSET_DIR`.

### DB dicipta dalam folder EXE

Masih ada modul yang mengira laluan sendiri. Ulang grep §3.2 dan pusatkan
semua laluan.

### MSIX gagal upload kerana Publisher/Name

Salin semula nilai tepat dari **Product identity** Partner Center. Jangan
ubah PublisherDisplayName secara rawak.

### Pakej tempatan tidak boleh dipasang

Sijil tidak dipercayai atau Subject tidak sepadan dengan Publisher manifest.
Store tidak mempunyai masalah ini kerana Microsoft menandatangani selepas
pensijilan.

### Aplikasi berjalan dalam folder PyInstaller tetapi gagal sebagai MSIX

Periksa:

- tulisan ke lokasi pemasangan;
- current working directory;
- AppData virtualization;
- fail DLL dimuat dari lokasi salah;
- entry point MSIX;
- `runFullTrust`.

Gunakan ProcMon dan pertimbang Package Support Framework hanya jika kod tidak
boleh diperbetulkan. Pembetulan dalam kod lebih mudah diselenggara.

---

## 18. Checklist Keluaran

### Kod

- [ ] Semua laluan data dipusatkan.
- [ ] `multiprocessing.freeze_support()` dipanggil.
- [ ] Tiada subprocess `python main.py` melalui `launcher.py`.
- [ ] Semua ujian projek lulus.

### PyInstaller

- [ ] Binaan debug berkonsol lulus.
- [ ] Binaan windowed lulus.
- [ ] Diuji tanpa Python dipasang.
- [ ] Model/index dijumpai.
- [ ] Tiada `.env`, DB atau rahsia dalam dist.

### MSIX

- [ ] Identiti sama dengan Partner Center.
- [ ] Versi empat bahagian.
- [ ] x64.
- [ ] Ikon lengkap.
- [ ] `runFullTrust`.
- [ ] Uji install/update/uninstall.
- [ ] Uji Windows 10 + 11.

### Store

- [ ] Dasar privasi tersedia.
- [ ] Pautan sokongan tersedia.
- [ ] Atribusi data lengkap.
- [ ] Lesen data disahkan.
- [ ] Tangkapan skrin disediakan.
- [ ] Notes for certification lengkap.

---

## 19. Urutan Paling Ringkas

```text
1. Selesaikan laluan %LOCALAPPDATA%
2. Tempah nama + salin identiti Partner Center
3. Bina PyInstaller debug onedir
4. Uji pada Windows bersih
5. Bina PyInstaller windowed onedir
6. Bina Inno Setup EXE
7. Convert EXE -> MSIX dalam VM bersih
8. Tandatangan sendiri untuk ujian sahaja
9. Uji MSIX + naik taraf
10. Upload MSIX ke Partner Center
11. Lengkapkan listing/privasi/lesen
12. Submit dan baiki laporan pensijilan
```

---

## 20. Rujukan Rasmi

- Microsoft Store publishing:
  `https://learn.microsoft.com/windows/apps/publish/`
- Pilihan MSIX berbanding EXE/MSI:
  `https://learn.microsoft.com/windows/apps/distribute-through-store/how-to-distribute-your-win32-app-through-microsoft-store`
- MSIX Packaging Tool:
  `https://learn.microsoft.com/windows/msix/packaging-tool/create-app-package`
- Tandatangan MSIX:
  `https://learn.microsoft.com/windows/msix/package/sign-msix-package-guide`
- Tingkah laku aplikasi desktop berbungkus:
  `https://learn.microsoft.com/windows/msix/desktop/desktop-to-uwp-behind-the-scenes`
- Sediakan aplikasi desktop untuk MSIX:
  `https://learn.microsoft.com/windows/msix/desktop/desktop-to-uwp-prepare`
- Pensijilan Store:
  `https://learn.microsoft.com/windows/apps/publish/publish-your-app/msix/app-certification-process`
- PyInstaller:
  `https://pyinstaller.org/`

---

## 21. Keputusan Go/No-Go

**Boleh mula sekarang:**

- refactor laluan;
- bina EXE debug;
- ujian VM;
- cipta MSIX persendirian;
- siapkan listing, ikon dan dasar privasi.

**Belum boleh diterbitkan awam:**

- jika lesen data belum selesai;
- jika DB masih ditulis ke folder aplikasi;
- jika carian makna gagal dalam binaan;
- jika update memadam data;
- jika hanya diuji pada mesin pembangun.
