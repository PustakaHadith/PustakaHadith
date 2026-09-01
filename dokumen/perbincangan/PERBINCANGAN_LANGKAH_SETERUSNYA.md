# Perbincangan: Langkah Seterusnya — Ujian, Prestasi Tema, & Aqua Glass

**Tarikh:** 28 Ogos 2026
**Rujukan:** PERBINCANGAN_ANALISIS_UIUX_PENUH.md (analisis penuh projek)
**Status:** Dokumen perancangan — tiada kod diubah

---

## Ringkasan

Tiga langkah penambahbaikan utama telah dikenal pasti berdasarkan analisis projek:

| # | Langkah | Kesan | Usaha | Keutamaan |
|---|---------|-------|-------|-----------|
| 1 | Tambah unit tests (pytest) | 🔴 Tinggi | Sederhana | PERTAMA |
| 2 | Baiki `set_theme()` performance | 🔴 Tinggi | Rendah-Sederhana | KEDUA |
| 3 | Laksanakan Aqua Glass UI | 🔴 Tinggi | Tinggi | KETIGA |

**Justifikasi urutan:** Ujian mesti ada sebelum refaktor (langkah 2) supaya kita tahu jika perubahan memecahkan sesuatu. `set_theme()` mesti dibaiki sebelum Aqua Glass (langkah 3) kerana tema baru memerlukan mekanisme tukar tema yang cekap.

---

## 1. Tambah Unit Tests dengan pytest

### 1.1 Masalah Semasa

Projek ini mempunyai banyak skrip uji tetapi tiada **unit test sebenar**:

```
❌ Tiada tests/ folder
❌ Tiada pytest / unittest
❌ Semua uji memerlukan GUI (tidak boleh headless)
❌ Tiada CI/CD untuk automasi ujian
```

**Yang ada:**
- `semak.py` — 13+ ujian pra-hantar (CRLF, susun atur)
- `uji_visual_*.py` — ujian visual (perlu paparan)
- `uji_negatif_8z.py` — 45+ cabang ujian kepekaan mutasi
- `uji_pra_hantar.py` — 13 ujian dalam satu arahan

### 1.2 Apa Yang Perlu Diuji

#### Layer 1 — Fungsi Murni (Tiada GUI, Paling Pantas)

| Modul | Fungsi | Apa Yang Diuji |
|-------|--------|----------------|
| `db.py` | `search(slug, q)` | Carian FTS5 pulangkan hasil |
| `db.py` | `search_fallback(slug, q)` | AND→OR fallback bila tiada hasil |
| `db.py` | `bersih_tashkeel(teks)` | Buang harakat Arab dengan betul |
| `db.py` | `_fts_perlu_bina_semula(conn)` | Pengesanan indeks FTS5 rosak |
| `db.py` | `get_hadith(slug, nombor)` | Teks hadis dikembalikan |
| `config.py` | `get_api_key("")` | Fallback ke env var |
| `config.py` | `get_api_key("sk-xxx")` | Direct key dikembalikan |
| `config.py` | `validate_config()` | Assert DB wujud |
| `core/semantic_search.py` | `bersih_teks(teks)` | Buang tanda baca/HTML |
| `utils/bahasa.py` | `simbol_boleh_dipapar(font)` | True/False ikut fon |
| `utils/bahasa.py` | `terjemah_ralat(kod)` | Mesej BM dikembalikan |
| `ui/helpers.py` | `_parse_lompat("bukhari 433")` | ("bukhari", 433) |
| `ui/helpers.py` | `_parse_lompat("B433")` | ("bukhari", 433) |
| `ui/helpers.py` | `_parse_lompat("b:433")` | ("bukhari", 433) |
| `ui/helpers.py` | `_read_json / _write_json` | CRUD fail JSON |

#### Layer 2 — Integrasi (Dengan DB)

| Ujian | Butiran |
|-------|---------|
| DB init → migrasi 0→8 | Cipta DB kosong, pastikan semua lajur wujud |
| Search → FTS5 index | Cari selepas DB diisi (perlu fixture data) |
| Bookmark → CRUD | Tambah/simpan/buang bookmarks |
| Reading history | Rekod + baca semula sejarah |

