# Rancangan 4 Fasa — PustakaHadith

> **Kemas kini 3 Ogos 2026 (v1.0).** Fasa 3 SIAP pada data
> sebenar (31,833 terjemahan, 98%). **Huraian auto (Fasa 4 HadeethEnc +
> nota topik) DIBUANG daripada UI** (Sesi 18.9) — bertumpuk dan
> mengelirukan dengan huraian asli SemakHadis. Sumber huraian BM kini:
> **SemakHadis** (4,237 padanan matn) + syarah klasik Arab + darjat. Fasa
> 4B Fath al-Bari **DIBATALKAN buat sementara** — dakwaan lama "penomboran
> sejajar 5/5" telah DIBATALKAN oleh ujian pada data sebenar (keputusan
> 31 Jul). Fasa 4A Irsyad al-Hadith **DISIASAT SELESAI — lesen TERTUTUP**
> ("Hak Cipta Terpelihara"). Butiran: `dokumen/perubahan/PERUBAHAN_31JUL.md` §12–13,
> `dokumen/sesi/sesi_index.md` Sesi 18.8–18.9.

> **Kemas kini Sesi 18.9:** Halaman pipeline dan butang "📖 Huraian"
> DIBUANG sepenuhnya (huraian auto Fasa 4 tidak lagi dipapar).

> **Kemas kini Sesi 9 (SEJARAH):** Halaman pipeline lama memapar Huraian
> sahaja. Halaman itu sendiri kini DIBUANG (Sesi 18.9). Fasa 1-3 KEKAL
> sebagai modul.

> Konteks teknikal: lihat `dokumen/manual/MULA_SINI.md`.
> Nombor dalam dokumen ini datang daripada ujian langsung. Di mana
> ujian lama telah dibatalkan oleh ujian baharu, kedua-duanya
> ditunjukkan supaya kesilapan itu tidak diulang.

## Keputusan asas

| Perkara | Keputusan |
|---|---|
| Pengguna sasaran | **Campuran** — awam sebagai teras, mod lanjutan untuk penuntut ilmu |
| Fasa 3 | **SIAP** — 31,833 terjemahan, 98%, diaudit saksi bebas |
| Fasa 4 | **DIBUANG (Sesi 18.9)** — huraian auto HadeethEnc + nota topik tidak lagi dipapar; sumber huraian BM: SemakHadis 4,237 padanan. Irsyad al-Hadith **DITUTUP (lesen tertutup, disiasat 31 Jul)**; Fath al-Bari **DIBATALKAN buat sementara** |

**Prinsip UI daripada keputusan "campuran":**
Paparan asal bersih untuk orang awam. Segala yang teknikal — sanad, syarah
Arab, transliterasi — berada di belakang bahagian boleh kembang. Orang awam
tidak nampak; penuntut ilmu jumpa bila cari.

---

## Gambaran besar

```
        API hadis.my
             |
    +--------+--------+
    |                 |
  FASA 1           FASA 3
  Ekstrak          Terjemah / Padan
  arab + ms + id   + eng (sumber luar, padan ikut teks Arab)
    |                 |
  FASA 2           FASA 4
  Transliterasi    Huraian
  (bantu baca)     Irsyad BM + Fath al-Bari Arab
             |
        Satu rekod hadis lengkap
```

---

## FASA 1 — Ekstrak  ✅ siap

Sumber: API hadis.my. Beri Arab + Melayu + Indonesia, liputan 100%.

**Kuota:** Basic 200/hari; **Developer 10,000/hari**.
62,169 hadis = 622 permintaan -> **satu sesi sahaja** pada pelan Developer.
Kuota BUKAN lagi kekangan.

Kekangan sebenar kini ialah **masa dinding**: pada throttle 1.1s,
622 permintaan = ~12 minit. Munasabah.

Tetap simpan kemajuan supaya boleh sambung jika terputus.

---

## FASA 2 — Transliterasi  ✅ siap + dipasang semula di UI

Diuji 1,000 hadis: 0 ralat, baki tanpa baris 0.13%.

**Sesi 7:** dipulangkan ke halaman baca hadis sebagai `Collapsible`
tertutup lalai, dengan pembinaan malas. Dua gaya — Gaya Melayu
didahulukan, Akademik selepasnya.

Jangan lipat `ة -> ه` — memecahkan carian.

---

## FASA 3 — Terjemahan  ✅ SIAP (98%, diaudit)

### Hasil akhir

```
31,833 terjemahan Inggeris tersimpan · gagal 487 (dari 3,962)
Audit Bukhari: 100.0% disahkan, 0 disyaki
```

| kitab | liputan | kitab | liputan |
|---|---|---|---|
| bukhari | 99% | nasai | 98% |
| muslim | 96% | ibnu-majah | 99% |
| abu-daud | 99% | malik | 96% |
| tirmidzi | 96% | | |

