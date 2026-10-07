# Reka Bentuk: Halaman Senarai Hadis (Aqua Glass)

Tarikh: 26 Ogos 2026 · Status: DILULUSKAN (pengguna: "komit terus")
Mockup: `selected_page_senarai_hadis_1366x768.png` (terkunci)

## Matlamat

Reka bentuk semula halaman senarai hadis dalam sebuah kitab
(`ui/pages_kitab.py`, indeks stack `1` — KEKAL) daripada gaya hadis.my
kepada susun atur Split Command Center mockup: banner kaca + sidebar
bab + panel senarai dwibahasa, di atas `BackgroundCanvas` (glob AQUA,
sama pola Utama/rak).

## Keputusan Pengguna (terkunci)

1. **Kad dwibahasa** (terjemahan KIRI | Arab KANAN) — halaman senarai
   SAHAJA; carian/tersimpan/rak kekal kad lama.
2. **Chips penapis** — semua berfungsi: `Semua / Tersimpan /
   Belum dibaca` + togol `Nombor ↓/↑`.
3. **Carian banner** "Cari dalam <kitab>…" — buka halaman Pencarian
   dengan slug kitab dikunci (guna semula ciri sedia ada).
4. **Lompat No. hadis** — kekal, dipindah ke sidebar; Ctrl+G kekal.
5. **Pendekatan** — reka semula in-place (`pages_kitab.py`); tiada
   indeks/halaman baharu; semua pemanggil `open_kitab`, `_lompat_ke`,
   `_buka_hadis_terus` tidak berubah.

## Susun Atur

```
BackgroundCanvas (glob timeline AQUA / pepejal tema lain)
└─ QScrollArea#homeScroll (telus) → body#homeBody
   ├─ Banner QFrame#glassPanel
   │   ├─ eyebrow "JELAJAH KITAB / <NAMA KITAB>"
   │   ├─ H1 "Senarai Hadis" (homeH1)
   │   ├─ meta "<Nama> · N hadis · M kitab" (muted; "· M kitab"
   │   │   hanya bila senarai bab tersedia)
   │   └─ kanan: QLineEdit "Cari dalam <short>…" + butang "Cari" (primary)
   └─ Baris: [Sidebar 300px] [Panel senarai stretch]
      ├─ Sidebar QFrame#glassPanel
      │   ├─ eyebrow "KITAB SEMASA"
      │   ├─ kad sideCard: lencana <SHORT[:2]> <no urutan 2 digit>
      │   │   (noBadge, bg TEAL_PALE) + nama + "N hadis" + "M kitab"
      │   ├─ pautan "← Kembali ke rak" → go("rak")
      │   ├─ panelSection "PILIH BAB" + skrol dalaman (max ~260px):
      │   │   baris babRow ("Semua hadis" + kiraan; setiap buku:
      │   │   nama_bab + kiraan) — aktif = babRow_active (bingkai teal)
      │   ├─ panelSection "LOMPAT NO. HADIS" + _kitab_go_box
      │   │   (validator, Enter → _hantar_go_box, Ctrl+G → _focus_lompat)
      │   └─ pautan "Lihat semua M kitab →" → go("rak")
      └─ Panel QFrame#glassPanel
          ├─ kepala: eyebrow "SENARAI DWIBAHASA" + muted
          │   "Terjemahan di kiri · Petikan teks Arab di kanan"
          │   + chips filterChip (Semua/Tersimpan/Belum dibaca)
          │   + togol filterChip "Nombor ↓/↑"
          ├─ _kitab_list (kad dwibahasa, spacing 12)
          ├─ kaki: muted "Menunjukkan X–Y daripada Z hadis"
          │   + "Halaman N / M"
          └─ _kitab_pager (Pager sedia ada)
Butang ↑ ke atas (backTop) — kekal, pola lama.
```

## Kad Dwibahasa — `hadith_card_dwibahasa()` (ui/widgets.py)

