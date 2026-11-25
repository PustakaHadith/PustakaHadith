# Senarai Fail - PustakaHadith v1.2.0

> **Tarikh:** 25 November 2026
> **Versi:** 1.2.0

---

## 📦 Fail Yang Dicipta

### 1. Dokumentasi

| Fail | Lokasi | Keterangan |
|---|---|---|
| **BUILD_MSIX.md** | `installer\BUILD_MSIX.md` | Dokumentasi lengkap pembuatan MSIX |
| **BUILD_ALL.bat** | `BUILD_ALL.bat` | Script build lengkap (EXE + ZIP + MSIX) |

### 2. EXE (PyInstaller)

| Item | Nilai |
|---|---|
| **Lokasi** | `D:\Pustaka Quran Hadis\Pustaka\PustakaHadith\dist\PustakaHadith\PustakaHadith.exe` |
| **Saiz** | 74.3 MB |
| **Tarikh** | 25 November 2026, 13:45 |
| **Build dengan** | `BINA.bat` atau `_rebuild.bat` |

### 3. ZIP (Portable)

| Item | Nilai |
|---|---|
| **Lokasi** | `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-portable-1.2.0-x64.zip` |
| **Saiz** | 757.9 MB |
| **Tarikh** | 25 November 2026, 13:51 |
| **Kandungan** | EXE + `_internal\` (hadis.db + semua dependencies) |

### 4. MSIX (Microsoft Store)

| Item | Nilai |
|---|---|
| **Lokasi** | `D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\msix\PustakaHadith_1.2.0_x64.msix` |
| **Saiz** | 783 MB |
| **Tarikh** | 25 November 2026, 13:52 |
| **Versi manifest** | `1.2.0.0` |

---

## 📁 Struktur Folder

```
D:\Pustaka Quran Hadis\Pustaka\
├── PustakaHadith\                    # Source code
│   ├── VERSI.py                      # Cap versi tunggal (1.2.0)
│   ├── semak.py                      # Ujian (381/381)
│   ├── main.py                       # Entry point
│   ├── PustakaHadith.spec            # PyInstaller spec
│   ├── BINA.bat                      # Build EXE
│   ├── _rebuild.bat                  # Rebuild EXE
│   ├── BUILD_ALL.bat                 # Build semua (EXE+ZIP+MSIX) ★ BARU
│   ├── dist\PustakaHadith\           # Output EXE
│   │   ├── PustakaHadith.exe
│   │   └── _internal\
│   │       ├── hadis.db              # 62,169 hadis
│   │       ├── transformers\
│   │       ├── torch\
│   │       └── ...
│   ├── installer\
│   │   ├── build_msix.ps1            # Build MSIX
│   │   ├── BUILD_MSIX.md             # Dokumentasi MSIX ★ BARU
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

## 🔧 Cara Guna

### Build Semua Sekali Guna

```cmd
BUILD_ALL.bat
```

### Build Berasingan

```cmd
# 1. Build EXE sahaja
BINA.bat

# 2. Build MSIX sahaja
powershell -ExecutionPolicy Bypass -File "installer\build_msix.ps1"
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

---

## 📝 Sejarah Versi

| Versi | Tarikh | MSIX Size | Catatan |
|---|---|---|---|
| 1.0.2.0 | 18 Sep 2026 | 781.9 MB | MSIX asal (penuh) |
| 1.1.0 | 9 Okt 2026 | 73.8 MB | Certified & Published ke Store |
| 1.2.0 | 25 Nov 2026 | 783 MB | Buka max 85% + nav no. 2 |
