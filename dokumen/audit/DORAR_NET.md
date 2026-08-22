# Dorar.net & sunnah.com — penilaian sumber rujukan

**Tarikh:** 10 Ogos 2026 · **disemak semula:** 11 Ogos 2026 (+sunnah.com)
**Status:** kedua-dua = pautan keluar, tiada integrasi data
**Berkaitan:** Sesi 18.8 (penilaian Dorar pertama, ditangguhkan)

---

## 1. Apa itu Dorar.net

**al-Durar al-Saniyyah** — al-Mawsu'ah al-Hadithiyyah. Pangkalan data
takhrij dan darjat hadis dalam Bahasa Arab, antara yang paling kerap
dirujuk oleh pengkaji hadis.

Kajian penggunaan laman hadis dalam kalangan pensyarah Universiti Islam
Selangor menyebut Dorar.net berulang kali sebagai rujukan utama untuk
status hadis.

---

## 2. Perbezaan penting: Dorar LEBIH TERBUKA

Ini yang membezakannya daripada semua sumber lain yang dinilai setakat
ini.

### Content-Signal dalam robots.txt

```
Content-Signal: search=yes, ai-train=no, use=reference
```

**`use=reference` ialah kebenaran eksplisit**, bukan ketiadaan
larangan. Bandingkan:

| sumber | pendirian |
|---|---|
| **dorar.net** | `use=reference` — **membenarkan rujukan** |
| semakhadis.com | sekat semua perangkak AI, tiada kelonggaran |
| hadith.my | sekat + `ai-input=no`, `ai-train=no` |
| hadithxpert.com | robots terbuka tetapi produk **berbayar** |

Nota: Dorar tetap menyekat `ClaudeBot`, `GPTBot`, `CCBot`, dan
`ai-train=no`. Kebenaran itu untuk **rujukan**, bukan latihan model.

### Widget rasmi untuk pemilik laman

Halaman `dorar.net/article/2107` menawarkan widget carian percuma
kepada pemilik laman web dan forum. Ringkasan kandungannya:

- Widget boleh diletak di mana-mana dalam laman anda
- Tujuan: pelawat boleh mengesahkan kesahihan hadis **sebelum
  menyebarkannya**
- Pemasangan mengambil beberapa minit, tidak menjejaskan prestasi laman
- Perkhidmatan **percuma** untuk pemilik laman dan forum
- Hubungan: `dorar@dorar.net`
- Mereka **meminta pemberitahuan** jika widget berjaya dipasang

Nada halaman itu jelas: mereka mahu ia digunakan dan tersebar.

---

## 3. Status teknikal API (diuji 10 Ogos 2026)

```
Endpoint : https://dorar.net/dorar_api.json?skey=<teks arab>
```

| ujian | keputusan |
|---|---|
| User-Agent `ClaudeBot` | **403 Forbidden** |
| User-Agent pelayar biasa | **200 OK**, JSON dikembalikan |

API **masih hidup**. Penolakan sebelum ini disebabkan penapisan
perangkak AI, bukan perkhidmatan mati.

Format respons: objek JSON dengan kunci `ahadith.result` yang
mengandungi HTML — teks hadis, perawi, darjat, dan sumber takhrij.

---

## 4. Tiga pilihan penggunaan

### A. Butang "Semak di Dorar.net" — DISYORKAN

Buka pelayar dengan teks Arab hadis sebagai pertanyaan carian.

| aspek | penilaian |
|---|---|
| Data disimpan | tiada |
| Padanan diperlukan | tiada — pengguna lihat sendiri |
| Isu lesen | tiada; sejajar `use=reference` |
| Liputan | penuh (Dorar cari sendiri) |
| Risiko padanan salah | **sifar** |
| Kerja | rendah — satu butang |

Sejajar dengan semangat widget rasmi mereka: alat pengesahan untuk
pengguna, bukan pengekstrakan data.

### B. Panggilan API atas permintaan

Pengguna klik → apl panggil `dorar_api.json` → papar darjat + atribusi.

- Perlu `User-Agent` biasa (bukan pengecam bot)
- **Melanggar prinsip luar talian** aplikasi
- Menambah kebergantungan rangkaian pada ciri yang sepatutnya tempatan
- Jika Dorar mengubah API atau menyekat, ciri itu mati senyap

### C. Muat turun pukal ke DB — JANGAN, buat masa ini

