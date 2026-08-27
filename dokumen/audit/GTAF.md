# GTAF Hadith Collection — Penilaian Pesaing & Penemuan Teknikal

> Ditulis 14 Ogos 2026. Hasil siasatan mendalam terhadap aplikasi
> "Hadith Collection (All in One)" oleh Greentech Apps Foundation
> (GTAF, https://gtaf.org/apps/hadith/), dicetuskan oleh perbandingan
> pesaing untuk PustakaHadith. Rujukan silang: `DEKLARASI.md`
> (jadual perbandingan platform), `INSTALLER.md` (rancangan pemasang
> Windows), `db.py` (skema FTS5).

---

## 1. Profil GTAF

| Perkara | Butiran |
|---|---|
| Organisasi | Greentech Apps Foundation (GTAF) — badan amal berpangkalan UK |
| Ditubuhkan | 2016 (9+ tahun beroperasi) |
| Pasukan | 20+ orang, sepenuhnya jarak jauh |
| Skala pengguna | 3.5 juta+ merentas semua app; app Hadis sahaja **1.5 juta+ pengguna** |
| Model | Percuma, tiada iklan, dibiayai derma |
| Produk lain | Al Quran (Tafsir & By Word) — 60+ bahasa; Dua & Zikr (Hisnul Muslim); Sadiq; Seerah |
| Platform app Hadis | Android, iOS, **Windows (.msix, S3 terus)**, Mac |

### Ciri app Hadis
- 41,000+ hadis daripada 15+ kitab (Bukhari, Muslim, Abu Dawud, Tirmidhi, Ibn Majah, Nasa'i,
  Malik, Ahmad, Riyad us-Saliheen, Syama'il, Al-Adab al-Mufrad, Bulugh al-Maram, 40 Hadis
  Nawawi/Qudsi/Shah Waliullah, Mishkat al-Masabih)
- Biografi **25,000+ ulama & Salaf as-Saliheen**
- Darjat hadis, banding isnad, cari hadis serupa, rantaian perawi
- Matlamat bacaan harian (1–60 minit), jejak streak
- Kongsi sebagai imej, widget hadis, mod terang/gelap

---

## 2. PENEMUAN #1 — Tiada Bahasa Melayu/Indonesia (Disahkan)

Disemak terus di Play Store versi `hl=in` (Indonesia) dan `hl=en` — nota rasmi GTAF **sama
di kedua-dua versi**:

> *"Hadith translations are available in **English, Bangla, and Urdu**... Primarily aimed
> at a non-Arabic, English speaking demographic."*

**Kesimpulan penting:** perihalan kedai app (listing) diterjemah Google Play secara automatik
ke Bahasa Indonesia, tapi **kandungan hadis sebenar dalam app kekal Inggeris/Bengali/Urdu
sahaja** — tiada Melayu, tiada Indonesia. Ini mengukuhkan kedudukan PustakaHadith sebagai
**satu-satunya** pilihan lengkap 9-kitab dalam Bahasa Melayu dengan carian AI di pasaran ini.

App kecil lain "Kumpulan Hadist Shahih Lengkap" (developer berbeza, tidak dikenali) ada dakwaan
terjemahan Indonesia tapi bukan pesaing serius (tiada rekod jelas, bukan projek besar/dipercayai).

---

## 3. PENEMUAN #2 — `sqlite3-arabic-tokenizer` (Repo GitHub GTAF, MIT)

**Repo:** `github.com/GreentechApps/sqlite3-arabic-tokenizer` (16 bintang, lesen MIT)
**Artikel teknikal:** Shahriar Nasim Nafi, Medium, "Search Arabic text with diacritics
using SQLite tokenizer" (Jan 2023)

### Masalah yang mereka selesaikan
Pengguna cari hadis Arab **tanpa** tashkeel (cara biasa orang taip Arab — papan kekunci
jarang ada harakat), tapi data tersimpan **dengan** tashkeel penuh. Tanpa penyelesaian,
carian `كتب` tidak akan jumpa `كَتَبَ`.

### Penyelesaian GTAF
Tokenizer FTS5 custom ditulis dalam **C**, fungsi `remove_diacritic()` khas kesan &
buang titik-kod harakat Arab semasa proses `xTokenize`. Perlu `load_extension()` — extension
native yang mesti dikompil untuk setiap platform (Android NDK, iOS, Windows, dll).

### Sebab sebenar mereka guna C, bukan ciri terbina SQLite
SQLite sendiri **sudah ada** ciri terbina `unicode61 remove_diacritics=2` sejak **SQLite
3.27.0 (Februari 2019)** — jauh sebelum tokenizer GTAF ditulis (Nov 2022). Tapi:

- **Android tidak sokong `remove_diacritics=2` sehingga API 30 (Android 11, 2020)** —
  peranti lebih lama akan *crash* (`unknown tokenizer`) jika cuba guna ciri ini
- GTAF (1.5 juta pengguna, banyak peranti lama) **tak mampu** bergantung pada ciri SQLite
  terbina yang tak serasi ke belakang — jadi mereka terpaksa bina C extension sendiri
  untuk keserasian sejagat merentas semua versi Android/iOS

---

## 4. PENEMUAN #3 (KRITIKAL) — `remove_diacritics 2` TIDAK Berkesan Untuk Arab

Diuji secara empirikal dalam sandbox (Python 3, SQLite 3.46.1):

| Ujian | Diinsert | Dicari | Hasil |
|---|---|---|---|
| Kawalan LATIN | `café résumé` | `cafe` (tanpa aksen) | ✅ JUMPA |
| Kawalan LATIN | `café résumé` | `resume` (tanpa aksen) | ✅ JUMPA |
| **Arab bertashkeel** | `كَتَبَ خَالِدٌ` | `كتب` (tanpa tashkeel) | ❌ **TAK JUMPA** |

**Kesimpulan:** `tokenize='unicode61 remove_diacritics 2'` yang digunakan dalam `db.py`
projek ini **berfungsi sempurna untuk aksen Latin** tapi **tidak berkesan langsung untuk
harakat Arab** (U+064B–U+065F) — had reka bentuk ciri SQLite itu sendiri (fokus blok
Latin-1/Latin Extended), bukan isu versi/pemasangan.

### Kesan sebenar pada PustakaHadith
Data `hadis.arab` disimpan **penuh dengan tashkeel** (ikut `DEKLARASI.md`) dan diindeks
terus dalam `hadis_fts`. Bermakna: **carian Arab tanpa harakat (cara biasa orang taip)
tidak akan menemui hadis walaupun perkataan itu wujud tepat**. Carian makna (AI) tidak
menyelamatkan keadaan ini kerana ia guna matn **Melayu** untuk *embedding*, bukan Arab
(Sesi 20, `sesi_index.md`).

**Ini isu tersembunyi yang belum pernah direkodkan dalam dokumentasi projek sebelum ini.**

---

## 5. PENEMUAN #4 — Fungsi Normalisasi Arab SUDAH WUJUD (Separuh Jalan)

`core/eng_source.py` sudah ada fungsi `normalisasi()` dan pemalar `_DIAKRITIK` yang
tepat buang julat tashkeel yang sama:

```python
# 064B-0652 tashkeel · 0653-0655 maddah/hamzah · 0656-065F tanda tambahan
# 0670 alif khanjariyyah · 0640 tatweel · 06D6-06ED tanda mushaf
_DIAKRITIK = re.compile(r"[\u064B-\u065F\u0670\u0640\u06D6-\u06ED]")
```

**Tapi — AMARAN dari kod & dokumentasi sedia ada projek sendiri:**

`normalisasi()` turut melipat varian huruf (`ة→ه`, `أ/إ/آ→ا`, dll.) — sesuai untuk
**padanan sumber data** (`eng_source.py`, `sema_source.py`) tapi **DILARANG** untuk indeks
carian pengguna. Petikan terus dari `MULA_SINI.md` Peraturan #3:

> *"JANGAN lipat `ة → ه` dalam indeks carian — `نية` jadi `نيه` — tidak wujud. Carian
> pecah. (Untuk kunci padanan dalaman, OK.)"*

**Kesimpulan:** tak boleh guna semula `normalisasi()` bulat-bulat untuk FTS carian. Perlu
fungsi **baharu, lebih ringkas** — cuma buang tashkeel (guna semula `_DIAKRITIK`),
**tanpa** lipat varian huruf.

---

## 6. PENEMUAN #5 — MSIX & SmartScreen (Pembetulan Cadangan Awal)

Cadangan awal ("MSIX ada mekanisme pengesahan sendiri") **dibetulkan** selepas siasatan
lanjut — fakta sebenar lebih bernuansa:

| Laluan | Kos | Keputusan SmartScreen |
|---|---|---|
| MSIX melalui **Microsoft Store rasmi** | **PERCUMA** (yuran $19/$99 dibuang 2026) | ✅ Sifar amaran, serta-merta — Microsoft tandatangan semula pakej |
| MSIX diedar sendiri (S3/GitHub Releases, macam GTAF) | Perlu beli sijil (OV/EV) | ⚠️ Sama macam `.exe` biasa — reputasi kena dibina dari masa ke masa |
| Sijil EV | $400+/tahun | ⚠️ Sejak 2024, tak lagi bypass serta-merta |

**Penemuan penting:** Pendaftaran Microsoft Partner Center (individu **mahupun** syarikat)
kini **PERCUMA** (perubahan baharu 2026) — dulu $19 (individu) / $99 (syarikat).

**Cadangan dikemas kini:** laluan Microsoft Store patut naik taraf dari "pertimbangan"
kepada **disyorkan kuat** dalam `INSTALLER.md` — sifar kos, sifar amaran kekal selamanya,
cuma perlu lalui semakan Store (beberapa hari).

---

## 6b. PENEMUAN #6 — `text-matcher` (Repo GTAF, Java) — Bukti Bebas + Jurang Normalisasi

**Repo:** `github.com/GreentechApps/text-matcher` (2 bintang, 2019, tiada lesen dinyatakan)
**Konteks:** GTAF sendiri hadapi masalah **sama persis** dengan `core/padan.py`/
`eng_source.py` projek ini — memadan/interlink 42,000 hadis merentas app berbeza
berasaskan data sunnah.com.

### 6b.1 Bukti bebas: masalah "positif palsu daripada frasa pendek"

> *"We found many matches using \[SQLite FTS diacless\] method, however had to limit
> the match for longer texts only as it was very common that a **small sentence
> matched in many hadiths and in that case they really were not similar**."*

Ini **pengesahan bebas** (pasukan lain, tiada kaitan) bagi masalah yang projek ini
dokumen panjang lebar dalam `PERUBAHAN_30JUL.md` (lapisan `kata` sehala = 35.3%
positif palsu, Bukhari). Mengukuhkan keputusan projek bina sistem 5-lapisan +
pengesahan dua-hala berbanding padanan teks ringkas.

### 6b.2 Perbandingan algoritma

| | GTAF | PustakaHadith |
|---|---|---|
| Kaedah | Sørensen-Dice (n-gram aksara, 2-gram & 3-gram serentak) | Jaccard (token perkataan) |
| Ambang | 0.75 | 0.55–0.95 ikut lapisan |
| Cosine similarity | Dicuba dahulu, **ditolak** — "a lot of false positives... even when 90% match" | Tidak dicuba (GTAF sudah buktikan bermasalah) |
| Seni bina | O(n²) — padan semua-lawan-semua, ~4 jam segerak untuk 42,000 hadis | Indeks kunci kata jarang dahulu (kurangkan calon) — lebih cekap |

**Kesimpulan:** seni bina projek ini (indeks dahulu, bukan padan brute-force) **lebih
cekap** daripada pendekatan GTAF. Sørensen-Dice 2-gram+3-gram GTAF boleh jadi rujukan
kaedah tambahan masa depan jika `core/padan.py` perlu pilihan lain untuk teks panjang.

### 6b.3 Jurang kecil normalisasi Arab — CADANGAN, BUKAN diterap terus

Fungsi `normalize()` GTAF (Java) buang julat **tambahan** yang tiada dalam
`core/eng_source.py::_DIAKRITIK` projek ini:

```java
.replaceAll("\u0610", "")  // ARABIC SIGN SALLALLAHOU ALAYHE WA SALLAM
.replaceAll("\u0611", "")  // ARABIC SIGN ALAYHE ASSALLAM
.replaceAll("\u0612", "")  // ARABIC SIGN RAHMATULLAH ALAYHE
.replaceAll("\u0613", "")  // ARABIC SIGN RADI ALLAHOU ANHU
.replaceAll("\u0614", "")  // ARABIC SIGN TAKHALLUS
```

`\u0610`–`\u0614` ialah titik kod Unicode **tersendiri** untuk simbol selawat/
rahimahullah tertanam — **berbeza** daripada `LIGATUR_SELAWAT` (`\ufdfa`) yang sudah
dikendali `utils/bahasa.py`. `_DIAKRITIK` sedia ada (`\u064B-\u065F\u0670\u0640
\u06D6-\u06ED`) tidak meliputi julat ini.

**Status tindakan (dikemas kini 15 Ogos 2026):**
- ✅ **DITERAP** dalam draf `dokumen/rujukan/DRAF_carian_arab.md` (`_TASHKEEL` untuk
  carian FTS baharu) — fail ini belum wujud dalam kod hidup.
- ✅ **DITERAP DAN DISAHKAN** pada `core/eng_source.py::_DIAKRITIK` sebenar.
  `uji_pembetulan_diakritik.py` membina baseline lama dengan mengganti satu
  regex sahaja, kemudian menjalankan `audit_eng.py --semua` pada kedua-dua
  keadaan. Output lama dan baharu **identik**:
  - Disemak: 30,547
  - Disahkan: 30,541
  - Disyaki: 6
  - Tiada perubahan bagi mana-mana kitab, kaedah padanan atau baris disyaki.

  Enam baris disyaki ialah keadaan baseline yang sama, bukan kesan julat
  `\u0610-\u0614`. Perubahan selamat dikekalkan berdasarkan audit bebas.

---

## 6c. PENEMUAN #7 — Versi Web `hadith.gtaf.org` (14 Ogos 2026, susulan)

GTAF turut ada **versi web** app Hadis (bukan sekadar mobile/desktop):
`https://hadith.gtaf.org/`.

### 6c.1 Pengesahan tambahan — tiada Melayu/Indonesia (bukti laluan URL, bukan teks pemasaran)

Dicuba terus laluan bahasa:

```
hadith.gtaf.org/ms/topics/1  -> "Application error: a server-side exception has occurred"
hadith.gtaf.org/id/topics/1  -> "Application error: a server-side exception has occurred"
hadith.gtaf.org/en/topics/1  -> berfungsi normal
```

Laluan `ms`/`id` **tidak wujud** dalam struktur routing app web mereka — bukti lebih
kukuh daripada sekadar teks perihalan Play Store. Mengesahkan sepenuhnya §2.

### 6c.2 Ciri UX menarik (bahan rujukan produk masa depan, BUKAN keutamaan semasa)

Dari halaman hadis individu (`hadith.gtaf.org/bukhari/1/1`):

- **"13 similar ahadith"** — pautan terus ke hadis LAIN yang serupa/berkaitan.
  Kemungkinan besar hasil kerja `text-matcher` (§6b) yang diterapkan pada produk
  akhir. Sepadan dengan ciri Play Store "Find Similar Ahadith".
- **"Narration chain"** — paparan rantaian sanad berasingan daripada teks utama
  (bukan sekadar teks mentah tertanam dalam matan macam pendekatan semasa).

Kedua-dua ciri ini **bukan keutamaan semasa** untuk PustakaHadith (skop sedia ada
sudah luas), tapi wajar direkod sebagai idea *roadmap* jangka panjang jika projek
berkembang selepas keperluan teras (lesen, installer, carian Arab) selesai.

### 6c.3 ⚠️ AMARAN METODOLOGI — Kiraan Jumlah Hadis Berbeza Merentas Sumber

Jumlah hadis per-kitab yang dipaparkan `hadith.gtaf.org` **berbeza ketara** daripada
hadis.my (sumber PustakaHadith):

| Kitab | GTAF web | PustakaHadith (hadis.my) |
|---|---|---|
| Bukhari | 7,563 | 7,008 |
| **Muslim** | **3,033** | **5,362** |
| Nasa'i | 5,758 | 5,662 |
| Abu Dawud | 5,274 | 4,590 |
| **Ahmad** | **4,376** | **26,363** |

Perbezaan besar (Muslim, Ahmad) berkemungkinan disebabkan **kaedah kiraan berbeza**
(cth. GTAF mungkin kira ikut nombor rujukan dalam-buku tertinggi/dedup riwayat
berulang; hadis.my mungkin kira setiap kemasukan termasuk pertindihan/riwayat
berlainan sanad bagi matan sama). **Ini bukan penunjuk mana sumber "lebih betul"**
— cuma definisi "satu hadis" berbeza antara projek.

**AMARAN PENTING untuk `DEKLARASI.md`:** JANGAN bandingkan "jumlah hadis" merentas
platform secara terus tanpa nyatakan kaedah kiraan — berisiko mengelirukan pembaca
(cth. PustakaHadith kelihatan "lebih sedikit" untuk Ahmad walhal 26,363 vs 4,376
mungkin sebenarnya lebih LENGKAP, bukan kurang, bergantung definisi kiraan).
Jadual perbandingan (§7) perlu tambah nota kaki menjelaskan ini.

---

## 7. Jadual Perbandingan (Cadangan Tambahan `DEKLARASI.md`)

```markdown
| | PustakaHadith | GTAF Hadith Collection |
|---|---|---|
| Fokus | ensiklopedia 9 kitab, BM | ensiklopedia 15+ kitab, antarabangsa |
| Pengguna sedia ada | belum dilancar | 1.5 juta+ (9 tahun) |
| Bahasa Melayu (kandungan hadis) | ✅ | ❌ (Inggeris/Bengali/Urdu sahaja) |
| Luar talian | ✅ | ✅ |
| Carian makna (AI) | ✅ e5-small + FAISS | ❌ (carian kata sahaja) |
| Biografi perawi | ❌ | ✅ 25,000+ ulama |
| Platform | Windows (belum installer) | Android, iOS, Windows, Mac |
```

> **Nota kaki disyorkan (§6c.3):** jika jadual ini dikembangkan untuk sertakan
> "jumlah hadis", WAJIB nyatakan kaedah kiraan — GTAF dan hadis.my kira "satu
> hadis" secara berbeza (cth. Musnad Ahmad: 4,376 GTAF vs 26,363 hadis.my).
> Angka mentah tanpa konteks boleh mengelirukan pembaca.

---

## 8. Tindakan Disyorkan

| # | Tindakan | Fail terjejas | Keutamaan |
|---|---|---|---|
| 1 | Tambah `arab_carian` + FTS tanpa tashkeel | `db.py`, `sync.py`, `uji_carian_arab.py` | ✅ Selesai; lulus pada salinan konsisten DB Windows sebenar 62,169 hadis |
| 2 | Tambah jadual perbandingan GTAF ke `DEKLARASI.md` | `dokumen/rujukan/DEKLARASI.md` | 🟡 Sederhana |
| 3 | Naik taraf MSIX+Store ke laluan utama; tambah langkah PyInstaller 6.22 → Inno → MSIX → Partner Center | `dokumen/rujukan/INSTALLER.md` | ✅ Dokumentasi selesai; binaan Windows belum dijalankan |
| 4 | (Tidak disyorkan) Port `sqlite3-arabic-tokenizer` C — tidak perlu, projek desktop kawal sepenuhnya versi Python/SQLite dibundle | — | ⚫ Tidak perlu |
| 5 | Julat `\u0610-\u0614` ditambah ke `_TASHKEEL` draf (`DRAF_carian_arab.md`) — SUDAH selesai | `dokumen/rujukan/DRAF_carian_arab.md` | ✅ Selesai |
| 6 | Tambah `\u0610-\u0614` ke `core/eng_source.py::_DIAKRITIK` — audit lama/baharu 30,547 hadis identik | `core/eng_source.py`, `audit_eng.py` | ✅ Selesai dan disahkan |
| 7 | Tambah nota kaki kaedah kiraan hadis jika jadual §7 dikembangkan (elak salah tafsir angka) | `dokumen/rujukan/DEKLARASI.md` | 🟡 Sederhana |
| 8 | (Roadmap jangka panjang, bukan keutamaan) Ciri "Hadis Serupa" & "Rantaian Sanad berasingan" — rujuk `text-matcher` §6b untuk asas teknikal | — | ⚫ Masa depan |

---

*Dokumen ini rekod siasatan sesi 14 Ogos 2026. Draf kod migrasi skema untuk item #1
disediakan berasingan.*