#### Layer 3 — End-to-End (Dengan GUI Mocking)

| Ujian | Butiran |
|-------|---------|
| App startup | Stack wujud, halaman default = home |
| Theme switch | QSS berubah, widget kekal hidup |
| Navigation | go("home") → stack index 0 |

### 1.3 Struktur Fail

```
tests/
├── __init__.py
├── conftest.py              # Fixtures: test DB, mock API
├── test_db_search.py        # Fungsi carian + fallback
├── test_db_migrasi.py       # Migrasi skema
├── test_db_bersih.py        # bersih_tashkeel, arab_carian
├── test_config.py           # API key, validasi
├── test_bahasa.py           # Terjemahan, simbol
├── test_helpers.py          # Parse lompat, JSON CRUD
├── test_semantic.py         # Bersih teks, mock model
└── test_theme.py            # Apply theme, QSS generation
```

### 1.4 Contoh Kod

#### conftest.py — Fixtures

```python
"""Fixtures untuk ujian PustakaHadith."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def tmp_db(tmp_path):
    """DB SQLite sementara untuk ujian.
    
    Cipta DB kosong, jalankan migrasi, pulangkan laluan.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import db
    
    db_path = str(tmp_path / "test.db")
    db.init_db(db_path)
    yield db_path
    db.close()


@pytest.fixture
def sample_hadith_data():
    """Data hadis contoh untuk ujian."""
    return {
        "slug": "bukhari",
        "nombor": 1,
        "teks_arab": "بَابُ الْوَحْيِ",
        "teks_melayu": "Bab Wahyu",
        "teks_english": "Revelation",
    }


@pytest.fixture
def mock_api_key():
    """API key palsu untuk ujian."""
    return "test-api-key-12345"
```

#### test_db_search.py — Ujian Carian

```python
"""Ujian untuk fungsi carian dalam db.py."""


def test_search_returns_list(tmp_db):
    """search() mengembalikan senarai walaupun DB kosong."""
    import db
    results = db.search("bukhari", "solat")
    assert isinstance(results, list)


def test_search_has_required_fields(tmp_db):
    """Setiap hasil carian mempunyai medan yang diperlukan."""
    import db
    results = db.search("bukhari", "wahyu")
    if results:  # Mungkin kosong jika tiada data
        for r in results:
            assert "nombor" in r


def test_bersih_tashkeel_removes_diacritics():
    """bersih_tashkeel() membuang harakat Arab."""
    import db
    input_text = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
    result = db.bersih_tashkeel(input_text)
    # Harakat (حركات) patut dibuang
    assert "ِ" not in result  # kasra
    assert "ُ" not in result  # damma  
    assert "َ" not in result  # fatha


def test_fts_perlu_bina_semula_returns_bool(tmp_db):
    """_fts_perlu_bina_semula() mengembalikan True/False."""
    import db
    import sqlite3
    conn = sqlite3.connect(tmp_db)
    result = db._fts_perlu_bina_semula(conn)
    assert isinstance(result, bool)
    conn.close()
```

#### test_helpers.py — Ujian Helper

```python
"""Ujian untuk fungsi helper dalam ui/helpers.py."""


def test_parse_lompat_full_syntax():
    """_parse_lompat('bukhari 433') → ('bukhari', 433)."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from ui.helpers import _parse_lompat
    slug, num = _parse_lompat("bukhari 433")
    assert slug == "bukhari"
    assert num == 433


def test_parse_lompat_short_syntax():
    """_parse_lompat('B433') → ('bukhari', 433)."""
    from ui.helpers import _parse_lompat
    slug, num = _parse_lompat("B433")
    assert slug == "bukhari"
    assert num == 433


def test_parse_lompat_colon_syntax():
    """_parse_lompat('b:433') → ('bukhari', 433)."""
    from ui.helpers import _parse_lompat
    slug, num = _parse_lompat("b:433")
    assert slug == "bukhari"
    assert num == 433


def test_parse_lompat_invalid_returns_none():
    """_parse_lompat('tiada nombor') → (None, None)."""
    from ui.helpers import _parse_lompat
    slug, num = _parse_lompat("tiada nombor")
    assert slug is None
    assert num is None


def test_read_write_json_roundtrip(tmp_path):
    """_write_json() + _read_json() = data asal."""
    from ui.helpers import _read_json, _write_json
    test_file = tmp_path / "test.json"
    data = {"key": "value", "num": 42}
    _write_json(str(test_file), data)
    loaded = _read_json(str(test_file), {})
    assert loaded == data
```

