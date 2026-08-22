# Perubahan 30 Julai 2026 — v2026.07.30-4

Ringkasan satu hari. Arkib penuh: `sesi_index.md` (Sesi 10 & 10B).

---

## 1. Hasil terbesar: terjemahan Inggeris 92.6% "ilusi" → 98% disahkan

### Kronologi

| peringkat | tersimpan | catatan |
|---|---|---|
| mula | 31,007 (92.6%) | **ilusi** — 23.2% dari lapisan `kata` yang rosak |
| + Jaccard dua hala | 28,469 (88%) | jujur; 2,538 padanan salah dibuang |
| + lapisan `indo` | 30,593 (94%) | padanan tepat teks Indonesia |
| + lapisan `indo~` | **31,833 (98%)** | padanan kabur Indonesia |

`gagal` jatuh 3,962 → **487**. Audit Bukhari: **100.0% disahkan, 0 disyaki**.

### Penemuan: kunci padanan yang salah selama ini

Padanan dibina atas **teks Arab**. Sepatutnya **teks Indonesia**.

Ditemui secara tidak sengaja: audit membandingkan `hadis.db.indonesia`
dengan CDN `ind-*` dan dapat pertindihan purata **1.00** — bukan ~0.85
seperti dijangka bagi dua terjemahan bebas. Kesimpulan: kedua-duanya
**terjemahan yang sama**.

| | Arab | Indonesia |
|---|---|---|
| tashkeel | hadis.my penuh, CDN tidak | tiada isu |
| sanad dikongsi | punca SEMUA positif palsu | tiada |
| lapisan perlu | 3 + Jaccard | padanan tepat |

### Turutan padanan baharu (5 lapisan — JANGAN susun semula)

```
1. indo    teks Indonesia dinormalisasi, TEPAT
2. indo~   token Indonesia, JACCARD_IND = 0.95
3. penuh   teks Arab penuh
4. awalan  200 aksara Arab, mesti UNIK
5. kata    token Arab jarang, JACCARD_MIN = 0.90 dua hala
```

### Pecahan akhir per kitab

| kitab | awal | akhir | indo+indo~ |
|---|---|---|---|
| bukhari | 93% | 99% | 6,589 |
| muslim | 93% | 96% | 4,842 |
| abu-daud | 98% | 99% | 4,354 |
| tirmidzi | 96% | 96% | 136 → **3,454** |
| nasai | 95% | 98% | 5,302 |
| ibnu-majah | 99% | 99% | 4,233 |
| malik | 93% | 96% | 1,550 |

---

## 2. Tiga pepijat padanan Inggeris

### 2a. `padan_kata` mengira skor SEHALA

Ia tanya "berapa kata soalan ada pada calon" — buta terhadap kata pada
calon yang tiada pada soalan. Sanad panjang boleh jadi 80% teks hadis
pendek, jadi dua hadis dengan matn **berbeza sepenuhnya** nampak serupa.

Ujian yatim (buang 600 hadis dari indeks; jawapan betul = "tiada"):

| kitab | tanpa Jaccard | dengan 0.90 | padanan betul hilang |
|---|---|---|---|
| bukhari | 35.3% | 5.2% | 0 |
| muslim | 16.0% | 2.3% | 0 |
| nasai | 29.3% | 3.3% | 0 |
| malik | 8.1% | 0.4% | 0 |

Baki 31 pada Bukhari: 22 teks normalisasi IDENTIK (pendua tulen),
9 benar tersalah = 1.5%.

### 2b. `INSERT OR REPLACE` tidak membersih

Baris yang dahulu dipadan dan kini ditolak **kekal** dengan terjemahan
salah. Jalankan semula sync tidak membaikinya.
→ `DELETE FROM terjemahan_eng WHERE collection=?` sebelum simpan.

### 2c. Tiada cara membezakan versi kod

Lihat bahagian 5.

---

## 3. Fasa 4B (Fath al-Bari) — TERSEKAT, punca dikenal pasti

### Penanda `# N` BUKAN nombor hadis Bukhari

Ia kiraan berjujukan dalam edisi Ibn Hajar. Bermula sejajar, menyimpang
apabila edisi berbeza pendapat tentang apa yang dikira hadis berasingan.

### Punca 1: sampel 80 hadis PERTAMA (artifak)

Syarah paling terperinci pada permulaan kitab:

```
   1-500    29%        3000-5000  11%
 500-1500   13%        5000-7600  10%
1500-3000   11%
```

80 pertama → 76%. Seluruh kitab → 13%. **Ambang 50% tidak pernah boleh
dicapai** oleh sumber ini, walaupun ia sah.

