# Rancangan Refactor — `ui/app_qt.py` (2,428 baris)

> Ditulis 8 Ogos 2026 (Sesi 30). Analisis sahaja pada mulanya; langkah 1
> (`ui/helpers.py`) dilaksanakan serta-merta kerana ia 100% selamat.
> Sumber: `dokumen/rujukan/PANDANGAN_RISIKO.md` §1, `dokumen/manual/MULA_SINI.md` §2.A.

---

## Masalah

`ui/app_qt.py` ~100 KB / 2,428 baris — setiap ciri baharu ditambah ke
satu fail yang terus membesar. Sukar dibaca, konflik edit meningkat.

## PUNCA kesukaran (mesti difahami dahulu)

`apply_theme()` dalam `ui/theme.py` menyalin palet warna ke ruang nama
modul yang DIDAFTARAKAN secara eksplisit:

```python
_THEMED_MODULES = ("ui.theme", "ui.widgets", "ui.pages",
                   "ui.app_qt", "ui.settings_panel", "ui.splash")
```

Peraturan #4 MULA_SINI: mana-mana modul UI baharu yang `from ui.theme
import CARD_BG` **MESTI ditambah ke `_THEMED_MODULES`** — jika tidak,
tukar tema pecah. Modul yang tiada import warna (cth. `ui/helpers.py`)
tidak perlu didaftar.

Kedua: `semak.py` menyemak **teks sumber** `ui/app_qt.py` untuk beberapa
pemalar/kaedah. Jangan alih keluar tanpa mengemas semak.py:

| semak.py | Carian dalam sumber app_qt.py |
|---|---|
| 8e HadeethEnc | `_he_luar`, `HadeethEnc`, `_bina_he`, `_ATRIBUSI_HE` |
| 8f SemakHadis | `SemakHadis.com`, `_ATRIBUSI_SEMA` |
| 8i bandingan | badan `_switch_lang` (lajur, butang Salin/Kongsi) |
| 8k pemula | `kemajuan_pramuat = pyqtSignal(str)`, `siap_pramuat = pyqtSignal(bool)` |

## Struktur sebenar

| Blok | Baris | Kaedah | Saiz |
|---|---|---|---|
| Helper + pemalar | 104–207 | `_parse_lompat`, `_clear`, `_read_json`… | ~100 |
| Infrastruktur (init, tema, worker) | 209–657 | `set_theme`, `closeEvent`, `_run`… | ~450 |
| Halaman Utama | 659–733 | `_page_home`, `_from_home_search` | ~75 |
| Halaman Kitab + lompat | 735–950 | `_render_kitab_shell`, `_lompat_hadis`… | ~215 |
| Halaman Carian | 952–1250 | `_do_search`, `_tampal_gabungan` (~125) | ~300 |
| Halaman Detail | 1251–2129 | `_render_detail` (~200), `_bina_*` (~300), `_switch_lang` (~115) | **~880** |
| Tersimpan + Tetapan | 2130–2418 | `_render_saved`, `_page_settings` (~170) | ~290 |
| `main()` | 2420 | | ~10 |

## Pelan — pendekatan Mixin berperingkat

Kenapa Mixin: callbacks (`lambda: self.go(...)`, `self._run(...)`) kekal
berfungsi kerana kaedah diakses melalui `self`; state kekal pada `self`;
`set_theme()`/`_build()` tidak berubah; operasi "potong & tampal".

1. ✅ **`ui/helpers.py`** (SELESAI 8 Ogos) — pemalar + fungsi bebas tanpa
   state Qt: `_parse_lompat`, `_slug_dari_awalan`, `_normalis_kitab`,
   `_ALIAS_KITAB`, `_read_json`, `_write_json`, `_clear`, `click_sound`,
   `PAGES`, `LANG_PARAM`, `_HAD_WA`, `BASE_DIR`, `SETTINGS`, `BOOKMARKS`.
   Diimport semula oleh app_qt.py (`from ui.helpers import ...`) supaya
   `ui.app_qt._parse_lompat` dsb. kekal wujud untuk `uji_lompat.py` dan
   `settings_panel.py`. **TIDAK import warna** → tidak perlu didaftar
   dalam `_THEMED_MODULES`.
2. ✅ **`ui/pages_kitab.py`** + **`ui/pages_carian.py`** (SELESAI 8 Ogos) —
   mixin `PagesKitab` (halaman kitab + lompat) dan `PagesCarian`
   (halaman carian + semantik). `PustakaApp(PagesKitab, PagesCarian,
   QMainWindow)`. Kedua-dua didaftar dalam `_THEMED_MODULES` (PagesCarian
   import warna AMBER). `semak.py` 8g dikemas: `_tampal_gabungan` kini
   dibaca dari `ui/pages_carian.py`. Import mati dibuang dari app_qt.py
   (Pager, BookCover, ListWorker, SearchWorker).
   **Gandingan rentas mixin**: PagesCarian bergantung pada `PagesKitab`
   (`_sahkan_lompat`, `_lompat_ke`) — jangan pisahkan.
3. ✅ **`ui/pages_detail.py`** (SELESAI 8 Ogos) — mixin `PagesDetail`
   (26 kaedah): `_render_detail`, `_bina_translit/_syarah/_sema/_he/
   _darjat`, `_switch_lang`, `_share/_copy/_tts`, `_teks_*`,
   `_is_saved/_toggle_save`. `PustakaApp(PagesKitab, PagesCarian,
   PagesDetail, QMainWindow)`. Pemalar `LANG_LABEL`/`_ATRIBUSI_*`
   dialih ke `ui/helpers.py` (hanya PagesDetail import — app_qt TIDAK
   mengimport semula kerana tiada pemanggil luar). Didaftar dalam
   `_THEMED_MODULES` (PagesDetail import warna TEXT_SECONDARY).
   `semak.py` tambah `_sumber_ui()` + `_cari_fungsi()` supaya semak
   8e/8f/8i baca sumber gabungan (mixin + helpers). Import mati dibuang
   dari app_qt.py (QUrl, LangTabs, breadcrumb, Collapsible,
   arabic_browser, text_browser, HadithWorker, RandomWorker dsb.).
   **Gandingan rentas mixin**: PagesKitab/PagesCarian memanggil
   `open_detail`, `open_by_ref`, `_papar_melayu`, `_ada_syarah` yang
   disediakan DI SINI — jangan alih keluar tanpa mengemas pemanggil.
   app_qt.py kini ~875 baris (dari 2,428).
4. ✅ **`ui/pages_tersimpan.py`** + **`ui/pages_tetapan.py`**
   (SELESAI 8 Ogos) — mixin `PagesTersimpan` (halaman Hadis Tersimpan:
   `_page_saved`, `_render_saved`) dan `PagesTetapan` (tetapan API/
   paparan/fon/bahasa: `_page_settings`, `_sync_settings`, `_step`,
   `_set`, `_set_simbol_selawat`, `_set_font`, `_save_api`).
   `PustakaApp(PagesKitab, PagesCarian, PagesDetail, PagesTersimpan,
   PagesTetapan, QMainWindow)`. Kedua-dua didaftar dalam
   `_THEMED_MODULES` (PagesTetapan import warna AMBER_*/RED_TEXT/
   GREEN_TEXT/TEXT_MUTED). `semak.py`: `_sumber_ui()` + `_cari_fungsi()`
   + semak 8d (stretch) kini sertakan kedua-dua modul baharu. Import
   mati dibuang dari app_qt.py (QComboBox, QLineEdit, empty_state,
   hadith_card, AMBER_*, RED_TEXT, GREEN_TEXT, FONT_SCALE_LABELS, dsb.)
   — `_slug_dari_awalan`/`_write_json`/`SETTINGS` kekal (pemanggil luar
   uji_lompat.py/settings_panel.py). **Gandingan rentas mixin**:
   PagesTersimpan memanggil `open_by_ref` (PagesDetail); PagesTetapan
   memanggil atribut teras PustakaApp (`_run`, `_refresh_current`,
   `per_page`, `_on_collections`).
5. ✅ **`ui/pages_home.py`** (SELESAI 8 Ogos) — mixin `PagesHome`
   (halaman Utama: `_page_home`, `_from_home_search`). `PustakaApp`
   kini warisi SEMUA 6 mixin: `PustakaApp(PagesKitab, PagesCarian,
   PagesDetail, PagesTersimpan, PagesTetapan, PagesHome, QMainWindow)`.
   Didaftar dalam `_THEMED_MODULES` (tiada import warna — hanya
   COLLECTION_META). `semak.py`: `_sumber_ui()` + `_cari_fungsi()`
   sertakan ui/pages_home.py. Import mati dibuang dari app_qt.py
   (QGridLayout, Hero/KitabCard/SearchBar, attach_copy_menu,
   centered_column, make_scroll, COLLECTION_META) — `_parse_lompat`/
   `_slug_dari_awalan` kekal (pemanggil luar uji_lompat.py).
   **Gandingan rentas mixin**: PagesHome memanggil `open_kitab`/
   `_lompat_ke` (PagesKitab) dan `_buka_hadis_terus`/`_do_search`
   (PagesCarian). app_qt.py kini ~500 baris — inti sahaja (init,
   header, tema, navigasi, worker).

Setiap modul baharu yang import warna **MESTI** ditambah ke
`_THEMED_MODULES` dalam `ui/theme.py` + disahkan dengan `semak.py`
(semakan 2 & 6) + `uji_tukar_tema.py`.

## Syarat & pengawal

- **JANGAN buang import "unused" yang disasarkan `apply_theme()`**
  (import warna dari `ui.theme`) — ia sasaran penyalinan tema.
- Stdlib yang menjadi tidak terpakai selepas alih (`json`, `re` di
  app_qt.py) BOLEH dibuang — bukan sasaran tema.
- Sasaran akhir: `app_qt.py` ~600–700 baris (inti sahaja).
- **Jangan mulakan langkah 2–4 sebelum ujian mesin sebenar** (risiko
  #1 dokumen/rujukan/PANDANGAN_RISIKO.md) — kecuali pengguna arahkan sebaliknya.
- Validasi: `python semak.py` + `python uji_lompat.py` +
  `python uji_lompat_fungsi.py`.
