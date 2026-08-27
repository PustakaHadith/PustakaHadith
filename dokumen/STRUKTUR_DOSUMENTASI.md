# Struktur Dokumentasi — PustakaHadith

Susunan fail dokumen ikut kategori. Semua perbincangan & perubahan projek
direkodkan untuk **sejarah pembuatan projek** (lihat
`sejarah_pembangunan/LOG_PEMBANGUNAN.md`).

## Kategori

| Folder | Isi |
|--------|-----|
| `dokumen/sejarah_pembangunan/` | **Log sejarah perjalanan projek** (entry point sejarah). |
| `dokumen/surat/hadis.my/` | **Emel & surat permohonan kepada hadis.my** (API + pembundelan data), termasuk versi PDF. |
| `dokumen/surat/kebenaran/` | Surat permohonan kebenaran / lesen lain: SemakHadis, terjemahan Inggeris Musnad Ahmad. |
| `dokumen/surat/sokongan/` | Dokumen sokongan edaran Store: Dasar Privasi, Pautan Sokongan. |
| `dokumen/perbincangan/` | Rekod perbincangan teknikal (cth. bab & nombor hadis). |
| `dokumen/penerbitan/` | Persediaan edaran Store: tangkapan skrin, proses MSIX, VM capture. |
| `dokumen/perubahan/` | Log harian perubahan (`PERUBAHAN_*.md`). |
| `dokumen/sesi/` | Indeks sesi kerja (`sesi_index.md`). |
| `dokumen/rujukan/` | Panduan rujukan (daftar MSIX Store, pelan bina edaran). |
| `dokumen/manual/` | Manual pengguna & pembangun. |
| `dokumen/audit/` | Audit padanan arkib & Ahmad Digital. |

## Fail Penting di Akar `dokumen/`

- `CHECKLIST_PEMANTAUAN.md` — status Fasa 1–7 (kemaskini setiap fasa).
- `STRUKTUR_DOSUMENTASI.md` — fail ini (peta folder).

## Nota

- `PustakaHadith.spec` & `installer/PustakaHadith.iss` **di-gitignore**
  (konfig binaan tidak di-commit).
- Data `hadis.db` / indeks FAISS **tidak dibundel** ke installer sehingga
  kebenaran hadis.my diperoleh (lihat `surat/hadis.my/SURAT_HADISMY.md`).