Ditangguhkan dalam Sesi 18.8 atas tiga sebab yang **diukur**, dan
kesemuanya masih sah — lihat [nota kaki](#nota-kaki-alasan-penangguhan-sesi-188).

Tambahan pula: `use=reference` mungkin **tidak merangkumi** penyimpanan
pukal untuk diedarkan bersama aplikasi. Rujukan berbeza daripada
pengedaran semula.

Jika hendak diteruskan kelak:

1. Selesaikan ketepatan padanan dahulu (ambang J >= 0.55, tolak calon
   kedua yang rapat)
2. E-mel `dorar@dorar.net` untuk pengesahan bertulis
3. Terima liputan separa — jangan paksa padanan untuk menutup jurang

---

## 4b. sunnah.com — disemak 11 Ogos 2026

### Dapatan

| perkara | keputusan |
|---|---|
| `robots.txt` | `Disallow: /selectiondata/*` sahaja — **tiada Content-Signal** |
| `api.sunnah.com/v1/collections` | **403** walaupun User-Agent pelayar |
| `sunnah.com/developers` | **403** — halaman pendaftaran disekat |
| Repo `sunnah-com/api` | **tiada lesen** (`license: null`), 490 bintang, aktif |

### Perbezaan penting dengan Dorar

```
dorar.net    Content-Signal: use=reference    <- kebenaran EKSPLISIT
sunnah.com   (tiada Content-Signal)            <- tiada kenyataan
```

`robots.txt` sunnah.com sangat longgar — hampir semua dibenarkan untuk
perangkak. Tetapi itu tentang **pengindeksan**, bukan penggunaan semula
data.

**Ketiadaan larangan bukan kebenaran.** Dorar menyatakan pendirian
mereka; sunnah.com tidak. Ditambah API tertutup (403 tanpa laluan
pendaftaran yang boleh dicapai) dan repo tanpa lesen — kedua-duanya
menunjukkan akses dikawal secara sengaja.

### Repo GitHub — apa ia sebenarnya

`github.com/sunnah-com/api` ialah **kod pelayan** (Flask + MySQL +
Docker), bukan data hadis. Folder `db/` mengandungi satu fail sampel
1.4 MB untuk pembangunan tempatan — bukan 30,000+ hadis mereka.

Nilai rujukan: **skema pangkalan data** mereka menunjukkan cara mereka
memodelkan koleksi, kitab, bab, hadis, dan sistem rujukan berganda.
Membaca skema untuk memahami reka bentuk berbeza daripada menyalin kod.

### Data mereka SUDAH ada dalam aplikasi

```
31,833 terjemahan Inggeris (51%)
audit saksi bebas: 30,541 disahkan, 0 salah
```

Melalui CDN `fawazahmed0` (domain awam, **atribusi wajib** — sudah
dalam deklarasi). Terjemahan itu berasal daripada sunnah.com.

Maka API rasmi **tidak menambah kandungan** yang belum ada. Ia hanya
menambah kebergantungan rangkaian pada aplikasi luar talian, plus satu
lagi soal lesen.

### Keputusan

**Jangan kejar API sunnah.com.** Tiga sebab: 403 tanpa laluan
pendaftaran, tiada lesen, dan kandungannya sudah dimiliki.

**Pautan keluar dibenarkan** — sama seperti Dorar. Butang membuka
`sunnah.com/bukhari:1` bagi hadis yang sedang dibaca.

Nilai untuk pengguna: sanad **boleh diklik** (setiap perawi memaut ke
profilnya), susunan Kitab -> Bab dengan tajuk dwibahasa, dan tiga
sistem rujukan serentak (termasuk penomboran lama yang ditandakan
*deprecated* tetapi tetap dipapar).

Itu ciri yang dikagumi tetapi tidak praktikal dibina sendiri — sanad
boleh-klik memerlukan pangkalan data perawi yang aplikasi ini tiada.

---

## 5. Cadangan

**Laksana Pilihan A.** Ia melengkapkan corak pautan keluar yang sudah
dirancang:

```
Hadis palsu (BM)          -> SemakHadis.com
Jawapan ulama bertauliah  -> HadithXpert
Takhrij & darjat (Arab)   -> Dorar.net
Sanad & rujukan silang    -> sunnah.com
```

Setiap satu untuk audiens berbeza. Aplikasi kekal sebagai ensiklopedia
sembilan kitab tanpa terbeban dengan tugasan luar skop.

Dorar khususnya sesuai untuk **pelajar dan pengkaji** — yang dinyatakan
sebagai pengguna sasaran dalam deklarasi.

### Cadangan pelaksanaan

Butang pada halaman hadis, bersebelahan butang sedia ada:

```
[ Salin ]  [ Kongsi ]  [ Simpan ]  [ Rujukan luar v ]
```

Menu jatuh `Rujukan luar` mengelakkan bar butang jadi sesak:

| item | URL |
|---|---|
| Semak takhrij (Dorar.net) | `dorar.net/hadith/search?q=<matn>` |
| Lihat di sunnah.com | `sunnah.com/<slug>:<no>` |
| Semak hadis palsu (SemakHadis) | `semakhadis.com/?s=<kata kunci>` |

**Dorar** — gunakan **matn** (sanad dibuang);
`core/sema_source.py::_matn()` sudah melakukan ini. Sanad panjang
mengelirukan enjin carian mereka.

**sunnah.com** — perlu peta slug (`abu-daud` -> `abudawud`,
`tirmidzi` -> `tirmidhi`, `ibnu-majah` -> `ibnmajah`). Peta itu sudah
wujud sebagai `PETA_KITAB` dalam `core/eng_source.py`.

Amaran: penomboran hadis.my dan sunnah.com **tidak selalu sepadan**
(Malik: 1,594 vs 1,858). Pautan mungkin membawa ke hadis yang berbeza.
Untuk kitab yang penomborannya menyimpang, lebih selamat pautkan ke
**carian** dan bukan nombor terus.

Buka dalam pelayar luar: `QDesktopServices.openUrl(QUrl(...))`.

---

## 6. Nota: adakah SemakHadis menggunakan API Dorar?

Hipotesis ini disemak pada 10 Ogos 2026. **Bukti tidak menyokongnya.**

Medan `sources` dalam API SemakHadis (sampel 25 rekod, carian "niat")
menunjukkan sitasi **kitab bercetak** dengan butiran akademik penuh:

```
10x  al-Albani & Mashhur Hasan, Silsilah al-Ahadith al-Da'ifah (2010)
 6x  al-Azami, Talkhis al-Jami' al-Kamil (2022)
 3x  Mulla Ali al-Qari, al-Masnu' fi Ma'rifat al-Hadith al-Mawdu' (1398H)
 2x  al-Ghumari, al-Mughir 'ala al-Ahadith al-Mawdu'ah (2015)
 2x  al-'Amiri, al-Jadd al-Hathith
```

Setiap satu dengan penyunting, penerbit, tahun, dan edisi. Ditambah
medan `researchers` yang menamakan individu (cth. Dr. Nur Afifi Bin
Alit) dan merujuk disertasi kedoktoran USIM.

**Mengapa tanggapan itu mungkin timbul:**

1. **Istilah darjat sama** — *Palsu, Batil, Munkar, Daif, Tidak
   ditemui* ialah terjemahan istilah mustalah hadis standard
   (`موضوع`, `باطل`, `منكر`, `لا أصل له`). Kesamaan kerana kedua-duanya
   mengikut istilah yang sama, bukan kerana perkongsian data.

2. **Sumber asal sama** — kedua-duanya merujuk al-Albani secara meluas.
   Hadis yang sama akan mendapat darjat yang sama daripada kedua-duanya.

**Kesan:** permohonan lesen kepada SemakHadis kekal perlu dan sah.
Mereka melakukan kerja penyelidikan asal — membaca kitab, menyitasi
halaman, menterjemah ke Bahasa Melayu.

---

## 7. Ringkasan status sumber luar

| sumber | integrasi | lesen | tindakan |
|---|---|---|---|
| hadis.my / hadith.my | data teras (62,169) | pengguna uruskan sendiri | `SUMBER_hadis-my.md` |
| fawazahmed0 CDN | 31,833 eng + darjat | domain awam | atribusi |
| SemakHadis | 4,237 huraian | **menunggu** | `SUMBER_semakhadis.md` |
| HadeethEnc | 280 (tidak dipapar) | jelas, 3 syarat | sandaran |
| **Dorar.net** | **tiada** | **`use=reference`** | **pautan keluar** |
| **sunnah.com** | via CDN sahaja | tiada kenyataan; API 403 | **pautan keluar** |
| Fath al-Bari | dibatalkan | CC BY-NC-SA | — |
| Irsyad al-Hadith | ditutup | hak cipta terpelihara | — |

Dorar ialah satu-satunya sumber dengan **kebenaran rujukan eksplisit**.
sunnah.com tiada kenyataan — pautan keluar selamat, integrasi data
tidak.

---

## Nota kaki: alasan penangguhan Sesi 18.8

Rujukan untuk Pilihan C (§4). Ketiga-tiga alasan **diukur**, bukan
diandaikan.

### 1. Liputan rendah

Sampel padanan mengikut kitab:

```
Bukhari     50%        Ibn Majah   40%
Muslim      50%        Ahmad       30%
Nasai       35%        lain-lain   <=15%
```

Separuh koleksi terbesar tidak berpadanan. Untuk kitab kecil, liputan
jatuh ke bawah 15%.

### 2. Padanan boleh SALAH

Bukhari #50 memberi Jaccard **0.32** dan memadan hadis yang **berbeza
sama sekali**.

Ini corak yang sama seperti kegagalan lapisan `kata` (35.3% positif
palsu) dan Fath al-Bari (penomboran hanyut): sanad yang dikongsi
menghasilkan skor tinggi walaupun matn berlainan.

**Memaparkan darjat yang salah lebih buruk daripada tiada darjat.**
Pengguna yang melihat "Sahih" pada hadis yang sebenarnya daif tidak
mempunyai cara mengesan ralat itu.

### 3. Kos muat turun

Anggaran **8-12 jam** untuk ~14,000 rekod pada throttle yang sopan.

### Nilai yang ditawarkan (jika masalah di atas diselesaikan)

Mengisi jurang darjat untuk `bukhari`, `muslim`, `ahmad`, dan `darimi`
— keempat-empatnya mempunyai **0%** darjat dalam sumber `fawazahmed0`.

Itu jurang sebenar. Tetapi ia tidak berbaloi diisi dengan data yang
mungkin salah.
