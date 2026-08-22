# Isu: matn tidak diterjemah dalam teks Melayu hadis.my

**Tarikh:** 6 Ogos 2026
**Dilaporkan oleh:** pengguna (Muwatta Malik #153)
**Kaedah:** imbasan penuh `hadis.db` (262 MB, skema v7, 62,169 hadis)
**Punca:** data sumber hadis.my — **bukan** pepijat kod

---

## 1. Ringkasan

**80 hadis (0.13%)** mempunyai teks Melayu di mana sanad diterjemah tetapi
**matn kekal dalam bahasa Arab**.

Teks Indonesia bagi kesemua 80 kes adalah **lengkap** — sandaran tersedia
100%.

Kadar 0.13% menunjukkan kualiti hadis.my sebenarnya tinggi. Ini lubang
kecil, bukan kegagalan sistemik.

---

## 2. Kes yang dilaporkan — Muwatta Malik #153

```
ARAB   : و حَدَّثَنِي عَنْ مَالِك عَنْ ابْنِ شِهَابٍ عَنْ سَالِمِ بْنِ عَبْدِ اللَّهِ
         أَنَّ عَبْدَ اللَّهِ بْنَ عُمَرَ كَانَ يُكَبِّرُ فِي الصَّلَاةِ كُلَّمَا خَفَضَ وَرَفَعَ

MELAYU : Dan telah menceritakan kepadaku daripada Malik daripada Ibn Shihab
         daripada Salim bin 'Abdullah bahawa 'Abdullah bin 'Umar
         كانَ يُكَبِّرُ فِي الصَّلَاةِ كُلَّمَا خَفَضَ وَرَفَعَ        <- MATN TIDAK DITERJEMAH

INDO   : Telah menceritakan kepadaku dari Malik dari Ibnu Syihab dari Salim
         bin Abdullah, bahwa Abdullah bin 'Umar bertakbir dalam shalatnya
         setiap kali turun dan bangkit.                              <- LENGKAP
```

Terjemahan Melayu yang sepatutnya:
*"...bahawa 'Abdullah bin 'Umar **bertakbir dalam solatnya setiap kali
turun dan bangkit**."*

**Nota:** `malik #153` dalam hadis.db BUKAN hadis yang sama dengan CDN
`ara-malik #153` (azan Subuh / Umar). Penomboran berbeza — hadis.my Malik
= 1,594 hadis, CDN = 1,858. Kedua-duanya betul untuk penomboran
masing-masing.

---

## 3. Kaedah pengesanan

Mengukur **jujukan aksara Arab berterusan terpanjang** dalam teks Melayu.
Ambang **40 aksara**.

Sensitiviti ambang:

| ambang | kes |
|---|---|
| 25 aksara | 255 |
| 30 aksara | 230 |
| **40 aksara** | **80** |
| 60 aksara | 40 |
| 100 aksara | 17 |

Lompatan besar antara 30 dan 40 mencadangkan ambang 40 memisahkan
**petikan Arab yang wajar** (lafaz doa, istilah, nama) daripada **matn
yang benar-benar tercicir**.

---

## 4. Taburan

| kitab | terjejas | jumlah | % |
|---|---|---|---|
| **malik** | **26** | 1,594 | **1.6%** |
| bukhari | 19 | 7,008 | 0.3% |
| tirmidzi | 19 | 3,891 | 0.5% |
| ahmad | 8 | 26,363 | 0.0% |
| darimi | 7 | 3,367 | 0.2% |
| nasai | 1 | 5,662 | 0.0% |
| abu-daud | 0 | 4,590 | 0.0% |
| ibnu-majah | 0 | 4,332 | 0.0% |
| muslim | 0 | 5,362 | 0.0% |
| **JUMLAH** | **80** | **62,169** | **0.13%** |

Malik 12x lebih teruk daripada purata. Muslim, Abu Daud dan Ibnu Majah
bersih sepenuhnya.

---

## 5. Senarai penuh 80 ID

Untuk dilaporkan kepada hadis.my.

**malik (26)**
```
36, 108, 109, 152, 153, 181, 190, 341, 522, 552, 556, 572, 619,
647, 685, 701, 775, 779, 799, 806, 809, 828, 881, 1082, 1418, 1513
```

**bukhari (19)**
```
1782, 2863, 3394, 3459, 3477, 3525, 4162, 4311, 4413, 4511,
4578, 4603, 4604, 4935, 6236, 6654, 6875, 6936, 6990
```

**tirmidzi (19)**
```
231, 1341, 1419, 1922, 2175, 2562, 2711, 2863, 2877, 3028,
3029, 3031, 3073, 3104, 3116, 3120, 3179, 3270, 3726
```

**ahmad (8)**
```
4303, 4976, 8072, 9358, 10614, 17426, 24278, 26329
```

**darimi (7)**
```
91, 478, 645, 909, 2133, 2608, 3246
```

**nasai (1)**
```
468
```

---

## 6. Pilihan tindakan

### A. Papar amaran (disyorkan)

Kesan pada masa jalan dengan regex yang sama (blok Arab >= 40 aksara dalam
`melayu`), papar nota:

> *Sebahagian teks tidak diterjemah dalam sumber. Rujuk tab Indonesia.*

- Jujur — tidak menyembunyikan atau mengubah data
- Kerja kecil: satu semakan pada paparan
- Berfungsi automatik jika hadis.my membetulkannya kelak

### B. Isi dengan Indonesia

Untuk 80 hadis ini, papar teks Indonesia dengan label
*"(terjemahan Indonesia — Melayu tidak lengkap)"*.

- Indonesia lengkap untuk **kesemua 80** — sandaran tersedia
- **Kelemahan:** menukar bahasa tanpa pengguna meminta. Keputusan projek
  sebelum ini ialah mengekalkan Melayu dan Indonesia berasingan.

### C. Laporkan kepada hadis.my (disyorkan, selari dengan A)

Hantar senarai §5 kepada:
- `khai@webmaster.my`
- WhatsApp +60 19-209 2006

Membaiki punca sebenar; semua pengguna API mendapat manfaat.
Tiada kos kod.

---

## 7. Cadangan

**A + C.** Amaran memberi kejujuran serta-merta; laporan membaiki punca.

B ditolak kerana ia menukar bahasa tanpa kebenaran pengguna, bertentangan
dengan keputusan reka bentuk sedia ada.

---

## 8. Nota

Isu ini **tidak** berkaitan dengan lapisan padanan (`indo`, `indo~`,
`penuh`, `awalan`, `kata`). Teks Melayu datang terus daripada
`hadis.melayu` — tiada padanan terlibat.

Semasa siasatan, satu perkara berasingan ditemui: sumber CDN `ind-*`
mempunyai banyak rekod kosong (`ind-muslim` 34.9%, `ind-malik` 16.5%,
`ind-bukhari` 9.6%, `ind-nasai` 7.5%). Ini **berkaitan** dengan padanan
kerana lapisan `indo` menggunakan teks Indonesia sebagai kunci, dan
`audit_eng.py` menggunakannya sebagai saksi.

Corak hanyutan yang didokumenkan dalam `PERUBAHAN_31JUL.md` §9 (6 kes
"disyaki") mungkin lebih meluas daripada yang dilaporkan. **Belum
disiasat** — audit menggunakan sumber yang sama yang mempunyai lubang,
jadi ia mungkin tidak dapat melihatnya.

Diagnosis yang dicadangkan: bagi setiap hadis yang dipadan melalui
`indo`/`indo~`, banding teks **Arab** hadis.db dengan `ara-*` pada nombor
yang dipadan. Jaccard Arab rendah = padanan salah.