`ahmad` dan `darimi` tiada dalam sumber — tab English kekal kelabu.

### Penemuan yang mengubah segalanya: kunci padanan SALAH

Rancangan asal memadan ikut **teks Arab**. Itu berfungsi tetapi lemah.
Audit saksi bebas mendedahkan `hadis.db.indonesia` dan CDN `ind-*`
mempunyai pertindihan purata **1.00** — bukan ~0.85 seperti dijangka
bagi dua terjemahan bebas. Kedua-duanya **terjemahan yang sama**.

| | Arab | Indonesia |
|---|---|---|
| tashkeel | hadis.my penuh, CDN tidak | tiada isu |
| sanad dikongsi | punca SEMUA positif palsu | tiada |
| lapisan perlu | 3 + Jaccard dua hala | padanan tepat |

### Turutan padanan (5 lapisan — JANGAN susun semula)

```
1. indo    teks Indonesia dinormalisasi, TEPAT
2. indo~   token Indonesia, JACCARD_IND = 0.95
3. penuh   teks Arab penuh
4. awalan  200 aksara Arab, mesti UNIK
5. kata    token Arab jarang, JACCARD_MIN = 0.90 DUA HALA
```

Selepas lapisan Indonesia masuk, lapisan Arab hampir tidak digunakan:
Bukhari `penuh` jatuh dari 4,288 ke **9**.

### Kronologi — mengapa 92.6% lebih teruk daripada 88%

| peringkat | tersimpan | catatan |
|---|---|---|
| mula | 31,007 (92.6%) | **ilusi** — 23.2% dari lapisan `kata` rosak |
| + Jaccard dua hala | 28,469 (88%) | jujur; 2,538 salah dibuang |
| + `indo` | 30,593 (94%) | |
| + `indo~` | **31,833 (98%)** | |

Lapisan `kata` mengira skor **sehala** — buta terhadap kata pada calon
yang tiada pada soalan. Sanad panjang boleh jadi 80% teks hadis pendek.
Ujian yatim (buang 600 hadis dari indeks; jawapan betul = "tiada"):

| kitab | tanpa Jaccard | dengan 0.90 | padanan betul hilang |
|---|---|---|---|
| bukhari | 35.3% | 5.2% | 0 |
| nasai | 29.3% | 3.3% | 0 |
| muslim | 16.0% | 2.3% | 0 |
| malik | 8.1% | 0.4% | 0 |

### Butiran teknikal

```
CDN  : https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{kod}.min.json
Guna : ind-* (padanan) · eng-* (hasil) · ara-*1 (sandaran)
ara-*1 identik dengan ara-* selepas normalisasi, fail lebih kecil
```

Tiada kunci API, tiada kuota.

### Dua larangan

- **JANGAN buang pengesahan dua hala** pada lapisan `kata` — 35.3%
  positif palsu tanpa ia
- **JANGAN guna `INSERT OR REPLACE` sahaja** — baris salah dari
  larian lama akan kekal. `DELETE` per-kitab dahulu

### Audit mesti guna bukti BEBAS

`diagnos_padanan.py` menilai padanan-Arab dengan teks Arab — berhujah
dalam bulatan. `audit_eng.py` guna teks Indonesia yang tidak pernah
dipakai untuk memadan. Pemisahan diukur: betul 1.00 · salah 0.05 ·
sifar pertindihan. Lapisan `indo`/`indo~` ditanda
**"(bukan bukti bebas)"** atas sebab yang sama.

---

## FASA 4 — Huraian  ⚫ HadeethEnc DIBUANG + ✅ SemakHadis (BM)

**⚫ DIBUANG 3 Ogos 2026 (Sesi 18.9):** huraian auto HadeethEnc + nota
topik generik (`status="auto"`) tidak lagi dipapar. Keputusan pengguna:
dua jenis "Huraian" (auto + SemakHadis) mengelirukan; huraian asli
SemakHadis + syarah klasik Arab + darjat mencukupi. Butang "📖 Huraian",
halaman pipeline, `ui/workers.PipelineWorker`, `core/phase4_exegesis.py`
dipadam. Data HadeethEnc (jadual `hadethenc`, `.cache_he/`,
`sync_hadeethenc.py`) kekal sebagai **arsip** — tidak dipapar UI.

**SEJARAH (Sesi 10):** huraian Melayu ringkas datang dari **HadeethEnc.com**
(projek IslamHouse) untuk 280 → 310 hadis — padan ikut **MATN** (sanad
ditanggalkan), bukan ID, kerana penomboran HadeethEnc bebas.

```
python sync_hadeethenc.py      # arsip; UI tidak lagi membaca hadethenc
python sync_sema.py            # AKTIF: 4,237 padanan SemakHadis BM
```

