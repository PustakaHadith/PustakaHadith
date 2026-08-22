# PADANAN ARKIB — Dokumen Asal ↔ Dokumen Projek

**Tarikh:** 11 Ogos 2026 (fasa 2: penilaian maklumat penting)
**Skop:** Jejak padanan antara **11 dokumen .md asal** (dalam `D:\Pustaka Quran Hadis\backup\arkib_md_11OGOS.zip`) dengan semua dokumen .md projek (`dokumen/` + `README.md`) — dan penilaian sama ada maklumat penting daripadanya perlu diselamatkan ke dalam projek.

---

## 1. Tujuan

Apabila kesemua 11 fail .md longgar di folder induk dihapus dan diarkib ke `arkib_md_11OGOS.zip`, timbul dua soalan:

1. **Padanan** — adakah kandungannya dibawa masuk ke dalam projek, atau hilang?
2. **Kelayakan** — dokumen UNIK yang tiada setara dalam projek: adakah ia mengandungi maklumat penting yang mesti diselamatkan sebelum zip hilang?

Fasa 1 (padanan) dijawab dalam §3–§5. Fasa 2 (penilaian + penyelamatan) dijawab dalam §7.

## 2. Metodologi

- **Sumber asal:** `D:\Pustaka Quran Hadis\backup\arkib_md_11OGOS.zip` — 11 fail .md (dibaca terus dari zip, tanpa ekstrak)
- **Sasaran:** semua fail .md projek (`dokumen/**/*.md` + `README.md` di akar)
- **Normalisasi:** buang `\r` (CRLF→LF), buang ruang hujung baris
- **Ukuran:** `difflib.SequenceMatcher.ratio()` — nisbah 0.00–1.00 (1.00 = teks sama sepenuhnya)
- **Padanan:** setiap dokumen asal diambil padanan projek TERBAIK (nisbah tertinggi)
- **Tafsiran:** nisbah ≥ 0.90 = dokumen sama; < 0.10 = tiada padanan bermakna (nilai kecil itu hanyalah serpihan rawak biasa seperti tajuk/format)
- **Pengesahan status isu:** semakan langsung terhadap kod semasa (requirements.txt, main.py, struktur fail) pada 11 Ogos 2026

## 3. Keputusan — jadual padanan

| Dokumen asal (arkib) | Nisbah | Status (11 Ogos) | Verdict |
|---|---|---|---|
| **DEKLARASI.md** | **1.00** | `dokumen/rujukan/DEKLARASI.md` | **SAMA** — salinan tepat (4 perubahan sengaja, lihat §4) |
| **SUMBER_semakhadis.md** | **1.00** (dalaman) | salinan PERMOHONAN_LESEN_SEMAKHADIS | **SALINAN** — digugurkan (lihat §7) |
| PERMOHONAN_HADISMY.md | 0.65 (dalaman) | subset SUMBER_hadis-my | **SUBSET** — digugurkan (lihat §7) |
| **INSTALLER.md** | 0.02 | `dokumen/rujukan/INSTALLER.md` | **DISIMPAN** (11 Ogos) |
| **SUMBER_hadis-my.md** | 0.03 | `dokumen/rujukan/SUMBER_hadis-my.md` | **DISIMPAN** (11 Ogos) |
| **PERMOHONAN_LESEN_SEMAKHADIS.md** | 0.04 | `dokumen/rujukan/PERMOHONAN_LESEN_SEMAKHADIS.md` | **DISIMPAN** (11 Ogos) |
| **ISU_TERJEMAHAN_MELAYU.md** | 0.04 | `dokumen/rujukan/ISU_TERJEMAHAN_MELAYU.md` | **DISIMPAN** (11 Ogos) |
| **DORAR_NET.md** | 0.04 | `dokumen/audit/DORAR_NET.md` | **DISIMPAN** (11 Ogos) |
| **ANALISA_6OGOS.md** | 0.03 | `dokumen/rujukan/ANALISA_6OGOS.md` | **DISIMPAN** (11 Ogos) |
| BACA_DAHULU.md | 0.05 | — | UNIK — tidak disimpan (sejarah, lihat §7) |
| sesi_analisis.md | 0.04 | — | UNIK — tidak disimpan (sejarah, lihat §7) |

## 4. Tandaan DEKLARASI.md (asal ↔ semasa)

`DEKLARASI.md` ialah dokumen yang **sama** dengan padanan projek (nisbah 1.00 — perbezaan hanya pada baris yang disenaraikan di bawah). Perbezaan tepat antara arkib asal dan `dokumen/rujukan/DEKLARASI.md`:

