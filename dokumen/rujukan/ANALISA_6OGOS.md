# Analisis Keseluruhan — PustakaHadith v1.0

**Tarikh:** 6 Ogos 2026
**Kaedah:** 31 fail sumber dimuat turun dari Google Drive dan diperiksa terus
(bukan daripada dokumen). Sintaks disemak, `requirements.txt` diuji dengan
`packaging`, saiz fail dan struktur DB diukur.

**Keputusan ringkas:** seni bina kukuh, sifar ralat sintaks. Tujuh kekurangan
dikenal pasti — dua kritikal, tiga sederhana, dua rendah.

---

## 1. Kekuatan yang disahkan

| perkara | bukti diukur |
|---|---|
| Padanan berbilang lapisan | 5 lapisan + Jaccard dua hala; audit **30,541 disahkan, 0 salah** |
| Carian makna e5-small | skor 0.21 → **0.85** selepas matn Melayu + prompt `query:`/`passage:` |
| Disiplin pengawal | Fath al-Bari ditolak (nisbah 1.00x < 1.8x) walaupun menyakitkan |
| Fix DLL Qt/torch | punca dikesan tepat: MSVC 14.26 (PyQt5) vs 14.44 (torch) |
| Ujian automatik | `semak.py` 1,222 baris, **17 fungsi ujian** |
| Buang huraian auto | 195 baris + `phase4_exegesis.py` + `PipelineWorker` dipadam, bukan disembunyikan |
| Skema DB | 9 jadual, **6 indeks** — tiada jadual besar tanpa indeks |

Struktur fail (31 modul Python):

```
akar     : main.py launcher.py config.py db.py semak.py semak_db.py
           audit_eng.py sync*.py VERSI.py
core/    : eng_source · sema_source · semantic_search · draft_answer
           hadeethenc_api · syarah_source · phase2 · phase3
ui/      : app_qt · pages · widgets · theme · workers · settings_panel
utils/   : bahasa · transliteration
scripts/ : build_faiss_index · muat_turun_sema
```

---

## 2. Kekurangan mengikut keutamaan

### 🔴 KRITIKAL 1 — `requirements.txt` mengandungi versi tidak sah

```
sentence-transformers>=2.2.2.2.2      <- LIMA segmen
```

Versi sebenar ialah `2.2.2`. Diuji dengan `packaging`: ia **diterima tanpa
ralat**, tetapi tiada versi sedemikian pernah wujud, jadi kekangan itu tidak
bermakna.

Risiko sebenar: `torch` **langsung tidak disenaraikan**, walaupun ia punca
crash terbesar projek ini (Sesi 19 dan Sesi 20 samb. 2). Jika pip
menyelesaikan `sentence-transformers` kepada versi lama yang menarik
`torch` tanpa wheel Python 3.14, keadaan `fix.bat` Sesi 19 berulang.

**Cadangan** — pin kepada versi yang sudah disahkan berfungsi:

```
PyQt5>=5.15.11
requests>=2.28.0
pyperclip>=1.8.0
tqdm>=4.65.0

# Carian Makna (AI) — versi ini disahkan ada wheel Python 3.14 (Sesi 19)
torch>=2.6
sentence-transformers>=5.0
faiss-cpu>=1.9
```

---

### 🔴 KRITIKAL 2 — Fix DLL bergantung pada PowerShell semasa runtime

`main.py::_baik_pulih_dll_qt_torch()` memanggil
`os.popen('powershell -NoProfile -Command Get-ChildItem ...')` sebelum
import PyQt5.

Tiga risiko:

1. **Kegagalan senyap** — jika dasar pelaksanaan PowerShell disekat (biasa
   pada mesin korporat), `senarai` kosong, tiada DLL dialih, apl crash
   `WinError 1114` tanpa petunjuk punca.
2. **Kelewatan permulaan** — spawn PowerShell pada setiap pelancaran.
3. **Tidak kekal** — ia mengubah `site-packages`. Jika pengguna menjalankan
   `pip install --force-reinstall PyQt5`, DLL kembali dan apl rosak semula
   tanpa amaran.

**Cadangan** (pilih satu):

- **A (disyorkan):** pin PyQt5 kepada versi yang membundel runtime serasi —
  masalah dielak sepenuhnya, tiada kod pembaikan diperlukan.
- **B:** baca versi DLL dengan `ctypes` (`GetFileVersionInfoW`) — tiada
  subproses, tiada kebergantungan dasar PowerShell.
- **C:** kekalkan pendekatan semasa tetapi **lapor kegagalan dengan jelas**
  kepada pengguna, jangan `except: pass`.

Nota: blok `try/except Exception: pass` yang membungkus seluruh fungsi
bermakna **setiap** kegagalan senyap. Itu bertentangan dengan corak
projek ini di tempat lain (pengawal syarah, audit) yang gagal dengan kuat.

---

### 🟠 SEDERHANA 3 — Lapan skrip build usang masih ada

```
build.py              build_index.py       build_index_now.py
build_semantic.py     run_build.py         run_semantic_build.py
start_build.py        check_build.py
```

Sesi 20 sendiri menamakannya *"fail wrapper usang yang tidak digunakan"*.
Skrip sebenar: **`scripts/build_faiss_index.py`**.

Ini bukan isu kekemasan sahaja — ia **perangkap**. Sesi akan datang (atau
pengguna sendiri beberapa bulan kemudian) akan menjalankan `build.py` dan
tertanya-tanya mengapa indeks tidak terbina.

