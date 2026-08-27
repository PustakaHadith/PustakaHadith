# Terjemahan Inggeris — Musnad Ahmad & Sunan ad-Darimi (Jurang 0%)

> Ditulis 14 Ogos 2026, dikemas kini 15 Ogos 2026. Susulan
> `dokumen/rujukan/SUMBER_hadis-my.md` § "Kitab tidak tersedia" — menjawab
> soalan: bolehkah jurang 0% terjemahan Inggeris untuk Ahmad & Darimi dalam
> Pustaka Hadith diisi daripada sumber lain?

> **KEMAS KINI PENTING — 15 Ogos 2026:** Bahagian audit Ahmad di bawah
> merekodkan urutan siasatan dan sebahagiannya kini **digantikan** oleh
> `dokumen/audit/AHMAD_HOCR.md`. Fakta terkini: Jilid 4 Darussalam
> (#4377–6030) telah ditemui; aset Jilid 1–4 mengandungi 5,527/6,030 entri;
> nombor terus dibuktikan gagal (#700 Darussalam = #662 data projek); dan
> segmentasi koordinat hOCR berjaya pada lima sampel disahkan. Siasatan susulan
> turut memperoleh **1,345 padanan tepat Arab digital tanpa OCR**; lihat
> `AHMAD_DIGITAL.md`. **Import produksi masih ditangguhkan** kerana lesen teks
> terjemahan belum jelas dan baki OCR memerlukan semakan. Jika terdapat
> percanggahan, `AHMAD_DIGITAL.md` / `AHMAD_HOCR.md` mengatasi dokumen ini.

**Keputusan ringkas (dikemas kini):**
- **Sunan ad-Darimi** — TIDAK boleh diisi dgn kualiti dipercayai. Kekal 0%.
- **Musnad Ahmad** — aset OCR Inggeris Jilid 1–4 kini berjumlah **5,527
  entri** (sekitar 21% daripada 26,363 hadis projek), tetapi belum boleh
  diimport secara pukal. Segmentasi koordinat hOCR menyelesaikan punca utama
  kegagalan padanan lama pada sampel disahkan; lihat `AHMAD_HOCR.md` untuk
  status, ujian dan sekatan terkini.

---

## 1. Konteks

`core/eng_source.py` (Fasa 3) guna CDN `fawazahmed0/hadith-api` untuk terjemahan
Inggeris 7 daripada 9 kitab. Komen kod sedia ada:

> *"KITAB TIDAK TERSEDIA — `ahmad` (Musnad Ahmad) dan `darimi` — tiada dalam
> sumber ini. Tab English mesti kekal kelabu untuk kedua-duanya; jangan
> berpura-pura."*

Soalan asal: adakah `hadith.my`/sunnah.com ada liputan lebih baik? Soalan
susulan (sesi ini): adakah sumber **luar CDN** (cetakan buku, GitHub, laman AI)
boleh isi jurang?

---

## 2. hadith.my — Tiada Bantuan (disahkan)

| # | Koleksi | Jumlah Hadis (Inggeris, 100% siap) |
|---|---|---|
| 1 | Sahih Bukhari | 7,554 |
| 2 | Sahih Muslim | 7,360 |
| 3 | Sunan An-Nasa'i | 5,672 |
| 4 | Sunan Abi Dawud | 5,272 |
| 5 | Sunan Ibn Majah | 4,338 |
| 6 | Jami' At-Tirmidhi | 3,889 |
| 7 | Muwatta Malik | 1,818 |
| 8 | Forty Hadith An-Nawawi | 42 |
| 9 | Forty Hadith Qudsi | 40 |

**Musnad Ahmad dan Sunan ad-Darimi TIDAK wujud dalam senarai.** hadith.my dan
hadis.my (API) pengendali sama (webmaster.my) — jurang sumber sama persis
diwarisi merentas kedua-dua produk mereka. (Nota skema nombor berbeza antara
API vs web kekal berkaitan — lihat `SUMBER_hadis-my.md`.)

---

## 3. sunnah.com — Sumber Rujukan Silang (bukan sumber isi)

| Kitab | Status Inggeris | Anggaran liputan |
|---|---|---|
| **Musnad Ahmad** | ⚠️ Label eksplisit di laman: **"4% complete"** | ~1,128–1,200 / ~28,199 hadis |
| **Sunan ad-Darimi** | ❌ *"has unfortunately not been translated into English yet"* | 0 / ~3,400 hadis |

**Diuji langsung (14 Ogos 2026):** `sunnah.com/ahmad:1` dan `sunnah.com/ahmad:1200`
wujud & ada teks Inggeris; `sunnah.com/ahmad:2000`, `:2500`, `:3000`, `:4376`
**semua "not available yet"**. Jadi sempadan sebenar liputan sunnah.com berada
di antara hadis #1200 dan #2000 (anggaran laman "4%" adalah tepat mengikut
jumlah keseluruhan ~28,199).

**Penemuan penting:** teks Inggeris `sunnah.com/ahmad:1` dan `:1200` **sepadan
100% perkataan-demi-perkataan** dengan cetakan Darussalam (lihat §4) — kerana
sunnah.com memang guna terjemahan Darussalam yang sama (penterjemah sama:
Nasiruddin Al-Khattab). Ini membuktikan sunnah.com bukan sumber bebas — ia
cuma **sebahagian kecil** drpd cetakan Darussalam yg sama dipaparkan dlm talian.

---

## 4. PENEMUAN BAHARU — Cetakan Darussalam di Archive.org (disahkan berfungsi)

### 4.1 Apa yang wujud

Darussalam menerbitkan terjemahan Inggeris **Musnad Ahmad** oleh
**Nasiruddin Al-Khattab** (disunting Huda Al-Khattab). Imbasan berikut
ditemui di Archive.org:

| Jilid | Julat Hadis | Identifier archive.org |
|---|---|---|
| 1 | 1–1,380 | `EnglishTranslationOfMusnadImamAhmedBinHanbalVolume1` |
| 2 | 1,381–2,822 | `musnad-imam-ahmad-bin-hanbal-volume-1-3` |
| 3 | 2,823–4,376 | `musnad-imam-ahmad-bin-hanbal-volume-1-3` |
| 4 | 4,377–6,030 | `musnadahmadvol.4final` |

Jilid 5 (#6031–7624) dan Jilid 6 (#7625–9344) turut diterbitkan, tetapi PDF
Inggeris terbuka belum disahkan. Dua calon fail RMP yang diperiksa secara
visual sebenarnya edisi Urdu. Lihat `AHMAD_HOCR.md` §2.

### 4.2 archive.org sudah ada teks OCR sedia (jimat kerja besar)

Setiap fail PDF di archive.org **automatik** diproses archive.org sendiri
menghasilkan fail `..._djvu.txt` (OCR ABBYY, drpd 2016). **Ini bermakna TIDAK
perlu jalankan OCR sendiri drpd imej PDF utk lapisan Inggeris** — terus muat
turun teks siap:

```
https://archive.org/download/EnglishTranslationOfMusnadImamAhmedBinHanbalVolume1/EnglishTranslationOfMusnadImamAhmedBinHanbal-Volume1_djvu.txt
https://archive.org/download/musnad-imam-ahmad-bin-hanbal-volume-1-3/EnglishTranslationOfMusnadImamAhmedBinHanbal-Volume2_djvu.txt
https://archive.org/download/musnad-imam-ahmad-bin-hanbal-volume-1-3/EnglishTranslationOfMusnadImamAhmedBinHanbal-Volume3_djvu.txt
https://archive.org/download/musnadahmadvol.4final/Musnad%20Ahmad%20Vol.%204%20final_djvu.txt
```

### 4.3 Masalah OCR: teks Arab bocor sbg "sampah" dalam lajur Inggeris

Cetakan Darussalam ini **dwibahasa 2-lajur** (Inggeris kiri, Arab kanan pada
muka sama — disahkan render imej PDF sebenar, lihat Lampiran A). Enjin OCR
ABBYY yg dijalankan archive.org (mod Inggeris) cuba baca lajur Arab sbg huruf
Latin & hasilkan gibberish yg tersisip di tengah teks Inggeris, cth:

> *"...he came with the leaves ilL JJU jjai- 1 4lU ^>\j : Jtf dropping from
> his hands..."*

**Diselesaikan** dgn skrip `ekstrak_ahmad_darussalam.py` (disertakan) — tapis
setiap baris guna pustaka `wordfreq` (kekerapan perkataan Inggeris sebenar):
baris dikekalkan hanya jika ≥78% token (≥3 huruf) ialah perkataan Inggeris
sah. **Keputusan diuji:**

| Jilid | Hadis diekstrak bersih | Drpd jumlah |
|---|---|---|
| 1 | 1,290 | 1,380 (93.5%) |
| 2 | 1,344 | 1,442 (93.2%) |
| 3 | 1,424 | 1,554 (91.6%) |
| 4 | 1,469 | 1,654 (88.8%) |
| **Jumlah** | **5,527** | **6,030 (91.7%)** |

503 hadis yang tidak berjaya diekstrak automatik masih ada dalam fail OCR
mentah. Jangan turunkan ambang secara buta; teks bercampur Arab-Latin perlu
semakan manusia. **Sampel Jilid 1–3 disahkan tepat** (lihat §4.4), manakala
Jilid 4 kekal aset OCR awal yang memerlukan sampel semakan lebih luas.

### 4.4 Pengesahan ketepatan — padanan 100% dgn sunnah.com

Baris pertama hasil ekstrak utk hadis #1 dan #1200 dibandingkan **perkataan-
demi-perkataan** dgn teks rasmi `sunnah.com/ahmad:1` dan `:1200`:

> **#1** (kedua-dua sumber): *"It was narrated that Qais said: Abu Bakr stood
> up and praised and glorified Allah, then he said: O people, you recite this
> verse..."* — **sepadan 100%**

> **#1200** (kedua-dua sumber): *"It was narrated that Abu Ma'mar said: We
> were with 'Ali when a funeral passed by him and some people stood up for
> it..."* — **sepadan 100%**

Ini mengesahkan: (a) skrip ekstrak berfungsi betul, (b) OCR archive.org cukup
tepat utk teks Inggeris bersih, (c) nombor hadis Darussalam **1, 1200** ialah
nombor **SAMA** yg dipakai sunnah.com.

### 4.5 Fail diserahkan

- `dokumen/rujukan/ekstrak_ahmad_darussalam.py` — skrip lengkap (muat turun +
  bersih + simpan), boleh dijalankan semula bila-bila (idempoten, cache lokal)
- `dokumen/rujukan/ahmad_darussalam_1_4376.json` — fail lama Jilid 1–3
  (4,058 entri, dikekalkan untuk keserasian)
- `dokumen/rujukan/ahmad_darussalam_1_6030.json` — Jilid 1–4 (5,527 entri)

---

## 5. ISU PENOMBORAN — SELESAI DISAHKAN BERBEZA

Musnad Ahmad **tiada "nombor antarabangsa"** rasmi. Pada 15 Ogos 2026, set
data Arab 26,363 hadis yang mempunyai kiraan dan teks sama dengan projek
ditemui dalam `abdelrahmaan/Hadith-Data-Sets`. Ujian kandungan mengesahkan:

| Nombor Darussalam | `hadis_id` projek/data Arab |
|---:|---:|
| 1 | 1 |
| 699 | 661 |
| 700 | 662 |
| 701 | 663 |
| 1200 | 1138 |

Maka **nombor terus dibatalkan**. Contoh paling jelas: teks Darussalam #1200
berada pada `hadis_id` #1138, manakala `hadis_id` #1200 ialah hadis zakat yang
berbeza. JSON Darussalam tidak boleh digunakan terus sebagai kunci DB.

### 5.3 Plan B lama — OCR blob halaman (dijalankan 14 Ogos 2026; kini digantikan)

Cetakan Darussalam turut ada edisi imbasan **dwibahasa** (Arab+Inggeris sama
muka surat). **Kerja OCR Arab PENUH telah dijalankan dlm sesi ini** —
bukan lagi proof-of-concept, tapi hasil sebenar 4,058 hadis:

- Dipasang `tesseract-ocr` + pek bahasa `tesseract-ocr-ara`
- Setiap muka surat PDF asal (1,841 muka surat, 3 jilid) dirender 200 DPI,
  dipotong separuh kanan (lajur Arab, disahkan susun atur 2-lajur dgn
  semakan visual pelbagai muka surat), di-OCR semula dgn `-l ara`
- **Offset ms bercetak → indeks PDF dikalibrasi & disahkan dgn render imej
  SEBENAR** (bukan anggaran): Jilid 1 `+2`, Jilid 2 `+3`, Jilid 3 `+0` —
  setiap satu disahkan tepat dgn membuka imej sebenar & padan kandungan
  (cth. hadis #1380 "End of the Musnad..." tepat di ms bercetak 622/pdf#624)
- **Keputusan:** 1,841/1,841 muka surat berjaya diproses (98%+ ada teks
  bermakna), digabung ikut sempadan hadis (drpd `_djvu.txt`) jadi teks Arab
  mentah bagi 4,058/4,376 hadis

**NOTA KETEPATAN — diuji & dilaporkan jujur, DIKEMAS KINI selepas ujian skala PENUH:**
OCR Arab imbasan lama **TIDAK sempurna**, dan ujian skala kecil (3 sampel)
awal ternyata **terlalu optimistik**. Ujian susulan (padan #700 thd
**KESEMUA 3,929 calon**, bukan cuma 2-3):
- Skor pasangan yg SEPATUTNYA betul: 0.577
- **Kedudukan pasangan betul dlm ranking: #238 drpd 3,929** (BUKAN #1)
- Skor calon SALAH tertinggi: 0.981

**Kesimpulan Plan B (dikemas kini, jujur):** kaedah padanan automatik
trigram/containment semasa **TIDAK CUKUP DIPERCAYAI pada skala sebenar**
(ura ayat formula Arab yg dikongsi merata hadis + gabungan OCR pelbagai
hadis sehalaman menyebabkan calon SALAH kerap dpt skor lebih tinggi drpd
calon BETUL). Skrip `padan_ahmad_darussalam.py` kini ada **sekatan
keselamatan** (`--terap` perlu pengesahan eksplisit taip
"SAYA-FAHAM-RISIKO") supaya tidak disangka siap-guna.

**Apa yang MASIH sah & berguna drpd Plan B:**
- Teks Inggeris (4,058 hadis) — kualiti baik, disahkan tepat
- Teks Arab OCR mentah — berguna sbg BAHAN RUJUKAN kerja manual (nama
  perawi masih boleh dikenal pasti), TAPI BUKAN input algoritma automatik
  tanpa penambahbaikan besar (cadangan teknikal dlm skrip: OCR per-lajur
  `--psm 4` + pengesanan koordinat nombor Arab utk sempadan hadis individu
  yg tepat, ATAU serah kpd penyemak manusia fasih Arab sbg panduan sahaja)

**Kemas kini 15 Ogos:** padanan nombor terus telah dibuktikan gagal. Kaedah
blob di atas kini digantikan oleh segmentasi koordinat dalam
`audit_padan_ahmad_hocr.py`; lihat `AHMAD_HOCR.md` untuk keputusan terkini.


**Fail dihasilkan (siap, tiada perlu OCR semula):**
- `dokumen/rujukan/_arab_ocr_output/jilid{1,2,3}_arab_mentah.json` — OCR
  Arab mentah bagi 1,841 muka surat (~1.4MB)
- `dokumen/rujukan/ocr_arab_darussalam.py` — skrip OCR (boleh dijalankan
  semula/disambung jika perlu proses ulang)
- `dokumen/rujukan/padan_ahmad_darussalam.py` — rekod kaedah blob lama;
  **jangan jalankan `--terap`**
- `dokumen/rujukan/audit_padan_ahmad_hocr.py` — kaedah koordinat baharu,
  audit sahaja dan tidak menulis `hadis.db`


---

## 6. Sunan ad-Darimi — Kekal Mustahil (disahkan, tiada perubahan kesimpulan)

Semua sumber terbuka disiasat semula khusus utk Darimi:

| Sumber | Keputusan |
|---|---|
| sunnah.com | ❌ 0% — *"has unfortunately not been translated into English yet"*; `/darimi` cuma papar struktur 23 bab Arab |
| GitHub `AhmedBaset/hadith-json` (a.k.a. `A7med3bdulBaset`, 299 ⭐) | ❌ **README MENGELIRUKAN** — dakwa "50,884 hadiths ... in both Arabic and English" merentas 17 kitab termasuk Darimi. **Disahkan PALSU** dgn fetch terus `raw.githubusercontent.com/.../darimi.json`: setiap entri ada `"english":{"narrator":"","text":""}` — **KOSONG SEPENUHNYA** utk semua hadis Darimi (Arab sahaja ada isi) |
| `islamicnexus.org/hadith/8` | ❌ 3,406 hadis/23 bab dipaparkan tapi setiap muka surat hadis sebenar (cth `/hadith/8/chapter/348`) cuma papar Arab, sifar Inggeris |
| `hadithunlocked.com/darimi` | ⚠️ **ADA** teks Inggeris tapi **setiap entri berlabel jelas "[AI]"/"[Machine]"** (cth. `darimi:2660`) — ini **terjemahan mesin/AI**, BUKAN kerja sarjana. Risiko ketepatan tinggi utk teks agama — **TIDAK disyorkan** tanpa semakan sarjana penuh |
| Cetakan bercetak (Darussalam/lain) | Tiada projek terjemahan Darimi diketahui wujud/dijumpai setakat siasatan |

**Kesimpulan Darimi tidak berubah:** kekal 0% boleh dipercayai. Satu-satunya
pilihan (`hadithunlocked.com`, AI) membawa risiko ketepatan yg tidak sesuai
utk teks agama tanpa semakan sarjana — **tidak disyorkan untuk projek ini**.

---

## 7. Kesimpulan & Cadangan Tindakan (status 15 Ogos 2026)

| Soalan | Jawapan terkini |
|---|---|
| Bolehkah hadith.my isi jurang Ahmad/Darimi? | ❌ Tidak |
| Wujudkah teks Inggeris tambahan untuk Ahmad? | ✅ Ya — 5,527 entri OCR Jilid 1–4 |
| Adakah nombor Darussalam sama dengan `hadis_id`? | ❌ Tidak — #700 Darussalam = #662 data projek |
| Adakah kaedah blob lama selamat? | ❌ Tidak — pasangan betul #238/3,929 |
| Adakah segmentasi koordinat lebih baik? | ✅ Ya pada sampel: lima pasangan disahkan lulus 3/3 varian OCR |
| Boleh import secara pukal sekarang? | ❌ Belum — perlu penjajaran global dan semakan manusia |
| Bolehkah Darimi diisi daripada sumber dipercayai? | ❌ Tidak |

**Tindakan disyorkan:**

1. Kekalkan tab English Ahmad dan Darimi kelabu dalam keluaran produksi.
2. Simpan aset Jilid 1–4 dan manifest koordinat sebagai bahan kerja.
3. Gunakan hanya `audit_padan_ahmad_hocr.py` untuk ujian; skrip itu tidak
   membuka atau menulis `hadis.db`.
4. Bina penjajaran global monotonik untuk menangani OCR lemah, laporan
   “serupa” dan pemetaan banyak-ke-satu.
5. Semak sekurang-kurangnya 100 pasangan dengan penyemak fasih Arab sebelum
   mempertimbangkan import subset keyakinan tinggi.
6. Sahkan kebenaran pengedaran semula terjemahan Darussalam.
7. Sunan ad-Darimi: tiada tindakan lanjut sehingga sumber sarjana wujud.

**Rujukan muktamad teknikal:** `dokumen/audit/AHMAD_HOCR.md`.

---

## Lampiran A — Bukti Susun Atur Cetakan Darussalam

Muka surat 25–26 Jilid 1 (render 200 DPI drpd PDF asal archive.org) mengesahkan
susun atur **2 lajur**: Inggeris (kiri) | Arab bertashkeel penuh (kanan),
tajuk bab berulang di atas setiap muka ("Musnad Abu Bakr Siddeeq" / "مسند أبي
بكر الصديق"), rujukan takhrij di penghujung setiap hadis (cth. "إسناده صحيح.
خ: (3615) م: (2009)"). Ini struktur cetakan sarjana piawai (bukan blog/laman
tanpa rujukan) — kualiti kandungan boleh dipercayai setanding penerbitan
Darussalam yg lain (spt terjemahan Bukhari/Muslim yg projek ini sedia guna
scr tak langsung mll CDN fawazahmed0).

## Lampiran B — Sumber Rujukan Luaran

- `https://sunnah.com/ahmad` (& `/ahmad:1`, `/ahmad:700`, `/ahmad:1200`,
  `/ahmad:2000+` disahkan "not available")
- `https://sunnah.com/darimi`
- `https://archive.org/details/EnglishTranslationOfMusnadImamAhmedBinHanbalVolume1`
- `https://archive.org/details/musnad-imam-ahmad-bin-hanbal-volume-1-3`
- `https://archive.org/details/musnad-ahmad-ibn-hanbal` (edisi dwibahasa)
- `https://islam.stackexchange.com/questions/75227/international-numbering-of-musnad-ahmad-hadiths`
- `https://islam.stackexchange.com/questions/51888/i-need-an-exact-reference-for-a-hadith-in-musnad-ahmed`
- `https://github.com/AhmedBaset/hadith-json` (README diperiksa vs data sebenar)
- `https://hadithunlocked.com/darimi`
- `https://islamicnexus.org/hadith/8`

*Rujukan silang: `dokumen/rujukan/SUMBER_hadis-my.md`, `core/eng_source.py`,
`dokumen/rujukan/ekstrak_ahmad_darussalam.py`,
`dokumen/rujukan/ahmad_darussalam_1_4376.json`,
`dokumen/audit/GTAF.md` §6c.3 (isu kaedah kiraan serupa).*
