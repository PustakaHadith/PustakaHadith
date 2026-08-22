# Manual Pemasangan — PustakaHadith v1.0

> Panduan memasang PustakaHadith pada Windows (64-bit).
> Untuk pengguna aplikasi. Bahasa: Melayu.

---

## Keperluan

| Perkara | Keperluan |
|---|---|
| Sistem | Windows 10 atau Windows 11 (64-bit) |
| Ruang cakera | Lebih kurang 2 GB (aplikasi 1.4 GB + data pengguna) |
| Internet | Perlu untuk muat turun/sync data hadis (cara 1 & 2) |
| Python | **TIDAK diperlukan** — binaan edaran serba lengkap |

---

## Cara Pemasangan

Ada tiga cara. Pilih satu sahaja.

### Cara 1 — Microsoft Store (pakej utama, disyorkan)

Status: **sedang disediakan** — akan tersedia selepas pendaftaran
Microsoft Store selesai.

1. Buka aplikasi **Microsoft Store** pada Windows.
2. Cari **PustakaHadith**.
3. Klik **Dapatkan / Install**.
4. Selepas siap, klik **Buka** — atau cari **PustakaHadith** di menu
   Mula.

Kemas kini dikendalikan automatik oleh Store.

### Cara 2 — Pemasang EXE (pakej sekunder)

Fail: `PustakaHadith-Setup-1.0.0-x64.exe`

1. Klik dua kali fail pemasang.
2. Ikut arahan wizard (bahasa Melayu). Pilihan:
   - **Folder pemasangan** — lalai di folder pengguna anda (tiada
     keperluan pentadbir).
   - **Pintasan Desktop** — tandakan jika mahu ikon di desktop.
3. Klik **Selesai** untuk membuka aplikasi (pilihan).

Mengemas kini: jalankan pemasang versi baharu atas versi lama — data
anda (tetapan, penanda buku, data hadis) **tidak dipadam**.

Membuang: **Tetapan → Apl → Apl dipasang → PustakaHadith → Nyahpasang**
(atau jalankan pemasang dan pilih buang). Data pengguna kekal di
folder data anda.

### Cara 3 — Zip mudah alih (untuk penguji dalaman)

Fail: `PustakaHadith-portable-1.0.0-x64.zip`

1. Buka zip dan **ekstrak penuh** ke satu folder (contoh:
   `D:\PustakaHadith`). Jangan jalankan terus dari dalam zip.
2. Buka folder itu dan klik dua kali **`PustakaHadith.exe`**.
3. Untuk mudah, klik kanan `PustakaHadith.exe` → **Tunjuk lagi pilihan →
   Hantar ke → Desktop (cipta pintasan)**.

Tiada proses pemasangan; buang = padam folder sahaja. Data pengguna
masih disimpan di folder data Windows anda (lihat di bawah).

---

## Kali Pertama Membuka Aplikasi

1. **Skrin pemula (splash)** — aplikasi memuatkan model carian makna
   (AI). Bar kemajuan dipapar; boleh klik untuk melangkau. Kali pertama
   mungkin mengambil masa 1–2 minit kerana Windows menyemak fail —
   ini normal, larian seterusnya lebih laju.
2. **Notis** — baca dan sahkan.
3. **Tetapan API (jika perlu)** — untuk memuat turun data hadis:
   - Klik ikon **gear** (atas kanan) → **Tetapan API**.
   - Masukkan kunci API (percuma): daftar di https://hadis.my
   - Kuota: 200 permintaan sehari, diset semula tengah malam.
   - Klik **Uji** — mesej hijau bermakna berjaya.
4. Aplikasi sedia digunakan.

> Data hadis yang dimuat turun disimpan di komputer anda. Selepas
> dimuat, carian hadis boleh berfungsi tanpa internet (mod luar talian).

---

## Lokasi Data Pengguna

Semua data anda disimpan di satu tempat:

```
%LOCALAPPDATA%\PustakaHadith
```

Cara lihat: tekan `Win + R`, taip `%LOCALAPPDATA%\PustakaHadith`, Enter.

Isi penting:

| Fail | Fungsi |
|---|---|
| `hadis.db` | Data hadis (62,169 hadis) — jangan padam |
| `user_settings.json` | Tetapan anda (tema, saiz fon, kunci API) — jangan padam |
| `bookmarks.json` | Penanda halaman anda — jangan padam |
| `profil_model.json` | Log masa muat model — boleh abaikan |

> Fail-fail ini dicipta sendiri oleh aplikasi. Jangan padam semasa
> aplikasi sedang berjalan. Untuk memindah ke komputer lain, salin
> keseluruhan folder `PustakaHadis` ini.

---

## Masalah Lazim

| Masalah | Penyelesaian |
|---|---|
| **Aplikasi lambat buka kali pertama** | Windows sedang mengimbas fail besar. Tunggu; larian seterusnya lebih laju. |
| **Carian kata kunci tiada hasil** | Cuba perkataan lain, atau gunakan soalan penuh untuk carian makna (AI). |
| **Tab English kelabu / tidak tersedia** | Reka bentuk semasa: terjemahan Inggeris tidak disertakan dalam binaan edaran buat masa ini (menunggu kebenaran lesen). |
| **Sambungan gagal / tiada internet** | Semak sambungan; hadis yang sudah dimuat turun masih boleh dicari (mod luar talian). |
| **Data hilang selepas nyahpasang** | Nyahpasang tidak memadam data pengguna (`%LOCALAPPDATA%\PustakaHadith`). Padam folder itu secara manual jika mahu data dibuang sepenuhnya. |

---

## Sumber dan Atribusi

- **Teks hadis, terjemahan Melayu & Indonesia:** hadis.my — API Hadis
  Malaysia (https://hadis.my)
- **Darjat ulama:** koleksi `fawazahmed0/hadith-api` (domain awam),
  berasal daripada sunnah.com
- **Huraian ringkas:** SemakHadis.com — atribusi dipaparkan pada setiap
  huraian
- **Carian makna (AI):** model `intfloat/multilingual-e5-small`
- **Sumber kod:** https://github.com/opencodemk/PustakaHadith

Notis: teks hadis adalah terjemahan yang mungkin tidak menyeluruh dalam
sumber asal. Semak dengan sumber rujukan utama untuk kegunaan rasmi.

---

*Dokumen: `dokumen/MANUAL_INSTALASI.md` · Folder binaan installer ·
Versi: 1.0 · 20 Ogos 2026*