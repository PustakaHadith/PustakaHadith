# PustakaHadith

Pustaka digital **62,169 hadis** daripada 9 kitab utama, dengan carian kata
kunci dan carian makna (AI), huraian SemakHadis.com, darjat ulama, syarah,
transliterasi, dan terjemahan Melayu/Indonesia/Inggeris.

## Isi Kandungan

- [Ciri-ciri](#ciri-ciri)
- [Pemasangan](#pemasangan)
- [Cara Guna](#cara-guna)
- [Struktur Projek](#struktur-projek)
- [Carian Makna (AI)](#carian-makna-ai)
- [Pembangunan](#pembangunan)
- [Penyelesaian Masalah](#penyelesaian-masalah)
- [Lesen](#lesen)

---

## Ciri-ciri

| Ciri | Butiran |
|---|---|
| **9 kitab hadis** | Bukhari, Muslim, Abu Daud, Tirmizi, Nasa'i, Ibnu Majah, Ahmad, Darimi, Malik |
| **62,169 hadis** | Disimpan dalam SQLite (`hadis.db`) dengan indeks FTS5 |
| **Carian gabungan automatik** | Carian kata kunci (FTS5) + carian makna (AI) berjalan selari setiap carian |
| **Jawapan draf AI** | Ringkasan padanan makna + rujukan teratas bagi setiap carian |
| **Huraian SemakHadis.com** | 4,237 hadis — tajuk, syarah, dan maklumat darjat (atribusi dipaparkan) |
| **Sandaran HadeethEnc** | 310 padanan matn — huraian Melayu dipapar bila SemakHadis tiada (v1.1) |
| **Darjat ulama** | 63,930 rekod — klasifikasi Sahih/Hasan/Da'if dsb. mengikut penilaian ulama |
| **Pembahagian bab** | 31,322 rekod bab untuk navigasi bertema |
| **Mesej bantuan carian** | Bila kata kunci pulang 0 hasil tetapi AI ada padanan (cth. "hukum riba"), nota menerangkan mengapa dan mengarah ke hasil makna |
| **Tab bahasa dua lajur** | Butiran hadis: lajur kanan tab **ARAB \| TRANSLITERASI** (2 gaya rumi), lajur kiri tab **Melayu \| Indonesia \| English** — susunan RTL (Arab di kanan, terjemahan di kiri, 14 Ogos) · teks terjemahan sentiasa sama paras dengan Arab |
| **Bar teks `Lapor ralat \| Kongsi \| Salin`** | Di bawah terjemahan (tiru sunnah.com): Lapor ralat → sunnah.com; Kongsi → WhatsApp ikut bahasa semasa; Salin → menu 3 pilihan (Arab sahaja / terjemahan semasa / Arab + terjemahan semasa). 💬 WhatsApp juga di bar tajuk |
| **Skrin pemula (splash)** | Fasa muat model carian makna dipapar dengan bar kemajuan — pengguna tahu apl tidak beku; boleh dilangkau dengan klik (v1.3) |
| **Lompat terus ke hadis** | Taip `bukhari 433`, `B433`, `b:433` di bar carian untuk buka kitab pada kad hadis, atau `433` sahaja untuk buka butiran terus; kotak "Lompat No. hadis" di atas senarai + pintasan `Ctrl+G` pada halaman kitab (v1.3) |
| **Ralat diterjemah Melayu** | 23 corak ralat runtime (sqlite3/requests/OSError/faiss/HTTP/JSON) dipetakan ke mesej mesra pengguna sebelum dipapar |
| **Syarah & transliterasi** | Transliterasi Arab dan syarah tambahan |
| **4 bahasa** | Arab, Melayu, Indonesia, Inggeris |
| **Penanda halaman** | Simpan hadis kegemaran |
| **Mod luar talian** | Semua data tempatan — tiada internet diperlukan selepas pemasangan |

---

## Pemasangan
 
 Aplikasi ini diedarkan sebagai **aplikasi Windows langsung** — **tiada Python diperlukan**.
 
 ### 1. Microsoft Store (MSIX) — *Akan Datang*
 
 Buka **Microsoft Store** → cari **"PustakaHadith"** → klik **Pasang**.
 
 > *Memerlukan pendaftaran Partner Center — sedang dalam proses.*
 
 ### 2. Pemasang EXE (Inno Setup) — **Sedia**
 
 1. Muat turun `PustakaHadith-Setup-1.0.0-x64.exe` daripada laman rasmi / GitHub Releases.
 2. Klik dua kali fail → ikut wizard pemasangan (bahasa Melayu).
 3. Pilih folder pemasangan (lalai: `%LOCALAPPDATA%\Programs\PustakaHadith`).
 4. Tandakan "Cipta pintasan Desktop" jika dikehendaki.
 5. Klik **Selesai** — aplikasi sedia digunakan.
 
 **Naik taraf:** Jalankan pemasang versi baharu atas versi lama — data anda (tetapan, penanda buku, data hadis) **tidak dipadam**.
 
 **Nyahpasang:** *Tetapan → Aplikasi → Aplikasi dipasang → PustakaHadith → Nyahpasang* (data pengguna kekal di `%LOCALAPPDATA%\PustakaHadith`).
 
 ### 3. ZIP Mudah Alih (Portable) — **Sedia**
 
 1. Muat turun `PustakaHadith-portable-1.0.0-x64.zip`.
 2. **Extract penuh** ke folder (contoh: `D:\PustakaHadith`). **Jangan jalankan dari dalam ZIP.**
 3. Klik dua kali `PustakaHadith.exe`.
 4. Untuk akses mudah: klik kanan `PustakaHadith.exe` → **Hantar ke → Desktop (cipta pintasan)**.
 
 **Tiada pemasangan sistem** — buang = padam folder sahaja. Data pengguna kekal di `%LOCALAPPDATA%\PustakaHadith`.
 
 ---
 
 ### Keperluan Sistem
 
 | Item | Minimum |
|---|---|
| **OS** | Windows 10 / 11 (64-bit) |
| **RAM** | 4 GB (disyorkan 8 GB+) |
| **Ruang Cakera** | 2 GB (aplikasi 1.4 GB + data pengguna) |
| **Internet** | Diperlukan untuk sync data hadis (sekali sahaja) |
| **Python** | **TIDAK diperlukan** — serba lengkap |

---

## Cara Guna

```bash
python main.py
```

Lancarkan aplikasi, kemudian:

1. **Cari** — taip soalan atau kata kunci (contoh: "hukum makan riba",
   "kelebihan bersedekah", "niat puasa"). Kedua-dua carian kata kunci dan
   carian makna berjalan automatik; jawapan draf AI dipaparkan di atas.
2. **Semak hadis** — klik kad hadis untuk lihat penuh: Arab, terjemahan,
   transliterasi, darjat, dan syarah.
3. **Tandakan** — klik ikon bintang untuk menyimpan hadis ke penanda halaman.
4. **Tukar bahasa & fon** — klik ikon **⚙ gear** di penjuru atas kanan untuk panel Tetapan (fon Arab, saiz, tema).

Carian menapis ikut kitab melalui senarai pilihan di atas kotak carian.

---

## Struktur Projek

```
akar     : main.py launcher.py config.py db.py semak.py semak_db.py
           sync*.py VERSI.py requirements.txt
core/    : eng_source · sema_source · semantic_search · draft_answer
           hadeethenc_api · syarah_source · phase2 · phase3
ui/      : app_qt · pages · widgets · theme · workers · settings_panel
utils/   : bahasa · transliteration
scripts/ : build_faiss_index · muat_turun_sema
_arkib/  : skrip usang (tidak aktif)
```

Fail utama:

- `main.py` — titik masuk aplikasi
- `db.py` — skema SQLite, indeks FTS5, migrasi
- `ui/app_qt.py` — antara muka PyQt5 (6 halaman)
- `ui/workers.py` — semua I/O rangkaian/DB berjalan dalam QThread
- `core/semantic_search.py` — enjin carian makna (FAISS + e5-small)
- `core/draft_answer.py` — penggubal jawapan draf

---

## Carian Makna (AI)

Carian makna memadankan hadis **ikut maksud**, bukan sekadar perkataan sama.
Ia berguna untuk soalan berbeza perkataan tetapi sama maksud (contoh: mencari
"hukum riba" sedangkan teks hadis guna "faedah").

Carian kata kunci (FTS5) memadankan dengan AND — semua perkataan mesti
hadir serentak. Jika carian pulang 0 hasil kata kunci tetapi AI menjumpai
padanan makna, aplikasi memaparkan nota bantuan yang menerangkan sebab dan
mengarahkan anda ke hasil makna di bawah.

- Model: **intfloat/multilingual-e5-small** (pelbagai bahasa, ~0.46 GB)
- Indeks: **FAISS**, 62,169 vektor, dimensi 384
- Ambang: skor minimum 0.6 (boleh ubah dalam `semantic_search.py`)

Model dimuat turun automatik pada kali pertama (perlu internet).

**Bina semula indeks** (jika model/teks berubah):

```bash
python scripts/build_faiss_index.py
```

Semak status indeks:

```bash
python -c "from core.semantic_search import get_index_stats; print(get_index_stats())"
```

---

## Pembangunan

Ujian automatik:

```bash
python semak.py                  # semakan pra-hantar: integriti padanan, DB,
                                 # susun atur, versi, dokumen, fail sisa, #12
                                 # 'Sesi Terakhir' + #15 ringkasan satu muka
                                 # seiring git log
python semak_db.py               # audit struktur & indeks pangkalan data
python semak_versi.py            # semak versi semasa + ciri yang dijanjikan

# Suite pra-hantar rasmi (14 ujian — semak.py + 13 suite; log: bukti_visual/):
python uji_pra_hantar.py         # SEMUA LULUS = selamat hantar

# Ujian mutasi negatif (semakan semak.py benar-benar mengesan pepijat):
python uji_negatif_8z.py         # 55/0 — 36 cabang GAGAL dimutasi + pulihan byte-tepat

# Ujian parser (tiada GUI):
python uji_lompat.py             # parser 'lompat ke hadis': ejaan kitab & format (bukhari 433, B433, b:433)
python uji_lompat_fungsi.py      # fungsi penuh 'lompat': parser + halaman + skrol ke kad + buka butiran

# Ujian integrasi UI (lancarkan aplikasi secara automatik):
python uji_data_baharu.py        # data baharu: bab, darjat, sema, sandaran HadeethEnc
python uji_tukar_tema.py         # tukar tema berulang + carian, tanpa kebocoran widget
python uji_end_to_end.py         # aliran penuh: kitab → butiran → 3 tab bahasa → penanda buku → carian
python uji_bandingan.py          # 3 tab bahasa (mockup), teks sama paras dengan Arab, nyahdaya bila tiada bahasa
python uji_splash.py             # rantaian splash → fasa pramuat → model sedia (~30s, muat model sebenar)
python uji_visual_sebenar.py     # tangkapan skrin sebenar, kedua-dua tema (perlu skrin)
python uji_visual_ralat.py       # toast ralat diterjemah Melayu (skrin sebenar, perlu skrin)
```

Langkah pengesahan:

```bash
python semak.py && python semak_versi.py      # 394 semakan (15 bahagian) + versi
                                 # (folder binaan bukan git + tiada cache pengguna:
                                 #  semak #12 bandingan git & sebahagian #9 dilangkau;
                                 #  +1 kerana dokumen CHECKLIST_PEMANTAUAN.md baharu)
QT_QPA_PLATFORM=offscreen python uji_data_baharu.py   # Windows: jalankan seperti biasa
```

Sesetengah ujian `semak.py` dijalankan tanpa fail data untuk mengelak
kegagalan palsu; lihat `_arkib/` untuk skrip usang yang tidak perlu
dijalankan.

---

## Penyelesaian Masalah

**Apl crash `WinError 1114` / DLL:** sebabnya konflik runtime MSVC antara
PyQt5 dan torch. `main.py` membaiki ini automatik pada pelancaran. Jika masih
gagal, pasang semula PyQt5 (versi membundel runtime serasi) dan pastikan
`torch>=2.6` dipasang.

**Indeks carian makna tiada:**

```bash
python scripts/build_faiss_index.py
```

**Model belum dimuat turun:** pada carian pertama, model e5-small (~0.46 GB)
dimuat turun dari Hugging Face — perlu sambungan internet.

**Database tidak jumpa:**

```bash
python sync.py
```

---

## Lesen

Data hadis bersumber daripada `service.hadis.my`. Huraian daripada
**SemakHadis.com** — digunakan dengan atribusi dalam aplikasi. Sebelum edaran
komersial, dapatkan kebenaran bertulis daripada SemakHadis.com.

Sebahagian struktur projek ini adalah ringkasan perjalanan pembangunan; rekod
penuh (alasan reka bentuk, audit, sesi) ada dalam `dokumen/sesi/sesi_index.md`.
Perbandingan paparan detail hadis **lama → baharu** (susun atur dua lajur,
palet kertas hangat, cip warna) dengan tangkap layar ada dalam
`dokumen/manual/TRANSFORMASI_DETAIL.md`. Log perubahan harian terbaru
(13 Ogos — buang tab Sebelah, teks sama paras, lalai Arab Kecil,
pembetulan draf jawapan AI): `dokumen/perubahan/PERUBAHAN_13OGOS.md`.
