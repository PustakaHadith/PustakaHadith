# Perubahan 31 Julai 2026 — v2026.07.30-9 → -10 → v2026.07.31-11

Ringkasan satu hari. Arkib penuh: `sesi_index.md` (Sesi 10, HadeethEnc).

---

## 1. Hasil terbesar: Fasa 4 (Huraian) mendapat sumber SEBENAR — HadeethEnc

Fasa 4 sebelum ini hanya mampu memberi nota automatik berasaskan topik
(`status="auto"` + penafian). Pengguna mahukan huraian ulama, tetapi
Fath al-Bari tersekat (penomboran hanyut, `core/syarah_source.py`).

**Penyelesaian: HadeethEnc.com** (projek IslamHouse) — hadis sahih +
penjelasan ringkas dalam Bahasa Melayu. Tiada kunci API.

```
hadis.db (arab)  --padan matn-->  .cache_he/{he_id}.json  --sumber-->
                                    explanation/hints (Melayu)
```

Kunci padanan ialah **teks Arab dinormalisasi** (matn), BUKAN ID — hadis.my
dan HadeethEnc tidak berkongsi penomboran langsung.

### Hasil akhir

| ukuran | nilai |
|---|---|
| hadis sumber ber-BM | **147** (dari ~40,000 hadis HadeethEnc) |
| cache tempatan | `.cache_he/` — 147 `.json`, muat turun sekali |
| padanan disimpan | **280** / 62,169 hadis (0.5%) |
| bukhari · muslim · abu-daud | 60 · 32 · 16 |
| tirmidzi · nasai · ibnu-majah | 12 · 19 · 22 |
| ahmad · darimi · malik | 107 · 10 · 2 |
| status UI | `dari_sumber` ✓ — huraian sebenar, bukan nota automatik |

---

## 2. Punca 404 API didiagnosis (jika tidak, kerja tersasar sehari)

Permulaan: enumerasi `list?language=ms` menghasilkan 2,328 ID, tetapi
banyak `one?language=ms` membalas **404**. Ujian diagnosis:

- `one?id=NNNN&language=ms` → 404 **hanya bila hadis itu tiada terjemahan
  Melayu**. Hadis wujud dalam Arab; `language=ar` berfungsi.
- `list?language=ms` **menyembunyikan** hadis tanpa BM — kategori yang sama
  memberi 8 item (ms) vs 100 item (en). Paginasi berbeza = pensampelan salah.
- 2,328 itu ialah bilangan ID dalam senarai ms, tetapi hampir semuanya
  tiada fail `one?language=ms` — senarai dan `one` memakai logik berbeza.

**Enumerasi betul:** `list?language=en` (452 kategori) + tapis medan
`translations[]` mengandungi `"ms"` → **147 unik**. Ditulis semula ke
`.cache_he/senarai_id.json`.

Dokumen ke `url_list()`: mesti `language=en`; `ms` mengubah paginasi.

---

## 3. Padanan MATN (bukan teks penuh, bukan ID)

### Mengapa matn?

Teks penuh hadis.my dan HadeethEnc berbeza: **sanad tidak sepadan**
(rantaian perawi berbeza), tetapi matn selepas penanda hampir sama.
Padanan pada teks penuh dihina oleh sanad.

### Penanda permulaan matn (ditemui secara empirik)

```
قال رسول الله   سمعت رسول الله   قال النبي
عن النبي        قال صلى الله     قالرسول
```

`_matn()` menormalisasi teks, cari penanda yang TERAKHIR, ambil teks
selepasnya. Kalau tiada penanda, matn = teks penuh dinormalisasi.

### Ambang

`JACCARD_MATN = 0.55`, diukur pada Bukhari #1,2,8,20,50:

```
betul  0.62 - 1.00
salah  0.04 - 0.48
```

Margin besar — 0.55 selamat di tengah.

### Lapisan padanan `padan()`

