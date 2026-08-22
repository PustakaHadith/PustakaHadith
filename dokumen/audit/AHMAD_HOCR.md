# Audit Padanan Musnad Ahmad — Segmentasi Koordinat hOCR

**Tarikh audit:** 15 Ogos 2026  
**Status:** Kaedah baharu berjaya pada sampel disahkan; **belum diluluskan untuk import produksi**  
**Skop:** Darussalam Jilid 1–4, data Arab 26,363 hadis projek, koordinat OCR dan padanan teks

> **Kemas kini:** 1,345 terjemahan awal kini mempunyai padanan lebih kuat
> berasaskan Arab digital penuh, tanpa OCR. Lihat `AHMAD_DIGITAL.md`.
> Sunnah.com melarang scraping/pengeluaran semula koleksi dan buku Darussalam
> ialah “All Rights Reserved”; maka kerja hOCR besar-besaran **ditangguhkan**
> sehingga kebenaran bertulis diterima.

---

## 1. Ringkasan Eksekutif

Audit terdahulu betul dalam satu kesimpulan utama: padanan nombor terus tidak
selamat dan padanan berdasarkan blob satu muka surat gagal. Walau bagaimanapun,
audit lanjutan menemui dua perkembangan besar:

1. **Nombor hadis.my dapat diuji tanpa `hadis.db` pengguna.** Repositori
   `abdelrahmaan/Hadith-Data-Sets` mempunyai kiraan yang tepat sama dengan
   projek — 62,169 keseluruhan dan 26,363 untuk Musnad Ahmad — serta teks
   hadis #1 yang sama dengan hadis.my.
2. **Segmentasi menggunakan koordinat lajur Inggeris berjaya.** Nombor hadis
   pada lajur Inggeris lebih mudah dibaca OCR. Koordinat menegaknya digunakan
   untuk memotong hadis Arab di lajur kanan pada aras yang sama. Ini membuang
   pencemaran utama kaedah lama: 2–4 hadis bercampur dalam satu blob halaman.

Lima pasangan yang disahkan semuanya dipilih dengan undi **3/3 varian OCR**:

| Darussalam | `hadis_id` projek/data Arab | Skor terbaik | Keputusan |
|---:|---:|---:|---|
| 1 | 1 | 0.443 | Lulus |
| 699 | 661 | 0.386 | Lulus |
| 700 | 662 | 0.371 | Lulus |
| 701 | 663 | 0.667 | Lulus |
| 1200 | 1138 | 0.509 | Lulus |

Ini turut membuktikan bahawa **nombor Darussalam tidak boleh disalin terus** ke
`hadis_id`. Contohnya, Darussalam #700 bukan hadis.my #700 tetapi #662.

---

## 2. Pembetulan Penemuan Jilid Darussalam

Audit lama menyatakan hanya Jilid 1–3 ditemui. Maklumat itu kini dibetulkan:

| Jilid | Julat Darussalam | Status |
|---:|---:|---|
| 1 | 1–1380 | PDF dwibahasa dan OCR ditemui |
| 2 | 1381–2822 | PDF dwibahasa dan OCR ditemui |
| 3 | 2823–4376 | PDF dwibahasa dan OCR ditemui |
| 4 | 4377–6030 | **PDF Darussalam Inggeris–Arab ditemui di Archive.org** |
| 5 | 6031–7624 | Diterbitkan Darussalam; PDF Inggeris terbuka belum disahkan |
| 6 | 7625–9344 | Diterbitkan Darussalam; PDF Inggeris terbuka belum disahkan |

Dua fail Archive.org bernama “Volume 5 By RMP” dan “Volume 6 By RMP” telah
**dimuat turun dan diperiksa secara visual**. Kedua-duanya ialah edisi **Urdu**,
bukan terjemahan Inggeris Darussalam, lalu tidak digunakan.

Siri ini masih hanya bahagian awal Musnad; penerbit menyatakan rancangan
lengkap lebih banyak jilid. Frasa sesetengah kedai bahawa “complete English
translation ... in six volumes” bercanggah dengan julat sebenar yang berhenti
pada #9344 dan perlu dianggap keterangan jualan yang tidak tepat.

---

## 3. Aset Inggeris Jilid 1–4

