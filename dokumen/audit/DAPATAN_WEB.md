# Dapatan Web — sunnah.com (11 Ogos 2026)

> Dapatan daripada siasatan web sunnah.com, dorar.net, dan
> semakhadis.com: laman utama, halaman hadis, corak URL, skema
> penomboran, audit pautan "Baca penuh" (semak.py 8o), dan
> perkhidmatan API (dorar.net + SemakHadis). Rujukan audit penuh:
> `dokumen/audit/AUDIT_SUNNAH.md`.

## 1. Laman utama — `https://sunnah.com/`

- **Tajuk:** "Sunnah.com — Sayings and Teachings of Prophet Muhammad
  (صلى الله عليه و سلم)". Tagline: "The Hadith of the Prophet Muhammad
  at your fingertips".
- **Navigasi atas:** Qur'an | Sunnah | Prayer Times | Audio, dengan
  pautan sokongan/derma.
- **The Nine Books** (الكتب التسعة): Sahih al-Bukhari, Sahih Muslim,
  Sunan an-Nasa'i, Sunan Abi Dawud, Jami' at-Tirmidhi, Sunan Ibn Majah,
  Muwatta Malik, Musnad Ahmad, Sunan ad-Darimi — sama dengan 9 kitab
  dalam aplikasi Pustaka Hadith.
- **Koleksi lain:** Ibn Khuzayma, Ibn Hibban, Mustadrak al-Hakim,
  Musannaf 'Abd ar-Razzaq, Musannaf Ibn Abi Shayba, Sunan
  ad-Daraqutni, al-Kubra (Bayhaqi), Nasa'i al-Kubra, al-Adab al-Mufrad,
  ash-Shama'il al-Muhammadiyah, Nawawi 40, Riyad as-Salihin, Mishkat
  al-Masabih, Bulugh al-Maram, Hisn al-Muslim.
- **Carian:** sintaks lanjutan — petikan `"..."`, wildcard `test*`,
  kabur `swore~`, pemberat `pledge^4`, operator boolean
  `("a" OR "b") AND c`.
- **Bahasa disokong laman:** Inggeris, Arab, Urdu, Bangla — **tiada
  Melayu/Indonesia**. Implikasi: pautan "Baca penuh" dari Pustaka
 Hadith membuka halaman Inggeris.
- **Status HTTP:** 200 (HTTPS), halaman berfungsi.

## 2. Halaman hadis dalam buku — contoh `https://sunnah.com/bukhari/1/1`

- **Tajuk:** "Sahih al-Bukhari 1 — Revelation — Sunnah.com".
- **Serbuk roti:** Home » Sahih al-Bukhari » Revelation » Hadith 1.
- **Bab:** tajuk bab Inggeris + Arab (كتاب بدء الوحى), dengan tajuk
  kecil bab (كتاب كَيْفَ كَانَ بَدْءُ الْوَحْىِ...).
- **Isi hadis:** riwayat penuh — terjemahan Inggeris + teks Arab
  dengan harakat penuh.
- **Rujukan tiga bentuk:**
  1. "Sahih al-Bukhari 1" (nombor sunnah.com),
  2. **In-book reference:** Book 1, Hadith 1 — sumber peta
     `sunnah_map/`,
  3. USC-MSA web (English) reference: Vol. 1, Book 1, Hadith 1 —
     ditanda "(deprecated numbering scheme)".
- **Alat halaman:** Report Error | Share | Copy; paparan hadis boleh
  ditukar (Arabic / Translation / Grade / Reference / Concise /
  Detailed / URL).
- **Navigasi:** nombor hadis seterusnya ("2") — paging mengikut
  nombor sunnah.com, bukan penomboran hadis.my.
- **Status HTTP:** 200.

## 3. Corak URL + pemetaan slug

Corak pautan "Baca penuh": `https://sunnah.com/{slug}/{book}/{hadith}`.