```
1. penuh   kunci teks penuh sama (jarang)   -> 1.00, "penuh"
2. matn    indeks kata jarang matn + Jaccard -> 0.55+, "matn"
```

Calon hanya layak jika kata jarang bertindih ≥35%; Jaccard dua hala pada
matn (sanad tidak dikira).

### Pengawal tolak calon hampir-sama (hadis asing)

Bukhari #50 memberi dua calon berbeza dengan skor hampir sama — matn
pembukaan dikongsi hadis lain. Pengawal: jika calon kedua skor ≥ `terbaik -
0.05` DAN Jaccard matn < 0.9, **tidak selamat → None**. Lebih baik tiada
daripada salah.

### Verifikasi luar talian

```
Bukhari #1   -> (66511, 0.8666, "matn")
Bukhari #50  -> (66515, 0.7758, "matn")
Bukhari #2,#8,#20 -> None   (betul — padanan HadeethEnc tiada BM)
```

---

## 4. Infrastruktur

### DB — migrasi 4

```sql
CREATE TABLE hadethenc (
    collection TEXT NOT NULL,
    hadis_id   INTEGER NOT NULL,
    he_id      INTEGER NOT NULL,
    jaccard    REAL    NOT NULL,
    kaedah     TEXT    NOT NULL,
    PRIMARY KEY (collection, hadis_id)
);
CREATE INDEX idx_hadethenc_he ON hadethenc (he_id);
```

`SKEMA_VERSI` 3 → 4.

### `sync_hadeethenc.py`

- Padan semua 9 kitab (buang baris lama `DELETE ... WHERE collection=?`
  dahulu, sama seperti `sync_english.py` — `INSERT OR REPLACE` sahaja
  tidak membersih padanan yang kini ditolak).
- `--semak` papar liputan per kitab.
- Cap versi pada baris pertama output.

### `core/phase4_exegesis.py`

- `_hadeethenc(collection, hadis_id, conn)` — baca padanan dari jadual
  `hadethenc` (`ambil`) + huraian dari cache (`huraian`). Pulangkan:
  `topic`=title · `teachings`=explanation · `summary`=hints ·
  `background`=sumber+attribution · `status="dari_sumber"` ·
  `disclaimer`=ATRIBUSI_HE.
- `exegesis()` kini `(text, collection, hadis_id, malay, conn)` dan
  **mengutamakan HadeethEnc** — jika padan, hadis itu MESTI papar huraian
  sebenar, bukan nota automatik.
- `ATRIBUSI_HE`: "Huraian ringkas oleh HadeethEnc.com (projek IslamHouse)
  untuk hadis berkenaan. Kandungan tidak diubah..."

### UI

- `PipelineWorker(hadis, conn=None, parent=None)`; `_huraian` lulus
  `conn=self._conn` ke `exegesis`.
- `ui/app_qt.py` lulus `conn` dari `self.api`.
- Pemetaan `"dari_sumber": "✓"` di UI.

---

## 5. Pepijat yang dibetulkan

| # | pepijat | pembetulan |
|---|---|---|
| 1 | `padan()` `_jaccard_set(set_soalan, ...split())` — `set` & `list` → `TypeError` (dua tempat) | balut argumen kedua dalam `set(...)` |
| 2 | `semak.py` semakan jadual `hadethenc` diletak SELEPAS `conn.close()` → `ProgrammingError` | pindah ke atas `conn.close()` |
| 3 | `list?language=ms` menyembunyikan hadis tanpa BM → senarai 2,328 palsu | guna `en` + tapis `translations[]` |

---

## 6. Fail

### Baharu

| fail | fungsi |
|---|---|
| `core/hadeethenc_api.py` | muat turun, indeks, padan matn, huraian, simpan/ambil |
| `sync_hadeethenc.py` | padan semua kitab → jadual `hadethenc` |
| `.cache_he/{he_id}.json` | 147 hadis HadeethEnc (tidak diedar — lihat semak) |
| `PERUBAHAN_31JUL.md` | dokumen ini |

