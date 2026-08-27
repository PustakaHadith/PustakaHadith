# Perubahan 11 Ogos 2026 — Sesi 54 (rujukan)

> Log ringkas perubahan fail `.md` pada 11 Ogos 2026 untuk rujukan
> pantas. Butiran penuh: `dokumen/sesi/sesi_index.md` (entri Sesi 54).

## Fail `.md` yang diubah (11 Ogos 2026)

| Fail | Perubahan |
|---|---|
| `dokumen/sesi/sesi_index.md` | Entri Sesi 54 + lampiran (7 kali dikemas sepanjang sesi) |
| `dokumen/manual/MANUAL_REFERENSI_DEV.md` | Senarai semak pra-hantar: kesemua 6 ujian visual + `uji_negatif_8z.py`; baris versi → v1.0 |
| `MANUAL_PENGGUNA.md` | Versi rujukan → v1.0 |
| `MANUAL_PENGGUNA_EN.md` | Reference version → v1.0 |
| `dokumen/manual/MULA_SINI.md` | Versi semasa → v1.0 |
| `dokumen/rujukan/PANDANGAN_RISIKO.md` | Jadual versi + ciri → v1.0 |
| `dokumen/perubahan/PERUBAHAN_11OGOS.md` | Fail ini (rujukan) |
| `dokumen/perubahan/CHANGELOG.md` | Fail rujukan baharu — log perubahan versi (1.0–1.3 + reset) |
| `dokumen/manual/manual/manual/MANUAL_INSTALASI.md` | Manual baharu — pemasangan pengguna (pecah dari MANUAL_PENGGUNA.md) |
| `dokumen/manual/manual/manual/MANUAL_PENGGUNAAN.md` | Manual baharu — cara guna aplikasi (pecah dari MANUAL_PENGGUNA.md) |

## Kandungan Sesi 54

- Penyatuan corak koma ribuan + sempadan int menjadi `_label_kiraan`
  (banner + kad); kotak lompat kekal berasingan (format julat).
- Semakan statik 8w/8x/8y/8z mengunci fungsi kongsi, tiada literal
  hanyut, kesemua ujian visual kekal + dirujuk dalam senarai semak.
- Ujian visual skrin sebenar: **138 lulus, 0 gagal** (6 fail).
- Ujian negatif berulang: **21 lulus, 0 gagal** (8z/8w/8x/8l/8p/8q/8r)
  dengan pulihan byte-tepat.
- Pembetulan: `getdata()` → `get_flattened_data()` (deprecation
  Pillow); bbox tangkapan `uji_visual_sebenar.py` (skrin penuh →
  tetingkap); pengawal manual hilang dalam 8z (GAGAL bersih, bukan
  ranap).
- Manual pengguna dipecah dua: `MANUAL_PENGGUNA.md` →
  `dokumen/manual/manual/manual/MANUAL_INSTALASI.md` (pemasangan) + `dokumen/manual/manual/manual/MANUAL_PENGGUNAAN.md` (cara
  guna); `MANUAL_PENGGUNA_EN.md` digugurkan (terjemahan manual lama).

## Versi apl → 1.0

Apl **rasmi (official)** (11 Ogos 2026): `VERSI.py` ditetapkan
`VERSI = "1.0"` (dahulu 1.3). Pernyataan "versi semasa v1.3" dalam
5 dokumen dikemas ke v1.0; penanda sejarah (README `(v1.1/v1.2/v1.3)`,
komen `CIRI` dalam VERSI.py, log sesi) dikekalkan sebagai rekod.

Disahkan pada skrin sebenar (11 Ogos 2026): header app memapar `v1.0`
dan skrin pemula memapar `Versi 1.0 — carian kata kunci + makna (AI)`
(8 semakan, 0 gagal); tangkapan `bukti_visual/versi_1_0.png`. Log
perubahan versi penuh: `dokumen/perubahan/CHANGELOG.md` (fail baharu).

## 8 commit sesi ini (11 Ogos 2026)

| Commit | Kandungan |
|---|---|
| `cfcac39` | Satukan `_label_kiraan` (banner+kad) + semakan 8w/8x/8y + audit `set_total` |
| `d66f0c3` | `getdata` → `get_flattened_data` + senarai semak visual penuh + lampiran Sesi 54 |
| `5718c45` | Semakan 8z: kunci kesemua ujian visual kekal + dirujuk |
| `7c4f37e` | Pengawal 8z (manual hilang → GAGAL bersih) + ujian negatif 8z |
| `4a08e80` | Bbox tangkapan sebenar + ujian negatif 8w/8x + penutup Sesi 54 |
| `e6690a1` | Perluas ujian negatif ke 8l/8p/8q/8r (21 lulus) |
| `dbfa420` | Header "Sesi Terakhir": skop penuh Sesi 54 |
| `66a2dee` | Reset versi apl ke 1.0 (belum official) + fail rujukan dokumen/perubahan/PERUBAHAN_11OGOS.md |

## Log penuh perubahan `.md` sepanjang sejarah

```bash
git log --format="%h %ad %s" --date=short -- "*.md"
```
