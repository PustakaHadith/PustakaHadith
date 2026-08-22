# Audit Musnad Ahmad — Padanan Arab Digital Tanpa OCR

**Tarikh:** 15 Ogos 2026  
**Status padanan:** ✅ 1,345 padanan teks penuh disahkan terhadap `hadis.db` Windows sebenar  
**Status import:** ⛔ Ditangguhkan — lesen/pengedaran semula belum jelas

---

## 1. Penemuan

Set data `AhmedBaset/hadith-json` mengandungi:

- 1,374 rekod awal Musnad Ahmad dengan Arab digital;
- 1,359 rekod mempunyai terjemahan Inggeris sunnah.com/Darussalam;
- nombor 1–1,359 tersusun berterusan untuk bahagian yang diterjemahkan.

Ini membolehkan bahagian awal dipadan tanpa OCR PDF. Teks Arab penuh menjadi
jambatan kepada 26,363 hadis projek.

## 2. Kaedah

1. Pin sumber kepada komit GitHub tertentu.
2. Sahkan SHA-256 fail sumber.
3. Normalisasi Arab menggunakan prinsip yang sama seperti
   `core/eng_source.py`.
4. Padan **keseluruhan teks Arab**, bukan nombor atau awalan.
5. Terima hanya:
   - satu kunci sumber ↔ satu `hadis_id`; atau
   - kumpulan teks Arab yang benar-benar identik dengan bilangan rekod sama,
     dipasangkan mengikut turutan.
6. Tolak semua kes lain.

Skrip `audit_ahmad_digital.py` membuka `hadis.db` dalam mod baca sahaja dan
tidak mempunyai pilihan `--terap`.

## 3. Keputusan

| Kategori | Bilangan |
|---|---:|
| Sumber mempunyai Inggeris | 1,359 |
| Padanan teks penuh unik | 1,337 |
| Pendua Arab identik, diselesaikan ikut turutan | 8 |
| **Jumlah diterima** | **1,345** |
| Ditolak | 14 |

Kes pendua terdiri daripada empat pasangan teks Arab identik. Setiap rekod
sasaran digunakan sekali sahaja; tiada pemilihan nombor secara rawak.

Empat belas rekod ditolak kerana perbezaan segmentasi antara edisi, contohnya:

- satu rekod sumber menggabungkan dua rekod sasaran;
- dua rekod sumber terkandung dalam satu rekod sasaran;
- tambahan/pemotongan sanad atau laporan ulangan.

Walaupun skor kandungan tinggi bagi kes tersebut, semuanya sengaja tidak
dimasukkan ke pemetaan selamat.

## 4. Bukti Nombor Berbeza

Pemetaan digital mengesahkan lagi bahawa nombor Darussalam tidak boleh disalin
sebagai `hadis_id`:

| Darussalam | `hadis_id` projek |
|---:|---:|
| 1 | 1 |
| 699 | 661 |
| 700 | 662 |
| 701 | 663 |
| 1200 | 1138 |

## 5. Fail

- `dokumen/rujukan/audit_ahmad_digital.py`
- `dokumen/rujukan/ahmad_digital_exact_mapping_1_1359.json`

Fail pemetaan tidak mengandungi teks Inggeris atau Arab penuh. Ia hanya
menyimpan nombor, kaedah dan SHA-256 sebagai bukti audit.

## 6. Cara Jalankan pada DB Pengguna

```powershell
python dokumen/rujukan/audit_ahmad_digital.py
```

Keputusan yang dijangka jika DB sepadan:

```text
Hadis Ahmad DB          : 26,363
Sumber ada Inggeris     : 1,359
Padanan tepat diterima  : 1,345
  unik                  : 1,337
  pendua ikut turutan   : 8
Ditolak                 : 14
Tiada perubahan dibuat pada hadis.db.
```

## 7. Lesen dan Pengedaran — Halangan Disahkan

Repositori mempunyai metadata pakej `ISC`, tetapi tiada fail `LICENSE`, dan
data dinyatakan sebagai hasil scrape sunnah.com. Sunnah.com secara eksplisit
menyatakan bahawa mereka tidak membenarkan scraping atau pengeluaran semula
koleksi/buku secara besar-besaran. Mereka mengarahkan pemohon kepada API dan
permohonan data luar talian.

Terjemahan Musnad Ahmad pula diterbitkan Darussalam sebagai karya “All Rights
Reserved”. Oleh itu lesen metadata repositori pihak ketiga tidak mengatasi hak
sunnah.com/Darussalam.

Keputusan:

- pemetaan nombor/SHA boleh digunakan sebagai audit dalaman;
- teks terjemahan **tidak boleh dibundel** sekarang;
- hOCR besar-besaran ditangguhkan kerana menghasilkan teks berhak cipta yang
  sama;
- permohonan bertulis disediakan dalam
  `dokumen/rujukan/PERMOHONAN_LESEN_AHMAD.md`.

## 8. Kesan kepada Kerja OCR

Sebanyak 1,345 terjemahan awal kini mempunyai pemetaan berasaskan teks Arab
digital penuh, jauh lebih kuat daripada OCR. Kerja hOCR seterusnya boleh
menumpukan bahagian yang tiada sumber digital dan tidak perlu mengulang
bahagian ini.

*Rujukan silang: `AHMAD_HOCR.md` dan `TERJEMAHAN_AHMAD_DARIMI.md`.*