### Diubah

| fail | perubahan |
|---|---|
| `db.py` | migrasi 4 (`hadethenc` + indeks); `SKEMA_VERSI` 4 |
| `core/phase4_exegesis.py` | `_hadeethenc()`; `exegesis(..., conn=None)`; `ATRIBUSI_HE` |
| `ui/workers.py` | `PipelineWorker(..., conn=None)`; `_huraian` lulus conn |
| `ui/app_qt.py` | lulus `conn` ke `PipelineWorker`; peta `dari_sumber`→✓ |
| `semak.py` | 8e `semak_hadeethenc()` (9 semakan); `.cache_he` dalam semak_bersih; semak migrasi `hadethenc` |
| `semak_db.py` | lajur `hdeethenc` + baris jumlah (280) |
| `VERSI.py` | `2026.07.30-9` → `-10`; +4 ciri `core.hadeethenc_api` |
| `MULA_SINI.md` | Fasa 4 HadeethEnc SIAP; keadaan projek dikemas kini |
| `RANCANGAN_4FASA.md` | Fasa 4 ✅; keutamaan paparan `dari_sumber` dahulu |
| `sesi_index.md` | Sesi 10 (HadeethEnc) — punca 404, padanan matn, integrasi |

---

## 7. Ujian ditambah (`semak.py` 8e)