- 147 sumber ber-BM ditemui melalui `language=en` + tapis `translations[]`
- Jaccard matn 0.55: hadis betul 0.62-1.00, salah 0.04-0.48
- Status `dari_sumber` (✓) di UI — dulu; kini keseluruhan UI Fasa 4 dibuang
- Atribusi: "Huraian ringkas oleh HadeethEnc.com (projek IslamHouse)" — dulu

### Lapisan A — Irsyad al-Hadith (BM) — ⚫ **DITUTUP (lesen tertutup)**

**Keputusan pengguna 31 Jul 2026:** disiasat selesai — lesen
**"Hak Cipta Terpelihara © 2024 Jabatan Mufti Wilayah Persekutuan"**,
artikel Irsyad TIDAK termasuk dalam Data Terbuka Kerajaan (hanya 2 set
waktu solat), dan tiada terma penggunaan semula. Memasukkan huraiannya
ke aplikasi = pelanggaran hak cipta.

Jabatan Mufti Wilayah Persekutuan. 574+ siri, disemak ulama, Bahasa Melayu.
Ada bahagian *Fiqh al-Hadith* yang memang huraian sebenar.

- **Kelebihan:** boleh dibaca pengguna sasaran, berautoriti
- **Kelemahan:** liputan rendah berbanding 62,169 hadis
- **Sikap:** liputan rendah tetapi **setiap satu berguna** — lebih baik
  daripada 5,074 syarah yang pengguna tak boleh baca

