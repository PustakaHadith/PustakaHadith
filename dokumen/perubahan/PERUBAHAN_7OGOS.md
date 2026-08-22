# Perubahan 7 Ogos 2026 — Siasatan & Pembaikan Crash Carian Gabungan (0xC0000409)

Ringkasan sesi. Arkib penuh: `sesi_index.md`.

---

## 1. Gejala

Aplikasi (`app_qt.py`) **crash keras `0xC0000409`** (fail-fast, EXIT=-1073740791
dalam PowerShell; tiada jejak `PYTHONFAULTHANDLER`) apabila menjalankan **carian
gabungan** (keyword + semantik) pada sesetengah mesin. Crash berlaku tanpa mesej
Python — proses mati serta-merta.

Lingkungan ujian: Windows/PowerShell, `QT_QPA_PLATFORM=offscreen`,
`python -u` + redirect output, semak `EXIT=$LASTEXITCODE`.

---

## 2. Punca #1 (disahkan): pra-muat model dalam `__init__` serentak dengan CollectionsWorker

Eksperimen penghapusan (`C:\Users\MKAW\AppData\Local\Temp\opencode\uji_*.py`):

| ujian | keadaan | keputusan |
|---|---|---|
| `uji_idle.py` | pra-muat `__init__` AKTIF + kad dipapar + idle | EXIT=-1073740791 |
| `uji_kad_sahaja.py` | pra-muat `__init__` AKTIF, tampal + idle | EXIT=-1073740791 |
| `uji_nodraf2.py` | draf dikosongkan (patch) | masih crash → draf bukan punca |
| `uji_kad_simple.py` | kad diganti QLabel ringkas | gantung (bukan crash) |
| `uji_both.py` | kad ringkas + draf kosong | EXIT=0 |
| **`uji_nopre.py`** | **pra-muat `__init__` DILUMPUHKAN** + `_tampal_gabungan` penuh + idle | **EXIT=0, KAD=21** |

**Kesimpulan:** fail-fast berpunca daripada `_pra_muat_model()` yang dipanggil
dalam `__init__` (muat model torch serentak dengan `CollectionsWorker`),
BUKAN daripada kad, draf, `w.show()`, atau `semantic_search` kedua.

### Pembaikan awal yang dilaksanakan

- `ui/app_qt.py` `__init__`: **buang** `self._pra_muat_model()` (baris ±151).
- `_do_search`: panggil `self._pra_muat_model()` sebelum worker dimulakan.
- `_tampal_gabungan` hanya dipanggil dari isyarat `finished` QThread (bukan
  dari callback `done`) — `_on_search`, `_on_semantic_search`,
  `_on_semantic_failed` kini hanya set state (`_kw_res`, `_sem_res`, ...).
- `core/draft_answer.py`: `compose_draft_answer(..., semantic_results=None)`
  guna hasil semantik pra-kira → tiada `semantic_search` kedua.
- `_run`/`_run_semantic_search`: pasang `worker.finished.connect(...)`.

Ujian pengesahan awal: `uji_delay.py` dan `uji_gabung_ui.py` → **EXIT=0**.

---

## 3. Isu kedua: carian pertama membeku UI ~30s (pra-muat dalam `_do_search`)

`_load_model()` mengambil ~27–45s setiap proses:
- `local_files_only=True` menyingkir semakan metadata HF Hub (~18s): muat
  model turun dari ~45s → ~27s. Diterapkan dalam `core/semantic_search.py`
  `_load_model()` (cuba cache dahulu, fallback muat turun).

Ukuran per komponen (proses segar):

| komponen | masa |
|---|---|
| import sentence_transformers/torch | ~21s |
| `SentenceTransformer(...)` muat model | ~5s |
| `_load_index()` (faiss) | ~0.4s |
| `_load_id_map()` (pickle) | ~0.1s |
| `semantic_search()` encode + search | ~0.4s |

Maka pra-muat dalam `_do_search` (thread utama) membekukan UI ~30s pada
carian pertama (`uji_timing.py`: `_do_search` ambil 33s).

---

## 4. Punca #2 (disahkan): model dimuat dalam THREAD UTAMA, kemudian encode dalam QThread → crash

Ujian selepas pra-muat dipindah ke `_fetch_collections`
(`worker.finished.connect(self._pra_muat_model)`):

| ujian | keadaan | keputusan |
|---|---|---|
| `uji_pra_selepas.py` | pra-muat thread utama selepas Collections, TIADA carian | EXIT=0 |
| `uji_cari_pantas.py` | pra-muat thread utama, KEMUDIAN carian → encode QThread | **EXIT=-1073740791** |
| `uji_gabung_ui.py` / `uji_delay.py` | model dimuat oleh `SemanticWorker` dalam QThread sendiri | EXIT=0 |
| **`uji_pre_qthread.py`** | **pra-muat dalam QThread background**, kemudian carian | **EXIT=0, KAD=21, workers selesai** |

**Kesimpulan muktamad:** selamat HANYA jika model dimuat dalam QThread dan
di-encode dalam QThread. Model yang dimuat dalam thread utama kemudian
di-encode dalam `SemanticWorker` (QThread) masih mencetuskan fail-fast
0xC0000409.

