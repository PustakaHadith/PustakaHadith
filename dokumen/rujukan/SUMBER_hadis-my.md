# Sumber: hadis.my (dan hadith.my)

**Status:** pengguna akan uruskan sendiri dengan pemilik
**Kepentingan:** sumber **teras** — 62,169 hadis, seluruh aplikasi bergantung padanya
**Dikemas kini:** 11 Ogos 2026

---

## 1. Penemuan: hadith.my = hadis.my (pemilik sama)

Disemak 11 Ogos 2026. Pautan **Contact** pada `hadith.my` menghala ke
`webmaster.my` — domain yang sama dengan `khai@webmaster.my`, alamat
sokongan rasmi hadis.my.

Menu hadith.my turut memaparkan **Qari.my** sebagai projek adik.

```
webmaster.my (En. Khai)
├── hadis.my / service.hadis.my     API, Bahasa Melayu
├── hadith.my                        laman web, Bahasa Inggeris
└── qari.my                          bacaan al-Quran
```

**Kesan:** tiada permohonan berasingan diperlukan untuk hadith.my.
Satu perbincangan dengan En. Khai merangkumi kedua-duanya.

### Perbandingan dua laman

| | hadis.my (API) | hadith.my (web) |
|---|---|---|
| Bahasa | Melayu + Indonesia + Arab | **Inggeris sahaja** |
| Kitab | 9 (termasuk Ahmad, Darimi) | 9 (tiada Ahmad/Darimi; **ada** 40 Nawawi + 40 Qudsi) |
| Bukhari | 7,008 | 7,554 |
| Capaian | API dengan kunci | web sahaja |
| `robots.txt` | — | sekat ClaudeBot, GPTBot, CCBot; `ai-input=no`, `ai-train=no` |
| Hak cipta | — | "All rights reserved" |

**Nota:** 40 Nawawi dan 40 Qudsi yang ada pada hadith.my juga wujud
dalam CDN `fawazahmed0` (Unlicense) — 91 hadis baharu selepas menolak
pertindihan. Tiada keperluan mengambil dari hadith.my.

---

## 2. Fakta rasmi (dari dokumentasi mereka)

### Semua pelan PERCUMA

| Pelan | Req/Minit | Req/Hari | Max Keys | Harga |
|---|---|---|---|---|
| Basic | 60 | 200 | 1 | Percuma |
| Personal | 120 | 1,000 | 1 | Percuma |
| Developer | 500 | 10,000 | 1 | **Percuma** |

Nota rasmi: *"Pada masa ini, semua pelan adalah percuma. Hubungi kami
jika anda memerlukan had yang lebih tinggi."*

Maka permohonan **bukan** tentang mengelak bayaran — ia tentang
menghapus langkah pendaftaran bagi pengguna awam.

### Saluran hubungan

| tujuan | alamat |
|---|---|
| **Naik taraf pelan / kuota** | `hadisapi@gmail.com` |
| Sokongan am | `khai@webmaster.my` |
| WhatsApp | +60 19-209 2006 |

Gunakan **`hadisapi@gmail.com`** untuk permohonan ini — ia berkaitan
kuota dan pengedaran, bukan sokongan teknikal.

### Endpoint & koleksi

```
Base URL : https://service.hadis.my/api/v1
Header   : X-API-Key
Portal   : https://developer.hadis.my/dashboard
```

| Koleksi | Slug | Hadis |
|---|---|---|
| Sahih Bukhari | `bukhari` | 7,008 |
| Sahih Muslim | `muslim` | 5,362 |
| Sunan Abu Dawud | `abu-daud` | 4,590 |
| Sunan Tirmidzi | `tirmidzi` | 3,891 |
| Sunan An-Nasai | `nasai` | 5,662 |
| Sunan Ibnu Majah | `ibnu-majah` | 4,332 |
| Musnad Ahmad | `ahmad` | 26,363 |
| Sunan Ad-Darimi | `darimi` | 3,367 |
| Muwatta Malik | `malik` | 1,594 |
| | | **62,169** |

---

## 3. Mengapa kunci terbenam TIDAK boleh diguna

```
Sync penuh       = 622 permintaan
Pelan Developer  = 10,000/hari
                 = ~16 pengguna sehari
```

Jika kunci ditanam dalam aplikasi dan 100 orang memasang pada hari yang
sama, kuota habis pada pengguna ke-17. Selebihnya nampak aplikasi
rosak.

Hanya dua pilihan yang berskala:

- **Bundel snapshot** — sifar permintaan API
- **Pengguna daftar sendiri** — keadaan sekarang, dan halangannya

---

## 4. Hujah terkuat: bundel MENGURANGKAN beban mereka

Sekarang setiap pengguna baharu menjana **622 permintaan**. Dengan
bundel — **sifar**.