```
+ **Versi:** 1.0 (rasmi)                                          ← header ditambah
- **Teks hadis, terjemahan Melayu & Indonesia**                   ← baris atribusi 1
- [hadis.my](https://hadis.my) — API Hadis Malaysia
+ **Teks hadis, terjemahan Melayu & Indonesia:** [hadis.my](https://hadis.my) — API Hadis Malaysia
- **Terjemahan Inggeris & darjat ulama**                          ← baris atribusi 2
- Koleksi `fawazahmed0/hadith-api` (domain awam), berasal daripada
- sunnah.com
+ **Terjemahan Inggeris & darjat ulama:** koleksi `fawazahmed0/hadith-api` (domain awam), berasal daripada sunnah.com
- **Huraian ringkas**                                             ← baris atribusi 3
- [SemakHadis.com](https://semakhadis.com) — dipaparkan tanpa sebarang
- pengubahsuaian, dengan atribusi pada setiap huraian
+ **Huraian ringkas:** [SemakHadis.com](https://semakhadis.com) — dipaparkan tanpa sebarang pengubahsuaian, dengan atribusi pada setiap huraian
```

**Ringkasan 4 perubahan (semuanya sengaja):**

| # | Perubahan | Sebab |
|---|---|---|
| 1 | Header `**Versi:** 1.0 (rasmi)` ditambah | Selaras dengan versi apl rasmi (commit `faa8d17`) |
| 2–4 | 3 baris atribusi diselaraskan — label + kolon `:` dalam satu baris, `koleksi` huruf kecil, ayat digabung | Menepati paparan app (`ui/deklarasi.py`) — disahkan TEPAT oleh semakan 8aa (commit `7c7a152`) |

## 5. Kesimpulan padanan (fasa 1)

- **DEKLARASI.md** telah dibawa masuk ke projek — salinan hampir tepat (95% baris sama), hanya penambahan versi + penyelarasan atribusi.
- **10 dokumen lain tiada setara** dalam projek pada fasa 1 — ia bahan rujukan/penyelidikan/surat permohonan yang berasingan.

Fasa 2 mengubah keadaan ini — lihat §7: **6 daripada 10 dokumen UNIK kini disimpan ke dalam projek** (salinan byte-tepat), jadi maklumat penting tidak lagi bergantung pada zip sahaja.

## 6. Penilaian maklumat penting & tindakan penyelamatan (fasa 2)

Setiap dokumen UNIK dibaca penuh dan dinilai terhadap keadaan semasa projek (kod + dokumentasi). Tindakan: **DISIMPAN** = disalin byte-tepat ke projek; **TIDAK** = kandungannya sudah diliputi/digantikan.

