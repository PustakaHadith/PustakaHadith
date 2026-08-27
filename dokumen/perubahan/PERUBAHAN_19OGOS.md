# Perubahan 19 Ogos 2026

> Log ringkas perubahan pada 19 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md`. Versi apl kekal **1.0**.

## Kandungan sesi

- **Komit 1 (`b292515`) — Perubahan asas apl.** Tema dikurangkan kepada
  **2 Neutral** (gelap + terang; Kertas/Terang/Ikut sistem dibuang);
  butang 'Saiz antara muka' dibuang dari panel Tetapan; dialog
  disclaimer baharu (`ui/disclaimer.py`) papar sekali pada startup;
  carian nombor hadis pada halaman kitab buka detail terus.
  `semak_dokumen_ui` 110→109; suite 14/14 (414.4s).

- **Komit 2 (`e6d867b`) — Disclaimer selepas model + tajuk sepadan.**
  Disclaimer dipindah selepas splash (bukan sebelum); flag
  anti-dwicalla `_buka_dijalankan`; tajuk splash/disclaimer/header
  sepadan: Pustaka(bold teal) Hadis(light teal) v1.0; header v1.0
  inline satu label; warna disclaimer guna palet tema.

- **Komit 3 (`6c9f855`) — Fix disclaimer pythonw.exe.** Punca:
  `splash.close()` → `setQuitOnLastWindowClosed(True)` (lalai) → Qt
  quit event loop → `QTimer.singleShot(0)` tidak fire. Pembetulan:
  `setQuitOnLastWindowClosed(False)` + disclaimer dulu (sebelum
  splash) + 200ms delay; dialog 540×600; papar setiap kali larian;
  buang semua debug trace.

- **Komit 4 (`5dd6990`) — Tentang Pustaka Hadis table.**
  QTableWidget 2 lajur untuk Kandungan + Sumber dan atribusi; grid
  line, padding, warna tema; hyperlink pautan HTML dalam sel.

- **Komit 5 — Baiki gate semak.py (atribusi jadual + kiraan semakan).**
  Komit penutup 19 Ogos (`55c17f4`) merekod 3 kegagalan sedia ada;
  dua kekal selepasnya dan kini DITUTUP:

  1. **Semakan atribusi 8aa (`semak_deklarasi`)** — jangka ayat teks
     lama ("Teks hadis, terjemahan Melayu & Indonesia: ", dsb.) yang
     tidak wujud lagi selepas komit 4 (jadual QTableWidget memecahkan
     ayat kepada 2 sel). Diselaraskan ke format JADUAL: semak label
     sel kiri + nama sumber (`hadis.my`, `fawazahmed0/hadith-api`,
     `SemakHadis.com`) pada `ui/deklarasi.py` + ayat penuh ternormal
     pada `dokumen/rujukan/DEKLARASI.md` (3 pasangan, tidak berubah).
  2. **Kiraan semakan 394** — semak #16 (README automatik): README +
     ringkasan MULA_SINI dikemas ke 394 semakan; mutasi #35
     (uji_negatif_8z) disasarkan semula (394→391).
  3. **Mutasi #27/#30/#34/#36 uji_negatif_8z** — sasaran rentetan
     lapuk ("Sesi Terakhir — 18 Ogos 2026", "Kerja 18 Ogos — 8
     commit", "**8 commit** pada 18 Ogos") disasarkan semula ke
     rentetan 19 Ogos semasa (5 commit).
  4. **PERUBAHAN_19OGOS.md dicipta** — log harian 19 Ogos belum wujud
     walaupun dirujuk MULA_SINI (komit `55c17f4` hanya mengemas
     MULA_SINI + sesi_index).

  Gate: semak.py **394 semakan SEMUA LULUS** · uji_negatif_8z 55/0 ·
  semak_dokumen_ui 109/0 · pokok kerja bersih.

## Keputusan pengguna 19 Ogos

- **#7 kunci API hadis.my** — DIABAIKAN buat masa ini; kekal AKTIF
  sengaja dan direkod sebagai tertangguh §8.
- **Jurang Tafsir 843** — DIABAIKAN buat masa ini; kekal dipantau
  (MyHadith JAKIM + IslamHouse Melayu).
- **Installer (Fasa 0)** — dokumen kawalan `PLAN_BINA_EDARAN.md` +
  panduan `INSTALLER.md` + rekod keputusan `BANDING_INSTALLER.md` +
  bahan perbincangan `PERBANDINGAN_INSTALLER.md` dibaca penuh;
  keputusan Fasa 0 menunggu pengguna.

## Komit penutup (langkah-B) tambahan

- **Workflow lengkap ditambah ke `INSTALLER.md` (§1a)** — peta aliran
  Fasa 0→6 dengan gate setiap fasa, jadual langkah/kerja/output/gate/
  rujukan, 6 soalan Fasa 0 dan 6 peraturan aliran. Kiraan semakan kekal
  394 (semak #16 stabil selepas komit penutup; pokok bersih).

- **Fasa 0 DILULUSKAN pengguna (19 Ogos 2026)** — 6 keputusan skop:
  (1) bundel model e5 + indeks FAISS untuk profil ujian = ya; (2) Store
  = saluran utama = ya; (3) Inno EXE = sekunder/penguji = ya; (4) akaun
  Partner Center = WAJIB di Fasa 5 (daftar sekarang, percuma, tempah
  nama Pustaka Hadis segera); (5) portable ZIP = untuk penguji dalaman
  sahaja; (6) wizard permulaan = bina sebelum beta. Direkod dalam
  `PLAN_BINA_EDARAN.md` Fasa 0 + `PERBANDINGAN_INSTALLER.md` §5.
  Gate Fasa 0: LULUS. Langkah seterusnya: Fasa 1 (pisahkan laluan data).

## Status — 19 OGOS DIBUKA SEMULA (5 commit)

19 Ogos DIBUKA SEMULA — **5 commit kerja** (4 asal + komit 5 ini;
penutup `55c17f4` + `79675fe` + `b5bbff2` langkah-B tidak dikira,
8 sebenar − 3). Kiraan telus: 14 Ogos = 36 commit · 15 Ogos = 14
commit · 16 Ogos = 16 commit (18 sebenar − 2 langkah-B) · 17 Ogos =
18 commit (22 sebenar − 4 langkah-B) · 18 Ogos = 8 kerja + 2 langkah-B
· 19 Ogos = **5 commit**.