Permohonan ini bukan meminta lebih daripada mereka. Ia menawarkan untuk
mengambil kurang, sambil memaparkan atribusi dan menghantar pembangun
lain ke portal mereka.

---

## 5. Isu berasingan: 55 hadis matn tidak diterjemah

Ditemui melalui imbasan penuh `hadis.db` (lihat
`ISU_TERJEMAHAN_MELAYU.md`).

**80 hadis** mempunyai blok Arab >=40 aksara dalam teks Melayu. Selepas
menapis **25 petikan al-Quran** (yang sengaja dikekalkan dalam Arab —
betul), tinggal **55 kes** di mana matn benar-benar tercicir.

```
malik      25       bukhari     7
tirmidzi   14       ahmad       4
darimi      4       nasai       1
```

Teks Indonesia **lengkap untuk kesemua 55** — jadi ia isu terjemahan
Melayu sahaja, bukan data yang hilang.

Kadar 0.09% menunjukkan kualiti hadis.my sebenarnya tinggi. Senarai ID
penuh ada dalam `ISU_TERJEMAHAN_MELAYU.md` §5, sedia untuk dihantar.

**Cadangan:** sertakan sebagai lampiran dalam e-mel — ia menunjukkan
niat baik dan membantu mereka membaiki sumber.

---

## 6. E-MEL

**Kepada:** hadisapi@gmail.com
**Sk:** khai@webmaster.my
**Subjek:** Permohonan kebenaran bundel data — aplikasi Pustaka Hadis (percuma, bukan komersial)

---

Assalamualaikum warahmatullah.

**Pengenalan**

Saya [NAMA], pembangun **Pustaka Hadis** — aplikasi desktop Windows
untuk membaca dan mencari hadis dalam Bahasa Melayu. Aplikasi ini
dibangunkan secara persendirian, **diedarkan percuma**, dan **tiada
unsur komersial** (tiada langganan, iklan, atau pembelian dalam
aplikasi).

API Hadis Malaysia ialah sumber utama kandungan aplikasi ini. Terima
kasih atas usaha membina dan menyelenggara perkhidmatan ini secara
percuma — ia asas kepada seluruh projek saya.

**Keadaan semasa**

Aplikasi menggunakan kesemua 9 koleksi (62,169 hadis). Setiap pengguna
perlu:

1. Melawat developer.hadis.my dan mendaftar akaun
2. Menjana kunci API sendiri
3. Memasukkan kunci ke dalam aplikasi
4. Menunggu ~12 minit untuk sync (622 permintaan pada throttle 1.1s)

**Masalahnya:** developer.hadis.my ialah portal **pembangun**. Pengguna
sasaran saya orang awam yang ingin membaca hadis — mereka tidak biasa
dengan konsep kunci API, dan ramai berhenti pada langkah ini sebelum
sempat menggunakan aplikasi.

**Kunci terbenam bukan penyelesaian**

Saya telah pertimbangkan menanam satu kunci dalam aplikasi, tetapi
matematiknya tidak menjadi:

- Sync penuh = 622 permintaan
- Pelan Developer = 10,000/hari -> hanya ~16 pengguna sehari

Jika 100 orang memasang pada hari yang sama, kuota habis dan selebihnya
akan menyangka aplikasi rosak. Saya tidak mahu membebankan
perkhidmatan tuan sedemikian.

**Permohonan**

Saya memohon kebenaran untuk **membundel snapshot data** ke dalam
pemasang aplikasi, supaya pengguna boleh memasang dan terus membaca
tanpa kunci API dan tanpa sebarang permintaan ke pelayan tuan.

Ini juga **mengurangkan beban** pada infrastruktur hadis.my berbanding
keadaan sekarang, di mana setiap pengguna baharu menjana 622
permintaan.

Saya bersedia mematuhi apa-apa syarat, termasuk:

1. **Atribusi jelas** — "Sumber data: hadis.my" pada skrin utama,
   halaman Tentang, dan setiap hadis jika dikehendaki
2. **Pautan ke developer.hadis.my** dalam aplikasi, menggalakkan
   pembangun lain menggunakan API tuan
3. **Kekerapan kemas kini snapshot** mengikut kebenaran tuan
4. **Tiada pengedaran semula** dalam bentuk lain — tiada API pesaing,
   tiada muat turun data mentah, tiada penggunaan komersial
5. **Menarik balik sepenuhnya** jika diminta pada bila-bila masa

**Jika tidak sesuai**

Saya juga terbuka kepada:

- **Kunci khas dengan kuota tinggi** untuk aplikasi ini, jika tuan
  sanggup memberikannya dan yakin infrastruktur mampu
- **Kekalkan cara semasa** — saya akan memperbaiki panduan pendaftaran
  dalam aplikasi supaya lebih mudah diikuti orang awam

**Lampiran: 55 hadis dengan terjemahan Melayu tidak lengkap**

