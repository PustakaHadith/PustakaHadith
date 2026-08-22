# Audit Liputan SemakHadis — 14 Ogos 2026

> Audit penuh liputan huraian SemakHadis (BM) dalam hadis.db: per
> kitab, per bab, dan taburan jurang. Tujuan: mengenal pasti bahagian
> yang paling banyak tertinggal supaya sumber BM terbuka lain boleh
> dinilai ikut tempat ia paling diperlukan.
>
> Data: hadis.db (62,169 hadis) · semakhadis (4,237 padanan, 2,263
> sema_id unik) · bab (31,325 baris, 393 bab unik untuk 7 kitab
> bersumber CDN).

## 1. Liputan keseluruhan

| Metrik | Nilai |
|---|---|
| Hadis dalam DB | 62,169 |
| Hadis dengan huraian SemakHadis | **4,237 (6.8%)** |
| Sema_id unik | 2,263 |
| Sumber cache | `.cache_sema/` — 2,372 hadis SemakHadis.com (sahih-relevan: Muttafaq 'alayh, Sahih, Hasan) |

## 2. Liputan per kitab

| Kitab | Total | Sema | Liputan | Kedudukan |
|---|---|---|---|---|
| tirmidzi | 3,891 | 63 | **1.6%** | ⚠️ terendah |
| darimi | 3,367 | 148 | 4.4% | ⚠️ |
| ahmad | 26,363 | 1,645 | 6.2% | |
| nasai | 5,662 | 350 | 6.2% | |
| malik | 1,594 | 121 | 7.6% | |
| abu-daud | 4,590 | 354 | 7.7% | |
| muslim | 5,362 | 430 | 8.0% | |
| ibnu-majah | 4,332 | 409 | 9.4% | |
| bukhari | 7,008 | 717 | **10.2%** | terbaik |

Catatan: `ahmad` dan `darimi` tiada dalam jadual `bab` (tiada sumber
CDN) — jurangnya diukur ikut julat id (lihat §5).

## 3. Jurang per bab (7 kitab bersumber, 393 bab)

### 3.1 Taburan liputan bab

| Liputan bab | Bilangan bab | % |
|---|---|---|
| 0% (langsung tiada) | 103 | 26% |
| 1–4% | 77 | 20% |
| 5–9% | 68 | 17% |
| 10–19% | 68 | 17% |
| 20–49% | 34 | 9% |
| 50–100% | 3 | 1% |

**26% bab langsung tidak disentuh SemakHadis; hanya 3 bab melebihi
50% liputan.** Liputan SemakHadis sangat tertumpu pada hadis masyhur.

### 3.2 Bab paling banyak tertinggal (hadis tanpa SemakHadis)

| Kitab | Book | Bab | Total | Sema | Tertinggal | Liputan |
|---|---|---|---|---|---|---|
| bukhari | 65 | Prophetic Commentary on the Qur'an | 476 | 35 | **441** | 7.4% |
| bukhari | 64 | Military Expeditions | 419 | 25 | 394 | 6.0% |
| bukhari | 56 | Jihad | 273 | 9 | 264 | 3.3% |
| bukhari | 78 | Al-Adab | 241 | 21 | 220 | 8.7% |
| bukhari | 25 | Hajj | 222 | 16 | 206 | 7.2% |
| muslim | 15 | Pilgrimage | 446 | 31 | **415** | 7.0% |
| muslim | 1 | Faith | 315 | 51 | 264 | 16.2% |
| muslim | 44 | Merits of Companions | 224 | 13 | 211 | 5.8% |
| abu-daud | 2 | Prayer (Al-Salat) | 643 | 94 | **549** | 14.6% |
| abu-daud | 43 | Al-Adab | 446 | 25 | 421 | 5.6% |
| abu-daud | 1 | Purification | 329 | 21 | 308 | 6.4% |
| tirmidzi | 47 | Tafsir | 411 | 9 | **402** | 2.2% |
| tirmidzi | 49 | Virtues | 339 | 6 | 333 | 1.8% |
| tirmidzi | 2 | Salat | 274 | 1 | 273 | 0.4% |
| nasai | 24 | Hajj | 462 | 21 | **441** | 4.5% |
| nasai | 48 | Adornment | 326 | 2 | 324 | 0.6% |
| nasai | 1 | Purification | 320 | 17 | 303 | 5.3% |
| ibnu-majah | 5 | Establishing Prayer | 628 | 79 | **549** | 12.6% |
| ibnu-majah | 1 | Purification | 396 | 28 | 368 | 7.1% |
| ibnu-majah | 25 | Hajj | 238 | 10 | 228 | 4.2% |
| malik | 20 | Hajj | 224 | 16 | **208** | 7.1% |
| malik | 2 | Purity | 103 | 7 | 96 | 6.8% |
| malik | 29 | Divorce | 90 | 2 | 88 | 2.2% |

### 3.3 Bab sifar mutlak (contoh ketara)

| Kitab | Bab | Total | Sema |
|---|---|---|---|
| tirmidzi | 43 Chapters on Manners | 119 | 0 |
| tirmidzi | 14 The Book on Business | 116 | 0 |
| nasai | 26 The Book of Marriage | 191 | 0 |
| malik | 31 Business Transactions | 72 | 0 |
| malik | 36 Judgements | 51 | 0 |
| malik | 28 Marriage | 45 | 0 |

## 4. Corak jurang — tema paling terjejas

1. **Tafsir (huraian Qur'an)** — bukhari 65 (441 tertinggal) +
   tirmidzi 47 (402) = jurang bab tunggal terbesar
2. **Hajj** — 5 bab merentas 5 kitab (muslim 415, nasai 441,
   ibnu-majah 228, malik 208, abu-daud 272) ≈ **1,564 hadis**
3. **Solat** — abu-daud 2 (549) + ibnu-majah 5 (549) + tirmidzi 2
   (273) ≈ **1,371 hadis**
4. **Tirmidzi hampir kosong** (1.6%) — walaupun hadis masyhur dalam
   kitab lain ada, hampir semua riwayat Tirmidzi tiada huraian

## 5. Ahmad & Darimi (tiada bab CDN) — liputan per desil

**ahmad (26,363):** agak seragam 5–9% setiap desil — tiada tumpuan
(jurang menyeluruh).

**darimi (3,367):** tidak seragam — puncak 13.0% (id 1,347–1,684)
dan 7.1% (2,357–2,693); terendah 0.9% (2,693–3,030) dan 1.8%
(2,020–2,357).

## 6. Klasifikasi status (daripada 4,237 padanan)

| Status | Bilangan |
|---|---|
| Sahih | 1,517 |
| Muttafaq 'alayh | ~1,500 |
| Hasan | 643 |
| Lemah / Daif / Sangat lemah / Terlalu Daif | ~380 |
| Munkar / Palsu / Batil / Dusta | ~115 |

## 7. Implikasi untuk sumber BM lain

Siling SemakHadis (6.8%) bukan boleh ditambah dalam sumber itu sendiri
— `.cache_sema/` sudah mengandungi SEMUA hadis SemakHadis.com yang
relevan (2,372). Untuk menaikkan liputan, perlu sumber BM terbuka
LAIN. Audit ini menunjukkan keutamaan berdasarkan jurang:

1. **Tafsir** — sumber tafsir BM terbuka per-hadis (bukan buku PDF)
   akan menutup jurang terbesar (bukhari 65 + tirmidzi 47)
2. **Hajj + Solat** — ~2,900 hadis merentas kitab; sumber syarah BM
   yang meliputi bab ibadah
3. **Tirmidzi** — kitab paling terbiar; sumber yang menyenaraikan
   riwayat Tirmidzi sahaja
4. **Ahmad (26,363)** — liputan menyeluruh rendah; perlu sumber
   Musnad-berstruktur

Sumber yang telah disiasat dan TIDAK layak (rekod penuh:
`dokumen/audit/DAPATAN_WEB.md` + `dokumen/perubahan/PERUBAHAN_31JUL.md`
§13): Irsyad al-Hadith (lesen tertutup), MyHadith JAKIM (ralat
rangkaian), IslamHouse Malay (buku PDF, bukan per-hadis), hadits.id /
NU / tazkia / Kemenag (terjemahan sahaja), Bulughul Maram (kitab
berbeza), dorar.net (Arab, carian sahaja), sunnah.com (Inggeris).

## 8. Kaedah

Query SQL agregat pada hadis.db: gabung `hadis` + `bab` (book, nama_bab)
+ `semakhadis` (LEFT JOIN ikut collection + hadis_id). `ahmad`/`darimi`
tidak bergabung dengan `bab` (tiada sumber CDN) — dianalisis ikut
desil hadis_id. Tidak mengubah apa-apa.
