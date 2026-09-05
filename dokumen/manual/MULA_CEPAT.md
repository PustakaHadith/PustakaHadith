# Mula Cepat — PustakaHadith (untuk pengguna)

> Ringkasan pantas: **apa yang sudah disahkan**, **cara menjalankan
> app**, dan **cara memulakan carian**. Manual penuh:
> `MANUAL_PENGGUNAAN.md` · pemasangan:
> `MANUAL_INSTALASI.md` · panduan langkah pertama
> pemasangan: `BACA_SAYA.txt`.

**PustakaHadith** = koleksi **9 kitab hadis, 62,169 hadis** (Bukhari,
Muslim, Abu Daud, Tirmidzi, Nasai, Ibnu Majah, Ahmad, Darimi, Malik)
dengan teks Arab, terjemahan Melayu/Indonesia/English, transliterasi,
huraian SemakHadis, darjat ulama, dan carian makna (AI) — semua
berjalan **luar talian** selepas pemasangan.

---

## 1. Apa yang sudah disahkan ✅

Pengesahan terkini (17 Ogos 2026) — semua lulus pada mesin sebenar:

| Perkara | Status |
|---|---|
| Data penuh 62,169 hadis sejajar dengan sumber hadis.my | ✅ 62,169 unik, 0 duplikat, teks lengkap |
| Terjemahan Inggeris 31,833 hadis (7 kitab) | ✅ ketepatan audit 100% |
| Huraian SemakHadis 4,237 hadis (BM) + darjat 63,930 | ✅ dipapar dengan atribusi |
| Penanda buku (Tersimpan) — simpan, kekal selepas tutup, buka semula | ✅ diuji dengan data sebenar |
| Carian kata kunci + carian makna (AI) | ✅ |
| **5 tema, semua ≥ kontras WCAG AA** — 🌙 Neutral (lalai) · 📜 Kertas · ☀ Neutral terang · ☀ Terang · 🌓 Ikut sistem | ✅ galeri visual 5 tema dalam `MANUAL_PENGGUNAAN.md` §3 TEMA |
| **Paparan responsif** — kandungan betul pada sebarang saiz tetingkap dan penskalaan Windows (100%–150%) | ✅ pepijat paparan terpotong dibaiki (17 Ogos 2026) |
| Suite ujian pra-hantar 14 ujian | ✅ SEMUA LULUS |
| App berjalan pada Windows (Python 3.14) | ✅ |

Hadis tanpa huraian SemakHadis tetap dipapar lengkap (Arab +
terjemahan + transliterasi + darjat) — hanya bahagian "Huraian" yang
tiada, dengan jujur.

---

## 2. Cara menjalankan app

### Sudah dipasang

1. Klik dua kali ikon **"Hadis"** di **Desktop** atau **Start Menu**.
2. Selesai — app terbuka dalam beberapa saat (skrin pemula memapar
   kemajuan muat model carian; boleh klik untuk langkau).

### Belum dipasang (sekali sahaja, 1–3 minit)

1. Klik dua kali **`PASANG.bat`** → tunggu "SIAP" → tekan sebarang
   kekunci.
2. Klik dua kali ikon **"Hadis"** di Desktop.

### Jika ikon tidak jalan

- **`BUAT_PINTASAN.bat`** — cipta semula ikon.
- **`JALANKAN.bat`** — buka app terus tanpa ikon.
- **`NYAHPEPIJAT.bat`** — buka tetingkap diagnos yang kekal terbuka;
  salin teksnya dan hantar kepada pembangun.

### Data sudah lengkap (tiada kunci diperlukan)

- Binaan edaran membundel pangkalan data hadis lengkap (62,169 hadis).
  Buka app terus — **tiada kunci API atau muat turun data diperlukan**;
  semuanya berjalan **luar talian** selepas pemasangan.

---

## 3. Cara memulakan carian

**Cara paling mudah:**

1. Buka app → pada **skrin utama**, klik kad kitab (cth. **Sahih
   al-Bukhari**).
2. Senarai hadis dipapar (20 setiap halaman) — klik mana-mana hadis
   untuk membaca penuh.
3. Untuk lompat terus: taip nombor dalam kotak **"Lompat No. hadis"**
   (cth. `433`) lalu Enter — atau tekan **Ctrl+G**.

**Carian teks (kata kunci + makna AI serentak):**

1. Klik **Pencarian** di navigasi atas.
2. Taip perkataan — Arab, Melayu, atau Indonesia (cth. `zakat`,
   `sholat`, `الصلاة`).
3. Hasil dipapar: padanan makna (AI) dahulu, kemudian kata kunci.
   Untuk soalan, jawapan draf AI muncul di atas hasil.
4. **Lompat terus ke hadis tertentu:** taip nama kitab + nombor, cth.
   `bukhari 433` atau `B433` → Enter → butiran hadis itu dibuka
   terus.

**Pada halaman hadis:**