ClickCard (#kadDwi), QHBoxLayout:
- `QLabel#noBadge` nombor (44×44, TEAL_PALE bg, TEAL, bold 18)
- Kolum kiri (stretch 11): eyebrow "TERJEMAHAN" → teks terjemahan
  (elide ~230, wordwrap) → meta muted "<short> <no> · <nama_bab elide>"
- Pembahagi menegak `QFrame#lineV` (1px BORDER)
- Kolum kanan (stretch 9): Arab RTL (elide ~200, 17×scale, ar_font)
  → baris bawah: "Baca penuh →" (bacaLink) + stretch + butang 🔖
  (simpanChip / simpanChip_aktif; klik → `_toggle_save(h)` + muat
  semula halaman supaya chip Tersimpan konsisten)
- Klik kad → `open_detail(h, "kitab")`; `_hid` ditanda (lompat skrol)

## API (api/hadis_api.py) + Worker

- `get_bab_list(slug) -> list[dict]` — `SELECT book,
  MIN(nama_bab) nama_bab, COUNT(*) kiraan FROM bab WHERE collection=?
  AND book IS NOT NULL GROUP BY book ORDER BY book`. Tiada DB → `[]`.
- `get_hadis_list(slug, page, limit, lang, book=None, order="asc",
  ids=None, exclude_ids=None)` — DB: WHERE tambahan `b.book=?`,
  `hadis_id IN (...)`, `hadis_id NOT IN (...)`, `ORDER BY
  hadis_id ASC/DESC`. `ids=[]` → kosong + meta total 0. Mod dalam
  talian (tiada conn): param diabaikan (didokumenkan) — UI
  menyahaktifkan chips & sidebar bab.
- `ListWorker(..., book=None, order="asc", ids=None, exclude_ids=None)`.

## Logik Penapis (chips)

- `Semua`: biasa.
- `Tersimpan`: `ids = [b["id"] for b in bookmarks if b["slug"]==slug]`;
  kosong → empty_state "Tiada hadis tersimpan dalam kitab ini".
- `Belum dibaca`: `exclude_ids = [e["n"] for e in read_history()
  if e["slug"]==slug]` (≤50).
- `Nombor ↓/↑`: order desc/asc.
- Tukar chip/bab → reset halaman 1. `Tersimpan`/`Belum dibaca` +
  sidebar bab dinyahaktifkan (tooltip "Perlu pangkalan data tempatan")
  bila `api.conn` tiada.

## Tema & QSS (theme.py, satu templat 3 tema)

Baru: `QLabel#noBadge`, `QFrame#babRow`/`_active`, `QFrame#lineV`,
`QPushButton#simpanChip`/`_aktif`, `QFrame#kadDwi`(+hover).
Guna semula: glassPanel, eyebrow, homeH1, panelSection, muted, faint,
bacaLink, filterChip/_active, backTop, primary. AQUA: PANEL_BG/BORDER_GLASS
rgba kaca; tema lain: permukaan pepejal — automatik melalui pemalar tema.

## Kes Tepi

- Koleksi tiada data bab (book NULL / tiada DB): sembunyi bahagian
  PILIH BAB + "· M kitab"; kad semasa kekal.
- `open_kitab` slug baharu: reset bab=None, tapis="semua", urutan="asc".
- Lompat (`_lompat_ke`/`_lompat_hadis`/Ctrl+G) kekal berfungsi — skrol
  ke kad via `_skrol_ke_kad` (pola rangeChanged sedia ada).
- `_kitab_root`/`_kitab_container`/`_kitab_pager`/`_kitab_go_box`
  nama atribut KEKAL (skrip uji + semak merujuk).

## Ujian

- Unit (semak.py): `get_bab_list` (DB memori), `get_hadis_list`
  book/order/ids/exclude, `_julat_lompat` kekal.
- Struktur kad dwibahasa + interaksi chips (uji skrip kecil, skrin
  sebenar).
- Tangkap skrin AQUA + neutral → Output/.
- `uji_visual_kiraan.py` dijangka perlu dikemas (banner baharu) —
  dijalankan manual selepas sync DB (nota kepada pengguna).

## Di luar skop

Kad dwibahasa di halaman carian/tersimpan/rak; penapis "Belum dibaca"
merentasi keseluruhan kitab (sejarah dihad 50); terjemahan nama bab.
