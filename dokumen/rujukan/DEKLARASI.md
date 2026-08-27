# Deklarasi Pustaka Hadith

**Versi:** 1.0 (rasmi)
**Tarikh:** 8 Ogos 2026
**Guna:** teks untuk skrin permulaan (sekali) + halaman Tentang (kekal)

---

## Mengapa ini perlu

Pengguna perlu tahu **apa aplikasi ini** dan **apa ia bukan** sebelum
menggunakannya. Untuk bahan agama, jangkaan yang salah lebih merbahaya
daripada ciri yang kurang.

Ia juga melindungi skop: apabila pengguna meminta ciri di luar bidang
(semak hadis palsu, fatwa, takhrij), deklarasi ini menjadi rujukan.

---

## TEKS PENDEK — skrin permulaan

Papar **sekali** pada larian pertama, dengan butang "Faham".

---

### Pustaka Hadith

**Rujukan digital 9 kitab hadis dalam Bahasa Melayu**

Aplikasi ini menghimpunkan **62,169 hadis** daripada sembilan kitab
utama — Bukhari, Muslim, Abu Daud, Tirmidzi, An-Nasa'i, Ibnu Majah,
Ahmad, Ad-Darimi, dan Muwatta Malik — lengkap dengan teks Arab,
terjemahan, transliterasi, dan carian.

Ia dibina untuk **pelajar, pengkaji, peminat hadis, dan pengguna awam**
yang mahu merujuk hadis dengan cepat.

**Aplikasi ini BUKAN:**

- **Bukan sumber fatwa.** Ia tidak memberi hukum. Untuk keputusan
  agama, rujuk ulama bertauliah.
- **Bukan alat semakan hadis palsu.** Ia memaparkan hadis daripada
  sembilan kitab tersebut sahaja. Untuk menyemak hadis yang beredar di
  media sosial, gunakan **SemakHadis.com** (pautan disediakan dalam
  aplikasi).
- **Bukan pengganti guru.** Memahami hadis memerlukan ilmu alat —
  konteks, sanad, dan kaedah usul. Aplikasi hanya menyediakan teks.

**Tentang darjat hadis:** penilaian yang dipaparkan datang daripada
ulama hadis moden. **Ulama boleh berbeza pendapat** tentang hadis yang
sama. Aplikasi memaparkan setiap penilaian sebagaimana adanya, tanpa
memilih antara mereka.

*[ Faham ]*

---

## TEKS PENUH — halaman Tentang

---

### Tentang Pustaka Hadith

**Versi 1.0** — aplikasi desktop percuma, berjalan sepenuhnya luar
talian.

#### Tujuan

Menyediakan rujukan hadis yang **pantas, lengkap, dan boleh dipercayai**
dalam Bahasa Melayu untuk pelajar, pengkaji, peminat hadis, dan
pengguna awam.

#### Kandungan

