# Spesifikasi Reka Bentuk: Halaman Pencarian (Aqua Glass)

**Tarikh:** 26 Ogos 2026
**Keputusan sumber:** `SELECTED_UIUX.md` (bahagian "Halaman Pencarian") +
`selected_page_pencarian_1366x768.png`.

## Konteks
Halaman Pencarian sedia ada (`ui/pages_carian.py`) berfungsi penuh (carian
kata kunci FTS5 + semantik AI digabung, draf jawapan AI, penapis kitab) tetapi
paparan masih gaya hadis.my (kad Arab-atas-terjemahan-bawah, latar pepejal
tanpa glob). Mockup menghendaki gaya **Aqua Glass** sepadan halaman lain,
hasil **dwibahasa** (terjemahan kiri, Arab kanan), dan **kaedah carian**
boleh dipilih. Struktur kod dikekalkan — ini restyle *in-place*, bukan
penulisan semula.

## Keputusan daripada `SELECTED_UIUX.md`
- struktur semasa `pages_carian.py` dikekalkan;
- hero carian kompak dengan butang **Cari** berasingan;
- penapis kitab, **kaedah carian** dan bahasa;
- **draf jawapan AI dipaparkan sebelum hasil**;
- **hasil carian menggunakan terjemahan kiri dan petikan Arab kanan**
  (dwibahasa);
- gaya **Aqua Glass** dan opasiti sepadan dengan halaman lain.

## Tambahan keputusan (disahkan pengguna, 26 Ogos)
- **Kaedah carian**: togol 3-mod — `Kata kunci` / `Makna` / `Kedua-dua`
  (lalai `Kedua-dua`). Pilihan disimpan ke `user_settings.json`
  (`carian_mod`). Mengubah mod semasa hasil wujud memanggil semula carian.

## Reka Bentuk

### 1. Latar & skrol (Aqua Glass)
Akar halaman ditukar kepada `BackgroundCanvas` (glob AQUA / warna pepejal
tema lain) + `QScrollArea#homeScroll` telus + `QWidget#homeBody` telus —
pola sama Utama/rak/kitab. Hero + baris penapis + hasil duduk atas glob.

`Hero("Pencarian Hadis", compact=True)` dipaksa telus bila AQUA
(`ada_latar_imej()`) supaya glob tembus — `hero.setStyleSheet(
"QFrame#hero{background:transparent;border:none;}")`. Halaman lain yang
gunakan `Hero` (Tersimpan) tidak terkesan.

### 2. Hero + bar carian
Kekal: `Hero` kompak + `SearchBar` (butang **Cari** berasingan) + `chips`
penapis kitab. Tiada perubahan gelagat.

### 3. Baris kaedah carian (baru)
Baris baharu di atas hasil (dalam lajur tengah): label "Kaedah carian" +
3 butang `filterChip` (`Kata kunci` / `Makna` / `Kedua-dua`). Butang aktif
guna `filterChip_active`. Klik memanggil `_set_mod_carian(v)`:
- simpan `self.settings["carian_mod"] = v` → `_write_json(SETTINGS, ...)`
  (lazim import `ui.pages_tetapan`);
- segar semula gaya cip (`unpolish/polish`);
- jika ada query aktif, panggil `_do_search(1)`.

### 4. Draf jawapan AI
Dikekalkan. Dipaparkan sebelum hasil bila mod = `Makna`/`Kedua-dua` dan
ada hasil semantik. Bila mod = `Kata kunci`, draf tidak dipapar.

### 5. Kad hasil → dwibahasa
Ganti `hadith_card(...)` dengan `hadith_card_dwibahasa(...)` (widget sedia
ada dari kerja Senarai Hadis) untuk kedua-dua senarai semantik dan
kata kunci. Kad dwibahasa: No. | TERJEMAHAN (kiri) | pemisah | Arab (kanan)
+ butang 🔖. Nama kitab dipapar dalam meta kad (`faint`), tiada chip
berasingan.

🔖 disambung ke `_carian_toggle_simpan(h, card, slug, hid)` →
`self._toggle_save(h)` + segar semula `simpan_btn` (`simpanChip` /
`simpanChip_aktif`). Paparan dikemas kini tanpa muat semula penuh.

### 6. Pembolehubah mod dalam `_do_search`
`mod = self.settings.get("carian_mod", "kedua")`:
- `kata`  → jalankan hanya `SearchWorker` (tiada semantic, tiada draf);
- `makna` → jalankan hanya `SemanticWorker` (draf + hasil makna);
- `kedua` → kedua-dua serentak (gelagat semasa).

Enjin yang dilangkau ditetapkan `_sem_res = []` / `_kw_res = []` serta-merta
supaya `_tampal_gabungan` tetap tamat. Notis amber (OR-fallback / tiada
padanan kata-kata) **hanya** dipapar untuk mod `kata`/`kedua-dua`.

### 7. Status / notis / empty state
Baris status (jam berputar + "N padanan makna + M hadis ditemui"), notis
amber, dan `empty_state` + pautan SemakHadis dikekalkan.

### 8. Tetapan
`carian_mod` (lalai `"kedua"`) berterusan dalam `user_settings.json`;
dibaca semula bila halaman dibina semula (tukar tema).

### 9. QSS
Tiada baharu — guna semula `glassPanel`/`homeScroll`/`homeBody`
(`theme.py`), `kadDwi`/`noBadge`/`lineV`/`eyebrow`/`faint`/`bacaLink`/
`simpanChip`/`simpanChip_aktif`/`filterChip`/`filterChip_active` (ditambah
untuk Senarai Hadis).

### 10. `semak.py`
Tambah semakan sumber:
- `BackgroundCanvas` digunakan dalam `_page_search`;
- `hadith_card_dwibahasa` dipanggil untuk hasil carian;
- togol `carian_mod` wujud (`_bina_togol_kaedah` / `_set_mod_carian`);
- `carian_mod` lalai `"kedua"`.
Tambah ujian unit: mod `kata` melangkau semantic, mod `makna` melangkau
keyword (via pembalaman `_run`/`SemanticWorker`).

## Luar skop
- Tiada perubahan backend carian (`search_hadis`, `SemanticWorker`,
  `SearchWorker`).
- Bahasa adalah tetapan global (tidak dijadikan kawalan per-halaman).
- Halaman Tersimpan / Tetapan / Detail tidak disentuh.