**Cadangan:** alih ke `_arkib/` atau padam. Jika ragu, `_arkib/` cukup —
yang penting ia keluar dari aras akar.

---

### 🟠 SEDERHANA 4 — Lesen SemakHadis.com belum diselesaikan

Sesi 18.8 mencatat: *"SemakHadis.com tidak menyatakan lesen semula data
secara eksplisit... Sebelum edaran komersial, dapatkan kebenaran bertulis."*

Sejak itu padanan bertambah **2,045 → 4,237**. Selepas huraian auto dibuang
(Sesi 18.9), SemakHadis ialah **satu-satunya sumber huraian** dalam apl.

Jika kebenaran ditolak, ciri huraian hilang sepenuhnya — tiada sandaran.

Ini satu-satunya isu dalam senarai ini yang **tidak boleh diselesaikan
dengan kod**, dan tempoh jawapannya di luar kawalan. Sebab itu ia patut
dimulakan lebih awal daripada kerja teknikal yang lain.

**Cadangan:** hantar permohonan bertulis minggu ini. Sertakan: tujuan
bukan komersial, atribusi yang sudah dipaparkan, dan tawaran pautan balik.

---

### 🟠 SEDERHANA 5 — `README.md` dalam Bahasa Inggeris dan skopnya salah

Seluruh projek Bahasa Melayu. `README.md` — fail pertama yang dibuka
sesiapa — dalam English, dan menerangkan **hanya** ciri carian semantik:

```
# PustakaHadith - Semantic Search Implementation
This project implements semantic search for PustakaHadith using FAISS...
```

Ia tidak menyebut 62,169 hadis, 9 kitab, SemakHadis, darjat ulama,
transliterasi, atau terjemahan Inggeris. Pembaca akan menyangka ini projek
carian vektor, bukan PustakaHadith.

`core/draft_answer.py` juga menggunakan docstring English
(`"""Draft answer composer for semantic search results."""`) sedangkan
modul lain BM.

**Cadangan:** tulis semula `README.md` dalam BM sebagai gambaran
keseluruhan; pindahkan butiran carian semantik ke bahagian di dalamnya.

---

### 🟡 RENDAH 6 — `ui/app_qt.py` 1,725 baris

Satu fail memegang 7 halaman, navigasi, dan penyelarasan worker. Setiap
perubahan UI menyentuh fail yang sama.

Bukan masalah hari ini, tetapi ia akan menjadi kesesakan apabila ciri
bertambah.

**Cadangan (tidak mendesak):** `ui/pages/` — satu fail satu halaman,
kekalkan `app_qt.py` sebagai penyelaras sahaja.

Saiz fail lain untuk perbandingan:

```
1,725  ui/app_qt.py
1,222  semak.py
  815  ui/settings_panel.py
  664  ui/widgets.py
  565  core/eng_source.py
```

---

### 🟡 RENDAH 7 — Model tidak dibundel, tiada pengesahan muat turun

Pengguna kali pertama perlu memuat turun e5-small (~120 MB) secara senyap
pada carian makna pertama. Jika rangkaian terputus separuh jalan, gejalanya
ialah crash yang tidak menjelaskan puncanya.

**Cadangan:** semak kewujudan + saiz model sebelum guna; jika tiada, papar
mesej jelas ("Model carian makna belum dimuat turun — 120 MB diperlukan")
dan bukan traceback.

---

## 3. Perkara yang DISEMAK dan didapati SELAMAT

| perkara | dapatan |
|---|---|
| `core/draft_answer.py` menjana teks agama? | **Tidak.** Ia hanya meringkas hasil carian (senarai rujukan + pratonton). Tiada penjanaan hukum atau tafsiran. Selamat. |
| Import torch pada aras modul? | **Tidak.** `semantic_search.py` sudah lazy (`_load_model`/`_load_index`), dengan `faiss_available()`/`torch_available()`. Betul. |
| Jadual DB tanpa indeks? | **Tiada.** 9 jadual, 6 indeks pada semua lajur carian. |
| Ralat sintaks? | **0** merentas 31 fail. |

---

## 4. Susunan kerja yang disyorkan

### Hari ini (~30 minit)

1. Betulkan `requirements.txt` — pin versi disahkan, tambah `torch`
2. Alih 8 skrip build usang ke `_arkib/`
3. Tulis semula `README.md` dalam BM

### Minggu ini

4. **Hantar permohonan lesen SemakHadis.com** — jangka masa di luar kawalan,
   mulakan awal
5. Ganti fix DLL PowerShell dengan `ctypes`, atau pin PyQt5 (Pilihan A/B)

### Kemudian (tidak mendesak)

6. Pecahkan `ui/app_qt.py` kepada `ui/pages/`
7. Semakan integriti model + mesej ralat jelas

---

## 5. Nota metodologi

Analisis ini memeriksa **kod sebenar**, bukan dokumen. Dua dapatan hanya
kelihatan dengan cara itu:

- Versi `2.2.2.2.2` tidak disebut dalam mana-mana dokumen sesi
- Kebergantungan PowerShell dalam fix DLL didokumenkan sebagai "selesai",
  tetapi mod kegagalannya tidak dibincangkan

Ini selari dengan pelajaran berulang projek ini: **dokumen mencatat niat;
hanya ujian terhadap artifak sebenar mendedahkan keadaan.**