Skrip `ekstrak_ahmad_darussalam.py` kini menyokong Jilid 4. OCR Jilid 4 kerap
mengganti titik selepas nombor dengan koma, sempang, asterisk atau garis miring;
mod penanda longgar digunakan **untuk Jilid 4 sahaja**.

| Jilid | Berjaya diekstrak | Julat | Liputan |
|---:|---:|---:|---:|
| 1 | 1,290 | 1,380 | 93.5% |
| 2 | 1,344 | 1,442 | 93.2% |
| 3 | 1,424 | 1,554 | 91.6% |
| 4 | 1,469 | 1,654 | 88.8% |
| **Jumlah** | **5,527** | **6,030** | **91.7%** |

Fail:

- `ahmad_darussalam_1_4376.json` — fail lama dikekalkan untuk keserasian.
- `ahmad_darussalam_1_6030.json` — fail baharu Jilid 1–4, 5,527 entri.

**Had kualiti:** ini tetap OCR, bukan teks digital rasmi. Kesalahan huruf,
baris terpotong dan teks lajur Arab yang tersalah baca sebagai Latin masih
wujud. Semakan manusia dan urusan kebenaran pengedaran semula masih wajib.

---

## 4. Mengapa Kaedah Lama Gagal

Kaedah lama menggabungkan seluruh lajur Arab satu muka surat. Pada contoh
Darussalam #700:

- skor pasangan betul: 0.577;
- kedudukan pasangan betul: #238 daripada 3,929;
- calon salah tertinggi: 0.981.

Masalahnya bukan semata-mata ambang skor. Blob itu mengandungi hadis #699,
#700, #701, kepala halaman dan takhrij. Banyak formula sanad yang berulang
menjadikan calon salah kelihatan sangat serupa.

Percubaan membahagi blob mengikut nisbah panjang terjemahan juga gagal kerana
kedudukan teks Arab kanan-ke-kiri tidak berkadar terus dengan panjang teks
Inggeris kiri-ke-kanan.

---

## 5. Kaedah Koordinat Baharu

Aliran yang diuji:

1. Ambil koordinat nombor hadis daripada DjVu XML/hOCR lajur Inggeris.
2. Tukar koordinat relatif kepada saiz imej PDF yang dirender.
3. Potong lajur Arab pada aras menegak antara nombor semasa dan nombor
   berikutnya.
4. Beri margin kiri/kanan yang lebih luas supaya huruf Arab tidak terpotong.
5. Jalankan tiga varian OCR:
   - model standard, PSM 4, ambang binari 190;
   - model terbaik, PSM 3, imej mentah;
   - model terbaik, PSM 6, autokontras.
6. Normalisasi Arab dan kira Sørensen–Dice trigram terhadap 26,363 calon.
7. Gunakan undi tiga varian, bukan skor satu OCR sahaja.

Manifest koordinat prahitung:

- `ahmad_hocr_manifest_1_4376.json`
- 4,058 entri yang mempunyai terjemahan Inggeris berjaya diekstrak.
- SHA-256 tiga PDF disimpan dalam manifest bagi mencegah koordinat digunakan
  pada edisi/pindaian yang salah.

---

## 6. Keputusan Ujian Berstrata 87 Hadis

Sampel diambil merentas Jilid 1–3 dan pelbagai bahagian nombor. Keputusan yang
boleh diperhatikan tanpa menganggap jawapan automatik sentiasa betul:

| Persetujuan tiga varian OCR | Bilangan | Peratus |
|---|---:|---:|
| 3 daripada 3 memilih calon sama | 64 | 73.6% |
| 2 daripada 3 memilih calon sama | 18 | 20.7% |
| Ketiga-tiga memilih calon berbeza | 5 | 5.7% |
| **Jumlah** | **87** | **100%** |

Contoh urutan yang konsisten:

- Darussalam #699 → hadis.my #661
- Darussalam #700 → hadis.my #662
- Darussalam #701 → hadis.my #663

Sampel gagal pada OCR tunggal seperti #200 dan #201 pulih kepada #195 dan
#196 selepas margin potongan dibesarkan dan tiga varian digunakan.