| Kitab | Slug hadis.my | Slug sunnah.com |
|---|---|---|
| Sahih al-Bukhari | bukhari | bukhari |
| Sahih Muslim | muslim | muslim |
| Sunan an-Nasa'i | nasai | nasai |
| Sunan Abu Daud | abu-daud | **abudawud** |
| Sunan al-Tirmizi | tirmidzi | **tirmidhi** |
| Sunan Ibnu Majah | ibnu-majah | **ibnmajah** |
| Muwatta' Malik | malik | malik |
| Musnad Ahmad | ahmad | ahmad |
| Sunan al-Darimi | darimi | darimi |

`book`/`hadith` ialah rujukan dalam-buku sunnah.com (bukan penomboran
hadis.my). Terjemahan dibuat oleh peta `sunnah_map/{slug}.json`
(7 kitab: bukhari, muslim, nasai, abu-daud, tirmidzi, ibnu-majah,
malik — ahmad/darimi tiada terjemahan Inggeris).

## 4. Skema penomboran

- sunnah.com menombori hadis mengikut **skema dalam-buku** (book,
  hadith). Nombor hadith sunnah.com berbeza daripada penomboran global
  hadis.my.
- Contoh daripada audit: `muslim#932` (hadis.my) → `muslim/5/174`
  (sunnah.com); `bukhari#3821` → `bukhari/64/178`.
- Halaman sunnah.com turut memapar nombor USC-MSA (web) lama dengan
  label "deprecated" — jangan guna sebagai asas peta.

## 5. Keputusan audit pautan "Baca penuh" (semak.py 8o)

- `python semak.py --audit-sunnah=50` (11 Ogos 2026):
  **50 dipadan, 0 tidak padan, 0 tidak dapat disahkan (dari 50)**.
- Setiap pautan dimuat dan teks rujukan dalam-buku disahkan hadir
  dalam halaman (bandingan tanpa ruang, elak artifak HTML).
- Semak.py penuh: **SEMUA LULUS**. Butiran penuh: `dokumen/audit/AUDIT_SUNNAH.md`.

## 6. Penilaian dan implikasi

- **Kestabilan:** 50 muat turun dengan jeda 3 saat — tiada 403/sekatan
  kadar; laman berfungsi dengan baik.
- **Pemetaan tepat:** peta `sunnah_map/` menterjemah penomboran
  hadis.my → dalam-buku dengan betul (50/50).
- **Had bahasa:** sunnah.com tiada Melayu — "Baca penuh" sentiasa
  membuka Inggeris. Ini selari dengan reka bentuk semasa (pautan
  tambahan, bukan pengganti bacaan dalam app).
- **Jaring keselamatan:** semakan 8o ialah perlindungan terhadap
  perubahan penomboran/struktur sunnah.com — jalankan semula sebelum
  setiap hantaran versi.
- **Cadangan penambahbaikan:**
  - Sampel lebih besar (`--audit-sunnah=100`) atau benih berbeza untuk
    liputan lebih luas (sampel rawak kali ini tiada `malik`).
  - Sekiranya sunnah.com menukar struktur halaman, semakan 8o akan
    menandakan ketidakpadanan — semak output "NOTA" (ralat muat turun)
    dengan teliti, bukan hanya GAGAL.
  - Peta `sunnah_map/` dijana oleh `sync_english.py --peta-sunnah` —
    audit mengesahkan hasilnya terhadap halaman sebenar.

## 7. Cara siasat semula

```bash
python semak.py --audit-sunnah=50   # audit pautan (seksyen 8o)
python semak.py                     # gate penuh
```

Untuk pemeriksaan manual: `read_url`/pelayar pada
`https://sunnah.com/{slug}/{book}/{hadith}`.

---

## 8. dorar.net — Al-Mawsu'a al-Hadithiyya (Hadith Encyclopedia)

Dua halaman disiasat (11 Ogos 2026): laman ensiklopedia
(`https://dorar.net/hadith`) dan artikel API rasmi
(`https://dorar.net/article/389/...-API`). Kedua-duanya status HTTP
**200**. Endpoint API turut diuji langsung.

