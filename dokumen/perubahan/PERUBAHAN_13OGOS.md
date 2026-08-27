# Perubahan 13 Ogos 2026 — Sesi 55 (lanjutan)

> Log ringkas perubahan pada 13 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md` (entri "Lanjutan (Sesi 55)"
> di hujung fail). Versi apl kekal **1.0** — kerja ini ialah
> penambahbaikan dalam edaran semasa, bukan perubahan versi.

## Kandungan sesi (5 commit)

1. **App seperti mockup: buang baris Salin/Kongsi bawah tab + lalai teks
   Arab = Kecil** (`c306f88`) — label "BAHASA MELAYU" + butang 📋 Salin /
   💬 Kongsi di bawah tab bahasa DIBUANG supaya teks terjemahan tidak
   jatuh ke bawah; lalai saiz teks Arab ditukar 1 (Sederhana) → **0
   (Kecil, 0.85)** supaya lajur kiri padat; butang "Set Semula" pulang ke
   `1, 0, 1`.
2. **Ujian: kunci Set Semula → Arab Kecil + hadis panjang, baiki flak
   tangkapan** (`147a0cb`) — semakan fizikal "Set Semula" dan semakan
   hadis panjang (>1500 aksara); punca flak 93 B dijumpai: badan
   `_paksa_hadapan` tersilap keluar ke aras `skrin_fizikal` (hanya
   docstring), jadi semua panggilan retry tiada kesan — kini
   SW_RESTORE/TOPMOST berjalan setiap cubaan (stabil 3×68/0).
3. **Buang tab Sebelah + jamin teks terjemahan sama paras dengan Arab**
   (`0742a10`) — lihat seksyen di bawah.
4. **Baiki draf jawapan AI: bahagian "Carian Biasa (Keyword)" kini
   dipapar** (`0333040`) — lihat seksyen di bawah.
5. **Ujian runtime draf jawapan AI** (`90b04fc`) — `uji_draf_jawapan.py`
   9/9, daftar dalam `uji_pra_hantar.py` sebagai ujian #11.

## Keputusan: buang tab Sebelah + teks sama paras (keputusan pengguna)

- Tab **"Sebelah"** (bandingan Melayu vs Indonesia) **dibuang** — bukan
  dalam mockup (3 tab sahaja), dan teks di dalamnya tidak sama paras
  dengan Arab. `LangTabs` kini Melayu | Indonesia | English; fungsi
  "Salin semua bahasa" (milik tab itu) dibuang sekali.
- **Punca centering dijumpai**: Qt memusatkan widget saiz tetap dalam
  `QVBoxLayout` bila ada ruang menegak berlebihan (dibuktikan dengan
  ujian terpencil). Bila lajur Arab lebih tinggi, teks terjemahan jatuh
  ke tengah. Pembaikan: `Qt.AlignTop` pada setiap widget + `addStretch`
  di hujung kotak terjemahan supaya ruang lebih tinggal di bawah teks.
- Pengesahan: `uji_bandingan.py` **48/0** (termasuk kes baharu "Arab >>
  terjemahan", beza < 40px) · mockup **130/0** (kontrak `tab_lang` kini
  padan) · regresi tangkapan 7/7 (baseline `--kemas`).

## Keputusan: pembetulan bahagian "Carian Biasa (Keyword)" dalam draf AI

**Bug (dilaporkan pengguna 13 Ogos)**: setiap kali carian makna AI
berjaya, `TypeError` ditangkap SENYAP, jadi bahagian **"🔍 Carian Biasa
(Keyword)"** dalam kotak Jawapan Draf AI **tidak pernah muncul** —
walaupun kodnya wujud dan nampak berfungsi.

**Punca** di `core/draft_answer.py` (dua kesilapan, kedua-duanya lempar
TypeError yang dibasuh `except Exception: pass`):

1. `api.search_hadis(query, per_page=5)` — parameter sebenar ialah
   `limit` (tandatangan `api/hadis_api.py:456`) → `TypeError: unexpected
   keyword argument 'per_page'`.
2. Baca `exact["data"]["results"]` — `search_hadis` memulangkan
   `{"hadis": [...], "meta": {...}}` (`api/hadis_api.py:523`), bukan
   `{"data": {"results": [...]}}` → TypeError kedua.

Akibatnya `exact_results` sentiasa `[]` → bahagian Keyword tidak pernah
dipapar.

**Pembetulan**:
```python
exact = api.search_hadis(query, limit=5)
if exact and exact.get("hadis"):
    result["exact_results"] = exact["hadis"][:5]