### 1.5 Arahan Pelaksanaan

```bash
# 1. Pasang pytest
pip install pytest

# 2. Jalankan semua ujian
pytest tests/ -v

# 3. Jalankan ujian tertentu
pytest tests/test_db_search.py -v

# 4. Jalankan dengan coverage (pilihan)
pip install pytest-cov
pytest tests/ --cov=. --cov-report=term-missing
```

### 1.6 Rencana Masa

```
Hari 1: Setup tests/ + conftest.py + test_helpers.py (12 ujian)
Hari 2: test_db_search.py + test_db_bersih.py (10 ujian)
Hari 3: test_config.py + test_bahasa.py (8 ujian)
Hari 4: test_db_migrasi.py + test_semantic.py (6 ujian)
Hari 5: test_theme.py + integration tests (4 ujian)
Jumlah: ~40 ujian dalam 5 hari
```

---

## 2. Baiki `set_theme()` Performance

### 2.1 Masalah Semasa

**Lokasi:** `ui/app_qt.py` — kaedah `set_theme()`

```python
def set_theme(self, name: str, paksa: bool = False):
    ...
    self._build()  # ← BINA SEMULA SEMUA WIDGET!
```

**Apa yang `_build()` lakukan setiap kali tema ditukar:**

```
1. Cipta root widget baru
2. Bina header + nav buttons (4 butang)
3. Cipta QStackedWidget
4. Bina 6 halaman:
   ├── home    → hero, panel kiri/kanan, grid
   ├── kitab   → senarai hadis, filter
   ├── detail  → dua lajur Arab/Melayu
   ├── search  → carian + hasil
   ├── saved   → bookmarks + sejarah
   └── rak     → 9 kitab card
5. Tetapkan halaman default
```

**Kesan buruk:**

```
❌ Hilang konteks:
   - Kedudukan skrol dalam senarai hadis
   - Teks yang sedang ditaip dalam search bar
   - Halaman aktif (kembali ke home)
   - Pilihan bab yang sedang dilihat

❌ Lambat:
   - Cipta ~200+ widget setiap kali
   - Flood Qt event loop
   - Flash kelihatan (widget hilang muncul)

❌ Pembaziran memori:
   - Widget lama tidak dihapuskan serta-merta
   - Memory leak jika settings panel terbuka
```

### 2.2 Punca Teknikal

```
53 panggilan setStyleSheet() INLINE dalam UI code:

# Contoh dalam pages_kitab.py:
label.setStyleSheet(f"color: {TEXT_PRIMARY}; ...")
card.setStyleSheet(f"background-color: {CARD_BG}; ...")

Masalah: from theme import CARD_BG mengikat nilai pada MASA IMPORT.
Ganti QSS global SAHAJA tidak menukar nilai sedia ada.
```

### 2.3 Penyelesaian — Tiga Peringkat

#### Peringkat 1: Guna `unpolish/polish` (80% penyelesaian)