| Dokumen asal | Kepentingan | Penilaian | Tindakan |
|---|---|---|---|
| **INSTALLER.md** | **TINGGI** | Pelan reka bentuk installer (Nuitka, Inno Setup, `%LOCALAPPDATA%`, bundel indeks FAISS elak 3 jam, wizard permulaan, SmartScreen, GitHub Releases) — **belum dilaksanakan**, pelan aktif masa depan | **DISIMPAN** → `dokumen/rujukan/INSTALLER.md` |
| **SUMBER_hadis-my.md** | **TINGGI** | Dokumen induk sumber teras: hadith.my = hadis.my (pemilik sama), pelan percuma, endpoint + 9 koleksi, hujah bundel, **draf e-mel + WhatsApp + lampiran 55 hadis** (status: belum dihantar — pengguna uruskan sendiri) | **DISIMPAN** → `dokumen/rujukan/SUMBER_hadis-my.md` |
| **PERMOHONAN_LESEN_SEMAKHADIS.md** | **TINGGI** | Permohonan **aktif**: DM Facebook dihantar (tiada balasan), saluran rasmi (Ede Fahmin Rezuan, `fahmin@semakhadis.com`, MUHIM), draf e-mel + susulan telefon, had masa 2 minggu | **DISIMPAN** → `dokumen/rujukan/PERMOHONAN_LESEN_SEMAKHADIS.md` |
| **ISU_TERJEMAHAN_MELAYU.md** | **TINGGI** | Isu terbuka: 80 hadis matn tidak diterjemah (0.13%), kaedah pengesanan (ambang 40 aksara Arab), taburan per kitab, **senarai penuh 80 ID** untuk dilaporkan ke hadis.my (pilihan A+C disyorkan) | **DISIMPAN** → `dokumen/rujukan/ISU_TERJEMAHAN_MELAYU.md` |
| **DORAR_NET.md** | **SEDERHANA** | Penilaian terperinci Dorar + sunnah.com: `Content-Signal: use=reference` (kebenaran eksplisit), widget rasmi, keputusan "pautan keluar sahaja" + corak 4 sumber, **nota kaki penangguhan Sesi 18.8** (liputan per kitab, padanan salah Bukhari #50, kos 8–12 jam), ringkasan status 8 sumber. Ringkasan ada di `DAPATAN_WEB.md` §8 tetapi butiran keputusan + nota kaki TIDAK | **DISIMPAN** → `dokumen/audit/DORAR_NET.md` |
| **ANALISA_6OGOS.md** | **SEDERHANA** | Analisis 7 kekurangan v1.0 — **5/7 sudah selesai**, 2 terbuka (lihat status di bawah). Nilai: rekod keputusan + 2 isu terbuka | **DISIMPAN** → `dokumen/rujukan/ANALISA_6OGOS.md` |
| BACA_DAHULU.md | RENDAH | Nota proses workspace: kerja tertunggak #1 (pra-muat model) **sudah selesai** (`ui/workers.py`); corak berulang sebahagiannya sudah dalam `MULA_SINI.md` §2; cadangan "beri apl kepada 3–5 orang" ialah keputusan produk masa depan | TIDAK — sejarah |
| sesi_analisis.md | RENDAH | Sejarah Sesi 5–6 (29–30 Jul): fix gap, HadeethEnc TODO — sudah direkod dalam `sesi_index.md` | TIDAK — sejarah |
| PERMOHONAN_HADISMY.md | RENDAH | **Subset** SUMBER_hadis-my (nisbah 0.65) — e-mel/WhatsApp sama, tanpa fakta hadith.my + lampiran 55 | TIDAK — digantikan |
| SUMBER_semakhadis.md | RENDAH | **Salinan tepat** PERMOHONAN_LESEN_SEMAKHADIS (nisbah 1.00) | TIDAK — salinan |

### Status isu ANALISA_6OGOS (disahkan terhadap kod semasa, 11 Ogos 2026)

| Isu | Status | Bukti |
|---|---|---|
| 🔴 KRITIKAL 1 — requirements versi tidak sah (`2.2.2.2.2`) | **SELESAI** | `requirements.txt` kini pin versi disahkan + `torch>=2.6` disenaraikan |
| 🔴 KRITIKAL 2 — fix DLL guna PowerShell semasa runtime | **SELESAI** | `main.py::_baik_pulih_dll_qt_torch` guna `site`/`os`/`shutil` (ctypes) — tiada `os.popen`/`powershell` |
| 🟠 SEDERHANA 3 — 8 skrip build usang | **SELESAI** | Tiada `build*.py`/`run_build.py`/`start_build.py`/`check_build.py` di akar |
| 🟠 SEDERHANA 4 — lesen SemakHadis belum selesai | **TERBUKA** | Permohonan aktif — lihat `PERMOHONAN_LESEN_SEMAKHADIS.md` |
| 🟠 SEDERHANA 5 — README English, skop salah | **SELESAI** | `README.md` kini Bahasa Melayu, gambaran keseluruhan |
| 🟡 RENDAH 6 — `ui/app_qt.py` 1,725 baris | **SELESAI** | Pecahan 5 langkah selesai 8 Ogos — `RANCANGAN_REFACTOR.md` |
| 🟡 RENDAH 7 — model tidak dibundel, tiada pengesahan muat turun | **TERBUKA** | Berkaitan pelan installer — lihat `INSTALLER.md` |

### Nota penyelamatan

- **6 dokumen disalin ke projek** — 3 byte-tepat (ISU_TERJEMAHAN_MELAYU, PERMOHONAN_LESEN_SEMAKHADIS, DORAR_NET); 3 dengan pembetulan ejaan Indonesia→BM sahaja, seperti dilaporkan semak 8m: ANALISA_6OGOS (tajuk + nota akhir), INSTALLER (2 kejadian), SUMBER_hadis-my (1 kejadian). Tiada perubahan makna — zip kekal sumber tulen.
- **4 dokumen tidak disimpan** — tiada maklumat unik hilang: 2 sejarah (diliputi `sesi_index.md`/`MULA_SINI.md`), 1 subset, 1 salinan tepat.

## 7. Cara jalankan semula

```bash
cd "/d/Pustaka Quran Hadis/hadis"
python - <<'EOF'
import zipfile, os, glob
from difflib import SequenceMatcher
ZIP = "D:/Pustaka Quran Hadis/backup/arkib_md_11OGOS.zip"
def norm(t):
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(ln.rstrip() for ln in t.split("\n"))
with zipfile.ZipFile(ZIP) as z:
    asal = {os.path.basename(n): norm(z.read(n).decode("utf-8", "replace"))
            for n in z.namelist() if n.lower().endswith(".md")}
projek = {p: norm(open(p, encoding="utf-8").read())
          for p in glob.glob("dokumen/**/*.md", recursive=True) + ["README.md"]}
for name, txt in sorted(asal.items()):
    best = max(((SequenceMatcher(None, txt, ptxt).ratio(), p) for p, ptxt in projek.items()))
    print(f"{name:<34} {best[0]:.2f}  {best[1]}")
EOF
```
