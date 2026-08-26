# MULA SINI — baca sebelum menyentuh kod

> Untuk sesi AI baharu **dan** untuk diri sendiri selepas berehat lama.
> `dokumen/sesi/sesi_index.md` (865 baris) ialah arkib penuh. Dokumen ini ialah
> perkara yang benar-benar berulang.
> Log perubahan versi ringkas mengikut tarikh: `dokumen/perubahan/CHANGELOG.md`;
> log harian terbaru: **22 Ogos 2026** (rebranding PustakaHadith + GitHub push).
> Log folder binaan installer: `dokumen/perubahan/PERUBAHAN_20OGOS.md`
> (Fasa 1 — pisahkan laluan data; folder `binaan_installer` bukan git).
> Panduan Mula Cepat untuk pengguna: `dokumen/manual/MULA_CEPAT.md`.
> Transformasi paparan detail LAMA → BARU (dengan tangkap layar):
> `dokumen/manual/TRANSFORMASI_DETAIL.md`.
> Semua dokumen diasingkan dalam `dokumen/` mengikut jenis: `manual/`,
> `perubahan/`, `sesi/`, `audit/`, `rujukan/`. Peta penuh: §12
> `dokumen/manual/MANUAL_REFERENSI_DEV.md`.

---

## Keadaan projek — ringkasan satu muka (akhir 26 Ogos 2026)

**Apa ini:** Aplikasi desktop **PustakaHadith v1.0** — PyQt5, berjalan
sepenuhnya di luar talian selepas sync: **62,169 hadis** (9 kitab
hadis.my), carian kata kunci FTS5 + carian makna AI, 3 tab bahasa,
5 tema (Aqua lalai + Neutral gelap/terang + Kertas gelap/terang),
susun atur RTL.

**Status: SIAP & DISAHKAN** — suite rasmi **14/14 SEMUA LULUS**
· `semak.py` SEMUA LULUS (**395 semakan**) ·
`uji_negatif_8z` 55/0 · `semak_dokumen_ui` 109/0 · pokok kerja bersih ·
**19 commit** pada 26 Ogos (glassy scrim + latar dunia Makluman/Tetapan +
spec Senarai Hadis + Senarai Hadis dwibahasa + Pencarian Aqua Glass +
fiks dedupe carian + fiks klik kad + latar glob seragam API/Tentang/Detail
+ halaman Tersimpan diubah suai + fiks kelipan Senarai Hadis + tab Simpan
& Sejarah + tarikh simpan & navigasi Kembali + isi semula tarikh lama +
kotak semak buang pukal sejarah + kilat chip aktif + tarikh dibaca sejarah
+ fiks kembali dari Utama + kiraan Tersimpan Utama selari + maklum balas
Rawak).

**Kerja 26 Ogos (19 commit):** glassy scrim glob (`bb5a912`); latar peta
dunia Makluman + Tetapan sahaja (`eaf6f07`); spesifikasi Senarai Hadis
(`629ac49`); Halaman Senarai Hadis diubah suai — banner + sidebar PILIH
BAB + panel dwibahasa atas BackgroundCanvas glob AQUA (`[hadapan ini]`);
Halaman Pencarian diubah suai — BackgroundCanvas glob + kad dwibahasa +
togol kaedah carian Kata kunci/Makna/Kedua-dua (`4f1de4d`); fiks dedupe
carian keyword `hadis_id`→`id` supaya SEMUA hasil dipapar (`319787f`);
fiks klik kad carian/kitab — lambda sepadan isyarat `ClickCard.clicked`
(0 arg) (`d157235`); latar glob **dunia** (`BackgroundCanvas(dunia=True)`,
sama seperti Tetapan) untuk dialog Tetapan API, dialog Tentang, dan
halaman Detail (`360c74b`); halaman **Tersimpan (bookmark)** diubah suai
— glob garisan masa (sama Carian/Senarai), hero telus, kad dwibahasa +
togol 🔖 buang terus dari halaman (`6ab1f5a`); fiks kelipan Senarai
Hadis — butang 🔖 pada kad tidak lagi muat semula seluruh halaman
(`_load_kitab_page`) yang mengosongkan senarai + putar ListWorker semula
(~1 saat kelipan glob), sebaliknya kemas SATU kad di tempatnya (`52e83b2`); tab **Simpan &
Sejarah** pada halaman Tersimpan — bahagian "Telah dibaca" ambil
`read_history()` dan papar sebagai kad dwibahasa (klik 🔖 simpan terus,
`open_by_ref` buka detail), togol tab `filterChip` (`4546090`); pada
bahagian **Tersimpan**, setiap kad papar **tarikh disimpan** di sebelah
nama + nombor hadis (`hadith_card_dwibahasa` terima `tarikh_simpan`,
format `_fmt_tarikh_simpan`), dan `open_by_ref` terima `from_page` supaya
butang **Kembali** detail pulang ke halaman asal — `BACK_PETA["saved"]`
→ `go("saved")` (`03674bc`).
Kerja 25 Ogos kekal (halaman utama AQUA + rak kitab).

