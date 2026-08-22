# Perubahan 17 Ogos 2026

> Log ringkas perubahan pada 17 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md`. Versi apl kekal **1.0**.

## Kandungan sesi

- **Komit 1 (`cdf4e63`) — Penutup hari 16 Ogos (16 commit).** Rekod
  penuh: eksperimen grid (2 lajur mustahil dalam gate 730px → varian C
  3×3 kad 100→114px, desc 4 kitab dipendekkan, DESC_KLIP 0) +
  pengesahan border 9 kitab gelap/terang; kiraan telus 16 Ogos = 16
  commit dalam sesi_index + MULA_SINI; mutasi uji_negatif #30/#34
  dikunci ke "16 commit" (52/0). Komit ini ialah komit pertama 17 Ogos
  (ikut konvensyen).

- **Komit 2 — Galeri 5 tema kad 114px + ujian saiz/DPI.** Selepas
  eksperimen grid, tiga pengesahan tambahan dijalankan:

  1. **Galeri 5 tema halaman utama** — `dokumen/imej/tema_home_*.png`
     (5 tema: neutral, kertas, neutral_terang, terang, sistem) dikemas
     ke reka bentuk kad 114px semasa — galeri dalam
     `MANUAL_PENGGUNAAN.md` (seksyen TEMA) otomatis seiring. Bukti
     visual `lihat_5tema_home.html` (dibuka untuk semakan, dibuang
     sebelum commit — semak #9).

  2. **Ujian tetingkap kecil 1024×600** — grid **3×3 kekal**, kad
     114px, **tiada skrol mengufuk** (hbar_max 0), skrol menegak sahaja
     (content 695 > viewport 538, dijangkakan — kandungan tidak
     terpotong), DESC_KLIP 0. Halaman utama berskrol menegak seperti
     halaman lain; tiada pemampatan/gangguan susun atur.

  3. **Ujian DPI 125%/150%** (`QT_AUTO_SCREEN_SCALE_FACTOR=1` +
     `QT_SCALE_FACTOR`) — dpr 1.25 dan 1.50: grid **3×3 kekal**, kad
     114px, **tiada skrol mengufuk** walaupun pada saiz minimum
     900×560 (150%), DESC_KLIP 0. Kad menguncup mendatar (343→277→243px)
     tetapi teks desc satu baris kekal muat.

  Pengesahan: DESC_KLIP 0 dalam semua 5 tema (per-proses, satu tema
  setiap larian) · regresi fizikal kad 114px sebelum ini (gelap 80,320px
  / terang 48,720px hover, klik + navigasi 24 SELAMAT). Settings
  pengguna dipulihkan ke `sistem` selepas ujian (app menulis semula
  tema aktif semasa tutup — quirk biasa, dipulihkan terus).

- **Komit 3 — PEPIJAT VIEWPORT TERSEKAT 640×480 DITEMUI & DIBAIKI +
  ujian responsif/skrol + galeri muktamad.** Ujian responsif semua
  halaman mendedahkan pepijat sebenar: selepas `setCurrentIndex` ATAU
  selepas tetingkap disaiz semula, halaman bukan-semasa boleh kekal
  pada geometri lalai **640×480** dalam stack 1024px — kandungan
  terpotong di kanan (hbar tersembunyi oleh `ScrollBarAlwaysOff`;
  diukur: 1/2 larian navigasi, viewport 640×480 + hbar 176).

  1. **Pembetulan (`ui/app_qt.py`)**: `_paksa_saiz_halaman()` baharu
     — paksa halaman semasa == saiz stack; jika viewport QScrollArea
     masih basi (<80% lebar halaman), nudge -1/+1 supaya resizeEvent
     diterima (no-op resize dioptimumkan Qt). Dipanggil dari
     `_force_relayout` (setiap `go()`) + hook `resizeEvent` stack
     (saiz tetingkap tiba lewat). Hanya bertindak bila stack bersaiz
     sebenar (≥ 900×400). JANGAN saizkan viewport terus — menceroboh
     ruang bar skrol mengubah balutan teks (diukur: 17% piksel
     berbeza; nudge tanpa syarat juga ganggu susun atur, semak #5
     +11px → diperhalusi dengan pengawal <80%).

  2. **Pengesahan responsif**: semua 6 halaman (utama, kitab, detail,
     carian, tersimpan, tetapan) pada **1024×600** dan **DPI 150%**
     (`QT_SCALE_FACTOR=1.5`): tiada skrol mengufuk (hbar 0), DESC_KLIP
     0, skrol menegak sahaja, tiada ranap. 8+ larian lulus sejak
     pengukuhan.

  3. **Skrol papan kekunci + roda (utama)**: Key_Down ×3 skrol 0→60,
     roda turun-naik 60→0, Tab pindah fokus tanpa ranap — SEMUA OK.

  4. **Galeri muktamad**: `dokumen/imej/tema_home_*.png` ditangkap
     semula (semua 5 tema); `sistem` → `neutral` disahkan (Windows
     gelap). Tangkapan deterministik (fresh-vs-fresh 0.00%); imej
     terang ter-commit lama adalah tangkapan tak stabil (17.6% beza)
     — digantikan.

  Gate: semak.py SEMUA LULUS · uji_negatif_8z 52/0 · semak_dokumen_ui
  110/0.

## Gate

- semak.py **SEMUA LULUS** (16 semakan) · uji_negatif_8z **55/0** ·
  semak_dokumen_ui **110/0**
- MULA_SINI 'Sesi Terakhir' + ringkasan satu muka → **17 Ogos (18
  commit)**; mutasi #27/#30/#34 dikunci ke rentetan 17 Ogos baharu.

---

## PENUTUP HARI — 17 Ogos 2026 (18 commit + 4 langkah-B, rekod penuh)

**Ringkasan hari:** hari bermula dengan penutup 16 Ogos (16 commit,
komit pertama 17 Ogos) dan bersambung dengan pengesahan lanjut reka
bentuk halaman utama — galeri 5 tema, ujian saiz/DPI, ujian responsif
semua halaman yang MENEMUI pepijat viewport tersekat 640×480, skrol
papan kekunci/roda, galeri muktamad, optimum ujian visual, semak
semula kiraan tuntutan suite, MULA_CEPAT versi pengguna, penyelesaian
masalah + suite muktamad, kemudian CHANGELOG log versi seiring, rekod
hari dibuka semula (ringkasan keadaan + pembetulan kiraan + audit
konsistensi), tekanan uji_visual_sebenar 5 larian, semak #16 kiraan
semakan automatik, dan suite muktamad terakhir. Kerja 17 Ogos —
**18 commit** (22 sebenar − 4 langkah-B: c97d028, bb97f42, c5142ef,
6f8f1b8; 3 + penutup sementara + suite 13/13 + audit log + optimum
uji_visual_sebenar + semak kiraan suite + MULA_CEPAT + §4
penyelesaian masalah/poll stabil/suite + penutup sementara 8 +
CHANGELOG + buka semula rekod + ringkasan keadaan + kiraan + audit
konsistensi + tekanan 5 larian + semak #16 + suite muktamad — hari
dibuka semula dua kali selepas penutup sementara):

| # | Kerja | Komit |
|---|-------|-------|
| 1 | **Tutup hari 16 Ogos (16 commit)** — rekod eksperimen grid + pengesahan border 9 kitab + kiraan telus 16; mutasi #30/#34 ke 16 | `cdf4e63` |
| 2 | **Galeri 5 tema kad 114px + ujian saiz/DPI** — dokumen/imej/tema_home_*.png dikemas; ujian 1024×600 + DPI 125%/150% (3×3 kekal, hbar 0, DESC_KLIP 0); PERUBAHAN_17OGOS + sesi_index + MULA_SINI + mutasi ke 2 commit | `6d1f094` |
| 3 | **Baiki pepijat viewport tersekat 640×480 + ujian responsif/skrol + galeri muktamad** — `_paksa_saiz_halaman()` (ui/app_qt.py); 24/24 lulus (6 halaman × 4) pada 1024×600 + DPI 150%; skrol kekunci/roda/Tab OK; galeri 5 tema muktamad (sistem→neutral, deterministik 0.00%) | `5d6a786` |
| 4 | **Penutup sementara 3 commit + rekod penuh** — PERUBAHAN_17OGOS + sesi_index (PENUTUP HARI + kiraan telus) + MULA_SINI diselaraskan; mutasi #30/#34 (52/0); hari kemudian dibuka semula dengan lanjutan | `d35e4ff` |
| 5 | **Suite pra-hantar 13/13 dua larian + audit log** — dua larian berturut-turut SEMUA LULUS (514.4s + 485.1s) selepas pembetulan viewport; audit 13 log: tiada amaran tersembunyi, tiada Traceback/flak, 0 gagal per ujian, tiada yatim | `012e904` |
| 6 | **Optimum uji_visual_sebenar (143→87s)** — poll adaptif 0.15s ganti sleep 0.6s tetap; bersendirian 86.7/89.4s 68/0 | `26b5e57` |
| 7 | **Semak kiraan suite** — drift '377 semakan'→391 dibaiki; README dikemas; entri CHANGELOG 15 Ogos kekal sejarah | `6b8aeb8` |
| 8 | **MULA_CEPAT versi pengguna** — §1 5 tema + galeri + responsif, §3 'Tukar tema'; semak_dokumen_ui 110/0 kekal hijau | `7679ec9` |
| 9 | **MULA_CEPAT §4 Penyelesaian masalah + poll stabil + suite muktamad** — §4 senario pengguna awam; flak sebenar dijumpai (bingkai separa lukis) → poll stabil; suite **401.8s 13/13** (sebenar 74.2s) | `e885503` |
| 10 | **Penutup sementara 8 commit + rekod penuh** — PERUBAHAN_17OGOS (PENUTUP HARI jadual 8 baris + LANJUTAN 1–5) + sesi_index (kiraan telus 8 + jadual penuh) + MULA_SINI diselaraskan; mutasi #30/#34 kekal "8 commit"; hari kemudian dibuka semula dengan lanjutan | `095682f` |
| 11 | **CHANGELOG log versi seiring** — entri 'Kemas kini' dua hari terakhir ditambah (16 Ogos: reka bentuk halaman utama kad 114px + border warna kitab + hover; 17 Ogos: responsif penuh + optimum ujian 401.8s + MULA_CEPAT baharu) supaya log versi seiring log harian — CHANGELOG sebelum ini berhenti di 15 Ogos; kata Indonesia dalam entri baharu dikesan semak 8m dan dibetulkan (52/0 kembali) | `4da64ac` |
| 12 | **Buka semula rekod hari** — CHANGELOG entri 16 Ogos (log versi tiada jurang) + reka bentuk mutasi #27/#30/#34; blok 'Sesi Terakhir' dikemas semula | `e60a74d` |
| 13 | **Ringkasan satu-muka 'Keadaan projek' dikemas** — suite muktamad 463.6s → 401.8s; blok kerja dua hari terakhir; ciri dikunci + mockup ② (kad 114px, border warna, hover, viewport, responsif); pautan log harian → PERUBAHAN_17OGOS.md; kiraan 12 → 13 | `0770ec9` |
| 14 | **Kiraan dibetulkan ke 4** — blok 'Sesi Terakhir' + ringkasan + sesi_index + PERUBAHAN_17OGOS selaras; hash baharu dalam blok (semak #12 top-10 selepas 5d6a786 gugur); mutasi #30/#34 ke 14 commit | `34148a9` |
| 15 | **Audit kiraan silang + format** — MULA_SINI/sesi_index/PERUBAHAN_17OGOS/CHANGELOG disahkan konsisten; pepijat format PERUBAHAN_17OGOS (dua bullet bercantum) dibaiki; kiraan 14 → 15 | `a68efba` |
| 16 | **Tekanan uji_visual_sebenar 5 larian** — 5 larian berturut-turut **68/0 SEMUA LULUS** (105.6–108.3s setiap larian); poll stabil tanpa flak dalam keadaan RDP berbeza (sifar kegagalan, 11 tangkapan/larian); julat 72–108s = varian RDP, bukan poll; mutasi #34 ke 16 commit | `414ba1f` |
| 17 | **Semak #16: kiraan README automatik** — semak.py mencetak jumlah (391 semakan, 15 bahagian) + semak #16 mengesahkan tuntutan README (GAGAL bila lapuk; lompat tanpa hadis.db/bersendirian); pembilang lulus()/tajuk() + bilangan_bahagian(); mutasi #35 subproses (~30s); uji_negatif 52→**54/0 (35 cabang)**; README kekal 391 semakan + 52/0→54/0 | `09dc071` |
| 18 | **Suite muktamad + tutup hari** — suite pra-hantar penuh **13/13 SEMUA LULUS (387.5s)** selepas semak #16 (turun dari 401.8s; uji_visual_sebenar 64.2s dalam suite); semak #12/#15/#16 hijau selepas komit 17; kiraan 17 → 18; mutasi #34 ke 18 commit; PERUBAHAN_17OGOS + MULA_SINI 'Sesi Terakhir' + ringkasan diselaraskan | `8725872` |

**Ciri dikunci kekal:** 5 tema ≥ WCAG AA (semak #13) · susun atur RTL
Arab kanan (semak #14) · ringkasan satu muka seiring 'Sesi Terakhir'
(semak #15) · kiraan semakan README automatik (semak #16) · skema 8
carian Arab · suite 13/13 · halaman utama mockup ② dengan border warna
kitab + glow + kad 114px · pembetulan viewport `_paksa_saiz_halaman`.

**Baki tertangguh (§8):** tidak berubah — #7 kunci API hadis.my kekal
AKTIF sengaja; jurang Tafsir 843 dipantau (MyHadith JAKIM + IslamHouse);
installer Fasa 0 TERTUNDA (`PERBANDINGAN_INSTALLER.md` sedia).

**Gate penutup:** semak.py SEMUA LULUS (16 semakan, #12/#14/#15/#16
hijau — #12 termasuk peraturan tarikh sistem) · uji_negatif_8z
**55/0** · semak_dokumen_ui 110/0 · pokok kerja bersih · tema
pengguna "sistem" · tiada proses ujian tersadai.

---

## LANJUTAN selepas penutup — suite pra-hantar + audit log (komit 5)

Selepas penutup, pengesahan muktamad diminta: suite penuh dijalankan
DALAM keadaan selepas pembetulan viewport — **dua larian berturut-
turut 13/13 SEMUA LULUS**:

| Larian | Masa | Keputusan |
|---|---|---|
| 1 | 514.4s | 13/13 SEMUA LULUS (semak 25.6s · negatif 11.6s · mockup 43.1s · piksel 65.2s · sebenar 172.1s · tema 67.8s · bandingan 10.3s · lompat 6.1s · e2e 40.8s · tangkapan 30.7s · draf 2.0s · tersimpan 25.9s · dokumen_ui 10.1s) |
| 2 | 485.1s | 13/13 SEMUA LULUS (sebenar 143.3s · tema 74.4s · piksel 65.2s · e2e 43.9s · mockup 36.2s · tangkapan 33.5s · tersimpan 30.0s · semak 19.0s · dokumen_ui 11.4s · negatif 9.7s · bandingan 6.9s · lompat 6.7s · draf 1.7s) |

**Audit log pra_hantar (semua 13 log):** tiada amaran tersembunyi —
satu-satunya sebutan "amaran" ialah semakan `semak_versi.py` yang
LULUS (kes DB hilang dikendalikan); tiada Traceback, tiada retry/flak,
tiada ujian dilangkau. Keputusan per ujian: semak SEMUA LULUS ·
negatif 52/0 · mockup 130/0 · piksel 53/0 · sebenar 68/0 · tema 43/0 ·
bandingan 55/0 · lompat 48/0 · e2e 18/0 · draf 9/0 · tersimpan 20/0 ·
dokumen_ui 110/0. "GAGAL" dalam log negatif ialah mutasi yang
DIJANGKA dikesan (senario negatif). **Tiada proses ujian yatim** selepas
kedua-dua larian.

**Kesimpulan:** pembetulan viewport (`5d6a786`) tidak merosakkan
mana-mana ujian lain. Hari dibuka semula daripada 3 → **4 commit**
(komit ini = komit 4); kiraan semua dokumen diselaraskan.

---

## LANJUTAN 2 — optimum uji_visual_sebenar (komit 6)

**Soalan:** uji_visual_sebenar ialah ujian paling perlahan dalam suite
(172.1s / 143.3s dalam dua larian komit 4) — bolehkah ia dipercepat
TANPA mengurangkan liputan (68 semakan)?

**Siasatan profiler (cProfile):** ~45s import torch/transformers +
~30s muat model = 75s overhead model — tetapi semakan `_tampal_gabungan`
menunggu KEDUA-DUA keyword + semantik, jadi model WAJIB untuk liputan
carian (tidak boleh dilangkau). Punca masa berubah-ubah sebenar ialah
**58 tangkapan skrin / 11 panggilan `skrin_fizikal` = ~5 cubaan/panggilan**
pada paparan RDP tidak stabil — setiap cubaan membazir 0.6s sleep tetap.

**Pembetulan (`uji_visual_sebenar.py`):** gelung cubaan bertukar daripada
`sleep(0.6)` tetap ke **poll adaptif** — grab berulang selang 0.15s
sehingga bingkai BERUBAH (md5 != tangkapan semasa) atau 0.6s tamat.
Paparan yang kemas kini cepat pecah awal; paparan lambat masih mendapat
had 0.6s penuh (tiada flak baharu). Tiada perubahan liputan — bilangan
tangkapan, semakan, dan syarat-syaratnya kekal sama.

**Pengukuran (3 larian berturut-turut, 17 Ogos):**

| Larian | Masa | Keputusan |
|---|---|---|
| 1 | 86.7s | 68/0, EXIT=0 |
| 2 | ~87s | 68/0, EXIT=0 |
| 3 | 89.4s | 68/0, EXIT=0 |

vs **143.3–172.1s** asal → **~40–48% lebih laju, liputan kekal 68/0**.
`hashlib` import lazy sedia ada (baris 81) digunakan — tiada kebergantungan
baharu.

**Gate (komit 5):** semak.py SEMUA LULUS · uji_negatif_8z **52/0**
(mutasi #30/#34 dikunci ke "5 commit") · semak_dokumen_ui **110/0** ·
MULA_SINI 'Sesi Terakhir' + ringkasan → **17 Ogos (5 commit)** ·
settings pengguna `sistem` · pokok bersih.

---

## LANJUTAN 3 — semak semula tuntutan kiraan suite (komit 7)

**Permintaan:** semak semula tuntutan '13/13 dua larian' dalam README
dan CHANGELOG supaya kiraan suite kekal seiring.

**Dapatan:**

- **Tiada tuntutan '13/13 dua larian' dalam README atau CHANGELOG.**
  Frasa itu hanya wujud dalam rekod komit 4 (MULA_SINI/sesi_index/
  PERUBAHAN_17OGOS — 514.4s + 485.1s) yang tepat.
- **README '13 ujian' TEPAT** — uji_pra_hantar.py disahkan ada betul-betul
  13 ujian; '52/0 — 34 cabang' juga tepat.
- **Satu drift dijumpai:** README '377 semakan (15 bahagian)' kini
  tidak tepat — semak.py melaporkan **391 semakan** (deterministik,
  dua larian). Punca: `_SKIP_FOLDER` prun arkib/venv/binaan (komit
  5c28571, 16 Ogos) mengubah skop imbas fail .py (bilangan `lulus()`
  statik kekal 207 dalam kedua-dua versi — beza 377→391 datang dari
  fail yang diimbas). Dibaiki: README → **391 semakan (15 bahagian)**.
- **CHANGELOG:** entri 15 Ogos 'Suite penuh 13/13 SEMUA LULUS (458.5s)'
  ialah sejarah tepat untuk tarikh itu — kekal; tiada tuntutan lapuk.

**Gate (komit 6):** semak.py SEMUA LULUS · uji_negatif_8z **52/0**
(mutasi #30/#34 dikunci ke "6 commit") · semak_dokumen_ui **110/0** ·
MULA_SINI 'Sesi Terakhir' + ringkasan → **17 Ogos (6 commit)** ·
settings pengguna `sistem` · pokok bersih.

---

## LANJUTAN 4 — MULA_CEPAT versi pengguna (komit 8)

**Permintaan:** sediakan MULA_CEPAT versi pengguna yang menyebut ciri
galeri 5 tema dan pembetulan responsif terkini.

**Perubahan (`dokumen/manual/MULA_CEPAT.md`):**

- **§1 'Apa yang sudah disahkan'** — tarikh dikemas 14 → **17 Ogos
  2026**; dua baris baharu: (1) **5 tema, semua ≥ kontras WCAG AA**
  (Neutral lalai · Kertas · Neutral terang · Terang · Ikut sistem)
  dengan pautan galeri visual `MANUAL_PENGGUNAAN.md` §3 TEMA; (2)
  **paparan responsif** — kandungan betul pada sebarang saiz tetingkap
  dan penskalaan Windows (100%–150%), selepas pembaikan pepijat
  viewport tersekat (komit `5d6a786`).
- **§3 baharu 'Tukar tema (5 pilihan)'** — cara menukar tema melalui
  ⚙ gear → TEMA, senarai kelima-lima tema dengan penerangan ringkas,
  nota WCAG AA + rujukan galeri.
- **Nota 'Paparan responsif'** di §3 — tetingkap kecil 1024×600 + DPI
  125%/150% kini dipaparkan betul.

**Pengesahan:** semak_dokumen_ui **110/0** (audit tuntutan MULA_CEPAT
vs UI sebenar kekal hijau, termasuk semakan K frasa kunci) · semak.py
SEMUA LULUS · uji_negatif_8z **52/0** (mutasi #30/#34 ke "7 commit").
Semua imej galeri `dokumen/imej/tema_{home,detail}_*.png` (10 fail)
disahkan wujud sebelum menuntut galeri dalam dokumen.

---

## LANJUTAN 5 — MULA_CEPAT §4 + poll stabil + suite muktamad (komit 9)

**Permintaan "semua":** (1) seksyen penyelesaian masalah MULA_CEPAT;
(2) audit silang dokumen; (3) suite penuh muktamad.

**1. MULA_CEPAT §4 'Penyelesaian masalah (ringkas)'** — senario
pengguna awam dalam bahasa mudah: ikon tiada/app tak buka
(JALANKAN/BUAT_PINTASAN/NYAHPEPIJAT), kunci API kali pertama, app
lambat buka (splash + muat model ~30s), saiz teks/antara muka (⚙
gear → PAPARAN), tema Ikut sistem tidak berubah (periksa mod
Windows), carian tiada hasil. §4 Rujukan renombor ke §5. Audit
semak_dokumen_ui **110/0** kekal hijau (semakan G1/G2 + I1–I9 + K).

**2. Audit silang dokumen** — MULA_CEPAT (17 Ogos 2026, 13 ujian,
62,169/31,833/4,237/63,930) ↔ MULA_SINI 'Sesi Terakhir' (17 Ogos 2026)
↔ sesi_index (17 Ogos = 7 commit): **tiada hanyut tarikh/kiraan**.
Nota RTL '14 Ogos 2026' dalam MULA_CEPAT ialah fakta sejarah — kekal.

**3. Poll tangkapan diperbetulkan + suite muktamad** — semasa larian
bersendirian selepas suite, **flak sebenar dijumpai**: `sebenar_butang_atas`
10,881 B (53 warna) — poll lama boleh memecah pada grab pertama
t≈0 dan menyimpan bingkai separa dilukis selepas repaint/hide-show.
Pembetulan: poll kini menunggu **dua grab berturut-turut SAMA**
(stabil) sebelum simpan; had 0.6s kekal untuk paparan lambat.
Pengukuran:

| Larian | Masa | Keputusan |
|---|---|---|
| bersendirian 1 | 71.8s | 68/0 |
| bersendirian 2 | 71.7s | 68/0 |
| dalam suite | 74.2s | 13/13 SEMUA LULUS (401.8s) |

Rantaian penuh: **172.1s → 143.3s → 135.1s → 74.2s** (uji_visual_sebenar
dalam suite); jumlah suite **485.1s → 401.8s** (~17% lebih pantas).

**Gate (komit 9):** semak.py SEMUA LULUS · uji_negatif_8z **52/0**
(mutasi #30/#34 dikunci ke "9 commit") · semak_dokumen_ui **110/0** ·
MULA_SINI 'Sesi Terakhir' + ringkasan → **17 Ogos (9 commit)** ·
settings pengguna `sistem` · pokok bersih.

---

## LANJUTAN 6 — penutup sementara 8 + CHANGELOG + buka semula rekod
(komit 10–12)

- **Komit 10 (`095682f`) — Penutup sementara 8 commit + rekod penuh.**
  Rekod penuh 17 Ogos: PENUTUP HARI jadual 8 baris (cdf4e63..e885503)
  + kiraan telus 8 dalam PERUBAHAN_17OGOS + sesi_index + MULA_SINI;
  mutasi #30/#34 kekal "8 commit" (52/0). Hari kemudian dibuka semula
  dengan lanjutan.

- **Komit 11 (`4da64ac`) — CHANGELOG log versi seiring.** Entri
  'Kemas kini' dua hari terakhir ditambah (16 Ogos: reka bentuk halaman
  utama kad 114px + border warna kitab + hover; 17 Ogos: responsif penuh
  + optimum ujian 401.8s + MULA_CEPAT baharu) supaya log versi seiring
  log harian — CHANGELOG sebelum ini berhenti di 15 Ogos. Bonus: kata
  Indonesia dalam entri baharu dikesan semak 8m dan ditukar ke padanan
  Melayu (52/0 kembali).

- **Komit 12 (`e60a74d`) — Buka semula rekod hari.** CHANGELOG entri
  16 Ogos (log versi tiada jurang lagi); reka bentuk mutasi #27/#30/#34
  (tajuk, tarikh intro, kiraan ringkasan); blok 'Sesi Terakhir' dikemas
  semula.

## LANJUTAN 7 — ringkasan keadaan + kiraan + audit konsistensi
(komit 13–15)

- **Komit 13 (`0770ec9`) — Ringkasan satu-muka 'Keadaan projek' dikemas.**
  Suite muktamad 463.6s → **401.8s** (rantaian 485.1→401.8s selepas
  optimum uji_visual_sebenar 143→72s); blok kerja dua hari terakhir;
  ciri dikunci + halaman utama mockup ② (kad 114px, border warna kitab,
  hover, pembetulan viewport, responsif DPI); pautan log harian →
  PERUBAHAN_17OGOS.md; anggaran suite ~7 minit. Kiraan 12 → 13.

- **Komit 14 (`34148a9`) — Kiraan dibetulkan ke 4.** Blok 'Sesi
  Terakhir' + ringkasan + sesi_index + PERUBAHAN_17OGOS selaras; hash
  baharu 095682f/4da64ac/0770ec9 ditambah ke blok (semak #12 top-10 —
  5d6a786 gugur selepas komit 13); item blok tidak menyebut tarikh git
  literal (mutasi #30); mutasi #27/#30/#34 dikunci ke rentetan 14
  commit.

- **Komit 15 (`a68efba`) — Audit kiraan silang + format.** MULA_SINI /
  sesi_index / PERUBAHAN_17OGOS / CHANGELOG disahkan konsisten;
  pepijat format dalam PERUBAHAN_17OGOS (dua bullet bercantum) dibaiki.
  Kiraan 14 → 15.

## LANJUTAN 8 — tekanan uji_visual_sebenar 5 larian (komit 16)

- **Komit 16 (`414ba1f`) — Tekanan uji_visual_sebenar 5 larian.**
  Poll tangkapan stabil diuji 5 larian berturut-turut: **68/0 SEMUA
  LULUS setiap larian** (105.6s / 106.3s / 106.6s / 108.3s / 106.0s),
  sifar flak dalam keadaan RDP berbeza. 11 tangkapan setiap larian
  (sama seperti sebelum). Julat masa 72–108s antara sesi ialah varian
  persekitaran RDP (bilangan cubaan tangkapan), bukan tingkah laku
  poll. Kiraan 15 → 16.

## LANJUTAN 9 — semak #16 kiraan semakan automatik (komit 17)

- **Komit 17 (`09dc071`) — Semak #16: kiraan semakan automatik.**
  semak.py kini mencetak jumlah di akhir larian (391 semakan, 15
  bahagian) dan semak #16 baharu mengesahkan tuntutan README terhadap
  kiraan runtime — GAGAL bila README lapuk; lompat (NOTA) bila
  hadis.db tiada atau dipanggil bersendirian. Kiraan definisi bahagian
  = tajuk "N. " biasa (15, kekal selepas semak 16; #8 pecah ke
  8b–8o). Pembilang `lulus()`/`tajuk()` di-reset dalam `lari()`;
  semak 16 lompat bila dipanggil bersendirian (pembilang tidak
  lengkap); mutasi #35 baharu menjalankan semak.py penuh sebagai
  subproses (~30s) untuk mengunci kiraan. uji_negatif_8z
  52 → **54/0 (35 cabang)**; README kekal **391 semakan** + "52/0 —
  34 cabang" → "54/0 — 35 cabang" (kiraan per-dokumen berubah ikut
  bilangan fail .md — semak #8m lulus per fail). Kiraan 16 → 17.

## LANJUTAN 10 — suite muktamad + tutup hari (komit 18)

- **Komit 18 (`8725872`) — Suite muktamad + tutup hari.** Suite
  pra-hantar penuh selepas semak #16: **13/13 SEMUA LULUS (387.5s)** —
  turun dari 401.8s (semak.py 15.9s dengan semak #16 · uji_negatif
  24.4s · uji_visual_sebenar 64.2s dalam suite · semak_dokumen_ui
  10.5s; tiada proses yatim). Semak #12/#15/#16 hijau selepas komit 17
  (`09dc071`). Kiraan 17 → 18; semua dokumen diselaraskan: MULA_SINI
  ringkasan + 'Sesi Terakhir' (komit 1–18), sesi_index (kiraan telus
  18 + baris 18), mutasi #34 ke "18 commit".

## LANJUTAN 11 — pembetulan rekod tarikh (langkah-B, `c97d028`)

- **Langkah-B (`c97d028`) — Pembetulan rekod tarikh 17→18 Ogos.**
  Jam sistem menunjukkan semua kerja sesi ini (cdf4e63..8725872)
  berlaku pada **17 Ogos 2026** — tiada hari "18 Ogos" sebenar.
  Rekod "18 Ogos" yang dibuka pada `e60a74d` (19:30, masih 17 Ogos)
  dibetulkan: PERUBAHAN_18OGOS.md diserap ke PERUBAHAN_17OGOS.md
  (LANJUTAN 6–10 di atas), SESI 18 OGOS dibuang dari sesi_index,
  MULA_SINI 'Sesi Terakhir' + ringkasan dikunci ke **17 Ogos (18
  commit)**, mutasi #27/#30/#34/#35 disasarkan semula ke rentetan
  17 Ogos/18 commit, README 392→**391 semakan** (semak #8m lulus per
  fail .md — fail dibuang = −1). Gate: semak.py SEMUA LULUS (391
  semakan) · uji_negatif_8z **54/0** · semak_dokumen_ui **110/0**.
  Komit ini ialah **langkah-B** — tidak dikira dalam 17 Ogos (18
  sebenar kerja − 1 langkah-B = 18). Hari 17 Ogos DITUTUP — 18
  commit.

## LANJUTAN 12 — peraturan tarikh sistem (dalam semak #12) + finalisasi + audit rekod
(langkah-B kedua, `bb97f42`)

- **Langkah-B kedua (`bb97f42`) — peraturan tarikh sistem + audit
  rekod 17 Ogos.** (1) **Peraturan tarikh sistem ditambah ke semak
  #12** `semak_sesi_terakhir`: 'Sesi Terakhir' tidak boleh
  mendahului tarikh sistem (rekod "18 Ogos" pernah dibuka pada 17
  Ogos) — julat sah git ≤ tajuk ≤ hari ini; dikunci mutasi **#36**
  (tajuk → 1 Januari 2099, tarikh jauh supaya tidak lapuk) →
  uji_negatif **55/0 (36 cabang)**; semak.py **392 semakan (15
  bahagian)**. (2) **Finalisasi** baris langkah-B pertama →
  `c97d028`. (3) **Audit rekod 17 Ogos**: setiap hash dalam jadual
  18 baris disahkan wujud dalam git log dan bertarikh 2026-08-17
  (18/18); tiada tuntutan rekod hari berikutnya sebagai tarikh
  tajuk/kiraan/kerja dalam dokumen hidup (nota pembetulan berpetik
  dibenarkan); fail log harian lama dipadam. Gate: semak.py SEMUA
  LULUS (392 semakan, 15 bahagian) · uji_negatif_8z **55/0** ·
  semak_dokumen_ui **110/0**. Tidak dikira (langkah-B).

## LANJUTAN 13 — suite penuh muktamad dengan semak #12 baharu
(langkah-B ketiga, `c5142ef`)

- **Langkah-B ketiga (`c5142ef`) — suite penuh + penutup rekod.**
  Suite pra-hantar penuh dengan semak #12 peraturan tarikh sistem:
  **13/13 SEMUA LULUS (453.0s)** — semak.py 20.6s · uji_negatif
  28.5s (55/0) · mockup 33.2s (130/0) · piksel 65.3s · sebenar 106.2s
  (68/0) · tema 69.3s · bandingan 10.2s · lompat 6.8s · end-to-end
  41.0s · tangkapan 30.8s · draf 2.0s · tersimpan 26.4s · dokumen_ui
  9.7s (110/0); tiada proses yatim.
  **Dua kegagalan transien suite direkod (persekitaran RDP, bukan
  regresi):** larian 1 — uji_visual_sebenar 67/1 (tangkapan
  `sebenar_fon_sederhana` 10,906 B separa); larian 2 — uji_visual_
  mockup exit-code bukan sifar ("Loading weights" berterusan selepas
  ringkasan 130/0). Kedua-dua LULUS bersendirian (68/0, 130/0, exit
  0) dan suite LULUS penuh pada percubaan ketiga (453.0s) — konsisten
  dengan sejarah flak RDP (rantaian uji_visual_sebenar 172→74s,
  julat 72–108s). Kiraan 17 Ogos kekal **18 commit** (langkah-B ini
  tidak dikira). Gate: semak.py SEMUA LULUS (392 semakan, 15 bahagian)
  · uji_negatif_8z **55/0** · semak_dokumen_ui **110/0** · pokok
  bersih.

