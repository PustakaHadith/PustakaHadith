# Perubahan 28 Ogos 2026

## Perubahan UI — Bar Tindakan Halaman Detail Hadis
- Teks "Lapor ralat | Kongsi | Salin" ditukar kepada 3 ikon monokrom
  (flag / kongsi / salin). `ui/widgets.py` (`IconActionButton` + `_line_icon`),
  `ui/pages_detail.py`. Commit `a51996d`.
- Kemudian ditukar kepada **4 ikon**: WhatsApp, Salin, Dengar (TTS),
  Simpan (bookmark) menggantikan teks. Commit `83414d5`.
- Buang baris atas emoji duplikat (WhatsApp / Salin / Dengar + butang Simpan
  teks) — elak duplikasi dengan bar bawah ikon. Commit `c85e11e`.
- Ikon WhatsApp ditukar kepada logo gelembung sembang + telefon.
  Commit `c869e55`.

## Perubahan UI — Rak Kitab (Jilid Dipilih)
- Jilid dipilih **kekal terangkat** + sempadan oren `#FF9F1C` + lingkaran
  bercahaya oren. `ui/pages_rak.py` (`JilidRak`, `paintEvent`, `set_dipilih`).
  Commit `3cf640e`.
- Animasi angkat ditukar dari `QPropertyAnimation` ke tween `QTimer`
  (angkat boleh diharap, tidak bergantung pyqtProperty). Commit `bbcb78d`.
- Fix: jilid dipilih **KEKAL terangkat** bila tetikus keluar — `leaveEvent` /
  `enterEvent` guna `_kemas_angkat` (angkat = 1 jika `dipilih OR hover`).
  Commit `5b55535`.

## Siasatan "List Bab Hilang" (Sidebar Kitab)
- Laporan: bahagian "PILIH BAB" **tiada** dalam sidebar kiri bila masuk ke
  kitab (pengguna buka via EXE).
- Data `bab` **wujud**: jadual `bab` ada 31,325 baris (6,721 Bukhari);
  `get_bab_list("bukhari")` pulang **97 entri** dalam mod sumber (uji
  terus `HadisAPI`). Bab hilang BUKAN isu data.
- Punca: EXE lama (dibina 13:03) tidak mengandungi kod PILIH BAB. EXE
  **dibina semula** dari sumber terkini: `dist\PustakaHadith\PustakaHadith.exe`
  (74.2 MB; binaan ~35 minit — PyInstaller rebundle penuh torch/transformers/
  faiss setiap kali, bukan tambahan).
- **Nota pemeriksaan**: carian string mentah dalam `.exe` yang pulang `-1`
  TIDAK membuktikan kod tiada — arkib PKG di-zlib-compress. Pengesahan
  muktamad = uji EXE baru (pengguna).

## BERITA GEMBIRA — Kebenaran Bertulis hadis.my
- **Kebenaran bertulis diterima dari hadis.my (28 Ogos 2026)** untuk
  membundel `hadis.db` (data dari service.hadis.my) dalam binaan apl.
- Gerbang lesen (PERUBAHAN_27OGOS: "Kebenaran hadis.my diperlukan sebelum
  bundel data") kini **TERBUKA**.
- **Tangguh pelaksanaan**: pengguna arahkan bundel data kemudian — masih ada
  beberapa perkara dalam apl perlu dibetulkan dulu. Tunggu arahan.

## Status / Tertangguh
- Implementasi bundel `hadis.db` (kembalikan `hadis.db` + `hadis_faiss.index`
  + `hadis_id_map.pkl` ke `PustakaHadith.spec` `datas`) — **TANGGUH** sehingga
  arahan pengguna.
- EXE baru perlu diuji pengguna (sahkan bahagian PILIH BAB muncul).
- Beberapa pembaikan UI / apl lain masih dalam senarai pengguna.
