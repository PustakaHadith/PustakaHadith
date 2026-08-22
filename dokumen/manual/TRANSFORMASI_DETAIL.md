# Transformasi Paparan Detail — Lama kepada Baharu (Sesi 55)

Dokumen ini merakam **perubahan reka bentuk halaman detail hadis** daripada
susun atur lama (sebelum Sesi 55) kepada susun atur baharu yang dilaksanakan
pada 11–12 Ogos 2026. Semua keputusan datang daripada perbandingan tiga mockup
HTML (`mockup/mockup_bukhari1.html`, `mockup_nasai2117.html`,
`mockup_abudaud4177.html`, `mockup_ibnumajah2094.html`) dan dikunci oleh ujian
visual (rujuk bahagian [Pengesahan](#pengesahan)).

> **KEMASKINI 14 Ogos 2026 — susunan RTL:** lajur dua tab telah DICERMINKAN —
> teks Arab asal kini di lajur **KANAN** (aliran baca kanan-ke-kiri) dan
> terjemahan di lajur **KIRI**, demi menghormati status hadis rujukan. Semua
> rujukan "Arab kiri / terjemahan kanan" di bawah menggambarkan susunan asal
> Sesi 55; keadaan semasa ialah Arab kanan, terjemahan kiri.

Hadis rujukan di bawah ialah **Sunan An-Nasai No. 4934** — hadis yang sama
ditangkap sebelum dan selepas transformasi, supaya perbandingan adil.

---

## 1. Tangkapan skrin

### Tema gelap

| Paparan LAMA (7 Ogos 2026) | Paparan BARU (12 Ogos 2026) |
|---|---|
| ![Lama gelap](imej/lama_detail_gelap_nasai4934.png) | ![Baru gelap](imej/baru_detail_gelap_nasai4934.png) |

### Tema terang

| Paparan LAMA (7 Ogos 2026) | Paparan BARU (12 Ogos 2026) |
|---|---|
| ![Lama terang](imej/lama_detail_terang_nasai4934.png) | ![Baru terang](imej/baru_detail_terang_nasai4934.png) |

> Sumber tangkapan: `bukti_visual/gelap_nasai_4934.png` dan
> `bukti_visual/terang_nasai_4934.png` (lama, 7 Ogos — sebelum transformasi);
> `dokumen/imej/baru_detail_*.png` (baharu, 12 Ogos — tangkapan penuh halaman
> widget app sebenar, bukan mockup).

### Kes tambahan (paparan baharu)

**Kes darjat kosong** — Sahih al-Bukhari No. 1 tiada penilaian ulama;
paparan baharu memaparkan mesej jujur "Tiada penilaian ulama" (keputusan
Sesi 55 #9):

![Bukhari 1 — darjat kosong](imej/baru_detail_gelap_bukhari1.png)

**Hadis discroll ke bawah** — viewport sebenar Sunan An-Nasai No. 2117
discroll ke hujung; bahagian Penilaian ulama TERBUKA (baris "Nama — Darjat")
kelihatan tanpa klik:

![Nasai 2117 — discroll ke bawah](imej/baru_detail_gelap_skrol_nasai2117.png)

**Cip pastel tema terang** — cip klasifikasi dalam bahagian Huraian (tema
erang; latar pastel + teks pekat):

| Cip hijau (Muttafaq 'alayh — nasai#2117) | Cip merah (Palsu — abu-daud#4177) | Cip amber (Lemah — ibnu-majah#2094) |
|---|---|---|
| ![Cip hijau](imej/baru_detail_terang_cip_hijau_nasai2117.png) | ![Cip merah](imej/baru_detail_terang_cip_merah_abudaud4177.png) | ![Cip amber](imej/baru_detail_terang_cip_amber_ibnumajah2094.png) |

---

## 2. Perbandingan ringkas

| Aspek | LAMA (sebelum Sesi 55) | BARU (Sesi 55) |
|---|---|---|
| **Susun atur utama** | Satu lajur menegak: Arab di atas, terjemahan di bawah | **Dua lajur sebelah-menyebelah**: Arab di kanan, terjemahan di kiri pada baris yang sama (susunan RTL, 14 Ogos) |
| **Tab transliterasi** | Collapsible berasingan "Transliterasi (bacaan rumi)" di bawah kad Arab | **Tab ARAB / TRANSLITERASI** dalam lajur kanan; transliterasi dua gaya (GAYA MELAYU + AKADEMIK) |
| **Tab bahasa** | LangTabs global satu bar di atas kotak terjemahan | **Tab MELAYU / INDONESIA / ENGLISH** dalam lajur terjemahan |
| **Bahagian Huraian** | Collapsible terbuka (kekal) | Terbuka + **cip klasifikasi berwarna ikut makna** |
| **Penilaian ulama (darjat)** | Collapsible **tertutup** lalai (keputusan Sesi 14) | **Terbuka** lalai + papar mentah (baris "Nama — Darjat") + penafian ulama moden |
| **Cip warna ikut makna** | Tiada | Muttafaq 'alayh/Sahih/Hasan → **hijau**; Palsu/Munkar → **merah**; Lemah/Daif → **amber** |
| **Palet** | TEAL biru `#7FC4DE`, latar tidak kertas hangat | **Palet kertas hangat**: `#F4F1EA` (terang) / `#1E1D1A` (gelap), TEAL hijau `#5CBF85` |
| **Nama kitab** | Ejaan lama | Ejaan rasmi "Sahih al-Bukhari" + prefix **"Bab:"** pada baris bab |
| **Tindakan (WhatsApp/Salin/Dengar/Simpan)** | Di baris tajuk | Kekal di baris tajuk (baris yang sama, tidak lagi di bawah kad) |

---

## 3. Butiran setiap perubahan

### 3.1 Susun atur dua lajur (keputusan utama)

**Lama**: keseluruhan halaman ialah satu `QVBoxLayout` menegak — breadcrumb,
tajuk, bab, kad Arab lebar penuh, transliterasi, tab bahasa, kotak terjemahan,
huraian, syarah, penilaian. Pengguna terpaksa skrol jauh untuk membandingkan
teks Arab dengan terjemahan.

**Baharu**: panel `QFrame` dengan `QHBoxLayout` dua lajur. Lajur kanan
membawa teks Arab (atau transliterasi), lajur kiri membawa terjemahan
(susunan RTL, 14 Ogos) — kedua-duanya pada baris yang sama, jadi perbandingan
teks sumber–terjemahan dapat dibuat tanpa skrol menegak. Diuji secara
gemetri: `x` Arab > `x` terjemahan + 100px dan |y Arab − y terjemahan| < 300px
(`uji_visual_mockup.py`).

### 3.2 Transliterasi sebagai tab, bukan Collapsible

**Lama**: transliterasi ialah Collapsible berasingan di bawah kad Arab — satu
lagi bahagian menegak yang menolak kandungan ke bawah.

**Baharu**: lajur Arab mempunyai tab **ARAB / TRANSLITERASI** dengan
`QStackedWidget`: halaman 0 = teks Arab, halaman 1 = transliterasi dua gaya
(GAYA MELAYU + AKADEMIK), dibina malas bila tab dipilih. Konsisten dengan
mockup (`tab-bahasa lajur 1`).

### 3.3 Tab bahasa dalam lajur terjemahan

**Lama**: `LangTabs` global — satu bar tab di atas kotak terjemahan, melekat
ke kiri.

**Baharu**: tab bahasa (MELAYU / INDONESIA / ENGLISH) terletak **dalam** lajur
terjemahan (kiri, susunan RTL), sebaris dengan tab transliterasi di lajur
kanan (keputusan mockup `tab-bahasa lajur 2`).

**Lanjutan (13 Ogos)**: tab "Sebelah" (bandingan Melayu vs Indonesia) yang
sedia ada **dibuang** — ia bukan dalam mockup (yang hanya ada 3 tab), dan teks
translasi di dalamnya tidak sama paras dengan teks Arab. Fungsi "Salin semua
bahasa" (milik tab itu) turut dibuang. Paparan bahasa tunggal kini menjamin
teks terjemahan **sama paras (top-aligned) dengan teks Arab di lajur kanan
walau apa keadaan** — `Qt.AlignTop` pada setiap widget + `addStretch` di hujung
kotak terjemahan supaya ruang menegak berlebihan (bila lajur Arab lebih tinggi)
tinggal di bawah teks, bukan memusatkannya. Diuji oleh `uji_bandingan.py`
(kes "Arab >> terjemahan": beza < 40px pada Melayu lalai, Indonesia, dan
kembali Melayu).

### 3.4 Huraian terbuka + cip klasifikasi

Bahagian "Huraian (SemakHadis)" kekal terbuka seperti sebelumnya, tetapi kini
memaparkan **cip klasifikasi** (`chip`) dengan warna yang membawa makna:
- Hijau: Muttafaq 'alayh, Sahih, Hasan, صحيح
- Merah: Palsu, Munkar, Batil
- Amber: Lemah, Daif, ضعيف

`_warna_cip()` (semak.py 8v) memetakan klasifikasi DB kepada palet
GREEN/RED/AMBER mengikut tema aktif.

### 3.5 Penilaian ulama terbuka + papar mentah

**Lama** (keputusan Sesi 14): bahagian "Penilaian ulama (darjat)" tertutup
lalai — pengguna perlu klik untuk melihatnya.

**Baharu** (keputusan Sesi 55): bahagian ini **terbuka** lalai dan memaparkan
darjat secara **mentah** (baris "Nama — Darjat", 3 baris), tanpa tafsiran
pihak ketiga, bersama penafian "Penilaian ini daripada ulama hadis moden".
Kes tanpa data memaparkan mesej jujur "Tiada penilaian ulama".

### 3.6 Palet kertas hangat + TEAL hijau

Palet keseluruhan app bertukar kepada palet kertas hangat mockup:
- **Gelap**: latar `#1E1D1A`, kad `#282721`, teks `#E8E4DA`
- **Terang**: latar `#F4F1EA`, kad `#FFFFFF`, teks `#2B2B2B`
- Aksen TEAL lama biru (`#7FC4DE`) diganti **TEAL hijau** (`#5CBF85` gelap /
  `#1A6B3C` terang) — konsisten dengan breadcrumb, pautan dan bar bawah mockup.

Logo aplikasi dikunci kepada palet ini (semak.py 10aa menolak TEAL biru lama
kembali).

### 3.7 Nama kitab + prefix "Bab:"

- Ejaan nama kitab dibakukan kepada bentuk rasmi, cth. "Sahih al-Bukhari".
- Baris bab kini berprefix **"Bab:"** (cth. "Bab: ...") supaya jelas ia nama
  bab, bukan tajuk lain; tag "Bab Tafsir" muncul untuk kitab tafsir.

---

## 4. Fail sumber

| Peranan | Fail |
|---|---|
| Susun atur baharu (mixin) | `ui/pages_detail.py` |
| Palet (DARK/LIGHT) | `ui/theme.py` |
| Mockup rujukan reka bentuk | `mockup/mockup_{bukhari1,nasai2117,abudaud4177,ibnumajah2094}.html` |
| Semakan `_warna_cip` | `semak.py` (8v) |
| Semakan palet logo | `semak.py` (10aa) |
| Ujian struktur vs mockup | `uji_visual_mockup.py` |
| Ujian piksel (histogram + kehadiran) | `uji_visual_piksel.py` |
| Regresi tangkapan dokumen (jana semula vs baseline) | `bina_tangkapan_dokumentasi.py` |

Versi lama `ui/pages_detail.py` (sebelum komit `2972de2`) boleh dilihat
melalui `git show 823f417:ui/pages_detail.py`.

---

## 5. Pengesahan

Semua keputusan Sesi 55 dikunci oleh 10 lapisan ujian (12 Ogos 2026,
412 semakan, 0 gagal):

| Ujian | Peranan |
|---|---|
| `uji_visual_mockup.py` | 130/0 — kontrak struktur mockup vs widget app (susun atur dua lajur, tab per lajur, huraian/darjat terbuka, cip warna) |
| `uji_visual_piksel.py` | 53/0 — histogram warna, kehadiran aksen/cip, kepekaan mutasi palet |
| `uji_visual_sebenar.py` | 65/0 — tangkapan skrin fizikal + kecerahan ikut tema |
| `semak.py` | SEMUA LULUS — semakan statik termasuk 8v (cip) dan 10aa (logo) |
| `uji_negatif_8z.py` | 40/0 — mutasi semakan 8k/8v/10aa mesti dikesan |
| `bina_tangkapan_dokumentasi.py` | 7/7 — jana semula tangkapan dokumen, banding piksel vs baseline (nmad + pecahan berbeza); GAGAL bila rupa berubah |

Jalankan semuanya dengan satu arahan:

```bash
python uji_pra_hantar.py
```

---

## 6. Sejarah reka bentuk selepas Sesi 55 (13 Ogos 2026)

Keputusan Sesi 55 ditapis lagi pada 13 Ogos — berikut rekod penuh
setiap percubaan supaya sejarah reka bentuk lengkap:

### 6.1 Tab "Sebelah" dibuang

`LangTabs` kini **3 tab sahaja** (Melayu | Indonesia | English), sepadan
mockup. Fungsi "Salin semua bahasa" (milik tab Sebelah) turut dibuang;
tindakan salin/kongsi kekal di bar tajuk + menu klik kanan.

### 6.2 Teks terjemahan sama paras dengan Arab

Punca sebenar centering menegak dijumpai: **Qt memusatkan widget saiz
tetap dalam `QVBoxLayout` bila ada ruang menegak berlebihan**. Bila
lajur Arab lebih tinggi daripada terjemahan, kotak terjemahan menerima
ruang lebih → teks jatuh ke tengah. Pembaikan dalam `_switch_lang`:
`Qt.AlignTop` pada setiap widget terjemahan + `addStretch(1)` di hujung
kotak — ruang lebih tinggal DI BAWAH teks. Disahkan beza 0px pada
bukhari#3 dan kes "Arab jauh lebih panjang" (uji_bandingan).

### 6.3 Bar tindakan bawah terjemahan (sudut kanan) — KEPUTUSAN AKHIR

Pengguna meminta bar `Report Error | Share | Copy` seperti
sunnah.com/bukhari/1. Tiga iterasi diuji:

1. **Percubaan 1 — bawah teks Arab** (lajur kiri): tiga butang `⚠
   Lapor Ralat | 💬 Kongsi | 📋 Salin ▾`; Salin membuka menu popup
   (`QMenu`) dengan pilihan *Arab sahaja / terjemahan bahasa semasa /
   semuanya*. `Lapor Ralat` membuka halaman sunnah.com hadis itu
   dalam pelayar.
2. **Percubaan 2 — bawah terjemahan** (arahan pengguna "alih ke bhg
   bawah terjemahan"): bar dipindahkan ke lajur kanan, selepas
   `_trans_box` (tetap di bawah teks supaya paras kekal).
3. **DIBUANG sementara** (arahan "buang kotak kekal teks shj"):
   paparan kembali TAB + teks sahaja. **Kemudian DIPULIHKAN** atas
   arahan seterusnya: "letak bawah terjemahan sudut bawah kanan".

**KEPUTUSAN AKHIR — bar sebagai TEKS (bukan butang), di bawah
terjemahan, sudut BAWAH KANAN** (keputusan muktamad pengguna 13 Ogos:
"saya mahu text bagitu bukan button"): SATU `QLabel` HTML `Lapor
ralat | Kongsi | Salin` (pautan teal, pemisah `|` kelabu, warna ikut
tema via `TEAL`/`TEXT_SECONDARY`) di lajur kanan selepas `_trans_box`,
dijajarkan ke kanan (`addStretch(1)` di kiri menolak teks ke hujung
kanan). `Lapor ralat` membuka sunnah_url dalam pelayar; `Kongsi` =
WhatsApp bahasa semasa; `Salin` membuka menu popup (`QMenu`) pada
KEDUDUKAN KURSOR (punca "3 pilihan tak fungsi" sebelum ini: menu
dibuka di bawah butang → luar skrin) dengan pilihan *Arab sahaja /
terjemahan bahasa semasa / Arab + terjemahan semasa* (pilihan ke-3
ditukar daripada "semuanya" — tanpa baris rujukan). Diletak SELEPAS
`_trans_box` supaya teks tidak ditolak ke bawah (paras Arab ==
terjemahan kekal — disahkan beza < 40px). Disahkan: uji_bandingan
53/0, mockup 130/0, semak.py 0 GAGAL. Tangkapan skrin bukhari#1
(gelap + terang): `bukti_visual/bukhari1_gelap.png` dan
`bukti_visual/bukhari1_terang.png`.

### 6.4 Pembaikan flak ujian (bonus semasa percubaan 6.3)

`uji_bandingan.py` menjangka tetapan lalai saiz Arab (ar_idx=0) tetapi
`user_settings.json` sedia ada boleh menyimpan ar_idx=3 (dari ujian
lain) → semakan skala GAGAL walaupun kod betul. Ujian kini **sandarkan
+ pulihkan** user_settings.json, menulis lalai **dengan
`deklarasi_dibaca: true`** (penting: memadam fail membuat app cipta
semula tanpa bendera itu → dialog deklarasi modal menyekat offscreen).

### 6.5 Pengesahan akhir

Suite pra-hantar penuh `uji_pra_hantar.py` **SEMUA LULUS 11/11**
(405.5s, exit 0) selepas semua penapisan: semak.py (0 GAGAL) ·
mockup 130/0 · piksel · sebenar · tukar_tema · bandingan 48/0 ·
lompat_fungsi · end-to-end 18/0 · bina_tangkapan_dokumentasi 7/7 ·
draf_jawapan 9/9. Selepas pemulihan bar (keputusan akhir): bandingan
52/0. Tangkapan skrin bukhari#1 (gelap + terang):
`bukti_visual/bukhari1_gelap.png` dan `bukti_visual/bukhari1_terang.png`.