1. `JACCARD_MATN` dalam julat 0.45–0.65
2. `_matn` menanggalkan sanad (teks berpenanda dan tanpa penanda)
3. hadis TULEN masih dipadan (teks penuh sama → "penuh")
4. hadis ASING yang berkongsi pembukaan matn → ditolak (kawalan #50)
5. `sync_hadeethenc.py` memadam baris lama sebelum simpan
6. `phase4_exegesis._hadeethenc` wujud
7. UI memetakan `dari_sumber` → ✓
8. `sync_hadeethenc.py` mencetak cap versi
9. migrasi 4 wujud (`hadethenc`)

---

## 8. Pelajaran

**Senarai API dan butiran API boleh guna logik penapisan berbeza.**
`list?language=ms` memberi 2,328 ID sedangkan `one?language=ms` 404 untuk
hampir semuanya. Jangan andaikan kedua-duanya memakai peraturan sama —
UJI padanan senarai ↔ butiran sebelum memuat turun 2,328 fail.

**"Tiada terjemahan" ≠ "hadis tiada".** 404 API selalunya bermaksud
sumber itu tidak wujud DALAM BAHASA yang diminta, bukan tidak wujud sama
sekali. Periksa dengan bahasa lain (`language=ar`) sebelum menganggap API
rosak.

---

## 9. Audit penuh `audit_eng.py --semua` — 100.0% disahkan

Seluruh 7 kitab CDN diaudit dengan saksi bebas (teks Indonesia hadis.my
vs CDN ind-*). Sebelum ini hanya Bukhari.

```
bukhari      100.0%   6,598/6,598    disyaki=0
muslim        99.9%   4,865/4,869    disyaki=4
abu-daud     100.0%   4,400/4,400    disyaki=0
tirmidzi     100.0%   3,526/3,527    disyaki=1
nasai        100.0%   5,331/5,332    disyaki=1
ibnu-majah   100.0%   4,269/4,269    disyaki=0
malik        100.0%   1,552/1,552    disyaki=0
---------------------------------------------
JUMLAH       100.0%  30,541/30,547   disyaki=6 (0.0%)
```

- ahmad & darimi tiada di CDN (tiada eng) — dilangkau.
- 6 disyaki: 2 `kata`, 1 `awalan`, 3 `penuh` pada muslim/tirmidzi/nasai.
- Lapisan `indo`/`indo~` purata 1.00 tetapi **bukan bukti bebas**
  (padanan memakai teks Indonesia yang sama).
- Keputusan pengguna: kunci API kekal AKTIF — pelan developer untuk
  ujian app (jangan revoke).

### 6 "disyaki" disiasat — semuanya POSITIF PALSU

Setiap kes diperiksa dengan membandingkan teks ARAB hadis.db vs CDN
`ara-*` pada nombor yang dipadan:

```
muslim #2567 -> #3503   jaccard_matn 0.992   PADAN
muslim #3581 -> #5005   (kaedah awalan, matn sama)  PADAN
muslim #4812 -> #6768   jaccard_matn 0.842   PADAN
muslim #5094 -> #6682   jaccard_matn 1.000   PADAN (kaedah penuh)
tirmidzi #3070 -> #3145 jaccard_matn 1.000   PADAN (kaedah penuh)
nasai   #3938 -> #4003  jaccard_matn 1.000   PADAN (kaedah penuh)
```

Punca audit menandakannya: `ind-*` dan `ara-*` TIDAK sejajar di 6 titik
itu. Contoh muslim: `ind #3502` KOSONG (hadis tanpa terjemahan Indonesia
ditinggalkan) → semua nombor selepasnya hanyut. Audit memadankan Arab ke
`ara #3503` dengan betul, kemudian membaca `ind #3503` yang sebenarnya
hadis LAIN.

Kesimpulan: padanan Inggeris untuk 6 hadis ini juga BETUL. Angka sebenar:
**30,541 disahkan, 0 padanan salah** (6 saksi Indonesia tersasar pada
nombor yang tidak sejajar).

Nota untuk audit akan datang: semak jajarkan `ara-*` dan `ind-*` dengan
padanan teks sebelum guna `ind-*` sebagai saksi pada lapisan Arab.

---

## 10. Belum selesai

| perkara | status |
|---|---|
| HadeethEnc liputan | hanya 280/62,169 (0.5%) — hadis sahih ber-BM sahaja |
| Fasa 4 lapisan A (Irsyad al-Hadith) | kebenaran + cara padan belum dikaji |
| Fasa 4B (Fath al-Bari) | TERSEKAT — lihat `PERUBAHAN_30JUL.md` §3 |
| `ind-*` vs `ara-*` jajarkan | penomboran hanyut di sesetengah titik — perbaiki audit |
| Atribusi HadeethEnc | perlu disahkan paparan dalam semua mod (gelap/terang) |

## 11. Kategori topik auto dipulihkan untuk hadis berpadan HadeethEnc

**Isu:** Pengguna laporkan maklumat "hadis ini berkaitan zakat/solat/pusaka"
hilang untuk hadis berstatus `dari_sumber`. `_hadeethenc()` hanya menerima
`(collection, hadis_id, conn)` dan memulangkan tajuk HadeethEnc sebagai
`topic` — tanpa pengesanan topik automatik.

**Punca:** `exegesis()` memanggil `_hadeethenc(collection, hadis_id, conn)`
tanpa lulus `text`/`malay`, jadi `_detect_topic()` tiada input untuk berfungsi.

**Pembetulan:**
- `_hadeethenc()` kini menerima `text`/`malay` dan memulangkan `kategori`
  (hasil `_detect_topic`, contoh "Niat & Keikhlasan" untuk bukhari #1).
- `exegesis()` lulus `text or ""` / `malay or ""`.
- UI tambah medan `Kategori (auto)` (label jujur — dikesan automatik) selepas
  Topic. Kandungan HadeethEnc TIDAK diubah; kategori sekadar maklumat tambahan.

**Ujian baru (`semak.py` 8e):**
- `_hadeethenc` terima `text`+`malay` → kategori auto kekal.
- UI papar `Kategori (auto)`.

**Verifikasi luar talian** (bukhari #1 → `Niat & Keikhlasan`, bukhari #2 →
`auto` + topik Akhlak: Kejujuran; muslim #1/nasai #1/malik #1 kekal `auto`).

### Langkah seterusnya

```
python sync_hadeethenc.py --semak   # liputan per kitab
python semak.py                     # mesti lulus kecuali 5 fail pengedaran
python -c "from core.hadeethenc_api import senarai_id_ms; senarai_id_ms()"  # jika cache tiada
```

## 12. Keputusan: Fasa 4B DIBATALKAN buat sementara

Pengguna pilih **Pilihan 4** — gugurkan Fath al-Bari buat sementara, tumpu
Fasa 4A (Irsyad al-Hadith, BM).

**Sebab** (halangan asas, bukan boleh-baiki):
- Penomboran hanyut dari nombor hadis: delta median 174, julat −4,853..+7,519
- Tashkeel 0.00% (309,912 huruf diukur) — Arab gundul
- Arab klasik, median 1,971 aksara, Bukhari sahaja, CC BY-NC-SA
- Walaupun papar ikut BAB boleh laksana, kandungan tetap Arab klasik — nilai
  rendah untuk pengguna Melayu berbanding 4A (BM, disemak ulama, 574+ siri)

**Dokumen dikemas kini:** `RANCANGAN_4FASA.md` (status lapisan B + jadual
pilihan + kerja cadangan), `MULA_SINI.md` (§Fasa 4B), `sesi_index.md`
(Status Fasa 4B). Bukti siasatan kekal di arkib — tidak dibuang.

**Langkah seterusnya:** siasatan Fasa 4A — kebenaran penggunaan semula
(izin Jabatan Mufti) + struktur data & cara padan.

## 13. Siasatan Fasa 4A SELESAI — tiada sumber BM terbuka lain; guna HadeethEnc + auto

### Lesen Irsyad al-Hadith (JMWP) — TERTUTUP

- Footer muftiwp.gov.my: **"Hak Cipta Terpelihara © 2024 Jabatan Mufti
  Wilayah Persekutuan"** — *all rights reserved*.
- Halaman "Data Terbuka Kerajaan" (mygov / data.gov.my) hanya menyenaraikan
  **2 set data waktu solat** — artikel Irsyad **TIDAK termasuk**.
- Tiada terma penggunaan semula untuk artikel. Memuat turun + memasukkan
  semula huraian ke aplikasi = pelanggaran hak cipta tanpa izin.

### Struktur & padanan (jika izin pernah diberi — kini tidak)

- Senarai: `/ms/artikel/irsyad-al-hadith?start=N`, ~25 halaman × 25 artikel.
- Setiap artikel: Soalan + Jawapan + **Nota hujung** yang memetik nombor
  hadis berstruktur ("Riwayat Muslim no 1037" → muslim #1037;
  "Riwayat al-Bukhari (697)").
- **Kelemahan padanan:** banyak rujuk kitab **luar 9 koleksi DB** (al-Baihaqi,
  Syu'ab al-Iman, al-Marasil, al-Adab al-Mufrad); artikel mustholah umum
  (cth. "Hadith Mursal") tiada satu hadis untuk dipadan.

### Keputusan pengguna: cari sumber BM lain → disiasat

| Sumber | Lesen | Bentuk | Padanan per-hadis? |
|---|---|---|---|
| HadeethEnc (diguna) | ✅ percuma (3 syarat) | 147 hadis BM | ✅ 280 padanan |
| Irsyad al-Hadith (JMWP) | ❌ Hak Cipta Terpelihara | artikel Q&A | ✅ tetapi dilarang |
| MyHadith (islam.gov.my) | ❌ kerajaan | Q&A | ❌ `Transport error` ×2 |
| IslamHouse Malay | ✅ percuma (3 syarat) | 53–74 buku PDF | ❌ buku, bukan per-hadis |
| hadits.id / NU / tazkia / Kemenag | ❌ kerajaan/komersial | terjemahan sahaja | ❌ tiada syarah |
| Syarah Bulughul Maram (TanyaSyariah) | ❌ terjemahan penerbit | syarah Utsaimin | ❌ kitab berbeza dari 9 kitab |

### Kesimpulan

**Tidak ada sumber syarah BM per-hadis berlesen terbuka selain HadeethEnc.**
Hadis ber-BM HadeethEnc (147) ialah siling tetap; semua calon lain sama ada
dilarang (kerajaan/komersial) atau tidak berstruktur per-hadis.

**Keputusan:** Fasa 4A ditutup sebagai *disiasat, tiada calon sah*.
Nilai sebenar yang tinggal bukan sumber baharu tetapi **kualiti**:
- Kategori auto (lihat §11) — kini berfungsi untuk hadis berpadan.
- Nota auto (Lapisan C) kekal sandaran jujur (`status="auto"` + penafian).
- Projek boleh dianggap **SIAP untuk diedar** pada liputan semasa
  (280/62,169 huraian dari sumber, bakinya nota auto + transliterasi +
  terjemahan penuh).

## 14. Keluaran v2026.07.31-11 — bina ZIP edaran

Pengguna memilih "implement" selepas Fasa 4A ditutup. Keluaran pertama
yang dianggap **SIAP untuk diedar**:

- **VERSI.py:** `2026.07.30-10` → `2026.07.31-11`.
- **CIRI** ditambah 4 entri (17 jumlah) supaya `semak_versi.py` mengunci
  ciri paling baharu: `core.phase4_exegesis.ATRIBUSI_HE`,
  `core.phase4_exegesis._detect_topic`, `utils.bahasa.betulkan_melayu`,
  `utils.bahasa.simbol_boleh_dipapar`.
- **PustakaHadith.zip** dibina semula (ZIP lama tertinggal dari sebelum
  Sesi 10 — tiada `sync_hadeethenc.py`, `core/hadeethenc_api.py`,
  `PERUBAHAN_31JUL.md`).
- ZIP **tidak termasuk** fail yang tidak patut diedar: `hadis.db`
  (+`-wal`/`-shm`), `.cache_eng`, `.cache_he`, `.cache_syarah`,
  `user_settings.json`, `bookmarks.json`, `.env`, `__pycache__`.

**Mesej kepada pengguna:** ekstrak ke folder sama + jalankan
`KEMASKINI.bat` (guna `Expand-Archive -Force`) atau ekstrak terus;
kemudian `python semak_versi.py` mesti menunjukkan v2026.07.31-11,
diikuti `python semak.py` (5 GAGAL pengedaran dijangka pada mesin
pembangunan yang ada hadis.db).

## 15. Kelarikan workspace — dokumentasi (selepas bina ZIP)

Pengguna menjelaskan selepas §14: folder root `hadis/` ialah **workspace
Developer**, BUKAN untuk pengguna akhir lagi. `PustakaHadith.zip` **belum
diedar**; penambahbaikan tertangguh akan dilakukan apabila developer
menjalankan app untuk semakan. Maka:

- `MULA_SINI.md` §5 — dikemas kini: status workspace + senarai
  penambahbaikan tertangguh.
- **`MANUAL_PENGGUNA.md`** — manual pengguna akhir baharu: apa itu app,
  keperluan, cara pasang (`PASANG.bat`), cara dapat/masukkan kunci API,
  cara guna (antara muka, kitab, hadis, huraian, carian, tersimpan),
  kemas kini, penyelesaian masalah, nyahpasang, privasi.
- **`MANUAL_REFERENSI_DEV.md`** — rujukan utama developer (satu fail):
  keadaan workspace, struktur, status fasa, fakta API, hadis.db, peraturan
  padanan, skrip utiliti, penambahbaikan tertangguh, senarai semak, corak
  pepijat, pepijat Qt, peta dokumen.
- `semak.py` disahkan lulus selepas kemas kini (5 kegagalan pengedaran
  dijangka — `.cache_eng`, `.cache_he`, hadis.db, -wal, -shm pada mesin
  pembangunan). Semakan #11 (dokumen konsisten) lulus.