**Peringatan:** persetujuan model bukan bukti muktamad ketepatan. Beberapa
hadis yang menyatakan “laporan serupa” boleh berkongsi teks Arab/ID sasaran,
dan beberapa calon salah masih menerima undi majoriti. Penjajaran global
mengikut turutan serta semakan manusia tetap diperlukan.

---

## 7. Keputusan Keselamatan

| Tindakan | Keputusan |
|---|---|
| Import nombor Darussalam terus | **Dilarang** — dibuktikan tidak sepadan |
| Import hasil skrip blob lama | **Dilarang** — kegagalan #238/3,929 |
| Jalankan `audit_padan_ahmad_hocr.py` pada sampel | **Selamat** — baca/audit sahaja |
| Import semua keputusan hOCR sekarang | **Belum diluluskan** |
| Simpan aset Inggeris/manifest untuk kerja lanjut | **Diluluskan** |

Skrip `audit_padan_ahmad_hocr.py` sengaja:

- tidak membuka `hadis.db`;
- tidak mempunyai pilihan `--terap`;
- hanya menulis laporan JSON audit;
- mengesahkan SHA-256 PDF sebelum menggunakan koordinat.

---

## 8. Langkah Seterusnya yang Disyorkan

1. **Bina penjajaran global monotonik** antara turutan 4,058 entri Darussalam
   dan data Arab projek. Calon mesti bergerak ke hadapan; padanan rawak jauh
   daripada jiran perlu ditolak.
2. Jalankan OCR asas pada semua entri, kemudian jalankan dua varian tambahan
   hanya bagi skor/margin rendah untuk menjimatkan masa.
3. Tangani 188 jurang terjemahan yang sempadan berikutnya melangkau satu atau
   lebih nombor; pulihkan sempadan daripada penanda OCR bukan piawai dahulu.
4. Pilih hanya subset keyakinan tinggi dan semak sekurang-kurangnya 100
   pasangan secara manual, termasuk hadis pendek, laporan serupa dan rentas
   halaman.
5. Dapatkan pandangan penyemak fasih Arab sebelum sebarang import produksi.
6. Sahkan lesen/kebenaran Darussalam untuk pengedaran semula teks terjemahan.

**Import produksi kekal ditangguhkan sehingga semua syarat di atas selesai.**

---

## 9. Fail Berkaitan

- `dokumen/rujukan/audit_padan_ahmad_hocr.py`
- `dokumen/rujukan/ahmad_hocr_manifest_1_4376.json`
- `dokumen/audit/AHMAD_HOCR_SAMPEL_5.json` — bukti lima sampel lulus 3/3
- `dokumen/rujukan/ekstrak_ahmad_darussalam.py`
- `dokumen/rujukan/ahmad_darussalam_1_4376.json`
- `dokumen/rujukan/ahmad_darussalam_1_6030.json`
- `dokumen/rujukan/padan_ahmad_darussalam.py` — kaedah lama, kekal disekat
- `dokumen/audit/TERJEMAHAN_AHMAD_DARIMI.md`

---

## 10. Rujukan

- Data Arab 62,169 hadis:
  `https://github.com/abdelrahmaan/Hadith-Data-Sets`
- Hadis.my Musnad Ahmad:
  `https://hadis.my/kitab/musnad-ahmad`
- Darussalam Jilid 1:
  `https://archive.org/details/EnglishTranslationOfMusnadImamAhmedBinHanbalVolume1`
- Darussalam Jilid 2–3:
  `https://archive.org/details/musnad-imam-ahmad-bin-hanbal-volume-1-3`
- Darussalam Jilid 4:
  `https://archive.org/details/musnadahmadvol.4final`
- Jilid 5 (julat 6031–7624):
  `https://darussalam.com/english-translation-of-musnad-imam-ahmad-bin-hanbal-vol-5-hadith-6031-7624/`
- Jilid 6 (julat 7625–9344):
  `https://darussalamus.com/products/english-translation-of-musnad-imam-ahmad-bin-hanbal-vol-6-hadith-7625-9344-by-imam-ahmed-bin-hanbal`
- Sunnah.com sampel:
  `https://sunnah.com/ahmad:1`, `:699`, `:700`, `:701`, `:1200`

*Rujukan silang: `TERJEMAHAN_AHMAD_DARIMI.md` dan `GTAF.md`.*
