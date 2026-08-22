# Perubahan 16 Ogos 2026

> Log ringkas perubahan pada 16 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md`. Versi apl kekal **1.0**.

## Kandungan sesi

- **Komit 1 (`5c28571`) — Penutup hari 15 Ogos (14 commit) + semak.py
  prun venv.** Hari 15 Ogos ditutup dengan rekod penuh: jadual 14 baris
  dalam `sesi_index.md` (PENUTUP HARI) + entri PERUBAHAN_15OGOS +
  MULA_SINI (item penutup); kiraan semua dokumen diselaraskan ke 14
  (semak #15 hijau, mutasi #30/#34 kekal 14). **semak.py TERGANTUNG**
  selepas venv PyInstaller/Nuitka wujud (`glob('**/*.py')` merentas
  ribuan fail torch) — dibaiki: `_senarai_py_projek()` memprun
  `_SKIP_FOLDER` (.venv, build, dist) dari scan sintaks/bahasa/
  set_total; `.gitignore` kini `.venv*/`. Gate: semak.py SEMUA LULUS ·
  uji_negatif_8z 52/0 · semak_dokumen_ui 110/0 · gate_pantas SEMUA
  LULUS (66.3s).
- **Komit 2 — MULA_SINI ke 16 Ogos.** Ringkasan + 'Sesi Terakhir'
  dikemas ke 16 Ogos (2 commit); mutasi #30/#34 dikunci ke rentetan
  16 Ogos; formula kiraan telus sesi_index/PERUBAHAN_15OGOS dibetulkan
  (15 Ogos = 14 sebenar − 0 langkah-B; komit penutup ialah komit
  pertama 16 Ogos).

## Sesi petang — perbincangan installer + reka bentuk halaman utama

- **Komit 3–6 — Perbincangan installer (ditunda).** `PERBANDINGAN_INSTALLER.md`
  disediakan (dua hala tuju A PyInstaller→MSIX / B Nuitka→Inno, tanpa syor),
  ditambah kos penuh setahun (yuran Microsoft Store **dibuang Sept 2025** —
  kini RM 0) + pengalaman pengguna akhir, kemudian digantikan dengan versi
  disemak (`_1`) — satu dokumen sahaja. **Keputusan Fasa 0 TERTUNDA** —
  pengguna mahu finalise apl dahulu; dokumen kekal di `dokumen/rujukan/`.

- **Komit 7 (`4dd9aa9`) — Halaman utama: reka bentuk mockup 16 Ogos.**
  Audit visual + fungsi penuh (gate hijau). 3 mockup HTML dibina; pengguna
  pilih **② Hero Statistik** yang ditala iteratif (buang ikon masjid,
  mod terang kertas lembut, chip segi empat, v1.0 rapat, hover timbul).
  Perlaksanaan: KitabCard jalur aksen 4px warna kitab (9 warna) + badge
  kiraan + "Buka →", chip radius 15→4px, tajuk seksi berpusat, hover
  timbul. **semak.py SEMUA LULUS · uji_negatif 52/0 · semak_dokumen_ui
  110/0** (jalur 9 warna disahkan fizikal).

- **Komit 8 (`6c090b5`) — Baiki ranap hover kad.** `leaveEvent` panggil
  `deleteLater()` kedua pada efek yang sudah dipadam (Qt memadam automatik
  pada `setGraphicsEffect(None)`) → RuntimeError bila tetikus keluar kad.

- **Komit 9 (`cbefeaa`) — Hover timbul: efek pada pembungkus lutsinar.**
  QGraphicsDropShadowEffect TIDAK dirender pada widget berlatar QSS
  (diukur fizikal: 0 piksel bayang pada kad). Pembungkus `BungkusTimbul`
  (tanpa stylesheet) membawa efek — 647 piksel bayang disahkan fizikal.

- **Komit 10 (`bed79f0`) — Baiki ranap klik kad kitab (kritikal).**
  Bisect fizikal: kod lama 24 navigasi bersih; reka bentuk baharu ranap
  dalam `go()` → `QStackedWidget.setCurrentIndex` (access violation).
  Punca: **efek QGraphicsEffect aktif pada kad (hover) semasa halaman
  ditukar**. Preload/torch BUKAN punca (ranap kekal walaupun dimatikan
  sepenuhnya). Pembetulan: `_buang_bayang_semua()` dipanggil dari `go()`
  SEBELUM setCurrentIndex — meliputi klik kad dan navigasi programatik.
  Disahkan: 24 kitaran hover+klik+navigasi fizikal tanpa ranap; gate
  SEMUA LULUS.

- **Komit 11 (`b60df90`) — Betulkan hover kad tak timbul.** Dua punca
  diukur fizikal: (1) bayang HITAM atas latar gelap #1f1f1f tak nampak —
  diganti **glow teal** (halo terang, alpha 110) untuk tema gelap, tema
  terang kekal bayang hitam; sempadan hover `TEAL_GLOW`→`TEAL`; (2) kad
  menutupi pembungkus jadi Enter/Leave pergi ke KAD, bukan pembungkus
  (0 piksel beza selepas hover) — **penapis peristiwa** pada kad mencetuskan
  efek pembungkus. Margin pembungkus dikecilkan (2,2,2,12) + spacing grid
  10→6 supaya halaman utama kekal muat 730px (LEBIHAN 0).

  **Pengesahan fizikal (skrin sebenar, bukan grab widget):**
  - Tema gelap (neutral): 31,315 piksel berbeza, kecerahan 49 > latar → GLOW
  - Tema terang Kertas: 31,205 piksel, kecerahan 238 < latar 253 → BAYANG
  - Tema lightneutral: 31,205 piksel berbeza
  - Kad hadis dalam senarai kitab: 82,361 piksel — hover QSS jelas, tiada
    glow diperlukan (diputuskan kekal QSS)
  - Klik kad + 24 kitaran navigasi: SELAMAT tanpa ranap
  - Gate: semak.py SEMUA LULUS · uji_negatif 52/0 · semak_dokumen_ui 110/0

  **Jumlah 16 Ogos setakat ini: 11 commit** (2 penutup 15 Ogos + 4
  installer + 5 reka bentuk/ranap/hover). Bukti visual: `bukti_visual/audit/`
  (gitignored).

## Penutup hari — 16 Ogos 2026 (13 commit, rekod penuh)

- **Komit 12 (`92b3992`) — Rekod sesi petang.** PERUBAHAN_16OGOS,
  sesi_index + MULA_SINI dikemas: 11 commit, bukti fizikal glow/bayang
  (gelap 31,315 px · Kertas 31,205 px · lightneutral 31,205 · kad hadis
  82,361 px), kiraan telus. Gate: semak.py SEMUA LULUS · uji_negatif
  **50/2** (2 kegagalan dikesan) · semak_dokumen_ui 110/0.

- **Komit 13 (`23cafbc`) — Selaraskan mutasi uji_negatif #30/#34.**
  Rekod dokumen menaikkan kiraan 3 → 11 commit; rentetan sasaran
  mutasi masih '3 commit' — ganti_teks tiada padanan, mutasi tidak
  berlaku, semak tidak mengesan (50/2). Dikemas ke '11 commit' →
  **52/0 kembali**. Nota kunci dua hala: bila intro/kiraan MULA_SINI
  diubah, mutasi #30/#34 mesti diubah sama.

- **Komit 14 (`ed8ad67`) — Tala halus halaman utama selepas penutup.**
  Glow tema gelap diperkuat: alpha 110 + blur 18 terlalu halus (diukur
  fizikal hanya #1f1f1f → #212523, 2-6 aras) — ditala ke alpha 200 +
  blur 8 + offset (0,1): kini #1f1f1f → #304d3c (teal jelas, ~7px band,
  2,600 px dalam jalur betul) + border teal #5cbf85. Jalur aksen kitab
  4→6px (identiti lebih kuat; LEBIHAN 0, susun atur tak berubah). Gate
  SEMUA LULUS.

- **Komit 15 (`8b760c8`) — Border kad ikut warna kitab.** Gantikan jalur
  atas 6px dengan **border keliling 2px warna kitab** (9 warna) —
  identiti kitab jelas dari semua sisi. Bila hover, border bertukar
  mengikut warna kitab: cerah 45% dalam tema gelap, gelap 30% dalam
  tema terang (cth. Muslim #2e5d8c → #8ca5bf / #204162). Glow
  pembungkus turut ikut warna kitab (dicerahkan 50%) supaya koheren.
  Helper `_campur()` (ui/pages.py). Disahkan fizikal: border Bukhari
  #2e7d6b / Muslim #2e5d8c pada 4 sisi; klik + 24 kitaran navigasi
  SELAMAT; LEBIHAN 0; gate SEMUA LULUS.

**Rekod penuh 16 Ogos — 16 commit (komit penutup akan menjadi komit
pertama 17 Ogos):**

| # | Kerja | Komit |
|---|-------|-------|
| 1 | Penutup hari 15 Ogos (14 commit) + semak.py prun venv (.venv, build, dist) | `5c28571` |
| 2 | MULA_SINI ke 16 Ogos + kunci mutasi #30/#34 | `1cf7ce8` |
| 3 | Serap dokumen kawalan Installer Khas (PyInstaller/MSIX) + pengerasan Terabox | `7410c3d` |
| 4 | Tambah PERBANDINGAN_INSTALLER.md — dua hala tuju tanpa syor | `70f214b` |
| 5 | PERBANDINGAN_INSTALLER: kos penuh setahun + pengalaman pengguna | `9aea12b` |
| 6 | PERBANDINGAN_INSTALLER: versi disemak (satu dokumen sahaja) — Fasa 0 TERTUNDA | `6f988df` |
| 7 | Halaman utama: reka bentuk mockup — jalur warna kitab + hover timbul | `4dd9aa9` |
| 8 | Baiki ranap hover kad: buang deleteLater kedua (RuntimeError) | `6c090b5` |
| 9 | Hover timbul: efek pada pembungkus lutsinar (QSS menyekat QGraphicsEffect) | `cbefeaa` |
| 10 | Baiki ranap klik kad kitab: buang efek bayang sebelum setCurrentIndex (bisect fizikal) | `bed79f0` |
| 11 | Betulkan hover tak timbul: glow teal tema gelap + penapis peristiwa pada kad | `b60df90` |
| 12 | Rekod sesi petang (PERUBAHAN_16OGOS, sesi_index, MULA_SINI ke 11 commit) | `92b3992` |
| 13 | Selaraskan mutasi uji_negatif #30/#34 ke 11 commit (52/0 kembali) | `23cafbc` |
| 14 | Tala halus halaman utama: glow diperkuat (alpha 200, blur 8) + jalur aksen 6px | `ed8ad67` |
| 15 | Border kad ikut warna kitab: keliling 2px + hover cerah/gelap + glow ikut warna | `8b760c8` |
| 16 | Kad kitab 100→114px: hero compact + tajuk ketat; desc 4 kitab dipendekkan (pembetulan terpotong) | `e8032cb` |
| L | **Langkah-B: penutup sementara 13 commit (`f8dd057`)** — tutup hari 16 Ogos pada 13 commit (rekod penuh sesi_index + PERUBAHAN_16OGOS + MULA_SINI + mutasi); hari kemudian dibuka semula dengan lanjutan (ed8ad67..e8032cb). Tidak dikira | `f8dd057` |
| L | **Langkah-B: rekod border warna kitab (`2cb76b8`)** — rekod `8b760c8` dalam PERUBAHAN_16OGOS + sesi_index; kiraan 13→15 + mutasi uji_negatif. Tidak dikira | `2cb76b8` |

**Pengesahan border 5 tema (fizikal, selepas komit 15):** neutral /
Kertas gelap / sistem (→ Neutral) hover cerah 45% (Muslim
#2e5d8c → #8ca5bf) · Kertas terang / Neutral terang hover gelap 30%
(#204162) — semuanya OK; settings pengguna dipulihkan ke "sistem"
(penemuan: satu larian ujian sempat menukar ke "neutral" — dibetulkan).

**Eksperimen grid (selepas komit 16, `e8032cb`):** 2 lajur × 5 baris
DITOLAK — ukuran 1240×730: LEBIHAN 207px (hero 231px + grid 624px),
kad perlu ~50px = tidak boleh dibaca; 9 kad tidak bahagi 2 (baris ke-5
anak yatim). 3×3 dikekalkan dengan kad 100→114px (+14%) — ruang
dijimat: hero compact (pad 30→20), tajuk margin 18→8, jarak grid
6→5, margin bawah 14. Penemuan bonus: desc 4 kitab (bukhari, muslim,
malik, ahmad) TERPOTONG pada mana-mana saiz kad < 124px — teks
dipendekkan ke satu baris (cth. "Kompilasi hadis sahih oleh Imam
al-Bukhari." → "Hadis sahih oleh Imam al-Bukhari."). Kandungan penuh
halaman 50%→56%, LEBIHAN 0, DESC_KLIP 0.

**Pengesahan border 9 kitab (selepas komit 16):** render offscreen
kesemua 9 warna betul dalam tema dark + light (bukhari #2e7d6b,
muslim #2e5d8c, abu-daud #a96b2f, tirmidzi #8c3a4a, nasai #6b4e8c,
ibnu-majah #a08a2e, malik #3a4a6b, ahmad #3f6b3a, darimi #4e6b7a);
pengiraan hover cerah/gelap semua 9 dalam 2 tema betul (cth. Muslim
#8ca5bf / #204162); mekanisme hover fizikal sudah dibuktikan pada
komit 15 (31,315 px glow + border cerah/gelap, 5 tema). Nota: paparan
fizikal tidak dapat diambil semasa sesi (RDP/konsol menunjukkan
sambungan lain) — pengesahan render guna grab widget offscreen.

**Gate penutup:** semak.py SEMUA LULUS (15 semakan, #12/#14/#15 hijau) ·
uji_negatif_8z **52/0** · semak_dokumen_ui 110/0 · pokok kerja bersih ·
tema pengguna "sistem".
