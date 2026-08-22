# Manual Penggunaan — PustakaHadith v1.0

> Panduan menggunakan aplikasi PustakaHadith.
> Bahasa: Melayu · Untuk pengguna aplikasi.

---

## Mengenai PustakaHadith

PustakaHadith ialah aplikasi membaca dan mencari hadis daripada
**9 kitab utama** (kutub al-tis'ah) — **62,169 hadis** dengan teks Arab
berbaris penuh, terjemahan Melayu & Indonesia, transliterasi, darjat
ulama, huraian ringkas, dan carian makna (AI).

| Kitab | Bilangan hadis |
|---|---|
| Sahih al-Bukhari | 7,563 |
| Sahih Muslim | 7,563 |
| Sunan Abu Daud | 5,274 |
| Jami' al-Tirmizi | 3,998 |
| Sunan al-Nasa'i | 5,765 |
| Sunan Ibnu Majah | 4,343 |
| Musnad Ahmad | 26,363 |
| Sunan al-Darimi | 3,350 |
| Muwatta' Malik | 1,858 |

*(jumlah sebenar mengikut penomboran sumber)*

---

## Skrin Utama

- **Bar carian** — di tengah skrin utama. Taip soalan atau kata kunci.
- **Senarai kitab** — 9 kad kitab; klik untuk masuk.
- **Ikon gear (⚙)** — atas kanan: panel Tetapan.
- **Ikon bintang** — buka senarai penanda halaman anda.
- **Ikon dadu (⚄)** — hadis rawak.

---

## Mencari Hadis

### Carian kata kunci

1. Taip perkataan di bar carian (contoh: `puasa`, `zakat`, `niat`).
2. Hasil dipapar sebagai kad — klik kad untuk baca penuh.

Carian boleh ditapis ikut kitab melalui senarai pilihan di atas kotak
carian.

### Carian makna (AI)

Taip soalan penuh seperti:

- `hukum riba dalam islam`
- `kelebihan puasa ramadhan`
- `cara bertaubat dari dosa`

Aplikasi memadankan hadis **ikut maksud**, bukan sekadar perkataan
sama. Ia berguna apabila kata kunci anda berbeza daripada perkataan
tepat dalam teks hadis. Hasil carian makna dipapar di bawah hasil kata
kunci, dengan skor padanan.

### Lompat terus ke hadis

Taip nombor atau gabungan kitab+nombor di bar carian:

| Taip | Kesan |
|---|---|
| `433` | Buka hadis nombor 433 (carian automatik) |
| `bukhari 433` | Buka kitab Bukhari pada hadis 433 |
| `B433` / `b:433` | Sama seperti di atas |
| `Ctrl+G` | Kotak "Lompat No. hadis" pada halaman kitab |

---

## Membaca Hadis

Setiap hadis dipapar dalam **dua lajur**:

- **Kanan (lajur Arab):** teks Arab penuh dengan tab **Arab |
  Transliterasi** (dua gaya bacaan rumi).
- **Kiri (lajur terjemahan):** tab **Melayu | Indonesia | English**.

Di bawah teks:

- **Transliterasi (bacaan rumi)** — boleh kembang, di belakang tajuk
  klik.
- **Darjat ulama** — penilaian Sahih/Hasan/Da'if mengikut ulama
  (dipapar mentah tanpa tafsiran).
- **Huraian ringkas** — daripada SemakHadis.com (atribusi dipapar).
- **Syarah** — tambahan rujukan Arab.

### Bar tindakan di bawah terjemahan

| Butang | Fungsi |
|---|---|
| **Lapor ralat** | Buka halaman laporan di sunnah.com |
| **Kongsi** | Kongsi ke WhatsApp (ikut bahasa semasa) |
| **Salin** | Menu 3 pilihan: Arab sahaja / terjemahan semasa / Arab + terjemahan |
| **💬 WhatsApp** | Kongsi terus ke WhatsApp |
| **🔊 Dengar** | Baca teks dengan suara (TTS) |

**Navigasi:** butang **‹ No. sebelumnya** / **No. seterusnya ›** untuk
hadis jiran dalam kitab. **Kembali** untuk kembali ke senarai.

---

## Penanda Halaman (Bookmark)

1. Buka mana-mana hadis.
2. Klik ikon **bintang/Simpan** — hadis disimpan.
3. Buka senarai penanda halaman melalui ikon bintang di skrin utama.
4. Klik hadis untuk membuka semula; klik bintang sekali lagi untuk
   buang.

Penanda halaman disimpan dalam fail `bookmarks.json` di folder data
anda — kekal selepas aplikasi ditutup atau dikemas kini.

---

## Tetapan

Klik ikon **gear (⚙)** di penjuru atas kanan.

### Paparan

| Tetapan | Fungsi |
|---|---|
| **Tema** | Gelap / Terang / Neutral gelap / Neutral terang |
| **Fon Arab** | Pilih fon Arab yang sesuai |
| **Saiz Arab** | Saiz teks Arab |
| **Saiz terjemahan** | Saiz teks terjemahan |
| **Saiz antara muka** | Saiz keseluruhan aplikasi |
| **Hadis per halaman** | Bilangan kad dalam satu halaman senarai |

### Bacaan

| Tetapan | Fungsi |
|---|---|
| **Bahasa dimuat** | Bahasa terjemahan yang dimuat/disimpan |
| **Transliterasi** | Papar / sembunyikan bacaan rumi |

### Sambungan

| Tetapan | Fungsi |
|---|---|
| **Tetapan API** | Masukkan/uji kunci API hadis.my (https://hadis.my) |
| **Mod** | Paparan mod dalam talian / luar talian semasa |

> Kunci API dilindungi: kelihatan bertopeng, perlu "Buka Kunci" untuk
> mengubah, dengan pengesahan.

---

## Mod Luar Talian

Selepas data hadis dimuat turun (selepas kali pertama), aplikasi boleh
digunakan **tanpa internet**. Carian kata kunci, membaca hadis, penanda
halaman dan tema semua berfungsi. Carian makna (AI) juga berjalan
setempat kerana model sudah dimuat semasa pemasangan.

---

## Petua

- Model carian makna dimuat pada kali pertama dibuka — jangan tutup
  aplikasi sebelum skrin pemula selesai (atau klik skrin pemula untuk
  melangkau).
- Untuk hasil carian terbaik, taip soalan penuh, bukan satu perkataan.
- Simpan hadis yang kerap dirujuk ke penanda halaman.
- Data anda selamat — nyahpasang tidak memadam folder data
  (`%LOCALAPPDATA%\PustakaHadis`).

---

## Masalah Lazim

| Masalah | Penyelesaian |
|---|---|
| Aplikasi lambat buka | Kali pertama sahaja; larian seterusnya laju. |
| Tiada hasil carian kata kunci | Cuba soalan penuh untuk carian makna (AI). |
| Tab English kelabu | Tidak disertakan dalam binaan edaran buat masa ini (menunggu lesen). |
| Ralat sambungan | Semak internet; hadis yang dimuat masih boleh dicari. |

---

## Sumber dan Atribusi

- **Teks hadis, terjemahan Melayu & Indonesia:** hadis.my — API Hadis
  Malaysia (https://hadis.my)
- **Darjat ulama:** koleksi `fawazahmed0/hadith-api` (domain awam),
  berasal daripada sunnah.com
- **Huraian ringkas:** SemakHadis.com — atribusi dipaparkan pada setiap
  huraian
- **Carian makna (AI):** model `intfloat/multilingual-e5-small`

---

*Dokumen: `dokumen/MANUAL_PENGGUNAAN.md` · Folder binaan installer ·
Versi: 1.0 · 20 Ogos 2026*