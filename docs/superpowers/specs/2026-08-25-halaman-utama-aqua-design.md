# Reka Bentuk: Halaman Utama Baharu (Split Command Center + AQUA)

**Tarikh:** 25 Ogos 2026 · **Status:** Diluluskan (keputusan pengguna 25 Ogos)

## Keputusan terkunci

1. **Skop:** Halaman utama + header navigasi baharu (dikongsi semua halaman).
2. **Panel kanan:** data sebenar — sejarah bacaan baharu dicipta.
3. **AQUA = tema ke-5** (bukan ganti); 4 tema lama kekal. AQUA jadi lalai pengguna baharu sahaja.
4. **Layout baharu untuk SEMUA tema** — satu kod halaman; AQUA tambah latar globe + panel kaca, tema lain kekal warna sendiri tanpa latar.
5. **Pendekatan A** — berperingkat: fondasi → backend → header → halaman → ujian.

## Arkitektur

| Komponen | Fail | Nota |
|---|---|---|
| Palet AQUA | `ui/theme.py` | Tema ke-5; `is_dark()` termasuk aqua; kunci baru `PANEL_BG`/`BORDER_GLASS` pada SEMUA palet (aqua=rgba kaca, lain=CARD_BG/BORDER) |
| BackgroundCanvas | `ui/widgets.py` | Root widget; lukis globe (aqua sahaja) + scrim gelap utk kontras AA; cache QPixmap per saiz; fallback warna jika imej hilang |
| GlassPanel | QSS `QFrame#glassPanel` | Panel alpha 20/255 (aqua) / CARD_BG (tema lain) |
| Sejarah bacaan | `ui/helpers.py` + `config.py` | `reading_history.json` (DATA_DIR), cap 50, tulis atomik; hook di `_render_detail` |
| Header | `app_qt.py::_header` | Nav: Utama · Pencarian · Jelajah Kitab · Tersimpan + gear; Rawak dipindah ke panel kanan |
| Halaman utama | `ui/pages_home.py` | Split 2 panel kaca; logik carian/lompat sedia ada dikekalkan |

## Halaman utama

- **Kiri:** eyebrow → tajuk hero → sub (kiraan dinamik) → carian (+Cari berasingan) → chip topik (Niat/Solat/Puasa/Adab/Keluarga) → 3 jalan pantas (Jelajah 9 Kitab/Carian Makna/Sambung) → Petikan Hari Ini → kaki statistik.
- **Kanan:** HARI INI + tarikh → Terakhir dibaca (sejarah; state kosong jika tiada) → Tersimpan (kiraan) → Rawak → Pilihan Hari Ini (hadis deterministik ikut tarikh, worker DB, sembunyi jika gagal).

## Aliran data

- Sejarah: `record_reading(slug,n,label)` dipanggil automatik dari render detail.
- Pilihan hari ini: `date.today().timetuple().tm_yday` → indeks Bukhari via worker (`db.get_one`); kiraan dari `_on_collections`.
- Petikan hari ini: senarai kurasi statik ~10 petikan, giliran ikut hari tahun (tiada DB).

## Ralat & keadaan tepi

- Tiada sejarah → kad "Mula baca — jelajah 9 kitab".
- Imej latar hilang → warna PAGE_BG AQUA sahaja.
- DB kosong/ralat → kad Pilihan Hari Ini disembunyi; halaman tetap berfungsi.
- Halaman lain kekal opaque — hanya halaman utama telus (viewport+body) supaya globe kelihatan.

## Ujian

- `semak.py` + `uji_tukar_tema.py` (5 tema) mesti lulus.
- Tangkap skrin visual AQUA vs tema lama utk semakan mata.
- Kontras AA semua tier teks AQUA ≥ 4.5:1.