```python
def set_theme(self, name: str, paksa: bool = False):
    """Tukar tema — KEMAS KINI QSS sahaja."""
    if not paksa and name == self.settings.get("theme", DEFAULT_TEMA):
        return
    
    if name != self.settings.get("theme", DEFAULT_TEMA):
        self.settings["theme"] = name
        _write_json(SETTINGS, self.settings)

    # Simpan keadaan semasa
    idx = self.stack.currentIndex()
    page = next((k for k, v in PAGES.items() if v == idx), "home")
    detail, slug, kpage = self._detail_h, self._kitab_slug, self._kitab_page
    q, qslug, qpage = self._search_q, self._search_slug, self._search_page

    # Kemas kini palet global + QSS
    apply_theme(name)
    self.setStyleSheet(build_qss(FONT_SCALES[self.ui_idx]))

    # PAKSA SEMUA widget kemas kini warna
    self._refresh_theme_all(self)

    # Pulihkan keadaan
    self._detail_h, self._kitab_slug, self._kitab_page = detail, slug, kpage
    self._search_q, self._search_slug, self._search_page = q, qslug, qpage

    if page == "detail" and detail:
        self.go("detail")
        self._render_detail(detail)
    elif page == "kitab":
        self.open_kitab(slug, kpage)
    elif page == "search" and q:
        self.go("search")
        self.search_bar.input.setText(q)
        self._do_search(qpage)
    else:
        self.go(page if page in PAGES else "home")

    self.toast.show_msg("Tema terang" if not is_dark() else "Tema gelap")


def _refresh_theme_all(self, widget):
    """Lalui semua widget, paksa polish semula untuk QSS baru."""
    for child in widget.findChildren(QWidget):
        child.style().unpolish(child)
        child.style().polish(child)
        child.update()
    # Proses anak-anak secara rekursif
    for child in widget.findChildren(QWidget):
        self._refresh_theme_all(child)
```

**Kelebihan:**
- ✅ Tiada widget dicipta semula
- ✅ Kekalkan semua konteks (skrol, teks, halaman)
- ✅ Lebih pantas (~10x)

**Kelemahan:**
- ⚠️ 53 inline styles masih tidak berubah (warna lama kekal)

#### Peringkat 2: Tukar Inline Styles ke QSS Selectors

```python
# SEBELUM (inline):
label.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 14px;")

# SELEPAS (objectName + QSS):
label.setObjectName("body")
# Dalam build_qss():
# QLabel#body { color: TEXT_PRIMARY; font-size: 14px; }
```

**Yang perlu ditukar (53 tempat):**

| Fail | Bilangan | Contoh |
|------|----------|--------|
| `pages_home.py` | ~15 | Label heading, butang |
| `pages_kitab.py` | ~12 | Kad hadis, teks Arab |
| `pages_detail.py` | ~10 | Panel dua lajur |
| `pages_carian.py` | ~8 | Kotak carian, hasil |
| `pages_tersimpan.py` | ~5 | Senarai bookmarks |
| `settings_panel.py` | ~3 | Butang tetapan |

#### Peringkat 3: Hapuskan Semua Inline Styles

```
Selepas peringkat 2, semua warna dikawal oleh QSS global.
set_theme() hanya perlu:
1. apply_theme(name)     → tukar palet global
2. setStyleSheet(qss)    → kemas kini QSS global
3. _refresh_theme_all()  → paksa widget baca QSS baru
```

### 2.4 Pengukuhan

```
SEBELUM: ~50ms (cipta semula 200+ widget)
SELEPAS: ~5ms (tukar QSS + polish sahaja)

Ukur masa dengan:
import time
t0 = time.perf_counter()
self.set_theme("aqua")
dt = time.perf_counter() - t0
print(f"Tema ditukar dalam {dt*1000:.1f}ms")
```

### 2.5 Rencana Pelaksanaan

```
Hari 1: Peringkat 1 — refactor set_theme() + _refresh_theme_all()
Hari 2: Uji tema gelap ↔ terang ↔ neutral ↔ aqua
Hari 3: Peringkat 2 — tukar inline styles pages_home.py
Hari 4: Peringkat 2 — tukar pages_kitab.py + pages_detail.py
Hari 5: Peringkat 2 — tukar pages_carian.py + pages_tersimpan.py
Hari 6: Peringkat 2 — tukar settings_panel.py
Hari 7: Ujian integrasi penuh + ukur masa
```

---

## 3. Laksanakan Aqua Glass UI

### 3.1 Apa Yang Sudah Ada

