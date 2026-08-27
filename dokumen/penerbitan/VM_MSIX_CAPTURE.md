# Persediaan VM Bersih untuk MSIX Capture

> Dokumentasi untuk sediakan VM Windows 11 bersih untuk capture MSIX
> menggunakan MSIX Packaging Tool (Manual installation).

---

## Keperluan VM

| Item | Spesifikasi |
|---|---|
| OS | Windows 11 Pro/Enterprise 23H2+ (x64) |
| RAM | Minimum 8 GB (disyorkan 16 GB) |
| Cakera | Minimum 100 GB bebas |
| Rangkaian | Internet (muat turun alatan) |
| Snapshot | **Wajib** sebelum capture |

---

## Pemasangan Alatan dalam VM

```powershell
# 1. Pasang winget (sudah ada dalam Windows 11)
# 2. Pasang MSIX Packaging Tool
winget install --id Microsoft.MSIXPackagingTool --source winget --accept-source-agreements --accept-package-agreements

# 3. Pasang WinApp CLI (untuk sijil ujian)
winget install --id Microsoft.WinAppCli --source winget --accept-source-agreements --accept-package-agreements

# 4. Semak pemasangan
msixpackagingtool --version
winappcert --version
```

---

## Persediaan Payload

Salinkan folder payload ke VM (contoh: `C:\Payload\PustakaHadis`):

```powershell
# Dari mesin binaan, salin:
# dist\PustakaHadis\*  →  VM:C:\Payload\PustakaHadis\
```

Struktur payload yang bersih (sudah disahkan audit):
```
C:\Payload\PustakaHadis\
├── _internal\           # Semua kebergantungan Python/PyQt/FAISS/model
├── PustakaHadis.exe     # Entry point tunggal
```

**Tiada** fail terlarang: hadis.db, .env, user_settings.json, bookmarks.json, .cache_*, *.bak, __pycache__, log.

---

## Sediakan Aset PNG

Salinkan aset ke VM:
```
installer\Assets\StoreLogo.png           → 50×50
installer\Assets\Square44x44Logo.png     → 44×44
installer\Assets\Square150x150Logo.png   → 150×150
installer\Assets\Wide310x150Logo.png     → 310×150
```

---

## Cipta Snapshot VM (Wajib)

Selepas pemasangan alatan + payload + aset disalin:

1. Hyper-V Manager → VM → **Checkpoint** → nama: `Pre-MSIX-Capture`
2. Atau PowerShell:
```powershell
Checkpoint-VM -Name "PustakaHadith-VM" -SnapshotName "Pre-MSIX-Capture"
```

---

## Jalankan MSIX Packaging Tool (Manual Installation)

1. Buka **MSIX Packaging Tool** (Start Menu).
2. Pilih **Create package** → **Manual installation**.
3. **Package details**:
   - Package name: `PustakaHadis`
   - Publisher: `CN=<Publisher dari Partner Center>` (contoh: `CN=12345678-ABCD-...`)
   - Version: `1.0.0.0`
   - Architecture: x64
4. **Installation**:
   - Installer: **kosongkan** (Manual)
   - Install location: `C:\Program Files\PustakaHadis`
   - **Prepare computer** — wizard akan cuba aktifkan driver (2 kali cuba)
5. Klik **Next** → wizard bersedia untuk capture.

### Capture Installation

1. Wizard papar: "Ready to capture" — **jangan klik Next lagi**.
2. Buka Explorer → `C:\Payload\PustakaHadis` → jalankan `PustakaHadis.exe`.
3. **Dalam aplikasi**:
   - Terima notis (Enter)
   - **JANGAN** masukkan API key
   - **JANGAN** klik Sync
   - Tutup aplikasi (Alt+F4 atau butang X)
4. Kembali ke wizard → klik **Next**.
5. Wizard mengesan perubahan → papar fail/folder baru.

### Package Editor (Semak Sebelum Simpan)

| Item | Nilai Diperlukan |
|---|---|
| Entry point | `PustakaHadis.exe` (satu sahaja) |
| Capabilities | `runFullTrust` ✓ |
| Device capabilities | `Windows.Desktop` ✓ |
| Min version | `10.0.19041.0` (Windows 10 2004) |
| Target device family | `Windows.Desktop` |
| Applications | 1 aplikasi: `PustakaHadis` |
| Visual assets | 4 PNG (50, 44, 150, 310×150) ✓ |
| **Tiada** | DB, .env, settings, bookmarks, cache, log |

Jika ada item tidak perlu → **Delete** dalam Package Editor.

---

## Simpan & Tandatangan Ujian

1. **Save package** → lokasi output (contoh: `C:\Output\PustakaHadis_1.0.0.0_x64.msix`)
2. **Sign package** (ujian tempatan):
```powershell
# Jana sijil ujian tempatan
winappcert create --publisher "CN=<Publisher>" --output "C:\Certs\TestCert.pfx" --password "test123"

# Tandatangani MSIX
SignTool sign /fd SHA256 /f "C:\Certs\TestCert.pfx" /p "test123" "C:\Output\PustakaHadis_1.0.0.0_x64.msix"
```
Atau guna **Package Editor → Sign** dengan sijil yang sama.

---

## Uji Pemasangan MSIX

```powershell
# Pasang
Add-AppxPackage -Path "C:\Output\PustakaHadis_1.0.0.0_x64.msix"

# Lancar
Start-Process "shell:AppsFolder\<PackageFamilyName>!PustakaHadis"

# Semak
# - Splash papar
# - Notis papar
# - Tiada API key (mod luar talian - carian kata kunci berfungsi)
# - Tetapan → API key boleh dimasukkan

# Nyahpasang
Get-AppxPackage -Name "PustakaHadis" | Remove-AppxPackage
```

---

## Rollback Jika Gagal

```powershell
# Kembalikan VM ke snapshot bersih
Restore-VMSnapshot -VMName "PustakaHadith-VM" -Name "Pre-MSIX-Capture"
```

---

## Nota Penting

- **Jangan** sync/masukkan API key semasa capture
- **Jangan** buka hadis berbeza-beda (hanya buka, tutup)
- **Satu** entry point sahaja
- **Tiada** data pengguna dalam pakej
- Identiti Publisher **mesti sepadan** Partner Center (selewnya instal gagal)

---

*Dokumen: `dokumen\penerbitan/penerbitan/VM_MSIX_CAPTURE.md` · Folder binaan installer*