**Kerja 22 Ogos:** Rebranding lengkap **Pustaka Hadis → PustakaHadith** —
update 40+ fail Python (main, ui/*, config, sync_*, test_*), installer
(.iss, .spec), README.md (section Pemasangan pengguna akhir), dokumen
surat (emel rasmi Outlook/Gmail/Proton). Rename file: `PustakaHadis.iss`
→ `PustakaHadith.iss`, `PustakaHadis.spec` → `PustakaHadith.spec`.
Build baharu: `PustakaHadith.exe` (89 MB), `dist\PustakaHadith\` (1.36 GB),
`PustakaHadith-Setup-1.0.0-x64.exe` (0.27 GB),
`PustakaHadith-portable-1.0.0-x64.zip` (0.47 GB). Uji EXE launch 8s OK.
GitHub push: `https://github.com/opencodemk/PustakaHadith`. semak.py
**395/395 LULUS**.
terang; Kertas/Terang/Ikut sistem dibuang) + buang 'Saiz antara muka'
dari panel Tetapan (`b292515`) · dialog disclaimer baharu
(ui/disclaimer.py) papar setiap larian + carian nombor hadis buka detail
terus · disclaimer selepas model + tajuk splash/disclaimer/header
sepadan (`e6d867b`) · fix disclaimer pythonw.exe —
`setQuitOnLastWindowClosed(False)` + papar sebelum splash (`6c9f855`) ·
Tentang Pustaka Hadis QTableWidget 2 lajur (Kandungan + Sumber dan
atribusi) (`5dd6990`) · **baiki gate: semak.py semakan atribusi
diselaraskan ke format jadual Tentang + kiraan semakan 394
(README, MULA_SINI, mutasi #27/#30/#34/#35/#36) + PERUBAHAN_19OGOS.md
dicipta**.

**Kerja 18 Ogos (8 commit):** buka rekod hari — finalkan baris
langkah-B keempat (`6f8f1b8`) dalam sesi_index + PERUBAHAN_17OGOS ·
seksyen SESI 18 OGOS + kiraan telus · PERUBAHAN_18OGOS.md baharu ·
'Sesi Terakhir' + ringkasan → 18 Ogos · mutasi #27/#30/#34/#36
disasarkan semula. · **audit konvensyen langkah-B (komit 2)** —
16 Ogos dibetulkan ke "18 sebenar − 2 langkah-B" (`f8dd057` +
`2cb76b8`); 14/15/17 Ogos disahkan konsisten. · **ujian responsif
viewport penuh + pembetulan tajuk responsif detail (komit 3)** —
`uji_responsif_viewport.py` baharu; panel dua lajur tidak lagi
melimpah pada saiz kecil/DPI 150% (`_kemas_tajuk_detail` dua baris +
bar teks membalut). · **suite rasmi 14 ujian (komit 4)** —
`uji_responsif_viewport` didaftar sebagai ujian #14; DPI 125%/175%
76/0; suite penuh **14/14 SEMUA LULUS (465.3s)**. · **audit fon
besar (komit 5)** — bungkusan tab/butang responsif + reflow
tertangguh; semua 5 skala fon + DPI 100–175% = 76/0. · **tutup hari
(langkah-B)** — suite penuh **14/14 SEMUA LULUS (438.0s)**; kiraan
telus → 5 kerja + 1 langkah-B. · **bar 'Lapor ralat | Kongsi | Salin'
sebaris (komit 7)** — wordWrap dibuang + bar di aras panel (lebar
penuh); sebaris 476×20 semua saiz/DPI. · **audit lebar minimum
(komit 8)** — mod `--minlebar`: semua 6 halaman 900px (lantai) pada
DPI 150% + fon 1.5×. · **audit kiraan + pendaftaran
buka_hari.py (komit 10)** — semak #9 `buka_hari.py` didaftar dalam
DIBENARKAN_UNTRAKCED (fail sah belum di-commit — konvensyen skrip
baharu); kiraan semakan 393→394 (README + mutasi #35 diselaraskan);
semua kiraan 18 Ogos merentas sesi_index/MULA_SINI/CHANGELOG/PER18
disahkan konsisten dengan git log (10 sebenar − 2 = 8 kerja + 2
langkah-B).

**Kerja 17 Ogos (18 commit, sebelum ini):** penutup 16 Ogos (grid 3×3
kad 114px + border 9 kitab) · galeri 5 tema + ujian DPI · **pepijat
viewport tersekat dibaiki** (`_paksa_saiz_halaman`, 24/24) · optimum
uji_visual_sebenar 143→72s · semak kiraan suite (README 377→391→392) ·
MULA_CEPAT pengguna (5 tema + galeri + responsif + §4) · CHANGELOG
log versi seiring · ringkasan keadaan + pembetulan kiraan + audit
konsistensi rentas dokumen · tekanan uji_visual_sebenar 5 larian 68/0
(sifar flak) · **semak #16 kiraan semakan automatik + peraturan
tarikh sistem dalam #12** (393 semakan, uji_negatif 55/0 — 36
cabang) · **suite muktamad 13/13 SEMUA LULUS (387.5s)** + tutup
hari.

**Ciri dikunci — jangan ubah tanpa sebab:**

- **5 tema, semua ≥ WCAG AA** (semak #13, 72 pasangan warna): 🌙
  Neutral (lalai) · 📜 Kertas · ☀ Neutral terang · ☀ Terang · 🌓
  Ikut sistem (ikut mod Windows, QTimer 2s — flip hidup bertukar 1.0s)
- **Susun atur RTL** — Arab di **KANAN**, terjemahan di **KIRI**
  (semakan geometri: arab x > terjemahan x; `6b853f0`)
- **3 tab bahasa** — Melayu | Indonesia | English; terjemahan English
  31,833 (98%, padanan ara-* 1,628 pengisi celah); teks SAMA PARAS
  dengan Arab (AlignTop)
- Bar teks `Lapor ralat | Kongsi | Salin` (bukan butang) + menu Salin
  3 pilihan (Arab / terjemahan semasa / Arab + terjemahan semasa) +
  justify semua teks rumi + panel transliterasi di atas
- Huraian SemakHadis (4,237 hadis BM) + darjat (63,930) + syarah
  klasik Arab — collapsible TERBUKA selepas tab bahasa
- Lompat terus ke hadis (`bukhari 433` / `B433` / `Ctrl+G`), butang ↑
  terapung, Kongsi WhatsApp ikut bahasa semasa, selawat ﷺ, splash
- Halaman utama mockup ② — kad 114px 3×3, border keliling warna kitab
  + hover cerah/gelap + glow ikut warna + hover timbul (16–17 Ogos);
  pembetulan viewport `_paksa_saiz_halaman` (halaman tidak lagi
  terpotong 640×480); paparan responsif 1024×600 + DPI 150%

**Data (disahkan 14 Ogos):** sync penuh dari mula — 62,169 sejajar
API (622 muka surat, 45/45 padan teks), 0 duplikat, id kontigu, FTS5
sejajar; `sync_english.py` 31,833 deterministik; audit bebas padanan
30,541/30,547 (100.0%).

**Baki tertangguh (§8):** hanya **#7 kunci API hadis.my** — kekal
AKTIF sengaja (sync jalan pada mesin pengguna; kunci tidak dalam
repo). Siasatan tafsir BM: tiada sumber per-hadis terbuka menutup
jurang Tafsir 843 (pantau MyHadith JAKIM + IslamHouse Melayu).
**Keputusan pengguna 19 Ogos:** #7 kunci API dan jurang Tafsir 843
**diabaikan buat masa ini** (kekal direkod sebagai tertangguh);
tumpuan seterusnya = installer (Fasa 0, `PLAN_BINA_EDARAN.md`).

**Gate sebelum commit:**

```
python gate_pantas.py      # ~35s — semak.py + uji_negatif_8z + pokok bersih
python uji_pra_hantar.py   # suite penuh 14 ujian (~7 minit, log bukti_visual/)
```

**Jangan lupa:** peraturan §1 (tiada tkinter, tiada arabic-reshaper,
CRLF .bat, dsb.) · corak pepijat §2 · fakta API/hadis.db §4 ·
selepas selesai, bahagian 'Sesi Terakhir' di bawah DAN ringkasan ini
MESTI dikemas (semak #12 + #15 akan GAGAL jika tidak).

**Pautan dokumen:** pengguna — `dokumen/manual/MULA_CEPAT.md` ·
`dokumen/manual/MANUAL_PENGGUNAAN.md` · `dokumen/manual/MANUAL_INSTALASI.md`
· transformasi paparan — `dokumen/manual/TRANSFORMASI_DETAIL.md` ·
audit — `dokumen/audit/AUDIT_SEMAKHADIS.md` ·
`dokumen/audit/SIASATAN_TAFSIR_BM.md` · log harian —
`dokumen/perubahan/PERUBAHAN_19OGOS.md` · arkib penuh —
`dokumen/sesi/sesi_index.md`.

---

## Sesi Terakhir — 26 Ogos 2026 (9 commit)

Versi semasa: **v1.0**. Kerja 26 Ogos — **19 commit** (glassy scrim +
latar dunia Makluman/Tetapan + spesifikasi + redesign halaman Senarai
Hadis):

1. **Scrim latar dikurangkan (glassy)** (`bb5a912`) — alpha glob 150→85,
   gradient 200→120; glob lebih jelas menembusi panel kaca pada Utama/
   rak/Makluman/Tetapan. Teks kekal terbaca (imej asas navy gelap).

2. **Latar peta dunia: Makluman + Tetapan SAHAJA** (`eaf6f07`) — imej
   `latar_globe_dunia.png` (bg_03 daripada pengguna) dipakai pada
   dialog Makluman (`BackgroundCanvas(dunia=)`) dan panel Tetapan sahaja;
   Utama/rak kekal `latar_globe_timeline.png` (bg_04). `_GLOB_CACHE`
   ikut laluan imej; `lukis_latar_dunia()` baharu.

3. **Spesifikasi Senarai Hadis** (`629ac49`) —
   `docs/superpowers/specs/2026-08-26-halaman-senarai-hadis-design.md`.

4. **Halaman Senarai Hadis diubah suai** (`[hadapan ini]`) — susun atur
   Split Command Center: banner kaca + sidebar KITAB SEMASA/PILIH BAB
   (senarai buku + kiraan dari `get_bab_list`) + panel senarai dwibahasa
   (terjemahan kiri | Arab kanan, `hadith_card_dwibahasa`), di atas
   `BackgroundCanvas` glob AQUA. Chips berfungsi: Semua / Tersimpan
   (tanda buku) / Belum dibaca (sejarah) + togol Nombor ↓/↑. Carian
   banner buka Pencarian tertapis kitab; Lompat No. dipindah ke sidebar
   (Ctrl+G kekal). API: `get_bab_list` + `get_hadis_list(book/order/
    ids/exclude_ids)` + `ListWorker` sokong param.

5. **Halaman Pencarian diubah suai** (`4f1de4d`) — gaya Aqua Glass: akar
   `BackgroundCanvas` glob AQUA (hero telus) + kad hasil dwibahasa
   (`hadith_card_dwibahasa`, terjemahan kiri | Arab kanan, butang 🔖
   simpan) di atas `BackgroundCanvas`. Togol kaedah carian 3-mod **Kata
   kunci / Makna / Kedua-dua** (lalai, disimpan `carian_mod` ke
   `user_settings.json`); mod `kata` melangkau semantik, `makna`
   melangkau keyword. Draf jawapan AI kekal sebelum hasil (mod Makna/
   Kedua-dua). Spesifikasi:
   `docs/superpowers/specs/2026-08-26-halaman-pencarian-design.md`.

6. **Fiks dedupe carian keyword** (`319787f`) — `search_hadis` pulang `id`
   (bukan `hadis_id`), maka kunci dedupe `(collection, hadis_id)` sentiasa
   `None` → hanya 1 kad setiap koleksi dipapar (cth. "riba" 20 hasil jadi
   7). Guna `hadis_id or id` supaya SEMUA 20 hasil setiap halaman dipapar.
   Bug ini juga menjejaskan kad lama (hadith_card) sebelum ubah suai.

7. **Fiks klik kad** (`d157235`) — `ClickCard.clicked` ialah `pyqtSignal()`
   (0 arg), tetapi lambda sambungan guna param wajib `lambda _, hh=h:`
   (carian) dan `lambda _, bk=book:` (senarai kitab). Klik mana-mana kad
   → `TypeError: missing 1 required positional argument: '_'` → apl
   terus keluar. Betulkan ke `lambda hh=h:` / `lambda bk=book:` (param
   ada nilai lalai). Disahkan: klik kad carian & baris kitab tiada lagi
   pecah (CRASH LIST: NONE, `_detail_from='search'`). Senarai Hadis
   (`lambda hh=h:`, baris 516) sudah betul sejak mula.

8. **Latar glob seragam** (`360c74b`) — dialog **Tetapan API**
   (`ApiDialog`), dialog **Tentang** (`DeklarasiDialog`), dan **halaman
   Detail** (`PagesDetail._page_detail`) dibalut `BackgroundCanvas(
   dunia=True)` supaya latar sama dengan panel Tetapan (peta dunia AQUA;
   pepejal pada tema lain). Sebelum ini ketiga-tiganya guna latar
   pepejal (`HEADER_BG`/`PAGE_BG`). Scroll & body detail dibuat telus
   (`detailScroll`/`detailBody`) supaya glob kelihatan. Disahkan offscreen:
    ketiga-tiga mengandungi `BackgroundCanvas`, detail render dengan data
    sebenar tanpa ralat.

9. **Halaman Tersimpan (bookmark)** (`6ab1f5a`) — dibalut `BackgroundCanvas()`
   (glob **garisan masa**, sama Carian/Senarai — bukan glob dunia seperti
   Tetapan) supaya seragam dengan halaman kandungan lain. Hero dibuat telus
   (`QFrame#hero { background: transparent }` bila `ada_latar_imej()`), kad
   lama `hadith_card` diganti `hadith_card_dwibahasa` (Arab+Melayu), dan
   togol 🔖 kini membuang/masuk semula tanda buku terus dari halaman
   (`_bookmark_toggle` → `_toggle_save` → `_render_saved`). Fix susulan:
   lambda `simpan_clicked` guna param pendahulu `_` supaya arg bool butang
   tidak menulis ganti `slug` (bug senyap — togol tambah dan bukannya buang).
   `_toggle_save` dijamin dengan `getattr(self, "_save_btn", None)` supaya
   selamat dipanggil dari halaman lain (tiada butang detail). Disahkan
   offscreen: 3 tanda buku → 3 kad dwibahasa; togol 🔖 → 2 kad + 2 bookmark.

10. **Fiks kelipan Senarai Hadis** (`52e83b2`) — butang 🔖 pada kad
   (`_kitab_toggle_simpan`) asal memanggil `_load_kitab_page` yang
   mengosongkan senarai lalu memutar `ListWorker` semula (~1 saat kelipan
   glob). Diganti: kemas SATU kad di tempatnya (tukar `objectName`
   `simpanChip`↔`simpanChip_aktif` + `unpolish/polish`); bila penapis
   "tersimpan", buang kad itu dari senarai. `_load_kitab_page` langsung
   TIDAK dipanggil. Disahkan offscreen: 2 kad kekal 2, butang flip, 0
    muat semula; penapis tersimpan: 2→1 kad, 0 muat semula.

11. **Tab Simpan & Sejarah** (`4546090`) — halaman Tersimpan diberi togol
    dua tab: **Tersimpan** (penanda buku, `_render_bookmarks_simpan`) dan
    **Telah dibaca** (`_render_sejarah_simpan`). Bahagian sejarah ambil
    `read_history()` lalu `api.get_hadis_by_id(slug, n)` untuk setiap
    entri, dipapar sebagai kad dwibahasa sama; klik 🔖 simpan/masuk
    terus, klik kad `open_by_ref` buka detail. Label tab & sub-tajuk
    dikemas dengan kiraan (`_kemas_tab_simpan`). Nav "Tersimpan"
    ditukar "Simpan & Sejarah". Disahkan offscreen: tab Simpan 3 kad,
    tab Baca 10 kad (sejarah sebenar), tukar tab + klik/kunci 🔖 tiada
    ralat.

12. **Tarikh simpan + navigasi Kembali** (`03674bc`) — bahagian **Tersimpan**
    papar **tarikh disimpan** di sebelah nama + nombor hadis: `_toggle_save`
    simpan `saved_at` (ISO) bila simpan; `hadith_card_dwibahasa` terima
    `tarikh_simpan` dan tambah `· disimpan <DD Bulan YYYY>` (helper
    `_fmt_tarikh_simpan`); kad disusun mengikut `saved_at` terkini dulu.
    Butang **Kembali** pada halaman detail pulang ke halaman asal: `open_by_ref`
    terima `from_page` (pemanggil Tersimpan hantar `"saved"`, Carian
    `"search"`), lalu `BACK_PETA["saved"]` → `go("saved")`. Bonus: buang/
    simpan dari tab **Telah dibaca** kini bawa data hadis penuh supaya kad
    tersimpan ada teks. Disahkan offscreen: meta kad = "Sunan Abu Daud 2906
    · … · disimpan 26 Ogos 2026"; `_detail_from` = "saved" (Kembali →
     halaman simpan), kekal bila buka hadis seterusnya.

13. **Isi semula tarikh simpan lama** (`234b2ef`) — penanda buku disimpan
     SEBELUM ciri `saved_at` wujud tiada rujukan masa. `backfill_saved_at`
     (helpers.py) dijalankan sekali pada permulaan (`app_qt.py`): isi
     `saved_at` yang hilang dengan *mtime* fail `bookmarks.json` sebagai
     anggaran; tulis semula bila berubah. Hadis simpan BAHARU kekal guna
     `datetime.now()`. Idempoten. Disahkan: lama dapat mtime, baru kekal,
     backfill kedua tiada ubah; boot app semua penanda ada `saved_at`.

14. **Kotak semak buang pukal (Telah dibaca)** (`42ef681`) — bahagian
     **Telah dibaca** (`_render_sejarah_simpan`) dapat bar kawalan:
     `☐ Pilih semua` + butang `🗑 Buang dipilih (N)` (lumpuh bila N=0).
     Setiap kad dibalut baris `[☐][kad]`; tanda semak dikira ke N dan
     `Pilih semua` segerak. `helpers.remove_reading(slug, n)` buang
     ikut `(slug, n)`; `_sejarah_buang_pilih` panggil untuk setiap
     pilihan lalu `_render_saved` semula. Klik kad masih buka detail
     (☐ berasingan). Disahkan offscreen: 14 entri→14 ☐, tick 2→butang
     "(2)" aktif, Pilih Semua→"(11)", buang panggil `remove_reading` 11×.

15. **Kilat chip aktif (bukan teks hitam)** (`f77506e`) — `filterChip_active`
     (theme.py) tukar `color: PAGE_BG` (hitam, mengelirukan) kepada
     `#ffffff` + sempadan `TEAL_GLOW`. Chip aktif kini teal penuh + teks
     putih jelas. Objek nama ini dikongsi tab Tersimpan/Telah dibaca DAN
     togol Arab/Transliterasi + mod Pencarian di **halaman detail**, jadi
     satu pembetulan QSS membaiki kedua-dua tempat (permintaan "buat juga
     pada detail page").

16. **Tarikh dibaca + buang butang Simpan (sejarah)** (`67e9271`) — pada
     bahagian **Telah dibaca**: (a) `record_reading` kini simpan `read_at`
     (ISO); `backfill_reading_at` (helpers.py, sama corak `backfill_saved_at`)
     isi `read_at` lama dengan mtime fail pada permulaan (`app_qt.py`); kad
     papar `· dibaca <DD Bulan YYYY>` guna `tarikh_label="dibaca"` pada
     `hadith_card_dwibahasa`; (b) butang 🔖 **disembunyikan** (`c.simpan_btn
     .hide()`) kerana buang pukal kini guna kotak semak — klik kad masih
     buka detail. Tab **Tersimpan** tidak berubah (🔖 + "disimpan" kekal).
     Disahkan offscreen: 13 kad sejarah, semua `simpan_btn` tersembunyi,
     meta "Sahih al-Bukhari 1 · … · dibaca 26 Ogos 2026".

17. **Fiks kembali dari Utama** (`e19f216`) — klik "Terakhir dibaca" (atau
     pintasan nombor) di halaman Utama buka detail tetapi butang Kembali
     menuju Carian, bukan Utama. Punca: `_buka_hadis_terus` (`pages_carian
     .py`) tetapkan `self._detail_from = dari` BETUL, namun talian
     berikutnya memanggil `open_by_ref(slug, n, "search")` (keras) yang
     menulis semula `_detail_from="search"`. Diubah kepada `open_by_ref
     (slug, n, dari)` supaya sumber sebenar (home/carian) dihormati.
     Disahkan offscreen: `dari="home"` → `_detail_from="home"` →
     `BACK_PETA["home"]`=("Utama","home"); lalai carian kekal "search".

18. **Kiraan Tersimpan Utama selari** (`d247b98`) — badge "Tersimpan" di
     halaman Utama dikira SEKALI pada binaan (`n_simpan = len(self
     .bookmarks)`) dan tidak disegar; bila simpan/buang dari halaman lain,
     kiraan tidak padan dengan tab Tersimpan. Simpan rujukan badge
     (`_kad_tersimpan_badge`) dan segarkan melalui `_kemas_kiraan_home`
     yang dipanggil setiap `_render_sejarah` (go("home")). Disahkan
     offscreen: 3→4→2 sepadan `len(self.bookmarks)`.

19. **Maklum balas Rawak** (`4cdf6c4`) — butang **Rawak** (kad sisi Utama)
     berfungsi tetapi tiada maklum balas semasa `RandomWorker` memuat,
     jadi nampak "tak fungsi". `_random` kini papar toast "🎲 Membuka hadis
     rawak…" (kekal) lalu `RandomWorker`→`_on_random`: buka detail (`from
     ="home"`, jadi Kembali → Utama) dan sembunyi toast selepas jaminan
     paparan minimum 1200ms; kegagalan papar "Tiada hadis rawak dijumpai".
     `import time` ditambah di peringkat modul (sebelum ini hanya import
     setempat dalam `open_by_ref`). Disahkan offscreen: toast kelihatan →
     detail (indeks 2) → toast disembunyi; tiada hadis → toast ralat.

**Kiraan telus:** 26 Ogos = **19 commit**.

**Gate:** semak.py SEMUA semakan kod LULUS (termasuk semakan baharu
halaman Pencarian: BackgroundCanvas + kad dwibahasa + togol `carian_mod`)
· API senarai 12/12 · ujian fungsional `uji_api_senarai.py` (DB memori) ·
ujian mod carian kata/makna (offscreen, routing enjin sah) · ujian berdata
(uji_tukar_tema/uji_pra_hantar) menunggu hadis.db penuh di
persekitaran ini. `uji_visual_kiraan.py` dijangka perlu dikemas
(banner baharu) — jalankan manual selepas sync DB.

---

1. **Buka rekod hari (komit 1, 18 Ogos)** — finalkan baris komit 10
   (`c10986e`) dalam sesi_index; seksyen SESI 18
   74/2 (hbar 133/122) — DIBETULKAN: LangTabs + tab ARAB/TRANSLITERASI
   + butang tindakan kini boleh bungkus ke baris kedua (`kemas_lebar`/
   `_kemas_tab_arab`/`_kemas_butang_tindakan`), panel ketatkan margin
   bila sempit, dan laluan reflow tertangguh (`_kemas_semua_detail`,
   singleShot 0) — punca sebenar: QStackedWidget tidak ubah saiz
   halaman tersembunyi jadi render guna geometri basi; disahkan semua
   5 skala fon @ DPI 150% + DPI 100/125/175% = 76/0, mockup 130/0
   (regresi tab bahasa hilang dikesan & dibaiki), sebenar 68/0,
   bandingan 55/0.

1. **Suite rasmi 14 ujian (komit 4)** — `uji_responsif_viewport.py`
   didaftar sebagai ujian #14 dalam `uji_pra_hantar.py` (7.2s dalam
   suite); semak_dokumen_ui A8 dikemas (14 ujian); QT_SCALE_FACTOR
   boleh ganti + header dinamik — DPI 125%/175% disahkan 76/0;
   dokumen diselaraskan (README, MULA_CEPAT, MANUAL_REFERENSI_DEV,
   MULA_SINI); suite penuh **14/14 SEMUA LULUS (465.3s)**.

1. **Buka rekod hari (komit 1)** — finalkan baris langkah-B keempat
   (`6f8f1b8`) dalam sesi_index + PERUBAHAN_17OGOS; seksyen SESI 18
   OGOS + kiraan telus (1 commit); PERUBAHAN_18OGOS.md baharu;
   'Sesi Terakhir' + ringkasan dikemas; mutasi #27/#30/#34/#36
   disasarkan semula.

1. **Audit konvensyen langkah-B (komit 2)** — bandingkan kiraan
   telus setiap hari dengan git log sebenar: 14 (44 sebenar − 8
   langkah-B), 15 (14 − 0), 17 (22 − 4) konsisten; 16 DIBETULKAN —
   jadual sebelum ini kata "16 sebenar − 0 langkah-B" sedangkan git
   ada 18 komit bertarikh hari itu; `f8dd057` (penutup sementara) +
   `2cb76b8` (rekod border) ditambah sebagai 2 langkah-B →
   18 sebenar − 2 = 16 kerja; baris L dalam sesi_index +
   PERUBAHAN_16OGOS.

1. **Ujian responsif viewport penuh (komit 3)** — uji baharu
   `uji_responsif_viewport.py` (6 halaman × 4 saiz, DPI 150%):
   `_paksa_saiz_halaman` STABIL (halaman == stack, viewport tidak
   640×480, 76/0); ujian mendedahkan panel dua lajur detail
   melimpah (hbar 254) pada 900/1024 — punca: tajuk_bar satu baris
   mahu ~1210px + bar teks 'Lapor ralat | Kongsi | Salin' mahu
   ~476px; pembetulan: tajuk/butang dua baris bila sempit
   (`_kemas_tajuk_detail`) + bar teks boleh membalut; disahkan
   76/0 DPI 150% + DPI 100%, mockup 130/0, sebenar 68/0.

1. **Tutup hari (komit 18)** — suite pra-hantar penuh
   **13/13 SEMUA LULUS (387.5s)** selepas semak #16 (turun dari
   401.8s; uji_visual_sebenar 64.2s dalam suite); semak #12/#15/#16
   hijau selepas komit 17 (`09dc071`); kiraan hari 17 → 18; mutasi
   #34 dikunci ke "18 commit"; semua dokumen diselaraskan (PERUBAHAN
   17OGOS Komit 18 + sesi_index + ringkasan ini). + 1 langkah-B
   (pembetulan rekod tarikh — semua kerja hari ini cdf4e63..8725872
   direkod ikut jam sistem, tiada hari salah label).

1. **Semak #16: kiraan README automatik (komit 17)** — semak.py kini
   mencetak jumlah semakan (**391 semakan, 15 bahagian**) dan semak
   #16 mengesahkan tuntutan kiraan README (GAGAL bila lapuk; lompat
   bila hadis.db tiada); pembilang lulus()/tajuk() ditambah; mutasi
   #35 subproses; uji_negatif 52 → **54/0 (35 cabang)**; README kekal
   391 semakan + 52/0 → 54/0.

1. **Tekanan uji_visual_sebenar 5 larian (komit 16)** — 5 larian
   berturut-turut **68/0 SEMUA LULUS** (105.6–108.3s setiap larian);
   poll stabil disahkan tanpa flak dalam keadaan RDP berbeza (sifar
   kegagalan, 11 tangkapan setiap larian); julat masa 72–108s ialah
   varian persekitaran RDP, bukan poll.

1. **Audit kiraan silang + format (komit 15)** — MULA_SINI/sesi_index/
   PERUBAHAN_17OGOS/CHANGELOG disahkan konsisten; pepijat format
   PERUBAHAN_17OGOS (dua bullet bercantum) dibaiki.

1. **Kiraan hari dibetulkan ke 4 (komit 14)** — blok 'Sesi Terakhir'
   + ringkasan + sesi_index + PERUBAHAN_17OGOS selaras; hash baharu
   095682f/4da64ac/0770ec9 dalam blok (semak #12 top-10); mutasi
   #30/#34 dikunci.

1. **Ringkasan satu-muka 'Keadaan projek' dikemas (`0770ec9`, komit
   13)** — suite muktamad 463.6s → 401.8s (rantaian 485→402s); blok
   kerja dua hari terakhir ditambah; ciri dikunci + mockup ② (kad
   114px, border warna, hover, pembetulan viewport, responsif);
   pautan log harian → PERUBAHAN_17OGOS.md; anggaran suite ~7
   minit. Gate: semak SEMUA LULUS · 52/0 · 110/0.

1. **Buka semula rekod hari (`e60a74d`, komit 12)** — CHANGELOG
   entri 16 Ogos ditambah (log versi tiada jurang); reka bentuk
   mutasi #27/#30/#34; blok 'Sesi Terakhir' dikemas semula.

1. **CHANGELOG log versi seiring (`4da64ac`, komit 11)** — entri
   'Kemas kini' dua hari terakhir ditambah (reka bentuk halaman
   utama + responsif/optimum ujian) supaya log versi seiring log
   harian; kata Indonesia dalam entri baharu dikesan semak 8m dan
   dibetulkan; gate: semak SEMUA LULUS · uji_negatif_8z 52/0 ·
   semak_dokumen_ui 110/0.

1. **Penutup sementara — rekod penuh 8 commit (`095682f`, komit 10)**
   — PERUBAHAN_17OGOS (PENUTUP HARI jadual 8 baris + LANJUTAN 1–5) +
   sesi_index (kiraan telus 8 + jadual penuh) + MULA_SINI
   diselaraskan; mutasi #30/#34 kekal "8 commit"; hari kemudian
   dibuka semula dengan lanjutan.

1. **MULA_CEPAT §4 Penyelesaian masalah + poll stabil + suite 401.8s
   (komit 9)** — §4 baharu 'Penyelesaian masalah (ringkas)' untuk
   pengguna awam (ikon tiada, kunci API, lambat buka, saiz fon, tema
   Ikut sistem, carian kosong); poll tangkapan diperbetulkan ke corak
   stabil (dua grab sama) — elak menyimpan bingkai separa dilukis
   (flak 10,881 B dijumpai semasa ujian); suite penuh **13/13 SEMUA
   LULUS (401.8s)** — uji_visual_sebenar **74.2s** dalam suite (vs
   143.3–172.1s sebelum optimum, 135.1s poll lama); bersendirian
   **71.8s, 68/0 dua larian**. Audit silang MULA_CEPAT ↔ MULA_SINI ↔
   sesi_index: tiada hanyut tarikh/kiraan.

1. **MULA_CEPAT versi pengguna (komit 8)** — seksyen §1 dikemas
   ke tarikh semasa + 2 baris baharu (5 tema ≥ WCAG AA dengan galeri
   visual; paparan responsif 1024×600 + DPI 125%/150% selepas
   pembaikan pepijat viewport); seksyen §3 baharu 'Tukar tema (5
   pilihan)' + nota paparan responsif. Audit dokumen-vs-UI **110/0**
   kekal hijau.

1. **Semak semula tuntutan kiraan suite (komit 7)** — disahkan
   tiada tuntutan '13/13 dua larian' dalam README/CHANGELOG (frasa itu
   hanya dalam rekod komit 4 — betul); kiraan '13 ujian' dan '52/0'
   README tepat; satu drift dijumpai dan dibaiki: '377 semakan' →
   **391 semakan (15 bahagian)** (semak.py deterministik 391, dua
   larian; punca: _SKIP_FOLDER prun arkib/venv pada 16 Ogos mengubah
   skop imbas; kekal **391** — dikunci automatik oleh semak #16).
   Entri CHANGELOG 15 Ogos (458.5s) kekal sejarah.
   Gate: semak SEMUA LULUS · 110/0.

1. **Optimum uji_visual_sebenar (komit 6)** — profiler mendedahkan
   58 tangkapan skrin / 11 panggilan = ~5 cubaan/panggilan (paparan RDP
   tidak stabil — punca masa berubah 172s vs 143s); gelung cubaan
   bertukar daripada sleep tetap 0.6s ke **poll adaptif 0.15s** (pecah
   awal bila bingkai berubah). Diukur 3 larian berturut-turut:
   **86.7s / 89.4s / 89.4s — ~40–48% lebih laju, liputan kekal 68/0**
   (vs 143–172s asal). Gate penuh hijau (semak SEMUA LULUS · 52/0 ·
   110/0). Hari dibuka semula selepas penutup — kiraan berlanjutan.

1. **Suite pra-hantar 13/13 + audit log (komit 5)** — dua larian
   berturut-turut SEMUA LULUS (514.4s + 485.1s) selepas pembetulan
   viewport; audit semua 13 log pra_hantar: tiada amaran tersembunyi,
   tiada Traceback/flak, semua ujian 0 gagal (52/0, 130/0, 110/0,
   dsb.), tiada proses yatim. Pembetulan viewport tidak merosakkan
   ujian lain. Hari dibuka semula selepas penutup — kiraan berlanjutan.

1. **Penutup sementara — rekod penuh 3 commit (`d35e4ff`, komit 4)**
   — PERUBAHAN_17OGOS + sesi_index (PENUTUP HARI + kiraan telus) +
   MULA_SINI diselaraskan; hari kemudian dibuka semula dengan
   lanjutan (suite, optimum, MULA_CEPAT).

1. **Baiki pepijat viewport tersekat 640×480 (komit 3)** —
   ujian responsif semua halaman mendedahkan: selepas setCurrentIndex
   atau resize tetingkap, halaman bukan-semasa boleh kekal 640×480
   dalam stack 1024px → kandungan terpotong kanan (hbar tersembunyi
   oleh ScrollBarAlwaysOff; diukur 1/2 larian). Pembetulan
   `_paksa_saiz_halaman()` di ui/app_qt.py: paksa halaman == saiz
   stack + nudge -1/+1 hanya bila viewport basi (<80%); dipanggil
   setiap go() + hook resizeEvent stack. Disahkan 24/24 (6 halaman ×
   4 larian) pada 1024×600 + DPI 150%: hbar 0, DESC_KLIP 0. Skrol
   papan kekunci (Key_Down 0→60), roda (turun-naik 60→0), Tab (fokus
   pindah) — SEMUA OK. Galeri muktamad: 5 tema ditangkap semula
   (sistem→neutral disahkan), deterministik (fresh 0.00%).

1. **Galeri 5 tema kad 114px + ujian saiz/DPI (komit 2)** —
   `dokumen/imej/tema_home_*.png` (5 tema) dikemas ke reka bentuk kad
   114px — galeri MANUAL_PENGGUNAAN.md otomatis seiring; bukti visual
   `lihat_5tema_home.html`. Ujian tetingkap kecil 1024×600: grid 3×3
   kekal, kad 114px, **tiada skrol mengufuk** (hbar_max 0), skrol
   menegak sahaja, DESC_KLIP 0. Ujian DPI 125%/150%
   (`QT_SCALE_FACTOR`): grid 3×3 kekal, kad 114px, tiada skrol mengufuk
   walaupun saiz minimum 900×560, DESC_KLIP 0.

1. **Penutup hari 16 Ogos — rekod penuh (`cdf4e63`, komit 1)** —
   eksperimen grid (2 lajur mustahil dalam gate 730px → varian
   C 3×3 kad 100→114px, desc 4 kitab dipendekkan) + pengesahan border 9
   kitab gelap/terang + kiraan telus 16; mutasi uji_negatif #30/#34 ke
   "16 commit" (52/0).

1. **Eksperimen saiz kad grid (`e8032cb`)** — 2 lajur × 5 baris
   DITOLAK: ukuran 1240×730 LEBIHAN 207px (hero 231px + grid 624px =
   855px), kad perlu ~50px = tidak boleh dibaca, 9 kad tidak bahagi 2
   (baris ke-5 anak yatim). 3×3 dikekalkan dengan kad 100→114px
   (+14%) — ruang dijimat: hero compact (pad 30→20), tajuk margin
   18→8, jarak grid 6→5, margin bawah 14. Penemuan bonus: desc 4
   kitab (bukhari, muslim, malik, ahmad) TERPOTONG pada saiz < 124px
   — dipendekkan ke satu baris (cth. "Kompilasi hadis sahih oleh
   Imam al-Bukhari." → "Hadis sahih oleh Imam al-Bukhari.").
   Kandungan penuh halaman 50%→56%, LEBIHAN 0, DESC_KLIP 0. Border 9
   kitab disahkan render dark + light (offscreen; paparan fizikal
   tidak dapat diambil sesi ini — RDP).

1. **Border kad ikut warna kitab (`8b760c8`)** — ganti jalur atas 6px
   dengan border keliling 2px warna kitab (9 warna); hover border
   cerah 45% (tema gelap) / gelap 30% (terang); glow ikut warna kitab.
   Disahkan fizikal 5 tema + klik/navigasi SELAMAT.

1. **Tala halus halaman utama (`ed8ad67`)** — glow diperkuat (alpha
   200, blur 8: jelas kelihatan) + jalur aksen 4→6px; LEBIHAN 0.

1. **Penutup hari — rekod penuh (`92b3992` + `23cafbc` + `f8dd057`)**
   — PERUBAHAN_16OGOS, sesi_index (PENUTUP HARI + kiraan telus) dan
   MULA_SINI diselaraskan; mutasi uji_negatif #30/#34 dikemas seiring
   kiraan (52/0).

1. **Betulkan hover kad tak timbul (`b60df90`)** — dua punca diukur
   fizikal: (1) bayang HITAM atas latar gelap #1f1f1f tak nampak →
   **glow teal** (halo terang alpha 110) untuk tema gelap, tema terang
   kekal bayang hitam; sempadan hover TEAL_GLOW→TEAL; (2) kad menutupi
   pembungkus jadi Enter/Leave pergi ke KAD, bukan pembungkus →
   **penapis peristiwa** pada kad mencetuskan efek pembungkus. Margin
   + spacing grid ditala supaya halaman utama kekal muat 730px.
   Pengesahan skrin sebenar: gelap 31,315 px (GLOW) · Kertas 31,205 px
   (BAYANG) · lightneutral 31,205 · kad hadis 82,361 (QSS, kekal tanpa
   glow) · klik + 24 navigasi SELAMAT. Gate SEMUA LULUS.

1. **Baiki ranap klik kad kitab (`bed79f0`, kritikal)** — bisect
   fizikal: punca QGraphicsDropShadowEffect aktif semasa
   QStackedWidget.setCurrentIndex (access violation dalam `go()`);
   preload/torch BUKAN punca. Pembetulan: `_buang_bayang_semua()`
   dalam `go()` sebelum setiap navigasi. 24 kitaran fizikal tanpa ranap.

1. **Hover timbul via pembungkus lutsinar (`cbefeaa`)** —
   QGraphicsDropShadowEffect tak dirender pada widget QSS; `BungkusTimbul`
   (tanpa stylesheet) membawa efek. **`6c090b5`** baiki ranap `deleteLater()`
   kedua.

1. **Reka bentuk halaman utama (`4dd9aa9`)** — mockup ② Hero Statistik
   ditala iteratif (buang ikon masjid, mod terang kertas, chip segi
   empat, hover timbul, ⚙ 22px, v1.0 rapat). Jalur aksen 4px warna
   kitab (9 warna) + badge kiraan + "Buka →"; chip 15→4px; tajuk
   berpusat. Gate hijau + jalur disahkan fizikal.

1. **Perbincangan installer TERTUNDA (`6f988df` dsb.)** —
   `PERBANDINGAN_INSTALLER.md` sedia (dua hala tuju + kos setahun +
   pengalaman + versi disemak) di dokumen/rujukan/; Fasa 0 terbuka.
   Pengguna pilih finalise apl dahulu.

1. **Penyerapan dokumen kawalan installer PyInstaller/MSIX dari
   Dokumentasi_Khas (komit 3)** — tiga dokumen luar projek diserap ke
   `dokumen/rujukan/`: INSTALLER.md (902 baris, panduan PyInstaller →
   EXE → MSIX → Store), PLAN_BINA_EDARAN.md (diselaraskan: PyInstaller
   utama, MSIX/Store utama, Nuitka fallback), BANDING_INSTALLER.md
   (keputusan didokumen + §10 syor empirikal). Keputusan alat bina
   dibalikkan daripada "terbuka sama rata" kepada PyInstaller/MSIX,
   disokong bukti diagnostik (binaan 33 minit, app dibuka tanpa
   crash; `main.py` perlu `freeze_support()`). Fasa 0 kekal CADANGAN
   — menunggu kelulusan pengguna. Rekod penuh: PENYELARASAN_KHAS.md.

1. **Penutup hari 15 Ogos (14 commit) + semak.py prun venv (`5c28571`)** —
   hari 15 Ogos ditutup dengan rekod penuh: jadual 14 baris dalam
   `sesi_index.md` + entri PERUBAHAN_15OGOS + item penutup MULA_SINI;
   kiraan semua dokumen diselaraskan ke 14 (semak #15 hijau, mutasi
   #30/#34 kekal 14). Komit ini juga membaiki semak.py yang TERGANTUNG
   selepas venv PyInstaller/Nuitka wujud: `_senarai_py_projek()`
   memprun `_SKIP_FOLDER` (.venv, build, dist) dari scan `**/*.py`;
   `.gitignore` kini `.venv*/`. Komit pertama hari baharu — 15 Ogos
   kekal **14 commit** (14 sebenar − 0 langkah-B).

1. **Gabung ZIP pembetulan luaran ①–④ (`329bbbb`)** — 4 pembetulan
   kod daripada `Pustaka_Hadis_Pembetulan_Lengkap/` (bahan luaran
   kini gitignored) digabung berperingkat dengan gate: RandomWorker
   `terjemah_ralat` · SemanticWorker → `_Base` di ui/workers.py ·
   buang `_page_settings` dari `_build()` · `_DIAKRITIK` + `\u0610-
   \u0614` (audit identik 30,547/30,541/6). Status dalam list-we-do.md
   seksyen K (5 DIGABUNG, 3 BELUM).

1. **README diselaraskan + suite penuh akhir (`250216d`)** — kiraan
   `uji_negatif_8z` dikemas `45/0 — 30 cabang` → `52/0 — 34 cabang`;
   `370+ semakan` → `377 semakan (15 bahagian)`; komen semak.py kini
   sebut semak #15 ringkasan satu muka; suite penuh **13/13 SEMUA
   LULUS (458.5s)** — larian penuh ketiga berturut-turut + "OK tiada
   proses ujian yatim selepas suite". Butiran:
   `dokumen/perubahan/PERUBAHAN_15OGOS.md`.

Kerja penuh **14 Ogos — 36 commit (11 teras + 25 susulan)** (sila
baca konteks penuh hari itu dahulu):

1. **4 item tertangguh §8 DITUTUP** (`341bdc9`) — (1) suite pra-hantar
   11 ujian pada mesin sebenar SEMUA LULUS (termasuk `uji_visual_sebenar`
   68/0 dengan tetingkap fizikal); (2) `uji_tersimpan_sebenar.py` 20/0 —
   halaman Tersimpan dengan tanda buku SEBENAR (simpan 3 hadis 3 kitab,
   restart → kekal, buka, tanggalkan, pulihkan) + daftar ujian #12;
   (3) `diagnos_syarah.py` pada data sebenar — penomboran Fath al-Bari
   **HANYUT** (julat 520, 1/8 sejajar) → Fasa 4B kekal dibatalkan;
   (4) `uji_pipeline_api.py` 18/0 — install → **API HIDUP** (kunci
   developer, memori sahaja) → baca → tersimpan.
2. **Sync penuh dari mula (#2, `f59cd95`)** — `sync.py --paksa`, 9 kitab
   100% (622 muka surat, ~12.5 min, kuota 9,999→9,360); "Rekod baharu: 0"
   tiap kitab; pengesahan 62,169: unik, 0 duplikat, id kontigu, FTS
   sejajar, **teks API vs DB 45/45 padan**.
3. **Padanan ara-* penuh (#3, `8512b47`)** — 32,439 hadis 7 kitab:
   31,952 berjaya (98.5%), lapisan Arab 1,628 (5.1%) mengisi celah
   Indonesia, 0 entri basi; audit bebas 30,541/30,547 (100.0%, 6 disyaki
   = positif palsu saksi); `sync_english.py` dari mula = **31,833
   deterministik**.
4. **Audit liputan SemakHadis (#8, `988c803`)** — 4,237/62,169 (6.8%);
   tirmidzi 1.6% terendah → bukhari 10.2%; 103/393 bab 0%; jurang
   terbesar Tafsir 843, Hajj ≈1,564, Solat ≈1,371 — dokumen
   `dokumen/audit/AUDIT_SEMAKHADIS.md`.
5. **Penutupan hari (`79eb722`)** — jadual 8 item tertangguh dalam
   `sesi_index.md`; baki #7 kunci API (kekal AKTIF sengaja).
6. **Siasatan tafsir BM (`1326aaf`)** — TIADA sumber tafsir/syarah BM
   per-hadis terbuka menutup jurang Tafsir 843. MyHadith JAKIM kini
   BERFUNGSI (sebelum ini "Transport error") tetapi koleksi separa + hak
   cipta JAKIM; Tafsir Kemenag = Quran Indonesia, bukan BM. Dokumen:
   `dokumen/audit/SIASATAN_TAFSIR_BM.md`. Pantau MyHadith + IslamHouse
   Melayu.
7. **Dokumen Mula Cepat (`3973c7e`)** — `dokumen/manual/MULA_CEPAT.md`
   untuk pengguna: apa yang disahkan, cara jalankan, cara carian.
   Hierarki dokumen pengguna lengkap: MULA_CEPAT → MANUAL_PENGGUNAAN →
   MANUAL_INSTALASI → BACA_SAYA.
8. **Semakan dokumen vs UI (`1b1390c`)** — `semak_dokumen_ui.py`
   **74 semakan, 0 gagal**: setiap tuntutan `MULA_CEPAT.md` +
   `MANUAL_PENGGUNAAN.md` disahkan terhadap UI sebenar offscreen
   (angka DB, dua lajur, cip warna, bar teks, menu Salin, 2 enjin
   carian, panel Tetapan, deklarasi, fail .bat, Python 3.14) — semua
   TEPAT, tiada dokumen ketinggalan kod.
9. **Semakan #12 semak.py: 'Sesi Terakhir' MULA_SINI seiring git log**
   — bahagian ini TIDAK boleh ketinggalan: tarikhnya mesti ≥ tarikh
   commit git terbaru, **teks ringkasannya mesti menyebut tarikh kerja
   terkini** (bukan hanya tajuk), menyebut hash daripada 10 commit
   terbaru, dan semua hash yang disebut mesti wujud. Dikunci oleh
   `uji_negatif_8z` (4 cabang mutasi, 45/0).
10. **Semakan #13: audit dokumen digate** — `semak_dokumen_ui.py` kini
    ujian #13 dalam `uji_pra_hantar.py` (suite **13 ujian**); semakan
    J/K (README ↔ MANUAL_PENGGUNAAN ↔ MULA_CEPAT tidak hanyut) + I
    (tuntutan .bat) + A (angka DB) — **110/0**; MULA_CEPAT URL kunci
    API dibetulkan (hadis.my → Developer/API); suite 12/12 lulus
    (389.2s) + `SUMBER_hadis-my.md` diaudit konsisten (`c3d6a7d`).
11. **Tema NEUTRAL lalai + WCAG AA dikunci (`f4a0900`)** — untuk
    pengguna awam, lalai bertukar kertas hangat → **gelap neutral** gaya
    Windows (`#1F1F1F`, teks putih, tiada hue hangat); panel TEMA kini
    3 pilihan (☀ Terang · 🌙 Neutral lalai · 📜 Kertas); tier malap
    semua tema dinaikkan ke ≥ 4.5:1 (WCAG AA) — semakan **#13 semak.py**
    (54 pasangan warna) dikunci, `uji_negatif_8z` **50/0** (33 cabang);
    pepijat cache .pyc Windows (mtime 2 saat) dijumpai & dibaiki dalam
    ujian mutasi.
12. **Tema NEUTRAL TERANG (`d81df8f`)** — palet `lightneutral` baharu
    (PAGE_BG `#F4F4F4`, CARD `#FFFFFF`, teks hitam neutral, TIADA hue
    hangat) untuk pengguna mod terang; panel TEMA kini **grid 2×2**:
    🌙 Neutral (lalai) · 📜 Kertas · ☀ Neutral terang · ☀ Terang;
    semak kontras #13 kini **72 pasangan (4 tema)**; uji_tukar_tema
    8 kitaran 35/0; uji_negatif_8z kekal 47/0.
13. **Tema 'Ikut sistem' (`4717c32`)** — ikut mod gelap Windows secara
    automatik: `windows_gelap()` baca registry `AppsUseLightTheme`;
    `tema_efektif('sistem')` → 🌙 Neutral (Windows gelap) / ☀ Neutral
    terang (Windows terang); pemantau QTimer 2 saat bina semula UI
    bila Windows bertukar mod (disahkan ujian flip hidup: bertukar
    dalam 1.0 s); panel TEMA + **🌓 Ikut sistem** (5 butang); toast
    dibetulkan guna `is_dark()`; uji_tukar_tema 10 kitaran 43/0,
    semak 6 melancar 5 mod.
14. **Penutup hari — status akhir** — **24 commit**
    (11 teras + 13 susulan); ciri tema siap: **5 pilihan
    TEMA** (🌙 Neutral lalai · 📜 Kertas · ☀ Neutral terang · ☀ Terang
    · 🌓 Ikut sistem), semua tier ≥ WCAG AA (semak #13, 72 pasangan);
    ujian flip Windows HIDUP direkod (`ce2c3cf`): app bertukar
    automatik 1.0 s; suite rasmi **13/13 SEMUA LULUS** berulang kali
    (terakhir 449.1s); `semak.py` SEMUA LULUS; pokok kerja bersih;
    baki tertangguh §8 hanya **#7 kunci API** (kekal AKTIF sengaja).
15. **Galeri 5 tema dalam manual** — 10 tangkapan skrin
    tema (Utama + Detail, halaman sama) disalin ke `dokumen/imej/`;
    `MANUAL_PENGGUNAAN` TEMA ada seksyen **"Rujukan visual (5 tema)"**
    (2 jadual 5 lajur); `MANUAL_INSTALASI` senarai ZIP dikemas:
    **120 → 130 fail** (imej 9 → 19); `MANUAL_REFERENSI_DEV` §12A
    mendokumenkan kumpulan imej + proses galeri.
16. **Susun atur RTL — Arab di KANAN, terjemahan di KIRI** —
    demi menghormati status hadis rujukan (naskhah Arab asal
    dibaca kanan-ke-kiri), lajur dua tab dicerminkan:
    `ui/pages_detail.py` — lajur kanan tab **ARAB | TRANSLITERASI**
    (dijajarkan kanan), lajur kiri tab **Melayu | Indonesia |
    English**; semakan geometri dikemas (`semak_dokumen_ui` D3b +
    `uji_visual_mockup`: arab x > terjemahan x); README/MULA_CEPAT/
    MANUAL_PENGGUNAAN diselaraskan; baseline `bina_tangkapan --kemas`
    + **10 imej galeri tema ditangkap semula** dengan susun atur RTL.
17. **Penutup RTL — Numpy + galeri muktamad** — `bina_tangkapan`
    `_metrik`/offset-scan digantikan Numpy (formula IDENTIK, beza
    metrik 0.00e+00; ~13× saiz sama, offset-scan 78M piksel kini
    saat — dahulu menggantung mesin perlahan); **10 imej galeri
    tema ditangkap semula** tanpa toast (tunggu 3.2s) dengan kod
    RTL muktamad; cabaran suite lambat direkod (proses yatim +
    `profil_model.json` patologi — cara pemulihan penuh dalam
    sesi_index); suite **13/13 SEMUA LULUS** (bersegmen: 1–9 via
    pra-hantar, 10–13 individu).
18. **Pengukuhan suite + pengesahan akhir** — `uji_pra_hantar.py`
    kini **bunuh proses ujian yatim secara automatik** pada mula
    (`_bersihkan_orphan()`, juga `--bersihkan`) — hanya skrip ujian
    projek, bukan app/tugas pengguna (diuji keselamatan); galeri
    manual TEMA → **`<img>` sebaris** (render terus di GitHub/ZIP);
    **pengesahan visual akhir** pada app sebenar: tema "sistem" →
    Neutral, **Arab@(554,275) kanan vs terjemahan@(104,275) kiri**
    — susun atur RTL disahkan pada widget sebenar + tangkapan
    `bukti_visual/sistem_rtl_*.png`.
19. **Pengesahan dua hala orphan** — `uji_pra_hantar.py` kini
    **sahkan TIADA proses yatim selepas suite** (`_semak_orphan_selepas()`,
    logik dikongsi `_cari_orphan()` dengan pembersihan awal): subproses
    ujian mesti keluar sendiri, apa-apa yang tinggal → GAGAL; diuji
    orphan tiruan dikesan→dibunuh→0; `--bersihkan` + `_cari_orphan()`
    didokumenkan dalam MANUAL_REFERENSI_DEV seksyen suite ujian.
20. **Audit dokumen RTL + gate pantas** — susulan pengesahan dua hala
    (`a9e9d44`): semua rujukan susun atur lama (Arab kiri / terjemahan
    kanan) dibersihkan — MANUAL_PENGGUNAAN (jadual sejarah), TRANSFORMASI_
    DETAIL (nota RTL di atas + 5 tuntutan susun atur/geometri), nota
    sejarah MULA_SINI; **`gate_pantas.py` baharu** — semak.py +
    uji_negatif_8z + pokok bersih dalam satu arahan (~35s) sebelum
    setiap commit kecil (bukan pengganti suite penuh).
21. **Semak #14: audit RTL dokumen dikunci** — `semak_rtl_dokumen()`
    semak.py: frasa susun atur lama ("Arab di kiri", "terjemahan di
    kanan", dsb.) dalam TRANSFORMASI_DETAIL/MANUAL_PENGGUNAAN → GAGAL
    (nota sejarah berpetik selamat); dikunci `uji_negatif_8z`
    **50/0 (33 cabang)** — mutasi #32 "Arab di kiri" disuntik → dikesan;
    suite penuh AKHIR **13/13 SEMUA LULUS (463.6s)** + "tiada proses
    ujian yatim selepas suite".
22. **Semak #14 diperluas — README + sesi_index** — audit RTL kini
    turut menutup README.md (imbas penuh) dan sesi_index.md (hanya
    ringkasan "Sesi Terakhir" — arkib sejarah berketarikh dikecualikan);
    dikunci mutasi **#33** ("Arab di kiri" disuntik ke README →
    dikesan) → `uji_negatif_8z` **50/0 (33 cabang)**.
23. **Penutup hari — rekod penuh 35 commit** — hari ditutup dengan
    semua ciri disahkan (lihat sesi_index seksyen penutup): 5 tema
    semua ≥ WCAG AA, RTL Arab kanan (`6b853f0`), Numpy bandingan
    piksel, gate pantas (`09fe9db`), semak #14 audit RTL dikunci
    (`c8878ec` + `4ed70a6`), pembersihan orphan dua hala (`a9e9d44`),
    suite penuh **13/13 SEMUA LULUS** (akhir 463.6s); baki tertangguh
    §8 hanya #7 kunci API (kekal AKTIF sengaja).
24. **Ringkasan satu muka di atas + semak #15 dikunci (`6894212`)** —
    ringkasan 'Keadaan projek' dipindah ke bahagian PALING ATAS
    dokumen (sebelum 'Sesi Terakhir') supaya sesi AI baharu selesai
    tanpa arkib penuh; pautan silang dokumen berkaitan; §5 kini nota
    penunjuk; semak #15 `semak_ringkasan_keadaan` mengunci ringkasan
    seiring 'Sesi Terakhir' (tarikh + kiraan commit) — dikunci
    `uji_negatif_8z` **52/0 (34 cabang)**, mutasi #34.
25. **Gabung skema 8 `arab_carian` + dokumen audit ⑤⑥** — kesinambungan
    gabung ZIP (①–④ komit 11/12): diff bersih disahkan (folder db.py/sync.py
    = root + skema 8 sahaja). `db.py` SKEMA_VERSI 7→8: `bersih_tashkeel()`
    (buang harakat sahaja, TIDAK lipat ة→ه), kolum `arab_carian`, FTS5
    indeks `arab_carian`, trigger dalam `_backfill_arab_carian()`, self-heal
    migrasi terganggu, normalisasi query. `sync.py` isi `arab_carian`
    rekod baharu. Ujian pada SALINAN DB sebenar SEMUA LULUS 74.67s
    (62,169, 0 NULL, 3 trigger, `كتب`=`كَتَبَ` 767); backup + migrasi
    produksi; `semak_db.py` 62,169. Dokumen audit (GTAF, AHMAD_*, DARIMI,
    CARIAN_ARAB, DRAF_carian_arab, PERMOHONAN_LESEN_AHMAD) disalin ke
    dokumen/audit + rujukan. **Carian Arab tanpa tashkeel kini berfungsi**
    (isu GTAF.md §4 tertutup).
26. **Ujian hidup carian Arab + suite penuh + banding INSTALLER** —
    carian Arab tanpa tashkeel di UI SEBENAR disahkan 9/9 (كتب=767 sama
    dengan كَتَبَ, نية=10, puasa=911, tema sistem→Neutral); suite penuh
    **13/13 SEMUA LULUS (502.1s)** dengan skema 8 hidup; `dokumen/rujukan/
    BANDING_INSTALLER.md` — ZIP pilih PyInstaller/MSIX vs projek utama
    Nuitka/GitHub: alat bina kekal TERBUKA (uji diagnostik kedua-dua),
    nilai ZIP (masalah lazim, checklist, ujian naik taraf) dikenal pasti.
27. **Penutup hari — rekod penuh 14 commit** — hari ditutup: rekod
    penuh 14 commit dalam `sesi_index.md` (jadual 14 baris); kiraan
    semua dokumen diselaraskan ke 14 (komit penutup ini ialah rekod
    semata-mata — komit pertama hari baharu; 15 Ogos = 14 sebenar − 0).
    Baki tertangguh §8
    hanya #7 kunci API (kekal AKTIF sengaja). Status Fasa 2: binaan
    PyInstaller siap di disk (gitignored, app dibuka tanpa crash;
    `main.py` tiada `freeze_support()`); bina Nuitka ditangguh — alat
    bina kekal TERBUKA (BANDING_INSTALLER.md).

Butiran penuh: `dokumen/perubahan/PERUBAHAN_14OGOS.md` (log harian) ·
`dokumen/sesi/sesi_index.md` (arkib penuh — seksyen baharu di hujung
fail untuk setiap kerja di atas).

**Sebelum ini (13 Ogos, Sesi 55 lanjutan):** buang tab "Sebelah" (3 tab
bahasa sahaja) · teks terjemahan SAMA PARAS dengan Arab (`Qt.AlignTop`
+ `addStretch`) · lalai saiz teks Arab Kecil · pembetulan draf jawapan
AI (bahagian "Carian Biasa (Keyword)") · bar TEKS `Lapor ralat |
Kongsi | Salin` (bukan butang) + menu Salin 3 pilihan · justify pada
semua teks rumi (terjemahan/transliterasi/huraian) · panel transliterasi
dijajarkan ke atas. Pengesahan 13 Ogos: suite 11/11 tiga larian
berturut-turut (395.6s/392.6s/392.9s) — `dokumen/perubahan/PERUBAHAN_13OGOS.md`.

---

## 1. Peraturan yang TIDAK boleh dilanggar

| # | Peraturan | Kos jika dilanggar |
|---|---|---|
| 1 | **JANGAN** kembali ke tkinter/CustomTkinter | Tiada sokongan bidi. Teks Arab songsang. Sudah gagal 2x. |
| 2 | **JANGAN** guna `arabic-reshaper` / `python-bidi` | Qt kendalikan RTL secara natif. Menggunakannya = shaping dua kali. |
| 3 | **JANGAN** lipat `ة → ه` dalam indeks carian | `نية` jadi `نيه` — tidak wujud. Carian pecah. (Untuk kunci padanan dalaman, OK.) |
| 4 | **JANGAN** buang import "unused" dalam `ui/*.py` | Ia sasaran `apply_theme()`. Tukar tema terus pecah. |
| 5 | **JANGAN** tulis `.bat`/`.ps1` dengan baris LF | cmd.exe perlukan CRLF. Gagal SENYAP. |
| 6 | **JANGAN** minta / terima kunci API dalam sembang | Sudah 2 kunci terdedah. Sync jalan pada mesin pengguna. |

---

## 2. Tiga corak pepijat yang BERULANG

Setiap satu sudah menggigit lebih daripada sekali. Semak sebelum hantar.

### A. Nilai dinilai pada masa import → terkunci selama-lamanya

```python
def text_browser(text="", color=TEXT_SECONDARY):   # SALAH
```
Python menilai nilai lalai **sekali** semasa import. Warna tema gelap
terkunci; mod terang jadi kelabu atas putih.

```python
def text_browser(text="", color=None):             # BETUL
    if color is None:
        import ui.theme as _t
        color = _t.THEMES[_t.CURRENT_THEME]["TEXT_SECONDARY"]
```

Berkait: `from theme import CARD_BG` mengikat NILAI. `apply_theme()`
mesti menyalin ke ruang nama **semua** modul UI.

**Imbas dengan AST sebelum hantar** — cari `def f(x=WARNA)`.

### B. Pembolehubah persekitaran null → `Join-Path` melontar

Sudah berlaku **3 kali**: `$env:WINDIR`, `$env:APPDATA` (×2).

```powershell
if ($env:APPDATA -and (Test-Path (Join-Path $env:APPDATA '...'))) { }  # SALAH
```
`Join-Path` dinilai SEBELUM `Test-Path` — melontar jika null.

```powershell
$dir = $null                                                    # BETUL
if ($env:APPDATA) { $dir = Join-Path $env:APPDATA '...' }
if ($dir -and (Test-Path $dir)) { }
```

### C. Andaian tidak diuji menghentikan segalanya

Dua kes besar sesi ini, kedua-dua **salah**:

- *"Penomboran `eng-*` tak sepadan, jadi English mustahil"* → Ada edisi
  `ara-*` sebagai jambatan. Padan ikut **teks**, bukan ID. Fasa 3 siap.
- *"Fath al-Bari tiada dalam OpenITI"* → Ada. Repo AH dibundarkan
  **KE ATAS**: Ibn Hajar (852H) berada dalam `0875AH`, bukan `0850AH`.

**Uji terhadap data sebenar SEBELUM membuat kesimpulan.**

### D. Skrip ujian print emoji → crash 0xC0000409 (Sesi 29)

`print()` emoji (🤖 dalam teks UI seperti `search_info.text()`) ke stdout
Windows cp1252 **dalam gelung acara Qt** (QTimer callback) → fail-fast
`0xC0000409` (EXIT=-1073740791), crash native yang **TIDAK** dapat
ditangkap `try/except`. Di luar Qt ia cuma `UnicodeEncodeError`.

**Semua skrip ujian yang mencetak kandungan UI MESTI** tetapkan dahulu:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")   # atau set PYTHONIOENCODING=utf-8
```

Tanpa ini, crash dianggap sebagai bug aplikasi (QThread/torch) sedangkan
ia artifak pengekodan stdout. Bukti penuh: `dokumen/sesi/sesi_index.md` Sesi 29.

---

## 3. Senarai semak sebelum hantar

**Satu arahan sahaja:**

```bash
python semak.py
```

Menjalankan berpuluh semakan (senarai ringkas di bawah), setiap satu
wujud kerana sesuatu pernah rosak:

| # | Semakan | Menangkap |
|---|---|---|
| 1 | Sintaks Python | fail rosak |
| 2 | Import modul teras | `from client import ...` yang tidak wujud |
| 3 | Warna sebagai nilai lalai | Lesson #17 |
| 4 | `.bat`/`.ps1` CRLF + ASCII | Lesson #20 |
| 5 | `Join-Path $env:` tanpa pengawal | Lesson #19 |
| 6 | Migrasi DB (data + favorit kekal) | kehilangan data pengguna |
| 7 | Apl melancar, 5 mod tema (termasuk 'sistem') | Lesson #17, #11 |
| 8 | Transliterasi (12 kes) | jalalah, shadda, tanwin, syamsiyyah |
| 9 | Syarah: parser + pengawal | penomboran sumber berubah |
| 10 | Folder bersih | `__pycache__`, DB ujian |
| 11 | 'Sesi Terakhir' MULA_SINI seiring git log | bahagian ringkasan lapuk (cth. kekal '13 Ogos' selepas kerja 14 Ogos) |
| 12 | Kontras WCAG AA semua tema | warna/tier teks baharu bawah 4.5:1 (GAGAL AA) |

Keluar 0 = selamat hantar. Keluar 1 = jangan hantar.

**Ujian penuh (visual + fungsi + mutasi) — satu arahan:**

```bash
python uji_pra_hantar.py
```

Menjalankan semak.py dahulu, kemudian **12 suite ujian** dengan laporan
ringkas + masa setiap ujian (14 Ogos 2026): mutasi negatif (`uji_negatif_8z`),
mockup (`uji_visual_mockup`), piksel (`uji_visual_piksel`), skrin sebenar
(`uji_visual_sebenar`), tema (`uji_tukar_tema`), bandingan 3 tab + sama
paras (`uji_bandingan`), lompat (`uji_lompat_fungsi`), aliran penuh
(`uji_end_to_end`), regresi tangkapan dokumen (`bina_tangkapan_dokumentasi`),
draf jawapan AI (`uji_draf_jawapan`), Tersimpan dengan tanda buku
sebenar (`uji_tersimpan_sebenar` — ujian #12), dan audit dokumen manual
vs UI sebenar (`semak_dokumen_ui` — ujian #13, 110/0, digate 14 Ogos).
Berhenti pada kegagalan pertama (`--teruskan` untuk jalankan semua).
Log penuh disimpan dalam `bukti_visual/pra_hantar_*.log`. `semak.py`
masih perlu dijalankan sendiri untuk output penuh setiap semakan.

`semak.py` menetapkan stdout/stderr ke UTF-8. Tanpa itu ia mati dengan
`UnicodeEncodeError` pada konsol Windows (cp437) sebaik cuba mencetak
teks Arab — atau malah tanda sempang panjang.

Disahkan menangkap pepijat sebenar: 3 pepijat lama disuntik semula
ke dalam salinan projek, kesemuanya dikesan.

**Masih perlu manual:** uji dengan folder bernama **ada ruang**
(`D:\Pustaka Quran Hadis`) — banyak pepijat hanya muncul di situ.

---

## 4. Fakta yang perlu diingat

### API hadis.my
```
Base   : https://service.hadis.my/api/v1     Header: X-API-Key
Kuota  : Basic 200/hari · DEVELOPER 10,000/hari    Reset 12AM MY
Throttle: 1.1s  →  622 permintaan ≈ 12 minit
```
- `/hadis/search` → `data.results` (BUKAN `data.hadis`)
- Senarai guna `per_page`, bukan `limit`. Maks 100.
- `meta` di **top-level**, bukan dalam `data`
- `lang=ms|id` sahaja. Nilai lain diabaikan senyap.
- Slug: `bukhari muslim abu-daud tirmidzi nasai ibnu-majah malik ahmad darimi`

### hadis.db
```
62,169 hadis  →  164 MB  (138 MB selepas VACUUM)
FTS5 hanya 19% saiz · carian 0.03 ms
Versi skema: db.SKEMA_VERSI, migrasi automatik dalam init()
journal_mode=WAL — KEKALKAN (diuji: 2x lebih laju baca sambil tulis)
```
Fail `-wal`/`-shm` bukan sampah: ia wujud hanya semasa sambungan
terbuka dan dibersihkan sendiri. Jangan "betulkan" dengan tukar ke
DELETE — itu andaian yang sudah diuji dan ditolak.
Tambah jadual baharu? Naikkan `SKEMA_VERSI` dan tambah ke `MIGRASI`.
Jangan cipta skema di tempat lain — satu sumber kebenaran.

### Terjemahan Inggeris (Fasa 3, SIAP — 98%, diaudit)

**Kunci padanan ialah teks INDONESIA, bukan Arab.** hadis.my dan CDN
berkongsi terjemahan Indonesia yang SAMA (pertindihan diukur 1.00),
manakala teks Arab berkongsi sanad panjang dan mudah tersalah padan.

```
hadis.my (indonesia) --padan--> ind-* --nombor sama--> eng-*
hadis.my (arab)      --sandaran--> ara-*    (bila indonesia tiada)
```

Turutan 5 lapisan dalam `padan()` — JANGAN susun semula:
| # | kaedah | kunci | ambang |
|---|---|---|---|
| 1 | `indo` | teks Indonesia dinormalisasi | tepat |
| 2 | `indo~` | token Indonesia | `JACCARD_IND` 0.95 |
| 3 | `penuh` | teks Arab penuh | tepat |
| 4 | `awalan` | 200 aksara Arab | mesti UNIK |
| 5 | `kata` | token Arab jarang | `JACCARD_MIN` 0.90 dua hala |

- **JANGAN buang pengesahan dua hala** pada lapisan `kata`. Skor sehala
  memberi **35.3% positif palsu** (Bukhari, ujian yatim). Sanad dikongsi
  = 80% teks hadis pendek.
- **JANGAN guna `INSERT OR REPLACE` sahaja** dalam sync. Baris lama yang
  kini ditolak akan KEKAL dengan terjemahan salah. `DELETE` per-kitab dulu.
- 7 kitab ada · `ahmad` & `darimi` TIADA
- `ara-*1` identik dengan `ara-*` selepas normalisasi, fail lebih kecil

**Audit mesti guna bukti BEBAS.** `diagnos_padanan.py` menilai padanan
Arab dengan teks Arab — berhujah dalam bulatan. Guna `audit_eng.py`:
ia membandingkan teks Indonesia yang tidak pernah dipakai untuk memadan.
Lapisan `indo`/`indo~` ditanda "(bukan bukti bebas)" atas sebab sama.

```
python sync_english.py      # ~31,833 tersimpan, 98%
python audit_eng.py --semua # Bukhari: 100.0% disahkan, 0 disyaki
```

### Syarah Fath al-Bari (Fasa 4B) — ⚫ DIBATALKAN buat sementara

**Keputusan pengguna 31 Jul 2026:** gugurkan 4B buat sementara, tumpu 4A
(Irsyad al-Hadith). Fath al-Bari kekal di arkib; jangan buka semula tanpa
sebab baru.

**Penanda `# N` BUKAN nombor hadis Bukhari.** Ia kiraan berjujukan
dalam edisi Ibn Hajar. Ia bermula sejajar lalu hanyut progresif:

```
   1-200  anjakan  +0        2000-3500  anjakan -120
 600-800  anjakan -32        5000-7000  anjakan -320
```

- **JANGAN** simpan syarah ikut padanan ID. 95% kitab akan salah.
- **JANGAN** percaya sampel dari hujung julat: 80 hadis pertama
  memberi 76%, kadar sebenar merentas kitab 13%.
- Padanan teks juga gagal: syarah memetik potongan sanad, bukan matn.
  300 seksyen diuji, delta median 174 tanpa corak.
- Pengawal `nisbah_keyakinan()` kini menolaknya dengan betul dan
  mencetak jadual hanyut. `sync_syarah.py` selamat dijalankan —
  ia akan batal sendiri.

### Huraian auto (Fasa 4) — ⚫ DIBUANG 3 OGOS 2026

Huraian HadeethEnc (Fasa 4) + nota topik auto **DIBUANG daripada UI** pada
Sesi 18.9. Dua jenis "Huraian" (auto + SemakHadis) mengelirukan pengguna;
keputusan pengguna: hanya **SemakHadis** (syarah sebenar BM) + syarah
klasik Arab + darjat yang dipapar. Butang "📖 Huraian", halaman huraian,
`ui/workers.PipelineWorker` dan `core/phase4_exegesis.py` dibuang.

- Data HadeethEnc (jadual `hadethenc`, `.cache_he/`, `sync_hadeethenc.py`)
  kekal sebagai arsip — tiada lagi dipapar dalam UI.
- `core/hadeethenc_api.py` KEKAL — `_matn` masih dipakai `core/sema_source`.
- Sebelum ini (31 Jul): huraian Melayu ringkas datang dari
  **HadeethEnc.com** (projek IslamHouse) dengan padanan MATN sahaja.
  `python sync_hadeethenc.py` ~310 padanan, 147 sumber ber-Melayu.

### Huraian SemakHadis — TAMBAH 3 OGOS 2026

**SemakHadis.com** menyediakan syarah Bahasa Melayu SEBENAR (terjemahan +
komentar + status hadis) untuk 4,237 hadis popular — nilai tambah besar
berbanding HadeethEnc (310). Padanan juga ikut MATN Arab (0.55).

```
python scripts/muat_turun_sema.py   # muat turun cache SemakHadis (16,547 rekod)
python sync_sema.py                 # 4,237 padanan, 16,547 sumber ber-BM
```

- Sumber: 16,547 rekod SemakHadis dimuat ke `.cache_sema/` — tiada kunci API
  (API had 1,000 rekod/query; skrip enumerate 42 query huruf Arab).
- Bukhari 717 · Muslim 430 · Ahmad 1,645 · lain 1,445.
- UI papar Collapsible "Huraian (SemakHadis · status)" TERBUKA selepas
  tab bahasa: tajuk, status, terjemahan, takhrij, komentar, atribusi.
- **LESEN TIDAK NYATA**: SemakHadis tidak menyatakan lesen semula data.
  Atribusi dipaparkan; dapatkan kebenaran bertulis sebelum edaran komersial.
- Hasil penilaian penuh + keputusan dorar.net: `dokumen/sesi/sesi_index.md` Sesi 18.8.

### Fasa 4 lapisan A (Irsyad al-Hadith) — ⚫ DITUTUP 31 Jul

**Lesen TERTUTUP.** Footer muftiwp.gov.my: "Hak Cipta Terpelihara © 2024
Jabatan Mufti Wilayah Persekutuan". Artikel Irsyad TIDAK termasuk dalam
Data Terbuka Kerajaan (hanya 2 set waktu solat). Tiada terma penggunaan
semula — jangan guna, jangan simpan.

**Sumber BM lain juga disiasat dan ditolak:** MyHadith JAKIM (kerajaan),
IslamHouse Malay (lesen terbuka ✅ tetapi buku PDF, bukan per-hadis),
hadits.id/NU/tazkia/Kemenag (terjemahan sahaja), syarah Bulughul Maram
(terjemahan penerbit). **HadeethEnc (147 hadis BM) + SemakHadis (4,237
hadis BM selepas sync penuh) kini menjadi sumber syarah BM per-hadis.**
Butiran: `dokumen/perubahan/PERUBAHAN_31JUL.md` §13.

### Qt — pepijat yang sudah dibetulkan
Jangan "perbaiki" perkara ini semula:
- `setAlignment()` mesti **sebelum** `setPlainText()`
- JANGAN `setDefaultTextOption`/`WrapAtWordBoundaryOrAnywhere`/
  `setTextWidth()` pada dokumen hidup — merosakkan bidi
- Auto-tinggi: ukur pada `document().clone()`
- `QSizePolicy.Maximum` menegak = halaman kosong. Guna `Minimum`.
- Menu klik-kanan perlu eventFilter + pasang pada `viewport()` juga

---

## 5. Keadaan projek

> **Ringkasan satu muka kini di bahagian paling atas dokumen** (sebelum
> 'Sesi Terakhir') — baca itu dahulu. Sejarah penuh mengikut sesi di
> bawah kekal sebagai arkib berketarikh; rujuk ringkasan atas + §1–§4.

**Versi semasa: v1.0** (11 Ogos; Sesi 28 — skrin pemula/splash + Salin/Kongsi
bahasa semasa; Sesi 29 — lompat terus ke hadis `bukhari 433`, `B433`, `Ctrl+G`;
Sesi 30 — refactor developer lengkap: `ui/helpers.py` + 6 mixin halaman;
Sesi 31 — indikator jam berputar semasa carian;
Sesi 32 — simbol selawat ﷺ lalai + pembersihan sandaran + 8m ke .py;
Sesi 33 — lalai saiz fon Sederhana untuk semua;
Sesi 34 — butang ↑ terapung + kotak "Lompat No. hadis" di atas senarai;
Sesi 34 lanjutan — selawat ﷺ lengkap dalam transliterasi rumi;
Sesi 35 — Kongsi WhatsApp ikut bahasa semasa (petikan Arab + satu
terjemahan) + selawat ﷺ lengkap (petik melengkung + Arab tertanam) +
manual pengguna EN;
Sesi 36 — kongsi Ringkas sertakan pautan "Baca penuh" sunnah.com
(peta dalam-buku + semak 8n/8o);
Sesi 37 — pepijat skrol "Lompat No. hadis" dibetulkan;
Sesi 38 — carian khusus (cth. "bukhari 500") terus ke butiran + toast
"Membuka…";
Sesi 39–40 — ujian GUI polling tunggu_sedia() + butang Kembali ikut
halaman asal (Utama/Carian);
Sesi 41–46 — semakan unit pemalar render: BACK_PETA 8p,
Sebelum/Seterusnya 8q, _label_simpan/LABEL_RAWAK 8r, _tab_lalai 8s,
tag "Bab Tafsir" _ialah_bab_tafsir 8t);
Sesi 55 (12 Ogos) — halaman detail DUA LAJUR (Arab | terjemahan) + palet
kertas hangat + cip warna ikut makna + huraian/darjat TERBUKA;
Sesi 55 lanjutan (13 Ogos) — buang tab "Sebelah" (3 tab bahasa sahaja) +
teks terjemahan SAMA PARAS dengan Arab + lalai saiz teks Arab Kecil +
pembetulan draf jawapan AI (bahagian "Carian Biasa (Keyword)") + bar
teks `Lapor ralat | Kongsi | Salin` (bukan butang) + menu Salin 3 pilihan +
justify semua teks rumi + panel transliterasi di atas;
Sesi 56 (14 Ogos) — semakan mesin sebenar, 8 commit (`341bdc9` →
`1b1390c`): (1) 4 item tertangguh §8 DITUTUP — suite pra-hantar 12 ujian
SEMUA LULUS (tetingkap fizikal) · Tersimpan dengan tanda buku sebenar
(uji #12) · `diagnos_syarah.py` — penomboran Fath al-Bari HANYUT ·
pipeline API HIDUP 18/0; (2) **sync penuh dari mula** — 62,169 sejajar
API (622 muka surat, 45/45 padan teks); (3) **padanan ara-* penuh** —
31,952/32,439 (98.5%), audit bebas 100.0%, sync English 31,833
deterministik; (4) **audit liputan SemakHadis** — 4,237 (6.8%), peta
jurang per kitab/bab (`AUDIT_SEMAKHADIS.md`); (5) penutupan hari — 8
item §8: 7 ditutup/diaudit, baki #7 kunci API (AKTIF sengaja);
(6) **siasatan tafsir BM** — TIADA sumber per-hadis terbuka menutup
jurang Tafsir 843 (`SIASATAN_TAFSIR_BM.md`; MyHadith JAKIM berfungsi
tetapi separa + hak cipta — pantau); (7) dokumen Mula Cepat pengguna
(`MULA_CEPAT.md`); (8) **audit dokumen vs UI** — `semak_dokumen_ui.py`
74/0, semua tuntutan manual TEPAT; (9) susulan: audit dokumen digate
sebagai ujian #13 · semakan #12 'Sesi Terakhir' seiring git log ·
konsistensi rentas dokumen (J/K, 110/0) · **SESI TEMA (malam)** —
**5 pilihan TEMA** (🌙 Neutral lalai + WCAG AA 72 pasangan · 📜
Kertas · ☀ Neutral terang · ☀ Terang · 🌓 Ikut sistem ikut mod
Windows, ujian flip hidup bertukar 1.0 s) — jumlah 24 commit,
suite rasmi 13/13 SEMUA LULUS, pokok bersih, baki #7 kunci API
(AKTIF sengaja).

> **KEMASKINI 11 Ogos (Sesi 28–29):**
> - **Skrin pemula (splash)** — `ui/splash.py` `SplashPermula`: bar kemajuan
>   beranimasi, label fasa, klik untuk langkau. `PreloadWorker.kemajuan`
>   (4 fasa) → `main.py` tutup splash bila sedia/dilangkau/45s. VERSI 1.3.
> - **Salin/Kongsi bahasa semasa** — butang dalam cabang bahasa tunggal
>   `_switch_lang`.
> - **Lompat terus ke hadis (Sesi 29)** — `_parse_lompat` + `_slug_dari_awalan`:
>   `'bukhari 433'`, `'bukhari:433'`, `'B433'`, `'b 433'`, `'433'`. Kotak
>   "Lompat No. hadis" di atas senarai kitab + pintasan `Ctrl+G` (kotak
>   "No. hadis… / Pergi" di pager digantikan, Sesi 34). Nombor sahaja
>   membuka butiran terus. Ujian `uji_lompat.py` 67/67 lulus.
> - **Pelajaran Sesi 29**: skrip ujian yang print teks UI (ada emoji) MESTI
>   set `PYTHONIOENCODING=utf-8` — jika tidak crash 0xC0000409 disalah anggap
>   sebagai bug aplikasi (lihat §2.D).

> **KEMASKINI 8 Ogos (Sesi 30) — refactor developer (tiada perubahan fungsi):**
> - **Risiko #2 dokumen/rujukan/PANDANGAN_RISIKO.md DITUTUP** — `tampalan_preload/` di-gitignore
>   + dibuang dari git (`git rm -r --cached`); fail kekal di disk.
>   `dokumen/rujukan/PANDANGAN_RISIKO.md` §2 ditanda ✅ DITUTUP.
> - **Refactor langkah 1 — `ui/helpers.py`**: pemalar + fungsi bebas
>   (`_parse_lompat`, `_slug_dari_awalan`, `_ALIAS_KITAB`, `_read_json/_write_json`,
>   `_clear`, `click_sound`, `PAGES`, `LANG_PARAM`, `_HAD_WA`, `BASE_DIR`/`SETTINGS`/
>   `BOOKMARKS`) dipisah dari `ui/app_qt.py` dan diimport semula supaya
>   `ui.app_qt._parse_lompat` dsb. kekal untuk `uji_lompat.py`/`settings_panel.py`.
>   **Tiada import warna** → tidak perlu daftar `_THEMED_MODULES`.
> - **Refactor langkah 2 — mixin halaman**: `ui/pages_kitab.py` (`PagesKitab`) +
>   `ui/pages_carian.py` (`PagesCarian`); `PustakaApp(PagesKitab, PagesCarian,
>   QMainWindow)`. `ui/app_qt.py` 2,428 → 1,774 baris. Kedua-dua modul didaftar
>   dalam `_THEMED_MODULES` (PagesCarian import warna AMBER). `semak.py` 8g dikemas
>   (`_tampal_gabungan` kini dibaca dari `ui/pages_carian.py`).
> - **Refactor langkah 3 — `ui/pages_detail.py`** (`PagesDetail`, 26 kaedah):
>   `_render_detail`, `_bina_translit/_syarah/_sema/_he/_darjat`, `_switch_lang`,
>   `_share/_copy/_tts`, `_teks_*`, `_is_saved/_toggle_save`. `app_qt.py` 1,774 →
>   875 baris. Pemalar `LANG_LABEL`/`_ATRIBUSI_*` dialih ke `ui/helpers.py`;
>   `semak.py` tambah `_sumber_ui()` + `_cari_fungsi()` (semak 8e/8f/8i baca
>   sumber gabungan mixin). Didaftar dalam `_THEMED_MODULES` (import warna
>   TEXT_SECONDARY). Komit `fcf77e7`.
> - **Refactor langkah 4 — `ui/pages_tersimpan.py` + `ui/pages_tetapan.py`**
>   (`PagesTersimpan`: halaman Hadis Tersimpan; `PagesTetapan`: API/saiz/fon/
>   bahasa). `app_qt.py` 875 → 586 baris; `_THEMED_MODULES` + kedua-dua modul
>   (PagesTetapan import warna); `semak.py` `_sumber_ui()`/`_cari_fungsi()`/8d
>   sertakan modul baharu. Komit `3344a86`.
> - **Refactor langkah 5 — `ui/pages_home.py`** (`PagesHome`: halaman Utama) —
>   `PustakaApp` kini warisi SEMUA 6 mixin `(PagesKitab, PagesCarian, PagesDetail,
>   PagesTersimpan, PagesTetapan, PagesHome, QMainWindow)`; `app_qt.py` 586 →
>   504 baris — **inti sahaja** (init, header, tema, navigasi, worker).
>   Komit `7507ba2`.
> - **dokumen/rujukan/RANCANGAN_REFACTOR.md** — pelan 5 langkah; SEMUA langkah SELESAI (8 Ogos).
> - **Disahkan**: semak.py SEMUA LULUS · uji_lompat 67/67 · uji_lompat_fungsi
>   15/15 · uji_tukar_tema 19/19 · uji_bandingan 28/28 · uji_end_to_end 18/18 ·
>   uji_data_baharu 18/18.
> - Komit: `40228d4` (risiko #2), `1b3b8fd` (helpers), `5288852` (kitab/carian),
>   `fcf77e7` (detail), `3344a86` (tersimpan/tetapan), `7507ba2` (home).

> **KEMASKINI 8–9 Ogos (Sesi 31) — indikator jam berputar semasa carian:**
> - **Indikator carian sedang berjalan** — halaman Carian kini memaparkan emoji
>   jam berputar 🕐→🕛 (QTimer 120ms) di baris status semasa carian berjalan
>   (kata kunci FTS5 + makna AI selari); disembunyikan bila kedua-dua worker
>   selesai. Sebelum ini skrin kosong + teks "Mencari…" statik — pengguna tidak
>   tahu sama ada carian berjalan (carian makna AI boleh ~24 saat pada larian
>   pertama, model belum dimuat).
> - **Laluan gagal keyword dibaiki** — sebelum ini carian kata kunci yang gagal
>   (ralat API/jaringan) tersangkut pada "Mencari…" selama-lamanya. Kini
>   `_on_search_failed()` menamatkan carian, menyembunyikan jam, dan hasil AI
>   masih dipapar jika ada. Pembaikan ariti isyarat (`SearchWorker.failed` =
>   1 argumen, `tok` ditangkap lambda).
> - **Semakan 8l semak.py** — 5 sub-semakan AST per fungsi (`_page_search`,
>   `_do_search`, `_tampal_gabungan`, `_on_search_failed`) mengesahkan
>   label/QTimer, 12 muka jam, show/start, hide/stop, laluan gagal; kemudian
>   ditambah sub-semakan 6–7: `uji_visual_carian.py` wujud + konsisten
>   (penanda `_carian_sibuk`/`_carian_timer`/🕐🕛/`w.grab()`/`_do_search`/
>   `isVisible()`).
> - **Ujian visual kekal `uji_visual_carian.py`** (11/11) — struktur, bukti
>   render tetingkap `w.grab()` (pin 🕐 vs 🕛 berbeza), kitaran hidup carian
>   sebenar ("hukum riba").
> - Komit: `95d4785` (⏳ + laluan gagal), `0c1e037` (jam berputar),
>   `f654fad` (semakan 8l), `dc795da` (uji_visual_carian.py).

> **KEMASKINI 9 Ogos (Sesi 32) — simbol selawat ﷺ lalai + pembersihan + 8m ke .py:**
> - **Simbol selawat ﷺ lalai** — paparan Melayu kini menggantikan frasa
>   "Sallallahu 'alaihi wasallam" dengan ligatur Arab U+FDFA ﷺ secara lalai
>   (`simbol_selawat` True). Sebelum ini lalai bentuk penuh (perlu hidupkan
>   di Tetapan). Jaring keselamatan kekal: `_ada_glif_selawat` — fon tiada
>   glif → teks penuh, tiada tofu; togol Tetapan masih ada; hadis.db tidak
>   diubah. Komit `74d31be`. Disahkan skrin fizikal: "Rasulullah ﷺ bersabda".
> - **Ujian visual kekal** — `uji_visual_sebenar.py` seksyen 6 (5 semakan
>   baharu: hadis frasa selawat, lalai diganti `_papar_melayu`, glif
>   tersedia, teks dipapar ﷺ, skrin fizikal). Kepekaan: mutasi lalai →
>   2 GAGAL → pulihkan → 19/19.
> - **Folder sandaran dipadam** — `sandaran_1300/`, `sandaran_1302/`,
>   `tampalan_preload/` (sisa tampalan §6 pra-muat, salinan app_qt.py
>   monolitik lama) redundan dengan git history. dokumen/rujukan/PANDANGAN_RISIKO.md §2
>   dikemas (risiko ditutup sepenuhnya); entri mati dibuang dari
>   .gitignore. Komit `4a86474` + `9c3716b`.
> - **Semakan 8m diluaskan ke .py** — helper `_imabas_kata_indo` (tokenize
>   komen + AST docstring; string kandungan dikecualikan) mengesan kata
>   Indonesia dalam komen/docstring kod, bukan hanya dokumen .md; 8 tapak
>   dibetulkan. BACA.md diarkib ke `_arkib/BACA_TAMPALAN_PRAMUAT.md`
>   dengan nota TAMAT. Komit `30942f1`.

> **KEMASKINI 9 Ogos (Sesi 33) — lalai saiz fon Sederhana untuk semua:**
> - **Ketiga-tiga saiz fon kini lalai "Sederhana"** (skala 1.0) — antara
>   muka, teks Arab, dan terjemahan. Sebelum ini saiz teks Arab lalai
>   "Besar" (indeks 2) sejak komit pertama (`arabic_font_idx = 2`).
>   `ui/app_qt.py` lalai → 1; butang "Set Semula" (`ui/settings_panel.py`)
>   kini pulang ke 1,1,1. `config.py` (diagnostik) + `MANUAL_PENGGUNA.md`
>   §7 BACAAN diselaraskan dengan lalai baharu. Komit `a2ea80e`.
> - Pengguna sedia ada dengan tetapan tersimpan kekal pada pilihan mereka
>   — perubahan ini menetapkan lalai pemasangan baharu dan "Set Semula".
> - Disahkan: semak.py SEMUA LULUS; app offscreen `ui=Sederhana,
>   ar=Sederhana, tr=Sederhana` (indeks 1, skala 1.0).
>
> **KEMASKINI 12 Ogos (Sesi 55) — lalai teks Arab kini KECIL:**
> - Susun atur dua lajur Sesi 55 memerlukan teks Arab padat supaya
>   terjemahan di lajur kanan sama paras (top-aligned) [susunan asal;
>   **14 Ogos: dicerminkan RTL — Arab kini di KANAN, terjemahan di KIRI**;
>   lalai Kecil kekal]. `ui/app_qt.py`
>   lalai `arabic_font_idx` 1 → **0 (Kecil, skala 0.85)**; butang "Set
>   Semula" (`ui/settings_panel.py`) kini `1, 0, 1`. UI dan terjemahan
>   kekal Sederhana. Pengguna sedia ada kekal pada pilihan mereka.

> **KEMASKINI 13 Ogos (Sesi 55 lanjutan) — tab Sebelah dibuang + teks sama paras + draf AI dibaiki:**
> - **Tab "Sebelah" DIBUANG** — `LangTabs` kini 3 tab sahaja (Melayu |
>   Indonesia | English), sepadan reka bentuk mockup (mockup hanya ada 3
>   tab). Fungsi "Salin semua bahasa" (milik tab itu) turut dibuang;
>   tindakan salin/kongsi kekal di bar tajuk + menu klik kanan.
> - **Teks terjemahan SAMA PARAS dengan Arab (punca sebenar dijumpai)** —
>   Qt memusatkan widget saiz tetap dalam `QVBoxLayout` bila ada ruang
>   menegak berlebihan (dibuktikan dengan ujian terpencil), jadi bila
>   lajur Arab lebih tinggi, teks terjemahan jatuh ke tengah. Pembaikan
>   dalam `_switch_lang`: `Qt.AlignTop` pada setiap widget + `addStretch`
>   di hujung kotak supaya ruang lebih tinggal DI BAWAH teks. Disahkan
>   bukhari#3 + kes "Arab >> terjemahan" beza 0px (uji_bandingan 48/0).
> - **Pembetulan draf jawapan AI** — bahagian "🔍 Carian Biasa
>   (Keyword)" dalam kotak Jawapan Draf tidak pernah dipapar kerana dua
>   ralat dalam `compose_draft_answer` (`per_page=5` vs parameter sebenar
>   `limit`; baca `exact["data"]["results"]` vs struktur sebenar
>   `{"hadis": [...]}`) melempar TypeError yang ditangkap SENYAP. Kini
>   `search_hadis(query, limit=5)` + baca `exact["hadis"]`; ujian runtime
>   baharu `uji_draf_jawapan.py` 9/9 (kepekaan mutasi: corak lama → 6
>   GAGAL) + semakan statik semak.py 8t2.
> - Disahkan: suite pra-hantar penuh **SEMUA LULUS 11/11** pada dua
>   larian berturut-turut (395.6s + 392.6s); semak.py 0 GAGAL. Butiran:
>   `dokumen/perubahan/PERUBAHAN_13OGOS.md`.
> - **Ujian ZIP edaran (petang 13 Ogos)** — `PustakaHadis.zip` (120
>   fail) diuji dari folder bernama dengan ruang (`D:\Pustaka Quran
>   Hadis\Ujian Ruang`): `semak_versi.py` 23 ciri + `semak.py` SEMUA
>   LULUS + app melancar. Pepijat tersembunyi dijumpai & dibaiki:
>   semak.py **9b** (peraturan fail sisa untracked) sentiasa GAGAL
>   dalam edaran kerana folder pengguna BUKAN repo git — kini melangkau
>   bila tiada `.git`, kekal aktif dalam repo pembangunan.
> - **Senarai rasmi fail ZIP** — `MANUAL_INSTALASI.md` seksyen 9:
>   jadual 7 bahagian (Akar 51, api 2, core 9, ui 16, utils 3, scripts
>   3, dokumen 36 = 120 fail) + senarai penuh + pengecualian telus +
>   seksyen 10 prosedur pengesahan edaran. Pembetulan pembinaan ZIP:
>   `.env.example` kini disertakan (padanan `.env` sebelum ini tersilap
>   kecualikannya), `opencode.json` (konfigurasi AI dev) dikecualikan.

> **KEMASKINI 9 Ogos (Sesi 34) — butang ↑ terapung + kotak "Lompat No. hadis":**
> - **Butang ↑ terapung** pada 4 halaman (kitab, Carian, Tersimpan,
>   Detail) — muncul di sudut kanan-bawah bila skrol >250px, klik →
>   skrol lancar (animasi QTimer) ke atas. Gaya QSS `#backTop` dalam
>   `ui/theme.py` (ikut tema). Komit `0e77890` (kitab + ujian seksyen 8),
>   `526af1e` (carian + penyatuan kotak), `6b1cbd6` (Tersimpan + Detail
>   — ukur julat: Koleksi/Tetapan muat, tak perlu).
> - **Kotak "Lompat No. hadis" di atas senarai** — menggantikan kotak
>   "No. hadis… / Pergi" di pager bawah (dibuang). Placeholder kabur
>   "0–7008" ikut kiraan db (Bukhari 7008, Muslim 5362); Enter → lompat +
>   sah julat + skrol ke kad. `Ctrl+G` kini fokus ke kotak atas ini.
> - **Garis mode terang ditebalkan** (komit `52cc191`) — `BORDER`
>   `#D8E0E4` → `#C2CDD3` (kontras, bukan hanya ketebalan) + divider
>   header 1px → 2px; semua garis 1px kini kelihatan atas putih.
> - **Selawat ﷺ lengkap dalam transliterasi rumi** (komit `52855a4`) —
>   regex sebelumnya hanya padan bentuk pausal ("salla Allah 'alayhi
>   wa-sallam") sedangkan output transliterasi sebenar ialah bentuk kes
>   penuh ("salla Allahu 'alayhi wa-sallama", damma + fatha) — 541/541
>   sampel terlepas. `_FRASA_SELAWAT` diluaskan (`All[āa]h[u]?` +
>   `sallam[a]?`); seksyen 6b uji_visual_sebenar (7 semakan kekal) +
>   semak 8bb headless (4 semakan rumi + 2 kes kekal) mengunci regresi.
> - Disahkan: semak.py SEMUA LULUS; uji_visual_sebenar.py **60/60** pada
>   skrin fizikal (seksyen 8 + 9 kekal, ujian kepekaan dikesan); suite
>   penuh 13 fail ujian lulus. Rujukan kotak dalam README/MANUAL_PENGGUNA
>   dikemas (komit `6944e22`); butang ↑ didokumenkan dalam manual.

> **KEMASKINI 11 Ogos (Sesi 36–46) — pautan "Baca penuh" sunnah.com + carian khusus terus ke butiran + semakan unit pemalar render:**
> - **Pautan "Baca penuh" sunnah.com** (Sesi 36) — mesej kongsi Ringkas
>   berakhir dengan `Baca penuh: https://sunnah.com/{slug}/{book}/{hadith}`.
>   Nombor apl ≠ penomboran sunnah.com (dedup), jadi
>   `sync_english.py --peta-sunnah` menjana `sunnah_map/` (rujukan
>   dalam-buku; liputan 93.7–99.3%). Semak 8n (peta seiring hadis.db)
>   + audit opt-in `python semak.py --audit-sunnah` — 20/20 pautan
>   disahkan terhadap halaman sunnah.com sebenar.
> - **Carian khusus terus ke butiran** (Sesi 38) — "bukhari 500" atau
>   "433" (chip kitab) membuka butiran hadis TERUS (bukan senarai),
>   dengan toast "📖 Membuka … No. 500…" yang kekal minimum 1800ms
>   semasa muatan async. Carian umum ("hukum riba") kekal senarai hasil.
> - **Butang Kembali ikut halaman asal** — dari butiran yang dibuka
>   melalui Utama/Carian/Tersimpan/Senarai kitab, Kembali menuju ke
>   halaman itu (BACK_PETA, semak 8p; diuji GUI 40b/40c).
> - **Tag "Bab Tafsir"** — dipapar pada kad carian + halaman butiran
>   bila buku = buku tafsir Al-Quran (BAB_TAFSIR: bukhari 65, muslim
>   56, tirmidzi 47); logik diekstrak ke `_ialah_bab_tafsir` + semak 8t
>   supaya kedua-dua paparan tidak hanyut.
> - **Ujian stabil** — semua ujian GUI guna polling `tunggu_sedia()`
>   (QTimer mod offscreen tidak menunggu masa sebenar); semak unit
>   8p–8t mengekstrak logik render kepada fungsi tulen boleh uji.
> - Disahkan: semak.py SEMUA LULUS, uji_lompat_fungsi.py 48/48,
>   uji_bandingan.py 48/48, uji_lompat.py 67/67.

> **KEMASKINI 8 Ogos (Sesi 23):**
> - **Carian kata kunci fallback OR** — kes "hukum riba" sebelum ini pulang
>   0 hasil FTS5 (AND memerlukan SEMUA perkataan). Kini bila AND pulang 0
>   hasil, enjin cuba OR (486 hasil untuk "hukum riba") dengan tanda
>   `meta.fallback` supaya UI memaparkan nota "carian kata kunci longgar".
>   Fungsi: `db._to_match_query(q, gabung)` + `search_hadis` API.
> - **Mesej bantuan carian** — bila kata kunci 0 hasil tetapi AI ada padanan,
>   lencana AMBER memberitahu pengguna mengapa kad kata kunci kosong dan
>   mengarah ke hasil makna (AI).
> - Komit `4f86954` (mesej bantuan) + `f7402a0` (uji tukar tema + end-to-end).
> - `README.md` dikemas kini: liputan data sebenar (SemakHadis 4,237 ·
>   HadeethEnc 310 · darjat 63,930 · bab 31,322) + senarai ujian lengkap.

> **KEMASKINI 8 Ogos (Sesi 22):**
> - **Git diwujudkan** — komit `2970234` (pertama, 89 fail) dan `c3249bf`
>   (v1.1). `.gitignore` mengecualikan data besar + kunci + cache.
> - **Kunci API terdedah dialih keluar dari `semak_kunci.py`** ke
>   `kunci_terdedah.txt` (di-gitignore) — jangan masukkan semula ke kod.
> - **Sync data lengkap**: `bab` 31,322 · `darjat` 63,930 · `hadethenc` 310
>   (sebelum ini kosong). `darjat`=0 untuk Bukhari/Muslim ialah sifat
>   sumber CDN, bukan pepijat.
> - **HadeethEnc kini dipapar dalam UI** sebagai sandaran bila SemakHadis
>   tiada (211 hadis mendapat huraian). Fungsi: `HadisAPI._he/_he_luar` +
>   `_bina_he()` di app_qt.
> - Ujian baharu `uji_data_baharu.py` (18 semakan offscreen) + semak.py
>   135 semakan lulus.

> **KEMASKINI 6 Ogos (Sesi 20):** "Carian Makna (AI)" dibaiki sepenuhnya —
> model `intfloat/multilingual-e5-small` + teks matn Melayu (sanad dibuang),
> indeks 62,169 vektor dibina semula. Skor naik dari 0.21-0.50 (tidak relevan)
> ke 0.84-0.88 (relevan). **PENTING:** `main.py` kini membaiki konflik DLL
> runtime MSVC antara PyQt5 (14.26) dan torch (14.44) — jangan buang fungsi
> `_baik_pulih_dll_qt_torch()` (butiran penuh: `dokumen/sesi/sesi_index.md` Sesi 20).

> **PENTING (keputusan pengguna 31 Jul, selepas bina ZIP):** folder root
> `hadis/` ialah **workspace Developer**, BUKAN untuk pengguna akhir.
> Projek masih dalam **pengembangan**; ZIP hanyalah sandaran/arkib
> pembangunan, bukan pakej edaran. Semua perubahan selesai + tertangguh
> direkodkan dalam `dokumen/perubahan/PERUBAHAN_31JUL.md` dan ringkasan di bawah. Manual
> pengguna: `MANUAL_PENGGUNA.md`. Rujukan developer satu-fail:
> `dokumen/manual/MANUAL_REFERENSI_DEV.md`.

**Siap:** Fasa 1 · Fasa 2 (+ `Collapsible` di UI) · Fasa 3 (English hidup) ·
SemakHadis (4,237 huraian BM selepas sync penuh) · HadeethEnc sandaran (310) ·
tema terang/gelap · pelancar · `BUANG.bat` · migrasi skema · **git** ·
fallback OR carian (v1.2) · bahasa Melayu penuh + ralat diterjemah (Sesi 24) ·
tab Sebelah 3 bahasa (v1.2, dibuang Sesi 55: bukan dalam mockup, teks tidak sama paras) · Salin semua bahasa + Kongsi WhatsApp ikut bahasa semasa (Sesi 26-28; Kongsi semua bahasa dibuang Sesi 34, Salin semua bahasa ikut tab Sebelah dibuang Sesi 55) ·
skrin pemula/splash (v1.3) · **lompat terus ke hadis + Ctrl+G (Sesi 29)** ·
refactor developer lengkap: helpers + 6 mixin halaman, app_qt.py 2,428 → 504 baris (Sesi 30) ·
indikator jam berputar semasa carian (Sesi 31) ·
simbol selawat ﷺ lalai paparan Melayu (Sesi 32) ·
lalai saiz fon Sederhana untuk semua (Sesi 33) ·
butang ↑ terapung 4 halaman + kotak "Lompat No. hadis" + garis terang ditebalkan + selawat ﷺ lengkap dalam transliterasi rumi (Sesi 34) ·
Kongsi WhatsApp ikut bahasa semasa (petikan Arab + satu terjemahan) + selawat ﷺ lengkap merentas paparan + manual pengguna EN + dokumen selaras dengan kod (Sesi 35) ·
pautan "Baca penuh" sunnah.com pada kongsi Ringkas (peta dalam-buku + audit 8n/8o; Sesi 36) · carian khusus terus ke butiran + toast "Membuka…" (Sesi 38) · butang Kembali ikut halaman asal (Sesi 40b/40c) · tag "Bab Tafsir" pada kad carian + butiran (Sesi 46; semak 8t)

**Huraian auto (Fasa 4) DIBUANG 3 Ogos 2026** (keputusan pengguna Sesi 18.9):
butang "📖 Huraian", halaman pipeline, `ui/workers.PipelineWorker` dan
`core/phase4_exegesis.py` dipadam — bertumpuk dengan huraian asli
SemakHadis.

**HadeethEnc dipapar semula 8 Ogos (v1.1)** — tetapi sebagai **sandaran**
yang jujur: bila SemakHadis tiada padanan, huraian HadeethEnc (hadis sahih
BM + penjelasan) dipapar dalam Collapsible berasingan dengan atribusi
wajib IslamHouse. BUKAN "huraian auto" generik lama.

**Fasa 4B DIBATALKAN buat sementara — keputusan 31 Jul** (lihat bahagian
penuh di atas). Muat turun dan parser berfungsi; **padanan ikut ID TIDAK
selamat** — penanda `# N` hanyut merentas kitab. `sync_syarah.py`
membatalkan diri sendiri.
```
OpenITI/0875AH/master/data/0852IbnHajarCasqalani/
  0852IbnHajarCasqalani.FathBari/0852IbnHajarCasqalani.FathBari.JK000166-ara1
30.5 MB · penanda '# N' · 5,075 seksyen · 71.2% dlm julat Bukhari
tashkeel 0.00% · CC BY-NC-SA
```
Dakwaan lama "penomboran SEJAJAR, diuji 5/5" **SUDAH DIBATALKAN**:
ketiga-tiga hadis yang diuji (#1 #2 #8) berada dalam julat 1-200 yang
memang sejajar. Hanyut bermula selepas itu.

**Belum selesai:**
- Fasa 4A Irsyad al-Hadith **DITUTUP 31 Jul** — lesen "Hak Cipta Terpelihara",
  tiada terma penggunaan semula; Data Terbuka Kerajaan hanya 2 set waktu
  solat. Sumber BM lain disiasat, tiada yang sah (butiran `dokumen/perubahan/PERUBAHAN_31JUL.md` §13).
  **JANGAN buka semula tanpa sebab baharu.**
- Huraian auto Fasa 4 **DIBUANG** — lihat bahagian "Huraian auto" di atas
- ~~Sync belum dijalankan pada mesin pengguna~~ — ✅ **DIJALANKAN 14 Ogos**: `sync.py --paksa` penuh, 62,169 hadis sejajar API (45/45 padan teks)
- ~~Padanan `ara-*` diuji dengan proksi~~ — ✅ **DISAHKAN 14 Ogos pada hadis.db sebenar**: 31,952/32,439 (98.5%), audit bebas 100.0%, sync English 31,833 deterministik
- Kunci API kekal AKTIF sengaja — pelan developer untuk ujian app (keputusan pengguna, 31 Jul); #7 item tertangguh satu-satunya yang kekal
- SemakHadis meliputi hadis popular (4,237/62,169) — bukan semua; HadeethEnc
  sandaran menambah 211 lagi (310 padanan); jurang penuh dipetakan dalam `dokumen/audit/AUDIT_SEMAKHADIS.md`
- Lesen SemakHadis belum disahkan secara bertulis

**Penambahbaikan tertangguh (senarai penuh: `dokumen/manual/MANUAL_REFERENSI_DEV.md` §8):**
- ~~App belum disemak pada mesin sebenar~~ — ✅ **DITUTUP 14 Ogos**: suite pra-hantar 12 ujian SEMUA LULUS (termasuk tetingkap fizikal)
- ~~Halaman Tersimpan belum diuji dengan tanda buku sebenar~~ — ✅ **DITUTUP 14 Ogos**: `uji_tersimpan_sebenar.py` 20/0 (ujian #12)
- ~~`diagnos_syarah.py` belum dijalankan pada data sebenar~~ — ✅ **DITUTUP 14 Ogos**: penomboran HANYUT disahkan
- ~~Sesi semakan end-to-end (install → API → baca → tersimpan)~~ — ✅ **DITUTUP 14 Ogos**: `uji_pipeline_api.py` 18/0 (API hidup)
- ~~Sync penuh belum dijalankan dari mula~~ — ✅ **DITUTUP 14 Ogos**: 62,169 sejajar (45/45 padan)
- ~~Padanan `ara-*` belum disahkan pada hadis.db sebenar~~ — ✅ **DITUTUP 14 Ogos**: 31,952/32,439 (98.5%), audit 100.0%
- Kandungan ZIP tidak dianggap siap sehingga semakan selesai — semakan selesai; ZIP kekal arkib pembangunan (bukan pakej edaran)

**Keputusan pengguna:** pengguna campuran (awam teras + mod lanjutan) ·
sync sendiri, DB tidak dibundel · Indonesia kekal · huraian: SemakHadis +
syarah klasik Arab + darjat (huraian auto Fasa 4 dibuang, Sesi 18.9)

---

## 6. Cara bekerja dengan pengguna ini

- **Bahasa Melayu Malaysia**, bukan Indonesia
- `"sama"` boleh bermaksud *masalah berterusan* **atau** *hasil betul*.
  **Tanya**, jangan teka.
- Bila diminta *"analisis sahaja"* — jangan ubah kod.
- Hantar ZIP siap-jalan. Pengguna mahu "download dan jalan".
- Projek sebenar di `D:\Pustaka Quran Hadis` — tidak boleh dicapai dari
  sandbox. Fail di sini ialah binaan semula.

### Nota sandbox
```bash
pip install PyQt5 pyperclip          # perlu setiap sesi
QT_QPA_PLATFORM=offscreen            # untuk ujian
```
Tiada fon Arab dipasang — tangkapan skrin guna fallback DejaVu Sans.

---

## 7. Perbandingan fungsi dengan platform lain (TAMBAH 6 Ogos 2026)

Perbandingan ini hanya bertujuan membantu pengguna memahami perbezaan
fungsi utama setiap platform dalam konteks carian dan semakan hadis.
Setiap platform ada kelebihan masing-masing.

| Fungsi | Pustaka Hadis (apps ini) | MyHadith (JAKIM) | Sunnah.com | SemakHadis.com |
|---|---|---|---|---|
| **1. Carian keyword & semantik** | ✅ Keyword (FTS5) **+ Semantik AI** (e5-small, skor 0.84–0.88) | ✅ Carian kata kunci hadith sahih | ✅ Carian Lucene (quotes, wildcard, fuzzy, boolean) | ✅ Carian/semak hadis |
| **2. Jumlah data** | ✅ 62,169 hadis, 9 kitab (kutub al-tis'ah) | Koleksi hadith sahih rasmi JAKIM | ✅ Paling banyak: 20+ koleksi, 30,000+ riwayat | Koleksi hadis disahkan pengkaji |
| **3. Rujukan hadis disertakan** | ✅ Nama kitab + nombor hadis | ✅ Hadith sahih + riwayat | ✅ Rujukan nombor + grading | ✅ Riwayat + darjat |
| **4. Jawapan ringkas, tersusun** | ✅ "Carian Makna (AI)" draf jawapan tersusun + kad hadis | — | ❌ Paparan mentah, bukan AI | ❌ Fokus semak status, bukan jawapan |
| **5. Bahasa Melayu & Arab** | ✅ Arab (RTL) + Melayu/Indonesia + transliterasi | ✅ Bahasa Melayu + Arab | ⚠️ Arab + English + Urdu + Bangla (**tiada Melayu**) | ✅ Bahasa Melayu |
| **6. Semakan oleh pakar hadis** | ⚠️ Data darjat dari SemakHadis + sumber hadis.my (bukan panel sendiri) | ✅ JAKIM (berautoriti) | ⚠️ Grading al-Albani / Darussalam (sebahagian) | ✅ Ulama / pengkaji hadis |
| **7. Semakan tanpa had** | ✅ Pangkalan tempatan 62,169 + offline | ⚠️ Bergantung portal | ✅ Carian bebas | ✅ Semak sebelum sebar |

**Kedudukan ringkas:** Pustaka Hadis unik pada **Carian Semantik AI + jawapan
tersusun** dan **data lengkap offline dalam Bahasa Melayu**; MyHadith dan
SemakHadis.com unggul pada **autoriti semakan pakar**; Sunnah.com unggul pada
**keluasan data dan carian teknikal**.
