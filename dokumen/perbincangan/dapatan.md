# Dapatan Analisis — PustakaHadith

**Tarikh:** 28 Ogos 2026
**Analisis oleh:** Buffy (Codebuff)
**Status:** Tiada perubahan kod dilakukan

---

## Ringkasan Eksekutif

PustakaHadith ialah aplikasi desktop PyQt5 untuk membaca dan mencari hadis
dengan 62,169 hadis daripada 9 kitab utama. Projek ini menunjukkan tahap
profesionalisme yang tinggi untuk projek seorang individu, terutamanya
dalam aspek dokumentasi dan reka bentuk database.

---

## Kekuatan Utama

### Seni Bina Database
- Migrasi berperingkat 8 tahap (skema 0→8) — sangat matang
- Self-healing FTS5 — membaiki indeks rosak secara automatik
- `arab_carian` lajur berasingan untuk carian tanpa tashkeel
- WAL mode dikekalkan untuk prestasi baca sambil tulis

### Backend AI
- FAISS + e5-small (multilingual) untuk carian semantik
- Lazy Loading — model dimuat hanya pada carian pertama
- Thread-safe dengan `_model_lock` (elak fail-fast 0xC0000409)
- Profil prestasi automatik untuk kesan regresi

### UX yang Diperincikan
- Fallback carian AND→OR bila tiada hasil
- 23 corak mesej ralat dalam Bahasa Melayu
- Sintaks lompat pantas: `bukhari 433`, `B433`, `b:433`
- Kontras WCAG AA — semua tier teks ≥ 4.5:1
- Tema "Ikut sistem" pantau mod gelap Windows setiap 2 saat

### Dokumentasi
- Folder `dokumen/` lengkap dengan audit, sesi, manual, surat
- `VERSI.py` dengan senarai ciri yang dikesah automatik
- Kod sangat berkomentar — setiap keputusan dijustifikasikan

---

## Kelemahan yang Dikenal Pasti

### Kritikal
1. **`set_theme()` membina semula seluruh UI** — setiap tukar tema,
   semua widget dicipta semula (53 panggilan setStyleSheet inline)

2. **Tiada unit test sebenar** — semua ujian memerlukan GUI;
   tiada cara jalankan headless dalam CI/CD

3. **`sys.path.insert` anti-pattern** — patut guna pyproject.toml

### Sederhana
4. **Root projek bersepah** — 50+ fail (uji, batch, log, JSON)

5. **Aqua Glass belum dilaksanakan sepenuhnya** — mockup dikunci
   25 Ogos tetapi kod belum konsisten dengan reka bentuk

6. **Kebergantungan berat** — ~1.1 GB untuk torch + sentence-transformers

7. **Tiada CI/CD** — `semak.py` patut dijalankan automatik

---

## Penilaian

| Aspek | Skor | Catatan |
|-------|------|---------|
| Kualiti Kod | ⭐⭐⭐⭐ | Sangat baik, isu `set_theme()` |
| Seni Bina DB | ⭐⭐⭐⭐⭐ | Migrasi + self-healing = profesional |
| Seni Bina AI | ⭐⭐⭐⭐ | Mantap tetapi berat |
| UX | ⭐⭐⭐⭐½ | Sangat diperincikan |
| Dokumentasi | ⭐⭐⭐⭐⭐ | Tiada tandingan |
| Ujian | ⭐⭐½ | Tiada unit test sebenar |
| Kebersihan Kod | ⭐⭐⭐ | Root bersepah, tiada pyproject.toml |

---

## Cadangan Penambahbaikan

### Fasa 1 — Kebersihan (Rendah Usaha)
- Pindahkan fail uji/batch/log ke folder sesuai
- Tambah `pyproject.toml`
- Sediakan GitHub Actions CI

### Fasa 2 — Ujian (Sederhana Usaha)
- Tambah unit tests dengan `pytest`
- Fokus: `db.search()`, `config.get_api_key()`, `core.semantic_search()`

### Fasa 3 — UI/UX (Tinggi Usaha)
- Baiki `set_theme()` — guna QSS sahaja tanpa bina semula widget
- Laksanakan Aqua Glass sepenuhnya mengikut mockup

### Fasa 4 — Prestasi (Tinggi Usaha)
- Pertimbangkan ONNX Runtime ganti torch
- Optimumkan masa mula

---

## Kesimpulan

Projek ini **amat mengagumkan** untuk dibangunkan oleh seorang individu.
Kualiti kod, dokumentasi, dan perhatian terhadap UX menunjukkan tahap
profesionalisme yang tinggi. Kelemahan utama (tiada ujian automatik,
kebersihan struktur) adalah isu yang boleh diselesaikan secara berperingkat.

Untuk aplikasi desktop berniche untuk komuniti Islam berbahasa Melayu,
projek ini sudah berada pada tahap yang **sangat baik** — jauh melebihi
jangkaan biasa untuk projek solo.
