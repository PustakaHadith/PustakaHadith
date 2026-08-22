# Pandangan & Risiko — Pustaka Hadis

> Ditulis 7–8 Ogos 2026 (Sesi 29). Hasil analisis keseluruhan projek.
> Bukan senarai tugasan wajib — konteks untuk sesi akan datang supaya
> keputusan diambil sedar risiko.
> Sumber utama lain: `dokumen/manual/MULA_SINI.md`, `dokumen/manual/MANUAL_REFERENSI_DEV.md`,
> `dokumen/sesi/sesi_index.md`.

---

## 1. `ui/app_qt.py` terlalu besar (~100 KB / 2,428 baris)

Setiap ciri baharu ditambah ke satu fail yang terus membesar. Risiko:

- Sukar dibaca/diurus; konflik edit meningkat
- Peraturan MULA_SINI #4 ("jangan buang import 'unused' dalam `ui/*.py` —
  ia sasaran `apply_theme()`") menjadikan refactor berisiko

Cadangan: pecah halaman search/detail/kitab ke modul berasingan (corak
`ui/pages.py` sudah ada). Lakukan SELEPAS ujian mesin sebenar, bukan kini.

**✅ SELESAI 8 Ogos 2026 (Sesi 30):** refactor 5 langkah dilaksanakan atas
arahan pengguna — `ui/helpers.py` + 6 mixin halaman (`pages_kitab`,
`pages_carian`, `pages_detail`, `pages_tersimpan`, `pages_tetapan`,
`pages_home`). `app_qt.py` 2,428 → **504 baris (inti sahaja)**.
Disahkan: `semak.py` SEMUA LULUS + 8 suite ujian (termasuk `uji_tukar_tema`
19/19 dan ujian visual sebenar `uji_visual_sebenar` 14/14 +
`uji_visual_bandingan` 2/2). Import warna hanya dibuang bila benar-benar
mati dan modul penerimanya didaftar dalam `_THEMED_MODULES` (peraturan #4
dipatuhi).

---

## 2. Salinan `app_qt.py` dalam folder arkib/sandaran

Dulu wujud di `sandaran_1300/`, `sandaran_1302/`, `tampalan_preload/`.
Risiko: tersilap edit salinan lama dan menganggap ia kod aktif.

**✅ DITUTUP 8 Ogos 2026:** ketiga-tiga folder di-gitignore dan
`tampalan_preload` dibuang dari git (`git rm -r --cached`).
**9 Ogos 2026: folder dipadam** — kandungan redundan dengan git history
(salinan app_qt.py monolitik lama yang sudah dipecahkan ke mixin pada
Sesi 30; semakan 8m semak.py mengesahkan tiada lagi kod hidup di situ).
Pengawal: semak.py mengimport daripada `ui/app_qt.py` (aktif);
git tidak lagi menjejak mana-mana salinan arkib.

---

## 3. Dokumentasi ketinggalan versi

- `dokumen/manual/MANUAL_REFERENSI_DEV.md` sebelum ini "v1.0", `dokumen/manual/MULA_SINI.md` v1.3
- `dokumen/sesi/sesi_index.md` kini lengkap hingga Sesi 29

Cadangan: kemas kini versi + peta dokumen apabila menutup sesi, supaya
tiada dokumen bercanggah.

**✅ DITUTUP 8 Ogos 2026 (Sesi 30):** `dokumen/manual/MANUAL_REFERENSI_DEV.md` v1.3,
`dokumen/manual/MULA_SINI.md` v1.3, `dokumen/sesi/sesi_index.md` lengkap hingga **Sesi 30**,
`dokumen/rujukan/PANDANGAN_RISIKO.md` sendiri dikemas (risiko #1/#2/#3), peta dokumen
(MANUAL_REFERENSI_DEV §12) kini termasuk `dokumen/rujukan/RANCANGAN_REFACTOR.md`.

---

## 4. Skrip ujian: crash 0xC0000409 palsu daripada pengekodan emoji

Penyiasatan Sesi 29 membuktikan crash `EXIT=-1073740791` (0xC0000409)
dalam skrip ujian `uji_cari_*.py` ialah fail-fast daripada `print()` emoji
(🤖 dalam `search_info.text()`) ke stdout cp1252 dalam gelung acara Qt —
BUKAN bug aplikasi (QThread/torch/pra-muat). try/except tidak menangkapnya.

Risiko berulang: crash disalah anggap sebagai bug sebenar dan menghabiskan
masa siasatan. Pengawal: semua skrip ujian baharu MESTI set
`sys.stdout.reconfigure(encoding="utf-8")` atau `PYTHONIOENCODING=utf-8`.

---

## 5. Lesen SemakHadis belum disahkan bertulis

SemakHadis.com tidak menyatakan lesen semula data secara eksplisit
(direkod sejak Sesi 18.8). Atribusi dipaparkan. Risiko: isu hak cipta
sebelum edaran komersial. Tindakan: dapatkan kebenaran bertulis sebelum
pengedaran komersial.

---

## 6. Kunci API kekal AKTIF dalam repo

Sengaja (keputusan pengguna 31 Jul, pelan developer). Risiko penyalahgunaan
kuota. Pengawal: `dokumen/rujukan/REVOKE_KUNCI.md` — jangan masukkan kunci baru ke kod.

---

## 7. SemakHadis liputan terhad (3.3%)

4,237/62,169 hadis popular sahaja. Siling tetap selagi tiada sumber BM
terbuka lain yang sah (Fasa 4A ditutup atas lesen).

---

## 8. Ringkasan status (selepas semakan penuh)

| Perkara | Nilai |
|---|---|
| Versi | v1.0 |
| Hadis | 62,169 (9 kitab) |
| `semak.py` | SEMUA LULUS (169 OK, 0 GAGAL) |
| `semak_versi.py` | 23/23 ciri v1.0 hadir |
| `uji_lompat.py` | 67/67 lulus |
| Kualiti data | kukuh; 3 pepijat klasik Qt/torch/QThread selesai dengan bukti |
| Ciri terkini | carian gabungan, draf AI, tab Sebelah 3 bahasa, splash, lompat hadis |

---

## 9. Keputusan pengguna

- **Bahasa Melayu Malaysia**, bukan Indonesia
- Bila diminta *"analisis sahaja"* — jangan ubah kod
- Pengguna mahu "download dan jalan" — hantar ZIP siap-jalan
