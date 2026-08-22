# Audit Pautan "Baca Penuh" sunnah.com — 11 Ogos 2026

> **Keputusan: 50 dipadan, 0 tidak padan, 0 tidak dapat disahkan
> (dari 50)** — kesemua pautan "Baca penuh" membuka hadis yang betul
> di sunnah.com. Semak.py penuh: **SEMUA LULUS**.
>
> Cara jalankan semula: `python semak.py --audit-sunnah=50` (seksyen 8o).

## Tujuan

Pautan **"Baca penuh"** pada halaman hadis membuka hadis yang sama di
sunnah.com dalam pelayar. Sebelum versi dihantar, audit mengesahkan
pautan itu betul terhadap halaman **sebenar** sunnah.com — bukan
sekadar struktur URL.

## Metodologi

- **Sampel:** 50 hadis rawak daripada `sunnah_map/` (peta dalam-buku;
  7 kitab: bukhari, muslim, nasai, abu-daud, tirmidzi, ibnu-majah,
  malik). Benih rawak tetap (`seed 42`) supaya sampel boleh diulang.
- **URL:** dibina sebagai `sunnah.com/{slug}/{book}/{hadith}` dengan
  `book`/`hadith` daripada rujukan dalam-buku sunnah.com.
- **Pengesahan:** muat halaman sebenar, kemudian sahkan teks CDN
  (rujukan dalam-buku) hadir dalam halaman — perbandingan tanpa ruang
  untuk mengelak artifak HTML.
- **Jeda 3 saat** antara muat turun (hormati sunnah.com). Ralat muat
  turun (403/offline) dikira NOTA, bukan kegagalan — audit hanya gagal
  pada ketidakpadanan yang DISAHKAN.
- **Tarikh larian:** 11 Ogos 2026, `python semak.py --audit-sunnah=50`.

## Keputusan

| Ukuran | Bilangan |
|---|---|
| Dipadan (pautan betul) | 50 |
| Tidak padan | 0 |
| Tidak dapat disahkan (NOTA) | 0 |
| **Jumlah sampel** | **50** |

Liputan sampel mengikut kitab: bukhari 13, nasai 11, muslim 11,
tirmidzi 7, abu-daud 4, ibnu-majah 4, malik 0 (tiada dalam sampel
rawak kali ini).

## Jadual 50 sampel