```

**Pengesahan langsung**: `compose_draft_answer("solat", semantic_results=[])`
kini pulang 5 hasil exact; jawapan mengandungi "Carian Biasa (Keyword) —
5 hasil" dengan hadis sebenar (Ibnu Majah #1403, Ahmad #21208, Abu Daud
#675) + "Preview Hadis Teratas".

**Audit corak sama**: imbasan seluruh kod (`core/`, `ui/`, `api/`, `sync*`)
mendapati TIADA kes lain. Semua panggilan lain betul: `ui/workers.py`
(`limit=` + `.get("hadis")`), `sync.py` (`limit=` + `.get("hadis")`),
pembungkus `hadis_api.py` (`d["data"]` pada respons mentah `_request`
adalah betul), `hadeethenc_api.py` (`per_page` ialah parameter URL API
luaran, bukan kwarg Python), `sync_sema.py` (`indeks["data"]` ialah JSON
tempatan).

**Regresi dikunci dua aras**:
- semak.py **8t2** (statik): `search_hadis(query, limit=5)` + `exact["hadis"]`
  mesti kekal; `per_page=5` / `exact["data"]["results"]` tidak boleh
  kembali.
- `uji_draf_jawapan.py` **9/9** (runtime): (1) `exact_results` terisi +
  hasil wujud dalam `hadis.db`; (2) "Carian Biasa (Keyword)" wujud dalam
  jawapan + menyebut hasil pertama; (3) sandaran statik corak lama.
  Kepekaan mutasi disahkan: corak lama disuntik → **6 GAGAL**, pulih →
  **9/0**.

## Fail yang diubah (13 Ogos)

| Fail | Perubahan |
|---|---|
| `ui/app_qt.py` | Lalai `arabic_font_idx` 1 → 0 (Kecil) |
| `ui/settings_panel.py` | "Set Semula" → `1, 0, 1` |
| `ui/pages_detail.py` | Buang baris Salin/Kongsi bawah tab; buang cabang "sebelah" + `_copy_semua_bahasa`/`_teks_semua_bahasa`; `Qt.AlignTop` + `addStretch` (sama paras) |
| `ui/pages.py` | `LangTabs`: 3 tab sahaja (tiada Sebelah) |
| `ui/helpers.py` | Kunci "sebelah" dalam `LANG_LABEL` dibuang |
| `core/draft_answer.py` | `search_hadis(query, limit=5)` + `exact["hadis"]` |
| `semak.py` | 8i ditulis semula (3 tab + sama paras); semakan 8t2 baharu (draf jawapan) |
| `uji_bandingan.py` | Ganti ujian Sebelah → 3 tab + kes "Arab >> terjemahan" |
| `uji_end_to_end.py` | Semakan tab Sebelah → 3 tab |
| `uji_visual_sebenar.py` | Set Semula fizikal + hadis panjang; baiki `_paksa_hadapan` (flak 93 B) |
| `uji_draf_jawapan.py` | **BAHARU** — ujian runtime draf jawapan AI (9/9) |
| `uji_pra_hantar.py` | Ujian #11: uji_draf_jawapan |
| `uji_visual_bandingan.py` | **DIPADAM** (tab yang diuji sudah tiada) |
| `dokumen/imej/*.png` | Baseline tangkapan dikemas (`--kemas`) |
| `dokumen/*` | README, MANUAL_PENGGUNAAN, MULA_SINI, MANUAL_REFERENSI_DEV, CHANGELOG, TRANSFORMASI_DETAIL, sesi_index dikemas |

## 5 commit sesi ini (13 Ogos 2026)

| Commit | Kandungan |
|---|---|
| `c306f88` | App seperti mockup: buang baris Salin/Kongsi bawah tab + lalai teks Arab Kecil |
| `147a0cb` | Ujian: kunci Set Semula → Arab Kecil + hadis panjang, baiki flak tangkapan |
| `0742a10` | Buang tab Sebelah + jamin teks terjemahan sama paras dengan Arab |
| `0333040` | Baiki draf jawapan AI: bahagian "Carian Biasa (Keyword)" kini dipapar |
| `90b04fc` | Ujian runtime draf jawapan AI: exact_results + bahagian Carian Biasa |
| `911ef7b` | Dokumen 13 Ogos: PERUBAHAN_13OGOS.md + rujukan CHANGELOG + header Sesi Terakhir |
| `287db0a` | CHANGELOG v1.0: entri perubahan pengguna 13 Ogos (draf AI + tab Sebelah) |
| `14a0ede` | Pautan silang konsisten: semua pintu masuk rujuk PERUBAHAN_13OGOS + TRANSFORMASI_DETAIL |

## Pengesahan akhir (suite pra-hantar penuh)

Tiga larian berturut-turut selepas SEMUA perubahan sesi ini (kod + ujian +
dokumentasi) — kesemuanya **SEMUA LULUS, 11/11 ujian**:

| Larian | Masa | Keputusan |
|---|---|---|
| 1 | 395.6s | SEMUA LULUS (exit 0) |
| 2 | 392.6s | SEMUA LULUS (exit 0) |
| 3 (selepas kemas kini MULA_SINI) | 392.9s | SEMUA LULUS (exit 0) |

Ujian: semak.py (0 GAGAL) · uji_negatif_8z · uji_visual_mockup (130/0) ·
uji_visual_piksel · uji_visual_sebenar · uji_tukar_tema · uji_bandingan
(48/0) · uji_lompat_fungsi · uji_end_to_end (18/0) ·
bina_tangkapan_dokumentasi (7/7) · uji_draf_jawapan (9/9). Pokok kerja
bersih (git status kosong). Kestabilan tiga larian berturut-turut
mengesahkan tiada flak selepas semua perubahan kod + dokumentasi.

**UJIAN ZIP DARI FOLDER BERNAMA DENGAN RUANG (13 Ogos, petang)**: ZIP
dibina semula (120 fail, 1.1 MB, guna `git ls-files` tolak `_arkib/`,
`.agents/`, `.opencode/`, `.freebuff/`, `bukti_visual/`, data
`hadis.db`/cache/kunci/mockup) dan diekstrak ke `D:\Pustaka Quran Hadis\
Ujian Ruang` (nama folder mengandungi ruang). **Pepijat tersembunyi
dijumpai**: semakan semak.py **9b (peraturan fail sisa untracked)**
menyuntik fail ujian dan menjangkakan `git` mengesannya sebagai
untracked — tetapi folder pengguna (hasil ekstrak ZIP) **BUKAN repo
git**, jadi `_senarai_untracked_git()` pulangkan `[]` dan semakan
sentiasa GAGAL dalam edaran. **Pembetulan**: 9b kini melangkau (lulus
dengan nota "folder bukan repo git (edaran ZIP) -- peraturan fail sisa
dilangkau") apabila tiada `.git`; dalam repo pembangunan ia kekal aktif
(disahkan: fail sisa masih dikesan). Selepas pembetulan, dari folder
berruang: `semak_versi.py` (23 ciri v1.0 hadir) + `semak.py` **SEMUA
LULUS 0 GAGAL** + app_qt diimport (VERSI 1.0). Folder ujian dibuang;
ZIP akhir `PustakaHadith.zip` (120 fail, 1,103,530 bytes).

**SENARAI RASMI FAIL ZIP + 2 PEMBETULAN PEMBINAAN (13 Ogos, petang):**
`manual/manual/MANUAL_INSTALASI.md` seksyen 9 baharu "Kandungan ZIP edaran (senarai
rasmi)" — jadual ringkasan 7 bahagian (Akar 51, `api/` 2, `core/` 9,
`ui/` 16, `utils/` 3, `scripts/` 3, `dokumen/` 36 = 120 fail) +
senarai penuh dalam blok kod + pengecualian telus + seksyen 10
"Pengesahan edaran". Semasa mengesahkan senarai (skrip banding ZIP ↔
dokumen), **2 pepijat pembinaan ZIP dijumpai**: (1) padanan pengecualian
`.env` tersilap kecualikan `.env.example` (template persekitaran hilang
dari ZIP) — dibaiki dengan padanan TEPAT `.env`/`.env.local` sahaja;
(2) `opencode.json` (konfigurasi AI dev) tersilap MASUK ZIP — kini
dikecualikan. ZIP dibina semula (120 fail, 1,105,754 bytes) dan disahkan
semula dari folder berruang: `.env.example` ada, `opencode.json` tiada,
`semak.py` SEMUA LULUS 0 GAGAL.

**BAR TINDAKAN BAWAH TEKS ARAB (tiru sunnah.com, 13 Ogos malam):**
Pengguna minta `Report Error | Share | Copy ▾` di bawah teks Arab
seperti sunnah.com/bukhari/1. Ditambah dalam `ui/pages_detail.py`
(lajur Arab, selepas `_ar_stack`): tiga butang kecil `⚠ Lapor Ralat |
💬 Kongsi | 📋 Salin ▾`. `Lapor Ralat` membuka `sunnah_url` hadis itu
dalam pelayar (lapor di sumber); `Kongsi` = `_share_bahasa_semasa`
(WhatsApp); `Salin ▾` membuka **menu popup** (`QMenu` di bawah butang)
dengan 3 pilihan: Salin Arab sahaja / Salin terjemahan (bahasa semasa)
/ Salin semuanya (rujukan + Arab + terjemahan). PENTING: bar ini DI
LAJUR ARAB (bukan bawah tab terjemahan) — tidak menolak teks
terjemahan ke bawah, jadi keputusan "sama paras" kekal. Ujian
`uji_bandingan.py` +2 semakan (bar 3 butang + menu 3 pilihan) → 50/0.
**KEMASKINI (arahan pengguna "alih ke bhg bawah terjemahan")**: bar
dipindahkan dari lajur Arab ke **bawah teks terjemahan** (lajur kanan,
selepas `_trans_box`) — tetap selepas kotak terjemahan supaya teks
tidak ditolak ke bawah dan paras Arab == terjemahan kekal. Ujian
`uji_bandingan.py` semakan bar + semakan "paras kekal" → 51/0.
**DIBUANG (arahan pengguna "buang kotak kekal teks sahaja")**: bar
`Lapor Ralat | Kongsi | Salin ▾` dibuang SEPENUHNYA — paparan
terjemahan kembali TAB + teks sahaja (keputusan mockup Sesi 55).
Kaedah `_lapor_ralat`, `_menu_salin_arab`, `_salin_ke` + import
`QMenu`/`QPoint`/`QCursor` dibuang (kod mati). Ujian bar dibuang;
`uji_bandingan.py` kembali 48/0.
Flak sedia ada dijumpai & dibaiki: ujian ini menjangka tetapan lalai
saiz Arab (ar_idx=0) tetapi `user_settings.json` sedia ada boleh
menyimpan ar_idx=3 → semakan skala GAGAL. Ujian kini sandarkan +
pulihkan user_settings.json (tulis lalai DENGAN `deklarasi_dibaca`
supaya dialog deklarasi modal tidak menyekat offscreen). Disahkan:
semak.py 0 GAGAL · mockup 130/0 · bandingan 50/0 · end-to-end 18/0.

**PENGESAHAN AKHIR (suite pra-hantar penuh, selepas pembuangan bar
— 13 Ogos malam)**: `uji_pra_hantar.py` **SEMUA LULUS 11/11** dalam
satu larian (405.5s, exit 0): semak.py (0 GAGAL) · uji_negatif_8z ·
uji_visual_mockup (130/0) · uji_visual_piksel · uji_visual_sebenar ·
uji_tukar_tema · uji_bandingan (48/0 — kembali ke bilangan asal
selepas semakan bar dibuang) · uji_lompat_fungsi · uji_end_to_end
(18/0) · bina_tangkapan_dokumentasi (7/7) · uji_draf_jawapan (9/9).
Pokok kerja bersih.

**BAR DIPULIHKAN — BAWAH TERJEMAHAN, SUDUT BAWAH KANAN (keputusan
akhir pengguna)**: selepas "buang kotak kekal teks shj", pengguna
meminta bar diletak semula: "letak bawah terjemahan sudut bawah
kanan". Bar `Lapor ralat | Kongsi | Salin` kini di lajur kanan
selepas `_trans_box`, dijajarkan ke KANAN (`addStretch(1)` di kiri).
`Salin` membuka menu popup (Arab / terjemahan / semuanya); `Lapor
ralat` buka sunnah_url; `Kongsi` = WhatsApp bahasa semasa. Diletak
selepas `_trans_box` supaya paras Arab == terjemahan kekal. Disahkan:
uji_bandingan **52/0** (+4 semakan: 3 butang, spacer kiri, urutan,
menu 3 pilihan) · mockup 130/0 · semak.py 0 GAGAL. Tangkapan skrin
bukhari#1 gelap + terang dikemas (`bukti_visual/bukhari1_*.png`).

**BAR DIBUANG SEMULA — KEKAL TEKS SAHAJA (arahan pengguna, malam 13
Ogos)**: pengguna mengulangi "saya mahu teks sahaja bukan butang" dan
melaporkan menu `Salin` 3 pilihan tidak berfungsi. Bar `Lapor ralat |
Kongsi | Salin` di bawah terjemahan dibuang SEPENUHNYA sekali lagi;
kaedah `_lapor_ralat`, `_menu_salin`, `_salin_ke` + import
`QMenu`/`QPoint`/`QCursor` dibuang (kod mati). Paparan terjemahan
kembali TAB + teks sahaja (keputusan mockup Sesi 55). Tindakan kekal
di bar tajuk (💬 WhatsApp / 📋 Salin / 🔊 Dengar / Simpan) + menu klik
kanan. Disahkan: semak.py 0 GAGAL · uji_bandingan **50/0** (+2 semakan
negatif: TIADA butang 'Lapor ralat' / 'Salin' berlabel biasa) ·
mockup 130/0 · bina_tangkapan_dokumentasi **7/7** (nmad=0.0000 —
rupa tepat sama baseline teks sahaja 12 Ogos).

**BAR DIPULIHKAN SEBAGAI TEKS — BUKAN BUTANG (keputusan sebenar
pengguna, malam 13 Ogos)**: pembuangan bar itu SALAH FAHAM. Pengguna
menjelaskan: "'Lapor ralat | Kongsi | Salin' kenapa buang? saya mahu
text bagitu bukan button" — bar MESTI KEKAL tetapi sebagai **Teks**
(pautan, tiru sunnah.com 'Report Error | Share | Copy'), bukan
QPushButton. Bar dibina semula di bawah terjemahan (sudut bawah
kanan, `addStretch` di kiri) sebagai SATU `QLabel` HTML: pautan teal
`Lapor ralat | Kongsi | Salin` dengan pemisah `|` kelabu (warna ikut
tema via `TEAL`/`TEXT_SECONDARY`). Kaedah `_lapor_ralat`/`_menu_salin`/
`_salin_ke` + import `QMenu`/`QCursor` dipulihkan. **Pembaikan punca
"3 pilihan tak fungsi"**: menu Salin kini dibuka pada `QCursor.pos()`
(bukan di bawah butang) supaya sentiasa kelihatan walaupun bar di
hujung skrol. Disahkan hidup (papan klip diuji): pilihan 1 Arab →
klip = teks Arab; pilihan 2 terjemahan → klip = terjemahan bahasa
semasa; pilihan 3 semuanya → klip = rujukan + Arab + terjemahan —
SEMUA BERFUNGSI. Ujian: semak.py 0 GAGAL · uji_bandingan **52/0**
(+4: bar teks wujud, bukan butang, menu 3 pilihan, `_salin_ke`
menyalin) · mockup 130/0 · bina_tangkapan_dokumentasi 7/7 (nmad ≤
0.0007, dalam toleransi — baseline tidak perlu dikemas).

**PILIHAN SALIN KE-3 DITUKAR (arahan pengguna, hujung 13 Ogos):**
pilihan ke-3 menu Salin ditukar daripada "Salin semuanya (rujukan +
Arab + terjemahan)" (`_copy`) kepada **"Salin Arab + terjemahan
semasa"** (`_salin_arab_terjemahan` baharu) — salin Arab + terjemahan
bahasa yang aktif SEKARANG (Melayu/Indonesia/English), TANPA baris
rujukan. Ujian: uji_bandingan **53/0** (pilihan ke-3 disemak dengan
bahasa Indonesia aktif — klip = Arab + terjemahan Indonesia, tiada
"No."). Kerja hari ini selesai — sambung esok.

**TEXT TERJEMAHAN DIJUSTIFY (arahan pengguna, malam 13 Ogos):**
"saya nak awak justify text terjemahan" — teks terjemahan dalam kotak
bahasa (kanan) kini dijajarkan kiri-kanan penuh (`text-align:
**PANEL TRANSLITERASI DIJAJARKAN KE ATAS (arahan pengguna, malam 13
Ogos):** "transliterasi jgn center vertical. top vertical." — panel
transliterasi dalam lajur Arab dipusatkan menegak oleh Qt bila lajur
lebih tinggi; kini `Qt.AlignTop` pada panel + setiap kandungan +
`addStretch(1)` di hujung (corak sama pembaikan Sesi 55 kotak
terjemahan). Ujian baharu `uji_bandingan.py` 7e (mock model
transliterasi, tanpa torch): panel y ≤ 30px — uji_bandingan **55/0**.

justify`). Pelaksanaan: parameter `justify=True` pada `text_browser`
(ui/widgets.py) — `document().setDefaultTextOption(QTextOption(
Qt.AlignJustify))` (berfungsi dengan `setPlainText`, tanpa HTML
escape); diaktifkan pada SEMUA teks terjemahan/rumi dalam
ui/pages_detail.py (8 panggilan): kotak terjemahan `_switch_lang`,
transliterasi (Gaya Melayu + Akademik), huraian SemakHadis
(terjemahan/takhrij/komentar), huraian HadeethEnc
(terjemahan/penjelasan/pengajaran). Teks Arab (RTL) kekal tidak
justify — betul dari segi tipografi. Baseline `dokumen/imej/*.png`
dikemas dengan `--kemas` (perubahan reka bentuk sah). Disahkan:
semak.py 0 GAGAL · uji_bandingan 53/0 · mockup 130/0 · tangkapan
7/7 (nmad=0.0000 selepas kemas).