**Teknikal (didokumenkan, bukan untuk dilaksanakan):** senarai
`/ms/artikel/irsyad-al-hadith?start=N` (~25 halaman); setiap artikel =
Soalan + Jawapan + Nota hujung yang memetik nombor hadis ("Riwayat Muslim
no 1037"). Kelemahan padanan: banyak rujuk kitab LUAR 9 koleksi
(al-Baihaqi, Syu'ab al-Iman, al-Marasil, al-Adab al-Mufrad); artikel
mustholah umum tiada satu hadis untuk dipadan.

**Sumber BM lain juga disiasat — tiada yang sah:** MyHadith JAKIM
(kerajaan, `Transport error`), IslamHouse Malay (lesen terbuka ✅ tetapi
buku PDF, bukan per-hadis), hadits.id/NU/tazkia/Kemenag (terjemahan
sahaja, lesen kerajaan), syarah Bulughul Maram (terjemahan penerbit +
kitab berbeza). Butiran: `dokumen/perubahan/PERUBAHAN_31JUL.md` §13.

### Lapisan B — Fath al-Bari (Arab) — ⚫ **DIBATALKAN buat sementara**

**Keputusan pengguna 31 Jul 2026:** gugurkan 4B buat sementara, tumpu 4A.
Fath al-Bari kekal di arkib (Sesi 7-9 + dokumen/sesi/sesi_index.md) — bukti tidak
dibuang, cuma projek tidak lagi mengerjakannya sehingga ada sebab baru.

Muat turun dan parser **berfungsi**. Padanan **tidak**.

```
Repo   : OpenITI/0875AH   (852H dibundarkan KE ATAS, bukan 0850AH)
Fail   : 0852IbnHajarCasqalani.FathBari.JK000166-ara1   30.5 MB
Format : penanda '# N'   5,075 seksyen   71.2% dlm julat Bukhari
```

#### Dakwaan lama DIBATALKAN

Sesi 7 melaporkan **"penomboran sejajar — diuji 5/5 ikut sanad"**
(#1 #2 #8). Ujian itu **tidak sah**: ketiga-tiga hadis berada dalam
julat 1-200 yang memang sejajar.

**Penanda `# N` BUKAN nombor hadis Bukhari.** Ia kiraan berjujukan
dalam edisi Ibn Hajar — bermula sejajar, menyimpang apabila edisi
berbeza pendapat tentang apa yang dikira hadis berasingan:

```
   1-200   anjakan   +0      2000-3500  anjakan -120
 600-800   anjakan  -32      5000-7000  anjakan -320
```

Jika ambang diturunkan supaya sync lulus, **95% Bukhari akan dapat
syarah hadis yang salah**. Untuk teks agama itu tidak boleh diterima.

#### Padanan ikut TEKS juga gagal

300 seksyen diuji melalui kata jarang: hanya **2** memberi nombor yang
sama, 169 berbeza, delta median 174 dengan julat -4,853..+7,519 —
tiada corak. Syarah memetik potongan sanad (`قوله حدثنا الحميدي`),
bukan matn, jadi isyarat teks tidak mencukupi.

#### Kadar padanan sebenar (bukan 76%)

Metrik lama guna sampel 80 hadis **pertama**. Syarah paling terperinci
pada permulaan kitab:

```
   1-500    29%        3000-5000  11%
 500-1500   13%        5000-7600  10%
```

Ambang 50% **tidak pernah boleh dicapai** oleh sumber ini.

#### Halangan lain (kekal sah)

1. **Tashkeel 0.00%** — diukur pada 309,912 huruf. Arab gundul
2. Arab klasik — majoriti pengguna Melayu tak boleh baca
3. Median 1,971 aksara — terlalu panjang untuk kad hadis
4. Bukhari sahaja
5. CC BY-NC-SA — atribusi wajib, tiada guna komersial

#### Pilihan seterusnya (keputusan: Pilihan 4)

| # | Pilihan | Nota |
|---|---|---|
| 1 | Papar ikut **BAB**, bukan hadis | Boleh laksana; ketepatan terjamin |
| 2 | Cari sumber lain bernombor standard | Belum dikaji |
| 3 | Padanan separa-manual, hadis masyhur | Kos tinggi, liputan rendah |
| 4 | **Gugurkan 4B**, tumpu 4A | ✅ DIPILIH 31 Jul — nilai lebih tinggi |
| 5 | Betulkan jika sisihan MALAR | Perlu `diagnos_syarah.py` dahulu |

`sync_syarah.py` selamat dijalankan — ia membatalkan diri sendiri dan
mencetak jadual hanyut.

### Lapisan C — automatik (sedia ada)

**DIBUANG 3 Ogos 2026 (Sesi 18.9)** — nota topik generik (`status="auto"`)
dan huraian HadeethEnc (`dari_sumber`) tidak lagi dipapar UI. Sumber
huraian BM kini: **SemakHadis** + syarah klasik Arab + darjat.

### Keutamaan paparan (selepas Sesi 18.9)
```
SemakHadis ada?           -> Collapsible "Huraian (SemakHadis · status)"
Syarah klasik Arab?       -> papar (sumber asal)
Darjat ada?               -> papar
Tiada sumber?             -> tanpa lapisan huraian tambahan (huraian auto dibuang)
```

---

## Susunan kerja dicadang

| # | Kerja | Sebab dahulukan |
|---|---|---|
| ~~1~~ | ~~Fasa 3 English~~ | ✅ SIAP — 31,833 (98%) |
| ~~2~~ | ~~Sync penuh~~ | ✅ SIAP — 62,169 hadis dalam DB |
| ~~3~~ | ~~Fasa 4 lapisan B~~ | ⚫ DIBATALKAN buat sementara — penomboran hanyut |
| ~~4~~ | ~~Fasa 4 HadeethEnc~~ | ⚫ DIBUANG 3 Ogos 2026 (Sesi 18.9) — huraian auto tidak dipapar UI |
| ~~1~~ | ~~`audit_eng.py --semua`~~ | ✅ SIAP — 30,541/30,547 (100.0%), 6 positif palsu |
| ~~1~~ | ~~Keputusan Fasa 4B~~ | ✅ SIAP 31 Jul — Pilihan 4 (gugurkan 4B, tumpu 4A) |
| ~~1~~ | ~~Siasatan Fasa 4A~~ | ✅ SIAP 31 Jul — lesen Irsyad TERTUTUP; tiada sumber BM terbuka lain |
| — | **Projek sedia untuk diuji** | Sumber selesai: SemakHadis + syarah Arab + darjat + transliterasi + terjemahan |

---

## Isu belum selesai

- **Kunci API kekal AKTIF sengaja** — pelan developer untuk ujian app
  (keputusan pengguna 31 Jul). Panduan guna semula: `dokumen/rujukan/REVOKE_KUNCI.md`
- `audit_eng.py --semua` — SIAP 31 Jul: 30,541/30,547 disahkan (100.0%),
  6 "disyaki" disiasat = semua positif palsu (penomboran `ind-*` hanyut
  dari `ara-*`). Ahmad & Darimi tiada di CDN — dilangkau
- `diagnos_syarah.py` belum dijalankan pada data sebenar
- Halaman Tersimpan belum diuji dengan tanda buku sebenar
- Saiz DB: +~14 MB (eng) sahaja. Fath al-Bari tidak disimpan
- Huraian auto (HadeethEnc) **DIBUANG** — data kekal arsip, tidak dipapar UI
- SemakHadis hanya meliputi hadis popular (4,237/62,169)
- Lesen SemakHadis belum disahkan secara bertulis (atribusi dipapar)
- **Workspace = Developer sahaja; ZIP hanyalah arkib development** — semakan app oleh
  developer belum dijalankan (senarai penuh: `dokumen/manual/MANUAL_REFERENSI_DEV.md` §8)

**Selesai sejak versi lalu:** `hadis.db` kini penuh (62,169) ·
padanan diuji pada 7 kitab, bukan Bukhari sahaja