### Punca 2: penomboran hanyut

Diukur pada proksi CDN: `+0 -60 -140 +0 -300 -360`
Diukur pada **hadis.db sebenar**: `+0 +20 +0 +80 +100 +0`

Hanyut sebenar jauh lebih kecil (julat 100 vs 360), arah **positif**
bukan negatif, 3/6 julat sejajar. **Proksi memberi gambaran salah.**

### Padanan teks juga gagal

300 seksyen diuji: 171 dapat calon, nombor sama hanya 2, berbeza 169.
Delta median 174, julat −4,853..+7,519 — tiada corak. Syarah memetik
potongan sanad (`قوله حدثنا الحميدي`), bukan matn.

### Metrik lama tidak membezakan apa-apa

Berasaskan kata **sanad**: penomboran betul 1.21x vs digeser 50 →
**1.20x**. Metrik baharu guna **kata jarang matn** (df≤30, panjang>4).

### Pengawal ditulis semula

`nisbah_keyakinan()` menggantikan ambang mutlak:
1. anjakan-0 mengatasi kawalan (−2,−1,+1,+2) sebanyak `NISBAH_MIN` 1.8×
2. anjakan terbaik kekal ~0 pada **≥80%** julat

| ujian | nisbah | putusan |
|---|---|---|
| Fath al-Bari | 2.09× | TOLAK (hanyut) |
| kawalan **positif** | 10.36× | **TERIMA** |
| kawalan negatif | 0.96× | TOLAK |

Kawalan positif itu penting: versi pertama menolak Fath al-Bari (betul)
**tetapi juga menolak sumber sah** (salah).

### Pepijat sampingan: penanda manuskrip

`ms00022` menyelit **di tengah ayat Arab, 10,952 kali**. Berbeza
daripada `PageV..P..` yang berdiri sendiri. Akan dipapar sebagai
aksara Latin dalam teks Arab.
→ `_MS = re.compile(r"\bms\d{3,}\b")` (3+ digit; `ms12` kekal)

---

## 4. Pepijat pengedaran: ZIP folder bersarang