- Lajur kanan: tab **ARAB / TRANSLITERASI** (2 gaya rumi) — teks
  Arab asal di kanan (susunan RTL, 14 Ogos 2026).
- Lajur kiri: tab **Melayu / Indonesia / English** (terjemahan).
- Bawah terjemahan: **Huraian (SemakHadis)** jika ada + **Darjat**
  ulama.
- Bar teks **`Lapor ralat | Kongsi | Salin`** di bawah terjemahan:
  - **Lapor ralat** → buka sunnah.com untuk semakan
  - **Kongsi** → kongsi melalui WhatsApp
  - **Salin** → menu 3 pilihan: Arab sahaja · terjemahan semasa ·
    Arab + terjemahan semasa
- **⭐ Simpan** (bar tajuk) → hadis masuk halaman **Tersimpan**.
- **💬 WhatsApp** / **🔊 Dengar** / **📋 Salin** di bar tajuk untuk
  tindakan pantas.

### Tukar tema (5 pilihan)

1. Klik **⚙ gear** (penjuru kanan atas) → panel Tetapan gelongsor
   dari kanan.
2. Bahagian **TEMA** — pilih salah satu:
   - **🌙 Neutral** (lalai) — gelap neutral, kontras tertinggi
   - **📜 Kertas** — kertas hangat (gaya mushaf bercetak)
   - **☀ Neutral terang** — terang neutral (pasangan kepada Neutral)
   - **☀ Terang** — terang kertas hangat
   - **🌓 Ikut sistem** — ikut mod Windows automatik: gelap → 🌙
     Neutral, terang → ☀ Neutral terang (bertukar hampir serta-merta)
3. Semua tema lulus kontras WCAG AA (≥ 4.5:1). Perbandingan visual
   kelima-lima tema (halaman Utama + Detail) ada dalam
   `MANUAL_PENGGUNAAN.md` §3 TEMA.

**Paparan responsif:** app kini memaparkan kandungan dengan betul
pada sebarang saiz tetingkap — termasuk tetingkap kecil (1024×600)
dan penskalaan Windows 125%/150%. Sebelum ini sesetengah halaman
boleh terpotong di kanan selepas mengecilkan tetingkap; pepijat itu
telah dibaiki dan diuji penuh (17 Ogos 2026).

---

## 4. Penyelesaian masalah (ringkas)

**App tidak terbuka / ikon tiada:**

- Klik dua kali **`JALANKAN.bat`** — buka app terus tanpa ikon.
- **`BUAT_PINTASAN.bat`** — cipta semula ikon Desktop/Start Menu.
- **`NYAHPEPIJAT.bat`** — buka tetingkap diagnos yang kekal terbuka;
  salin teks dan hantar kepada pembangun.

**Data hadis tidak kelihatan:**

- Pastikan anda memasang binaan edaran rasmi (Setup EXE / Portable /
  MSIX) — ia membundel data lengkap. Jika data tiada, pasang semula
  atau hantar output `NYAHPEPIJAT.bat` kepada pembangun.

**App lambat buka:**

- Biasalah pada kali pertama setiap sesi — skrin pemula memuat model
  carian makna (AI) (~30 saat). Klik skrin pemula untuk langkau;
  carian kata kunci tetap berfungsi.

**Saiz teks / antara muka terlalu kecil atau besar:**

- ⚙ gear → **PAPARAN** — laraskan saiz antara muka, saiz teks Arab,
  saiz terjemahan, atau fon Arab serta-merta.

**Tema tidak berubah seperti dijangka:**

- Tema **🌓 Ikut sistem** mengikut mod Windows: Windows gelap → 🌙
  Neutral, Windows terang → ☀ Neutral terang. Jika nampak "tidak
  berubah", periksa mod Windows (Tetapan Windows → Peribadi → Warna).
  Tema lain (Neutral, Kertas, Neutral terang, Terang) kekal tetap
  tanpa mengira mod Windows.

**Carian tiada hasil:**

- Cuba ejaan lain atau perkataan lebih umum (cth. `zakat` dan bukan
  frasa panjang). Carian kata kunci padan perkataan tepat; carian
  makna (AI) sesuai untuk soalan.

**Masih bermasalah?** — hantar kandungan `NYAHPEPIJAT.bat` kepada
pembangun; butiran penuh dalam `MANUAL_INSTALASI.md`
§Penyelesaian masalah.

---

## 5. Rujukan & bantuan

| Perlu | Buka |
|---|---|
| Manual penuh | `MANUAL_PENGGUNAAN.md` |
| Pemasangan terperinci | `MANUAL_INSTALASI.md` |
| Langkah pertama pasang | `BACA_SAYA.txt` |
| Penyelesaian masalah penuh | `MANUAL_INSTALASI.md` §Penyelesaian masalah |
| Peta dokumen pembangunan | `MANUAL_REFERENSI_DEV.md` |
