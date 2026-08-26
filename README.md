# PustakaHadith

A digital library of **62,169 hadiths** from the 9 primary books (Kutub al-Tis'ah), featuring keyword search, semantic search (AI), SemakHadis.com commentaries, scholar grading (darjat), syarah, transliteration, and translations in Malay, Indonesian, and English.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Semantic Search (AI)](#semantic-search-ai)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

| Feature | Details |
|---|---|
| **9 Hadith Books** | Bukhari, Muslim, Abu Daud, Tirmizi, Nasa'i, Ibnu Majah, Ahmad, Darimi, Malik |
| **62,169 Hadiths** | Stored in SQLite (`hadis.db`) with FTS5 index |
| **Combined Search** | Keyword search (FTS5) + semantic search (AI) run in parallel |
| **AI Draft Answer** | Summary of top semantic matches + references |
| **SemakHadis.com Commentary** | 4,237 hadiths — title, syarah, and grading info (attribution displayed) |
| **HadeethEnc Fallback** | 310 matn matches — Malay commentary shown when SemakHadis unavailable (v1.1) |
| **Scholar Grading (Darjat)** | 63,930 records — Sahih/Hasan/Da'if classifications per scholar assessment |
| **Chapter Division** | 31,322 chapter records for thematic navigation |
| **Search Assist Message** | When keyword search returns 0 but AI finds matches, explains why and guides to semantic results |
| **Dual-Column Language Tabs** | Detail view: right column **ARAB \| TRANSLITERATION** (2 romanization styles), left column **Malay \| Indonesian \| English** — RTL layout (Arabic right, translations left, 14 Aug) · translation text always aligned with Arabic |
| **Action Bar `Report \| Share \| Copy`** | Below translation (like sunnah.com): Report → sunnah.com; Share → WhatsApp per current language; Copy → 3 options (Arabic only / current translation / Arabic + current translation). 💬 WhatsApp also in title bar |
| **Splash Screen** | Semantic model loading phase shown with progress bar — user knows app isn't frozen; skippable by click (v1.3) |
| **Jump Direct to Hadith** | Type `bukhari 433`, `B433`, `b:433` in search to open book at hadith number, or `433` alone to open detail directly; "Jump to Hadith #" box above list + `Ctrl+G` shortcut on book page (v1.3) |
| **Errors Translated to Malay** | 23 runtime error patterns (sqlite3/requests/OSError/faiss/HTTP/JSON) mapped to user-friendly messages before display |
| **Syarah & Transliteration** | Arabic transliteration and additional syarah |
| **4 Languages** | Arabic, Malay, Indonesian, English |
| **Bookmarks** | Save favorite hadiths |
| **Offline Mode** | All data local — no internet required after installation |

---

## Installation

This application is distributed as a **standalone Windows application** — **no Python required**.

### 1. Microsoft Store (MSIX) — *Coming Soon*

Open **Microsoft Store** → search **"PustakaHadith"** → click **Install**.

> *Requires Partner Center registration — in progress. Panduan daftar:
> `dokumen/rujukan/DAFTAR_MSIX_STORE.md`.*

### 2. Inno Setup EXE — **Ready**

1. Download `PustakaHadith-Setup-1.0.0-x64.exe` from official site / GitHub Releases.
2. Double-click → follow installation wizard (Malay language).
3. Choose install folder (default: `%LOCALAPPDATA%\Programs\PustakaHadith`).
4. Tick "Create Desktop shortcut" if desired.
5. Click **Finish** — app ready to use.

**Upgrade:** Run new installer over existing — your data (settings, bookmarks, hadith data) **is preserved**.

**Uninstall:** *Settings → Apps → Installed apps → PustakaHadith → Uninstall* (user data remains in `%LOCALAPPDATA%\PustakaHadith`).

### 3. Portable ZIP — **Ready**

1. Download `PustakaHadith-portable-1.0.0-x64.zip`.
2. **Extract fully** to a folder (e.g., `D:\PustakaHadith`). **Do not run from inside ZIP.**
3. Double-click `PustakaHadith.exe`.
4. For easy access: right-click `PustakaHadith.exe` → **Send to → Desktop (create shortcut)**.

**No system installation** — delete = remove folder. User data persists in `%LOCALAPPDATA%\PustakaHadith`.

---

### System Requirements

| Item | Minimum |
|---|---|
| **OS** | Windows 10 / 11 (64-bit) |
| **RAM** | 4 GB (8 GB+ recommended) |
| **Disk Space** | 2 GB (app 1.4 GB + user data) |
| **Internet** | Required for hadith data sync (one-time) |
| **Python** | **NOT required** — fully self-contained |

---

## Usage

```bash
python main.py
```

Launch the application, then:

1. **Search** — type a question or keywords (e.g., "hukum riba", "kelebihan bersedekah", "niat puasa"). Both keyword and semantic search run automatically; AI draft answer appears on top.
2. **View Hadith** — click a hadith card to view full: Arabic, translations, transliteration, grading, and syarah.
3. **Bookmark** — click the star icon to save hadith to bookmarks.
4. **Change Language & Font** — click the **⚙ gear** icon (top-right) for Settings panel (Arabic font, sizes, theme).

Filter search by book via the dropdown above the search box.

---

## Project Structure

```
root     : main.py launcher.py config.py db.py semak.py semak_db.py
           sync*.py VERSI.py requirements.txt
core/    : eng_source · sema_source · semantic_search · draft_answer
           hadeethenc_api · syarah_source · phase2 · phase3
ui/      : app_qt · pages · widgets · theme · workers · settings_panel
utils/   : bahasa · transliteration
scripts/ : build_faiss_index · muat_turun_sema
_arkib/  : deprecated scripts (inactive)
```

Key files:

- `main.py` — application entry point
- `db.py` — SQLite schema, FTS5 index, migrations
- `ui/app_qt.py` — PyQt5 UI (6 pages)
- `ui/workers.py` — all network/DB I/O runs in QThread
- `core/semantic_search.py` — semantic search engine (FAISS + e5-small)
- `core/draft_answer.py` — AI draft answer generator

---

## Semantic Search (AI)

Semantic search matches hadiths **by meaning**, not just exact words. Useful when your query uses different words but same meaning (e.g., searching "hukum riba" while hadith text uses "faedah").

Keyword search (FTS5) uses AND — all words must be present simultaneously. If keyword search returns 0 results but AI finds semantic matches, the app shows a help note explaining why and guides you to semantic results below.

- Model: **intfloat/multilingual-e5-small** (multilingual, ~0.46 GB)
- Index: **FAISS**, 62,169 vectors, dimension 384
- Threshold: minimum cosine similarity 0.6 (adjustable in `semantic_search.py`)

Model is auto-downloaded on first use (requires internet).

**Rebuild index** (if model/text changes):

```bash
python scripts/build_faiss_index.py
```

Check index status:

```bash
python -c "from core.semantic_search import get_index_stats; print(get_index_stats())"
```

---

## Development

Automated tests:

```bash
python semak.py                  # pre-commit checks: integrity, DB, structure, version, docs, orphan files, #12
                                 # 'Sesi Terakhir' + #15 one-page summary aligned with git log
python semak_db.py               # audit DB structure & indexes
python semak_versi.py            # check current version + promised features

# Official pre-commit suite (14 tests — semak.py + 13 suites; logs: bukti_visual/):
python uji_pra_hantar.py         # ALL PASS = safe to commit

# Negative mutation tests (semak.py actually catches bugs):
python uji_negatif_8z.py         # 55/0 — 36 branches FAILED mutated + byte-exact recovery

# Parser tests (no GUI):
python uji_lompat.py             # 'jump to hadith' parser: book spelling & format (bukhari 433, B433, b:433)
python uji_lompat_fungsi.py      # full 'jump' function: parser + page + scroll to card + open detail

# UI integration tests (launch app automatically):
python uji_data_baharu.py        # new data: chapters, grades, sema, HadeethEnc fallback
python uji_tukar_tema.py         # repeated theme switching + search, no widget leaks
python uji_end_to_end.py         # full flow: book → detail → 3 language tabs → bookmark → search
python uji_bandingan.py          # 3 language tabs (mockup), text aligned with Arabic, graceful degradation when language missing
python uji_splash.py             # splash → preload chain → model ready (~30s, real model load)
python uji_visual_sebenar.py     # real screenshots, both themes (requires display)
python uji_visual_ralat.py       # Malay-translated error toasts (real display, requires display)
```

Verification steps:

```bash
python semak.py && python semak_versi.py      # 399 checks (15 sections) + version
                                 # (build folder not git + no user cache:
                                 #  semak #12 git comparison & part #9 skipped;
                                 #  +1 for new CHECKLIST_PEMANTAUAN.md)
QT_QPA_PLATFORM=offscreen python uji_data_baharu.py   # Windows: run normally
```

Some `semak.py` checks run without data files to avoid false failures; see `_arkib/` for deprecated scripts not needed.

---

## Troubleshooting

**App crashes `WinError 1114` / DLL:** caused by MSVC runtime conflict between PyQt5 and torch. `main.py` fixes this automatically on launch. If still failing, reinstall PyQt5 (version bundling compatible runtime) and ensure `torch>=2.6` is installed.

**Semantic index missing:**

```bash
python scripts/build_faiss_index.py
```

**Model not yet downloaded:** on first semantic search, e5-small model (~0.46 GB) downloads from Hugging Face — needs internet.

**Database not found:**

```bash
python sync.py
```

---

## Verification

```bash
python semak.py && python semak_versi.py      # 399 semakan (15 bahagian) + version
                                 # (build folder not git + no user cache:
                                 #  semak #12 git comparison & part #9 skipped)
```

---

## License

Hadith data sourced from `service.hadis.my`. Commentary from **SemakHadis.com** — used with attribution in app. Before commercial distribution, obtain written permission from SemakHadis.com.

Part of this project structure summarizes the development journey; full records (design rationale, audits, sessions) in `dokumen/sesi/sesi_index.md`. Detailed before/after UI comparison (two-column layout, warm paper palette, color chips) with screenshots in `dokumen/manual/TRANSFORMASI_DETAIL.md`. Latest daily changelog (13 Aug — removed Sebelah tab, aligned text, default Arabic Small, AI draft fix): `dokumen/perubahan/PERUBAHAN_13OGOS.md`.