**Kesalahan saya, bukan pengguna.** ZIP mengandungi folder `hadis/`,
jadi ekstrak ke `pustaka\` menghasilkan `pustaka\hadis\core\...`
sedangkan skrip `import core.syarah_source` dari `pustaka\core\`.

**Fail lama tak pernah diganti — tiga kali berturut-turut.** Setiap
laporan kelihatan sah.

→ ZIP kini tanpa folder bersarang; isinya mendarat terus.

---

## 5. Infrastruktur versi (supaya #4 tak berulang)

- **`VERSI.py`** — cap tunggal + senarai 8 ciri wajib
- **`semak_versi.py`** — sahkan pemasangan, exit 1 jika lama,
  beri amaran jika jumpa folder `hadis/` bersarang
- **Cap versi** pada `sync_english.py`, `sync_syarah.py`, `audit_eng.py`
- **`semak.py` seksyen 10** — 6 semakan menguji semua ini

---

## 6. Fail

### Baharu

| fail | fungsi |
|---|---|
| `audit_eng.py` | audit saksi bebas (teks Indonesia) |
| `diagnos_syarah.py` | imbasan hanyut halus (8 julat, langkah 2) |
| `VERSI.py` | cap versi + senarai ciri |
| `semak_versi.py` | sahkan pemasangan terkini |
| `PERUBAHAN_30JUL.md` | dokumen ini |

### Diubah

| fail | perubahan |
|---|---|
| `core/eng_source.py` | `JACCARD_MIN` `JACCARD_IND` `kunci_indonesia()` `bina_indeks_ind()` `bina_indeks_ind_kata()` `padan_ind_kabur()` `_token_ind()`; `padan()` 5 lapisan |
| `core/syarah_source.py` | `_MS`; `nisbah_keyakinan()` `diagnos_hanyut()` `_skor_julat()` `_skor_anjakan()`; buang ambang mutlak |
| `sync_english.py` | DELETE dahulu; muat `ind-*`; cap versi |
| `sync_syarah.py` | pengawal baharu + jadual hanyut; cap versi |
| `diagnos_padanan.py` | cap versi; taburan kualiti Jaccard |
| `semak.py` | 8b (+4) · 8c (12 semakan) · 8d · **10 baharu** |
| `sesi_index.md` | Sesi 10 & 10B |
| `MULA_SINI.md` | Fasa 3 ditulis semula; Fasa 4B ditanda TERSEKAT |

### Kekal (perubahan pengguna, disahkan md5)

- `ui/widgets.py` baris 67 — `inner` `Preferred`
- `ui/app_qt.py` — `_laras_tinggi()` di 615, 723, 1392; tiada spacer

---

## 7. Dua pelajaran am (berulang sepanjang hari)

**A. Sampel dari SATU HUJUNG julat memberi jawapan yang salah.**
- Fasa 3: audit ikut nombor menyembunyikan 35% positif palsu
- Fasa 4B: 80 hadis pertama beri 76%, sebenarnya 13%

**B. Audit mesti guna bukti yang TIDAK dipakai untuk membuat keputusan.**
`diagnos_padanan.py` menilai padanan-Arab dengan teks Arab — berhujah
dalam bulatan. `audit_eng.py` guna teks Indonesia yang tidak pernah
dipakai memadan. Pemisahan: betul 1.00 · salah 0.05 · sifar pertindihan.

Lapisan `indo`/`indo~` ditanda **"(bukan bukti bebas)"** atas sebab sama.

**C. Setiap pengawal perlu kawalan POSITIF dan NEGATIF.**
Pengawal syarah pertama menolak Fath al-Bari (betul) tetapi juga
menolak kawalan positif tiruan (salah) — tak dapat dikesan tanpa ujian.

---

## 8. Belum selesai

| perkara | status |
|---|---|
| `audit_eng.py --semua` | hanya Bukhari diaudit; 6 kitab lain belum |
| `diagnos_syarah.py` | belum dijalankan pada data sebenar |
| Fasa 4B keputusan | (1) ikut bab · (2) sumber lain · (3) separa-manual · (4) gugurkan · (5) betulkan jika sisihan MALAR |
| Dua kunci API | masih AKTIF dan terdedah — lihat `REVOKE_KUNCI.md` |
| Halaman Tersimpan | belum diuji dengan tanda buku sebenar |
| Fasa 4A Irsyad al-Hadith | kebenaran guna semula belum dikaji |

### Langkah seterusnya

```
python semak_versi.py       # mesti v2026.07.30-4
python diagnos_syarah.py    # guna cache, tak muat turun semula
python audit_eng.py --semua # 6 kitab belum diaudit
```

---

## 9. Kemas kini v2026.07.30-5 — tiga pepijat dalam alat diagnostik

### 9a. `_skor_julat` sampel N-PERTAMA (ralat yang SAMA, kali ketiga)

```python
for hid in range(lo, hi + 1):    # SALAH — berhenti selepas `had` capai
    ...
    if len(nilai) >= had: break
