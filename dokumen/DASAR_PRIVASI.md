# Dasar Privasi — PustakaHadith

**Tarikh berkuat kuasa:** 20 Ogos 2026  
**Versi:** 1.0  
**Pemilik:** PustakaHadith

---

## Ringkasan

PustakaHadith adalah aplikasi pangkalan data hadis luar talian. Aplikasi ini **tidak mengumpul, menyimpan, atau mengongsikan** sebarang data peribadi anda kepada pihak ketiga.

---

## Data Yang Dikumpul (Tiada)

| Kategori | Dikumpul? | Butiran |
|---|---|---|
| Data peribadi (nama, e-mel, ID) | **Tidak** | Aplikasi tidak meminta daftar akaun |
| Data lokasi | **Tidak** | Tiada akses GPS/lokasi |
| Data penggunaan/analitik | **Tidak** | Tiada telemetri, crash report, analitik |
| Kandungan pengguna | **Tidak** | Penanda buku, tetapan hanya dalam peranti anda |
| Pengenal peranti | **Tidak** | Tiada pengesan peranti/unik |

---

## Data Yang Disimpan Secara Tempatan (Dalam Peranti Anda)

Semua data disimpan **hanya dalam folder data aplikasi anda**:

```
%LOCALAPPDATA%\PustakaHadis\
├── hadis.db              # Pangkalan data hadis (62,169 rekod) — hanya baca
├── user_settings.json    # Tetapan anda (tema, saiz fon, kunci API tertopeng)
├── bookmarks.json        # Penanda halaman anda
└── profil_model.json     # Log masa muat model AI (teknikal)
```

- Fail-fail ini **tidak dihantar ke server mana-mana**.
- Anda boleh memadam folder ini untuk mengosongkan data.
- Nyahpasang aplikasi **tidak memadam** folder ini.

---

## Kunci API (Pilihan)

- Untuk **muat turun data hadis** (sync), anda memasukkan kunci API dari https://hadis.my
- Kunci disimpan **tertulis (tertutup/bertopeng)** dalam `user_settings.json`
- Kunci **tidak dikongsi** ke mana-mana server kecuali hadis.my (apabila anda klik "Sync")
- Kuota: 200 permintaan/hari, diset semula 12 malam (polisi hadis.my)

---

## Carian Makna (AI) — Sepenuhnya Luar Talian

- Model AI (`intfloat/multilingual-e5-small`) **dibundel dalam aplikasi**
- Carian makna dijalankan **sepenuhnya di peranti anda** (tiada internet diperlukan)
- Tiada teks carian dihantar ke cloud

---

## Sambungan Rangkaian

Aplikasi hanya menyambung ke internet untuk **satu** tujuan:

| Tujuan | Server | Data Dihantar |
|---|---|---|
| Sync data hadis | `service.hadis.my` (API hadis.my) | Kunci API + permintaan data hadis (hanya jika anda klik Sync) |

Tiada sambungan lain (tiada pemeriksaan kemas kini automatik, tiada telemetri).

---

## Hak Anda

- **Akses**: Semua data anda dalam peranti anda.
- **Padam**: Padam folder `%LOCALAPPDATA%\PustakaHadis` bila-bila masa.
- **Portabiliti**: Salin folder data ke peranti lain.
- **Tidak perlu** menghubungi kami untuk memadam data — data dalam milik anda.

---

## Perubahan Dasar

Sebarang perubahan akan dikemaskini di halaman ini dengan tarikh baharu. Semak sebelum kemas kini aplikasi.

---

## Hubungi Kami

Soalan mengenai privasi:

| Jenis | E-mel |
|---|---|
| **Umum / Surat menyurat** | `pustakahadith@gmail.com` |
| **Microsoft Store / MSIX** | `pustaka.hadith@outlook.com` |
| **Backup / Selamat** | `pustaka.hadith@proton.me` |

GitHub Issues: https://github.com/opencodemk/PustakaHadith/issues

---

*Dokumen: `dokumen\DASAR_PRIVASI.md` · Untuk Microsoft Store (Gate 6)*