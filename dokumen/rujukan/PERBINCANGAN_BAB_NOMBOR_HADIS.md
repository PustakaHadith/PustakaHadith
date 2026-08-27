# Perbincangan: Senarai "Bab" & Penomoran No. Hadis

**Tarikh:** 27 Ogos 2026
**Latar:** Sesi ujian binaan dist (`dist/PustakaHadith/PustakaHadith.exe`) — isu paparan
sidebar `PILIH BAB` (pemetaan hadis) hilang, "Lihat bab" buka halaman sama, dan
penomoran No. Hadis tak sepadan dengan sunnah.com / hadith.my.

---

## 1. Senarai "Bab" (ruang `PILIH BAB` di halaman Kitab / Jelajah Kitab)

### Dari mana datanya?
- Disimpan dalam jadual `bab` di `hadis.db`: `collection, hadis_id, book, nama_bab`.
- Dijana oleh `core/eng_source.py`:
  - `bina_bab(fail_ara)` membaca JSON metadata CDN → `metadata.sections`
    `= {nombor_buku: nama_bab_Inggeris}`; setiap hadis membawa `reference.book`
    yang menunjuk ke nombor buku itu.
  - `simpan_bab()` `INSERT OR REPLACE` ke jadual `bab`. Dipanggil dari `sync_english.py`.
- **Nama bab = Inggeris apa adanya dari CDN** (belum diterjemah ke Bahasa Melayu).

### Cara ia dipaparkan (sidebar kiri)
- `api.get_bab_list(slug)` (`api/hadis_api.py:389`):

  ```sql
  SELECT b.book, MIN(b.nama_bab) AS nama_bab, COUNT(*) AS kiraan
  FROM bab b WHERE b.collection=? AND b.book IS NOT NULL
  GROUP BY b.book ORDER BY b.book
  ```

- Satu baris untuk setiap **nombor buku** (cth. Bukhari = 97 buku), dengan nama
  bab (Inggeris) + kiraan hadis. Bahagian ini **hanya dipapar bila
  `self._kitab_bab_data` tidak kosong** (iaitu bila `api.conn` wujud DAN
  jadual `bab` ada rekod untuk koleksi berkenaan).

### Skop semasa (dari `hadis.db`)
| Koleksi     | Bilangan bab |
|-------------|--------------|
| bukhari     | 97           |
| muslim      | 56           |
| tirmidzi    | 49           |
| nasai       | 51           |
| malik       | 60           |
| ibnu-majah  | 37           |
| abu-daud    | 43           |
| **ahmad**   | **0**        |
| **darimi**  | **0**        |

→ `ahmad` & `darimi` **tiada** data bab → bahagian `PILIH BAB` kekal tersembunyi
untuk kedua-dua koleksi itu.

### Kaitan dengan regresi UI (laporan pengguna sebelum ini)
- Binaan dist / terpasang **tidak menyertakan `hadis.db`** → `api.conn = None`
  → `get_bab_list()` pulang `[]` → `PILIH BAB` tak dipapar, dan "Lihat bab"
  tak boleh menapis (buka senarai tak ditapis = "buka page sama").
- **Fix segera (untuk ujian):** salin `hadis.db` (+ `hadis_faiss.index`,
  `hadis_id_map.pkl`) ke `%LOCALAPPDATA%\PustakaHadith` (lokasi `DATA_DIR`
  mod frozen).
- **Fix binaan (permanent):** tambah `('hadis.db', '.')` ke senarai `datas`
  dalam `PustakaHadith.spec` supaya PyInstaller bundel fail itu ke dalam dist,
  dan Inno Setup menyalinnya ke `{app}` (= `%LOCALAPPDATA%\PustakaHadith`).
  *(Fail spec/.iss di-gitignore ikut polisi repo — fix kekal dalam working tree
  setempat, bukan di-commit.)*

---

## 2. Isu Penomoran No. Hadis (ralat besar — BELUM selesai)

### Bukti konkrit
- **Bukhari #858 dalam app** = «لا تقوموا حتى تروني وعليكم السكينة»
  (riwayat Abu Qatadah) = **Bukhari #909 yang sebenar** (disahkan di
  surahquran.com / sunnah.com).