```

Ia berhenti selepas 120 hadis pertama dalam setiap julat. Ini ralat
yang identik dengan pengawal lama (80 hadis pertama → 76% palsu) yang
saya dokumenkan pagi tadi sebagai Pelajaran A — kemudian saya ulangi
dalam pembetulannya sendiri.

Dibetulkan: `calon[::langkah]` merentas julat.

Kesan pada proksi CDN:
```
sebelum: nisbah 2.09x   [+0 -60 -140 +0 -300 -360]
selepas: nisbah 1.51x   [+0 -100 +0 +0 -320 -400]
```

Kawalan disahkan: positif 8.87x TERIMA · negatif 1.05x TOLAK.

### 9b. Paparan mencampur dua metrik berbeza

```
padanan: 73/200 = 10%      <- 73/200 = 36.5%, BUKAN 10%
```
`73/200` ialah kiraan kata-sanad (`_skor_anjakan`); `10%` ialah skor
kata-jarang (`_skor_julat`). Dua benda berlainan pada baris yang sama.

Dibetulkan — satu metrik sahaja:
```
skor sejajar 10.4%  vs  kawalan 11.9%   nisbah 0.87x
```

### 9c. Cache syarah tidak tersimpan

Pengguna memuat turun 29 MB tiga kali; `diagnos_syarah.py` kemudian
lapor "Cache tiada". Punca tidak dapat ditentukan dari jauh (kebenaran
folder / antivirus / OneDrive).

Dua pembetulan:
- `muat_turun()` mengesahkan saiz selepas tulis dan melaporkan
  `[cache disimpan]` atau amaran eksplisit; jika tulis gagal ia guna
  fail sementara supaya sync tetap jalan
- `diagnos_syarah.py` memuat turun sendiri jika cache tiada — tidak
  lagi bergantung pada `sync_syarah.py` berjaya menyimpan

### Fail diubah
`core/syarah_source.py` (`_skor_julat`) · `sync_syarah.py` (paparan +
cache) · `diagnos_syarah.py` (muat turun sendiri) · `semak.py`
(ujian sampling) · `VERSI.py` → `2026.07.30-5`

### Pelajaran (kemas kini Pelajaran A)

Mendokumenkan ralat TIDAK menghalang pengulangannya. Hanya **ujian
automatik** yang menghalang. `semak.py` kini ada ujian yang gagal
secara khusus apabila `_skor_julat` mengambil N-pertama: korpus di
mana hadis 1-100 padan sempurna dan 101-1000 tidak padan langsung —
sampel N-pertama beri ~100%, sampel merentas beri ~20%.

---

## 10. Kemas kini v2026.07.30-6 — `semak_versi.py` sendiri menipu

### Masalah

Pengguna menjalankan v-4 sedangkan v-5 telah dihantar. `semak_versi.py`
melaporkan:

```
Versi : 2026.07.30-4
Semua 8 ciri hadir. Pemasangan TERKINI.      <- PALSU
```

Skrip itu **tidak boleh tahu** apa versi terbaru yang wujud — ia cuma
menyemak 8 ciri yang ia sendiri kenal. Dakwaan "TERKINI" menukar alat
pengesan-versi-lapuk menjadi alat yang **mengesahkan** versi lapuk.
Ini kali ke-4 pemasangan lapuk berjalan tanpa dikesan.

### Punca sebenar ekstrak gagal

`Expand-Archive` **tanpa `-Force`** gagal pada setiap fail yang sudah
wujud. Ia melapor ralat lalu berhenti — meninggalkan kod lama utuh.

### Pembetulan

- `semak_versi.py` tidak lagi mencetak "TERKINI". Ia menyatakan versi
  yang dijumpai dan meminta pengguna membandingkannya dengan ZIP
  terakhir, plus memberi arahan `Expand-Archive ... -Force` yang tepat.
- **`KEMASKINI.bat` baharu** — ekstrak dengan `-Force`, beri amaran
  jika jumpa folder `hadis/` bersarang, lalu jalankan `semak_versi.py`.
  Boleh diseret-lepas ZIP ke atasnya.

### Ujian ditambah (`semak.py`)

- `semak_versi.py` tidak MENCETAK "TERKINI" — semak baris `print()`
  sahaja, bukan sumber mentah (percubaan pertama saya tersalah tangkap
  perkataan itu di dalam komen)
- `KEMASKINI.bat` wujud, CRLF, mengandungi `-Force`

### Fail
`semak_versi.py` · `KEMASKINI.bat` (baharu) · `semak.py` ·
`VERSI.py` → `2026.07.30-6`

---

## 11. Kemas kini v2026.07.30-8 — data tertinggal di folder lama

### Masalah

Pengguna mengekstrak ZIP ke folder **baharu** `PustakaHadis\` dan
bukan `pustaka\`. `semak_versi.py` melaporkan v-7 dengan betul, tetapi:

```
D:\Pustaka Quran Hadis\pustaka\        <- hadis.db (62,169 hadis, 31,833 eng)
D:\Pustaka Quran Hadis\PustakaHadis\   <- kod v-7, TIADA data
```

`config.py` mengira laluan relatif kepada folder skrip:
```python
DB_PATH = os.path.join(BASE_DIR, "hadis.db")
```
Jadi kod baharu tidak nampak DB lama. Aplikasi kelihatan kosong dan
puncanya tidak jelas -- pengguna mungkin menjalankan semula sync
selama 12 minit tanpa perlu.

### Pembetulan

- **`PINDAH_DATA.ps1`** (baharu) -- salin `hadis.db` + `-wal` + `-shm`
  + `bookmarks.json` + `user_settings.json` + `.env` + folder cache
  dari pemasangan lama. Tidak menimpa tanpa `-Force`; fail asal
  tidak disentuh.
  Nota: `-wal`/`-shm` MESTI dipindah bersama `hadis.db` -- memindah
  db sahaja boleh kehilangan transaksi terakhir.
- **`semak_db.py`** (baharu) -- papar laluan DB SEBENAR yang digunakan
  plus kiraan per kitab. Menjawab "adakah kod ini nampak data saya?"
- **`semak_versi.py`** -- beri amaran jika `hadis.db` tiada di sebelah
  kod, dengan arahan pemindahan

### Ujian ditambah
`PINDAH_DATA.ps1` wujud + CRLF + ASCII · `semak_db.py` wujud ·
`semak_versi.py` menyebut PINDAH_DATA

### Fail
`PINDAH_DATA.ps1` `semak_db.py` (baharu) · `semak_versi.py` ·
`semak.py` · `VERSI.py` -> `2026.07.30-8`
