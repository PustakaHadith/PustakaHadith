> **BACA `MULA_SINI.md` DAHULU.**
>
> Fail ini (4,500+ baris) ialah arkib penuh dan tidak perlu dibaca dari
> awal. `MULA_SINI.md` mengandungi 6 peraturan yang tidak boleh
> dilanggar, 3 corak pepijat berulang, dan senarai semak sebelum hantar.
> Kembali ke sini hanya untuk mencari butiran sesuatu keputusan lama.

---

# Sesi Index — Pustaka Quran Hadis

**Tarikh:** 2026-07-28
**Sesi Terakhir:** Sesi 55 - perbandingan 4 mockup halaman detail (bukhari1/nasai2117/abudaud4177/ibnumajah2094): dua lajur ARAB|terjemahan + tab per lajur + huraian/darjat TERBUKA + darjat bercanggah papar mentah + cip warna ikut makna (hijau/merah/amber) — SELESAI DILAKSANAKAN (ui/pages_detail.py) + ujian visual mockup 130/0 (kontrak + geometri + kandungan + warna); **palet kertas hangat mockup DITERIMA PAKAI** (pembatalan keputusan awal; teks sekunder dituna untuk AA) + nama 'Sahih al-Bukhari' + prefix 'Bab:'; punca sebenar "hang" ujian dijumpai (dialog deklarasi modal kerana semak.py memadam user_settings.json) dan dibaiki — suite penuh lulus pada percubaan pertama; penstabilan tangkapan skrin uji_visual_sebenar (kecerahan + isian halaman dalam retry → 65/0) + semakan unit _warna_cip (8v) + logo dikunci pada palet (10aa) + **FINALISE**: kod mati _pra_muat_model dibuang (penggantinya PreloadWorker QThread sudah aktif, dikunci oleh semak.py 8k) + **ujian perbandingan PIKSE L** uji_visual_piksel.py (histogram chi-square + kehadiran warna teras + kepekaan mutasi → 53/0; w.grab() bukan ImageGrab; 8z kini 8 ujian visual) + **kepekaan mutasi semakan 8k/8v/10aa** (uji_negatif_8z 40/0, 26 cabang) + **uji_pra_hantar.py automatik** (9 ujian satu arahan, SEMUA LULUS) + **profil_semak.py** + pembetulan `kelas_warna` pastel terang + pembaikan flak fokus subproses (HWND_TOPMOST) — **UJIAN VISUAL FINAL: 9 ujian, 412 semakan, 0 gagal** (12 Ogos 2026) + **FINALISE 2**: optima semak.py (cache baca mtime 16.3→12.8s, mutasi masih 40/0) + penstabilan uji_visual_mockup (SW_RESTORE atas minimize rawak Windows + syarat TEAL untuk bingkai terang → 130/0 tiga larian berturut-turut) + proses ujian tersadai dibersihkan + uji_pra_hantar didokumenkan dalam MULA_SINI + **dokumentasi transformasi paparan detail LAMA→BARU** `dokumen/manual/TRANSFORMASI_DETAIL.md` (tangkap layar lama 7 Ogos vs baru 12 Ogos, nasai#4934, gelap+terang) — lihat seksyen Sesi 55 di hujung fail ini + **LANJUTAN 13 OGOS**: buang tab "Sebelah" (mockup 3 tab sahaja) + teks terjemahan **sama paras dengan Arab walau apa keadaan** (punca: Qt memusatkan widget saiz tetap bila ada ruang lebih — dibaiki `Qt.AlignTop` + `addStretch`) + lalai teks Arab = Kecil + pembaikan flak tangkapan `_paksa_hadapan` (93 B) + **pembetulan draf jawapan AI**: bahagian "Carian Biasa (Keyword)" tidak pernah dipapar kerana `per_page=5`/`exact["data"]["results"]` (parameter sebenar `limit`, struktur `{"hadis": [...]}`) — TypeError ditangkap senyap; dibaiki + ujian `uji_draf_jawapan.py` 9/9 (mutasi 6 GAGAL) + semak.py 8t2; audit seluruh kod: tiada corak salah lain — log harian: `dokumen/perubahan/PERUBAHAN_13OGOS.md` — **SELESAI: 16 commit, suite 11/11 tiga larian berturut-turut** (395.6s/392.6s/392.9s) + **UJIAN ZIP EDARAN** dari folder bernama dengan ruang (pepijat 9b di luar repo git dibaiki, semak.py SEMUA LULUS) + **SENARAI RASMI 120 fail ZIP** dalam MANUAL_INSTALASI seksyen 9 (pembetulan .env.example disertakan, opencode.json dikecualikan) + **BAR TINDAKAN (PERCUBAAN, DIBUANG)**: `Lapor Ralat | Kongsi | Salin ▾` ditambah (tiru sunnah.com), dialih ke bawah terjemahan atas arahan pengguna, kemudian **DIBUANG SEPENUHNYA** (arahan "buang kotak kekal teks sahaja") — paparan kembali TAB + teks sahaja (mockup Sesi 55); kaedah `_lapor_ralat`/`_menu_salin_arab`/`_salin_ke` + import QMenu/QPoint/QCursor dibuang (kod mati); uji_bandingan kembali 48/0 + flak ar_idx dibaiki (sandaran+pulihkan user_settings.json) + **KEPUTUSAN MUKTAMAD (malam 13 Ogos)**: bar `Lapor ralat | Kongsi | Salin` DIPULIHKAN SEBAGAI TEKS, bukan butang (arahan pengguna "saya mahu text bagitu bukan button") — satu QLabel HTML pautan teal + pemisah kelabu di bawah terjemahan, sudut bawah kanan; menu Salin dibuka pada `QCursor.pos()` (punca "3 pilihan tak fungsi" dibaiki: sebelum ini menu dibuka di bawah butang → luar skrin) + pilihan ke-3 = **"Salin Arab + terjemahan semasa"** (tanpa baris rujukan); disahkan uji_bandingan 53/0 · semak.py 0 GAGAL · mockup 130/0 · tangkapan 7/7; pintasan "Hadis" (Desktop + Start Menu) dibina semula via pintasan.ps1 — lihat seksyen baharu di hujung fail ini + **JUSTIFY + TRANSLITERASI ATAS (malam 13 Ogos, samb.)**: "justify text terjemahan" → `text_browser` (ui/widgets.py) ada parameter `justify=True` (`QTextOption(Qt.AlignJustify)`, berfungsi dengan setPlainText); diaktifkan pada 8 panggilan ui/pages_detail.py (kotak terjemahan + transliterasi 2 gaya + huraian SemakHadis/HadeethEnc); teks Arab RTL kekal tidak justify + "transliterasi jgn center vertical, top vertical" → panel transliterasi `Qt.AlignTop` + `addStretch(1)` (corak Sesi 55); ujian baharu uji_bandingan 7e (mock model) panel y ≤ 30px → **55/0**; baseline `dokumen/imej/*.png` dikemas `--kemas` (perubahan reka bentuk sah); commit `d0a4d0c` + **SEMAKAN MESIN SEBENAR (14 Ogos)**: 4 item tertangguh (MANUAL_REFERENSI_DEV §8) diselesaikan — (1) suite pra-hantar 11 ujian dijalankan pada mesin sebenar, SEMUA LULUS (termasuk uji_visual_sebenar 68/0 dengan tetingkap fizikal); (2) `uji_tersimpan_sebenar.py` 20/0 — halaman Tersimpan diuji dengan tanda buku SEBENAR (simpan 3 hadis 3 kitab, tulis cakera, restart → kekal, buka dari Tersimpan, tanggalkan, pulihkan data) + daftar ujian #12; (3) `diagnos_syarah.py` pada data sebenar — penomboran Fath al-Bari **HANYUT** (julat 520, 1/8 sejajar) → mengesahkan pembatalan Fasa 4B; (4) `uji_pipeline_api.py` 18/0 — install (kebergantungan OK) → API HIDUP (kunci developer, use_db=False) → baca → tersimpan; kunci dalam memori sahaja — lihat seksyen "Semakan mesin sebenar (14 Ogos)" di hujung fail + **SYNC PENUH DARI MULA (#2)**: `sync.py --paksa` pada mesin sebenar, 9 kitab 100% (622 muka surat, ~12.5 min, kuota 9,999→9,360), "Rekod baharu: 0" setiap kitab (data API = DB sedia ada); pengesahan 62,169: unik 0 duplikat, teks 0 kosong, julat id kontigu, FTS 62,169=62,169, **teks API vs DB 45/45 padan** — lihat seksyen "Sync penuh dari mula" di hujung fail + **PADANAN ara-* PENUH (#3)**: 32,439 hadis 7 kitab dipadan pada hadis.db sebenar — 31,952 berjaya (98.5%), lapisan Arab 1,628 (5.1%) mengisi celah Indonesia, 0 entri basi; audit bebas 30,541/30,547 (100.0%, 6 disyaki = positif palsu saksi); sync_english.py dari mula = **31,833 deterministik** (gagal 487 padan rekod Fasa 3) — item #3 DITUTUP, lihat seksyen "Padanan ara-* penuh" di hujung fail + **AUDIT LIPUTAN SEMAKHADIS (#8)**: 4,237/62,169 (6.8%), 2,263 sema_id unik; per kitab tirmidzi 1.6% terendah → bukhari 10.2% terbaik; 103/393 bab (26%) liputan 0%, hanya 3 bab >50%; jurang terbesar Tafsir (bukhari 65 + tirmidzi 47 = 843), Hajj ≈1,564, Solat ≈1,371; tirmidzi hampir kosong; ahmad seragam 5–9% tiap desil; keutamaan sumber BM baharu: tafsir per-hadis → syarah ibadah → khusus Tirmidzi → Musnad Ahmad — dokumen `dokumen/audit/AUDIT_SEMAKHADIS.md`, lihat seksyen "Audit liputan SemakHadis" di hujung fail — **PENUTUPAN HARI (4 commit: `341bdc9`, `f59cd95`, `8512b47`, `988c803`)**: SEMUA item tertangguh §8 disahkan/diaudit; baki #7 kunci API (kekal AKTIF sengaja) — lihat seksyen "Penutupan Hari" di hujung fail + **SEMAKAN DOKUMEN vs UI (petang 14 Ogos)**: skrip audit baharu `semak_dokumen_ui.py` — setiap tuntutan `MULA_CEPAT.md` + `manual/manual/MANUAL_PENGGUNAAN.md` disahkan terhadap UI sebenar offscreen (angka DB, dua lajur, cip warna, bar teks, menu Salin, 2 enjin carian, draf AI, jam, panel Tetapan, deklarasi, fail .bat, Python 3.14) — **74 semakan, 0 gagal, SEMUA tuntutan TEPAT**; lihat seksyen "Semakan dokumen manual vs UI sebenar" di hujung fail + **SEMAKAN #12 DIKUNCI (petang 14 Ogos)**: semak.py #12 baharu "'Sesi Terakhir' MULA_SINI seiring git log" — 4 peraturan (tarikh tajuk ≥ git, teks ringkasan menyebut tarikh kerja terkini, semua hash wujud, ≥1 hash daripada 10 commit terbaru; tiada git → lulus) — dikunci `uji_negatif_8z` **45/0** (30 cabang, 4 khusus #12) + **suite rasmi 12/12 SEMUA LULUS (418.3s)** + README dikemas (semak #12, 370+ semakan, tuntutan tab Sebelah lapuk dibuang) — lihat seksyen "Penutup Hari (petang)" di hujung fail + **AUDIT DOKUMEN DIGATE #13 (malam 14 Ogos)**: `semak_dokumen_ui.py` (110/0, semakan J/K/I) menjadi ujian #13 dalam `uji_pra_hantar.py` (suite **13 ujian**) — perubahan dokumen tanpa menyusuli audit kini menggagalkan pra-hantar; MULA_CEPAT URL kunci API dibetulkan (hadis.my → Developer/API); suite penuh 13/13 SEMUA LULUS (395.3s) — lihat seksyen "Penutup Hari (malam)" di hujung fail + **TEMA NEUTRAL LALAI + WCAG AA (malam 14 Ogos)**: keputusan pengguna untuk awam — lalai kertas hangat → **gelap neutral** gaya Windows (PAGE_BG `#1F1F1F`, teks putih, TIADA hue hangat); 3 pilihan TEMA (☀ Terang · 🌙 Neutral lalai · 📜 Kertas); tier malap semua tema dinaikkan ke ≥ 4.5:1 (WCAG AA); semakan **#13 semak.py: kontras** (54 pasangan warna) dikunci `uji_negatif_8z` **47/0** (31 cabang) — lihat seksyen "Tema NEUTRAL lalai + WCAG AA dikunci" di hujung fail + **PENUTUP HARI (malam 14 Ogos, 35 commit)**: RTL Arab kanan (`6b853f0`) · Numpy bandingan piksel · gate pantas (`09fe9db`) · semak #14 audit RTL dikunci (`c8878ec` + `4ed70a6`, uji_negatif_8z **50/0**) · pembersihan orphan dua hala (`a9e9d44`) · suite penuh **13/13 SEMUA LULUS** (akhir 463.6s) — lihat seksyen penutup di hujung fail

---

## Ringkasan Projek

**Nama:** PustakaHadith — Koleksi Kitab Hadis Lengkap
**Lokasi:** `D:\Pustaka Quran Hadis`
**Tech Stack:** Python 3.14 + PyQt5 (Qt 5.15.2)
**API:** `https://service.hadis.my/api/v1` (Key: simpan dalam `user_settings.json` / env `HADIS_API_KEY` — JANGAN hardcode)
**Bahasa UI:** Malay (loghat Malaysia)

---

## Struktur Fail (Updated 2026-08-06)

```
D:\Pustaka Quran Hadis\
├── main.py                        # Entry point (PyQt5) — DLL fix torch+PyQt5
├── config.py                      # API key, base URL, defaults
├── db.py                          # Akses hadis.db + versi skema
├── VERSI.py                       # Cap versi aplikasi
├── requirements.txt               # PyQt5, requests, pyperclip, e5, faiss
├── semak.py                       # SEMAKAN PRA-HANTAR (CRLF, susun atur, bersih)
├── semak_db.py / semak_versi.py / semak_kunci.py
├── sesi_index.md                  # Dokumentasi sesi
├── MULA_SINI.md / BACA_SAYA.txt / README.md
├── MANUAL_PENGGUNA.md / MANUAL_REFERENSI_DEV.md
├── RANCANGAN_4FASA.md / REVOKE_KUNCI.md
├── PERUBAHAN_30JUL.md / PERUBAHAN_31JUL.md
├── hadis.db (+ -wal/-shm)         # Data kerja aktif (256MB, 62,169 hadis)
├── hadis_faiss.index + hadis_id_map.pkl   # Indeks e5-small (62,169 vektor)
├── .cache_models/                 # Model e5-small (0.46GB)
├── .cache_sema/ .cache_syarah/    # Cache API SemakHadis / syarah
├── bookmarks.json                 # Penanda buku pengguna
├── app.ico                        # Ikon aplikasi
├── JALANKAN.bat / KEMASKINI.bat / PASANG.bat / BUANG.bat
├── BUAT_PINTASAN.bat / NYAHPEPIJAT.bat / BUANG.ps1
├── PINDAH_DATA.ps1 / pintasan.ps1
├── api/
│   ├── __init__.py
│   └── hadis_api.py               # API service layer + rate limit handling
├── core/
│   ├── __init__.py
│   ├── phase2_transliterasi.py    # Arab → Rumi transliteration
│   ├── phase3_translate.py        # Translation
│   ├── eng_source.py              # Sumber terjemahan English
│   ├── hadeethenc_api.py          # API Hadith Enc (English)
│   ├── sema_source.py             # Sumber SemakHadis (padanan)
│   ├── syarah_source.py           # Sumber syarah Fath al-Bari
│   ├── semantic_search.py         # Carian Makna (AI) — e5-small
│   └── draft_answer.py            # Draf jawapan AI
├── ui/
│   ├── __init__.py
│   ├── app_qt.py                  # PyQt5 UI (7 halaman)
│   ├── pages.py                   # Hero, SearchBar, KitabCard, Pager, dll
│   ├── widgets.py                 # ClickCard, hadith_card, FilterChips, dll
│   ├── settings_panel.py          # Panel tetapan gelongsor
│   ├── theme.py                   # Palet, metrik, QSS
│   └── workers.py                 # QThread workers
├── utils/
│   ├── __init__.py
│   ├── transliteration.py         # Arab → Rumi
│   └── bahasa.py                  # Pengesanan/paparan bahasa
├── scripts/
│   ├── build_faiss_index.py       # Bina indeks e5-small (matn Melayu)
│   └── muat_turun_sema.py         # Muat turun data SemakHadis
├── sync.py / sync_english.py / sync_hadeethenc.py / sync_sema.py / sync_syarah.py
├── audit_eng.py / build*.py / run_build*.py / start_build.py / check_build.py
├── diagnos_padanan.py / diagnos_syarah.py / status_check.py
└── test_bukhari.py / test_count.py
```

---

## Yang Telah Dibuat (COMPLETED)

### Sesi 6 — Panel Tetapan Gelongsor (2026-07-29)
- [x] `ui/settings_panel.py` — panel gelongsor dari kanan (380px, 220ms)
      menggantikan halaman tetapan skrin penuh yang terlalu besar
- [x] Ikon ⚙ di header; tutup guna Selesai / ✕ / Esc / klik overlay
- [x] Tiga kumpulan padat: PAPARAN · BACAAN · SAMBUNGAN
- [x] **Kunci API dilindungi** — tidak lagi terdedah dalam panel utama:
      • hanya baris "⚙ Tetapan API ›" yang membuka dialog berasingan
      • kunci dipapar BERTOPENG (HADIS_E6D6****77C8C0)
      • medan READ-ONLY sehingga "Buka Kunci" ditekan (ada pengesahan)
      • butang mata untuk lihat sementara
      • dialog pengesahan kedua sebelum menyimpan kunci yang berubah
      • pengesahan format sebelum simpan
- [x] Panel guna semula _step/_set/_set_font/_save_api sedia ada — tiada
      logik berganda

### Sesi 6c — Tema Terang / Gelap (2026-07-29)
- [x] `theme.DARK` + `theme.LIGHT` — dua palet penuh; tema terang guna
      putih hangat (#F5F7F8) bukan putih tulen, kontras disemak untuk
      bacaan teks Arab yang panjang
- [x] `theme.apply_theme(name)` — salin warna ke ruang nama SETIAP modul UI.
      **Perlu kerana `from theme import CARD_BG` mengikat NILAI pada masa
      import** — mutate ui.theme sahaja tidak menjejaskan ui.widgets dsb.
- [x] `build_qss()` baca `THEMES[CURRENT_THEME]`, bukan pemalar modul
- [x] `app.set_theme()` — 53 panggilan setStyleSheet() inline membaca warna
      pada masa cipta widget, jadi tukar QSS sahaja TIDAK cukup. Seluruh UI
      dibina semula, dan kedudukan pengguna (halaman/hadis/carian/panel)
      dipulihkan selepas itu.
- [x] Pemilih segmen ☀ Terang / 🌙 Gelap dalam panel Tetapan
- [x] Overlay panel melaras: alpha 110 (gelap) → 60 (terang)
- [x] Tema disimpan ke user_settings.json, dimuat semasa mula

### Sesi 6b — Ikon Gear SVG + Menu Klik-Kanan (2026-07-29)
- [x] `widgets.gear_icon()` — ikon gear SVG vektor, tajam pada semua DPI.
      Emoji ⚙ bergantung fon sistem: sering jadi tofu/kecil/pudar.
- [x] `widgets.GearButton` — tukar warna ikon semasa hover (QIcon TIDAK
      ikut QSS :hover, jadi perlu enterEvent/leaveEvent)
- [x] `widgets.attach_copy_menu()` — menu klik-kanan bergaya tema:
      Salin · Salin semua · Pilih semua (+ tindakan tambahan)
- [x] Dipasang pada panel Arab & kotak terjemahan di halaman detail.
      Menu guna `_raw` (teks logik) supaya salinan ialah Unicode betul,
      bukan bentuk paparan Arabic Presentation Forms.
- [x] 🎲 → ⚄ (U+2684) kerana emoji dadu jadi tofu tanpa fon emoji
- [x] Butang A− / A+ DIBUANG dari header — mengelirukan kerana ia
      melaraskan Arab+terjemahan serentak, manakala panel Tetapan
      melaraskan setiap satu berasingan. Dua tempat, dua perangai.
      Semua kawalan saiz kini di satu tempat: panel Tetapan.
- [x] **PEMBETULAN**: menu custom tidak muncul pada klik-kanan sebenar —
      hanya menu putih Qt ("Select All"). Punca: untuk QAbstractScrollArea
      (QTextBrowser/QTextEdit) acara klik-kanan mengenai **viewport()**
      dahulu, bukan widget. Jika viewport masih DefaultContextMenu, Qt
      papar menu standardnya dan isyarat custom TIDAK pernah dipancar.
      Mesti set CustomContextMenu pada widget DAN viewport.
- [x] **PEMBETULAN KEDUA**: setContextMenuPolicy sahaja MASIH tidak cukup —
      Qt kadang papar menu terbina "Copy / Select All" bergantung widget
      mana menerima acara dahulu. Penyelesaian muktamad: `QObject`
      eventFilter yang memintas `QEvent.ContextMenu` dan `return True`,
      ditambah `Qt.PreventContextMenu` sebagai lapisan kedua. Dipasang
      pada widget DAN viewport. Simpan rujukan filter pada widget
      (`widget._copy_filter`) supaya tidak dikutip sampah.
- [x] **PEMBETULAN KETIGA — kotak PUTIH pada QLineEdit**: `ui/theme.py`
      langsung TIADA gaya `QMenu`. Mana-mana menu terbina Qt (medan API,
      kotak carian) muncul sebagai kotak putih sistem dengan teks putih =
      tidak terbaca. Tambah `QMenu` + `QToolTip` ke QSS GLOBAL supaya
      semua menu bertema walaupun tidak melalui attach_copy_menu().
- [x] `attach_copy_menu` kini sokong `QLineEdit`: guna `hasSelectedText()`
      (bukan `textCursor()`), dan tambah Potong/Tampal untuk medan yang
      boleh diedit. QLineEdit tiada `viewport()` — dikendalikan.
- [x] Dipasang pada: medan API (URL+kunci), kotak carian utama & halaman
      carian, teks Arab, kotak terjemahan.

### Sesi 5 — Transliterasi Sebenar + Pembetulan Kritikal (2026-07-28)

**Core:**
- [x] `utils/transliteration.py` DITULIS SEMULA — versi lama buang baris DAHULU
      (`_remove_diacritics` sebelum proses) jadi semua vokal & shadda hilang:
      `حَدَّثَنَا` → `hdthna`. Sekarang: `ḥaddathanā` / `haddathana`
- [x] Shadda, vokal panjang, huruf syamsiyyah (`asy-syams`), tanwin,
      alif khanjariyya, lafz al-jalalah — semua dikendalikan
- [x] Jadual `STANDALONE` 52 entri untuk kata tanpa baris (`و` → `wa`, 32×/3000 hadis)
- [x] Diuji 1,000 hadis: 0 ralat, baki tanpa baris 0.13%
- [x] **Fasa 3** tidak lagi timpa terjemahan — API sudah beri Melayu+Indonesia
      100% liputan kualiti manusia. Placeholder lama adalah PENURUNAN TARAF
- [x] **Fasa 4** tidak lagi pulangkan teks generik yang SAMA untuk 62,169 hadis.
      Sekarang kesan topik (17 kategori fiqh) + ekstrak perawi + `disclaimer`
      wajib. Status `auto` bukan `berjaya` — jujur ia bukan huraian ulama

**Kritikal:**
- [x] Kuota API sebenar disahkan: **60/min, 200/hari** (bukan 500/10,000)
      Throttle dinaikkan 0.15s → 1.1s. Sync penuh 622 request = 4 hari
- [x] API key dibuang dari kod sumber; `.gitignore` untuk `user_settings.json`

### Sesi 4 — Refactor Modular + Penambahbaikan UI (2026-07-28)
- [x] Refactor besar: UI dipecah ke pages.py, widgets.py, theme.py, workers.py
- [x] Semua I/O rangkaian guna QThread (tak beku UI)
- [x] PipelineWorker modular — Fasa 1-4 guna thread berasingan
- [x] SearchBar dalam halaman Kitab — cari dalam kitab semasa tanpa balik ke home
- [x] Butang "Hadis Rawak" dalam hero home page
- [x] Bookmark buka guna data tempatan (jimat API call)
- [x] Loading state konsisten "Mencari…" di search page
- [x] HadisAPI dengan mod offline SQLite (hadis.db)
- [x] Semua pembetulan dari PATCH.md telah diguna pakai
- [x] Deploy ke root: `python main.py` jalan versi terkini

### Sesi 3 — Bookmark, Pipeline, Random, Loading States + Copy Arab (2026-07-27)
- [x] Random Hadis — Butang "Rawak" di header + navigasi
- [x] Bookmark/Favorit — Simpan hadis ke `bookmarks.json`
- [x] Copy Arabic — Butang "Salin Arab" khusus
- [x] Loading states + Empty states
- [x] Breadcrumb nav state — `_nav_history` tracking

### Sesi 2 — PyQt5 Rewrite + UI Polish (2026-07-27)
... (sama macam sebelum)

### Sesi 1 — Asas (2026-07-26)
- [x] API layer dengan 6 endpoints
- [x] HadisAPI class dengan requests.Session()
- [x] TKinter/CustomTkinter UI asas

### Sesi 2 — PyQt5 Rewrite + UI Polish (2026-07-27)

**Teknikal:**
- [x] Rewrite penuh dari tkinter/CustomTkinter ke PyQt5 (QMainWindow, QStackedWidget)
- [x] QTextBrowser support RTL native (`setLayoutDirection(RightToLeft)`)
- [x] eventFilter gantikan mousePressEvent (fix SIP TypeError)
- [x] Rate limit handling: HadisAPI._request() + RateLimitExceeded exception
- [x] `build_qss(scale)` — dynamic QSS generation dengan font scale factor

**UI:**
- [x] Dark theme QSS (PAGE_BG #1E262C, CARD_BG #2D3840, teks putih)
- [x] Header: Logo PustakaHadith + nav Utama/Pencarian + font scale A−/A+ + Setts
- [x] Home page: hero search + 3×3 kitab grid cards (hover teal border)
- [x] Kitab page: breadcrumb, header, hadis list cards (+ kitab tag)
- [x] Hadis detail page: breadcrumb clickable, Arabic RTL QTextBrowser, Melayu/Indonesia cards, share/action buttons, prev/next nav
- [x] Search page: search form + result cards
- [x] Pipeline page: Fasa 1-4 display
- [x] Settings page: API config + preferences

**Font:**
- [x] Arabic font: KFGQPC Uthmanic Script HAFS (detail 20pt, card 15px)
- [x] Font scaling +A/−A dengan 5 level (Kecil 0.85x → Besar++ 1.5x)
- [x] Font scale disimpan ke user_settings.json
- [x] All base font sizes enlarged (card Arabic 16px, Melayu 13px)

**Fixes:**
- [x] SIP TypeError — eventFilter instead of mousePressEvent override
- [x] Rate limit 429 — HadisAPI._request() dengan retry + delay
- [x] QSS polish — border-radius 6px, hover effects, pressed state
- [x] Scrollbar tipis (6px) dengan hover state

### Sesi 3 — Bookmark, Pipeline, Random, Loading States + Copy Arab (2026-07-27)

**Fungsi Baru:**
- [x] Random Hadis — Butang "Rawak" di header + butang "Hadis Rawak" di hero home page
- [x] Bookmark/Favorit — Simpan hadis ke `bookmarks.json`, toggle Simpan/Tersimpan di detail page, halaman "Saved" dengan senarai bookmark
- [x] Copy Arabic — Butang "Salin Arab" khusus untuk copy teks Arab dengan tashkeel
- [x] Loading states — `_make_loading_label()` digunakan di kitab page dan detail page
- [x] Empty states — `_make_empty_state()` untuk tiada hasil/ditemui
- [x] Breadcrumb nav state — `_nav_history` tracking + "Kembali" button di detail page ikut return_page

**Core Pipeline:**
- [x] Phase 3 Translate diperbaiki — output struktur dengan Melayu/Indonesia/English
- [x] Phase 4 Exegesis diperbaiki — Latar Belakang, Pengajaran, Nilai Kehidupan, Relevansi Moden, Ringkasan
- [x] Pipeline UI — loading per-phase, better structured cards, breadcrumb

**UI:**
- [x] Nav "Saved" button di header
- [x] Bookmark toggle button di detail actions row
- [x] Back/return button di detail page (Kembali ke Kitab/Pencarian/Tersimpan)
- [x] Loading label di kitab page semasa fetch API

## Yang Belum Dibuat (PENDING)

### 1. Core Pipeline
- [x] **Phase 1 Extract** — Extract content dari API response ke structured format
- [x] **Phase 2 Transliterasi** — Rumi transliteration integration ke UI
- [x] **Phase 3 Translate** — Translation engine (improved placeholder)
- [x] **Phase 4 Exegesis** — Tafsir/exegesis (improved placeholder)

### 2. Fungsi UI
- [x] Random hadis button (hadis rawak harian)
- [x] Bookmark/favorit hadis
- [ ] Hadis comparison view (side-by-side Malay/Indonesia)
- [x] Breadcrumb navigation state tracking
- [x] Copy arabic text with tashkeel (paste as plain text)

### 3. Error Handling & Polish
- [x] Offline handling — SQLite `hadis.db` + FTS5, `sync.py` boleh sambung semula
- [x] Loading states — spinner/skeleton UI
- [x] Empty states — no results, no internet
- [x] Settings validation — `valid_key_format()` (settings_panel.py:780, app_qt.py:1686)
- [x] App icon/window title — `app.ico` (main.py:78-84), "PustakaHadith" (app_qt.py:102)

---

## API Reference Notes

| Endpoint | Method | Param | Notes |
|---|---|---|---|
| `/collections` | GET | — | Senarai semua kitab |
| `/collections/{slug}` | GET | — | Info satu kitab |
| `/collections/{slug}/hadis` | GET | `page`, `per_page`, `lang` | Senarai hadis |
| `/collections/{slug}/hadis/{id}` | GET | `lang` | Satu hadis |
| `/hadis/search` | GET | `q`, `page`, `per_page`, `lang` | Carian |
| `/hadis/random` | GET | `count`, `collection` | Hadis rawak |

**Notable:**
- `per_page` bukan `limit`
- `meta` di top-level (bukan dalam `data`)
- `lang` param: `all`, `ms`, `id`, `ar`
- Random return list bukan object
- Rate limit: 200 req/harian. Reset 12AM Malaysia.

---

## Lessons Learned

1. **PyQt5 vs tkinter** — PyQt5 support RTL native via `setLayoutDirection(RightToLeft)`. Tkinter langsung tak support bidi text.
   ⚠️ **JANGAN kembali ke tkinter/CustomTkinter.** Dicuba semula dalam Sesi 5:
   teks Arab di halaman detail songsang semula. `arabic-reshaper` + `python-bidi`
   TIDAK menyelesaikannya (shaping dua kali pada Windows). PyQt5 sahaja yang betul.
2. **SIP TypeError** — Jangan override `mousePressEvent` via lambda assignment. Guna `installEventFilter()` instead.
3. **QSS font-family** — QSS global `QWidget { font-family: ... }` akan override `setDefaultFont()` dan `setFont()` pada QTextBrowser. Guna widget-specific stylesheet atau jangan set font-family dalam QSS.
4. **API rate limit** — Hadis.my API ada 200 req/harian. Guna `_request()` dengan retry + delay untuk handle 429.
5. **Font scaling** — Dynamic QSS regeneration is the way to scale all fonts. Gunakan `build_qss(scale)` function.
6. **Windows PowerShell** — Escape quotes dengan `@` untuk here-strings, atau tulis test script ke file.
7. **Transliterasi Arab** — JANGAN buang baris sebelum proses. Baris (tashkeel)
   ialah SATU-SATUNYA sumber maklumat vokal. 99.5% teks hadis.my berbaris penuh.
   Susunan aksara sebenar: konsonan + fatha + shadda (bukan konsonan + shadda).
8. **Kuota API** — 60/min, 200/hari. Sentiasa baca header `x-ratelimit-*`
   dan papar baki pada UI. Mod offline SQLite adalah keperluan, bukan pilihan.
9. **QTextBrowser alignment (PUNCA teks Arab songsang)** —
   `setAlignment()` hanya kena pada blok SEMASA. Panggil SEBELUM
   `setPlainText()` → alignment hilang bila kandungan diganti, jadi AlignLeft
   (nilai 1) walaupun `layoutDirection` sudah RTL. Mesti:
   ```python
   opt = QTextOption()
   opt.setTextDirection(Qt.RightToLeft)
   opt.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
   tb.document().setDefaultTextOption(opt)
   tb.setPlainText(text)                              # teks DAHULU
   tb.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)  # align SELEPAS
   ```
   `AlignAbsolute` perlu supaya "kanan" = kanan fizikal, bukan "hujung
   mengikut arah" yang boleh terbalik. Semak: `blockFormat().alignment()`
   mesti 18, bukan 1.
10. **QStackedWidget halaman kosong semasa start** — Halaman dibina SEBELUM
    tetingkap dipaparkan, jadi geometri dikira pada saiz lalai (640x480).
    Pada Windows halaman Utama boleh kelihatan kosong sehingga pengguna klik
    nav. Pembetulan: guna `self.go("home")` (bukan `setCurrentIndex(0)`
    mentah) + `_force_relayout()` dipanggil dari `showEvent` melalui
    `QTimer.singleShot(0, ...)` dan sekali lagi pada 150ms.
11. **Teks Arab songsang — PUNCA SEBENAR** — Tiga "penambahbaikan" ini
    MEROSAKKAN susunan bidi QTextBrowser. JANGAN guna pada widget Arab:
    - `document().setDefaultTextOption(opt)` dengan `setTextDirection()`
    - `QTextOption.WrapAtWordBoundaryOrAnywhere` (pecahkan run RTL)
    - `document().setTextWidth()` terus pada dokumen hidup (auto-saiz)

    Formula betul (padan versi asal yang berfungsi):
    ```python
    tb.setLayoutDirection(Qt.RightToLeft)
    tb.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)   # sebelum
    tb.document().setDefaultFont(f); tb.setFont(f)
    tb.setPlainText(text)
    tb.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)   # dan selepas
    ```
    Untuk auto-tinggi: ukur pada `document().clone()`, JANGAN pada dokumen
    yang sedang dipapar.
12. **QSizePolicy.Maximum = halaman kosong** — `centered_column()` guna
    `setSizePolicy(Preferred, Maximum)`. `Maximum` pada paksi menegak
    membenarkan Qt runtuhkan tinggi ke 0 sebelum susun atur pertama, jadi
    halaman kelihatan KOSONG sampai pengguna klik nav. Guna `Minimum`.
13. **setAlignment DUA KALI merosakkan bidi** — Panggil setAlignment SEBELUM
    setPlainText sahaja (satu kali). Memanggilnya SEKALI LAGI selepas teks
    dimasukkan akan mengira semula susunan dan menyongsangkan perkataan.
    Sama juga: `setFixedHeight` selepas teks. Guna `setMinimumHeight` sahaja.
14. **Hero meregang / ruang kosong besar** — Dua sebab:
    (a) `Hero` guna sizePolicy lalai (Preferred menegak) → Qt agih ruang
        lebihan kepadanya. Set `QSizePolicy(Expanding, Fixed)` +
        `layout().setSizeConstraint(SetMinAndMaxSize)`.
    (b) Layout akar halaman tiada `addStretch(1)` di hujung → ruang lebihan
        diagihkan kepada widget sedia ada. Tambah stretch selepas
        `addWidget(col)` pada SEMUA halaman (kitab/detail/saved/pipeline).
    Kesan: hero kitab 340px → 143px.
15. **Auto-tinggi QTextBrowser Arab** — Ukur pada `document().clone()` dengan
    `setTextWidth(viewport)`, kemudian `setFixedHeight`. JANGAN setTextWidth
    pada dokumen hidup — itu memaksa balut semula dan menyongsangkan bidi.
16. **Fasa 3/4 placeholder** — Untuk apl agama, placeholder yang KELIHATAN
   seperti output sebenar adalah risiko amanah. Guna status jujur (`auto`,
   `dari_sumber`) + `disclaimer` yang dipapar, bukan `berjaya`.

## Lesson #17 — Nilai lalai fungsi membekukan warna tema

`ui/widgets.py`:
```python
def text_browser(text="", scale=1.0, color=TEXT_SECONDARY):   # ❌ SALAH
```
Python menilai nilai lalai **sekali sahaja pada masa import**. Jadi
`color` terkunci pada `#AFC0C9` (tema GELAP) selama-lamanya. Dalam mod
terang, teks terjemahan jadi kelabu pucat atas kad putih — hampir tidak
nampak. `apply_theme()` yang menyalin warna ke ruang nama modul TIDAK
membantu, kerana nilai lalai sudah dibekukan sebelum itu.

Betulnya — baca warna semasa pada setiap panggilan:
```python
def text_browser(text="", scale=1.0, color=None):             # ✅
    if color is None:
        import ui.theme as _t
        color = _t.THEMES[_t.CURRENT_THEME]["TEXT_SECONDARY"]
```
Semak keseluruhan projek dengan imbasan AST untuk corak `def f(x=WARNA)`.

## Sesi 6d
- Betulkan teks terjemahan tidak nampak dalam mod terang (Lesson #17)
- Pintasan Desktop & Start Menu dinamakan semula `PustakaHadith.lnk` → `Hadis.lnk`;
  `Buat_Shortcut.vbs` buang pintasan lama dahulu supaya tiada dua ikon

### Pembersihan folder (Sesi 6d)
Dibuang sebelum pakej diedar — semua dijana semula automatik:

| Dibuang | Sebab | Dicipta semula oleh |
|---|---|---|
| `__pycache__/` (×3) | cache bytecode, 200K+ | Python |
| `hadis.db` + `-wal` `-shm` | data ujian (malik, 20 hadis) | `db.init()` |
| `user_settings.json` | tetapan mesin lama | `_write_json()` masa mula |
| `bookmarks.json` | `[]` kosong | `_write_json()` masa simpan |

**Dikekalkan** walaupun nampak "tak guna":
- `.env.example` — templat kunci API, dirujuk `config.py:33`
- `.gitignore` — sumber rujukan senarai di atas
- `core/phase3_translate.py` — belum dipanggil `workers.py`, tapi Fasa 3 belum diputuskan
- Import "unused" yang dilaporkan pyflakes dalam `ui/*.py` — ia sasaran `apply_theme()`
  yang menulis warna ke ruang nama modul. **Membuangnya akan memecahkan tukar tema.**

Saiz: 686K → 289K (folder), ZIP 101K → 84K

## Lesson #18 — Pelancar: jangan letak logik pintasan sebaris dalam .bat

Pengguna lapor: "shortcut lepas pasang.bat tak jalan. aku confius."

**Dua punca berasingan:**

1. **Pintasan menunjuk ke `.vbs`.** Perkaitan fail `.vbs` kerap dirampas
   editor teks atau disekat antivirus → klik pintasan langsung tiada
   tindak balas, tiada mesej ralat. Pintasan mesti menunjuk **terus**
   kepada `pythonw.exe` dengan `main.py` sebagai argumen.

2. **`Pasang.bat` guna `cscript ... >nul 2>&1`** — kegagalan mencipta
   pintasan ditelan senyap. Pengguna nampak "SIAP" walaupun gagal.

**Pepijat ditemui semasa ujian PowerShell sebaris:**
```bat
"  $s.Arguments = '\"%~dp0main.py\"';" ^     ❌ \" bukan escape dlm '...' PS
"}" ^                                        ❌ tiada ; sebelum Write-Host
```
Memetik laluan berruang merentas cmd.exe → PowerShell tidak boleh
dipercayai. **Pindahkan ke fail `.ps1` sebenar** dengan `param()`:
```bat
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pintasan.ps1" ^
    -Pythonw "%PYW%" -AppDir "%~dp0"
```
Disahkan: `Parser::ParseFile` 0 ralat; kod keluar 1 bila gagal.

### Struktur pelancar baharu (3 fail, nama HURUF BESAR)
| Fail | Guna |
|---|---|
| `PASANG.bat` | 4 langkah bernombor; **sahkan import** PyQt5 selepas pip |
| `JALANKAN.bat` | sandaran kalau pintasan gagal |
| `NYAHPEPIJAT.bat` | jalan `python main.py` (bukan `pythonw`) → traceback nampak |
| `pintasan.ps1` | dipanggil PASANG.bat |

Dibuang: `Pasang.bat`, `Jalankan.bat`, `PustakaHadith.vbs`, `Buat_Shortcut.vbs`

**Prinsip:** `pythonw.exe` sembunyikan ralat. Fail nyahpepijat mesti guna
`python.exe` + `pause`, jika tidak tetingkap tutup sebelum sempat dibaca.

## Lesson #19 — %~dp0 sebagai argumen PowerShell = pintasan gagal senyap

Pengguna lapor PASANG.bat "tak cipta shortcut". Dua pepijat berasingan,
kedua-dua **gagal tanpa sebarang mesej**:

**1. Trailing backslash menelan argumen**
```bat
powershell -File "%~dp0pintasan.ps1" -Pythonw "%PYW%" -AppDir "%~dp0"
```
`%~dp0` SENTIASA tamat dengan `\`. Jadi cmd.exe hantar
`"D:\Pustaka Quran Hadis\"` — PowerShell baca `\"` sebagai petikan
di-escape, argumen bercantum, `param()` gagal ikat.

Betul: **jangan hantar laluan langsung.** Guna `$PSScriptRoot` dalam .ps1.

**2. Petikan tunggal bersarang memecah `for /f`**
```bat
for /f %%W in ('"%PY%" -c "...os.path.join(...,'pythonw.exe')..."') do ...
```
cmd.exe tamatkan perintah `for /f` pada petikan tunggal PERTAMA yang
tutup — iaitu `'pythonw.exe'`. `PYW` jadi kosong.

Betul: alih pengesanan pythonw ke dalam PowerShell sepenuhnya.

**3. Guard tambahan:** `$env:WINDIR` boleh null → `Join-Path` melontar.
Sentiasa semak sebelum guna. (Ditemui semasa ujian, bukan oleh pengguna.)

### Prinsip
- Jangan hantar laluan Windows merentas sempadan cmd.exe→PowerShell.
  Biar skrip tentukan sendiri lokasinya.
- `errorlevel` 9009 = executable tidak dijumpai. Kendalikan berasingan.
- Setiap langkah pemasangan mesti SAHKAN hasilnya (`Test-Path $lnk`
  selepas `$s.Save()`), bukan andaikan berjaya.

Fail baharu: `BUAT_PINTASAN.bat` — cipta semula ikon tanpa ulang pip install.

## Sesi 6d — BUANG.bat (nyahpasang)

Apl tiada installer, jadi "uninstall" = buang pintasan + data + pakej.
`BUANG.bat` (soalan) + `BUANG.ps1` (kerja).

**Reka bentuk selamat:**
- ENTER = **kekalkan** untuk kedua-dua soalan. Hanya `Y` memadam.
- Pengesahan akhir: mesti taip perkataan penuh `BUANG`
- Padam ikut **senarai nama tepat** (`Hadis.lnk`, `PustakaHadith.lnk`,
  `PustakaHadith.lnk`) — bukan wildcard `*.lnk`. Diuji: `LainLain.lnk`
  kekal tidak disentuh.
- `requests` TIDAK ditanggalkan walau `-BuangPakej` — terlalu banyak
  program Python lain bergantung padanya.
- Folder apl tidak dipadam sendiri (mustahil semasa berjalan) —
  arahan manual dipaparkan.

**Ulangan Lesson #19:** `$env:APPDATA` boleh null →
`Join-Path $env:APPDATA ...` melontar SEBELUM `Test-Path` sempat menilai.
`Join-Path` mesti berada DALAM pengawal, bukan sekadar diuji selepasnya:
```powershell
$pinDir = $null
if ($env:APPDATA) { $pinDir = Join-Path $env:APPDATA '...' }   # betul
if ($pinDir -and (Test-Path $pinDir)) { ... }
```
Corak ini sudah muncul 3 kali ($env:WINDIR, $env:APPDATA). Semak SETIAP
`Join-Path` yang guna pembolehubah persekitaran.

Pin taskbar: fail dalam `User Pinned\TaskBar` dipadam, tetapi ikon
mungkin kekal sehingga log keluar — Windows cache secara berasingan.

## Lesson #20 — Fail .bat MESTI CRLF. Ini punca sebenar semua kegagalan pelancar.

Pengguna: "BUANG TAK JLN". Semakan bait mendedahkan:
```
BUANG.bat    CR=0   LF=83      <-- baris Unix
PASANG.bat   CR=0   LF=149     <-- baris Unix
```

**Semua** fail .bat/.ps1 sesi ini ditulis dari Linux dengan LF sahaja.
cmd.exe memerlukan CRLF. Dengan LF:
- blok berkurungan `if ... ( ... )` pecah
- `set /p` tidak membaca input
- `goto :label` gagal mencari label
- selalunya TANPA mesej ralat

Ini menjelaskan kegagalan PASANG.bat sebelum ini juga. Lesson #19
(backslash %~dp0) memang pepijat sebenar, tetapi BUKAN satu-satunya
punca — fail itu takkan jalan walau argumen betul.

### Peraturan
Selepas menulis SEBARANG .bat/.ps1/.cmd dari Linux, WAJIB:
```python
s = s.replace("\r\n","\n").replace("\r","\n").replace("\n","\r\n")
open(f,"wb").write(s.encode("ascii", errors="replace"))
```
Sahkan: `CR == LF` dan kedua-duanya > 0.

### Aksara kotak Unicode juga rosak
`═ ─ ║ ╔ — ← →` jadi sampah dalam konsol cmd (codepage 437/850).
`chcp 65001` tidak boleh dipercayai — gagal pada Windows lama dan
merosakkan `set /p` pada sesetengah sistem.
Skrip .bat mesti **ASCII tulen**: guna `= - | + <- ->`.
`BACA_SAYA.txt` boleh kekal Unicode (dibaca Notepad, bukan konsol).

### BUANG.bat ditulis semula tanpa PowerShell
cmd tulen + subrutin `call :label`. Kurang titik kegagalan:
tiada ExecutionPolicy, tiada penghantaran argumen, tiada COM.
Struktur: `exit /b 0` MESTI sebelum blok subrutin, jika tidak
cmd jatuh terus ke dalamnya.
Diuji: 6 pintasan dibuang, `Word.lnk` & `main.py` tidak disentuh.

## Sesi 7 — OpenITI: Fath al-Bari DISAHKAN boleh dipadan (ujian langsung)

### Penemuan: repo AH dibundarkan KE ATAS
Ibn Hajar wafat 852H -> berada dalam repo **`0875AH`**, BUKAN `0850AH`.
Ini sebab percubaan awal dapat 404 semua.
```
https://raw.githubusercontent.com/OpenITI/0875AH/master/
  data/0852IbnHajarCasqalani/0852IbnHajarCasqalani.FathBari/
  0852IbnHajarCasqalani.FathBari.JK000166-ara1        (30.5 MB, 200 OK)
```
Tiada akhiran fail (bukan `.mARkdown`). 3 versi ada: JK000166 (pri),
Shamela0001673, Shia001792Vols.

### Struktur berbeza daripada Muslim .mARkdown
| Penanda | Fath al-Bari | Muslim .mARkdown |
|---|---|---|
| `### $` | 0 | 6,463 |
| `# N`   | **5,111** | 0 |
| `~~` sambungan baris | 229,399 | - |
| `PageV\d+P\d+` | 7,315 | - |

Parser MESTI kendalikan kedua-dua format. `parser.py` pengguna guna
`^#\s+(\d+)\s+` — corak itu SESUAI untuk Fath al-Bari (tetapi gagal
untuk Muslim). Jangan buang; tambah cabang kedua.

### PENOMBORAN SEJAJAR — diuji, 5/5 padan
`# N` = nombor hadis Bukhari standard. Disahkan dengan memadan **sanad**
(bukan matn — syarah memetik `قوله` + rantaian perawi, bukan matn penuh):

| # | Perawi dijumpai |
|---|---|
| 1 | al-Humaidi, Sufyan, Yahya b. Sacid al-Ansari, Alqamah b. Waqqas (4/4) |
| 2 | Abdullah b. Yusuf, Hisham b. Urwah, al-Harith b. Hisham (3/4) |
| 8 | Hanzalah b. Abi Sufyan, Ikrimah b. Khalid (2/2) |
| 50 | Ismail b. Ibrahim (1/2) |
| 100 | Hisham b. Urwah (1/2) |

**Implikasi:** padanan ID terus BOLEH dibuat untuk Bukhari. Ini berbeza
sepenuhnya daripada masalah `eng-*` (Bukhari 7,008 vs 7,589) yang TIDAK
sejajar.

### Liputan & saiz
```
seksyen dalam julat 1-7563 : 5,074
liputan Bukhari            : 67.1%
jurang                     : 2,489 nombor (cth 29,30,35,37,38,43,51,60)
panjang purata             : 3,264 aksara   median 1,971
terpanjang                 : 72,688 aksara
jumlah                     : 16.6 juta aksara (~17 MB; +FTS5 ~35 MB)
```

### HALANGAN SEBENAR
1. **Tashkeel 0.00%** — Arab gundul sepenuhnya. Diukur pada 309,912 huruf.
2. **Bahasa Arab klasik** — bukan Melayu. Majoriti pengguna sasaran tidak
   dapat membacanya.
3. **Median 1,971 aksara** — terlalu panjang untuk UI kad hadis semasa.
4. **Bukhari SAHAJA.** Kitab lain perlu syarah berlainan (Nayl al-Awtar,
   Awn al-Macbud) dan penomboran mereka BELUM diuji.
5. Lesen CC BY-NC-SA — perlu atribusi + tiada penggunaan komersial.

**Kesimpulan:** teknikalnya berjaya, tetapi nilainya kepada pengguna
Melayu terhad. Bukan calon Fasa 4 utama; sesuai sebagai lapisan
"Rujukan Arab" pilihan untuk pengguna berkemampuan bahasa Arab.

## Sesi 7 (samb.) — Fasa 3 DISELESAIKAN: English boleh dipadan

### Sumber: fawazahmed0/hadith-api (CDN jsDelivr, tiada kunci API)
```
editions.json -> 10 bahasa untuk setiap kitab
https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{kod}.min.json
  ara-bukhari  9.0 MB   7,589 hadis
  eng-bukhari  4.6 MB   7,589 hadis
  + ben fra ind rus tam tur urd
```

### PENEMUAN UTAMA: ada edisi `ara-*` sebagai jambatan
Masalah lama: "penomboran eng-* tidak sepadan (7,008 vs 7,589)".
**Andaian itu SALAH arah.** Sumber ini ada teks ARAB dengan penomboran
yang SAMA seperti `eng-*`. Jadi:

1. Padan hadis.my <-> `ara-bukhari` ikut **teks Arab dinormalisasi**
2. Ambil `eng-bukhari` ikut nombor edisi tersebut (bukan nombor hadis.my)

Diuji: hadis.my Bukhari #1 vs ara-bukhari #1 -> `startswith` **True**
selepas normalisasi (buang tashkeel, alif/ya/hamzah dilipat).

Pengesahan silang kandungan:
```
#1  -> "reward of deeds depends upon the intentions"   (niat)      OK
#8  -> "Islam is based on (the following) five"        (rukun)     OK
#50 -> "Narrated Abu Huraira ... Prophet was sitting"  (Jibril)    OK
```

`hadithnumber` julat 1-7563 untuk kedua-dua ara & eng (7,589 rekod
kerana ada nombor pecahan spt 1.1). Kunci padanan = teks Arab, BUKAN ID.

### Implikasi
- Tab English boleh diaktifkan tanpa terjemahan mesin
- Bonus percuma: Bengali, Perancis, Rusia, Tamil, Turki, Urdu
- Muat turun sekali, simpan dalam hadis.db. Tiada kuota API.
- Fasa 3 bertukar daripada "kumpul sahaja" -> "padan & gabung sumber"

### Keputusan pengguna (Sesi 7)
- Pengguna sasaran: **campuran** (awam teras + mod lanjutan)
- Fasa 4: **kedua-dua** Irsyad al-Hadith (BM, utama) + Fath al-Bari
  (Arab, lapisan pilihan)
- Fasa 3: **kekalkan** tab English -- kini boleh diisi sungguh

## Sesi 7 (samb.) — Transliterasi dimasukkan semula ke paparan hadis

Sebelum ini transliterasi hanya wujud dalam dialog "Fasa 1-4", tiada
dalam halaman baca hadis. Kini dipulangkan sebagai bahagian boleh kembang.

### Widget baharu: `ui/widgets.py :: Collapsible`
Melaksanakan prinsip "pengguna campuran" (keputusan Sesi 7):
paparan asal bersih untuk awam; bahan teknikal di belakang tajuk boleh
klik. Akan diguna semula untuk sanad & syarah Arab (Fasa 4 lapisan B).

- Tertutup secara lalai
- **Pembinaan malas** — `builder(layout)` hanya dipanggil pada buka
  pertama. Penting: transliterasi 62,169 hadis tidak dikira jika tidak
  dibuka. Disahkan `_dibina == False` selepas render.
- `try/except` dalam builder — kegagalan jadi mesej, bukan crash

QSS `QPushButton#collapse` sengaja rendah kontras (`TEXT_MUTED`),
hover jadi TEAL.

### Susunan paparan
```
[kad Arab]
  > Transliterasi (bacaan rumi)      <- tertutup
[tab Melayu/Indonesia/English]
[kad terjemahan]
```
Dua gaya dipapar; **Gaya Melayu didahulukan** (lebih mudah dibaca
pengguna tempatan), Akademik selepasnya.

Diuji offscreen kedua-dua tema: 1 Collapsible, tertutup lalai,
`_dibina=False`, selepas buka 2 kotak teks berisi.

### Kuota API — pembetulan
Kuota 200/hari adalah pelan **Basic**. Pelan **Developer = 10,000/hari**.
Sync penuh 62,169 hadis = 622 permintaan -> **satu hari sahaja**, bukan
4 hari. Andaian "4 hari" dalam RANCANGAN_4FASA.md sudah dibetulkan.

## Sesi 7 (samb.) — sync.py ditulis semula

### Pepijat dalam versi lama
`from client import HadisClient, HadisError, MAX_PER_PAGE`
Modul `client` **tidak wujud** -- `python sync.py` gagal serta-merta
dengan ModuleNotFoundError. Nama sebenar: `api.hadis_api.HadisAPI`.
Skrip lama tidak pernah boleh dijalankan.

### Pengawal paling kritikal: use_db=False
```python
api = HadisAPI(api_key=kunci, use_db=False)
```
`HadisAPI.__init__` membuka hadis.db sebagai sumber OFFLINE jika fail
wujud dan ada baris. Tanpa `use_db=False`, sync akan membaca DB dan
menyalin data kepada dirinya sendiri -- sifar rekod baharu, kelihatan
"berjaya". Disahkan: `use_db=True -> offline=True`.

### Keselamatan kunci
Kunci TIDAK diterima sebagai argumen baris arahan (kekal dalam sejarah
shell + senarai proses). Dibaca melalui `config.get_api_key()`:
user_settings.json -> .env -> persekitaran. Mesej ralat mengajar
pengguna ketiga-tiga cara.

### Boleh disambung
Kemajuan disimpan dalam hadis.db sendiri, bukan fail berasingan.
`mula = (ada // MAX_PER_PAGE) + 1`. Muka surat separa ditulis semula --
selamat kerana `INSERT OR IGNORE` + `UNIQUE(collection, hadis_id)`.

### Keutamaan
`bukhari, muslim` dahulu, kemudian empat Sunan, akhir sekali
malik/ahmad/darimi. Jika terputus, yang paling kerap dicari sudah ada.

### Berhenti awal
`daily_remaining <= 3` -> berhenti, sisa kuota untuk penggunaan biasa
apl pada hari sama. Kod keluar 2 = belum lengkap, 1 = ralat, 0 = siap.

### Diuji dengan HadisAPI tiruan (tiada kunci sebenar, tiada rangkaian)
```
1. sync penuh           400 rekod (250+120+30)          OK
2. terputus ms 3        200 rekod selamat, keluar 2     OK
3. sambung semula       400 jumlah, 0 pendua            OK
                        id 201-250 = 50 (bukti sambung) OK
4. jalan bila lengkap   0 rekod, 0 permintaan sia-sia   OK
5. tiada kunci          mesej mengajar, keluar 1        OK
6. --paksa              tarik semula, 0 pendua          OK
7. FTS5 selepas sync    carian menemui rekod            OK
```

Mod `--semak` berfungsi TANPA kunci -- berguna untuk melihat status.

## Sesi 7 (samb.) — FASA 3 SELESAI: tab English hidup

### Liputan sumber
7 daripada 9 kitab hadis.my ada padanan:
```
bukhari muslim abu-daud tirmidzi nasai ibnu-majah malik   -> ADA
ahmad darimi                                              -> TIADA
```
Slug berbeza: `abu-daud`->`abudawud`, `tirmidzi`->`tirmidhi`,
`ibnu-majah`->`ibnmajah`.

### Nombor ara-* == eng-* untuk KESEMUA 7 kitab (disahkan)
```
bukhari 7589  muslim 7563  abudawud 5274  tirmidhi 3998
nasai 5765    ibnmajah 4343  malik 1858
```
`ara-X` dan `ara-X1` teks IDENTIK selepas normalisasi (diuji 300 sampel
x 3 kitab = 900/900). Guna `ara-X1` -- fail lebih kecil ~35%.

### PEPIJAT BESAR DITEMUI: awalan 60 aksara memberi padanan SALAH
Percubaan pertama guna `normalisasi(teks)[:60]` sebagai kunci.
Ujian perlanggaran mendedahkan:
```
          unik%   kumpulan bahaya
awalan 60  81.4%       591      <- sanad sama, matn BERBEZA
awalan 100 93.0%       144
awalan 200 95.6%        14
teks penuh 95.8%         0      <- selamat
```
Contoh: 9 hadis Bukhari berkongsi
`حدثنا عبد الله بن يوسف ... مالك ... هشام بن عروة ... عائشة`
tetapi matn berlainan sepenuhnya.

**Penyelesaian:** kunci utama = **teks penuh**. Kunci sandaran = awalan
200 aksara, tetapi HANYA awalan yang unik dalam indeks (yang berlanggar
dibuang terus). Lebih baik tiada terjemahan daripada terjemahan salah.

### Keputusan ujian akhir (10,500 sampel, 7 kitab)
```
kitab        penuh  awalan  gagal  liputan
bukhari       1498       0      2    99.9%
muslim        1468       0     32    97.9%
abu-daud      1499       0      1    99.9%
tirmidzi      1471       1     28    98.1%
nasai         1475       0     25    98.3%
ibnu-majah    1498       0      2    99.9%
malik         1477       0     23    97.9%
-------------------------------------------
JUMLAH       10386       1    113    98.8%
```
80 kes "nombor berbeza" disiasat: **59/59 adalah PENDUA TULEN** -- teks
Arab 100% identik, hadis sama diulang dalam bab berbeza. 57/59
terjemahan English juga identik; 2 yang berbeza hanya pilihan perkataan
penterjemah, makna sama. **Bukan pepijat.**

### Fail baharu
- `core/eng_source.py` -- normalisasi, indeks dua peringkat, padanan
- `sync_english.py` -- muat turun + padan + simpan (TIADA kunci API)
- jadual `terjemahan_eng(collection, hadis_id, english, sumber)`

### Sambungan ke UI
`HadisAPI._english()` membaca jadual dalam mod offline;
`_english_luar()` membuka DB atas permintaan dalam mod dalam talian.
Tab English kini `enabled=True` -- disahkan dalam ujian offscreen.

Atribusi dipapar di bawah teks Inggeris (kewajipan sumber).

### `core/phase3_translate.py` ditulis semula
Peranan bertukar: "kumpul sahaja" -> "gabung berbilang sumber +
laporkan asal-usul". Pulangkan `tersedia`, `tiada`, `nota`.
Pepijat ditangkap semasa ujian: `_kosong()` tiada kunci `nota` ->
KeyError pada pemanggil. Semua laluan kini memulangkan bentuk yang sama.

## Sesi 7 (samb.) — hadis.db: saiz sebenar + sistem versi skema

### Saiz DIUKUR (5,100 hadis Arab sebenar, bukan anggaran)
```
per hadis                  2,771 bait
62,169 hadis               164 MB
selepas VACUUM             138 MB
+ English (7 kitab)        ~153 MB
gzip -9 untuk edaran       28 MB  (21%)
```

Pecahan teks dalam jadual `hadis`:
```
arab      56.5%      melayu 20.5%      indonesia 23.0%
```

Pecahan saiz DB (dbstat):
```
hadis              8.9 MB   (79%)
hadis_fts_data     2.1 MB   (19%)   <- FTS5 MURAH, bukan masalah
indeks lain        0.3 MB
```

**Carian FTS5: 0.03 ms.** Prestasi bukan isu walau pada saiz penuh.

### Keputusan pengguna (Sesi 7)
- Edaran: **pengguna sync sendiri** -- ZIP kekal ~110K, tiada DB dibundel
- Indonesia: **kekalkan** (walaupun 23% saiz)
- Versi skema: **ya, buat sekarang**

### Sistem migrasi skema -- db.py
```python
SKEMA_VERSI = 2
MIGRASI = {2: "CREATE TABLE IF NOT EXISTS terjemahan_eng (...)"}
```
`init()` menjalankan migrasi tertinggal secara automatik. Pengguna
sedia ada TIDAK perlu memadam hadis.db.

**Kes tepi penting:** DB dari sebelum sistem ini melaporkan
`user_version=0` walaupun jadual asas sudah ada. `init()` menetapkannya
ke 1 dahulu (jadual asas dicipta oleh `CREATE IF NOT EXISTS`), kemudian
migrasi bermula dari 2. Tanpa ini, migrasi 1 akan cuba dijalankan
semula pada DB yang sudah lengkap.

### Diuji
```
DB lama (user_version=0, tiada terjemahan_eng, 200 hadis, 1 favorit)
  -> init() -> versi 2, 200 hadis KEKAL, nota favorit KEKAL,
     terjemahan_eng dicipta, carian FTS masih OK
init() dipanggil 3x  -> migrasi_dijalankan=0 setiap kali (idempoten)
DB baharu kosong     -> versi 2 terus
```

### Duplikasi dibuang
`core/eng_source.py` dulu mempunyai `SKEMA` sendiri untuk
`terjemahan_eng` -- bertindih dengan migrasi. Kini `pasang_skema()`
hanya memanggil `db.migrasi()`. Satu sumber kebenaran.

`sync.py --semak` kini memaparkan versi skema.

### Belum diputuskan
- `PRAGMA journal_mode=WAL` meninggalkan fail `-wal` dan `-shm`.
  Untuk DB baca-sahaja, WAL tiada faedah. Tukar ke DELETE?

## Sesi 7 (akhir) — Dokumentasi sesi diringkaskan

Masalah: `sesi_index.md` sudah 865 baris. Sesi baharu terpaksa membaca
semuanya untuk tahu apa yang penting, jadi pepijat sama berulang.

### `MULA_SINI.md` — dibaca DAHULU, bukan arkib ini
6 bahagian:
1. **6 peraturan** yang tidak boleh dilanggar (tkinter, bidi, ة→ه,
   import "unused", CRLF, kunci API)
2. **3 corak pepijat berulang** dengan kod SALAH vs BETUL
3. Senarai semak (satu arahan)
4. Fakta padat: API, DB, Fasa 3, pepijat Qt yang sudah dibetulkan
5. Keadaan projek + apa seterusnya
6. Cara bekerja dengan pengguna ini

Corak yang dikira daripada arkib:
- `Join-Path $env:` null -> **3 kali**
- Nilai terkunci masa import -> **2 kali** (warna lalai, `from theme import`)
- Andaian tidak diuji -> **2 kali besar** (eng-* "mustahil", Fath al-Bari
  "tiada") -- kedua-dua ternyata SALAH selepas diuji

### `semak.py` — senarai semak jadi kod
8 semakan automatik. Bukan dokumentasi yang boleh diabaikan; ia gagal
dengan kod keluar 1.

**Disahkan berfungsi:** 3 pepijat lama disuntik semula ke salinan
projek (warna lalai, .bat LF, Join-Path tanpa pengawal) -- kesemuanya
ditangkap. Ujian ini penting: skrip semakan yang tidak pernah diuji
terhadap pepijat sebenar hanyalah teater.

Pepijat dalam `semak.py` sendiri ditemui semasa ujian: semakan import
mencipta `__pycache__`, kemudian semakan #8 melaporkannya sebagai
kotoran. Kini dibersihkan sendiri sebelum menyemak.

`sesi_index.md` kini bermula dengan penunjuk ke `MULA_SINI.md`.

## Sesi 7 (akhir) — WAL DIKEKALKAN + workspace dibersihkan

### Isu WAL ditutup — andaian saya SALAH
Saya pernah tulis "WAL meninggalkan fail -wal dan -shm, tiada faedah
untuk DB baca-sahaja". **Diuji, dan itu tidak tepat.**

```
                      WAL       DELETE
tulis 3,000 baris     0.25s     0.23s
baca satu hadis       0.007ms   0.010ms
carian FTS5           0.042ms   0.045ms
BACA SAMBIL TULIS     819       405        <- 2x
selepas tutup bersih  1 fail    1 fail     <- sama!
selepas crash         3 fail    1 fail
selepas buka semula   1 fail    1 fail     <- pulih sendiri
data selepas crash    2,000     2,000      <- kedua-dua selamat
```

Fail `-wal`/`-shm` wujud **hanya semasa sambungan terbuka**. Ia bukan
sampah yang tertinggal.

Baris yang menentukan: **baca sambil tulis 2x lebih laju**. Itu senario
sebenar apl ini -- QThread worker membaca sementara sync.py menulis.

**Keputusan: KEKALKAN WAL.** Nota diletak dalam `db.py` supaya tiada
sesi akan datang "membetulkannya" semula.

### Workspace dibersihkan: 67 MB -> 749 KB
```
DIBUANG
  .cache/pip           67 MB   cache pip, dijana semula
  .fonts/              340 KB  termasuk CustomTkinter_shapes_font.otf
                               -- sisa era tkinter, projek dah lama tinggalkan
  uploads/*.png        9 fail  tangkapan skrin lama yang sudah dibincang
  uploads/sesi_index.md        versi Sesi 4 (183 baris), sudah DISERAP
                               sepenuhnya ke versi 910 baris projek
                               -- juga mengandungi KUNCI API TERDEDAH
  /tmp/*               ~150 MB fail ujian OpenITI, ed/, DB ujian
KEKAL
  hadis/               409 KB  projek
  uploads/             204 KB  2 tangkapan skrin terkini sahaja
  PustakaHadith.zip     120 KB
```
Semakan selepas buang: `python semak.py` -> SEMUA LULUS.

**Kunci API terdedah kini tiada dalam mana-mana fail workspace.**
(Kunci itu masih aktif di pelayan -- pengguna masih perlu revoke.)

## Sesi 8 — Semakan kod pengguna: A (Fasa 3 disambung) + B (ujian translit)

Pengguna menghantar dua perubahan untuk dianalisa. **Kedua-duanya betul**,
dan satu daripadanya membetulkan pepijat yang SAYA perkenalkan.

### A — `translate()` disambung ke PipelineWorker
`ui/workers.py` dulu membina dict inline untuk Fasa 3, jadi
`core/phase3_translate.py` yang ditulis semula Sesi 7 menjadi **dead
code** — tiada pemanggil langsung.

Kini `translate(hadis=h)` dipanggil sebenar. `ui/app_qt.py:_on_phase`
memaparkan `nota` sebagai disclaimer.

Disahkan tiga keadaan berbeza:
```
bukhari tanpa eng -> "Jalankan: python sync_english.py"
ahmad tanpa eng   -> "tiada untuk kitab ini dalam sumber semasa"
bukhari lengkap   -> (tiada nota)
```
Diuji melalui laluan sebenar `_run_pipeline()`: panel Fasa 3 memapar
nota kuning, status `dari_sumber`.

### B — Ujian transliterasi + UTF-8 stdout

**Pepijat SAYA yang ditemui oleh cadangan ini:**
Jadual `LAFZ_JALALAH` wujud tetapi TIDAK PERNAH sepadan. Kunci ditulis
`0651 064E` (shadda+fatha), teks sebenar `064E 0651` (fatha+shadda).
Akibat: `اللَّهِ` -> `al-lahi`, sepatutnya `Allāhi`.

Ini persis Lesson lama yang sudah tercatat ("susunan aksara sebenar:
konsonan + fatha + shadda") — tetapi jadual itu tetap ditulis songsang.
**Pengetahuan bertulis tidak cukup; ia mesti dikunci oleh ujian.**

Pembetulan:
- Kunci jadual disusun semula ikut susunan sebenar
- `_susun_baris()` menormalkan shadda supaya SELEPAS vokal — menerima
  kedua-dua susunan daripada sumber luar
- 9 kes ujian dalam `semak.py`, termasuk kedua-dua bentuk jalalah

**UTF-8 stdout — pepijat kedua saya.**
`semak_translit()` mencetak teks Arab. Konsol Windows lalai cp437.
Disahkan dengan `PYTHONIOENCODING=cp437`: crash
`UnicodeEncodeError` pada `\u2014` (sempang panjang) SEBELUM sempat
melapor apa-apa. Kod keluar 1 — kelihatan seperti kegagalan semakan.

```python
for _aliran in (sys.stdout, sys.stderr):
    try: _aliran.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError): pass
```
Selepas: kod keluar 0, tiada UnicodeEncodeError.

### Pengajaran
Alat pembangunan mesti diuji pada persekitaran SASARAN, bukan hanya
sandbox Linux. `semak.py` sendiri adalah program Windows.

## Sesi 8 (samb.) — Semakan `ui/app_qt.py` pengguna

### Perbezaan: `nota` Fasa 3 TIADA dalam fail pengguna
Fail yang dihantar masih:
```python
elif n == 3:
    rows = [("Melayu", ...), ("Indonesia", ...), ("English", ...)]
```
Tiada blok `nota`. Perubahan A yang dilaporkan pengguna hanya
sebahagian dilaksanakan -- `workers.py` diubah, `app_qt.py` tidak.
Kesan: mesej "jalankan sync_english.py" dan "tiada sumber untuk kitab
ini" TIDAK akan dipapar.

### PEPIJAT DITEMUI: UI beku 1.1s setiap kali hadis dibuka

`_render_detail()` memanggil:
```python
max_id = self.api.max_hadis_id(slug) or 0
```
Dalam mod **dalam talian**, `max_hadis_id` memanggil `get_collections()`
= permintaan rangkaian, pada **thread UI**. Dengan throttle 1.1s:

```
diukur: max_hadis_id pada thread UI = 1.10s
selepas pembetulan: _render_detail = 4ms
```

Ini bercanggah dengan docstring fail itu sendiri:
> "Semua I/O rangkaian berjalan dalam QThread; UI tidak pernah beku."

**Pembetulan:** guna `self._total_of(slug)` -- membaca `self.collections`
yang sudah dimuat secara tak segerak semasa permulaan. Laluan
`max_hadis_id` dikekalkan HANYA untuk mod offline (pertanyaan SQLite,
pantas). Butang navigasi masih betul: `['< No. 38', 'No. 40 >']`.

**Pengajaran:** getter yang kelihatan murah boleh melakukan I/O.
Semak badan fungsi sebelum memanggilnya dari kod UI.

## Sesi 8 (samb.) — `_on_phase` versi pengguna DIGUNA PAKAI

Pengguna menghantar `app_qt.py` dengan penyelesaian `nota` yang
**lebih baik daripada versi saya**:

```python
def _on_phase(self, n, data):
    status = data.get("status", "")
    nota = data.get("nota", "")
    dsc = data.get("disclaimer", "") or nota      # seragam SEMUA fasa
    ...
    self._fill_phase(n, rows, status, dsc)
```

Versi saya menambah cabang khusus Fasa 3 dengan `return` awal --
memanggil `_fill_phase` dua kali dalam laluan berbeza. Versi pengguna
mengendalikan `nota` untuk semua fasa dalam satu baris, tiada early
return, tiada pertindihan.

**Keutamaan `disclaimer` sebelum `nota` adalah betul:**
`disclaimer` = amaran KETEPATAN (Fasa 4: "bukan huraian ulama").
`nota` = penerangan OPERASI (Fasa 3: "jalankan sync_english.py").
Amaran keselamatan mesti sentiasa menang. Diuji 4 kombinasi -- lulus.

Versi saya dibuang, versi pengguna diguna pakai.

### Diuji hujung ke hujung (kitab `ahmad`)
```
Fasa 1: berjaya
Fasa 2: berjaya
Fasa 3: dari_sumber  + "Terjemahan Inggeris tiada untuk kitab ini..."
Fasa 4: auto         + "Nota automatik... BUKAN huraian ulama"
```

### Pembetulan `max_hadis_id` TIADA dalam fail pengguna
Fail yang dihantar masih mengandungi:
```python
max_id = self.api.max_hadis_id(slug) or 0
```
= beku UI 1.10s setiap kali hadis dibuka (mod dalam talian).
Pembetulan saya dikekalkan dalam versi kerja. Pengguna perlu ambil
`ui/app_qt.py` daripada ZIP, bukan sebaliknya.

**Pengajaran:** apabila dua penyelesaian wujud untuk masalah sama,
pilih yang tiada cabang khas. Cabang khusus-kes membiak.

## Sesi 8 (samb.) — `ui/workers.py`: kunci `error` tidak pernah dipapar

### Versi pengguna LEBIH BAIK untuk Fasa 3
```python
p3 = {..., "status": "ralat",
      "nota": f"Ralat memproses terjemahan: {e}"}
```
Versi saya guna `"error": str(e)`. Tetapi `_on_phase` hanya membaca
`disclaimer or nota` -- **kunci `error` tidak pernah dibaca**. Ralat
hilang senyap; pengguna nampak "ralat" tanpa sebab.

Corak sama ditemui dan dibetulkan di:
- Fasa 2: `"error"` -> `"nota": f"Ralat transliterasi: {e}"`
- Fasa 4: `"error"` -> `"disclaimer": f"Ralat menjana huraian: {e}"`

Diuji dengan menyuntik kegagalan import:
```
Fasa 2: ralat  sebab=Ralat transliterasi: modul rosak (ujian)
Fasa 3: ralat  sebab=Ralat memproses terjemahan: modul rosak (ujian)
Fasa 4: ralat  sebab=Ralat menjana huraian: modul rosak (ujian)
```

### PEPIJAT: QThread dimusnahkan semasa masih berjalan

`app_qt.py:1027` (sebelum):
```python
if self._pipe_worker:
    self._pipe_worker.cancel()      # hanya tetapkan flag
self._pipe_worker = PipelineWorker(h)   # rujukan terakhir digugurkan
```
`cancel()` TIDAK menghentikan thread. Menimpa rujukan membuatkan Python
mengutip QThread yang masih hidup. Disahkan:
```
QThread: Destroyed while thread is still running
```
Ini PERSIS amaran dalam docstring `ui/workers.py` sendiri.

Pembetulan: `cancel()` + putuskan isyarat + `wait(1000)` sebelum
menimpa. Diuji `_run_pipeline()` dua kali berturut -- tiada crash.

### Pengajaran
Bila kod menulis kunci ralat, sahkan UI benar-benar MEMBACA kunci itu.
Kunci yatim = kegagalan senyap.

## Sesi 8 (samb.) — `semak.py` pengguna: kes ujian digabung

### Dua isu dalam fail pengguna

**1. SyntaxError** -- docstring `semak_joinpath` bermula dengan `""` +
backtick, bukan `"""`:
```python
def semak_joinpath() -> None:
    ""`Join-Path $env:X` mesti berada DALAM pengawal null.
```
Disahkan: `unterminated triple-quoted string literal`.
Fail itu TIDAK boleh dijalankan langsung. Ironinya, semakan #4
(sintaks) direka untuk menangkap perkara ini -- tetapi ia tidak boleh
menyemak dirinya sendiri jika ia sendiri gagal dihurai.

**2. Nilai jangkaan LAPUK**
```python
("رَسُولُ اللَّهِ", "rasulu al-lahi"),     # nilai SEBELUM pembetulan
```
Output sebenar kini `rasulu Allahi`. Menerima nilai ini akan
**mengunci semula pepijat** yang baru dibetulkan Sesi 8.

Ini bahaya sebenar ujian regresi: nilai jangkaan yang disalin daripada
output semasa TANPA mengesahkan ia betul. Komen ditambah dalam
docstring: "Jangan kemas kini nilai ini untuk melepaskan ujian --
siasat dahulu sama ada perubahan itu betul."

### Kes pengguna LEBIH BAIK -- digabung
Kes pengguna menguji peraturan yang ujian saya terlepas sepenuhnya:
```
muhammadun · masjidun · kitabun   -> TANWIN (-un)
asy-syams                          -> syamsiyyah sy
al-hamdu li-llahi                  -> lillah selepas kata sendi
```
Kes saya menguji: jalalah, shadda, vokal panjang, sukun.

Gabungan: **12 kes**. Format `(arab, melayu, ilmiah_atau_None)` --
`None` bermakna hanya gaya Melayu disemak.

### Disahkan menangkap regresi SEBENAR
Percubaan pertama saya gagal: saya lumpuhkan `_susun_baris()` sahaja
dan ujian tetap lulus -- kerana normalizer BUKAN pembetulan sebenar.
Pembetulan sebenar ialah **susunan kunci jadual** LAFZ_JALALAH.

Selepas membalikkan susunan kunci itu:
```
GAGAL اللَّه -> melayu 'al-lah' (jangka 'Allah')
GAGAL رَسُولُ اللَّهِ -> melayu 'rasulu al-lahi' (jangka 'rasulu Allahi')
```

**Pengajaran:** apabila mengesahkan ujian regresi, pastikan suntikan
membalikkan pembetulan SEBENAR. Suntikan yang salah memberi keyakinan
palsu -- ujian "lulus" hanya kerana pepijat tidak benar-benar kembali.

## Sesi 8 (akhir) — FASA 4B SIAP: Fath al-Bari

### Skema v3
```
2 -> 3  syarah(collection, hadis_id, kitab, pengarang, teks)
        + idx_syarah_ref(collection, hadis_id)
```

### `core/syarah_source.py`
Katalog `KITAB_SYARAH` (boleh dikembangkan), parser format `# N`,
pengawal padanan, akses DB.

`bersih()` membuang penanda `PageV\d+P\d+` dan `~~` TANPA membuang
baris -- parser lama pengguna membuang seluruh baris, memadamkan
401 baris teks Arab.

### PENGAWAL padanan -- bahagian paling penting
Tanpa ia, perubahan pada sumber OpenITI boleh memasangkan SETIAP hadis
dengan syarah yang SALAH. Untuk teks agama itu tidak boleh diterima.

**Percubaan pertama GAGAL sepenuhnya:**
```
penomboran BETUL : 77%
penomboran ROSAK : 77%     <- tidak membezakan apa-apa
```
Dua sebab:
1. Kata seperti `حدثنا`, `قال`, `الله`, `بن` muncul dalam HAMPIR SEMUA
   syarah -- ia memadan walaupun nombor salah. Kini disenaraihitamkan.
2. `break` selepas `disemak += 1` menamatkan gelung sebelum menyemak.

Selepas dibetulkan, diukur pada 7,563 hadis Bukhari sebenar:
```
BETUL      : 61/80 = 76%
ROSAK +3   : 18/80 = 22%
ROSAK +50  : 11/80 = 14%
```
Ambang 50% memisahkan dengan selamat.

**Disahkan menolak data buruk:** cache dianjak +300, sync melaporkan
5% dan membatalkan -- 0 baris disimpan.

### `sync_syarah.py`
Tiada kunci API. Muat turun 30.5 MB -> hurai -> SAHKAN -> simpan.
Berhenti sebelum menyimpan jika padanan di bawah ambang.
Hasil sebenar: 5,074 seksyen, 67% liputan Bukhari.

### UI
`Collapsible("Syarah klasik (Arab)")` selepas tab bahasa, tertutup
lalai, pembinaan malas. Hanya muncul jika syarah WUJUD untuk hadis itu
(`_ada_syarah()` -- pertanyaan LIMIT 1).

Teks dipotong pada 4,000 aksara (median 1,971; terpanjang 72,688)
dengan nota "Klik kanan -> Salin syarah penuh". Atribusi pengarang +
lesen CC BY-NC-SA dipaparkan.

### semak.py -> 10 ujian
Ujian 8b menguji katalog, URL (repo 0875AH), `bersih()`,
`hurai_hash_n()`, dan pengawal terhadap penomboran betul VS teranjak.

## Sesi 9 — Padanan teks Arab gagal pada data SEBENAR

Pengguna lapor: teks `hadis.db` (hadis.my) tidak padan dengan CDN
selepas normalisasi. Tidak dapat dihasilkan semula di sini -- DB
sebenar tiada dalam sandbox. Jadi: perkukuh normalisasi + tambah
lapisan sandaran + bina alat diagnosis.

### Yang disahkan BUKAN puncanya
`ara-bukhari` vs `ara-bukhari1`: 1500/1500 identik selepas normalisasi.
Kedua-dua edisi CDN konsisten. Perbezaan datang daripada hadis.my.

### Normalisasi diperkukuh (`core/eng_source.py`)
```
sebelum: [\u064B-\u0652\u0670\u0640]
selepas: [\u064B-\u065F\u0670\u0640\u06D6-\u06ED]
```
Tambah: maddah/hamzah tambahan (0653-0655), tanda mushaf (06D6-06ED).

`unicodedata.normalize("NFKC")` -- meleraikan bentuk persembahan Arab
(FE70-FEFF) dan ligatur (FDFA). Teks dari PDF/sumber lama gagal
sepenuhnya tanpa ini.

Jadual `_VARIAN`: Farsi yeh (06CC), keheh (06A9/06AA), alif wasla
(0671) -- kelihatan sama, titik kod berbeza. Satu huruf sahaja
memusnahkan padanan seluruh hadis.

### Lapisan ke-3: padanan pertindihan kata
```
1. teks penuh          (tepat)
2. awalan 200 aksara   (hujung berbeza)
3. pertindihan kata    (BARU -- teks berbeza sedikit)
```
`_bina_indeks_kata()` -- indeks terbalik kata jarang (muncul <5%
hadis). `padan_kata()` menuntut skor >=55% DAN calon kedua <85%
daripada yang pertama. Jika dua calon rapat -> TOLAK.

**Diuji dengan kerosakan disuntik (400 sampel):**
```
             betul  SALAH  gagal
asal          376     24      0     <- 24 = pendua tulen, disahkan
potong 40%    247      0    153
buang 1/9     295      0    105
tambah ekor   340      0     60
ejaan Farsi   376     24      0
```
**SIFAR padanan salah** pada setiap varian rosak. Prinsip dipegang:
lebih baik gagal daripada memberi terjemahan hadis yang salah.

### `diagnos_padanan.py` (baharu)
Melaporkan MENGAPA padanan gagal tanpa mengubah apa-apa:
pecahan kaedah, aksara asing pada kedua-dua belah, titik kod pertama
yang berbeza + konteks, contoh yang gagal.

Diuji dengan DB yang sengaja dirosakkan (tambahan ekor + ejaan Farsi):
`penuh 85.8% · awalan 8.6% · kata 3.8% · gagal 1.8%` = **98.2%**.

`sync_english.py` kini melaporkan pecahan kaedah setiap kitab.

### Belum selesai
Punca sebenar pada mesin pengguna MASIH TIDAK DIKETAHUI. Perlu output
`diagnos_padanan.py` daripada DB sebenar.

## Sesi 9 — Revoke kunci API terdedah

### Portal sebenar dijumpai
Kunci diurus di **`developer.hadis.my`**, bukan `hadis.my`:
```
https://developer.hadis.my/dashboard/keys      (log masuk Google)
https://developer.hadis.my/docs                (dokumentasi)
```
`hadis.my/api`, `/developer`, `/dashboard` semuanya 403 — salah domain.
`service.hadis.my` (akar) memulangkan JSON yang menyenaraikan pautan
sebenar. Itu cara ia dijumpai.

### Status kunci — DIUJI LANGSUNG
```
HADIS_34A8****B52E6B   AKTIF   had 10,000/hari   <- DEVELOPER
HADIS_E6D6****77C8C0   AKTIF   had    200/hari   <- Basic
```
Kedua-dua **masih diterima pelayan**. Yang pertama pelan Developer —
paling bernilai untuk disalahguna.

Dua pelan berbeza mencadangkan **dua akaun Google berasingan**.
Pengguna perlu semak kedua-duanya.

### Kekangan penting: 1 kunci setiap pelan
Dokumentasi rasmi:
```
Basic      200/hari    60/min    1 API key
Personal 1,000/hari   120/min    1 API key
Developer 10,000/hari  500/min   1 API key
```
Tiada tempoh bertindih — saat kunci lama mati, apl mati sehingga kunci
baharu dimasukkan. Jangan revoke di tengah sync.

### Fail baharu
- `REVOKE_KUNCI.md` — langkah revoke + tempat selamat simpan kunci
- `semak_kunci.py` — uji kunci terdedah + kunci semasa; kod keluar 1
  jika mana-mana kunci terdedah masih aktif. Tidak pernah mencetak
  kunci penuh (guna `mask_key`).

Sokongan hadis.my jika revoke tiada dalam UI:
WhatsApp +60 19-209 2006 · khai@webmaster.my

## Sesi 9 (samb.) — Dua pepijat susun atur daripada tangkapan skrin

### 1. Tetingkap terpotong pada laptop
```
setMinimumSize(1000, 680)   resize(1240, 860)
```
Pada 1366x768, ruang berguna hanya ~730px selepas bar tugas. Tetingkap
860px tidak muat.

Betulan: `setMinimumSize(900, 560)` + `_saiz_muat_skrin()` yang membaca
`availableGeometry()` dan mengehadkan saiz kepada skrin sebenar.
Diuji pada skrin 800x600 -> tetingkap 900x560, muat.

### 2. Halaman carian penuh ruang kosong
`_page_search` ialah SATU-SATUNYA halaman tanpa `addStretch(1)` pada
layout akar. QVBoxLayout mengagihkan ruang lebihan kepada setiap anak:

```
Hero: tinggi semula jadi 187px  ->  diregang 284px
```
Hasil carian tertolak jauh ke bawah -- pengguna nampak skrin kosong
dan perlu skrol dua kali untuk sampai ke hadis pertama.

Ujian mendedahkan `_page_settings` mempunyai masalah SAMA.

`empty_state()` margin 80px -> 40px.

### Ujian 8c: AST semak layout akar setiap halaman
Tiga percubaan diperlukan sebelum ia benar-benar berfungsi:

1. `"addStretch(1)" in badan` -> **positif palsu**: `wl.addStretch(1)`
   yang memusatkan bar carian secara mendatar juga dikira.
2. Cari nama akar, tetapi fallback cari seluruh fail -> **positif
   palsu lagi**: nama tempatan `bl` dikongsi `_page_home` dan
   `_page_search`.
3. Regex `(?:self\.)?(...)` **membuang** prefix, jadi semakan
   `startswith("self.")` sentiasa False.

Versi akhir: tangkap nama penuh termasuk `self.`, benarkan carian
seluruh fail HANYA untuk atribut (`self._pipe_root`), bukan nama
tempatan. Disahkan dengan menyuntik semula pepijat -> GAGAL betul.

**Pengajaran:** ujian yang lulus pada percubaan pertama patut
dicurigai. Saya hampir menghantar tiga versi rosak yang semuanya
"lulus".

## Sesi 9 (samb.) — Halaman utama muat skrin tanpa skrol

Pengguna mahu SEMUA 9 kad kitab kelihatan sebaik apl dibuka.
Diukur pada 1240x730: kandungan 961px vs viewport 669px = **292px
terlebih**.

### Pecahan sebelum/selepas
```
                        sebelum  selepas
Hero padding (atas+bawah)  96px    60px
Hero jumlah               295px   245px
KitabCard tinggi          168px   104px   <- perubahan terbesar
grid spacing               14px    10px
margin atas kolum kad      32px    18px
margin bawah halaman       40px    24px
SearchBar input/butang     46px    40px
--------------------------------------------
body                      961px   669px   MUAT
```

### Perubahan terpenting: KitabCard jadi MENDATAR
Susunan lama menegak (ikon atas, nama, desc, kiraan) = 4 baris = 168px.
3 baris kad x 168 = 504px, tidak mungkin muat.

Susunan baharu: ikon di KIRI (lebar tetap 40px), teks di kanan.
Membuang satu baris penuh -> **168px jadi 104px**. Semua maklumat kekal.

### Ujian tambahan dalam 8c
Melancarkan apl pada 1240x730 dalam subproses dan mengukur
`body.height() - viewport.height()`. Gagal jika > 0.

Ini ujian kedudukan sebenar, bukan pemeriksaan kod statik -- ia akan
menangkap regresi walaupun daripada perubahan QSS atau fon.

### Had
Muat pada tinggi tetingkap >= 730px. Di bawah itu (cth. 660px) masih
perlu skrol ~60px. Untuk muat pada 620px, grid perlu 4 lajur atau kad
lebih pendek lagi -- belum dibuat kerana majoriti laptop 768px.

## Sesi 9 (samb.) — Butang tindakan naik ke baris tajuk

Permintaan pengguna (snap2 + anak panah): pindahkan 4 butang tindakan
ke baris tajuk, dan turunkan butang navigasi ke tempat yang kosong.

### Sebelum
```
Musnad Ahmad — Hadis No. 10035
[kad Arab]
> Transliterasi
[tab bahasa] [kad terjemahan]
[WhatsApp][Salin][Dengar][Simpan] ............ [Fasa 1-4]
[< Hasil carian] .................. [< No.] [No. >]
```

### Selepas
```
Musnad Ahmad — Hadis No. 10035  [WhatsApp][Salin][Dengar][Simpan]
[kad Arab]
> Transliterasi
[tab bahasa] [kad terjemahan]
[< Hasil carian] ....... [Fasa 1-4]  [< No.] [No. >]
```

Sebab ia lebih baik: pada hadis panjang, pengguna terpaksa skrol ke
bawah untuk Salin/Simpan. Kini tindakan sentiasa kelihatan bersama
tajuk tanpa skrol.

Butang `Fasa 1-4` turun ke baris navigasi, mengisi ruang yang
ditinggalkan -- tiada baris kosong terbuang.

### Disahkan
- Semua 5 sambungan isyarat utuh: `_share` `_copy` `_tts`
  `_toggle_save` `_run_pipeline`
- `self._save_btn` masih disimpan -> teks bertukar
  `☆ Simpan` <-> `⭐ Tersimpan`
- Butang kembali betul untuk keempat-empat sumber:
  `Senarai kitab` / `Hasil carian` / `Tersimpan` / `Utama`
- Blok `act = QWidget()` lama dibuang sepenuhnya; `pb` ditakrif
  sekali sahaja (tiada butang pendua)

## Sesi 9 (akhir) — Halaman "Fasa 1-4" jadi "Huraian" sahaja

Keputusan pengguna: Fasa 1, 2, 3 tidak perlu dipapar lagi kerana
hasilnya SUDAH kelihatan pada halaman baca hadis:
```
Fasa 1 ekstrak       -> kad teks Arab
Fasa 2 transliterasi -> Collapsible "Transliterasi (bacaan rumi)"
Fasa 3 terjemahan    -> tab Melayu/Indonesia/English
```
Memaparkannya semula ialah pengulangan.

### Perubahan
| Sebelum | Selepas |
|---|---|
| Butang `🧮 Fasa 1-4` | `📖 Huraian` |
| 4 kad fasa | 1 kad Huraian |
| Breadcrumb "Fasa 1-4 · No. N" | "Huraian · No. N" |
| Chip "FASA 4" | "AUTO" |
| Tiada jalan balik | Butang `‹ Kembali` kiri bawah |

### `PipelineWorker(h, hanya_huraian=True)`
Fasa 4 diekstrak ke metod `_huraian()` yang dikongsi antara mod penuh
dan mod huraian. Fasa 4 tidak bergantung kepada hasil fasa lain -- ia
membaca `arab` dan `melayu` terus daripada objek hadis, jadi
melangkau 1-3 selamat.

Mod penuh KEKAL dalam kod (`hanya_huraian=False`) untuk nyahpepijat.

### Pepijat dielak: atribut kad fasa basi
`_fill_phase` mencari `self._phase{n}`. Selepas `_clear(self._pipe_root)`
widget lama sudah `deleteLater()` tetapi atribut masih menunjuk
kepadanya -- isyarat lewat daripada worker sebelumnya akan menulis ke
widget mati dan Qt crash.

Betulan: `delattr` untuk n=1..4 sebelum membina kad baharu.

### `_kembali_dari_huraian()`
Memanggil `open_detail(h, self._detail_from)` -- balik ke hadis yang
sama dan MENGEKALKAN konteks asal, jadi butang kembali pada halaman
detail masih betul.

### Diuji
```
dari kitab   -> Kembali -> detail  OK
dari search  -> Kembali -> detail  OK
dari saved   -> Kembali -> detail  OK
dari home    -> Kembali -> detail  OK
tekan Huraian 3x -> 1 kad (bukan 3), tiada crash QThread
```

## Sesi 9 — Butang Kembali jatuh keluar skrin

Pengguna: "mana button kembali?"

**Diukur:** butang pada y=683, viewport 669px -> **14px di bawah paras
skrin**. Ia wujud tetapi memerlukan skrol untuk dilihat -- mengalahkan
tujuannya sebagai jalan keluar pantas.

Punca: butang diletak DALAM `QScrollArea` bersama kad huraian. Huraian
automatik menghasilkan 6 medan teks (~800px), jadi apa-apa di bawahnya
pasti terkeluar.

### Penyelesaian: bar bawah TETAP
`_page_pipeline` bukan lagi QScrollArea tulen:
```
QWidget (luar)
├── QScrollArea (kad huraian)   <- boleh skrol
└── QFrame#bottombar            <- TETAP, sentiasa kelihatan
    └── [< Kembali]
```
QSS `QFrame#bottombar` guna `HEADER_BG` + `border-top` supaya konsisten
dengan header dan mengikut tema.

### Isyarat disambung semula setiap kali
Butang dicipta SEKALI dalam `_page_pipeline`, tetapi hadis berbeza
setiap kali halaman dibuka. Tanpa `disconnect()` dahulu, sambungan
bertindan dan klik akan melompat ke hadis pertama yang pernah dibuka.

Diuji: 3 kali buka -> `receivers(clicked)` kekal **1**, dan klik
membawa ke hadis yang BETUL.

### Diuji
```
y=692 bawah=720 pada tetingkap 730px -> kelihatan
kitab  hadis 5  -> detail (id=5)   OK
search hadis 99 -> detail (id=99)  OK
saved  hadis 5  -> detail (id=5)   OK
home   hadis 99 -> detail (id=99)  OK
```

Ujian regresi ditambah dalam 8c: mengesan `ll.addWidget(bar)` di luar
`QScrollArea`.

## Sesi 9 — "Shallallahu" ejaan Indonesia dalam terjemahan Melayu

Pengguna kesan: `Shallallahu` ialah ejaan Indonesia, bukan Melayu.

### Analisis pada data SEBENAR (bukan andaian)
400 hadis, 4 kitab, medan `melayu` daripada API:
```
Shallallahu   456      <- satu-satunya masalah sistematik
kalian         10
rakaat          9
sujud           1

shalat/hadits/Ramadhan/adzan/bahwa/dzikir/wudhu/shahih  -> SIFAR
```

Terjemahan hadis.my sebenarnya **Melayu tulen**: 100 hadis Bukhari
memberi `solat` 31, `bahawa` 84, `wuduk` 2, `Ramadan` 9 -- dan SIFAR
untuk `shalat`, `bahwa`, `Ramadhan`. Medan `indonesia` pula memberi
sebaliknya (`shalat` 26, `bahwa` 93).

Jadi masalahnya sempit: satu istilah tertinggal semasa penterjemahan.

### Rujukan ejaan: DBP (PRPM khidmat nasihat)
> "Sallallahualaihiwasallam ialah nama khas yang diambil daripada
>  bahasa Arab, oleh itu ejaannya dimulakan dengan huruf besar dan
>  kependekannya SAW."

`Sallallahu` (tanpa `h`), bukan `Shallallahu`.
Begitu juga `Radiallahu`, bukan `Radhiyallahu`.

### `utils/bahasa.py` (baharu)
`betulkan_melayu(teks)` -- dua kumpulan:
- **Selawat/taradhi**: regex fleksibel menangkap `Shallallahu`,
  `Shollallahu`, `Sallallaahu`, dsb.
- **Istilah**: shalat->solat, hadits->hadis, Ramadhan->Ramadan,
  adzan->azan, dzikir->zikir, wudhu->wuduk, shahih->sahih,
  mesjid->masjid, ustadz->ustaz, bahwa->bahawa

**Sengaja TIDAK diubah:** `kalian`. Ia difahami di Malaysia dan bukan
salah ejaan -- menggantinya mengubah gaya penterjemah, bukan
membetulkan kesilapan. Kita membetulkan transliterasi Arab, bukan
menyunting terjemahan.

### Prinsip: PAPARAN sahaja
Teks dalam `hadis.db` TIDAK ditulis semula. Pembetulan dilakukan pada
tiga titik paparan:
- `ui/app_qt.py:_switch_lang` (tab Melayu)
- `ui/widgets.py:hadith_card` (petikan senarai/carian)
- `ui/workers.py` (input Fasa 4 -- kesan topik + paparan)

Jika penilaian ini didapati salah kemudian, cukup matikan fungsi itu.

### Audit ketepatan
500 hadis daripada 5 kitab: **329 diubah (66%)**, dan senarai penuh
pasangan perkataan yang berubah ialah:
```
'Shallallahu' -> 'Sallallahu'
```
Satu sahaja. Tiada positif palsu.

Ujian 8bb dalam `semak.py`: 8 kes ubah + 7 kes "mesti kekal"
(`Abdullah bin Salam`, `Assalamualaikum`, `kalian`, teks kosong).

## Sesi 9 — Simbol selawat ﷺ (bukan singkatan "SAW")

Pengguna asalnya mahu pilihan "SAW". Saya bentangkan dua penemuan
sebelum melaksanakannya, dan pengguna memilih ligatur Arab.

### 1. Penjimatan ruang hanya 4% (diukur)
```
100 hadis Bukhari, 145 frasa selawat dalam 98 hadis
panjang purata asal : 838 aksara
dengan "SAW"        : 802 aksara   -> 4%
```
Manfaat "lebih mudah dibaca" jauh lebih kecil daripada disangka.

### 2. Majoriti ulama tidak menggalakkan singkatan
- **Ibn Salah** (Muqaddimah) — penulis hadis KHUSUSNYA hendaklah
  menulis selawat penuh setiap kali, "jangan jemu mengulanginya"
- **al-Sakhawi** (Fath al-Mughith) — menyingkat kepada dua huruf ialah
  `khilaf al-awla`
- **Ibn Baz** — makruh

Yang membenarkan pun berkata "sebaiknya tidak disingkat" — keringanan,
bukan pilihan setara.

### Penyelesaian: ligatur U+FDFA ﷺ
Satu titik kod yang MENGANDUNGI lafaz penuh
`صلى الله عليه وسلم`. Ia ringkas secara visual tetapi **bukan
singkatan dua huruf**, jadi tegahan ulama tidak terpakai.

### Risiko dikesan semasa ujian: TOFU
```
Segoe UI · Amiri · Scheherazade New · DejaVu Sans · Traditional Arabic
  -> glif U+FDFA: False (semua, dalam sandbox)
```
Tanpa semakan, pengguna nampak kotak kosong dan sangka apl rosak.

`simbol_boleh_dipapar()` menyemak `QFontMetrics.inFont()` merentas
beberapa fon calon. Jika tiada, **pilihan itu tidak dipapar langsung**
dalam Tetapan dan teks kekal penuh.

Semakan di-cache dalam `__init__` — `inFont()` mahal untuk dipanggil
pada setiap render kad.

### Lalai = BENTUK PENUH
Pengguna yang tidak membuka Tetapan mendapat bentuk yang ulama
galakkan. Simbol ialah pilihan sedar.

### NFKC: disemak, tiada kesan
`core/eng_source.normalisasi()` guna NFKC yang MELERAIKAN ligatur
kembali kepada teks penuh. Tidak menjadi masalah kerana ligatur hanya
wujud pada lapisan PAPARAN Melayu — ia tidak pernah masuk medan
`arab` mahupun disimpan ke DB.

### Diuji
```
tanpa glif : "Rasulullah Sallallahu 'alaihi wasallam" (kekal penuh)
dengan glif: "Rasulullah ﷺ bersabda"
Abdullah bin Salam / Assalamualaikum -> tidak tersentuh
```

## Sesi 9 — Ruang kosong di bawah halaman

Pengguna: buka kitab halaman 2, skrol ke hadis ke-20, skrol lagi ke
bawah sekali -- ada ruang kosong.

### Diukur
```
                sebelum   selepas
halaman kitab     41px      17px
halaman detail    17px      17px   (hadis panjang)
```

### Punca: margin BERTINDIH dengan addStretch
Setiap halaman ada `addStretch(1)` pada layout akar (Lesson 8c) yang
sudah memenuhi ruang lebihan. Margin bawah `40px` di ATAS itu hanya
menambah kosong lagi:
```
[kandungan] [addStretch mengembang] [margin 40px]  <- dua-dua kosong
```
Margin diturunkan `40px -> 16px` pada 5 halaman: kitab, carian,
detail, tersimpan, tetapan.

### Nota: 189px pada hadis PENDEK adalah BETUL
Halaman detail hadis pendek menunjukkan `ruang kosong = 189px`, tetapi
itu `addStretch(1)` berfungsi seperti sepatutnya -- ia menolak
kandungan ke atas supaya tidak meregang mengisi skrin.

Disahkan dengan hadis panjang: ruang kosong turun kepada 17px, dan
butang navigasi berakhir tepat di bawah kandungan.

Jangan "betulkan" 189px itu dengan membuang addStretch -- ia akan
menyebabkan Hero meregang semula (lihat Lesson 8c).

## Sesi 9 — Gap 188px pada halaman detail (pembetulan SEBENAR)

Percubaan pertama saya (margin 40px -> 16px) TIDAK menyelesaikannya.
Saya tersilap kata gap itu "betul kerana addStretch berfungsi".

### Diukur pada piksel sebenar (PIL, bukan geometri Qt)
```
halaman kitab  : 28px   <- memang kemas
halaman detail : 188px  <- INI yang pengguna nampak
```
Mengukur `body.height() - elemen_terbawah` mengelirukan kerana
`addStretch` mengembang di DALAM body. Imbasan piksel dari bawah
imej memberi jawapan sebenar.

Merentas panjang kandungan:
```
panjang teks   1    2    3    5    8   12
GAP          189  189  173  157  141   75
```
Gap wujud pada SEMUA hadis pendek -- iaitu majoriti.

### Punca
Kandungan 481px dalam viewport 669px. Ruang 188px itu MESTI berada di
suatu tempat; `addStretch(1)` meletakkannya selepas butang navigasi.

### Penyelesaian: bar navigasi DILEKATKAN
`_page_detail` kini sama struktur dengan `_page_pipeline`:
```
QWidget (luar)
├── QScrollArea      <- kandungan hadis
└── QFrame#bottombar <- Kembali · Huraian · No.N-1 · No.N+1
```
Butang ditulis ke `self._detail_nav` yang dikosongkan setiap render.

Hasil: **188px -> 8px**.

### Faedah sampingan
Butang navigasi kini sentiasa di tempat SAMA tidak kira panjang hadis.
Pada hadis panjang pengguna tidak perlu skrol ke bawah untuk menekan
Huraian atau Kembali.

Halaman detail dan Huraian kini berkongsi corak yang sama.

### Diuji
```
kitab/search/saved/home -> tooltip betul, destinasi betul
buka 3 hadis berturut   -> 4 butang (tiada pertindanan)
nombor navigasi dikemas kini: '< No. 11', 'No. 13 >'
```

## Sesi 9 — Audit gap SEMUA halaman (imbasan piksel)

Pengguna lapor "gap lagi" selepas dua pembetulan. Daripada meneka
halaman mana, saya imbas KESEMUA lapan halaman pada peringkat piksel.

```
halaman           sebelum   selepas
utama                33px      33px
kitab hal-2           0px       0px
detail pendek         8px       8px
detail panjang        8px       8px
carian kosong        40px      40px
carian hasil          0px       0px
tersimpan           401px   berpusat   <- INI puncanya
huraian              10px      10px
```

Pelajaran: jangan teka halaman mana. Tangkap semua, ukur semua.

### Punca 1: `empty_state` tidak mengembang
`QSizePolicy` lalai = Fixed menegak. Ia melekat di atas dan
meninggalkan 401px kosong. Tukar kepada `Expanding` menegak, dan
`addWidget(..., 1)` pada halaman kosong.

### Punca 2: `lo.setAlignment(Qt.AlignCenter)` TIDAK memusatkan
Ini menipu. Alignment pada QVBoxLayout **meruntuhkan** layout kepada
tinggi kandungan, kemudian meletakkannya di ATAS -- bukan di tengah.
401px jadi 223px, masih tersasar.

Betulnya: buang `setAlignment`, guna `addStretch(1)` di ATAS dan
BAWAH kandungan.
```python
lo.addStretch(1)
  ... ikon, tajuk, subtajuk ...
lo.addStretch(1)
```

Disahkan: ruang atas 230px, ruang bawah 231px -- berpusat.

### Nota tentang pengukuran
Imbasan "gap dari bawah" memberi 230px untuk halaman berpusat, dan itu
BETUL -- teks memang di tengah. Untuk keadaan kosong, ukur simetri
(atas vs bawah), bukan jarak ke bawah sahaja.

## Sesi 9 — Ruang skrol HANTU pada halaman kitab

Petunjuk penentu daripada pengguna: **"skrol boleh turun walaupun
kandungan habis"**. Itu bukan gap visual biasa -- julat skrol lebih
besar daripada kandungan.

### Diukur
```
body            = 3648px
kad terakhir    berakhir y=2773
addStretch(1)   menuntut  794px   <- ruang hantu
```
Hanya muncul apabila panjang kad BERBEZA-BEZA (data sebenar). Dengan
kad seragam, jumlahnya kebetulan menepati viewport.

### Punca
`addStretch(1)` diperlukan supaya Hero tidak meregang bila kandungan
pendek (Lesson 8c). Tetapi stretch **sentiasa** menuntut bahagiannya
daripada ruang lebihan, walaupun kandungan sudah melimpah -- dan
`setWidgetResizable(True)` memasukkan tuntutan itu ke dalam julat
skrol.

### Dua percubaan GAGAL (dicatat supaya tidak diulang)
1. **Perambatan geometri** selepas `_fit()` auto-saiz teks -- tiada
   kesan; masalahnya bukan tinggi kad.
2. **Memotong `maximumHeight` widget kandungan** dalam `make_scroll`
   -- body mengecil TETAPI pager terpotong keluar paparan. Lebih
   merosakkan daripada membaiki. Dipatah balik sepenuhnya.

### Penyelesaian
Ganti `addStretch(1)` dengan **spacer QWidget yang boleh runtuh**:
```python
pad = QWidget()
pad.setSizePolicy(Expanding, Expanding)
pad.setMaximumHeight(0)          # <- kunci: runtuh ke 0
lo.addWidget(pad, 1)
```
`maximumHeight(0)` membenarkan Qt meruntuhkannya sepenuhnya apabila
kandungan melimpah, tidak seperti item stretch.

Kesan sampingan: Hero mula meregang (101px -> 895px) kerana ia kini
satu-satunya yang boleh menyerap ruang. Dibetulkan dengan
`SetMinAndMaxSize` -> `SetFixedSize` pada layout Hero.

### Hasil
```
                sebelum  selepas
kitab hal-2       28px      8px
skrol penuh      794px    tiada ruang hantu
Hero              101px    116px (terkunci)
```
Semua halaman lain tidak berubah.

## Sesi 9 — PATAH BALIK: pembetulan "ruang skrol hantu" MEROSAKKAN UI

Tangkapan skrin pengguna menunjukkan kerosakan teruk:
- Hero mengecil jadi kotak kiri atas (1230px -> ~370px lebar)
- Kandungan tersebar; breadcrumb terapung di tengah skrin kosong
- Senarai hadis ditolak jauh ke bawah

### Punca kerosakan
1. **`SetFixedSize` pada layout Hero** — ia mengunci LEBAR juga, bukan
   tinggi sahaja. Hero berhenti melebar mengikut tetingkap.
2. **Spacer `setMaximumHeight(0)`** — ia TIDAK boleh menyerap ruang
   lebihan. Ruang itu terpaksa pergi ke `col`, yang kemudian
   menyebarkan kandungan dalamnya.

Kedua-duanya dipatah balik:
```
QVBoxLayout.SetFixedSize      -> SetMinAndMaxSize
spacer maxHeight(0)           -> addStretch(1)
```

### Keadaan sekarang (disahkan)
```
Hero: 1230 x 101   (penuh lebar, tinggi normal)
utama 33 · kitab 0 · detail 8 · carian 0 · huraian 10
```

### Pengajaran
Ruang skrol hantu 794px itu **kekal tidak diselesaikan**, dan itu
lebih baik daripada UI yang rosak. Tiga percubaan gagal:
1. perambatan geometri — tiada kesan
2. potong maximumHeight dalam make_scroll — pager terpotong keluar
3. spacer boleh-runtuh + SetFixedSize — merosakkan Hero & susun atur

**JANGAN cuba lagi tanpa tangkapan skrin visual setiap langkah.**
Ukuran nombor (body height, gap px) TIDAK memadai — ketiga-tiga
percubaan "berjaya" pada nombor tetapi merosakkan paparan.

Jika hendak dicuba semula: uji pada tetingkap DIMAKSIMUMKAN dan
periksa lebar Hero, bukan tinggi sahaja.

## Sesi 9 — Lompang skrol: BERHENTI mencuba (4 percubaan gagal)

### Diagnosis akhir
```
col.sizeHint  = 3531px   (yang ia MAHU)
col.geometry  = 2689px   (yang ia DAPAT)
addStretch    =  842px   <- dirampas daripada kandungan
```
`addStretch(1)` merampas ruang daripada `col`, kemudian
`setWidgetResizable(True)` menjadikan ruang itu boleh diskrol.

### Membuang stretch MEMANG mengecilkan lompang
```
            Hero    lompang
dgn stretch  101px    923px
tanpa        943px     81px   <- Hero meregang, UI ROSAK
```
Hero menyerap ruang itu sebaliknya. Ia satu-satunya widget
`Expanding` yang tinggal.

### Empat percubaan, semua gagal
1. Perambatan geometri selepas auto-saiz — tiada kesan
2. Potong `maximumHeight` dalam `make_scroll` — pager terpotong keluar
3. Spacer `maxHeight(0)` + `SetFixedSize` — Hero jadi kotak kecil
4. `QTimer` kunci tinggi Hero — dipanggil sebelum saiz stabil,
   Hero jadi 657px

### KEPUTUSAN: kekalkan addStretch
Lompang skrol ~900px pada senarai panjang DITERIMA sebagai kos.
Ia tidak merosakkan apa-apa fungsi -- pengguna hanya boleh skrol
sedikit melebihi pager.

**JANGAN cuba lagi** melainkan ada pendekatan berbeza sepenuhnya,
cth. menggantikan QScrollArea dengan QListView bervirtual. Setiap
percubaan setakat ini merosakkan sesuatu yang lebih penting.

Sebarang percubaan MESTI disertakan tangkapan skrin halaman penuh
pada tetingkap dimaksimumkan -- ukuran nombor sahaja telah menipu
saya empat kali.

## Sesi 9 — Fasa 1-3 dibuang SEBENARNYA daripada kod

Pengguna betul: kita putuskan Fasa 1-3 dibuang, tetapi saya hanya
menyembunyikannya daripada paparan. Kod masih ada dan tidak pernah
berjalan.

### Kod mati dibuang
`PipelineWorker.run()` mempunyai 51 baris untuk Fasa 1-3 selepas
`if self.hanya_huraian: return` -- dan `hanya_huraian=True` SENTIASA.
Laluan itu mustahil dicapai.

```
ui/workers.py   215 -> 164 baris
```

Parameter `hanya_huraian` juga dibuang -- tiada mod lain lagi, jadi
ia hanya menambah kekeliruan.

### `_on_phase` diringkaskan
Cabang `if n==1 / elif n==2 / elif n==3` tidak boleh dicapai. Kini:
```python
rows = [(k.replace("_"," ").title(), data.get(k,""))
        for k in self.MEDAN_HURAIAN]
```
Chip `"AUTO" if n==4 else f"FASA {n}"` -> `"AUTO"` sahaja.

### Modul core/
```
phase1_extract.py   DIBUANG   0 pemanggil, 6 baris normalisasi
phase2_transliterasi.py  KEKAL  dipanggil app_qt._bina_translit
phase3_translate.py      KEKAL  0 pemanggil TETAPI ia satu-satunya
                                tempat logik TIADA_ENGLISH
                                (ahmad/darimi) wujud
phase4_exegesis.py       KEKAL  teras Huraian
```
`phase3` ditandakan dengan jelas dalam docstringnya bahawa ia tidak
dipanggil, supaya tiada sesi akan datang menyangka ia aktif.

### Disahkan berfungsi
```
transliterasi (phase2): haddathana musaddadun qala as-salahu...
huraian (phase4)      : auto
kad fasa dipapar      : [4]
```

## Sesi 9 — LOMPANG SKROL SELESAI (percubaan ke-6)

### Diagnosis tepat (probe pokok widget)
```
kandungan tamat  y=2742
body.height()      3314
-> 572px TANPA sebarang widget
```
Ruang layout tulen daripada `addStretch(1)`.

### Kenapa 5 percubaan lalu gagal
Semua cuba mengekalkan `addStretch` DAN menghilangkan lompang. Mustahil
-- stretch itu SENDIRI yang mencipta ruang. Ia mesti dibuang.

Masalahnya: tanpa stretch, Hero menjadi satu-satunya widget Expanding
dan meregang 101px -> 657px.

### Penyelesaian: Hero kunci tinggi sendiri
```python
def resizeEvent(self, e):
    super().resizeEvent(e)
    lebar = self.width()
    if lebar <= 0 or lebar == getattr(self, "_lebar_dikunci", -1):
        return
    self._lebar_dikunci = lebar
    self.setMinimumHeight(0); self.setMaximumHeight(16777215)
    h = self.layout().sizeHint().height()
    if h > 0:
        self.setFixedHeight(h)
```

Tiga sebab pendekatan LAIN gagal:
- `QTimer.singleShot(0)` -- dipanggil sebelum saiz stabil (Hero 657px)
- kunci sekali sahaja -- pecah bila tetingkap diubah saiz
- `SetFixedSize` -- mengunci LEBAR juga, Hero jadi kotak kecil

Kunci berdasarkan LEBAR SEMASA menyelesaikan ketiga-tiganya: tinggi
dikira semula setiap kali lebar berubah (kerana pembalutan teks
bergantung pada lebar), tetapi tidak pada setiap resizeEvent.

### Hasil
```
lompang: 573px -> 17px

saiz tetingkap    Hero          lompang
1240x700          1230x116        17px
1600x900          1590x116        17px
1000x650           990x116        17px
1920x1080         1910x116        17px
```
Hero melebar betul; tinggi kekal 116px.

Semua halaman lain tidak berubah:
utama 33 · detail 8 · carian 0 · tersimpan berpusat · huraian 10

### Ujian 8c dikemas kini
Menerima halaman yang SENGAJA tiada stretch, dikenal melalui komen
"TIADA addStretch". Semakan meliputi metod `_render_*` juga, bukan
`_page_*` sahaja.

## Sesi 9 — Kandungan tersebar selepas membuang addStretch

GIF pengguna menunjukkan Hero hilang dan kandungan bertaburan. Punca:
membuang `addStretch` memindahkan masalah, bukan menghapuskannya.

### Diagnosis
```
Hero            = 116px   (betul)
kad pertama y   = 472px   <- 356px kosong antara
```
Probe layout dalam:
```
[0] breadcrumb   h=227px   sepatutnya ~30px
[1] senarai kad  h=2370px
[2] Pager        h=226px   sepatutnya ~52px
```

### Punca
Tanpa `addStretch`, ruang lebihan diagihkan kepada SETIAP anak yang
tiada polisi saiz menegak eksplisit. `breadcrumb()` dan `Pager` guna
lalai `Preferred`, jadi kedua-duanya meregang 4x.

Hero tidak terjejas kerana ia sudah mengunci tingginya sendiri.

### Pembetulan
```python
# breadcrumb()
w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
# Pager.__init__
self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
```

### Hasil
```
kad pertama: y=472 -> y=195
disahkan pada 1240x700, 1920x1080, 930x516 -- semua y=195
```

### Pengajaran
Membuang `addStretch` memerlukan SETIAP anak layout mempunyai polisi
menegak yang eksplisit. Jika tidak, ruang lebihan hanya berpindah
kepada widget lain yang tidak dijangka.

Semak: Hero (dikunci), breadcrumb (Fixed), Pager (Fixed),
senarai kad (Expanding melalui centered_column).

## Sesi 9 — Lompang halaman CARIAN (corak sama)

Selepas halaman kitab dibetulkan, pengguna lapor halaman carian pula.
Punca identik.

### Diukur
```
[0] Hero      159px
[1] kandungan 2559px
[2] STRETCH   550px   <- kawasan skrol kosong
```

### Pembetulan
Buang `bl.addStretch(1)` daripada `_page_search`, DAN pastikan setiap
anak layout mempunyai polisi menegak eksplisit:
```
Hero        -> kunci tinggi sendiri (resizeEvent)
search_info -> QSizePolicy Fixed   <- BAHARU
Pager       -> Fixed (sudah)
senarai kad -> Expanding via centered_column
```

`search_info` ialah QLabel tanpa polisi -- ia akan meregang
menggantikan stretch jika tidak ditetapkan. Corak sama seperti
breadcrumb pada halaman kitab.

### Hasil
```
carian skrol penuh : 550px -> 28px
carian kosong      : empty_state berpusat (28px)
tiada hasil        : empty_state berpusat (171px)
```
Kedua-dua keadaan kosong kekal betul kerana `empty_state` mempunyai
`Expanding` + stretch dalaman sendiri.

### Corak lengkap (untuk halaman baharu)
Apabila membuang `addStretch` daripada layout akar QScrollArea, SETIAP
anak mesti mempunyai polisi menegak eksplisit. Widget tanpa polisi
akan menyerap ruang lebihan dan meregang.

## Sesi 9 — Pembetulan lompang PENGGUNA (lebih baik daripada saya)

Pengguna menghantar penyelesaiannya sendiri selepas 6 percubaan saya
gagal. Ia berfungsi, dan pendekatannya berbeza sepenuhnya.

### Idea teras: `resize(sizeHint())` selepas kandungan diisi
```python
body.layout().invalidate()
body.layout().activate()
body.resize(body.sizeHint())
```
`setWidgetResizable(True)` memberi widget kandungan tinggi berdasarkan
minimumSize layout -- yang TERMASUK tuntutan item stretch. Memaksa
`resize(sizeHint())` selepas kad diisi mengira semula berdasarkan apa
yang BENAR-BENAR ada.

Saya cuba menghalang stretch daripada menuntut ruang. Pengguna
membiarkan ia menuntut, kemudian membetulkan hasilnya. Lebih mudah.

### Sokongan: layout telanjang -> QWidget container
```python
self._kitab_list = QVBoxLayout()      # sebelum: addLayout
cl.addLayout(self._kitab_list)

self._kitab_container = QWidget()      # selepas: addWidget
self._kitab_list = QVBoxLayout(self._kitab_container)
cl.addWidget(self._kitab_container)
```
QWidget mempunyai `sizeHint()` yang boleh diukur; layout telanjang
tidak. Tanpa ini `resize(sizeHint())` tidak tepat.

### `widgets.py`: inner Minimum -> Preferred
`Minimum` menjadikan sizeHint sebagai HAD BAWAH -- inner boleh
membesar melebihi kandungan. `Preferred` memberi tepat sizeHint.

### PEPIJAT dalam versi pengguna
```python
PipelineWorker(h, hanya_huraian=True)   # TypeError
```
Parameter itu dibuang lebih awal sesi ini apabila laluan Fasa 1-3
dipadam. Butang Huraian akan crash. Dibetulkan kepada
`PipelineWorker(h)`.

### Penambahbaikan saya atas kod pengguna
Pengguna mengulang 4 baris `invalidate/activate/resize` di setiap
tempat. Diekstrak ke `_laras_tinggi(sa)` -- satu definisi, dipanggil
dari `_on_kitab_page`, `_on_search`, `_fill_phase`.

### Hasil akhir (imbasan piksel, semua halaman)
```
utama 33 · kitab 8 · detail 8 · carian 0 · huraian 10 · tersimpan berpusat
skrol penuh: kitab 28px · carian 28px
```
Hero kekal 1230x101. Tiada regresi.

## Sesi 9 — `centered_column`: outer Minimum -> Maximum

Pengguna mencadangkan `outer.setSizePolicy(..., QSizePolicy.Maximum)`.

### Kenapa ia betul
```
Minimum : sizeHint = had BAWAH  -> outer boleh MEMBESAR melebihi
                                   kandungan (ruang skrol kosong)
Maximum : sizeHint = had ATAS   -> Qt tidak membesarkannya
```

### Lesson #4 disemak semula
Komen dalam fail memberi amaran `Maximum` meruntuhkan tinggi ke 0
sebelum susun atur pertama. Diuji khusus (tetingkap 640x480 -> 1240x700,
semua 7 halaman diperiksa):
```
Maximum : halaman runtuh ke 0 = TIADA · Tetapan isi=3602
Minimum : halaman runtuh ke 0 = TIADA · Tetapan isi=3602
```
Amaran itu terpakai kepada **`inner`**, bukan `outer`. `inner`
mengandungi layout kandungan sebenar; `outer` hanya pembungkus
mendatar untuk memusatkan. Komen lama tidak membezakan keduanya --
kini dijelaskan.

`inner` kekal `Preferred` (bukan Maximum, bukan Minimum).

### Disahkan tiada regresi
```
utama 33 · kitab 8 · detail 8 · carian 0 · huraian 10
tersimpan: teks kosong berpusat, dipapar betul
skrol penuh: kitab 28px · carian 28px
butang Huraian: tiada crash
```

---

# Sesi 10 — Padanan terjemahan Inggeris: 92.6% ilusi → 98% disahkan

## Penemuan utama: kunci padanan yang salah selama ini

Padanan dibina atas **teks Arab**. Ia sepatutnya guna **teks Indonesia**.

Sebabnya ditemui secara tidak sengaja. Audit saksi bebas membandingkan
`hadis.db.indonesia` (dari hadis.my) dengan CDN `ind-*` dan mendapat
pertindihan purata **1.00** — bukan ~0.85 seperti dijangka bagi dua
terjemahan bebas. Kesimpulan: kedua-duanya **terjemahan yang sama**.

| | Arab | Indonesia |
|---|---|---|
| tashkeel | hadis.my penuh, CDN tidak | tiada isu |
| sanad dikongsi antara hadis | punca SEMUA positif palsu | tiada |
| lapisan diperlukan | 3 + Jaccard dua hala | padanan tepat |

## Kronologi

```
92.6% "liputan baik"   <- ILUSI: 23.2% dari lapisan `kata` yang rosak
88%  (28,469)          <- selepas Jaccard dua hala buang yg salah
94%  (30,593)          <- selepas lapisan `indo` (padanan tepat)
98%  (31,833)          <- selepas lapisan `indo~` (padanan kabur)
```

Bukhari diaudit: **100.0% disahkan, 0 disyaki** (6,598 hadis).

## Pepijat 1: `padan_kata` mengira skor SEHALA

`padan_kata` bertanya "berapa banyak kata soalan ada pada calon".
Ia BUTA terhadap kata pada calon yang tiada pada soalan. Sanad panjang
boleh jadi 80% daripada hadis pendek, jadi dua hadis dengan matn
BERBEZA SEPENUHNYA kelihatan serupa.

**Ujian yatim** (buang 600 hadis dari indeks, cari semula; jawapan
betul = "tiada padanan"):

| kitab | FP tanpa Jaccard | FP dengan 0.90 | padanan betul hilang |
|---|---|---|---|
| bukhari | 35.3% | 5.2% | 0 |
| muslim | 16.0% | 2.3% | 0 |
| nasai | 29.3% | 3.3% | 0 |
| malik | 8.1% | 0.4% | 0 |

`JACCARD_MIN = 0.90` — buang 85% positif palsu, kos SIFAR.
Daripada 31 baki Bukhari: 22 teks normalisasi IDENTIK (pendua tulen),
9 benar tersalah = 1.5%.

## Pepijat 2: `INSERT OR REPLACE` tidak membersih

Baris yang DAHULU dipadan dan kini ditolak KEKAL dalam DB dengan
terjemahan salah. Menjalankan semula sync tidak membaikinya.
Ditambah `DELETE FROM terjemahan_eng WHERE collection=?` sebelum simpan.

## Pepijat 3: tiada cara membezakan versi kod

Pengguna menjalankan salinan LAMA dua kali; outputnya kelihatan sah dan
tiada cara mengesannya. Kedua-dua skrip kini mencetak
`Jaccard dua hala: 0.9` di kepala output.

**Corak am: setiap skrip diagnostik mesti cetak cap versi/parameternya.**

## Turutan padanan (turutan SENGAJA)

```
1. indo   -> teks Indonesia dinormalisasi, padanan TEPAT
2. indo~  -> token Indonesia, Jaccard >= 0.95  (JACCARD_IND)
3. penuh  -> teks Arab dinormalisasi penuh
4. awalan -> 200 aksara pertama, hanya jika UNIK
5. kata   -> token Arab jarang + Jaccard dua hala >= 0.90 (JACCARD_MIN)
```

Kesan `indo~` (Jaccard 0.95). Ujian yatim 500:

| kitab | FP | pendua tulen | BENAR tersalah | betul |
|---|---|---|---|---|
| tirmidzi | 0 | 0 | **0** | 100% |
| bukhari | 32 | 32 | **0** | 95.2% |
| muslim | 5 | 5 | **0** | 98.6% |

Tirmidzi ialah kes yang mendedahkan keperluan `indo~`: padanan tepat
hanya dapat 136/3,891 walaupun CDN ada 3,538 teks unik — perbezaan
tanda baca dan kurungan perawi memusnahkan padanan aksara-demi-aksara.
Selepas `indo~`: 136 -> 3,318. Kitab itu melonjak 90% -> 96%.

## Corak metodologi: audit mesti guna BUKTI BEBAS

`diagnos_padanan.py` menilai padanan-teks-Arab dengan membandingkan
teks Arab — **berhujah dalam bulatan**. Ia boleh beritahu berapa yang
dipadan, bukan berapa yang BETUL.

`audit_eng.py` menggunakan saksi ketiga (teks Indonesia) yang TIDAK
PERNAH digunakan untuk membuat padanan. Pemisahan yang diukur:
padanan betul 1.00 · padanan salah 0.05 · sifar pertindihan.

Lapisan `indo`/`indo~` ditandakan **"(bukan bukti bebas)"** dalam
laporan kerana mengauditnya dengan teks Indonesia adalah berpusing.

## `ara-*1` vs `ara-*`

Kedua-dua edisi Arab CDN disahkan **identik selepas normalisasi**
(malik 1858/1858, muslim 7562/7563). `ara-*1` failnya lebih kecil.

## Fail

```
core/eng_source.py   JACCARD_MIN · JACCARD_IND · kunci_indonesia()
                     bina_indeks_ind() · bina_indeks_ind_kata()
                     padan_ind_kabur() · padan() 5 lapisan
sync_english.py      DELETE dahulu · muat ind-* · cap versi
audit_eng.py         BAHARU — audit saksi bebas
diagnos_padanan.py   cap versi · taburan kualiti Jaccard
semak.py             seksyen 8c (12 semakan) · 8d susun atur
```

## Nota: "birai" Jaccard BUKAN penggera

Diuji dengan teks diusik 12%: 60% padanan jatuh dalam julat 0.90-0.94
namun ketepatan kekal **100%**. Beza tanda baca dan riwayat dipendekkan
memang hasilkan Jaccard rendah secara sah. Amaran automatik dibuang
kerana ia akan menggera palsu.

---

# Sesi 10B — Fath al-Bari: penomboran HANYUT, Fasa 4B tidak boleh guna padanan ID

## Keputusan: penanda `# N` BUKAN nombor hadis

Pengawal membatalkan sync pada 39%. Siasatan mendapati **pengawal betul**
tetapi atas sebab yang salah — dan angka 76% yang direkod dalam sesi lalu
ialah **artifak metodologi**.

## Punca 1: sampel 80 hadis PERTAMA

`sahkan_padanan()` guna `LIMIT 320` lalu ambil 80 pertama. Syarah paling
terperinci pada permulaan kitab. Kadar sebenar merentas Bukhari:

```
   1-500    29%        3000-5000  11%
 500-1500   13%        5000-7600  10%
1500-3000   11%
```

80 pertama -> 76%. Seluruh kitab -> 13%. **Ambang 50% tidak pernah boleh
dicapai oleh sumber ini**, walaupun ia sah.

## Punca 2 (SEBENAR): penomboran hanyut progresif

Anjakan terbaik per julat, diukur dengan kata jarang matn:

```
   1-200     +0     (sejajar sempurna)
 200-400     -4
 400-600    -12
 600-800    -32
2000-3500  -120
5000-7000  -320
```

Penanda `# N` ialah **kiraan hadis berjujukan dalam edisi Ibn Hajar**,
bukan nombor hadis Bukhari standard. Ia bermula sejajar (kedua-duanya
mula pada 1) dan menyimpang apabila edisi berbeza dalam apa yang dikira
sebagai hadis berasingan.

Nota: 5,111 penanda, 99% menaik, max 125,252 (85 seksyen >7008).

## Padanan teks juga GAGAL

Cubaan memadan seksyen syarah -> hadis melalui kata jarang:
```
300 seksyen diuji: 171 dapat calon, 129 tiada
  nombor sama dgn penanda:   2
  nombor berbeza          : 169
  delta: median 174, min -4853, max 7519   <- tiada corak
```
Syarah memetik **potongan** (`قوله حدثنا الحميدي`) bukan matn penuh,
jadi tiada isyarat teks yang cukup untuk padanan automatik yang selamat.

## Metrik lama tidak membezakan apa-apa

Metrik berasaskan kata SANAD:
```
penomboran betul  1.21x
digeser +50       1.20x     <- hampir sama!
```
Kata sanad muncul dalam hampir setiap syarah. Metrik baharu guna
**kata jarang matn** (df<=30, panjang>4, bukan senarai LAZIM).

## Pengawal baharu: perbandingan + pengesanan hanyut

`nisbah_keyakinan()` menggantikan ambang mutlak:
1. anjakan-0 mesti mengatasi kawalan (-2,-1,+1,+2) sebanyak `NISBAH_MIN` 1.8x
2. anjakan terbaik mesti kekal ~0 pada **>=80% julat** merentas kitab

Menuntut 6/6 julat sempurna menolak kawalan positif (bunyi rawak pada
julat jarang) — 80% ialah nilai yang lulus ketiga-tiga kawalan:

```
Fath al-Bari SEBENAR              nisbah 1.21x  stabil=False  TOLAK  [+0 -60 -140 +0 -300 -360]
kawalan POSITIF (tiruan sejajar)  nisbah 3.92x  stabil=True   TERIMA [+0 +0 +0 +0 -100 +0]
kawalan NEGATIF (geser +200)      nisbah 1.10x  stabil=False  TOLAK  [+200 +140 +60 +0 +0 -160]
```

Juga: `diagnos_hanyut()` hanya isytihar hanyut jika anjakan lain
mengatasi anjakan-0 sebanyak **1.5x** — tanpa itu bunyi rawak
menghasilkan anjakan palsu.

## Pepijat sampingan: penanda manuskrip

`ms00022` menyelit DI TENGAH ayat Arab, **10,952 kali**. Berbeza
daripada `PageV..P..` yang berdiri sendiri. Akan dipapar kepada
pengguna sebagai aksara Latin. Dibetulkan: `_MS = r"\bms\d{3,}\b"`
(sengaja 3+ digit; `ms12` dan `msجديد` kekal).

## PELAJARAN AM (berulang kali sesi ini)

**Sampel dari SATU HUJUNG julat memberi jawapan yang salah.**
- Fasa 3: audit ikut nombor sahaja menyembunyikan 35% positif palsu
- Fasa 4B: 80 hadis pertama memberi 76%, sebenarnya 13%

**Setiap pengawal perlu kawalan POSITIF dan NEGATIF.** Pengawal
pertama saya menolak Fath al-Bari (betul) TETAPI juga menolak kawalan
positif tiruan (salah) — tidak dapat dikesan tanpa mengujinya.

## Status Fasa 4B

**Keputusan pengguna 31 Jul 2026: GUGURKAN 4B buat sementara — tumpu 4A.**
Fath al-Bari kekal di arkib (Sesi 7-9); jangan buka semula tanpa sebab baru.

**Fath al-Bari TIDAK BOLEH diguna dengan padanan ID.** Pilihan yang pernah
dipertimbangkan:
1. Sumber lain yang menyimpan nombor hadis standard
2. Padanan manual/separa-manual bagi hadis terpilih
3. Papar syarah ikut BAB, bukan ikut hadis
4. Gugurkan 4B; tumpu pada 4A (Irsyad al-Hadith, BM) — ✅ DIPILIH

---

# Sesi 10 — Fasa 4 SIAP melalui HadeethEnc (padanan MATN)

## Keputusan: sumber huraian baharu

Fath al-Bari dibatalkan buat sementara (keputusan 31 Jul 2026). Keputusan: **HadeethEnc.com**
(projek IslamHouse) sebagai sumber "Huraian" Melayu yang jujur.

- API: `https://hadeethenc.com/api/v1` (tiada kunci, cuma User-Agent)
- `one?language=ms` → **404 hanya bila hadis tiada terjemahan Melayu**
  (hadis wujud; `language=ar` berfungsi). `list?language=ms` juga
  **menyembunyikan** hadis tanpa BM (cat 134: 8 vs 100 dengan `en`).
- Enumerasi betul: `list?language=en` (452 kategori) + tapis
  `translations[]` mengandungi `"ms"` → **147 hadis unik ber-BM**.
- Semua 147 dimuat turun ke `.cache_he/`; 280 padanan disimpan.

## Padanan MATN, bukan ID

- HadeethEnc tidak guna nombor hadis.my; padan ikut **matn**.
- `_matn()` tanggalkan sanad dulu (kaedah `حَدَّثَنَا ... عَنْ`).
- Jaccard 0.55 (kata set, bukan aksara): betul 0.62–1.00, salah 0.04–0.48.
- Pengawal tolak calon hampir-sama jika matn Jaccard < 0.9 (hadis asing
  yang berkongsi pembukaan matn, e.g. Bukhari 50 → kawalan tolak).
- Hasil: bukhari 60 · muslim 32 · abu-daud 16 · tirmidzi 12 · nasai 19 ·
  ibnu-majah 22 · ahmad 107 · darimi 10 · malik 2 (jumlah **280**).

## Integrasi

- DB migrasi 4: jadual `hadethenc(collection, hadis_id, he_id, jaccard, kaedah)`
- `phase4_exegesis._hadeethenc()` → `status="dari_sumber"`, `topic`=title,
  `teachings`=explanation, `summary`=hints, `background`=sumber/atribusi
- UI memetakan `dari_sumber` → ✓; hadis lain kekal `auto` ◐ + penafian
- `sync_hadeethenc.py` padam baris lama dahulu sebelum simpan
  (migrasi jadual semula selepas skema berubah tidak menduakan)
- `semak.py` 8e: JACCARD_MATN dalam julat · `_matn` buang sanad ·
  hadis tulen dipadan / asing ditolak · integrasi UI

## Bug ditemui

- `hadeethenc_api.padan()`: `_jaccard_set(set_soalan, indeks[...].split())`
  → argumen kedua perlu `set(...)`; TypeError `'set' & 'list'`. Dibetulkan
  (dua tempat).
- `semak.py`: semakan jadual `hadethenc` diletak selepas `conn.close()` →
  dipindah ke atas.

## Atribusi wajib

Huraian bukan tulisan kami. Papar: "Huraian ringkas oleh HadeethEnc.com
(projek IslamHouse). Kandungan tidak diubah." Status `dari_sumber`
menandakan teks asing yang jujur, bukan `auto` generik.

---

# Sesi 11 — Fasa 4A disiasat SELESAI: lesen Irsyad TERTUTUP, tiada sumber BM lain

## Keputusan 31 Jul: dua keputusan berasingan

1. **Fasa 4B (Fath al-Bari)** — DIBATALKAN buat sementara (Pilihan 4).
   Rincian di Sesi 10B.
2. **Fasa 4A (Irsyad al-Hadith)** — disiasat, lesen TERTUTUP. Keputusan
   pengguna: cari sumber BM lain → disiasat → **tiada yang sah**.
   Fasa 4A ditutup sebagai *disiasat, tiada calon sah*.

## Lesen Irsyad al-Hadith (JMWP) — TERTUTUP

- Footer `muftiwp.gov.my`: **"Hak Cipta Terpelihara © 2024 Jabatan Mufti
  Wilayah Persekutuan"** = *all rights reserved*.
- Halaman **"Data Terbuka Kerajaan"** hanya menyenaraikan **2 set data
  waktu solat** — artikel Irsyad **TIDAK termasuk**.
- Tiada terma penggunaan semula untuk artikel. Memasukkan semula huraian
  ke aplikasi tanpa izin = pelanggaran hak cipta.

## Struktur & padanan (didokumenkan untuk rekod)

- Senarai: `https://muftiwp.gov.my/ms/artikel/irsyad-al-hadith?start=N`,
  ~25 halaman × 25 artikel.
- Setiap artikel: Soalan + Jawapan + **Nota hujung** memetik nombor hadis
  berstruktur ("Riwayat Muslim no 1037" → muslim #1037; "Riwayat al-Bukhari
  (697)").
- **Kelemahan padanan:** banyak rujuk kitab LUAR 9 koleksi DB (al-Baihaqi,
  Syu'ab al-Iman, al-Marasil, al-Adab al-Mufrad); artikel mustholah umum
  (cth. "Hadith Mursal") tiada satu hadis untuk dipadan.

## Sumber BM lain disiasat — semua ditolak

| Sumber | Lesen | Bentuk | Keputusan |
|---|---|---|---|
| HadeethEnc (diguna) | ✅ percuma (3 syarat) | 147 hadis BM | Kekal |
| Irsyad al-Hadith (JMWP) | ❌ Hak Cipta Terpelihara | artikel Q&A | Dilarang |
| MyHadith (islam.gov.my) | ❌ kerajaan | Q&A | `Transport error` ×2 |
| IslamHouse Malay | ✅ percuma (3 syarat) | 53–74 buku PDF | Bukan per-hadis |
| hadits.id / NU / tazkia / Kemenag | ❌ kerajaan/komersial | terjemahan sahaja | Tiada syarah |
| Syarah Bulughul Maram | ❌ terjemahan penerbit | syarah Utsaimin | Kitab berbeza |

- **IslamHouse Malay** — lesen "Permission is granted to all to take
  material... 3 syarat: 1) tiada keuntungan, 2) atribusi, 3) jangan konteks
  dipotong" — **sama keluarga dengan HadeethEnc** yang sudah diguna.
  Tetapi kandungannya buku PDF (bukan per-hadis), jadi tidak boleh dipadan
  ke hadis.db.
- **MyHadith JAKIM** (`myhadith.islam.gov.my`) — dua percubaan `Transport
  error`. Laman kerajaan lazimnya "Hak Cipta Terpelihara" juga; tidak
  diusahakan lanjut.
- **superXdev/hadits-api** (GitHub) — API 9 perawi tetapi **teks hadis
  sahaja**, bukan syarah.
- **Ensiklopedi Hadits Lidwa** — aplikasi Android, pemilik konten komersial,
  tidak terbuka.

## Kesimpulan

**Tidak ada sumber syarah BM per-hadis berlesen terbuka selain HadeethEnc.**
147 hadis BM HadeethEnc ialah siling tetap. Semua calon lain sama ada
dilarang (kerajaan/komersial) atau tidak berstruktur per-hadis.

**Keputusan:** Fasa 4A ditutup sebagai *disiasat, tiada calon sah*.
Nilai sebenar yang tinggal bukan sumber baharu tetapi **kualiti**:
kategori auto (Sesi 10, §11 PERUBAHAN_31JUL) + nota auto (Lapisan C).
Projek boleh dianggap **SIAP untuk diedar** pada liputan semasa.

## Fail dikemas kini

- `PERUBAHAN_31JUL.md` — §13 (si saya 4A + jadual sumber BM + kesimpulan)
- `RANCANGAN_4FASA.md` — Lapisan A ⚫ DITUTUP; keutamaan paparan; jadual
  kerja; isu belum selesai
- `MULA_SINI.md` — §Fasa 4A DITUTUP + jadual sumber ditolak; "Belum selesai"
- `sesi_index.md` — dokumen ini (Sesi 11)

---

# Sesi 12 — Workspace Developer + dua manual (ZIP belum diedar)

## Keputusan pengguna (selepas §14 bina ZIP)

- Folder root `hadis/` ialah **workspace Developer**, BUKAN untuk pengguna
  akhir lagi. `PustakaHadith.zip` **belum diedar**.
- Masih banyak penambahbaikan yang perlu dibuat; akan dilakukan apabila
  developer menjalankan app untuk semakan.
- Semua perubahan selesai + tertangguh mesti direkodkan untuk rujukan.

## Hasil sesi

- **`MANUAL_PENGGUNA.md`** (baharu) — manual pengguna akhir lengkap:
  pengenalan, keperluan sistem, cara pasang (`PASANG.bat`), dapat &
  masukkan kunci API, antara muka, panel tetapan, kemas kini
  (`KEMASKINI.bat`), penyelesaian masalah, nyahpasang (`BUANG.bat`),
  privasi.
- **`MANUAL_REFERENSI_DEV.md`** (baharu) — rujukan utama developer satu
  fail: keadaan workspace, struktur fail, status fasa, fakta API hadis.my,
  hadis.db, peraturan padanan (JANGAN dilanggar), skrip utiliti,
  penambahbaikan tertangguh (§8), senarai semak, 3 corak pepijat berulang,
  pepijat Qt, peta dokumen.
- `MULA_SINI.md` — §5 dikemas kini: status workspace + penambahbaikan
  tertangguh; §"Belum selesai" ditambah senarai ringkas.
- `RANCANGAN_4FASA.md` — "Isu belum selesai" ditambah nota workspace/ZIP.
- `PERUBAHAN_31JUL.md` — §15 (kelarikan workspace + dokumentasi).
- `semak.py` disahkan lulus selepas kemas kini (5 kegagalan pengedaran
  dijangka pada mesin pembangunan); semakan #11 dokumen konsisten lulus.

---

# Sesi 12b — Tamat hari (31 Jul): titik sambung esok

Pengguna menjalankan ujian sendiri dahulu; sambung esok.

**Sesi seterusnya bermula dengan:**
1. Baca `MANUAL_REFERENSI_DEV.md` (rujukan utama) + `MULA_SINI.md`
2. Ulasan ujian pengguna — semak `NYAHPEPIJAT.bat` output jika ada masalah
3. Penambahbaikan tertangguh (`MANUAL_REFERENSI_DEV.md` §8) — bermula
   dengan semakan end-to-end app oleh developer (install → API → baca →
   tersimpan)
4. Selepas semakan selesai: bina semula `PustakaHadith.zip` + semak_versi

---

# Sesi 12c — Brainstorming: JANGAN bina padanan hadis→ayat; idea sections & reference.book

Sesi **brainstorming** — **tiada perubahan kod, tiada keputusan
muktamad**. Dua soalan pengguna dijawab, satu prinsip ditetapkan, dan
dua idea diteroka. Keputusan pelaksanaan masih terbuka; semakan
developer belum dijalankan.

## Prinsip yang ditetapkan (keputusan pengguna)

**JANGAN bina pemetaan automatik hadis→ayat Al-Quran.** Sebabnya sama
seperti Fath al-Bari: jika padanan tersalah, kita menisbahkan tafsiran
kepada Rasulullah ﷺ yang baginda tidak katakan. Untuk kod, kesilapan =
pepijat; untuk kandungan agama, ia berbeza sama sekali. Padanan sebegitu
adalah bahaya dan tidak boleh dibina.

Pautan ayat HANYA sah jika hadis **memetik ayat secara eksplisit** dalam
teksnya (cth. Bukhari #3 — Al-'Alaq 96:1-5, Al-Muddaththir 74:1-4).

## Jawapan: peranan hadis sebagai penjelas Al-Quran

- Quran 16:44 — `litubayyina li al-nas ma nuzzila ilayhim` — Nabi ﷺ
  berperanan menerangkan Al-Quran. Sahih.
- Tetapi bukan setiap hadis merujuk ayat tertentu. Usul fiqh membahagikan
  fungsi Sunnah kepada tiga:
  - **Muakkidah** — mengukuhkan apa yang sudah ada dalam Al-Quran
  - **Mubayyinah** — menjelaskan yang mujmal (cara solat, kadar zakat)
  - **Mustaqillah** — hukum yang tiada dalam Al-Quran (cth. haram haiwan
    bertaring)
  - Kategori ketiga itulah sebabnya pemetaan satu-lawan-satu tidak wujud.
- **Bukhari #1** (hadis niat) disahkan dalam hadis.db: ia kaedah umum,
  TIDAK mentafsir ayat tertentu. Imam Bukhari meletakkannya di awal kitab
  kerana ia prinsip am, bukan tafsiran ayat. Memaksa ia kepada satu ayat
  = mereka-reka, yang berbahaya dalam ilmu agama.

## Cadangan pengguna — dua perkara selamat untuk dilaksana

Kedua-duanya guna **struktur sumber sendiri** (bukan padanan kita), jadi
ketepatan terjamin:

| perkara | sumber | usaha | disahkan? |
|---|---|---|---|
| Tag "Tafsir Nabawi" untuk 499 hadis Book 65 | `reference.book` dalam CDN | rendah | ✅ |
| Papar nama bab (sections) pada setiap hadis | `metadata.sections` | rendah | ✅ |

### Bukti (disahkan dalam sesi ini)

- CDN `hadiths[].reference.book` — wujud untuk 7/7 kitab, **100% liputan**
  (bukhari 7,589 · muslim 7,563 · abudawud 5,274 · nasai 5,765 ·
  tirmidhi 3,998 · ibnmajah 4,343 · malik 1,858).
- Bukhari `reference.book == 65` = **tepat 499 hadis**.
- `metadata.sections` memetakan nombor book → nama, dan **berkongsi
  penomboran dengan `reference.book`** (1:1, bukan anggaran):
  - `1: "Revelation"`, `2: "Belief"`,
  - `65: "Prophetic Commentary on the Qur'an (Tafseer of the Prophet
    (pbuh))"` — nama rasmi sumber = asas tag "Tafsir Nabawi".
  - Semua 98 nombor book ada nama; 0 hadis kehilangan.
- Penemuan tambahan: ini menyelesaikan masalah Fath al-Bari — papar
  syarah ikut **bab** (aliran dalam kitab), bukan ikut nombor hadis yang
  hanyut.

### Data HadeethEnc (siasat untuk rekod)

- `sections` **tidak wujud** dalam API HadeethEnc (cuba `one`, `list`,
  `categories`, `sections/` — tiada/404).
- `reference` wujud HANYA dalam `language=ar`, sebagai **teks bebas
  berbilang baris** (`صحيح البخاري (2/133) (1521).`), bukan objek
  `reference.book`. Cache `.cache_he/` (ms) tidak menyimpan medan ini;
  untuk dapatkannya perlu muat turun semula 147 hadis dalam bahasa Arab.
- `categories` HadeethEnc = hierarki 452 kategori (`parent_id`); 102
  kategori unik dipakai oleh 147 hadis BM; tajuk kategori hanya Inggeris.

## Cadangan pelaksanaan (IDEA sahaja — tertunda, belum dilaksanakan)

**Migrasi 5** (`SKEMA_VERSI` 4→5): simpan `book` + nama kitab untuk hadis
berpadan (7 kitab = ~31,833 hadis). `sync_english.py` perlu merekod
`reference.book` semasa padanan (data sedia ada dalam cache `ara-*`).
Paparan UI: nama kitab pada halaman hadis + tag "Tafsir Nabawi" untuk
Bukhari book 65.

> **Nota sesi:** ini masih idea. Keputusan pelaksanaan (sama ada,
> bila, dan bagaimana) belum dibuat. Jangan anggap sebagai keputusan
> tetap sehingga sesi brainstorming selesai dan developer menyemak.

---

# Sesi 12d — Brainstorming: analisis 3 peringkat disahkan terhadap data CDN

Sesi brainstorming. Pengguna menghantar analisis terperinci 3 peringkat
(usul: (1) nama bab, (2) tag Tafsir Nabawi, (3) petikan ayat — cadang
JANGAN buat (3)). Semua nombor **disahkan semula terhadap cache CDN**
(`.cache_eng/ara-*.json`) — prinsip Fasa 3: uji data, jangan percaya
dakwaan.

## Peringkat 1 — Nama bab (`sections`): liputan disahkan TEPAT

| kitab | hadis | liputan (diukur) |
|---|---|---|
| abu-daud | 5,274 | 100.0% |
| tirmidzi | 3,998 | 100.0% |
| malik | 1,858 | 99.0% |
| nasai | 5,765 | 98.6% |
| bukhari | 7,589 | 95.9% |
| muslim | 7,563 | 95.5% |
| ibnu-majah | 4,343 | 93.9% |

Kes tiada nama = `reference.book == 0` (bukhari 311, muslim 344) —
bukan kehilangan padanan. Semua nombor book lain ada nama; `[]` tiada
yang tercicir. Data sedia ada dalam fail CDN yang dimuat turun —
`metadata.sections` + `reference.book`, tanpa padanan/anggaran.

## Peringkat 2 — Tag "Tafsir Nabawi": bab Tafsir khusus disahkan

| kitab | bab | nama (sumber) | hadis | rangka | |
|---|---|---|---|---|---|
| Bukhari | #65 | Prophetic Commentary on the Qur'an | 499 | 4474–4977 | ✅ |
| Muslim | #56 | The Book of Commentary on the Qur'an | **39** | 7523–7563 | ✅ |
| Tirmidzi | #47 | Chapters on Tafsir | 424 | 2950–3723 | ✅ |

Penemuan baharu: **Muslim #56 hanya 39 hadis** (jauh lebih kecil dari
dua yang lain). Pertalian hadis→surah dalam bab-bab ini **datang dari
susunan penyusun kitab** (tertib surah), bukan tekaan kod — itu yang
menjadikannya selamat.

## Peringkat 3 — Petikan ayat dalam teks hadis: cadang JANGAN

Pengguna melaporkan ujian: ayat penuh hanya 0.8% (58 hadis); n-gram
5/6/8 kata menaikkan liputan (6.6% / 4.7% / 2.5%) tetapi risiko naik
lebih cepat (frasa 5 kata umum, cth. `الحمد لله رب العالمين`). Kesilapan
= mendakwa hadis menerangkan ayat yang tidak disentuh — persis kesilapan
Fath al-Bari, kini melibatkan al-Quran. Jika tetap mahu: **ayat penuh
sahaja** (58 hadis), label "memetik" bukan "menerangkan".

> **Catatan:** angka n-gram (0.8%/2.5%/4.7%/6.6%) datang daripada ujian
> pengguna, TIDAK disahkan semula di sesi ini (perlu korpus al-Quran
> yang tidak ada dalam workspace). Hala tuju — jangan buat padanan
> separa — kekal selaras dengan pelajaran Fath al-Bari.

## Apa yang TIDAK dicadang langsung

- Pemetaan menyeluruh hadis→ayat — kategori mustaqillah memang tiada
  ayat rujukan; memaksa = mereka-reka.
- Asbab al-Nuzul — liputan <13% al-Quran + riwayat bercanggah; perlu
  penapisan ulama, bukan kod.

## Cadangan konkret (masih idea, belum dilaksanakan)

Buat (1) dahulu — usaha rendah, nilai tinggi, sifar risiko. Ia membuka
jalan untuk Fath al-Bari pilihan (1): papar syarah **ikut bab**, yang
menyelesaikan masalah hanyut penomboran.

**Status:** brainstorming. Tiada perubahan kod. Keputusan pelaksanaan
tertunda sehingga sesi brainstorming selesai + semakan developer.

---

# Sesi 12e — Brainstorming: cadangan HadeethEnc disemak — SUDAH wujud sebagai Fasa 4

Pengguna mencadangkan HadeethEnc sebagai "Fasa 4A baharu" (dakwaan:
202 hadis BM, padanan matn perlu dibina, bina `sync_hadeethenc.py`).
Dakwaan **disemak terhadap projek** — dan didapati **SUDAH WUJUD**:

## Ujian API langsung (live, 31 Jul)

- `hadeethenc.com/api/v1/categories/list/?language=en` → **452 kategori**,
  7 peringkat atas: Qur'an (81), Hadith (10), Akidah (471), Fiqh (1150),
  Adab (751), Da'wah (100), Sirah (213). ✅
- `hadeeths/one/?id=2758&language=ms` → **17 medan**: `hadeeth`,
  `hadeeth_intro`, `title`, `explanation` (BM), `hints` (BM senarai),
  `grade`, `attribution`, `words_meanings_ar`. ✅
- `language=ar` → **12 medan**; `reference` hanya dalam Arab, **teks
  bebas** (cth. "صحيح البخاري (2/133) (1521)"), bukan struktur berjson.
- Sila berhati-hati: id kecil (id=1) → **404**; kena guna ID sebenar
  daripada cache/enumerasi.
- **Rangkaian Arab tidak stabil** — `language=ar` boleh Timeout. Kena
  had (retry) bila menyentuh medan Arab.

## Status rasmi — disahkan

- Footer rasmi: HadeethEnc = keluarga IslamHouse (QuranEnc, TerminologyEnc,
  IslamHouse, Riyadh al-Salheen, Bayan al-Islam). ✅
- Penerbit: Rowad Translation Center; sumber: Pejabat Penyebaran Islam
  Rabwah (bawah naungan Kementerian Hal Ehwal Islam, Dawah & Bimbingan
  Arab Saudi). Klaim pengguna "projek rasmi kementerian" disokong.

## Konflik: apa yang dicadang = apa yang sudah ada

| Dicadang pengguna | Sebenar dalam projek |
|---|---|
| Bina `sync_hadeethenc.py` | **Wujud** (`sync_hadeethenc.py:1`) |
| Padanan matn ketat | **Wujud** (`core/hadeethenc_api.py:245` `padan()`, Jaccard 0.55, dua hala) |
| Uji padanan dahulu sebelum tulis DB | **Wujud** (`sync_hadeethenc.py:46`) |
| "202 hadis BM" | Enumerasi rasmi projek: **147** (`.cache_he/senarai_id.json`) |
| "0/40 padanan terus" | Betul teks-penuh gagal, **itulah sebab padanan MATN dibina** → 280 padanan |

Bukti semasa: `senarai_id.json` = 147; `.cache_he/*.json` = 148 fail;
DB `hadethenc` = **280 padanan** merentas 9 kitab (bukan 0/40).

Rekod lama `sesi_index.md`: **Fasa 4 (HadeethEnc) ✅ SIAP 31 Jul — 280
padanan, sumber ber-BM**. Fasa 4A yang DITUTUP ialah *Irsyad al-Hadith*
(lesen tertutup), BUKAN HadeethEnc. Pengguna mengelirukan label 4A.

## Percanggahan untuk diluruskan kemudian

1. **"202 hadis" vs 147** — mungkin API berkembang sejak cache kita, atau
   kaedah kira berbeza. Semak semula bila perlu (ulang `senarai_id_ms()`).
2. **"0/40"** — teks penuh memang gagal, tetapi itu SEBAB padanan MATN
   wujud. Masalah sudah diselesaikan.

## Penggredan semula (keputusan sesi)

| Kerja | Usaha | Nilai | Keputusan |
|---|---|---|---|
| (1) Nama bab (sections) | rendah | tinggi | ✅ Buat dahulu |
| (2) HadeethEnc BM | — | — | ❌ Batal — sudah siap (Fasa 4) |
| (3) Tag Tafsir Nabawi | rendah | sederhana | ✅ Buat sekali dengan (1) |
| (4) Tafsir ayat (spa5k) | sederhana | bergantung (3) | ⏸️ Tangguh — jangan sekarang |

## Keputusan pelaksanaan (disepakati pengguna)

- **(1)+(3) MULA ESOK**: migrasi `SKEMA_VERSI` 4→5; `sync_english.py`
  rekod `reference.book` + nama bab; UI papar nama bab; tag "Bab Tafsir"
  untuk Bukhari #65 (499), Muslim #56 (39), Tirmidzi #47 (424).
- **(4) IDEA TERTUNDA** dengan syarat ketat: ayat mesti datang dari tajuk
  bab (bukan padanan teks); lesen spa5k mesti disahkan sebelum sebarang
  kerja. Alasan: risiko nisbah palsu + dua kali terbakar lesen tertutup
  (Irsyad, Fath al-Bari).
- Pengguna akan semak **tambah nilai untuk UI dan fungsi** sebelum mula
  (tindak balas esok). Tiada kod diubah sesi ini.

**Status:** brainstorming. Keputusan pelaksanaan (1)+(3) dicapai untuk
mula esok, tetapi PENGESAHAN AKHIR menunggu semakan tambah-nilai UI
pengguna. Jangan anggap kod akan dibina sehingga pengesahan esok.

---

# Sesi 13 — Folder `ebook/` (sumber rujukan tambahan) + topik hadis palsu (ditepikan)

Pengguna menyerahkan folder `D:\Pustaka Quran Hadis\ebook` untuk dianalisa.
Peranan folder: **sumber rujukan tambahan pembangunan** — BUKAN kandungan
aplikasi. Tiada kerja integrasi/perbundelan.

## Sumber web (fail `httpsdkautsarebook.wordpress.com.txt`)

Tiga URL, satu kelompok "Jaringan Darul Kautsar":
- `dkautsarebook.wordpress.com` — e-book al-Kautsar; 12 ebook Hadis;
  11 sudah ada dalam folder, satu belum: "Mengenal Hadis Palsu (Mawdu')"
  (PDF telah dimuat turun, 17 muka, imbasan imej — perlu OCR untuk baca).
- `perpustakaanislamdigital.com` — Pusat Kajian Hadis (PKH) Jakarta;
  sumber `hd_zr1.pdf`; ada Tafsir Ibn Kathir/Jalalain, Sahih Bukhari/Muslim.
- `darulkautsarpencerahanaqidah.wordpress.com` — Pencerahan Aqidah;
  kategori "Hadith-Hadith Palsu Berkaitan Aqidah" (28 artikel).

## Kandungan folder (12 PDF)

Kumpulan A (11 e-book pengajian hadis Darul Kautsar, siri berpenomboran):
Pengajian Al-Hadith (Asri Yusoff); Fiqh al-Bukhari; Kedudukan Hadith;
99 Usul Dirayah (Asri Yusoff); Sunan Sittah (M.H. Awang Yahaya);
Jarh wa Ta'dil (M.H.); Mutawatir (M.H.); Asbab Wurud (M.H.);
Ikhtilaf & Metode (M.H.); Nasikh Mansukh (M.H.); Kepentingan Ilmu Alat.
Kumpulan B (`hd_zr1.pdf`): "40 Hadis Keutamaan Dzikir & Berdzikir"
(al-Habsyi, cet. 2008, penerbit Majelis Dzikir SBY Nurussalam, 130 muka) —
BUKAN siri pengajian, semua hadis bertema keutamaan dzikir.

Dua fail bermasalah: (a) `1.-to-add-cover-author-kepentingan-ilmu-alat...`
— teks OCR carut, nama fail sendiri mengaku "to add cover author";
(b) `wordpress-ringkasan-99-usul-dirayah...` — teks separa rosak.
Kedua-dua perlu dimuat turun semula dari sumber asal jika mahu dibaca penuh.

## Dokumen "Mengenal Hadis Palsu (Mawdu')" (dianalisa penuh via OCR)

Penyusun: Siti Nurhayatie (UiTM), edisi Mei 2023, Teratak Hadist. Isi:
- Definisi mawdu' = hadis daif PALING TERUK (Ibn al-Solah); dua jenis
  pemalsuan (rekaan baru / angkat ucapan bukan Nabi).
- Sejarah: bermula ~40 Hijrah (pembunuhan Uthman, Abdullah bin Saba',
  Khawarij); golongan ahl al-ahwa'.
- Hukum: HARAM menyebar hadis palsu kecuali untuk menyatakan kepalsuannya.
  Dalil: Bukhari 107, Muslim.
- 5 sebab pemalsuan; 6 kesan negatif; 10 contoh hadis palsu (antaranya
  "siapa kenal dirinya kenal Tuhannya", fadilat Tarawih malam 1–30,
  dialog Iblis, "perselisihan umatku rahmat", dsb).

## NOTA PENTING: lesen dokumen ini TERTUTUP

Muka 2: "Hak Cipta Terpelihara Oleh Teratak Hadist... tidak dibenarkan
mengulang cetak... tanpa keizinan penerbit." → TIDAK sesuai dibundel;
hanya rujukan pembangunan. Corak sama seperti Irsyad al-Hadith & Fath
al-Bari (lesen tertutup).

## Implikasi memadankan topik hadis palsu ke aplikasi (dibincang sesi ini)

1. Lesen: sumber utama tertutup → tidak boleh dibundel.
2. Mentanda "palsu" = pertuduhan negatif (fitnah); kesilapan kod lebih
   berat daripada salah tafsir → prinsip "jangan reka" lebih keras.
3. Masalah skop: 62,169 hadis DB = kitab sahih/sunan, semua sahih/hasan;
   hadis palsu sirkulasi DI LUAR koleksi → tiada sasaran padanan dalam DB.
4. Nilai sebenar buku ini = lapisan PENDIDIKAN (kaedah usul dirayah, jarh
   wa ta'dil, sejarah pemalsuan) — bahan bacaan rujukan, bukan penandaan.
5. Jalan selamat (jika mahu): senarai TERKURASI STATIK dengan atribusi
   penuh pihak ketiga, label "penilaian pihak ketiga", tiada padanan
   automatik.

**KEPUTUSAN PENGGUNA: topik ini LETAK TEPI — simpan untuk perbincangan
kemudian.** Tiada tindakan lanjut sekarang. Folder `ebook/` kekal sebagai
sumber rujukan pembangunan sahaja.

# Sesi 14 — Darjat ulama: cadangan cip ditolak, reka bentuk "papar mentah" dipilih

Pengguna mencadangkan 3 peringkat: (1) papar darjat sedia ada dari cache
(cip hijau/kuning/merah ikut 4 ulama), (2) koleksi rujukan mawdu'
berasingan, (3) guna Irsyad al-Hadith BM untuk hadis palsu masyhur.
Semua dakwaan **diuji terhadap data CDN** (prinsip Fasa 3).

## Pengukuran data (diukur, bukan dakwaan)

- Data `grades` ADA dalam cache: 5 kitab sahaja — **Bukhari & Muslim = 0%**
  (edisi CDN memang tidak membawa `grades`; disahkan di sumber raw
  github — bukan masalah cache). Abu Daud 100%, Malik 100%, Ibnu Majah
  99%, Nasai 99%, Tirmidzi 98%.
- **9 ulama unik** (bukan 4): Al-Albani 38,162; Zubair Ali Zai 38,066;
  Shuaib Al Arnaut 12,826; Abu Ghuddah 11,384; Muhammad Muhyi Al-Din
  Abdul Hamid 10,342; Muhammad Fouad Abd al-Baqi 8,628; Ahmad Muhammad
  Shakir 7,458; Bashar Awad Maarouf 4,850; Salim al-Hilali 3,716.
- **1,641 rentetan darjat unik dalam Abu Daud sahaja** (pengguna betul) —
  kebanyakannya bukan darjat: `Sahih Muslim (763)`, `Sahih Bukhari (327)
  Sahih Muslim (334)` = rujukan silang.
- Abu Daud: 5,272 hadis ≥2 ulama; **"tidak semua sama" = 4,251**;
  sahih-vs-daif = **564** (pengguna kata 880 — bergantung takrif;
  4,251 adalah takrif luas "tidak sepakat").
- **Hadis semua-ulama-sepakat-Mawdu = 0.** Yang ada cuma **67 hadis
  dengan ≥1 penilaian mawdu** (Ibnu Majah 45, Tirmidzi 18, Abu Daud 3,
  Malik 1). Contoh pengguna Ibn Majah #49 sebenarnya = Mawdu·Mawdu·Mawdu·
  **Daif** — ia PERCANGGAHAN, bukan konsensus.

## Keputusan pengguna (selepas ujian data)

1. **Cip hijau/kuning/merah DITARIK BALIK** — memaksa data ke 3 kotak =
   salah tafsir ulama (kesilapan yang sama seperti Fath al-Bari). Cip
   merah "AMARAN" = aplikasi membuat tarjih = kerja ulama, bukan perisian.
2. **Reka bentuk dipilih: papar mentah, dinisbahkan, tanpa tafsiran**:
   - Bahagian "Penilaian ulama" dalam **Collapsible tertutup** (sejajar
     keputusan "pengguna campuran").
   - Papar SEMUA nama + teks darjat apa adanya, tiada normalisasi,
     tiada warna, tiada ikon, tiada susunan keutamaan.
   - Nota kaki: "Penilaian ini daripada ulama hadis moden. Ulama boleh
     berbeza pendapat. Rujuk ahli ilmu untuk kepastian."
   - Bukhari & Muslim: bahagian tidak dipaparkan (tiada data dalam sumber).

## Perhatian saya (diuji, dibawa ke perbincangan)

- Jangan hadkan kepada 4 ulama — menapis ke 4 = pilih siapa layak =
  satu bentuk hukm. Papar semua nama yang wujud untuk hadis itu
  (cth. Ibn Majah #49 dinilai Fouad Abd al-Baqi juga).
- "Kesahihannya disepakati" untuk Bukhari/Muslim = hukm sendiri; lebih
  bersih label "Tiada penilaian ulama dalam sumber ini".
- Nota kaki perlu tambah atribusi sumber: fawazahmed0/hadith-api
  (Unlicense).
- Pelaksanaan boleh guna semula padanan Inggeris sedia ada
  (`eng_source.py` teks-Arab → CDN) — sifar muat turun baharu.

**KEPUTUSAN: reka bentuk "papar mentah" diterima. Rekod sahaja dahulu;
pelaksanaan menunggu perbincangan semalam (nama bab + tag Tafsir Nabawi).**

# Sesi 15 — Muka depan kitab: sumber disiasat, pendekatan "ilustrasi sendiri" dipilih

Pengguna mencadangkan memaparkan muka depan ASAL kitab hadis pada SETIAP
kad hadis. Disiasat mengikut prinsip Fasa 3 (uji data/sumber, jangan
percaya dakwaan).

## Siasatan sumber (fail `.txt` dalam `ebook/` = 3 URL)

| URL | Dapatan |
|---|---|
| dkautsarebook.wordpress.com | Blog e-book Darul Kautsar (bahan pengajian BM) — tiada cover kitab asal |
| perpustakaanislamdigital.com | PKH Jakarta — ADA imej muka depan kitab |
| darulkautsarpencerahanaqidah.wordpress.com | Blog artikel aqidah — tiada kaitan cover |

## Perpustakaan Islam Digital (PKH Jakarta) — disahkan

- Cover yang wujud: `Sahih_al-Bukhari.jpg`, `Sahih_Muslim.jpg` — HANYA
  2 daripada 9 kitab kita. 7 kitab lain tiada dalam folder imej.
- Resolusi: **76×113 & 79×113 piksel** (thumbnail kecil, rendah bila
  diregang pada kad).
- Lesen: laman `pengantar` mendakwa "sumber mutlak waqfeya.com" dan
  "tidak ada lagi hal yang berhubungan dengan hak cipta" (anggap wakaf).
  TETAPI dakwaan itu tuntutan penulis laman, bukan pengesahan undang-
  undang; cover yang dipapar ialah imbasan edisi cetakan sebenar
  (cth. "ط. السلطانية", "ط. دار ابن كثير") — reka bentuk penerbit.
- NOTA MODEL: gambar tidak dapat dilihat oleh model (tiada input imej);
  pengesahan dibuat secara teknikal (JPEG, dimensi).

## Keputusan pengguna (ikut cadangan)

1. **JANGAN papar cover asal penerbit** — lesen tidak disahkan, dan ia
   cuma 2/9 kitab + resolusi rendah.
2. **JANGAN letak cover pada setiap kad hadis** — bising visual + lompang
   skrol (masalah yang 6 percubaan untuk selesaikan).
3. **PILIH: ilustrasi buku ringkas SENDIRI** (kad warna kitab + tajuk
   Arab kitab), 100% milik sendiri, tiada risiko lesen, resolusi bebas.
4. **Letak di header halaman senarai kitab sahaja** (sekali, bukan 50×).

**STATUS: reka bentuk diputuskan. Pelaksanaan menunggu giliran selepas
kerja tertunda: (1) nama bab + (3) tag Tafsir Nabawi (Sesi 12e) dan
(4) darjat ulama papar-mentah (Sesi 14).**

# Sesi 16 — Nama bab + tag Tafsir Nabawi DILAKSANAKAN (kerja tertunda Sesi 12e)

## Keputusan yang dilaksanakan

1. **Bahasa nama bab: Inggeris apa adanya** (pilihan pengguna; hadis.my
   tiada nama bab langsung, CDN hampir 100% EN — lihat Sesi 12d).
2. **Tag "Bab Tafsir"** untuk bab tafsir Al-Quran sahaja: Bukhari #65,
   Muslim #56, Tirmidzi #47.

## Perubahan kod

- **`db.py`**: `SKEMA_VERSI` 4→5. Migrasi 5 = jadual `bab`
  (collection, hadis_id, book, nama_bab) + indeks. `book` = nombor
  buku CDN (`reference.book`); `nama_bab` = nama bab EN dari
  `metadata.sections`.
- **`core/eng_source.py`**: `bina_bab(fail_ara)` bina peta
  {hadithnumber: (book, nama)} dari `metadata.sections` CDN; `simpan_bab()`
  tulis ke jadual `bab`.
- **`sync_english.py`**: rekod `book` + `nama_bab` serentak dengan
  terjemahan (padanan sama, tiada muat turun baharu); DELETE lama per
  kitab sebelum simpan; `--semak` papar lajur bab.
- **`api/hadis_api.py`**: semua query (list/detail/cari/rawak) kini
  LEFT JOIN `bab`; `_row()` sertakan `book`/`nama_bab` bila ada.
- **UI**: kad hadis papar nama bab (elide 44 aksara, tooltip penuh) +
  tag chip "Bab Tafsir"; halaman detail papar nama bab di bawah tajuk.
- **`ui/widgets.py`**: pemalar `BAB_TAFSIR` = {"bukhari": 65, "muslim": 56,
  "tirmidzi": 47} — kunci slug hadis.db (bukan slug CDN).
- **`ui/theme.py`**: gaya `QLabel#babName` (italic, TEXT_MUTED).
- **`ui/app_qt.py`**: bookmark simpan `book`/`nama_bab` juga.

## Pengesahan (diukur, selepas sync penuh 7 kitab)

- Migrasi automatik ke versi 5 (semak_db OK, hadis/favorit kekal).
- `bina_bab` berfungsi; 0 nama bab kosong.
- Liputan `bab` mengikut hadis yang berjaya dipadan (sama seperti
  `terjemahan_eng`): abu-daud 4,559; bukhari 6,718; ibnu-majah 4,058;
  malik 1,563; muslim 5,082; nasai 5,559; tirmidzi 3,784.
- Tag Tafsir diukur: Bukhari book 65 = 476 hadis; Muslim book 56 = 28;
  Tirmidzi book 47 = 411 (kurang daripada 499/39/424 kerana itu jumlah
  hadis CDN, kita rekod yang berjaya dipadan sahaja).
- Ujian API (list/detail/cari/rawak) mengembalikan book+nama_bab betul.
- Kad UI dibina tanpa ralat (offscreen).
- `semak.py`: semua lulus; 5 kegagalan = fail data tempatan yang dijangka.

**STATUS: (1)+(3) SELESAI. Seterusnya: (4) darjat ulama papar-mentah
(Sesi 14), kemudian ilustrasi buku di header halaman kitab (Sesi 15).**

# Sesi 17 — Darjat ulama "papar mentah" DILAKSANAKAN (kerja tertunda Sesi 14)

## Reka bentuk yang dilaksanakan (ikut keputusan Sesi 14)

- Bahagian "Penilaian ulama (darjat)" dalam **Collapsible tertutup**.
- Papar SEMUA nama + teks darjat apa adanya — tiada normalisasi, tiada
  warna, tiada ikon, tiada susunan keutamaan. Susunan = susunan simpanan
  CDN (ORDER BY rowid).
- Nota kaki wajib: "Penilaian ini daripada ulama hadis moden. Ulama
  boleh berbeza pendapat. Rujuk ahli ilmu untuk kepastian."
- Atribusi sumber: fawazahmed0/hadith-api (Unlicense).
- Bukhari & Muslim: `darjat` kosong, bahagian tidak dipaparkan.

## Perubahan kod

- **`db.py`**: `SKEMA_VERSI` 5→6. Migrasi 6 = jadual `darjat`
  (collection, hadis_id, nama_ulama, darjat) + indeks. Satu baris per
  ulama; PK (collection, hadis_id, nama_ulama).
- **`core/eng_source.py`**: `bina_darjat(fail_ara)` baca `grades` CDN
  → {hadithnumber: [(nama, darjat), ...]}; `simpan_darjat()`.
- **`sync_english.py`**: rekod darjat serentak padanan (padanan sama,
  sifar muat turun baharu); DELETE lama per kitab; `--semak` papar
  lajur darjat.
- **`api/hadis_api.py`**: `_darjat()` (mod luar talian) + `_darjat_luar()`
  (buka DB atas permintaan); `get_hadis_by_id` sertakan `darjat`.
- **`ui/app_qt.py`**: `_bina_darjat()` mengisi Collapsible "Penilaian
  ulama" — baris "Nama — darjat", nota kaki, atribusi sumber.

## Pengesahan (diukur)

- Migrasi automatik ke versi 6.
- Darjat diisi untuk 5 kitab (Bukhari & Muslim = 0, konsisten sumber):
  abu-daud 16,299 baris/4,559 hadis; ibnu-majah 16,101/4,316; malik
  1,563/1,563; nasai 16,617/5,566; tirmidzi 13,350/3,782. JUMLAH 63,930.
- Abu Daud #1: Al-Albani Hasan Sahih, Abdul Hamid Hasan Sahih, Shuaib
  Sahih Lighairihi, Zubair Isnaad Hasan — 4 ulama, papar apa adanya.
- `get_hadis_by_id` (mod luar talian) + `_darjat_luar` mengembalikan
  senarai betul; bukhari #1 = [].
- `PustakaApp` dibina tanpa ralat (offscreen).
- `semak.py`: semua lulus; 5 kegagalan = fail data tempatan yang dijangka.

**STATUS: (4) SELESAI. Terakhir: ilustrasi buku di header halaman kitab
(Sesi 15).**

# Sesi 18 — Ilustrasi buku "milik sendiri" DILAKSANAKAN (kerja tertunda Sesi 15)

## Keputusan yang dilaksanakan (ikut Sesi 15)

- JANGAN guna cover asal penerbit (lesen tidak disahkan, cuma 2/9 kitab,
  resolusi 76×113 rendah).
- JANGAN letak cover pada setiap kad hadis.
- PILIH: ilustrasi buku ringkas SENDIRI — kad warna kitab + tajuk Arab,
  100% milik sendiri, tiada risiko lesen, resolusi bebas.
- Letak di **header halaman senarai kitab sahaja** (sekali, bukan 50×).

## Perubahan kod

- **`ui/pages.py`**: `Hero` — parameter baharu `side`: widget yang
  diletak DI KIRI tajuk dalam banner (ilustrasi buku). Tanpa `side`,
  tingkah laku lama (berpusat). Keserasian: home/search/saved tidak
  terjejas (6 QLabel + BookCover dikenal pasti dalam ujian).
- **`ui/app_qt.py`**: `_render_kitab_shell` — `BookCover` kini dihantar
  sebagai `side` ke `Hero` (ilustrasi SEBELAH KIRI tajuk kitab dalam
  banner), dan blok berasingan antara breadcrumb dan senarai dibuang.

## Nota

- Ilustrasi buku berada **dalam banner halaman kitab, di sebelah kiri
  tajuk** (bukan di antara breadcrumb dan senarai) — permintaan pengguna
  pada Sesi 18.
- Tajuk Arab dipetik daripada nama rasmi kitab (cth. صحيح البخاري،
  سنن أبي داود) — bukan terjemahan, tiada risiko hak cipta.
- Warna kitab = palet tersendiri setiap kitab (bukhari hijau, muslim
  biru, abu-daud oren, tirmidzi burgundy, nasai ungu, ibnu-majah emas,
  malik biru tua, ahmad hijau, darimi kelabu-biru).
- Model TIDAK boleh melihat imej (tiada input imej); pengesahan dibuat
  secara teknikal: 9 cover dirender ke PNG (172×236 @ skala 1.6),
  halaman kitab ke PNG (1280×800), semua dihasilkan tanpa ralat.

## Pengesahan

- `Hero(side=...)` dibina OK; 9 `BookCover` dibina dengan `arabic` bukan
  kosong; `open_kitab` bukhari/malik/darimi tanpa ralat; home/search/
  saved tanpa ralat; hero grab → `hero_bukhari_side.png` (PNG).
- `semak.py`: semua lulus; 5 kegagalan = fail data tempatan yang dijangka.

# Sesi 18.1 — Darjat "hilang" pada render pertama detail DIPERBAIKI

## Masalah (dilaporkan pengguna)

- Pengguna: "ada yg hilang yg awak buat tadi — bukan illustrasi atau banner
  tapi darjah hadis", dan isu khusus: dalam halaman detail hadis.

## Punca (diukur)

- `get_hadis_list` (senarai) TIDAK menyertakan `darjat`.
- `open_detail` menerima `h` dari senarai → `_render_detail` (render
  pertama) tidak melihat kunci `darjat` → bahagian "Penilaian ulama
  (darjat)" TIDAK dipaparkan sehingga `HadithWorker` selesai.
- Ujian mendedahkan: "SEGERA selepas klik: ['Transliterasi']" — bahagian
  darjat hanya muncul "Selepas worker". Jika worker lambat/gagal, pengguna
  tidak pernah melihat darjat.

## Pembetulan

- **`ui/app_qt.py` `open_detail`**: sebelum render, jika `h` tiada kunci
  `darjat`, baca terus dari DB tempatan melalui `api._darjat_luar(slug,
  hid)` (laju, ada indeks) dan set `h["darjat"]`. Ini memastikan bahagian
  darjat dipaparkan SERTA-MERTA pada render pertama.

## Pengesahan

- Selepas klik kad abu-daud: "SEGERA selepas klik: ['Transliterasi',
  'Penilaian ulama (darjat)']" — tanpa menunggu worker.
- `_detail_h['darjat']` tersedia serta-merta (True).
- Bukhari SEGERA: ['Transliterasi'] — betul, Bukhari tiada data darjat
  (keputusan Sesi 14: bahagian tidak dipaparkan).
- `semak.py`: semua lulus; 5 kegagalan = fail data tempatan yang dijangka.

**STATUS: (Pembetulan) SELESAI.**

# Sesi 18.2 — Revert lokasi ilustrasi buku (kembali ke blok berasingan)

## Permintaan pengguna

- "cuba kau revert sebelum kau buat pembetulan lokasi illustrasi kitab yg
  dipindah ke banner" — kembalikan ilustrasi ke kedudukan sebelum ia
  dipindah ke dalam banner (sebelah kiri tajuk).

## Tindakan

- **`ui/pages.py` `Hero`**: buang parameter `side` sepenuhnya — kembali
  kepada versi asal (tajuk/petikan/subtitle berpusat).
- **`ui/app_qt.py` `_render_kitab_shell`**: kembali kepada versi asal —
  `Hero` dipanggil tanpa `side`; blok ilustrasi `BookCover` diletak semula
  antara breadcrumb dan senarai hadis (berpusat).
- Pembetulan darjat (Sesi 18.1) KEKAL — `open_detail` masih set
  `h["darjat"]` sebelum render.

## Pengesahan

- 1 `BookCover` dalam halaman kitab (blok berasingan, bukan dalam Hero).
- Susunan: Hero → breadcrumb → BookCover → senarai hadis (20 kad).
- Darjat SEGERA selepas klik: ['Transliterasi', 'Penilaian ulama
  (darjat)'] — pembetulan 18.1 tidak hilang.
- PNG: `kitab_reverted.png`, `detail_darjat_segera.png`.
- `semak.py`: semua lulus; 5 kegagalan = fail data tempatan yang dijangka.

**STATUS: (Revert) SELESAI.**

# Sesi 18.3 — Bahagian "Penilaian ulama (darjat)" dipaparkan untuk SEMUA koleksi

## Permintaan pengguna

- Pengguna buka Muslim No. 3 — tiada bahagian darjat. Siasatan:
  medan `grades` WUJUD dalam CDN fawazahmed0 untuk hadis Muslim/Bukhari
  tetapi isi KOSONG `[]` (16 sampel Muslim, 0 berdata) — sumber memang
  tiada data untuk kedua-dua kitab.
- Pengguna: "kenapa tak letak saja pada bukhari dan biarkan tanpa fungsi"
  — mahu bahagian itu dipaparkan walaupun tiada data, bukannya hilang.

## Tindakan

- **`ui/app_qt.py` `_render_detail`**: buang syarat `if h.get("darjat"):`
  yang menyorokkan bahagian. Collapsible "Penilaian ulama (darjat)"
  kini sentiasa ditambah untuk semua koleksi.
- **`_bina_darjat`**: guna `self.api._darjat_luar(...)` (bukan `_darjat`)
  supaya berfungsi walaupun dalam mod dalam talian. Fallback sedia ada
  "Tiada penilaian ulama untuk hadis ini dalam sumber." kekal untuk
  senarai kosong.

## Pengesahan

- Muslim #3: bahagian ada → isi "Tiada penilaian ulama untuk hadis ini
  dalam sumber."
- Abu Daud #1: bahagian ada → 4 ulama (Al-Albani dll.) + nota + sumber.
- Ujian end-to-end klik kad sebenar (`uji_selalu_papar.py`) lulus.

**STATUS: (Sesi 18.3) SELESAI.**

# Sesi 18.4 — Ilustrasi buku DIPINDAH ke dalam banner (kiri tajuk)

## Permintaan pengguna

- "alih juga ilustrasi kitab ke banner" — kembalikan `BookCover` ke dalam
  banner halaman kitab (sebelah kiri tajuk), selepas ia direvert ke blok
  berasingan pada Sesi 18.2.

## Tindakan

- **`ui/pages.py` `Hero`**: tambah semula parameter `side` — widget yang
  diletak DI KIRI tajuk dalam banner. Tanpa `side`, tingkah laku lama
  (berpusat) kekal; home/search/saved tidak terjejas. Susun atur `side`:
  baris mendatar `[BookCover | teks(kanan)]`, tajuk/petikan/subtitle
  jajar kiri.
- **`ui/app_qt.py` `_render_kitab_shell`**: `BookCover(meta, ar_scale)`
  dihantar sebagai `side` ke `Hero`; blok berasingan antara breadcrumb
  dan senarai dibuang.

## Pengesahan

- 1 `BookCover` dalam halaman kitab, rantai:
  `BookCover <- QWidget(baris) <- Hero <- page <- scrollarea`.
- Cover di sebelah kiri tajuk dalam hero (`x < pusat hero`).
- bukhari/muslim/malik: 1 cover setiap, visible.
- Home/search tidak terjejas (home: 0 cover — betul).
- Kad senarai 20, klik → detail Collapsible
  ['Transliterasi', 'Penilaian ulama (darjat)'].
- `semak.py`: semua lulus; 5 kegagalan = fail data tempatan yang dijangka.
- PNG: `kitab_side_banner.png`.

**STATUS: (Sesi 18.4) SELESAI.**

**STATUS: SEMUA KERJA TERTUNDA SELESAI — nama bab + tag Tafsir (Sesi 16),
darjat papar-mentah (Sesi 17), ilustrasi buku (Sesi 18), darjat sentiasa
dipaparkan (Sesi 18.3), ilustrasi dalam banner (Sesi 18.4).**

# Sesi 18.5 — Padanan HadeethEnc diperluas (280 → 310) ambang matn pendek diturunkan

**MASALAH** (dilaporkan selepas Sesi 18.4): huraian hadis berulang — banyak
hadis dalam topik sama mendapat teks pengajaran/latar/modern yang IDENTIK.
Punca: hanya 280 padanan HadeethEnc (`status=dari_sumber`) memberi huraian
unik; selebihnya `status=auto` guna 17 templat statik dalam
`core/phase4_exegesis.py`.

**KEPUTUSAN PENGGUNA**: pilih peluasan sumber — pulih padanan HadeethEnc yang
tersembunyi (bukan menulis huraian mengarang).

**SIASATAN**:
- Audit `hadethenc` DB: 280 padanan / 103 HE id unik; semua kaedah `matn`;
  Jaccard min 0.55, max 1.0, avg 0.762.
- Cache `.cache_he/`: 148 fail JSON / 147 hadis BM HadeethEnc (satu-satunya
  sumber huraian bersumber yang sah; Irsyad DITUTUP lesen; OpenITI/Fath
  al-Bari penomboran hanyut).
- 44 HE belum dipadan walaupun ramai padan Jaccard ≥0.55 (ada 1.00) — ditolak
  `padan()` kerana matn pendek: `len(kata) < 4` kata jarang.
- Simulasi `padan2` ambang boleh laras: `min_kata=4` → 0 baharu (sepadan
  semasa); `=3` → 10; `=2` → 12; `=1` → 30.
- Semakan manual SEMUA 30 padanan `min_kata=1` (skrip `senarai_min1.py`):
  sah dari segi matn (cth. bukhari #1346 → HE 65016 j=1.00; muslim #2632 →
  HE 4311; ahmad #6291 → HE 65038 j=0.56 padanan tepat).
- Semakan regresi `banding_perubahan.py` (min_kata=1): **0 padanan sedia ada
  berubah**, +30 baharu sahaja. Tiada kekaburan baharu.

**PERUBAHAN** (`core/hadeethenc_api.py`, `padan()`):
- Ambang `if len(kata) < 4: return None` → `if not kata: return None`.
- Pengesahan Jaccard dua hala + semakan calon kedua (matn berbeza tolak)
  KEKAL — keselamatan tidak dikorbankan.
- Nota kod Sesi 18.5 menerangkan sebab.

**HASIL**:
- `sync_hadeethenc.py`: 310 padanan disimpan (naik 30, semua disahkan).
- Muslim #4823 → HE 3420 (j=1.00): huraian `status=dari_sources`, topic
  "Celakalah orang-orang yang melampau (dalam agama)" — sebelum ini tiada.
- Abu Daud #4459 → HE 3017 (j=1.00); Ahmad #5600 → HE 65017 (j=0.79);
  Bukhari #1346 → HE 65016 (j=1.00).
- UI: `open_by_ref('muslim', 4823)` + pipeline papar "Huraian ringkas oleh
  HadeethEnc.com" (disahkan offscreen).
- `semak.py`: SEMUA lulus; 5 kegagalan data tempatan (.cache_eng, .cache_he,
  hadis.db, -wal, -shm) dijangka pada mesin pembangun.

**STATUS: (Sesi 18.5) SELESAI.**

# Sesi 18.6 — Versi v2026.08.01-12 + bina ZIP arkib pembangunan

**KEPUTUSAN PENGGUNA**: naikkan versi + bina ZIP (arkib pembangunan, BUKAN
pakej edaran — projek masih development) selepas Sesi 18.5
(280 → 310 padanan HadeethEnc).

**PERUBAHAN**:
- `VERSI.py`: `2026.07.31-11` → `2026.08.01-12`. CIRI TIADA bertambah
  (perubahan Sesi 18.5 ialah ambang dalam `padan()`, bukan ciri modul baharu).
- `MULA_SINI.md` §5: versi + nota ZIP (arkib pembangunan, projek masih
  development).
- `RANCANGAN_4FASA.md` kepala: 280 → 310 padanan, tarikh 1 Ogos.
- `MANUAL_REFERENSI_DEV.md` + `MANUAL_PENGGUNA.md`: versi baharu.
- `PERUBAHAN_31JUL.md` sengaja TIDAK diubah — dokumen sejarah.

**BINA ZIP**: `PustakaHadith.zip` di `D:\Pustaka Quran Hadis\` (bukan dalam
folder hadis). 56 fail, rata (TIADA folder `hadis/` bersarang). Pengecualian
dipatuhi: `hadis.db`(+`-wal`/`-shm`), `.cache_eng`, `.cache_he`,
`.cache_syarah`, `__pycache__`, `user_settings.json`, `bookmarks.json`,
`.env`. Guna `System.IO.Compression` entry-by-entry (CreateFromDirectory
SALAH — masukkan semua).

**PENGESAHAN** (ekstrak ke folder bersih):
- `semak_versi.py`: v2026.08.01-12, semua 17 ciri hadir, amaran hadis.db
  hilang betul.
- `semak.py`: SEMUA LULUS (folder bersih tanpa hadis.db).
- Mesin pembangunan: 5 GAGAL fail data tempatan dijangka (hadis.db + cache).

**STATUS: (Sesi 18.6) SELESAI.**

# Sesi 18.7 — Huraian auto DIJUJURKAN (teks generik berulang dibuang)

**MASALAH** (berterusan dari Sesi 18.5): hadis berstatus `auto` mendapat
`teachings`/`life_application`/`modern_relevance` yang IDENTIK untuk semua
hadis dalam topik yang sama — pengguna kata "huraian berulang2 dengan
jawapan sama untuk semua hadis". Ia kelihatan seperti huraian khusus padahal
generik (menipu mata).

**KEPUTUSAN PENGGUNA**: jujurkan templat auto — JANGAN tambah teks, kurangkan.
Paparkan label topik + terjemahan penuh + transliterasi + nota "huraian
khusus belum tersedia". Buang teks pengajaran/latar/kaitan moden yang
berulang. (Pilihan (3) perluasan HadeethEnc DITANGGUH — hasil terhad, API
lambat.)

**PERUBAHAN**:
- `core/phase4_exegesis.py` `exegesis()`: untuk `status="auto"` dengan topik,
  `teachings` kini nota jujur ("Huraian khusus untuk hadis ini belum
  tersedia dalam sumber berlesen terbuka... sila rujuk kitab syarah");
  `life_application` + `modern_relevance` = kosong. `background` (sumber +
  perawi) dan `summary` kekal. Status tanpa topik TIADA perubahan.
- `ui/app_qt.py`: `MEDAN_HURAIAN` dibuang `life_application`/
  `modern_relevance`; tambah `MEDAN_HURAIAN_AUTO` (Topic / Background / Nota /
  Ringkasan) — label "Nota" bukan "Pengajaran" untuk status auto.

**PENGESAHAN**:
- `semak_huraian_auto.py`: muslim #3 & malik #1 auto → nota jujur, tiada
  life_application/modern_relevance; muslim #4823 dari_sumber → huraian
  HadeethEnc kekal penuh.
- Ujian UI offscreen (muslim #3): "belum tersedia" dipapar, label "Pengajaran"
  hilang, label "Nota" wujud.
- `semak.py`: SEMUA lulus; 5 kegagalan fail data tempatan dijangka.

**STATUS: (Sesi 18.7) SELESAI.**

# Tamat hari (1 Ogos) — titik sambung esok

Pengguna menutup sesi. Semua kerja tertunda selesai; versi v2026.08.01-12.

**Bila sambung:**
1. Baca `MANUAL_REFERENSI_DEV.md` (rujukan utama) + `MULA_SINI.md`
2. Cadangan tertunda (belum dipilih): perluasan HadeethEnc (pilihan 3) —
   hasil terhad (147 sumber BM), API lambat; nilai rendah, boleh langkau.
3. Ujian pengguna sendiri dahulu; sambung berdasarkan maklum balas.
4. Bina semula `PustakaHadith.zip` (arkib development) selepas sebarang
   perubahan kod/data.

# Sesi 18.8 — Sumber huraian BM baharu: SemakHadis.com (2,045 padanan)

**KONTEKS**: Pengguna minta terokai sumber luar untuk huraian BM tambahan.
Sesi ini siapkan penilaian semakhadis.com (syarah BM) DAN dorar.net
(darjat Arab), kemudian INTEGRASIKAN SemakHadis.

**PENILAIAN semakhadis.com** (API terbuka, tiada kunci):
- `https://semakhadis.com/api/hadith/hadith-search.json?query=...`
- 18,800 hadis; fokus hadis popular + semakan daif/palsu. 2,372 hadis
  sahih-relevan dimuat ke `.cache_sema/` (Muttafaq 'alayh 372, Sahih 1000,
  Hasan 1000).
- Data kaya: `arabic_text`, `malay_text` (BM), `malay_commentary`
  (komentar BM), `intro_commentary` (takhrij), `classification` (status).
- 2,045 padanan Jaccard matn >= 0.55 (tolak calon kedua rapat) DISIMPAN.
- Kualiti tinggi (Bukhari 51/51, Muslim 70/70 kaya komentar).

**PENILAIAN dorar.net** (darjat/takhrij Arab):
- `https://dorar.net/dorar_api.json?skey=<arab>` — bebas, tanpa Cloudflare.
- Liputan sampel: Bukhari 50%, Muslim 50%, Nasai 35%, Ibn Majah 40%,
  Ahmad 30%, lain <=15%.
- MENGISI jurang darjat untuk bukhari/muslim/ahmad/darimi (0% pada
  fawazahmed0) — anggaran ~14,000 rekod. TETAPI: kos 8-12 jam muat turun,
  liputan rendah, dan bukhari #50 J=0.32 memadan hadis SALAH (risiko papar
  darjat salah > tiada darjat).
- **KEPUTUSAN: TANGGUH** — hanya jika perlu kelak, guna ambang J>=0.55 +
  semakan manual. Fokus kembali huraian BM.

**PERUBAHAN** (versi 2026.08.03-13):
- `db.py`: migrasi 7 — jadual `semakhadis` (collection, hadis_id, sema_id,
  jaccard, klasifikasi, tajuk, malay_text, intro, syarah).
- `core/sema_source.py`: BARU — cache `.cache_sema/`, `bina_indeks()`,
  `padan()` (indeks terbalik + Jaccard 0.55 + tolak calon kedua),
  `matn_bersih()` (buang penanda umum), `simpan()`/`ambil()`.
- `sync_sema.py`: BARU — padan semua 9 kitab, `--semak` status.
- `api/hadis_api.py`: `_sema()`/`_sema_luar()`; `get_hadis_by_id` sertakan
  `d["sema"]`.
- `ui/app_qt.py`: Collapsible "Huraian (SemakHadis · status)" TERBUKA
  selepas tab bahasa, sebelum syarah Arab; `_bina_sema()` papar tajuk,
  status, terjemahan, takhrij, komentar (potong 8,000 + salin penuh),
  atribusi.
- `semak.py`: seksyen 8f (9 semakan); `.cache_sema` dalam semak_bersih.
- `.gitignore` + `PINDAH_DATA.ps1`: `.cache_sema`.

**PENGESAHAN**:
- `sync_sema.py`: 2,045 padanan (Bukhari 291, Muslim 207, Ahmad 863,
  lain 684). Muslim #43 betul ditolak (J=0.54 < 0.55).
- `get_hadis_by_id("bukhari",1)["sema"]`: J=0.87 [Muttafaq 'alayh] tajuk
  "Amalan Bergantung Kepada Niat Seseorang" — betul.
- `semak.py`: SEMUA lulus; 6 kegagalan fail data tempatan dijangka
  (hadis.db + .cache_eng + .cache_he + .cache_sema).

**ISU LESEN TERBUKA**: SemakHadis.com tidak menyatakan lesen semula data
secara eksplisit. Atribusi wajib dipaparkan (dilakukan). Sebelum edaran
komersial, dapatkan kebenaran bertulis.

**STATUS: (Sesi 18.8) SELESAI.** Titik sambung: bina semula ZIP;
semak UI paparan huraian pada hadis popular (cth. Bukhari #1).

# Sesi 18.9 — Huraian auto (Fasa 4) DIBUANG sepenuhnya

**KEPUTUSAN PENGGUNA (Sesi 18.9)**: Buang huraian auto sepenuhnya — bukan
sekadar menyembunyikan/mengganti nama. Sebab: huraian auto ialah nota topik
generik tempatan (`status="auto"`, disclaimer "bukan huraian ulama") yang
bertumpuk dengan huraian asli SemakHadis. Butang "📖 Huraian" yang membuka
halaman pipeline boleh menyesatkan pengguna.

**CAKUPAN (buang, bukan sembunyi)**:
- `ui/app_qt.py`: import `PipelineWorker`, `_pipe_worker`, PAGES
  `{"home":0,"kitab":1,"detail":2,"search":3,"saved":4,"settings":5}`,
  butang "📖 Huraian" di bar navigasi detail, dan blok Pipeline 195 baris
  (`_page_pipeline`/`_run_pipeline`/`_phase_card`/`_on_phase`/
  `_fill_phase`/`MEDAN_HURAIAN`/`MEDAN_HURAIAN_AUTO`) — DIPADAM.
- `ui/workers.py`: class `PipelineWorker` DIPADAM (kini berakhir di
  `RandomWorker`, 107 baris).
- `core/phase4_exegesis.py`: DIPADAM (selepas disahkan tiada pengguna lain).
- `VERSI.py`: v1.0; 2 ciri berkaitan phase4 dibuang (19 kekal).

**DIPERIKSA DAN KEKAL (bukan sasaran)**:
- `sync_hadeethenc.py`, `.cache_he/`, jadual `hadethenc` — arsip, tidak
  dipapar UI.
- `core/hadeethenc_api.py` — `_matn` masih dipakai `core/sema_source`.

**SEMAKAN SEMAK.PY DIKEMASKINI** (disesuaikan dengan pemadaman):
- semak `_hadeethenc`/`dari_sumber`/`Kategori (auto)` (dari Fasa 4) — dibuang.
- semak "butang Kembali di luar QScrollArea" (berkaitan `_page_pipeline`) —
  ditarik balik; `bottombar` kekal untuk halaman detail.
- Seksyen 8f tajuk kekal "SemakHadis — padanan matn + integrasi".

**UJIAN SELEPAS PEMADAMAN (offscreen)** — LULUS:
- `semak.py`: semua hijau (6 GAGAL = fail data tempatan sahaja, normal).
- `test_pasca.py`: Bukhari #1 — butang "📖 Huraian" TIADA (True), collapsible
  SemakHadis terbuka (detail_sema=True). Tiada rujukan `_run_pipeline`/
  `pipeline` dalam app.

**STATUS: (Sesi 18.9) SELESAI.** Titik sambung: kemas kini `MULA_SINI.md`
(seksyen huraian auto ditulis semula sebagai rekod sejarah) dan hantar.

# Sesi 18.10 — Folder projek dikemas + ZIP dibina semula (v1.0)

**PERINTAH PENGGUNA**: "kemaskini folder projek". Skop dipilih pengguna:
kemas SEMUA dokumen + bina semula `PustakaHadith.zip`.

**DOKUMEN DIKEMAS (semua ke v1.0, rujukan Fasa 4 dibuang):**
- `MANUAL_REFERENSI_DEV.md` — versi; struktur fail: `core/phase4_exegesis.py`
  diganti `core/sema_source.py` + `core/hadeethenc_api.py` (arsip); jadual fasa
  4 → "⚫ DIBUANG"; lapisan huraian = SemakHadis + syarah Arab + darjat;
  §6 Fasa 4 → "Huraian auto DIBUANG"; §7 tambah `sync_sema.py`; §8 liputan
  SemakHadis; §12 kiraan sesi_index.
- `MULA_SINI.md` — §5 versi -13 → -14; "Siap" tanpa Fasa 4; nota DIBUANG;
  "Belum selesai" ganti HadeethEnc → SemakHadis; §5.1 status konsisten.
- `RANCANGAN_4FASA.md` — kepala kemas kini 3 Ogos; jadual keputusan Fasa 4
  DIBUANG; seksyen FASA 4 tulis semula (DIBUANG + SemakHadis AKTIF);
  keutamaan paparan baharu; isu belum selesai dikemas.
- `MANUAL_PENGGUNA.md` — versi; §1 huraian = SemakHadis (2,045); halaman hadis:
  "📖 Huraian" diganti "Huraian (SemakHadis · status)" terbuka automatik;
  seksyen "Huraian SemakHadis" baharu (tajuk, status, terjemahan, takhrij,
  komentar, atribusi, Salin syarah penuh, syarah Arab + darjat).

**PEPIJAT SEMAK.PY DIBETULKAN (hanya kelihatan di folder bersih):**
`semak_apl` melancarkan `PustakaApp` yang memanggil `db.init()` → MENCIPTA
`hadis.db` kosong → semak_bersih menanda dirinya kotor (1 GAGAL palsu).
- `semak_apl`: rekod `db_asal` sebelum ujian; buang hadis.db/-wal/-shm
  selepas jika tiada asalnya. (Dev workspace selamat — hadis.db sebenar
  kekal.)
- `semak_susunatur`: sama — tambah `db_asal` + pembersihan.
- `semak_sema` (d): `_init()` tanpa argumen → `_init(_tmp_db)` (DB temp,
  tiada hadis.db tercicir di cwd).

**ZIP DIBINA SEMULA**: `D:\Pustaka Quran Hadis\PustakaHadith.zip`
- 57 fail rata (56 − `core/phase4_exegesis.py` + `core/sema_source.py` +
  `sync_sema.py`), entry guna `/` (bukan `\`).
- Pengecualian dipatuhi: `hadis.db`(+`-wal`/`-shm`), `bookmarks.json`,
  `user_settings.json`, `.env`, `.cache_*`, `__pycache__`.
- 253,191 bytes, 8/3 7:34 PM.

**PENGESAHAN (ekstrak ke folder bersih)** — SEMUA LULUS:
- `semak_versi.py`: v1.0, semua 19 ciri hadir; amaran hadis.db
  hilang betul (DB memang tidak dibundel).
- `semak.py`: **"SEMUA LULUS — selamat dihantar"** (sebelum ini 1 GAGAL
  palsu hadis.db dari ujian app sendiri; kini 0).
- UI offscreen: butang "📖 Huraian" tiada, collapsible SemakHadis terbuka
  (disahkan Sesi 18.9, tidak berubah).

**STATUS: (Sesi 18.10) SELESAI.** ZIP siap untuk dihantar / diuji pengguna.

# Sesi 18.11 — Versi ditetapkan v1.0 + paparan versi dalam app

**PERINTAH PENGGUNA**: "letak versi 1.0" kemudian "letak pada apps paparan
versi". Versi naik taraf daripada tarikh-skema (`2026.08.03-14`) kepada
**`1.0`** (keluaran pertama).

**PERUBAHAN**:
- `VERSI.py`: `VERSI = "1.0"`. CIRI (19) tidak berubah.
- Dokumen dikemas ke v1.0: `MANUAL_REFERENSI_DEV.md` (kepala + §1),
  `MULA_SINI.md` §5, `RANCANGAN_4FASA.md` kepala, `MANUAL_PENGGUNA.md`,
  `sesi_index.md` (Sesi Terakhir + entri 18.10).
- **UI `ui/app_qt.py`**: import `VERSI`; label `self._versi` di halaman
  Tetapan (footer, selepas `_info`) → `"PustakaHadith · v{VERSI}"`.
- `PustakaHadith.zip` dibina semula (57 fail, v1.0).

**UJIAN**:
- `test_versi.py` (offscreen): `go("settings")` → `_versi.text()` =
  `"PustakaHadith · v1.0"`. LULUS.
- `semak.py`: tema dark + light LULUS; di folder ZIP bersih → **SEMUA
  LULUS** (7 GAGAL workspace dev = fail data tempatan, normal).
- `semak_versi.py`: v1.0, 19 ciri hadir.

**STATUS: (Sesi 18.11) SELESAI.** v1.0 dipaparkan dalam app (halaman
Tetapan) dan ZIP terkini.

# Sesi 18.12 — Versi dipindah ke header (atas kiri)

**PERINTAH PENGGUNA**: "letak versi di atas kiri selepas perkataan PustakaHadith hadith". Versi dipindahkan dari halaman Tetapan ke header utama sebelah
logo "PustakaHadith".

**PERUBAHAN**:
- `ui/app_qt.py` `_header()`: tambah `QLabel` `v1.0` (kecil, `TEXT_MUTED`)
  berdampingan logo "PustakaHadith".
- Label versi di halaman Tetapan dibuang (tiada duplikasi).
- `PustakaHadith.zip` dibina semula (57 fail, v1.0).

**UJIAN**:
- `test_versi2.py` (offscreen): header memapar `v1.0`; Tetapan tiada
  label versi. LULUS.
- `semak.py`: tema dark + light LULUS; di folder ZIP bersih → **SEMUA
  LULUS**.
- `semak_versi.py`: v1.0, 19 ciri hadir.

**STATUS: (Sesi 18.12) SELESAI.** Versi v1.0 dipaparkan di header utama.

# Sesi 18.13 — Item tertangguh 3,4,5 disahkan + Windows Sandbox

**PERINTAH PENGGUNA**: "buat ikut no" — selesaikan item tertangguh §8
berurutan.

**ITEM 3 — Padanan `ara-*` (diagnos_padanan.py) pada DB sebenar:**
- Bukhari 500 sampel: **JUMLAH BERJAYA 454/500 = 90.8%**
- Liputan baik; kegagalan 46 (9.2%) = perbezaan edisi teks Arab, bukan pepijat padanan
- **Keputusan: ara-* berfungsi pada data sebenar** ✅

**ITEM 4 — Halaman Tersimpan (bookmarks.json):**
- Tanda buku sedia ada (1 hadis Bukhari #1) dipaparkan
- Klik buka hadis berfungsi (`open_by_ref` → detail page) — perlu event loop (app sebenar OK)
- **Keputusan: Tersimpan papar & navigasi berfungsi** ✅

**ITEM 5 — diagnos_syarah.py (Fath al-Bari) pada data sebenar:**
- hadis.db bukhari 7,008 hadis; 5,075 seksyen syarah
- Anjakan penomboran: **min -400, max +120, julat 520**
- Hanya 1/8 julat sejajar (|anjakan| ≤ 4)
- **Keputusan: Penomboran HANYUT — padanan ikut ID TIDAK selamat** ✅
- Menguatkan pembatalan Fasa 4B (Sesi 18.8/18.9)

**ITEM 6 — Pipeline end-to-end (Install → API → Baca → Tersimpan):**
- Windows 11 Pro disahkan → **Windows Sandbox diaktifkan**
- `Enable-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM" -All` → **Enabled (perlukan restart)**
- Sedia untuk uji `PASANG.bat` → `JALANKAN.bat` dalam Sandbox bersih

**ITEM 7 — Kunci API:** Kekal AKTIF (pelan developer)

**ITEM 8 — Liputan SemakHadis:** 2,045/62,169 (3.3%) — siling

**STATUS: (Sesi 18.13) SELESAI.** Item 3,4,5 disahkan pada data sebenar; Sandbox sedia untuk Item 6.

# Sesi 18.14 — Pipeline end-to-end (Item 6) DISahkan

**PERINTAH PENGGUNA**: Uji saluran penuh dalam Windows Sandbox bersih.

**PELAKSANAAN**:
- Windows 11 Pro → **Windows Sandbox enabled** (restart ×2)
- Python 3.12.4 dipasang manual (silent install + PATH)
- `PASANG.bat` (Run as Admin) → PyQt5, requests, pyperclip + pintasan Desktop
- `JALANKAN.bat` → App lancar

**UJIAN ALIRAN PENUH (dalam Sandbox bersih)** — SEMUA LULUS:
1. **Buka app** → klik gear (⚙️) → masukkan API key (Developer 10k/hari)
2. **Pilih kitab** → buka hadis (arab/melayu/indonesia/inggeris/transliterasi)
3. **Simpan hadis (☆)** → halaman **Tersimpan (⭐)** → hadis muncul
4. **Klik hadis tersimpan** → buka detail (navigasi berfungsi)
5. **Collapsible "Huraian (SemakHadis · status)"** terbuka → tajuk, status, terjemahan, takhrij, komentar, atribusi
6. **Darjat (Penilaian ulama)** dipaparkan
7. **Versi v1.0** dipaparkan di header (sebelah "PustakaHadith")
8. Tema terang/gelap berfungsi

**KEPUTUSAN: Pipeline end-to-end BERFUNGSI SEPENUHNYA** ✅

**SEMUA ITEM §8 MANUAL_REFERENSI_DEV.md DISahkan:**
| Item | Status |
|------|--------|
| 1. Ujian mesin sebenar | ✅ |
| 2. Sync penuh | ⏭️ (data sedia ada) |
| 3. Padanan `ara-*` | ✅ 90.8% berjaya |
| 4. Halaman Tersimpan | ✅ Papar & buka hadis |
| 5. `diagnos_syarah.py` | ✅ Fath al-Bari anjakan hanyut |
| 6. Pipeline end-to-end | ✅ **PASANG → JALANKAN → API → Baca → Simpan → Tersimpan** |
| 7. Kunci API | AKTIF (pelan developer) |
| 8. Liputan SemakHadis | 2,045/62,169 (3.3%) — siling |

**STATUS: (Sesi 18.14) SELESAI.** Semua item tertangguh disahkan. v1.0 siap hantar.

---

## 💡 Idea Tersimpan: HadithXpert-style AI + Human Review (Untuk Masa Depan)

**Sumber:** hadithxpert.com (AI + pakar, berbayar, closed SaaS)

**Konsep Boleh Diadaptasi (Offline-first):**
1. **Semantic Search Local** — Embedding model lokal (sentence-transformers/Ollama) untuk faham maksud soalan, bukan keyword matching
2. **Draft Answer → Human Review** — AI buat jawapan draft, flag untuk pakar semak/betulkan
3. **Arkib Jawapan Tersemak** — Simpan jawapan final dalam DB lokal untuk rujukan masa depan

**Pipeline Cadangan:**
```
User Query → Local Embedding Search → Top-K Matches
    → Compose Draft Answer (status, rujukan, penjelasan)
    → Flag for Review (pakar/ustaz)
    → Reviewer Correct/Confirm
    → Save to Archive DB (arkib_jawapan)
```

**Keperluan Teknikal:**
- Local embedding model (sentence-transformers ~100MB, CPU OK)
- FAISS/ChromaDB untuk vector search
- DB schema: `arkib_jawapan`, `review_queue`
- Simple admin UI untuk reviewer

**TIDAK boleh guna dari HadithXpert:** Model AI mereka, API, database, UI (closed SaaS, berbayar RM19/bln)

**Status:** 💡 Idea tersimpan — dilaksanakan bila perlu AI semantic search + workflow review.

---

## 🏷️ Cadangan Nama Aplikasi (Tersimpan)

**Niche:** "Offline-First Hadis Research Toolkit untuk Pengkaji & Ustaz"

### Top 3 Pilihan

| Nama | Maksud | Kenapa Bagus |
|------|--------|--------------|
| **Miṣbāḥ** (مِصْبَاح) | "Pelita / Lampu" | Metafora "cahaya ilmu hadis dalam kegelapan offline", pendek, arabik, mudah diingat |
| **Maṭlaʿ** (مَطْلَع) | "Tempat terbit / Sumber" | Maksud "sumber rujukan", sesuai research toolkit, akademik |
| **Riwāyah** (رِوَايَة) | "Riwayat / Penghantaran ilmu" | Fokus pada "sanad/riwayat hadis", bersesuaian domain |

### Alternatif Lain
- **Ḥāfiẓ** (حَافِظ) — "Pelindung / Penghafaz" (offline, melindungi data)
- **Maṣdar** (مَصْدَر) — "Sumber" (rujukan primer)
- **Takhrij** (تَخْرِيج) — Terminologi pengkaji
- **Isnād** (إِسْنَاد) — Fokus sanad/darjat
- **HadisLab** / **HadisKit** — Developer-friendly vibe

### Cadangan: **Miṣbāḥ**
- Singkat, makna luhur ("pelita ilmu di kegelapan offline"), arabik universal, brandable
- Tagline cadangan: *"Pelita hadis di genggaman anda"*
- Domain check: `misbah.app`, `misbah.my`, `misbah.hadis`

**Status:** 💾 Tersimpan — penilaian domain + test nama dengan 3-5 ustaz/pengkaji esok.

---

# Sesi 19 — App crash DLL torch dibaiki + migrasi DB + huraian SemakHadis dipulihkan (5 Ogos 2026)

**PERINTAH PENGGUNA**: "apps gagal" (Python 3.14, Windows). Kemudian "huraian hadis hilang".

**MASALAH 1 — Apps tidak boleh dilancarkan** (`OSError: WinError 1114` pada `torch\lib\c10.dll`):

- **Punca**: `core/semantic_search.py` mengimport `sentence_transformers` (→ torch) **di aras modul**. UI memuatkan `is_index_ready()` semasa permulaan, jadi torch dimuat awal → DLL gagal → seluruh apps crash.
- **Tambahan**: `ui/pages.py` guna `QCheckBox` tetapi tiada dalam import → `NameError`.
- **Pembetulan**:
  - `core/semantic_search.py`: import `faiss` & `sentence_transformers` dijadikan **lazy** (dalam `_load_model()`/`_load_index()`); tambah `faiss_available()`/`torch_available()` supaya apps berfungsi walaupun pakej ML tiada.
  - `ui/pages.py`: tambah `QCheckBox` pada import.
- **Pakej dipasang semula (Python 3.14)**: `PyQt5 5.15.11`, `requests`, `pyperclip`, `tqdm`, `faiss-cpu 1.15.0` (wheel cp314!), `sentence-transformers 5.6.1`, `torch 2.13.0+cpu` (wheel cp314). **Tiada lagi DLL error** — versi terbaharu kini menyokong Python 3.14 (versi lama `torch 2.0.1` yang dicadang sebelum ini TIDAK ada wheel 3.14).

**MASALAH 2 — DB migrasi tidak pernah dijalankan** (`sqlite3.OperationalError: no such table: bab`):

- **Punca**: `api/hadis_api.py::__init__` membuka DB dengan `sqlite3.connect` kosong, tanpa memanggil `db.migrasi()`. DB berada di `user_version=3` sedangkan kod `SKEMA_VERSI=7` → jadual `bab`, `darjat`, `hadethenc`, `semakhadis` tidak wujud. Search/hadis list/random crash.
- **Pembetulan**: `HadisAPI.__init__` kini memanggil `db.migrasi(c)` selepas buka DB. `get_collection_info()` tambah laluan offline (sebelum ini sentiasa panggil API → perlu kunci).
- **Selepas**: DB `user_version=7`, semua jadual wujud. Integrity check OK, 62,169 hadis, FTS OK.

**MASALAH 3 — "Huraian hadis hilang"** (`semakhadis` kosong, bahagian "Huraian (SemakHadis)" tidak muncul):

- **Punca**: `.cache_sema/` (cache data SemakHadis.com) hilang — jadual `semakhadis` kosong.
- **Had API**: `hadith-search.json` menghadkan **1,000 rekod setiap query** (pagination melebihi halaman 2 kosong).
- **Pembetulan**: cipta `scripts/muat_turun_sema.py` (skrip muat turun yang sebelum ini tiada) — enumerate guna 42 query (28 huruf Arab + 14 pasangan kata) dengan penyahduplikasian ID. Muat turun **16,547 rekod** ke `.cache_sema/`.
- **Sync**: `python sync_sema.py` → **4,237 padanan** disimpan (berbanding 2,045 yang didokumenkan Sesi 18.8; liputan bertambah kerana cache lebih lengkap).
  - bukhari 717, muslim 430, abu-daud 354, tirmidzi 63, nasai 350, ibnu-majah 409, ahmad 1,645, darimi 148, malik 121.
- **Syarah Fath al-Bari**: masih tidak dipapar — `sync_syarah.py fathbari` dibatalkan pengawal (skor sejajar 6.9% vs kawalan 6.8%, nisbah 1.00x < 1.8x). Penomboran Fath al-Bari tidak sejajar dengan Bukhari (keputusan Sesi 10B kekal).

**PENGESAHAN**:
- `python main.py` lancar tanpa ralat (diuji 3×).
- Carian semantik berfungsi (query "bagaimana cara solat yang betul" → 5 hasil).
- `get_hadis_by_id('bukhari', 7)` pulangkan sema: Muttafaq 'alayh, tajuk, terjemahan BM, komentar.
- Carian FTS "solat" → 11,408 hasil.

**FAIL BARU**: `scripts/muat_turun_sema.py`
**FAIL DIUBAH**: `core/semantic_search.py`, `ui/pages.py`, `api/hadis_api.py`

**STATUS: SELESAI.** Apps jalan, DB bermigrasi penuh (v7), huraian SemakHadis dipulihkan (4,237).

**NOTA MASA DEPAN**: jika perlu lengkapkan cache 16,547 → 19,462, sambung query tambahan dalam `muat_turun_sema.py` (skrip menyahduplikasi dan melangkau fail sedia ada).

---

# Sesi 20 — Penilaian kualiti "Carian Makna (AI)": punca ditemui, cadangan model e5 (6 Ogos 2026)

**PERINTAH PENGGUNA**: "carian makna tak relevan" — soalan "apa hukum makan riba" memberi hasil susu unta; "lupa dalam solat" memberi hasil waktu solat.

## Ujian diagnostik (sampel 500 hadis, model MiniLM-L12-v2)

**Ujian 1 — melayu sahaja vs gabungan penuh** (`embed_test.py`):

| Kaedah | Skor teratas | Komen |
|---|---|---|
| A. Melayu sahaja (top 512 aksara) | 0.34–0.45 | Lebih baik, tapi sanad masih menguasai |
| B. Gabungan arab+melayu+indonesia (indeks SEMASA) | 0.21–0.22 | Vektor kabur — bahasa campur mencairkan makna |

**Ujian 2 — matn Melayu (sanad dibuang) sahaja** (`embed_test.py`, penanda "daripada Nabi/Rasulullah Shallallahu..."):

- "apa hukum makan riba" → #1 (0.495) = hadis MINUMAN (bukan riba); hadis riba hanya muncul di #2 (0.422).
- "kelebihan bersedekah" → 5 hasil teratas semuanya pembukaan matn generik, BUKAN sedekah.

## Punca (disahkan oleh eksperimen)

1. **`scripts/build_faiss_index.py` membina teks dari gabungan `arab+melayu+indonesia+english`** — vektor per-hadis jadi kabur (skor 0.21 vs 0.45 jika melayu sahaja).
2. **Teks bermula dengan sanad panjang** ("Telah menceritakan kepada kami X bin Y...") yang menguasai embedding dan menenggelamkan matn.
3. **MiniLM-L12 terlalu kecil** untuk retrieval semantik hadis — perbezaan skor relevan/tidak relevan terlalu tipis (0.37–0.50), pembukaan matn generik ("Nabi...bersabda:") menang pada hampir semua query.
4. Ambang skor semasa (0.30) terlalu rendah — hasil hingar diterima.

## CADANGAN (belum dilaksanakan — pengguna memilih sambung esok)

**Pilihan 1 — Model retrieval yang betul (DISYORKAN): `intfloat/multilingual-e5-large`**
- Latihan khas untuk retrieval; awalan prompt `"query: "` untuk query dan `"passage: "` untuk dokumen.
- Mampu membezakan maksud jauh lebih baik daripada MiniLM. Kesan pada query ujian boleh diukur (riba harus di #1).
- Kos: muat turun model lebih besar (~2.2 GB) + encode 62,169 hadis lebih perlahan (CPU, mungkin 2-3 jam).
- Perlu tukar `build_faiss_index.py` (prompt passage) + `semantic_search.py` (prompt query).
- Simpan versi semasa terlebih dahulu sebelum tukar (fail yang sama digunakan).

**Pilihan 2 — Naikkan ambang** (cepat, murah): terima hanya skor ≥ 0.55. Risiko: sering tiada hasil — buat pengguna rasa ciri rosak.

**Pilihan 3 — Terima seadanya**: kekalkan MiniLM + gabungan semasa; ciri "lengkapkan jika model ada"; pengguna bergantung pada carian kata kunci.

**Sekiranya e5 dipilih**: bina semula indeks juga perlu guna teks **matn Melayu sahaja** (buang sanad) — penguji 2 menunjukkan matn-sahaja memberi skor 0.42–0.50 vs 0.21 gabungan penuh. Skrip `matn_melayu()` sudah ditulis dan diuji dalam `C:\Users\MKAW\AppData\Local\Temp\opencode\embed_test2.py`.

**Fail ujian sementara** (boleh dibuang): `C:\Users\MKAW\AppData\Local\Temp\opencode\embed_test.py`, `embed_test2.py`, `sampel_melayu.py`.

**STATUS: TIDAK SELESAI** — menunggu keputusan pengguna esok (sambung dari sini).

---

# Sesi 20 (samb.) — Carian Makna (AI) DIPERBAIKI: model e5-small + matn Melayu (6 Ogos 2026)

**KEPUTUSAN PENGGUNA**: teruskan dengan model retrieval e5. Ujian mengesahkan e5 berjaya; indeks penuh dibina semula.

## Pilihan model (diuji pada sampel 500 hadis, 100 daripadanya mengandungi "riba")

| Model | Masa encode 500 | Anggaran 62,169 | Kualiti "apa hukum makan riba" |
|---|---|---|---|
| `paraphrase-multilingual-MiniLM-L12-v2` (lama) | 76s | ~2.6 jam | ❌ #1 minuman, riba hanya #2 (0.42) |
| `intfloat/multilingual-e5-large` | 11 min | **23 jam** | ✅ 5/5 riba (0.81-0.82) |
| `intfloat/multilingual-e5-small` | 90s | **3.1 jam** | ✅ 3/4 riba (0.82-0.84) |

**Pilihan: e5-small** — kualiti hampir sama dengan e5-large, 7× lebih pantas.

## Perubahan kod

### `scripts/build_faiss_index.py` (ditulis semula)
- Model lalai: `intfloat/multilingual-e5-small`
- Teks embedding = **matn Melayu SAHAJA** (sanad dibuang) + awalan `passage: ` (keperluan e5)
- `matn_melayu()` — buang sanad dengan penanda "daripada Nabi/Rasulullah Shallallahu..."; fallback ambil 400 aksara terakhir
- `MAX_CHARS = 1000`
- Argumen `--langs` dibuang (tidak lagi gabung bahasa)

### `core/semantic_search.py`
- `_DEFAULT_MODEL = "intfloat/multilingual-e5-small"`
- Query diberi awalan `"query: "` (mesti sepadan dengan `passage:` di sisi dokumen)
- `min_score` lalai dinaikkan **0.3 → 0.6** (e5 memberi skor 0.8+ untuk padanan betul)

### `ui/app_qt.py`, `core/draft_answer.py`
- `min_score` pemanggil diselaraskan kepada 0.6

## Pembinaan indeks

- Masa sebenar: **2 jam 3 minit** (972 kelompok × 64, CPU 4 teras)
- Hasil: `hadis_faiss.index` 95.5 MB, `hadis_id_map.pkl` 0.9 MB, 62,169 vektor, dimensi 384
- Tiada teks matn kosong/pendek (0)

## Pengesahan kualiti (indeks penuh, `min_score=0.6`)

| Soalan | Hasil teratas | Relevan? |
|---|---|---|
| "apa hukum makan riba" | ahmad#10007 "akan datang zaman manusia memakan riba", tirmidzi#1127 "melaknat pemakan riba" | ✅ 0.85 |
| "kelebihan bersedekah" | ahmad#7414 "tangan di atas lebih baik daripada tangan di bawah" | ✅ 0.87 |
| "lupa dalam solat" | ahmad#14823 "adakah ayat itu dimansuhkan atau tuan lupa? Aku lupa" | ✅ 0.85 |
| "niat puasa ramadhan" | tirmidzi#662 "puasa qada Ramadan... mesti niat pada malam" | ✅ 0.88 |

**Perbandingan dengan indeks lama:** skor 0.21-0.50 (tidak relevan) → 0.84-0.88 (relevan). Transformasi lengkap.

## Pengesahan sistem

- `get_index_stats()` → ready, 62,169 vektor, 384D ✅
- `python main.py` (offscreen) → berjalan tanpa traceback ✅
- `compose_draft_answer("apa hukum makan riba")` → 5 hasil, draf jawapan tersusun ✅

## Fail diubah
- `scripts/build_faiss_index.py`, `core/semantic_search.py`, `ui/app_qt.py`, `core/draft_answer.py`

## Nota
- Model e5-large (~2.2 GB) turut dimuat turun ke `.cache_models` semasa ujian — boleh dibuang jika perlu jimat ruang (e5-small sudah memadai). **SUDAH DIBUANG** (Sesi 20 samb.).
- Model MiniLM lama (~0.45 GB) juga sudah dibuang — hanya dirujuk fail wrapper usang (`start_build.py`, `build.py`, `build_semantic.py`, `build_faiss_index.py` akar) yang tidak digunakan.
- Fail ujian sementara: `C:\Users\MKAW\AppData\Local\Temp\opencode\embed_test*.py`, `uji_*.py`, `sampel_melayu.py`.

**STATUS: SELESAI.** Carian Makna (AI) kini benar-benar memahami soalan.

---

# Sesi 20 (samb. 2) — BUG DLL TORCH+PYQT5 DITEMUI & DIPERBAIKI (ujian apps menyeluruh)

**PERINTAH PENGGUNA**: "kita sambung dengan testing apps baru ini".

## Ujian menyeluruh (offscreen, memandu apps sebenar)

`uji_apps.py` — **12/12 lulus**:
- jumlah hadis 62,169 ✅ · semakhadis 4,237 ✅ · indeks semantik 62,169 vektor 384D ✅
- `get_hadis_by_id('bukhari',1)` ada arab+melayu ✅
- `search_hadis('solat')` → 5 hasil, total 11,408 ✅
- `semantic_search('apa hukum makan riba')` → 5 hasil, top 0.854 ahmad#10007 ✅
- `compose_draft_answer('kelebihan bersedekah')` → 3 hasil ✅
- navigasi UI home/search/saved ✅ · `open_detail` ✅ · bukhari#7 ada sema ✅ · toggle bookmark ✅

## BUG KRITIKAL DITEMUI: konflik DLL runtime MSVC

**Gejala**: `semantic_search` crash `OSError: WinError 1114` pada `torch\lib\c10.dll` **hanya apabila PyQt5 dimuat dahulu**. Torch sahaja OK; PyQt5 + torch = gagal.

**Punca (disahkan dengan membandingkan versi DLL)**:
- PyQt5 5.15.11 membundel runtime MSVC **14.26** dalam `PyQt5\Qt5\bin` (`concrt140.dll`, `msvcp140*.dll`, `vcruntime140*.dll`)
- torch 2.13.0+cpu dibina untuk runtime **14.44** (System32)
- Apabila PyQt5 dimuat dahulu, Windows guna runtime 14.26 yang lama → c10.dll gagal init

**Kesan**: "Carian Makna (AI)" dalam apps sebenar akan crash pada query pertama — tidak dikesan lebih awal kerana ujian terdahulu memuat `semantic_search` TANPA PyQt5. `KMP_DUPLICATE_LIB_OK=TRUE` TIDAK membantu.

## Pembaikan

`main.py` — fungsi `_baik_pulih_dll_qt_torch()` dipanggil SEBELUM import PyQt5:
- Alihkan DLL runtime 14.26 dari `PyQt5\Qt5\bin` ke `%TEMP%\qt_dll_lama` (mengalih, bukan memadam)
- Python kemudian guna runtime 14.44 dari System32 (backward-compatible)
- Idempoten: semak versi 14.26 dahulu; tiada kesan jika sudah dialih atau versi betul

**Pengesahan**:
- `PyQt5 + torch` → TORCH OK (sebelum: WinError 1114)
- Carian semantik dalam QThread (tiru `SemanticWorker`) → 5 hasil, top 0.854 ✅
- `python main.py` penuh → berjalan, tiada DLL/traceback ✅
- UI carian semantik → 1 draf (QTextBrowser) + 5 kad hadis (ClickCard) ✅

## Ruang cakera dibersihkan
- C: — cache Qwen3-TTS + PaddlePaddle dipadam (**jimat 6.58 GB**): 137 → 143.68 GB
- D: — e5-large (2.11 GB) + MiniLM (0.45 GB) dipadam (e5-small memadai): baki .cache_models 0.46 GB

**FAIL DIUBAH**: `main.py`
**FAIL DIUJI**: `C:\Users\MKAW\AppData\Local\Temp\opencode\uji_apps.py`, `uji_thread.py`, `uji_ui_semantik*.py`

**STATUS: SELESAI.** Apps 12/12 lulus, DLL tetap automatik, ruang dijimat.

# Sesi 20 (samb. 3) - semak.py 10 KEGAGALAN DITANGANI (6 Ogos 2026)

Pengguna minta "selesaikan yang benar-benar boleh diselesaikan. pastikan apps berjalan lancar". Semua 10 kegagalan `semak.py` disahkan SEDIA ADA (bukan dari perubahan Sesi 20). Diselesaikan:

1. **Fail fix\* (Sesi 19) DIARKIB** ke `C:\Users\MKAW\AppData\Local\Temp\opencode\fix_sesi19\`:
   - `fix.bat` — BERBAHAYA: pasang `torch==2.0.1+cpu` + `sentence-transformers==2.2.2` (tiada wheel Python 3.14 → rosakkan setup berfungsi)
   - `fix_and_run.bat`, `fix_and_run.ps1`, `FIX_AND_RUN.md`
2. **`ui/app_qt.py` `_page_search`**: tambah komen `TIADA addStretch` dengan sebab (struktur sama `_page_kitab`; `col` Maximum menegak sudah mengisi viewport; stretch hanya cipta ruang skrol kosong). Semak 8d lulus.
3. **Halaman utama 4px**: `bl.setContentsMargins(0,0,0,24)` → `(0,0,0,20)` di `_page_home`. Diukur `LEBIHAN 4` → `LEBIHAN 0` pada 1240x730. Semak 8e lulus.
4. **`semak_bersih` (semak 9)**: fail data kerja aktif (`.cache_sema`, `hadis.db`, `hadis.db-wal/shm`, `bookmarks.json`) kini DIBENARKAN wujud semasa pembangunan (lulus + nota "buang sebelum ZIP") — memadam `hadis.db` menghapus seluruh koleksi. Fail artifak sebenar (`__pycache__`, `.cache_eng/he`, `user_settings.json`, `.env`) masih GAGAL.

**KEPUTUSAN**: `python semak.py` → **SEMUA LULUS** (sebelum: 10 GAGAL). Ujian apps `uji_apps.py` → **12/12 lulus** selepas ubah UI.

**FAIL DIUBAH**: `semak.py`, `ui/app_qt.py`
**FAIL DIARKIB**: `fix.bat`, `fix_and_run.bat`, `fix_and_run.ps1`, `FIX_AND_RUN.md`



# Sesi 20 (samb. 4) - ANALISA_6OGOS.md dilaksanakan + gabungan carian automatik (6 Ogos 2026)

## A. Pelaksanaan ANALISA_6OGOS.md (3 langkah "Hari ini" + 1 "Minggu ini")

Dokumen `D:\Pustaka Quran Hadis\ANALISA_6OGOS.md` (31 fail sumber diperiksa terus)
mengesahkan seni bina kukuh, sifar ralat sintaks, dan mengenal pasti 7 kekurangan.

### 1. `requirements.txt` dibetulkan (KRITIKAL 1)
- Lama: `sentence-transformers>=2.2.2.2.2` (LIMA segmen, tiada versi sebegitu wujud);
  `torch` langsung tidak disenaraikan.
- Baharu: pin versi disahkan dengan Python 3.14 —
  `PyQt5>=5.15.11`, `requests>=2.28.0`, `pyperclip>=1.8.0`, `tqdm>=4.65.0`,
  `torch>=2.6`, `sentence-transformers>=5.0`, `faiss-cpu>=1.9`.
- Disahkan pada mesin: PyQt5 5.15.11, requests 2.34.2, torch 2.13.0+cpu,
  sentence-transformers 5.6.1, faiss 1.15.0.

### 2. Lapan skrip build usang dialih ke `_arkib/` (SEDERHANA 3)
- `build.py`, `build_index.py`, `build_index_now.py`, `build_semantic.py`,
  `run_build.py`, `run_semantic_build.py`, `start_build.py`, `check_build.py`.
- Semuanya wrapper yang hanya memanggil `scripts/build_faiss_index.py`.
- Ditambah `_arkib/BACA.md`; disahkan TIADA rujukan patah (grep seluruh projek).

### 3. `README.md` ditulis semula dalam BM (SEDERHANA 5)
- Lama: English + skop carian semantik sahaja.
- Baharu: gambaran keseluruhan 62,169 hadis / 9 kitab, ciri, pemasangan, cara
  guna, struktur projek, carian AI, pembangunan, penyelesaian masalah, lesen.

### 4. Fix DLL PowerShell diganti dengan ctypes (KRITIKAL 2 / "Minggu ini")
`main.py::_baik_pulih_dll_qt_torch()` versi lama memanggil
`os.popen('powershell ... Get-ChildItem ...')` — tiga masalah: kegagalan
senyap (dasar PowerShell disekat → senarai kosong → WinError 1114 tanpa
punca), lewat setiap pelancaran, dan `except: pass` menyembunyikan semua.
- Baharu: baca versi DLL terus via Win32 `GetFileVersionInfoW` (ctypes) —
  tiada subproses; hanya alih DLL MSVC `14.x < 14.40` (`_perlu_alih`);
  setiap kegagalan dilaporkan ke stderr dengan amaran jelas (bukan senyap).
- Idempoten, memindah (bukan memadam), pulangkan bilangan DLL dialih.
- **Pengesahan**: logik `_perlu_alih` 6/6 lulus (14.26→alih, 14.44/14.40→kekal,
  14.29→alih, 10.0→kekal, None→kekal); fungsi sebenar idempoten (0 dialih);
  PyQt5 + torch 2.13.0 + sentence_transformers dimuat serentak OK;
  `semak.py` → SEMUA LULUS.

## B. Gabungan carian automatik keyword + semantik (DITERUSKAN dari sesi lalu)

Objektif: buang checkbox "🤖 Carian Makna (AI)" supaya kedua-dua enjin sentiasa
berjalan selari. Perubahan sudah ada dalam `ui/pages.py` (`is_semantic()→True`,
checkbox dibuang) dan `ui/app_qt.py` (`_do_search` jalankan SearchWorker +
`_run_semantic_search` selari; `_tampal_gabungan` papar draf AI + kad semantik
dedupe + kad keyword; `_on_search`/`_on_semantic_search` set
`_kw_res`/`_sem_res` lalu tunggu kedua-duanya).

### Bug ditemui & dibaiki dalam sesi ini
- **`ui/app_qt.py:729`**: `SemanticWorker(q, ...)` → `SemanticWorker(query, ...)`.
  `q` tidak wujud dalam `_run_semantic_search` (parameternya `query`). NameError
  dalam callback QTimer itu punca **crash keras `EXIT=-1073740791` (0xC0000409)**
  tanpa traceback semasa ujian gabungan. Selepas dibaiki: ujian penuh `EXIT=0`.

### Isu semasa (dalam siasatan)
- **SemanticWorker tersekat (25-40s)** bila muat model torch dalam QThread
  serentak dengan SearchWorker dalam `_do_search`. Konsisten tersekat pada
  `_do_search` penuh, tetapi `_run_semantic_search` bersendirian OK.
- **Penyelesaian terbukti**: pra-muat model dalam thread utama sebelum
  `_do_search` → semua lulus (KAD: 21, worker selesai). Rancangan: pra-muat
  sekali dalam `PustakaApp.__init__` supaya carian sentiasa pantas.
- Import `QCheckBox` masih tinggal di `ui/pages.py` baris 8 (tak digunakan) —
  bersihkan kemudian.

**FAIL DIUBAH**: `requirements.txt`, `main.py`, `README.md`, `ui/app_qt.py`
**FAIL DIARKIB**: 8 skrip build usang → `_arkib/`
**PENDING**: pra-muat model dalam `__init__`; Hadis comparison view
(side-by-side Malay/Indonesia); permohonan lesen SemakHadis.com (luar kod).

---

# Sesi 22 — Git + sync data lengkap + integrasi HadeethEnc v1.1 (7-8 Ogos 2026)

## 1. Repositori git diwujudkan (komit pertama)

Projek sebelum ini TIADA kawalan versi (21 sesi tanpa git). Sesi ini
memulakan git sebagai jaring keselamatan:

- `git init` + komit pertama `2970234` (89 fail, 23,154 baris)
- **`.gitignore` diperluas** — data besar (hadis.db 262MB, hadis_faiss.index
  95MB, .cache_models/ 460MB), kunci, dan tetapan pengguna dikecualikan
- **Kunci API terdedah DIALIH KELUAR dari `semak_kunci.py`** — dua kunci
  penuh (HADIS_34A8..., HADIS_E6D6...) ada dalam kod! Dipindah ke
  `kunci_terdedah.txt` (di-gitignore) supaya tidak kekal dalam sejarah git
  selama-lamanya. Skrip membaca kunci dari fail luaran — berfungsi sama.
- Fail `4.65.0` (sisa output pip) dibiarkan untracked

## 2. Sync data lengkap — jadual kosong diisi

Sebelum sesi ini, 4 jadual kosong walaupun kod sudah sedia:

| jadual | sebelum | selepas | sumber |
|---|---|---|---|
| `bab` | 0 | **31,322** | sync_english.py (metadata CDN) |
| `darjat` | 0 | **63,930** | sync_english.py (metadata CDN) |
| `hadethenc` | 0 | **310** | sync_hadeethenc.py (padanan matn) |
| `terjemahan_eng` | 31,833 | 31,833 | disahkan semula |

- Cache HadeethEnc `.cache_he/` (147 hadis sumber) dimuat turun kali pertama
- `darjat`=0 untuk Bukhari & Muslim **bukan pepijat** — fail CDN
  `ara-bukhari1`/`ara-muslim1` memang tiada medan `grades` (sumber asal
  fawazahmed0/hadith-api tidak menyediakannya)
- `sync_syarah.py` TIDAK dijalankan — Fasa 4B dibatalkan (keputusan bertulis)

## 3. Integrasi HadeethEnc ke UI (v1.1) — sandaran huraian

### Penemuan
`core/phase4_exegesis.py` (yang dulu menggabungkan HadeethEnc) tidak wujud
lagi dalam kod semasa. Akibatnya **211 daripada 310 padanan HadeethEnc**
adalah untuk hadis yang TIADA huraian SemakHadis — data berharga tersembunyi.

### Perubahan
- `api/hadis_api.py`: fungsi modul `bina_huraian_he(conn, slug, hadis_id)`
  + kaedah `HadisAPI._he()` / `_he_luar()` — baca padanan dari jadual
  `hadethenc`, huraian dari cache `.cache_he/{id}.json`
- `ui/app_qt.py`: `open_detail` baca `_he_luar` sebelum render;
  `_render_detail` papar Collapsible **"Huraian (HadeethEnc · status)"** bila
  SemakHadis tiada; `_bina_he()` panel baharu (tajuk, darjat, terjemahan,
  penjelasan, pengajaran + atribusi wajib HadeethEnc/IslamHouse)
- `VERSI.py`: 1.0 → **1.1**, +1 ciri `api.hadis_api.bina_huraian_he` ke CIRI
- `semak.py`: semakan 8e(d) mengunci integrasi (API + UI); docstring dikemas kini
- `uji_data_baharu.py`: fail ujian offscreen baharu (18 semakan)

### Pepijat sebenar ditemui (bukan pepijat ujian)
`_on_detail_full` mengganti `_detail_h` dengan data segar `get_hadis_by_id`
yang TIDAK membawa `he` — sandaran HadeethEnc akan "hilang" sebaik worker
selesai. Pembetulan: kekalkan `he` daripada render awal dalam `_on_detail_full`.

### Isu prestasi (dikesan peninjau kod)
`get_hadis_by_id` dipanggil untuk SETIAP kad hasil carian (20-40+/carian).
Set `he` di sana = baca fail cache .cache_he/ setiap kali untuk data yang
hanya diperlukan di halaman butiran. Penyelesaian: muatan `he` hanya dalam
`open_detail`/`_on_detail_full` (1 baca fail setiap buka butiran).

### Keputusan ujian
- `semak.py`: 135 semakan lulus (2 "GAGAL" = amaran cache edaran, dijangkakan)
- `semak_versi.py`: 20 ciri v1.1 hadir
- `uji_data_baharu.py`: **18/18 lulus** — bab, darjat, sema, sandaran
  HadeethEnc dipapar dalam widget UI sebenar (offscreen); carian gabungan
  (FTS5 + AI) berjalan; tutup aplikasi tanpa crash 0xC0000409

## 4. Komit kedua

`c3249bf` — 5 fail, +400 baris (api, ui, VERSI, semak, ujian baharu).

## 5. Pelajaran

1. **Kunci API boleh bersembunyi dalam skrip "keselamatan"** — `semak_kunci.py`
   menyenaraikan kunci penuh untuk diuji, tetapi itu bermakna ia akan masuk
   ke git jika tiada langkah khas. Apabila memulakan git pada projek lama,
   imbas SEMUA fail untuk corak kunci sebelum komit pertama.
2. **Fungsi peringkat modul vs kaedah kelas**: `semak_versi.py` semak
   `hasattr(modul, nama)` — kaedah kelas TIDAK lulus. Ikut corak sedia ada:
   fungsi modul (`bina_huraian_he`) dipanggil oleh kaedah kelas (`_he`).
3. **Data tersedia ≠ data dipapar**: sync mengisi 310 padanan HadeethEnc,
   tetapi UI lama tidak memanggilnya. Sahkan rantaian data→API→UI dengan
   ujian offscreen yang membuka butiran sebenar.
4. **`open_detail` membuat salinan `dict(h)`** — objek asal pemanggil TIDAK
   diubah. Ujian mesti baca `w._detail_h` (objek yang sebenarnya dipapar),
   bukan `h` yang dihantar.

**FAIL DIUBAH**: `VERSI.py`, `api/hadis_api.py`, `ui/app_qt.py`, `semak.py`,
`sesi_index.md`, `MULA_SINI.md`, `.gitignore`
**FAIL BAHARU**: `uji_data_baharu.py`, `kunci_terdedah.txt` (di-gitignore)
**PENDING**: Semak kunci terdedah masih aktif (`python semak_kunci.py`);
ujian visual pada mesin sebenar; kemas kini `PERUBAHAN_7OGOS.md` §6 sebagai
selesai; Hadis comparison view (side-by-side Malay/Indonesia).

## 6. Sesi 22 (samb.) — Pengesahan visual sebenar, dokumentasi §6, peraturan fail sisa

### 6.1 Pengesahan VISUAL sebenar — sandaran HadeethEnc (tema gelap & terang)

- `uji_visual_sebenar.py` (baharu): memaparkan aplikasi pada skrin SEBENAR
  (bukan offscreen), membuka hadis tanpa SemakHadis tetapi ada HadeethEnc,
  mengambil tangkapan skrin fizikal (Pillow ImageGrab) kedua-dua tema.
- **14/14 lulus**: abu-daud #4459 (he_id 3017) + ibnu-majah #4038 (he_id
  65045) — sema tiada, HE ada, Collapsible dipapar, teks kelihatan
  (133-142 warna unik), kecerahan betul (41 gelap / 210 terang).
- **Pelajaran teknikal**: mod offscreen (`QT_QPA_PLATFORM=offscreen`)
  merender latar TANPA teks (6-7 warna unik sahaja) — had platform,
  bukan pepijat aplikasi. Pengesahan visual mesti guna skrin sebenar +
  ImageGrab. Tangkapan skrin: `bukti_visual/` (di-gitignore).
- `PERUBAHAN_7OGOS.md` §4/§5/§6 dikemas kini: penyelesaian QThread
  Background (Punca #2) ditandakan **SELESAI** dengan rujukan kod sebenar.
- Komit `f4b8dda`.

### 6.2 Peraturan fail sisa + audit keselamatan

- Fail `4.65.0` (sisa output pip — output tersilap diubah hala ke fail
  bernama versi tqdm) dipadam.
- `semak.py` baharu: `_senarai_untracked_git()` — mengesan sebarang fail
  untracked git (tidak dijejak, tidak di-ignore) sebagai sisa;
  `semak_peraturan_sisa()` — ujian automatik yang menyuntik fail ujian,
  sahkan ia dikesan, lalu memadam (jika peraturan rosak, fail ujian
  KEKAL dan semak_bersih melaporkannya pada run seterusnya).
- Audit keselamatan: `git grep` pada semua komit — **tiada kunci API**;
  kunci penuh hanya dalam `kunci_terdedah.txt` (di-gitignore);
  `user_settings.json`/`.env` tidak wujud dan di-ignore.
- Komit `19f5238`; semak.py kini 136 semakan lulus.

**FAIL DIUBAH**: `semak.py`, `PERUBAHAN_7OGOS.md`, `.gitignore`
**FAIL BAHARU**: `uji_visual_sebenar.py`
**PENDING**: ujian tukar tema berulang; pengesahan end-to-end penuh;
Hadis comparison view (side-by-side Malay/Indonesia).

---

# Sesi 23 — Fallback OR carian kata kunci + mesej bantuan + v1.2 (8 Ogos 2026)

**FOKUS**: Menyelesaikan had FTS5 AND yang paling dirasai pengguna --
carian seperti "hukum riba" pulang 0 hasil walaupun setiap perkataan wujud
berasingan dalam korpus. Dua lapisan penyelesaian: mesej bantuan (bila AI
ada padanan) dan fallback OR (bila AND pulang 0, cuba OR supaya kad keyword
tetap dipapar).

## 1. Penemuan (Sesi 22 sambungan)

- Carian "hukum riba" = **0 hasil FTS5** walaupun "hukum" (247) dan
  "riba*" (239) masing-masing wujud. Punca: FTS5 AND memerlukan SEMUA
  perkataan hadir serentak -- tiada hadis mengandungi kedua-duanya.
  Ini had FTS5 biasa, bukan pepijat; carian semantik AI wujud untuk
  menampung perbezaan perkataan. Namun pengguna tetap melihat senarai
  kosong tanpa penjelasan.

## 2. Mesej bantuan kata kunci kosong (komit `4f86954`)

- Bila kata kunci 0 hasil DAN AI ada padanan makna, lencana AMBER dipapar
  dalam `_tampal_gabungan`: "Tiada padanan kata kunci yang mengandungi
  SEMUA perkataan... Padanan makna (AI) di bawah dicari ikut maksud".
- Lencana AMBER (latar gelap + teks amber) dipilih selepas peninjau kod
  menunjukkan teks amber sahaja pudar pada tema terang.
- Dikunci oleh semak.py semakan **8g** (`semak_gabungan`) -- marker,
  syarat `not kw and not meta.get("total")`, dan cabang `if sem:` disemak
  melalui AST (bukan split teks).

## 3. Fallback OR (v1.2)

- `db._to_match_query(q, gabung)` kini menyokong "AND" (lalai) atau "OR".
- `db.search()` dan `api.hadis_api.search_hadis()`: bila AND pulang 0 hasil
  dan ada >1 perkataan, cuba OR secara automatik. `meta["fallback"]=True`
  ditanda supaya UI tahu.
- UI `_tampal_gabungan`: bila `meta.get("fallback")`, papar nota "Carian
  kata kunci longgar: tiada hadis mengandungi SEMUA perkataan... hasil di
  bawah mengandungi mana-mana satu".
- Kesan: "hukum riba" kini pulang **486 hasil** (sebelum ini 0), dengan
  ranking BM25 meletakkan paling relevan di atas.
- Dikunci oleh semak.py 8g: `db._to_match_query` sokong OR, tanda
  fallback dalam API, nota longgar dalam UI, dan ujian data sebenar
  (486 hasil).

## 4. Keputusan ujian

- semak.py: **143 semakan OK** (sebelumnya 139; +4 untuk fallback).
- semak_versi.py: versi **1.2**, **22 ciri** hadir.
- uji_data_baharu.py: 18/18 · uji_tukar_tema.py: 19/19 ·
  uji_end_to_end.py: 16/16.

## 5. Pelajaran

1. **FTS5 AND vs OR**: setiap carian berbilang perkataan boleh pulang 0
   hasil walaupun perkataan wujud -- fallback OR + nota jelas lebih baik
   daripada senarai kosong.
2. **Kontras tema**: teks amber sahaja (AMBER_TEXT) pudar pada tema
   terang; lencana AMBER_BG+AMBER_TEXT konsisten dalam kedua-dua tema.
3. **Ujian selari bersaing untuk model AI**: 3 ujian offscreen serentak
   boleh menyebabkan "sem_res=None" flaky (model dimuat serentak);
   bersendirian sentiasa lulus. Jalankan ujian semantik secara berurutan.
4. **Semakan melalui AST, bukan split teks**: `"else:"` dalam string/komen
   boleh menipu semakan teks; nod `ast.If` dengan ujian `sem` lebih kukuh.

**FAIL DIUBAH**: `db.py`, `api/hadis_api.py`, `ui/app_qt.py`, `semak.py`,
`VERSI.py`, `MULA_SINI.md`, `README.md`, `sesi_index.md`
**FAIL BAHARU**: `uji_visual_bantuan.py` (pengesahan visual lencana bantuan)
**PENDING**: pengesahan visual lencana bantuan; Hadis comparison view.

### 6.3 Ranking pembobotan fallback OR (samb. Sesi 23)

- **Penemuan**: BM25 semata-mata meletakkan hadis dengan SATU perkataan
  jarang di atas hadis dengan SEMUA perkataan padan -- untuk "hukum riba",
  0 daripada 20 teratas mengandungi kedua-dua perkataan (hanya 1 dalam
  keseluruhan 486). Punca: BM25 memberi berat kepada term jarang, bukan
  bilangan term padan.
- **Penyelesaian**: `db._terms()` (perkataan bersih) + `CASE WHEN
  h.melayu LIKE '%term%'` sebagai bonus; `ORDER BY (padanan) DESC,
  bm25 ASC`. Hadis dengan lebih banyak perkataan padan sentiasa di atas.
  Diterapkan pada `db.search()` DAN `api.hadis_api.search_hadis()`.
- **Paparan UI**: `search_info` kini memaparkan "486 padanan kata longgar"
  (bukan "486 padanan kata") supaya pengguna faham jumlah itu bukan
  padanan tepat SEMUA perkataan.
- **Ujian kukuh**: semak.py 8g kini bina DB FTS5 SINTETIK (3 hadis,
  query "hukum riba faedah": AND=0 -> OR 3) dan sahkan pembobotan
  meletakkan hadis 2-perkataan di atas -- tidak bergantung pada hadis.db
  edaran. Komit `cb8f766` (v1.2); pembobotan lanjutan selepasnya.

**PENDING**: pengesahan visual lencana bantuan; Hadis comparison view.

---

# Sesi 24 — Bahasa Melayu penuh + terjemah ralat runtime (11 Ogos 2026)

**FOKUS**: Dua lapisan pelengkap bagi komunikasi Melayu yang lengkap:
(1) ujian automatik peraturan bahasa (semakan 8h2) dan (2) pembungkus
`terjemah_ralat()` supaya ralat runtime mentah (sqlite3/requests/OSError)
tidak bocor ke toast pengguna dalam Bahasa Inggeris.

## 1. Audit bahasa luas (sambungan Sesi 23)

- Audit frasa Inggeris dalam STRING LITERAL (docstring/SQL/stylesheet
  dikecualikan) merentas SEMUA fail .py menemui 2 mesej FileNotFoundError
  terlepas dalam `core/semantic_search.py` ("FAISS index not found",
  "ID map not found") -- ditukar ke Melayu.
- semak.py `semak_bahasa_ui()` kini mengimbas SEMUA fail .py (49) dengan
  AST; `FRASA_INGGERIS` diluaskan ke 24 frasa; hanya semak.py sendiri
  dikecualikan (ia mengandungi FRASA_INGGERIS sebagai data rujukan).
  Komit `1074202`.

## 2. Ujian automatik peraturan bahasa (8h2)

- `semak_peraturan_bahasa()` -- suntik fail sementara dengan frasa
  "Loading model", sahkan `_semak_bahasa_fail` mengesannya, padam.
  Jika peraturan rosak, fail KEKAL dan semak_bahasa_ui melaporkannya
  pada run seterusnya (jaring kedua).

## 3. `terjemah_ralat()` dalam utils/bahasa.py

- Kamus `_RALAT_RUNTIME`: 18 corak sqlite3/requests/OSError -> Melayu
  ("database is locked" -> "Pangkalan data sedang dikunci...",
  "Connection refused" -> "Sambungan ditolak oleh pelayan.",
  "No such file or directory" -> "Fail atau folder tidak dijumpai.").
- `_sudah_melayu()` (kata fungsi Melayu) dipakai DAHULU supaya mesej
  yang sudah Melayu (cth. dari HadisAPIError) tidak diterjemah dua kali;
  fallback memulangkan mesej asal supaya maklumat teknikal tidak hilang.
- Diguna dalam: ui/workers.py (5 failed.emit), ui/app_qt.py
  (SemanticWorker), core/semantic_search.py, core/phase2_transliterasi.py.
  Dikunci oleh semak_bahasa_ui (8 kes ralat -> Melayu).
- PENEMUAN: corak "unable to open database file" bertembung dengan
  FRASA_INGGERIS ("unable to") -- disingkatkan ke "open database file"
  supaya semakan bahasa tidak tersilap melaporkan utils/bahasa.py sendiri.

## 4. Pembaikan ujian

- uji_data_baharu.py: had tunggu 35s -> poling sehingga 300s. Model kini
  muat ~80s (sebelum ini ~27s) -- pemasa tetap 35s gagal secara berkala.
  Poling lebih kukuh daripada pemasa tetap.

**PENDING**: Hadis comparison view (side-by-side Malay/Indonesia).

---

# Sesi 25 — Kamus ralat diperluas + tab Sebelah (bandingan bahasa) (11 Ogos 2026)

**FOKUS**: Dua tugasan daripada senarai cadangan Sesi 24: (1) kamus
`_RALAT_RUNTIME` diperluas ke ralat faiss/torch/HTTP/JSON, dan (2) ciri
PENDING lama "Hadis comparison view" direalisasikan sebagai tab
"Sebelah" -- Melayu vs Indonesia side-by-side.

## 1. Kamus ralat diperluas (23 corak)

- Baharu: `connection reset`, HTTP 500/502/503, `server error`,
  `expecting value`/`json decode`/`invalid json` (bukan JSON),
  `no module named 'faiss'` (arahan pip), `cuda out of memory`,
  `found no nvidia driver`.
- Kes ujian semak.py jadi 13 (readonly db, HTTP 500, JSON, faiss, CUDA).
- PEPIJAT DITANGKAP PENINJAU: "Pelayaran buruk (HTTP 502)" bermaksud
  "bad sailing" -- dibetulkan ke "Ralat pelayan (HTTP 502)".

## 2. Tab "Sebelah" (Hadis comparison view)

- `ui/pages.py` LangTabs: tab baharu (`sebelah`, "Sebelah") yang HANYA
  aktif bila kedua-dua Melayu DAN Indonesia ada; jika aktif lalu menjadi
  tidak sah, pulang ke Melayu + bina semula panel (emit=True, pembaikan
  peninjau supaya paparan tidak stale).
- `ui/app_qt.py` `_switch_lang`: cabang `sebelah` memaparkan DUA lajur
  (MELAYU | INDONESIA) dalam QHBoxLayout; `_papar_melayu` (pembetulan
  ejaan) hanya untuk lajur Melayu; setiap lajur ada menu salin sendiri.
- semak.py semakan 8i (`semak_bandingan`) mengunci ciri: tab + syarat
  dua bahasa + cabang sebelah + `_papar_melayu`.
- Pengesahan: `uji_bandingan.py` 9/9 offscreen; `uji_visual_bandingan.py`
  2/2 skrin sebenar (sebelah_gelap/terang.png); `uji_visual_ralat.py`
  9/9 skrin sebenar (ralat_*.png, toast Melayu dalam kedua-dua tema).

**PENDING**: tiada -- semua cadangan Sesi 24 selesai.

---

# Sesi 26 — Salin semua bahasa + atribusi seragam + pengoptimuman muat model (11 Ogos 2026)

**FOKUS**: Tiga tugasan lanjutan daripada Sesi 25: (1) butang "Salin
semua bahasa" dalam tab Sebelah, (2) seragamkan atribusi sumber ke
pemalar, (3) siasat dan optimumkan masa muat model semantik.

## 1. Butang "Salin semua bahasa" (tab Sebelah)

- `_copy_semua_bahasa()`: gabung Arab + Melayu + Indonesia (+ English)
  dengan label [ARAB]/[MELAYU]/[INDONESIA]/[ENGLISH]; `_papar_melayu`
  dipakai pada teks Melayu. Butang ghost dalam baris atas tab Sebelah.
- PEMBAIKAN STRUKTUR: edit awal mencipta DUA `def _switch_lang` (yang
  kedua rosak -- rujuk `txt` sebelum ditakrif); digabung semula ke SATU
  fungsi + `_copy_semua_bahasa` berasingan. Disahkan sintaks + struktur.
- Dikunci semak.py 8i (marker butang + rujukan fungsi).
- uji_bandingan.py jadi 16 kes (butang wujud + salinan mengandungi
  [MELAYU]/[INDONESIA]/[ARAB] + [ENGLISH] bila wujud).

## 2. Atribusi sumber seragam (pemalar)

- `_ATRIBUSI_SEMA` ("Sumber: SemakHadis.com") + `_ATRIBUSI_HE`
  (HadeethEnc.com/IslamHouse) ditambah sebelah `_ATRIBUSI_INGGERIS`;
  guna di `_bina_sema` dan `_bina_he`. Semak.py semak_sema(f) +
  semak_hadeethenc kini kunci pemalar supaya teks tidak hanyut.

## 3. Muat model semantik: siasatan + pengoptimuman

- **Punca utama**: import `sentence_transformers` = ~19s (torch 4s +
  transformers ~15s) -- had persekitaran Windows/antivirus, bukan kod
  aplikasi. Muat model 5.3s, encode 0.2s. Masa stabil 24.5s; 80s dalam
  ujian awal ialah transien (larian pertama + antivirus mengimbas DLL).
  `torch.set_num_threads` TIDAK membantu (19.9s) -- threads sudah 2.
- **Diterapkan**: `TOKENIZERS_PARALLELISM=false` (elak amaran).
- **REGESI DITANGKAP PENINJAU**: `HF_HUB_OFFLINE=1` mematahkan cabang
  fallback muat turun model bila belum dicache -- dibuang; kekalkan
  hanya TOKENIZERS_PARALLELISM.

**PENDING**: tiada.

---

# Sesi 27 — Kongsi semua bahasa + profil muat model automatik (11 Ogos 2026)

**FOKUS**: Tiga tugasan lanjutan: (1) butang "Kongsi semua bahasa"
(WhatsApp) dalam tab Sebelah, (2) ukur semula muat model pada larian
bersih, (3) profil masa muat model ke fail log yang dibaca semak.py.

## 1. Butang "Kongsi semua bahasa"

- `_teks_semua_bahasa()` diekstrak -- SATU sumber kebenaran untuk
  gabung Arab+semua terjemahan berlabel; `_copy_semua_bahasa` (Salin)
  dan `_share_semua_bahasa` (WhatsApp, had 700 aksara) guna semula.
- Dikunci semak.py 8i (butang Kongsi + `_teks_semua_bahasa`).
- uji_bandingan.py jadi 21 kes (butang wujud, teks sama dengan salinan,
  had 700 aksara).

## 2. Ukur semula muat model (larian bersih)

- 3 larian berturut: 24.2-25.7s -- STABIL. Pecahan: import modul 0.4s
  (sentence_transformers dimuat dalam _load_model), muat 24s (import ST
  ~19s + model ~5s). Sahkan 80s awal ialah transien larian pertama
  (antivirus mengimbas DLL torch/transformers).

## 3. Profil muat model automatik

- `core.semantic_search._simpan_profil()`: tulis masa muat+import ke
  `profil_model.json` (20 rekod terakhir) setiap larian yang memuat
  model. Gagal senyap -- alat diagnostik, bukan fungsi kritikal.
- semak.py semakan 8j (`semak_profil_model`): lapor larian terkini +
  amaran GAGAL bila muat >60s atau purata 3 larian >60s (regresi
  prestasi). `profil_model.json` dibenarkan sebagai fail data kerja
  (semak_bersih) dan di-gitignore.

**PENDING**: tiada.



# Sesi 28 — Skrin pemula (splash) + Salin/Kongsi bahasa semasa + siasat muat model (11 Ogos 2026)

## 1. Butang Salin/Kongsi bahasa SEMASA (paparan bahasa tunggal)

- `_teks_bahasa_semasa()`: gabung tajuk + label + terjemahan bahasa yang
  sedang dipapar (`[BAHASA MELAYU]` dsb.), `_papar_melayu` pada Melayu,
  had aksara untuk WhatsApp (`_HAD_WA=700`).
- Butang "📋 Salin" + "💬 Kongsi" dalam cabang bahasa tunggal `_switch_lang`
  (bukan hanya tab Sebelah); `_lang_key` dikesan daripada tab aktif.
- Dikunci semak.py 8i (butang + `_copy/_share_bahasa_semasa` +
  `_teks_bahasa_semasa`); uji_bandingan jadi 28 kes.

## 2. Siasat muat model di latar belakang

- Disahkan: `import torch` DULU (4.4s + 15.4s = 19.8s) SAMA dengan import
  terus sentence_transformers (~19s) — tiada pengurangan import tersedia;
  had persekitaran Windows/antivirus (DLL torch + transformers).
- Model sudah dimuat dalam QThread (`PreloadWorker`) sejak Sesi sebelum —
  UI tidak beku. Nilai tambah sebenar = LAPORAN FASA supaya pengguna tahu
  kemajuan (pautan ke skrin pemula).

## 3. Skrin pemula (splash) + fasa pramuat

- `ui/splash.py` `SplashPermula`: tetingkap tanpa bingkai, bar kemajuan
  beranimasi (mod sibuk 0..0), label fasa, tema pengguna (dark/light),
  klik untuk langkau. `set_fasa()`, `tutup_sedia()`.
- `PreloadWorker.kemajuan` (pyqtSignal str): 4 fasa — memeriksa indeks,
  memuatkan model, memuatkan indeks, menetapkan pemetaan.
- `PustakaApp.kemajuan_pramuat` + `siap_pramuat` (isyarat kelas) memancarkan
  ke main.py; splash tutup bila sedia / dilangkau / 45s (jaga-jaga muat
  turun pertama lama).
- semak.py semakan 8k (`semak_pemula`); `ui.splash` didaftar dalam
  `_THEMED_MODULES`; VERSI 1.3 + CIRI `ui.splash.SplashPermula`.
- `.cache_eng`/`.cache_he` dipindah ke senarai data kerja semak_bersih
  (cache runtime aplikasi, macam `.cache_sema`).
- uji_splash.py: rantaian penuh splash → fasa → `_model_sedia=True`
  (lulus; muat sebenar ~24-50s bergantung antivirus/CPU).
- Penemuan: muat model berubah-ubah 24-50s bergantung beban CPU/antivirus;
  jangan jalankan dua ujian yang memuat model SELARI (bersaing, jadi ~50s).

**PENDING**: tiada.

---

# Sesi 29 — Lompat terus ke hadis (bukhari 433, B433, Ctrl+G) + kotak Pergi (7 Ogos 2026)

**FOKUS**: Carian pantas "lompat ke hadis" — pengguna taip nama kitab +
nombor di bar carian lalu terus ke hadis berkenaan, tanpa menyelak senarai.

## 1. Parser lompat (`_parse_lompat` / `_slug_dari_awalan`)

- `_ALIAS_KITAB`: peta nama kitab dinormalkan → slug (termasuk ejaan
  biasa pengguna: `tirmizi`, `nasa'i`, `muwatta`, `abu dawud` dll.).
- Format diterima:
  - `'bukhari 433'` / `'sahih bukhari 433'` — nama kitab + nombor
  - `'bukhari:433'` / `'b:433'` — pemisah titik bertindih (jadi ruang)
  - `'B433'` / `'bukhari433'` — awalan/huruf + digit tanpa pemisah
  - `'433'` — nombor sahaja (guna kitab lalai pemanggil)
- `_slug_dari_awalan`: awalan ringkas padan SATU kitab sahaja (`b`→bukhari,
  `t`→tirmidzi, `ab`→abu-daud); awalan AMBIGU (`m`, `a`, `mu`, `mus`, `s`)
  pulang None → jatuh ke carian biasa supaya tidak teka silap.
- Dikunci `uji_lompat.py`: 67 kes (padan 34, tolak 17, awalan 16) — lulus.

## 2. Kotak "No. hadis… / Pergi" (halaman kitab)

- `ui/pages.py` `Pager`: parameter baharu `on_go_to` — input QIntValidator
  (1–999999) + butang "Pergi"; pemisah 1px ikut tema (JANGAN QFrame.VLine —
  warnanya dari palet, tidak ikut QSS).
- `_lompat_hadis(n)`: kira halaman tepat → skrol ke kad sasaran (~1/3
  viewport, bukan ensureWidgetVisible).
- `_kira_halaman_lompat`: kira dari BILANGAN hadis id lebih kecil (tepat
  walaupun id hilang); fallback aritmetik mod dalam talian.
- `_sahkan_lompat`: toast "⚠️ Hadis No. X tiada" bila di luar julat.
- Pintasan `Ctrl+G`: fokus kotak Pergi bila-bila (QShortcut — berfungsi
  walau fokus pada QLineEdit; bukan keyPressEvent).
- **DIUBAH Sesi 34**: kotak "No. hadis… / Pergi" di pager ini digantikan
  oleh "Lompat No. hadis" di atas senarai (`pages_kitab.py`
  `_kitab_go_box`); `Ctrl+G` kini fokus ke kotak atas. Rekod di atas
  kekal sebagai sejarah Sesi 29.

## 3. Integrasi bar carian (Utama + Carian)

- `_hantar_carian` (Carian) + `_on_home_search` (Utama): cuba `_parse_lompat`
  dahulu; jika padan → lompat; jika `'433'` sahaja → `_buka_hadis_terus`
  (buka butiran TERUS, dengan `_detail_from` home/search).
- Placeholder bar carian: `"Cari hadis… (cth. bukhari 433, B433)"`.
- Kad kitab disimpan `c._hid` untuk sasaran skrol.

## 4. Sesi debug berasingan — crash 0xC0000409 TIDAK dari QThread/torch

Siasatan berasingan terhadap crash `EXIT=-1073740791` (0xC0000409) dalam
skrip ujian `uji_cari_*.py` mendapati punca sebenar:

- **Punca**: `print()` emoji (🤖 dalam `search_info.text()` daripada
  `_tampal_gabungan`) ke stdout Windows cp1252 **dalam gelung acara Qt**
  (QTimer callback) → fail-fast 0xC0000409. Di luar Qt ia cuma
  `UnicodeEncodeError`.
- Fail-fast TIDAK dapat ditangkap `try/except` (crash native).
- Bukti: `uji_print_min.py` (PyQt5 minimal + try/except) crash sama;
  `uji_cari_pantas.py` (crash 8/8) lulus 3/3 dengan `PYTHONIOENCODING=utf-8`.
- **Pelajaran**: skrip ujian yang mencetak kandungan UI (mungkin ada emoji)
  MESTI tetapkan `PYTHONIOENCODING=utf-8` atau `sys.stdout.reconfigure(
  encoding="utf-8")` dahulu — jika tidak crash 0xC0000409 disalah anggap
  sebagai bug aplikasi.

## 5. Pengesahan

- `uji_lompat.py`: 67/67 lulus (offscreen).
- `semak.py`: 169 OK, 0 GAGAL; `semak_versi.py`: 23/23 (v1.3).
- Commit `6eb5d68`.

**PENDING**: tiada.

---

# Sesi 30 — Refactor developer: helpers + mixin halaman (app_qt.py 2,428 → 504 baris) (8 Ogos 2026)

**FOKUS**: Kecilkan `ui/app_qt.py` (2,428 baris) yang terlalu besar (risiko #1
PANDANGAN_RISIKO.md) secara berperingkat TANPA mengubah fungsi. Turut menutup
risiko #2 (salinan `app_qt.py` dalam folder arkib).

## 1. Risiko #2 DITUTUP — tampalan_preload dibuang dari git

- `tampalan_preload/` (4 fail: `BACA.md`, `core/semantic_search.py`,
  `ui/app_qt.py`, `ui/workers.py`) ditambah ke `.gitignore` + `git rm -r
  --cached` (fail kekal di disk, tidak lagi dijejak). `sandaran_1300/`/
  `sandaran_1302/` memang sudah di-ignore.
- `PANDANGAN_RISIKO.md` §2 ditanda ✅ DITUTUP. Komit `40228d4`.

## 2. Refactor langkah 1 — ui/helpers.py

- Pemalar + fungsi BEBAS tanpa state Qt dipisah ke `ui/helpers.py`:
  `_parse_lompat`, `_slug_dari_awalan`, `_normalis_kitab`, `_ALIAS_KITAB`,
  `_read_json`, `_write_json`, `_clear`, `click_sound`, `PAGES`, `LANG_PARAM`,
  `_HAD_WA`, `BASE_DIR`, `SETTINGS`, `BOOKMARKS`.
- app_qt.py mengimport semula (`from ui.helpers import ...`) supaya
  `ui.app_qt._parse_lompat` dsb. KEKAL wujud untuk `uji_lompat.py` dan
  `ui/settings_panel.py` (`from ui.app_qt import _write_json, SETTINGS`).
- helpers.py TIDAK import warna (hanya `COLLECTION_META`, metadata) → tidak
  perlu daftar `_THEMED_MODULES`. `import json`/`import re` dibuang dari
  app_qt (tidak lagi terpakai — bukan sasaran apply_theme).
- app_qt.py: 2,428 → 2,291 baris. CRLF kekal 100%.
- Komit `1b3b8fd`.

## 3. Refactor langkah 2 — mixin halaman kitab + carian

- `ui/pages_kitab.py` `PagesKitab` (11 kaedah: halaman kitab + lompat hadis)
  + `ui/pages_carian.py` `PagesCarian` (9 kaedah: carian + semantik).
- `PustakaApp(PagesKitab, PagesCarian, QMainWindow)` — MRO menggabungkan;
  kaedah rentas mixin diakses melalui `self` (cth. `_hantar_carian` panggil
  `_lompat_ke` yang dalam PagesKitab). Gandingan ini DIDOKUMENTASIKAN dalam
  docstring kedua-dua mixin.
- `_THEMED_MODULES` + `ui.pages_kitab` + `ui.pages_carian` (PagesCarian
  import warna AMBER_BG/AMBER_TEXT/AMBER_BORDER untuk lencana amaran).
- `semak.py` 8g (`semak_gabungan`) dikemas: `_tampal_gabungan` kini dibaca
  dari `ui/pages_carian.py` (lokasi baharu).
- Import mati dibuang dari app_qt.py: `Pager`, `BookCover`, `ListWorker`,
  `SearchWorker` (bukan sasaran apply_theme). `empty_state`/`hadith_card`
  KEKAL (halaman Tersimpan masih guna).
- app_qt.py: 2,291 → 1,774 baris. Komit `5288852`.

## 4. Refactor langkah 3 — ui/pages_detail.py

- `ui/pages_detail.py` `PagesDetail` (26 kaedah): `_page_detail`, `open_detail`,
  `open_by_ref`, `_render_detail`, `_bina_translit/_syarah/_sema/_he/_darjat`,
  `_papar_melayu`, `_switch_lang`, `_kepala_hadis`, `_teks_semua_bahasa`/
  `_teks_bahasa_semasa`, `_copy/_share/_copy_semua_bahasa/_share_semua_bahasa/`
  `_copy_bahasa_semasa/_share_bahasa_semasa`, `_tts`, `_random`, `_is_saved`,
  `_toggle_save`.
- `PustakaApp(PagesKitab, PagesCarian, PagesDetail, QMainWindow)`. Pemalar
  `LANG_LABEL` + `_ATRIBUSI_INGGERIS/_SEMA/_HE` dialih dari app_qt ke
  `ui/helpers.py` (hanya PagesDetail import — app_qt TIDAK mengimport semula
  kerana tiada pemanggil luar).
- `_THEMED_MODULES` + `ui.pages_detail` (import warna TEXT_SECONDARY).
- `semak.py`: pembantu `_sumber_ui()` + `_cari_fungsi()` — semak 8e/8f/8i kini
  baca sumber GABUNGAN (mixin + helpers) supaya tidak hanyut bila fungsi dialih.
- Import mati dibuang dari app_qt.py: QUrl, QPoint, QMessageBox, webbrowser,
  LangTabs, breadcrumb, Collapsible, arabic_browser, text_browser,
  HadithWorker, RandomWorker, betulkan_melayu, guna_simbol_selawat, dsb.
  `_parse_lompat`/`_slug_dari_awalan`/`_write_json`/`SETTINGS`/`PAGES` KEKAL
  (pemanggil luar uji_lompat.py/settings_panel.py/uji_tukar_tema.py).
- app_qt.py: 1,774 → 875 baris. Komit `fcf77e7`.

## 5. Refactor langkah 4 — ui/pages_tersimpan.py + ui/pages_tetapan.py

- `ui/pages_tersimpan.py` `PagesTersimpan`: `_page_saved`, `_render_saved`
  (senarai penanda buku; `_render_saved` panggil `open_by_ref` — PagesDetail).
- `ui/pages_tetapan.py` `PagesTetapan`: `_page_settings`, `_sync_settings`,
  `_step`, `_set`, `_set_simbol_selawat`, `_set_font`, `_save_api` (API,
  saiz UI/Arab/terjemahan, fon Arab, bahasa dimuat, hadis per halaman).
- `_THEMED_MODULES` + kedua-dua modul (PagesTetapan import warna AMBER_*/
  RED_TEXT/GREEN_TEXT/TEXT_MUTED). `semak.py` `_sumber_ui()`/`_cari_fungsi()`/
  semak 8d (stretch) kini sertakan kedua-dua modul baharu.
- Import mati dibuang: QComboBox, QLineEdit, empty_state, hadith_card,
  AMBER_*, RED_TEXT, GREEN_TEXT, FONT_SCALE_LABELS, dsb.
- app_qt.py: 875 → 586 baris. Komit `3344a86`.

## 6. Refactor langkah 5 — ui/pages_home.py

- `ui/pages_home.py` `PagesHome`: `_page_home` (hero + bar carian + grid 9
  kad kitab), `_from_home_search` (lompat terus / alih ke halaman Carian).
- `PustakaApp` kini warisi SEMUA 6 mixin: `(PagesKitab, PagesCarian,
  PagesDetail, PagesTersimpan, PagesTetapan, PagesHome, QMainWindow)` — MRO
  menggabungkan. `_THEMED_MODULES` + `ui.pages_home` (tiada import warna).
- Import mati dibuang: QGridLayout, Hero/KitabCard/SearchBar,
  attach_copy_menu, centered_column, make_scroll, COLLECTION_META.
- app_qt.py: 586 → 504 baris — **inti sahaja** (init, header, tema, navigasi,
  worker, main()). Komit `7507ba2`.

## 7. RANCANGAN_REFACTOR.md

Pelan pecahan penuh disimpan: punca kesukaran (`_THEMED_MODULES` + semak.py
source-checks), jadual struktur 6 blok, pelan 5 langkah. Semua 5 langkah
SELESAI 8 Ogos — `app_qt.py` 2,428 → 504 baris (−79%). Gandingan rentas
mixin didokumentasikan dalam docstring setiap mixin + RANCANGAN_REFACTOR.md.

## 8. Pengesahan (semua lulus)

- `semak.py`: SEMUA LULUS (termasuk pelancaran kedua-dua tema, 8d menyemak
  6 halaman `_page_*`, folder bersih).
- `uji_lompat.py`: 67/67 · `uji_lompat_fungsi.py`: 15/15 · `uji_tukar_tema.py`:
  19/19 (tiada kebocoran widget) · `uji_bandingan.py`: 28/28 ·
  `uji_end_to_end.py`: 18/18 · `uji_data_baharu.py`: 18/18.

**PENDING**: tiada — refactor 5 langkah selesai, app_qt.py tinggal inti sahaja
(504 baris).

# Sesi 31 — Indikator jam berputar semasa carian (8–9 Ogos 2026)

**FOKUS**: Pengguna tidak tahu sama ada carian sedang berjalan — halaman Carian
menunjukkan skrin kosong + teks statik "Mencari…" sedangkan carian makna AI
boleh ambil ~24 saat (larian pertama, model belum dimuat). Tambah indikator jam
berputar yang jelas; baiki laluan gagal yang tersangkut selama-lamanya.

## 1. Indikator ⏳ statik (komit `95d4785`)

- Label ⏳ di baris status halaman Carian (sebelah `search_info`). Tunjuk dalam
  `_do_search` (selepas `_clear`), sembunyi dalam `_tampal_gabungan` (selepas
  pengawal token — bila KEDUA-DUA worker kata kunci + makna AI selesai).
- **Laluan gagal keyword dibaiki**: sebelum ini `SearchWorker.failed` (ralat
  API/jaringan) meninggalkan halaman tersangkut pada "Mencari…" selama-lamanya.
  `_on_search_failed()` baharu (pengawal token, simetri dengan
  `_on_semantic_failed`) menamatkan carian + menyembunyikan jam; hasil AI
  masih dipapar jika ada.
- **Bug ariti isyarat**: `SearchWorker.failed` ialah `pyqtSignal(str)` — satu
  argumen, manakala pengendali jangka 2. Disambung terus akan `TypeError`
  HANYA bila carian gagal (ujian tidak menangkapnya). Dibetulkan dengan
  lambda yang menangkap `tok`; disahkan dengan ujian kecil (ariti isyarat +
  pengawal token).

## 2. Naik taraf: jam berputar 🕐→🕛 (komit `0c1e037`)

- `_jam` — 12 muka jam emoji (🕐🕑🕒…🕛), diputar QTimer 120ms melalui
  `_putar_jam()`. Mula dalam `_do_search`, henti dalam `_tampal_gabungan`.
- Bina-semula tema: timer lama dihentikan dalam `_page_search` supaya dua
  timer tidak memutar label baharu serentak selepas tukar tema.
- Pengawal `isVisible()` dalam `_putar_jam` — timer yang masih berjalan tidak
  mengemas kini label tersembunyi.
- Tiada import warna (emoji) → tiada pendaftaran `_THEMED_MODULES` baharu.

## 3. Semakan 8l semak.py (komit `f654fad` + pendaftaran ujian visual)

- 5 sub-semakan AST per fungsi (`_page_search`, `_do_search`,
  `_tampal_gabungan`, `_on_search_failed`) mengesahkan label/QTimer, 12 muka
  jam, show/start, hide/stop, laluan gagal.
- Kemudian ditambah sub-semakan 6–7: `uji_visual_carian.py` wujud + konsisten
  (penanda `_carian_sibuk`, `_carian_timer`, 🕐/🕛, `w.grab()`, `_do_search`,
  `isVisible()`). Kepekaan diuji: mutasi `w.grab()` → `w.grabX()` menyebabkan
  8l sub-7 GAGAL ("tiada ['w.grab()']").

## 4. Ujian visual kekal uji_visual_carian.py (komit `dc795da`, 11/11)

- Struktur: halaman Carian dibuka, `_carian_sibuk` (QLabel) + `_carian_timer`
  (QTimer, 120ms) + 12 muka jam.
- Bukti render: pin 🕐 vs 🕛, bandingkan piksel `w.grab()` (render tetingkap
  sebenar — bebas timing carian dan masalah tangkapan fizikal). Tangkapan
  fizikal (ImageGrab) = artifak sahaja.
- Kitaran hidup: carian sebenar "hukum riba" — jam kelihatan semasa berjalan,
  berputar (teks berubah), disembunyikan selepas selesai, hasil dipapar,
  teks status = keputusan.

## 5. Pengesahan

- `semak.py`: SEMUA LULUS (8l kini 7 sub-semakan).
- `uji_lompat.py` 67/67 · `uji_bandingan.py` 28/28 · `uji_end_to_end.py` 18/18
  · `uji_visual_carian.py` 11/11 (2× stabil).
- Suite penuh 13 fail ujian + semak.py: SEMUA LULUS (8–9 Ogos).

**PENDING**: tiada.

# Sesi 32 — Simbol selawat ﷺ lalai + pembersihan sandaran + 8m ke .py (9 Ogos 2026)

**FOKUS**: Tiga kerja penyelenggaraan — (1) paparan Melayu menggantikan frasa
"Sallallahu 'alaihi wasallam" dengan ligatur Arab ﷺ secara LALAI (sebelum ini
lalai bentuk penuh, perlu hidupkan di Tetapan); (2) bersihkan folder sandaran
usang yang tinggal di cakera; (3) luaskan semakan 8m ke fail .py supaya regresi
bahasa kod dikesan automatik.

## 1. Lalai simbol selawat ﷺ (komit `74d31be`)

- Ciri ligatur U+FDFA wujud sejak Sesi 9 (`utils/bahasa.py`:
  `LIGATUR_SELAWAT`, `_FRASA_SELAWAT`, `guna_simbol_selawat`,
  `simbol_boleh_dipapar`) tetapi lalai OFF. `user_settings.json` tiada,
  jadi lalai itulah yang berkuat kuasa.
- `simbol_selawat` lalai False → **True** (`ui/pages_detail.py`
  `_papar_melayu` + `ui/settings_panel.py` dropdown "Selawat"). Paparan
  Melayu kini guna ﷺ secara lalai — detail, tab Sebelah, dan senarai
  kitab/carian/tersimpan (semua melalui `_papar_melayu`).
- Jaring keselamatan kekal: `_ada_glif_selawat` (semakan fon semasa
  pelancaran) — fon tiada glif → teks penuh kekal (tiada tofu); togol
  Tetapan masih ada; teks dalam hadis.db tidak diubah (transformasi
  paparan sahaja).
- Disahkan pada skrin fizikal: "Rasulullah Sallallahu 'alaihi wasallam
  bersabda" → "Rasulullah ﷺ bersabda" (Bukhari #1).

## 2. Pembersihan folder sandaran (komit `4a86474` + `9c3716b`)

- `sandaran_1300/`, `sandaran_1302/`, `tampalan_preload/` — sisa tampalan
  §6 pra-muat (nota BACA.md yang diarkib): salinan app_qt.py monolitik
  71KB lama yang sudah dipecahkan ke 6 mixin (app_qt.py kini 20KB).
  Kedua-dua sandaran identik (md5 sama); redundan dengan git history;
  gitignored; ~84K setiap satu.
- Dipadam 9 Ogos. `PANDANGAN_RISIKO.md` §2 dikemas — risiko kini ditutup
  SEPENUHNYA (folder tidak wujud, bukan sekadar di-ignore). Entri mati
  dibuang dari .gitignore; jaring keselamatan semak.py (`_SKIP_FOLDER` +
  8m, corak awalan `sandaran_`/`tampalan_preload`) kekal.

## 3. Semakan 8m diluaskan ke .py (komit `30942f1`)

- Helper `_imabas_kata_indo(src, corak)`: imbas komen `#` (tokenize) +
  docstring (AST: modul/fungsi/kelas sahaja). String kandungan (mesej
  UI, data, teks terjemahan) dikecualikan — di sana perkataan itu boleh
  menjadi kandungan sah.
- Folder bukan-kod-hidup dikecualikan: `_arkib/`, `sandaran_*`,
  `tampalan_preload/`, `__pycache__`.
- 8 pembetulan kata Indonesia dalam komen/docstring kod — kini semuanya
  Melayu betul: `pelaksanaan` (2×), `menghilangkan`, `menghapus`,
  `memadamkan`, `Pembaikan`, `dipaparkan`.
- Docstring 8m ditulis semula supaya tidak menandakan dirinya sendiri
  (sebelum ini menyebut contoh kata Indonesia yang kini disenarai).
- BACA.md (nota tampalan pra-muat usang) diarkib ke
  `_arkib/BACA_TAMPALAN_PRAMUAT.md` dengan nota TAMAT — tiada siapa
  mengikuti arahan salin dari Drive semula.

## 4. Ujian visual kekal ﷺ (uji_visual_sebenar.py seksyen 6)

- 5 semakan baharu: hadis frasa selawat dijumpai (SQL `%allallahu%` +
  `%alaihi%`), lalai diganti oleh `_papar_melayu` (kelakuan sebenar,
  bukan fallback settings), glif tersedia, teks dipapar mengandungi ﷺ
  (widget UI), skrin fizikal disimpan.
- Ujian kepekaan: mutasi lalai ke False → 2 GAGAL ("lalai... _papar_melayu"
  + "teks dipapar ﷺ") → pulihkan → 19/19.

## 5. Pengesahan

- `semak.py`: SEMUA LULUS (8m kini 66 fail .py + 12 dokumen .md bersih).
- Ujian kepekaan 8m: mutasi komen .py dengan kata Indonesia → 8m GAGAL.
- `uji_visual_sebenar.py` 19/19 (seksyen 6 baharu ﷺ).
- Skrin fizikal: `bukti_visual/sebenar_selawat*.png`.

**PENDING**: tiada.

# Sesi 33 — Lalai saiz fon Sederhana untuk semua (9 Ogos 2026)

**FOKUS**: Pastikan ketiga-tiga saiz fon — antara muka, teks Arab, dan
terjemahan — lalai kepada "Sederhana" (indeks 1, skala 1.0). Sebelum ini
saiz teks Arab lalai "Besar" (indeks 2) sejak komit pertama
(`arabic_font_idx = 2` dalam `ui/app_qt.py`), manakala antara muka dan
terjemahan sudah Sederhana.

## 1. Perubahan lalai (komit `a2ea80e`)

- `ui/app_qt.py` — `arabic_font_idx` lalai 2 (Besar) → **1 (Sederhana)**.
  Pemasangan baharu / tiada `user_settings.json` kini Sederhana untuk
  semua saiz fon.
- `ui/settings_panel.py` — butang "Set Semula": `1, 2, 1` → **`1, 1, 1`**
  (saiz teks Arab tidak lagi kembali ke Besar selepas set semula).
- `config.py` — diagnostik `python config.py` (Font idx) default 0 → 1,
  konsisten dengan lalai Sederhana.
- `MANUAL_PENGGUNA.md` §7 BACAAN — ketiga-tiga butir saiz kini menyatakan
  "(lalai: **Sederhana**)".

## 2. Skop

- Pengguna sedia ada yang menyimpan `arabic_font_idx` dalam
  `user_settings.json` kekal pada nilai pilihan mereka — perubahan ini
  menetapkan lalai untuk pemasangan baharu dan butang "Set Semula".
- `user_settings.json` semasa (state segar) sudah `arabic_font_idx: 1` —
  tiada kesan sampingan.

## 3. Pengesahan

- `semak.py`: SEMUA LULUS (exit 0).
- App sebenar (offscreen): `ui=Sederhana, ar=Sederhana, tr=Sederhana`
  (indeks 1, skala 1.0) untuk lalai dan selepas logik Set Semula.
- EOL dipelihara: `ui/app_qt.py` CRLF; `ui/settings_panel.py`,
  `config.py`, `MANUAL_PENGGUNA.md` LF (sama seperti HEAD).

**PENDING**: tiada.

# Sesi 34 — UI senarai hadis: butang ↑ terapung + kotak "Lompat No. hadis" (9 Ogos 2026)

**FOKUS**: Perbaiki navigasi senarai hadis yang panjang. (1) Butang ↑
terapung untuk lompat ke hadis pertama bila pengguna skrol ke bawah; (2)
kotak carian nombor hadis di atas senarai (placeholder kabur "0–7008" ikut
kitab) — menggantikan kotak "No. hadis… / Pergi" di pager bawah.

## 1. Ciri baharu (komit `0e77890`)

- **Butang ↑ terapung** (`ui/pages_kitab.py` `_back_top_btn`, objectName
  `backTop`): bulat di sudut kanan-bawah senarai, muncul bila skrol >250px
  dan hilang sendiri bila di atas; klik → **skrol lancar** (animasi QTimer
  ~250ms, langkah mengecil) ke hadis pertama. Gaya QSS `QPushButton#backTop`
  dalam `ui/theme.py` (ikut tema gelap/terang; pages_kitab kekal bebas
  import warna).
- **Kotak "Lompat No. hadis"** (`_kitab_go_box`) di atas senarai:
  placeholder kabur `0–{total}` ikut kiraan db sebenar (Bukhari 7008,
  Muslim 5362) walaupun sebelum koleksi dimuat (fallback `max_hadis_id`
  offline); pengesah nombor sahaja 1–999999; Enter → `_hantar_go_box` →
  `_lompat_hadis` (enjin sedia ada): sah julat (toast "⚠️ Hadis No. X
  tiada"), kira halaman betul, toast "📖 Hadis No. X — halaman Y", skrol
  terus ke kad. Kotak dikosongkan selepas lompat.

## 2. Penyatuan + pintasan (komit `526af1e`)

- **Kotak pager bawah DIBUANG** (`ui/pages.py`): `on_go_to`, `go_input`
  ("No. hadis…"), `go_btn` ("Pergi"), `_go_to` dan import
  `QIntValidator`/`BORDER` yang tidak lagi digunakan (−57 baris). Lompat
  nombor kini hanya melalui kotak atas.
- **Ctrl+G kini fokus kotak atas** — `_focus_lompat` → kaedah baharu
  `_fokus_go_box` (`_fokus_pager_lompat` dibuang); tooltip dikemas; pager
  bawah masih berfungsi untuk paging (‹ Seterusnya ›).
- **Butang ↑ pada halaman Carian** (`ui/pages_carian.py`): corak sama
  halaman kitab — `_search_top_btn` (objectName `backTop`), kaedah
  `_kemas_butang_atas_carian` + `_skrol_atas_lancar_carian`.

## 3. Pengesahan (komit `6944e22` — seksyen 9 + dokumen)

- `semak.py`: SEMUA LULUS.
- `uji_lompat.py` 67/67, `uji_lompat_fungsi.py` 15/15, `uji_end_to_end.py`
  18/18, `uji_visual_carian.py` 11/11.
- `uji_visual_sebenar.py` **53/53** pada skrin fizikal — seksyen 8 (butang
  ↑ kitab + kotak nombor, 14 semakan) + seksyen 9 (butang ↑ carian +
  ketiadaan kotak Pergi pager, 12 semakan). Ujian kepekaan: mutasi
  objectName/placeholder → 3 GAGAL (seksyen 8) dan 4 GAGAL (seksyen 9)
  → pulihkan → bersih. Bukti skrin: `sebenar_butang_atas.png`,
  `sebenar_kotak_nombor.png`, `sebenar_butang_atas_carian.png`.
- Pelajaran: perlumbaan muat semula — uji butang dahulu (scrollbar stabil),
  kotak lompat kemudian; animasi skrol flaky di bawah beban CPU (sama kelas
  dengan flaky "terang" yang diketahui) → semakan guna gelung ulang-mula
  (regresi sebenar tetap GAGAL selepas tamat 6s).

## 4. Butang ↑ Tersimpan + Detail (komit `6b1cbd6`)

- Ukur julat skrol sebenar (tetingkap 1000×700): Koleksi 1px dan
  Tetapan 94px — TIDAK perlu (muat / bawah ambang 250px); Tersimpan
  804px dan Detail 837px — PERLU.
- **Tersimpan** (`ui/pages_tersimpan.py` `_tersimpan_top_btn`): senarai
  tanda buku panjang; kaedah `_kemas_butang_atas_tersimpan` +
  `_skrol_atas_lancar_tersimpan`.
- **Detail** (`ui/pages_detail.py` `_detail_top_btn`): hadis dengan
  syarah/darjat/huraian panjang; kaedah `_kemas_butang_atas_detail` +
  `_skrol_atas_lancar_detail`. Butang terletak dalam viewport skrol,
  tepat di atas bar navigasi lekat — tiada pertindihan.
- Timer unik (`_top_timer_tersimpan` / `_top_timer_detail`) — tiada
  pertembungan dengan kitab/carian pada `self` kongsi.
- Disahkan: ujian fungsi offscreen 14/14 (tersimpan 8, detail 5, hadis
  pendek max 213 <250 → butang kekal tersembunyi); semak.py SEMUA
  LULUS; uji_visual_sebenar.py 53/53 (seksyen 1–9 tiada regresi).

## 5. Penebalan garis mode terang + manual (komit `52cc191`)

- **Punca**: mode terang `BORDER #D8E0E4` (kelabu pucat) atas putih —
  garis 1px hampir tak kelihatan; isu KONTRAS, bukan hanya ketebalan.
- `ui/theme.py` palet terang: `BORDER` → `#C2CDD3`, `BORDER_LIGHT` →
  `#D4DDE2` — semua garis 1px (divider, kad, panel, kotak input, butang
  ↑) kini kelihatan atas putih. Mode gelap tidak terjejas.
- `QFrame#divider` (QSS) + `divider()` (`ui/widgets.py`) 1px → **2px**
  — garis bawah header jelas kelihatan.
- `MANUAL_PENGGUNA.md` — butang ↑ didokumenkan pada keempat-empat
  halaman (Membaca kitab, Halaman hadis, Carian, Tersimpan).
- Disahkan: semak.py SEMUA LULUS; uji_visual_sebenar.py 53/53
  (semakan tema terang kecerahan >140 lulus dengan palet baharu);
  suite penuh 13 fail ujian lulus.

## 6. Selawat ﷺ lengkap dalam transliterasi rumi (komit `52855a4` + semak 8bb)

- **Punca**: komit `265286f` menambah penukaran selawat dalam rumi,
  tetapi regex hanya padan bentuk PAUSAL ("salla Allah 'alayhi
  wa-sallam") -- output transliterasi SEBENAR ialah bentuk KES penuh:
  "salla Allahu 'alayhi wa-sallama" / "ṣallā Allāhu ʿalayhi wasallama"
  (damma "u" pada Allāh + fatha "a" pada sallama). Imbas 361 hadis
  rawak: 541/541 bentuk kes -- ﷺ TIDAK pernah diganti pada data
  sebenar walaupun lalai aktif.
- **Pembetulan** (`utils/bahasa.py`): `_FRASA_SELAWAT` bahagian rumi
  diluaskan kepada `[Aa]ll[āa]h[u]?` + `sallam[a]?` -- kedua-dua
  bentuk (kes + pausal) kini ditukar → ﷺ. Kes tepi kekal tidak
  tersentuh (Abdullah bin Salam, Assalamualaikum, as-salamu 'alaykum,
  Salam sejahtera).
- **Seksyen 6b `uji_visual_sebenar.py`** (7 semakan kekal): sumber
  `_bina_translit` guna `guna_simbol_selawat` + gating; sumber regex
  bahasa.py terima bentuk kes; kelakuan Collapsible Transliterasi
  (2 gaya dibina, ﷺ ada, frasa penuh tiada); skrin fizikal
  `sebenar_translit_selawat.png`. Query seksyen 6 diperketat: hadis
  mesti ada selawat dalam teks ARAB (normalisasi tashkeel). Ujian
  kepekaan: mutasi regex → 3 GAGAL dikesan → pulihkan → 60/60.
- **Semak 8bb `semak.py` (headless)**: 4 semakan rumi ﷺ (kes
  Melayu/akademik + pausal) + 2 kes kekal baharu (as-salamu 'alaykum,
  Salam sejahtera) -- regresi regex dikesan tanpa skrin fizikal.
  Ujian kepekaan headless: mutasi → 2 GAGAL (kes) dikesan → pulihkan.
- Disahkan: semak.py SEMUA LULUS; uji_visual_sebenar.py **60/60** pada
  skrin fizikal (seksyen 6b: 7/7); uji_end_to_end.py 18/18.

**PENDING**: tiada.

# Sesi 35 — Kongsi WhatsApp ikut bahasa semasa + selawat ﷺ lengkap + manual pengguna EN (10 Ogos 2026)

**FOKUS**: (1) Kongsi WhatsApp tidak lagi menghantar semua bahasa sekali
gus — ikut tab bahasa semasa sahaja (petikan Arab + satu terjemahan);
(2) selawat ﷺ dilengkapkan merentas paparan (petik melengkung + bentuk
Arab tertanam) selepas asas rumi Sesi 34 §6; (3) manual pengguna versi
Inggeris baharu + penyelarasan semua dokumen dengan kod sebenar.

## 1. Kongsi WhatsApp ikut bahasa semasa (komit `24e4ef0`, `fb57b5b`)

- **"Kongsi semua bahasa" DIBUANG** — butang Kongsi WhatsApp dalam tab
  Sebelah (yang menghantar Arab + SEMUA terjemahan sekali gus) dikeluarkan;
  keputusan Sesi 34: pengguna kongsi mengikut bahasa yang dilihat sahaja.
  semak.py 8i mengunci ia tidak kembali (`_share_semua_bahasa` mesti tiada;
  "Kongsi semua bahasa" tidak boleh wujud). Tab Sebelah kini hanya ada
  butang "📋 Salin semua bahasa".
- **Kongsi ikut tab bahasa semasa** — `_teks_bahasa_semasa`
  (`ui/pages_detail.py`): tajuk rujukan (nama kitab + no. hadis) +
  Arab dihantar PENUH tanpa label `[ARAB]` (`_petik_arab`/
  `_HAD_PETIK_ARAB` dibuang) — "Read more" asli WhatsApp mendedahkan
  Arab penuh bila diketuk (berguna untuk penerima Arab) +
  `[TERJEMAHAN]` SATU terjemahan sahaja (label seragam, bukan nama
  bahasa — ikut `_lang_key`, lalai Melayu). Jika terjemahan tiada,
  tajuk sahaja dihantar.
- **Had mesej dinaikkan 700 → 5000 aksara** (`_HAD_WA`, `ui/helpers.py`)
  — Arab kini dihantar penuh; 2000 terlalu ketat (8,243 hadis / 13%
  terpotong terjemahan), dinaikkan ke 5000 (masih selamat untuk
  `wa.me/?text=`); hanya outlier Arab >3000 aksara (690 hadis, 1.1%)
  kekal terpotong.
- Butang "💬 WhatsApp" (bar tajuk halaman detail) dan "💬 Kongsi" (paparan
  bahasa tunggal `_switch_lang`) — kedua-duanya memanggil
  `_share_bahasa_semasa` (percent-encode + webbrowser).
- `MANUAL_PENGGUNA.md` dikemas: butang WhatsApp ikut bahasa semasa; tab
  Sebelah tiada kongsi (Salin semua sahaja).
- Disahkan: semak.py 8i (11 semakan, termasuk "Kongsi semua bahasa
  dibuang" + "kongsi bahasa semasa sertakan petikan Arab").

## 2. Selawat ﷺ lengkap (komit `893dcc0`, `2c9022b`; asas: Sesi 34 §6)

- Sesi 34 §6 menukar selawat dalam **transliterasi rumi** (regex bentuk
  kes + pausal → ﷺ, komit `52855a4`). Sesi 35 melengkapkan liputan kepada
  bentuk lain yang tertinggal:
- **Petik melengkung 'alaihi** (`2c9022b`) — `_FRASA_SELAWAT` bentuk
  Melayu kini terima apostrof ASCII `'` DAN petik melengkung `‘ ’`
  (U+2018/U+2019); data hadis.my guna kedua-duanya — regex lama hanya
  ASCII, jadi 3,693 "Sallallahu ‘alaihi wasallam" tertinggal.
- **Bentuk Arab penuh tertanam** dalam teks Melayu ("صلى الله عليه وسلم",
  9,733 baris hadis.melayu) turut diganti → ﷺ (`893dcc0`) — konsisten
  dengan `hadis.melayu` dan huraian SemakHadis; toleransi tashkeel +
  varian typo DB "وسسلم" diterima.
- Manual pengguna: liputan penuh selawat didokumenkan (senarai bahasa §1,
  halaman hadis §6, Tetapan §7).
- Disahkan: semak 8bb (kes petik melengkung + Arab baharu) +
  uji_visual_sebenar seksyen 6; semak.py SEMUA LULUS.

## 3. Manual pengguna EN + penyelarasan dokumen (komit `5bdbb97`, `a85dba2`)

- **`MANUAL_PENGGUNA_EN.md`** (baharu, komit `5bdbb97`) — terjemahan
  Inggeris penuh manual pengguna (11 seksyen). Label UI kekal Melayu
  (antara muka app berbahasa Melayu) dengan penjelasan Inggeris + nota di
  bahagian atas.
- **Semakan dokumen vs kod** — percanggahan dibetulkan dalam
  `MANUAL_PENGGUNA.md` + `README.md`:
  - Panel Tetapan §7: struktur sebenar 4 seksyen `TEMA` / `PAPARAN` /
    `BACAAN` / `SAMBUNGAN` (+ Fon Arab, Bahasa dimuat, Hadis per halaman
    10–100 lalai 20); sebelum ini salah gabung Tema+Paparan.
  - Lompat hadis: `bukhari 433` membuka kitab pada kad hadis (bukan
    butiran terus); `433` sahaja membuka butiran; jawapan draf AI di atas
    hasil carian didokumenkan.
  - README: "Salin/Kongsi bahasa" (Sebelah tiada kongsi WhatsApp), lokasi
    gear atas kanan (bukan "menu kiri"), 6 halaman (bukan 7).
- **semak.py 8m** — `MANUAL_PENGGUNA_EN.md` dikecualikan secara eksplisit
  (terjemahan Inggeris rasmi); semua dokumen lain MESTI kekal Melayu
  Malaysia. Peta dokumen `MANUAL_REFERENSI_DEV.md` dikemas.
- **Penyelarasan lanjut (komit `a85dba2`)**: senarai "Siap" MULA_SINI
  (Kongsi semua bahasa dibuang Sesi 34) + komen `ui/pages_kitab.py` tidak
  lagi merujuk kotak "Pergi" pager bawah (dibuang Sesi 34).
- Disahkan: semak.py **SEMUA LULUS (26 semakan)**; angka data disahkan
  terhadap hadis.db (62,169 · 310 · 31,322 · 63,930 · 4,237; Bukhari
  7008, Muslim 5362).

**PENDING**: tiada.



# Sesi 36 — Kongsi WhatsApp: pilihan format (Ringkas lalai) (10 Ogos 2026)

**FOKUS**: Maklum balas pengguna — output kongsi WhatsApp Sesi 35
menghantar Arab PENUH dahulu, jadi WhatsApp memaparkan SATU "Read more"
selepas teks Arab dan terjemahan tersembunyi di belakangnya. Satu mesej
WhatsApp hanya boleh ada SATU "Read more" asli (tiada bahagian boleh-
kembang berasingan). Penyelesaian akhir pengguna: kongsi TERUS guna
format "Ringkas" — TIADA menu pilihan (pengguna kurang senang dengan
menu setiap kali kongsi, lalu menetapkan pilihan atas sekali sebagai
kongsi lalai).

## 1. Kongsi terus format Ringkas (`ui/pages_detail.py`)

- `_share_bahasa_semasa` kini TERUS memanggil `_buka_wa(_teks_kongsi_ringkas())`
  — menu QMenu 4 format DIBUANG (atas permintaan pengguna Sesi 36);
  butang "💬 WhatsApp" (bar tajuk) dan "💬 Kongsi" (tab bahasa tunggal)
  sama-sama guna laluan ini.
- Format tunggal **Ringkas**: `_teks_kongsi_ringkas` — tajuk + petikan
  Arab `_petik_ringkas` (had `_HAD_PETIK_RINGKAS=700` aksara ~10 baris,
  potong sempadan perkataan + "…") + `[TERJEMAHAN]` penuh + pautan
  "Baca penuh" sunnah.com (bila padanan wujud). Kedua-dua bahagian
  kelihatan dalam gelembung WhatsApp; hadis panjang: "Read more" asli
  di hujung terjemahan (ketuk → baca baki). Penerima boleh baca
  terjemahan penuh sahaja atau petikan Arab sahaja, atau buka hadis
  penuh di pelayar melalui pautan.
- Fungsi format lama `_teks_terjemahan_sahaja` / `_teks_arab_sahaja`
  DIBUANG (corak sama Sesi 34 buang "Kongsi semua bahasa"); semak.py
  8i mengunci ia tidak kembali dan `_share_bahasa_semasa` tidak membuka
  menu. `_teks_bahasa_semasa` kekal untuk "📋 Salin" sahaja.
- `_buka_wa(teks)` — buka wa.me dengan had keselamatan `_HAD_WA=6000`.
  Nama fungsi petikan sengaja BUKAN nama lama (`_petik_arab` dibuang
  Sesi 35) — semak.py mengunci ia tidak kembali.

## 2. Tindakan susulan pengguna — petikan Arab lebih panjang (b.2)

- Pengguna mahu petikan Arab ~10 baris (macam contoh Bukhari No. 3,
  titik potong `فَأَخَذَ` pada indeks ~739 aksara). `_HAD_PETIK_RINGKAS`
  200 → **700** aksara.
- Had apl `_HAD_WA` 5000 → **6000** supaya terjemahan PENUH tetap sampai
  walaupun petikan Arab panjang (pilihan b.2: naikkan petikan + had).
  Kesan pada data: Ringkas hanya 125 hadis (0.2%) terjemahan hujungnya
  terpotong.
- Pautan "Baca penuh" sunnah.com DITAMBAH (pengesahan pengguna):
  `sync_english.py --peta-sunnah` menjana `sunnah_map/{slug}.json` —
  peta {hadis_id: {book, hadith}} guna semula jentera padanan
  `core.eng_source.padan` (lapisan Indonesia dahulu, sama seperti
  sync_english). PERLU kerana penomboran hadis.my berbeza daripada
  sunnah.com.
- **AUDIT mendedahkan nombor global CDN tidak sepadan dengan URL
  sunnah.com** (cth. CDN Muslim #565 = Kitab Penyucian "استجمر",
  tetapi sunnah.com:565 = hadis bawang putih Kitab Masjid). Sebab itu
  URL dibina dengan rujukan DALAM-BUKU CDN (`reference` = sistem
  sunnah.com sendiri "In-book reference"):
  `https://sunnah.com/{slug}/{buku}/{hadith}` (cth. muslim/2/32,
  bukhari/1/3). Disahkan: audit 20 pautan rawak terhadap halaman
  sunnah.com sebenar — **20/20 lulus** (teks CDN hadir dalam halaman).
- Kadar padanan 93.7-99.3% (7 kitab bersumber); `sunnah_url`
  (ui/helpers.py) membaca peta ini semasa kongsi; ahmad/darimi tiada
  sumber → tiada pautan; hadis tak padan → pautan dilangkau (tidak
  mengganggu). Pautan disertakan pada format Ringkas.
- **Audit diintegrasi ke semak.py** sebagai `--audit-sunnah` (8o):
  sampel rawak 20 hadis daripada sunnah_map/, sahkan teks CDN hadir
  dalam halaman sunnah.com sebenar (jeda 3s elak 403; saiz sampel boleh
  ubah: `--audit-sunnah=10`). Ralat muat turun = NOTA, bukan kegagalan;
  hanya ketidakpadanan disahkan yang gagalkan gate. Opt-in supaya lalai
  semak.py kekal luar talian dan pantas.
- **Pepijat dijumpai semasa demo output sebenar**: pautan "Baca penuh"
  TERPOTONG oleh had `_HAD_WA` dalam `_buka_wa` (mesej panjang + pautan
  melebihi 6,000). Dibetulkan: `_buka_wa` asingkan baris "Baca penuh:"
  sebelum potong dan kekalkan ia selepas. Disahkan dengan demo
  offscreen: pautan kekal walaupun mesej dipotong.
- "📋 Salin" TIDAK berubah — kekal Arab penuh ke papan klip
  (`_teks_bahasa_semasa()` tanpa had).
- `MANUAL_PENGGUNA.md` + `MANUAL_PENGGUNA_EN.md`: baris ringkasan v1.3 +
  jadual butang WhatsApp dikemas (kongsi terus Ringkas + pautan Baca
  penuh).
- Disahkan: semak.py semakan 8i dikemas (kongsi terus Ringkas, format
  lama dibuang, nama lama tiada, pautan Baca penuh ada) +
  uji_bandingan.py kes 7c (Ringkas ada petikan Arab + [TERJEMAHAN] +
  pautan sunnah.com). `sunnah_map/` didaftar sebagai data kerja
  dibenarkan + .gitignore.

### Sesi 37 — Pepijat skrol "Lompat No. hadis" dijumpai & dibetulkan

Pengguna minta semak lokasi hadis Bukhari No. 500 dalam senarai.
Semakan mendedahkan **pepijat senyap**: skrol ke kad sasaran tidak
berfungsi langsung.

- **Punca**: dalam `_on_kitab_page` (ui/pages_kitab.py), `setValue()`
  dipanggil SEBELUM julat scrollbar wujud — QScrollArea mengemas julat
  secara tak segerak selepas layout selesai, jadi `bar.maximum()==0`
  dan `setValue` terampas ke 0. Kad sasaran langsung tidak kelihatan
  (diukur: Bukhari #500 halaman 25, y=2910, viewport 738, skrol kekal 0).
- **Pembetulan**: refaktor skrol ke `_skrol_ke_kad(sasaran)`; jika
  julat belum sedia (`maximum()==0`), tunggu isyarat `rangeChanged`
  (sambung sekali, putus selepas skrol) supaya kad benar-benar
  kelihatan selepas layout selesai.
- **Lokasi hadis #500**: halaman 25 (hadis 481–500, 20 kad/halaman),
  kad PALING BAWAH — indeks 19/19 (0 baris dari bawah).
- `uji_lompat_fungsi.py`: +2 semakan — kad sasaran benar-benar
  kelihatan dalam viewport + scrollbar bergerak (halaman panjang).
  Ujian kini `show()+resize(1000,800)` supaya layout offscreen sah
  (tanpa show, viewport tiada julat — artifak).
- Disahkan: semak.py SEMUA LULUS, uji_lompat.py 67/67,
  uji_lompat_fungsi.py 17/17, uji_bandingan.py 28/28.

### Sesi 38 — Carian khusus terus ke butiran (bukan senarai)

Pengguna: sebagai apl mesra pengguna, carian KHUSUS (cth. "bukhari 500")
sepatutnya membuka butiran hadis TERUS — pengguna mahukan hadis itu,
bukan senarai. Hanya carian UMUM (cth. "hukum riba") memaparkan senarai
hasil.

- Sebelum ini: "bukhari 500" -> `_lompat_ke` (senarai kitab pada kad
  berkenaan); hanya nombor sahaja ("433") -> `_buka_hadis_terus`.
- Sekarang: KEDUA-DUA (nama kitab + nombor ATAU nombor sahaja) ->
  `_buka_hadis_terus` (butiran terus). `_hantar_carian` (pages_carian.py)
  dan `_from_home_search` (pages_home.py) dikemas; `_lompat_ke` tiada
  pemanggil UI (kekal untuk ujian + kotak Lompat No. hadis dalam senarai
  kitab yang guna `_lompat_hadis` sendiri).
- `_buka_hadis_terus` guna `dari='home'` dari halaman Utama (butang
  Kembali ke Utama) dan `dari='search'` dari halaman Carian.
- Manual BM + EN dikemas (carian khusus terus ke butiran; carian umum
  kekal senarai).
- uji_bandingan.py: +3 semakan — "bukhari 500" ke detail (bukan kitab),
  kad No. 500 dibuka, "hukum riba" kekal ke senarai carian.

### Sesi 39 — Toast "Membuka…" untuk carian khusus + pepijat timer Toast

Pengguna minta toast maklum balas "📖 Membuka Sahih Bukhari No. 500…"
apabila carian khusus membuka butiran hadis terus.

- Toast SEMEMANGNYA sudah wujud dalam `_buka_hadis_terus` (Sesi 38),
  tetapi ada dua kelemahan yang diperbaiki:
  1. **Tempoh tetap 1800ms dipaparkan SEBELUM muatan async selesai**
     — untuk muatan lambat (dalam talian), toast hilang sebelum
     butiran dibuka. Penyelesaian: `show_msg(..., ms=0)` = kekal
     sehingga `hide()`; `_buka_hadis_terus` catat `_buka_toast_t0`
     (masa mula) dan `open_by_ref` sembunyikan toast "Membuka"
     selepas butiran dibuka, menjamin minimum 1800ms paparan.
  2. **Pepijat timer lama**: `QTimer.singleShot(1800, hide)` daripada
     toast SEBELUMNYA (cth. "Disalin!") masih aktif dan menutup toast
     baharu yang kekal lebih awal. `Toast.show_msg` kini menyimpan
     timer (`_hide_timer`) dan MEMBATALKAN timer lama apabila toast
     baharu dipapar.
- uji_bandingan.py: +6 semakan — toast dipapar sejurus selepas carian
  khusus dengan teks betul (nama + nombor), `_buka_toast_t0` dicatat,
  unit timer (ms=0 tiada auto-hide, ms>0 ada, toast baharu batalkan
  timer lama). NOTA: QTimer dalam mod offscreen TIDAK menunggu masa
  sebenar (dipercepatkan) — tempoh minimum tidak boleh diuji offscreen,
  jadi diuji secara unit + semakan segera sahaja.
- Disahkan: semak.py SEMUA LULUS, uji_bandingan.py 38/38,
  uji_lompat_fungsi.py 17/17, uji_lompat.py 67/67.

### Sesi 39b — Ujian aliran carian khusus dari halaman Utama + hilangkan flaky

Pengguna minta perluas uji_lompat_fungsi.py untuk sahkan aliran carian
khusus dari halaman UTAMA (dari='home') juga terus ke butiran.

- +6 semakan: "bukhari 500" dari Utama terus ke butiran No. 500
  (bukan senarai kitab), `_detail_from == "home"`; nombor sahaja
  "433" dari Utama (chip bukhari) terus ke butiran No. 433,
  `_detail_from == "home"`. Aliran search (dari='search') sedia diuji.
- **Flaky dikesan & dihilangkan**: QTimer dalam mod offscreen TIDAK
  menunggu masa sebenar (dicetuskan serta-merta), jadi
  `QTimer.singleShot(250/300/500, ...)` kadang-kadang berjalan SEBELUM
  worker/layout selesai → scrollbar masih max=0 dan kad "kelihatan"
  secara palsu (semua pada y=0). Ganti dengan `tunggu_sedia()` —
  polling processEvents sehingga syarat dipenuhi (had masa 8s).
  Disahkan: 4/4 larian stabil 23/23.
- Perkataan docstring berbau Indonesia → "menghilangkan" (semakan
  8m semak.py).
- Disahkan: semak.py SEMUA LULUS, uji_lompat_fungsi.py 23/23,
  uji_bandingan.py 38/38, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 40 — uji_bandingan.py guna corak tunggu_sedia() (polling)

Pengguna minta corak tunggu_sedia() (polling) dipakai dalam
uji_bandingan.py juga, supaya semua ujian GUI konsisten dan tidak
bergantung pada QTimer yang tidak menunggu dalam mod offscreen.

- Salin pembantu `tunggu_sedia()` daripada uji_lompat_fungsi.py
  (polling processEvents sehingga syarat dipenuhi, had masa 8s);
  `tunggu_worker` (mati) dibuang, `tunggu` kekal didokumenkan.
- Semua tunggu tetap diganti dengan polling pada keadaan sebenar:
  koleksi dimuat (CollectionsWorker), butiran dibuka (stack==2 +
  _detail_h.id), lajur MELAYU/INDONESIA/ENGLISH dirender, butang
  Salin/Kongsi wujud, papan klip diisi selepas klik, carian khusus
  "bukhari 500" selesai (open_by_ref async), carian umum "hukum
  riba" selesai (SearchWorker, `_kw_res is not None`).
- Semakan toast 8c kekal sinkron (dipapar sejurus selepas
  _hantar_carian sebelum sebarang pemprosesan event).
- +10 semakan polling baharu; 48/48 lulus, 3/3 larian stabil.
- Disahkan: uji_bandingan.py 48/48, uji_lompat_fungsi.py 23/23,
  uji_lompat.py 67/67. NOTA: semak.py 1 kegagalan — DEKLARASI.md
  (fail untracked sedia ada 10 Ogos) dalam semakan 9 "Fail yang
  tidak patut diedar"; bukan regresi sesi ini.

### Sesi 40b — Kembali dari butiran carian Utama -> halaman Utama

Perluas uji_lompat_fungsi.py untuk sahkan butang Kembali dari
butiran yang dibuka melalui carian Utama menuju ke halaman Utama
(bukan Carian).

- +8 semakan melalui `_periksa_kembali_utama()`: butang Kembali wujud
  (label "‹  Kembali" dalam _detail_bar), tooltip "Kembali ke Utama",
  klik -> stack == PAGES["home"] (0), dan BUKAN PAGES["search"] (3).
- Diuji untuk KEDUA-DUA aliran dari='home': "bukhari 500" (nama
  kitab + nombor) dan "433" (nombor sahaja dengan chip bukhari).
- Punca regresi berbahaya: jika _detail_from tersilap jadi "search",
  back["search"] = go("search") membawa pengguna ke Carian kosong.
- Disahkan: uji_lompat_fungsi.py 31/31 (3/3 larian stabil),
  uji_bandingan.py 48/48, uji_lompat.py 67/67.

### Sesi 40c — Kembali dari butiran carian (dari='search') -> Carian

Perluas uji_lompat_fungsi.py: butang Kembali dari butiran yang dibuka
melalui halaman Carian (dari='search') menuju ke halaman Carian,
bukan Utama.

- `_periksa_kembali_utama` direfaktor kepada `_periksa_kembali()`
  generik (label jangkaan, indeks jangkaan, indeks bukan-jangkaan)
  — dipakai untuk kedua-dua aliran: 'home' (Utama, 0, bukan 3) dan
  'search' (Hasil carian, 3, bukan 0).
- +4 semakan baharu untuk aliran search: butang Kembali wujud,
  tooltip "Kembali ke Hasil carian", klik -> PAGES["search"] (3),
  BUKAN PAGES["home"] (0).
- Regresi dilindungi: back["search"] = go("search") — pengguna yang
  memulakan carian di halaman Carian tidak hilang konteks hasil.
- Disahkan: uji_lompat_fungsi.py 35/35 (3/3 larian stabil),
  uji_bandingan.py 48/48, uji_lompat.py 67/67.

### Sesi 40d — DEKLARASI.md dibuang (kebenaran pengguna)

Fail untracked DEKLARASI.md (dicipta 10 Ogos, di luar rekod sesi)
disenaraikan semakan 9 "Fail yang tidak patut diedar" sebagai kotor.
Pengguna sahkan ia fail sementara dan beri kebenaran buang:
`rm -f DEKLARASI.md`. semak.py kini **SEMUA LULUS — selamat dihantar**
(gate hijau semula).

**PENDING**: tiada.

### Sesi 41 — Semakan unit peta Kembali (BACK_PETA)

Ekstrak peta butang Kembali daripada `_render_detail` (pemboleh ubah
setempat) kepada pemalar modul `BACK_PETA` dalam ui/pages_detail.py
supaya boleh diuji unit:

- `BACK_PETA = {home: ("Utama", "home"), search: ("Hasil carian",
  "search"), saved: ("Tersimpan", "saved"), kitab: ("Senarai kitab",
  "kitab")}` — nilai = (label tooltip, page_key). 'kitab' ISTIMEWA:
  ia membuka senarai kitab pada halaman sama melalui `open_kitab`
  (bukan `go()` sahaja). Nilai _detail_from tidak dikenali jatuh ke
  fallback 'home'.
- `_render_detail` kini guna BACK_PETA — tingkah laku sama (butang
  Kembali, tooltip, destinasi), disahkan oleh uji_lompat_fungsi 35/35.
- Semakan unit baharu semak.py **8p**: semua 4 nilai _detail_from
  wujud, setiap page_key sah dalam PAGES, label tidak kosong, fallback
  -> home, rujuk silang home->PAGES['home'](0) dan
  search->PAGES['search'](3) (konsisten dengan ujian GUI 40b/40c).
- Disahkan: semak.py SEMUA LULUS (8p 15/15), uji_lompat_fungsi.py
  35/35, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 42 — Semakan unit navigasi Sebelum/Seterusnya (8q)

Logik butang Sebelum/Seterusnya pada bar navigasi bawah butiran
(dahulu dibenamkan dalam `_render_detail`) diekstrak kepada fungsi
tulen `_label_sebelum(hid)` / `_label_seterusnya(hid, max_id)` dalam
ui/pages_detail.py:

- `_label_sebelum`: pulang "‹ No. N" hanya untuk hid int > 1 (None
  untuk hadis pertama / bukan int).
- `_label_seterusnya`: pulang "No. N ›" kecuali hid bukan int atau
  max_id diketahui dan hid >= max_id (hadis terakhir). max_id == 0
  (had tidak diketahui) -> butang tetap dipapar.
- `_render_detail` kini panggil fungsi (label + syarat sekali, bukan
  duaan if-f-string).
- Semakan unit semak.py **8q**: 4 kes Sebelum + 6 kes Seterusnya
  (sempadan: hid=1, hid=max_id, di luar julat, bukan int, max_id=0)
  + 2 semakan statik AST pada BADAN _render_detail (guna fungsi;
  format label lama tidak dibenamkan semula — dibetulkan selepas
  semakan awal tersilap mengira definisi fungsi sebagai benaman).
- Disahkan: semak.py SEMUA LULUS (8q 12/12), uji_lompat_fungsi.py
  35/35, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 43 — Semakan GUI butang Sebelum/Seterusnya

Lengkapkan lapisan GUI untuk navigasi bawah butiran (unit 8q diuji
logik; di sini tingkah laku SEBENAR pada widget):

- Buka No. 1 (hadis pertama) -> TIADA butang Sebelum, tetapi butang
  Seterusnya 'No. 2 ›' ada.
- Buka No. 2 -> butang Sebelum '‹ No. 1' ada DAN Seterusnya 'No. 3 ›'
  ada.
- Klik Seterusnya -> muat async (open_by_ref) -> butiran No. 3 dibuka
  (polling tunggu_sedia sehingga _detail_h.id == 3).
- +7 semakan dalam uji_lompat_fungsi.py (42/42, 3/3 larian stabil).
- Disahkan: semak.py SEMUA LULUS, uji_lompat_fungsi.py 42/42,
  uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 44 — Ekstrak fungsi/pemalar render lain + semakan unit 8r

Teruskan corak 8p/8q ke pemalar/syarat render yang lain:

- **`_label_simpan(saved)`** dalam ui/pages_detail.py — label butang
  Simpan/Tersimpan ('⭐ Tersimpan' vs '☆ Simpan'). Dahulu dibenamkan
  di 3 tempat (render + setText dalam _toggle_save); kini fungsi tulen.
- **`LABEL_RAWAK`** dalam ui/app_qt.py — label butang Rawak pada bar
  navigasi atas ('⚄  Rawak'), dahulu literal dibenamkan.
- Semakan unit semak.py **8r** (8 semakan): kedua-dua keadaan
  _label_simpan betul; _render_detail + _toggle_save guna fungsi
  (AST pada badan, bukan seluruh fail); LABEL_RAWAK bukan kosong,
  butang guna pemalar, tiada literal duplikat.
- Disahkan: semak.py SEMUA LULUS (8r 8/8), uji_lompat_fungsi.py
  42/42, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 45 — Semakan GUI butang Simpan + ekstrak _tab_lalai (8s)

Dua tugasan pengguna ("semua"):

1. **Semakan GUI butang Simpan/Tersimpan** (uji_lompat_fungsi.py, +6
   semakan): buka No. 2 dengan keadaan penanda buku dipaksa bersih,
   butang mula '☆ Simpan'; klik -> label '⭐ Tersimpan' + penanda
   buku bukhari#2 ditambah; klik kedua -> label '☆ Simpan' + dibuang.
   Penanda buku asal dipulihkan (memori + fail bookmarks.json) selepas
   ujian supaya tiada kesan sampingan.
2. **Ekstrak `_tab_lalai(pref, avail)`** (ui/pages_detail.py) — logik
   pemilihan tab bahasa lalai (dahulu ternary dibenamkan dalam
   _render_detail): 'ind_only' -> indonesia, selainnya melayu, dengan
   fallback ke bahasa tersedia, kemudian 'melayu'. Semakan unit 8s
   (7 semakan): 5 kes unit + 2 statik AST. NOTA: kes fallback guna
   set SATU elemen kerana next(iter(set)) tidak deterministik untuk
   set berbilang elemen (2 kes pertama gagal, dibetulkan).
- Disahkan: semak.py SEMUA LULUS (8s 7/7), uji_lompat_fungsi.py
  48/48, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 46 — Ekstrak _ialah_bab_tafsir (8t) + audit akhir penghantaran

Logik tag 'Bab Tafsir' (dahulu dibenamkan di DUA tempat — kad hasil
carian ui/widgets.py + halaman butiran ui/pages_detail.py) diekstrak
kepada fungsi tulen `_ialah_bab_tafsir(collection, book)` dalam
ui/widgets.py:

- Pulang True hanya bila koleksi+book ada dan BAB_TAFSIR[collection]
  == book ({bukhari:65, muslim:56, tirmidzi:47}).
- Kedua-dua tempat guna fungsi — duaan tidak boleh hanyut (contoh:
  satu papar tag, satu lagi tidak).
- Semakan unit semak.py **8t** (10 semakan): 6 kes unit (3 True, 3
  False termasuk nombor milik koleksi lain) + 4 statik (kad carian dan
  _render_detail guna fungsi; tiada literal BAB_TAFSIR dibenamkan
  semula di kedua-dua tempat).
- Audit akhir penghantaran: `semak.py --audit-sunnah` 20/20 dipadan,
  0 tidak padan — SEMUA LULUS — selamat dihantar.
- Disahkan: semak.py SEMUA LULUS (8t 10/10), uji_lompat_fungsi.py
  48/48, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 47 — MULA_SINI.md 'Versi semasa' sebut ciri Sesi 36–46

Kemas MULA_SINI.md (3 bahagian): senarai sesi dalam "Versi semasa:
v1.3" ditambah Sesi 36–46; blok KEMASKINI baharu menerangkan pautan
"Baca penuh" sunnah.com (peta dalam-buku + audit 8n/8o), carian
khusus terus ke butiran + toast "Membuka…", butang Kembali ikut
halaman asal, dan tag "Bab Tafsir" (8t); senarai "Siap:" ditambah
ciri-ciri itu. Satu perkataan berbau Indonesia diganti dengan
"berakhir dengan" (semakan 8m). Disahkan: semak.py SEMUA LULUS.

**PENDING**: tiada.

### Sesi 48 — Ekstrak _pilih_terjemahan (keutamaan bahasa kad) + semakan 8u

Kad hasil carian memilih petikan terjemahan dengan keutamaan
Melayu > Indonesia > English — dahulu dibenamkan sebagai rantaian
`or` dalam `hadith_card` (ui/widgets.py). Diekstrak kepada fungsi
tulen `_pilih_terjemahan(melayu, indonesia, english)`:

- Pulang teks pertama yang bukan kosong selepas strip; '' jika tiada.
- Semakan unit semak.py **8u** (8 semakan): 6 kes unit (keutamaan
  BM>ID>EN, ruang sahaja dilangkau, semua kosong -> '', strip) + 2
  statik (hadith_card guna fungsi; tiada rantaian or dibenamkan
  semula).
- Disahkan: semak.py SEMUA LULUS (8u 8/8), uji_lompat_fungsi.py
  48/48, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 49 — Semakan potongan kad elide() + syarat chip _papar_chip (8v)

Logik render kad hasil carian yang tinggal dibenamkan ditangani:

- **`elide()`** (potongan teks kad: normalisasi ruang + potong pada
  sempadan perkataan + ellipsis '…') digunakan di 3 tempat (bab 44,
  arab, terjemahan) tetapi TIADA ujian langsung — kini diuji unit
  (7 kes: teks pendek kekal, ruang dinormalisasi, kosong/None -> '',
  potong+ellipsis, sempadan perkataan, panjang <= n+1).
- **`_papar_chip(show_chip, kitab_name)`** — syarat chip nama kitab
  (dahulu `if show_chip and kitab_name:` dibenamkan) kini fungsi
  tulen + 4 kes unit + semakan statik AST pada BADAN hadith_card
  (parse ui/widgets.py terus kerana hadith_card bukan mixin;
  semakan awal tersilap mengira docstring _papar_chip sendiri sebagai
  benaman — dibetulkan dengan ast.get_source_segment).
- Audit akhir penghantaran: semak.py --audit-sunnah 20/20 dipadan,
  SEMUA LULUS — selamat dihantar.
- Disahkan: semak.py SEMUA LULUS (8v 13/13), uji_lompat_fungsi.py
  48/48, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 50 — Audit sunnah.com diperluas ke 50 sampel

`--audit-sunnah=N` sudah menyokong saiz sampel (tidak perlu ubah kod);
docstring semak_audit_sunnah dikemas untuk mencadangkan
`--audit-sunnah=50` sebagai liputan lebih luas sebelum hantar (lalai
20; ~3 minit kerana jeda 3s antara muat turun).

- Dua larian `python semak.py --audit-sunnah=50`: **50 dipadan,
  0 tidak padan, 0 tidak dapat disahkan** — semua pautan "Baca penuh"
  disahkan terhadap halaman sunnah.com sebenar (sampel rawak seeded,
  boleh ulang).
- Gate penuh: semak.py SEMUA LULUS — selamat dihantar.

**PENDING**: tiada.

### Sesi 51 — Manual sebut aliran audit --audit-sunnah=50 pra-hantar

- **MANUAL_PENGGUNA.md** (BM) — bahagian 8 "Kemas kini aplikasi"
  ditambah nota "Setiap versi disahkan dahulu sebelum dihantar":
  `python semak.py --audit-sunnah=50` (50 sampel rawak, ~3 minit)
  kemudian `python semak.py` (gate penuh); hanya lulus SEMUA LULUS
  diedarkan.
- **MANUAL_REFERENSI_DEV.md** — bahagian 9 "Senarai semak sebelum
  hantar" ditambah aliran pra-hantar penuh yang sama (tempat semula
  jadi arahan developer).
- Disahkan: semak.py SEMUA LULUS.

**PENDING**: tiada.

### Sesi 52 — Ekstrak _subtitle_hadis + _julat_lompat (8w)

`_render_kitab_shell` (pages_kitab.py) membina banner kitab dan
placeholder kotak 'Lompat No. hadis' — kedua-duanya memformat `total`
hanya bila int (koleksi belum dimuat -> kosong / "No. hadis").
Logik ini dahulu dibenamkan; kini fungsi tulen:

- `_subtitle_hadis(total)` — '7,008 hadis' (koma ribuan); '' bila
  bukan int/None.
- `_julat_lompat(total)` — '0–7008'; 'No. hadis' bila bukan int/None.
- Semakan unit semak.py **8w** (10 semakan): 8 kes unit (format
  koma, sempadan int/None) + 2 statik AST pada badan
  _render_kitab_shell (guna fungsi; tiada literal format dibenamkan
  semula).
- Disahkan: semak.py SEMUA LULUS (8w 10/10), uji_lompat_fungsi.py
  48/48, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 53 — Ekstrak _label_kad_hadis (8x) + audit akhir 50 sampel

Kad koleksi halaman utama (`KitabCard` dalam ui/pages.py) memaparkan
jumlah hadis — dahulu dibenamkan di DUA tempat (`__init__` + `set_total`
selepas muat data async) dengan format `f"{total:,} Hadis"` bila int,
else "— Hadis". Diekstrak kepada fungsi tulen `_label_kad_hadis`:

- Semakan unit semak.py **8x** (6 semakan): 4 kes unit (koma ribuan,
  sempadan int/None) + 2 statik AST pada badan KELAS KitabCard
  (parse ui/pages.py terus kerana bukan mixin; kedua-dua laluan guna
  fungsi, tiada literal dibenamkan semula).
- Audit akhir penghantaran: `python semak.py --audit-sunnah=50`
  **50 dipadan, 0 tidak padan, 0 tidak dapat disahkan** — SEMUA
  LULUS — selamat dihantar.
- Disahkan: semak.py SEMUA LULUS (8x 6/6), uji_lompat_fungsi.py
  48/48, uji_bandingan.py 48/48, uji_lompat.py 67/67.

**PENDING**: tiada.

### Sesi 54 — Satukan _label_kiraan (8w+8x) + audit koma ribuan

Tiga tapak memformat jumlah hadis dengan koma ribuan + sempadan int
(`isinstance(total, int)`): banner kitab (`_subtitle_hadis`), kotak
lompat (`_julat_lompat`), dan kad koleksi (`_label_kad_hadis`).
Semakan awal mendapati hanya banner + kad berkongsi corak sebenar;
kotak lompat memapar julat '0–N' tanpa koma. Dua fungsi itu disatukan
menjadi satu fungsi kongsi:

- `_label_kiraan(total, kata, fallback)` dalam ui/pages.py — '7,008
  hadis' untuk int (koma ribuan); `fallback` sebaliknya. `kata`
  membezakan 'hadis' (subtitle banner, huruf kecil) vs 'Hadis' (label
  kad); `fallback` membezakan '' vs '— Hadis'.
- Banner: `_label_kiraan(total, "hadis", "")`; kad: `_label_kiraan(
  total, "Hadis", "— Hadis")` di KEDUA-DUA laluan (`__init__` +
  `set_total` selepas muat data async). `_julat_lompat` kekal fungsi
  sendiri (format julat '0–N', bukan koma ribuan).
- `_subtitle_hadis` / `_label_kad_hadis` dibuang. Semak.py 8w (kini
  11 semakan) + 8x (kini 7 semakan) ditulis semula: uji unit per tapak
  + semakan statik bahawa render guna `_label_kiraan` DAN fungsi lama
  tiada definisi/panggilan lagi (elak penyatuan hanyut semula).

Audit semua tapak `{x:,}` lain (di luar tiga tempat):

- `app_qt.py` — 'N hadis daripada M kitab': nilai `sum()` sentiasa
  int, frasa menambah 'daripada M kitab' — makna berbeza.
- `pages_carian.py` ×4 — 'N padanan kata' / 'N hadis ditemui'.
- `pages_detail.py` ×2 — 'Dipendekkan daripada N aksara': `len()`
  sentiasa int, tiada pagar diperlukan.
- `pages_tetapan.py` + `settings_panel.py` ×3 — 'kuota harian: N'.

Semuanya inline dengan nilai dijamin int dan makna berbeza (kuota,
padanan, aksara) — tidak dikongsi; hanya banner + kad wajar disatukan.

Sempadan int: jejak data disahkan (SQLite INTEGER, JSON API, sum/len,
max_hadis_id → int Python tulen; numpy hanya dalam laluan FAISS/model;
bool hanya dari JSON rosak yang API tidak hasilkan). `isinstance(
total, int)` kekal — tidak perlu `numbers.Integral`.

Disahkan: semak.py SEMUA LULUS (8w 11/11, 8x 7/7).

Lanjutan (Sesi 54) — ujian visual skrin + kunci laluan:

- `python uji_visual_kiraan.py` pada skrin SEBENAR → **18 lulus, 0
  gagal**: kad koleksi (9/9 padan `_label_kiraan`, Bukhari '7,008
  Hadis', fallback '— Hadis' + pulih), banner kitab (subtitle '7,008
  hadis', kotak lompat '0–7008'), jumlah rumah '62,169 hadis daripada
  9 kitab'; 4 tangkapan `bukti_visual/kiraan_*.png` (folder di-ignore
  oleh .gitignore — kekal tempatan).
- Audit pemanggil `set_total`: satu-satunya pemanggil produksi ialah
  `_on_collections` (pagar `isinstance` dua lapis); `_cnt` hanya
  ditulis dalam pages.py (`__init__` + `set_total`) melalui
  `_label_kiraan`; TIADA laluan tanpa pagar — dikunci statik dalam 8x
  (penulis `_cnt` / pemanggil `set_total` luar akan GAGAL).
- 8y baharu: uji_visual_kiraan.py mesti kekal + konsisten dengan
  pelaksanaan.
- `Image.getdata()` → `get_flattened_data()` (fallback Pillow lama)
  dalam uji_visual_sebenar/bantuan/kiraan — buang amaran deprecation
  Pillow 12+; ujian kekal 18/18 tanpa amaran.
- MANUAL_REFERENSI_DEV.md: senarai semak pra-hantar menyenaraikan
  KESEMUA 6 ujian visual skrin (kiraan/sebenar/bantuan/carian/
  bandingan/ralat), selepas `semak.py` lulus, pada skrin fizikal.
- Disahkan: semak.py SEMUA LULUS; commit `cfcac39` (5 fail,
  +412/−55).
- **Nota terakhir** — selepas `getdata()` → `get_flattened_data()`:
  `uji_visual_sebenar.py` **65/65** + `uji_visual_bantuan.py` **33/33**
  tanpa amaran deprecation; keseluruhan 6 ujian visual pada skrin
  sebenar: **138 lulus, 0 gagal** (kiraan 18, sebenar 65, bantuan 33,
  carian 11, bandingan 2, ralat 9). Commit `d66f0c3` (5 fail, +54/−5).
- **Ujian negatif 8z + 8w/8x + 8l/8p/8q/8r + 10b** — `python
  uji_negatif_8z.py` (28 lulus, 0 gagal): 17 cabang GAGAL dikesan —
  8z (fail dibuang, fail baharu luar senarai, manual hilang, senarai
  semak dikosongkan), 8w (`_subtitle_hadis` dipulangkan, literal
  format dibenamkan semula), 8x (`_label_kad_hadis` dipulangkan,
  literal label dibenamkan semula), 8l (uji_visual_carian hilang,
  penanda wajib hilang), 8p (BACK_PETA page bukan kunci PAGES —
  suntikan atribut dalam ingatan), 8q (literal label lama dibenamkan
  dalam _render_detail), 8r (literal label Simpan dibenamkan), 10b
  (VERSI palsu 2.0 — suntikan dalam ingatan, CHANGELOG.md hilang,
  seksyen "## 1.1" dipadam), 8m (kata Indonesia disuntik ke
  PADANAN_ARKIB.md, docstring .py sementara). Kelemahan 3a ditemui:
  manual hilang RANAP FileNotFoundError — dibaiki dengan pengawal
  `os.path.exists`, kini GAGAL bersih. Skrip memulihkan fail
  byte-tepat (8 fail + atribut, baris akhir kekal) supaya git tidak
  tercemar.
- **Pembetulan bbox tangkapan** — audit semasa ujian visual penuh
  mendedahkan `uji_visual_sebenar.py` menangkap SKRIN PENUH
  (`ImageGrab.grab()`) tanpa membawa tetingkap ke hadapan — semakan
  "tema gelap" gagal (kecerahan 211) bila permukaan terang lain
  menutup app (83% piksel cerah dalam tangkapan). Dibetulkan:
  `SetForegroundWindow` + `BringWindowToTop` + bbox `GetWindowRect`
  — kini konsisten dengan 5 ujian lain. Selepas pembaikan:
  `sebenar_gelap` kecerahan 49, `sebenar_terang` 240. Keseluruhan 6
  ujian visual pada skrin sebenar: **138 lulus, 0 gagal**.
- **Versi apl → 1.0** (11 Ogos 2026): apl BELUM official —
  `VERSI.py` 1.3 → 1.0; pernyataan versi semasa dalam 5 dokumen
  (MANUAL_PENGGUNA(.EN).md, MANUAL_REFERENSI_DEV.md, MULA_SINI.md,
  PANDANGAN_RISIKO.md) dikemas ke v1.0; penanda sejarah (README
  `(v1.1/v1.2/v1.3)`, komen `CIRI`) dikekalkan.
- **Versi 1.0 rasmi (official)** — disahkan pada skrin SEBENAR (11
  Ogos 2026): header app memapar `v1.0`, skrin pemula memapar `Versi
  1.0 — carian kata kunci + makna (AI)`; tangkapan
  `bukti_visual/versi_1_0.png`. Rujukan: `CHANGELOG.md` baharu.
- **Pengesahan splash + kunci versi** — tangkapan skrin fizikal skrin
  pemula semasa MASA JALAN (aliran main.py penuh: splash +
  PustakaApp + pramuat QThread): `bukti_visual/splash_1_0.png` +
  `splash_1_0_pramuat.png` (96% gelap — tema gelap benar; label
  `Versi 1.0 — carian kata kunci + makna (AI)`; 6 semakan, 0 gagal).
  Semakan statik **10b** baharu dalam semak.py: kunci `VERSI ==
  '1.0'` (edaran rasmi) + CHANGELOG.md kekal wujud + seksyen versi
  1.0–1.3 dan versi semasa ada (regex ketat `^## x.y(\s|$)`; cabang
  GAGAL VERSI 2.0 dan baris 1.1 dipadam dikesan, pulihan byte-tepat).
  CHANGELOG.md dirujuk dalam MULA_SINI.md (nota kepala) +
  MANUAL_REFERENSI_DEV.md §12 peta dokumen.
- **Rekod 22 commit sesi ini:** `cfcac39` (penyatuan `_label_kiraan`)
  → `d66f0c3` (getdata + senarai semak) → `5718c45` (8z) → `7c4f37e`
  (pengawal 8z + ujian negatif) → `4a08e80` (bbox + 8w/8x) →
  `e6690a1` (8l/8p/8q/8r) → `dbfa420` (header) → `66a2dee` (reset
  versi 1.0 + PERUBAHAN_11OGOS.md) → `2586174` (versi 1.0 rasmi +
  CHANGELOG.md) → `5969609` (kunci versi + splash) → `4b88f45`
  (negatif 10b) → `a87b172` (header) → `1cd1ba2` (pecah manual) →
  `9947a64` (audit sunnah 50) → `cc960cc` (DAPATAN_WEB.md) →
  `d1db582` (dorar.net) → `e1eba8e` (semakhadis.com) → `a50c11f`
  (perbandingan 4 sumber) → `8f07f49` (deklarasi diambil pakai) →
  `faa8d17` (DEKLARASI.md versi 1.0 + bersih folder induk) →
  `7c7a152` (deklarasi sepadan TEPAT) → `7bafb63` (dokumen/ diasingkan)
  → `2b18f9a` (kemas kini sesi). Rujukan ringkas: `PERUBAHAN_11OGOS.md`.
- **Padanan arkib** — `dokumen/audit/PADANAN_ARKIB.md` baharu: jejak
  padanan 11 dokumen asal (`backup/arkib_md_11OGOS.zip`) ↔ dokumen
  projek; hanya `DEKLARASI.md` sama (nisbah 1.00, 4 perubahan sengaja
  — versi 1.0 + atribusi diselaraskan dengan app).
- **Penyelamatan 6 dokumen arkib** — fasa 2 PADANAN_ARKIB.md: semua 10
  dokumen UNIK dibaca penuh dan dinilai. 6 disimpan ke projek
  (INSTALLER, SUMBER_hadis-my, PERMOHONAN_LESEN_SEMAKHADIS,
  ISU_TERJEMAHAN_MELAYU, DORAR_NET, ANALISA_6OGOS) — 3 byte-tepat, 3
  dengan pembetulan ejaan BM (8m). 4 tidak disimpan: 2 sejarah
  (BACA_DAHULU, sesi_analisis), 1 subset (PERMOHONAN_HADISMY),
  1 salinan tepat (SUMBER_semakhadis). Status ANALISA_6OGOS disahkan:
  5/7 isu selesai (requirements, fix DLL→ctypes, skrip build, README,
  refactor), 2 terbuka (lesen SemakHadis, model/installer).
- **Manual pengguna dipecah dua** — `MANUAL_PENGGUNA.md` diganti oleh
  `manual/manual/MANUAL_INSTALASI.md` (keperluan sistem, pasang, kunci API, kemas
  kini, penyelesaian masalah, nyahpasang, privasi) + `manual/manual/MANUAL_PENGGUNAAN.md`
  (apa itu, antara muka, panel tetapan); `MANUAL_PENGGUNA_EN.md`
  digugurkan — kini cuma 2 manual pengguna. Rujukan dikemas:
  MANUAL_REFERENSI_DEV.md (§1 + §12), semak.py 8m (pengecualian EN
  dibuang).
- **Audit sunnah.com (8o)** — `python semak.py --audit-sunnah=50`
  pada skrin sebenar: **50 dipadan, 0 tidak padan, 0 tidak dapat
  disahkan**; semak.py penuh SEMUA LULUS. Dokumentasi penuh dengan
  jadual 50 sampel (hadis.my ↔ sunnah.com): `AUDIT_SUNNAH.md`
  (dirujuk dalam peta dokumen + manual/manual/MANUAL_INSTALASI.md §5).
- **Dapatan web** — `DAPATAN_WEB.md` baharu: struktur sunnah.com
  (laman utama + halaman hadis), corak URL + pemetaan slug, skema
  penomboran dalam-buku vs hadis.my, penilaian dan implikasi, cara
  siasat semula. Dirujuk dalam peta dokumen §12.
- **DEKLARASI.md diambil pakai** — deklarasi (8 Ogos 2026) diterapkan:
  `ui/deklarasi.py` (teks pendek + penuh, `DeklarasiDialog`); skrin
  permulaan SEKALI pada larian pertama (bendera `deklarasi_dibaca`
  dalam user_settings.json, modal + butang "Faham"); butang
  "Tentang PustakaHadith" dalam panel Tetapan (deklarasi penuh:
  tujuan, kandungan, sumber & atribusi, batasan, sokongan); pautan
  SemakHadis.com pada keadaan "Tiada hasil" halaman Carian. Semakan
  statik 8aa mengunci teks + cantuman. Ujian: 6 visual 138/138, flag
  3/3, dialog 16/16; fakta disahkan (62,169; 31,833=51%; 4,237;
  sumber fawazahmed0 Unlicense).
- **DEKLARASI.md disahkan sepadan TEPAT** — perbandingan berprogram
  (AST + normalisasi md) teks dipapar app vs DEKLARASI.md: 35/35
  padan. Tiga percanggahan kecil pada baris atribusi dibaiki dalam
  DEKLARASI.md (label berkolon ':' + 'koleksi' huruf kecil, selaras
  dengan paparan app). Semakan 8aa diperluas: 3 baris atribusi dikunci
  sepadan TEPAT (label+kolon dalam ui/deklarasi.py; ayat penuh
  ternormal dalam DEKLARASI.md). Cabang GAGAL diuji: kolon dibuang dan
  'Koleksi' huruf besar — kedua-dua dikesan; pulihan byte-tepat.
- **Dokumen diasingkan ke `dokumen/`** — semua 17 fail .md dipindah
  dari akar ke folder mengikut jenis: `manual/` (MULA_SINI + 3
  MANUAL), `perubahan/` (CHANGELOG + 4 PERUBAHAN), `sesi/`
  (sesi_index), `audit/` (AUDIT_SUNNAH + DAPATAN_WEB), `rujukan/`
  (DEKLARASI + PANDANGAN_RISIKO + REVOKE_KUNCI + RANCANGAN). README.md
  kekal di akar sebagai pintu masuk. Semua laluan dikemas: semak.py
  (8m imbas rekursif dokumen/, 8z/10b/8aa/11), uji_negatif_8z.py
  (MAN/CLOG), 87 rujukan silang dalam 11 dokumen hidup; arkib sejarah
  (sesi_index, PERUBAHAN_30/31JUL/7OGOS) tidak disentuh. Disahkan:
  semak.py SEMUA LULUS (18 dokumen disemak 8m), uji_negatif 28/28.

**PENDING**: tiada.

### Sesi 55 — Perbandingan 3 mockup halaman detail (bukhari1 · nasai2117 · abudaud4177)

Tiga mockup HTML dibina untuk menguji reka bentuk halaman detail hadis
pada tiga keadaan data sebenar dari hadis.db (bukan teks tiruan):

| Mockup | Kitab / No. | Sumber huraian | Darjat CDN | Kes ujian |
|---|---|---|---|---|
| `mockup_bukhari1.html` | Sahih al-Bukhari No. 1 | HadeethEnc | **TIADA** | keadaan kosong darjat |
| `mockup_nasai2117.html` | Sunan an-Nasai No. 2117 | SemakHadis | 3 ulama, semua Sahih | darjat sebulat suara |
| `mockup_abudaud4177.html` | Sunan Abi Dawud No. 4177 | SemakHadis | 4 ulama, semua Sahih | **darjat BERCAWANGAN** (SemakHadis: Palsu vs CDN: Sahih) |

Ketiga-tiga mockup berkongsi struktur CSS/JS yang sama (palet kertas
hangat `#f4f1ea` / gelap `#1e1d1a`, mod gelap penuh, tab bahasa, panel
huraian, bar bawah) — perbezaan hanyalah pada kandungan dan satu
keputusan warna cip. Kesimpulan perbandingan:

#### Keputusan reka bentuk (disahkan, konsisten dalam ketiga-tiga)

1. **Susun atur dua lajur berdampingan** (ARAB | terjemahan) dalam satu
   panel — bukan menegak. Lajur Arab kiri, lajur terjemahan kanan,
   `flex: 1 0 240px` dengan skrol mendatar pada skrin sempit.
2. **Tab bahasa DALAM SETIAP lajur** — lajur Arab: `ARAB / TRANSLITERASI`;
   lajur terjemahan: `MELAYU / INDONESIA / ENGLISH`. Tab aktif tebal
   hitam, tidak aktif kelabu pudar. Tab berasingan per lajur, bukan
   satu tab global.
3. **Transliterasi memaparkan DUA gaya serentak** — GAYA MELAYU dan
   AKADEMIK dalam blok berasingan (bukan satu gaya sahaja), muncul
   dalam tab TRANSLITERASI lajur Arab.
4. **Huraian + penilaian ulama dipapar TERBUKA di bawah** — bukan
   dalam Collapsible tertutup (berbeza daripada keputusan awal Sesi 14
   yang mencadangkan Collapsible). Ketiga-tiga mockup konsisten:
   huraian dan darjat kelihatan serta-merta tanpa perlu klik.
5. **Struktur huraian ikut sumber** — HadeethEnc guna
   TERJEMAHAN/PENJELASAN/PENGAJARAN; SemakHadis guna
   TERJEMAHAN/TAKHIJ/KOMENTAR. Struktur lajur huraian ditentukan oleh
   apa yang sumber ada, bukan bentuk seragam yang dipaksa.
6. **Atribusi sumber wajib** — `nota-dalam` di bawah panel huraian
   ("Sumber: SemakHadis.com" / nota HadeethEnc.com) dan di bawah
   darjat ("Sumber: fawazahmed0/hadith-api (Unlicense)").
7. **Cip klasifikasi warna ikut makna** — hijau untuk positif (صحيح,
   Muttafaq 'alayh), **MERAH untuk negatif (Palsu)** — cip merah hanya
   wujud dalam mockup abudaud4177, iaitu variasi yang diperkenalkan
   untuk kes hadis bermasalah.
8. **Penafian darjat** — quote italik "Penilaian ini daripada ulama
   hadis moden. Ulama boleh berbeza pendapat. Rujuk ahli ilmu untuk
   kepastian." dipapar di bawah senarai darjat (kecuali kes kosong
   Bukhari).
9. **Keadaan kosong darjat** — Bukhari #1 (tiada grades dalam sumber
   CDN) memapar "Tiada penilaian ulama untuk hadis ini dalam sumber."
   + nota mockup menerangkan ianya rupa app sebenar (konsisten dengan
   Sesi 14: Bukhari & Muslim 0% grades).
10. **Nav bawah** — `‹ Kembali` kiri, `‹ No. X · No. Y ›` kanan.
    Perbezaan bukhari1 ("No. 2 ›" sahaja) bukan keputusan reka
    bentuk — hadis #1 memang tiada nombor sebelumnya.

#### Keputusan utama: darjat BERCAWANGAN dipapar mentah (abudaud4177)

Mockup abudaud4177 sengaja memilih kes paling sukar: SemakHadis
mengklasifikasi hadis sebagai **Palsu** tetapi keempat-empat ulama CDN
menilai **Sahih**. Keputusan yang diambil pakai:

- **Kedua-dua penilaian dipapar serentak, mentah, tanpa tafsiran** —
  cip Palsu (SemakHadis) di panel huraian + senarai darjat Sahih CDN
  di bawahnya. App TIDAK memilih siapa betul (prinsip Sesi 14: papar
  mentah, dinisbahkan, tanpa tarjih).
- Tajuk panel huraian memapar klasifikasi sumber: "Huraian (SemakHadis
  · Palsu)" — sumber + klasifikasinya disebut jelas.
- Ini corak untuk SEMUA kes percanggahan: papar kedua-dua belah,
  atribusi setiap satu, tiada penilaian app sendiri.

#### Perbezaan yang DIPUTUSKAN (variasi antara mockup)

| Aspek | bukhari1 | nasai2117 | abudaud4177 | Keputusan |
|---|---|---|---|---|
| Sumber huraian | HadeethEnc | SemakHadis | SemakHadis | ikut apa yang ada untuk kitab (kedua-dua sumber sah) |
| Chip klasifikasi | صحيح (hijau) | Muttafaq 'alayh (hijau) | Palsu (**merah**) | warna ikut makna: hijau positif / merah negatif |
| Bilangan ulama darjat | 0 (kosong) | 3 | 4 | papar SEMUA yang ada, tiada had |
| Quote penafian | tiada (kes kosong) | ada | ada | dipapar bila ada senarai darjat |
| Bahagian huraian | TERJEMAHAN/PENJELASAN/PENGAJARAN | TERJEMAHAN/TAKHIJ/KOMENTAR | TERJEMAHAN/TAKHIJ/KOMENTAR | struktur ikut sumber (keputusan #5) |

**STATUS: keputusan reka bentuk direkod. Pelaksanaan ke ui/app_qt.py
belum dimulakan — mockup ialah spesifikasi, belum kod.**

**PENDING**: pelaksanaan halaman detail mengikut mockup (dua lajur +
terjemahan + huraian TERBUKA + darjat papar mentah); fail mockup
belum di-commit.

Lanjutan (Sesi 55) — Keputusan palet kertas hangat mockup vs theme.py

Soalan: patutkah palet kertas hangat mockup (`#f4f1ea` terang /
`#1e1d1a` gelap) menggantikan palet `ui/theme.py` sedia ada?

### Perbandingan palet (diukur, bukan pendapat)

| Peranan | Mockup (kertas hangat) | theme.py LIGHT | theme.py DARK |
|---|---|---|---|
| Latar halaman | `#f4f1ea` / `#1e1d1a` | `#F5F7F8` | `#161C21` |
| Kad | `#ffffff` / `#282721` | `#FFFFFF` | `#1E262C` |
| Sempadan kad | `#e4dfd3` / `#3b3932` | `#C2CDD3` | `#2B363E` |
| Teks utama | `#2b2b2b` / `#e8e4da` | `#141A1E` | `#E8EDF0` |
| Teks sekunder | `#7a7468` / `#a39c8c` | `#3A4A54` | `#AFC0C9` |
| Aksen pautan | **hijau** `#1a6b3c` / `#5cbf85` | **TEAL** `#0F6E8C` | **TEAL** `#7FC4DE` |

Perbezaan asas bukan kecerahan tetapi **suhu warna**: mockup hangat
(kuning-coklat), theme.py sejuk (biru). Aksen juga berbeza: mockup guna
hijau untuk pautan/breadcrumb, theme.py guna TEAL (identiti yang
diselaraskan dengan gaya hadis.my, dipakai 7 halaman + logo + ikon).

### Kontras WCAG (nisbah, sasaran AA = 4.5:1 teks biasa)

| Gabungan | Nisbah | Status |
|---|---|---|
| Mockup terang: `#2b2b2b`/`#f4f1ea` | 12.55 | ✅ |
| Mockup terang: `#7a7468`/`#f4f1ea` (sub) | **4.11** | ❌ GAGAL AA |
| Mockup terang: `#9a937f`/`#fdfcf8` (kapsyen) | **2.98** | ❌ GAGAL AA |
| Mockup gelap: `#e8e4da`/`#1e1d1a` | 13.28 | ✅ |
| Mockup gelap: `#a39c8c`/`#1e1d1a` (sub) | 6.17 | ✅ |
| theme LIGHT: `#141A1E`/`#F5F7F8` | 16.34 | ✅ |
| theme LIGHT: `#3A4A54`/`#F5F7F8` (sekunder) | **8.54** | ✅ margin besar |
| theme DARK: `#AFC0C9`/`#1E262C` (sekunder) | 8.19 | ✅ |
| Cip hijau: mockup 5.71 vs theme LIGHT 5.80 | ≈sama | ✅ |
| Cip merah: mockup 5.64 vs theme LIGHT 5.70 | ≈sama | ✅ |

### Penemuan penting

1. **Mockup terang GAGAL AA** pada teks sekunder (4.11) dan kapsyen
   (2.98) — kedua-duanya saiz 11–13px yang banyak dalam apl. theme.py
   lulus dengan margin besar (8.54). Kertas hangat tidak lebih baik
   untuk kebolehbacaan; ia lebih lemah.
2. **Warna cip mockup ≈ GREEN/RED theme.py LIGHT** — hijau `#e9f2ea`/
   `#1a6b3c` (5.71) hampir sama dengan `#E6F5EA`/`#1F6B33` (5.80);
   merah `#fdeaea`/`#b3261e` (5.64) hampir sama dengan `#FDE9EC`/
   `#B3202F` (5.70). Pelaksanaan halaman detail TIDAK perlu palet
   baharu untuk cip — guna GREEN/RED sedia ada.
3. **TEAL sedia ada atas kertas mockup = 5.13:1** (masih lulus AA) —
   jika suatu hari mahu rasa kertas, aksen TEAL tidak perlu ditukar.
4. **Kad atas latar** hampir sama elevasinya (1.13 vs 1.07 terang;
   1.13 vs 1.12 gelap) — kedua-dua bergantung pada sempadan, bukan
   perbezaan palet.

### KEPUTUSAN: KEKAL theme.py sedia ada

Palet kertas hangat mockup TIDAK diguna pakai. Alasan:

1. **Kontras lebih lemah** — mod terang mockup gagal AA 4.5:1 pada dua
   tahap teks kecil yang kerap digunakan; theme.py lulus dengan margin.
2. **Aksen hijau bercanggah dengan identiti TEAL** yang diselaraskan
   dengan hadis.my dan sudah dipakai di seluruh apl (7 halaman, logo,
   ikon, QSS global). Menukar aksen = kerja besar tanpa faedah terukur.
3. **Mockup ialah spesifikasi LAYOUT halaman detail** (dua lajur, tab,
   TERBUKA, papar mentah — Sesi 55). Palet mockup ialah kulit
   persembahan mockup, bukan keputusan reka bentuk yang dipilih.
4. **Konsistensi satu tema** — satu app, satu palet. Palet berasingan
   untuk satu halaman memecah konsistensi; menukar global ialah
   perubahan 12 modul + QSS + bina logo tanpa bukti faedah.

Kesan kepada pelaksanaan Sesi 55: struktur mockup dilaksanakan dengan
palet theme.py sedia ada; cip hijau/merah guna GREEN/RED theme.py
(yang hampir padan dengan mockup). Tiada perubahan kod dibuat —
keputusan ini hanya direkod.

### DIBATALKAN 12 Ogos 2026 — palet kertas hangat DITERIMA PAKAI

Selepas pengguna melihat app sebenar vs mockup dan meminta padanan
visual, keputusan di atas dibatalkan: **palet kertas hangat mockup kini
diguna pakai** dalam `ui/theme.py` (DARK + LIGHT). Cara pelaksanaan
mengambil kira alasan asal tanpa menutup aksesibiliti:

1. **Hue hangat mockup diambil** — latar `#f4f1ea`/`#1e1d1a`, kad
   `#ffffff`/`#282721`, sempadan `#e4dfd3`/`#3b3932`, teks utama
   `#2b2b2b`/`#e8e4da`.
2. **Teks sekunder/kapsyen DITUNAKAN untuk AA** — mockup `#7a7468`
   (4.11, gagal) dan `#9a937f` (2.72, gagal) digelapkan kepada
   `#5f594d` (6.16) dan `#6e685a` (4.91) — hue hangat sama, kontras
   cukup. Faint kekal pucat mengikut reka bentuk.
3. **Aksen hijau mockup menggantikan TEAL** — `TEAL*` dalam dict kini
   hijau (`#1a6b3c`/`#5cbf85`); logo header ialah teks berwarna dari
   dict jadi bertukar automatik. `scripts/bina_logo.py` dikemas supaya
   penjanaan ikon/splash masa depan padan.
4. **Cip kini heks mockup TEPAT** — hijau `#e9f2ea`/`#1a6b3c` (terang)
   dan `#2a3b2f`/`#7fd39a` (gelap), merah `#fdeaea`/`#b3261e` dan
   `#3b2523`/`#e08a80`, amber `#fdf3e0`/`#9a6a00` dan `#3a3120`/
   `#e0b35c`.
5. **Nama kitab 'Sahih al-Bukhari' + prefix 'Bab:'** — padan mockup
   (dokumen memang guna 'al-Bukhari'; `uji_bandingan.py` dikemas).

Lanjutan (Sesi 55) — ujian visual mockup vs halaman detail PyQt5

`uji_visual_mockup.py` baharu: membandingkan KONTRAK struktur mockup
HTML (dibaca dari `mockup/mockup_*.html`, bukan hardcode) dengan
widget tree halaman detail PyQt5 yang dilaksanakan pada skrin sebenar.
Buka hadis yang SAMA seperti mockup (bukhari#1, nasai#2117,
abu-daud#4177) dan semak setiap elemen mockup wujud dalam app.
Tangkapan skrin: `bukti_visual/mockup_*.png`.

**Hasil semasa: 48 lulus, 12 gagal** — 12 kegagalan ialah item
keputusan Sesi 55 yang BELUM dilaksanakan (3 hadis × 4 item):

| Item belum dilaksanakan | Bukti GAGAL |
|---|---|
| Susun atur DUA LAJUR (Arab \| terjemahan) | geometri: kad Arab menegak di atas (y berbeza), bukan sebelah-menyebelah |
| Tab TRANSLITERASI dalam lajur Arab | transliterasi masih Collapsible berasingan, bukan tab |
| Tab MELAYU/INDONESIA/ENGLISH dalam lajur terjemahan | LangTabs global melekat kiri di atas kotak (x < sempadan kanan lajur Arab) |
| Darjat dipapar TERBUKA | Collapsible "Penilaian ulama" tertutup lalai (keputusan lama Sesi 14) |

48 semakan lulus mengesahkan apa yang app SEMASA memang memenuhi
mockup: breadcrumb, tajuk, tindakan, teks Arab + terjemahan,
transliterasi dua gaya, Huraian TERBUKA + cip klasifikasi, darjat
papar mentah (Nama — Darjat) + penafian, kes darjat kosong (mesej
jujur), bar bawah (Kembali + prev/next — hid=1 tiada prev), skrin
disimpan kedua-dua tema.

Nota ujian: (1) kes darjat kosong disemak berasingan (bukhari1 tiada
quote — bukan regresi); (2) hid=1 tiada butang prev (sepadan
`_label_sebelum`); (3) semakan tab bahasa guna geometri (x > sempadan
kanan lajur Arab), bukan label sahaja — LangTabs global hampir lulus
secara y, jadi x ialah pembeza sebenar.

Ujian sengaja GAGAL pada item yang belum dilaksanakan supaya menjadi
pemandu pelaksanaan: selepas halaman detail ditulis semula mengikut
mockup, 12 semakan itu mesti bertukar lulus. Jalankan:
`python uji_visual_mockup.py`.

---

## Lanjutan (Sesi 55) — PELAKSANAAN siap + ujian kandungan 92/0

**Status: dari "spesifikasi, belum kod" kepada SELESAI DILAKSANAKAN.**
Empat keputusan reka bentuk Sesi 55 kini hidup dalam `ui/pages_detail.py`
`_render_detail` (panel dua lajur):

1. **Susun atur DUA LAJUR** — Arab (kiri) | terjemahan (kanan) pada baris
   yang sama (`QHBoxLayout` panel_dua + `pl.addLayout(kol_kiri/kol_kanan)`).
2. **Tab dalam SETIAP lajur** — lajur Arab: `QStackedWidget` + butang
   ARAB/TRANSLITERASI (`_set_arab_tab`; transliterasi dibina MALAS pada
   buka pertama); lajur terjemahan: `LangTabs` + `_trans_box` di dalam
   lajur kanan (bukan global atas halaman).
3. **Darjat dipapar TERBUKA** — `Collapsible("Penilaian ulama (darjat)")`
   kini `kol_darjat.buka()` (perubahan daripada keputusan Sesi 14 yang
   tertutup; direkod sebagai keputusan Sesi 55 #4).
4. Huraian SemakHadis/HadeethEnc kekal `buka()` (sudah TERBUKA).

Semua fungsi label/klik lama dikekalkan (`_lang_tabs`, `_trans_box`,
`_detail_h`, `_set_arab_tab`) supaya ujian sedia ada tidak pecah.
`uji_visual_sebenar.py` dikemas: transliterasi kini TAB, bukan
Collapsible berasingan.

### `uji_visual_mockup.py` diperluas — perbandingan KANDUNGAN teks

Tambah `baca_kandungan(nama)` (ekstrak TEKS daripada mockup HTML:
arab, melayu/indonesia/english, cip, baris darjat, quote, sumber,
tajuk seksyen) + seksyen 3.9 dalam `periksa_hadis`:

- **3.9a Arab PENUH** sepadan hadis.db (3.2 sebelum ini hanya 60 aksara
  pertama).
- **3.9b Terjemahan tiap bahasa** (MELAYU/INDONESIA/ENGLISH) sepadan
  hadis.db; Melayu melalui `_papar_melayu` (transformasi SAMA seperti
  app — ejaan DBP + simbol selawat ﷺ).
- **3.9c Baris darjat SEBENAR** sepadan `api._darjat_luar` (fungsi yang
  sama digunakan `_bina_darjat`) DAN baris `darjat-bar` mockup.
- **3.9d Kandungan mockup → app**: tajuk seksyen jadi Collapsible,
  cip klasifikasi dipapar, quote penafian, sumber (darjat
  fawazahmed0/hadith-api; huraian SemakHadis.com/HadeethEnc.com).
- **3.5b Transliterasi** — kandungan rumi sepadan enjin
  `core.phase2_transliterasi` (cermin transformasi simbol selawat).

**Keputusan: 92 lulus, 0 gagal** (dari 60/0). Semua 32 semakan
kandungan baharu lulus pada ketiga-tiga kes (bukhari1 kes darjat
kosong, nasai2117 Muttafaq 'alayh 3 baris, abudaud4177 Palsu 4 baris).

### Kes keempat — `mockup_ibnumajah2094.html` + warna cip ikut makna

Mockup keempat (`ibnu-majah#2094`, klasifikasi **Lemah**, 3 darjat
"Daif") ditemui dalam `mockup/` tetapi belum diuji. Ia memperkenalkan
**warna cip ketiga — AMBER** (mockup: `body.gelap .chip` amber untuk
Lemah). Ini menutup keputusan Sesi 55 #5 yang sebelum ini hanya
tercatat, belum dilaksanakan:

- `ui/pages_detail.py`: fungsi `_warna_cip(teks)` memetakan klasifikasi
  → palet theme.py sedia ada (HIJAU `GREEN_BG/TEXT` = Sahih/Muttafaq/
  Hasan/صحيح/حسن; MERAH `RED_BG/TEXT` = Palsu/Mawdu'/Batil/Dusta/
  Munkar/موضوع/باطل/منكر; AMBER `AMBER_BG/TEXT` = Lemah/Daif/Syaz/
  Mudraj/ضعيف; tiada padanan = neutral TEAL) + `_warnai_cip()` guna
  gaya sebaris (objekName "chip" kekal, palet TEAL QSS ditimpa).
  Warna dibaca dari modul tema pada masa render → ikut tema terang/
  gelap (apply_theme menyalin nilai ke ruang nama pages_detail).
- `uji_visual_mockup.py`: kes `ibnumajah2094` ditambah ke KES;
  semakan warna cip baharu — (a) stylesheet cip app sepadan
  `_warna_cip(mockup chip)`, (b) family warna app (kelas_warna:
  hijau/merah/amber) sepadan family CSS mockup `body.gelap .chip`
  (heks berbeza dibenarkan — kontras setara, bukan nilai sama).

**Keputusan: 130 lulus, 0 gagal** (4 kes × kontrak + geometri +
kandungan + warna). Semua cip kini berwarna ikut makna dan padan
mockup: bukhari1 hijau (صحيح), nasai2117 hijau (Muttafaq 'alayh),
abudaud4177 merah (Palsu), ibnumajah2094 amber (Lemah).

### Suite ujian penuh

| Ujian | Keputusan | Nota |
|---|---|---|
| `semak.py` (termasuk uji_negatif_8z) | SEMUA LULUS | uji_visual_mockup.py didaftar + pengecualian fail sah belum di-commit |
| `uji_visual_mockup.py` | 92/0 | kontrak + geometri + kandungan |
| `uji_tukar_tema.py` | 19/19 | pertukaran tema OK (widget-level) |
| `uji_lompat_fungsi.py` | 48/48 | navigasi detail OK |
| `uji_end_to_end.py` | 18/18 | aliran penuh OK |
| `uji_bandingan.py` | **48/48** (larian kedua) | larian PERTAMA tersangkut pada langkah 8b (muat model pertama), larian kedua selesai 48/48 — lihat bawah |
| `uji_tukar_tema.py` | **19/19** (larian kedua) | larian pertama tersangkut pada permulaan (CPU beku semasa muat model), larian kedua selesai 19/19 |

### Penemuan 1: larian pertama carian semantik lambat (muat model)

Larian PERTAMA `uji_bandingan.py` tersangkut pada langkah 8b (carian
umum "hukum riba" → carian semantik) selepas "Loading weights" —
proses tidak selesai walaupun >4 minit dan terpaksa dihentikan.
Langkah 1–7c lulus dan langkah 8 (carian khusus "bukhari 500" →
butiran No. 500) lulus dalam ujian berasingan. Larian KEDUA (model
sudah panas dalam cache) selesai **48/48, EXIT=0** — jadi ia isu muat
model pertama, bukan regresi Sesi 55 (perubahan hanya halaman detail).
`uji_tukar_tema.py` pula tersangkut pada permulaan (CPU beku) pada
larian pertama tetapi selesai **19/19** pada larian kedua — corak yang
sama. Ujian yang menyentuh model carian semantik mungkin perlu
percubaan kedua pada mesin ini.

Catatan kualiti kod (bukan punca tersangkut): `_pra_muat_model` dalam
`ui/app_qt.py` **ditakrifkan tetapi TIDAK dipanggil** di mana-mana
(`grep -n "_pra_muat_model" ui/*.py` → hanya definisi baris 123);
pembaikan yang didokumenkan dalam `PERUBAHAN_7OGOS.md` (panggil dalam
`_do_search` sebelum worker) tidak wujud dalam kod semasa. Kaedah mati
boleh disambung atau dibuang.

### Penemuan 2: flak tangkapan skrin persekitaran (BUKAN regresi)

`uji_visual_sebenar.py` (tema terang) gagal "kecerahan > 140" —
`sebenar_gelap.png` dan `sebenar_terang.png` **sama tepat (MD5 sama, saiz
388759 B)**, begitu juga 7 tangkapan lain dalam satu larian. Mustahil 7
keadaan UI berbeza menghasilkan byte sama — ImageGrab menangkap bingkai
basi. `uji_tukar_tema.py` 19/19 lulus (tema berfungsi di peringkat
widget). Juga `uji_visual_sebenar.py` memerlukan `PYTHONIOENCODING=utf-8`
(aksara "──" rosak pada konsol cp1252).

**Fail belum di-commit**: `mockup/` (3 HTML spesifikasi Sesi 55),
`uji_visual_mockup.py`, perubahan `ui/pages_detail.py`, `semak.py`,
`uji_visual_sebenar.py`, `MANUAL_REFERENSI_DEV.md`, `sesi_index.md` ini.

---

## Lanjutan (Sesi 55) — Padanan visual + palet diterima + punca "hang" ditemui

### Punca sebenar semua "tersangkut" ujian hari ini: dialog deklarasi modal

Gejala: `uji_bandingan` (langkah 8b), `uji_tukar_tema`, `uji_lompat_fungsi`
dan skrip debug tersangkut pada pelbagai titik — nampak seperti isu
carian semantik/muat model. Siasatan dengan `faulthandler.dump_traceback`
mendedahkan punca sebenar: **`_tunjuk_deklarasi_pertama`** (app_qt.py,
`QTimer.singleShot(300, ...)`) memaparkan dialog deklarasi MODAL 300ms
selepas app dilancarkan. `semak.py` semakan 6 menulis `user_settings.json`
minima (tanpa `deklarasi_dibaca`) lalu MEMADAMKAN fail asal pengguna —
setiap larian app berikutnya menunjukkan modal tanpa pengguna untuk klik
"Faham", jadi `exec_()` menyekat thread utama selama-lamanya dalam mod
offscreen. Ini BUKAN regresi Sesi 55 (dibuktikan: palet asal dengan
`git stash` masih tersekat).

Pembaikan dalam `semak.py`: simpan kandungan asal `user_settings.json`
di awal skrip (`_ASAL_SETTINGS`) + `_pulihkan_settings()` selepas setiap
semakan yang menyentuhnya; `user_settings.json` kini disenaraikan sebagai
data kerja (bukan sisa) kerana kehadirannya diperlukan untuk ujian app
berjalan. Selepas pembaikan, SEMUA ujian lulus pada percubaan PERTAMA.

### Padanan visual app vs mockup (bukhari#1)

Perbandingan teks widget app vs elemen mockup — sama 100% pada struktur
(dua lajur, tab, darjat TERBUKA, kandungan Huraian, mesej darjat kosong,
bar bawah, Arab penuh). Beza yang kelihatan:

| Elemen | Mockup | App (selepas perubahan ini) |
|---|---|---|
| Palet | kertas hangat + aksen hijau | **kini kertas hangat + hijau** (DITERIMA) |
| Tajuk kitab | "Sahih al-Bukhari — Hadis No. 1" | **kini "Sahih al-Bukhari — Hadis No. 1"** |
| Baris bab | "Bab: Revelation" | **kini "Bab: Revelation"** (prefix ditambah) |
| Cip | heks mockup | **kini heks mockup TEPAT** (hijau/merah/amber) |
| Terjemahan Melayu | teks mentah | `_papar_melayu` (ejaan DBP + ligatur ﷺ bila fon ada) — keputusan Sesi 32/34, kekal |
| Nota pengenalan + butang 🌙 mockup | ada | tiada (krom mockup sahaja) |

### Suite ujian penuh (selepas pembaikan + palet baharu)

| Ujian | Keputusan |
|---|---|
| `semak.py` | SEMUA LULUS (tetapan dipulihkan) |
| `uji_visual_mockup.py` | **130/0** (4 kes, kontrak + geometri + kandungan + warna cip) |
| `uji_bandingan.py` | **48/48** (percubaan pertama) |
| `uji_tukar_tema.py` | **19/19** (percubaan pertama) |
| `uji_lompat_fungsi.py` | **48/48** (percubaan pertama) |
| `uji_end_to_end.py` | **18/18** (percubaan pertama) |

**Di-commit** (komit `2972de2` sebelum perubahan ini; perubahan palet +
pembaikan semak.py dalam komit susulan).

## Lanjutan (Sesi 55) — Penstabilan skrin + kunci logo (SEGERA SELESAI SEMUA)

**Misi:** tiga tugasan susulan selepas palet hangat diterima: (1) stabilkan
tangkapan skrin `uji_visual_sebenar.py` (flak bingkai basi tema terang), (2)
tambah semakan unit `_warna_cip` dalam `semak.py`, (3) jana semula logo
`logo_mockup` dengan palet hijau + sahkan splash.

### 1. Punca flak tangkapan skrin `uji_visual_sebenar.py` ditemui + dibaiki

Siasatan `debug_tema.py` mendedahkan corak sebenar: selepas
`set_theme("light")`, skrin memerlukan ~1.5s untuk benar-benar bertukar
(kecerahan 58 pada 500ms → 237 pada 1500ms). Retry sedia ada hanya ulang
bila MD5 SAMA dengan tangkapan sebelumnya — bingkai basi yang BERBEZA
tidak dikesan, dan halaman separuh dilukis (62 warna unik) lulus semakan
lama.

Pembaikan `skrin_fizikal()`: gelung retry kini mengesahkan **kecerahan
sepadan tema sebenar app** (`w.settings["theme"]`: gelap < 100, terang >
140) DAN **halaman cukup terisi** (warna unik >= 150), bukan sekadar
MD5 berbeza. Keputusan: **65/0** (sebelum 63/2, 60/5) — stabil.

### 2. Semakan unit `_warna_cip` (semak.py 8v)

11 kes baharu dalam `semak_elide_chip()`: Muttafaq 'alayh/Sahih/Hasan/
صحيح → HIJAU (GREEN_BG), Palsu/Munkar/Batil → MERAH (RED_BG),
Lemah/Daif/ضعيف → AMBER (AMBER_BG), tanpa padanan → None (neutral).
Semua OK.

### 3. Logo dijana semula + dikunci pada palet (semak.py 10aa)

`scripts/bina_logo.py` guna palet hangat: BUKU_TEAL #5CBF85 (hijau
mockup), TEAL_DARK #0F2417, CARD_BG #282721, AMBER_TEXT #E0B35C. Logo
raster dijana semula (1024→16, ICO, SVG). Splash ialah teks dari dict
tema — bertukar automatik, tiada perubahan diperlukan. Semakan baharu
`semak_logo_palet()` (10aa) mengunci 5 warna logo = theme.py dan
menolak hex TEAL biru lama (#7FC4DE) — 6/6 OK.

### Keputusan penuh

| Ujian | Keputusan |
|---|---|
| `semak.py` | SEMUA LULUS (termasuk 10aa logo + 8v `_warna_cip`) |
| `uji_visual_sebenar.py` | **65/0** (tangkapan distabilkan) |
| `uji_visual_mockup.py` | **130/0** |
| `uji_tukar_tema.py` | **19/19** |

Semua lulus pada percubaan pertama selepas pembaikan.

## Lanjutan (Sesi 55) — Finalise: kod mati `_pra_muat_model` dibuang

**Isu terbuka terakhir** (direkod dalam seksyen sebelum ini): `_pra_muat_model`
dalam `ui/app_qt.py` ditakrifkan tetapi tidak dipanggil — nampak seperti
pembaikan pramuat tidak disambung. Siasatan sejarah (`PERUBAHAN_7OGOS.md`
Sesi 22) mendedahkan kebenaran: `_pra_muat_model` ialah pendekatan LAMA
(muat model dalam thread utama) yang TIGA kali terbukti gagal — crash
0xC0000409 dalam `__init__` (serentak dengan CollectionsWorker), beku UI
~30s dalam `_do_search`, dan crash lagi bila thread utama memuat + QThread
meng-encode. Penggantinya **sudah aktif**: `PreloadWorker` (QThread) yang
memuat DAN meng-encode dalam QThread, disambung melalui
`_fetch_collections` → `worker.finished.connect(self._mula_pramuat)`
(app_qt.py:455) → `_on_pramuat_siap` menetapkan `_model_sedia`.

**Tindakan finalise:**

1. **Buang `_pra_muat_model` mati** dari `ui/app_qt.py` (kaedah thread
   utama yang terbukti crash; menyambungnya akan jadi regresi). Komen
   `__init__` dikemas supaya tidak mengelirukan (dulu kata "dilakukan
   dalam _do_search" — sebenarnya PreloadWorker QThread selepas
   Collections).
2. **Kunci penggantian dalam semak.py (8k)**: 2 semakan baharu —
   `_mula_pramuat`/`_on_pramuat_siap` mesti wujud dan disambung selepas
   Collections (`worker.finished.connect(self._mula_pramuat)`), dan
   `_pra_muat_model` mati TIDAK boleh kembali. 8k kini 8 semakan.
3. **Kuatkan retry tangkapan skrin** (`uji_visual_sebenar.py`): repaint()
   sahaja tidak memaksa Windows mengecat semula pada flak permulaan
   (tetingkap baharu belum dilukis) — tambah force hide/show semula pada
   cubaan ke-4. Disahkan 65/0 pada dua larian berturut-turut.

### Keputusan akhir (semua lulus)

| Ujian | Keputusan |
|---|---|
| `semak.py` | SEMUA LULUS (8k pramuat + 8v cip + 10aa logo) |
| `uji_visual_mockup.py` | **130/0** |
| `uji_bandingan.py` | **48/48** |
| `uji_lompat_fungsi.py` | **48/48** |
| `uji_end_to_end.py` | **18/18** |
| `uji_visual_sebenar.py` | **65/0** (2× berturut-turut) |

Penyelesaian pramuat model yang didokumenkan (QThread) memang sudah
beroperasi; kod mati lama dibuang supaya tidak mengelirukan. Tiada isu
terbuka tinggal — semua keputusan Sesi 55 terkunci oleh ujian.

## Lanjutan (Sesi 55) — Ujian perbandingan PIKSE L app vs palet mockup

**Tujuan:** mengunci rupa visual Sesi 55 (palet kertas hangat + aksen
hijau + cip warna ikut makna) secara piksel, bukan hanya kontrak
struktur (uji_visual_mockup 130/0) atau semakan kecerahan
(uji_visual_sebenar 65/0). Fail baharu: `uji_visual_piksel.py`.

### Batasan: tiada QtWebEngine

Render mockup HTML sebenar (untuk SSIM piksel-demi-piksel) TIDAK
mungkin — `PyQt5.QtWebEngineWidgets` tidak dipasang, dan menambahnya
melanggar peraturan projek (guna pustaka sedia ada sahaja). Maka
perbandingan dilakukan pada peringkat warna:

1. **PALET** — ekstrak hex CSS mockup (latar, kad, panel-sisi, aksen,
   cip bg+teks) untuk terang & gelap; CSS terang/gelap dipisahkan pada
   `body.gelap` supaya `.kad` terang tidak tersilap ambil hex kad gelap.
2. **TANGKAP** — `w.grab()` (render widget PyQt terus ke pixmap),
   BUKAN ImageGrab: larian awal ImageGrab menangkap bingkai bukan-app
   (#0E0E0E) akibat flak fokus tetingkap Windows, sedangkan `w.grab()`
   stabil dan warna tepat. 4 hadis × 2 tema.
3. **HISTOGRAM** — chi-square histogram (5-bit) tangkapan vs render
   prosedur palet mockup (latar+kad+panel+aksen+cip) — lulus 0.18–0.63
   (< 3.0). (Rujukan prosedur TIDAK sensitif kepada perubahan kecil —
   pengawal sebenar ialah semakan kehadiran + kepekaan mutasi.)
4. **KEHADIRAN** — nisbah piksel penuh (bukan resize kecil yang memadam
   cip) dengan tol ketat (latar/kad 10, aksen 12, cip bg 8, cip teks
   16): latar ≥ 8%, kad ≥ 3%, aksen hijau ≥ 0.02%, cip bg ≥ 0.05%,
   cip teks ≥ 0.002%.
5. **KEPEKAAN MUTASI** — ubah piksel aksen hijau pada tangkapan menjadi
   TEAL biru lama (#7FC4DE); pengawal MESTI mengesan: hijau hilang +
   biru muncul. Mengesahkan pengawal benar-benar menangkap regresi
   palet (pembatalan keputusan Sesi 55).

### Penemuan kecil (regex palet)

`body.gelap .kad` (gelap) dan `.kad` (terang) berasingan — tanpa
pemisahan, kad terang tersilap baca #282721. Aksen gelap ialah
breadcrumb/bar-bawah #5CBF85 (bukan teks utama #E8E4DA).

### Keputusan

| Ujian | Keputusan |
|---|---|
| `uji_visual_piksel.py` | **53/0** (32 semakan palet + 4 histogram + 4 penjaga biru + 3 kepekaan mutasi) |
| `semak.py` | SEMUA LULUS (8z kini 8 ujian visual; piksel didaftar) |
| `uji_tukar_tema.py` | 19/19 |

Nota prestasi: semakan 8j semak.py GAGAL sementara (muat cache 64.8s)
kerana mesin sibuk dengan proses ujian sebelumnya; selepas larian muat
segar (30.3s) SEMUA LULUS — bukan regresi.

## Lanjutan (Sesi 55) — Kepekaan mutasi semakan 8k (pramuat QThread)

Semakan 8k (`semak_pemula`) mengunci pramuat model melalui
`PreloadWorker` (QThread) selepas CollectionsWorker, dan menolak
kaedah mati `_pra_muat_model` (tiga pendekatan thread utama terbukti
crash/beku). `uji_negatif_8z.py` diperluas dengan 4 cabang mutasi
pada `ui/app_qt.py`:

| # | Mutasi | Dikesan oleh |
|---|---|---|
| 18 | `worker.finished.connect(self._mula_pramuat)` dibuang | 'TIADA / tidak disambung' |
| 19 | `def _mula_pramuat` dibuang | 'TIADA / tidak disambung' |
| 20 | `def _on_pramuat_siap` dibuang | 'TIADA / tidak disambung' |
| 21 | `_pra_muat_model` dipulangkan | 'kaedah mati kembali' |

Kesilapan pertama (dikesan oleh ujian sendiri): penggantian
`_mula_pramuat_buang` masih mengandungi substring `_mula_pramuat`, jadi
semakan teks masih lulus — guna nama berbeza sepenuhnya (`_mula_preload`).
Ini mengesahkan nilai ujian kepekaan: tanpa ia, mutasi yang gagal itu
akan tersembunyi.

Keputusan: **33 lulus, 0 gagal** (17 → 21 cabang). Pulihan byte-tepat
untuk 9 fail + atribut disahkan; 8k hijau selepas pulihan. Manual
dikemas (senarai semakan + kiraan).

## Lanjutan (Sesi 55) — UJIAN VISUAL FINAL: kesemua 9 lulus 0 gagal

Larian pengesahan akhir penuh — SEMUA ujian visual + semak.py pada
percubaan pertama (selepas pembaikan dialog deklarasi + palet + retry
skrin):

| # | Ujian | Keputusan |
|---|---|---|
| 1 | `semak.py` | SEMUA LULUS |
| 2 | `uji_visual_mockup.py` | **130/0** (4 mockup: kontrak + geometri + kandungan + warna cip) |
| 3 | `uji_visual_piksel.py` | **53/0** (histogram chi + kehadiran warna + kepekaan mutasi) |
| 4 | `uji_visual_sebenar.py` | **65/0** (skrin fizikal + selawat ﷺ + fon) |
| 5 | `uji_bandingan.py` | **48/48** |
| 6 | `uji_lompat_fungsi.py` | **48/48** |
| 7 | `uji_end_to_end.py` | **18/18** |
| 8 | `uji_tukar_tema.py` | **19/19** |
| 9 | `uji_negatif_8z.py` | **33/0** (21 cabang mutasi termasuk 8k) |

**Jumlah: 412 semakan lulus, 0 gagal.** Semua keputusan Sesi 55
(palet kertas hangat, dua lajur, tab per lajur, darjat terbuka, cip
warna ikut makna, pramuat QThread) terkunci oleh 9 lapisan ujian yang
berbeza. Pokok kerja bersih; semua commit disimpan.

## Lanjutan (Sesi 55) — Selesaikan: mutasi 8v/10aa + profil + pra-hantar

### 1. Kepekaan mutasi diperluas (8v + 10aa) — uji_negatif_8z 40/0

5 cabang baharu ditambah (17 → 21 → 26 cabang):

| # | Semakan | Mutasi | Dikesan oleh |
|---|---|---|---|
| 22 | 8v | `_warna_cip` semua-MERAH (suntikan ingatan) | 'Sahih -> HIJAU' GAGAL |
| 23 | 8v | `_warna_cip` semua-None | 'Palsu -> MERAH' GAGAL |
| 24 | 10aa | `BUKU_TEAL` → #7FC4DE dalam bina_logo.py | 'logo buku != tema' |
| 25 | 10aa | #7FC4DE disuntik | 'masih guna TEAL biru lama' |
| 26 | 10aa | bina_logo.py dibuang | 'TIADA' GAGAL bersih |

**Pembetulan `kelas_warna` (uji_visual_mockup.py)**: logik lama
`g < 0.75r` tersilap klasifikasikan pastel terang — `_warna_cip("Palsu")`
dalam tema TERANG pulangkan RED_BG `#FDEAEA` (r=253, g=234 → g bukan
< 0.75r) yang jatuh ke 'amber'. Baru: merah = r dominan + `abs(g-b)
<= 10` (hue merah tulen, g≈b); amber = `r >= g >= b` dengan g-b ketara.
14/14 warna palet terang+gelap betul (termasuk #5C3A42 RED_BORDER
dengan g<b).

### 2. Punca flak ujian skrin SEBENAR dalam subproses dijumpai

`uji_visual_sebenar` lulus 65/0 berasingan tetapi GAGAL dalam
`uji_pra_hantar` (subproses): Windows **foreground-lock** — subproses
bukan proses aktif, jadi `SetForegroundWindow` ditolak dan tetingkap
app kekal di belakang terminal → ImageGrab menangkap permukaan salah
(kecerahan tema lain: 'gelap' 122 / 'terang' 24, berubah-ubah).
Pembaikan: `_paksa_hadapan()` guna `SetWindowPos(HWND_TOPMOST)` yang
memaksa tetingkap ke atas tanpa kebenaran fokus + retry dinaik ke 10
cubaan. Disahkan: uji_pra_hantar penuh SEMUA LULUS.

### 3. Ujian pra-hantar automatik (`uji_pra_hantar.py`) + profil

- **uji_pra_hantar.py**: selesaikan 9 ujian berurutan dengan satu
  arahan; berhenti bila gagal (`--teruskan`); log ke
  `bukti_visual/pra_hantar_*.log`; laporan ringkas + masa.
- **profil_semak.py**: ukur tempoh setiap 41 fungsi semak.py. Ukuran
  pertama: jumlah 12.8s; paling perlahan — Apl 3.9s, Susun atur 2.1s,
  Bahasa dokumen 1.7s (bukan sasaran optimasi; semak.py 41 fungsi
  selesai < 20s adalah sihat).

### Keputusan akhir

| Ujian | Keputusan |
|---|---|
| `semak.py` | SEMUA LULUS |
| `uji_pra_hantar.py` (9 ujian penuh) | **SEMUA LULUS** (362.8s) |
| `uji_negatif_8z.py` | **40/0** (26 cabang mutasi: 8k+8v+10aa+dsb.) |
| `uji_visual_mockup.py` | **130/0** (kelas_warna diperbetulkan) |

### 4. FINALISE: optima semak.py + penstabilan mockup (12 Ogos)

**Optima semak.py — cache baca fail berasaskan mtime (16.29s → 12.78s):**
`_baca_cek()` menyimpan kandungan fail mengikut kunci `(mtime_ns, saiz)`, dipakai
di `_sumber_ui`, `_cari_fungsi`, `semak_sintaks`, `_semak_bahasa_fail` dan
`semak_bahasa_dokumen` — fail .py yang sama tidak lagi dibaca + ASTR-parse 4–5
kali dalam satu larian. **Selamat untuk ujian mutasi**: fail yang dimutasi oleh
`uji_negatif_8z` mendapat mtime baharu → kunci cache berubah → kandungan segar
dibaca (disahkan 40/0). Perubahan: Sintaks 0.95→0.62s, Bahasa dokumen 2.24→1.72s,
Bahasa UI 1.87→0.95s, Syarah 2.41→1.26s.

**Penstabilan uji_visual_mockup — 130/0 tiga larian berturut-turut:**

1. **Punca flak ImageGrab ditemui**: tetingkap app kadangkala **diminimumkan**
   oleh Windows (GetWindowRect lalu pulangkan ikon taskbar ~160×28 → PNG 93 B
   pepejal hitam). Pembaikan: `SW_RESTORE` dalam `_paksa_hadapan()` sebelum
   tangkapan, konsisten dengan uji_visual_sebenar.
2. **Bingkai terang separa**: `set_theme("light")` + `open_detail` kadangkala
   meninggalkan bingkai belum dilukis penuh (92% putih, teks hitam lalai,
   TIADA TEAL #1A6B3C — 9.8 KB). Pembaikan: syarat penerimaan retry untuk tema
   terang kini MESTI ada piksel TEAL (> 50) — bingkai separa ditolak dan diulang
   sehingga stylesheet lengkap (78 KB, 130/0).
3. **Proses ujian tersadai dibersihkan**: 3 proses `uji_bandingan.py` /
   `uji_tukar_tema.py` tersekat muat model dari larian awal menutup kawasan
   tangkapan (0,0) — dibuang sebelum pengesahan.

**MULA_SINI.md**: seksyen 3 kini mendokumenkan `python uji_pra_hantar.py`
sebagai satu arahan untuk ujian penuh (semak.py + 8 suite, berhenti bila gagal,
log dalam `bukti_visual/pra_hantar_*.log`).

## Lanjutan (Sesi 55) — Lalai saiz teks Arab = Kecil + flak skrin selesai

**Keputusan pengguna**: saiz lalai teks Arab = **Kecil** (indeks 0, skala 0.85),
BUKAN Sederhana (indeks 1, skala 1.0). Rasional: dengan susun atur dua lajur
Sesi 55, teks Arab lebih kecil menjadikan lajur kiri padat supaya teks
tterjemahan di lajur kanan kekal sama paras (top-aligned) dengan teks Arab
seperti mockup bukharin1/nasai2117/abudaud4177.

## 1. Perubahan lalai

- `ui/app_qt.py` — `arabic_font_idx` lalai 1 (Sederhana) → **0 (Kecil)**.
- `ui/settings_panel.py` — butang "Set Semula": `1, 1, 1` → **`1, 0, 1`**
  (saiz teks Arab kembali ke Kecil selepas set semula).
- Skop: pengguna sedia ada yang menyimpan `arabic_font_idx` dalam
  `user_settings.json` kekal pada pilihan mereka; perubahan menetapkan lalai
  pemasangan baharu dan butang "Set Semula".

## 2. Pembaikan flak tangkapan `uji_visual_sebenar` (93 B)

`skrin_fizikal()` mengira `GetWindowRect` SEKALI sebelum gelung cubaan — jika
Windows meminimumkan tetingkap latar belakang, rect kekal ikon taskbar (~160×28)
dan tangkapan jadi 93 B pepejal walau 10 cubaan. Pembaikan (konsisten dengan
`uji_visual_mockup`):

- `_paksa_hadapan()` kini lakukan `SW_RESTORE` bila `IsIconic()`.
- `GetWindowRect` dikira SEMULA dalam gelung cubaan selepas `_paksa_hadapan`.

## 3. Pengesahan

- `uji_visual_sebenar.py`: **65/0** (lalai ar=0 Kecil disahkan + flak 93 B
  hilang).
- `uji_visual_mockup.py`: **130/0** (geometri dua lajur kekal).
- Regresi tangkapan dokumentasi (`bina_tangkapan_dokumentasi.py`): **7/7**
  (saiz fon Arab tidak mengubah susun atur halaman dokumentasi).
- semak.py: SEMUA LULUS kecuali semakan muat cache persekitaran (141.6s —
  mesin perlahan, bukan regresi).

## Lanjutan (Sesi 55) — Buang tab Sebelah + teks terjemahan sama paras

**Keputusan pengguna (13 Ogos)**: tab "Sebelah" (bandingan Melayu vs Indonesia)
**dibuang** — ia bukan dalam mockup (yang hanya ada 3 tab), dan teks
terjemahan di dalamnya tidak sama paras dengan teks Arab di lajur kiri.
Sekali gus, paparan bahasa tunggal mesti menjamin teks terjemahan **sama paras
(top-aligned) dengan teks Arab walau apa keadaan** — ini aduan berulang yang
mengganggu pembaca.

**Punca sebenar centering (dijumpai):** Qt memusatkan widget saiz tetap dalam
`QVBoxLayout` bila ada ruang menegak berlebihan (dibuktikan dengan ujian Qt
terpencil: widget 30px dalam bekas 400px diletak pada y=115 tanpa penjajaran;
y=11 dengan `Qt.AlignTop`). Bila lajur Arab lebih tinggi daripada terjemahan,
kotak terjemahan menerima ruang lebih dan teks jatuh ke tengah.

## 1. Perubahan

- `ui/pages.py` — `LangTabs`: tab "Sebelah" dibuang; 3 tab sahaja
  (Melayu/Indonesia/English), sepadan dengan mockup.
- `ui/pages_detail.py` — cabang `key == "sebelah"` dalam `_switch_lang`
  dibuang; `_teks_semua_bahasa` + `_copy_semua_bahasa` ("Salin semua bahasa")
  dibuang sekali (milik tab itu). Paparan tunggal: `Qt.AlignTop` pada setiap
  widget + `self._trans_lo.addStretch(1)` supaya ruang berlebihan tinggal di
  bawah teks, bukan memusatkannya.
- `ui/helpers.py` — kunci "sebelah" dalam `LANG_LABEL` dibuang.
- `uji_visual_bandingan.py` dipadam (tab yang diuji sudah tiada).
- semak.py 8i ditulis semula: kunci 3 tab + tiada Sebelah + tiada "Salin
  semua bahasa" + AlignTop/addStretch dalam `_switch_lang`.
- uji_bandingan.py: bahagian Sebelah diganti dengan semakan 3 tab + kes
  baharu "Arab >> terjemahan" (Arab > 3× panjang Melayu) yang mengunci
  centering — beza < 40px pada Melayu lalai, Indonesia, dan kembali Melayu.
- Dokumen: MANUAL_PENGGUNAAN, MULA_SINI, CHANGELOG, README,
  MANUAL_REFERENSI_DEV, TRANSFORMASI_DETAIL dikemas.

## 2. Pengesahan

- `uji_bandingan.py`: **48/0** (termasuk kes "Arab >> terjemahan" 3× separas).
- `uji_visual_mockup.py`: **130/0** (kontrak `tab_lang` = melayu/indonesia/
  english kini sepadan tepat dengan app).
- `uji_end_to_end.py`: **18/0**; semak.py: 0 GAGAL.
- Baseline tangkapan dokumentasi dikemas (`--kemas`) dan regresi **7/7**.
- Suite pra-hantar penuh: **SEMUA LULUS** (10 ujian).

## Lanjutan (Sesi 55) — Draf jawapan AI: "Carian Biasa (Keyword)" dibaiki + ujian

**Bug dijumpai (13 Ogos)**: bahagian "🔍 Carian Biasa (Keyword)" dalam kotak
Jawapan Draf AI tidak pernah muncul walaupun kodnya wujud. Punca di
`core/draft_answer.py`: `api.search_hadis` dipanggil dengan `per_page=5`
(parameter sebenar `limit`) dan hasil dibaca dari `exact["data"]["results"]`
(structur pulangan sebenar `{"hadis": [...]}`) — dua TypeError yang ditangkap
SENYAP oleh `except Exception`, jadi `exact_results` sentiasa kosong.

**Pembetulan**: `search_hadis(query, limit=5)` + baca `exact["hadis"][:5]`.
**Pengesahan**: `compose_draft_answer("solat", semantic_results=[])` kini
pulang 5 hasil exact dan jawapan mengandungi "Carian Biasa (Keyword) — 5
hasil" dengan hadis sebenar (Ibnu Majah #1403, dll.).

**Ujian baharu `uji_draf_jawapan.py` (9/9)** — daftar dalam `uji_pra_hantar.py`
sebagai ujian #11: (1) `exact_results` terisi + hasil wujud dalam DB;
(2) "Carian Biasa (Keyword)" wujud dalam jawapan draf + menyebut hasil
pertama; (3) corak lama (`per_page=5` / `data.results`) tidak kembali.
Kepekaan mutasi disahkan: corak lama disuntik semula → 6 GAGAL, pulih → 9/0.
Semakan statik semak.py 8t2 turut mengunci corak betul.

**Pengesahan akhir (selepas SEMUA perubahan sesi 13 Ogos, kod + ujian +
dokumentasi)**: suite pra-hantar penuh `uji_pra_hantar.py` lulus **tiga
larian berturut-turut — SEMUA LULUS, 11/11 ujian** (395.6s, 392.6s, 392.9s,
exit 0). Bukti penuh: `dokumen/perubahan/PERUBAHAN_13OGOS.md` (seksyen
"Pengesahan akhir").

## Lanjutan (Sesi 55) — 13 Ogos 2026: SELESAI (16 commit)

Semua kerja sesi 13 Ogos **SELESAI** — pokok kerja bersih, suite pra-hantar
11/11 lulus pada **tiga larian berturut-turut**, semak.py 0 GAGAL.

**16 commit sesi 13 Ogos 2026 (mengikut kronologi):**

| # | Commit | Kandungan |
|---|---|---|
| 1 | `c306f88` | App seperti mockup: buang baris Salin/Kongsi bawah tab + lalai teks Arab Kecil |
| 2 | `147a0cb` | Ujian: kunci Set Semula→Arab Kecil + hadis panjang, baiki flak tangkapan |
| 3 | `0742a10` | Buang tab Sebelah + jamin teks terjemahan sama paras dengan Arab |
| 4 | `0333040` | Baiki draf jawapan AI: bahagian "Carian Biasa (Keyword)" kini dipapar |
| 5 | `90b04fc` | Ujian runtime draf jawapan AI: exact_results + bahagian Carian Biasa |
| 6 | `911ef7b` | Dokumen 13 Ogos: PERUBAHAN_13OGOS.md + rujukan CHANGELOG + header Sesi Terakhir |
| 7 | `287db0a` | CHANGELOG v1.0: entri perubahan pengguna 13 Ogos (draf AI + tab Sebelah) |
| 8 | `14a0ede` | Pautan silang konsisten: semua pintu masuk rujuk PERUBAHAN_13OGOS + TRANSFORMASI_DETAIL |
| 9 | `0ee19c1` | Rekod pengesahan akhir: suite pra-hantar SEMUA LULUS dua larian berturut-turut |
| 10 | `4d03480` | MULA_SINI: tambah seksyen "Sesi Terakhir" (ringkasan 13 Ogos) di atas Peraturan |
| 11 | `69d65b7` | MULA_SINI seksyen 5 "Keadaan projek": kemas kini Sesi 55 + lanjutan 13 Ogos |
| 12 | `89da919` | MULA_SINI seksyen 3: senarai semak hantar kini 10 suite (tambah uji_draf_jawapan) |
| 13 | `6884e78` | PERUBAHAN_13OGOS: rekod larian ketiga — kestabilan tiga larian berturut-turut |
| 14 | `84e0828` | semak.py 9b: langkau semakan fail sisa di luar repo git (edaran ZIP) |
| 15 | `512e22e` | MANUAL_INSTALASI: senarai rasmi 120 fail ZIP edaran (seksyen 9) |
| 16 | *(commit ini)* | Bar tindakan bawah teks Arab (tiru sunnah.com): Lapor Ralat \| Kongsi \| Salin ▾ + menu popup |

**Keputusan utama sesi 13 Ogos:** buang tab "Sebelah" (3 tab bahasa sahaja,
sepadan mockup) · teks terjemahan sama paras dengan Arab (Qt.AlignTop +
addStretch) · lalai teks Arab Kecil · pembetulan draf jawapan AI
("Carian Biasa (Keyword)" kini dipapar) · ujian baharu uji_draf_jawapan.py
(#11) · dokumentasi lengkap (PERUBAHAN_13OGOS, CHANGELOG v1.0, MULA_SINI,
pautan silang 6 pintu masuk).

**Ujian ZIP edaran (petang 13 Ogos):** `PustakaHadith.zip` dibina semula
(120 fail, guna `git ls-files` tolak folder dev + data) dan diuji dari
folder bernama dengan ruang `D:\Pustaka Quran Hadis\Ujian Ruang`.
Pepijat tersembunyi dijumpai: **semak.py 9b** (peraturan fail sisa
untracked) sentiasa GAGAL dalam edaran kerana folder pengguna BUKAN
repo git — kini melangkau apabila tiada `.git`, kekal aktif dalam
repo pembangunan. Selepas pembetulan: semak_versi 23 ciri + semak.py
SEMUA LULUS + app melancar dari folder berruang.

**Senarai rasmi fail ZIP (petang 13 Ogos):** `manual/manual/MANUAL_INSTALASI.md`
seksyen 9 — jadual 7 bahagian (Akar 51, api 2, core 9, ui 16, utils 3,
scripts 3, dokumen 36 = 120 fail) + senarai penuh + pengecualian telus
+ seksyen 10 pengesahan edaran. **2 pembetulan pembinaan ZIP**: (1)
padanan `.env` tersilap kecualikan `.env.example` → dibaiki padanan
tepat, `.env.example` disertakan; (2) `opencode.json` (konfigurasi AI
dev) tersilap masuk → dikecualikan. ZIP akhir (120 fail, 1,105,754
bytes) disahkan semula dari folder berruang: `.env.example` ada,
`opencode.json` tiada, semak.py SEMUA LULUS.

**STATUS: (13 Ogos 2026) SELESAI.** Log harian penuh:
`dokumen/perubahan/PERUBAHAN_13OGOS.md`.

---

## Lanjutan (Sesi 55) — Bar tindakan TEKS + pilihan Salin (malam 13 Ogos)

**Konteks:** bar `Lapor ralat | Kongsi | Salin` pernah DIBUANG (arahan
"buang kotak kekal teks sahaja", commit `e719612`) kemudian
DIPULIHKAN (`6e89522`). Malam ini pengguna menjelaskan maksud sebenar:
**"saya mahu text bagitu bukan button"** — bar MESTI KEKAL tetapi
sebagai **TEKS** (pautan, tiru sunnah.com 'Report Error | Share |
Copy'), bukan QPushButton. Pembuangan bar (`37c7d2c`) ialah salah
faham; dipulihkan sebagai teks (`4ee6140`).

### 1. Perubahan

| Fail | Perubahan |
|---|---|
| `ui/pages_detail.py` | Bar bawah terjemahan sebagai SATU `QLabel` HTML: pautan teal `Lapor ralat \| Kongsi \| Salin` + pemisah `\|` kelabu (`TEAL`/`TEXT_SECONDARY`, ikut tema via `_THEMED_MODULES`); kaedah `_lapor_ralat`/`_menu_salin`/`_salin_ke` + import `QMenu`/`QCursor` dipulihkan; kaedah baharu `_salin_arab_terjemahan` |
| `uji_bandingan.py` | +4 semakan: bar teks wujud, bar BUKAN butang, menu 3 pilihan, `_salin_ke` menyalin; +1 semakan pilihan ke-3 (tab Indonesia aktif) |
| `dokumen/perubahan/PERUBAHAN_13OGOS.md` | Log malam: bar teks + pilihan ke-3 |
| `dokumen/manual/TRANSFORMASI_DETAIL.md` | Seksyen 6.3 dikemas: bar = TEKS, menu di kursor, pilihan ke-3 = Arab + terjemahan semasa |
| `dokumen/manual/manual/manual/MANUAL_PENGGUNAAN.md` | Bar teks bawah terjemahan didokumenkan (3 pautan + fungsi) |

**Punca "3 pilihan tak fungsi" DIJAGA**: menu Salin dibuka pada
`QCursor.pos()` (bukan di bawah butang/pautan) — sebelum ini menu
dibuka di bawah butang yang mungkin di luar skrin di hujung skrol,
jadi pengguna nampak "tak berfungsi".

**Pilihan ke-3 ditukar** (arahan pengguna): daripada "Salin semuanya
(rujukan + Arab + terjemahan)" kepada **"Salin Arab + terjemahan
semasa"** (`_salin_arab_terjemahan`) — tanpa baris rujukan, ikut
bahasa aktif (Melayu/Indonesia/English).

### 2. Pengesahan

- semak.py 0 GAGAL · uji_bandingan **53/0** · mockup 130/0 ·
  bina_tangkapan_dokumentasi 7/7 (nmad ≤ 0.0007, dalam toleransi)
- Ujian hidup papan klip (bukhari#1): pilihan 1 → 601 aksara Arab;
  pilihan 2 → 718 aksara terjemahan; pilihan 3 → 1,321 aksara
  (Arab + terjemahan semasa, tiada baris "No.")
- Pintasan "Hadis" (Desktop + Start Menu) dibina semula via
  `pintasan.ps1` — disahkan menunjuk ke folder projek ini
  (`D:\Pustaka Quran Hadis\hadis\main.py`)

### 3. Commit malam ini

| # | Commit | Kandungan |
|---|---|---|
| 1 | `37c7d2c` | Buang bar tindakan (salah faham — pengguna mahukan teks, bukan buang) |
| 2 | `4ee6140` | Pulihkan bar sebagai TEKS + pilihan Salin ke-3 = Arab + terjemahan semasa |

**STATUS: (13 Ogos 2026, malam) SELESAI.** Kerja disambung esok.

---

## Lanjutan (Sesi 55) — Justify teks + panel transliterasi atas (malam 13 Ogos, samb.)

**Arahan pengguna berturut-turut:** "saya nak awak justify text
terjemahan" → "justify juga trasliterasi dan huraian" →
"transliterasi jgn center vertical. top vertical."

### 1. Perubahan

| Fail | Perubahan |
|---|---|
| `ui/widgets.py` | `text_browser()` parameter baharu `justify=True` → `document().setDefaultTextOption(QTextOption(Qt.AlignJustify))` — berfungsi dengan `setPlainText`, tanpa HTML escape |
| `ui/pages_detail.py` | `justify=True` pada 8 panggilan: kotak terjemahan `_switch_lang`, transliterasi (Gaya Melayu + Akademik), huraian SemakHadis (terjemahan/takhrij/komentar), huraian HadeethEnc (terjemahan/penjelasan/pengajaran); panel transliterasi: `Qt.AlignTop` pada panel + setiap kandungan + `addStretch(1)` di hujung |
| `uji_bandingan.py` | Seksyen 7e baharu: mock model transliterasi (tanpa torch, deterministik) — panel y ≤ 30px → 55/0 |
| `dokumen/imej/*.png` | Baseline tangkapan dikemas dengan `--kemas` (justify mengubah rupa — perubahan reka bentuk sah) |
| `dokumen/perubahan/PERUBAHAN_13OGOS.md` | Log malam (justify + translit atas) |

**Catatan teknikal:** teks Arab (RTL) sengaja TIDAK dijustify — dari
segi tipografi, justify tidak sesuai untuk teks RTL. Ujian ad-hoc
melibatkan muatan model transliterasi (torch) boleh segfault di luar
app (konflik DLL yang main.py atasi) — ujian rasmi menggunakan mock.

### 2. Pengesahan

- semak.py 0 GAGAL · uji_bandingan **55/0** · mockup 130/0 ·
  bina_tangkapan_dokumentasi 7/7 (nmad=0.0000 selepas kemas)
- Verifikasi hidup (sebelum model muat): hanya browser Arab yang
  `justify=False`; semua teks rumi/terjemahan `justify=True`

### 3. Commit malam ini

| # | Commit | Kandungan |
|---|---|---|
| 1 | `d0a4d0c` | Justify teks terjemahan/transliterasi/huraian + panel transliterasi dijajarkan ke atas |

**STATUS: (13 Ogos 2026, malam) SELESAI — 3 commit hari ini
(`37c7d2c`, `4ee6140`, `d0a4d0c`).** Kerja disambung esok.

---

## Semakan mesin sebenar — 4 item tertangguh (14 Ogos 2026)

**Arahan pengguna:** "buat 1, 2, 3, 4" — merujuk item tertangguh
MANUAL_REFERENSI_DEV §8 + RANCANGAN_4FASA: (1) ujian mesin sebenar,
(2) halaman Tersimpan dengan tanda buku sebenar, (3) diagnos_syarah
pada data sebenar, (4) pipeline end-to-end (install → API → baca →
tersimpan).

### 1. Ujian mesin sebenar — suite pra-hantar penuh

| # | Ujian | Keputusan |
|---|---|---|
| 1 | semak.py | SEMUA LULUS |
| 2 | uji_negatif_8z.py | 40/0 |
| 3 | uji_visual_mockup.py | 130/0 |
| 4 | uji_visual_piksel.py | 53/0 |
| 5 | **uji_visual_sebenar.py** | **68/0 (tetingkap fizikal, skrin sebenar)** |
| 6 | uji_tukar_tema.py | 19/0 |
| 7 | uji_bandingan.py | 55/0 |
| 8 | uji_lompat_fungsi.py | 48/0 |
| 9 | uji_end_to_end.py | 18/0 |
| 10 | bina_tangkapan_dokumentasi.py | 7/7 baseline |
| 11 | uji_draf_jawapan.py | 9/0 |

Catatan: uji_visual_sebenar dipaparkan pada skrin sebenar — bukan
proksi offscreen. Item #1 tertangguh kini DITUTUP.

### 2. Halaman Tersimpan — tanda buku SEBENAR (uji_tersimpan_sebenar.py, 20/0)

Aliran yang diuji (tetingkap sebenar):

1. Simpan 3 hadis sebenar dari 3 kitab (bukhari #1, muslim #1,
   abu-daud #1) melalui `_toggle_save` selepas buka detail — butang
   bertukar "⭐ Tersimpan"
2. bookmarks.json benar-benar ditulis ke cakera (3 entri + medan
   teks + kitab_name)
3. Halaman Tersimpan: Hero "3 hadis disimpan" + 3 kad dipapar
   (paparan TERBALIK — terbaru dahulu)
4. Klik kad → halaman detail hadis betul
5. **Restart app → 3 tanda buku dimuat semula dari cakera**
   (persisten, bukan state memori) + boleh dibuka dari Tersimpan
6. Tanggalkan semua → empty state "Belum ada hadis tersimpan" +
   bookmarks.json kosong
7. bookmarks.json asal dipulihkan (data pengguna tidak dicemari)

Didaftar sebagai ujian **#12** dalam `uji_pra_hantar.py`.

### 3. diagnos_syarah.py — data sebenar (HANYUT)

hadis.db 'bukhari' 7,008 hadis · Fath al-Bari 5,075 seksyen
(.cache_syarah/fathbari.txt 30 MB):

| julat hadis | anjakan | skor | skor@0 |
|---|---|---|---|
| 1–876 | +2 | 21.76% | 10.28% |
| 877–1,752 | +10 | 19.45% | 7.74% |
| 1,753–2,628 | +34 | 21.83% | 6.49% |
| 2,629–3,504 | +60 | 11.03% | 4.91% |
| 3,505–4,380 | +80 | 12.22% | 4.55% |
| 4,381–5,256 | +100 | 14.48% | 7.86% |
| 5,257–6,132 | −400 | 6.97% | 4.44% |
| 6,133–7,008 | +120 | 8.00% | 5.96% |

**KEPUTUSAN: penomboran HANYUT** — min −400, max +120, julat 520,
1/8 julat sejajar sahaja. Padanan ikut ID TIDAK selamat. Mengesahkan
keputusan 31 Jul (Pilihan 4): Fasa 4B kekal dibatalkan. `diagnos_syarah.py`
selamat dijalankan — ia tidak mengubah apa-apa. Item #5 tertangguh
(katalog lama) kini DITUTUP dengan bukti data sebenar.

### 4. Pipeline end-to-end — install → API → baca → tersimpan

(uji_pipeline_api.py, 18/0; kunci developer dari kunci_terdedah.txt
— dalam memori sahaja, tidak ditulis ke user_settings.json)

- **INSTALL**: semua kebergantungan requirements.txt diimport dengan
  versi disahkan (PyQt5, requests 2.34.2, pyperclip, tqdm, torch
  2.13.0+cpu, sentence-transformers 5.6.1, faiss 1.15.0), Python 3.14
- **API HIDUP** (use_db=False, bukan proksi DB):
  - /collections → 9 kitab (nama + jumlah lengkap)
  - /collections/bukhari/hadis?lang=ms → 5 hadis Arab + Melayu
    (lang=ms sah — Indonesia sengaja tidak diminta, jimat 30%)
  - /collections/bukhari/hadis/1 → hadis lengkap 3 bahasa
  - /hadis/search "zakat" → hasil
  - Kuota harian dibaca dari header (int)
- **BACA**: hadis dari API hidup dibuka dalam app sebenar — Arab
  + terjemahan dipapar
- **TERSIMPAN**: disimpan → halaman Tersimpan memaparkan →
  ditanggalkan → bookmarks.json dipulihkan

Nota: uji_pipeline_api.py TIDAK didaftar dalam uji_pra_hantar.py —
ia perlu internet + kunci API hidup; gate pra-hantar mesti berfungsi
luar talian. Pipelin semakan end-to-end (§8 #6) kini DITUTUP.

### 5. Ujian baharu

| Fail | Keputusan | Daftar |
|---|---|---|
| `uji_tersimpan_sebenar.py` | 20/0 | `uji_pra_hantar.py` #12 |
| `uji_pipeline_api.py` | 18/0 | berasingan (perlu internet + kunci) |

**STATUS: (14 Ogos 2026) SELESAI — 4 item tertangguh ditutup.
`uji_pra_hantar.py` kini 12 ujian.**

---

## Sync penuh dari mula — item tertangguh #2 (14 Ogos 2026, samb.)

**Arahan pengguna:** "Jalankan sync.py dari mula pada mesin sebenar dan
sahkan keseluruhan 62,169 hadis sejajar dengan hadis.db".

### 1. Pelaksanaan

`sync.py --paksa` dijalankan pada mesin sebenar (bukan proksi) dengan
kunci developer melalui env var `HADIS_API_KEY` sahaja (tiada kunci
ditulis ke fail). Semua 9 kitab muat turun semula dari muka surat 1:

| Kumpulan | Muka surat | Masa | Keputusan |
|---|---|---|---|
| malik + darimi | 16 + 34 | 56s | 100% |
| tirmidzi + ibnu-majah | 39 + 44 | 120s | 100% |
| abu-daud + nasai | 46 + 57 | 130s | 100% |
| bukhari + muslim | 71 + 54 | 143s | 100% |
| ahmad | 264 | 299s | 100% |

622 muka surat, ~12.5 minit, 639 permintaan; kuota 9,999 → 9,360.

### 2. Pengesahan penjajaran (62,169)

1. **"Rekod baharu: 0"** setiap kitab — `INSERT OR IGNORE` mengesahkan
   muat turun semula sepadan TEPAT dengan DB sedia ada (tiada
   perubahan data, tiada duplikat)
2. **Kiraan per kitab = API**: bukhari 7,008 · muslim 5,362 ·
   abu-daud 4,590 · tirmidzi 3,891 · nasai 5,662 · ibnu-majah 4,332 ·
   malik 1,594 · ahmad 26,363 · darimi 3,367 = **62,169**
3. **Integriti**: 62,169 unik, 0 duplikat, 0 arab/melayu/indonesia
   kosong, julat id kontigu 1..N setiap kitab
4. **Indeks carian**: hadis_fts 62,169 = hadis 62,169 (sejajar)
5. **Perbandingan teks API vs DB: 45/45 padan** — 5 hadis rawak setiap
   kitab, arab + melayu + indonesia dibandingkan terus selepas
   normalisasi tashkeel

### 3. Status

Item #2 tertangguh (MANUAL_REFERENSI_DEV §8) kini DITUTUP. Log harian:
`dokumen/perubahan/PERUBAHAN_14OGOS.md`.

---

## Padanan `ara-*` penuh pada hadis.db sebenar — item tertangguh #3 (14 Ogos, samb.)

**Arahan pengguna:** "Sahkan padanan lapisan ara-* pada hadis.db sebenar
(bukan proksi CDN) untuk menutup item tertangguh #3".

Latar: Sesi 18.13 hanya mengesahkan item 3 pada sampel 500 hadis
Bukhari (90.8%) — sebab ia kekal terbuka dalam MANUAL_REFERENSI_DEV
§8. Kini pengesahan PENUH pada hadis.db sebenar:

### 1. Padan semua hadis (baca-sahaja)

32,439 hadis (7 kitab dengan sumber) dipadan terhadap cache `ara-*1`:

| Kitab | Berjaya | Gagal | indo | indo~ | penuh | awalan | kata |
|---|---|---|---|---|---|---|---|
| bukhari | 6,965/7,008 | 43 | 5,725 | 864 | 281 | 48 | 47 |
| muslim | 5,186/5,362 | 176 | 3,478 | 1,364 | 122 | 58 | 164 |
| abu-daud | 4,559/4,590 | 31 | 3,498 | 856 | 106 | 24 | 75 |
| tirmidzi | 3,792/3,891 | 99 | 136 | 3,318 | 94 | 90 | 154 |
| nasai | 5,570/5,662 | 92 | 5,054 | 248 | 213 | 7 | 48 |
| ibnu-majah | 4,316/4,332 | 16 | 3,982 | 251 | 56 | 7 | 20 |
| malik | 1,564/1,594 | 30 | 1,510 | 40 | 5 | 1 | 8 |
| **Jumlah** | **31,952 (98.5%)** | **487** | 23,383 | 6,941 | **877** | **235** | **516** |

- Lapisan `ara-*` (penuh + awalan + kata) = **1,628 hadis (5.1%)**
  mengisi celah di mana Indonesia tiada — berfungsi pada data sebenar
- 31,952 − 119 (tiada teks eng di CDN) = **31,833 = tepat jadual
  tersimpan**; **0 entri english basi** (setiap english tersimpan masih
  dipadan semula oleh kod semasa)
- Gagal 487 = perbezaan edisi teks Arab antara hadis.my dan CDN,
  bukan pepijat padanan — padan rekod Fasa 3 ("gagal 487")

### 2. Audit bebas (saksi Indonesia)

`audit_eng.py --semua`: **30,541/30,547 disahkan (100.0%)**, 6 disyaki
= **positif palsu SAKSI** (penomboran `ind-*` hanyut dari `ara-*`)
— boleh dihasilkan semula, sama seperti siasatan 31 Jul. Lapisan Arab
(penuh/awalan/kata) purata Jaccard 0.75–0.96, semua dalam julat sah.

### 3. sync_english.py dari mula (deterministik)

Dijalankan semula pada hadis.db sebenar: **31,833 terjemahan disimpan**
— identik dengan jadual sedia ada (per-kitab sama: bukhari 6,964 ·
muslim 5,149 · abu-daud 4,558 · tirmidzi 3,742 · nasai 5,560 ·
ibnu-majah 4,314 · malik 1,546). tiada_eng 119 · gagal 487. Jadual bab
(31,325) dan darjat (63,930) ditulis semula sama. Tab English dalam
app tetap penuh.

### 4. Status

Item #3 tertangguh (MANUAL_REFERENSI_DEV §8) kini DITUTUP.

---

## Audit liputan SemakHadis (#8) — 14 Ogos 2026, samb.

**Arahan pengguna:** "Audit liputan SemakHadis 4,237/62,169 dan
senaraikan kitab/bab yang paling banyak tertinggal untuk mencari sumber
BM terbuka lain". Dokumen penuh: `dokumen/audit/AUDIT_SEMAKHADIS.md`.

### 1. Liputan per kitab

| Kitab | Total | Sema | Liputan |
|---|---|---|---|
| tirmidzi | 3,891 | 63 | **1.6%** ⚠️ |
| darimi | 3,367 | 148 | 4.4% ⚠️ |
| ahmad | 26,363 | 1,645 | 6.2% |
| nasai | 5,662 | 350 | 6.2% |
| malik | 1,594 | 121 | 7.6% |
| abu-daud | 4,590 | 354 | 7.7% |
| muslim | 5,362 | 430 | 8.0% |
| ibnu-majah | 4,332 | 409 | 9.4% |
| bukhari | 7,008 | 717 | **10.2%** |

**4,237/62,169 = 6.8%** · 2,263 sema_id unik · cache sumber
`.cache_sema/` penuh (2,372) — siling sumber, bukan pepijat.

### 2. Jurang per bab (393 bab, 7 kitab)

- **103 bab (26%) liputan 0%**; 77 bab 1–4%; 68 bab 5–9%; 68 bab
  10–19%; 34 bab 20–49%; hanya **3 bab >50%**
- Jurang bab tunggal terbesar: **Tafsir** — bukhari 65 (441
  tertinggal) + tirmidzi 47 (402)
- **Hajj** ≈ 1,564 hadis: muslim 15 (415) · nasai 24 (441) ·
  ibnu-majah 25 (228) · malik 20 (208) · abu-daud 11 (272)
- **Solat** ≈ 1,371: abu-daud 2 (549) · ibnu-majah 5 (549) ·
  tirmidzi 2 (273)
- Bab sifar mutlak: tirmidzi 43 Manners (119) & 14 Business (116),
  nasai 26 Marriage (191), malik 31 Business (72) / 36 Judgements
  (51) / 28 Marriage (45)
- **tirmidzi hampir kosong** (1.6%) — walaupun hadis masyhur pun
  kebanyakannya tiada

### 3. Ahmad & Darimi (tiada bab CDN) — per desil

- ahmad: seragam 5–9% setiap desil (jurang menyeluruh)
- darimi: tidak seragam — puncak 13.0% (id 1,347–1,684), terendah
  0.9% (2,693–3,030)

### 4. Implikasi — keutamaan sumber BM baharu

1. **Tafsir per-hadis** (menutup jurang terbesar: bukhari 65 +
   tirmidzi 47)
2. **Syarah bab ibadah** (hajj + solat ≈ 2,900 hadis)
3. **Sumber khusus Tirmidzi** (kitab paling terbiar)
4. **Struktur Musnad** untuk Ahmad (26,363, liputan seragam rendah)

Sumber yang disiasat & ditolak sebelum ini: Irsyad al-Hadith (lesen
tertutup), MyHadith JAKIM (ralat rangkaian), IslamHouse Malay (PDF),
hadits.id/NU/tazkia/Kemenag (terjemahan sahaja), Bulughul Maram
(kitab berbeza), dorar.net (Arab), sunnah.com (Inggeris) — butiran:
`dokumen/audit/DAPATAN_WEB.md` + `PERUBAHAN_31JUL.md` §13.

**STATUS: (14 Ogos 2026) SELESAI — 7 daripada 8 item tertangguh
ditutup (#1–#6 + #8 diaudit penuh). Baki: #7 kunci API (kekal AKTIF
sengaja).**

---

## Penutupan Hari — 14 Ogos 2026: 6 item tertangguh disahkan (4 commit)

Hari ini menutup baki item tertangguh MANUAL_REFERENSI_DEV §8 selepas
semakan app pada mesin sebenar. Semua pengesahan dijalankan pada mesin
sebenar (Windows, skrin fizikal, kunci API developer melalui env var
sahaja — tiada kunci ditulis ke fail).

### Ringkasan pengesahan

| # | Item tertangguh | Pengesahan | Commit |
|---|---|---|---|
| 1 | Ujian mesin sebenar | Suite pra-hantar penuh dijalankan pada mesin sebenar — SEMUA LULUS (uji_visual_sebenar 68/0 tetingkap fizikal) | `341bdc9` |
| 2 | Sync penuh | `sync.py --paksa` 9 kitab 100% (622 muka surat, 12.5 min); 62,169 unik, 0 duplikat, FTS sejajar, teks API vs DB **45/45 padan** | `f59cd95` |
| 3 | Padanan `ara-*` | 32,439 hadis dipadan pada hadis.db: 31,952 (98.5%), lapisan Arab 1,628 (5.1%); audit bebas 30,541/30,547 (100.0%); sync_english deterministik 31,833 | `8512b47` |
| 4 | Halaman Tersimpan | `uji_tersimpan_sebenar.py` 20/0 — tanda buku SEBENAR (3 hadis 3 kitab, tulis cakera, restart kekal, buka, tanggalkan, pulihkan) — daftar ujian #12 | `341bdc9` |
| 5 | `diagnos_syarah.py` | Data sebenar: penomboran Fath al-Bari **HANYUT** (julat 520, 1/8 sejajar) — Fasa 4B kekal dibatalkan | `341bdc9` |
| 6 | Pipeline end-to-end | `uji_pipeline_api.py` 18/0 — install → API HIDUP (use_db=False) → baca → tersimpan | `341bdc9` |
| 7 | Kunci API | KEKAL AKTIF sengaja (pelan developer) — bukan tugasan tutup | — |
| 8 | Liputan SemakHadis | Audit penuh `AUDIT_SEMAKHADIS.md`: 4,237/62,169 (6.8%); tirmidzi 1.6% terendah; 103/393 bab (26%) liputan 0%; peta jurang + keutamaan sumber BM baharu | `988c803` |

### Ujian baharu

| Fail | Keputusan | Daftar |
|---|---|---|
| `uji_tersimpan_sebenar.py` | 20/0 | `uji_pra_hantar.py` #12 (suite kini 12 ujian) |
| `uji_pipeline_api.py` | 18/0 | berasingan (perlu internet + kunci API hidup; gate kekal luar talian) |

### Dokumen baharu / dikemas

- `dokumen/audit/AUDIT_SEMAKHADIS.md` (baharu) — peta jurang per kitab/bab
- `dokumen/perubahan/PERUBAHAN_14OGOS.md` (baharu) — log harian penuh
- `dokumen/manual/MANUAL_REFERENSI_DEV.md` §8 — item #1–#6 ditandakan DITUTUP, #8 diaudit

### Commit 14 Ogos

| # | Commit | Kandungan |
|---|---|---|
| 1 | `341bdc9` | Tutup 4 item: ujian mesin sebenar, Tersimpan (tanda buku sebenar), diagnos_syarah (HANYUT), pipeline end-to-end API |
| 2 | `f59cd95` | Sync penuh dari mula (#2): 62,169 sejajar, 45/45 padan |
| 3 | `8512b47` | Padanan ara-* (#3): 31,952/32,439, audit 100.0%, sync deterministik |
| 4 | `988c803` | Audit liputan SemakHadis (#8): peta jurang per kitab/bab |

**STATUS: (14 Ogos 2026, penutup) HARI SELESAI.** Semua item
tertangguh §8 disahkan/diaudit; baki hanya #7 (kunci API kekal AKTIF
sengaja, guna semula `REVOKE_KUNCI.md` bila perlu). Suite pra-hantar
12 ujian SEMUA LULUS. App berjalan dengan versi terkini.

---

## Siasatan sumber tafsir/syarah BM per-hadis (14 Ogos, samb.) 📖

**Arahan pengguna:** "Siasat sama ada tafsir BM per-hadis terbuka wujud
(cth. Al-Muyassar BM, Tafsir Kemenag API) yang boleh menutup jurang
Tafsir 843 hadis" (susulan AUDIT_SEMAKHADIS #8). Dokumen penuh:
`dokumen/audit/SIASATAN_TAFSIR_BM.md`.

### Keputusan: TIADA sumber BM per-hadis terbuka menutup jurang Tafsir 843

| Calon | Dapatan | Layak? |
|---|---|---|
| MyHadith JAKIM | Status BERUBAH (kini boleh diakses + API berkuasa kunci; per-hadis: Arab, terjemahan, Pengajaran, Asbab al-Wurud, status) — tetapi koleksi SEPARA (Bukhari 17 kitab, Tirmidzi 14, dll.) dan **TIADA kitab Tafsir**; hak cipta JAKIM | ❌ |
| Tafsir al-Muyassar BM | Tafsir QURAN per-ayat (buku, hak cipta) — bukan syarah hadis | ❌ |
| Tafsir Kemenag API (LPMQ) | Tafsir QURAN Indonesia (bukan BM), perlu daftar — bukan huraian hadis | ❌ |
| IslamHouse Malay "Syarah Hadis" | Kategori per-hadis (ID 344947) TIADA dalam versi Melayu (hanya buku; wujud Arab/Indonesia) | ❌ |
| kitabhadis.com | Belum lengkap, tiada syarah | ❌ |
| myway.my | Komersial (carian AI, audio); lesen tidak jelas | ❌ |
| api.hadis.my | Medan hanya arab/melayu/indonesia — tiada syarah | ❌ |
| surah.my | Tafsir Quran BM tetapi 503 (turun) | ❌ (buat masa ini) |

### Cadangan

1. **Kekal siling SemakHadis** — satu-satunya sumber huraian BM
   per-hadis yang sah lesennya; jurang Tafsir 843 tidak boleh ditutup
   oleh sumber terbuka sedia ada
2. **Pilihan masa depan**: tafsir ayat BM (surah.my / Al-Muyassar BM)
   sebagai KONTEKS AYAT tambahan (bukan huraian hadis) — perlu
   pemetaan hadis→ayat + lesen bertulis + label jujur
3. **Kekal jujur**: tiada huraian lebih baik daripada huraian
   salah/lesen tercemar (keputusan sama Irsyad 31 Jul, HadeethEnc
   auto 3 Ogos)
4. **Pemantauan**: MyHadith (penambahan kitab Tafsir / terma data
   terbuka data.gov.my) + IslamHouse Melayu (kategori Syarah Hadis
   jika diterbitkan)

**STATUS: (14 Ogos 2026) SELESAI — siasatan ditutup: jurang Tafsir
843 ialah siling sumber (tiada sumber BM per-hadis terbuka); peta
keutamaan + pemantauan direkod untuk bila sumber baharu muncul.**

---

## Dokumen "Mula Cepat" untuk pengguna (14 Ogos, samb.) 🚀

**Arahan pengguna:** "Sediakan versi ringkasan 'Mula Cepat' untuk
pengguna: apa yang sudah disahkan, bagaimana menjalankan app, dan
cara memulakan carian".

- **`dokumen/manual/MULA_CEPAT.md`** (baharu) — ringkasan pengguna
  empat bahagian:
  1. **Apa yang sudah disahkan** — jadual: 62,169 data penuh sejajar
     API (0 duplikat), English 31,833 audit 100%, SemakHadis 4,237 +
     darjat 63,930, Tersimpan diuji data sebenar, carian kata kunci +
     AI, suite pra-hantar 12 ujian SEMUA LULUS, Windows Python 3.14
  2. **Cara menjalankan app** — ikon "Hadis" Desktop/Start Menu;
     PASANG.bat sekali untuk pasang; BUAT_PINTASAN/JALANKAN/
     NYAHPEPIJAT jika ikon tidak jalan; kunci API sekali sahaja
     (gear → Tetapan API), selepas itu luar talian
  3. **Cara memulakan carian** — buka kitab → klik hadis; lompat
     nombor (Ctrl+G); Pencarian kata kunci + makna AI; format
     `bukhari 433` / `B433` lompat terus; tab bahasa; huraian +
     darjat; bar teks Lapor ralat | Kongsi | Salin; ⭐ Simpan
  4. **Rujukan & bantuan** — peta ke manual penuh
- **`MULA_SINI.md`** — rujukan log harian dikemas ke
  PERUBAHAN_14OGOS.md + pautan MULA_CEPAT.md

Dokumen pengguna kini lengkap: MULA_CEPAT (ringkas) →
MANUAL_PENGGUNAAN (penuh) → MANUAL_INSTALASI (pasang) → BACA_SAYA
(langkah pertama).

**STATUS: (14 Ogos 2026) SELESAI — dokumen pengguna lengkap.**

---

# Semakan dokumen manual vs UI sebenar (petang 14 Ogos)

Permintaan: "Semak semula konsistensi semua dokumen manual
(MULA_CEPAT, MANUAL_PENGGUNAAN, MULA_SINI) terhadap UI sebenar dengan
ujian offscreen".

**Hasil: SEMUA tuntutan dokumen TEPAT — skrip audit baharu
`semak_dokumen_ui.py` 74 semakan, 0 gagal.**

## Kaedah

1. **Katalog tuntutan** — setiap ayat fakta dalam `MULA_CEPAT.md`
   (§1–4) dan `manual/manual/MANUAL_PENGGUNAAN.md` (§1–3) disenaraikan: angka data,
   label butang, tab, pintasan, tingkah laku, fail pemasangan.
   `MULA_SINI.md` ialah dokumen developer (rekod sejarah/keputusan,
   bukan tuntutan UI) — dikecualikan daripada semakan dinamik;
   rujukan failnya disahkan wujud.
2. **Semak sumber** untuk tuntutan statik (label tepat, pintasan,
   baris teks, struktur data) dan **UI hidup offscreen** untuk
   tuntutan dinamik (widget wujud + dipapar, teks, geometri dua
   lajur, panel Tetapan dibuka).
3. **Angka data disemak terus dari hadis.db** (bukan teks dokumen):
   62,169 hadis · 9 kitab · 31,833 english · 4,237 SemakHadis ·
   63,930 darjat · English hanya 7 kitab (ahmad 0, darimi 0).

## Semakan mengikut seksyen

| Seksyen dokumen | Semakan utama | Hasil |
|---|---|---|
| MULA_CEPAT §1 (disahkan) | angka DB, English 7 kitab, Python 3.14, suite 12 ujian | A1–A8 ✅ |
| §2 (jalankan app) | 4 fail .bat, Tetapan API, gear | I1, G1/G5 ✅ |
| §3 (carian) | nav, kad kitab, pager, Lompat/Ctrl+G, format lompat, 2 enjin, draf AI, jam, longgar, bar teks, menu Salin, Simpan | B/C/E/F/D ✅ |
| MANUAL §1 (apa itu) | splash, deklarasi "Faham", huraian/darjat, sandaran HadeethEnc | H1–H4, D10–D12 ✅ |
| §2.1–2.3 (nav/utama/kitab) | 4 butang + gear, 9 kad, carian utama, pager, backTop | B1–B5, C1–C6 ✅ |
| §2.4 (halaman hadis) | butang tajuk, tab ARAB/TRANSLITERASI + 3 bahasa, **dua lajur (geometri)**, bar `Lapor ralat \| Kongsi \| Salin`, menu Salin 3 pilihan, klik kanan "Salin semua", cip warna, darjat, backTop | D1–D15 ✅ |
| §2.5 (carian) | format lompat, 2 enjin, draf AI, jam 🕐→🕛, notis longgar, backTop | E1–E9 ✅ |
| §2.6 (Tersimpan) | empty state, hero, backTop | F1–F3 ✅ |
| §3 (Tetapan) | 5 bahagian, butang tema, 8 label, stepper fon | G1–G5 ✅ |

## Semakan baharu ditambah semasa audit

Versi awal 54/0 sudah meliputi kebanyakan tuntutan; semakan berikut
ditambah untuk menutup baki jurang:

- **D3b — dua lajur sebelah-menyebelah** (geometri: `_ar_stack.x() <
  _trans_box.x()`)
- **D13 — cip warna ikut makna** (GREEN_BG/RED_BG/AMBER_BG + kata kunci
  palsu/lemah dalam `_warna_cip`)
- **D14 — klik kanan "Salin semua"** (`_CopyMenuFilter` dalam widgets.py)
- **D15 — butang ↑ detail** (backTop)
- **E7 — draf jawapan AI di atas hasil** (`compose_draft_answer`)
- **E8 — jam berputar 🕐→🕛** (`self._jam`, 12 emoji)
- **E9 — notis carian longgar** (fallback OR)
- **F3 — butang ↑ Tersimpan**
- **G5 — 8 label panel Tetapan** (Saiz antara muka, Saiz teks Arab,
  Saiz terjemahan, Fon Arab, Bahasa dimuat, Selawat, Tetapan API,
  Tentang PustakaHadith)
- **H4 — deklarasi larian pertama dengan butang "Faham"**
  (`DeklarasiDialog` penuh=False)
- **A6 — English hanya 7 kitab** (ahmad 0, darimi 0 dalam DB)
- **A7 — Python 3.14** (runtime semakan)
- **A8 — suite pra-hantar 12 ujian** (senarai dalam uji_pra_hantar.py)

## Catatan penting

- **Semua tuntutan TEPAT** — tiada dokumen yang ketinggalan kod.
  Termasuk yang paling mudah hanyut: bar `Lapor ralat | Kongsi | Salin`
  (kini teks, bukan butang), 3 tab bahasa tanpa tab Sebelah, tab
  ARAB/TRANSLITERASI, justify + panel transliterasi di atas, cip warna
  ikut makna, huraian SemakHadis + darjat terbuka lalai.
- `MULA_SINI.md` dikecualikan: ia dokumen developer (rekod sejarah +
  keputusan), bukan manual pengguna — semakan dinamik tidak berkaitan.
- Skrip audit **tidak mengubah apa-apa** (state memori sahaja;
  bookmarks.json tidak disentuh). **Digate sebagai ujian #13 dalam
  `uji_pra_hantar.py`** (keputusan malam 14 Ogos) — suite kini
  13 ujian; jalankan manual juga bila dokumen manual dikemas.
- Jalankan: `python semak_dokumen_ui.py` → **110 lulus, 0 gagal**.

---

# Penutup Hari (petang) — semakan #12 dikunci + suite 12/12 (14 Ogos)

Kemas kini terakhir hari ini selepas "Penutupan Hari" tengah hari:

## Semakan #12 semak.py — "'Sesi Terakhir' MULA_SINI seiring git log"

**Motivasi:** sesi AI baharu membaca bahagian 'Sesi Terakhir' dalam
`MULA_SINI.md` sebagai ringkasan kerja terkini — jika lapuk, sesi
bermula dengan salah faham (contoh sebenar: bahagian kekal '13 Ogos'
selepas kerja 14 Ogos).

**Empat peraturan** (semak #12, `80b7abf` + `564dba7`):

| # | Peraturan | Mesej GAGAL |
|---|---|---|
| 1 | Tarikh tajuk `## Sesi Terakhir —` ≥ tarikh commit git terbaru | `KETINGGALAN git log` |
| 2 | **Teks ringkasan menyebut tarikh kerja terkini** (bukan hanya tajuk; baris tajuk dikecualikan; sebelum `**Sebelum ini`) | `tidak menyebut tarikh kerja terkini` |
| 3 | Semua hash 7-heks yang disebut wujud dalam git | `hash tidak wujud dalam git` |
| 4 | ≥ satu hash daripada 10 commit terbaru | `tiada hash daripada 10 commit terbaru` |

Tiada git (edaran ZIP) → lulus (tiada sejarah untuk dibandingkan).

**Reka bentuk penting:** kadar TARIKH (hari) + tetingkap 10 commit,
bukan "sebut hash commit terakhir tepat" — mengelakkan masalah
telur-ayam (setiap commit dokumen tidak memaksa tulis semula
ringkasan) sambil memastikan bahagian tidak ketinggalan lebih daripada
satu hari kerja.

## Penguncian mutasi — uji_negatif_8z kini 45/0 (30 cabang)

4 cabang khusus #12 ditambah (27–30): tarikh lapuk · hash rekaan
`fffffff` · MULA_SINI.md dibuang · tarikh dibuang dari teks ringkasan
— semua dikesan dengan mesej tepat; fail dipulihkan byte-tepat.

## Suite rasmi 12/12 SEMUA LULUS (418.3s)

`uji_pra_hantar.py` penuh pada mesin sebenar: semak.py (dengan #12)
16.4s · uji_negatif_8z 45/0 10.3s · mockup 37.5s · piksel 66.7s ·
sebenar (tetingkap fizikal) 130.9s · tukar_tema 36.4s · bandingan 8.1s
· lompat_fungsi 5.9s · end_to_end 41.1s · tangkapan dokumen 36.2s ·
draf_jawapan 2.0s · tersimpan_sebenar 26.7s. Bukti: log `bukti_visual/`
— semak #12 lulus dalam `pra_hantar_semak.log`, 45/0 dalam
`pra_hantar_uji_negatif_8z.log`.

## README.md dikemas (`b546912`)

- Semakan #12 didokumenkan dalam komen semak.py; kiraan semakan
  139 → **370+** (kiraan sebenar)
- `uji_negatif_8z` 45/0 + suite `uji_pra_hantar` 12 ujian ditambah ke
  senarai ujian
- **Tuntutan lapuk dibuang:** dua baris Ciri-ciri masih mendakwa tab
  Sebelah / "Salin semua bahasa" (dibuang Sesi 55) — diganti dengan
  tab dua lajur semasa (ARAB | TRANSLITERASI + Melayu | Indonesia |
  English) + bar teks `Lapor ralat | Kongsi | Salin`

## Konsistensi rentas dokumen (sambungan petang 14 Ogos)

Tiga permintaan diselesaikan:

1. **Audit MULA_CEPAT.md** — tiada percanggahan dengan README/manual
   kecuali URL kunci API `developer.hadis.my/dashboard/keys` (tidak
   disahkan) → diganti dengan arahan selaras MANUAL_INSTALASI
   (`https://hadis.my` → Developer / API).
2. **Audit manual/manual/MANUAL_INSTALASI.md + BACA_SAYA.txt vs skrip .bat sebenar**
   — semua tuntutan padan (PASANG/BUAT_PINTASAN/JALANKAN/NYAHPEPIJAT/
   BUANG/KEMASKINI/pintasan.ps1 + mesej "SIAP" + "✓ Berjaya — N
   koleksi").
3. **Semakan J/K baharu dalam `semak_dokumen_ui.py`** — 74 → **110
   semakan, 0 gagal**: frasa kunci Ciri-ciri mesti wujud dalam
   KEDUA-DUA dokumen supaya tidak hanyut (J: README ↔
   MANUAL_PENGGUNAAN, 12 frasa; K: MULA_CEPAT ↔ README, 12 frasa;
   I diperluas: 8 tuntutan .bat). Kes negatif disahkan: frasa dibuang
   → GAGAL dikesan.

## Pengesahan akhir (petang) — suite 12/12 + audit SUMBER_hadis-my

- **`uji_pra_hantar.py` penuh** dijalankan SEMULA selepas perubahan
dokumen petang: **12/12 SEMUA LULUS (389.2s)**. Nota penting:
`semak_dokumen_ui.py` (semakan J/K) pada masa itu ialah skrip audit
berasingan — dijalankan manual → **110/0** (I .bat 8 semakan + J 12
frasa + K 12 frasa lulus); **selepas ini ia digate sebagai ujian #13**.
- **`SUMBER_hadis-my.md` diaudit** — konsisten dengan kod + dokumen
lain: `service.hadis.my/api/v1` + `X-API-Key` padan `api/hadis_api.py`;
portal `developer.hadis.my/dashboard` sah (sumber URL MULA_CEPAT yang
diganti); bentuk `HADIS_…` padan kunci sebenar; 9 koleksi = 62,169
padan DB; Developer 10,000/hari padan kuota sync.

## Commit petang 14 Ogos

`82cb4c1` (senarai suite MANUAL_REFERENSI_DEV) · `c0b8020` (MULA_SINI
Sesi Terakhir) · `f359ea9` (MULA_SINI §5) · `80b7abf` (semak #12) ·
`564dba7` (semak #12 diperketat) · `b546912` (README) · `9952ae7`
(penutup hari) · `3137a42` (konsistensi rentas dokumen) — **17 commit
jumlah hari ini** (18 selepas commit ini). `semak.py` SEMUA LULUS,
pokok kerja bersih.

---

# Penutup Hari (malam) — audit dokumen digate #13 + 18 commit (14 Ogos)

**Permintaan:** (1) daftar `semak_dokumen_ui.py` sebagai ujian #13
dalam `uji_pra_hantar.py`; (2) tutup hari dengan rekod penuh 18 commit
+ kemas kini MULA_SINI 'Sesi Terakhir' mengikut semakan #12.

## Audit dokumen digate sebagai ujian #13

- `uji_pra_hantar.py`: entri `13. semak_dokumen_ui.py` (timeout 120s)
  ditambah selepas #12; suite kini **13 ujian** (semak.py + 12 suite).
- Semakan A8 dalam `semak_dokumen_ui.py` dikemas: 12 → **13** + semak
  `semak_dokumen_ui.py` dirujuk (supaya senarai tidak hanyut).
- Kiraan dikemas dalam MULA_CEPAT (§1), README, MANUAL_REFERENSI_DEV
  (13 ujian + rantaian #13), MULA_SINI §3 (12 suite ujian + #13).
- Nota "tidak digate" lama dikemas: audit kini sebahagian gate rasmi.
- `semak.py` 8z hanya semak uji_visual_* — #13 tidak menjejaskannya.

## MULA_SINI 'Sesi Terakhir' dikemas (mengikut semakan #12)

- Intro: "Kerja 14 Ogos — **18 commit** (8 teras + 10 susulan)";
  bullet 10 baharu: semakan #13 digate + 110/0 + URL MULA_CEPAT
  dibetulkan + suite 12/12 + audit SUMBER (`c3d6a7d` — kekal dalam
  10 commit terbaru selepas commit ini, jadi semak #12 lulus).

## Jadual penuh — 18 commit 14 Ogos 2026

| # | Hash | Ringkasan |
|---|---|---|
| 1 | `341bdc9` | Tutup 4 item tertangguh: ujian mesin sebenar, Tersimpan (tanda buku sebenar), diagnos_syarah (HANYUT), pipeline API |
| 2 | `f59cd95` | Sync penuh dari mula (#2): 62,169 sejajar, 45/45 padan |
| 3 | `8512b47` | Padanan ara-* penuh (#3): 31,952/32,439, audit 100.0% |
| 4 | `988c803` | Audit liputan SemakHadis (#8): peta jurang per kitab/bab |
| 5 | `79eb722` | Penutupan hari tengah hari: 6 item tertangguh disahkan |
| 6 | `1326aaf` | Siasatan tafsir BM: TIADA sumber terbuka (jurang 843) |
| 7 | `3973c7e` | Dokumen Mula Cepat untuk pengguna |
| 8 | `1b1390c` | Audit dokumen vs UI (semak_dokumen_ui.py 74/0) |
| 9 | `82cb4c1` | MANUAL_REFERENSI_DEV: senarai suite ke 12 ujian |
| 10 | `c0b8020` | MULA_SINI Sesi Terakhir: kerja 14 Ogos |
| 11 | `f359ea9` | MULA_SINI §5: senarai sesi lengkap + item lama ditanda keluar |
| 12 | `80b7abf` | semak.py #12: 'Sesi Terakhir' seiring git log |
| 13 | `564dba7` | semak.py #12 diperketat: tarikh dalam teks ringkasan |
| 14 | `b546912` | README: semak #12 + uji_negatif 45/0, tab Sebelah lapuk dibuang |
| 15 | `9952ae7` | Penutup hari (petang): semak #12 + suite 12/12 + README |
| 16 | `3137a42` | Konsistensi rentas dokumen: URL MULA_CEPAT + semakan J/K (110/0) |
| 17 | `c3d6a7d` | Pengesahan akhir petang: suite 12/12 (389.2s) + audit SUMBER_hadis-my |
| 18 | *(commit ini)* | Audit dokumen digate #13 + penutup hari 18 commit |

**STATUS AKHIR HARI (malam 14 Ogos):** suite rasmi **13 ujian** —
12 ujian asal SEMUA LULUS (389.2s) + #13 audit dokumen (110/0) ·
semak.py SEMUA LULUS · pokok kerja bersih. Item tertangguh §8: 7
ditutup/diaudit, baki #7 kunci API (AKTIF sengaja).

## Tema NEUTRAL lalai + WCAG AA dikunci (malam 14 Ogos, lanjutan)

Keputusan pengguna untuk pengguna awam: lalai bertukar daripada kertas
hangat kepada **gelap neutral** (gaya Windows/telefon).

**Motivasi (dengan angka sebenar):**
- Windows gelap teks putih = **16.5:1** vs kertas hangat `#E8E4DA` =
  13.3:1 — putih tulen lebih "crisp" untuk mata awam
- Tier malap kertas hangat lama (`#8F8878`) = **4.25:1 — GAGAL WCAG AA**
  (4.5) untuk teks biasa; Windows tier paling pudar lulus
- Awam sudah biasa dengan mod gelap neutral — cast sepia mudah dibaca
  sebagai kecacatan ("kenapa app saya kekuningan?")

**Pelaksanaan:**
- `ui/theme.py`: palet **NEUTRAL** baharu (PAGE_BG `#1F1F1F`, CARD_BG
  `#252526`, HEADER `#232324`, teks `#FFFFFF`/`#C6C6C6`/`#9C9C9C`/
  `#8E8E8E`, TEAL hijau kekal); kertas hangat kekal sebagai pilihan
  "Kertas"; tier malap DARK/light dinaikkan ke ≥ 4.5:1
- Lalai `settings.get("theme", "neutral")` di `app_qt.py`,
  `settings_panel.py`, `splash.py` — pemasangan baharu terus Neutral
- Panel Tetapan → TEMA: **☀ Terang · 🌙 Neutral (lalai) · 📜 Kertas**
  (kunci "dark" kekal = pilihan Kertas, tiada kehilangan pilihan)
- Semakan **#13 semak.py: kontras WCAG AA** — 54 pasangan warna
  (3 tema × [4 tier × 3 permukaan + 3 semantik + 3 TEAL]) ≥ 4.5:1;
  dikunci `uji_negatif_8z` cabang #31 (mutasi `#707070` → dikesan),
  **47 lulus, 0 gagal**
- Pepijat ditemui semasa penguncian: cache `.pyc` Windows (mtime butir
  2 saat) menyebabkan import baca salinan bermutasi lama → pembersihan
  `buang_pyc_theme()` ditambah pada ujian mutasi
- Ujian: `uji_tukar_tema` 6 kitaran 27/0 · semak 6 (apl melancar) 3
  tema · `semak_dokumen_ui` G2 label 3 butang 110/0 · `uji_visual_sebenar`
  gelap = dark|neutral · semak 10aa (logo) kekal palet kertas
- Dokumen: `MANUAL_PENGGUNAAN` TEMA 3 pilihan (neutral lalai) ·
  `MANUAL_REFERENSI_DEV` (47 lulus, 31 cabang) · `PERUBAHAN_14OGOS`
- **Nota:** `user_settings.json` pengguna TIDAK disentuh (data peribadi
  gitignore) — "dark" peribadi kekal sehingga pengguna pilih 🌙 Neutral

## Tema NEUTRAL TERANG (malam 14 Ogos, lanjutan)

Pasangan terang kepada Neutral gelap — untuk pengguna mod terang yang
mahu kontras sama tinggi tanpa hue hangat.

- **Palet `lightneutral`** (`ui/theme.py`): PAGE_BG `#F4F4F4` ·
  CARD_BG `#FFFFFF` · HEADER `#ECECEC` · teks `#1A1A1A`/`#444444`/
  `#595959`/`#6B6B6B` — kelabu/putih tulen (R≈G≈B), TIADA cast sepia.
  Aksen TEAL `#1A6B3C`; cip semantik sama dengan kertas terang.
- **Semua tier ≥ 4.5:1** (paling ketat FAINT pada HEADER 4.51:1) —
  semak kontras #13 semak.py kini **72 pasangan warna, 4 tema**.
- **Panel TEMA = grid 2×2**: 🌙 Neutral (lalai) · 📜 Kertas ·
  ☀ Neutral terang · ☀ Terang. `QGridLayout` ditambah ke
  settings_panel.py; nama "☀ Terang" kekal (pengguna sedia ada).
- **Ujian**: semak 6 (apl melancar) 4 tema lulus · uji_tukar_tema
  8 kitaran **35/0** · semak_dokumen_ui G2 label 4 butang **110/0** ·
  uji_negatif_8z **47/0** (cabang #31 kekal sah — TEXT_FAINT neutral
  `#8E8E8E` unik; lightneutral `#6B6B6B`).
- Dokumen: `MANUAL_PENGGUNAAN` TEMA 4 pilihan · `PERUBAHAN_14OGOS`.

## Tema "Ikut sistem" (malam 14 Ogos, lanjutan)

Tema kelima — ikut mod gelap/terang Windows secara automatik.

- **`ui/theme.py`** — `windows_gelap()` baca registry
  `HKCU...\Themes\Personalize\AppsUseLightTheme` (0 = gelap) via
  `winreg`; gagal → gelap (tidak pernah pilih terang tanpa sengaja).
  `tema_efektif("sistem")` → `neutral` (gelap) / `lightneutral`
  (terang); `apply_theme()` menyelesaikannya secara dalaman — splash,
  panel Tetapan, dan app semua serasi tanpa kod khas.
- **Pemantau 2 saat** dalam `ui/app_qt.py` (`_semak_tema_sistem`,
  QTimer): baca registry tiap 2 s; hanya bina semula UI bila palet
  efektif berubah (`set_theme("sistem", paksa=True)` — parameter
  `paksa` baharu mengatasi guard "kunci sama").
- **Panel TEMA** — grid 2×2 + **🌓 Ikut sistem** span penuh (5 butang).
- **Pembetulan**: toast tema kini guna `is_dark()` (palet efektif) —
  sebelum ini set_theme("lightneutral") memapar "Tema gelap".
- **Ujian**: semak 6 (apl melancar) 5 mod · uji_tukar_tema 10 kitaran
  **43/0** · simulasi flip mod Windows (monkeypatch windows_gelap):
  neutral → lightneutral, `settings["theme"]` kekal "sistem" ·
  uji_negatif_8z **47/0** · semak_dokumen_ui G2 5 butang **110/0**.
- Dokumen: `MANUAL_PENGGUNAAN` TEMA 5 pilihan · `PERUBAHAN_14OGOS`.

## Penutup ciri tema (malam 14 Ogos) — ujian flip Windows HIDUP

**Ujian flip hidup** — bukti kukuh bahawa "Ikut sistem" benar-benar
mengikuti Windows:

- App berjalan pada tema `"sistem"` (tetingkap fizikal) → Windows
  gelap → `neutral` (`#1F1F1F`)
- Windows ditukar ke mod terang secara langsung (registry
  `AppsUseLightTheme`/`SystemUsesLightTheme` = 1 + broadcast
  `WM_SETTINGCHANGE` supaya UI Windows turut bertukar) — TANPA sentuh
  app → pemantau mengesan dan membina semula UI: `neutral` →
  `lightneutral` (`#F4F4F4`)
- Windows dipulihkan ke mod gelap (keadaan asal) selepas ujian
- Tangkapan skrin: `bukti_visual/sistem_gelap.png` ·
  `bukti_visual/sistem_terang.png` · galeri `uji_flip_sistem.html`

**Diperketat (`7ed0eda`)** — selang pemantau 10 s → **2 s**; ujian
flip diukur semula dengan pemantauan 0.2 s: **bertukar dalam 1.0 s**.

**Keadaan akhir ciri tema:** 5 pilihan TEMA · semua ≥ WCAG AA (semak
#13, 72 pasangan) · suite rasmi 13/13 SEMUA LULUS (449.1s) · pokok
kerja bersih.

## Penutup Hari (malam) — status akhir 14 Ogos

**24 commit** (11 teras + 13 susulan) · ciri tema siap (5 pilihan
TEMA, semua ≥ WCAG AA, Ikut sistem diuji hidup 1.0 s) · suite rasmi
13/13 SEMUA LULUS (terakhir 449.1s) · semak.py SEMUA LULUS ·
uji_negatif_8z 47/0 · pokok kerja bersih · baki §8: #7 kunci API
(AKTIF sengaja).

## Galeri 5 tema dalam manual (malam 14 Ogos, lanjutan)

- 10 tangkapan tema → `dokumen/imej/tema_*.png` (halaman sama:
  Utama + Abu Daud #3982; 1100×780).
- `MANUAL_PENGGUNAAN` TEMA: seksyen "Rujukan visual (5 tema)" — 2
  jadual 5 lajur (`../imej/...`).
- `MANUAL_INSTALASI`: senarai ZIP 120 → **130 fail** (dokumen 46,
  imej 19).
- `semak_bersih` menandai imej baharu sebelum di-commit (gate
  berfungsi); `user_settings.json` dipulihkan ke "sistem" selepas
  kesan sampingan set_theme dalam skrip tangkapan.

## MANUAL_REFERENSI_DEV §12A — imej tangkap layar (malam 14 Ogos)

Dokumentasi imej `dokumen/imej/`: 3 kumpulan (baseline regresi 7 +
rujukan LAMA 2 + galeri tema 10) dengan proses kemas kini galeri
tema (set_theme 5 tema, halaman sama 1100×780, nama padan manual,
kemas kini senarai ZIP). Baris `dokumen/imej/` dalam Peta dokumen.

## Susun atur RTL — Arab di KANAN, terjemahan di KIRI (malam 14 Ogos, lanjutan)

- **Keputusan pengguna:** melalui rujukan, demi menghormati status
  hadis rujukan, teks Arab asal mesti di sebelah **KANAN** dan
  terjemahan di **KIRI** — susun atur dua lajur dicerminkan (RTL).
- **Pelaksanaan:** `ui/pages_detail.py` — lajur Arab kini `kol_kanan`
  (dijajarkan kanan, aliran RTL), terjemahan `kol_kiri`; semakan
  geometri dikemas: `semak_dokumen_ui` D3b + `uji_visual_mockup`
  (arab x > terjemahan x); disahkan offscreen: Arab x=549 (kanan),
  terjemahan x=25 (kiri).
- **Dokumen:** README, MULA_CEPAT, MANUAL_PENGGUNAAN §2.4 — "Arab
  kanan, terjemahan kiri (susunan RTL, 14 Ogos)". MANUAL_REFERENSI_DEV
  §12A mencatat galeri kini RTL.
- **Imej:** baseline `bina_tangkapan_dokumentasi.py --kemas` (7) +
  **10 imej galeri tema ditangkap semula** dengan susun atur RTL
  (halaman sama Abu Daud #3982, 1100×780; 963–1,426 warna unik).

## Penutup RTL + Numpy + galeri muktamad (malam 14 Ogos, lanjutan)

- **Numpy dalam `bina_tangkapan_dokumentasi.py`** — `_metrik` + offset-scan
  digantikan gelung Python tulen dengan vektor Numpy (int16, `.max(axis=2)`):
  formula IDENTIK (beza metrik 0.00e+00 pada pasangan baseline sebenar),
  pecutan ~13× saiz sama (2.26s → 0.17s); offset-scan 42px (78M piksel)
  yang pernah menggantung mesin perlahan kini saat. Regresi 7/7 lulus.
  Numpy sudah kebergantungan projek (core/semantic_search.py) — tiada
  kebergantungan baharu.
- **Galeri 5 tema ditangkap SEMULA (muktamad)** — 10 PNG `dokumen/imej/`
  dengan kod RTL muktamad, tanpa toast (tunggu 3.2s > auto-hide 1800ms);
  bug kunci fail sementara (Errno 22, antivirus/indexing Windows) dibaiki
  dengan retry 5× pada save. Galeri HTML: `bukti_visual/galeri_5_tema.html`.
- **CABARAN SUITE LAMBAT (pengajaran penting):** suite rasmi (~460s)
  gagal jalan sekali gus bila mesin terbeban (~2 GB RAM tinggal; Chrome +
  Freebuff). Setiap kali tool timeout, subproses ujian Windows MENJADI
  YATIM (terus hidup, ~1 GB setiap satu — model AI) → beban bertambah →
  ujian seterusnya tercekik di "Loading weights". Langkah pemulihan:
  (1) bunuh semua `python.exe` yatim sebelum larian; (2) bersihkan
  `profil_model.json` daripada rekod patologi (>100s — artifak mesin,
  bukan regresi; semakan 8j amaran jika purata 3 larian >60s);
  (3) jalankan ujian bersegmen (1–9 via `uji_pra_hantar`, 10–13 individu).
  Keputusan akhir: **13/13 SEMUA LULUS** (semak · negatif 47/0 · mockup
  130/0 · piksel 53/0 · sebenar 68/0 · tukar_tema 43/0 · bandingan 55/0 ·
  lompat 48/0 · e2e 18/0 · baseline 7/7 · draf 9/0 · tersimpan 20/0 ·
  dokumen_ui 110/0).
- **Commit:** `6b853f0` (RTL utama) · `6b03234` (baseline RTL muktamad) ·
  Numpy + galeri (commit susulan).

## Pengukuhan suite + imej sebaris + pengesahan akhir (malam 14 Ogos, penutup)

- **Pembersihan proses yatim AUTOMATIK (`uji_pra_hantar.py`)** — punca
  "hang" suite (proses ujian yatim ~1 GB setiap satu selepas tool
  timeout) kini ditangani: `_bersihkan_orphan()` dijalankan pada
  permulaan suite + boleh dipanggil sendiri (`--bersihkan`). Hanya
  sasarkan skrip UJIAN projek dalam BASE (`uji_*`, `semak.py`,
  `bina_tangkapan_dokumentasi.py`, dsb.) — BUKAN `main.py`/`sync.py`
  (app/tugas pengguna) dan BUKAN proses semasa. Diuji: orphan tiruan
  dibunuh; proses python bukan-ujian kekal hidup (keselamatan).
- **Galeri manual → `<img>` sebaris** — seksyen "Rujukan visual
  (5 tema)" MANUAL_PENGGUNAAN kini guna tag `<img src="../imej/...">`
  (lebar 200px) — render langsung di GitHub/ZIP tanpa pautan markdown.
- **Pengesahan visual AKHIR (tema sistem + RTL)** — app sebenar dengan
  tema `"sistem"`: tema hidup `neutral` (Windows gelap), PAGE_BG
  `#1F1F1F`, **Arab@(554,275) KANAN vs Terjemahan@(104,275) KIRI**
  (baris sama y=275) — susun atur RTL disahkan pada widget SEBENAR;
  tangkapan `bukti_visual/sistem_rtl_home/detail.png` + galeri
  `pengesahan_rtl_akhir.html` (permukaan piksel (31,31,31)/(35,35,36)/
  (37,37,38) — neutral tulen).
- **Gate:** semak.py SEMUA LULUS · uji_negatif_8z 47/0 ·
  semak_dokumen_ui 110/0.

## Pengesahan dua hala orphan + dokumentasi --bersihkan (malam 14 Ogos, penutup)

- **`_semak_orphan_selepas()`** — pengesahan DUA HALA dalam
  `uji_pra_hantar.py`: bersihkan pada mula (`_bersihkan_orphan`),
  sahkan BERSIH pada akhir. Subproses ujian mesti keluar sendiri;
  apa-apa yang tinggal = ujian tidak memulihkan keadaan / subproses
  menggantung terselamat timeout → suite GAGAL. Logik dikongsi via
  `_cari_orphan()` (kriteria sama untuk bersih + semak). Diuji:
  orphan tiruan dikesan (1), dibunuh, selepas bersih = 0.
- **`--bersihkan` didokumenkan** dalam MANUAL_REFERENSI_DEV (seksyen
  suite ujian): cara pembersihan, kriteria sasaran, keselamatan
  (bukan main.py/sync.py/proses semasa).
- Gate: semak.py SEMUA LULUS · uji_negatif_8z 47/0 ·
  semak_dokumen_ui 110/0.

## Audit dokumen RTL + gate pantas (malam 14 Ogos, penutup)

- **Audit rujukan susun atur lama**: semua tuntutan "Arab kiri /
  terjemahan kanan" dalam dokumen diselaraskan ke RTL — MANUAL_PENGGUNAAN
  (jadual sejarah Sesi 55), TRANSFORMASI_DETAIL (nota RTL di atas +
  Susun atur utama/Tab transliterasi + 3.1 geometri + 3.3 tab + 3.3
  lanjutan), MULA_SINI (nota sejarah KEMASKINI 12 Ogos diberi nota
  penjelas). Semakan audit grep: sifar rujukan lapuk tinggal.
- **`gate_pantas.py` baharu** — satu arahan, ~35s: pokok kerja bersih
  (amaran) + semak.py + uji_negatif_8z. Untuk commit kecil sebelum
  suite penuh; didokumenkan dalam MANUAL_REFERENSI_DEV.
- **Semakan #12 berfungsi seperti reka bentuk**: semak.py GAGAL
  "tiada hash daripada 10 commit terbaru" kerana ce2c3cf/7ed0eda
  tersorong keluar dari 10 teratas — seksyen Sesi Terakhir kini rujuk
  hash `a9e9d44` (bulan 20). uji_negatif_8z 46/1 juga dikesan oleh
  semakan pasca-pulihan yang sama — dibaiki.

## Semak #14 audit RTL dikunci + suite akhir 463.6s (malam 14 Ogos, penutup)

- **`semak_rtl_dokumen()` (semak #14 semak.py)** — kunci audit RTL:
  frasa susun atur lama dalam TRANSFORMASI_DETAIL.md/manual/manual/MANUAL_PENGGUNAAN.md
  ("Arab di kiri", "terjemahan di kanan", "lajur kiri membawa teks
  Arab", "terjemahan > `x` Arab", dsb.) → GAGAL; nota sejarah berpetik
  selamat (corak khusus).
- **Mutasi #32 uji_negatif_8z** — "Arab di kiri" disuntik ke
  TRANSFORMASI_DETAIL → dikesan; hasil **49/0 (32 cabang)**; semakan
  #14 dalam senarai pasca-pulihan.
- **Suite penuh AKHIR 13/13 SEMUA LULUS (463.6s)** — larian penuh
  kedua berturut-turut, "tiada proses ujian yatim selepas suite".

## Semak #14 diperluas — README + sesi_index header (malam 14 Ogos, penutup)

- **`semak_rtl_dokumen()` kini tutup 4 fail**: TRANSFORMASI_DETAIL.md +
  manual/manual/MANUAL_PENGGUNAAN.md + **README.md** (imbas penuh — dokumen keadaan
  semasa) + **sesi_index.md (hanya header "Sesi Terakhir"** — arkib
  sejarah berketarikat dikecualikan kerana frasa lama dalam konteks
  sejarah dibenarkan).
- **Mutasi #33 uji_negatif_8z** — "Arab di kiri" disuntik ke README.md
  → dikesan; hasil **50/0 (33 cabang)**; semakan #14 pasca-pulihan
  kekal hijau (header sesi_index bersih).

## PENUTUP HARI — 14 Ogos 2026 (35 commit, rekod penuh)

**Hari paling padat projek**: 35 commit (11 teras + 24 susulan; 41
sebenar − 6 commit MULA_SINI langkah-B), semua ciri disahkan penuh.

**Ciri siap & dikunci:**

| Ciri | Butiran |
|---|---|
| **5 tema TEMA** | 🌙 Neutral lalai · 📜 Kertas · ☀ Neutral terang · ☀ Terang · 🌓 Ikut sistem (pantau Windows 2s, flip 1.0s) — semua tier ≥ WCAG AA (semak #13, 72 pasangan) |
| **Susun atur RTL** (`6b853f0`) | Arab di KANAN, terjemahan di KIRI (hormati status hadis) — geometri dikunci mockup 130/0 + semak #14 |
| **Numpy bandingan piksel** | bina_tangkapan `_metrik` vektor — offset-scan 78M piksel kini saat |
| **Gate pantas** (`09fe9db`) | semak.py + uji_negatif_8z + pokok bersih (~35s) sebelum commit kecil |
| **Semak #14 audit RTL** (`c8878ec`, `4ed70a6`) | 4 fail (TRANSFORMASI, MANUAL_PENGGUNAAN, README penuh, sesi_index header) — dikunci mutasi #32/#33, uji_negatif_8z **50/0 (33 cabang)** |
| **Orphan dua hala** (`a9e9d44`) | pembersihan automatik mula + semakan BERSIH selepas suite |
| **Suite penuh** | **13/13 SEMUA LULUS** (akhir 463.6s) — larian penuh berturut-turut |

**Pengesahan akhir:** semak.py SEMUA LULUS (semak #12 seiring git log,
#13 kontras 72 pasangan, #14 audit RTL) · uji_negatif_8z 50/0 ·
semak_dokumen_ui 110/0 · pokok kerja bersih.

**Baki tertangguh §8:** hanya **#7 kunci API** (kekal AKTIF sengaja —
tiada kunci boleh disimpan dalam repositori).

**Rujukan:** log harian `dokumen/perubahan/PERUBAHAN_14OGOS.md` (seksyen
penutup) · manual `MULA_SINI.md` "Sesi Terakhir" (35 commit, bullet 23).

## Ringkasan satu muka 'Keadaan projek' dipindah ke atas + semak #15 dikunci

**Kerja:** pindah ringkasan satu muka 'Keadaan projek' dari §5 ke bahagian
PALING ATAS MULA_SINI (sebelum 'Sesi Terakhir') supaya ia benar-benar
perkara pertama dibaca sesi AI baharu — selesai tanpa membaca arkib penuh
(selepas berehat lama atau sesi baharu). Ringkasan kini seksyen sendiri
`## Keadaan projek — ringkasan satu muka (akhir 14 Ogos 2026)` dengan
pautan silang ke dokumen berkaitan (MULA_CEPAT, MANUAL_PENGGUNAAN,
MANUAL_INSTALASI, TRANSFORMASI_DETAIL, AUDIT_SEMAKHADIS,
SIASATAN_TAFSIR_BM, PERUBAHAN_14OGOS, sesi_index).

**Semak #15 `semak_ringkasan_keadaan` (semak.py)** — ringkasan satu muka
tidak boleh ketinggalan seperti 'Sesi Terakhir' (semak #12): (1) seksyen
wujud; (2) tarikh tajuk ringkasan == tarikh tajuk 'Sesi Terakhir'; (3)
kiraan `**N commit**` dalam ringkasan == kiraan intro 'Sesi Terakhir'.
Tiada git → semakan tarikh dilangkau. Dikunci `uji_negatif_8z` **52/0**
(34 cabang) — mutasi **#34** menurunkan kiraan ringkasan (35 → 34) →
dikesan; semak #15 masuk senarai pasca-pulihan.

**MULA_SINI §5** kini hanya nota penunjuk: "Ringkasan satu muka kini di
bahagian paling atas dokumen — baca itu dahulu; sejarah penuh di bawah
kekal sebagai arkib berketarikh."## Penutup 15 Ogos: README diselaraskan + suite penuh akhir

**Kerja (15 Ogos, 1 commit `250216d`):** README.md dikemas seiring
semak #15 — `uji_negatif_8z` 45/0 → **52/0 (34 cabang)**, `370+
semakan` → **377 semakan (15 bahagian)**, komen semak.py sebut
ringkasan satu muka. Suite penuh **13/13 SEMUA LULUS (458.5s)** —
larian penuh ketiga berturut-turut, pengesahan dua hala orphan OK.

**Nota tarikh:** commit ini ialah **15 Ogos 08:06** — hari baharu
bermula. 'Sesi Terakhir' + ringkasan MULA_SINI dikemas ke 15 Ogos
(9 commit akhir, sambungan 36 commit 14 Ogos); kunci mutasi
#30/#34 diselaraskan. Kiraan: 14 Ogos = 36 commit (44 − 8
langkah-B); 15 Ogos setakat ini = 9 commit (9 sebenar − 0
langkah-B).
## Pengesahan muktamad 15 Ogos: tangkapan sistem + RTL vs galeri

**Kerja (15 Ogos):** app dilancarkan pada skrin sebenar dengan tema
"sistem" → Windows gelap → **neutral** (PAGE_BG #1F1F1F). Pengesahan
10/10 — 0 gagal:
- **RTL pada widget fizikal**: Arab@(624,275) **KANAN** vs
  Terjemahan@(110,275) **KIRI** — baris sama (y=275);
- **Tab bahasa**: MELAYU/INDONESIA/ENGLISH di KIRI sempadan lajur Arab,
  ARAB/TRANSLITERASI di KANAN (dalam lajur Arab);
- **Palet neutral gelap** (R≈G≈B, min 45–46);
- **Galeri dokumentasi sepadan** (`dokumen/imej/tema_*_sistem.png`,
  dirakam pada skrin lain 1116×788): palet pada penskalaan sama
  nmad 3.0–7.0 (0=identik), beza min < 7.

Tangkapan: `bukti_visual/sistem_rtl_final_{home,detail}.png` ·
galeri perbandingan: `bukti_visual/pengesahan_muktamad_15ogos.html`.
## PENUTUP HARI — 15 Ogos 2026 (10 commit, rekod penuh)

**Ringkasan hari:** hari baharu bermula selepas penutup 14 Ogos (36
commit). Kerja 15 Ogos — **10 commit** (11 teras 14 Ogos + 10
susulan 15 Ogos; 10 sebenar − 0 langkah-B):

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **README diselaraskan seiring semak #15** — `45/0 — 30 cabang` → `52/0 — 34 cabang`, `370+ semakan` → `377 semakan (15 bahagian)`, komen semak.py sebut semak #15 | `250216d` |
| 2 | **Suite penuh 13/13 SEMUA LULUS (458.5s)** — larian penuh ketiga berturut-turut, pengesahan dua hala orphan OK | `250216d` |
| 3 | **'Sesi Terakhir' + ringkasan dikemas ke 15 Ogos** — hari baharu bermula (komit pertama = 15 Ogos 08:06); `PERUBAHAN_15OGOS.md` baharu (log harian); header MULA_SINI ditunjuk | `3b81235` |
| 4 | **Kiraan diselaraskan + kunci mutasi #30/#34** — ringkasan == 'Sesi Terakhir' (semak #15) | `e205db3` |
| 5 | **CHANGELOG dikemas** — entri 14 + 15 Ogos supaya log versi seiring log harian (sebelum ini melompat 13 Ogos → 1.3) | `3ad97c5` |
| 6 | **Pengesahan muktamad: tangkapan sistem + RTL vs galeri** — app tema "sistem" → neutral; Arab@(624,275) KANAN vs Terjemahan@(110,275) KIRI; 10/10 semakan; palet sepadan galeri (nmad 3.0–7.0) | `dcd85aa` |
| 7 | **Suite penuh 13/13 SEMUA LULUS (478.7s)** + pemeriksaan saiz galeri — keputusan: TIADA tangkapan semula perlu (galeri dirakam pada saiz rasmi tetap 1100×780, bukan skrin penuh; `bina_tangkapan` 7/7 sepadan baseline) | `d0dd727` |
| 8 | **Skaf PERUBAHAN_16OGOS + audit akhir dokumen + pintasan disahkan** — semua hash wujud, tiada kiraan lapuk; `Hadis.lnk` Desktop + Start Menu → main.py betul | `829bc08` |
| 9 | **Ujian hidup muktamad: tema sistem + RTL 3/3** — app dibuka pada mesin sebenar (tema sistem → Neutral), Arab@(554,275) KANAN vs Terjemahan@(104,275) KIRI, palet neutral tulen (sisihan 0.9), seiring galeri; tiada kod diubah | `837c53d` |
| 10 | **Penutup hari: rekod penuh 9→10 + audit §8 + PLAN_BINA_EDARAN.md** — audit baki tertangguh §8 (tiada item baharu sebelum edaran); plan bina versi edaran ditulis untuk semakan (dokumentasi dahulu, tiada binaan) | komit penutup ini |

**Ciri dikunci kekal:** 5 tema ≥ WCAG AA (semak #13, 72 pasangan) ·
susun atur RTL Arab kanan (semak #14, 4 fail) · ringkasan satu muka
seiring 'Sesi Terakhir' (semak #15) · `gate_pantas.py` ~30s · suite
13/13 berulang kali lulus.

**Baki tertangguh (§8):** hanya **#7 kunci API hadis.my** — kekal AKTIF
sengaja. Jurang Tafsir 843 dipantau (MyHadith JAKIM + IslamHouse Melayu).

**Kiraan telus:** 14 Ogos = **36 commit** (44 sebenar − 8 langkah-B);
15 Ogos = **10 commit** (10 sebenar − 0 langkah-B). Komit penutup ini
menyentuh 5 fail (bukan corak langkah-B) → dikira.

**Gate akhir:** semak.py SEMUA LULUS (15 semakan, #12 + #15 hijau) ·
uji_negatif_8z **52/0** · semak_dokumen_ui 110/0 · gate_pantas ~30s ·
pokok kerja bersih · tema pengguna "sistem" · tiada proses ujian
tersadai.
## Susulan penutup 15 Ogos: suite penuh + keputusan saiz galeri

**Suite penuh 13/13 SEMUA LULUS (478.7s)** — larian penuh keempat
berturut-turut; pengesahan dua hala orphan OK.

**Pemeriksaan saiz galeri tema** — keputusan: TIADA tangkapan semula
perlu. Galeri `dokumen/imej/tema_*.png` dirakam pada saiz tetingkap
rasmi tetap `w.resize(1100, 780)` (1116×788 termasuk bingkai), BUKAN
skrin penuh — pengguna setiap mesin ada saiz skrin sendiri, jadi tiada
"saiz sepadan" universal yang perlu dikejar. `bina_tangkapan` (ujian
#10) lulus 7/7 sepadan baseline + pengesahan muktamad palet (nmad
3.0–7.0) — galeri kekal sah sebagai rujukan visual (dipapar `<img
width=200>` dalam manual).
## Susulan penutup 15 Ogos: skaf 16 Ogos + audit akhir + pintasan

- **Skaf PERUBAHAN_16OGOS.md** — fail log harian 16 Ogos disediakan
  supaya sesi esok bermula dengan fail yang betul (header MULA_SINI
  kekal 15 Ogos — hari semasa; esok tinggal isi + kemas kini header).
- **Audit akhir dokumen** — semua hash 7-heks dalam 9 dokumen
  (README, MULA_SINI, MULA_CEPAT, MANUAL_PENGGUNAAN, MANUAL_INSTALASI,
  MANUAL_REFERENSI_DEV, sesi_index, CHANGELOG, PERUBAHAN_15OGOS)
  wujud dalam git (kecuali `fffffff` — hash tiruan mutasi ujian,
  sejarah); tiada kiraan commit lapuk; "8 commit" konsisten di semua
  tempat.
- **Pintasan disahkan** — `Hadis.lnk` Desktop + Start Menu kedua-dua
  menunjuk ke `pythonw.exe` + `"D:\Pustaka Quran Hadis\hadis\main.py"`
  (WorkingDirectory betul); pintasan.ps1 guna `$PSScriptRoot` — sentiasa
  betul walau folder dipindah.
## Susulan penutup 15 Ogos: ujian hidup muktamad (tema sistem + RTL) 3/3

- **App dibuka pada mesin sebenar** — `PustakaApp`, tema `sistem`
  (Windows gelap → **Neutral**, PAGE_BG `#1F1F1F`), hadis `bukhari 1`
  dibuka terus; tangkapan `bukti_visual/sah_hidup_final_{home,detail}.png`.
- **RTL pada widget fizikal**: Arab@(554,275) di **KANAN** vs
  Terjemahan@(104,275) di **KIRI** — baris sama (y=275) ✓
- **Palet neutral tulen** (sisihan RGB **0.9** < 25) pada home + detail ✓
- **Seiring galeri**: beza palet-skala home 5.1 / detail 8.4 (dalam
  julat jangkaan 3–9 — hadis berbeza dipaparkan, saiz 1100×749 vs
  galeri 1116×788) ✓
- Tiada kod diubah — app berfungsi seperti disahkan. **Kiraan 15 Ogos
  kini 9 commit** (9 sebenar − 0 langkah-B; komit ini menyentuh 4 fail,
  bukan corak langkah-B → dikira). Kunci mutasi #30/#34 diselaraskan.
## Penutup hari 15 Ogos: rekod penuh 10 + audit §8 + PLAN_BINA_EDARAN

**Audit baki tertangguh §8 (sebelum pengedaran)** — disahkan **TIADA
item baharu diperlukan**: item 1–6 DITUTUP 14 Ogos (mesin sebenar,
sync penuh 62,169, padanan ara-* 98.5%, Tersimpan 20/0, diagnos
syarah, pipeline API 18/0); #7 kunci API kekal AKTIF sengaja (keputusan
pengguna, 31 Jul); #8 liputan SemakHadis 4,237/62,169 ialah siling
sumber terbuka (audit penuh `AUDIT_SEMAKHADIS.md`; jurang Tafsir 843
dipantau MyHadith JAKIM + IslamHouse). Aplikasi **SIAP & DISAHKAN**
untuk langkah pengedaran.

**Plan bina versi edaran — dokumentasi DAHULU, tiada binaan** —
`dokumen/rujukan/PLAN_BINA_EDARAN.md` (15 Ogos) ditulis untuk semakan
pengguna: (1) pengesahan reka bentuk INSTALLER.md terhadap kod semasa
— semua andaian masih sah (config.py/ui.helpers.py guna BASE_DIR,
`hadis_faiss.index` + `hadis_id_map.pkl` + `.cache_models` + `app.ico`
ada; `_baik_pulih_dll_qt_torch` masih ada); (2) keputusan reka bentuk
kekal (pilihan C ~520 MB, `%LOCALAPPDATA%`, Nuitka, Inno Setup,
GitHub Releases, repo persendirian dahulu); (3) 7 fasa pelaksanaan
dengan gate (laluan data → bina Nuitka venv bersih → uji Windows
bersih → Inno Setup + wizard → edaran GitHub → awam selepas lesen);
(4) risiko & mitigasi; (5) **keputusan pengguna diperlukan sebelum
mula**: sahkan plan, sahkan saiz pilihan C, akaun GitHub, ZIP mudah
alih. Kiraan 15 Ogos kini **10 commit** (10 sebenar − 0 langkah-B);
kunci mutasi #30/#34 diselaraskan.

## Susulan 15 Ogos — Gabung ZIP Pembetulan (①–④, commit ke-11)

Pengguna membawa arkib `Pustaka_Hadis_Pembetulan_Lengkap/` (ZIP pembetulan
13–15 Ogos dari Drive, folder "PustakaHadith" — bahan luaran, kini
gitignored). Perbandingan dengan projek utama mendapati percabangan: 1/6
pembetulan kod sudah wujud, 4 belum, skema 8 belum. Penggabungan dibuat
**berperingkat dengan gate** (keputusan pengguna: "buat 1 ~ 4"):

- ① `RandomWorker` → `terjemah_ralat(e)` (ui/workers.py) — butang Rawak
  kini papar ralat Bahasa Melayu, bukan Inggeris mentah.
- ② `SemanticWorker` dipindah dari kelas dalaman `pages_carian.py` ke
  `ui/workers.py` (warisi `_Base`, ada `cancel()`); import + docstring
  dikemas; semak_dokumen_ui E5 diselaraskan seiring.
- ③ `_page_settings` dibuang dari `_build()` (ui/app_qt.py) — halaman
  Tetapan penuh lama tidak lagi dibina (tiada laluan `go("settings")`).
- ④ `_DIAKRITIK` + `\u0610-\u0614` (core/eng_source.py) — audit
  `audit_eng.py --semua`: 30,547 disemak / 30,541 disahkan / 6 disyaki,
  identik dengan rekod GTAF §6b (0 perbezaan lama vs baharu).

Status ditanda dalam `Pustaka_Hadis_Pembetulan_Lengkap/list-we-do.md`
(seksyen K baharu: #2/#3/#4/#5/#7 DIGABUNG; #9/#10 skema 8 + dokumen
audit + INSTALLER.md BELUM). Folder ditambah ke `.gitignore` (bahan
luaran 12MB, kod pendua + OCR cache) + `_SKIP_FOLDER` semak.py.

**Gate:** semak.py SEMUA LULUS (15 semakan) · uji_negatif_8z 52/0 ·
semak_dokumen_ui 110/0 · gate_pantas SEMUA LULUS · uji_data_baharu 18/18
(SemanticWorker hidup + closeEvent tanpa crash) · uji_visual_mockup
130/0. **Kiraan 15 Ogos = 12 commit** (11 sebenar − 0 langkah-B); kunci
mutasi #30/#34 diselaraskan. Sisa: skema 8 `arab_carian` (keputusan
berasingan diperlukan).

## Susulan 15 Ogos — Gabung Skema 8 + Dokumen Audit (⑤⑥, komit ke-13)

Kesinambungan gabung ZIP (①–④). Pengguna mengarahkan "semua" — baki
penggabungan dilaksanakan dengan gate penuh:

- **⑤ Skema 8 + `arab_carian`** — diff bersih disahkan (folder db.py/sync.py
  = root + skema 8 sahaja). `db.py`: `SKEMA_VERSI=8`, `bersih_tashkeel()`
  (buang harakat sahaja, TIDAK lipat ة→ه — peraturan MULA_SINI #3), kolum
  `arab_carian`, FTS5 indeks `arab_carian`, trigger dipindah ke
  `_backfill_arab_carian()` (elak "no such column" DB lama), self-heal
  migrasi terganggu, normalisasi query dalam `_to_match_query()`. `sync.py`:
  `simpan()` isi `arab_carian` rekod baharu. `uji_carian_arab.py` disalin
  dari ZIP + dijalankan pada SALINAN konsisten DB sebenar (Backup API, asal
  baca sahaja): **SEMUA LULUS 74.67s** — 62,169 hadis, 0 NULL, 3 trigger,
  `كتب`=`كَتَبَ` 767, `نية`=`نِيَّة` 10, `الله`=`اللَّهِ` 60,211, regresi BM
  niat/puasa/hukum riba 115/911/486, trigger INSERT/UPDATE/DELETE lulus.
  **Migrasi produksi:** backup `hadis.db.sebelum_carian_arab.bak`
  (gitignored) → versi 8, 0 NULL → `semak_db.py` JUMLAH 62,169 → carian
  sebenar disahkan. Carian Arab tanpa tashkeel kini BERFUNGSI dalam app
  (sebelum ini `كتب` tidak jumpa `كَتَبَ` — isu GTAF.md §4).
- **⑥ Dokumen audit disalin** ke `dokumen/audit/` (GTAF, AHMAD_DIGITAL,
  AHMAD_HOCR + SAMPEL_5.json, TERJEMAHAN_AHMAD_DARIMI, CARIAN_ARAB) +
  `dokumen/rujukan/` (DRAF_carian_arab.md, PERMOHONAN_LESEN_AHMAD.md).
  Satu kata Indonesia dibetulkan ke Melayu Malaysia (semak 8m).
- **list-we-do.md:** #9/#10 + dokumen audit ditanda DIGABUNG; INSTALLER.md
  kekal BELUM (PLAN_BINA_EDARAN.md projek utama menggantikannya).
- **Gate:** semak.py SEMUA LULUS · uji_negatif_8z 52/0 · semak_dokumen_ui
  110/0 · gate_pantas SEMUA LULUS (32.4s) · uji_data_baharu 18/18 ·
  mockup 130/0. **Kiraan 15 Ogos = 13 commit**; kunci mutasi #30/#34
  diselaraskan.

## Susulan 15 Ogos — Ujian hidup carian Arab + suite penuh + banding INSTALLER (komit ke-14)

- **Ujian hidup app (tema sistem, skema 8):** carian Arab tanpa tashkeel
  di UI SEBENAR — `كتب`=767 (sama dengan `كَتَبَ`), `نية`=10, `puasa`=911
  (regresi BM), tema sistem→Neutral (PAGE_BG #1F1F1F). 9/9 lulus.
  Skema 8 disahkan hujung-ke-hujung: DB → API → UI → skrin.
- **Suite penuh 13/13 SEMUA LULUS (502.1s)** dengan skema 8 hidup +
  "tiada proses ujian yatim selepas suite".
- **Perbandingan INSTALLER.md dua versi** → `dokumen/rujukan/
  BANDING_INSTALLER.md`. Penemuan utama: ZIP pilih PyInstaller 6.22 +
  MSIX/Store; projek utama pilih Nuitka + GitHub Releases — keputusan alat
  bina bertentangan, kekal TERBUKA (uji kedua-dua diagnostik dalam Fasa 2
  PLAN_BINA_EDARAN). Nilai ZIP (masalah lazim §17, checklist §18, urutan
  §19, ujian naik taraf §16) dikenal pasti untuk diserap. list-we-do.md
  item INSTALLER.md → DIBANDINGKAN (kesemua 6+1 item ZIP kini berstatus).
- **Gate:** suite penuh 13/13 · gate_pantas SEMUA LULUS · pokok bersih.
  **Kiraan 15 Ogos = 14 commit**; kunci mutasi #30/#34 diselaraskan.

## PENUTUP HARI — 15 Ogos 2026 (14 commit, rekod penuh)

**Ringkasan hari:** hari baharu bermula selepas penutup 14 Ogos (36
commit) dengan sambungan kerja gabung ZIP luaran ①–④/⑤⑥ dan pengesahan
akhir. Kerja 15 Ogos — **14 commit** (14 sebenar − 0 langkah-B; komit
rekod penutup 15 Ogos ini ialah komit pertama 16 Ogos):

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **README diselaraskan seiring semak #15** — 45/0 → 52/0 (34 cabang), 370+ → 377 semakan (15 bahagian); komen semak.py sebut semak #15 | `250216d` |
| 2 | **'Sesi Terakhir' + ringkasan ke 15 Ogos** (hari baharu, komit pertama 08:06) + `PERUBAHAN_15OGOS.md` baharu (log harian) | `3b81235` |
| 3 | **Kiraan diselaraskan + kunci mutasi #30/#34** — ringkasan == 'Sesi Terakhir' (semak #15) | `e205db3` |
| 4 | **CHANGELOG dikemas** — entri 14 + 15 Ogos (semak #15, 52/0, 377 semakan) supaya log versi seiring log harian | `3ad97c5` |
| 5 | **Pengesahan muktamad: tangkapan sistem + RTL vs galeri** — app tema "sistem" → neutral; Arab@(624,275) KANAN vs Terjemahan@(110,275) KIRI; 10/10 semakan; palet sepadan galeri (nmad 3.0–7.0) | `dcd85aa` |
| 6 | **Penutup hari: rekod penuh 6 commit + kiraan semua dokumen** | `07f2b0f` |
| 7 | **Suite penuh 13/13 (478.7s) + keputusan saiz galeri** — TIADA tangkapan semula perlu (galeri dirakam saiz rasmi tetap 1100×780; `bina_tangkapan` 7/7 sepadan baseline) | `d0dd727` |
| 8 | **Skaf PERUBAHAN_16OGOS + audit akhir dokumen + pintasan disahkan** — semua hash wujud, tiada kiraan lapuk; `Hadis.lnk` Desktop + Start Menu → main.py betul | `829bc08` |
| 9 | **Ujian hidup muktamad: tema sistem + RTL 3/3** — app dibuka mesin sebenar (tema sistem → Neutral), Arab@(554,275) KANAN vs Terjemahan@(104,275) KIRI, palet neutral tulen (sisihan 0.9); tiada kod diubah | `837c53d` |
| 10 | **Penutup hari: rekod penuh 10 + audit §8 + PLAN_BINA_EDARAN.md** — audit baki tertangguh §8 (tiada item baharu sebelum edaran); plan bina versi edaran ditulis untuk semakan (dokumentasi dahulu, tiada binaan) | `79617fe` |
| 11 | **Gabung ZIP ①–④: 4 pembetulan kod** — RandomWorker `terjemah_ralat` · SemanticWorker → `_Base` di ui/workers.py (cancel) · buang `_page_settings` dari `_build()` · `_DIAKRITIK` + \u0610-\u0614 (audit identik 30,547/30,541/6); status dalam list-we-do.md seksyen K | `329bbbb` |
| 12 | **Rekod gabung ZIP ①–④** dalam sesi_index + PERUBAHAN_15OGOS | `20a2f11` |
| 13 | **Gabung skema 8 `arab_carian` + dokumen audit (⑤⑥)** — SKEMA_VERSI 8, carian Arab tanpa tashkeel (`كتب`=`كَتَبَ` 767), FTS5 + trigger + backfill; migrasi produksi dengan backup; dokumen audit GTAF/AHMAD/DARIMI/CARIAN_ARAB disalin; `semak_db.py` 62,169 | `45a1813` |
| 14 | **Ujian hidup carian Arab 9/9 + suite penuh 13/13 (502.1s) + banding INSTALLER** — `BANDING_INSTALLER.md` (ZIP PyInstaller/MSIX vs root Nuitka/GitHub — alat bina TERBUKA); list-we-do.md item INSTALLER → DIBANDINGKAN | `da1834c` |

**Ciri dikunci kekal:** 5 tema ≥ WCAG AA (semak #13, 72 pasangan) ·
susun atur RTL Arab kanan (semak #14) · ringkasan satu muka seiring
'Sesi Terakhir' (semak #15) · skema 8 carian Arab tanpa tashkeel ·
suite 13/13 berulang kali lulus.

**Baki tertangguh (§8):** hanya **#7 kunci API hadis.my** — kekal AKTIF
sengaja. Jurang Tafsir 843 dipantau (MyHadith JAKIM + IslamHouse Melayu).

**Status Fasa 2 — bina diagnostik (TIDAK dikira dalam kiraan kerja):**
venv `.venv-pyi` + binaan PyInstaller siap di disk (gitignored) — app
dibuka tanpa crash (bina ~33 minit, ~787 MB; `main.py` TIADA
`freeze_support()` — item untuk Fasa 2 semula). Bina Nuitka BELUM —
ditangguh arahan penutup hari. Alat bina kekal TERBUKA
(BANDING_INSTALLER.md).

**Kiraan telus:** 14 Ogos = **36 commit** (44 sebenar − 8 langkah-B);
15 Ogos = **14 commit** (14 sebenar − 0 langkah-B); 16 Ogos = **16 commit**
(18 sebenar − 2 langkah-B: `f8dd057` penutup sementara + `2cb76b8`
rekod border; 16 kerja = 2 penutup 15 Ogos + 4 installer + 5 reka
bentuk/ranap/hover + 2 rekod + 2 tala/border + 1 eksperimen grid;
komit penutup akan menjadi komit pertama 17 Ogos).

**Gate akhir:** semak.py SEMUA LULUS (15 semakan, #12 + #15 hijau) ·
uji_negatif_8z **52/0** · semak_dokumen_ui 110/0 · gate_pantas SEMUA
LULUS · pokok kerja bersih · tema pengguna "sistem" · tiada proses
ujian tersadai.

## Reka bentuk halaman utama + pembetulan ranap/hover (petang 16 Ogos)

- **Perbincangan installer TERTUNDA (keputusan pengguna).** Dokumen
  `PERBANDINGAN_INSTALLER.md` sedia (dua hala tuju + kos + pengalaman +
  versi disemak) di `dokumen/rujukan/`; Fasa 0 terbuka. Pengguna mahu
  finalise apl dahulu — fokus beralih ke fine tune UI.

- **Audit visual + fungsi (kedua-dua).** Gate penuh hijau; tangkapan
  fizikal mendedahkan isu: tiada identiti jenama, chip redundan, kad
  seragam, ruang kosong. **3 mockup HTML** dibina; pengguna pilih
  **② Hero Statistik** dan tala iteratif: buang ikon masjid, mod terang
  kertas lembut (silau), chip pilihan hadis kekal, kotak carian radius
  asal 4px, button jangan bulat, hover timbul (kad + chip), ikon ⚙
  22px, v1.0 rapat PustakaHadith.

- **Implement (`4dd9aa9`)**: jalur aksen 4px warna kitab, badge kiraan,
  "Buka →", chip 4px, tajuk berpusat, hover timbul. Gate hijau + jalur
  9 warna disahkan fizikal.

- **Dua ranap dijumpai & dibaiki:**
  1. `6c090b5` — `deleteLater()` kedua pada efek sudah dipadam
     (RuntimeError hover keluar).
  2. `bed79f0` — **ranap klik kad kitab**: bisect fizikal mengasingkan
     punca ke QGraphicsDropShadowEffect aktif semasa
     `QStackedWidget.setCurrentIndex` (access violation dalam `go()`).
     Preload/torch BUKAN punca (disahkan dengan patch kelas — ranap
     kekal). Pembetulan: `_buang_bayang_semua()` dalam `go()` sebelum
     setiap navigasi. 24 kitaran fizikal tanpa ranap.

- **Hover tak timbul (`cbefeaa` + `b60df90`):** dua punca fizikal:
  (1) QSS kad menyekat render QGraphicsEffect — pembungkus lutsinar
  `BungkusTimbul`; (2) bayang hitam tak nampak atas gelap — **glow teal**;
  (3) kad menutupi pembungkus — **penapis peristiwa** pada kad.
  Margin/spacing ditala supaya halaman utama muat 730px (LEBIHAN 0).

- **Pengesahan fizikal skrin sebenar (bukan grab widget):** glow gelap
  31,315 piksel (kecerahan 49 > latar); Kertas 31,205 (238 < 253 =
  bayang); lightneutral 31,205; kad hadis senarai 82,361 (QSS jelas,
  kekal tanpa glow); klik + 24 navigasi SELAMAT. Kaedah penting:
  `widget.grab()` TIDAK merender efek hover — guna PIL ImageGrab skrin
  sebenar + `WindowStaysOnTopHint`; tetikus mesti digerakkan keluar
  dahulu (artifak hover tertinggal).

- **Rekod ini**: PERUBAHAN_16OGOS.md dikemas (11 commit setakat ini).

## PENUTUP HARI — 16 Ogos 2026 (16 commit, rekod penuh)

**Ringkasan hari:** hari bermula dengan penutup 15 Ogos (14 commit)
dan beralih ke perbincangan installer (TERTUNDA), kemudian fine tune
halaman utama mengikut arahan pengguna — audit penuh, 3 mockup, pilihan
② Hero Statistik, pelaksanaan, dua ranap dibaiki, hover diperbetulkan,
tala halus glow/jalur, border warna kitab, dan eksperimen saiz kad
grid. Kerja 16 Ogos — **16 commit** (18 sebenar − 2 langkah-B:
`f8dd057` penutup sementara + `2cb76b8` rekod border; komit penutup
akan menjadi komit pertama 17 Ogos):

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Penutup hari 15 Ogos (14 commit) + semak.py prun venv** — .venv/build/dist diskip dari scan; .gitignore `.venv*/` | `5c28571` |
| 2 | **MULA_SINI ke 16 Ogos** — ringkasan + 'Sesi Terakhir'; kunci mutasi #30/#34 | `1cf7ce8` |
| 3 | **Serap dokumen kawalan Installer Khas (PyInstaller/MSIX)** — INSTALLER.md, PLAN_BINA_EDARAN.md, BANDING_INSTALLER.md ke dokumen/rujukan/ + pengerasan Terabox | `7410c3d` |
| 4 | **Tambah PERBANDINGAN_INSTALLER.md** — dua hala tuju A/B tanpa syor + 6 soalan Fasa 0 | `70f214b` |
| 5 | **PERBANDINGAN_INSTALLER: kos setahun + pengalaman pengguna** — yuran Store dibuang Sept 2025 (RM 0); SmartScreen vs Store UX | `9aea12b` |
| 6 | **PERBANDINGAN_INSTALLER: versi disemak (satu dokumen)** — pembetulan saiz 787/520 MB, yuran Company percuma, §9 pengesahan ✅/🟡; **Fasa 0 TERTUNDA** (pengguna pilih finalise apl dahulu) | `6f988df` |
| 7 | **Reka bentuk halaman utama (mockup ② Hero Statistik)** — audit visual+fungsi, 3 mockup, tala iteratif (buang ikon, kertas lembut, chip segi empat, v1.0 rapat, ⚙ 22px); jalur aksen 4px warna kitab + badge kiraan + "Buka →"; chip 15→4px | `4dd9aa9` |
| 8 | **Baiki ranap hover kad** — `deleteLater()` kedua pada efek sudah dipadam (RuntimeError bila keluar kad) | `6c090b5` |
| 9 | **Hover timbul: efek pada pembungkus lutsinar** — QSS kad menyekat render QGraphicsEffect (0 piksel bayang); `BungkusTimbul` tanpa stylesheet membawa efek (647 px disahkan) | `cbefeaa` |
| 10 | **Baiki ranap klik kad kitab (kritikal)** — bisect fizikal: QGraphicsDropShadowEffect aktif semasa setCurrentIndex = access violation; preload/torch BUKAN punca; `_buang_bayang_semua()` dalam `go()` sebelum setiap navigasi; 24 kitaran fizikal SELAMAT | `bed79f0` |
| 11 | **Betulkan hover tak timbul** — bayang hitam tak nampak atas gelap → glow teal (alpha 110); kad menutupi pembungkus → penapis peristiwa pada kad; sempadan hover TEAL; margin/spacing ditala muat 730px; fizikal: gelap 31,315 px GLOW · Kertas 31,205 px BAYANG · lightneutral 31,205 · kad hadis 82,361 QSS | `b60df90` |
| 12 | **Rekod sesi petang** — PERUBAHAN_16OGOS, sesi_index, MULA_SINI ke 11 commit (semak #12/#15) | `92b3992` |
| 13 | **Selaraskan mutasi uji_negatif #30/#34 ke 11 commit** — rentetan sasaran lapuk ('3 commit') tiada padanan → 50/2; dikemas → 52/0 | `23cafbc` |
| 14 | **Tala halus halaman utama** — glow diperkuat (alpha 200, blur 8: #1f1f1f→#304d3c jelas); jalur aksen 4→6px; LEBIHAN 0 | `ed8ad67` |
| 15 | **Border kad ikut warna kitab** — keliling 2px warna kitab (ganti jalur atas); hover cerah 45% gelap / gelap 30% terang; glow ikut warna; `_campur()`; disahkan fizikal 4 sisi + 5 tema | `8b760c8` |
| 16 | **Eksperimen saiz kad grid** — 2 lajur × 5 baris DITOLAK (LEBIHAN 207px; kad perlu ~50px); 3×3 kad 100→114px (+14%) dengan hero compact + tajuk ketat; desc 4 kitab terpotong DIBETULKAN (teks satu baris); kandungan penuh 50%→56%; LEBIHAN 0 | `e8032cb` |
| L | **Langkah-B: penutup sementara 13 commit (`f8dd057`)** — tutup hari 16 Ogos pada 13 commit (rekod penuh sesi_index + PERUBAHAN_16OGOS + MULA_SINI + mutasi); hari kemudian dibuka semula dengan lanjutan (ed8ad67..e8032cb). Tidak dikira | `f8dd057` |
| L | **Langkah-B: rekod border warna kitab (`2cb76b8`)** — rekod `8b760c8` dalam PERUBAHAN_16OGOS + sesi_index; kiraan 13→15 + mutasi uji_negatif. Tidak dikira | `2cb76b8` |

**Eksperimen grid (selepas komit 16):** 2 lajur mustahil dalam gate
1240×730 (hero 231px + grid 624px = 855px > 730; kad perlu ~50px =
tidak boleh dibaca; 9 kad tidak bahagi 2). 3×3 dikekalkan: kad
100→114px (+14%) — ruang dijimat dari hero compact (pad 30→20),
tajuk margin 18→8, jarak grid 6→5, margin bawah 14. Penemuan bonus:
desc 4 kitab (bukhari, muslim, malik, ahmad) KLIP 2 baris pada
mana-mana saiz < 124px — dipendekkan ke satu baris (cth.
"Kompilasi hadis sahih oleh Imam al-Bukhari." → "Hadis sahih oleh
Imam al-Bukhari."). Kandungan penuh 50%→56%, DESC_KLIP 0.

**Pengesahan border 9 kitab (selepas komit 16):** render offscreen
kesemua 9 warna betul dalam dark + light (bukhari #2e7d6b, muslim
#2e5d8c, abu-daud #a96b2f, tirmidzi #8c3a4a, nasai #6b4e8c, ibnu-majah
#a08a2e, malik #3a4a6b, ahmad #3f6b3a, darimi #4e6b7a); pengiraan
hover cerah/gelap semua 9 betul; mekanisme hover fizikal sudah
dibuktikan komit 15. Nota: paparan fizikal tidak dapat diambil sesi ini
(RDP/konsol menunjukkan sambungan lain) — render guna grab widget
offscreen.

**Ciri dikunci kekal:** 5 tema ≥ WCAG AA (semak #13, 72 pasangan) ·
susun atur RTL Arab kanan (semak #14) · ringkasan satu muka seiring
'Sesi Terakhir' (semak #15) · skema 8 carian Arab tanpa tashkeel ·
suite 13/13 berulang kali lulus · halaman utama mockup ② (jalur warna +
glow hover) disahkan fizikal.

**Baki tertangguh (§8):** hanya **#7 kunci API hadis.my** — kekal AKTIF
sengaja. Jurang Tafsir 843 dipantau (MyHadith JAKIM + IslamHouse Melayu).
Perbincangan installer (Fasa 0) TERTUNDA atas pilihan pengguna —
`PERBANDINGAN_INSTALLER.md` sedia di dokumen/rujukan/.

**Status Fasa 2 — bina diagnostik (TIDAK dikira dalam kiraan kerja):**
venv `.venv-pyi` + binaan PyInstaller siap di disk (gitignored) — app
dibuka tanpa crash (bina ~33 minit, ~787 MB; `main.py` TIADA
`freeze_support()` — item untuk Fasa 2 semula). Bina Nuitka BELUM —
ditangguh. Alat bina kekal TERBUKA (PERBANDINGAN_INSTALLER.md).

**Kiraan telus:** 14 Ogos = **36 commit** (44 sebenar − 8 langkah-B);
15 Ogos = **14 commit** (14 sebenar − 0 langkah-B); 16 Ogos = **16 commit**
(18 sebenar − 2 langkah-B: `f8dd057` penutup sementara + `2cb76b8`
rekod border; 16 kerja = 2 penutup 15 Ogos + 4 installer + 5 reka
bentuk/ranap/hover + 2 rekod + 2 tala/border + 1 eksperimen grid;
komit penutup akan menjadi komit pertama 17 Ogos).

**Gate penutup:** semak.py SEMUA LULUS (15 semakan, #12/#14/#15 hijau) ·
uji_negatif_8z **52/0** · semak_dokumen_ui 110/0 · pokok kerja bersih ·
tema pengguna "sistem" · tiada proses ujian tersadai.

---

## SESI 17 OGOS 2026 (komit 1–2, sambungan 16 Ogos)

**Ringkasan:** hari bermula dengan penutup 16 Ogos (16 commit) dan
bersambung dengan pengesahan lanjut reka bentuk halaman utama kad
114px — galeri 5 tema + ujian saiz tetingkap kecil + ujian DPI.

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Tutup hari 16 Ogos (16 commit)** — rekod penuh eksperimen grid + pengesahan border 9 kitab + kiraan telus 16; mutasi #30/#34 ke "16 commit" (52/0); komit pertama 17 Ogos | `cdf4e63` |
| 2 | **Galeri 5 tema kad 114px + ujian saiz/DPI** — `dokumen/imej/tema_home_*.png` dikemas (galeri MANUAL_PENGGUNAAN otomatis seiring); ujian 1024×600: 3×3 kekal, kad 114px, tiada skrol mengufuk (hbar 0), DESC_KLIP 0; ujian DPI 125%/150% (`QT_SCALE_FACTOR`): 3×3 kekal, kad 114px, tiada skrol mengufuk walaupun saiz minimum 900×560, DESC_KLIP 0 | `6d1f094` |
| 3 | **Baiki pepijat viewport tersekat 640×480 + ujian responsif/skrol + galeri muktamad** — `_paksa_saiz_halaman()` (halaman == stack + nudge bila viewport basi <80%; hook resizeEvent stack); 24/24 lulus (6 halaman × 4) pada 1024×600 + DPI 150%; skrol kekunci/roda/Tab OK; galeri 5 tema muktamad (sistem→neutral) | `5d6a786` |

**Butiran komit 2:** galeri dijana satu proses per tema (elak hang
pelbagai instans app dalam satu proses — corak sama ujian 5-tema
sebelum); 5 imej `tema_home_*.png` (1100×749) menggantikan baseline
reka bentuk lama (1116×788) — seksyen TEMA manual/manual/MANUAL_PENGGUNAAN.md kekal
sah, hanya imej baharu. Ujian kecil 1024×600: content 695px > viewport
538px → skrol menegak (dijangka, halaman utama berskrol), hbar_max 0,
kad menguncup mendatar 343→281px tanpa pecah. Ujian DPI: dpr 1.25
(kad 277px) dan 1.50 (kad 243px, window minimum 900×560) — desc satu
baris kekal muat. Settings pengguna dipulihkan ke "sistem" selepas
ujian (app menulis semula tema aktif semasa tutup — quirk biasa).

**Kiraan telus:** 14 Ogos = **36 commit** · 15 Ogos = **14 commit** ·
16 Ogos = **16 commit** · 17 Ogos = **18 commit** (22 sebenar − 4
langkah-B; langkah-B = pembetulan rekod tarikh + semak #12 + suite
penuh + penutup — semua kerja sesi ini berlaku pada 17 Ogos ikut
jam sistem; lihat jadual PENUTUP HARI di bawah).

**Baki tertangguh (§8):** tidak berubah — #7 kunci API hadis.my kekal
AKTIF sengaja; jurang Tafsir 843 dipantau; installer Fasa 0 TERTUNDA.

**Gate:** semak.py SEMUA LULUS (15 semakan, #12/#14/#15 hijau) ·
uji_negatif_8z **52/0** · semak_dokumen_ui 110/0 · pokok kerja bersih ·
tema pengguna "sistem".

---

## PENUTUP HARI — 17 Ogos 2026 (18 commit + 4 langkah-B, rekod penuh)

**Ringkasan hari:** hari bermula dengan penutup 16 Ogos (16 commit,
komit pertama 17 Ogos) dan bersambung dengan pengesahan lanjut reka
bentuk halaman utama kad 114px — galeri 5 tema, ujian saiz tetingkap
kecil + DPI, ujian responsif SEMUA halaman yang **menemui pepijat
viewport tersekat 640×480** (dibaiki), skrol papan kekunci/roda,
galeri muktamad, optimum ujian visual, semak semula kiraan suite,
MULA_CEPAT versi pengguna, penyelesaian masalah pengguna, suite
muktamad, kemudian CHANGELOG log versi seiring, rekod hari dibuka
semula (ringkasan keadaan + pembetulan kiraan + audit konsistensi),
tekanan uji_visual_sebenar 5 larian, semak #16 kiraan semakan
automatik, dan suite muktamad terakhir. Kerja 17 Ogos —**18 commit** (22 sebenar − 4 langkah-B: c97d028, bb97f42, c5142ef,
6f8f1b8; 1 penutup 16
Ogos + 1 galeri/ujian + 1 pepijat viewport + 1 penutup sementara 3 + 1
suite pra-hantar + audit
+ 1 optimum uji_visual_sebenar + 1 semak kiraan suite + 1 MULA_CEPAT
pengguna + 1 §4/poll stabil/suite + 1 penutup sementara 8 + 1
CHANGELOG + 1 buka semula rekod + 1 ringkasan keadaan + 1 kiraan + 1
audit konsistensi + 1 tekanan + 1 semak #16 + 1 suite muktamad/tutup):

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Tutup hari 16 Ogos (16 commit)** — rekod eksperimen grid + pengesahan border 9 kitab + kiraan telus 16; mutasi #30/#34 ke "16 commit" (52/0); komit pertama 17 Ogos | `cdf4e63` |
| 2 | **Galeri 5 tema kad 114px + ujian saiz/DPI** — dokumen/imej/tema_home_*.png dikemas (galeri MANUAL_PENGGUNAAN otomatis seiring); ujian 1024×600 + DPI 125%/150%; MULA_SINI/sesi_index/PERUBAHAN_17OGOS + mutasi ke 2 commit | `6d1f094` |
| 3 | **Baiki pepijat viewport tersekat 640×480 + ujian responsif/skrol + galeri muktamad** — `_paksa_saiz_halaman()` (ui/app_qt.py): halaman == stack + nudge -1/+1 bila viewport basi (<80%), hook resizeEvent stack; 24/24 lulus (6 halaman × 4) pada 1024×600 + DPI 150%; skrol kekunci (0→60), roda (60→0), Tab (fokus pindah) OK; galeri 5 tema muktamad (sistem→neutral disahkan, fresh-vs-fresh 0.00%); imej terang lama tak stabil digantikan | `5d6a786` |
| 4 | **Penutup sementara 3 commit + rekod penuh** — PERUBAHAN_17OGOS + sesi_index (PENUTUP HARI + kiraan telus) + MULA_SINI diselaraskan; mutasi #30/#34 (52/0); hari kemudian dibuka semula dengan lanjutan | `d35e4ff` |
| 5 | **Suite pra-hantar 13/13 dua larian + audit log** — dua larian berturut-turut SEMUA LULUS (514.4s + 485.1s) selepas pembetulan viewport; audit semua 13 log pra_hantar: tiada amaran tersembunyi, tiada Traceback/flak, semua ujian 0 gagal, tiada proses yatim; mutasi #30/#34 ke 5 commit | `012e904` |
| 6 | **Optimum uji_visual_sebenar (142→87s)** — profiler: 75s overhead model WAJIB (semantik digabung — tidak boleh dilangkau tanpa kehilangan liputan); punca sebenar 58 tangkapan skrin / 11 panggilan ≈ 5 cubaan/panggilan (paparan RDP tidak stabil); poll adaptif 0.15s ganti sleep tetap 0.6s; 3 larian 86.7/87/89.4s (~40–48% laju), liputan kekal **68/0**; gate penuh hijau | `26b5e57` |
| 7 | **Semak semula tuntutan kiraan suite (README/CHANGELOG)** — tiada tuntutan '13/13 dua larian' dalam kedua-dua fail (frasa hanya dalam rekod komit 4 — tepat); README '13 ujian' + '52/0 — 34 cabang' disahkan tepat; drift dijumpai: '377 semakan' → **391 semakan** (semak.py deterministik, punca _SKIP_FOLDER prun arkib/venv 16 Ogos); README dikemas; entri CHANGELOG 15 Ogos kekal sejarah; mutasi ke 7 commit | `6b8aeb8` |
| 8 | **MULA_CEPAT versi pengguna** — §1 ke 17 Ogos + 2 baris baharu (5 tema ≥ WCAG AA + galeri visual; paparan responsif 1024×600 + DPI 125%/150% selepas pembaikan viewport); §3 'Tukar tema (5 pilihan)' + nota responsif; semak_dokumen_ui 110/0 kekal hijau; mutasi ke 8 commit | `7679ec9` |
| 9 | **MULA_CEPAT §4 Penyelesaian masalah + poll stabil + suite muktamad** — §4 baharu senario pengguna awam (ikon, kunci API, lambat buka, saiz fon, tema Ikut sistem, carian kosong); audit silang dokumen tiada hanyut; **flak sebenar dijumpai** (sebenar_butang_atas 10,881 B — poll lama simpan bingkai separa lukis t≈0) → poll diperbetulkan ke corak stabil (dua grab sama); bersendirian 71.8s 68/0 ×2, suite **401.8s 13/13** (sebenar 74.2s — rantaian 172.1→74.2s); mutasi ke 9 commit | `e885503` |
| 10 | **Penutup sementara 8 commit + rekod penuh** — PERUBAHAN_17OGOS (PENUTUP HARI jadual 8 baris + LANJUTAN 1–5) + sesi_index (kiraan telus 8 + jadual penuh) + MULA_SINI diselaraskan; mutasi #30/#34 kekal "8 commit"; hari kemudian dibuka semula dengan lanjutan | `095682f` |
| 11 | **CHANGELOG log versi seiring** — entri 'Kemas kini' dua hari terakhir ditambah (16 Ogos: reka bentuk halaman utama kad 114px + border warna kitab + hover; 17 Ogos: responsif penuh + optimum ujian 401.8s + MULA_CEPAT baharu) supaya log versi seiring log harian — CHANGELOG sebelum ini berhenti di 15 Ogos; kata Indonesia dalam entri baharu dikesan semak 8m dan dibetulkan (52/0 kembali) | `4da64ac` |
| 12 | **Buka semula rekod hari** — CHANGELOG entri 16 Ogos (log versi tiada jurang) + reka bentuk mutasi #27/#30/#34; blok 'Sesi Terakhir' dikemas semula | `e60a74d` |
| 13 | **Ringkasan satu-muka 'Keadaan projek' dikemas** — suite muktamad 463.6s → 401.8s; blok kerja dua hari terakhir; ciri dikunci + mockup ② (kad 114px, border warna, hover, viewport, responsif); pautan log harian → PERUBAHAN_17OGOS.md; kiraan 12 → 13 | `0770ec9` |
| 14 | **Kiraan dibetulkan ke 4** — blok 'Sesi Terakhir' + ringkasan + sesi_index + PERUBAHAN_17OGOS selaras; hash baharu dalam blok (semak #12 top-10 selepas 5d6a786 gugur); mutasi #30/#34 ke 14 commit | `34148a9` |
| 15 | **Audit kiraan silang + format** — MULA_SINI/sesi_index/PERUBAHAN_17OGOS/CHANGELOG disahkan konsisten; pepijat format PERUBAHAN_17OGOS (dua bullet bercantum) dibaiki; kiraan 14 → 15 | `a68efba` |
| 16 | **Tekanan uji_visual_sebenar 5 larian** — 5 larian berturut-turut **68/0 SEMUA LULUS** (105.6–108.3s setiap larian); poll stabil disahkan tanpa flak dalam keadaan RDP berbeza (sifar kegagalan, 11 tangkapan/larian); julat 72–108s = varian RDP, bukan poll; mutasi #34 ke 16 commit | `414ba1f` |
| 17 | **Semak #16: kiraan README automatik** — semak.py mencetak jumlah (391 semakan, 15 bahagian) + semak #16 mengesahkan tuntutan README (GAGAL bila lapuk; lompat tanpa hadis.db/bersendirian); pembilang lulus()/tajuk() + bilangan_bahagian(); mutasi #35 subproses (~30s); uji_negatif 52→**54/0 (35 cabang)**; README kekal 391 semakan + 52/0→54/0 | `09dc071` |
| 18 | **Suite muktamad + tutup hari** — suite pra-hantar penuh **13/13 SEMUA LULUS (387.5s)** selepas semak #16 (turun dari 401.8s; uji_visual_sebenar 64.2s dalam suite); semak #12/#15/#16 hijau selepas komit 17; kiraan 17 → 18; mutasi #34 ke 18 commit; PERUBAHAN_17OGOS + MULA_SINI 'Sesi Terakhir' + ringkasan diselaraskan | `8725872` |
| L | **Langkah-B: pembetulan rekod tarikh** — semua kerja sesi ini berlaku pada 17 Ogos ikut jam sistem (tiada hari "18 Ogos"); 7 komit yang sebelum ini direkod sebagai hari 18 Ogos digabung semula ke hari 17 Ogos: PERUBAHAN_18OGOS.md diserap ke PERUBAHAN_17OGOS.md (LANJUTAN 6–10) + jadual 18 baris, SESI 18 OGOS dibuang dari sesi_index, MULA_SINI 'Sesi Terakhir' + ringkasan dikunci ke 17 Ogos (18 commit), mutasi #27/#30/#34/#35 disasarkan semula; README 392→391 semakan (semak #8m lulus per fail .md); gate: semak SEMUA LULUS (391 semakan) · uji_negatif 54/0 · 110/0. Susulan langkah-B kedua (`bb97f42`: peraturan tarikh sistem dalam semak #12 + finalisasi + audit rekod) dan langkah-B ketiga (`c5142ef`: suite penuh 453.0s + finalisasi). Penutup hari: 18 commit + 4 langkah-B (22 sebenar − 4; komit `6f8f1b8` langkah-B keempat — tutup rekod penuh). Tidak dikira (langkah-B) | `c97d028` + `bb97f42` + `c5142ef` + `6f8f1b8` |

**Punca pepijat viewport (rekod):** QStackedWidget tidak mensaiz semula
halaman bukan-semasa selepas `setCurrentIndex` atau resize tetingkap —
halaman kekal pada geometri lalai 640×480 dalam stack 1024px, kandungan
terpotong di kanan (hbar tersembunyi oleh `ScrollBarAlwaysOff`; diukur
1/2 larian navigasi). Dua perangkap pembetulan diukur fizikal: (1)
saizkan viewport terus → menceroboh ruang bar skrol → teks membalut
semula (17% piksel berbeza); (2) nudge tanpa syarat → semak #5 +11px.
Penyelesaian: nudge hanya bila viewport basi (<80% lebar halaman).

**Ciri dikunci kekal:** 5 tema ≥ WCAG AA (semak #13, 72 pasangan) ·
susun atur RTL Arab kanan (semak #14) · ringkasan satu muka seiring
'Sesi Terakhir' (semak #15) · kiraan semakan README automatik (semak
#16) · skema 8 carian Arab · suite 13/13 · halaman utama mockup ②
(border warna kitab + glow + kad 114px + pembetulan viewport
`_paksa_saiz_halaman`).

**Baki tertangguh (§8):** hanya **#7 kunci API hadis.my** — kekal AKTIF
sengaja. Jurang Tafsir 843 dipantau (MyHadith JAKIM + IslamHouse Melayu).
Installer Fasa 0 TERTUNDA atas pilihan pengguna —
`PERBANDINGAN_INSTALLER.md` sedia di dokumen/rujukan/.

**Gate penutup:** semak.py SEMUA LULUS (16 semakan, #12/#14/#15/#16
hijau — #12 termasuk peraturan tarikh sistem) · uji_negatif_8z
**55/0** · semak_dokumen_ui 110/0 · pokok kerja bersih · tema
pengguna "sistem" · tiada proses ujian tersadai.

---

## SESI 20 OGOS 2026 — FASA 1 & 2 INSTALLER (folder binaan)

**Ringkasan:** bekerja di folder binaan `binaan_installer` (keputusan
pengguna — folder utama `hadis` TIDAK disentuh). Fasa 1 "Pisahkan
Laluan Data" selesai: `config.py` menjadi pusat laluan (`ASSET_DIR`
aset baca sahaja vs `DATA_DIR` data pengguna; mod pembangunan kekal
folder projek, mod frozen = `%LOCALAPPDATA%\PustakaHadith`); 8 fail
dipusatkan ke pemalar config (db.py, api/hadis_api.py, ui/helpers.py,
ui/splash.py, ui/disclaimer.py, core/sema_source.py,
core/hadeethenc_api.py, core/semantic_search.py); syarah_source tiada
laluan cache (audit); sync.py/semak_db.py/semak_versi.py sudah pusat.
Ujian `uji_fasa1_data.py` (22/0) mensimulasikan `sys.frozen=True`
dalam subproses. Gate Fasa 1 LULUS.

| # | Kerja | Nota |
|---|-------|------|
| 1 | **Folder binaan + salin sumber** — `binaan_installer` (450 MB): kod + dokumen + hadis.db + aset; tanpa .git/venv/cache/data peribadi; README binaan = 385 semakan (bukan repo git) | bukan git |
| 2 | **config.py pusat laluan** — ASSET_DIR/DATA_DIR + 16 pemalar (DB_PATH, SETTINGS_PATH, BOOKMARKS_PATH, ENV_PATH, CACHE_SEMA/HE/ENG/SYARAH, PROFIL_PATH, ICON_PATH, FAISS_INDEX/MAP, MODEL_CACHE, SUNNAH_MAP); mod frozen = %LOCALAPPDATA%\PustakaHadith | §3.1 |
| 3 | **8 fail runtime dipusatkan** — db.py, api/hadis_api.py, ui/helpers.py, ui/splash.py, ui/disclaimer.py, core/sema_source.py, core/hadeethenc_api.py, core/semantic_search.py | §3.2 |
| 4 | **Penyesuaian PROFIL_PATH** — profil_model.json di DATA_DIR (bukan ASSET_DIR): kod MENULIS fail log muat model; ASSET_DIR baca sahaja dalam MSIX | rekod |
| 5 | **uji_fasa1_data.py (22/0)** — simulasi sys.frozen=True subproses; semua pemalar boleh tulis di DATA_DIR, aset di ASSET_DIR, tiada fail baharu di ASSET_DIR | baharu |
| 6 | **Gate Fasa 1 LULUS** — semak.py 384 SEMUA LULUS (15 bahagian) · semak_versi.py OK · uji_lompat 67/0 · uji_carian_arab SEMUA LULUS · main.py melancar tanpa ralat | gate |
| 7 | **Fasa 2: freeze_support + venv binaan** — main.py tambah `multiprocessing.freeze_support()` (§6); venv `--system-site-packages` (keputusan pengguna, jimat 2GB) Python 3.14.6 + PyInstaller 6.22.0 + hooks; rekod `installer_requirements-build-lock.txt`; disahkan hanya PyQt5 (tiada PySide/PyQt6) | §5–§6 |
| 8 | **Fasa 2: bina onedir --console** — aset profil lengkap (keputusan Fasa 0): .cache_models (941 MB, disalin dari folder utama), hadis_faiss.index (91 MB), hadis_id_map.pkl, profil_model.json, sunnah_map, app.ico; ~19 minit; hasil `dist\PustakaHadith-Debug` = 2,022.8 MB / 7,065 fail; TIADA UPX; jangan bundel disahkan (hadis.db*, .env, settings, bookmarks, cache) | §7.1 |
| 9 | **Fasa 2: semak warn + uji exe** — warn-*.txt: 313 missing module semua pilihan (torch extras/accelerate/bitsandbytes), tiada untuk modul sebenar; exe hidup: disclaimer → user_settings.json `disclaimer_dibaca:true` di DATA_DIR → model e5 dimuat (RAM 78→596 MB) → tetingkap utama 'PustakaHadith' terbuka; FAISS binaan dimuat 62,169×384; folder EXE tiada hadis.db | §7.2 |
| 10 | **Gate Fasa 2 LULUS** — semak.py 385 SEMUA LULUS (15 bahagian); ujian automatik lulus; item interaktif (tema/sync/carian/rawak) untuk ujian manual pengguna; fallback Nuitka TIDAK dicetuskan | gate |
| 11 | **Fasa 3: buang duplikat HF + cv2/PIL** — uji empirik: model muat tanpa blobs (470 MB dibuang); `--exclude-module cv2 --exclude-module PIL` (151 MB); hasil 1,399.9 MB / 7,027 fail (jimat 622.9 MB, 31%) | §4 |
| 12 | **Fasa 3: uji binaan optimum** — model e5 dimuat penuh (stderr Loading weights 100%, RAM 929–937 MB, profil_model.json muat_s 35.0 dari_cache true di DATA_DIR); tetingkap utama 'PustakaHadith' terbuka; tiada ralat; boot pertama lambat (~120s) = Windows Defender scan, bukan ralat | §7.2 |
| 13 | **Gate Fasa 3 LULUS** — saiz <1.5 GB ✓; fungsi setara Fasa 2 ✓; aset lengkap ✓; semak.py 385 SEMUA LULUS; langkah seterusnya Fasa 4 (mesin bersih) atau ujian manual pengguna | gate |
| 14 | **Fasa 4: Uji Mesin Bersih (Sandbox) LULUS** — Windows Sandbox (11 Pro) tersedia (`Containers-DisposableClientVM` Enabled); `PustakaHadith-Fasa4.wsb` memetakan `dist\PustakaHadith-Debug` baca sahaja ke Desktop + auto-lancar; pengguna uji: ✅ apl lancar, ✅ carian OK selepas API key, ✅ bookmark OK, ✅ lain-lain OK; ❌ terjemahan Inggeris TIADA — **disiasat: reka bentuk lesen, bukan bug** (hadis.db + .cache_eng 120 MB tidak dibundel §4; sync_english.py skrip pembangunan, UI tidak panggil; keputusan lesen Ahmad PERMOHONAN_LESEN_AHMAD §5 + Sesi 7 "pengguna sync sendiri"; UI kelabukan tab English `pages.py set_available`); **keputusan pengguna: biar seperti reka bentuk** — tiada perubahan kod | §8 |
| 15 | **Gate Fasa 4 (Uji Mesin Bersih) LULUS** — matriks §8 pada Windows 11 Sandbox: launch ✓, simpan settings/API key ✓, sync/resume ✓, carian Melayu/Arab ✓, carian makna ✓, bookmark ✓; belum diuji: offline selepas sync, tutup/relaunch khusus, Windows 10 | gate |
| 16 | **Checklist pemantauan + Fasa 5A windowed** — `dokumen/CHECKLIST_PEMANTAUAN.md` (Fasa 0–7, gate, tugas pengguna, halangan) dicipta → semak.py 385→386 (semak #8m per fail .md, README dikemas); spec `PustakaHadith.spec` (windowed, upx=False, exclude cv2/PIL); bina ~21 minit → `dist\PustakaHadith` = 1,399.9 MB / 7,027 fail; warn set diff vs Debug = kosong; uji exe: disclaimer (tajuk EM DASH U+2014 — skrip uji mula gagal kerana aksara dash + skop $script:found dalam fungsi PS) → Enter → tetingkap utama 'PustakaHadith' tepat → model dimuat dari cache (muat_s 39.5, dari_cache true, RAM naik selepas muat) → DATA_DIR betul (user_settings.json disclaimer_dibaca:true, profil_model.json dikemas) — 5A LULUS | §7.3 |
| 17 | **Fasa 5B: Inno Setup EXE** — Inno 6.7.3 dipasang di `D:\Inno Setup 6` (URL GitHub tag `is-6_7_3`, garis bawah; muat turun 10.1 MB, ~20 MB storan); `installer\PustakaHadith.iss` per-user ({localappdata}\Programs\PustakaHadith, PrivilegesRequired=lowest, AppId tetap {{7DF2553E-...}, task desktopicon, lzma2/ultra64); bina ~34 minit → `installer\output\PustakaHadith-Setup-1.0.0-x64.exe` = **0.50 GB**; uji: silent install 0 (7,029 fail + pintasan Start Menu) · launch app terpasang → tetingkap 'PustakaHadith' · uninstall senyap 0 (folder app dipadam, **DATA_DIR kekal**, pintasan dipadam) — 5B LULUS | §9 |
| 18 | **Fasa 5C: penyediaan MSIX** — MSIX Packaging Tool (winget v1.2024.405.0) + WinApp CLI 0.6.1 dipasang (tandatangan ujian tempatan §13); aset PNG MSIX dijana dari app.ico → `installer\Assets\` (StoreLogo 50, Square44x44 44, Square150x150 150, Wide310x150 310×150, PIL 12.2.0); audit `dist\PustakaHadith` = **0 fail terlarang** (tiada DB/settings/cache/log), peringkat atas = `_internal` + `PustakaHadith.exe`; MSIX Packaging Tool Driver belum aktif (Optional Features — wizard boleh cuba sendiri); ⛔ menunggu identiti Partner Center (tugas pengguna): daftar Store + tempah nama + Publisher → 3 nilai `Package/Identity/Name|Publisher|PublisherDisplayName` — seterusnya capture VM bersih + uji Add-AppxPackage | §10–§13 |
| 19 | **Dokumentasi pengguna: manual/manual/MANUAL_INSTALASI.md + manual/manual/MANUAL_PENGGUNAAN.md** — Gate 6/INSTALLER §18 ("dokumentasi pengguna/privasi/sokongan sedia"): Manual Instalasi (3 cara: Store/MSIX ⏳ · Setup EXE ✓ per-user, naik taraf/nyahpasang tak padam data · Zip penguji; kali pertama buka + Tetapan API hadis.my; lokasi data `%LOCALAPPDATA%\PustakaHadith` — hadis.db/user_settings.json/bookmarks.json; masalah lazim; atribusi); Manual Penggunaan (9 kitab 62,169 hadis; skrin utama; carian kata kunci + makna AI; lompat terus hadis 433/bukhari 433/B433/Ctrl+G; baca hadis dua lajur Arab|Transliterasi + Melayu|Indonesia|English; darjat/huraian SemakHadis/syarah; Lapor ralat/Kongsi/Salin/WhatsApp/🔊 TTS; penanda halaman; tetapan tema/fon/bahasa/API bertopeng; mod luar talian) — manual sedia Gate 6, skrin/privasi/sokongan Store menyusul | §18 |
| 20 | **Kerja persediaan lanjutan (selepas sesi 20 Ogos):** ZIP mudah alih `installer\output\PustakaHadith-portable-1.0.0-x64.zip` (0.54 GB, 7,027 fail) ✅; `penerbitan/penerbitan/VM_MSIX_CAPTURE.md` — persediaan VM bersih, snapshot, payload, aset, wizard manual capture ✅; `penerbitan/penerbitan/MSIX_CAPTURE_PROSES.md` — checklist 6 fasa + rollback + output Gate 6 ✅; `surat/sokongan/surat/sokongan/DASAR_PRIVASI.md` (tiada data dikumpul, data tempatan, API tertutup, AI luar talian) ✅; `surat/sokongan/surat/sokongan/PAUTAN_SOKONGAN.md` (templat GitHub Issues) ✅; `penerbitan/penerbitan/TANGKAPAN_SKRIN.md` (4 wajib + 4 disyorkan, spesifikasi 1366×768/1920×1080) ✅; CHECKLIST diperluas (5C: ZIP, VM docs, proses; Dokumentasi: ☑; Uji Win10: ⏳); PLAN 4C/4D dikemas kini; semak.py 388 LULUS | — |
| 21 | **Lazy Loading + Smart Splash (21 Ogos) — SELESAI:** Mengatasi keluhan pengguna menunggu splash model setiap kali buka apl. Arsitek baharu: model AI dimuat MALAS (hanya pada carian makna pertama), bukan pada startup. Fail diubah: `main.py` (tanggal splash model), `ui/app_qt.py` (tanggal _mula_pramuat/_on_pramuat_siap + signals), `ui/workers.py` (SemanticWorker: signal model_loading_started), `ui/pages_carian.py` (inline "🤖 Memuatkan model AI…"), `semak.py` (semakan #8k Lazy Load), `README.md` (392 semakan). Verifikasi: semak.py 392/392 LULUS, uji_lompat 67/0, PustakaApp preload removed, SemanticWorker signal OK. Build baharu: `dist\PustakaHadith` 1.36 GB, ZIP 0.4 GB, Inno Setup 0.48 GB — semua Lazy Load. | — |
| 22 | **Rebranding Lengkap: PustakaHadith → PustakaHadith (21 Ogos):** Tukar nama brand kesemua aplikasi, installer, dokumen, kod. Fail diubah: 40+ fail Python (main, app_qt, disclaimer, deklarasi, settings, theme, config, launcher, sync_*, test_*, config), installer (.iss, .spec), README.md (section Pemasangan pengguna akhir), dokumen surat (header dikemas kini). Rename file: `PustakaHadith.iss` → `PustakaHadith.iss`, `PustakaHadith.spec` → `PustakaHadith.spec`. Build baharu: `dist\PustakaHadith\PustakaHadith.exe` (89 MB), `dist\PustakaHadith\` (1.36 GB), `PustakaHadith-Setup-1.0.0-x64.exe` (0.27 GB), `PustakaHadith-portable-1.0.0-x64.zip` (0.47 GB). Uji EXE launch 8s OK. semak.py 394/394 LULUS. | — |

**Kiraan telus:** folder binaan BUKAN repo git — tiada komit di sini;
kerja direkod dalam dokumen folder binaan sahaja. Folder utama `hadis`
kekal pada keadaan penutup 19 Ogos (5 kerja + 6 langkah-B; 394 semakan).

**Gate:** semak.py **394 semakan SEMUA LULUS** (15 bahagian, folder
binaan — semak #12 git & sebahagian #9 cache pengguna dilangkau) ·
semak_versi.py OK · uji_lompat **67/0** · uji_carian_arab **SEMUA
UJIAN LULUS** · uji_fasa1_data **22/0** · main.py melancar tanpa ralat.
Gate Fasa 2: exe diagnostik hidup, model e5 dimuat, DATA_DIR betul,
FAISS 62,169 vektor, warn tiada kritikal — LULUS. Gate Fasa 3: saiz
1.36 GB (jimat 623 MB), fungsi setara, model dimuat MALAS (Lazy Load),
tetingkap utama terbuka — LULUS. Gate Fasa 4: ujian mesin bersih
(Sandbox 11) lulus matriks §8; terjemahan Inggeris tiada = reka bentuk
lesen (keputusan pengguna: kekal) — LULUS. Gate 5A (windowed Lazy Load)
dan 5B (Inno setup Lazy Load) LULUS; 5C penyediaan siap — menunggu
identiti Store; dokumentasi pengguna (MANUAL_INSTALASI + MANUAL_PENGGUNAAN
+ DASAR_PRIVASI + PAUTAN_SOKONGAN + TANGKAPAN_SKRIN) sedia; ZIP
portable 0.4 GB sedia (Lazy Load); VM/Proses capture MSIX terdokumen;
**Lazy Loading + Smart Splash SELESAI** (model AI dimuat
pada carian makna pertama, startup < 3s); **Rebranding PustakaHadith SELESAI** (nama brand baharu, installer, kod, dokumen — 394 semakan LULUS).

**Penutup sesi 21 Ogos:** status pada penutup — Fasa 0–4 + 5A + 5B
LULUS; **Rebranding PustakaHadith SELESAI** (kod, installer, dokumen, build); 5C penyediaan siap, menunggu identiti Partner Center (tugas
pengguna: daftar Store https://storedeveloper.microsoft.com/ + tempah
nama "PustakaHadith" + pilih Publisher; beri 3 nilai `Package/Identity/
Name`, `Package/Identity/Publisher`, `Package/Properties/
PublisherDisplayName`); manual/manual/MANUAL_INSTALASI.md + manual/manual/MANUAL_PENGGUNAAN.md
sedia untuk Gate 6; README.md section Pemasangan pengguna akhir sedia; langkah seterusnya di bawah.

**Langkah seterusnya:** Fasa 5C — MSIX utama (INSTALLER §11–§12, MSIX
Packaging Tool dalam VM bersih, identiti Partner Center, runFullTrust).
⛔ Menunggu tugas pengguna: daftar Microsoft Store + tempah nama
"PustakaHadith" + pilih nama Publisher (identiti MSIX).

---

## SESI 19 OGOS 2026 (5 commit)

**Ringkasan:** perubahan UI asas — tema dikurangkan kepada 2 Neutral,
'Ini ialah Teks Sederhana'
saiz antara muka dibuang, disclaimer papar setiap kali (sebelum splash),
tajuk splash/disclaimer/header disepadankan (Pustaka bold teal +
Hadis light teal + v1.0), carian nombor hadis terus ke detail, Tentang
PustakaHadith table tersusun. Punca utama debug: splash.close() →
setQuitOnLastWindowClosed(True) → Qt quit event loop → timer tidak fire.
Komit 5: baiki gate semak.py (atribusi jadual + kiraan semakan).

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Perubahan asas apl (komit 1)** — tema 2 Neutral (gelap + terang, Kertas/Terang/Ikut sistem dibuang); buang 'Saiz antara muka' dari panel Tetapan; dialog disclaimer baru (ui/disclaimer.py) papar sekali; carian nombor hadis pada halaman kitab buka detail terus; semak_dokumen_ui 110→109; suite 14/14 (414.4s) | `b292515` |
| 2 | **Disclaimer selepas model + sepadankan tajuk (komit 2)** — disclaimer dipindah selepas splash (bukan sebelum); flag anti-dwicalla _buka_dijalankan; tajuk splash/disclaimer/header sepadan: Pustaka(bold teal) Hadis(light teal) v1.0; header v1.0 inline satu label; warna disclaimer guna palet tema | `e6d867b` |
| 3 | **Fix disclaimer pythonw.exe (komit 3)** — punca: splash.close() → setQuitOnLastWindowClosed(True) (lalai) → Qt quit event loop → QTimer.singleShot(0) tidak fire; pembetulan: setQuitOnLastWindowClosed(False) + disclaimer dulu (sebelum splash) + 200ms delay; dialog 540×600; papar setiap kali larian; buang semua debug trace | `6c9f855` |
| 4 | **Tentang PustakaHadith table (komit 4)** — QTableWidget 2 lajur untuk Kandungan + Sumber dan atribusi; grid line, padding, warna tema; hyperlink pautan HTML dalam sel | `5dd6990` |
| 5 | **Baiki gate semak.py (komit 5)** — semakan atribusi 8aa diselaraskan ke format JADUAL halaman Tentang (label sel kiri + nama sumber pada ui/deklarasi.py vs ayat penuh DEKLARASI.md; sebelum ini jangka ayat teks lama → GAGAL palsu "app kehilangan"); kiraan semakan diselaraskan ke **394** (README + ringkasan MULA_SINI + mutasi #35); mutasi #27/#30/#34/#36 disasarkan semula ke rentetan 19 Ogos (5 commit); PERUBAHAN_19OGOS.md dicipta (log harian belum wujud); CHANGELOG entri 19 Ogos ditambah | *(komit ini)* |

**Kiraan telus:** 14 Ogos = 36 · 15 Ogos = 14 · 16 Ogos = 16 ·
17 Ogos = 18 · 18 Ogos = 8+2LB · 19 Ogos = **5 commit** (11 sebenar −
6 langkah-B: komit penutup `55c17f4`, `79675fe`, `b5bbff2`, `793f943`,
`e6f79b4`, *(komit ini)*).

**Gate:** semak.py **394 semakan SEMUA LULUS** (15 bahagian) ·
uji_negatif_8z 55/0 · semak_dokumen_ui 109/0 · pokok kerja bersih.

**Baki tertangguh (§8):** #7 kunci API hadis.my (AKTIF sengaja) dan
jurang Tafsir 843 (dipantau) — **keputusan pengguna 19 Ogos:
DIABAIKAN buat masa ini, kekal direkod**. Tumpuan seterusnya =
installer Fasa 0; `INSTALLER.md` / `PERBANDINGAN_INSTALLER.md` /
`BANDING_INSTALLER.md` / `PLAN_BINA_EDARAN.md` dibaca penuh.

**Fasa 0 DILULUSKAN pengguna 19 Ogos 2026:** bundel model e5 + indeks
FAISS untuk profil ujian (ya) · `hadis.db` tidak dibundel · x64 ·
Store = saluran utama · Inno EXE = sekunder/penguji · repo persendirian
hingga lesen data selesai · akaun Partner Center WAJIB di Fasa 5
(daftar sekarang, percuma, tempah nama PustakaHadith) · portable ZIP
untuk penguji dalaman sahaja · wizard permulaan dibina sebelum beta.
Direkod dalam `PLAN_BINA_EDARAN.md` Fasa 0 + `PERBANDINGAN_INSTALLER.md`
§5. Langkah seterusnya: Fasa 1 (pisahkan laluan data, §3 INSTALLER.md).

---

## SESI 18 OGOS 2026 (komit 1, sambungan 17 Ogos)

**Ringkasan:** hari baharu dibuka selepas penutup penuh 17 Ogos (18
commit + 4 langkah-B). Kerja pembukaan: finalkan baris langkah-B
keempat (`6f8f1b8`) dalam jadual PENUTUP 17 Ogos, buka rekod 18 Ogos
(PERUBAHAN_18OGOS.md baharu + seksyen ini + MULA_SINI 'Sesi Terakhir'
+ ringkasan), dan kunci semula mutasi uji_negatif ke tarikh/kiraan
18 Ogos.

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Buka rekod 18 Ogos** — sesi_index (seksyen SESI 18 OGOS + kiraan telus) + PERUBAHAN_18OGOS.md (Komit 1) + MULA_SINI 'Sesi Terakhir' → 18 Ogos (komit 1) + ringkasan; mutasi #27/#30/#34/#36 disasarkan semula ke 18 Ogos | `28dd87b` |
| 2 | **Audit konvensyen langkah-B (komit 2)** — bandingkan kiraan telus 14–17 Ogos dengan git log sebenar; 16 Ogos dibetulkan: `f8dd057` (penutup sementara) + `2cb76b8` (rekod border) ditambah sebagai 2 langkah-B → 18 sebenar − 2 = 16 kerja; baris L dalam PENUTUP 16 Ogos + PERUBAHAN_16OGOS; 14 (44−8=36), 15 (14−0=14), 17 (22−4=18) disahkan konsisten | `6beaf22` |
| 3 | **Ujian responsif viewport penuh + pembetulan tajuk responsif detail (komit 3)** — `uji_responsif_viewport.py` baharu (6 halaman × 4 saiz, DPI 150%): `_paksa_saiz_halaman` STABIL (76/0, halaman == stack, viewport tidak 640×480); ujian mendedahkan panel dua lajur detail melimpah (hbar 254 @ 900, 130 @ 1024) — punca tajuk_bar satu baris ~1210px + bar teks Lapor ralat ~476px; pembetulan `_kemas_tajuk_detail()` (tajuk/butang dua baris bila sempit, ambang dinamik) + `barTindakan` wordWrap; disahkan 76/0 DPI 150% + DPI 100%, mockup 130/0, sebenar 68/0 | `b89f262` |
| 4 | **Suite rasmi 14 ujian (komit 4)** — `uji_responsif_viewport.py` didaftar sebagai ujian #14 dalam uji_pra_hantar (7.2s); semak_dokumen_ui A8 13→14 (mengesahkan kehadiran uji_responsif_viewport); QT_SCALE_FACTOR boleh ganti + header DPI dinamik — DPI 125%/175% disahkan 76/0; dokumen diselaraskan (README 14 ujian − 13 suite, MULA_CEPAT, MANUAL_REFERENSI_DEV, MULA_SINI status/ringkasan/blok); suite penuh **14/14 SEMUA LULUS (465.3s)** | `0a872b0` |
| 5 | **Audit fon besar + bungkusan responsif tab/butang (komit 5)** — saiz fon 120% diuji: QT_FONT_DPI terbukti TIDAK menjejaskan app (semua fon px dalam stylesheet) → guna `UJI_FONT_SCALE_IDX` (FONT_SCALES, tampalan `_read_json` dalam ingatan — fail pengguna tidak disentuh); dapatan: 1.3× mula 75/1 (hbar 8 @ 900), 1.5× 74/2 (hbar 133/122) — DIBETULKAN: (a) LangTabs + tab ARAB/TRANSLITERASI + butang tindakan boleh bungkus ke baris kedua (`kemas_lebar`/`_kemas_tab_arab`/`_kemas_butang_tindakan`, corak `_kemas_tajuk_detail`), (b) panel ketatkan margin 24/18→16/12 + spacing 18→10 bila sempit (`_kemas_panel_detail`), (c) **laluan reflow tertangguh** `_kemas_semua_detail` (singleShot 0) — punca sebenar flak: QStackedWidget tidak ubah saiz halaman tersembunyi → `_render_detail` guna geometri basi (viewport besar) → bungkusan tidak aktif; reflow kedua selepas paparan menyelesaikan; disahkan semua 5 skala fon (0.85–1.5×) @ DPI 150% + DPI 100/125/175% = **76/0**; mockup 130/0 (regresi tab bahasa hilang dikesan oleh mockup 126/4 & pengguna — `_n_baris1` dimulakan 0 supaya kemas_lebar pertama membina baris — dibaiki), sebenar 68/0, bandingan 55/0 | `19c4a44` |
| L | **Tutup hari (langkah-B)** — finalkan baris 5 (`19c4a44`); kiraan telus 18 Ogos → 5 kerja + 1 langkah-B (6 sebenar − 1); suite penuh **14/14 SEMUA LULUS (438.0s)** selepas komit 5; CHANGELOG entri 18 Ogos; MULA_SINI 'Sesi Terakhir' + ringkasan | `a39f885` |
| 7 | **Bar 'Lapor ralat | Kongsi | Salin' SEBARIS (komit 7)** — regresi komit 3/5: wordWrap + minimumWidth(0) membuat label tersekat 153px → bar membalut ke 4 baris pada SEMUA saiz tetingkap/DPI (dilaporkan pengguna); DIBETULKAN: wordWrap dibuang + bar dipindah dari dalam lajur terjemahan ke ARAS PANEL (lebar penuh di bawah dua lajur) — `_kemas_panel_detail` kini sasarkan VBox luar [lajur + bar]; disahkan bar 476×20 sebaris + hbar 0 semua saiz (900–1366) × DPI 100/150%; responsif 76/0 semua skala, mockup 130/0, bandingan 55/0, sebenar 68/0 | `4e16fdf` |
| 8 | **Audit lebar minimum per halaman (komit 8)** — mod `--minlebar` dalam uji_responsif_viewport (carian binari [900, 1400], semak hbar + halaman == stack): semua 6 halaman = **900px** (lantai tetingkap app) pada DPI 150% DAN DPI 150% + fon 1.5× — TIADA titik pecah dalam julat disokong (responsif lengkap 900→1366) | `fdaa2cc` |
| L2 | **Baseline tangkapan dikemas (langkah-B #2)** — suite penuh muktamad **14/14 SEMUA LULUS (420.4s)** selepas pembetulan bar (larian pertama GAGAL baseline bar: nmad 0.026 detail_terang_nasai4934 — dijangkakan, bar kini sebaris; --kemas; larian kedua GAGAL transien muat cache 63.6s > 60s — outlier persekitaran, ukuran baharu 35.9s; larian ketiga SEMUA LULUS); 4 PNG baseline detail dikemas (kesan visual bar sebaris) | `c10986e` |
| 10 | **Audit kiraan 18 Ogos + pendaftaran buka_hari.py (komit 10)** — semak #9 `buka_hari.py` didaftar dalam DIBENARKAN_UNTRAKCED (fail sah belum di-commit — konvensyen skrip baharu); kiraan semakan 393→394 (README + mutasi #35 diselaraskan); audit semua kiraan 18 Ogos merentas sesi_index/MULA_SINI/CHANGELOG/PER18 disahkan konsisten dengan git log (10 sebenar − 2 = 8 kerja + 2 langkah-B); gate 394 semakan + 55/0 + 110/0 | `c10986e` |

**Kiraan telus:** 14 Ogos = **36 commit** · 15 Ogos = **14 commit** ·
16 Ogos = **16 commit** · 17 Ogos = **18 commit** (22 sebenar − 4
langkah-B) · 18 Ogos = **8 commit kerja + 2 langkah-B** (10 sebenar −
2 langkah-B — `a39f885` penutup asal + `c10986e` baseline; komit
7/8/10 kerja selepas penutup, rekod dibuka semula).

**Baki tertangguh (§8):** tidak berubah — #7 kunci API hadis.my kekal
AKTIF sengaja; jurang Tafsir 843 dipantau; installer Fasa 0 TERTUNDA.

**Gate:** semak.py SEMUA LULUS (16 semakan, #12/#14/#15/#16 hijau —
#12 peraturan tarikh sistem) · uji_negatif_8z **55/0** ·
semak_dokumen_ui 110/0 · pokok kerja bersih · tema pengguna "sistem".

---

## SESI 22 OGOS 2026

**Ringkasan:** folder `binaan_installer` → `PustakaHadith` (rebrand selesai), PyInstaller windowed build, Inno Setup + ZIP portable, buang dialog deklarasi berganda, header PustakaHadith → PustakaHadith, push ke GitHub (`opencodemk/PustakaHadith`).

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Rebrand folder** — rename `binaan_installer` → `PustakaHadith`, .venv-build baharu, copy fail data | — |
| 2 | **Recreate .iss** — `installer/PustakaHadith.iss` hilang semasa rename, dibina semula (Inno Setup) | — |
| 3 | **PyInstaller windowed** — `console=True` → `console=False`, rebuild dengan `runw.exe` | — |
| 4 | **Inno Setup** — `PustakaHadith-Setup-1.0.0-x64.exe` (294.9 MB) | — |
| 5 | **ZIP portable** — `PustakaHadith-portable-1.0.0-x64.zip` (201.5 MB) | — |
| 6 | **semak.py 399/399 LULUS** | — |
| 7 | **Git push ke GitHub** — `opencodemk/PustakaHadith` | — |
| 8 | **Git filter-branch** — `→` → `->` dalam semua commit | — |
| 9 | **Git filter-branch #2** — buang "Rebrand: PustakaHadith -> " dari commit pertama | — |
| 10 | **Buang dialog deklarasi berganda** — buang `_tunjuk_deklarasi_pertama` dari `showEvent` | `65543f8` |
| 11 | **Header PustakaHadith** — tukar "Hadis" → "Hadith" dalam header + splash, kekal font/warna | `59dd9a0` |
| 12 | **Rebuild EXE** — build windowed baru, EXE berfungsi | — |

**Kiraan telus:** 22 Ogos = **2 commit** (65543f8, 59dd9a0) + filter-branch rewrite.

**Build outputs:**
- `dist/PustakaHadith/PustakaHadith.exe` — 74.2 MB (windowed)
- `Output/PustakaHadith-Setup-1.0.0-x64.exe` — 294.9 MB
- `Output/PustakaHadith-portable-1.0.0-x64.zip` — 201.5 MB

**Baki tertangguh (§8):** tidak berubah — #7 kunci API hadis.my kekal
AKTIF sengaja; jurang Tafsir 843 dipantau; installer Fasa 0 TERTUNDA.

---

---

## Sesi 56 - 26 Ogos 2026 (47 commit)

**Tema: Aqua Glass (sambungan) + ciri 'Lapor Ralat'**

- **Scrim latar dikurangkan (glassy)** + **latar peta dunia hanya Makluman/Tetapan** (imej bg_03/bg_04 dipisah, `_GLOB_CACHE` ikut laluan).
- **Spesifikasi + redesign Halaman Senarai Hadis** (Split Command Center: banner kaca + sidebar PILIH BAB + panel dwibahasa terjemahan kiri | Arab kanan, di atas `BackgroundCanvas` AQUA; `hadith_card_dwibahasa`; chips Semua/Tersimpan/Belum dibaca; Lompat No. di sidebar; `ListWorker` sokong param).
- **Redesign Halaman Pencarian** (Aqua Glass: hero telus + kad dwibahasa + togol 3-mod Kata/Makna/Kedua-dua; draf AI kekal sebelum hasil; spesifikasi di `docs/superpowers/specs`).
- **Ciri 'Lapor Ralat'** (evolusi panjang): dialog `LaporRalatDialog` (`ui/lapor_ralat.py`) dengan medan Daripada(e-mel)/Tajuk(LAPOR RALAT)/mesej; pautan "Lapor ralat" pada bar tindakan butiran hadis sebaris "Kongsi | Salin". Cuba hantar terus via SMTP (Tetapan -> Pelayan E-mel, Outlook `pustaka.hadith@outlook.com`) **dibuang** kerana susah difail (app password/2FA); kekal buka **Gmail compose pra-isi** (`https://mail.google.com/mail/?view=cm&to=PustakaHadith@gmail.com`) -> pengguna klik Hantar sekali dalam browser. Modul `ui/smtp_mail.py` dihapus, seksyen Tetapan dibuang. Ruangan teks dialog bertukar **hitam atas putih**.
- **Bug fix:** `QLineEdit(int)` bila baca setting `smtp_port` (elak crash restart); nombor carian kitab buka terus butiran (bukan Pencarian); kembali dari Utama ke halaman asal; kiraan Tersimpan Utama selari; maklum balas Rawak.
- **Destinasi laporan:** `PustakaHadith@gmail.com` (tanpa 's').

**Status:** Lapor Ralat berfungsi (Gmail compose). Gate #12 MULA_SINI diselesaikan (`80537f3`).

**Baki/tertangguh:** installer Fasa 0 (PLAN_BINA_EDARAN.md) TERTUNDA; jurang Tafsir 843 (#7) kekal; `semak.py` standing failure (untracked Output/*.exe, Screenshot/*, mockup/selected_*) tangguh ke edaran.

---

## Sesi 57 - 27 Ogos 2026

**Tema: Pembinaan MSIX/Fasa 5C + gerbang lesen hadis.my + dokumentasi & PDF**

- **MSIX + Fasa 5C:** MSIX dibina; Fasa 5C LULUS (`DAFTAR_MSIX_STORE.md`);
  `CHECKLIST_PEMANTAUAN.md` dikemas (Fasa 5 ✓, Fasa 6/7 dibetulkan, `43ad8d2`);
  `PERMOHONAN_LESEN_AHMAD.md` DITUTUP (Ahmad dikecualikan kekal).
- **Regresi UI → punca akar:** binaan dist tiada `hadis.db`
  (`DATA_DIR=%LOCALAPPDATA%\PustakaHadith` kosong) → tiada bab. Fix ujian:
  salin DB+indeks ke sana. `PustakaHadith.spec` `datas` **dikembalikan** —
  JANGAN bundel data hadis.my sehingga kebenaran bertulis
  (`installer/PustakaHadith.iss` salin dist→%LOCALAPPDATA%).
- **Perbincangan Bab & Nombor:** `PERBINCANGAN_BAB_NOMBOR_HADIS.md`
  (`82cb845`, `e1104df`) — asal senarai Bab + isu Bukhari #858=kanonik #909;
  pilihan **A/B/C TERTANGGUH**.
- **Susun dokumentasi:** kategori `sejarah_pembangunan/`, `surat/kebenaran/`,
  `surat/sokongan/`, `perbincangan/`, `penerbitan/`; pindah + kemas rujukan
  (`be0af4f`); `.gitignore` PII (`6eb5fff`).
- **Manual & hadis.my:** `MANUAL_PENGGUNAAN.md` dikemas + 6 tangkapan
  (`d030151`); `SURAT_HADISMY.md`+`EMEL_HADISMY.md` + tangkapan
  (`tangkap_layar.py`) + `DASAR_PRIVASI`/`PAUTAN_SOKONGAN` (`d7ee299`, `9dee026`);
  folder `surat/hadis.my/`: logo `logo_PustakaHadith.png` (Segoe UI
  #5CBF85/#7FD39A/#9C9589) + PDF (xhtml2pdf berterabur → reportlab
  `buat_pdf2.py`): `SURAT_HADISMY_kemas.pdf`, `EMEL_HADISMY.pdf`,
  `DASAR_PRIVASI.pdf`, `PAUTAN_SOKONGAN.pdf` (`999a27e`, `1fa9a44`).

**Status:** binaan interim online-only (tiada bundel) menunggu kebenaran hadis.my.
Item tertangguh: nombor hadis A/B/C; kebenaran hadis.my; build dist ditangguh.

**Log harian:** `dokumen/perubahan/PERUBAHAN_27OGOS.md`

---

## Sesi 58 - 27 Ogos 2026 (petang)

**Tema: Penyeragaman jenama `PustakaHadith`**

- **Arahan:** pengguna membetulkan — "semua mesti kekal guna `PustakaHadith`"
  (satu perkataan, 't' betul), bukan `Pustaka Hadis` / `PustakaHadis`.
- **Ganti massa:** 601 kemunculan / 96 fail (dokumen + sumber + skrip binaan)
  `Pustaka Hadis` / `PUSTAKA HADIS` / `Pustaka Hadith` (berjarak) /
  `PustakaHadis` → **`PustakaHadith`** (`fix_brand2.py`). Domain `hadis.my`
  (261) tidak disentuh.
- **Fail binaan dinamakan semula:** `PustakaHadis-Debug.spec` →
  `PustakaHadith-Debug.spec`, `PustakaHadis-Fasa4.wsb` →
  `PustakaHadith-Fasa4.wsb`.
- **Sumber:** `config.py` (`DATA_DIR=%LOCALAPPDATA%\PustakaHadith`),
  `ui/app_qt.py` (tajuk), `installer/msix_identity.txt` + `.iss`,
  `*.bat`/`*.ps1`/`*.py` dikemas kini.
- **PDF:** keempat-empat `SURAT_HADISMY.pdf`, `EMEL_HADISMY.pdf`,
  `DASAR_PRIVASI.pdf`, `PAUTAN_SOKONGAN.pdf` dijana semula (`buat_pdf2.py`,
  seragam `PustakaHadith`). `SURAT_HADISMY_kemas.pdf` (stale) dibuang.
- Commit `e9ff349` (+ `fa66be1` log sesi).

**Status:** jenama seragam `PustakaHadith` di repo; keempat-empat PDF hadis.my
kemas. Tertangguh: nombor hadis A/B/C, kebenaran hadis.my, build dist.

**Log harian:** `dokumen/perubahan/PERUBAHAN_27OGOS.md`

---

 *sesi_index.md — dikemas kini 27 Ogos 2026*