```
✅ Warna AQUA dalam ui/theme.py (palet 25 Ogos 2026)
   PAGE_BG: #0A1520, CARD_BG: #10222F, TEAL: #3EC9B0

✅ BackgroundCanvas untuk latar globe/jaringan
   Hanya aktif tema AQUA (ada_latar_imej() → True)

✅ Panel kaca: 
   PANEL_BG: rgba(13, 42, 60, 20/255)
   BORDER_GLASS: rgba(62, 201, 176, 60/255)

✅ QSS selectors sedia ada:
   QFrame#glassPanel, QLabel#eyebrow, QLabel#homeH1
   QLabel#panelTitle, QLabel#panelSection, QLabel#rakNombor

✅ mockup 6 halaman dipilih dalam SELECTED_UIUX.md
```

### 3.2 Apa Yang Belum Dilaksanakan

#### 🔴 Halaman Utama — Split Command Center

```
MOCKUP (selected_home_1366x768.png):
┌─────────────────────────────────────────────────────────┐
│ KIRI (60%)                    │ KANAN (40%)             │
│ ┌───────────────────────────┐ │ ┌─────────────────────┐ │
│ │ EYEBROW: PUSTAKA HADITH  │ │ │ Sambung Pembacaan   │ │
│ │ H1: Temui Kebijaksanaan  │ │ │ [hadis terakhir]    │ │
│ │                          │ │ ├─────────────────────┤ │
│ │ [Search bar] [Cari]      │ │ │ Statistik           │ │
│ │                          │ │ │ 62,169 hadis        │ │
│ │ Cadangan Topik:          │ │ │ 9 kitab             │ │
│ │ [Niat] [Solat] [Iman]    │ │ ├─────────────────────┤ │
│ │                          │ │ │ Petikan Hari Ini    │ │
│ │ Petikan Hari Ini         │ │ │ [teks petikan]      │ │
│ │ "...                    "│ │ └─────────────────────┘ │
│ └───────────────────────────┘ │                         │
└─────────────────────────────────────────────────────────┘

KOD SEMASA (pages_home.py):
┌─────────────────────────────────────────────────────────┐
│ Hero section (penuh lebar)                              │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ PustakaHadith                                       │ │
│ │ [Search bar] [Cari]                                 │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Grid 9 Kitab (3×3)                                      │
│ ┌─────┐ ┌─────┐ ┌─────┐                                │
│ │Bukh.│ │Muslim│ │Abu D│                                │
│ ├─────┤ ├─────┤ ├─────┤                                │
│ │Tirm.│ │Nasai │ │IbnuM│                                │
│ ├─────┤ ├─────┤ ├─────┤                                │
│ │Malik│ │Ahmad │ │Darim│                                │
│ └─────┘ └─────┘ └─────┘                                │
└─────────────────────────────────────────────────────────┘
```

**Perubahan diperlukan:**

```python
# Dalam ui/pages_home.py — _page_home()

# SEBELUM: Hero + Grid 3×3
def _page_home(self):
    # hero section penuh lebar
    # grid 9 kitab 3×3
    
# SELEPAS: Split Command Center
def _page_home(self):
    # Panel kiri (60%): eyebrow + h1 + search + topik + petikan
    # Panel kanan (40%): sambung + statistik + pilihan hari
    # BackgroundCanvas: telus viewport untuk latar glob
```

#### 🔴 Halaman 9 Kitab — Rak Digital Interaktif

```
MOCKUP (selected_page_9_kitab_1366x768.png):
┌─────────────────────────────────────────────────────────┐
│ PANEL KIRI (pratonton)      │ RAK (jilid mendatar)      │
│ ┌───────────────────────────┐ │ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
│ │ [Imej kitab]              │ │ │ B │ │ M │ │ A │ │ T │ │
│ │ Sahih al-Bukhari          │ │ │ u │ │ u │ │ b │ │ i │ │
│ │ 7,563 hadis               │ │ │ k │ │ s │ │ u │ │ r │ │
│ │                           │ │ │ h │ │ l │ │ D │ │ m │ │
│ │ [Buka kitab] [Lihat bab]  │ │ │ a │ │ i │ │ a │ │ i │ │
│ └───────────────────────────┘ │ │ r │ │ m │ │ u │ │ d │ │
│                               │ └───┘ └───┘ └───┘ └───┘ │
│                               │ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
│                               │ │ N │ │ I │ │ M │ │ D │ │
│                               │ │ a │ │ b │ │ a │ │ a │ │
│                               │ │ s │ │ n │ │ l │ │ r │ │
│                               │ │ a │ │ u │ │ i │ │ i │ │
│                               │ │ i │ │ M │ │ k │ │ m │ │
│                               │ └───┘ └───┘ └───┘ └───┘ │
└─────────────────────────────────────────────────────────┘

KOD SEMASA (pages_kitab.py):
Grid kad 3×3 biasa — TIADA pratonton panel kiri
```