| # | Hadis (hadis.my) | Pautan sunnah.com |
|---|---|---|
| 1 | `nasai#814` | <https://sunnah.com/nasai/10/47> |
| 2 | `bukhari#3821` | <https://sunnah.com/bukhari/64/178> |
| 3 | `bukhari#841` | <https://sunnah.com/bukhari/11/15> |
| 4 | `nasai#4253` | <https://sunnah.com/nasai/42/65> |
| 5 | `muslim#2383` | <https://sunnah.com/muslim/15/468> |
| 6 | `muslim#1350` | <https://sunnah.com/muslim/6/322> |
| 7 | `muslim#615` | <https://sunnah.com/muslim/4/73> |
| 8 | `bukhari#4782` | <https://sunnah.com/bukhari/67/115> |
| 9 | `nasai#4086` | <https://sunnah.com/nasai/39/8> |
| 10 | `bukhari#3518` | <https://sunnah.com/bukhari/63/27> |
| 11 | `nasai#2039` | <https://sunnah.com/nasai/21/249> |
| 12 | `nasai#4224` | <https://sunnah.com/nasai/42/36> |
| 13 | `ibnu-majah#3806` | <https://sunnah.com/ibnmajah/33/160> |
| 14 | `tirmidzi#1549` | <https://sunnah.com/tirmidhi/22/6> |
| 15 | `bukhari#2977` | <https://sunnah.com/bukhari/59/27> |
| 16 | `tirmidzi#3064` | <https://sunnah.com/tirmidhi/47/191> |
| 17 | `abu-daud#2043` | <https://sunnah.com/abudawud/14/80> |
| 18 | `bukhari#1076` | <https://sunnah.com/bukhari/19/25> |
| 19 | `bukhari#1009` | <https://sunnah.com/bukhari/17/5> |
| 20 | `bukhari#3212` | <https://sunnah.com/bukhari/60/138> |
| 21 | `muslim#459` | <https://sunnah.com/muslim/3/20> |
| 22 | `muslim#932` | <https://sunnah.com/muslim/5/174> |
| 23 | `tirmidzi#201` | <https://sunnah.com/tirmidhi/2/69> |
| 24 | `tirmidzi#3445` | <https://sunnah.com/tirmidhi/48/154> |
| 25 | `bukhari#892` | <https://sunnah.com/bukhari/12/3> |
| 26 | `tirmidzi#2083` | <https://sunnah.com/tirmidhi/32/25> |
| 27 | `bukhari#6798` | <https://sunnah.com/bukhari/96/72> |
| 28 | `nasai#3331` | <https://sunnah.com/nasai/26/189> |
| 29 | `nasai#1159` | <https://sunnah.com/nasai/12/144> |
| 30 | `nasai#2850` | <https://sunnah.com/nasai/24/282> |
| 31 | `tirmidzi#1535` | <https://sunnah.com/tirmidhi/21/73> |
| 32 | `abu-daud#1964` | <https://sunnah.com/abudawud/13/134> |
| 33 | `muslim#522` | <https://sunnah.com/muslim/3/101> |
| 34 | `abu-daud#2939` | <https://sunnah.com/abudawud/23/62> |
| 35 | `tirmidzi#3024` | <https://sunnah.com/tirmidhi/47/151> |
| 36 | `muslim#2486` | <https://sunnah.com/muslim/16/4> |
| 37 | `ibnu-majah#1084` | <https://sunnah.com/ibnmajah/5/292> |
| 38 | `ibnu-majah#3057` | <https://sunnah.com/ibnmajah/25/185> |
| 39 | `bukhari#214` | <https://sunnah.com/bukhari/4/87> |
| 40 | `nasai#4818` | <https://sunnah.com/nasai/46/33> |
| 41 | `ibnu-majah#966` | <https://sunnah.com/ibnmajah/5/174> |
| 42 | `bukhari#5461` | <https://sunnah.com/bukhari/77/131> |
| 43 | `nasai#2744` | <https://sunnah.com/nasai/24/176> |
| 44 | `abu-daud#2066` | <https://sunnah.com/abudawud/14/107> |
| 45 | `muslim#4640` | <https://sunnah.com/muslim/45/25> |
| 46 | `muslim#2476` | <https://sunnah.com/muslim/15/590> |
| 47 | `bukhari#5320` | <https://sunnah.com/bukhari/76/76> |
| 48 | `muslim#349` | <https://sunnah.com/muslim/2/28> |
| 49 | `nasai#4974` | <https://sunnah.com/nasai/48/21> |
| 50 | `muslim#4519` | <https://sunnah.com/muslim/44/188> |

## Penilaian

- **Padanan tepat:** kesemua 50 pautan merentas 6 kitab membuka hadis
  yang betul di sunnah.com — terjemahan hadis.my ↔ sunnah.com
  (book/hadith dalam-buku) konsisten.
- **Skema penomboran:** nombor hadith sunnah.com mengikut skema
  dalam-buku (cth. `muslim#932` → `muslim/5/174`), berbeza daripada
  penomboran hadis.my — peta `sunnah_map/` menterjemah dengan betul.
- **Nota liputan:** sampel rawak kali ini tiada `malik`; jika mahu
  liputan penuh 7 kitab, jalankan audit berulang kali (benih berubah)
  atau tingkatkan saiz sampel (`--audit-sunnah=100`).
- **Cadangan:** jalankan semula audit ini sebelum setiap hantaran
  versi, terutamanya selepas sebarang perubahan pada peta `sunnah_map/`
  atau penomboran hadis.

## Cara jalankan semula

```bash
python semak.py --audit-sunnah=50   # 50 sampel rawak, ~3 minit
python semak.py                     # gate penuh (lalai luar talian)
```

Ralat muat turun sementara (offline/403) dilaporkan sebagai NOTA, bukan
kegagalan — jalankan semula untuk pengesahan.