- **Bukhari #858 di sunnah.com / hadith.my** = «الغسل يوم الجمعة واجب على كل
  محتلم» (riwayat Abu Sa'id al-Khudri).
- Bukhari #1 dalam app **padan** dengan sunnah.com → bukan ofset asas; nombor
  mula betul lalu "menggelincir" apabila hadis tertentu tiada dalam sumber.

### Punca akar
- `hadis.db` dibina dari sumber data yang menggunakan **edisi / penomoran
  BERBEZA** daripada sunnah.com:
  - Jumlah hadis Bukhari dalam app = **7008**; kanonik sunnah.com = **7563**
    (kurang **555**).
  - `bab` / `darjat` / `terjemahan_eng` kesemuanya kunci pada `hadithnumber`
    yang SAMA → data dalaman konsisten, cuma penomorannya ikut edisi sumber,
    bukan penomoran sunnah.com.
  - `collections.total_hadis` juga mencerminkan kiraan edisi sumber
    (bukhari = 7008).
- Kesan pada nombor: app #858 → kandungan kanonik #909 (sesaran **+51** pada
  titik itu, dan makin membesar mengikut nombor).

### Skop mengikut koleksi (jumlah app vs kanonik sunnah.com)
| Koleksi     | App   | Kanonik | Beza  |
|-------------|-------|---------|-------|
| bukhari     | 7008  | 7563    | −555  |
| abu-daud    | 4590  | 5274    | −684  |
| tirmidzi    | 3891  | 3956    | −65   |
| nasai       | 5662  | 5761    | −99   |
| ibnu-majah  | 4332  | 4341    | −9    |
| malik       | 1594  | 1717    | −123  |
| muslim      | 5362  | 5362    | ✓     |
| ahmad       | 26363 | 26363*  | ✓     |
| darimi      | 3367  | 3367    | ✓     |

\*Beza mengikut kaedah kiraan; sesetengah rujukan beri nilai lain.

Corak **tak seragam** (ada yang padan, ada yang tak) menunjukkan **sumber data
itu sendiri guna edisi berbeza-beza per koleksi** — bukan silap kod semata-mata.

### Kesan
- "Lompat No. hadis", penanda buku, sejarah bacaan, kiraan `PILIH BAB`, dan
  rujukan "kongsi / salin" semua akan tunjuk **nombor tak sepadan** dengan
  sunnah.com / hadith.my.
- Kandungan hadis masih **sahih** (app #858 = hadis Bukhari #909 yang tulen),
  cuma **nombor rujukan tersasar**.

### Pilihan pembaikan (BELUM DIPUTUSKAN — tunggu arahan pengguna)
- **A (disyorkan):** Ganti sumber data 9 koleksi ke dataset bernombor kanonik
  sunnah.com (7563 untuk Bukhari) → bina semula `hadis.db` + jalankan semula
  semua sinkron (english, darjat, bab, indeks FAISS). Kerja besar.
- **B:** Kekal data, label jelas bahawa nombor ikut "edisi terjemahan"
  (tidak sepadan sunnah.com). Paling cepat, tetapi tidak memuaskan jangkaan
  pengguna yang membanding dengan sunnah.com / hadith.my.
- **C:** Semak fail sumber JSON (tiada dalam repo sekarang) — mungkin ada medan
  nombor kanonik untuk pemetaan semula tanpa muat turun data baru.

---

## 3. Status & Tindakan
- ✅ Dokumen ini dihasilkan.
- ✅ Fix segera DB (salin `hadis.db` + indeks ke `%LOCALAPPDATA%\PustakaHadith`)
  — app berjalan kini memaparkan `PILIH BAB`.
- ⏳ **Binaan semula dist + Setup** dengan `hadis.db` dibundel (menyambung kerja
  tertangguh — lihat Fasa binaan semula di bawah).
- ⏳ Keputusan pengguna untuk Isu #2 (pilihan A / B / C) — menentukan sama ada
  perlu muat turun data bernombor kanonik sebelum binaan akhir.

### Fasa binaan semula (tertangguh)
1. `PustakaHadith.spec` — pastikan `datas` mengandungi
   `('hadis.db', '.'), ('hadis_faiss.index', '.'), ('hadis_id_map.pkl', '.')`.
2. PyInstaller: `pyinstaller PustakaHadith.spec --noconfirm` → `dist/PustakaHadith/`.
3. Inno Setup: `iscc installer/PustakaHadith.iss` →
   `Output/PustakaHadith-Setup-1.0.0-x64.exe` (kini menyertakan `hadis.db`
   ~354 MB + indeks FAISS ~91 MB).