**Perubahan diperlukan:**

```python
# Dalam ui/pages_kitab.py — _page_rak() BAHARU

def _page_rak(self):
    """Rak Digital Interaktif — 9 kitab sebagai jilid."""
    page = QScrollArea()
    page.setObjectName("page")
    body = QWidget()
    lo = QHBoxLayout(body)
    
    # Panel kiri: pratonton kitab dipilih
    self._rak_pratonton = QWidget()
    self._rak_pratonton.setMinimumWidth(350)
    lo.addWidget(self._rak_pratonton, 1)
    
    # Rak kanan: jilid mendatar
    rak_widget = QWidget()
    rak_lo = QGridLayout(rak_widget)
    for i, (slug, meta) in enumerate(COLLECTION_META.items()):
        card = self._rak_jilid_card(slug, meta)
        rak_lo.addWidget(card, i // 4, i % 4)
    lo.addWidget(rak_widget, 2)
    
    return page
```

#### 🔴 Halaman Senarai Hadis — Dwibahasa

```
MOCKUP (selected_page_senarai_hadis_1366x768.png):
┌─────────────────────────────────────────────────────────┐
│ PANEL KIRI (nav)     │ SENARAI DWIBAHASA                │
│ ┌───────────────────┐ │ ┌──────────────────────────────┐ │
│ │ Sahih al-Bukhari  │ │ │ No. 1 | Bab Wahyu            │ │
│ │ Bab: Wahyu        │ │ │ ┌──────────┐ ┌──────────────┐│ │
│ │                   │ │ │ Terjemahan│ │ Arab RTL      ││ │
│ │ [Semua Bab ▾]     │ │ │ "Pertama  │ │ بِسْمِ ٱللَّهِ││ │
│ │                   │ │ │  yang..."  │ │               ││ │
│ │                   │ │ └──────────┘ └──────────────┘│ │
│ │                   │ │ [💾 Simpan] [Baca →]          │ │
│ │                   │ ├──────────────────────────────┤ │
│ │                   │ │ No. 2 | ...                   │ │
│ └───────────────────┘ │                              │ │
└─────────────────────────────────────────────────────────┘

KOD SEMASA:
Senarai linear — terjemahan ATAU Arab, bukan keduanya
```

#### 🟡 Halaman Detail + Pencarian + Tetapan

```
Detail: Kekalkan layout dua lajur, tukar warna sahaja
Pencarian: Hero compact + draf AI + hasil dwibahasa
Tetapan: Kekalkan layout, tukar warna sahaja
```

### 3.3 Rencana Pelaksanaan

#### Fasa 1: Halaman Utama Split Command Center (Minggu 1)

```
Hari 1-2: Refactor _page_home()
  ├── Buat layout QHBoxLayout (60/40 split)
  ├── Panel kiri: eyebrow + h1 + search + topik + petikan
  ├── Panel kanan: sambung + statistik + pilihan hari
  └── BackgroundCanvas: telus viewport

Hari 3-4: Widget kaca
  ├── Glass card untuk panel kiri/kanan
  ├── Hover effects + transitions
  └── Uji dengan tema AQUA + DARK + LIGHT

Hari 5: Responsive
  ├── Uji 1366×768 (laptop)
  ├── Uji 1920×1080 (desktop)
  └── Uji 900×560 (minimum)
```

#### Fasa 2: Rak Digital Interaktif (Minggu 2)

