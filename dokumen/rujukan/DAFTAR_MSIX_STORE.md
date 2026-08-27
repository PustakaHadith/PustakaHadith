# Daftar Microsoft Store (Partner Center) & Tempah Identiti MSIX

> **TUJUAN:** Panduan langkah demi langkah untuk anda (pemilik akaun)
> mendaftar akaun pembangun Microsoft Store / Partner Center dan **menempah
> identiti aplikasi** yang diperlukan sebelum pakej MSIX boleh dibina.
>
> **STATUS:** ⛔ Belum dilakukan — ini adalah tugas **pengguna**, bukan
> tugas pembangun. Tanpa 3 nilai di bawah, Fasa 5C (MSIX) dan Fasa 6
> (Partner Center) **tersekat**.

---

## Mengapa ini perlu

Pakej MSIX **mesti** membawa identiti yang **tepat sepadan** dengan
Partner Center, jika tidak:

- `Add-AppxPackage` gagal (Publisher tidak sepadan).
- Upload ke Store ditolak.
- Microsoft **tidak boleh** menandatangani semula pakej → SmartScreen
  masih beri amaran.

Nilai yang diperlukan (salin **tepat**, jangan reka sendiri):

```text
Package/Identity/Name              = PustakaHadith
Package/Identity/Publisher         = CN=...., O=....,  (dari Partner Center)
Package/Properties/PublisherDisplayName = PustakaHadith
```

> **Nama:** identiti pakej = `PustakaHadith` (tanpa jarak). Nama paparan
> (Display name) boleh `PustakaHadith` (dengan jarak) — ditetapkan bila
> isi manifest MSIX, bukan di sini.

---

## Prasyarat

- **Microsoft account** (Outlook/Hotmail/peribadi). Boleh guna
  `pustaka.hadith@outlook.com` atau akaun anda sendiri.
- Akses ke **e-mel** dan **nombor telefon** untuk pengesahan.
- **Kad kredit/debit** — mungkin diperlukan untuk pengesahan identiti
  (Microsoft biasanya caj **pengesahan kecil $0–1**, bukan yuran; sejak
  2026 yuran $19/$99 individu/syarikat telah **dibuang** — sahkan di
  skrin pendaftaran).

---

## Langkah demi langkah

### 1. Buka portal pendaftaran
Pergi ke <https://storedeveloper.microsoft.com/>
(atau `https://partner.microsoft.com/dashboard` → **Apps and games**).

### 2. Log masuk / daftar
Guna Microsoft account. Jika pertama kali, klik **Register / Daftar
sebagai pembangun**.

### 3. Pilih jenis akaun
- **Individual** — lebih pantas (pengesahan diri).
- **Company** — perlubutiran syarikat + pengesahan tambahan (1–2 hari
  kerja).

> Untuk apl percuma tiada komersial seperti ini, **Individual** sudah
> memadai.

### 4. Lengkapkan profil & pengesahan identiti
- Isi nama, alamat, negara.
- **Pengesahan telefon** (SMS/kod).
- **Pengesahan e-mel** (pautan dalam inbox).
- Terima **App Developer Agreement** (perjanjian pembangun Store).

### 5. Cipta entri aplikasi
- Dalam Partner Center → **Apps and games** → **Create app** (atau
  **New product → MSIX or PWA app**).
- Taip **`PustakaHadith`** dalam kotak "app name".
- Klik **Check availability / Check name**.
- Jika tersedia, klik **Reserve / Create** untuk **menempah nama
  segera** (nama boleh diambil orang lain bila-bila masa).

### 6. Dapatkan identiti pakej
- Buka aplikasi yang baru ditempah → **Product management → Product
  identity** (atau **App management → App identity**).
- Salin **TEPAT** 3 nilai (huruf besar/kecil dan tanda koma mesti sama):
  - `Package/Identity/Name` → `PustakaHadith`
  - `Package/Identity/Publisher` → `CN=..., O=..., ...` (nilai penuh
    dari Store)
  - `Package/Properties/PublisherDisplayName` → `PustakaHadith`

### 7. Simpan nilai ke fail rujukan
Salin ke `installer\msix_identity.txt` supaya mudah dipaste semasa
capture MSIX:

```text
Package/Identity/Name=PustakaHadith
Package/Identity/Publisher=CN=.... (dari Partner Center - jangan ubah)
Package/Properties/PublisherDisplayName=PustakaHadith
```

### 8. Serahkan nilai kepada pembangun
Beri 3 nilai di atas (atau fail `msix_identity.txt`) kepada pembangun
untuk:

- **Fasa 5C** — isi manifest MSIX Packaging Tool (INSTALLER.md §11,
  penerbitan/penerbitan/VM_MSIX_CAPTURE.md).
- **Fasa 6** — upload + submission Store.

---

## Selepas daftar (bukan tugas anda)

1. **Fasa 5C — Bina MSIX:** pembangun jalankan MSIX Packaging Tool dalam
   VM Windows bersih, isi 3 nilai di atas, capture `dist/PustakaHadith`
   → `PustakaHadith_1.0.0.0_x64.msix` (rujuk INSTALLER.md §11,
   penerbitan/penerbitan/MSIX_CAPTURE_PROSES.md).
2. **Fasa 6 — Partner Center:** upload MSIX, isi listing, muat naik
   tangkapan skrin (penerbitan/penerbitan/TANGKAPAN_SKRIN.md), pautan sokongan
   (surat/sokongan/surat/sokongan/PAUTAN_SOKONGAN.md), dasar privasi (surat/sokongan/surat/sokongan/DASAR_PRIVASI.md).
3. Microsoft **menandatangani semula** pakej → tiada amaran SmartScreen
   (percuma untuk Store rasmi).

---

## Rujukan

- `dokumen/rujukan/INSTALLER.md` §10 (daftar), §11 (capture MSIX)
- `dokumen/CHECKLIST_PEMANTAUAN.md` — Fasa 0, 5C, 6
- `dokumen/penerbitan/penerbitan/penerbitan/VM_MSIX_CAPTURE.md`, `dokumen/penerbitan/penerbitan/penerbitan/MSIX_CAPTURE_PROSES.md`
- `dokumen/penerbitan/penerbitan/penerbitan/TANGKAPAN_SKRIN.md`, `dokumen/surat/sokongan/surat/sokongan/surat/sokongan/DASAR_PRIVASI.md`,
  `dokumen/surat/sokongan/surat/sokongan/surat/sokongan/PAUTAN_SOKONGAN.md`