Semasa membina aplikasi, saya menjalankan imbasan penuh ke atas 62,169
hadis dan menemui **55 hadis** (0.09%) di mana sanad diterjemah tetapi
matn kekal dalam Arab. Teks Indonesia bagi kesemuanya lengkap.

Kadar 0.09% menunjukkan kualiti terjemahan hadis.my sangat tinggi. Saya
sertakan senarai ID penuh di bawah dengan harapan ia berguna:

```
malik      : 36, 108, 109, 152, 153, 181, 190, 341, 522, 552, 556,
             572, 619, 647, 685, 701, 775, 779, 799, 806, 809, 828,
             881, 1082, 1418, 1513
bukhari    : 3459, 3477, 4413, 4604, 4935, 6236, 6990
tirmidzi   : 231, 1341, 1419, 1922, 2175, 2711, 2863, 2877, 3029,
             3031, 3073, 3116, 3120, 3270
ahmad      : 4303, 9358, 10614, 24278
darimi     : 91, 478, 2133, 2608
nasai      : 468
```

(Nota: 25 kes lain yang dikesan ialah petikan ayat al-Quran yang
sengaja dikekalkan dalam Arab — itu betul dan tidak disenaraikan.)

**Maklumat tambahan**

Aplikasi turut memaparkan huraian daripada SemakHadis.com (permohonan
berasingan sedang dibuat), darjat ulama daripada sumber domain awam,
dan mempunyai carian makna menggunakan model bahasa yang berjalan
sepenuhnya luar talian pada komputer pengguna.

Saya sedia memberikan demo, tangkapan skrin, atau salinan aplikasi
untuk semakan pihak tuan.

Terima kasih atas pertimbangan. Semoga usaha menyebarkan hadis dalam
Bahasa Melayu ini diberkati Allah SWT.

Wassalam,

[NAMA]
[E-MEL]
[TELEFON]

---

## 7. WHATSAPP (versi pendek)

**+60 19-209 2006**

> Assalamualaikum. Saya [NAMA], pembangun aplikasi desktop **Pustaka
> Hadis** — percuma, Bahasa Melayu, menggunakan API Hadis Malaysia.
>
> Saya ingin memohon kebenaran **membundel snapshot data** dalam
> pemasang aplikasi. Sebabnya: developer.hadis.my ialah portal
> pembangun, dan pengguna awam saya berhenti pada langkah daftar kunci
> API sebelum sempat guna aplikasi.
>
> Kunci terbenam tidak menjadi — sync penuh 622 permintaan, jadi pelan
> Developer hanya cukup untuk ~16 pengguna sehari.
>
> Membundel juga **mengurangkan beban** pelayan tuan berbanding
> sekarang. Saya sedia mematuhi apa-apa syarat: atribusi, pautan balik,
> atau tarik balik bila-bila diminta.
>
> Saya juga ada senarai 55 hadis yang terjemahan Melayunya tidak
> lengkap — mungkin berguna untuk pihak tuan.
>
> Boleh saya hantar butiran penuh ke hadisapi@gmail.com?
>
> Terima kasih.

---

## 8. Sebelum menghantar

**1. Isi butiran sebenar** — `[NAMA]`, `[E-MEL]`, `[TELEFON]`.

**2. Sahkan atribusi memang wujud.** E-mel menjanjikan "Sumber data:
hadis.my pada skrin utama" — semak ia ada, atau tambah dahulu.

**3. Nada.** Semua pelan percuma. Mereka menyediakan 62,169 hadis
tanpa bayaran. Mesej ini meminta izin, bukan menuntut hak.

**4. Lampiran 55 ID** ialah titik kuat — ia menunjukkan niat baik dan
memberi nilai kepada mereka, bukan hanya meminta.

**5. Simpan balasan** sebagai bukti kebenaran dalam projek.

---

## 9. Kesan kepada rancangan installer

| jawapan | kesan | saiz installer |
|---|---|---|
| **Setuju** | Klik sekali, tiada kunci API, 0 minit | ~660 MB |
| **Kunci khas** | Sync automatik; berisiko kuota habis | ~520 MB |
| **Tolak** | Kekal cara semasa; installer masih hapuskan 90% kerumitan | ~520 MB |

Walaupun ditolak, installer tetap membundel Python, PyQt5, torch, model
AI dan indeks FAISS. Hanya langkah kunci + sync kekal.

**Kerja installer berbaloi diteruskan tanpa mengira jawapan.**

---

## 10. Status

| perkara | status |
|---|---|
| E-mel | **belum dihantar** — pengguna akan uruskan sendiri |
| hadith.my | tiada tindakan berasingan (pemilik sama) |
| 55 hadis matn | senarai sedia, sertakan dalam e-mel |
| Atribusi dalam apl | **perlu disahkan wujud** sebelum hantar |