```
Hari 1-2: _page_rak() baharu
  ├── Layout dua lajur (pratonton + rak)
  ├── Jilid card dengan hover effects
  └── Klik kitab → papar pratonton

Hari 3-4: Integrasi
  ├── Sambung ke open_kitab()
  ├── Papar bab list dalam pratonton
  └── Navigasi antara kitab

Hari 5: Responsive + ujian
```

#### Fasa 3: Senarai Hadis Dwibahasa (Minggu 3)

```
Hari 1-2: Refactor _render_kitab_shell()
  ├── Layout dua lajur (terjemahan kiri + Arab kanan)
  ├── Panel kitab + bab di kiri
  └── Butang Simpan + Baca penuh

Hari 3-4: Integrasi
  ├── Sambung ke hadis API
  ├── Pagination
  └── Bookmark integration

Hari 5: Responsive + ujian
```

#### Fasa 4: Detail + Pencarian + Tetapan (Minggu 4)

```
Hari 1-2: Detail page
  ├── Kekalkan layout dua lajur
  ├── Tukar warna ke AQUA
  └── Pastikan breadcrumb + nav berfungsi

Hari 3: Pencarian
  ├── Hero compact
  ├── Draf AI jawapan
  └── Hasil dwibahasa

Hari 4: Tetapan
  ├── Kekalkan layout panel gelongsor
  ├── Tukar warna ke AQUA
  └── Uji semua kawalan

Hari 5: Ujian integrasi penuh
```

### 3.4 Konsistensi Visual

```
Semua halaman mesti:
✅ Gunakan alpha yang sama: 20/255 untuk panel kaca
✅ Gunakan BORDER_GLASS yang sama: rgba(62, 201, 176, 60/255)
✅ Gunakan BackgroundCanvas yang sama (hanya halaman utama telus)
✅ Gunakan FONT_SCALES yang sama (kekal dari tema sedia ada)
✅ Lulus ujian kontras WCAG AA (semua tier teks ≥ 4.5:1)
```

---

## 4. Jadual Pelaksanaan Penuh

```
MINGGU 1:
├── Hari 1-2: Unit tests (conftest + test_helpers + test_db)
├── Hari 3-4: Baiki set_theme() Peringkat 1 + 2
└── Hari 5: Ujian set_theme() + mula halaman utama

MINGGU 2:
├── Hari 1-3: Halaman utama Split Command Center
├── Hari 4-5: Rak Digital Interaktif
└── Hari 6-7: Responsive + polish

MINGGU 3:
├── Hari 1-3: Senarai Hadis Dwibahasa
├── Hari 4-5: Detail + Pencarian
└── Hari 6-7: Tetapan + integrasi

MINGGU 4:
├── Hari 1-3: Unit tests (lengkap semua layer)
├── Hari 4-5: Ujian integrasi penuh
├── Hari 6: Dokumentasi + changelog
└── Hari 7: Buffer (bug fixes)
```

---

## 5. Risiko & Mitigasi

| Risiko | Kesan | Mitigasi |
|--------|-------|----------|
| `unpolish/polish` tidak mencukupi untuk 53 inline styles | Tinggi | Fallback ke _build() untuk tema ini sahaja |
| BackgroundCanvas lambat pada PC lama | Sederhana | Optimumkan lukisan, beri toggle "kurang animasi" |
| FTS5 pecah selepas refactor | Tinggi | Unit tests wajib lulus sebelum commit |
| Konflik merge dengan kod sedia ada | Sederhana | Buat branch berasingan untuk setiap fasa |
| Responsive design tidak stabil | Rendah | Uji pada 3 saiz skrin minimum |

---

## 6. Kejayaan

```
✅ Semua unit tests lulus (pytest tests/ -v)
✅ set_theme() < 10ms (ukur dengan time.perf_counter)
✅ Tiada widget dicipta semula semasa tukar tema
✅ Semua 6 halaman konsisten dengan SELECTED_UIUX.md
✅ Lulus ujian kontras WCAG AA
✅ Responsive pada 900×560 hingga 1920×1080
```

---

## 7. Status

- ✅ Dokumen ini dihasilkan.
- ⏳ Menunggu keputusan pengguna untuk mulakan pelaksanaan.