| Perkara | Butiran |
|---|---|
| Hadis | 62,169 daripada 9 kitab (kutub al-tis'ah) |
| Teks Arab | penuh dengan tashkeel |
| Terjemahan Melayu | 62,169 (100%) |
| Terjemahan Indonesia | 62,169 (100%) |
| Terjemahan Inggeris | 31,833 (51%) |
| Huraian ringkas | 4,237 hadis |
| Darjat ulama | mengikut ketersediaan sumber |
| Transliterasi | dijana automatik |
| Carian | kata kunci + carian makna |

#### Sumber dan atribusi

**Teks hadis, terjemahan Melayu & Indonesia:** [hadis.my](https://hadis.my) — API Hadis Malaysia

**Terjemahan Inggeris & darjat ulama:** koleksi `fawazahmed0/hadith-api` (domain awam), berasal daripada sunnah.com

**Huraian ringkas:** [SemakHadis.com](https://semakhadis.com) — dipaparkan tanpa sebarang pengubahsuaian, dengan atribusi pada setiap huraian

Ucapan terima kasih kepada semua pihak di atas. Tanpa kerja mereka,
aplikasi ini tidak wujud.

#### Batasan — sila baca

**Bukan sumber fatwa.** Aplikasi memaparkan teks hadis dan penilaian
ulama. Ia **tidak** memberi hukum, tidak menjawab persoalan fiqh, dan
tidak boleh dijadikan asas keputusan agama. Rujuk ulama bertauliah.

**Bukan alat semakan hadis palsu.** Aplikasi ini terhad kepada sembilan
kitab hadis yang disebut. Hadis yang beredar melalui WhatsApp, media
sosial, atau ceramah **mungkin tidak** berasal daripada kitab-kitab ini.
Untuk menyemaknya, gunakan **SemakHadis.com** — pangkalan data khusus
hadis daif dan palsu dalam Bahasa Melayu.

**Darjat hadis: ulama berbeza pendapat.** Satu hadis boleh dinilai
*sahih* oleh seorang ulama dan *daif* oleh yang lain. Aplikasi
memaparkan **setiap penilaian sebagaimana adanya** dan tidak memilih
antara mereka — pemilihan (tarjih) adalah kerja ulama, bukan
perisian.

**Carian makna dijana mesin.** Ciri "Carian Makna" menggunakan model
bahasa untuk mencari hadis mengikut maksud soalan. Ia alat **carian**,
bukan tafsiran. Hasilnya perlu disemak sendiri.

**Terjemahan mungkin tidak lengkap.** Sebilangan kecil hadis mempunyai
terjemahan yang tidak menyeluruh dalam sumber asal. Bandingkan dengan
teks Arab jika ragu.

#### Sokongan

Aplikasi ini percuma dan akan kekal percuma. Penyelenggaraan bergantung
kepada sumbangan sukarela.

*[ Butang: Infak ]*  ·  *[ Butang: Laporkan Masalah ]*

---

## Nota pelaksanaan

**Skrin permulaan**

- Papar **sekali** sahaja — simpan bendera dalam `user_settings.json`
  (cth. `"deklarasi_dibaca": true`)
- Butang "Faham" sahaja; jangan paksa skrol atau kotak semak
- Boleh dibuka semula dari halaman Tentang

**Halaman Tentang**

- Bahagian **Batasan** jangan disembunyikan dalam `Collapsible` —
  itu maklumat yang pengguna perlu nampak
- Pautan SemakHadis.com buka dalam pelayar luar
  (`QDesktopServices.openUrl`)

**Pautan carian hadis palsu**

Selain dalam Tentang, letak juga di halaman Carian apabila **tiada
hasil** ditemui:

> Tiada hadis sepadan dalam 9 kitab ini.
> Hadis yang anda cari mungkin bukan daripada koleksi ini —
> [semak di SemakHadis.com]

Ini paling berguna tepat pada masanya: pengguna yang mencari hadis
WhatsApp dan tidak menjumpainya, kemungkinan besar mencari hadis yang
memang tiada asal.

---

## Kedudukan berbanding platform lain

Untuk rujukan dalaman — bukan untuk dipapar dalam aplikasi.

| | Pustaka Hadith | sunnah.com | SemakHadis | HadithXpert | MyHadith |
|---|---|---|---|---|---|
| Fokus | ensiklopedia 9 kitab | ensiklopedia luas | hadis daif/palsu | jawapan ulama | hadis pilihan |
| Saiz kandungan | 62,169 hadis | 20+ koleksi | 8,000+ semakan | ~48 semakan | terhad |
| Bahasa Melayu | ✅ | ❌ | ✅ | ✅ | ✅ |
| Luar talian | ✅ | ❌ | ❌ | ❌ | ❌ |
| Carian makna (AI) | ✅ e5-small + FAISS | ❌ (Lucene) | ❌ | ✅ AI + semakan ulama | ❌ |
| Darjat/penilaian | ⚠️ dari sumber, bukan panel sendiri | ⚠️ sebahagian | ✅ 340 pengkaji | ✅ Sarjana Hadis | ✅ JAKIM |
| Harga | percuma | percuma | percuma | **RM19/bulan** | percuma |

Ruang yang diisi: **ensiklopedia 9 kitab, Bahasa Melayu, luar talian,
dengan carian makna.** Tiada platform lain menawarkan kombinasi ini.

**Nota dua lajur AI:** aplikasi ini dan HadithXpert kedua-duanya guna
AI, tetapi untuk kerja yang berbeza:

| | soalan yang dijawab AI |
|---|---|
| Pustaka Hadith | *hadis mana yang berkaitan dengan soalan ini?* |
| HadithXpert | *apakah status hadis ini, dan mengapa?* |

Yang pertama ialah **retrieval** — mencari dokumen yang sudah ada.
Yang kedua ialah **penilaian** — dan output AI mereka disemak semula
oleh ulama sebelum diterbitkan.

Perbezaan ini penting: carian makna tidak memerlukan kelayakan syarak
kerana ia tidak membuat sebarang penilaian. Ia hanya mencari.

### Mereka BUKAN pesaing

Setiap platform menjawab soalan yang berbeza:

```
"Apa bunyi hadis ini?"          -> Pustaka Hadith
"Hadis WhatsApp ini betul?"     -> SemakHadis.com
"Apa hukumnya? Kenapa daif?"    -> HadithXpert
```

**HadithXpert** khususnya patut difahami betul. Mereka **tidak** menjual
saiz koleksi — 48 semakan berbanding 62,169 hadis. Mereka menjual
**jawapan bertauliah**: setiap semakan disemak Ust. Syihabudin Ahmad
(BA Syariah al-Azhar, Sarjana Hadis USM), lengkap dengan petikan ulama
klasik dan nombor halaman.

Itu memerlukan kelayakan syarak, bukan perisian. Aplikasi ini tidak
boleh — dan tidak sepatutnya cuba — menggantikannya.

Sebaliknya, mereka juga tidak boleh menjadi ensiklopedia. Membina
62,169 hadis dengan carian luar talian ialah kerja jenis lain.

### Kesan pada reka bentuk

Kefahaman ini menyokong keputusan yang sudah dibuat:

- **Tiada takhrij AI** — itu kerja HadithXpert, memerlukan ulama
- **Tiada tarjih darjat** — papar semua penilaian, jangan pilih
- **Tiada pangkalan hadis palsu** — pautan ke SemakHadis
- **Tiada fatwa** — nyatakan dalam deklarasi

Menyenaraikan platform lain dalam aplikasi **menguatkan** kepercayaan,
bukan melemahkannya. Ia menunjukkan pemaju faham had sendiri.
