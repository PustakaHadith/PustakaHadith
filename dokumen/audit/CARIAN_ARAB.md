# Audit Carian Arab Tanpa Tashkeel — Skema 8

**Tarikh:** 15 Ogos 2026  
**Status kod:** ✅ Dilaksanakan dan lulus ujian  
**Status `hadis.db` pengguna:** ✅ Disahkan pada salinan konsisten DB Windows sebenar (62,169 hadis)

---

## 1. Masalah

FTS5 `unicode61 remove_diacritics 2` membuang aksen Latin tetapi tidak membuang
harakat Arab. Indeks lama menyimpan `arab` bertashkeel, menyebabkan query biasa
seperti `كتب` tidak menemui teks `كَتَبَ`.

## 2. Pelaksanaan Semasa

Versi Drive terkini telah mempunyai perubahan berikut:

- `db.py`
  - `SKEMA_VERSI = 8`;
  - fungsi `bersih_tashkeel()`;
  - lajur `hadis.arab_carian`;
  - FTS5 mengindeks `melayu, arab_carian`;
  - migrasi/backfill Python untuk DB versi 7;
  - bina semula FTS dan trigger;
  - normalisasi query pengguna dalam `_to_match_query()`;
  - pemulihan indeks jika migrasi terganggu.
- `sync.py`
  - setiap rekod baharu mengisi `arab_carian=bersih_tashkeel(arab)`.
- `api/hadis_api.py`
  - tiada perubahan diperlukan kerana menggunakan fungsi carian `db.py`.

Paparan masih menggunakan `hadis.arab` asal bertashkeel; hanya indeks carian
menggunakan bentuk bersih.

## 3. Keputusan Ujian

Pelaksanaan Drive diuji dengan SQLite/FTS5 sebenar:

| Ujian | Keputusan |
|---|---|
| Migrasi DB lama versi 7 → 8 | ✅ Lulus |
| Semua data lama dikekalkan | ✅ Lulus |
| Backfill `arab_carian` | ✅ 0 NULL |
| Definisi FTS lama diganti | ✅ Lulus |
| Trigger INSERT | ✅ Lulus |
| Trigger UPDATE (buang token lama + tambah token baharu) | ✅ Lulus |
| Trigger DELETE | ✅ Lulus |
| Migrasi dijalankan kali kedua | ✅ Idempoten |
| DB baharu terus pada skema 8 | ✅ Lulus |
| Pemulihan indeks migrasi terganggu | ✅ Lulus |
| `sync.simpan()` mengisi `arab_carian` | ✅ Lulus |
| `كتب` dan `كَتَبَ` memberi hasil sama | ✅ Lulus |
| `نية` dan `نِيَّة` dinormalisasi sama | ✅ Lulus |
| `ة` dan `ه` tidak dilipat | ✅ Lulus |
| Migrasi sintetik 62,169 baris | ✅ Lulus, kira-kira 1.28 saat dalam sandbox |
| Salinan konsisten DB Windows sebenar | ✅ Lulus, 62,169 hadis dalam 11.62 saat |
| `كتب` = `كَتَبَ` | ✅ 767 hasil bagi kedua-duanya |
| `نية` = `نِيَّة` | ✅ 10 hasil bagi kedua-duanya |
| `الله` = `اللَّهِ` | ✅ 60,211 hasil bagi kedua-duanya |
| Regresi BM `niat` / `puasa` / `hukum riba` | ✅ 115 / 911 / 486 hasil |

## 4. Skrip Ujian Selamat

`uji_carian_arab.py`:

1. membuka `hadis.db` asal dalam mod baca sahaja;
2. menggunakan SQLite Backup API supaya keadaan WAL turut disalin secara
   konsisten;
3. menjalankan migrasi dan ujian pada fail sementara;
4. memadam fail sementara selepas selesai;
5. tidak mengubah DB asal.

Jalankan dari root projek dengan aplikasi ditutup:

```powershell
python uji_carian_arab.py
```

Output yang diperlukan:

```text
LULUS struktur: skema 8, ... hadis, 0 NULL, 3 trigger
LULUS Arab 'كتب' = 'كَتَبَ': ... hasil
LULUS prinsip: harakat dibuang, ة dan ه tidak dilipat
LULUS trigger FTS: INSERT, UPDATE dan DELETE
SEMUA UJIAN LULUS
hadis.db asal TIDAK berubah
```

## 5. Cara Terap pada DB Produksi

Hanya selepas ujian salinan lulus:

```powershell
# Pastikan aplikasi ditutup dahulu
Copy-Item hadis.db hadis.db.sebelum_carian_arab.bak

# db.init() menjalankan migrasi sebenar
python -c "import db; c=db.init(); print('versi', db.versi(c)); c.close()"

python semak_db.py
python semak.py
python uji_carian_arab.py
python main.py
```

Ujian manual dalam aplikasi:

- `كتب`
- `كَتَبَ`
- `نية`
- `نِيَّة`
- regresi Melayu: `niat`, `puasa`, `hukum riba`

## 6. Keputusan Keselamatan

| Tindakan | Status |
|---|---|
| Salin `db.py` dan `sync.py` versi Drive terkini | ✅ Disahkan sintetik |
| Jalankan `uji_carian_arab.py` | ✅ Selamat; DB asal baca sahaja |
| Migrasi DB produksi tanpa sandaran | ❌ Dilarang |
| Lipat `ة→ه` dalam carian pengguna | ❌ Dilarang |
| Gunakan `core.eng_source.normalisasi()` untuk FTS | ❌ Dilarang; terlalu agresif |

*Rujukan silang: `dokumen/rujukan/DRAF_carian_arab.md` dan
`dokumen/audit/GTAF.md`.*