### 8.1 Laman ensiklopedia hadis (`/hadith`)

- **الدرر السنية (Dorar Saniyyah)** — rangkaian ensiklopedia Islam
  Arab: Tafsir, Hadith, Aqidah, agama, sekte, Fiqh, Usul Fiqh, kaedah
  fiqh, akhlak, adab, sejarah, bahasa Arab.
- **Al-Mawsu'a al-Hadithiyya** — "ensiklopedia hadis terbesar" untuk
  mengetahui hadis sahih/daif ikut penghakiman ulama; huraian hadis
  sahih di bawah penyeliaan ilmiah (Jawatankuasa Pengawasan Ilmiah;
  metodologi fiqh disahkan Persatuan Fiqh Arab Saudi).
- **Kandungan:** teks hadis penuh (الحديث كاملاً), tanpa syakal
  (بدون تشكيل), klasifikasi tematik (آفات اللسان، أدعية وأذكار،
  أشراط الساعة، مناقب وفضائل...), carian tematik (البحث الموضوعي),
  cetakan yang diiktiraf (الطبعات المعتمدة), rujukan syarah,
  gharib al-hadith, biografi perawi (تراجم المحدثين), syarah
  mudah.
- **Bahasa:** antara muka Arab; ada versi Inggeris ("English");
  aplikasi mudah alih + kedai.
- Perlu pendaftaran/log masuk untuk fungsi lanjutan.

### 8.2 Artikel API rasmi (article/389)

"خدمة واجهة الموسوعة الحديثية API" — perkhidmatan untuk pemilik
laman web/forum memaparkan hasil carian hadis menggunakan **JSON**:

- **Endpoint:** `https://dorar.net/dorar_api.json?skey={perkataan}`
  (GET, tiada kunci API).
- **Kaedah 1 — JavaScript/JSONP:**
  `$.getJSON("https://dorar.net/dorar_api.json?skey=" + k +
  "&callback=?", fn)` — `data.ahadith` dipapar; `item.th` = teks
  hadis. Kod sedia: `dorar_json_api.js.zip`.
- **Kaedah 2 — PHP:** `file_get_contents(...dorar_api.json?skey=...)`
  + `json_decode`. Kod sedia: `dorar_api.zip`.
- Hasil disertakan kelas CSS untuk kawalan gaya.
- Sokongan teknikal melalui e-mel dorar.net.

### 8.3 Ujian endpoint langsung

`https://dorar.net/dorar_api.json?skey=كان رسول الله` → **200,
application/json**. Bentuk respons:

```json
{ "ahadith": { "result": "<rentetan HTML>" } }
```

Setiap hadis dalam `result` (rentetan HTML, bukan objek JSON):

- `<div class="hadith">` — teks hadis Arab; kata kunci padanan
  dibalut `<span class="search-keys">`.
- `<div class="hadith-info">` — maklumat: **الراوي** (perawi),
  **المحدث** (ulama yang menilai), **المصدر** (sumber/kitab),
  **الصفحة أو الرقم** (rujukan halaman), **خلاصة حكم المحدث**
  (ringkasan hukum — contoh: `حسن`, `[صحيح]`, atau ayat bebas seperti
  "dalam sanadnya ada perawi daif").
- Pemisah antara hadis: `--------------`.

### 8.4 Analisis dan implikasi untuk Pustaka Hadith

**Kekuatan:**

- Sumber **penilaian sahih/daif** ikut ulama (dengan sumber + rujukan)
  — boleh melengkapkan paparan "status hadis" (SemakHadis/darjat)
  sedia ada.
- Percuma, tiada kunci API, GET ringkas, sokongan JSONP (merentas
  domain untuk web).

**Had dan cabaran:**

- **Bahasa Arab sahaja** — tiada terjemahan Melayu/Indonesia dalam
  respons; antara muka utama Arab (versi Inggeris ada tetapi API
  pulang Arab). Sesuai sebagai pelengkap, bukan pengganti hadis.my.
