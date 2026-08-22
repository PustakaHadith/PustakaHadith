# Proses Capture MSIX — Checklist Lengkap

**Untuk Gate 5C → 6**  
**Versi:** 1.0 (20 Ogos 2026)

---

## Prasyarat (Perlu Sedia Sebelum Capture)

| Item | Status | Nota |
|---|---|---|
| Identiti Partner Center | ⛔ **Menunggu pengguna** | `Package/Identity/Name`, `Publisher`, `PublisherDisplayName` |
| VM bersih + snapshot | ☐ | Dokumentasi: `VM_MSIX_CAPTURE.md` |
| Payload `dist\PustakaHadis` | ✅ | 0.54 GB ZIP sedia, audit bersih |
| Aset PNG (50, 44, 150, 310×150) | ✅ | `installer\Assets\` |
| MSIX Packaging Tool + WinApp CLI | ✅ | Dipasang (winget) |
| Dasar privasi | ✅ | `DASAR_PRIVASI.md` |
| Pautan sokongan | ☐ | `PAUTAN_SOKONGAN.md` — perlu URL sebenar |
| Tangkapan skrin (4-8) | ☐ | `TANGKAPAN_SKRIN.md` — perlu ambil skrin |

---

## Checklist Capture (Dalam VM)

### Fasa 1: Persediaan VM
- [ ] VM Windows 11 Pro/Enterprise x64 (8+ GB RAM, 100+ GB cakera)
- [ ] Snapshot `Pre-MSIX-Capture` dibuat
- [ ] MSIX Packaging Tool dipasang (winget)
- [ ] WinApp CLI dipasang (winget)
- [ ] Payload disalin ke `C:\Payload\PustakaHadis`
- [ ] Aset PNG disalin ke lokasi akses mudah

### Fasa 2: Wizard MSIX Packaging Tool
- [ ] Buka MSIX Packaging Tool → **Create package** → **Manual installation**
- [ ] **Package details**:
  - [ ] Name: `PustakaHadis`
  - [ ] Publisher: `CN=<Publisher dari Partner Center>` (mesti sepadan!)
  - [ ] Version: `1.0.0.0`
  - [ ] Architecture: `x64`
- [ ] **Installation**:
  - [ ] Installer: **KOSONGKAN** (Manual installation)
  - [ ] Install location: `C:\Program Files\PustakaHadis`
  - [ ] **Prepare computer** — biarkan wizard cuba aktifkan driver (2×)
- [ ] Klik **Next** → "Ready to capture"

### Fasa 3: Capture Installation
- [ ] **JANGAN klik Next** dalam wizard lagi
- [ ] Buka `C:\Payload\PustakaHadis\PustakaHadis.exe`
- [ ] **Dalam aplikasi**:
  - [ ] Terima notis (Enter)
  - [ ] **JANGAN** masukkan API key
  - [ ] **JANGAN** klik Sync
  - [ ] Tunggu model dimuat (splash selesai)
  - [ ] Buka 1-2 hadis untuk memastikan berfungsi
  - [ ] Tutup aplikasi (Alt+F4 / butang X)
- [ ] Kembali ke wizard → klik **Next**
- [ ] Wizard mengesan perubahan → klik **Next**

### Fasa 4: Package Editor (Semak Kritikal)
| Item | Perlu | Tindakan Jika Tidak |
|---|---|---|
| Entry point: `PustakaHadis.exe` | ✅ 1 sahaja | Delete entry point lebihan |
| Capability: `runFullTrust` | ✅ | Tambah dalam Capabilities |
| Device capability: `Windows.Desktop` | ✅ | Tambah |
| Min version: `10.0.19041.0` | ✅ | Set dalam Properties |
| Target: `Windows.Desktop` | ✅ | Set dalam Properties |
| Visual assets: 4 PNG | ✅ | Drag-drop ke Visual Assets |
| **Tiada** `hadis.db`, `.env`, `settings`, `bookmarks`, cache, log | ✅ | Delete jika wujud |

### Fasa 5: Simpan & Tandatangan
- [ ] **Save package** → `C:\Output\PustakaHadis_1.0.0.0_x64.msix`
- [ ] **Jana sijil ujian**:
```powershell
winappcert create --publisher "CN=<Publisher>" --output "C:\Certs\TestCert.pfx" --password "test123"
```
- [ ] **Tandatangani**:
```powershell
SignTool sign /fd SHA256 /f "C:\Certs\TestCert.pfx" /p "test123" "C:\Output\PustakaHadis_1.0.0.0_x64.msix"
```

### Fasa 6: Uji Pemasangan
- [ ] `Add-AppxPackage -Path "C:\Output\PustakaHadis_1.0.0.0_x64.msix"` → **Kod 0**
- [ ] Lancar dari Start Menu → **Splash → Notis → UI utama**
- [ ] Semak: **Tiada API key diminta automatik**, carian kata kunci berfungsi
- [ ] Tetapan → API key → Uji → **Berjaya**
- [ ] Nyahpasang: `Get-AppxPackage -Name "PustakaHadis" | Remove-AppxPackage` → **Kod 0**
- [ ] Semak: **Tiada** folder `C:\Program Files\PustakaHadis` tinggal

---

## Rollback Jika Gagal

```powershell
# Kembalikan VM ke snapshot bersih
Restore-VMSnapshot -VMName "PustakaHadis-VM" -Name "Pre-MSIX-Capture"
# Ulangi dari Fasa 2
```

---

## Output Diperlukan Untuk Gate 6

| Fail | Lokasi | Keterangan |
|---|---|---|
| `PustakaHadis_1.0.0.0_x64.msix` | `installer\output\` | MSIX ditandatangani ujian |
| `TestCert.pfx` | `installer\certs\` | Sijil ujian (simpan selamat) |
| Tangkapan skrin (4-8) | `installer\StoreAssets\Screenshots\` | Untuk Store |
| Dasar privasi (URL) | `DASAR_PRIVASI.md` | URL raw GitHub / laman web |
| Pautan sokongan (URL) | `PAUTAN_SOKONGAN.md` | URL GitHub Issues / Form |

---

## Rujukan Teknikal

- `dokumen\VM_MSIX_CAPTURE.md` — langkah penuh VM
- `dokumen\rujukan\INSTALLER.md` §11–§13 — spesifikasi rasmi
- `dokumen\CHECKLIST_PEMANTAUAN.md` — status Gate 5C/6

---

*Dokumen: `dokumen\MSIX_CAPTURE_PROSES.md` · Folder binaan installer*