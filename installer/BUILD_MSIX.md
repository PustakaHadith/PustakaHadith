# Dokumentasi Pembuatan MSIX - PustakaHadith

> **Versi semasa:** 1.2.0 (25 November 2026)
> **Cap versi tunggal:** `VERSI.py` → `VERSI = "1.2.0"`

---

## 📦 Senarai Fail Yang Dicipta

### 1. EXE (PyInstaller)

| Item | Nilai |
|---|---|
| **Lokasi** | `D:\Pustaka Quran Hadis\Pustaka\PustakaHadith\dist\PustakaHadith\PustakaHadith.exe` |
| **Saiz** | 74.3 MB |
| **Tarikh** | 25 November 2026, 13:45 |
| **Build script** | `BINA.bat` atau `_rebuild.bat` |
| **Spec file** | `PustakaHadith.spec` |
| **Python** | `.venv-build\Scripts\python.exe` (Python 3.14.6) |

### 2. ZIP (Portable)

| Item | Nilai |
|---|---|
| **Lokasi** | `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-portable-1.2.0-x64.zip` |
| **Saiz** | 757.9 MB |
| **Tarikh** | 25 November 2026, 13:51 |
| **Kandungan** | EXE + `_internal\` (hadis.db + semua dependencies) |
| **Cipta dengan** | `Compress-Archive -Path "dist\PustakaHadith\*" -DestinationPath $zipPath` |

### 3. MSIX (Microsoft Store)

| Item | Nilai |
|---|---|
| **Lokasi** | `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\msix\PustakaHadith_1.2.0_x64.msix` |
| **Saiz** | 783 MB |
| **Tarikh** | 25 November 2026, 13:53 |
| **Versi manifest** | `1.2.0.0` |
| **Build script** | `installer\build_msix.ps1` |
| **Kandungan** | EXE + `_internal\` + `Assets\` + `AppxManifest.xml` |

---

## 🔧 Proses Pembinaan

### Langkah 1: Update Versi

Sebelum build, pastikan versi dikemas kini di:

1. **`VERSI.py`** (cap versi tunggal)
   ```python
   VERSI = "1.2.0"
   ```

2. **`semak.py`** (versi dikunci untuk ujian)
   ```python
   if VERSI != "1.2.0":
       salah(f"VERSI dikunci 1.2.0 (edaran rasmi), sebenar {VERSI!r}")
   ```

3. **`installer\build_msix.ps1`** (versi MSIX manifest)
   ```powershell
   # Line 38: Identity Version
   <Identity Name="$name" Publisher="$pub" Version="1.2.0.0" ... />
   
   # Line 72: Output filename
   $msix = Join-Path $out "PustakaHadith_1.2.0_x64.msix"
   ```

4. **`dokumen\perubahan\CHANGELOG.md`** (tambah entry versi baru)

### Langkah 2: Rebuild EXE

```powershell
# Option A: Guna BINA.bat (recommended)
BINA.bat

# Option B: Guna _rebuild.bat
_rebuild.bat

# Option C: Manual
cd "D:\Pustaka Quran Hadis\Pustaka\PustakaHadith"
".venv-build\Scripts\python.exe" -m PyInstaller PustakaHadith.spec --clean --noconfirm
```

**Output:** `dist\PustakaHadith\PustakaHadith.exe`

### Langkah 3: Cipta ZIP

```powershell
$sourceDir = "D:\Pustaka Quran Hadis\Pustaka\PustakaHadith\dist\PustakaHadith"
$zipPath = "D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-portable-1.2.0-x64.zip"

# Padam ZIP lama jika wujud
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

# Cipta ZIP baru
Compress-Archive -Path "$sourceDir\*" -DestinationPath $zipPath -Force
```

**Output:** `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-portable-1.2.0-x64.zip`

### Langkah 4: Rebuild MSIX

```powershell
# Jalankan build script
& "D:\Pustaka Quran Hadis\Pustaka\PustakaHadith\installer\build_msix.ps1"
```

**Output:** `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\msix\PustakaHadith_1.2.0_x64.msix`

**Nota:** SignTool verify error adalah normal (self-signed certificate).

---

## 📁 Struktur Folder

```
D:\Pustaka Quran Hadis\Pustaka\
├── PustakaHadith\                    # Source code
│   ├── VERSI.py                      # Cap versi tunggal
│   ├── semak.py                      # Ujian (381/381)
│   ├── main.py                       # Entry point
│   ├── PustakaHadith.spec            # PyInstaller spec
│   ├── BINA.bat                      # Build EXE
│   ├── _rebuild.bat                  # Rebuild EXE
│   ├── dist\PustakaHadith\           # Output EXE
│   │   ├── PustakaHadith.exe
│   │   └── _internal\
│   │       ├── hadis.db              # 62,169 hadis
│   │       ├── transformers\
│   │       ├── torch\
│   │       └── ...
│   ├── installer\
│   │   ├── build_msix.ps1            # Build MSIX
│   │   ├── BUILD_MSIX.md             # Dokumen ini
│   │   ├── msix_identity.txt         # Identity MSIX
│   │   ├── msix_temp.pfx             # Sertifikat self-signed
│   │   └── Assets\                   # Logo MSIX
│   └── dokumen\perubahan\
│       └── CHANGELOG.md              # Log perubahan versi
│
└── PustakaQH_dist\                   # Output final
    ├── msix\
    │   └── PustakaHadith_1.2.0_x64.msix    # MSIX untuk Store
    ├── PustakaHadith-portable-1.2.0-x64.zip # ZIP portable
    └── PustakaHadith\                # Copy EXE (untuk ujian)
        └── _internal\hadis.db
```

---

## ⚠️ Penting

### Saiz Fail

| Jenis | Saiz | Catatan |
|---|---|---|
| **EXE sahaja** | ~74 MB | Tanpa dependencies |
| **ZIP lengkap** | ~758 MB | Dengan hadis.db + dependencies |
| **MSIX lengkap** | ~783 MB | Untuk Microsoft Store |

**Jangan keliru:** MSIX 74 MB adalah TIDAK LENGKAP (tiada hadis.db).

### Versi

- **Cap versi tunggal:** `VERSI.py`
- **Semua UI guna:** `from VERSI import VERSI`
- **Jangan hardcode versi** dalam mana-mana fail lain

### Sertifikat

- **MSIX guna:** Self-signed certificate (`msix_temp.pfx`)
- **Password:** `PustakaMSIX2026`
- **SignTool verify error:** Normal (self-signed)

---

## 📝 Sejarah Versi

| Versi | Tarikh | MSIX Size | Catatan |
|---|---|---|---|
| 1.0.2.0 | 18 Sep 2026 | 781.9 MB | MSIX asal (penuh) |
| 1.1.0 | 9 Okt 2026 | 73.8 MB | Certified & Published ke Store |
| 1.2.0 | 25 Nov 2026 | 783 MB | Buka max 85% + nav no. 2 |

---

## 🔗 Pautan

- **GitHub:** https://github.com/PustakaHadith/Pustaka
- **Landing Page:** https://pustakahadith.my
- **Microsoft Store:** Pencarian "Pustaka Hadith"