- **Respons HTML dalam JSON** — bukan data berstruktur; perlu
  `html.parser` untuk mengasingkan teks + maklumat.
- **Tiada penomboran per kitab** (book/hadith seperti sunnah.com) —
  sukar memaut ID hadis.my ke item dorar.net; perlukan padanan teks
  ternormal (seperti JACCARD untuk HadeethEnc/Sema).
- **Hukum berbentuk ayat bebas** (bukan enum) — pengekstrakan status
  (sahih/hasan/daif) perlukan pengelasan teks, bukan bacaan terus.
- Kebergantungan jaringan; had kadar penggunaan tidak didokumenkan;
  syarat penggunaan komersial tidak disemak.

**Cadangan:**

- Jangan ganti sumber sedia ada (hadis.my untuk terjemahan,
  sunnah.com untuk pautan dalam-buku).
- Jika mahu: ciri pilihan — carian teks Arab ternormal → ambil
  "حكم" (hukum) daripada hasil pertama → papar dalam bahasa Melayu
  dengan atribusi dorar.net. Letakkan di luar laluan lalai supaya
  aplikasi kekal luar talian dahulu.
- Uji dengan sampel hadis daripada 9 kitab sebelum memutuskan
  kelayakan integrasi.

---

## 9. semakhadis.com — Semak Status Hadis (Bahasa Melayu)

Siasatan (11 Ogos 2026): laman utama `https://semakhadis.com/` +
ujian langsung API carian. Status HTTP **200**.

### 9.1 Laman utama

- **Tajuk:** "Semak Hadis — Semak Status Hadis Dengan Mudah". Misi:
  semak hadis **sebelum sebar**.
- **Contoh utama (hero):** "Sesiapa yang berdusta atasku dengan
  sengaja, maka siaplah tempat duduknya dalam neraka." — Riwayat
  al-Bukhari (122) dan Muslim (3).
- **Skala kesahihan 4 tahap** dipapar terus:
  - **Sahih** — sanad + matan kukuh
  - **Hasan** — baik, diterima pakai
  - **Da'if** — lemah, perlu berhati-hati
  - **Mawdu'/Palsu** — rekaan, wajib dijauhi
- Statistik paparan (ulama/pengkaji hadis, jumlah hadis, pelawat);
  koleksi hadis popular dimuat secara dinamik (JavaScript); video
  promosi. Kandungan **Bahasa Melayu sepenuhnya**.

### 9.2 API carian (terbuka, tiada kunci)

Didedahkan oleh `core/sema_source.py` projek ini dan disahkan dengan
ujian langsung:

- **Endpoint:**
  `GET https://semakhadis.com/api/hadith/hadith-search.json?query=...`
