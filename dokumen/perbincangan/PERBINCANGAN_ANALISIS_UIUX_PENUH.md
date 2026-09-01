# Perbincangan: Analisis Semula Projek PustakaHadith — Pandangan UI/UX & Seni Bina

**Tarikh:** 28 Ogos 2026
**Konteks:** Sesi perbincangan semula projek selepas keputusan UI/UX Aqua Glass dikunci
(25 Ogos 2026). Pengguna meminta analisis penuh sebelum melaksanakan sebarang
perubahan — TIADA COMMIT dilakukan.

---

## 1. Gambaran Besar

PustakaHadith ialah **aplikasi desktop PyQt5** untuk membaca dan mencari hadis —
sebuah perpustakaan digital dengan **62,169 hadis** daripada 9 kitab utama
(Kutub al-Tis'ah). Ia dibangunkan oleh seorang pembangun tunggal dan sudah
mencapai **versi 1.0** dengan pengedaran installer (Inno Setup) dan versi portable.

### Stack Teknikal
```
Bahasa     : Python 3.14
UI         : PyQt5 (Qt 5.15.2)
DB         : SQLite + FTS5 (hadis.db, 62,169 baris)
AI/Carian  : FAISS + sentence-transformers (intfloat/multilingual-e5-small)
API        : https://service.hadis.my/api/v1
Modul      : torch, faiss-cpu, sentence-transformers, requests, pyperclip
```

### Struktur Seni Bina
```
api/            → Lapisan API luaran (service.hadis.my)
core/           → Logik carian, transliterasi, terjemahan, draft AI
ui/             → PyQt5 (7 halaman, tema, widgets, workers)
utils/          → Alatan bahasa (transliterasi, pengesanan bahasa)
db.py           → Akses SQLite + FTS5 + migrasi berperingkat (skema 0→8)
config.py       → API key, laluan data, tetapan
main.py         → Entry point (PyQt5 + DLL fix)
```

---

## 2. Kekuatan Projek

### 2.1 Arsitektur DB yang Cemerlang

SQLite + FTS5 dengan **8 tahap migrasi** yang berperingkat — sangat matang.

**Ciri utama:**
- Self-healing: `_fts_perlu_bina_semula()` membaiki indeks FTS5 yang rosak
  secara automatik setiap kali DB dibuka.
- `arab_carian` (tanpa tashkeel) sebagai lajur berasingan untuk FTS5 —
  menyelesaikan masalah carian Arab tanpa harakat.
- `bersih_tashkeel()` tersuai — SQLite `remove_diacritics=2` tidak berkesan
  untuk harakat Arab (hanya aksen Latin seperti café/résumé).
- WAL mode dikekalkan — diuji Sesi 7: baca sambil tulis = 819 vs DELETE 405
  bacaan / 2 saat.

**Sejarah migrasi:**
```
0 → 1  asas: collections, hadis, hadis_fts, favorites
1 → 2  terjemahan_eng  (Fasa 3 - Inggeris dipadan ikut teks Arab)
2 → 3  syarah          (Fasa 4B - Fath al-Bari)
3 → 4  hadethenc       (Fasa 4 - HadeethEnc)
4 → 5  bab             (Fasa 3 - nama bab + nombor buku CDN)
5 → 6  darjat          (Fasa 3 - penilaian ulama moden)
6 → 7  semakhadis      (Fasa 4 - huraian SemakHadis.com)
7 → 8  arab_carian     (lajur baharu: arab tanpa tashkeel untuk FTS5)
```

### 2.2 Backend AI yang Mantap

- **FAISS + e5-small** untuk carian semantik — model pelbagai bahasa.
- Lazy Loading model: dimuat HANYA pada carian makna pertama, bukan startup.
- Thread-safe: `_model_lock` mengelak dua thread memuat model serentak
  (elak fail-fast 0xC0000409).
- Profil prestasi automatik (`profil_model.json`) untuk mengesan regresi
  masa muat.

**Butiran teknikal:**
```python
# core/semantic_search.py
_DEFAULT_MODEL = "intfloat/multilingual-e5-small"
_QUERY_PREFIX = "query: "  # wajib untuk e5-small

# Model dimuat dengan local_files_only=True (cache) terlebih dahulu
# Jika gagal, muat turun dari HF Hub
# Masa muat stabil: ~24s (cache), boleh beberapa minit (turun pertama)
```

### 2.3 UX yang Sangat Diperincikan

| Ciri | Butiran |
|------|---------|
| **Fallback carian** | AND→OR bila carian tiada hasil (kes "hukum riba") |
| **Mesej ralat** | 23 corak terjemahan ke Bahasa Melayu |
| **Skrin pemula** | Splash dengan bar kemajuan semasa muat model |
| **Lompat pantas** | `bukhari 433`, `B433`, `b:433` — buka terus ke hadis |
| **Tema sistem** | Pantau mod gelap Windows setiap 2 saat |
| **Petikan harian** | Deterministik berdasarkan hari tahun |
| **Sejarah bacaan** | Kekal selepas restart + tarikh simpan bookmarks |
| **Kontras WCAG** | Semua tier teks ≥ 4.5:1 (dikira untuk 54 pasangan warna) |
| **Fon Arab** | Auto-detect yang dipasang, cache senarai |

### 2.4 Disiplin Dokumentasi yang Luar Biasa

Folder `dokumen/` mengandungi:
- **Audit** — padanan arkib, liputan SemakHadis, Ahmad Digital
- **Sesi pembangunan** — indeks lengkap setiap keputusan reka bentuk
- **Manual** — pengguna & pembangun
- **Surat rasmi** — permohonan kebenaran data (hadis.my, SemakHadis, HadeethEnc)
- **Perbincangan** — rekod perbincangan teknikal
- **Perubahan** — log harian perubahan
- **Sejarah pembangunan** — log perjalanan projek

**`VERSI.py`** dengan senarai ciri yang dikesah oleh `semak_versi.py` — setiap
versi mesti mempunyai fungsi tertentu yang berfungsi.

### 2.5 Kualiti Kod

- Pemisahan lapisan jelas: `api/`, `core/`, `ui/`, `utils/`, `db.py`.
- QThread untuk semua I/O rangkaian — UI tidak pernah beku.
- SVG ikon vektor (bukan emoji) — konsisten merentas platform.
- Kod sangat berkomentar — setiap keputusan reka bentuk dijustifikasikan
  dengan data ujian dan rujukan dokumentasi dalaman.

---

## 3. Kelemahan & Isu Kritikal

### 3.1 🔴 `set_theme()` Membina Semula SELURUH UI

**Lokasi:** `ui/app_qt.py` — kaedah `set_theme()`

```python
def set_theme(self, name: str, paksa: bool = False):
    ...
    self._build()  # bina semula semua widget
```

**Masalah:** Setiap kali tema ditukar, **SEMUA widget dicipta semula** —
termasuk header, stack, semua halaman, settings panel. Ini bukan sahaja
membazir, tetapi juga berisiko kehilangan keadaan (kedudukan skrol, teks
yang sedang ditaip, posisi skrol dalam senarai hadis).

**Punca:** 53 panggilan `setStyleSheet()` inline dalam UI membaca warna pada
masa cipta widget. Menukar QSS global sahaja TIDAK cukup.

**Cadangan:** Refactor untuk gunakan QSS sahaja tanpa bina semula widget.
Widget yang inline style-nya bergantung pada warna tema perlu dirawat
secara berasingan (mungkin menggunakan property atau dynamic properties).

### 3.2 🔴 Tiada Unit Test Sebenar

Projek ini mempunyai banyak skrip uji (`uji_*.py`, `semak.py`) tetapi
tiada **unit test sebenar** menggunakan `pytest` atau `unittest`.

**Kekuatan sedia ada:**
- `semak.py` — suite 13+ ujian pra-hantar (CRLF, susun atur, bersih)
- `uji_visual_*.py` — ujian visual (tangkap layar, perbandingan piksel)
- `uji_negatif_8z.py` — ujian kepekaan mutasi (45+ cabang)
- `uji_pra_hantar.py` — 13 ujian dalam satu arahan

**Kelemahan:**
- Tiada cara menjalankan ujian secara headless dalam CI/CD.
- Tiada ujian untuk fungsi teras: `db.search()`, `config.get_api_key()`,
  `core.semantic_search()`, `utils.bahasa.betulkan_melayu()`.
- Ujian visual memerlukan paparan GUI — tidak boleh dijalankan dalam
  persekitaran CI.

### 3.3 🔴 `sys.path.insert` Anti-Pattern

```python
# ui/app_qt.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

Ini ada dalam beberapa fail. Patut selesaikan dengan `pyproject.toml` atau
pemasangan paket (`pip install -e .`).

### 3.4 🟡 Terlalu Banyak Fail di Root

Terdapat **50+ fail** di root projek:

| Kategori | Contoh | Bilangan |
|----------|--------|----------|
| Skrip uji | `uji_*.py` | ~20 fail |
| Batch files | `BUANG.bat`, `BUAT_PINTASAN.bat` | ~7 fail |
| Log | `build_log.txt`, `err.txt`, `out.txt` | ~5 fail |
| JSON | `bf9c0680...json`, `bookmarks.json` | ~3 fail |
| Skrip debug | `buka_hari.py`, `diagnos_*.py` | ~5 fail |
| Skrip utiliti | `buat_logo.py`, `buat_pdf.py` | ~3 fail |

**Cadangan:** Pindahkan ke folder yang sesuai:
- `uji_*.py` → `tests/`
- `diagnos_*.py` → `scripts/`
- Batch files → `scripts/` atau kekalkan di root untuk pengguna
- Log → `.gitignore` (sudah ada sebahagian)

### 3.5 🟡 UI/UX Aqua Glass Belum Selesai Dilaksanakan

Mockup `SELECTED_UIUX.md` sudah dipilih (25 Ogos 2026), tetapi:

- **Halaman 9 kitab:** `pages_rak.py` wujud sebagai halaman Rak Digital —
  perlu disahkan konsisten dengan mockup "Rak Digital Interaktif".
- **Tema AQUA:** Sudah ada dalam `theme.py` dengan alpha sebenar 20/255
  tanpa blur, tetapi visual akhir mungkin belum tepat dengan mockup.
- **Latar glob:** `BackgroundCanvas` sudah melukis latar glob untuk tema
  AQUA, tetapi perlu disahkan konsisten dengan mockup.

### 3.6 🟡 Kebergantungan Berat

```
torch>=2.6               → ~800MB
sentence-transformers>=5.0 → ~200MB
faiss-cpu>=1.9           → ~50MB
```

Total: ~1.1 GB untuk kebergantungan AI sahaja. Aplikasi desktop untuk
carian hadis sepatutnya ringan.

**Cadangan:** Pertimbangkan ONNX Runtime sebagai alternatif kepada torch
(jika model e5-small boleh ditukar ke format ONNX).

### 3.7 🟡 Tiada CI/CD

Tiada fail GitHub Actions, tiada automasi selepas commit. `semak.py`
sepatutnya dijalankan secara automatik.

---

## 4. Penilaian

| Aspek | Skor | Catatan |
|-------|------|---------|
| **Kualiti Kod** | ⭐⭐⭐⭐ (4/5) | Sangat baik, tapi `set_theme()` bina semula UI adalah isu besar |
| **Seni Bina DB** | ⭐⭐⭐⭐⭐ (5/5) | Migrasi berperingkat + self-healing FTS5 = kelas profesional |
| **Seni Bina AI** | ⭐⭐⭐⭐ (4/5) | Thread-safe, lazy loading, profil prestasi — tetapi terlalu berat |
| **UX** | ⭐⭐⭐⭐½ (4.5/5) | Fallback carian, terjemahan ralat, sintaks lompat — sangat diperincikan |
| **Dokumentasi** | ⭐⭐⭐⭐⭐ (5/5) | Tiada tandingan untuk projek seorang individu |
| **Ujian** | ⭐⭐½ (2.5/5) | Tiada unit test sebenar; semua integrasi/GUI |
| **Kebersihan Kod** | ⭐⭐⭐ (3/5) | Root bersepah, sys.path.insert, tiada pyproject.toml |

---

## 5. Cadangan Penambahbaikan (Mengikut Keutamaan)

### Fasa 1 — Kebersihan & Asas (Rendah Usaha, Tinggi Kesan)

1. **Bersihkan root projek** — pindahkan fail uji, batch, dan log ke folder
   yang sesuai.
2. **Tambah `pyproject.toml`** — selesaikan `sys.path.insert` anti-pattern.
3. **Tambah CI/CD** — GitHub Actions untuk menjalankan `semak.py` setiap commit.

### Fasa 2 — Ujian Automatik (Sederhana Usaha, Tinggi Kesan)

4. **Tambah unit tests** dengan `pytest` untuk fungsi teras:
   - `db.search()`, `db.random_hadis()`, `db.get_page()`
   - `config.get_api_key()`, `config.valid_key_format()`
   - `core.semantic_search()` (dengan mock model)
   - `utils.bahasa.betulkan_melayu()`, `utils.bahasa.simbol_boleh_dipapar()`
5. **Tambah integration tests** — ujian end-to-end tanpa GUI
   (menggunakan `QTest` atau `pytest-qt`).

### Fasa 3 — UI/UX (Tinggi Usaha, Tinggi Kesan)

6. **Baiki `set_theme()`** — refaktor supaya hanya stylesheet dikemas kini
   tanpa membina semula semua widget.
7. **Laksanakan mockup Aqua Glass sepenuhnya** — pastikan semua 6 halaman
   konsisten dengan `SELECTED_UIUX.md`.
8. **Uji responsif** — pastikan aplikasi berfungsi dengan baik pada pelbagai
   saiz tetingkap (900×560 hingga 1920×1080).

### Fasa 4 — Prestasi (Tinggi Usaha, Sederhana Kesan)

9. **Pertimbangkan ONNX Runtime** — ganti torch/sentence-transformers dengan
   model ONNX untuk mengurangkan saiz aplikasi.
10. **Optimumkan masa mula** — profilkan apa yang paling lambat dan optimumkan.

---

## 6. Kesimpulan

Projek ini menunjukkan **disiplin pembangunan peringkat profesional** —
terutamanya dalam aspek dokumentasi, reka bentuk DB, dan perhatian
terhadap UX. Perhatian terhadap perincian (terjemahan ralat, fallback
carian, sintaks lompat, self-healing DB) menunjukkan tahap profesionalisme
yang tinggi.

Kelemahan utama ialah ketiadaan ujian automatik, kebersihan struktur fail,
dan tema Aqua Glass yang belum sepenuhnya dilaksanakan dalam kod walaupun
sudah dikunci dalam reka bentuk.

Untuk projek seorang individu yang membangunkan aplikasi desktop berniche
untuk komuniti Islam berbahasa Melayu, projek ini sudah berada pada tahap
yang **sangat baik** — jauh melebihi jangkaan biasa untuk projek solo.

---

## 7. Status

- ✅ Dokumen ini dihasilkan.
- ⏳ Keputusan pengguna untuk langkah seterusnya:
  - A: Bersihkan root projek + tambah pyproject.toml
  - B: Tambah unit tests dengan pytest
  - C: Baiki set_theme() performance
  - D: Laksanakan mockup Aqua Glass sepenuhnya