**Cadangan penyelesaian akhir (SELESAI diterapkan dalam Sesi 22 — lihat §6):**
pra-muat model dalam QThread background (`PreloadWorker`) selepas
`CollectionsWorker` selesai, dengan `threading.Lock` dalam `_load_model`
supaya `SemanticWorker` menunggu jika pra-muat belum siap. Ini membolehkan
carian pertama pantas + UI tidak beku + tiada crash.

---

## 5. Status semasa kod (7 Ogos 2026, TAMAT sesi)

```text
DIBUAT:
  [x] __init__ tidak memanggil _pra_muat_model (buang crash #1)
  [x] _do_search tidak lagi memuat model dalam thread utama
  [x] _fetch_collections: worker.finished.connect(self._mula_pramuat)
      (dulu _pra_muat_model thread utama — ditukar ke PreloadWorker dalam Sesi 22)
  [x] core/semantic_search.py _load_model: local_files_only=True + fallback
  [x] core/draft_answer.py: semantic_results pra-kira (tiada semantic_search ke-2)
  [x] _tampal_gabungan hanya dari isyarat finished QThread
  [x] semak.py (semua lulus) + uji_apps.py (12/12 lulus)

BELUM SELESAI (pada TAMAT sesi):
  [ ] Pra-muat QThread background (Punca #2)

TUGAS LUAR SESI INI:
  [ ] Hantar draf DM Facebook kepada SemakHadis.com
```

> **KEMASKINI Sesi 22 (8 Ogos):** item "BELUM SELESAI" di atas kini
> **SELESAI** — lihat §6 yang dikemas kini.

---

## 6. SELESAI — Penyelesaian QThread Background (Punca #2)

**Status: SELESAI (8 Ogos 2026, Sesi 22).** Kesemua 5 langkah di bawah telah
diterapkan dan disahkan. Dokumen asal menandakannya "PENDING"; kini kod
semasa tidak lagi dalam keadaan crash yang dihuraikan di §5.

Langkah yang dilaksanakan (rujukan kod semasa):

1. **`ui/workers.py`** — `PreloadWorker(QThread)` (baris ~110): memanggil
   `_load_model()`, `_load_index()`, `_load_id_map()` dalam `run()` dan emit
   isyarat `siap(bool)`. Kegagalan tidak fatal: emit `False`, `SemanticWorker`
   boleh muat sendiri.
2. **`ui/app_qt.py` `_fetch_collections`** — `worker.finished.connect(
   self._mula_pramuat)` (baris ~472); `_mula_pramuat` mencipta dan memulakan
   `self._preload = PreloadWorker()` selepas `CollectionsWorker` selesai;
   `_on_pramuat_siap` menetapkan `self._model_sedia`.
3. **`core/semantic_search.py`** — `_model_lock = threading.Lock()` (baris ~39)
   dengan *double-checked locking* dalam `_load_model`, `_load_index` dan
   `_load_id_map`; worker kedua menunggu, tidak memuat model serentak.
4. **`_do_search`** — memulakan `SearchWorker` serta-merta; `SemanticWorker`
   menunggu `_model_lock` jika pra-muat belum siap (lock melindungi).
5. **Ujian disahkan dalam Sesi 22:**
   - `semak.py` — 135 semakan lulus (sebelumnya "semua lulus")
   - `semak_versi.py` — 20 ciri v1.1 hadir
   - `uji_data_baharu.py` (baharu) — **18/18 lulus**: carian gabungan
     keyword + semantik berjalan, model e5-small dimuat (199 lapisan),
     butiran dibuka, **aplikasi ditutup tanpa crash** (uji closeEvent
     merangkumi `PreloadWorker` yang masih berjalan — `pre.wait(2000)`)
   - Tampalan §6 asal diuji dalam sandbox (`tampalan_preload/BACA.md`):
     3/3 lulus (muat tunggal dari 8 thread, PreloadWorker dalam Qt loop,
     perlumbaan pra-muat + SemanticWorker)

### Pepijat kedua (ditemui semasa ujian tampalan) — juga dibetulkan

`closeEvent` memanggil `w.cancel()` pada SEMUA worker termasuk
`SemanticWorker` (mewarisi QThread terus, tiada `cancel()`)
→ `AttributeError` semasa Qt meruntuhkan tetingkap = fail-fast 0xC0000409.
Pembetulan: `if hasattr(w, "cancel")` + tunggu `self._preload`
(`pre.wait(2000)`) kerana ia QThread yang tidak berada dalam `_workers`.
Disahkan dalam `ui/app_qt.py` `closeEvent` (baris ~230).

---

## 7. Fail ujian (bukti eksperimen)

Semua dalam `C:\Users\MKAW\AppData\Local\Temp\opencode\`:
`uji_pre_qthread.py` (penyelesaian terbukti), `uji_cari_pantas.py` (crash
thread-utama), `uji_pra_selepas.py`, `uji_timing.py`, `uji_gabung_ui.py`,
`uji_delay.py`, `uji_nopre.py`, `uji_both.py`, `uji_kad_*.py`,
`uji_model_only.py`, `uji_komponen.py`, `uji_lfo.py`, `uji_gabung_langsung.py`,
`uji_gabung_noshow.py` (+ fail `*_out.txt` / `*_err.txt`).