- **Ujian langsung** (query `إنما الأعمال بالنيات`) → **200**, JSON
  bersih dengan `data[]`; setiap rekod:
  - `id` (UUID) + `slug` + `title` (tajuk Melayu)
  - `arabic_text_diacritics` + `arabic_text` (Arab penuh / tanpa syakal)
  - `malay_text` — terjemahan Melayu penuh
  - `intro_commentary` + `arabic_commentary` / `malay_commentary`
    (komentar penuh; contoh termasuk "Status Hadis: Muttafaq 'alayh.
    Riwayat al-Bukhari (1) dan Muslim (1907)")
  - `classification` — **status mesin-baca**: `{name, definition,
    color_code}` (contoh: `Muttafaq 'alayh`, `#22c55e` hijau)
  - `chapters`, `keywords`, `narrators`, `researchers`, `sources`
    (book/page/number), `translator`/`editor`/`reviewer` (rantaian
    semakan penuh)
  - `info` — maklumat tajaan (Yayasan Athar + Multaqa Ahli Hadis
    Malaysia + pensyarah UPSI)
  - `published` + cap masa (cipta/kemas)
  - `_formatted` — salinan dengan `<mark>` pada kata kunci padanan

Perbandingan cepat dengan dorar.net (bab 8): SemakHadis pulang JSON
berstruktur (bukan HTML dalam JSON), **dengan terjemahan Melayu** dan
status dalam bentuk boleh-baca mesin — jauh lebih mudah disepadukan.

### 9.3 Penggunaan semasa dalam Pustaka Hadith

- `core/sema_source.py` — sumber huraian Melayu aktif: padanan matn
  (Jaccard ≥ 0.55, calon kedua yang rapat DITOLAK), awalan sanad
  dibuang sebelum padanan, cache `.cache_sema/{id}.json`.
- Liputan: 4,237 hadis popular dengan huraian + status; UI memapar
  "Huraian (SemakHadis · status)" dengan atribusi wajib
  "Sumber: SemakHadis.com".
- Prinsip sedia ada: "lebih baik tiada daripada salah" — hanya padanan
  jelas diterima.

### 9.4 Pandangan, cadangan, dan kebolehgunaan (pros n con)

**Kebaikan (pros):**

- **Bahasa Melayu penuh** — paling serasi dengan pengguna aplikasi
  (berbanding dorar.net Arab / sunnah.com Inggeris).
- **API berstruktur** — JSON bersih; `classification.name` +
  `color_code` membolehkan lencana status berwarna terus dalam UI.
- **Rantaian semakan lengkap** (penterjemah, penyunting, penyemak,
  pengawal kualiti) — kualiti tinggi dan boleh dipercayai.
- Tiada kunci API; padanan matn berfungsi (sudah terbukti dalam app).
- Skala 4 tahap jelas untuk pengguna akhir.

**Kelemahan (cons):**

- **Liputan terhad** — 4,237 hadis popular sahaja, bukan keseluruhan
  62,169 hadis dalam app.
- **Kebergantungan pihak ketiga** — laman/API boleh berubah atau
  turun bila-bila masa.
- **Lesen tidak eksplisit** — penggunaan semula tidak dinyatakan;
  hanya atribusi wajib.
- Koleksi utama berfokus sahih/hasan — liputan Da'if/Palsu dalam
  koleksi terhad walaupun skala 4 tahap dipapar di laman.
- Pengambilan data penuh bergantung pada carian (tiada senarai penuh
  didedahkan di laman utama).

**Kebolehgunaan dengan projek:**

- **Sudah diintegrasi** — sumber utama huraian + status Melayu;
  padanan + cache terbukti berfungsi.
- **Sesuai sebagai teras** "status hadis": bahasa Melayu + status
  mesin-baca (`classification`) — paparan lencana warna konsisten
  dengan skala 4 tahap.

**Cadangan:**

1. Kekalkan SemakHadis sebagai sumber utama huraian/status Melayu.
2. Gunakan `classification.color_code` untuk lencana status dalam UI
   (Sahih/Hasan/Da'if/Palsu) — konsisten dengan skala laman.
3. Tambah audit berkala API SemakHadis (seperti 8o untuk sunnah.com)
   — laman mungkin menukar bentuk respons.
4. Jika liputan status perlu diluaskan: dorar.net (bab 8) sebagai
   pelengkap penilaian Arab (perlu pengelasan + terjemahan);
   sunnah.com untuk pautan luar.
5. Pastikan atribusi SemakHadis.com sentiasa dipapar (lesen tidak
   eksplisit).

**Pandangan ringkas:** tiga sumber saling melengkapi — SemakHadis
untuk huraian/status Melayu (teras), dorar.net untuk penilaian
sahih/daif Arab (pilihan), sunnah.com untuk pautan "Baca penuh".
Gandingan ini tidak menggantikan hadis.my (data terjemahan utama).

---

## 10. Perbandingan akhir: 4 sumber untuk keputusan integrasi

Jadual ini merumuskan dapatan bab 1–9 untuk memudahkan keputusan
integrasi. Sumber: siasatan langsung pada 11 Ogos 2026 (lihat bab
berkenaan untuk butiran).

### 10.1 Jadual perbandingan

| Dimensi | **hadis.my** | **SemakHadis** | **dorar.net** | **sunnah.com** |
|---|---|---|---|---|
| Peranan dalam projek | Data utama — 9 kitab, 62,169 hadis | Huraian + status Melayu (4,237 hadis) | Penilaian sahih/daif Arab (pilihan) | Pautan "Baca penuh" luar |
| Bahasa kandungan | Arab + Melayu + Indonesia + Inggeris | Melayu + Arab | Arab sahaja | Inggeris + Arab (+Urdu/Bangla) |
| API | `service.hadis.my/api/v1` — kunci (percuma, 200/hari) | `hadith-search.json` — terbuka, tiada kunci | `dorar_api.json?skey=` — terbuka, tiada kunci | Tiada API digunakan (halaman web) |
| Format respons | JSON berstruktur | JSON berstruktur + `classification` mesin-baca | HTML dalam JSON (perlu parse) | HTML (audit teks, semak 8o) |
| Status/hukum hadis | Darjat sedia ada | Status mesin-baca + skala 4 tahap | Hukum ayat bebas (perlu pengelasan) | Tiada status |
| Terjemahan | Lengkap (4 bahasa) | Melayu penuh | Tiada | Inggeris |
| Penomboran | Global hadis.my | N/A (slug/id UUID) | N/A (carian teks) | Dalam-buku (book/hadith) + peta `sunnah_map/` |
| Lesen / atribusi | Kunci API hadis.my | Atribusi wajib SemakHadis.com | Tidak didokumenkan | Pautan sahaja |
| Kos | Percuma (kuota 200/hari) | Percuma | Percuma | Percuma |
| Liputan | 62,169 (9 kitab penuh) | 4,237 (hadis popular) | Carian teks (luas, Arab) | 7 kitab terjemahan Inggeris |
| Integrasi semasa | **Teras** (data) | **Teras** (huraian/status) | Belum — cadangan pilihan | **Aktif** (pautan + audit 8o) |

### 10.2 Penilaian keputusan

- **Gabungan teras kini betul:** hadis.my untuk data (terjemahan
  4 bahasa), SemakHadis untuk huraian/status Melayu (JSON
  berstruktur + `classification` mesin-baca), sunnah.com untuk pautan
  luar (diaudit 8o, 50/50).
- **dorar.net = pilihan masa depan:** nilai tambah penilaian
  sahih/daif Arab, tetapi kos integrasi lebih tinggi — respons HTML
  dalam JSON, hukum berbentuk ayat bebas (perlu pengelasan), tiada
  terjemahan Melayu.
- **Kriteria pemilihan sumber** (ikut kepentingan): bahasa kandungan
  (Melayu dahulu) → struktur API → status mesin-baca → lesen/atribusi
  → liputan → kos.
- **Kebergantungan:** semua sumber pihak ketiga boleh berubah —
  audit berkala diperlukan (semak 8o untuk sunnah.com; cadangan
  serupa untuk SemakHadis/dorar.net).

### 10.3 Kedudukan dan kesimpulan

| Kedudukan | Sumber | Peranan | Cadangan |
|---|---|---|---|
| 1 | hadis.my | Data + terjemahan utama | Kekal teras (sedia ada) |
| 2 | SemakHadis | Huraian + status Melayu | Kekal teras (sedia ada) |
| 3 | sunnah.com | Pautan "Baca penuh" | Kekal aktif + audit 8o |
| 4 | dorar.net | Penilaian sahih/daif Arab | Pilihan masa depan (uji dahulu) |

Kesimpulan: kekalkan tiga sumber teras seperti sekarang; dorar.net
boleh ditambah kemudian sebagai pelengkap penilaian, dengan syarat
pengelasan hukum dan paparan Melayu dilaksanakan. Tiada sumber baharu
perlu menggantikan yang sedia ada.
