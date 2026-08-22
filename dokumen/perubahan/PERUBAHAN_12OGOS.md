# Perubahan 12 Ogos 2026 — Sesi 55 (rujukan)

> Log ringkas perubahan pada 12 Ogos 2026 untuk rujukan pantas.
> Butiran penuh: `dokumen/sesi/sesi_index.md` (entri Sesi 55 di hujung
> fail). Versi apl kekal **1.0** — kerja ini ialah penambahbaikan dalam
> edaran semasa, bukan perubahan versi.

## Kandungan Sesi 55

Sesi ini membandingkan **4 mockup HTML halaman detail** (bukhari1,
nasai2117, abudaud4177, ibnumajah2094) dan melaksanakan keputusannya
dalam aplikasi PyQt5:

1. **Susun atur dua lajur** — Arab | terjemahan sebelah-menyebelah,
   tab ARAB/TRANSLITERASI dalam lajur Arab, tab bahasa dalam lajur
   terjemahan, darjat/huraian **TERBUKA** (`ui/pages_detail.py`).
2. **Cip warna ikut makna** — hijau (Sahih/Muttafaq/Hasan/صحيح/حسن),
   merah (Palsu/Munkar/Batil/Dusta), amber (Lemah/Daif/Syaz); tiada
   padanan = neutral. Palet dari theme.py (`_warna_cip`).
3. **Palet kertas hangat mockup DITERIMA PAKAI** — `#f4f1ea`/`#1e1d1a`,
   aksen hijau menggantikan TEAL biru; teks sekunder dituna untuk
   kontras AA; cip guna heks mockup tepat (terang + gelap).
4. **Padanan kecil** — nama "Sahih al-Bukhari" + prefix "Bab:" supaya
   tajuk/breadcrumb/baris bab sepadan mockup bukhari#1.
5. **Penstabilan ujian visual** — `skrin_fizikal()` dalam
   `uji_visual_sebenar.py` kini mengesahkan kecerahan tangkapan sepadan
   tema sebenar app DAN halaman cukup terisi (warna unik ≥ 150),
   dengan force hide/show pada cubaan ke-4 — 65/0 pada dua larian
   berturut-turut.
6. **Finalise** — kod mati `_pra_muat_model` (pendekatan lama muat
   model thread utama yang tiga kali terbukti gagal) **dibuang**;
   penggantinya `PreloadWorker` (QThread) memang sudah aktif. Semak.py
   8k mengunci penggantian, 8v mengunci `_warna_cip`, 10aa mengunci
   logo pada palet.

## Penemuan penting

- **Punca sebenar semua "tersangkut" ujian** (larian pertama lambat):
  dialog deklarasi MODAL muncul 300ms selepas app dilancarkan.
  `semak.py` menulis `user_settings.json` minima lalu memadam fail
  asal → bendera `deklarasi_dibaca` hilang → dialog menyekat ujian
  offscreen (tiada pengguna untuk klik). Dibuktikan dengan
  `faulthandler` + disahkan (tetapkan bendera → ujian serta-merta
  lulus). `semak.py` kini **menyimpan + memulihkan tetapan asal** dan
  menyenaraikan `user_settings.json` sebagai data kerja.
- **Flak tangkapan skrin persekitaran** (ImageGrab bingkai basi/permulaan
  Windows) — dilemahkan dengan retry kecerahan + isian halaman + force
  hide/show, bukan isu kod.

## Keputusan ujian penuh

| Ujian | Keputusan |
|---|---|
| `semak.py` | SEMUA LULUS (8k pramuat + 8v cip + 10aa logo) |
| `uji_visual_mockup.py` | **130/0** (4 mockup: kontrak + geometri + kandungan + warna cip) |
| `uji_bandingan.py` | **48/48** |
| `uji_lompat_fungsi.py` | **48/48** |
| `uji_end_to_end.py` | **18/18** |
| `uji_tukar_tema.py` | **19/19** |
| `uji_visual_sebenar.py` | **65/0** (2× berturut-turut) |

## Fail yang diubah

| Fail | Perubahan |
|---|---|
| `ui/pages_detail.py` | Susun atur dua lajur + tab per lajur + darjat terbuka + `_warna_cip`/`_warnai_cip` + prefix "Bab:" |
| `ui/theme.py` | Palet kertas hangat diterima pakai + warna cip heks mockup + nama "Sahih al-Bukhari" |
| `ui/app_qt.py` | Komen `__init__` dikemas; kaedah mati `_pra_muat_model` dibuang |
| `scripts/bina_logo.py` | Palet logo → hijau mockup (TEAL_DARK/CARD_BG/AMBER_TEXT) |
| `semak.py` | Pemulihan `user_settings.json` + 8v `_warna_cip` + 10aa logo + 8k pramuat QThread |
| `uji_visual_mockup.py` | 4 kes mockup + semakan kandungan + warna cip (130/0) |
| `uji_visual_sebenar.py` | Retry tangkapan stabil (kecerahan + isian + hide/show) |
| `uji_bandingan.py` | Nama kitab "Sahih al-Bukhari" |
| `dokumen/manual/MANUAL_REFERENSI_DEV.md` | Senarai semak pra-hantar dikemas + peta dokumen (TRANSFORMASI_DETAIL) |
| `dokumen/manual/MULA_SINI.md` | Seksyen 3 mendokumenkan `uji_pra_hantar.py` |
| `dokumen/manual/TRANSFORMASI_DETAIL.md` | **BAHARU** — transformasi paparan detail LAMA → BARU + tangkapan skrin |
| `dokumen/imej/*.png` | **BAHARU** — tangkapan skrin lama (7 Ogos) + baharu (12 Ogos), nasai#4934 |
| `bina_tangkapan_dokumentasi.py` | **BAHARU** — jana semula tangkapan skrin dokumentasi |
| `dokumen/sesi/sesi_index.md` | Rekod Sesi 55 penuh + header "Sesi Terakhir" |
| `mockup/*.html` | 4 spesifikasi reka bentuk (bukhari1/nasai2117/abudaud4177/ibnumajah2094) |

## 10 commit sesi ini (12 Ogos 2026)

| Commit | Kandungan |
|---|---|
| `2972de2` | Laksana Sesi 55 sepenuhnya: halaman detail dua lajur + warna cip ikut makna + ujian mockup 130/0 |
| `50290a9` | Terima pakai palet kertas hangat mockup + baiki punca "hang" ujian (dialog deklarasi) |
| `e94f86d` | Stabilkan tangkapan skrin uji_visual_sebenar + kunci warna logo pada palet |
| `2e7416d` | Finalise: buang kod mati `_pra_muat_model` + kunci penggantian QThread |
| `878feac` | Dokumentasi Sesi 55: PERUBAHAN_12OGOS.md + CHANGELOG dikemas |
| `90571d4` | Ujian perbandingan piksel `uji_visual_piksel.py` (53/0) |
| `00b9f1f` | Kepekaan mutasi semakan 8k (33/0) |
| `af3b623` | Rekod ujian visual final: 9 ujian, 412 semakan, 0 gagal |
| `7c12ddd` | Mutasi 8v/10aa + pra-hantar automatik + profil semak.py (40/0) |
| `0491a73` | Optima semak.py (cache mtime 16.3→12.8s) + penstabilan uji_visual_mockup (130/0 ×3) |

## Log penuh perubahan `.md` sepanjang sejarah

```bash
git log --format="%h %ad %s" --date=short -- "*.md"
```
